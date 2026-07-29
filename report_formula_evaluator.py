from __future__ import annotations

import re
import statistics
import tempfile
from datetime import datetime
from dataclasses import dataclass
from pathlib import Path

from chromeleon_bridge import export_audit_raw, export_signal_raw
from cmbx_container import CmbxElement, CmbxPackage, extract_cmbx_entry, safe_filename
from embedded_report_extractor import ReportSheetObject, parse_report_sheet_objects


@dataclass(frozen=True)
class SignalPoint:
    time_min: float
    value: float


@dataclass(frozen=True)
class AuditRecord:
    retention_time_min: float | None
    device: str
    property_name: str
    property_value: str
    message: str = ""


@dataclass(frozen=True)
class FormulaEvaluation:
    report_name: str
    injection_name: str
    sheet_name: str
    excel_range: str
    object_type: str
    fixed_channel: str
    formula: str
    value: str
    status: str
    detail: str


@dataclass
class ReportFormulaEvaluationContext:
    cache: Path
    audit_records: list[AuditRecord]
    ret_times: dict[int, float]
    signal_cache: dict[str, list[SignalPoint]]
    audit_source_injection: str = ""


def build_report_formula_context(package: CmbxPackage, injection: CmbxElement) -> ReportFormulaEvaluationContext:
    cache = _formula_cache_folder(package, injection)
    audit_source = _audit_source_injection(package, injection)
    audit_records = _export_and_read_audit_records(package, audit_source, cache) if audit_source else []
    return ReportFormulaEvaluationContext(
        cache=cache,
        audit_records=audit_records,
        ret_times=audit_ret_times(audit_records),
        signal_cache={},
        audit_source_injection=audit_source.name if audit_source else "",
    )


def load_injection_signal(
    package: CmbxPackage,
    injection: CmbxElement,
    channel_name: str,
    context: ReportFormulaEvaluationContext | None = None,
) -> list[SignalPoint]:
    """Load one injection signal through the shared Chromeleon raw-data bridge."""
    context = context or build_report_formula_context(package, injection)
    if channel_name not in context.signal_cache:
        context.signal_cache[channel_name] = _export_and_read_signal(
            package,
            injection,
            channel_name,
            context.cache,
        )
    return context.signal_cache[channel_name]


def evaluate_external_report_formula(
    package: CmbxPackage,
    injection: CmbxElement,
    formula: str,
    fixed_channel: str = "",
    context: ReportFormulaEvaluationContext | None = None,
) -> tuple[str, str, str]:
    """Evaluate the verified formula subset used by the External Report Engine."""
    expression = formula.strip()
    metadata = _eval_metadata_formula(package, injection, expression)
    if metadata is not None:
        return metadata, "ok", "Package/injection metadata."
    context = context or build_report_formula_context(package, injection)
    audit_metadata = evaluate_audit_metadata_formula(expression, context.audit_records)
    if audit_metadata is not None:
        value, detail = audit_metadata
        return value, "ok" if value != "" else "missing-data", detail
    ret_time = _eval_ret_time_formula(expression, context.ret_times)
    if ret_time is not None:
        return f"{ret_time:.12g}", "ok", "RetTime value read from injection audit trail."
    time_value = _eval_time_expr(expression, context.ret_times)
    if time_value is not None and "rettime" in expression.lower():
        return f"{time_value:.12g}", "ok", "Time expression evaluated from injection audit RetTimes."
    audit_value = evaluate_audit_property_formula(expression, context.ret_times, context.audit_records)
    if audit_value is not None:
        value, detail = audit_value
        return value, "ok" if value != "" else "missing-data", detail
    if expression.lower().startswith(("chm.sig_value", "chm.signalstatistic", "chm.signalvalue", "chm.noise", "chm.drift")):
        if not fixed_channel:
            return "", "missing-channel", "Signal formula requires a channel."
        signal = load_injection_signal(package, injection, fixed_channel, context)
        lowered = expression.lower()
        if lowered.startswith(("chm.sig_value", "chm.signalstatistic")):
            return evaluate_chm_signal_formula(expression, fixed_channel, context.ret_times, signal)
        if lowered.startswith("chm.signalvalue"):
            return evaluate_chm_signal_value(expression, fixed_channel, context.ret_times, signal)
        if lowered.startswith("chm.noise"):
            return evaluate_chm_noise(expression, fixed_channel, context.ret_times, signal)
        return evaluate_chm_drift(expression, fixed_channel, context.ret_times, signal)
    return "", "unsupported", "External Report Engine does not implement this CM expression."


