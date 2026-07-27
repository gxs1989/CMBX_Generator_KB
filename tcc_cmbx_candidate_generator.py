from __future__ import annotations

import json
import zipfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path

from clone_select_generator import write_clone_select_cmbx
from cmbx_container import (
    CmbxPackage,
    _unique_output_path,
    extract_cmbx_entry,
    load_cmbx_package,
    read_cmbx_header_xml,
)
from semantic_generation import CloneSelectPlan
from tcc_project_generator import (
    build_single_point_temperature_accuracy_project,
    instrument_method_script_text,
    report_calculation_spec_text,
    report_formula_map_tsv,
    required_configuration_text,
    single_point_temperature_accuracy_project_to_dict,
)


@dataclass(frozen=True)
class TccCmbxCandidateOutputs:
    reference_cmbx: Path
    experimental_cmbx: Path
    request_cmbx: Path
    manifest: Path


def write_vh_temperature_accuracy_40c_cmbx_candidates(
    source_cmbx: str | Path,
    output_root: str | Path,
) -> TccCmbxCandidateOutputs:
    """Write CMBX candidates for the VH temperature accuracy 40C target.

    The reference CMBX keeps the original multi-point binary payload and is the
    safest package for checking Chromeleon import behavior. The experimental CMBX
    renames the visible method/report header objects to the generated 40C names,
    but the embedded sequence command payload is still the source payload.
    """
    source_package = load_cmbx_package(source_cmbx)
    output_root = Path(output_root)
    output_root.mkdir(parents=True, exist_ok=True)
    project = build_single_point_temperature_accuracy_project("VH-C10-A", 40.0)
    plan = CloneSelectPlan(
        source_package=str(source_package.path),
        family=project.family,
        device_model=project.device_model,
        report_template=project.source_report_template,
        injections=(project.injection_name,),
        instrument_methods=(project.source_method,),
        processing_methods=(project.processing_method,),
        required_capability_groups=("core_tcc", "external_thermometers"),
    )

    reference = write_clone_select_cmbx(
        source_package,
        plan,
        output_root / "VH-C10-A_temperature_accuracy_reference_multipoint.cmbx",
        sequence_name="VH-C10-A Temperature Accuracy Reference",
    )
    experimental = _write_header_alias_candidate(
        load_cmbx_package(reference),
        project.instrument_method,
        project.report_template,
        output_root / "VH-C10-A_temperature_accuracy_single_40C_header_candidate.cmbx",
    )
    request = _write_request_package(experimental, output_root)
    manifest = _write_manifest(reference, experimental, request, source_package, output_root)
    return TccCmbxCandidateOutputs(
        reference_cmbx=reference,
        experimental_cmbx=experimental,
        request_cmbx=request,
        manifest=manifest,
    )


def _write_header_alias_candidate(
    reference_package: CmbxPackage,
    method_name: str,
    report_name: str,
    output_path: Path,
) -> Path:
    source_root = ET.fromstring(read_cmbx_header_xml(reference_package.path))
    if reference_package.sequences:
        sequence_node = _find_node_by_id(source_root, reference_package.sequences[0].id)
        if sequence_node is not None:
            sequence_node.set("Name", "VH-C10-A Temperature Accuracy 40C Header Candidate")
    for node in source_root.iter("ChromeleonElement"):
        kind = _kind_for_node(node)
        if kind == "instrument_method" and _normalize_name(node.attrib.get("Name", "")) == _normalize_name("TEMPERATURE_ACCURACY"):
            node.set("Name", method_name)
            node.set("Url", _renamed_url(node.attrib.get("Url", ""), method_name))
        if kind == "report_template" and _normalize_name(node.attrib.get("Name", "")) == _normalize_name("Report_VTCC_V2_12"):
            node.set("Name", report_name)
            node.set("Url", _renamed_url(node.attrib.get("Url", ""), report_name))

    output = _unique_output_path(output_path)
    header_bytes = b'<?xml version="1.0" encoding="UTF-8"?>' + ET.tostring(source_root, encoding="utf-8")
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("header.xml", header_bytes)
        for entry in reference_package.entries:
            if entry.name == "header.xml":
                continue
            archive.writestr(entry.name, extract_cmbx_entry(reference_package.path, entry.name))
    return output


