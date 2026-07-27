from __future__ import annotations

import zipfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path

from cmbx_container import (
    CmbxPackage,
    _unique_output_path,
    extract_cmbx_entry,
    load_cmbx_package,
    read_cmbx_header_xml,
    safe_filename,
)
from semantic_generation import CloneSelectPlan


@dataclass(frozen=True)
class CloneSelectCandidateValidation:
    missing_header_injections: tuple[str, ...]
    missing_header_instrument_methods: tuple[str, ...]
    missing_header_processing_methods: tuple[str, ...]
    missing_header_report_templates: tuple[str, ...]
    unexpected_header_injections: tuple[str, ...]
    unexpected_header_instrument_methods: tuple[str, ...]
    unexpected_header_processing_methods: tuple[str, ...]
    unexpected_header_report_templates: tuple[str, ...]
    stale_sequence_cmd_references: tuple[str, ...]

    @property
    def header_passed(self) -> bool:
        return not (
            self.missing_header_injections
            or self.missing_header_instrument_methods
            or self.missing_header_processing_methods
            or self.missing_header_report_templates
            or self.unexpected_header_injections
            or self.unexpected_header_instrument_methods
            or self.unexpected_header_processing_methods
            or self.unexpected_header_report_templates
        )

    @property
    def command_payload_passed(self) -> bool:
        return not self.stale_sequence_cmd_references

    @property
    def passed(self) -> bool:
        return self.header_passed and self.command_payload_passed


def write_clone_select_cmbx(
    package: CmbxPackage,
    plan: CloneSelectPlan,
    output_path: str | Path,
    sequence_name: str | None = None,
) -> Path:
    """Write a shallow clone-and-select candidate CMBX.

    This preserves the original sequence command payload and raw data payloads, but filters
    header.xml to the selected injections, methods, processing methods, and report template.
    It is intended as a structural generator prototype before direct Chromeleon binary writing.
    """
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output = _unique_output_path(output)

    source_root = ET.fromstring(read_cmbx_header_xml(package.path))
    source_sequence = _find_source_sequence_node(source_root, plan)
    if source_sequence is None:
        raise ValueError("Could not find a source sequence matching the clone-select plan.")

    selected_sequence = _clone_selected_sequence_node(source_sequence, plan, sequence_name)
    header_root = ET.Element(source_root.tag, source_root.attrib)
    header_root.append(selected_sequence)
    header_bytes = b'<?xml version="1.0" encoding="UTF-8"?>' + ET.tostring(header_root, encoding="utf-8")

    entry_names = {entry.name for entry in package.entries}
    required_entries = _entry_names_for_selected_header(selected_sequence)
    sequence_entry = source_sequence.attrib.get("Filename", "")
    if sequence_entry:
        required_entries.insert(0, sequence_entry)

    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("header.xml", header_bytes)
        for entry_name in _unique_nonempty(required_entries):
            if entry_name in entry_names:
                archive.writestr(entry_name, extract_cmbx_entry(package.path, entry_name))
    return output


def default_clone_select_output_path(plan: CloneSelectPlan, output_folder: str | Path) -> Path:
    stem = safe_filename(f"{plan.device_model}_{Path(plan.source_package).stem}_candidate", "candidate")
    return Path(output_folder) / f"{stem}.cmbx"


def validate_clone_select_candidate(
    candidate: CmbxPackage,
    plan: CloneSelectPlan,
    source_package: CmbxPackage | None = None,
) -> CloneSelectCandidateValidation:
    expected_injections = tuple(plan.injections)
    expected_methods = tuple(plan.instrument_methods)
    expected_processing = tuple(plan.processing_methods)
    expected_reports = (plan.report_template,)

    actual_injections = tuple(injection.name for injection in candidate.injections)
    actual_methods = tuple(element.name for element in candidate.methods_and_reports if element.kind == "instrument_method")
    actual_processing = tuple(element.name for element in candidate.methods_and_reports if element.kind == "processing_method")
    actual_reports = tuple(element.name for element in candidate.methods_and_reports if element.kind == "report_template")

    stale_refs = _stale_sequence_cmd_references(candidate, plan, source_package) if source_package else ()
    return CloneSelectCandidateValidation(
        missing_header_injections=_missing(expected_injections, actual_injections),
        missing_header_instrument_methods=_missing(expected_methods, actual_methods),
        missing_header_processing_methods=_missing(expected_processing, actual_processing),
        missing_header_report_templates=_missing(expected_reports, actual_reports),
        unexpected_header_injections=_unexpected(actual_injections, expected_injections),
        unexpected_header_instrument_methods=_unexpected(actual_methods, expected_methods),
        unexpected_header_processing_methods=_unexpected(actual_processing, expected_processing),
        unexpected_header_report_templates=_unexpected(actual_reports, expected_reports),
        stale_sequence_cmd_references=stale_refs,
    )


def clone_select_candidate_validation_text(validation: CloneSelectCandidateValidation) -> str:
    return "\n".join(
        [
            f"Passed: {validation.passed}",
            f"Header Passed: {validation.header_passed}",
            f"Command Payload Passed: {validation.command_payload_passed}",
            f"Missing Header Injections: {', '.join(validation.missing_header_injections) or '(none)'}",
            f"Missing Header Instrument Methods: {', '.join(validation.missing_header_instrument_methods) or '(none)'}",
            f"Missing Header Processing Methods: {', '.join(validation.missing_header_processing_methods) or '(none)'}",
            f"Missing Header Report Templates: {', '.join(validation.missing_header_report_templates) or '(none)'}",
            f"Unexpected Header Injections: {', '.join(validation.unexpected_header_injections) or '(none)'}",
            f"Unexpected Header Instrument Methods: {', '.join(validation.unexpected_header_instrument_methods) or '(none)'}",
            f"Unexpected Header Processing Methods: {', '.join(validation.unexpected_header_processing_methods) or '(none)'}",
            f"Unexpected Header Report Templates: {', '.join(validation.unexpected_header_report_templates) or '(none)'}",
            f"Stale Sequence Cmd References: {', '.join(validation.stale_sequence_cmd_references) or '(none)'}",
        ]
    )