def evaluate_report_formulas(
    package: CmbxPackage,
    injection: CmbxElement,
    report_name: str,
    report_xml: str,
    sheet_name: str = "",
    context: ReportFormulaEvaluationContext | None = None,
) -> list[FormulaEvaluation]:
    objects = [obj for obj in parse_report_sheet_objects(report_xml, report_name, sheet_name) if obj.formula]
    return evaluate_report_formula_objects(package, injection, objects, report_name=report_name, context=context)


def evaluate_report_formula_objects(
    package: CmbxPackage,
    injection: CmbxElement,
    objects: list[ReportSheetObject],
    report_name: str = "",
    context: ReportFormulaEvaluationContext | None = None,
) -> list[FormulaEvaluation]:
    objects = [obj for obj in objects if obj.formula]
    if not objects:
        return []
    context = context or build_report_formula_context(package, injection)
    rows: list[FormulaEvaluation] = []
    for obj in objects:
        value, status, detail = _evaluate_formula_object(
            package,
            injection,
            context.cache,
            obj,
            context.ret_times,
            context.audit_records,
            context.signal_cache,
        )
        rows.append(
            FormulaEvaluation(
                report_name=report_name,
                injection_name=injection.name,
                sheet_name=obj.sheet_name,
                excel_range=obj.excel_range,
                object_type=obj.object_type,
                fixed_channel=obj.fixed_channel,
                formula=obj.formula,
                value=value,
                status=status,
                detail=detail,
            )
        )
    return rows


def formula_evaluations_tsv(rows: list[FormulaEvaluation]) -> str:
    header = [
        "Report",
        "Injection",
        "Sheet",
        "ExcelRange",
        "ObjectType",
        "FixedChannel",
        "Formula",
        "Value",
        "Status",
        "Detail",
    ]
    lines = ["\t".join(header)]
    for row in rows:
        lines.append(
            _tsv_row(
                [
                    row.report_name,
                    row.injection_name,
                    row.sheet_name,
                    row.excel_range,
                    row.object_type,
                    row.fixed_channel,
                    row.formula,
                    row.value,
                    row.status,
                    row.detail,
                ]
            )
        )
    return "\n".join(lines)


def read_signal_tsv(path: str | Path) -> list[SignalPoint]:
    points: list[SignalPoint] = []
    in_data = False
    for raw_line in Path(path).read_text(encoding="utf-8-sig", errors="ignore").splitlines():
        if raw_line.startswith("Time (min)"):
            in_data = True
            continue
        if not in_data:
            continue
        parts = raw_line.split("\t")
        if len(parts) < 3:
            continue
        try:
            points.append(SignalPoint(float(parts[0]), float(parts[2])))
        except ValueError:
            continue
    return points


def read_audit_ret_times_tsv(path: str | Path) -> dict[int, float]:
    return audit_ret_times(read_audit_records_tsv(path))


def read_audit_records_tsv(path: str | Path) -> list[AuditRecord]:
    text = Path(path).read_text(encoding="utf-8-sig", errors="ignore")
    records: list[AuditRecord] = []
    for line in text.splitlines():
        parts = line.split("\t")
        if len(parts) < 7 or parts[0] == "Index":
            continue
        try:
            retention_time = float(parts[1]) if parts[1].strip() else None
        except ValueError:
            retention_time = None
        records.append(
            AuditRecord(
                retention_time_min=retention_time,
                device=parts[2].strip(),
                property_name=parts[5].strip(),
                property_value=parts[6].strip(),
                message=parts[3].strip(),
            )
        )
    return records


def audit_ret_times(records: list[AuditRecord]) -> dict[int, float]:
    ret_times: dict[int, float] = {}
    for record in records:
        if record.device.lower() != "rettimes":
            continue
        match = re.fullmatch(r"RetTime(\d+)", record.property_name, flags=re.IGNORECASE)
        if not match:
            continue
        try:
            value = float(record.property_value)
        except ValueError:
            continue
        if value > 0:
            ret_times[int(match.group(1))] = value
    return ret_times


