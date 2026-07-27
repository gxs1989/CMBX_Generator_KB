from __future__ import annotations

import tempfile
import re
from pathlib import Path

from chromeleon_bridge import export_audit_raw, export_signal_raw
from chromeleon_method_decoder import MethodDecodeResult, decode_cpxm_method_xml
from cmbx_container import CmbxElement, CmbxPackage, element_path, extract_cmbx_entry, safe_filename
from embedded_method_extractor import EmbeddedMethodBlock, extract_embedded_instrument_method
from embedded_report_extractor import (
    EmbeddedReportTemplate,
    decode_report_template_xml,
    extract_embedded_report_template,
    parse_report_sheet_objects,
    parse_report_sheets,
)
from foq_contract_report import ReportCellValue, build_report_cell_value_map, resolve_contract_values, write_foq_contract_workbook
from foq_result_locations import locations_for_device_type
from formulaone_report_exporter import export_formulaone_report_template, formulaone_report_filename, report_export_sheet_names
from method_xml_flow import build_method_flow_from_xml, build_method_flow_tsv
from report_calculation_map import build_report_calculation_map
from report_formula_evaluator import build_report_formula_context, evaluate_report_formula_objects, evaluate_report_formulas, formula_evaluations_tsv, _eval_metadata_formula
from report_workbook_builder import write_report_workbook
from sequence_cmd_parser import build_embedded_object_summary


_REPORT_XML_CACHE: dict[tuple[str, str, int], str] = {}


def export_element(package: CmbxPackage, element: CmbxElement, output_root: str | Path) -> Path:
    return export_element_paths(package, element, output_root)[0]


def export_element_paths(package: CmbxPackage, element: CmbxElement, output_root: str | Path) -> list[Path]:
    output_base = Path(output_root)
    package_path = package.path
    if element.kind == "signal":
        raw_path = _extract_raw_to_cache(package, element, output_base)
        output_path = _element_output_path(package, element, output_base, ".tsv")
        return [export_signal_raw(raw_path, output_path, element.name)]
    if element.kind == "audit":
        raw_path = _extract_raw_to_cache(package, element, output_base)
        output_path = _element_output_path(package, element, output_base, "_audit.tsv")
        return [export_audit_raw(raw_path, output_path)]
    if element.kind == "instrument_method":
        embedded = extract_embedded_instrument_method(package, element)
        if embedded:
            return export_embedded_instrument_method(package, element, embedded, output_base)
    if element.kind == "report_template":
        embedded_report = extract_embedded_report_template(package, element)
        if embedded_report:
            return export_embedded_report_template(package, element, embedded_report, output_base)
    entry_name = element.package_entry_name
    if not entry_name:
        return [export_embedded_object_summary(package, element, output_base)]
    output_path = _element_output_path(package, element, output_base, Path(entry_name).suffix or ".bin")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(extract_cmbx_entry(package_path, entry_name))
    return [output_path]


def export_elements(package: CmbxPackage, elements: list[CmbxElement], output_root: str | Path) -> list[Path]:
    exported: list[Path] = []
    for element in elements:
        exported.extend(export_element_paths(package, element, output_root))
    return exported


def export_report_formula_values(package: CmbxPackage, injection: CmbxElement, report: CmbxElement, output_root: str | Path, sheet_name: str = "") -> Path:
    xml_text = _decode_report_xml_cached(package, report)
    rows = evaluate_report_formulas(package, injection, report.name, xml_text, sheet_name)
    output_path = _injection_output_path(package, injection, Path(output_root), f"{safe_filename(report.name)}_report_formula_values.tsv" if not sheet_name else f"{safe_filename(report.name)}_{safe_filename(sheet_name)}_formula_values.tsv")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(formula_evaluations_tsv(rows), encoding="utf-8")
    return output_path


