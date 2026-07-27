from __future__ import annotations

"""Compile report-template Markdown into a standalone report CMBX.

V0.2 keeps the legacy clone-and-patch path. V1 creates a new logical workbook
and report sheets inside an internal, serialization-safe carrier.
"""

from dataclasses import dataclass, field
import ast
import copy
import json
import re
import tempfile
import uuid
from pathlib import Path
import xml.etree.ElementTree as ET

from cmbx_container import CmbxPackage, load_cmbx_package
from embedded_report_extractor import decode_report_template_xml, parse_report_sheet_objects, parse_report_sheets
from formulaone_workbook_writer import (
    FormulaOneSheetSpec,
    FormulaOneWorkbookPatch,
    create_formulaone_workbook,
    write_formulaone_existing_cells,
)
from formulaone_report_exporter import extract_formulaone_spreadsheet_data
from tools.repack_standalone_report_cmbx import repack_standalone_report_cmbx


@dataclass(frozen=True)
class ReportFormulaPatch:
    sheet_name: str
    excel_range: str
    object_type: str
    operation: str
    formula: str
    fixed_channel: str
    fixed_component: str
    style: str = ""
    number_format: str = ""


@dataclass(frozen=True)
class WorkbookCellPatch:
    sheet_name: str
    excel_range: str
    value_type: str
    value: object
    operation: str = "replace"
    style: str = ""
    number_format: str = ""


@dataclass(frozen=True)
class ReportSheetSpec:
    name: str
    column_widths: tuple[tuple[int, float], ...] = ()
    row_heights: tuple[tuple[int, float], ...] = ()
    is_active: bool = True
    each_injection: bool = True


@dataclass(frozen=True)
class ReportTableColumnSpec:
    name: str
    formula: str
    header: str
    unit: str = ""
    channel: str = ""
    component: str = ""
    number_format: str = ""


@dataclass(frozen=True)
class DynamicReportTableSpec:
    sheet_name: str
    excel_range: str
    operation: str
    table_type: str
    body_rows: int = 2
    columns: tuple[ReportTableColumnSpec, ...] = ()
    audit_level: str = "Expert"
    show_run: bool = True
    show_preconditions: bool = False
    show_day_time: bool = True
    day_time_format: str = "hh:mm:ss"
    show_device: bool = False
    show_unknown: bool = True
    show_standard: bool = True
    show_validation: bool = True
    show_matrix: bool = True
    show_blank: bool = True
    show_spiked: bool = True
    show_unspiked: bool = True
    sort_formula: str = "injection.number"
    fixed_channel: str = ""
    requires_processing: bool = False
    processing_method: str = ""
    include_identified_peaks: bool = True
    include_unidentified_peaks: bool = True


@dataclass(frozen=True)
class ReportTemplateMdSpec:
    path: Path
    template_name: str
    reference_cmbx: str
    reference_template_name: str
    generation_mode: str
    workbook_policy: str
    patches: tuple[ReportFormulaPatch, ...]
    workbook_patches: tuple[WorkbookCellPatch, ...] = ()
    workbook_requests: tuple[str, ...] = ()
    sheets: tuple[ReportSheetSpec, ...] = ()
    dynamic_tables: tuple[DynamicReportTableSpec, ...] = ()
    errors: tuple[str, ...] = ()


@dataclass
class ReportTemplateCompileResult:
    spec: ReportTemplateMdSpec
    source_cmbx: Path | None
    source_report_name: str = ""
    sheets: tuple[str, ...] = ()
    applied_patches: tuple[ReportFormulaPatch, ...] = ()
    applied_workbook_patches: tuple[WorkbookCellPatch, ...] = ()
    applied_dynamic_tables: tuple[DynamicReportTableSpec, ...] = ()
    preserved_report_tables: tuple[tuple[str, str, str], ...] = ()
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    xml_text: str = ""

    @property
    def ready(self) -> bool:
        return bool(self.source_cmbx and self.xml_text and not self.errors)


_FRONT_MATTER_RE = re.compile(r"\A\s*---\s*\r?\n(.*?)\r?\n---\s*(?:\r?\n|\Z)", re.S)
_SHEET_RE = re.compile(r"^##\s+Sheet:\s*(.+?)\s*$", re.M | re.I)
_FORMULA_RE = re.compile(r"^###\s+CM Formula:\s*([^\r\n]+)\s*\r?\n\s*```yaml\s*\r?\n(.*?)\r?\n```", re.M | re.I | re.S)
_WORKBOOK_CELL_RE = re.compile(r"^###\s+Workbook\s+(Value|Text|Formula):\s*([^\r\n]+)\s*\r?\n\s*```yaml\s*\r?\n(.*?)\r?\n```", re.M | re.I | re.S)
_WORKBOOK_RE = re.compile(r"^###\s+Workbook Change Request:\s*([^\r\n]+)", re.M | re.I)
_SHEET_SETTINGS_RE = re.compile(r"^###\s+Sheet Settings\s*\r?\n\s*```yaml\s*\r?\n(.*?)\r?\n```", re.M | re.I | re.S)
_DYNAMIC_TABLE_RE = re.compile(r"^###\s+Dynamic Table:\s*([^\r\n]+)\s*\r?\n\s*```yaml\s*\r?\n(.*?)\r?\n```", re.M | re.I | re.S)
_TABLE_COLUMN_RE = re.compile(r"^####\s+Table Column:\s*([^\r\n]+)\s*\r?\n\s*```yaml\s*\r?\n(.*?)\r?\n```", re.M | re.I | re.S)
_DEFAULT_BLANK_CARRIER = Path(
    r"C:\ProgramData\CMBX Data Explorer Workspace\KB\Method Script Generator\TCC\report_template_cmbx\PressureEvaluation_changed.cmbx"
)
_REPORT_TABLE_SKELETONS = Path(__file__).resolve().parent / "assets" / "report_table_skeletons.json"


