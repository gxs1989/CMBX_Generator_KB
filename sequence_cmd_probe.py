from __future__ import annotations

from dataclasses import dataclass

from cmbx_container import CmbxPackage, extract_cmbx_entry
from sequence_cmd_parser import build_injection_method_links, get_injection_method_link


@dataclass(frozen=True)
class SequenceCmdNameHit:
    name: str
    kind: str
    encoding: str
    offset: int


@dataclass(frozen=True)
class SequenceCmdHitCluster:
    start_offset: int
    end_offset: int
    hits: tuple[SequenceCmdNameHit, ...]

    @property
    def span(self) -> int:
        return self.end_offset - self.start_offset

    @property
    def names(self) -> tuple[str, ...]:
        result: list[str] = []
        seen: set[str] = set()
        for hit in self.hits:
            if hit.name in seen:
                continue
            seen.add(hit.name)
            result.append(hit.name)
        return tuple(result)


@dataclass(frozen=True)
class SequenceOrderComparison:
    row_order: int
    injection_name: str
    cmd_occurrence: int | None
    processing_method: str
    instrument_method: str


@dataclass(frozen=True)
class SequenceCmdInjectionRecordProbe:
    row_order: int
    cmd_occurrence_rank: int | None
    injection_name: str
    record_anchor: int | None
    name_field_offset: int | None
    cmd_occurrence: int | None
    processing_method: str
    instrument_method: str
    sample_id: str
    injection_type: str
    sequence_status: str
    lock_state: str
    ext_temp_preview: str


def sequence_cmd_name_hits(package: CmbxPackage) -> list[SequenceCmdNameHit]:
    if not package.sequences or not package.sequences[0].filename:
        return []
    data = extract_cmbx_entry(package.path, package.sequences[0].filename)
    names: list[tuple[str, str]] = []
    names.extend((injection.name, "injection") for injection in package.injections)
    names.extend((element.name, element.kind) for element in package.methods_and_reports)

    hits: list[SequenceCmdNameHit] = []
    for name, kind in names:
        for encoding, encoded in (
            ("utf-8", name.encode("utf-8", errors="ignore")),
            ("utf-16le", name.encode("utf-16le", errors="ignore")),
        ):
            if not encoded:
                continue
            start = 0
            while True:
                offset = data.find(encoded, start)
                if offset < 0:
                    break
                hits.append(SequenceCmdNameHit(name=name, kind=kind, encoding=encoding, offset=offset))
                start = offset + 1
    return sorted(hits, key=lambda item: (item.offset, item.name, item.encoding))


def sequence_cmd_name_hits_tsv(hits: list[SequenceCmdNameHit]) -> str:
    lines = ["Offset\tKind\tName\tEncoding"]
    for hit in hits:
        lines.append(f"{hit.offset}\t{hit.kind}\t{hit.name}\t{hit.encoding}")
    return "\n".join(lines)


def sequence_cmd_hit_clusters(hits: list[SequenceCmdNameHit], max_gap: int = 4096) -> list[SequenceCmdHitCluster]:
    if not hits:
        return []
    clusters: list[SequenceCmdHitCluster] = []
    current: list[SequenceCmdNameHit] = [hits[0]]
    for hit in hits[1:]:
        if hit.offset - current[-1].offset <= max_gap:
            current.append(hit)
            continue
        clusters.append(_cluster_from_hits(current))
        current = [hit]
    clusters.append(_cluster_from_hits(current))
    return clusters


def sequence_cmd_hit_clusters_tsv(clusters: list[SequenceCmdHitCluster]) -> str:
    lines = ["StartOffset\tEndOffset\tSpan\tHitCount\tNames"]
    for cluster in clusters:
        lines.append(
            "\t".join(
                [
                    str(cluster.start_offset),
                    str(cluster.end_offset),
                    str(cluster.span),
                    str(len(cluster.hits)),
                    ", ".join(cluster.names),
                ]
            )
        )
    return "\n".join(lines)