def export_report_workbook(package: CmbxPackage, injection: CmbxElement, report: CmbxElement, output_root: str | Path, progress=None) -> Path:
    _progress(progress, f"Decoding report template: {report.name}")
    xml_text = _decode_report_xml_cached(package, report)
    _progress(progress, f"Reading report sheets for {injection.name}")
    sheets = parse_report_sheets(xml_text, report.name, injection.name)
    target_sheet_names = []
    if any(sheet.sheet_name == "Definitions" for sheet in sheets):
        target_sheet_names.append("Definitions")
    target_sheet_names.extend(
        sheet.sheet_name
        for sheet in sheets
        if sheet.applies_to_injection == "Yes" and sheet.sheet_name not in target_sheet_names
    )
    if not target_sheet_names:
        target_sheet_names = [sheet.sheet_name for sheet in sheets if sheet.is_active != "N"][:1]
    context = build_report_formula_context(package, injection)
    formula_sheets = {}
    for sheet_name in target_sheet_names:
        _progress(progress, f"Evaluating {injection.name} / {sheet_name}")
        formula_sheets[sheet_name] = evaluate_report_formulas(package, injection, report.name, xml_text, sheet_name, context=context)
    calculation_map = build_report_calculation_map(xml_text, formula_sheets)
    output_path = _injection_output_path(package, injection, Path(output_root), f"{safe_filename(report.name)[:32]}_report.xlsx")
    _progress(progress, f"Writing workbook: {injection.name}")
    return write_report_workbook(output_path, injection.name, formula_sheets, calculation_map=calculation_map)


def export_filled_report_template_workbook(
    package: CmbxPackage,
    injection: CmbxElement,
    report: CmbxElement,
    output_root: str | Path,
    progress=None,
    sheet_names: list[str] | None = None,
) -> Path:
    _progress(progress, f"Decoding report template: {report.name}")
    xml_text = _decode_report_xml_cached(package, report)
    sheets = parse_report_sheets(xml_text, report.name, injection.name)
    available_sheet_names = [sheet.sheet_name for sheet in sheets]
    target_sheet_names = _actual_report_sheet_names(sheet_names, available_sheet_names) if sheet_names is not None else report_export_sheet_names(injection.name, available_sheet_names)
    context = build_report_formula_context(package, injection)
    formula_sheets = {}
    for sheet_name in target_sheet_names:
        _progress(progress, f"Filling template sheet: {injection.name} / {sheet_name}")
        try:
            formula_sheets[sheet_name] = evaluate_report_formulas(package, injection, report.name, xml_text, sheet_name, context=context)
        except Exception as exc:
            _progress(progress, f"Skipping unavailable sheet formulas: {injection.name} / {sheet_name} ({exc})")
            formula_sheets[sheet_name] = []
    calculation_map = build_report_calculation_map(xml_text, formula_sheets)
    cell_values = build_report_cell_value_map(formula_sheets, calculation_map)
    output_path = _injection_output_path(package, injection, Path(output_root), formulaone_report_filename(injection.name))
    _progress(progress, f"Writing Chromeleon-style report: {injection.name}")
    return export_formulaone_report_template(output_path, xml_text, target_sheet_names, cell_values)


def _actual_report_sheet_names(requested: list[str] | None, available: list[str]) -> list[str]:
    if not requested:
        return available
    available_by_lower = {name.lower(): name for name in available}
    selected: list[str] = []
    for name in requested:
        actual = available_by_lower.get(str(name).strip().lower())
        if actual and actual not in selected:
            selected.append(actual)
    return selected or available


def export_sequence_report_sheets_workbook(package: CmbxPackage, sequence: CmbxElement, output_root: str | Path, progress=None) -> Path:
    report = next((child for child in sequence.children if child.kind == "report_template" and "ReportDefinition" in child.item_type), None)
    if not report:
        raise ValueError(f"No report definition was found for sequence: {sequence.name}")
    _progress(progress, f"Decoding report template: {report.name}")
    xml_text = _decode_report_xml_cached(package, report)
    template_sheets = parse_report_sheets(xml_text, report.name, "")
    available_sheet_names = [sheet.sheet_name for sheet in template_sheets]
    selected_sheet_names: list[str] = []
    merged_cell_values = {}
    injections = [child for child in sequence.children if child.kind == "injection"]
    total = len(injections)
    for index, injection in enumerate(injections, 1):
        _progress(progress, f"Evaluating sequence report {index}/{total}: {injection.name}")
        target_sheet_names = report_export_sheet_names(injection.name, available_sheet_names)
        for sheet_name in target_sheet_names:
            if sheet_name not in selected_sheet_names:
                selected_sheet_names.append(sheet_name)
        context = build_report_formula_context(package, injection)
        formula_sheets = {}
        for sheet_name in target_sheet_names:
            try:
                formula_sheets[sheet_name] = evaluate_report_formulas(package, injection, report.name, xml_text, sheet_name, context=context)
            except Exception as exc:
                _progress(progress, f"Skipping unavailable sheet formulas: {injection.name} / {sheet_name} ({exc})")
                formula_sheets[sheet_name] = []
        calculation_map = build_report_calculation_map(xml_text, formula_sheets)
        merged_cell_values.update(build_report_cell_value_map(formula_sheets, calculation_map))
    output_path = _element_sequence_output_path(package, sequence, Path(output_root)) / f"{safe_filename(sequence.name, 'sequence')}_report_sheets.xls"
    _progress(progress, f"Writing sequence report sheets: {sequence.name}")
    return export_formulaone_report_template(output_path, xml_text, selected_sheet_names, merged_cell_values)