def parse_report_template_md(path: Path) -> ReportTemplateMdSpec:
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    match = _FRONT_MATTER_RE.search(text)
    if not match:
        return ReportTemplateMdSpec(path, "", "", "", "", "", (), errors=("Missing YAML front matter delimited by ---.",))
    front = _parse_yaml_like(match.group(1))
    reference = front.get("reference_template", {})
    if not isinstance(reference, dict):
        reference = {}
    patches: list[ReportFormulaPatch] = []
    workbook_patches: list[WorkbookCellPatch] = []
    dynamic_tables: list[DynamicReportTableSpec] = []
    errors: list[str] = []
    for formula_match in _FORMULA_RE.finditer(text):
        sheet_name = _sheet_for_position(text, formula_match.start())
        payload = _parse_yaml_like(formula_match.group(2))
        patch = ReportFormulaPatch(
            sheet_name=sheet_name,
            excel_range=formula_match.group(1).strip(),
            object_type=str(payload.get("object_type", "ReportFormulaObject")).strip(),
            operation=str(payload.get("operation", "")).strip(),
            formula=str(payload.get("formula", "")).strip(),
            fixed_channel=str(payload.get("fixed_channel", "")).strip(),
            fixed_component=str(payload.get("fixed_component", "")).strip(),
            style=str(payload.get("style", "")).strip(),
            number_format=str(payload.get("number_format", "")).strip(),
        )
        if not patch.sheet_name:
            errors.append(f"CM Formula {patch.excel_range}: place it below a '## Sheet: <exact name>' heading.")
        if patch.operation not in {"replace", "create"}:
            errors.append(f"CM Formula {patch.excel_range}: operation must be replace or create.")
        if patch.object_type != "ReportFormulaObject":
            errors.append(f"CM Formula {patch.excel_range}: V0.1 only patches ReportFormulaObject.")
        if not patch.formula or patch.formula.startswith("="):
            errors.append(f"CM Formula {patch.excel_range}: formula must be a non-Excel CM formula.")
        patches.append(patch)
    for workbook_match in _WORKBOOK_CELL_RE.finditer(text):
        sheet_name = _sheet_for_position(text, workbook_match.start())
        payload = _parse_yaml_like(workbook_match.group(3))
        label = workbook_match.group(1).lower()
        value_type = str(payload.get("value_type", "")).strip().lower() or ({"value": "number", "text": "text", "formula": "formula"}[label])
        patch = WorkbookCellPatch(
            sheet_name=sheet_name,
            excel_range=workbook_match.group(2).strip(),
            value_type=value_type,
            value=payload.get("value", payload.get("formula", "")),
            operation=str(payload.get("operation", "")).strip(),
            style=str(payload.get("style", "")).strip(),
            number_format=str(payload.get("number_format", "")).strip(),
        )
        if not patch.sheet_name:
            errors.append(f"Workbook cell {patch.excel_range}: place it below a '## Sheet: <exact name>' heading.")
        if patch.operation not in {"replace", "create"}:
            errors.append(f"Workbook cell {patch.excel_range}: operation must be replace or create.")
        if patch.value_type not in {"number", "text", "formula"}:
            errors.append(f"Workbook cell {patch.excel_range}: value_type must be number, text, or formula.")
        if not _parse_single_cell_address(patch.excel_range):
            errors.append(f"Workbook cell {patch.excel_range}: existing-cell patches require one A1 address, not a range.")
        if patch.value_type == "formula" and not str(patch.value).strip().startswith("="):
            errors.append(f"Workbook formula {patch.excel_range}: formula must start with '=' in Markdown.")
        workbook_patches.append(patch)
    table_matches = list(_DYNAMIC_TABLE_RE.finditer(text))
    sheet_matches = list(_SHEET_RE.finditer(text))
    for index, table_match in enumerate(table_matches):
        sheet_name = _sheet_for_position(text, table_match.start())
        payload = _parse_yaml_like(table_match.group(2))
        next_table = table_matches[index + 1].start() if index + 1 < len(table_matches) else len(text)
        next_sheet = next((item.start() for item in sheet_matches if item.start() > table_match.start()), len(text))
        end = min(next_table, next_sheet)
        columns: list[ReportTableColumnSpec] = []
        for column_match in _TABLE_COLUMN_RE.finditer(text, table_match.end(), end):
            column_payload = _parse_yaml_like(column_match.group(2))
            columns.append(
                ReportTableColumnSpec(
                    name=column_match.group(1).strip(),
                    formula=str(column_payload.get("formula", "")).strip(),
                    header=str(column_payload.get("header", column_match.group(1))).strip(),
                    unit=str(column_payload.get("unit", "")).strip(),
                    channel=str(column_payload.get("channel", "")).strip(),
                    component=str(column_payload.get("component", "")).strip(),
                    number_format=str(column_payload.get("number_format", "")).strip(),
                )
            )
        table = DynamicReportTableSpec(
            sheet_name=sheet_name,
            excel_range=table_match.group(1).strip(),
            operation=str(payload.get("operation", "")).strip(),
            table_type=str(payload.get("table_type", "")).strip().lower(),
            body_rows=_parse_positive_int(payload.get("body_rows", 2), 2),
            columns=tuple(columns),
            audit_level=str(payload.get("audit_level", "Expert")).strip(),
            show_run=_parse_bool(payload.get("show_run", True), True),
            show_preconditions=_parse_bool(payload.get("show_preconditions", False), False),
            show_day_time=_parse_bool(payload.get("show_day_time", True), True),
            day_time_format=str(payload.get("day_time_format", "hh:mm:ss")).strip(),
            show_device=_parse_bool(payload.get("show_device", False), False),
            show_unknown=_parse_bool(payload.get("show_unknown", True), True),
            show_standard=_parse_bool(payload.get("show_standard", True), True),
            show_validation=_parse_bool(payload.get("show_validation", True), True),
            show_matrix=_parse_bool(payload.get("show_matrix", True), True),
            show_blank=_parse_bool(payload.get("show_blank", True), True),
            show_spiked=_parse_bool(payload.get("show_spiked", True), True),
            show_unspiked=_parse_bool(payload.get("show_unspiked", True), True),
            sort_formula=str(
                payload.get(
                    "sort_formula",
                    "peak.group" if str(payload.get("table_type", "")).strip().lower() == "integration" else "injection.number",
                )
            ).strip(),
            fixed_channel=str(payload.get("fixed_channel", "")).strip(),
            requires_processing=_parse_bool(payload.get("requires_processing", False), False),
            processing_method=str(payload.get("processing_method", "")).strip(),
            include_identified_peaks=_parse_bool(payload.get("include_identified_peaks", True), True),
            include_unidentified_peaks=_parse_bool(payload.get("include_unidentified_peaks", True), True),
        )
        if not table.sheet_name:
            errors.append(f"Dynamic table {table.excel_range}: place it below a '## Sheet: <exact name>' heading.")
        if table.operation != "create":
            errors.append(f"Dynamic table {table.excel_range}: operation must be create.")
        if table.table_type not in {"audittrail", "peak_summary", "integration"}:
            errors.append(f"Dynamic table {table.excel_range}: table_type must be audittrail, peak_summary, or integration.")
        if _parse_a1_range(table.excel_range) is None:
            errors.append(f"Dynamic table {table.excel_range}: invalid A1 range.")
        if table.table_type == "audittrail" and columns:
            errors.append(f"Dynamic table {table.excel_range}: audittrail uses Chromeleon's native event columns; omit Table Column blocks.")
        if table.table_type in {"peak_summary", "integration"} and not columns:
            errors.append(f"Dynamic table {table.excel_range}: {table.table_type} requires at least one Table Column block.")
        if table.table_type == "integration":
            if not table.requires_processing:
                errors.append(
                    f"Dynamic table {table.excel_range}: integration requires requires_processing: true."
                )
            if not table.processing_method:
                errors.append(
                    f"Dynamic table {table.excel_range}: integration requires an exact processing_method name."
                )
            if not table.fixed_channel:
                errors.append(
                    f"Dynamic table {table.excel_range}: integration requires fixed_channel matching the integrated signal."
                )
        for column in columns:
            if not column.formula or column.formula.startswith("="):
                errors.append(f"Dynamic table {table.excel_range}, column {column.name}: formula must be a CM report formula without '='.")
            if column.number_format:
                errors.append(
                    f"Dynamic table {table.excel_range}, column {column.name}: dynamic column number_format is not implemented."
                )
        if (
            table.table_type in {"peak_summary", "integration"}
            and any("peak." in column.formula.lower() for column in columns)
            and not table.requires_processing
        ):
            errors.append(
                f"Dynamic table {table.excel_range}: peak.* columns require requires_processing: true and a matching Processing Method contract."
            )
        dynamic_tables.append(table)
    kind = str(front.get("kind", "")).strip()
    version = str(front.get("spec_version", "")).strip()
    mode = str(front.get("generation_mode", "")).strip()
    workbook_policy = str(front.get("workbook_policy", "")).strip()
    template_name = str(front.get("template_name", "")).strip()
    sheet_specs: list[ReportSheetSpec] = []
    for sheet_match in _SHEET_RE.finditer(text):
        name = sheet_match.group(1).strip()
        next_sheet = _SHEET_RE.search(text, sheet_match.end())
        end = next_sheet.start() if next_sheet else len(text)
        settings_match = _SHEET_SETTINGS_RE.search(text, sheet_match.end(), end)
        settings = _parse_yaml_like(settings_match.group(1)) if settings_match else {}
        sheet_specs.append(
            ReportSheetSpec(
                name=name,
                column_widths=_parse_dimensions(settings.get("column_widths", ""), columns=True, errors=errors, context=name),
                row_heights=_parse_dimensions(settings.get("row_heights", ""), columns=False, errors=errors, context=name),
                is_active=_parse_bool(settings.get("active", True), True),
                each_injection=_parse_bool(settings.get("each_injection", True), True),
            )
        )
    if kind != "cm_report_template":
        errors.append("kind must be cm_report_template.")
    if version not in {"0.1", "0.2", "1.0"}:
        errors.append("spec_version must be 0.1, 0.2, or 1.0.")
    if not template_name:
        errors.append("template_name is required.")
    if mode not in {"clone_and_patch", "create_from_blank"}:
        errors.append("generation_mode must be clone_and_patch or create_from_blank.")
    if mode == "clone_and_patch" and not str(reference.get("cmbx", "")).strip():
        errors.append("reference_template.cmbx is required for clone_and_patch.")
    if mode == "clone_and_patch" and workbook_policy not in {"preserve", "existing_cells_only"}:
        errors.append("workbook_policy must be preserve or existing_cells_only for clone_and_patch.")
    if mode == "create_from_blank":
        if version != "1.0":
            errors.append("create_from_blank requires spec_version: 1.0.")
        if not sheet_specs:
            errors.append("create_from_blank requires at least one '## Sheet:' section.")
        if workbook_policy and workbook_policy != "create_static":
            errors.append("create_from_blank workbook_policy must be create_static when specified.")
        if any(patch.operation != "create" for patch in patches + workbook_patches):
            errors.append("Every cell/formula in create_from_blank mode must use operation: create.")
    if mode == "clone_and_patch" and workbook_patches and version != "0.2":
        errors.append("Workbook cell patches require spec_version: 0.2.")
    if mode == "clone_and_patch" and workbook_patches and workbook_policy != "existing_cells_only":
        errors.append("Workbook cell patches require workbook_policy: existing_cells_only.")
    return ReportTemplateMdSpec(
        path=path,
        template_name=template_name,
        reference_cmbx=str(reference.get("cmbx", "")).strip(),
        reference_template_name=str(reference.get("template_name", "")).strip(),
        generation_mode=mode,
        workbook_policy=workbook_policy,
        patches=tuple(patches),
        workbook_patches=tuple(workbook_patches),
        workbook_requests=tuple(item.strip() for item in _WORKBOOK_RE.findall(text)),
        sheets=tuple(sheet_specs),
        dynamic_tables=tuple(dynamic_tables),
        errors=tuple(errors),
    )


