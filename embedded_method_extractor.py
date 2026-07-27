from __future__ import annotations

import re
from dataclasses import dataclass

from cmbx_container import CmbxElement, CmbxPackage, element_path, extract_cmbx_entry


METHOD_HEADER_MARKER = b"\xca\x01"


@dataclass(frozen=True)
class EmbeddedMethodBlock:
    element_name: str
    sequence_name: str
    sequence_entry: str
    start: int
    end: int
    data: bytes
    method_payload: bytes
    cpxm_payload: bytes
    payload_start: int
    payload_end: int
    cpxm_start: int
    cpxm_end: int
    strings: list[str]

    @property
    def size(self) -> int:
        return len(self.data)

    def metadata_text(self) -> str:
        lines = [
            f"Name: {self.element_name}",
            "Kind: embedded_instrument_method",
            f"Sequence: {self.sequence_name}",
            f"Sequence Entry: {self.sequence_entry}",
            f"Byte Range: {self.start}..{self.end}",
            f"Size: {self.size} bytes",
            f"Method Payload Range: {self.payload_start}..{self.payload_end}",
            f"Method Payload Size: {len(self.method_payload)} bytes",
            f"CpXm Payload Range: {self.cpxm_start}..{self.cpxm_end}",
            f"CpXm Payload Size: {len(self.cpxm_payload)} bytes",
            "",
            "Note",
            "----",
            "This file is the embedded Chromeleon instrument method block extracted from the CMBX sequence command object.",
            "It is not generated from an external TXT export. The binary format is Chromeleon-specific.",
            "The CpXm payload is exported separately because it appears to contain the Chromeleon-specific method body.",
            "",
            "Readable Strings In Block",
            "-------------------------",
        ]
        lines.extend(self.strings or ["No readable strings were found in the embedded block."])
        return "\n".join(lines)


def extract_embedded_instrument_method(package: CmbxPackage, element: CmbxElement) -> EmbeddedMethodBlock | None:
    if element.kind != "instrument_method":
        return None
    sequence = _sequence_for_method(package, element)
    if not sequence or not sequence.filename:
        return None
    data = extract_cmbx_entry(package.path, sequence.filename)
    definitions = _instrument_method_definitions(package, data)
    current = definitions.get(element.name)
    if not current:
        return None
    payload = _extract_payload_for_definition(data, current)
    if not payload:
        return None
    block_start = current if payload.source_start == current else payload.method_payload_start
    block = data[block_start:payload.end]
    return EmbeddedMethodBlock(
        element_name=element.name,
        sequence_name=sequence.name,
        sequence_entry=sequence.filename,
        start=block_start,
        end=payload.end,
        data=block,
        method_payload=payload.method_payload,
        cpxm_payload=payload.cpxm_payload,
        payload_start=payload.method_payload_start,
        payload_end=payload.method_payload_end,
        cpxm_start=payload.cpxm_payload_start,
        cpxm_end=payload.cpxm_payload_end,
        strings=_extract_readable_strings(block),
    )


def _sequence_for_method(package: CmbxPackage, element: CmbxElement) -> CmbxElement | None:
    path = element_path(package, element)
    sequence = next((part for part in path if part.kind == "sequence"), None)
    if sequence:
        return sequence
    return package.sequences[0] if package.sequences else None


def _instrument_method_definitions(package: CmbxPackage, data: bytes) -> dict[str, int]:
    definitions: dict[str, int] = {}
    for method in package.methods_and_reports:
        if method.kind != "instrument_method":
            continue
        method_name = method.name.encode("utf-8", errors="ignore")
        candidates: list[int] = []
        for occurrence in _all_occurrences(data, method_name):
            if not _is_method_definition_name(data, occurrence, method_name):
                continue
            start = _find_header_start(data, occurrence)
            if start < 0 or start in candidates:
                continue
            payload = _extract_payload_for_definition(data, start)
            if payload and (occurrence <= payload.end or payload.end == start):
                candidates.append(start)
        if candidates:
            definitions[method.name] = candidates[-1]
    return definitions


def _all_occurrences(data: bytes, needle: bytes) -> list[int]:
    if not needle:
        return []
    start = 0
    positions: list[int] = []
    while True:
        pos = data.find(needle, start)
        if pos < 0:
            return positions
        positions.append(pos)
        start = pos + 1


def _is_method_definition_name(data: bytes, occurrence: int, method_name: bytes) -> bool:
    if occurrence < 3 or len(method_name) >= 128:
        return False
    return data[occurrence - 3 : occurrence - 1] == b"\xe2\x01" and data[occurrence - 1] == len(method_name)