def _write_request_package(experimental_cmbx: Path, output_root: Path) -> Path:
    project = build_single_point_temperature_accuracy_project("VH-C10-A", 40.0)
    package = load_cmbx_package(experimental_cmbx)
    output = _unique_output_path(output_root / "VH-C10-A_accuracy_40C_request_package.cmbx")
    embedded_assets = {
        "CMBX_DATA_EXPLORER_GENERATION/project_spec.json": json.dumps(
            single_point_temperature_accuracy_project_to_dict(project),
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        "CMBX_DATA_EXPLORER_GENERATION/required_configuration.md": required_configuration_text(project),
        "CMBX_DATA_EXPLORER_GENERATION/method_script_40C_only.txt": instrument_method_script_text(project),
        "CMBX_DATA_EXPLORER_GENERATION/report_calculation_spec.md": report_calculation_spec_text(project),
        "CMBX_DATA_EXPLORER_GENERATION/report_formula_map_40C.tsv": report_formula_map_tsv(project),
        "CMBX_DATA_EXPLORER_GENERATION/README.md": _request_package_readme(),
    }
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        for entry in package.entries:
            archive.writestr(entry.name, extract_cmbx_entry(package.path, entry.name))
        for name, text in embedded_assets.items():
            archive.writestr(name, text.encode("utf-8"))
    return output


def _write_manifest(reference: Path, experimental: Path, request: Path, source_package: CmbxPackage, output_root: Path) -> Path:
    project = build_single_point_temperature_accuracy_project("VH-C10-A", 40.0)
    manifest = {
        "schema": "cmbx-data-explorer.tcc-cmbx-candidate-manifest.v1",
        "source_cmbx": str(source_package.path),
        "project": single_point_temperature_accuracy_project_to_dict(project),
        "outputs": {
            "reference_cmbx": str(reference),
            "experimental_cmbx": str(experimental),
            "request_cmbx": str(request),
        },
        "status": {
            "reference_cmbx": "Preserves original multi-point TEMPERATURE_ACCURACY binary payload; use this first to test Chromeleon import.",
            "experimental_cmbx": "Header names match the generated 40C project, but embedded .cmd/CpXm payload is not yet rewritten to single-point 40C.",
            "request_cmbx": "One-injection package with generated 40C config/script/report assets embedded under CMBX_DATA_EXPLORER_GENERATION; CM may ignore these extra files.",
        },
    }
    path = output_root / "VH-C10-A_temperature_accuracy_40C_candidate_manifest.json"
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def _request_package_readme() -> str:
    return "\n".join(
        [
            "# VH-C10-A Accuracy 40C Request Package",
            "",
            "This CMBX is a generated request package for:",
            "",
            "```text",
            "Device: VH-C10-A",
            "Test: Temperature Accuracy",
            "Setpoint: 40 degC only",
            "DB field: TempAcc40",
            "Report cell: Temperature Accuracy_H.XLS / Temp Accuracy / D68",
            "```",
            "",
            "The package header exposes one injection, one generated method name, one processing method, and one generated report name.",
            "",
            "Important boundary:",
            "",
            "- The embedded Chromeleon `.cmd`/CpXm binary payload has not yet been rewritten.",
            "- The generated 40C-only method script and report formula map are included as CMBX_DATA_EXPLORER_GENERATION assets.",
            "- Chromeleon may ignore these extra assets; they are included so this CMBX carries the complete request contract with the import candidate.",
            "",
            "Generated assets:",
            "",
            "- `project_spec.json`",
            "- `required_configuration.md`",
            "- `method_script_40C_only.txt`",
            "- `report_calculation_spec.md`",
            "- `report_formula_map_40C.tsv`",
        ]
    ) + "\n"


def _find_node_by_id(root: ET.Element, element_id: str) -> ET.Element | None:
    if not element_id:
        return None
    return next((node for node in root.iter("ChromeleonElement") if node.attrib.get("Id", "") == element_id), None)


def _kind_for_node(node: ET.Element) -> str:
    lowered = node.attrib.get("ItemType", "").lower()
    if "instrumentmethod" in lowered:
        return "instrument_method"
    if "processingmethod" in lowered:
        return "processing_method"
    if "reportdefinition" in lowered or "datapresentationlayout" in lowered:
        return "report_template"
    return "other"


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
