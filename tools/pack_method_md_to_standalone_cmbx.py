from __future__ import annotations

import argparse
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

TOOL_ROOT = Path(__file__).resolve().parents[1]
if str(TOOL_ROOT) not in sys.path:
    sys.path.insert(0, str(TOOL_ROOT))
TOOLS_ROOT = TOOL_ROOT / "tools"
if str(TOOLS_ROOT) not in sys.path:
    sys.path.insert(0, str(TOOLS_ROOT))

from chromeleon_method_decoder import decode_cpxm_method_xml
from cm_method_xml_table import CmMethodTableRow, render_cm_method_table_rows
from cmbx_container import extract_cmbx_entry, load_cmbx_package
from embedded_method_extractor import _extract_method_payload
from render_cm_method_md import parse_md_to_rows
from repack_standalone_instmeth_cmbx import repack_standalone_method_cmbx


def pack_method_md_to_cmbx(source_cmbx: Path, edited_md: Path, output_cmbx: Path, include_comments: bool = False) -> dict[str, int]:
    package = load_cmbx_package(source_cmbx)
    methods = [element for element in package.methods_and_reports if element.kind == "instrument_method"]
    if len(methods) != 1:
        raise ValueError(f"Expected exactly one standalone instrument method, found {len(methods)}.")
    entry_name = methods[0].package_entry_name
    data = extract_cmbx_entry(source_cmbx, entry_name)
    payload = _extract_method_payload(data, 0)
    if payload is None:
        raise ValueError(f"Could not locate method payload inside {entry_name}.")

    with tempfile.TemporaryDirectory(prefix="cmbx_md_pack_") as tmp:
        tmp_root = Path(tmp)
        cpxm_path = tmp_root / "source.cpxm"
        xml_path = tmp_root / "source.xml"
        edited_xml_path = tmp_root / "edited.xml"
        cpxm_path.write_bytes(payload.cpxm_payload)
        decode_result = decode_cpxm_method_xml(cpxm_path, xml_path)
        if not decode_result.ok:
            raise RuntimeError(decode_result.message)
        xml_text = xml_path.read_text(encoding="utf-8")
        rendered_rows, error = render_cm_method_table_rows(xml_text)
        if error:
            raise ValueError(error)
        edited_rows = parse_md_to_rows(edited_md)
        if len(rendered_rows) != len(edited_rows):
            raise ValueError(f"Edited MD row count {len(edited_rows)} does not match template row count {len(rendered_rows)}.")

        root = ET.fromstring(xml_text)
        nodes = _nodes_by_id(root)
        changed = _apply_rows_to_xml(rendered_rows, edited_rows, nodes, include_comments=include_comments)
        if sum(changed.values()) == 0:
            edited_xml_path.write_text(xml_text, encoding="utf-8")
        else:
            _indent(root)
            ET.ElementTree(root).write(edited_xml_path, encoding="utf-8", xml_declaration=False)
        repack_standalone_method_cmbx(source_cmbx, edited_xml_path, output_cmbx)
        return changed


def _apply_rows_to_xml(
    rendered_rows: list[CmMethodTableRow],
    edited_rows: list[dict[str, str]],
    nodes: dict[str, ET.Element],
    include_comments: bool = False,
) -> dict[str, int]:
    changed = {
        "comments": 0,
        "command_values": 0,
        "command_comments": 0,
        "branch_conditions": 0,
        "trigger_values": 0,
    }
    trigger_edits: dict[str, list[tuple[CmMethodTableRow, dict[str, str]]]] = {}
    for rendered, edited in zip(rendered_rows, edited_rows):
        if rendered.kind in {"Stage", "Time", "End", "EndTrigger"}:
            continue
        if rendered.kind in {"Trigger", "TriggerParam"}:
            trigger_edits.setdefault(rendered.node_id, []).append((rendered, edited))
            continue
        node = nodes.get(rendered.node_id)
        if node is None:
            continue
        if rendered.kind == "Comment" and include_comments:
            if _set_child_attr(node, "Comment", "value", _edited_text(edited, "Command")):
                changed["comments"] += 1
        elif rendered.kind == "Branch":
            new_condition = _edited_text(edited, "Value") or _edited_text(edited, "Command")
            if _set_child_attr(node, "Condition", "value", new_condition):
                changed["branch_conditions"] += 1
        elif rendered.kind == "Command":
            new_value = _edited_text(edited, "Value")
            if _set_child_attr(node, "Value", "value", new_value):
                changed["command_values"] += 1
            if include_comments and _set_child_attr(node, "Comment", "value", _edited_text(edited, "Comment")):
                changed["command_comments"] += 1

    for node_id, group in trigger_edits.items():
        node = nodes.get(node_id)
        if node is None:
            continue
        trigger_value = _trigger_value_from_group(group)
        if _set_child_attr(node, "Value", "value", trigger_value):
            changed["trigger_values"] += 1
    return changed


def _trigger_value_from_group(group: list[tuple[CmMethodTableRow, dict[str, str]]]) -> str:
    trigger_name = ""
    params: list[str] = []
    for rendered, edited in group:
        if rendered.kind == "Trigger":
            trigger_name = _first_non_empty(edited, "Value", "Command", "Time")
        elif rendered.kind == "TriggerParam":
            param = _first_non_empty(edited, "Command", "Time", "Value")
            if param:
                params.append(param)
    return " ".join([part for part in [trigger_name, *params] if part]).strip()


def _nodes_by_id(root: ET.Element) -> dict[str, ET.Element]:
    nodes: dict[str, ET.Element] = {}
    for node in root.iter():
        node_id = node.find("NodeId")
        if node_id is not None:
            value = node_id.attrib.get("value", "")
            if value:
                nodes[value] = node
    return nodes


def _set_child_attr(node: ET.Element, child_name: str, attr_name: str, value: str) -> bool:
    child = node.find(child_name)
    if child is None:
        if not value:
            return False
        child = ET.SubElement(node, child_name)
    old = child.attrib.get(attr_name, "")
    if old == value:
        return False
    child.attrib[attr_name] = value
    return True


def _edited_text(row: dict[str, str], key: str) -> str:
    return (row.get(key, "") or "").strip()


def _first_non_empty(row: dict[str, str], *keys: str) -> str:
    for key in keys:
        value = _edited_text(row, key)
        if value:
            return value
    return ""


def _indent(elem: ET.Element, level: int = 0) -> None:
    # Preserve compactness reasonably while producing stable XML text for XmlCompressor.
    children = list(elem)
    if children:
        for child in children:
            _indent(child, level + 1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Patch a standalone exported instrument-method CMBX using a CM-style method MD table.")
    parser.add_argument("source_cmbx", type=Path)
    parser.add_argument("edited_md", type=Path)
    parser.add_argument("output_cmbx", type=Path)
    parser.add_argument("--include-comments", action="store_true", help="Also patch CM comment text from the MD table. Defaults off to avoid encoding/whitespace churn.")
    args = parser.parse_args()
    result = pack_method_md_to_cmbx(args.source_cmbx, args.edited_md, args.output_cmbx, include_comments=args.include_comments)
    print(args.output_cmbx)
    print(result)


if __name__ == "__main__":
    main()
