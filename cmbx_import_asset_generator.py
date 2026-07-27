from __future__ import annotations

import zipfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path

from cmbx_container import (
    CmbxPackage,
    CmbxElement,
    _unique_output_path,
    extract_cmbx_entry,
    load_cmbx_package,
    read_cmbx_header_xml,
    safe_filename,
)


@dataclass(frozen=True)
class ImportAssetValidation:
    path: Path
    sequence_count: int
    instrument_methods: tuple[str, ...]
    report_templates: tuple[str, ...]
    processing_methods: tuple[str, ...]
    entries: tuple[str, ...]

    @property
    def has_sequence_payload(self) -> bool:
        return any(entry.lower().endswith(".cmd") for entry in self.entries)


def write_import_asset_candidate(
    package: CmbxPackage,
    element_name: str,
    output_path: str | Path,
    asset_name: str | None = None,
) -> Path:
    """Write a minimal CMBX candidate exposing one embedded method or report.

    Chromeleon method/report objects in observed CMBX files are embedded in the
    sequence command payload, so this writer keeps the source sequence .cmd entry
    and filters header.xml to a single visible asset element.
    """
    element = _find_asset_element(package, element_name)
    sequence = _sequence_for_asset(package, element)
    if not sequence or not sequence.filename:
        raise ValueError(f"Could not find the sequence command payload for {element_name}.")

    source_root = ET.fromstring(read_cmbx_header_xml(package.path))
    source_sequence = _find_node_by_id(source_root, sequence.id)
    source_element = _find_node_by_id(source_root, element.id)
    if source_sequence is None or source_element is None:
        raise ValueError(f"Could not find header nodes for {element_name}.")

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output = _unique_output_path(output)

    selected_sequence = ET.Element(source_sequence.tag, source_sequence.attrib)
    selected_asset = ET.fromstring(ET.tostring(source_element, encoding="utf-8"))
    if asset_name:
        selected_asset.set("Name", asset_name)
        selected_asset.set("Url", _renamed_url(selected_asset.attrib.get("Url", ""), asset_name))
    selected_sequence.append(selected_asset)

    header_root = ET.Element(source_root.tag, source_root.attrib)
    header_root.append(selected_sequence)
    header_bytes = b'<?xml version="1.0" encoding="UTF-8"?>' + ET.tostring(header_root, encoding="utf-8")

    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("header.xml", header_bytes)
        archive.writestr(sequence.filename, extract_cmbx_entry(package.path, sequence.filename))
    return output


def default_import_asset_output_path(
    package: CmbxPackage,
    element_name: str,
    output_folder: str | Path,
    suffix: str = "import_candidate",
) -> Path:
    stem = safe_filename(f"{package.path.stem}_{element_name}_{suffix}", "import_candidate")
    return Path(output_folder) / f"{stem}.cmbx"


def validate_import_asset_candidate(path: str | Path) -> ImportAssetValidation:
    package = load_cmbx_package(path)
    return ImportAssetValidation(
        path=Path(path),
        sequence_count=len(package.sequences),
        instrument_methods=tuple(element.name for element in package.methods_and_reports if element.kind == "instrument_method"),
        report_templates=tuple(element.name for element in package.methods_and_reports if element.kind == "report_template"),
        processing_methods=tuple(element.name for element in package.methods_and_reports if element.kind == "processing_method"),
        entries=tuple(entry.name for entry in package.entries),
    )


def import_asset_validation_text(validation: ImportAssetValidation) -> str:
    return "\n".join(
        [
            f"Path: {validation.path}",
            f"Sequences: {validation.sequence_count}",
            f"Instrument Methods: {', '.join(validation.instrument_methods) or '(none)'}",
            f"Report Templates: {', '.join(validation.report_templates) or '(none)'}",
            f"Processing Methods: {', '.join(validation.processing_methods) or '(none)'}",
            f"Has Sequence Cmd Payload: {validation.has_sequence_payload}",
            f"Entries: {', '.join(validation.entries)}",
        ]
    )


def _find_asset_element(package: CmbxPackage, element_name: str) -> CmbxElement:
    normalized = _normalize_name(element_name)
    for element in package.methods_and_reports:
        if _normalize_name(element.name) == normalized:
            return element
    raise KeyError(f"Method/report element was not found: {element_name}")


def _sequence_for_asset(package: CmbxPackage, element: CmbxElement) -> CmbxElement | None:
    if element.parent_id:
        parent = package.elements_by_id.get(element.parent_id)
        if parent and parent.kind == "sequence":
            return parent
    for sequence in package.sequences:
        if any(child.id == element.id for child in sequence.children):
            return sequence
    return package.sequences[0] if package.sequences else None


def _find_node_by_id(root: ET.Element, element_id: str) -> ET.Element | None:
    if not element_id:
        return None
    return next((node for node in root.iter("ChromeleonElement") if node.attrib.get("Id", "") == element_id), None)


def _renamed_url(url: str, asset_name: str) -> str:
    if not url or "/" not in url:
        return url
    prefix, old_name = url.rsplit("/", 1)
    if "." not in old_name:
        return f"{prefix}/{asset_name}"
    _stem, extension = old_name.rsplit(".", 1)
    return f"{prefix}/{asset_name}.{extension}"


def _normalize_name(value: str) -> str:
    return "".join(char.lower() for char in value if char.isalnum())