def resolve_reference_cmbx(spec: ReportTemplateMdSpec, search_roots: tuple[Path, ...] = ()) -> Path | None:
    if spec.generation_mode == "create_from_blank":
        candidates = [
            Path(__file__).resolve().parent / "assets" / "report_blank_carrier.cmbx",
            _DEFAULT_BLANK_CARRIER,
        ]
        for root in search_roots:
            candidates.extend((root / "report_blank_carrier.cmbx", root / "PressureEvaluation_changed.cmbx"))
        return next((candidate.resolve() for candidate in candidates if candidate.is_file()), None)
    if not spec.reference_cmbx:
        return None
    reference = Path(spec.reference_cmbx)
    candidates = [reference, spec.path.parent / reference]
    for root in search_roots:
        candidates.extend((root / reference, root / reference.name))
    for candidate in candidates:
        if candidate.exists() and candidate.is_file():
            return candidate.resolve()
    return None


def prepare_report_template_md(spec: ReportTemplateMdSpec, search_roots: tuple[Path, ...] = ()) -> ReportTemplateCompileResult:
    result = ReportTemplateCompileResult(spec=spec, source_cmbx=resolve_reference_cmbx(spec, search_roots), errors=list(spec.errors))
    if result.source_cmbx is None:
        result.errors.append(f"Reference carrier was not found: {spec.reference_cmbx}")
        return result
    try:
        package, report, xml_text = _load_standalone_report(result.source_cmbx)
        result.source_report_name = report.name
        sheets = parse_report_sheets(xml_text, report.name)
        result.sheets = tuple(sheet.sheet_name for sheet in sheets)
        objects = parse_report_sheet_objects(xml_text, report.name)
        result.preserved_report_tables = tuple(
            (item.sheet_name, item.excel_range, item.table_type or "report table")
            for item in objects
            if item.object_type == "ReportTableObject"
        )
        root = ET.fromstring(xml_text)
        if spec.generation_mode == "create_from_blank":
            _prepare_blank_report(root, spec, result)
            result.xml_text = ET.tostring(root, encoding="unicode")
            return result
        if spec.reference_template_name and spec.reference_template_name != report.name:
            result.errors.append(f"Carrier name is '{report.name}', but MD expects '{spec.reference_template_name}'.")
        for patch in spec.patches:
            matches = [obj for obj in parse_report_sheet_objects(xml_text, report.name, patch.sheet_name) if obj.excel_range.upper() == patch.excel_range.upper()]
            if len(matches) != 1:
                result.errors.append(f"{patch.sheet_name} / {patch.excel_range}: expected one object, found {len(matches)}.")
                continue
            if matches[0].object_type != patch.object_type:
                result.errors.append(f"{patch.sheet_name} / {patch.excel_range}: carrier type is {matches[0].object_type or 'unknown'}, not {patch.object_type}.")
                continue
            node = _find_sheet_object(root, patch.sheet_name, patch.excel_range)
            if node is None:
                result.errors.append(f"{patch.sheet_name} / {patch.excel_range}: XML node could not be resolved.")
                continue
            formula_node = node.find(".//Formula")
            if formula_node is None:
                result.errors.append(f"{patch.sheet_name} / {patch.excel_range}: ReportFormulaObject has no Formula child.")
                continue
            formula_node.set("value", patch.formula)
            _set_value_child(node, "FixedChannel", patch.fixed_channel)
            _set_value_child(node, "FixedComponentName", patch.fixed_component)
            result.applied_patches += (patch,)
        if spec.workbook_patches:
            workbook_writes: list[FormulaOneWorkbookPatch] = []
            for patch in spec.workbook_patches:
                address = _parse_single_cell_address(patch.excel_range)
                if address is None:
                    continue
                if patch.sheet_name not in result.sheets:
                    result.errors.append(f"{patch.sheet_name} / {patch.excel_range}: workbook sheet was not found in carrier.")
                    continue
                row, column = address
                workbook_writes.append(FormulaOneWorkbookPatch(patch.sheet_name, row, column, patch.value_type, patch.value))
            if not result.errors:
                new_blob = write_formulaone_existing_cells(extract_formulaone_spreadsheet_data(ET.tostring(root, encoding="unicode")), tuple(workbook_writes))
                _replace_spreadsheet_data(root, new_blob)
                result.applied_workbook_patches = tuple(spec.workbook_patches)
        if spec.workbook_requests:
            result.warnings.append(f"{len(spec.workbook_requests)} FormulaOne workbook change request(s) are review-only and were not written.")
        if result.preserved_report_tables:
            result.warnings.append(
                f"{len(result.preserved_report_tables)} ReportTableObject(s) preserved unchanged; V0.2 does not create or edit dynamic table columns."
            )
        if not spec.patches:
            result.warnings.append("No direct CM formula patches declared; output is a renamed report clone.")
        result.xml_text = ET.tostring(root, encoding="unicode")
    except Exception as exc:
        result.errors.append(f"Could not decode or prepare report carrier: {exc}")
    return result


