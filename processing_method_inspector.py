from __future__ import annotations

from dataclasses import dataclass
import re
import xml.etree.ElementTree as ET

from cmbx_container import CmbxElement, CmbxPackage
from sequence_cmd_parser import build_embedded_object_summary


ACTION_TOKENS = (
    "SST/IRC",
    "Pass Actions",
    "Fail Actions",
    "IRC",
    "Intelligent",
    "Injection",
    "Stop",
    "Action",
    "Pass",
    "Fail",
)


@dataclass(frozen=True)
class ProcessingMethodEvidence:
    method_name: str
    found: bool
    sequence_name: str
    sequence_entry: str
    occurrence_count: int
    section_count: int
    root_types: tuple[str, ...]
    section_offsets: tuple[int, ...]
    action_columns: tuple[str, ...]
    tab_labels: tuple[str, ...]
    grid_summaries: tuple[str, ...]
    sst_grid_count: int
    empty_sst_grid_count: int
    row_candidate_count: int
    token_counts: tuple[tuple[str, int], ...]
    snippets: tuple[str, ...]
    status: str

    @property
    def summary(self) -> str:
        if not self.found:
            return f"{self.method_name}: processing method not found in loaded CMBX."
        columns = ", ".join(self.action_columns) or "no action columns detected"
        roots = ", ".join(self.root_types) or "no root type detected"
        grids = (
            f", grids={len(self.grid_summaries)}, sst_grids={self.sst_grid_count}, "
            f"empty_sst_grids={self.empty_sst_grid_count}, row_candidates={self.row_candidate_count}"
        )
        return (
            f"{self.method_name}: {self.section_count} XML/text section(s), "
            f"root={roots}, columns={columns}{grids}, status={self.status}"
        )

    def to_lines(self) -> tuple[str, ...]:
        lines = [
            f"Processing Method: {self.method_name}",
            f"Found: {'Yes' if self.found else 'No'}",
            f"Sequence: {self.sequence_name or '(not available)'}",
            f"Sequence Entry: {self.sequence_entry or '(not available)'}",
            f"Name Occurrences: {self.occurrence_count}",
            f"Embedded Sections: {self.section_count}",
            f"Root Types: {', '.join(self.root_types) or '(none)'}",
            f"Section Offsets: {', '.join(str(item) for item in self.section_offsets) or '(none)'}",
            f"Action Columns: {', '.join(self.action_columns) or '(none detected)'}",
            f"Relevant Tabs/Labels: {', '.join(self.tab_labels) or '(none detected)'}",
            f"Grid Summaries: {'; '.join(self.grid_summaries) or '(none detected)'}",
            f"SSTGrid Count: {self.sst_grid_count}",
            f"Empty SSTGrid Count: {self.empty_sst_grid_count}",
            f"Row Candidate Count: {self.row_candidate_count}",
            "Token Counts:",
        ]
        lines.extend(f"- {token}: {count}" for token, count in self.token_counts)
        lines.append("Evidence Snippets:")
        lines.extend(f"- {snippet}" for snippet in self.snippets or ("(none)",))
        lines.append(f"Status: {self.status}")
        return tuple(lines)


def inspect_processing_method(package: CmbxPackage, method_name: str) -> ProcessingMethodEvidence:
    element = _find_processing_method(package, method_name)
    if element is None:
        return ProcessingMethodEvidence(
            method_name=method_name,
            found=False,
            sequence_name="",
            sequence_entry="",
            occurrence_count=0,
            section_count=0,
            root_types=(),
            section_offsets=(),
            action_columns=(),
            tab_labels=(),
            grid_summaries=(),
            sst_grid_count=0,
            empty_sst_grid_count=0,
            row_candidate_count=0,
            token_counts=tuple((token, 0) for token in ACTION_TOKENS),
            snippets=(),
            status="missing - processing method object not found",
        )

    summary = build_embedded_object_summary(package, element)
    section_texts = tuple(section.text for section in summary.sections)
    combined_text = "\n".join(section_texts)
    root_types = _unique(re.findall(r"<DesignerRoot[^>]*\btype=\"([^\"]+)\"", combined_text))
    action_columns = _unique(
        value
        for value in _attribute_values(combined_text, ("HeaderText", "OriginalName", "Description"))
        if _is_action_column(value)
    )
    tab_labels = _unique(
        value
        for value in _attribute_values(combined_text, ("Text", "TextResourceKey", "Name"))
        if _is_relevant_label(value)
    )[:24]
    grid_summaries, sst_grid_count, empty_sst_grid_count, row_candidate_count = _grid_evidence(section_texts)
    token_counts = tuple((token, _count_token(combined_text, token)) for token in ACTION_TOKENS)
    snippets = _evidence_snippets(combined_text)
    has_root = "ProcessingMethodRootControl" in root_types
    has_action_columns = any(value in action_columns for value in ("Pass Actions", "Fail Actions", "PassActions", "FailActions"))
    if has_root and has_action_columns and sst_grid_count and row_candidate_count == 0:
        status = "xml evidence found - SST/IRC grid columns present but business rows absent"
    elif has_root and has_action_columns:
        status = "xml evidence found - action row semantics still open"
    elif section_texts:
        status = "embedded XML/text found - action columns incomplete"
    else:
        status = "name found but no useful embedded XML/text section extracted"
    return ProcessingMethodEvidence(
        method_name=method_name,
        found=True,
        sequence_name=summary.sequence_name,
        sequence_entry=summary.sequence_entry,
        occurrence_count=len(summary.occurrences),
        section_count=len(summary.sections),
        root_types=root_types,
        section_offsets=tuple(section.offset for section in summary.sections),
        action_columns=action_columns,
        tab_labels=tab_labels,
        grid_summaries=grid_summaries,
        sst_grid_count=sst_grid_count,
        empty_sst_grid_count=empty_sst_grid_count,
        row_candidate_count=row_candidate_count,
        token_counts=token_counts,
        snippets=snippets,
        status=status,
    )