def export_all_report_workbooks(package: CmbxPackage, output_root: str | Path, progress=None) -> list[Path]:
    paths: list[Path] = []
    total = len(package.injections)
    for index, injection in enumerate(package.injections, 1):
        sequence = package.elements_by_id.get(injection.parent_id or "")
        if not sequence:
            continue
        report = next((child for child in sequence.children if child.kind == "report_template" and "ReportDefinition" in child.item_type), None)
        if not report:
            continue
        _progress(progress, f"Exporting report {index}/{total}: {injection.name}")
        paths.append(export_report_workbook(package, injection, report, output_root, progress=progress))
    return paths


def export_foq_contract_report(
    package: CmbxPackage,
    mapping_path: str | Path,
    device_type: str,
    output_root: str | Path,
    progress=None,
    report_template_name: str = "",
    db_field_filter: str | list[str] | tuple[str, ...] = "",
) -> Path:
    mapping_sheet, values = evaluate_foq_contract_values(
        package,
        mapping_path,
        device_type,
        progress=progress,
        report_template_name=report_template_name,
        db_field_filter=db_field_filter,
    )
    sequence_name = _package_sequence_output_name(package)
    output_path = _package_sequence_output_path(package, Path(output_root)) / f"{safe_filename(sequence_name)}_FOQ_contract_DB.xlsx"
    _progress(progress, f"Writing FOQ contract workbook: {device_type}", 96)
    return write_foq_contract_workbook(output_path, device_type, mapping_sheet, values)


def evaluate_foq_contract_values(
    package: CmbxPackage,
    mapping_path: str | Path,
    device_type: str,
    progress=None,
    report_template_name: str = "",
    db_field_filter: str | list[str] | tuple[str, ...] = "",
    sequence: CmbxElement | None = None,
) -> tuple[str, list]:
    _progress(progress, f"Reading FOQ contract mapping: {device_type}", 2)
    mapping_sheet, locations = locations_for_device_type(mapping_path, device_type)
    locations = _filter_contract_locations_by_db_field(locations, db_field_filter)
    if not locations:
        raise ValueError(f"No FOQ mapping rows matched DB field filter: {db_field_filter}")
    target_injections = [child for child in sequence.children if child.kind == "injection"] if sequence else package.injections
    report_file_to_injection = _match_contract_injections(target_injections, locations)
    if not report_file_to_injection:
        raise ValueError("No CMBX injections matched the FOQ contract report files.")

    report = _sequence_report_template(package, report_template_name)
    if not report:
        raise ValueError("No report definition was found in the CMBX package.")
    _progress(progress, f"Decoding report template: {report.name}", 8)
    xml_text = _decode_report_xml_cached(package, report)
    _progress(progress, f"Indexing report formulas: {report.name}", 12)
    formula_objects_by_sheet: dict[str, list] = {}
    for obj in parse_report_sheet_objects(xml_text, report.name):
        if not obj.formula:
            continue
        formula_objects_by_sheet.setdefault(obj.sheet_name, []).append(obj)

    targets_by_injection: dict[str, set[str]] = {}
    injection_by_name = {injection.name: injection for injection in target_injections}
    for location in locations:
        injection_name = report_file_to_injection.get(_normalize_report_file(location.report_file))
        if not injection_name:
            continue
        targets_by_injection.setdefault(injection_name, set()).add(location.report_sheet)

    cell_values_by_injection = {}
    total = len(targets_by_injection)
    for index, (injection_name, sheet_names) in enumerate(targets_by_injection.items(), 1):
        injection = injection_by_name.get(injection_name)
        if not injection:
            continue
        percent = 12 + (index - 1) / max(total, 1) * 78
        _progress(progress, f"Evaluating FOQ contract {index}/{total}: {injection.name}", percent)
        context = build_report_formula_context(package, injection)
        formula_sheets = {}
        for sheet_name in sorted(sheet_names):
            formula_sheets[sheet_name] = evaluate_report_formula_objects(package, injection, formula_objects_by_sheet.get(sheet_name, []), report_name=report.name, context=context)
        calculation_map = build_report_calculation_map(xml_text, formula_sheets)
        cell_values = build_report_cell_value_map(formula_sheets, calculation_map)
        if not any(formula_sheets.values()):
            target_locations = [
                location
                for location in locations
                if report_file_to_injection.get(_normalize_report_file(location.report_file)) == injection.name
            ]
            cell_values.update(_formulaone_workbook_cell_values(xml_text, target_locations, progress=progress))
            cell_values.update(_legacy_foq_metadata_cell_values(package, injection, context, target_locations))
        cell_values_by_injection[injection.name] = cell_values

    values = resolve_contract_values(locations, cell_values_by_injection, report_file_to_injection)
    return mapping_sheet, values


