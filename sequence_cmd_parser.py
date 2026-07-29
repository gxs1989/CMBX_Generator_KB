from __future__ import annotations

import re
import zlib
from dataclasses import dataclass

from cmbx_container import CmbxElement, CmbxPackage, element_path, extract_cmbx_entry


GZIP_MAGIC = b"\x1f\x8b\x08"


@dataclass(frozen=True)
class EmbeddedSection:
    offset: int
    kind: str
    text: str


@dataclass(frozen=True)
class EmbeddedObjectSummary:
    element_name: str
    element_kind: str
    sequence_name: str
    sequence_entry: str
    occurrences: list[int]
    strings: list[str]
    sections: list[EmbeddedSection]

    def to_text(self, max_section_chars: int = 12000) -> str:
        lines = [
            f"Name: {self.element_name}",
            f"Kind: {self.element_kind}",
            f"Sequence: {self.sequence_name}",
            f"Sequence Entry: {self.sequence_entry}",
            f"Name Occurrences In Sequence Cmd: {', '.join(str(item) for item in self.occurrences) or 'not found'}",
            "",
            "Readable Context",
            "----------------",
        ]
        lines.extend(self.strings or ["No readable context was found near this object name."])
        for index, section in enumerate(self.sections, 1):
            lines.extend(
                [
                    "",
                    f"Embedded Section {index}: {section.kind} at byte offset {section.offset}",
                    "----------------",
                    section.text[:max_section_chars],
                ]
            )
            if len(section.text) > max_section_chars:
                lines.append(f"... truncated, full section length {len(section.text)} characters")
        return "\n".join(lines)


@dataclass(frozen=True)
class InjectionMethodLink:
    injection_name: str
    processing_method: str
    instrument_method: str
    occurrence: int
    sequence_name: str = ""
    sequence_id: str = ""
    injection_id: str = ""


def build_embedded_object_summary(package: CmbxPackage, element: CmbxElement) -> EmbeddedObjectSummary:
    sequence = _sequence_for_element(package, element)
    if not sequence or not sequence.filename:
        return EmbeddedObjectSummary(element.name, element.kind, "", "", [], [], [])
    data = extract_cmbx_entry(package.path, sequence.filename)
    occurrences = _find_occurrences(data, element.name)
    strings = _extract_context_strings(data, occurrences)
    sections = _extract_nearby_gzip_sections(data, occurrences)
    return EmbeddedObjectSummary(
        element_name=element.name,
        element_kind=element.kind,
        sequence_name=sequence.name,
        sequence_entry=sequence.filename,
        occurrences=occurrences,
        strings=strings,
        sections=sections,
    )


def build_injection_method_links(package: CmbxPackage) -> dict[str, InjectionMethodLink]:
    links: dict[str, InjectionMethodLink] = {}
    name_counts: dict[str, int] = {}
    for injection in package.injections:
        name_counts[injection.name] = name_counts.get(injection.name, 0) + 1
    for sequence in package.sequences:
        if not sequence.filename:
            continue
        data = extract_cmbx_entry(package.path, sequence.filename)
        for injection in (child for child in sequence.children if child.kind == "injection"):
            occurrence, refs = _injection_reference_block(data, injection.name)
            if occurrence < 0 or len(refs) < 2:
                continue
            key = injection.name if name_counts[injection.name] == 1 else f"{sequence.id}:{injection.name}"
            links[key] = InjectionMethodLink(
                injection_name=injection.name,
                processing_method=refs[0],
                instrument_method=refs[1],
                occurrence=occurrence,
                sequence_name=sequence.name,
                sequence_id=sequence.id,
                injection_id=injection.id,
            )
    return links


def get_injection_method_link(
    links: dict[str, InjectionMethodLink],
    injection: CmbxElement | str,
) -> InjectionMethodLink | None:
    if isinstance(injection, str):
        return links.get(injection)
    parent_id = getattr(injection, "parent_id", None)
    name = getattr(injection, "name", "")
    if parent_id:
        scoped = links.get(f"{parent_id}:{name}")
        if scoped is not None:
            return scoped
    return links.get(name)