def _find_processing_method(package: CmbxPackage, method_name: str) -> CmbxElement | None:
    normalized = _normalize_name(method_name)
    for element in package.methods_and_reports:
        if element.kind == "processing_method" and _normalize_name(element.name) == normalized:
            return element
    return None


def _attribute_values(text: str, attribute_names: tuple[str, ...]) -> tuple[str, ...]:
    values: list[str] = []
    for attribute_name in attribute_names:
        values.extend(re.findall(rf"\b{re.escape(attribute_name)}\s+value=\"([^\"]+)\"", text))
    return tuple(values)


def _is_action_column(value: str) -> bool:
    lowered = value.lower()
    return any(token in lowered for token in ("pass action", "fail action", "passactions", "failactions", "condition", "sst", "irc"))


def _is_relevant_label(value: str) -> bool:
    lowered = value.lower()
    tokens = (
        "sst",
        "irc",
        "pass",
        "fail",
        "action",
        "injection",
        "stop",
        "processing",
        "calibration",
        "chromatogram",
    )
    return any(token in lowered for token in tokens)


def _count_token(text: str, token: str) -> int:
    if not token:
        return 0
    return len(re.findall(re.escape(token), text, flags=re.IGNORECASE))


def _evidence_snippets(text: str) -> tuple[str, ...]:
    snippets: list[str] = []
    for token in ("SST/IRC", "Pass Actions", "Fail Actions", "IRC", "Injection"):
        pos = text.lower().find(token.lower())
        if pos < 0:
            continue
        start = max(0, pos - 160)
        end = min(len(text), pos + 260)
        snippet = re.sub(r"\s+", " ", text[start:end]).strip()
        if snippet and snippet not in snippets:
            snippets.append(snippet)
        if len(snippets) >= 6:
            break
    return tuple(snippets)


def _grid_evidence(section_texts: tuple[str, ...]) -> tuple[tuple[str, ...], int, int, int]:
    summaries: list[str] = []
    sst_grid_count = 0
    empty_sst_grid_count = 0
    row_candidate_count = 0
    for text in section_texts:
        try:
            root = ET.fromstring(text)
        except ET.ParseError:
            continue
        for item in root.iter():
            if item.tag != "Item":
                continue
            grid_type = item.attrib.get("type", "")
            if "Grid" not in grid_type and "SST" not in grid_type:
                continue
            if grid_type == "SSTGrid":
                sst_grid_count += 1
                if _has_empty_controls(item):
                    empty_sst_grid_count += 1
            columns = _grid_columns(item)
            row_candidates = _grid_row_candidate_count(item)
            row_candidate_count += row_candidates
            preview = ", ".join(columns[:8])
            if len(columns) > 8:
                preview += ", ..."
            empty_note = ", empty Controls" if grid_type == "SSTGrid" and _has_empty_controls(item) else ""
            summaries.append(f"{grid_type}: {len(columns)} column(s) [{preview}], row candidates={row_candidates}{empty_note}")
    return _unique(summaries), sst_grid_count, empty_sst_grid_count, row_candidate_count


def _grid_columns(grid_item: ET.Element) -> tuple[str, ...]:
    columns: list[str] = []
    for column in grid_item.iter("IColumnVisibilityManagement"):
        header = _child_value(column, "HeaderText")
        original = _child_value(column, "OriginalName")
        description = _child_value(column, "Description")
        label = header or original or description
        if label:
            columns.append(label)
    return _unique(columns)


def _has_empty_controls(item: ET.Element) -> bool:
    controls = item.find("Controls")
    return controls is not None and len(list(controls)) == 0


def _grid_row_candidate_count(grid_item: ET.Element) -> int:
    count = 0
    for node in grid_item.iter():
        if node is grid_item:
            continue
        tag = node.tag.lower()
        node_type = node.attrib.get("type", "").lower()
        if tag in {"row", "datarow", "gridrow"} or node_type in {"row", "datarow", "gridrow"}:
            count += 1
            continue
        if tag == "item" and any(child.tag.lower() in {"cells", "cell"} for child in node):
            count += 1
    return count


def _child_value(parent: ET.Element, child_tag: str) -> str:
    child = parent.find(child_tag)
    if child is None:
        return ""
    return child.attrib.get("value", "").strip()


def _unique(values: tuple[str, ...] | list[str]) -> tuple[str, ...]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        cleaned = value.strip()
        if not cleaned or cleaned in seen:
            continue
        seen.add(cleaned)
        result.append(cleaned)
    return tuple(result)


def _normalize_name(value: str) -> str:
    return re.sub(r"[\s_]+", "", value or "").lower()
