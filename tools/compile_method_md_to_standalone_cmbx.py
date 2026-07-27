from __future__ import annotations

import argparse
import copy
import re
import sys
import tempfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path

TOOL_ROOT = Path(__file__).resolve().parents[1]
if str(TOOL_ROOT) not in sys.path:
    sys.path.insert(0, str(TOOL_ROOT))
TOOLS_ROOT = TOOL_ROOT / "tools"
if str(TOOLS_ROOT) not in sys.path:
    sys.path.insert(0, str(TOOLS_ROOT))

from chromeleon_method_decoder import decode_cpxm_method_xml
from cmbx_container import extract_cmbx_entry, load_cmbx_package
from embedded_method_extractor import _extract_method_payload
from method_md_linter import lint_method_rows
from repack_standalone_instmeth_cmbx import repack_standalone_method_cmbx
from render_cm_method_md import parse_md_to_rows


DISPLAY_TO_XML_STAGE = {
    "Instrument Setup": "InstrumentSetup",
    "InstrumentSetup": "InstrumentSetup",
    "Equilibration": "Equilibration",
    "Inject Preparation": "InjectPreparation",
    "InjectPreparation": "InjectPreparation",
    "Start Run": "StartRun",
    "StartRun": "StartRun",
    "Run": "Run",
    "Stop Run": "StopRun",
    "StopRun": "StopRun",
    "Post Run": "PostRun",
    "PostRun": "PostRun",
}

COMMAND_STEP_NAMES = {
    "Delay",
    "Wait",
    "Log",
    "Message",
    "Protocol",
    "VirtualChannel",
    "System.AbortQueue",
    "End",
}

COMMAND_SUFFIXES = (
    ".AcqOn",
    ".AcqOff",
    ".GetServiceCode",
    "._SendCommand",
    ".AbortModalCommand",
    ".SwitchValve",
)

TRIGGER_PARAM_PREFIXES = ("TrueTime=", "Limit=", "Hysteresis=", "AllowImmediateExecution=")
TRIGGER_PARAM_NAMES = {"TrueTime", "Limit", "Hysteresis", "AllowImmediateExecution"}


@dataclass
class SourceRow:
    index: str
    kind: str
    time: str
    command: str
    value: str
    comment: str
    raw: str


class NodeFactory:
    def __init__(self, start: int = 900000, prototypes: dict[str, ET.Element] | None = None) -> None:
        self.next_id = start
        self.prototypes = prototypes or {}

    def node_id(self) -> str:
        value = str(self.next_id)
        self.next_id += 1
        return value

    def clone(self, key: str, fallback_type: str) -> ET.Element:
        prototype = self.prototypes.get(key) or self.prototypes.get(fallback_type)
        if prototype is None:
            return ET.Element("Item", {"type": fallback_type})
        node = copy.deepcopy(prototype)
        self.renumber(node)
        return node

    def renumber(self, node: ET.Element) -> None:
        for child in node.iter("NodeId"):
            child.attrib["value"] = self.node_id()


def compile_method_md_to_cmbx(source_cmbx: Path, source_md: Path, output_cmbx: Path, method_name: str | None = None) -> dict[str, int]:
    xml_text = _decode_source_method_xml(source_cmbx)
    root = ET.fromstring(xml_text)
    rows = _read_md_rows(source_md)
    issues = lint_method_rows(rows)
    errors = [issue for issue in issues if issue.severity == "error"]
    if errors:
        details = "\n".join(issue.display() for issue in errors[:20])
        if len(errors) > 20:
            details += f"\n... {len(errors) - 20} more error(s)"
        raise ValueError(f"Method MD preflight failed:\n{details}")
    stats = _replace_method_children(root, rows)
    with tempfile.TemporaryDirectory(prefix="cmbx_md_compile_") as tmp:
        xml_path = Path(tmp) / "compiled.xml"
        ET.ElementTree(root).write(xml_path, encoding="utf-8", xml_declaration=False)
        repack_standalone_method_cmbx(source_cmbx, xml_path, output_cmbx, method_name=method_name or source_md.stem)
    stats["rows"] = len(rows)
    return stats


