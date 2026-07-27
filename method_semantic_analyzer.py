from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Iterable, Sequence


CmMethodRow = Sequence[object]


@dataclass(frozen=True)
class VariableAssignment:
    row_index: int
    row_number: str
    variable: str
    value: str
    numeric_value: float | None


@dataclass(frozen=True)
class TemperatureSetpointEvent:
    row_index: int
    row_number: str
    target: str
    value: str
    numeric_value: float | None
    variable: str
    source: str


@dataclass(frozen=True)
class RetTimeEvent:
    row_index: int
    row_number: str
    ret_time: str
    value: str
    emission: bool


@dataclass(frozen=True)
class WaitEvent:
    row_index: int
    row_number: str
    command: str
    condition: str


@dataclass(frozen=True)
class TriggerEvent:
    row_index: int
    row_number: str
    name: str
    value: str
    bool_gate: str
    scheduler_variable: str
    rearm_minutes: float | None
    time_window_start: float | None
    time_window_end: float | None
    valve_positions: tuple[str, ...]
    logged_properties: tuple[str, ...]


@dataclass(frozen=True)
class MeasurementBlock:
    block_index: int
    start_row_index: int
    end_row_index: int
    setpoint: TemperatureSetpointEvent
    ret_times: tuple[RetTimeEvent, ...]
    waits: tuple[WaitEvent, ...]
    role: str


@dataclass(frozen=True)
class MethodSemanticSummary:
    variables: tuple[VariableAssignment, ...]
    temperature_setpoints: tuple[TemperatureSetpointEvent, ...]
    ret_times: tuple[RetTimeEvent, ...]
    waits: tuple[WaitEvent, ...]
    triggers: tuple[TriggerEvent, ...]
    measurement_blocks: tuple[MeasurementBlock, ...]
    safety_reset_rows: tuple[int, ...]

    @property
    def temperature_variables(self) -> tuple[str, ...]:
        assigned = {item.variable for item in self.variables}
        return tuple(dict.fromkeys(event.variable for event in self.temperature_setpoints if event.variable and event.variable in assigned))

    def assignments_for_variable(self, variable: str) -> tuple[VariableAssignment, ...]:
        return tuple(item for item in self.variables if item.variable == variable)

    def blocks_for_setpoint(self, setpoint: float, tolerance: float = 1e-9) -> tuple[MeasurementBlock, ...]:
        return tuple(
            block
            for block in self.measurement_blocks
            if block.setpoint.numeric_value is not None and abs(block.setpoint.numeric_value - setpoint) <= tolerance
        )


def analyze_cm_method_rows(rows: Iterable[CmMethodRow]) -> MethodSemanticSummary:
    row_list = [tuple(row) for row in rows]
    variables = _extract_variable_assignments(row_list)
    variable_values = {item.variable: item.numeric_value for item in variables if item.numeric_value is not None}
    temperature_setpoints = _extract_temperature_setpoints(row_list, variable_values)
    ret_times = _extract_ret_times(row_list)
    waits = _extract_waits(row_list)
    triggers = _extract_triggers(row_list)
    blocks = _build_measurement_blocks(row_list, temperature_setpoints, ret_times, waits)
    safety_reset_rows = _detect_safety_reset_rows(row_list, blocks, temperature_setpoints, ret_times)
    return MethodSemanticSummary(
        variables=tuple(variables),
        temperature_setpoints=tuple(temperature_setpoints),
        ret_times=tuple(ret_times),
        waits=tuple(waits),
        triggers=tuple(triggers),
        measurement_blocks=tuple(blocks),
        safety_reset_rows=tuple(safety_reset_rows),
    )


def cm_method_variable_name(text: object) -> str:
    match = re.search(r"\bVariables\.[A-Za-z0-9_]+", str(text or ""))
    return match.group(0) if match else ""


def cm_numeric_value(text: object) -> float | None:
    match = re.search(r"(-?\d+(?:\.\d+)?)", str(text or ""))
    if not match:
        return None
    try:
        return float(match.group(1))
    except ValueError:
        return None


def cm_method_row_text(row: CmMethodRow, column: int) -> str:
    return str(row[column] if len(row) > column else "")