def _prepare_blank_report(root: ET.Element, spec: ReportTemplateMdSpec, result: ReportTemplateCompileResult) -> None:
    declared = {sheet.name for sheet in spec.sheets}
    if len(declared) != len(spec.sheets):
        result.errors.append("Sheet names must be unique.")
        return
    for patch in (*spec.patches, *spec.workbook_patches, *spec.dynamic_tables):
        if patch.sheet_name not in declared:
            result.errors.append(f"{patch.sheet_name} / {patch.excel_range}: sheet is not declared.")
    occupied: list[tuple[str, tuple[int, int, int, int], str]] = []
    for patch in (*spec.patches, *spec.workbook_patches):
        bounds = _parse_a1_range(patch.excel_range)
        if bounds is not None:
            occupied.append((patch.sheet_name, bounds, "cell/formula"))
    for table in spec.dynamic_tables:
        bounds = _parse_a1_range(table.excel_range)
        if bounds is None:
            continue
        for sheet_name, existing, kind in occupied:
            if sheet_name == table.sheet_name and _ranges_overlap(bounds, existing):
                result.errors.append(f"{table.sheet_name} / {table.excel_range}: overlaps another {kind} declaration.")
        occupied.append((table.sheet_name, bounds, "dynamic table"))
        left, top, right, bottom = bounds
        width = right - left + 1
        if table.table_type in {"peak_summary", "integration"} and width != len(table.columns):
            result.errors.append(
                f"{table.sheet_name} / {table.excel_range}: {table.table_type} width is {width}, "
                f"but {len(table.columns)} columns are declared."
            )
        if table.table_type == "audittrail":
            expected_width = 2 + int(table.show_day_time) + int(table.show_device)
            if width != expected_width:
                result.errors.append(
                    f"{table.sheet_name} / {table.excel_range}: audittrail requires {expected_width} columns "
                    f"for the selected Day Time/Device options."
                )
    if result.errors:
        return

    carrier_blob = extract_formulaone_spreadsheet_data(ET.tostring(root, encoding="unicode"))
    workbook_sheets: list[FormulaOneSheetSpec] = []
    for sheet in spec.sheets:
        cells: list[FormulaOneWorkbookPatch] = []
        for patch in spec.workbook_patches:
            if patch.sheet_name != sheet.name:
                continue
            address = _parse_single_cell_address(patch.excel_range)
            if address is None:
                result.errors.append(f"{patch.sheet_name} / {patch.excel_range}: workbook values require one A1 address.")
                continue
            row, column = address
            cells.append(
                FormulaOneWorkbookPatch(
                    sheet.name,
                    row,
                    column,
                    patch.value_type,
                    patch.value,
                    patch.style,
                    patch.number_format,
                )
            )
        for patch in spec.patches:
            if patch.sheet_name != sheet.name or (not patch.style and not patch.number_format):
                continue
            address = _parse_single_cell_address(patch.excel_range)
            if address is None:
                result.errors.append(f"{patch.sheet_name} / {patch.excel_range}: styled CM formulas require one A1 address.")
                continue
            row, column = address
            cells.append(
                FormulaOneWorkbookPatch(sheet.name, row, column, "text", "", patch.style, patch.number_format)
            )
        workbook_sheets.append(FormulaOneSheetSpec(sheet.name, tuple(cells), sheet.column_widths, sheet.row_heights))
    if result.errors:
        return
    build = create_formulaone_workbook(carrier_blob, tuple(workbook_sheets))
    _replace_workbook_data(root, build.xml_text)
    _replace_report_sheets(root, spec)
    _replace_print_sheet_setups(root, spec)
    result.sheets = tuple(sheet.name for sheet in spec.sheets)
    result.applied_patches = spec.patches
    result.applied_workbook_patches = spec.workbook_patches
    result.applied_dynamic_tables = spec.dynamic_tables
    result.preserved_report_tables = ()
    if any(
        table.table_type in {"peak_summary", "integration"}
        and any("peak." in column.formula.lower() for column in table.columns)
        for table in spec.dynamic_tables
    ):
        result.warnings.append("A dynamic table includes peak.* formulas and therefore requires matching Processing Method peak results.")
    for table in spec.dynamic_tables:
        if table.table_type == "integration":
            result.warnings.append(
                f"Integration runtime contract: Processing Method '{table.processing_method}' must integrate "
                f"channel '{table.fixed_channel}'. The standalone report CMBX does not install or assign that Processing Method."
            )
    if spec.workbook_requests:
        result.warnings.append("Workbook change requests are notes only; declare concrete cells in create_from_blank mode.")


