from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


@dataclass(frozen=True)
class InstrumentMethodLine:
    time: str
    command: str
    value: str
    comment: str


@dataclass(frozen=True)
class InstrumentMethodText:
    path: Path
    lines: list[InstrumentMethodLine]

    @property
    def commands(self) -> list[InstrumentMethodLine]:
        return [line for line in self.lines if line.command]

    @property
    def triggers(self) -> list[InstrumentMethodLine]:
        return [line for line in self.lines if line.command.lower() == "trigger" or line.time.lower() == "trigger"]

    @property
    def ret_times(self) -> list[InstrumentMethodLine]:
        return [line for line in self.lines if line.command.startswith("RetTimes.")]

    @property
    def setpoints(self) -> list[InstrumentMethodLine]:
        return [line for line in self.lines if "Temperature.Nominal" in line.command or line.command.startswith("Variables.GenericDouble")]

    def summary_text(self, max_lines: int = 140) -> str:
        interesting = []
        for line in self.lines:
            text = "\t".join(part for part in (line.time, line.command, line.value, line.comment) if part)
            if not text:
                continue
            lowered = text.lower()
            if any(token in lowered for token in ("trigger", "rettimes.", "temperature.nominal", "genericdouble", "wait", "tempready", "exttemp", "sig_value")):
                interesting.append(text)
        preview = interesting[:max_lines]
        suffix = f"\n... {len(interesting) - max_lines} more key lines" if len(interesting) > max_lines else ""
        return "\n".join(
            [
                f"External Instrument Method TXT: {self.path}",
                f"Parsed rows: {len(self.lines)}",
                f"Command rows: {len(self.commands)}",
                f"Triggers: {len(self.triggers)}",
                f"RetTime assignments: {len(self.ret_times)}",
                f"Temperature / setpoint rows: {len(self.setpoints)}",
                "",
                "Key Lines",
                "---------",
                *(preview or ["No key lines matched."]),
            ]
        ) + suffix

    def source_text(self) -> str:
        return _read_method_text(self.path)

    def flow_text(self) -> str:
        setpoint_groups = self._setpoint_groups()
        acquisition_channels = self._acquisition_channels()
        measurement_steps = self._measurement_steps()
        trigger_blocks = self._trigger_blocks()

        lines = [
            f"Instrument Method Flow: {self.path.name}",
            "=" * (24 + len(self.path.name)),
            "",
            "Purpose",
            "-------",
            "This view condenses the exported Chromeleon method TXT into the execution flow used for temperature accuracy analysis.",
            "",
            "Setpoint Definitions",
            "--------------------",
        ]
        if setpoint_groups:
            for condition, values in setpoint_groups:
                lines.append(condition)
                for variable, value, comment in values:
                    note = f" - {comment}" if comment else ""
                    lines.append(f"  {variable}: {value}{note}")
        else:
            lines.append("No GenericDouble temperature setpoint definitions were found.")

        lines.extend(["", "Stability Logic", "---------------"])
        ready_delta = self._last_value_for_command("ColumnComp.CC.ReadyTempDelta")
        equilibration = self._last_value_for_command("ColumnComp.CC.EquilibrationTime")
        if ready_delta:
            lines.append(f"Instrument ready window: ColumnComp.CC.ReadyTempDelta = {ready_delta}")
        if equilibration:
            lines.append(f"Instrument equilibration time: ColumnComp.CC.EquilibrationTime = {equilibration} min")
        if trigger_blocks:
            for block in trigger_blocks:
                lines.append(f"- Trigger {block['name']}: {block['condition']}")
                if block["summary"]:
                    lines.append(f"  {block['summary']}")
        else:
            lines.append("No trigger blocks were found.")
        lines.append("External sensor stability rule inferred from the method: upper and lower external sensors must stay inside their logged value +/- 0.05 for four consecutive 30 s checks, then UpperReady/LowerReady are set.")
        lines.append("Abort rule inferred from the method: each nominal temperature must become stable within 40 min, otherwise the queue is aborted.")

        lines.extend(["", "Acquired Channels", "-----------------"])
        if acquisition_channels:
            lines.extend(f"- {channel}" for channel in acquisition_channels)
        else:
            lines.append("No *.AcqOn channel commands were found.")

        lines.extend(["", "Measurement Sequence", "--------------------"])
        if measurement_steps:
            for step in measurement_steps:
                lines.append(f"{step['index']}. Target {step['setpoint']}: wait until {step['wait']}; record {step['rettime']} = {step['value']}.")
                if step["next_setpoint"]:
                    lines.append(f"   Then set next nominal temperature to {step['next_setpoint']} and delay for transition.")
        else:
            lines.append("No RetTimes.RetTimeN = System.Retention measurement steps were found.")

        lines.extend(["", "Accuracy Calculation Window", "---------------------------"])
        if measurement_steps:
            for step in measurement_steps:
                ret_time = step["rettime"].split(".")[-1]
                lines.append(
                    f"- {step['setpoint']}: average external temperature from {ret_time} - 1.0 min to {ret_time} - 0.2 min; accuracy = observed average - nominal setpoint."
                )
        else:
            lines.append("Accuracy windows require RetTimes.RetTimeN assignments.")
        return "\n".join(lines)

    def _setpoint_groups(self) -> list[tuple[str, list[tuple[str, str, str]]]]:
        groups: list[tuple[str, list[tuple[str, str, str]]]] = []
        current_condition = "Default"
        current_values: list[tuple[str, str, str]] = []
        for line in self.lines:
            if line.time in {"If", "Else If"} and "ModelNo" in line.value:
                if current_values:
                    groups.append((current_condition, current_values))
                    current_values = []
                current_condition = line.value
            elif line.time == "Else" and current_values:
                groups.append((current_condition, current_values))
                current_condition = "Else"
                current_values = []
            elif line.command.startswith("Variables.GenericDouble"):
                current_values.append((line.command, line.value, line.comment))
        if current_values:
            groups.append((current_condition, current_values))
        return groups

    def _acquisition_channels(self) -> list[str]:
        channels: list[str] = []
        for line in self.lines:
            command = line.command
            if command.endswith(".AcqOn") and command not in channels:
                channels.append(command.removesuffix(".AcqOn"))
        return channels

    def _measurement_steps(self) -> list[dict[str, str]]:
        steps: list[dict[str, str]] = []
        for index, line in enumerate(self.lines):
            match = re.match(r"RetTimes\.RetTime(\d+)$", line.command)
            if not match or line.value != "System.Retention":
                continue
            wait = self._nearest_previous_wait(index)
            next_setpoint = self._nearest_next_nominal(index)
            nominal = f"Variables.GenericDouble{match.group(1)}"
            steps.append(
                {
                    "index": match.group(1),
                    "setpoint": nominal,
                    "wait": wait or "ready condition not found",
                    "rettime": line.command,
                    "value": line.value,
                    "next_setpoint": next_setpoint,
                }
            )
        return steps

    def _nearest_previous_wait(self, index: int) -> str:
        for line in reversed(self.lines[max(0, index - 8) : index]):
            if line.command == "Wait":
                return line.value.rstrip(",")
        return ""

    def _nearest_next_nominal(self, index: int) -> str:
        for line in self.lines[index + 1 : min(len(self.lines), index + 8)]:
            if line.command == "ColumnComp.CC.Temperature.Nominal":
                return line.value
        return ""

    def _trigger_blocks(self) -> list[dict[str, str]]:
        blocks: list[dict[str, str]] = []
        index = 0
        while index < len(self.lines):
            line = self.lines[index]
            if line.time.lower() != "trigger" and line.command.lower() != "trigger":
                index += 1
                continue
            name = (line.value or line.command or line.time).strip('",')
            block_lines: list[InstrumentMethodLine] = []
            index += 1
            while index < len(self.lines):
                current = self.lines[index]
                if current.time.lower() == "end trigger" or current.command.lower() == "end trigger":
                    break
                block_lines.append(current)
                index += 1
            blocks.append({"name": name, "condition": self._trigger_condition(block_lines), "summary": self._trigger_summary(name, block_lines)})
            index += 1
        return blocks

    def _trigger_condition(self, block_lines: list[InstrumentMethodLine]) -> str:
        for line in block_lines:
            text = "\t".join(part for part in (line.time, line.command, line.value) if part).rstrip(",")
            if text and not text.startswith("TrueTime") and not text.startswith("Delay") and not text.startswith("AllowImmediateExecution"):
                return text
        return "condition not found"

    def _trigger_summary(self, name: str, block_lines: list[InstrumentMethodLine]) -> str:
        commands = {line.command for line in block_lines if line.command}
        lowered_name = name.lower()
        if "gradient" in lowered_name:
            return "Runs as a 30 s stability check and alternates TriggerStab1/TriggerStab2 while updating upper/lower ready counters."
        if "exitrange_upper" in lowered_name:
            return "Resets upper external-sensor stability when the upper signal leaves the +/-0.05 range or CC is no longer ready."
        if "exitrange_lower" in lowered_name:
            return "Resets lower external-sensor stability when the lower signal leaves the +/-0.05 range or CC is no longer ready."
        if "abort" in lowered_name:
            return "Aborts the queue if a temperature step remains unstable for more than 40 min."
        if commands:
            return "Updates: " + ", ".join(sorted(commands)[:6])
        return ""

    def _last_value_for_command(self, command: str) -> str:
        values = [line.value for line in self.lines if line.command == command and line.value]
        return values[-1] if values else ""