def _decode_source_method_xml(source_cmbx: Path) -> str:
    package = load_cmbx_package(source_cmbx)
    methods = [element for element in package.methods_and_reports if element.kind == "instrument_method"]
    if len(methods) != 1:
        raise ValueError(f"Expected exactly one standalone instrument method, found {len(methods)}.")
    entry_name = methods[0].package_entry_name
    data = extract_cmbx_entry(source_cmbx, entry_name)
    payload = _extract_method_payload(data, 0)
    if payload is None:
        raise ValueError(f"Could not locate method payload inside {entry_name}.")
    with tempfile.TemporaryDirectory(prefix="cmbx_md_decode_") as tmp:
        tmp_root = Path(tmp)
        cpxm_path = tmp_root / "source.cpxm"
        xml_path = tmp_root / "source.xml"
        cpxm_path.write_bytes(payload.cpxm_payload)
        result = decode_cpxm_method_xml(cpxm_path, xml_path)
        if not result.ok:
            raise RuntimeError(result.message)
        return xml_path.read_text(encoding="utf-8")


def _replace_method_children(root: ET.Element, rows: list[SourceRow]) -> dict[str, int]:
    method = root.find("Method")
    if method is None:
        raise ValueError("Decoded method XML has no Method root child.")
    children = method.find("Children")
    if children is None:
        children = ET.SubElement(method, "Children", {"type": "SyntaxNodeCollection"})

    prototypes = _build_prototypes(root)
    stage_nodes: dict[str, ET.Element] = {}
    for child in list(children):
        if child.attrib.get("type") == "StageNode":
            stage_nodes[_stage_name(child)] = child
            _clear_collection_children(_children(child))
    initialized_stages: set[str] = set()
    factory = NodeFactory(_max_node_id(root) + 1, prototypes)
    timing = _method_timing_contract(rows)
    state = {
        "stage": None,
        "time_step": None,
        "pending_terminal_stage": None,
        "pending_terminal_time": None,
        "stage_count": 0,
        "time_count": 0,
        "command_count": 0,
        "trigger_count": 0,
        "comment_count": 0,
    }

    def flush_pending_terminal() -> None:
        stage = state.get("pending_terminal_stage")
        time_text = state.get("pending_terminal_time")
        if stage is not None and time_text:
            terminal = _new_time_step(factory, _format_number(float(time_text)))
            _children(stage).append(terminal)
            state["time_count"] += 1
        state["pending_terminal_stage"] = None
        state["pending_terminal_time"] = None

    def ensure_stage(display_name: str = "Instrument Setup", time_text: str = "") -> ET.Element:
        xml_name = DISPLAY_TO_XML_STAGE.get(display_name.strip(), display_name.strip().replace(" ", ""))
        stage = state.get("stage")
        if stage is not None and _stage_name(stage) == xml_name:
            if state.get("time_step") is None:
                state["time_step"] = _new_time_step(factory, _internal_time(time_text or "{Initial Time}"))
                _children(stage).append(state["time_step"])
                state["time_count"] += 1
            return stage
        flush_pending_terminal()
        stage = stage_nodes.get(xml_name)
        if stage is None:
            stage = _new_stage(factory, xml_name)
            children.append(stage)
            stage_nodes[xml_name] = stage
        state["stage"] = stage
        if xml_name not in initialized_stages:
            state["time_step"] = _new_time_step(factory, _internal_time(time_text or ("{Initial Time}" if xml_name == "InstrumentSetup" else "0.000")))
            _children(stage).append(state["time_step"])
            initialized_stages.add(xml_name)
            state["stage_count"] += 1
            state["time_count"] += 1
        else:
            stage_children = _children(stage)
            existing_times = [item for item in stage_children if item.attrib.get("type") == "TimeStepNode"]
            state["time_step"] = existing_times[-1] if existing_times else None
            if state["time_step"] is None:
                state["time_step"] = _new_time_step(factory, _internal_time(time_text or "0.000"))
                stage_children.append(state["time_step"])
                state["time_count"] += 1
        return stage

    def ensure_time_step(time_text: str = "") -> ET.Element:
        if state.get("stage") is None:
            ensure_stage("Instrument Setup", "{Initial Time}")
        if time_text:
            state["time_step"] = _new_time_step(factory, _internal_time(time_text))
            _children(state["stage"]).append(state["time_step"])
            state["time_count"] += 1
        elif state.get("time_step") is None:
            state["time_step"] = _new_time_step(factory, _internal_time(""))
            _children(state["stage"]).append(state["time_step"])
            state["time_count"] += 1
        return state["time_step"]

    index = 0
    while index < len(rows):
        row = rows[index]
        if _is_empty(row):
            index += 1
            continue
        if _is_stage_row(row):
            ensure_stage(row.command, row.time)
            duration = _duration_from_value(row.value)
            if duration is not None and row.command.strip() == "Run":
                duration = timing["run_duration"]
                # CM stores the stage duration as a terminal time step in the
                # Run stage. Append it after all explicit Run rows have been
                # compiled, not immediately after the Run stage row.
                state["pending_terminal_stage"] = state["stage"]
                state["pending_terminal_time"] = _format_number(duration)
            index += 1
            continue
        if _is_time_marker(row):
            ensure_time_step(row.time)
            index += 1
            continue
        row_time = row.time.strip()
        parent = _children(ensure_time_step(row_time if _looks_numeric_time(row_time) else ""))
        if _is_branch_start(row):
            if_node, consumed = _compile_if_block(factory, rows, index)
            parent.append(if_node)
            state["command_count"] += _count_command_nodes(if_node)
            index = consumed
            continue
        if _is_trigger_start(row):
            trigger_node, consumed = _compile_trigger(factory, rows, index)
            parent.append(trigger_node)
            state["trigger_count"] += 1
            state["command_count"] += _count_command_nodes(trigger_node)
            index = consumed
            continue
        node = _compile_simple_row(factory, row)
        if node is not None:
            parent.append(node)
            if node.attrib.get("type") in {"CommmentNode", "CommentNode"}:
                state["comment_count"] += 1
            else:
                state["command_count"] += 1
        index += 1
    for xml_name, stage in stage_nodes.items():
        if xml_name not in initialized_stages:
            _children(stage).append(_new_time_step(factory, _internal_time("{Initial Time}" if xml_name == "InstrumentSetup" else "0.000")))
            state["time_count"] += 1
    flush_pending_terminal()
    return {key: int(value) for key, value in state.items() if key.endswith("_count")}