def evaluate_chm_signal_formula(formula: str, fixed_channel: str, ret_times: dict[int, float], signal: list[SignalPoint]) -> tuple[str, str, str]:
    args = _function_args(formula.strip(), "chm.sig_value")
    function_name = "chm.sig_value"
    if not args:
        args = _function_args(formula.strip(), "chm.signalStatistic")
        function_name = "chm.signalStatistic"
    if not args:
        return "", "unsupported", "Only chm.sig_value(...) and chm.signalStatistic(...) are implemented here."
    operation = args[0].strip().strip('"').lower()
    if operation not in {"average", "avg", "min", "max", "drift", "stddev", "stdev"}:
        return "", "unsupported", f"Unsupported {function_name} operation: {operation}"
    start, end = _signal_window(args, ret_times, signal)
    if start is None or end is None:
        return "", "missing-ret-time", "Formula references a RetTime value that was not found in the audit trail."
    points = _signal_points_in_window(signal, start, end)
    values = [point.value for point in points]
    if not values:
        return "", "no-points", f"No {fixed_channel} signal points in {start:.6g}..{end:.6g} min."
    if operation in {"average", "avg"}:
        value = sum(values) / len(values)
    elif operation == "min":
        value = min(values)
    elif operation == "max":
        value = max(values)
    elif operation in {"stddev", "stdev"}:
        value = statistics.stdev(values) if len(values) > 1 else 0.0
    else:
        value = _signal_statistic_drift_rate(signal, start, end)
    return f"{value:.12g}", "ok", f"{fixed_channel} {operation} over {start:.6g}..{end:.6g} min, n={len(values)}"


def evaluate_chm_sig_value_average(formula: str, fixed_channel: str, ret_times: dict[int, float], signal: list[SignalPoint]) -> tuple[str, str, str]:
    return evaluate_chm_signal_formula(formula, fixed_channel, ret_times, signal)


def evaluate_chm_signal_value(formula: str, fixed_channel: str, ret_times: dict[int, float], signal: list[SignalPoint]) -> tuple[str, str, str]:
    args = _function_args(formula.strip(), "chm.signalValue")
    if len(args) != 1:
        return "", "unsupported", "Only chm.signalValue(time) is implemented."
    time_min = _eval_time_expr(args[0], ret_times)
    if time_min is None:
        return "", "missing-ret-time", "Formula references a time expression that could not be evaluated."
    value = _signal_value_at(signal, time_min)
    return f"{value:.12g}", "ok", f"{fixed_channel} value at {time_min:.6g} min."


def evaluate_chm_noise(formula: str, fixed_channel: str, ret_times: dict[int, float], signal: list[SignalPoint]) -> tuple[str, str, str]:
    args = _function_args(formula.strip(), "chm.noise")
    if len(args) != 2:
        return "", "unsupported", "Only chm.noise(start, end) is implemented."
    start = _eval_time_expr(args[0], ret_times)
    end = _eval_time_expr(args[1], ret_times)
    if start is None or end is None:
        return "", "missing-ret-time", "Formula references a time expression that could not be evaluated."
    points = _signal_points_in_window(signal, start, end)
    if not points:
        return "", "no-points", f"No {fixed_channel} signal points in {start:.6g}..{end:.6g} min."
    value = _linear_detrended_peak_to_peak(points)
    return f"{value:.12g}", "ok", f"{fixed_channel} detrended peak-to-peak noise over {start:.6g}..{end:.6g} min, n={len(points)}"


def evaluate_chm_drift(formula: str, fixed_channel: str, ret_times: dict[int, float], signal: list[SignalPoint]) -> tuple[str, str, str]:
    args = _function_args(formula.strip(), "chm.drift")
    if len(args) != 2:
        return "", "unsupported", "Only chm.drift(start, end) is implemented."
    start = _eval_time_expr(args[0], ret_times)
    end = _eval_time_expr(args[1], ret_times)
    if start is None or end is None:
        return "", "missing-ret-time", "Formula references a time expression that could not be evaluated."
    value = _signal_drift_rate(signal, start, end)
    return f"{value:.12g}", "ok", f"{fixed_channel} drift rate from {start:.6g} to {end:.6g} min."


