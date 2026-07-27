from __future__ import annotations

from dataclasses import dataclass
import re
from pathlib import Path
from typing import Any


STAGE_NAMES = {
    "Instrument Setup",
    "InstrumentSetup",
    "Equilibration",
    "Inject Preparation",
    "InjectPreparation",
    "Inject",
    "Start Run",
    "StartRun",
    "Run",
    "Stop Run",
    "StopRun",
    "Post Run",
    "PostRun",
}

TRIGGER_PARAM_NAMES = {"Condition", "TrueTime", "Delay", "Limit", "Hysteresis", "AllowImmediateExecution"}
TRIGGER_PARAM_PREFIXES = ("TrueTime=", "Delay=", "Limit=", "Hysteresis=", "AllowImmediateExecution=")


@dataclass(frozen=True)
class MethodMdLintIssue:
    severity: str
    code: str
    row: str
    message: str

    def display(self) -> str:
        row_text = f"Row {self.row}: " if self.row and self.row != "-" else ""
        return f"{self.severity.upper()} {self.code}: {row_text}{self.message}"


def lint_method_md(path: Path) -> list[MethodMdLintIssue]:
    from tools.render_cm_method_md import parse_md_to_rows

    return lint_method_rows(parse_md_to_rows(path))


def lint_method_rows(rows: list[Any]) -> list[MethodMdLintIssue]:
    issues: list[MethodMdLintIssue] = []
    inside_trigger = False
    trigger_start_row = "-"
    trigger_has_condition = False
    trigger_has_true_time = False
    trigger_has_limit = False
    current_stage = ""
    declared_run_duration: float | None = None
    declared_run_duration_row = "-"
    stop_run_time: float | None = None
    stop_run_row = "-"
    max_run_time = 0.0
    max_run_time_row = "-"
    placeholder_valves: dict[str, str] = {}

    for row in rows:
        row_id = _row_id(row)
        kind = _field(row, "Kind")
        time = _field(row, "Time")
        command = _field(row, "Command")
        value = _field(row, "Value")

        if kind == "Stage" and command in STAGE_NAMES:
            current_stage = _normalize_stage(command)
            if current_stage == "Run":
                duration = _duration_from_value(value)
                if duration is not None:
                    declared_run_duration = duration
                    declared_run_duration_row = row_id
            elif current_stage == "Stop Run" and _looks_float(time):
                stop_run_time = float(time)
                stop_run_row = row_id

        if current_stage == "Run" and _looks_float(time):
            numeric_time = float(time)
            if numeric_time > max_run_time:
                max_run_time = numeric_time
                max_run_time_row = row_id

        if kind == "Comment" and _looks_float(time):
            issues.append(
                MethodMdLintIssue(
                    "error",
                    "TIMED_COMMENT",
                    row_id,
                    "Numeric Time cannot be used for prose-only comment rows. Use a real Stage/Command/Trigger row and put the explanation in Comment.",
                )
            )

        if command == "Run":
            duration = _duration_from_value(value)
            if duration is not None:
                declared_run_duration = duration
                declared_run_duration_row = row_id

        placeholder_match = re.match(r"^(Valve\d+)\.", command)
        if placeholder_match:
            placeholder_valves.setdefault(placeholder_match.group(1), row_id)

        if time == "Trigger" or command == "Trigger":
            if inside_trigger:
                issues.append(
                    MethodMdLintIssue(
                        "error",
                        "NESTED_TRIGGER",
                        row_id,
                        "A Trigger started before the previous Trigger was closed with End Trigger.",
                    )
                )
            inside_trigger = True
            trigger_start_row = row_id
            trigger_has_condition = False
            trigger_has_true_time = False
            trigger_has_limit = False
            _check_trigger_name(command, value, row_id, issues)
            continue

        if time == "End Trigger" or command == "End Trigger":
            if not inside_trigger:
                issues.append(MethodMdLintIssue("error", "ORPHAN_END_TRIGGER", row_id, "End Trigger appears outside a Trigger block."))
            else:
                if not trigger_has_condition:
                    issues.append(MethodMdLintIssue("error", "TRIGGER_NO_CONDITION", trigger_start_row, "Trigger block has no Condition parameter."))
                if not trigger_has_true_time:
                    issues.append(MethodMdLintIssue("error", "TRIGGER_NO_TRUETIME", trigger_start_row, "Trigger block has no TrueTime parameter."))
                if not trigger_has_limit:
                    issues.append(MethodMdLintIssue("warning", "TRIGGER_NO_LIMIT", trigger_start_row, "Trigger block has no Limit parameter; leave blank only when this is intentional."))
            inside_trigger = False
            continue

        if inside_trigger:
            if kind == "Branch":
                issues.append(
                    MethodMdLintIssue(
                        "error",
                        "TRIGGER_BRANCH",
                        row_id,
                        "Branch rows inside Trigger are not valid structural MD. Split the logic into separate triggers or verified command rows.",
                    )
                )
            param_name = _trigger_param_name(time, command)
            if param_name == "Condition":
                trigger_has_condition = True
            elif param_name == "TrueTime":
                trigger_has_true_time = True
            elif param_name == "Limit":
                trigger_has_limit = True
                limit_value = _trigger_param_value(time, command, value)
                if limit_value.strip().lower() in {"infinite", "inf", "unlimited"}:
                    issues.append(
                        MethodMdLintIssue(
                            "error",
                            "TRIGGER_LIMIT_INVALID",
                            row_id,
                            "Trigger Limit must be numeric or blank. Do not write Infinite/inf/unlimited.",
                        )
                    )
            if param_name in {"Delay", "Hysteresis", "AllowImmediateExecution"}:
                param_value = _trigger_param_value(time, command, value)
                if any(token in param_value for token in ("Variables.", "System.", "ColumnComp.", "PumpModule.", "SamplerModule.")):
                    issues.append(
                        MethodMdLintIssue(
                            "error",
                            "TRIGGER_PARAM_SYMBOL",
                            row_id,
                            f"Trigger {param_name} expects a literal value, not a CM symbol/expression.",
                        )
                    )
        elif _is_trigger_param_outside(command):
            issues.append(
                MethodMdLintIssue(
                    "error",
                    "TRIGGER_PARAM_OUTSIDE",
                    row_id,
                    "Trigger parameters such as Condition/TrueTime/Limit must appear inside a Trigger block.",
                )
            )

        if command == "Log" and value.startswith('"') and value.endswith('"'):
            issues.append(
                MethodMdLintIssue(
                    "warning",
                    "LOG_TEXT",
                    row_id,
                    "Log with a string literal is usually wrong for CM data/audit anchors. Use Protocol/Message for text unless source evidence proves this pattern.",
                )
            )

        if command == "Message" and value and not _is_quoted_string(value):
            issues.append(
                MethodMdLintIssue(
                    "error",
                    "MESSAGE_TEXT_UNQUOTED",
                    row_id,
                    "Message text must be a quoted CM string literal. Example: Message -> \"Test stopped.\"",
                )
            )

    if inside_trigger:
        issues.append(MethodMdLintIssue("error", "UNCLOSED_TRIGGER", trigger_start_row, "Trigger block is not closed with End Trigger."))

    if declared_run_duration is not None and max_run_time > declared_run_duration + 0.0001:
        issues.append(
            MethodMdLintIssue(
                "error",
                "RUN_DURATION_TOO_SHORT",
                declared_run_duration_row,
                f"Run Duration is {declared_run_duration:g} min, but Run-stage row {max_run_time_row} is at {max_run_time:g} min.",
            )
        )
    if stop_run_time is not None and max_run_time > stop_run_time + 0.0001:
        issues.append(
            MethodMdLintIssue(
                "error",
                "RUN_ROW_AFTER_STOP",
                max_run_time_row,
                f"Run-stage row is at {max_run_time:g} min, but Stop Run starts at {stop_run_time:g} min.",
            )
        )
    if declared_run_duration is not None and stop_run_time is not None and abs(declared_run_duration - stop_run_time) > 0.0001:
        issues.append(
            MethodMdLintIssue(
                "error",
                "RUN_STOP_MISMATCH",
                declared_run_duration_row,
                f"Run Duration ({declared_run_duration:g} min) must match Stop Run time ({stop_run_time:g} min at row {stop_run_row}).",
            )
        )
    if placeholder_valves:
        valves = ", ".join(f"{name} (row {row_id})" for name, row_id in sorted(placeholder_valves.items()))
        issues.append(
            MethodMdLintIssue(
                "warning",
                "PLACEHOLDER_VALVE",
                "-",
                f"Placeholder valve command path(s) detected: {valves}. Replace with exact CM valve symbols from instrument configuration.",
            )
        )
    return issues