def _extract_variable_assignments(rows: list[tuple[object, ...]]) -> list[VariableAssignment]:
    assignments: list[VariableAssignment] = []
    for index, row in enumerate(rows):
        command = cm_method_row_text(row, 3)
        variable = cm_method_variable_name(command)
        if not variable:
            continue
        value = cm_method_row_text(row, 4)
        assignments.append(
            VariableAssignment(
                row_index=index,
                row_number=cm_method_row_text(row, 0),
                variable=variable,
                value=value,
                numeric_value=cm_numeric_value(value),
            )
        )
    return assignments


def _extract_temperature_setpoints(rows: list[tuple[object, ...]], variable_values: dict[str, float]) -> list[TemperatureSetpointEvent]:
    events: list[TemperatureSetpointEvent] = []
    for index, row in enumerate(rows):
        command = cm_method_row_text(row, 3)
        if "temperature.nominal" not in command.lower():
            continue
        value = cm_method_row_text(row, 4)
        variable = cm_method_variable_name(value)
        numeric_value = variable_values.get(variable) if variable else cm_numeric_value(value)
        source = "variable" if variable else "literal"
        events.append(
            TemperatureSetpointEvent(
                row_index=index,
                row_number=cm_method_row_text(row, 0),
                target=command,
                value=value,
                numeric_value=numeric_value,
                variable=variable,
                source=source,
            )
        )
    return events


def _extract_ret_times(rows: list[tuple[object, ...]]) -> list[RetTimeEvent]:
    events: list[RetTimeEvent] = []
    for index, row in enumerate(rows):
        command = cm_method_row_text(row, 3)
        match = re.search(r"\bRetTimes\.RetTime\d+\b", command)
        if not match:
            continue
        value = cm_method_row_text(row, 4)
        events.append(
            RetTimeEvent(
                row_index=index,
                row_number=cm_method_row_text(row, 0),
                ret_time=match.group(0),
                value=value,
                emission="system.retention" in value.lower(),
            )
        )
    return events


def _extract_waits(rows: list[tuple[object, ...]]) -> list[WaitEvent]:
    events: list[WaitEvent] = []
    for index, row in enumerate(rows):
        command = cm_method_row_text(row, 3)
        value = cm_method_row_text(row, 4)
        if command.strip().lower() != "wait" and "ready" not in value.lower():
            continue
        events.append(
            WaitEvent(
                row_index=index,
                row_number=cm_method_row_text(row, 0),
                command=command,
                condition=value,
            )
        )
    return events


def _extract_triggers(rows: list[tuple[object, ...]]) -> list[TriggerEvent]:
    events: list[TriggerEvent] = []
    for index, row in enumerate(rows):
        command = cm_method_row_text(row, 3).strip()
        if command != "System.Trigger":
            continue
        value = cm_method_row_text(row, 4)
        name = _trigger_name(value)
        bool_gate = _first_match(r"\b(Variables\.GenericBool\d+)\s*=\s*1\b", value)
        scheduler_variable = _first_match(r"System\.Retention\s*>\s*(Variables\.GenericFloat\d+)", value, flags=re.IGNORECASE)
        window_start, window_end = _trigger_retention_window(value)
        following = _trigger_following_rows(rows, index)
        rearm_minutes = _trigger_rearm_minutes(following, scheduler_variable)
        valve_positions = tuple(_trigger_valve_positions(following))
        logged_properties = tuple(_trigger_logged_properties(following))
        events.append(
            TriggerEvent(
                row_index=index,
                row_number=cm_method_row_text(row, 0),
                name=name,
                value=value,
                bool_gate=bool_gate,
                scheduler_variable=scheduler_variable,
                rearm_minutes=rearm_minutes,
                time_window_start=window_start,
                time_window_end=window_end,
                valve_positions=valve_positions,
                logged_properties=logged_properties,
            )
        )
    return events


def _trigger_following_rows(rows: list[tuple[object, ...]], trigger_index: int) -> list[tuple[object, ...]]:
    following: list[tuple[object, ...]] = []
    for row in rows[trigger_index + 1 :]:
        command = cm_method_row_text(row, 3).strip()
        if command == "System.Trigger":
            break
        kind = cm_method_row_text(row, 1)
        if kind == "Stage":
            break
        following.append(row)
    return following


