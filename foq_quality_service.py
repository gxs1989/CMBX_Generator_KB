from __future__ import annotations

import math
import re
import statistics
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Iterable

from cmbx_container import CmbxElement, CmbxPackage, load_cmbx_package
from db_upload_service import DatabaseUploadConfig, fetch_table_rows
from export_service import evaluate_foq_contract_values
from foq_result_locations import load_foq_workbook, locations_for_device_type, read_device_type_mappings
from report_formula_evaluator import build_report_formula_context


PASS_WORDS = {"ok", "pass", "passed", "test passed", "true", "yes"}
FAIL_WORDS = {"fail", "failed", "test failed", "false", "no", "not ok"}


@dataclass(frozen=True)
class FoqSequenceCandidate:
    package: CmbxPackage
    sequence: CmbxElement
    device: str
    device_source: str
    report_template: str


@dataclass(frozen=True)
class FoqSequenceInventory:
    package: CmbxPackage
    sequence: CmbxElement
    device: str
    device_source: str
    report_template: str
    eligible: bool
    reason: str

    @property
    def candidate(self) -> FoqSequenceCandidate | None:
        if not self.eligible:
            return None
        return FoqSequenceCandidate(
            self.package,
            self.sequence,
            self.device,
            self.device_source,
            self.report_template,
        )


@dataclass(frozen=True)
class HistoricalSummary:
    count: int = 0
    mean: float | None = None
    stdev: float | None = None
    minimum: float | None = None
    maximum: float | None = None
    ucl: float | None = None
    lcl: float | None = None


@dataclass(frozen=True)
class FoqMetricResult:
    package: str
    sequence: str
    device: str
    db_field: str
    description: str
    value: object
    unit: str
    calculation_status: str
    spec_status: str
    spec_evidence: str
    report_sheet: str
    report_cell: str
    injection: str
    detail: str
    history: HistoricalSummary = HistoricalSummary()
    history_delta: float | None = None
    history_z: float | None = None
    history_status: str = "not-loaded"


def default_mapping_path() -> Path:
    candidates = (
        Path(r"C:\ProgramData\CMBX Data Explorer Workspace\DB MAPPING\FOQResultLocations_V2.83.xls"),
        Path(__file__).resolve().parent.parent / "foq" / "FOQResultLocations_V2.83.xls",
    )
    return next((path for path in candidates if path.exists()), candidates[0])


def discover_foq_candidates(paths: Iterable[str | Path], mapping_path: str | Path) -> tuple[list[FoqSequenceCandidate], list[tuple[Path, str]]]:
    inventory, errors = inspect_foq_sources(paths, mapping_path)
    return [item.candidate for item in inventory if item.candidate is not None], errors


def inspect_foq_sources(paths: Iterable[str | Path], mapping_path: str | Path) -> tuple[list[FoqSequenceInventory], list[tuple[Path, str]]]:
    inventory: list[FoqSequenceInventory] = []
    errors: list[tuple[Path, str]] = []
    lookup = _device_lookup(mapping_path)
    for source in paths:
        path = Path(source)
        try:
            package = load_cmbx_package(path)
            sequence_evidence = [(sequence, *detect_sequence_device(package, sequence, lookup)) for sequence in package.sequences]
            package_devices = sorted({device for _sequence, device, _source in sequence_evidence if device != "unresolved"})
            for sequence, device, source_text in sequence_evidence:
                report = _preferred_report_template(sequence)
                # AdditionalInjections and similar support sequences contain reusable methods/injections,
                # but no completed report contract. They are not independent FOQ result candidates.
                if not report:
                    inventory.append(FoqSequenceInventory(package, sequence, device, source_text, "", False, "Support/template sequence: no report template"))
                    continue
                if device == "unresolved" and len(package_devices) == 1:
                    device = package_devices[0]
                    source_text = f"inherited from completed sequence in {path.name}"
                eligible = device != "unresolved"
                reason = "Ready" if eligible else "ModelNo not found"
                inventory.append(FoqSequenceInventory(package, sequence, device, source_text, report, eligible, reason))
        except Exception as exc:
            errors.append((path, str(exc)))
    return inventory, errors


def detect_sequence_device(package: CmbxPackage, sequence: CmbxElement, lookup: dict[str, str] | None = None) -> tuple[str, str]:
    lookup = lookup or {}
    injections = [child for child in sequence.children if child.kind == "injection"]
    for injection in injections:
        try:
            context = build_report_formula_context(package, injection)
        except Exception:
            continue
        for record in context.audit_records:
            path = f"{record.device}.{record.property_name}"
            if "modelno" not in path.lower():
                continue
            device = normalize_device(record.property_value, lookup)
            if device:
                source = "audit precondition" if record.retention_time_min is None else f"audit {record.retention_time_min:.6g} min"
                return device, f"{source}: {path}"
    return "unresolved", "AUDIT.ColumnComp.ModelNo was not found"