def _replace_report_sheets(root: ET.Element, spec: ReportTemplateMdSpec) -> None:
    report = root.find(".//ReportDefinition")
    if report is None:
        raise ValueError("Carrier ReportDefinition was not found.")
    existing = report.findall("SheetDescription")
    if not existing:
        raise ValueError("Carrier has no SheetDescription skeleton.")
    auto_repeat = existing[0].find("AutoRepeatAreaDescription")
    if auto_repeat is None:
        raise ValueError("Carrier has no AutoRepeatAreaDescription skeleton.")
    for sheet in existing:
        report.remove(sheet)
    current = report.find("CurrentSheet")
    if current is not None:
        current.set("value", spec.sheets[0].name)
    for sheet_spec in spec.sheets:
        sheet = ET.Element("SheetDescription", {"type": "SheetDescription"})
        ET.SubElement(sheet, "Id", {"value": str(uuid.uuid4())})
        ET.SubElement(sheet, "SheetName", {"value": sheet_spec.name})
        for patch in spec.patches:
            if patch.sheet_name == sheet_spec.name:
                sheet.append(_new_report_formula_object(patch))
        for table in spec.dynamic_tables:
            if table.sheet_name == sheet_spec.name:
                sheet.append(_new_dynamic_report_table_object(table))
        sheet.append(copy.deepcopy(auto_repeat))
        report.append(sheet)


def _replace_workbook_data(root: ET.Element, workbook_xml: str) -> None:
    generated_root = ET.fromstring(workbook_xml)
    generated = generated_root.find("WorkbookData") if generated_root.tag != "WorkbookData" else generated_root
    if generated is None:
        raise ValueError("FormulaOne runtime did not return WorkbookData.")
    current = root.find(".//SpreadsheetDefinition/CmData/WorkbookData")
    if current is None:
        raise ValueError("Carrier WorkbookData was not found.")
    parent = next((node for node in root.iter() if current in list(node)), None)
    if parent is None:
        raise ValueError("Carrier WorkbookData parent was not found.")
    index = list(parent).index(current)
    parent.remove(current)
    parent.insert(index, copy.deepcopy(generated))


def _replace_print_sheet_setups(root: ET.Element, spec: ReportTemplateMdSpec) -> None:
    setups = root.find(".//PrintSettings/PrintSheetSetups/Setups")
    if setups is None or not list(setups):
        raise ValueError("Carrier print-sheet setup skeleton was not found.")
    skeleton = copy.deepcopy(list(setups)[0])
    for item in list(setups):
        setups.remove(item)
    for sheet_spec in spec.sheets:
        item = copy.deepcopy(skeleton)
        name = item.find("Name")
        data = item.find("Data")
        if name is None or data is None:
            raise ValueError("Carrier print-sheet setup is incomplete.")
        name.set("value", sheet_spec.name)
        active = data.find("IsActive")
        each = data.find(".//EachInjection")
        if active is not None:
            active.set("value", "Y" if sheet_spec.is_active else "N")
        if each is not None:
            each.set("value", "Y" if sheet_spec.each_injection else "N")
        setups.append(item)


def _new_report_formula_object(patch: ReportFormulaPatch) -> ET.Element:
    bounds = _parse_a1_range(patch.excel_range)
    if bounds is None:
        raise ValueError(f"Invalid CM formula range: {patch.excel_range}")
    left, top, right, bottom = bounds
    node = ET.Element("SheetObject", {"type": "ReportFormulaObject"})
    ET.SubElement(node, "Id", {"value": f"ReportFormula1_{{{str(uuid.uuid4()).upper()}}}"})
    range_node = ET.SubElement(node, "Range", {"type": "CellRange"})
    ET.SubElement(range_node, "Left", {"value": str(left - 1)})
    ET.SubElement(range_node, "Top", {"value": str(top - 1)})
    ET.SubElement(range_node, "Right", {"value": str(right - 1)})
    ET.SubElement(range_node, "Bottom", {"value": str(bottom - 1)})
    ET.SubElement(range_node, "SubRanges")
    ET.SubElement(node, "UndoRedoId", {"value": str(uuid.uuid4())})
    ET.SubElement(node, "Formula", {"value": patch.formula})
    fixed_channel = ET.SubElement(node, "FixedChannel")
    if patch.fixed_channel:
        fixed_channel.set("value", patch.fixed_channel)
    else:
        fixed_channel.set("null", "Y")
    ET.SubElement(node, "FixedComponentName", {"value": patch.fixed_component})
    ET.SubElement(node, "IsSignatureFormula", {"value": "N"})
    return node