def lint_error_rows(rows: list[Any]) -> set[str]:
    return {issue.row for issue in lint_method_rows(rows) if issue.severity == "error" and issue.row and issue.row != "-"}


def _field(row: Any, name: str) -> str:
    if isinstance(row, dict):
        return str(row.get(name, "") or "").strip()
    attr = name.lower()
    return str(getattr(row, attr, "") or getattr(row, name, "") or "").strip()


def _row_id(row: Any) -> str:
    return _field(row, "#") or _field(row, "Index") or "?"


def _looks_float(value: str) -> bool:
    try:
        float(str(value).strip())
        return True
    except (TypeError, ValueError):
        return False


def _is_quoted_string(value: str) -> bool:
    text = str(value or "").strip()
    return len(text) >= 2 and text.startswith('"') and text.endswith('"')


def _duration_from_value(value: str) -> float | None:
    match = re.search(r"Duration\s*=\s*([-+]?\d+(?:\.\d+)?)", value or "")
    return float(match.group(1)) if match else None


def _normalize_stage(command: str) -> str:
    compact = command.replace(" ", "")
    return {
        "InstrumentSetup": "Instrument Setup",
        "InjectPreparation": "Inject Preparation",
        "StartRun": "Start Run",
        "StopRun": "Stop Run",
        "PostRun": "Post Run",
    }.get(compact, command)