def _find_header_start(data: bytes, name_offset: int) -> int:
    search_start = max(0, name_offset - 256)
    pos = data.rfind(METHOD_HEADER_MARKER, search_start, name_offset)
    return pos


@dataclass(frozen=True)
class _PayloadParts:
    source_start: int
    end: int
    method_payload: bytes
    cpxm_payload: bytes
    method_payload_start: int
    method_payload_end: int
    cpxm_payload_start: int
    cpxm_payload_end: int


def _extract_method_payload(data: bytes, start: int) -> _PayloadParts | None:
    pos = start
    while pos < len(data):
        field_start = pos
        try:
            tag, pos = _read_varint(data, pos)
        except ValueError:
            return None
        field_number = tag >> 3
        wire_type = tag & 7
        if wire_type == 0:
            try:
                _value, pos = _read_varint(data, pos)
            except ValueError:
                return None
        elif wire_type == 1:
            pos += 8
        elif wire_type == 2:
            try:
                length, pos = _read_varint(data, pos)
            except ValueError:
                return None
            value_start = pos
            value_end = value_start + length
            if value_end > len(data):
                return None
            if field_number == 19:
                return _extract_field19_payload(data, start, field_start, value_start, value_end)
            pos = value_end
        elif wire_type == 5:
            pos += 4
        else:
            return None
    return None


def _extract_payload_for_definition(data: bytes, definition_start: int) -> _PayloadParts | None:
    search_end = definition_start
    checked = 0
    while checked < 1000:
        candidate = data.rfind(METHOD_HEADER_MARKER, 0, search_end)
        if candidate < 0:
            break
        checked += 1
        payload = _extract_method_payload(data, candidate)
        if payload and payload.end == definition_start:
            return payload
        search_end = candidate
    return _extract_method_payload(data, definition_start)


def _extract_field19_payload(data: bytes, source_start: int, field19_start: int, value_start: int, value_end: int) -> _PayloadParts | None:
    pos = value_start
    while pos < value_end:
        nested_start = pos
        try:
            tag, pos = _read_varint(data, pos)
            field_number = tag >> 3
            wire_type = tag & 7
            if wire_type != 2:
                return None
            length, pos = _read_varint(data, pos)
        except ValueError:
            return None
        nested_value_start = pos
        nested_value_end = nested_value_start + length
        if nested_value_end > value_end:
            return None
        if field_number == 11:
            method_payload = data[nested_value_start:nested_value_end]
            cpxm_start, cpxm_end, cpxm_payload = _extract_cpxm_payload(data, nested_value_start, nested_value_end)
            return _PayloadParts(
                source_start=source_start,
                end=nested_value_end,
                method_payload=method_payload,
                cpxm_payload=cpxm_payload,
                method_payload_start=nested_value_start,
                method_payload_end=nested_value_end,
                cpxm_payload_start=cpxm_start,
                cpxm_payload_end=cpxm_end,
            )
        pos = nested_value_end
    return None


def _extract_cpxm_payload(data: bytes, payload_start: int, payload_end: int) -> tuple[int, int, bytes]:
    pos = payload_start
    while pos < payload_end:
        try:
            tag, pos = _read_varint(data, pos)
            field_number = tag >> 3
            wire_type = tag & 7
        except ValueError:
            break
        if wire_type == 0:
            try:
                _value, pos = _read_varint(data, pos)
            except ValueError:
                break
        elif wire_type == 2:
            try:
                length, pos = _read_varint(data, pos)
            except ValueError:
                break
            value_start = pos
            value_end = value_start + length
            if value_end > payload_end:
                break
            if field_number == 3:
                return value_start, value_end, data[value_start:value_end]
            pos = value_end
        elif wire_type == 1:
            pos += 8
        elif wire_type == 5:
            pos += 4
        else:
            break
    return payload_start, payload_end, data[payload_start:payload_end]


def _read_varint(data: bytes, offset: int) -> tuple[int, int]:
    value = 0
    shift = 0
    pos = offset
    while pos < len(data):
        byte = data[pos]
        pos += 1
        value |= (byte & 0x7F) << shift
        if not byte & 0x80:
            return value, pos
        shift += 7
        if shift > 63:
            break
    raise ValueError(f"Invalid varint at byte offset {offset}")


def _extract_readable_strings(data: bytes) -> list[str]:
    strings: list[str] = []
    seen: set[str] = set()
    for match in re.finditer(rb"[ -~]{4,}", data):
        text = match.group().decode("latin1", errors="replace").strip()
        if text in seen:
            continue
        seen.add(text)
        strings.append(text)
        if len(strings) >= 120:
            break
    return strings
