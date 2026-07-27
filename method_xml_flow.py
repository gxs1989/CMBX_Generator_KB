from __future__ import annotations

from dataclasses import dataclass
import xml.etree.ElementTree as ET


FLOW_NODE_TYPES = {
    "StageNode",
    "TimeStepNode",
    "CommmentNode",
    "CommentNode",
    "PropertyStepNode",
    "CommandStepNode",
    "IfBlockNode",
    "IfNode",
    "ElseIfNode",
    "ElseNode",
}


@dataclass(frozen=True)
class FlowRow:
    order: int
    level: int
    stage: str
    time: str
    node_type: str
    action: str
    target: str
    value: str
    comment: str
    condition: str


def build_method_flow_from_xml(xml_text: str, method_name: str = "") -> str:
    lines = [
        f"Embedded Instrument Method Flow: {method_name}".rstrip(),
        "Source: decoded CMBX CpXm method XML",
        "",
    ]
    rows, error = build_method_flow_rows(xml_text)
    if error:
        lines.extend(["XML parse error", "---------------", error])
        return "\n".join(lines)
    if not rows:
        lines.append("No method flow nodes were found in the decoded XML.")
        return "\n".join(lines)

    for row in rows:
        indent = "  " * row.level
        if row.action == "COMMENT":
            lines.append(f"{indent}# {row.comment}")
        elif row.action == "STAGE":
            lines.append(f"\n[Stage] {row.value or row.stage}")
        elif row.action == "TIME":
            lines.append(f"\n@ {row.time}")
        elif row.action == "SET":
            lines.append(f"{indent}SET {row.target} = {row.value}")
        elif row.action == "RUN":
            lines.append(f"{indent}RUN {row.target} {row.value}".rstrip())
        elif row.action == "TRIGGER":
            trigger_lines = [line.strip() for line in row.value.splitlines() if line.strip()]
            if trigger_lines:
                lines.append(f"{indent}TRIGGER {trigger_lines[0]}")
                for param in trigger_lines[1:]:
                    lines.append(f"{indent}  {param}")
            else:
                lines.append(f"{indent}TRIGGER")
        elif row.action == "END TRIGGER":
            lines.append(f"{indent}END TRIGGER")
        elif row.action == "IF":
            lines.append(f"{indent}IF {row.condition}".rstrip())
        elif row.action == "ELSE IF":
            lines.append(f"{indent}ELSE IF {row.condition}".rstrip())
        elif row.action == "ELSE":
            lines.append(f"{indent}else")
        elif row.action == "END IF":
            lines.append(f"{indent}END IF")
        elif row.action == "END":
            lines.append(f"{indent}END")
    return "\n".join(lines)


def build_method_flow_tsv(xml_text: str, method_name: str = "") -> str:
    rows, error = build_method_flow_rows(xml_text)
    header = ["Method", "Order", "Level", "Stage", "Time", "NodeType", "Action", "Target", "Value", "Comment", "Condition"]
    output = ["\t".join(header)]
    if error:
        output.append(_tsv_row([method_name, "", "", "", "", "ParseError", "ERROR", "", "", error, ""]))
        return "\n".join(output)
    for row in rows:
        output.append(
            _tsv_row(
                [
                    method_name,
                    str(row.order),
                    str(row.level),
                    row.stage,
                    row.time,
                    row.node_type,
                    row.action,
                    row.target,
                    row.value,
                    row.comment,
                    row.condition,
                ]
            )
        )
    return "\n".join(output)


def build_method_flow_rows(xml_text: str) -> tuple[list[FlowRow], str | None]:
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as exc:
        return [], str(exc)

    rows: list[FlowRow] = []
    state = {"stage": "", "time": ""}

    def visit(node: ET.Element, level: int) -> None:
        node_type = node.attrib.get("type", "")
        if node_type == "TimeStepNode":
            time_text = _method_time(node)
            if time_text:
                state["time"] = time_text
            for child in list(node):
                visit(child, level)
            return
        if node_type == "IfBlockNode":
            for child in list(node):
                visit(child, level)
            rows.append(FlowRow(len(rows) + 1, level, state["stage"], state["time"], node_type, "END IF", "", "", "", ""))
            return
        if node_type in FLOW_NODE_TYPES:
            row = _flow_row(len(rows) + 1, level, state["stage"], state["time"], node_type, node)
            if row:
                rows.append(row)
                if row.action == "STAGE":
                    state["stage"] = row.value
                    if row.time:
                        state["time"] = row.time
                elif row.action == "TIME":
                    state["time"] = row.time
        for child in list(node):
            visit(child, level + (1 if node_type in {"IfNode", "ElseIfNode", "ElseNode"} else 0))
        if node_type == "CommandStepNode" and rows and rows[-1].action != "END TRIGGER":
            symbol = _child_value(node, "SymbolPath") or _child_value(node, "CommandPath")
            if symbol == "System.Trigger":
                rows.append(FlowRow(len(rows) + 1, level, state["stage"], state["time"], node_type, "END TRIGGER", "", "", "", ""))

    visit(root, 0)
    if rows and rows[-1].action != "END":
        rows.append(FlowRow(len(rows) + 1, 0, state["stage"], state["time"], "EndNode", "END", "", "", "", ""))
    return rows, None


