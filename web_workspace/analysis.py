from __future__ import annotations

import math
import shutil
import statistics
import threading
import zipfile
from dataclasses import asdict
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any, Iterable

from db_upload_service import fetch_table_rows, list_database_tables
from foq_quality_service import filter_database_rows, summarize_history
from read_analyze_service import (
    ChannelRecord,
    FormulaRecord,
    IntegrationSettings,
    adapt_integration_settings,
    channel_records,
    decode_channel_points,
    evaluate_formula_batch,
    export_channel_records,
    formula_records,
    injection_records,
    integrate_signal,
    load_workset,
)


_CACHE_LOCK = threading.Lock()
_WORKSET_CACHE: dict[tuple[tuple[str, int, int], ...], tuple[list[Any], list[tuple[Path, str]]]] = {}


def load_cached_workset(paths: Iterable[str | Path]):
    resolved = [Path(value).resolve() for value in paths]
    key = tuple(sorted((str(path), path.stat().st_mtime_ns, path.stat().st_size) for path in resolved))
    with _CACHE_LOCK:
        cached = _WORKSET_CACHE.get(key)
    if cached is not None:
        return cached
    loaded = load_workset(resolved)
    with _CACHE_LOCK:
        _WORKSET_CACHE.clear()
        _WORKSET_CACHE[key] = loaded
    return loaded


def build_catalog(paths: Iterable[str | Path]) -> dict[str, Any]:
    packages, errors = load_cached_workset(paths)
    channels = channel_records(packages)
    injections = injection_records(packages)
    return {
        "packages": [
            {"name": item.package.path.name, "path": str(item.package.path), "type": item.package_type}
            for item in packages
        ],
        "injections": [
            {
                "key": item.key,
                "package": item.package.path.name,
                "sequence": item.sequence.name,
                "injection": item.injection.name,
            }
            for item in injections
        ],
        "channels": [serialize_channel(item) for item in channels],
        "errors": [{"path": str(path), "detail": detail} for path, detail in errors],
    }


def serialize_channel(record: ChannelRecord) -> dict[str, str]:
    return {
        "key": record.key,
        "label": record.label,
        "package": record.package.path.name,
        "sequence": record.sequence.name,
        "injection": record.injection.name,
        "channel": record.channel.name,
    }


def selected_channels(paths: Iterable[str | Path], keys: Iterable[str]) -> list[ChannelRecord]:
    packages, errors = load_cached_workset(paths)
    if errors and not packages:
        raise ValueError(errors[0][1])
    lookup = {record.key: record for record in channel_records(packages)}
    selected = [lookup[key] for key in dict.fromkeys(keys) if key in lookup]
    if not selected:
        raise ValueError("Choose at least one channel")
    return selected


def selected_injections(paths: Iterable[str | Path], keys: Iterable[str]):
    packages, errors = load_cached_workset(paths)
    if errors and not packages:
        raise ValueError(errors[0][1])
    records = injection_records(packages)
    wanted = set(keys)
    return [record for record in records if not wanted or record.key in wanted]


def export_raw_zip(paths: Iterable[str | Path], keys: Iterable[str], output_zip: Path) -> dict[str, Any]:
    records = selected_channels(paths, keys)
    folder = output_zip.with_suffix("")
    if folder.exists():
        shutil.rmtree(folder)
    exported, errors = export_channel_records(records, folder)
    output_zip.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as archive:
        for file in folder.rglob("*"):
            if file.is_file():
                archive.write(file, file.relative_to(folder))
    shutil.rmtree(folder, ignore_errors=True)
    return {
        "traces": len(records),
        "exported": len(exported),
        "errors": [{"trace": record.label, "detail": detail} for record, detail in errors],
    }


def chromatogram_payload(
    paths: Iterable[str | Path], keys: Iterable[str], raw_settings: dict[str, Any], max_points: int = 2400,
    *, perform_integration: bool = True,
) -> dict[str, Any]:
    records = selected_channels(paths, keys)
    if len(records) > 16:
        raise ValueError("A single preview supports at most 16 traces")
    point_sets = [decode_channel_points(record) for record in records]
    requested = IntegrationSettings(
        baseline_noise_start_min=_optional_float(raw_settings.get("baseline_noise_start_min")),
        baseline_noise_end_min=_optional_float(raw_settings.get("baseline_noise_end_min")),
        smoothing_width_s=float(raw_settings.get("smoothing_width_s", 1.0) or 1.0),
        noise_multiplier=float(raw_settings.get("noise_multiplier", 5.0) or 5.0),
        minimum_height=float(raw_settings.get("minimum_height", 0.0) or 0.0),
        minimum_area=float(raw_settings.get("minimum_area", 0.0) or 0.0),
        minimum_width_s=float(raw_settings.get("minimum_width_s", 0.0) or 0.0),
        detect_negative=bool(raw_settings.get("detect_negative", False)),
    )
    settings = adapt_integration_settings(point_sets, requested)
    traces = []
    all_peaks = []
    for record, points in zip(records, point_sets):
        peaks = integrate_signal(record.key, points, settings) if perform_integration else []
        sampled = _downsample(points, max(300, min(int(max_points), 6000)))
        traces.append({
            **serialize_channel(record),
            "points": [[point.time_min, point.value] for point in sampled],
            "point_count": len(points),
            "min_time": points[0].time_min if points else None,
            "max_time": points[-1].time_min if points else None,
        })
        all_peaks.extend(asdict(peak) for peak in peaks)
    return {
        "traces": traces,
        "peaks": all_peaks,
        "settings": asdict(settings),
        "integrated": perform_integration,
    }


