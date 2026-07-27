from __future__ import annotations

from dataclasses import dataclass
import re
import xml.etree.ElementTree as ET


STAGE_DISPLAY_NAMES = {
    "InstrumentSetup": "Instrument Setup",
    "InjectPreparation": "Inject Preparation",
    "StartRun": "Start Run",
    "StopRun": "Stop Run",
    "PostRun": "Post Run",
}


@dataclass(frozen=True)
class CmMethodTableRow:
    index: int
    kind: str
    time: str
    command: str
    value: str
    comment: str
    node_id: str
    xml_role: str


def render_cm_method_table_rows(xml_text: str) -> tuple[list[CmMethodTableRow], str | None]:
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as exc:
        return [], str(exc)

    rows: list[CmMethodTableRow] = []

    def add(kind: str, time: str = "", command: str = "", value: str = "", comment: str = "", node_id: str = "", xml_role: str = "") -> None:
        rows.append(CmMethodTableRow(len(rows), kind, time, command, value, comment, node_id, xml_role))

    for stage in root.iter():
        if stage.attrib.get("type") != "StageNode":
            continue
        stage_name = _stage_name(stage)
        display_name = STAGE_DISPLAY_NAMES.get(stage_name, stage_name)
        time_steps = [node for node in _direct_time_steps(stage)]
        first_time = _method_time(time_steps[0]) if time_steps else ""
        add("Stage", first_time, display_name, _stage_duration_text(stage), "", _node_id(stage), "StageNode")
        for index, time_step in enumerate(time_steps):
            time_text = _method_time(time_step)
            if index > 0 and time_text:
                add("Time", time_text, "", "", "", _node_id(time_step), "TimeStepNode")
            for child in _syntax_children(time_step):
                _render_node(child, add)

    if rows and rows[-1].kind != "End":
        add("End", "", "End", "", "", "", "EndNode")
    return rows, None


def render_cm_method_table_tsv(xml_text: str) -> str:
    rows, error = render_cm_method_table_rows(xml_text)
    header = ["#", "Kind", "Time", "Command", "Value", "Comment", "NodeId", "XmlRole"]
    lines = ["\t".join(header)]
    if error:
        lines.append(_tsv([0, "Error", "", "", "", error, "", "ParseError"]))
        return "\n".join(lines)
    for row in rows:
        lines.append(_tsv([row.index, row.kind, row.time, row.command, row.value, row.comment, row.node_id, row.xml_role]))
    return "\n".join(lines)


def _render_node(node: ET.Element, add) -> None:
    node_type = node.attrib.get("type", "")
    if node_type in {"CommmentNode", "CommentNode"}:
        add("Comment", "", _child_value(node, "Comment"), "", "", _node_id(node), node_type)
        return
    if node_type == "PropertyStepNode":
        add("Command", "", _child_value(node, "SymbolPath"), _child_value(node, "Value"), _child_value(node, "Comment"), _node_id(node), node_type)
        return
    if node_type == "CommandStepNode":
        symbol = _child_value(node, "SymbolPath") or _child_value(node, "CommandPath")
        if symbol == "System.Trigger":
            _render_trigger_node(node, add)
            return
        add("Command", "", symbol, _child_value(node, "Value"), _child_value(node, "Comment"), _node_id(node), node_type)
        return
    if node_type == "IfBlockNode":
        for child in _syntax_children(node):
            _render_node(child, add)
        add("Branch", "End If", "", "", "", _node_id(node), node_type)
        return
    if node_type == "IfNode":
        add("Branch", "If", "", _child_value(node, "Condition"), "", _node_id(node), node_type)
        for child in _syntax_children(node):
            _render_node(child, add)
        return
    if node_type == "ElseIfNode":
        add("Branch", "Else If", "", _child_value(node, "Condition"), "", _node_id(node), node_type)
        for child in _syntax_children(node):
            _render_node(child, add)
        return
    if node_type == "ElseNode":
        add("Branch", "Else", "", "", "", _node_id(node), node_type)
        for child in _syntax_children(node):
            _render_node(child, add)
        return
    for child in _syntax_children(node):
        _render_node(child, add)


def _render_trigger_node(node: ET.Element, add) -> None:
    trigger_name, parameters = _split_trigger_value(_child_value(node, "Value"))
    add("Trigger", "Trigger", "", trigger_name, "", _node_id(node), "CommandStepNode:System.Trigger")
    for param in parameters:
        add("TriggerParam", "", param, "", "", _node_id(node), "System.Trigger.Value")
    for child in _syntax_children(node):
        _render_node(child, add)
    add("EndTrigger", "End Trigger", "", "", "", _node_id(node), "CommandStepNode:System.Trigger:End")


def _split_trigger_value(value: str) -> tuple[str, list[str]]:
    text = (value or "").strip()
    if not text:
        return "", []
    match = re.match(r'("[^"]+"\s*,)\s*(.*)$', text, flags=re.S)
    if not match:
        return text, []
    trigger_name = match.group(1).strip()
    rest = match.group(2).strip()
    if not rest:
        return trigger_name, []
    parts = [part.strip() for part in rest.split(",")]
    output: list[str] = []
    for index, part in enumerate(parts):
        if not part:
            continue
        suffix = "," if index < len(parts) - 1 else ""
        output.append(part + suffix)
    return trigger_name, output


def _direct_time_steps(stage_node: ET.Element) -> list[ET.Element]:
    children = stage_node.find("Children")
    if children is None:
        return []
    return [child for child in list(children) if child.attrib.get("type") == "TimeStepNode"]


def _syntax_children(node: ET.Element) -> list[ET.Element]:
    children = node.find("Children")
    if children is None:
        return []
    return list(children)


def _stage_name(node: ET.Element) -> str:
    return _child_value(node, "StageName") or _child_value(node, "Name")


def _stage_duration_text(node: ET.Element) -> str:
    values: list[float] = []
    for time_step in _direct_time_steps(node):
        raw = _raw_method_time(time_step)
        if raw in {"", "-Infinity", "Infinity"}:
            continue
        try:
            values.append(float(raw))
        except ValueError:
            continue
    if len(values) < 2:
        return ""
    duration = max(values) - min(values)
    return f"Duration = {duration:.3f} [min]" if duration >= 0 else ""


def _method_time(node: ET.Element) -> str:
    return _format_method_time(_raw_method_time(node))


def _raw_method_time(node: ET.Element) -> str:
    child = node.find("MethodTime/InternalValue")
    if child is None:
        child = node.find("Time/InternalValue")
    return child.attrib.get("value", "").strip() if child is not None else ""


def _format_method_time(value: str) -> str:
    text = (value or "").strip()
    if not text:
        return ""
    if text == "-Infinity":
        return "{Initial Time}"
    if text == "Infinity":
        return "Infinity"
    try:
        return f"{float(text):.3f}"
    except ValueError:
        return text


def _child_value(node: ET.Element, child_name: str) -> str:
    child = node.find(child_name)
    if child is None:
        return ""
    return _normalize_method_text(child.attrib.get("value", ""))


def _node_id(node: ET.Element) -> str:
    child = node.find("NodeId")
    return child.attrib.get("value", "") if child is not None else ""


def _normalize_method_text(value: str) -> str:
    return (value or "").replace("\r\n", "\n").strip()


def _tsv(values: list[object]) -> str:
    return "\t".join(str(value).replace("\t", " ").replace("\r\n", "\n").replace("\n", "\\n") for value in values)