def _injection_reference_block(data: bytes, injection_name: str) -> tuple[int, list[str]]:
    needle = injection_name.encode("utf-8", errors="ignore")
    if not needle:
        return -1, []
    start = 0
    while True:
        occurrence = data.find(needle, start)
        if occurrence < 0:
            return -1, []
        refs = _relative_urls_after(data, occurrence, 1000)
        if len(refs) >= 2:
            return occurrence, refs
        start = occurrence + 1


def _sequence_for_element(package: CmbxPackage, element: CmbxElement) -> CmbxElement | None:
    for candidate in reversed(element_path(package, element)):
        if candidate.kind == "sequence":
            return candidate
    return package.sequences[0] if package.sequences else None


def _relative_urls_after(data: bytes, offset: int, window: int) -> list[str]:
    chunk = data[offset : min(len(data), offset + window)]
    refs: list[str] = []
    key = b"RelativeUrl*"
    start = 0
    while True:
        pos = chunk.find(key, start)
        if pos < 0:
            break
        length_index = pos + len(key)
        if length_index >= len(chunk):
            break
        length = chunk[length_index]
        value_start = length_index + 1
        value_end = value_start + length
        if value_end <= len(chunk):
            value = chunk[value_start:value_end].decode("utf-8", errors="replace")
            if value:
                refs.append(value)
        start = value_start
    return refs


def _find_occurrences(data: bytes, name: str) -> list[int]:
    encoded_values = {name.encode("utf-8", errors="ignore")}
    encoded_values.add(name.encode("utf-16le", errors="ignore"))
    occurrences: set[int] = set()
    for encoded in encoded_values:
        if not encoded:
            continue
        start = 0
        while True:
            pos = data.find(encoded, start)
            if pos < 0:
                break
            occurrences.add(pos)
            start = pos + 1
    return sorted(occurrences)


def _extract_context_strings(data: bytes, occurrences: list[int], radius: int = 2200) -> list[str]:
    seen: set[str] = set()
    results: list[str] = []
    for occurrence in occurrences:
        start = max(0, occurrence - radius)
        end = min(len(data), occurrence + radius)
        chunk = data[start:end]
        for match in re.finditer(rb"[ -~]{5,}", chunk):
            text = match.group().decode("latin1", errors="replace").strip()
            if not _is_interesting_string(text):
                continue
            if text in seen:
                continue
            seen.add(text)
            results.append(text)
            if len(results) >= 80:
                return results
    return results


def _is_interesting_string(text: str) -> bool:
    lowered = text.lower()
    tokens = (
        "temperature",
        "accuracy",
        "method",
        "report",
        "formula",
        "trigger",
        "rettime",
        "relativeurl",
        "chromeleon",
        "processing",
        "instrument",
        "sequence",
        "injection",
        "result",
        "condition",
        "sig_value",
    )
    return any(token in lowered for token in tokens) or len(text) >= 30


def _extract_nearby_gzip_sections(data: bytes, occurrences: list[int], search_after: int = 120000) -> list[EmbeddedSection]:
    gzip_offsets = _gzip_offsets(data)
    definition_occurrences = [
        occurrence
        for occurrence in occurrences
        if any(0 <= offset - occurrence <= 2048 for offset in gzip_offsets)
    ]
    search_occurrences = definition_occurrences or occurrences
    sections: list[EmbeddedSection] = []
    used: set[int] = set()
    for occurrence in search_occurrences:
        for offset in gzip_offsets:
            if offset in used or offset < occurrence or offset > occurrence + search_after:
                continue
            text = _decompress_gzip_text(data, offset)
            if not text:
                continue
            if text == '<CmData><ExtensibleData type="ExtensibleItemData" /></CmData>':
                continue
            used.add(offset)
            kind = "XML" if text.lstrip().startswith("<") else "text"
            sections.append(EmbeddedSection(offset=offset, kind=kind, text=text))
            if len(sections) >= 4:
                return sections
    return sections


def _gzip_offsets(data: bytes) -> list[int]:
    offsets: list[int] = []
    start = 0
    while True:
        pos = data.find(GZIP_MAGIC, start)
        if pos < 0:
            break
        offsets.append(pos)
        start = pos + 1
    return offsets


def _decompress_gzip_text(data: bytes, offset: int) -> str:
    try:
        decoded = zlib.decompress(data[offset:], 16 + zlib.MAX_WBITS)
    except zlib.error:
        return ""
    if not decoded:
        return ""
    return decoded.decode("utf-8", errors="replace").strip()