def normalize_device(value: object, lookup: dict[str, str] | None = None) -> str:
    text = str(value or "").strip().strip("'\"").upper().replace("_", "-")
    if not text:
        return ""
    lookup = lookup or {}
    if text in lookup:
        return lookup[text]
    for key, device in sorted(lookup.items(), key=lambda item: len(item[0]), reverse=True):
        if key in text:
            return device
    match = re.search(r"\bV[A-Z]-[A-Z0-9]{2,4}-[A-Z0-9]{1,4}\b", text)
    return match.group(0) if match else ""


def evaluate_candidate(
    candidate: FoqSequenceCandidate,
    mapping_path: str | Path,
    progress=None,
    db_fields: Iterable[str] | None = None,
    selected_injection_ids: Iterable[str] | None = None,
) -> list[FoqMetricResult]:
    if not candidate.device or candidate.device == "unresolved":
        raise ValueError(f"{candidate.sequence.name}: device is unresolved; AUDIT.ColumnComp.ModelNo is required")
    requested = {str(field).strip().lower() for field in (db_fields or []) if str(field).strip()}
    evaluation_fields = expand_metric_dependencies(mapping_path, candidate.device, requested) if requested else []
    _mapping_sheet, values = evaluate_foq_contract_values(
        candidate.package,
        mapping_path,
        candidate.device,
        progress=progress,
        report_template_name=candidate.report_template,
        db_field_filter=evaluation_fields,
        sequence=candidate.sequence,
        selected_injection_ids=None if selected_injection_ids is None else list(selected_injection_ids),
    )
    result_by_sheet = _result_status_by_sheet(values)
    rows: list[FoqMetricResult] = []
    for contract in values:
        location = contract.location
        own_status = classify_result_value(contract.value) if location.db_field.upper().startswith("RES_") else ""
        spec_status, evidence = result_by_sheet.get(location.report_sheet.strip().lower(), ("not-evaluated", "No mapped RES_* result for this report sheet"))
        if own_status:
            spec_status, evidence = own_status, location.db_field
        calculation_status = "ok" if str(contract.status).lower() == "ok" else str(contract.status)
        rows.append(
            FoqMetricResult(
                package=candidate.package.path.name,
                sequence=candidate.sequence.name,
                device=candidate.device,
                db_field=location.db_field,
                description=location.description,
                value=contract.value,
                unit=location.unit if location.unit.upper() != "NO SEARCH RESULT" else "",
                calculation_status=calculation_status,
                spec_status=spec_status,
                spec_evidence=evidence,
                report_sheet=location.report_sheet,
                report_cell=location.report_cell,
                injection=contract.injection_name,
                detail=contract.detail,
            )
        )
    return [row for row in rows if not requested or row.db_field.lower() in requested]


def attach_history(rows: Iterable[FoqMetricResult], history_rows: Iterable[dict[str, object]]) -> list[FoqMetricResult]:
    history = list(history_rows)
    output: list[FoqMetricResult] = []
    for row in rows:
        scoped, _scope = filter_history_for_device(history, row.device)
        values = [number for item in scoped if (number := coerce_number(_case_value(item, row.db_field))) is not None]
        summary = summarize_history(values)
        current = coerce_number(row.value)
        delta = current - summary.mean if current is not None and summary.mean is not None else None
        z = None
        status = "insufficient-data"
        if current is not None and summary.count:
            status = "within-history"
            if summary.stdev and summary.stdev > 0:
                z = delta / summary.stdev
                status = "outside-3sigma" if abs(z) > 3 else ("outside-2sigma" if abs(z) > 2 else "within-history")
        output.append(FoqMetricResult(**{**row.__dict__, "history": summary, "history_delta": delta, "history_z": z, "history_status": status}))
    return output


def filter_history_for_device(history_rows: Iterable[dict[str, object]], device: str) -> tuple[list[dict[str, object]], str]:
    """Keep one model family together when the database table stores several device types."""
    rows = list(history_rows)
    device_fields = ("ModelNo", "Device", "DeviceType", "Module", "InstrumentModel")
    available = next((field for field in device_fields if any(_case_value(row, field) not in (None, "") for row in rows)), "")
    if not available:
        return rows, "whole table (no device column found)"
    target = normalize_device(device)
    filtered = [row for row in rows if normalize_device(_case_value(row, available)) == target]
    return filtered, f"{available} = {target}"


def metric_catalog_for_devices(mapping_path: str | Path, devices: Iterable[str]) -> list[str]:
    """Return every measurable DB field available to any selected device model."""
    field_sets: list[set[str]] = []
    display_names: dict[str, str] = {}
    for device in sorted({str(value).strip() for value in devices if str(value).strip() and value != "unresolved"}):
        _sheet, locations = locations_for_device_type(mapping_path, device)
        fields = set()
        for location in locations:
            if location.db_field.upper().startswith("RES_"):
                continue
            unit = location.unit.strip().upper()
            if not unit or unit == "NO SEARCH RESULT":
                continue
            key = location.db_field.lower()
            fields.add(key)
            display_names.setdefault(key, location.db_field)
        field_sets.append(fields)
    if not field_sets:
        return []
    available = set.union(*field_sets)
    return sorted((display_names[key] for key in available), key=str.lower)