def _new_dynamic_report_table_object(spec: DynamicReportTableSpec) -> ET.Element:
    skeletons = json.loads(_REPORT_TABLE_SKELETONS.read_text(encoding="utf-8"))
    payload = skeletons.get(spec.table_type)
    if not isinstance(payload, dict) or not payload.get("xml"):
        raise ValueError(f"Native report-table skeleton is missing: {spec.table_type}")
    node = ET.fromstring(str(payload["xml"]))
    _set_report_object_range(node, spec.excel_range)
    _refresh_report_table_ids(node)
    report_table_type = node.find("ReportTableType")
    if report_table_type is not None:
        report_table_type.set("value", spec.table_type)
    if spec.table_type == "audittrail":
        _configure_audittrail_table(node, spec)
    elif spec.table_type == "peak_summary":
        _configure_peak_summary_table(node, spec)
    elif spec.table_type == "integration":
        _configure_integration_table(node, spec)
    else:
        raise ValueError(f"Unknown dynamic table type: {spec.table_type}.")
    return node


def _set_report_object_range(node: ET.Element, excel_range: str) -> None:
    bounds = _parse_a1_range(excel_range)
    if bounds is None:
        raise ValueError(f"Invalid dynamic table range: {excel_range}")
    left, top, right, bottom = bounds
    values = {"Left": left - 1, "Top": top - 1, "Right": right - 1, "Bottom": bottom - 1}
    range_node = node.find("Range")
    if range_node is None:
        raise ValueError("Native report-table skeleton has no Range.")
    for name, value in values.items():
        child = range_node.find(name)
        if child is None:
            child = ET.SubElement(range_node, name)
        child.set("value", str(value))


def _refresh_report_table_ids(node: ET.Element) -> None:
    for name in ("Id", "UndoRedoId", "UndoRedoIdTable"):
        child = node.find(name)
        if child is not None:
            child.set("value", str(uuid.uuid4()))
    for name in ("TableGuid", "ColumnId"):
        for child in node.findall(f".//{name}"):
            child.set("value", str(uuid.uuid4()))


def _configure_audittrail_table(node: ET.Element, spec: DynamicReportTableSpec) -> None:
    report_table = node.find(".//ReportTable")
    properties = node.find(".//Properties")
    bounds = _parse_a1_range(spec.excel_range)
    if report_table is None or properties is None or bounds is None:
        raise ValueError("Audit Trail table skeleton is incomplete.")
    left, top, right, bottom = bounds
    width, height = right - left + 1, bottom - top + 1
    _set_value_child(report_table, "NumberOfBodyRows", str(spec.body_rows))
    _set_value_child(report_table, "NumberOfHeaderRows", "1")
    _set_value_child(report_table, "TableSizeForUnknownReportTable", f"{width},{height}")
    _set_value_child(report_table, "NumberOfColumns", str(width))
    level = properties.find("AuditLevel")
    if level is not None:
        level.set("value", spec.audit_level)
    _set_yes_no_child(properties, "ShowRun", spec.show_run)
    _set_yes_no_child(properties, "ShowPreconditions", spec.show_preconditions)
    _set_yes_no_child(properties, "ShowDayTime", spec.show_day_time)
    _set_value_child(properties, "DayTimeFormat", spec.day_time_format)
    _set_yes_no_child(properties, "ShowDevice", spec.show_device)


def _configure_peak_summary_table(node: ET.Element, spec: DynamicReportTableSpec) -> None:
    report_table = node.find(".//ReportTable")
    columns = node.find(".//Columns")
    properties = node.find(".//Properties")
    bounds = _parse_a1_range(spec.excel_range)
    if report_table is None or columns is None or properties is None or bounds is None:
        raise ValueError("Peak Summary table skeleton is incomplete.")
    left, top, right, bottom = bounds
    width, height = right - left + 1, bottom - top + 1
    _set_value_child(report_table, "NumberOfBodyRows", str(spec.body_rows))
    _set_value_child(report_table, "TableSizeForUnknownReportTable", f"{width},{height}")
    for child in list(columns):
        columns.remove(child)
    for column in spec.columns:
        columns.append(_new_summary_column(column))
    _set_yes_no_child(properties, "SortByInjectionNumber", True)
    _set_value_child(properties, "SortFormula", spec.sort_formula)
    _set_yes_no_child(properties, "ReportOnlyLastRowOfGroup", False)
    _set_yes_no_child(properties, "IgnoreCaseComparingTextResults", True)
    _set_value_child(properties, "FixedChannelName", spec.fixed_channel)
    for name, value in (
        ("ShowUnknown", spec.show_unknown),
        ("ShowStandard", spec.show_standard),
        ("ShowValidation", spec.show_validation),
        ("ShowMatrix", spec.show_matrix),
        ("ShowBlank", spec.show_blank),
        ("ShowSpiked", spec.show_spiked),
        ("ShowUnspiked", spec.show_unspiked),
    ):
        _set_yes_no_child(properties, name, value)
    custom = properties.find("CustomConditions")
    if custom is not None:
        custom.clear()
        custom.set("null", "Y")
    headers = properties.find("VisibleAdditionalHeaderRows")
    if headers is not None:
        headers.set("value", "")


def _new_summary_column(spec: ReportTableColumnSpec) -> ET.Element:
    item = ET.Element("Item", {"type": "SummaryReportTableColumn"})
    _append_report_formula(item, "Formula", spec.formula)
    _append_report_formula(item, "Header", _quoted_formula(spec.header))
    _append_report_formula(item, "Dimension", _quoted_formula(spec.unit))
    channel = ET.SubElement(item, "Channel")
    if spec.channel:
        channel.set("value", spec.channel)
    else:
        channel.set("null", "Y")
    ET.SubElement(item, "ColumnId", {"value": str(uuid.uuid4())})
    _append_report_formula(item, "InjectionFormula", "injection.name")
    _append_report_formula(item, "ChannelFormula", _quoted_formula(spec.channel))
    _append_report_formula(item, "ComponentFormula", _quoted_formula(spec.component))
    ET.SubElement(item, "FixedPeak", {"null": "Y"})
    return item