def _filter_contract_locations_by_db_field(locations, db_field_filter: str | list[str] | tuple[str, ...]):
    if isinstance(db_field_filter, (list, tuple, set)):
        selected = [str(field or "").strip() for field in db_field_filter if str(field or "").strip()]
        if not selected:
            return locations
        selected_keys = {field.lower() for field in selected}
        return [location for location in locations if location.db_field.lower() in selected_keys]
    filter_text = str(db_field_filter or "").strip()
    if not filter_text:
        return locations
    exact = [location for location in locations if location.db_field.lower() == filter_text.lower()]
    if exact:
        return exact
    tokens = [token for token in re.split(r"[\s,;]+", filter_text.lower()) if token]
    if not tokens:
        return locations
    return [location for location in locations if all(token in location.db_field.lower() for token in tokens)]


def export_embedded_instrument_method(package: CmbxPackage, element: CmbxElement, embedded: EmbeddedMethodBlock, output_root: Path) -> list[Path]:
    block_path = _element_output_path(package, element, output_root, "_embedded.instmeth.bin")
    payload_path = _element_output_path(package, element, output_root, "_embedded_payload.bin")
    cpxm_path = _element_output_path(package, element, output_root, "_embedded_payload.cpxm.bin")
    xml_path = _element_output_path(package, element, output_root, "_embedded_method.xml")
    flow_path = _element_output_path(package, element, output_root, "_embedded_method_flow.txt")
    flow_tsv_path = _element_output_path(package, element, output_root, "_embedded_method_flow.tsv")
    metadata_path = _element_output_path(package, element, output_root, "_embedded_metadata.txt")
    block_path.parent.mkdir(parents=True, exist_ok=True)
    _remove_stale_method_exports(package, element, output_root)
    block_path.write_bytes(embedded.data)
    payload_path.write_bytes(embedded.method_payload)
    cpxm_path.write_bytes(embedded.cpxm_payload)
    decode_result = decode_cpxm_method_xml(cpxm_path, xml_path)
    metadata = embedded.metadata_text() + "\n\nDecode Status\n-------------\n" + decode_result.message
    metadata_path.write_text(metadata, encoding="utf-8")
    paths = [block_path, payload_path, cpxm_path]
    if decode_result.ok:
        xml_text = xml_path.read_text(encoding="utf-8")
        flow_path.write_text(build_method_flow_from_xml(xml_text, element.name), encoding="utf-8")
        flow_tsv_path.write_text(build_method_flow_tsv(xml_text, element.name), encoding="utf-8")
        paths.append(xml_path)
        paths.append(flow_path)
        paths.append(flow_tsv_path)
    paths.append(metadata_path)
    return paths


def export_embedded_report_template(package: CmbxPackage, element: CmbxElement, embedded: EmbeddedReportTemplate, output_root: Path) -> list[Path]:
    workbook_path = _element_output_path(package, element, output_root, "_report_template.xls")
    workbook_path.parent.mkdir(parents=True, exist_ok=True)
    _remove_stale_report_exports(package, element, output_root)
    _embedded, xml_text = decode_report_template_xml(package, element)
    export_formulaone_report_template(workbook_path, xml_text)
    return [workbook_path]