def _method_timing_contract(rows: list[SourceRow]) -> dict[str, float]:
    current_stage = ""
    declared_run_duration: float | None = None
    stop_run_time: float | None = None
    max_run_time: float = 0.0
    for row in rows:
        if _is_stage_row(row):
            current_stage = row.command.strip()
            if current_stage == "Run":
                duration = _duration_from_value(row.value)
                if duration is not None:
                    declared_run_duration = duration
            elif current_stage == "Stop Run" and _looks_numeric_time(row.time):
                stop_run_time = float(row.time)
            continue
        if current_stage == "Run" and _looks_numeric_time(row.time):
            max_run_time = max(max_run_time, float(row.time))

    if stop_run_time is not None and max_run_time > stop_run_time + 0.0001:
        raise ValueError(
            f"Run-stage row exists at {max_run_time:g} min, but Stop Run starts at {stop_run_time:g} min. "
            "Move the row before Stop Run or increase the Stop Run time."
        )
    if stop_run_time is not None:
        effective_duration = stop_run_time
    elif declared_run_duration is not None:
        effective_duration = max(declared_run_duration, max_run_time)
    else:
        effective_duration = max_run_time
    return {"run_duration": effective_duration, "max_run_time": max_run_time, "stop_run_time": stop_run_time or 0.0}


def _compile_if_block(factory: NodeFactory, rows: list[SourceRow], start: int) -> tuple[ET.Element, int]:
    block = _new_if_block(factory)
    block_children = _children(block)
    current_branch: ET.Element | None = None
    index = start
    while index < len(rows):
        row = rows[index]
        branch = _branch_keyword(row)
        if branch == "End If":
            index += 1
            break
        if branch in {"If", "Else If", "Else"}:
            current_branch = _new_branch_node(factory, branch, row.command.strip() or row.value.strip())
            block_children.append(current_branch)
            index += 1
            continue
        if current_branch is None:
            index += 1
            continue
        branch_children = _children(current_branch)
        if _is_trigger_start(row):
            trigger_node, consumed = _compile_trigger(factory, rows, index)
            branch_children.append(trigger_node)
            index = consumed
            continue
        child = _compile_simple_row(factory, row)
        if child is not None:
            branch_children.append(child)
        index += 1
    return block, index