def _function_args(formula: str, function_name: str) -> list[str]:
    prefix = function_name + "("
    if not formula.lower().startswith(prefix.lower()) or not formula.endswith(")"):
        return []
    body = formula[len(prefix) : -1]
    args: list[str] = []
    start = 0
    depth = 0
    in_quote = False
    for index, char in enumerate(body):
        if char == '"':
            in_quote = not in_quote
        elif not in_quote and char == "(":
            depth += 1
        elif not in_quote and char == ")":
            depth -= 1
        elif not in_quote and depth == 0 and char == ",":
            args.append(body[start:index].strip())
            start = index + 1
    args.append(body[start:].strip())
    return args


def _evaluate_formula_object(
    package: CmbxPackage,
    injection: CmbxElement,
    cache: Path,
    obj: ReportSheetObject,
    ret_times: dict[int, float],
    audit_records: list[AuditRecord],
    signal_cache: dict[str, list[SignalPoint]],
) -> tuple[str, str, str]:
    formula = obj.formula.strip()
    literal = _literal_formula_value(formula)
    if literal is not None:
        return literal, "ok", "Literal report text."
    audit_timebase = _eval_audit_timebase_formula(formula, audit_records)
    if audit_timebase is not None:
        return audit_timebase, "ok", "Instrument timebase parsed from injection audit trail."
    metadata = _eval_metadata_formula(package, injection, formula)
    if metadata is not None:
        return metadata, "ok", "Package/injection metadata."
    audit_metadata = evaluate_audit_metadata_formula(formula, audit_records)
    if audit_metadata is not None:
        value, detail = audit_metadata
        return value, "ok", detail
    ret_time = _eval_ret_time_formula(formula, ret_times)
    if ret_time is not None:
        return f"{ret_time:.12g}", "ok", "RetTime value read from injection audit trail."
    time_value = _eval_time_expr(formula, ret_times)
    if time_value is not None and "rettime" in formula.lower():
        return f"{time_value:.12g}", "ok", "Time expression evaluated from injection audit RetTimes."
    audit_value = evaluate_audit_property_formula(formula, ret_times, audit_records)
    if audit_value is not None:
        value, detail = audit_value
        return value, "ok", detail
    if formula.lower().startswith(("chm.sig_value", "chm.signalstatistic", "chm.signalvalue", "chm.noise", "chm.drift")):
        if not obj.fixed_channel:
            return "", "missing-channel", "Signal formula has no FixedChannel."
        signal = signal_cache.get(obj.fixed_channel)
        if signal is None:
            try:
                signal = _export_and_read_signal(package, injection, obj.fixed_channel, cache)
            except ValueError as exc:
                return "", "missing-channel", str(exc)
            signal_cache[obj.fixed_channel] = signal
        lowered = formula.lower()
        if lowered.startswith(("chm.sig_value", "chm.signalstatistic")):
            return evaluate_chm_signal_formula(formula, obj.fixed_channel, ret_times, signal)
        if lowered.startswith("chm.signalvalue"):
            return evaluate_chm_signal_value(formula, obj.fixed_channel, ret_times, signal)
        if lowered.startswith("chm.noise"):
            return evaluate_chm_noise(formula, obj.fixed_channel, ret_times, signal)
        return evaluate_chm_drift(formula, obj.fixed_channel, ret_times, signal)
    return "", "unsupported", "Formula evaluator does not implement this Chromeleon expression yet."


def _eval_ret_time_formula(formula: str, ret_times: dict[int, float]) -> float | None:
    match = re.fullmatch(r'AUDIT\.RetTime(\d+)\((?:1(?:\.0+)?\s*,\s*)?"forward"\s*\)', formula.strip(), flags=re.IGNORECASE)
    if not match:
        return None
    return ret_times.get(int(match.group(1)))