def parse_instrument_method_txt(path: str | Path) -> InstrumentMethodText:
    method_path = Path(path)
    lines: list[InstrumentMethodLine] = []
    for raw_line in _read_method_text(method_path).splitlines():
        parts = raw_line.rstrip("\r\n").split("\t")
        parts += [""] * (4 - len(parts))
        time, command, value, comment = (part.strip() for part in parts[:4])
        if not any((time, command, value, comment)):
            continue
        lines.append(InstrumentMethodLine(time=time, command=command, value=value, comment=comment))
    return InstrumentMethodText(path=method_path, lines=lines)


def _read_method_text(path: Path) -> str:
    data = path.read_bytes()
    text = data.decode("utf-8-sig", errors="replace")
    if "\ufffd" in text:
        text = data.decode("cp1252", errors="replace")
    return text


def discover_external_instrument_methods(cmbx_path: str | Path, method_names: list[str]) -> dict[str, InstrumentMethodText]:
    folder = Path(cmbx_path).parent
    txt_files = sorted(folder.glob("*Method*.txt"), key=lambda path: path.name.lower())
    discovered: dict[str, InstrumentMethodText] = {}
    for txt_file in txt_files:
        matched_name = _match_method_name(txt_file, method_names)
        if not matched_name:
            continue
        discovered[matched_name] = parse_instrument_method_txt(txt_file)
    return discovered


def _match_method_name(path: Path, method_names: list[str]) -> str | None:
    file_text = _normalize(path.stem)
    for method_name in method_names:
        method_text = _normalize(method_name)
        if method_text and (method_text in file_text or file_text in method_text):
            return method_name
    if "accuracy" in file_text:
        return next((name for name in method_names if _normalize(name) == "temperatureaccuracy"), None)
    if "calibration" in file_text:
        return next((name for name in method_names if "calibration" in _normalize(name)), None)
    return None


def _normalize(value: str) -> str:
    return "".join(ch for ch in value.lower() if ch.isalnum())