def _compile_trigger(factory: NodeFactory, rows: list[SourceRow], start: int) -> tuple[ET.Element, int]:
    start_row = rows[start]
    trigger_name = start_row.value if start_row.command.strip() == "Trigger" else (start_row.command or start_row.value or start_row.time)
    params: list[str] = []
    children: list[ET.Element] = []
    index = start + 1
    while index < len(rows):
        row = rows[index]
        if row.time.strip() == "End Trigger" or row.command.strip() == "End Trigger":
            index += 1
            break
        param = _trigger_param_text(row)
        if param is not None:
            params.append(param)
            index += 1
            continue
        child = _compile_simple_row(factory, row)
        if child is not None:
            children.append(child)
        index += 1
    value = _format_trigger_value(trigger_name, params)
    node = _new_command(factory, "System.Trigger", value, "")
    node_children = _children(node)
    for child in children:
        node_children.append(child)
    return node, index


def _compile_simple_row(factory: NodeFactory, row: SourceRow) -> ET.Element | None:
    if _is_empty(row):
        return None
    command = row.command.strip()
    value = row.value.strip()
    comment = row.comment.strip()
    if row.kind == "Comment":
        return _new_comment(factory, _comment_text(row))
    if not command and row.time:
        command = row.time.strip()
    if _looks_like_comment(command, value, comment):
        return _new_comment(factory, command)
    if _is_command_step(command):
        return _new_command(factory, command, value, comment)
    return _new_property(factory, command, value, comment)


def _read_md_rows(path: Path) -> list[SourceRow]:
    normalized_rows = parse_md_to_rows(path)
    if normalized_rows:
        return [
            SourceRow(
                row.get("#", "").strip(),
                row.get("Kind", "").strip(),
                row.get("Time", "").strip(),
                row.get("Command", "").strip(),
                row.get("Value", "").strip(),
                row.get("Comment", "").strip(),
                "",
            )
            for row in normalized_rows
            if row.get("Kind", "") != "End" or row.get("Command", "").strip() == "End"
        ]
    lines = path.read_text(encoding="utf-8-sig", errors="replace").splitlines()
    rows: list[SourceRow] = []
    for index, line in enumerate(lines):
        if not line.strip():
            continue
        parts = line.rstrip("\r\n").split("\t")
        while len(parts) < 4:
            parts.append("")
        row = SourceRow(str(index), "", parts[0].strip(), parts[1].strip(), parts[2].strip(), parts[3].strip(), line)
        if row.time.lower() == "time" and row.command.lower() == "command":
            continue
        rows.append(row)
    return rows


def _is_empty(row: SourceRow) -> bool:
    return not (row.time or row.command or row.value or row.comment)


def _is_stage_row(row: SourceRow) -> bool:
    return row.command.strip() in DISPLAY_TO_XML_STAGE


def _is_time_marker(row: SourceRow) -> bool:
    return bool(row.time and not row.command and not row.value and _looks_numeric_time(row.time))


def _is_trigger_start(row: SourceRow) -> bool:
    return row.time.strip() == "Trigger" or row.command.strip() == "Trigger"


def _is_branch_start(row: SourceRow) -> bool:
    return _branch_keyword(row) == "If"


def _branch_keyword(row: SourceRow) -> str:
    text = row.time.strip() or row.command.strip()
    if text in {"If", "Else If", "Else", "End If"}:
        return text
    return ""


def _comment_text(row: SourceRow) -> str:
    command = row.command.strip()
    comment = row.comment.strip()
    if command and comment:
        return f"{command}    {comment}"
    return command or comment


def _trigger_param_text(row: SourceRow) -> str | None:
    time = row.time.strip()
    command = row.command.strip()
    value = row.value.strip()
    comment = row.comment.strip()
    if time and not value and (
        time.startswith(TRIGGER_PARAM_PREFIXES)
        or time.endswith(",")
        or any(token in time for token in (" AND ", " OR ", "<=", ">=", "=", "System.Retention"))
    ):
        return time
    if time.startswith(TRIGGER_PARAM_PREFIXES):
        return row.time.strip()
    if command == "Condition":
        return value
    if command in TRIGGER_PARAM_NAMES and value:
        if command == "Limit" and value.strip().lower() in {"infinite", "inf", "unlimited"}:
            return ""
        return f"{command}={value.rstrip(',')}"
    if command.startswith(TRIGGER_PARAM_PREFIXES):
        if command.lower().startswith("limit="):
            limit_value = command.split("=", 1)[1].strip().rstrip(",").lower()
            if limit_value in {"infinite", "inf", "unlimited"}:
                return ""
        return command
    if row.time == "" and (
        command.startswith("(")
        or command.endswith(",")
        or any(token in command for token in (" AND ", " OR ", "<=", ">=", "=", "System.Retention"))
    ):
        return command
    if row.time == "" and row.value == "" and row.comment == "" and (
        command.endswith(",")
        or any(token in command for token in (" AND ", " OR ", "<=", ">=", "=", "System.Retention"))
    ):
        return command
    return None


