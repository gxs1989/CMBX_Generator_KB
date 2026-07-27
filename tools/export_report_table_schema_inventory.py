from __future__ import annotations

"""Export native Chromeleon report-table structures from reference CMBX files."""

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cmbx_container import load_cmbx_package  # noqa: E402
from embedded_report_extractor import decode_report_template_xml  # noqa: E402


def _value(node: ET.Element, path: str) -> str:
    child = node.find(path)
    return child.attrib.get("value", "") if child is not None else ""


def _compact_tree(node: ET.Element) -> dict[str, object]:
    result: dict[str, object] = {"tag": node.tag}
    if node.attrib:
        result["attributes"] = dict(node.attrib)
    children = [_compact_tree(child) for child in list(node)]
    if children:
        result["children"] = children
    return result


def inventory_file(path: Path) -> list[dict[str, object]]:
    package = load_cmbx_package(path)
    rows: list[dict[str, object]] = []
    reports = [item for item in package.methods_and_reports if item.kind == "report_template"]
    for report in reports:
        try:
            _embedded, xml_text = decode_report_template_xml(package, report)
        except Exception as exc:  # pragma: no cover - diagnostic utility
            rows.append({"source": str(path), "report": report.name, "error": str(exc)})
            continue
        root = ET.fromstring(xml_text)
        for sheet in root.findall(".//SheetDescription"):
            sheet_name = _value(sheet, "SheetName")
            for obj in sheet.findall("SheetObject"):
                if obj.attrib.get("type") != "ReportTableObject":
                    continue
                formulas = [
                    item.attrib.get("value", "")
                    for item in obj.findall(".//Formula")
                    if item.attrib.get("value", "")
                ]
                type_counts = Counter(
                    item.attrib.get("type", "")
                    for item in obj.iter()
                    if item.attrib.get("type", "")
                )
                rows.append(
                    {
                        "source": str(path),
                        "report": report.name,
                        "sheet": sheet_name,
                        "range": {
                            "left": _value(obj, "Range/Left"),
                            "top": _value(obj, "Range/Top"),
                            "right": _value(obj, "Range/Right"),
                            "bottom": _value(obj, "Range/Bottom"),
                        },
                        "report_table_type": _value(obj, "ReportTableType"),
                        "native_types": dict(sorted(type_counts.items())),
                        "formulas": formulas,
                        "xml": ET.tostring(obj, encoding="unicode"),
                        "tree": _compact_tree(obj),
                    }
                )
    return rows


def render_markdown(rows: list[dict[str, object]]) -> str:
    lines = [
        "# Chromeleon Report Table Schema Inventory",
        "",
        "Generated from verified CMBX report templates. XML blocks are retained as native schema evidence.",
        "",
        "| Source | Report | Sheet | Range | ReportTableType | Native types | Formula count |",
        "|---|---|---|---|---|---|---:|",
    ]
    for row in rows:
        if "error" in row:
            lines.append(f"| {Path(str(row['source'])).name} | {row.get('report', '')} | ERROR | | | {row['error']} | |")
            continue
        bounds = row["range"]
        assert isinstance(bounds, dict)
        address = f"({bounds['left']},{bounds['top']})-({bounds['right']},{bounds['bottom']})"
        types = row.get("native_types", {})
        native = ", ".join(f"{key}:{value}" for key, value in types.items()) if isinstance(types, dict) else ""
        lines.append(
            f"| {Path(str(row['source'])).name} | {row['report']} | {row['sheet']} | {address} | "
            f"{row.get('report_table_type', '')} | {native} | {len(row.get('formulas', []))} |"
        )
    for index, row in enumerate(rows, 1):
        if "xml" not in row:
            continue
        lines.extend(
            [
                "",
                f"## {index}. {row['report']} / {row['sheet']}",
                "",
                f"- Source: `{row['source']}`",
                f"- Report table type: `{row.get('report_table_type', '')}`",
                f"- Formulas: `{row.get('formulas', [])}`",
                "",
                "```xml",
                str(row["xml"]),
                "```",
            ]
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--markdown", type=Path, required=True)
    parser.add_argument("--skeletons", type=Path)
    args = parser.parse_args()
    files: list[Path] = []
    for item in args.inputs:
        files.extend(sorted(item.glob("*.cmbx")) if item.is_dir() else [item])
    rows: list[dict[str, object]] = []
    for path in files:
        rows.extend(inventory_file(path))
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.markdown.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
    args.markdown.write_text(render_markdown(rows), encoding="utf-8")
    if args.skeletons:
        skeletons: dict[str, dict[str, object]] = {}
        for table_type in ("audittrail", "peak_summary", "integration"):
            candidates = [row for row in rows if row.get("report_table_type") == table_type and "xml" in row]
            if not candidates:
                continue
            selected = min(candidates, key=lambda row: len(str(row["xml"])))
            skeletons[table_type] = {
                "source": Path(str(selected["source"])).name,
                "report": selected["report"],
                "sheet": selected["sheet"],
                "xml": selected["xml"],
            }
        args.skeletons.parent.mkdir(parents=True, exist_ok=True)
        args.skeletons.write_text(json.dumps(skeletons, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"tables={sum('xml' in row for row in rows)} errors={sum('error' in row for row in rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