def _flow_row(order: int, level: int, stage: str, time: str, node_type: str, node: ET.Element) -> FlowRow | None:
    if node_type in {"CommmentNode", "CommentNode"}:
        comment = _child_value(node, "Comment")
        return FlowRow(order, level, stage, time, node_type, "COMMENT", "", "", comment, "") if comment else None
    if node_type == "PropertyStepNode":
        symbol = _child_value(node, "SymbolPath")
        value = _child_value(node, "Value")
        comment = _child_value(node, "Comment")
        return FlowRow(order, level, stage, time, node_type, "SET", symbol, value, comment, "") if symbol else None
    if node_type == "CommandStepNode":
        symbol = _child_value(node, "SymbolPath") or _child_value(node, "CommandPath")
        value = _child_value(node, "Value")
        comment = _child_value(node, "Comment")
        if symbol == "System.Trigger":
            return FlowRow(order, level, stage, time, node_type, "TRIGGER", symbol, value, comment, "")
        return FlowRow(order, level, stage, time, node_type, "RUN", symbol, value, comment, "") if symbol else None
    if node_type == "StageNode":
        name = _child_value(node, "Name") or _child_value(node, "StageName")
        stage_time = _stage_time(node)
        duration = _stage_duration_text(node)
        return FlowRow(order, level, name or stage, stage_time, node_type, "STAGE", "", name, duration, "") if name else None
    if node_type == "TimeStepNode":
        time_text = _method_time(node)
        return FlowRow(order, level, stage, time_text, node_type, "TIME", "", time_text, "", "") if time_text else None
    if node_type == "IfBlockNode":
        return None
    if node_type == "IfNode":
        condition = _condition_text(node)
        return FlowRow(order, level, stage, time, node_type, "IF", "", "", "", condition)
    if node_type == "ElseIfNode":
        condition = _condition_text(node)
        return FlowRow(order, level, stage, time, node_type, "ELSE IF", "", "", "", condition)
    if node_type == "ElseNode":
        return FlowRow(order, level, stage, time, node_type, "ELSE", "", "", "", "")
    return None


def _child_value(node: ET.Element, child_name: str) -> str:
    child = node.find(child_name)
    if child is None:
        return ""
    return _normalize_method_text(child.attrib.get("value", "").strip())


def _method_time(node: ET.Element) -> str:
    return _format_method_time(_raw_method_time(node))


def _stage_time(node: ET.Element) -> str:
    first_time_step = next(_iter_stage_time_steps(node), None)
    if first_time_step is None:
        return ""
    return _method_time(first_time_step)


def _stage_duration_text(node: ET.Element) -> str:
    values: list[float] = []
    for time_step in _iter_stage_time_steps(node):
        raw = _raw_method_time(time_step)
        if not raw or raw in {"-Infinity", "Infinity"}:
            continue
        try:
            values.append(float(raw))
        except ValueError:
            continue
    if len(values) < 2:
        return ""
    duration = max(values) - min(values)
    if duration <= 0:
        return ""
    return f"Duration = {duration:.3f} [min]"


def _iter_stage_time_steps(stage_node: ET.Element):
    for child in list(stage_node):
        yield from _iter_time_steps(child)


def _iter_time_steps(node: ET.Element):
    node_type = node.attrib.get("type", "")
    if node_type == "StageNode":
        return
    if node_type == "TimeStepNode":
        yield node
        return
    for child in list(node):
        yield from _iter_time_steps(child)


def _raw_method_time(node: ET.Element) -> str:
    child = node.find("MethodTime/InternalValue")
    if child is None:
        child = node.find("Time/InternalValue")
    if child is None:
        return ""
    return child.attrib.get("value", "").strip()


def _condition_text(node: ET.Element) -> str:
    return _child_value(node, "Condition")


def _format_method_time(value: str) -> str:
    text = (value or "").strip()
    if not text:
        return ""
    if text in {"-Infinity", "Infinity"}:
        return "{Initial Time}" if text.startswith("-") else text
    try:
        return f"{float(text):.3f}"
    except ValueError:
        return text


def _tsv_row(values: list[str]) -> str:
    return "\t".join(_clean_cell(value) for value in values)


def _clean_cell(value: str) -> str:
    return _normalize_method_text(str(value)).replace("\t", " ").replace("\r", " ").replace("\n", " ").strip()


def _normalize_method_text(value: str) -> str:
    return str(value).replace("�C", "°C").replace("�", "°")
