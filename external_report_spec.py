from __future__ import annotations

import ast
import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class ExternalReportOperation:
    operation_id: str
    kind: str
    label: str = ""
    channel: str = ""
    formula: str = ""
    expression: str = ""
    property_paths: tuple[str, ...] = ()
    message_contains: tuple[str, ...] = ()
    columns: tuple[str, ...] = ()
    start_min: float | None = None
    end_min: float | None = None
    threshold: float | None = None
    edge: str = "both"
    hysteresis: float = 0.0
    debounce_seconds: float = 0.0
    group_within_seconds: float = 0.0
    value_changes_only: bool = False
    number_format: str = "General"


@dataclass(frozen=True)
class ExternalReportSpec:
    name: str
    version: str = "1.0"
    channels: tuple[str, ...] = ()
    audit_paths: tuple[str, ...] = ()
    ret_times: tuple[int, ...] = ()
    operations: tuple[ExternalReportOperation, ...] = ()
    source_path: Path | None = None
    warnings: tuple[str, ...] = ()


_BLOCK_RE = re.compile(
    r"^###\s+(Scalar|Formula|Audit Event Table|Raw Event Table|Plot):\s*([^\r\n]+)\s*\r?\n"
    r"\s*```(?:yaml|yml)\s*\r?\n(.*?)\r?\n```",
    re.I | re.M | re.S,
)
_REQUIREMENTS_RE = re.compile(
    r"^##\s+Data Requirements\s*\r?\n\s*```(?:yaml|yml)\s*\r?\n(.*?)\r?\n```",
    re.I | re.M | re.S,
)
_FRONT_RE = re.compile(r"\A\s*---\s*\r?\n(.*?)\r?\n---", re.S)


def parse_external_report_md(source: str | Path, *, from_text: bool = False) -> ExternalReportSpec:
    path = None if from_text else Path(source)
    text = str(source) if from_text else path.read_text(encoding="utf-8-sig")
    front_match = _FRONT_RE.search(text)
    front = _parse_yaml_like(front_match.group(1)) if front_match else {}
    req_match = _REQUIREMENTS_RE.search(text)
    requirements = _parse_yaml_like(req_match.group(1)) if req_match else {}
    warnings: list[str] = []
    operations: list[ExternalReportOperation] = []
    seen: set[str] = set()
    for match in _BLOCK_RE.finditer(text):
        heading, operation_id, body = match.groups()
        operation_id = operation_id.strip()
        if operation_id in seen:
            raise ValueError(f"Duplicate report operation id: {operation_id}")
        seen.add(operation_id)
        payload = _parse_yaml_like(body)
        kind = heading.lower().replace(" ", "_")
        operation = ExternalReportOperation(
            operation_id=operation_id,
            kind=kind,
            label=str(payload.get("label") or operation_id),
            channel=str(payload.get("channel") or ""),
            formula=str(payload.get("formula") or ""),
            expression=str(payload.get("expression") or ""),
            property_paths=_as_strings(payload.get("property_paths")),
            message_contains=_as_strings(payload.get("message_contains")),
            columns=_as_strings(payload.get("columns")),
            start_min=_optional_float(payload.get("start_min")),
            end_min=_optional_float(payload.get("end_min")),
            threshold=_optional_float(payload.get("threshold")),
            edge=str(payload.get("edge") or "both").lower(),
            hysteresis=_float(payload.get("hysteresis"), 0.0),
            debounce_seconds=_float(payload.get("debounce_seconds"), 0.0),
            group_within_seconds=_float(payload.get("group_within_seconds"), 0.0),
            value_changes_only=_bool(payload.get("value_changes_only"), False),
            number_format=str(payload.get("number_format") or "General"),
        )
        _validate_operation(operation)
        operations.append(operation)
    if not operations:
        warnings.append("No executable report operation blocks were found.")
    inferred_ret_times = {
        int(number)
        for operation in operations
        for number in re.findall(r"AUDIT\.RetTime(\d+)", operation.formula, flags=re.I)
    }
    return ExternalReportSpec(
        name=str(front.get("report_name") or front.get("template_name") or front.get("name") or (path.stem if path else "External Report")),
        version=str(front.get("spec_version") or "1.0"),
        channels=_as_strings(requirements.get("channels")),
        audit_paths=_as_strings(requirements.get("audit_paths")),
        ret_times=tuple(sorted(set(_as_ints(requirements.get("ret_times"))) | inferred_ret_times)),
        operations=tuple(operations),
        source_path=path,
        warnings=tuple(warnings),
    )


def _validate_operation(operation: ExternalReportOperation) -> None:
    if operation.kind in {"raw_event_table", "plot"} and not operation.channel:
        raise ValueError(f"{operation.operation_id}: channel is required for {operation.kind}.")
    if operation.kind == "scalar" and not operation.formula:
        raise ValueError(f"{operation.operation_id}: formula is required.")
    if operation.kind == "scalar" and operation.formula.casefold().startswith("chm.") and not operation.channel:
        raise ValueError(f"{operation.operation_id}: channel is required for a chm.* formula.")
    if operation.kind == "formula" and not operation.expression:
        raise ValueError(f"{operation.operation_id}: expression is required.")
    if operation.kind == "audit_event_table" and not (operation.property_paths or operation.message_contains):
        raise ValueError(f"{operation.operation_id}: property_paths or message_contains is required.")
    if operation.kind == "raw_event_table" and operation.threshold is None:
        raise ValueError(f"{operation.operation_id}: threshold is required.")
    if operation.edge not in {"rising", "falling", "both"}:
        raise ValueError(f"{operation.operation_id}: edge must be rising, falling, or both.")


def _parse_yaml_like(text: str) -> dict[str, object]:
    result: dict[str, object] = {}
    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#") or ":" not in stripped:
            continue
        key, raw_value = stripped.split(":", 1)
        result[key.strip()] = _parse_scalar(raw_value.strip())
    return result


def _parse_scalar(value: str) -> object:
    if not value:
        return ""
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    if value.startswith("[") and value.endswith("]"):
        try:
            parsed = ast.literal_eval(value)
            return parsed if isinstance(parsed, (list, tuple)) else [parsed]
        except (ValueError, SyntaxError):
            return [item.strip().strip("'\"") for item in value[1:-1].split(",") if item.strip()]
    return value.strip("'\"")


def _as_strings(value: object) -> tuple[str, ...]:
    if value is None or value == "":
        return ()
    if isinstance(value, (list, tuple)):
        return tuple(str(item).strip() for item in value if str(item).strip())
    return tuple(item.strip() for item in str(value).split(",") if item.strip())


def _as_ints(value: object) -> list[int]:
    result: list[int] = []
    for item in _as_strings(value):
        match = re.search(r"\d+", item)
        if match:
            result.append(int(match.group()))
    return result


def _optional_float(value: object) -> float | None:
    if value is None or value == "":
        return None
    return float(str(value).strip())


def _float(value: object, default: float) -> float:
    try:
        return float(str(value).strip())
    except (TypeError, ValueError):
        return default


def _bool(value: object, default: bool) -> bool:
    if isinstance(value, bool):
        return value
    if str(value).lower() in {"true", "yes", "1"}:
        return True
    if str(value).lower() in {"false", "no", "0"}:
        return False
    return default