def expand_metric_dependencies(mapping_path: str | Path, device: str, requested_fields: Iterable[str]) -> list[str]:
    """Include the mapped RES_* cell needed to preserve each metric's SPEC decision."""
    requested = {str(field).strip().lower() for field in requested_fields if str(field).strip()}
    if not requested:
        return []
    _sheet, locations = locations_for_device_type(mapping_path, device)
    sheets = {location.report_sheet.strip().lower() for location in locations if location.db_field.lower() in requested}
    fields = {location.db_field for location in locations if location.db_field.lower() in requested}
    fields.update(
        location.db_field
        for location in locations
        if location.report_sheet.strip().lower() in sheets and location.db_field.upper().startswith("RES_")
    )
    return sorted(fields, key=str.lower)


def filter_database_rows(rows: Iterable[dict[str, object]], filters: dict[str, str]) -> list[dict[str, object]]:
    output = list(rows)
    exact_fields = {"model": ("ModelNo", "Device", "DeviceType"), "variant": ("ModelVariant",), "timebase": ("TimeBase",)}
    for filter_name, candidates in exact_fields.items():
        wanted = {token.strip().lower() for token in re.split(r"[,;]", filters.get(filter_name, "")) if token.strip()}
        if not wanted:
            continue
        output = [row for row in output if str(_first_case_value(row, candidates) or "").strip().lower() in wanted]
    start = _parse_date(filters.get("date_from", ""))
    end = _parse_date(filters.get("date_to", ""))
    if start or end:
        dated = []
        for row in output:
            value = _parse_date(_case_value(row, "TestDate"))
            if value is None:
                continue
            if start and value < start:
                continue
            if end and value > end:
                continue
            dated.append(row)
        output = dated
    return output


def summarize_history(values: Iterable[float]) -> HistoricalSummary:
    numbers = [float(value) for value in values if math.isfinite(float(value))]
    if not numbers:
        return HistoricalSummary()
    mean = statistics.fmean(numbers)
    stdev = statistics.stdev(numbers) if len(numbers) > 1 else 0.0
    return HistoricalSummary(len(numbers), mean, stdev, min(numbers), max(numbers), mean + 3 * stdev, mean - 3 * stdev)


def read_historical_rows(config: DatabaseUploadConfig, device: str = "", limit: int = 5000) -> list[dict[str, object]]:
    table = config.table
    if not table or table.upper() == "AUTO":
        from db_upload_service import FOQ_TABLE_BY_DEVICE_TYPE

        table = FOQ_TABLE_BY_DEVICE_TYPE.get(device.upper(), "VTCC")
    return fetch_table_rows(config, table=table, limit=limit)


def classify_result_value(value: object) -> str:
    text = re.sub(r"\s+", " ", str(value or "").strip().lower())
    if text in PASS_WORDS or ("pass" in text and "fail" not in text):
        return "pass"
    if text in FAIL_WORDS or "fail" in text:
        return "fail"
    if not text:
        return "not-evaluated"
    return "review"


def coerce_number(value: object) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value or "").strip().replace(",", "")
    try:
        return float(text)
    except ValueError:
        return None


def _result_status_by_sheet(values) -> dict[str, tuple[str, str]]:
    rows: dict[str, tuple[str, str]] = {}
    for contract in values:
        field = contract.location.db_field
        if not field.upper().startswith("RES_"):
            continue
        key = contract.location.report_sheet.strip().lower()
        status = classify_result_value(contract.value)
        previous = rows.get(key)
        if previous and previous[0] == "fail":
            continue
        if status == "fail" or not previous:
            rows[key] = (status, field)
    return rows


def _device_lookup(mapping_path: str | Path) -> dict[str, str]:
    try:
        workbook = load_foq_workbook(mapping_path)
        mappings = read_device_type_mappings(workbook)
    except Exception:
        return {}
    return {key.upper().replace("_", "-"): value.device_type for key, value in mappings.items()}


def _preferred_report_template(sequence: CmbxElement) -> str:
    reports = [child for child in sequence.children if child.kind == "report_template"]
    if not reports:
        return ""
    report = next((item for item in reports if "reportdefinition" in item.item_type.lower() and item.name.lower() != "default"), None)
    report = report or next((item for item in reports if item.name.lower() != "default"), reports[0])
    return report.name


def _case_value(row: dict[str, object], field: str) -> object:
    key = field.lower()
    return next((value for name, value in row.items() if str(name).lower() == key), None)


def _first_case_value(row: dict[str, object], fields: Iterable[str]) -> object:
    for field in fields:
        value = _case_value(row, field)
        if value not in (None, ""):
            return value
    return None


def _parse_date(value: object) -> date | None:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    text = str(value or "").strip()
    if not text:
        return None
    for candidate in (text, text[:10]):
        try:
            return datetime.fromisoformat(candidate).date()
        except ValueError:
            pass
    return None