def export_embedded_object_summary(package: CmbxPackage, element: CmbxElement, output_root: str | Path) -> Path:
    output_base = Path(output_root)
    output_path = _element_output_path(package, element, output_base, "_summary.txt")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    summary = build_embedded_object_summary(package, element)
    output_path.write_text(_element_metadata_text(element) + "\n\n" + summary.to_text(), encoding="utf-8")
    for index, section in enumerate(summary.sections, 1):
        suffix = ".xml" if section.kind == "XML" else ".txt"
        section_path = output_path.with_name(f"{output_path.stem}_embedded_{index}{suffix}")
        section_path.write_text(section.text, encoding="utf-8")
    return output_path


def _remove_stale_method_exports(package: CmbxPackage, element: CmbxElement, output_root: Path) -> None:
    stale_paths = [
        _element_output_path(package, element, output_root, "_summary.txt"),
        _element_output_path(package, element, output_root, "_original_method.txt"),
        _element_output_path(package, element, output_root, "_method_flow.txt"),
        _element_output_path(package, element, output_root, "_embedded_method.xml"),
        _element_output_path(package, element, output_root, "_embedded_method_flow.txt"),
        _element_output_path(package, element, output_root, "_embedded_method_flow.tsv"),
    ]
    summary_path = stale_paths[0]
    embedded_pattern = f"{summary_path.stem}_embedded_*"
    for path in [*stale_paths, *summary_path.parent.glob(embedded_pattern)]:
        try:
            path.unlink(missing_ok=True)
        except OSError:
            pass


def _remove_stale_report_exports(package: CmbxPackage, element: CmbxElement, output_root: Path) -> None:
    stale_paths = [
        _element_output_path(package, element, output_root, "_summary.txt"),
        _element_output_path(package, element, output_root, "_embedded.report.bin"),
        _element_output_path(package, element, output_root, "_embedded_report.cpxm.bin"),
        _element_output_path(package, element, output_root, "_embedded_report.xml"),
        _element_output_path(package, element, output_root, "_report_template.xlsx"),
        _element_output_path(package, element, output_root, "_report_template.xls"),
        _element_output_path(package, element, output_root, "_report_sheets.tsv"),
        _element_output_path(package, element, output_root, "_report_sheet_objects.tsv"),
        _element_output_path(package, element, output_root, "_embedded_report_metadata.txt"),
    ]
    summary_path = stale_paths[0]
    embedded_pattern = f"{summary_path.stem}_embedded_*"
    for path in [*stale_paths, *summary_path.parent.glob(embedded_pattern)]:
        try:
            path.unlink(missing_ok=True)
        except OSError:
            pass


def _extract_raw_to_cache(package: CmbxPackage, element: CmbxElement, output_root: Path) -> Path:
    if not element.raw_filename:
        raise ValueError(f"Element has no raw file: {element.name}")
    raw_folder = _element_sequence_output_path(package, element, output_root) / "_raw_cache"
    raw_folder.mkdir(parents=True, exist_ok=True)
    raw_path = raw_folder / element.raw_filename
    raw_path.write_bytes(extract_cmbx_entry(package.path, element.raw_filename))
    return raw_path


def _element_sequence_output_path(package: CmbxPackage, element: CmbxElement, output_root: Path) -> Path:
    sequence = next((part for part in element_path(package, element) if part.kind == "sequence"), None)
    if sequence:
        return output_root / safe_filename(sequence.name, "sequence")
    return _package_sequence_output_path(package, output_root)


def _package_sequence_output_path(package: CmbxPackage, output_root: Path) -> Path:
    return output_root / safe_filename(_package_sequence_output_name(package), "sequence")


def _package_sequence_output_name(package: CmbxPackage) -> str:
    if package.sequences:
        return package.sequences[0].name
    return package.path.stem