def _find_source_sequence_node(source_root: ET.Element, plan: CloneSelectPlan) -> ET.Element | None:
    selected_injections = {_normalize_name(name) for name in plan.injections}
    best: tuple[int, ET.Element] | None = None
    for sequence in source_root.iter("ChromeleonElement"):
        if _kind_for_node(sequence) != "sequence":
            continue
        injection_names = {
            _normalize_name(child.attrib.get("Name", ""))
            for child in sequence
            if child.tag == "ChromeleonElement" and _kind_for_node(child) == "injection"
        }
        score = len(selected_injections & injection_names)
        if score and (best is None or score > best[0]):
            best = (score, sequence)
    return best[1] if best else None


def _clone_selected_sequence_node(source_sequence: ET.Element, plan: CloneSelectPlan, sequence_name: str | None) -> ET.Element:
    selected_injections = {_normalize_name(name) for name in plan.injections}
    selected_methods = {_normalize_name(name) for name in plan.instrument_methods}
    selected_processing = {_normalize_name(name) for name in plan.processing_methods}
    selected_reports = {_normalize_name(plan.report_template)}

    sequence = ET.Element(source_sequence.tag, source_sequence.attrib)
    if sequence_name:
        sequence.set("Name", sequence_name)

    for child in source_sequence:
        if child.tag != "ChromeleonElement":
            continue
        name = _normalize_name(child.attrib.get("Name", ""))
        kind = _kind_for_node(child)
        keep = (
            kind == "injection" and name in selected_injections
            or kind == "instrument_method" and name in selected_methods
            or kind == "processing_method" and name in selected_processing
            or kind == "report_template" and name in selected_reports
        )
        if keep:
            sequence.append(ET.fromstring(ET.tostring(child, encoding="utf-8")))
    return sequence


def _entry_names_for_selected_header(node: ET.Element) -> list[str]:
    names: list[str] = []
    for child in node.iter("ChromeleonElement"):
        for attr_name in ("RawDataFilename", "Filename"):
            entry_name = child.attrib.get(attr_name, "")
            if entry_name:
                names.append(entry_name)
    return names


def _unique_nonempty(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if not value or value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def _kind_for_node(node: ET.Element) -> str:
    lowered = node.attrib.get("ItemType", "").lower()
    if "subfolder" in lowered or lowered.endswith(".folder") or "data.folder" in lowered:
        return "folder"
    if "sequencefolder" in lowered or "sequence.folder" in lowered:
        return "folder"
    if "sequence" in lowered:
        return "sequence"
    if "injection" in lowered:
        return "injection"
    if "signal" in lowered:
        return "signal"
    if "audittrail" in lowered:
        return "audit"
    if "instrumentmethod" in lowered:
        return "instrument_method"
    if "processingmethod" in lowered:
        return "processing_method"
    if "reportdefinition" in lowered or "datapresentationlayout" in lowered:
        return "report_template"
    return "other"


def _normalize_name(value: str) -> str:
    return "".join(char.lower() for char in value if char.isalnum())


def load_generated_clone(path: str | Path) -> CmbxPackage:
    return load_cmbx_package(path)


def _missing(expected: tuple[str, ...], actual: tuple[str, ...]) -> tuple[str, ...]:
    actual_normalized = {_normalize_name(value) for value in actual}
    return tuple(value for value in expected if _normalize_name(value) not in actual_normalized)


def _unexpected(actual: tuple[str, ...], expected: tuple[str, ...]) -> tuple[str, ...]:
    expected_normalized = {_normalize_name(value) for value in expected}
    return tuple(value for value in actual if _normalize_name(value) not in expected_normalized)


def _stale_sequence_cmd_references(
    candidate: CmbxPackage,
    plan: CloneSelectPlan,
    source_package: CmbxPackage | None,
) -> tuple[str, ...]:
    if not candidate.sequences or not candidate.sequences[0].filename or source_package is None:
        return ()
    data = extract_cmbx_entry(candidate.path, candidate.sequences[0].filename)
    allowed = {
        *(_normalize_name(value) for value in plan.injections),
        *(_normalize_name(value) for value in plan.instrument_methods),
        *(_normalize_name(value) for value in plan.processing_methods),
        _normalize_name(plan.report_template),
    }
    source_names = [
        *(injection.name for injection in source_package.injections),
        *(
            element.name
            for element in source_package.methods_and_reports
            if element.kind in {"instrument_method", "processing_method", "report_template"}
        ),
    ]
    stale: list[str] = []
    seen: set[str] = set()
    for name in source_names:
        normalized = _normalize_name(name)
        if not normalized or normalized in allowed or normalized in seen:
            continue
        if _sequence_cmd_contains_name(data, name):
            stale.append(name)
            seen.add(normalized)
    return tuple(stale)


def _sequence_cmd_contains_name(data: bytes, name: str) -> bool:
    encoded_values = (
        name.encode("utf-8", errors="ignore"),
        name.encode("utf-16le", errors="ignore"),
    )
    return any(encoded and encoded in data for encoded in encoded_values)
