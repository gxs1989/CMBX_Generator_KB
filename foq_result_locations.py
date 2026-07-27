from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DeviceTypeMapping:
    device_type: str
    sheet_name: str


@dataclass(frozen=True)
class FoqResultLocation:
    row_id: int | None
    db_field: str
    description: str
    report_value: str
    lower_limit: str
    upper_limit: str
    limit_check: str
    report_file: str
    report_sheet: str
    report_cell: str
    value_type: str
    unit: str

    @property
    def report_key(self) -> tuple[str, str, str]:
        return (_normalize_report_file(self.report_file), self.report_sheet.strip().lower(), self.report_cell.strip().upper())


def load_foq_workbook(path: str | Path):
    import xlrd

    return xlrd.open_workbook(path)


def read_device_type_mappings(workbook) -> dict[str, DeviceTypeMapping]:
    if "DeviceTypes" not in workbook.sheet_names():
        return {}
    sheet = workbook.sheet_by_name("DeviceTypes")
    rows: dict[str, DeviceTypeMapping] = {}
    for row_index in range(1, sheet.nrows):
        device_type = _cell_text(sheet, row_index, 1)
        sheet_name = _cell_text(sheet, row_index, 2)
        if device_type and sheet_name:
            rows[device_type.upper()] = DeviceTypeMapping(device_type=device_type, sheet_name=sheet_name)
    return rows


def resolve_mapping_sheet_for_device_type(workbook, device_type: str) -> str | None:
    mappings = read_device_type_mappings(workbook)
    mapping = mappings.get(str(device_type or "").strip().upper())
    return mapping.sheet_name if mapping else None


def read_result_locations(workbook, sheet_name: str) -> list[FoqResultLocation]:
    sheet = workbook.sheet_by_name(sheet_name)
    headers = [_cell_text(sheet, 0, col) for col in range(sheet.ncols)]
    by_name = {header: index for index, header in enumerate(headers)}

    def value(row_index: int, name: str) -> str:
        col_index = by_name.get(name)
        if col_index is None:
            return ""
        return _cell_text(sheet, row_index, col_index)

    rows: list[FoqResultLocation] = []
    for row_index in range(1, sheet.nrows):
        db_field = value(row_index, "dbField")
        report_file = value(row_index, "xlsReportFile")
        report_sheet = value(row_index, "xlsReportSheet")
        report_cell = value(row_index, "xlsReportCell")
        if not db_field or not report_file or not report_sheet or not report_cell:
            continue
        rows.append(
            FoqResultLocation(
                row_id=_cell_int(sheet, row_index, by_name.get("ID")),
                db_field=db_field,
                description=value(row_index, "Description"),
                report_value=value(row_index, "ReportValue"),
                lower_limit=value(row_index, "LowerLimit"),
                upper_limit=value(row_index, "UpperLimit"),
                limit_check=value(row_index, "LimitCheck"),
                report_file=report_file,
                report_sheet=report_sheet,
                report_cell=report_cell,
                value_type=value(row_index, "ValueType"),
                unit=value(row_index, "Unit"),
            )
        )
    return rows


def locations_for_device_type(path: str | Path, device_type: str) -> tuple[str, list[FoqResultLocation]]:
    workbook = load_foq_workbook(path)
    sheet_name = resolve_mapping_sheet_for_device_type(workbook, device_type)
    if not sheet_name:
        raise KeyError(f"Device type not found in FOQResultLocations DeviceTypes: {device_type}")
    return sheet_name, read_result_locations(workbook, sheet_name)


def filter_locations_for_report(
    locations: list[FoqResultLocation],
    report_file: str = "",
    report_sheet: str = "",
) -> list[FoqResultLocation]:
    file_key = _normalize_report_file(report_file) if report_file else ""
    sheet_key = report_sheet.strip().lower() if report_sheet else ""
    rows = []
    for row in locations:
        if file_key and _normalize_report_file(row.report_file) != file_key:
            continue
        if sheet_key and row.report_sheet.strip().lower() != sheet_key:
            continue
        rows.append(row)
    return rows


def summarize_locations(locations: list[FoqResultLocation]) -> dict[str, int]:
    by_sheet: set[tuple[str, str]] = set()
    result_fields = 0
    numeric_fields = 0
    for row in locations:
        by_sheet.add((_normalize_report_file(row.report_file), row.report_sheet))
        if row.db_field.upper().startswith("RES_"):
            result_fields += 1
        if row.unit and row.unit.upper() != "NO SEARCH RESULT":
            numeric_fields += 1
    return {
        "fields": len(locations),
        "report_sheets": len(by_sheet),
        "result_fields": result_fields,
        "numeric_fields": numeric_fields,
    }


def _cell_text(sheet, row_index: int, col_index: int | None) -> str:
    if col_index is None or col_index < 0 or col_index >= sheet.ncols or row_index < 0 or row_index >= sheet.nrows:
        return ""
    value = sheet.cell_value(row_index, col_index)
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value).strip()


def _cell_int(sheet, row_index: int, col_index: int | None) -> int | None:
    text = _cell_text(sheet, row_index, col_index)
    try:
        return int(float(text))
    except ValueError:
        return None


def _normalize_report_file(value: str) -> str:
    text = str(value or "").strip().lower()
    for suffix in (".xlsx", ".xls"):
        if text.endswith(suffix):
            return text[: -len(suffix)]
    return text