def evaluate_audit_property_formula(formula: str, ret_times: dict[int, float], audit_records: list[AuditRecord]) -> tuple[str, str] | None:
    match = re.fullmatch(r"AUDIT\.([A-Za-z0-9_.]+)\s*\((.+)\)", formula.strip(), flags=re.IGNORECASE)
    if not match or match.group(1).lower().startswith("rettime"):
        return None
    audit_path = match.group(1)
    normalized_formula = re.sub(r"^((?:AUDIT|audit)\.[A-Za-z0-9_.]+)\s+\(", r"\1(", formula.strip())
    args = _function_args(normalized_formula, f"AUDIT.{audit_path}") or _function_args(normalized_formula, f"audit.{audit_path}")
    time_min = _eval_time_expr(args[0], ret_times) if args else _eval_time_expr(match.group(2), ret_times)
    direction = args[1].strip().strip('"').lower() if len(args) > 1 else "backward"
    if time_min is None:
        return "", "Formula references a RetTime value that was not found in the audit trail."
    candidates = [
        record
        for record in audit_records
        if record.retention_time_min is not None
        and _audit_path_matches(record, audit_path)
        and record.property_value
    ]
    if direction == "forward":
        candidates = [record for record in candidates if record.retention_time_min is not None and record.retention_time_min >= time_min]
        selector = min
    else:
        candidates = [record for record in candidates if record.retention_time_min is not None and record.retention_time_min <= time_min]
        selector = max
    if not candidates:
        return "", f"No audit property value found for {audit_path} {direction} from {time_min:.6g} min."
    record = selector(candidates, key=lambda item: item.retention_time_min or float("-inf"))
    return record.property_value, f"{audit_path} at {time_min:.6g} min from audit record {record.retention_time_min:.6g} min."


def evaluate_audit_metadata_formula(formula: str, audit_records: list[AuditRecord]) -> tuple[str, str] | None:
    match = re.fullmatch(r"(?:AUDIT|precond)\.([A-Za-z0-9_.]+)", formula.strip(), flags=re.IGNORECASE)
    if not match:
        return None
    audit_path = match.group(1)
    for record in audit_records:
        if _audit_path_matches(record, audit_path) and record.property_value:
            source = "audit precondition" if record.retention_time_min is None else f"audit record {record.retention_time_min:.6g} min"
            return record.property_value, f"{audit_path} from {source}."
    return "", f"No audit metadata value found for {audit_path}."


def _audit_path_matches(record: AuditRecord, audit_path: str) -> bool:
    record_path = f"{record.device}.{record.property_name}".lower()
    wanted = audit_path.lower()
    return record_path == wanted or record_path.endswith("." + wanted)


def _eval_time_expr(expr: str, ret_times: dict[int, float]) -> float | None:
    expr = expr.strip()
    try:
        return float(expr)
    except ValueError:
        pass
    duration = re.fullmatch(
        r'AUDIT\.RetTime(\d+)\((?:1(?:\.0+)?\s*,\s*)?"forward"\s*\)\s*-\s*AUDIT\.RetTime(\d+)\((?:1(?:\.0+)?\s*,\s*)?"forward"\s*\)',
        expr,
        flags=re.IGNORECASE,
    )
    if duration:
        left = ret_times.get(int(duration.group(1)))
        right = ret_times.get(int(duration.group(2)))
        return (left - right) if left is not None and right is not None else None
    match = re.fullmatch(r'AUDIT\.RetTime(\d+)\((?:1(?:\.0+)?\s*,\s*)?"forward"\s*\)\s*([+-])?\s*([0-9]+(?:\.[0-9]+)?)?', expr, flags=re.IGNORECASE)
    if not match:
        return None
    base = ret_times.get(int(match.group(1)))
    if base is None:
        return None
    if not match.group(2):
        return base
    offset = float(match.group(3) or "0")
    return base + offset if match.group(2) == "+" else base - offset


def _signal_window(args: list[str], ret_times: dict[int, float], signal: list[SignalPoint]) -> tuple[float | None, float | None]:
    if len(args) >= 3:
        return _eval_time_expr(args[1], ret_times), _eval_time_expr(args[2], ret_times)
    if not signal:
        return None, None
    return signal[0].time_min, signal[-1].time_min