def _format_trigger_value(trigger_name: str, params: list[str]) -> str:
    parts = [part.strip() for part in [trigger_name, *params] if part and part.strip()]
    if not parts:
        return ""
    normalized: list[str] = []
    for index, part in enumerate(parts):
        if index < len(parts) - 1 and not part.endswith(","):
            part += ","
        if index == len(parts) - 1:
            part = part.rstrip(",")
        normalized.append(part)
    return "\n".join(normalized)


def _looks_like_comment(command: str, value: str, comment: str) -> bool:
    if not command:
        return False
    if value or comment:
        return False
    if command.startswith(("=", "-", "IM ", "HPLC-System", "Parameters ", "Variable ", "Initialize ", "Settings ", "Column compartment", "External ", "Pre-Run", "Trigger ")):
        return True
    if " " in command and not command.startswith(("ColumnComp.", "Thermometer", "Variables.", "RetTimes.", "StabVars.", "TempVars.", "System.", "CC.")):
        return True
    return False


def _is_command_step(command: str) -> bool:
    return command in COMMAND_STEP_NAMES or command.endswith(COMMAND_SUFFIXES)


def _new_stage(factory: NodeFactory, name: str) -> ET.Element:
    node = factory.clone(f"StageNode:{name}", "StageNode")
    node.attrib["type"] = "StageNode"
    _set_or_create_child_attr(node, "StageName", "value", name)
    children = _children(node)
    _clear_collection_children(children)
    return node


def _new_time_step(factory: NodeFactory, internal_value: str) -> ET.Element:
    node = factory.clone("TimeStepNode", "TimeStepNode")
    node.attrib["type"] = "TimeStepNode"
    time = node.find("Time")
    if time is None:
        time = ET.Element("Time", {"type": "MethodTime"})
        node.insert(0, time)
    internal = time.find("InternalValue")
    if internal is None:
        internal = ET.SubElement(time, "InternalValue")
    internal.attrib["value"] = internal_value
    children = _children(node)
    _clear_collection_children(children)
    return node


def _new_comment(factory: NodeFactory, text: str) -> ET.Element:
    node = factory.clone("CommmentNode", "CommmentNode")
    node.attrib["type"] = "CommmentNode"
    _set_or_create_child_attr(node, "Comment", "value", text)
    return node


def _new_if_block(factory: NodeFactory) -> ET.Element:
    node = factory.clone("IfBlockNode", "IfBlockNode")
    node.attrib["type"] = "IfBlockNode"
    children = _children(node)
    _clear_collection_children(children)
    return node


def _new_branch_node(factory: NodeFactory, keyword: str, condition: str = "") -> ET.Element:
    type_name = {"If": "IfNode", "Else If": "ElseIfNode", "Else": "ElseNode"}[keyword]
    node = factory.clone(type_name, type_name)
    node.attrib["type"] = type_name
    children = _children(node)
    _clear_collection_children(children)
    if keyword != "Else":
        _set_or_create_child_attr(node, "Condition", "value", condition)
    else:
        _remove_child(node, "Condition")
    return node


def _new_property(factory: NodeFactory, symbol: str, value: str, comment: str = "") -> ET.Element:
    node = factory.clone(f"PropertyStepNode:{symbol}", "PropertyStepNode")
    node.attrib["type"] = "PropertyStepNode"
    _set_optional_comment(node, comment)
    _set_or_create_child_attr(node, "NodeType", "value", "PropertyStep")
    _set_or_create_child_attr(node, "SymbolPath", "value", symbol)
    _set_or_create_child_attr(node, "Value", "value", value)
    return node