def _configure_integration_table(node: ET.Element, spec: DynamicReportTableSpec) -> None:
    report_table = node.find(".//ReportTable")
    columns = node.find(".//Columns")
    properties = node.find(".//Properties")
    bounds = _parse_a1_range(spec.excel_range)
    if report_table is None or columns is None or properties is None or bounds is None:
        raise ValueError("Integration table skeleton is incomplete.")
    left, top, right, bottom = bounds
    width, height = right - left + 1, bottom - top + 1
    _set_value_child(report_table, "NumberOfBodyRows", str(spec.body_rows))
    _set_value_child(report_table, "TableSizeForUnknownReportTable", f"{width},{height}")
    for child in list(columns):
        columns.remove(child)
    for column in spec.columns:
        columns.append(_new_integration_column(column, spec.fixed_channel))
    _set_yes_no_child(properties, "SortByPeakNumber", True)
    _set_value_child(properties, "SortFormula", spec.sort_formula or "peak.group")
    _set_yes_no_child(properties, "ReportOnlyLastRowOfGroup", False)
    _set_yes_no_child(properties, "IgnoreCaseComparingTextResults", False)
    _set_value_child(properties, "VisibleAdditionalHeaderRows", "None")
    _set_yes_no_child(properties, "IncludeIdentifiedPeaks", spec.include_identified_peaks)
    _set_yes_no_child(properties, "IncludeUnidentifiedPeaks", spec.include_unidentified_peaks)
    _set_yes_no_child(properties, "IncludeComponentTable", False)
    _set_yes_no_child(properties, "IncludeUnidentifiedPeakGroupTable", False)
    _set_yes_no_child(properties, "RejectPeaksByRelativeArea", False)
    _set_value_child(properties, "FixedChannelName", spec.fixed_channel)
    _set_yes_no_child(properties, "UseFixedChannelFilter", True)
    selection = properties.find("TableChannelSelection")
    if selection is not None:
        mode = selection.find("Mode")
        if mode is not None:
            mode.set("value", "SelectedChannel")


def _new_integration_column(spec: ReportTableColumnSpec, default_channel: str) -> ET.Element:
    item = ET.Element("Item", {"type": "IntegrationReportTableColumn"})
    _append_report_formula(item, "Formula", spec.formula)
    _append_report_formula(item, "Header", _quoted_formula(spec.header))
    if spec.unit:
        _append_report_formula(item, "Dimension", _quoted_formula(spec.unit))
    else:
        ET.SubElement(item, "Dimension", {"null": "Y"})
    channel_name = spec.channel or default_channel
    channel = ET.SubElement(item, "Channel")
    channel.set("value", channel_name)
    ET.SubElement(item, "ColumnId", {"value": str(uuid.uuid4())})
    _append_report_formula(item, "InjectionFormula", "injection.name")
    _append_report_formula(item, "ChannelFormula", _quoted_formula(channel_name))
    if spec.component:
        _append_report_formula(item, "ComponentFormula", _quoted_formula(spec.component))
    else:
        _append_report_formula(item, "ComponentFormula", "peak.name")
    return item


def _append_report_formula(parent: ET.Element, name: str, formula: str) -> ET.Element:
    node = ET.SubElement(parent, name, {"type": "ReportFormula"})
    ET.SubElement(node, "Formula", {"value": formula})
    return node


def _quoted_formula(value: str) -> str:
    escaped = value.replace('"', '""')
    return f'"{escaped}"'


def _set_yes_no_child(node: ET.Element, name: str, value: bool) -> None:
    _set_value_child(node, name, "Y" if value else "N")


def compile_report_template_md_to_cmbx(spec: ReportTemplateMdSpec, output_cmbx: Path, search_roots: tuple[Path, ...] = ()) -> ReportTemplateCompileResult:
    result = prepare_report_template_md(spec, search_roots)
    if not result.ready:
        return result
    assert result.source_cmbx is not None
    with tempfile.TemporaryDirectory(prefix="cmbx_report_md_compile_") as tmp:
        xml_path = Path(tmp) / "edited_report.xml"
        xml_path.write_text(result.xml_text, encoding="utf-8")
        try:
            repack_standalone_report_cmbx(result.source_cmbx, xml_path, output_cmbx, report_name=spec.template_name)
        except Exception as exc:
            result.errors.append(f"Could not package report CMBX: {exc}")
            return result
    try:
        _package, report, output_xml = _load_standalone_report(output_cmbx)
        if report.name != spec.template_name:
            result.errors.append(f"Output carrier name check failed: expected {spec.template_name}, got {report.name}.")
        if spec.generation_mode == "create_from_blank":
            expected_sheets = [sheet.name for sheet in spec.sheets]
            actual_sheets = [sheet.sheet_name for sheet in parse_report_sheets(output_xml, report.name)]
            if actual_sheets != expected_sheets:
                result.errors.append(f"Output sheet check failed: expected {expected_sheets}, got {actual_sheets}.")
            actual_objects = {
                (item.sheet_name, item.excel_range.upper(), item.formula, item.fixed_channel, item.fixed_component)
                for item in parse_report_sheet_objects(output_xml, report.name)
                if item.object_type == "ReportFormulaObject"
            }
            for patch in spec.patches:
                expected = (patch.sheet_name, patch.excel_range.upper(), patch.formula, patch.fixed_channel, patch.fixed_component)
                if expected not in actual_objects:
                    result.errors.append(f"Output CM formula check failed: {patch.sheet_name}!{patch.excel_range}.")
            actual_tables = {
                (item.sheet_name, item.excel_range.upper(), item.table_type)
                for item in parse_report_sheet_objects(output_xml, report.name)
                if item.object_type == "ReportTableObject"
            }
            for table in spec.dynamic_tables:
                expected = (table.sheet_name, table.excel_range.upper(), table.table_type)
                if expected not in actual_tables:
                    result.errors.append(f"Output dynamic table check failed: {table.sheet_name}!{table.excel_range} ({table.table_type}).")
                    continue
                if table.table_type == "integration":
                    root = ET.fromstring(output_xml)
                    obj = _find_sheet_object(root, table.sheet_name, table.excel_range)
                    actual_formulas = tuple(
                        _value(item.find("Formula"), "Formula")
                        for item in obj.findall(".//Columns/Item")
                    ) if obj is not None else ()
                    expected_formulas = tuple(column.formula for column in table.columns)
                    if actual_formulas != expected_formulas:
                        result.errors.append(
                            f"Output Integration column check failed: expected {expected_formulas}, got {actual_formulas}."
                        )
            if not extract_formulaone_spreadsheet_data(output_xml):
                result.errors.append("Output FormulaOne workbook payload is empty.")
    except Exception as exc:
        result.errors.append(f"Output decode verification failed: {exc}")
    return result