def _signal_points_in_window(signal: list[SignalPoint], start: float, end: float) -> list[SignalPoint]:
    low, high = (start, end) if start <= end else (end, start)
    return [point for point in signal if low <= point.time_min <= high]


def _signal_drift_rate(signal: list[SignalPoint], start: float, end: float) -> float:
    points = _signal_points_in_window(signal, start, end)
    if len(points) >= 2:
        return _linear_regression_slope(points)
    duration = end - start
    if duration == 0:
        return 0.0
    return (_signal_value_at(signal, end) - _signal_value_at(signal, start)) / duration


def _signal_statistic_drift_rate(signal: list[SignalPoint], start: float, end: float) -> float:
    duration = end - start
    if duration == 0:
        return 0.0
    step = 0.5 if abs(duration) >= 0.5 else abs(duration)
    if step == 0:
        return _signal_drift_rate(signal, start, end)
    direction = 1 if duration > 0 else -1
    points: list[SignalPoint] = []
    time_min = start
    while (time_min - end) * direction <= 1e-9:
        points.append(SignalPoint(time_min, _signal_value_at(signal, time_min)))
        time_min += direction * step
    if not points or abs(points[-1].time_min - end) > 1e-9:
        points.append(SignalPoint(end, _signal_value_at(signal, end)))
    return _linear_regression_slope(points) if len(points) >= 2 else _signal_drift_rate(signal, start, end)


def _linear_detrended_peak_to_peak(points: list[SignalPoint]) -> float:
    if len(points) <= 1:
        return 0.0
    slope = _linear_regression_slope(points)
    mean_x = sum(point.time_min for point in points) / len(points)
    mean_y = sum(point.value for point in points) / len(points)
    intercept = mean_y - slope * mean_x
    residuals = [point.value - (slope * point.time_min + intercept) for point in points]
    return max(residuals) - min(residuals)


def _linear_regression_slope(points: list[SignalPoint]) -> float:
    mean_x = sum(point.time_min for point in points) / len(points)
    mean_y = sum(point.value for point in points) / len(points)
    denominator = sum((point.time_min - mean_x) ** 2 for point in points)
    if denominator == 0:
        return 0.0
    return sum((point.time_min - mean_x) * (point.value - mean_y) for point in points) / denominator


def _signal_value_at(signal: list[SignalPoint], time_min: float) -> float:
    if not signal:
        raise ValueError("Signal has no points.")
    if time_min <= signal[0].time_min:
        return signal[0].value
    if time_min >= signal[-1].time_min:
        return signal[-1].value
    for index in range(1, len(signal)):
        left = signal[index - 1]
        right = signal[index]
        if left.time_min <= time_min <= right.time_min:
            span = right.time_min - left.time_min
            if span <= 0:
                return right.value
            fraction = (time_min - left.time_min) / span
            return left.value + (right.value - left.value) * fraction
    return min(signal, key=lambda point: abs(point.time_min - time_min)).value


def _literal_formula_value(formula: str) -> str | None:
    text = formula.strip()
    if len(text) >= 2 and text[0] == '"' and text[-1] == '"':
        return text[1:-1]
    return None


def _eval_metadata_formula(package: CmbxPackage, injection: CmbxElement, formula: str) -> str | None:
    text = formula.strip()
    if text in {"injection.name", "smp.name"}:
        return injection.name
    if text == "seq.name":
        sequence = package.elements_by_id.get(injection.parent_id or "")
        return sequence.name if sequence else package.path.stem
    if text == "seq.update_time":
        sequence_update_time = _sequence_update_time_excel_serial(package, injection)
        if sequence_update_time is not None:
            return f"{sequence_update_time:.17g}"
        return package.header_attributes.get("DateCreated") or package.header_attributes.get("CreationDate")
    if text == "seq.timebase":
        sequence = package.elements_by_id.get(injection.parent_id or "")
        if sequence and sequence.url:
            match = re.match(r"chrom://[^/]+/([^/]+)/", sequence.url)
            if match:
                return match.group(1)
    return None


def _eval_audit_timebase_formula(formula: str, audit_records: list[AuditRecord]) -> str | None:
    if formula.strip() != "seq.timebase":
        return None
    for record in audit_records:
        match = re.search(r"\bon instrument\s+(.+?)(?:\.?$|\s{2,})", record.message, flags=re.IGNORECASE)
        if match:
            return re.sub(r"\s+\(server\b.*$", "", match.group(1).strip().rstrip("."), flags=re.IGNORECASE)
    return None


