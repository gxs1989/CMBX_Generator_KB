from __future__ import annotations

import json
from dataclasses import asdict, replace
from pathlib import Path
from typing import Any, Callable, Iterable

from db_upload_service import DatabaseUploadConfig
from foq_quality_service import (
    FoqSequenceInventory,
    attach_history,
    coerce_number,
    default_mapping_path,
    evaluate_candidate,
    filter_database_rows,
    filter_history_for_device,
    inspect_foq_sources,
    metric_catalog_for_devices,
    read_historical_rows,
)
from windows_credentials import unprotect_secret


Progress = Callable[[int, int, str, str], None]
DEFAULT_DATABASE_CONFIG = Path(r"C:\ProgramData\CMBX Data Explorer Workspace\database_config.json")
DEFAULT_DATABASE_SOURCES = Path(r"C:\ProgramData\CMBX Data Explorer Workspace\database_sources.json")


def sequence_key(artifact_id: str, item: FoqSequenceInventory) -> str:
    identity = item.sequence.id or item.sequence.url or item.sequence.name
    return f"{artifact_id}:{identity}"


def inspect_sources(
    artifacts: Iterable[dict[str, Any]],
    mapping_path: str | Path,
    progress: Progress,
) -> dict[str, Any]:
    records = list(artifacts)
    progress(0, max(1, len(records) + 1), "preparing", "Reading FOQ Location mapping")
    paths = [Path(record["storage_path"]) for record in records]
    artifact_by_path = {str(Path(record["storage_path"]).resolve()).lower(): record for record in records}
    inventory, errors = inspect_foq_sources(paths, mapping_path)
    rows: list[dict[str, Any]] = []
    eligible_devices: set[str] = set()
    for index, item in enumerate(inventory, 1):
        artifact = artifact_by_path.get(str(item.package.path.resolve()).lower())
        if artifact is None:
            continue
        injections = [child for child in item.sequence.children if child.kind == "injection"]
        totals: dict[str, int] = {}
        for injection in injections:
            name_key = injection.name.strip().lower()
            totals[name_key] = totals.get(name_key, 0) + 1
        occurrences: dict[str, int] = {}
        injection_rows = []
        for injection in injections:
            name_key = injection.name.strip().lower()
            occurrences[name_key] = occurrences.get(name_key, 0) + 1
            injection_rows.append(
                {
                    "id": injection.id,
                    "name": injection.name,
                    "occurrence": occurrences[name_key],
                    "occurrence_total": totals[name_key],
                    "default_selected": totals[name_key] == 1,
                }
            )
        key = sequence_key(artifact["id"], item)
        if item.eligible:
            eligible_devices.add(item.device)
        rows.append(
            {
                "key": key,
                "artifact_id": artifact["id"],
                "package": artifact["original_name"],
                "sequence_id": item.sequence.id,
                "sequence": item.sequence.name,
                "device": item.device,
                "device_source": item.device_source,
                "report_template": item.report_template,
                "eligible": item.eligible,
                "reason": item.reason,
                "default_selected": item.eligible,
                "injections": injection_rows,
            }
        )
        progress(index, max(1, len(inventory) + 1), "running", f"Indexed {item.sequence.name}")
    metrics = metric_catalog_for_devices(mapping_path, eligible_devices) if eligible_devices else []
    progress(max(1, len(inventory) + 1), max(1, len(inventory) + 1), "validating", "FOQ scope ready")
    return {
        "sequences": rows,
        "metrics": metrics,
        "mapping_path": str(mapping_path),
        "errors": [{"file": path.name, "detail": detail} for path, detail in errors],
    }


def metric_catalog(mapping_path: str | Path, devices: Iterable[str]) -> list[str]:
    return metric_catalog_for_devices(mapping_path, devices)


def run_check(
    artifacts: Iterable[dict[str, Any]],
    mapping_path: str | Path,
    selected_sequences: dict[str, list[str]],
    metrics: Iterable[str],
    history_options: dict[str, Any],
    progress: Progress,
) -> dict[str, Any]:
    records = list(artifacts)
    paths = [Path(record["storage_path"]) for record in records]
    artifact_by_path = {str(Path(record["storage_path"]).resolve()).lower(): record for record in records}
    inventory, load_errors = inspect_foq_sources(paths, mapping_path)
    candidates: list[tuple[str, Any, list[str], str]] = []
    for item in inventory:
        artifact = artifact_by_path.get(str(item.package.path.resolve()).lower())
        if artifact is None or item.candidate is None:
            continue
        key = sequence_key(artifact["id"], item)
        if key in selected_sequences:
            candidates.append((key, item.candidate, selected_sequences[key], artifact["original_name"]))
    if not candidates:
        raise ValueError("No eligible FOQ sequence was selected")
    requested = [str(field).strip() for field in metrics if str(field).strip()]
    if not requested:
        raise ValueError("Choose at least one FOQ metric")

    rows = []
    total = len(candidates) * 100
    for index, (_key, candidate, injection_ids, original_name) in enumerate(candidates):
        base = index * 100

        def formula_progress(message: object) -> None:
            text = str(message)
            percent = 0
            detail = text
            if text.startswith("__PROGRESS__=") and "|" in text:
                value, detail = text.split("|", 1)
                try:
                    percent = int(float(value.removeprefix("__PROGRESS__=")))
                except ValueError:
                    percent = 0
            progress(base + percent, total, "running", f"{candidate.sequence.name}: {detail}")

        evaluated = evaluate_candidate(
                candidate,
                mapping_path,
                progress=formula_progress,
                db_fields=requested,
                selected_injection_ids=injection_ids,
            )
        rows.extend(replace(row, package=original_name) for row in evaluated)
        progress(base + 100, total, "running", f"Completed {candidate.sequence.name}")

    history_rows: list[dict[str, object]] = []
    history_samples: dict[str, list[float]] = {}
    history_detail = {"enabled": False, "count": 0, "source": "SPEC only"}
    if history_options.get("enabled"):
        database = load_database_source(str(history_options.get("source_id") or ""))
        table = str(history_options.get("table") or database.table or "AUTO")
        database = DatabaseUploadConfig(**{**asdict(database), "table": table})
        limit = max(100, min(int(history_options.get("limit") or 5000), 100000))
        devices = sorted({candidate.device for _key, candidate, _ids, _name in candidates})
        for device in devices:
            history_rows.extend(read_historical_rows(database, device=device, limit=limit))
        history_rows = filter_database_rows(history_rows, history_options.get("filters") or {})
        rows = attach_history(rows, history_rows)
        for row in rows:
            scoped, _scope = filter_history_for_device(history_rows, row.device)
            values = [
                number
                for item in scoped
                if (number := coerce_number(_case_value(item, row.db_field))) is not None
            ]
            history_samples[f"{row.device}|{row.db_field}"] = _sample_evenly(values, 400)
        history_detail = {
            "enabled": True,
            "count": len(history_rows),
            "source": database.dsn or f"{database.server}/{database.database}",
            "table": table,
        }

    return {
        "rows": [asdict(row) for row in rows],
        "summary": summarize_results(rows),
        "history": history_detail,
        "history_samples": history_samples,
        "errors": [{"file": path.name, "detail": detail} for path, detail in load_errors],
    }