def _element_output_path(package: CmbxPackage, element: CmbxElement, output_root: Path, suffix: str) -> Path:
    path_parts = element_path(package, element)
    sequence = next((part for part in path_parts if part.kind == "sequence"), None)
    injection = next((part for part in path_parts if part.kind == "injection"), None)
    folder = output_root
    if sequence:
        folder = folder / safe_filename(sequence.name, "sequence")
    if injection:
        folder = folder / safe_filename(injection.name, "injection")
    name = safe_filename(element.name, element.kind)
    if suffix.startswith("_"):
        return folder / f"{name}{suffix}"
    return folder / f"{name}{suffix}"


def _injection_output_path(package: CmbxPackage, injection: CmbxElement, output_root: Path, filename: str) -> Path:
    path_parts = element_path(package, injection)
    sequence = next((part for part in path_parts if part.kind == "sequence"), None)
    folder = output_root
    if sequence:
        folder = folder / safe_filename(sequence.name, "sequence")
    folder = folder / safe_filename(injection.name, "injection")
    return folder / filename


def _decode_report_xml_cached(package: CmbxPackage, report: CmbxElement) -> str:
    try:
        package_mtime = package.path.stat().st_mtime_ns
    except OSError:
        package_mtime = 0
    key = (str(package.path.resolve()), report.id, package_mtime)
    xml_text = _REPORT_XML_CACHE.get(key)
    if xml_text is None:
        _embedded, xml_text = decode_report_template_xml(package, report)
        _REPORT_XML_CACHE[key] = xml_text
    return xml_text


def _sequence_report_template(package: CmbxPackage, preferred_name: str = "") -> CmbxElement | None:
    preferred_key = str(preferred_name or "").strip().lower()
    reports: list[CmbxElement] = []
    for sequence in package.sequences:
        reports.extend(child for child in sequence.children if child.kind == "report_template" and "ReportDefinition" in child.item_type)
    reports.extend(element for element in package.methods_and_reports if element.kind == "report_template")
    if preferred_key:
        preferred = next((report for report in reports if report.name.strip().lower() == preferred_key), None)
        if preferred:
            return preferred
    return reports[0] if reports else None


def _match_contract_injections(injections: list[CmbxElement], locations) -> dict[str, str]:
    result: dict[str, str] = {}
    for location in locations:
        report_key = _normalize_report_file(location.report_file)
        if report_key in result:
            continue
        matched = _find_injection_for_report_file(injections, report_key)
        if matched:
            result[report_key] = matched.name
    return result


def _find_injection_for_report_file(injections: list[CmbxElement], report_key: str) -> CmbxElement | None:
    compact_report = _compact_name(report_key)
    for injection in injections:
        compact_injection = _compact_name(injection.name)
        if compact_report == compact_injection or compact_report in compact_injection or compact_injection in compact_report:
            return injection
    return None


def _formulaone_workbook_cell_values(xml_text: str, locations, progress=None) -> dict[tuple[str, str], ReportCellValue]:
    if not locations:
        return {}
    try:
        import xlrd
    except ImportError:
        return {}
    sheet_names = sorted({location.report_sheet for location in locations if location.report_sheet})
    values: dict[tuple[str, str], ReportCellValue] = {}
    with tempfile.TemporaryDirectory(prefix="cmbx_formulaone_contract_") as tmp:
        workbook_path = Path(tmp) / "formulaone_contract.xls"
        try:
            _progress(progress, "Falling back to FormulaOne workbook cell extraction")
            export_formulaone_report_template(workbook_path, xml_text, sheet_names)
            workbook = xlrd.open_workbook(str(workbook_path), on_demand=True)
        except Exception as exc:
            _progress(progress, f"FormulaOne workbook fallback unavailable: {exc}")
            return {}
        available = {name.lower(): name for name in workbook.sheet_names()}
        for location in locations:
            actual_sheet = available.get(str(location.report_sheet or "").lower())
            if not actual_sheet:
                continue
            parsed = _cell_to_indexes(location.report_cell)
            if not parsed:
                continue
            row_index, col_index = parsed
            sheet = workbook.sheet_by_name(actual_sheet)
            if row_index >= sheet.nrows or col_index >= sheet.ncols:
                continue
            value = sheet.cell_value(row_index, col_index)
            values[(location.report_sheet.strip().lower(), location.report_cell.strip().upper())] = ReportCellValue(
                sheet_name=location.report_sheet,
                cell=location.report_cell.strip().upper(),
                value=value,
                status="ok",
                detail="Read from exported FormulaOne workbook fallback.",
            )
    return values