def sequence_cmd_injection_links_tsv(package: CmbxPackage) -> str:
    links = build_injection_method_links(package)
    lines = ["Occurrence\tInjection\tProcessingMethod\tInstrumentMethod"]
    for link in sorted(links.values(), key=lambda item: item.occurrence):
        lines.append(
            "\t".join(
                [
                    str(link.occurrence),
                    link.injection_name,
                    link.processing_method,
                    link.instrument_method,
                ]
            )
        )
    return "\n".join(lines)


def sequence_order_comparison(package: CmbxPackage) -> list[SequenceOrderComparison]:
    links = build_injection_method_links(package)
    rows: list[SequenceOrderComparison] = []
    for index, injection in enumerate(package.injections, 1):
        link = get_injection_method_link(links, injection)
        rows.append(
            SequenceOrderComparison(
                row_order=index,
                injection_name=injection.name,
                cmd_occurrence=link.occurrence if link else None,
                processing_method=link.processing_method if link else "",
                instrument_method=link.instrument_method if link else "",
            )
        )
    return rows


def sequence_order_comparison_tsv(rows: list[SequenceOrderComparison]) -> str:
    lines = ["RowOrder\tCmdOccurrence\tInjection\tProcessingMethod\tInstrumentMethod"]
    for row in rows:
        lines.append(
            "\t".join(
                [
                    str(row.row_order),
                    "" if row.cmd_occurrence is None else str(row.cmd_occurrence),
                    row.injection_name,
                    row.processing_method,
                    row.instrument_method,
                ]
            )
        )
    return "\n".join(lines)


def sequence_cmd_injection_record_probes(package: CmbxPackage) -> list[SequenceCmdInjectionRecordProbe]:
    if not package.sequences or not package.sequences[0].filename:
        return []
    data = extract_cmbx_entry(package.path, package.sequences[0].filename)
    links = build_injection_method_links(package)
    occurrence_ranks = {
        link.injection_name: index
        for index, link in enumerate(sorted(links.values(), key=lambda item: item.occurrence), 1)
    }
    rows: list[SequenceCmdInjectionRecordProbe] = []
    for row_order, injection in enumerate(package.injections, 1):
        link = get_injection_method_link(links, injection)
        if link is None:
            rows.append(
                SequenceCmdInjectionRecordProbe(
                    row_order=row_order,
                    cmd_occurrence_rank=None,
                    injection_name=injection.name,
                    record_anchor=None,
                    name_field_offset=None,
                    cmd_occurrence=None,
                    processing_method="",
                    instrument_method="",
                    sample_id="",
                    injection_type="",
                    sequence_status="",
                    lock_state="",
                    ext_temp_preview="",
                )
            )
            continue
        name_field_offset = _name_field_offset(data, link.occurrence, injection.name)
        record_anchor = _row_record_anchor(data, name_field_offset or link.occurrence)
        rows.append(
            SequenceCmdInjectionRecordProbe(
                row_order=row_order,
                cmd_occurrence_rank=occurrence_ranks.get(injection.name),
                injection_name=injection.name,
                record_anchor=record_anchor,
                name_field_offset=name_field_offset,
                cmd_occurrence=link.occurrence,
                processing_method=link.processing_method,
                instrument_method=link.instrument_method,
                sample_id=_custom_field_value_after(data, link.occurrence, "cm6_sample_id"),
                injection_type=_nearby_value(data, link.occurrence, "Unknown", 520),
                sequence_status=_nearby_value(data, link.occurrence, "Finished", 560),
                lock_state=_nearby_value(data, link.occurrence, "Unlocked", 180, before=True),
                ext_temp_preview=_length_prefixed_text_before(data, link.occurrence, 0x72, 180),
            )
        )
    return rows