def _new_command(factory: NodeFactory, symbol: str, value: str = "", comment: str = "") -> ET.Element:
    node = factory.clone(f"CommandStepNode:{symbol}", "CommandStepNode")
    node.attrib["type"] = "CommandStepNode"
    if symbol == "System.Trigger":
        children = _children(node)
        _clear_collection_children(children)
    elif node.find("Children") is not None:
        _remove_child(node, "Children")
    _set_optional_comment(node, comment)
    _set_or_create_child_attr(node, "NodeType", "value", "CommandStep")
    _set_or_create_child_attr(node, "SymbolPath", "value", symbol)
    _set_or_create_child_attr(node, "Value", "value", value)
    return node


def _children(node: ET.Element) -> ET.Element:
    children = node.find("Children")
    if children is None:
        children = ET.SubElement(node, "Children", {"type": "SyntaxNodeCollection"})
    return children


def _set_or_create_child_attr(node: ET.Element, child_name: str, attr_name: str, value: str) -> ET.Element:
    child = node.find(child_name)
    if child is None:
        child = ET.SubElement(node, child_name)
    child.attrib[attr_name] = value
    return child


def _set_optional_comment(node: ET.Element, comment: str) -> None:
    if comment:
        _set_or_create_child_attr(node, "Comment", "value", comment)
    else:
        _remove_child(node, "Comment")


def _remove_child(node: ET.Element, child_name: str) -> None:
    child = node.find(child_name)
    if child is not None:
        node.remove(child)


def _stage_name(stage: ET.Element) -> str:
    child = stage.find("StageName")
    return child.attrib.get("value", "") if child is not None else ""


def _internal_time(value: str) -> str:
    text = (value or "").strip()
    if not text or text == "{Initial Time}":
        return "-Infinity"
    if text.lower() in {"infinity", "+infinity"}:
        return "Infinity"
    return _format_number(float(text))


def _format_number(value: float) -> str:
    return f"{value:.15g}"


def _looks_numeric_time(value: str) -> bool:
    try:
        float(value)
        return True
    except ValueError:
        return False


def _duration_from_value(value: str) -> float | None:
    match = re.search(r"Duration\s*=\s*([-+]?\d+(?:\.\d+)?)", value or "")
    return float(match.group(1)) if match else None


def _count_command_nodes(node: ET.Element) -> int:
    return sum(1 for item in node.iter() if item.attrib.get("type") in {"CommandStepNode", "PropertyStepNode"})


def _clear_collection_children(collection: ET.Element) -> None:
    # ET.Element.clear() also removes attributes; CM needs type="SyntaxNodeCollection".
    for child in list(collection):
        collection.remove(child)


def _build_prototypes(root: ET.Element) -> dict[str, ET.Element]:
    prototypes: dict[str, ET.Element] = {}
    for item in root.iter("Item"):
        type_name = item.attrib.get("type", "")
        if not type_name:
            continue
        prototypes.setdefault(type_name, copy.deepcopy(item))
        if type_name == "StageNode":
            stage_name = _stage_name(item)
            if stage_name:
                prototypes.setdefault(f"StageNode:{stage_name}", copy.deepcopy(item))
        if type_name in {"CommandStepNode", "PropertyStepNode"}:
            symbol = item.find("SymbolPath")
            if symbol is not None:
                prototypes.setdefault(f"{type_name}:{symbol.attrib.get('value', '')}", copy.deepcopy(item))
    return prototypes


def _max_node_id(root: ET.Element) -> int:
    values: list[int] = []
    for node_id in root.iter("NodeId"):
        try:
            values.append(int(node_id.attrib.get("value", "")))
        except ValueError:
            continue
    return max(values) if values else 900000


def main() -> None:
    parser = argparse.ArgumentParser(description="Compile a CM-style method MD table into a standalone instrument-method CMBX using an exported method CMBX as carrier.")
    parser.add_argument("source_cmbx", type=Path)
    parser.add_argument("source_md", type=Path)
    parser.add_argument("output_cmbx", type=Path)
    parser.add_argument("--method-name", default=None, help="Display/import name for the generated standalone method. Defaults to the source MD stem.")
    args = parser.parse_args()
    stats = compile_method_md_to_cmbx(args.source_cmbx, args.source_md, args.output_cmbx, method_name=args.method_name)
    print(args.output_cmbx)
    print(stats)


if __name__ == "__main__":
    main()