def _legacy_foq_metadata_cell_values(package: CmbxPackage, injection: CmbxElement, context, locations) -> dict[tuple[str, str], ReportCellValue]:
    if not locations:
        return {}
    values_by_field = {
        "TestDate": _eval_metadata_formula(package, injection, "seq.update_time") or "",
        "TimeBase": _eval_metadata_formula(package, injection, "seq.timebase") or _audit_timebase(context.audit_records),
        "ModelNo": _audit_suffix_value(context.audit_records, "ColumnComp.ModelNo") or _audit_any_property_value(context.audit_records, "ModelNo"),
        "Serial": _audit_suffix_value(context.audit_records, "ColumnComp.SerialNo") or _audit_any_property_value(context.audit_records, "SerialNo"),
        "HardwareVersion": _audit_suffix_value(context.audit_records, "ColumnComp.HardwareVersion"),
        "Firmware": _audit_suffix_value(context.audit_records, "ColumnComp.FirmwareVersion"),
        "ModelVariant": _format_model_variant(_audit_suffix_value(context.audit_records, "ColumnComp.ModuleHardwareRevision")),
    }
    rows: dict[tuple[str, str], ReportCellValue] = {}
    for location in locations:
        if location.db_field not in values_by_field:
            continue
        value = values_by_field.get(location.db_field, "")
        if value in {None, ""}:
            continue
        rows[(location.report_sheet.strip().lower(), location.report_cell.strip().upper())] = ReportCellValue(
            sheet_name=location.report_sheet,
            cell=location.report_cell.strip().upper(),
            value=value,
            status="ok",
            detail="Resolved by legacy FOQ metadata fallback from audit/precondition/sequence metadata.",
        )
    return rows


def _audit_suffix_value(records, wanted_path: str) -> str:
    wanted = wanted_path.lower()
    for record in records:
        record_path = f"{record.device}.{record.property_name}".lower()
        if (record_path == wanted or record_path.endswith("." + wanted)) and record.property_value:
            return record.property_value
    return ""


def _audit_any_property_value(records, property_name: str) -> str:
    wanted = property_name.lower()
    for record in records:
        if record.property_name.lower() == wanted and record.property_value:
            return record.property_value
    return ""


def _audit_timebase(records) -> str:
    for record in records:
        match = re.search(r"\bon instrument\s+(.+?)(?:\.?$|\s{2,})", record.message, flags=re.IGNORECASE)
        if match:
            return re.sub(r"\s+\(server\b.*$", "", match.group(1).strip().rstrip("."), flags=re.IGNORECASE)
    return ""


def _format_model_variant(value: str) -> str:
    text = str(value or "").strip()
    try:
        return f"{int(float(text)):02d}"
    except ValueError:
        return text


def _cell_to_indexes(cell: str) -> tuple[int, int] | None:
    match = re.fullmatch(r"([A-Z]+)([0-9]+)", str(cell or "").strip().upper())
    if not match:
        return None
    column = 0
    for char in match.group(1):
        column = column * 26 + ord(char) - 64
    return int(match.group(2)) - 1, column - 1


def _normalize_report_file(value: str) -> str:
    text = str(value or "").strip().lower()
    for suffix in (".xlsx", ".xls"):
        if text.endswith(suffix):
            return text[: -len(suffix)]
    return text


def _compact_name(value: str) -> str:
    return "".join(ch for ch in _normalize_report_file(value).lower() if ch.isalnum())


def _progress(callback, message: str, percent: float | None = None) -> None:
    if callback:
        if percent is not None:
            callback(f"__PROGRESS__={max(0, min(100, percent)):.1f}|{message}")
            return
        callback(message)


def _element_metadata_text(element: CmbxElement) -> str:
    return "\n".join(
        [
            f"Name: {element.name}",
            f"Kind: {element.kind}",
            f"ItemType: {element.item_type}",
            f"URL: {element.url}",
            f"RawDataFilename: {element.raw_filename}",
            f"Filename: {element.filename}",
            f"Size: {element.size if element.size is not None else ''}",
            f"RawDataFileId: {element.raw_data_file_id}",
            "",
            "Note: this CMBX header object does not expose an independent package entry. "
            "Its full definition may be stored inside the sequence command object.",
        ]
    )