def sequence_cmd_injection_record_probes_tsv(rows: list[SequenceCmdInjectionRecordProbe]) -> str:
    lines = [
        "RowOrder\tCmdOccurrenceRank\tInjection\tRecordAnchor\tNameFieldOffset\tCmdOccurrence\tProcessingMethod\tInstrumentMethod\tSampleID\tType\tStatus\tLockState\tExtTempPreview"
    ]
    for row in rows:
        lines.append(
            "\t".join(
                [
                    str(row.row_order),
                    "" if row.cmd_occurrence_rank is None else str(row.cmd_occurrence_rank),
                    row.injection_name,
                    "" if row.record_anchor is None else str(row.record_anchor),
                    "" if row.name_field_offset is None else str(row.name_field_offset),
                    "" if row.cmd_occurrence is None else str(row.cmd_occurrence),
                    row.processing_method,
                    row.instrument_method,
                    row.sample_id,
                    row.injection_type,
                    row.sequence_status,
                    row.lock_state,
                    row.ext_temp_preview,
                ]
            )
        )
    return "\n".join(lines)


def _cluster_from_hits(hits: list[SequenceCmdNameHit]) -> SequenceCmdHitCluster:
    return SequenceCmdHitCluster(
        start_offset=hits[0].offset,
        end_offset=hits[-1].offset,
        hits=tuple(hits),
    )


def _name_field_offset(data: bytes, occurrence: int, name: str) -> int | None:
    encoded = name.encode("utf-8", errors="ignore")
    if not encoded or occurrence < 3:
        return None
    if data[occurrence - 3 : occurrence - 1] == b"\xe2\x01" and data[occurrence - 1] == len(encoded):
        return occurrence - 3
    return None


def _row_record_anchor(data: bytes, name_field_offset: int) -> int | None:
    start = max(0, name_field_offset - 260)
    for offset in range(name_field_offset - 1, start - 1, -1):
        value = _read_length_prefixed_ascii(data, offset, 0x72)
        if value:
            return offset
    return None


def _custom_field_value_after(data: bytes, occurrence: int, field_name: str, window: int = 800) -> str:
    chunk = data[occurrence : min(len(data), occurrence + window)]
    field = field_name.encode("utf-8", errors="ignore")
    field_offset = chunk.find(field)
    if field_offset < 0:
        return ""
    typed_value = b"TypeString\x22"
    value_type_offset = chunk.find(typed_value, field_offset)
    if value_type_offset < 0:
        return ""
    length_offset = value_type_offset + len(typed_value)
    if length_offset >= len(chunk):
        return ""
    length = chunk[length_offset]
    value_start = length_offset + 1
    value_end = value_start + length
    if value_end > len(chunk):
        return ""
    return chunk[value_start:value_end].decode("utf-8", errors="replace")


def _nearby_value(data: bytes, occurrence: int, value: str, window: int, before: bool = False) -> str:
    encoded = value.encode("utf-8", errors="ignore")
    if before:
        chunk = data[max(0, occurrence - window) : occurrence]
    else:
        chunk = data[occurrence : min(len(data), occurrence + window)]
    return value if encoded and encoded in chunk else ""


def _length_prefixed_text_before(data: bytes, occurrence: int, tag_byte: int, window: int) -> str:
    start = max(0, occurrence - window)
    for offset in range(occurrence - 1, start - 1, -1):
        value = _read_length_prefixed_ascii(data, offset, tag_byte)
        if value:
            return value
    return ""


def _read_length_prefixed_ascii(data: bytes, offset: int, tag_byte: int) -> str:
    if offset + 2 > len(data) or data[offset] != tag_byte:
        return ""
    length = data[offset + 1]
    if length == 0 or length > 80:
        return ""
    value_start = offset + 2
    value_end = value_start + length
    if value_end > len(data):
        return ""
    raw_value = data[value_start:value_end]
    if any(byte < 32 or byte > 126 for byte in raw_value):
        return ""
    return raw_value.decode("ascii", errors="replace")