def _check_trigger_name(command: str, value: str, row_id: str, issues: list[MethodMdLintIssue]) -> None:
    name = value.strip() if command.strip() == "Trigger" else (command.strip() or value.strip())
    if not name:
        issues.append(MethodMdLintIssue("error", "TRIGGER_NO_NAME", row_id, "Trigger row must provide a quoted trigger name in Command or Value."))
    elif not name.lstrip().startswith('"'):
        issues.append(MethodMdLintIssue("warning", "TRIGGER_NAME_QUOTE", row_id, "Trigger name should be quoted, for example \"T_HOLD_40\",."))


def _trigger_param_name(time: str, command: str) -> str:
    for text in (command, time):
        if text in TRIGGER_PARAM_NAMES:
            return text
        for prefix in TRIGGER_PARAM_PREFIXES:
            if text.startswith(prefix):
                return prefix.split("=", 1)[0]
    if command == "Condition" or (not command and _looks_like_condition(time)):
        return "Condition"
    if _looks_like_condition(command):
        return "Condition"
    return ""


def _trigger_param_value(time: str, command: str, value: str) -> str:
    if value:
        return value
    for text in (command, time):
        if "=" in text:
            return text.split("=", 1)[1].strip().rstrip(",")
    return ""


def _is_trigger_param_outside(command: str) -> bool:
    if command == "Delay":
        # Delay is also a normal CM command outside Trigger blocks.
        return False
    return command in TRIGGER_PARAM_NAMES or command.startswith(TRIGGER_PARAM_PREFIXES)


def _looks_like_condition(text: str) -> bool:
    stripped = text.strip()
    if not stripped:
        return False
    return any(token in stripped for token in (" AND ", " OR ", "<=", ">=", "<>", "=", "System.Retention"))