def scan_direct_formulas(paths: Iterable[str | Path], progress=None) -> dict[str, Any]:
    packages, load_errors = load_cached_workset(paths)
    records, formula_errors = formula_records(packages, include_formulaone=False, progress=progress)
    return {
        "formulas": [serialize_formula(record) for record in records],
        "errors": [
            *({"source": str(path), "detail": detail} for path, detail in load_errors),
            *({"source": source, "detail": detail} for source, detail in formula_errors),
        ],
    }


def serialize_formula(record: FormulaRecord) -> dict[str, str]:
    return {
        "key": record.key,
        "package": record.package.path.name,
        "report": record.report_name,
        "sheet": record.sheet_name,
        "cell": record.excel_range,
        "object_type": record.object_type,
        "formula": record.formula,
        "fixed_channel": record.fixed_channel,
        "fixed_component": record.fixed_component,
        "meaning": _formula_meaning(record.formula, record.fixed_channel),
    }


def evaluate_direct_formulas(paths: Iterable[str | Path], injection_keys: Iterable[str], requested: list[dict[str, Any]]):
    packages, _errors = load_cached_workset(paths)
    contexts = selected_injections(paths, injection_keys)
    package_by_name = {item.package.path.name: item.package for item in packages}
    formulas = []
    for item in requested:
        package = package_by_name.get(str(item.get("package") or "")) or next(iter(package_by_name.values()))
        formulas.append(FormulaRecord(
            package, str(item.get("report") or "Formula library"), str(item.get("sheet") or ""),
            str(item.get("cell") or ""), str(item.get("object_type") or "ReportFormulaObject"),
            str(item.get("formula") or ""), str(item.get("fixed_channel") or ""),
            str(item.get("fixed_component") or ""),
        ))
    results = evaluate_formula_batch(contexts, formulas)
    return {"results": [asdict(result) for result in results]}


def quality_catalog(config) -> dict[str, Any]:
    return {"tables": [f"{schema}.{table}" for schema, table in list_database_tables(config)]}


def quality_query(config, table_name: str, metric: str, filters: dict[str, str], limit: int) -> dict[str, Any]:
    schema, table = (table_name.split(".", 1) if "." in table_name else (config.schema, table_name))
    rows = fetch_table_rows(config, table=table, schema=schema, limit=limit)
    filtered = filter_database_rows(rows, filters)
    columns = list(rows[0].keys()) if rows else []
    numeric = [column for column in columns if any(_number(row.get(column)) is not None for row in rows[:200])]
    selected_metric = metric if metric in columns else (numeric[0] if numeric else "")
    values = [_number(row.get(selected_metric)) for row in filtered]
    values = [value for value in values if value is not None]
    summary = summarize_history(values)
    display_columns = [column for column in ("ID", "TestDate", "Serial", "TimeBase", "ModelNo", "ModelVariant", selected_metric) if column in columns]
    return {
        "table": f"{schema}.{table}", "columns": columns, "numeric_metrics": numeric,
        "metric": selected_metric, "count": len(filtered), "summary": asdict(summary),
        "samples": _sample_values(values, 1200),
        "rows": [{column: _json_value(row.get(column)) for column in display_columns} for row in filtered[:1000]],
        "display_columns": display_columns,
        "choices": {
            "models": _choices(filtered, ("ModelNo", "DeviceType")),
            "variants": _choices(filtered, ("ModelVariant",)),
            "timebases": _choices(filtered, ("TimeBase",)),
        },
    }


def _downsample(points, limit: int):
    if len(points) <= limit:
        return points
    step = (len(points) - 1) / (limit - 1)
    return [points[round(index * step)] for index in range(limit)]


def _optional_float(value: Any) -> float | None:
    return None if value in (None, "") else float(value)


def _formula_meaning(formula: str, channel: str) -> str:
    lower = formula.strip().lower()
    source = channel or "the report-bound channel"
    if lower.startswith("chm.sig_value") or lower.startswith("chm.signalstatistic"):
        return f"Calculate a signal statistic from {source} over the formula time window."
    if lower.startswith("chm.signalvalue"):
        return f"Read {source} at the requested retention time."
    if lower.startswith("chm.noise"):
        return f"Calculate baseline noise for {source}."
    if lower.startswith("chm.drift"):
        return f"Calculate linear signal drift for {source}."
    if lower.startswith("audit.rettime"):
        return "Read a RetTime anchor recorded in the injection audit trail."
    if lower.startswith("audit."):
        return "Read a time-directed property from the injection audit trail."
    if lower.startswith("precond."):
        return "Read device metadata captured at injection start."
    if lower.startswith(("seq.", "smp.", "injection.", "gen.")):
        return "Read sequence, sample, injection, or report metadata."
    return "Evaluate this Direct CM expression in the selected injection context."


def _number(value: Any) -> float | None:
    if isinstance(value, bool) or value is None:
        return None
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    return result if math.isfinite(result) else None


def _json_value(value: Any) -> Any:
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return float(value)
    return value


def _choices(rows: list[dict[str, Any]], names: tuple[str, ...]) -> list[str]:
    lookup = {key.casefold(): key for key in (rows[0].keys() if rows else [])}
    actual = next((lookup[name.casefold()] for name in names if name.casefold() in lookup), "")
    return sorted({str(row.get(actual)).strip() for row in rows if actual and row.get(actual) not in (None, "")})


def _sample_values(values: list[float], limit: int) -> list[float]:
    if len(values) <= limit:
        return values
    step = len(values) / limit
    return [values[min(len(values) - 1, int(index * step))] for index in range(limit)]