def _trigger_name(value: str) -> str:
    return str(value or "").split(",", 1)[0].strip().strip('"')


def _trigger_retention_window(value: str) -> tuple[float | None, float | None]:
    starts = [
        float(match.group(1))
        for match in re.finditer(r"System\.Retention\s*>\s*(-?\d+(?:\.\d+)?)", value or "", flags=re.IGNORECASE)
    ]
    ends = [
        float(match.group(1))
        for match in re.finditer(r"System\.Retention\s*<\s*(-?\d+(?:\.\d+)?)", value or "", flags=re.IGNORECASE)
    ]
    return (starts[-1] if starts else None, ends[-1] if ends else None)


def _trigger_rearm_minutes(rows: list[tuple[object, ...]], scheduler_variable: str) -> float | None:
    if not scheduler_variable:
        return None
    for row in rows[:8]:
        command = cm_method_row_text(row, 3).strip()
        if command != scheduler_variable:
            continue
        value = cm_method_row_text(row, 4)
        match = re.search(r"System\.Retention\s*\+\s*(-?\d+(?:\.\d+)?)", value, flags=re.IGNORECASE)
        if match:
            return float(match.group(1))
    return None


def _trigger_valve_positions(rows: list[tuple[object, ...]]) -> list[str]:
    positions: list[str] = []
    for row in rows:
        command = cm_method_row_text(row, 3)
        if "Valve.CurrentPosition" in command:
            positions.append(f"{command}={cm_method_row_text(row, 4)}")
    return positions


def _trigger_logged_properties(rows: list[tuple[object, ...]]) -> list[str]:
    properties: list[str] = []
    for row in rows:
        if cm_method_row_text(row, 3).strip() == "Log":
            properties.append(cm_method_row_text(row, 4))
    return properties


def _first_match(pattern: str, value: str, flags: int = 0) -> str:
    match = re.search(pattern, value or "", flags=flags)
    return match.group(1) if match else ""


def _build_measurement_blocks(
    rows: list[tuple[object, ...]],
    setpoints: list[TemperatureSetpointEvent],
    ret_times: list[RetTimeEvent],
    waits: list[WaitEvent],
) -> list[MeasurementBlock]:
    blocks: list[MeasurementBlock] = []
    for index, setpoint in enumerate(setpoints):
        next_start = setpoints[index + 1].row_index if index + 1 < len(setpoints) else len(rows)
        block_ret_times = tuple(item for item in ret_times if setpoint.row_index <= item.row_index < next_start and item.emission)
        block_waits = tuple(item for item in waits if setpoint.row_index <= item.row_index < next_start)
        role = "measurement"
        if not block_ret_times and index == len(setpoints) - 1:
            role = "safety_reset"
        elif not block_ret_times and not block_waits:
            role = "setup"
        blocks.append(
            MeasurementBlock(
                block_index=index + 1,
                start_row_index=setpoint.row_index,
                end_row_index=max(setpoint.row_index, next_start - 1),
                setpoint=setpoint,
                ret_times=block_ret_times,
                waits=block_waits,
                role=role,
            )
        )
    return blocks


def _detect_safety_reset_rows(
    rows: list[tuple[object, ...]],
    blocks: list[MeasurementBlock],
    setpoints: list[TemperatureSetpointEvent],
    ret_times: list[RetTimeEvent],
) -> list[int]:
    if not setpoints:
        return []
    emitted_rows = [item.row_index for item in ret_times if item.emission]
    last_emission = max(emitted_rows) if emitted_rows else -1
    reset_rows = [block.setpoint.row_index for block in blocks if block.role == "safety_reset" and block.setpoint.row_index > last_emission]
    for event in setpoints:
        if event.row_index > last_emission and event.row_index not in reset_rows:
            command_context = " ".join(cm_method_row_text(rows[index], 3).lower() for index in range(event.row_index, min(len(rows), event.row_index + 4)))
            if "stop" in command_context or "triggerstab" in command_context or event.numeric_value in {20.0, 25.0}:
                reset_rows.append(event.row_index)
    return sorted(set(reset_rows))