def _case_value(row: dict[str, object], field: str) -> object:
    target = field.casefold()
    return next((value for key, value in row.items() if str(key).casefold() == target), None)


def _sample_evenly(values: list[float], limit: int) -> list[float]:
    if len(values) <= limit:
        return values
    step = (len(values) - 1) / (limit - 1)
    return [values[round(index * step)] for index in range(limit)]


def summarize_results(rows: Iterable[Any]) -> dict[str, int]:
    summary = {"total": 0, "pass": 0, "fail": 0, "review": 0, "not_evaluated": 0}
    for row in rows:
        summary["total"] += 1
        status = str(row.spec_status).replace("-", "_")
        if status in summary:
            summary[status] += 1
        else:
            summary["review"] += 1
    return summary


def database_public_status() -> dict[str, Any]:
    try:
        sources, default_source = load_database_sources()
    except Exception as exc:
        return {"configured": False, "sources": [], "detail": str(exc)}
    public_sources = [
        {
            "id": source_id,
            "label": label,
            "configured": bool((config.dsn or config.server) and config.username),
            "source": config.dsn or config.server,
            "database": config.database,
            "schema": config.schema,
            "table": config.table,
            "username": config.username,
        }
        for source_id, label, config in sources
    ]
    selected = next((item for item in public_sources if item["id"] == default_source), public_sources[0] if public_sources else {})
    return {
        "configured": any(item["configured"] for item in public_sources),
        "default_source": selected.get("id", ""),
        "sources": public_sources,
        **{key: value for key, value in selected.items() if key != "configured"},
    }


def load_database_source(source_id: str = "") -> DatabaseUploadConfig:
    sources, default_source = load_database_sources()
    requested = source_id or default_source
    match = next((config for item_id, _label, config in sources if item_id == requested), None)
    if match is None:
        raise ValueError(f"Unknown database source: {requested}")
    return match


def load_database_sources(path: str | Path = DEFAULT_DATABASE_SOURCES) -> tuple[list[tuple[str, str, DatabaseUploadConfig]], str]:
    registry = Path(path)
    if not registry.exists():
        config = load_database_config()
        return [("default", "Configured database", config)], "default"
    data = json.loads(registry.read_text(encoding="utf-8"))
    output: list[tuple[str, str, DatabaseUploadConfig]] = []
    for item in data.get("sources", []):
        source_id = str(item.get("id", "")).strip()
        if not source_id:
            continue
        output.append(
            (
                source_id,
                str(item.get("label") or source_id),
                DatabaseUploadConfig(
                    server=str(item.get("server", "")),
                    database=str(item.get("database", "")),
                    username=str(item.get("username", "")),
                    password=unprotect_secret(str(item.get("password_dpapi", ""))),
                    schema=str(item.get("schema", "dbo") or "dbo"),
                    table=str(item.get("table", "AUTO") or "AUTO"),
                    driver=str(item.get("driver", "ODBC Driver 17 for SQL Server") or "ODBC Driver 17 for SQL Server"),
                    dsn=str(item.get("dsn", "")),
                ),
            )
        )
    if not output:
        raise ValueError("No database sources are configured")
    return output, str(data.get("default_source") or output[0][0])


def load_database_config(path: str | Path = DEFAULT_DATABASE_CONFIG) -> DatabaseUploadConfig:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return DatabaseUploadConfig(
        server=str(data.get("server", "")),
        database=str(data.get("database", "")),
        username=str(data.get("username", "")),
        password=unprotect_secret(str(data.get("password_dpapi", ""))),
        schema=str(data.get("schema", "dbo") or "dbo"),
        table=str(data.get("table", "AUTO") or "AUTO"),
        driver=str(data.get("driver", "ODBC Driver 17 for SQL Server") or "ODBC Driver 17 for SQL Server"),
        dsn=str(data.get("dsn", "")),
    )