def _sequence_update_time_excel_serial(package: CmbxPackage, injection: CmbxElement) -> float | None:
    sequence = package.elements_by_id.get(injection.parent_id or "")
    if not sequence or not sequence.package_entry_name:
        return None
    try:
        payload = extract_cmbx_entry(package.path, sequence.package_entry_name)
    except (KeyError, ValueError, OSError):
        return None

    timestamp = _sequence_update_time_from_payload(payload)
    if timestamp is None:
        return None
    excel_base = datetime(1899, 12, 30)
    local_timestamp = timestamp.replace(tzinfo=None)
    return (local_timestamp - excel_base).total_seconds() / 86400


def _sequence_update_time_from_payload(payload: bytes) -> datetime | None:
    iso_pattern = rb"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:[+-]\d{2}:\d{2}|Z)"
    imported_at = payload.find(b"Imported from")
    if imported_at >= 0:
        match = re.search(iso_pattern, payload[imported_at:])
        if match:
            return _parse_cm_iso_datetime(match.group(0).decode("ascii", errors="ignore"))
    matches = list(re.finditer(iso_pattern, payload))
    if matches:
        return _parse_cm_iso_datetime(matches[-1].group(0).decode("ascii", errors="ignore"))
    return None


def _parse_cm_iso_datetime(value: str) -> datetime | None:
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        return None


def _audit_source_injection(package: CmbxPackage, injection: CmbxElement) -> CmbxElement | None:
    if any(child.kind == "audit" for child in injection.children):
        return injection
    sequence = package.elements_by_id.get(injection.parent_id or "")
    if not sequence:
        return None
    injections = [child for child in sequence.children if child.kind == "injection"]
    try:
        index = injections.index(injection)
    except ValueError:
        return None
    for candidate in reversed(injections[:index]):
        if any(child.kind == "audit" for child in candidate.children):
            return candidate
    for candidate in injections[index + 1 :]:
        if any(child.kind == "audit" for child in candidate.children):
            return candidate
    return None


def _export_and_read_audit_records(package: CmbxPackage, injection: CmbxElement, cache: Path) -> list[AuditRecord]:
    audit = next((child for child in injection.children if child.kind == "audit"), None)
    if not audit:
        return []
    raw_path = _extract_raw_to_cache(package, audit, cache)
    output_path = cache / f"{safe_filename(injection.name)}_audit.tsv"
    export_audit_raw(raw_path, output_path)
    return read_audit_records_tsv(output_path)


def _export_and_read_signal(package: CmbxPackage, injection: CmbxElement, channel_name: str, cache: Path) -> list[SignalPoint]:
    signal = next((child for child in injection.children if child.kind == "signal" and child.name == channel_name), None)
    if not signal:
        raise ValueError(f"Signal channel was not found in {injection.name}: {channel_name}")
    raw_path = _extract_raw_to_cache(package, signal, cache)
    output_path = cache / f"{safe_filename(injection.name)}_{safe_filename(channel_name)}.tsv"
    export_signal_raw(raw_path, output_path, channel_name)
    return read_signal_tsv(output_path)


def _extract_raw_to_cache(package: CmbxPackage, element: CmbxElement, cache: Path) -> Path:
    if not element.raw_filename:
        raise ValueError(f"Element has no raw file: {element.name}")
    cache.mkdir(parents=True, exist_ok=True)
    raw_path = cache / element.raw_filename
    if not raw_path.exists():
        raw_path.write_bytes(extract_cmbx_entry(package.path, element.raw_filename))
    return raw_path


def _formula_cache_folder(package: CmbxPackage, injection: CmbxElement) -> Path:
    return Path(tempfile.gettempdir()) / "CmbxDataExplorer" / "report_formula_eval" / safe_filename(package.path.stem) / safe_filename(injection.name)


def _tsv_row(values: list[str]) -> str:
    return "\t".join(str(value).replace("\t", " ").replace("\r", " ").replace("\n", " ").strip() for value in values)