def _load_standalone_report(path: Path):
    package = load_cmbx_package(path)
    reports = [element for element in package.methods_and_reports if element.kind == "report_template"]
    if len(reports) != 1:
        raise ValueError(f"Expected exactly one standalone report template, found {len(reports)}.")
    _embedded, xml_text = decode_report_template_xml(package, reports[0])
    return package, reports[0], xml_text


def _find_sheet_object(root: ET.Element, sheet_name: str, excel_range: str) -> ET.Element | None:
    target = excel_range.upper()
    for sheet in root.findall(".//SheetDescription"):
        if _value(sheet, "SheetName") != sheet_name:
            continue
        for obj in sheet.findall("SheetObject"):
            range_node = obj.find("Range")
            if range_node is None:
                continue
            candidate = _range_to_a1(_value(range_node, "Left"), _value(range_node, "Top"), _value(range_node, "Right"), _value(range_node, "Bottom"))
            if candidate.upper() == target:
                return obj
    return None


def _set_value_child(node: ET.Element, name: str, value: str) -> None:
    child = node.find(name)
    if child is None:
        child = ET.SubElement(node, name)
    if value:
        child.attrib.pop("null", None)
        child.set("value", value)
    else:
        child.attrib.pop("value", None)
        child.set("null", "Y")


def _value(node: ET.Element | None, name: str) -> str:
    if node is None:
        return ""
    child = node.find(name)
    return child.attrib.get("value", "") if child is not None else ""


def _range_to_a1(left: str, top: str, right: str, bottom: str) -> str:
    try:
        values = [int(value) for value in (left, top, right, bottom)]
    except ValueError:
        return ""
    start = f"{_column(values[0] + 1)}{values[1] + 1}"
    end = f"{_column(values[2] + 1)}{values[3] + 1}"
    return start if start == end else f"{start}:{end}"


def _parse_single_cell_address(value: str) -> tuple[int, int] | None:
    match = re.fullmatch(r"\s*([A-Za-z]+)([1-9][0-9]*)\s*", value)
    if not match:
        return None
    column = 0
    for letter in match.group(1).upper():
        column = column * 26 + (ord(letter) - 64)
    return int(match.group(2)), column


def _parse_a1_range(value: str) -> tuple[int, int, int, int] | None:
    parts = [part.strip() for part in value.split(":")]
    if len(parts) not in {1, 2}:
        return None
    start = _parse_single_cell_address(parts[0])
    end = _parse_single_cell_address(parts[-1])
    if start is None or end is None:
        return None
    top, left = start
    bottom, right = end
    if right < left or bottom < top:
        return None
    return left, top, right, bottom


def _ranges_overlap(first: tuple[int, int, int, int], second: tuple[int, int, int, int]) -> bool:
    left_a, top_a, right_a, bottom_a = first
    left_b, top_b, right_b, bottom_b = second
    return not (right_a < left_b or right_b < left_a or bottom_a < top_b or bottom_b < top_a)


def _parse_dimensions(value: object, *, columns: bool, errors: list[str], context: str) -> tuple[tuple[int, float], ...]:
    if value is None or value == "":
        return ()
    items = value if isinstance(value, list) else [item.strip() for item in str(value).split(",") if item.strip()]
    parsed: list[tuple[int, float]] = []
    for item in items:
        text = str(item).strip().strip("'\"")
        if "=" not in text:
            errors.append(f"{context}: invalid {'column_widths' if columns else 'row_heights'} item '{text}'.")
            continue
        key, raw_number = (part.strip() for part in text.split("=", 1))
        try:
            number = float(raw_number)
            if columns:
                address = _parse_single_cell_address(f"{key}1")
                index = address[1] if address else 0
            else:
                index = int(key)
            if index < 1 or number <= 0:
                raise ValueError
            parsed.append((index, number))
        except (TypeError, ValueError):
            errors.append(f"{context}: invalid {'column width' if columns else 'row height'} '{text}'.")
    return tuple(parsed)


def _replace_spreadsheet_data(root: ET.Element, blob: bytes) -> None:
    import base64

    for node in root.iter():
        if node.tag == "SpreadSheetData":
            node.set("value", base64.b64encode(blob).decode("ascii"))
            return
    raise ValueError("No FormulaOne SpreadSheetData payload was found in carrier XML.")


def _column(index: int) -> str:
    letters: list[str] = []
    while index:
        index, remainder = divmod(index - 1, 26)
        letters.append(chr(65 + remainder))
    return "".join(reversed(letters))


def _sheet_for_position(text: str, position: int) -> str:
    current = ""
    for match in _SHEET_RE.finditer(text):
        if match.start() >= position:
            break
        current = match.group(1).strip()
    return current


def _parse_yaml_like(text: str) -> dict[str, object]:
    """A deliberately small YAML subset for the documented MD contract."""
    result: dict[str, object] = {}
    active_map: dict[str, object] | None = None
    active_indent = -1
    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        stripped = raw_line.strip()
        if ":" not in stripped:
            continue
        key, raw_value = stripped.split(":", 1)
        key, raw_value = key.strip(), raw_value.strip()
        if indent == 0:
            active_map = None
            active_indent = -1
            if raw_value:
                result[key] = _parse_scalar(raw_value)
            else:
                child: dict[str, object] = {}
                result[key] = child
                active_map = child
                active_indent = indent
        elif active_map is not None and indent > active_indent:
            active_map[key] = _parse_scalar(raw_value)
    return result


def _parse_scalar(value: str):
    if not value:
        return ""
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    if value.startswith("[") and value.endswith("]"):
        try:
            return ast.literal_eval(value)
        except (ValueError, SyntaxError):
            return [item.strip().strip("'\"") for item in value[1:-1].split(",") if item.strip()]
    return value.strip("'\"")


def _parse_bool(value: object, default: bool) -> bool:
    if isinstance(value, bool):
        return value
    normalized = str(value).strip().lower()
    if normalized in {"true", "yes", "y", "1"}:
        return True
    if normalized in {"false", "no", "n", "0"}:
        return False
    return default


def _parse_positive_int(value: object, default: int) -> int:
    try:
        parsed = int(str(value).strip())
    except (TypeError, ValueError):
        return default
    return parsed if parsed > 0 else default
