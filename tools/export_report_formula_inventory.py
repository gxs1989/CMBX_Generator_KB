from __future__ import annotations

"""Export report formula evidence from a standalone report CMBX as Markdown."""

import argparse
import sys
from collections import Counter, defaultdict
from pathlib import Path

TOOL_ROOT = Path(__file__).resolve().parents[1]
if str(TOOL_ROOT) not in sys.path:
    sys.path.insert(0, str(TOOL_ROOT))

from cmbx_container import load_cmbx_package
from embedded_report_extractor import decode_report_template_xml, parse_report_sheet_objects, parse_report_sheets
from formulaone_report_exporter import extract_formulaone_spreadsheet_data
from formulaone_workbook_writer import read_formulaone_formula_inventory


def export_report_formula_inventory(
    source_cmbx: Path,
    output_md: Path,
    report_name: str = "",
    include_formulaone: bool = False,
) -> None:
    package = load_cmbx_package(source_cmbx)
    reports = [item for item in package.methods_and_reports if item.kind == "report_template"]
    if report_name:
        reports = [item for item in reports if item.name.casefold() == report_name.casefold()]
        if len(reports) != 1:
            raise ValueError(f"Expected one report named {report_name!r} in {source_cmbx.name}, found {len(reports)}.")
    elif len(reports) != 1:
        available = ", ".join(item.name for item in reports) or "(none)"
        raise ValueError(
            f"Expected exactly one report_template in {source_cmbx.name}, found {len(reports)}: {available}. "
            "Pass --report <exact template name>."
        )
    report = reports[0]
    _embedded, xml = decode_report_template_xml(package, report)
    sheets = parse_report_sheets(xml, report.name)
    objects = [item for item in parse_report_sheet_objects(xml, report.name) if item.formula]
    namespaces = Counter(_namespace(item.formula) for item in objects)
    workbook_formulas: list[dict[str, object]] = []
    if include_formulaone:
        workbook_formulas = read_formulaone_formula_inventory(extract_formulaone_spreadsheet_data(xml))
    per_sheet: dict[str, list] = defaultdict(list)
    for item in objects:
        per_sheet[item.sheet_name].append(item)

    lines = [
        f"# {report.name} Direct CM Formula Inventory",
        "",
        f"- **Source CMBX:** `{source_cmbx.name}`",
        "- **Extraction scope:** `SheetObject` direct CM formulas"
        + (" plus FormulaOne workbook cell formulas." if include_formulaone else " only."),
        "- **FormulaOne scope:** "
        + (
            f"{len(workbook_formulas)} workbook cell formulas read from `SpreadSheetData`; layout, values and formats are not expanded."
            if include_formulaone
            else "Not included. Re-run with `--include-formulaone` to export workbook-cell formula evidence."
        ),
        "- **Authoring rule:** Retain the sheet/cell binding and fixed channel/component unless a configuration contract approves a change.",
        "",
        "## Summary",
        "",
        f"- Sheets: {len(sheets)}",
        f"- Direct CM formula objects: {len(objects)}",
        f"- FormulaOne workbook formulas: {len(workbook_formulas)}",
        "- Formula namespaces: " + ", ".join(f"`{name}` ({count})" for name, count in sorted(namespaces.items())),
        "",
        "## Web Authoring Context (Self-Contained)",
        "",
        "This section is included so this inventory can be supplied directly to a web-based GPT. It does not require access to local Chromeleon Help files. The formula table below is the carrier-specific evidence; this section explains how to read and safely reuse that evidence.",
        "",
        "### Two Calculation Layers",
        "",
        "| Layer | Storage / syntax | Use it for | V0.1 standalone-CMBX rule |",
        "|---|---|---|---|",
        "| Direct CM report formula | `ReportFormulaObject` with CM expressions such as `chm.noise(...)`, `AUDIT.*`, `precond.*` | Pulling raw signal, audit, metadata, or peak data into an existing report cell | May replace an existing formula object only when sheet, cell/range and object type match the carrier |",
        "| FormulaOne workbook formula | Embedded `SpreadSheetData`, Excel-like syntax such as `=MAX(...)` | Visible labels, layout, calculated summaries, pass/fail display and print structure | Preserve it. Record requested edits as `workbook_change_request`; do not write them as CM formulas |",
        "",
        "Do not put an Excel formula beginning with `=` into a `ReportFormulaObject`. Do not assume every visible result cell appears in this inventory: workbook-derived cells are intentionally outside this direct-CM extraction scope.",
        "",
        "### HPLC Report Signal Context",
        "",
        "The channel names and audit paths observed in the table are carrier-specific configuration contracts, not generic aliases. Use the exact evidence rows below to decide which of these source categories apply:",
        "",
        "| Observed item | Meaning for authoring | Required evidence before reuse |",
        "|---|---|---|",
        "| Raw channel, for example `UV_VIS_1` or `PumpPressureVirtual` | Detector, pump, virtual, or other acquired-signal context used by raw-statistic and peak formulas | The method/config must acquire or create that exact channel with compatible settings |",
        "| Timed audit path, for example `AUDIT.UV.*` or `audit.ColumnComp.*` | Time-resolved settings/events, such as detector state, valve position, flow, or temperature | The selected injection audit must log the exact property path |",
        "| Precondition path, for example `precond.UV.*` | Pre-run device identity/configuration | The device configuration must expose and log the property |",
        "| `peak.*` / `chm.peak(...)` | Processed chromatographic peak/calibration result | A compatible processing method, channel and component must exist |",
        "",
        "Time arguments in observed `chm.*` and timed `AUDIT.*` expressions are in minutes. Preserve all observed scale factors: for example `chm.noise(1,2)*1000` and `chm.drift(1,21)*60` are carrier-specific result contracts; do not remove or reinterpret multipliers without an acceptance/report-unit review.",
        "",
        "### CM Formula Semantics Used by This Carrier",
        "",
        "| Expression family | Meaning | Authoring constraint |",
        "|---|---|---|",
        "| `chm.noise(start,end)` | Signal noise over the stated raw-data time window | Bind the exact fixed channel. Preserve window boundaries and multiplier unless the test specification changes them deliberately |",
        "| `chm.drift(start,end)` | Regression slope across the stated baseline window | Keep the signal channel and any unit conversion such as `*60` explicit |",
        "| `chm.sig_value(stat,start,end)` / `chm.signalStatistic(...)` | Signal statistic over a window, commonly average/min/max | A raw signal channel and minute-based range are required |",
        "| `chm.signalValue(time)` | Signal value at a specific minute | Requires a sampled signal at that point |",
        "| `AUDIT.path(time,\"forward\"/\"backward\")` | Audit property selected at/after or at/before the requested minute | Retain the full observed device path unless its abbreviation is proven unambiguous |",
        "| `precond.path` | Pre-run configuration/identity property | It does not read a raw chromatogram and cannot substitute for an audit event |",
        "| `peak.*`, `chm.peak(...)` | Processed peak, calibration or component property | Require the matching processing method and component/channel binding |",
        "| `seq.*`, `smp.*`, `injection.*`, `gen.*` | Sequence, sample, injection or software metadata | Use only fields observed in the selected carrier/config or explicitly verified |",
        "",
        "### Direct Formula Object Contract",
        "",
        "For every proposed direct-formula change, supply all of: exact existing sheet name, A1 cell/range from this inventory, `object_type: ReportFormulaObject`, CM formula text, `fixed_channel` when the source object uses a channel, `fixed_component` for component/peak context, and the required audit/channel/processing dependencies. If an object is absent from this inventory, it is not safe to invent in V0.1 clone-and-patch generation.",
        "",
        "### HPLC Report Authoring Guardrails",
        "",
        "1. Choose the data source first: raw VWD signal, detector audit setting, detector precondition, processed peak, or metadata.",
        "2. Reuse the observed sheet/cell/object and fixed channel whenever it has the same semantic role.",
        "3. A report formula can be syntactically valid but evaluate to `n.a.` when the instrument configuration, channel, audit path, wavelength, lamp configuration or processing component is absent.",
        "4. Mark `OPEN VERIFICATION REQUIRED` rather than fabricating an unobserved channel, audit path, FormulaOne formula, acceptance criterion, display format or report-table schema.",
        "5. Report tables (`ReportTableObject`) are structured, pipe-delimited definitions, not scalar cell formulas; preserve them unless a controlled CM before/after pair validates a table write rule.",
        "",
        "## Sheet Applicability",
        "",
        "| Sheet | Active | Each Injection | Query | Injection Variable | Query Values |",
        "|---|---|---|---|---|---|",
    ]
    for sheet in sheets:
        lines.append(
            "| " + " | ".join(
                _cell(value)
                for value in (
                    sheet.sheet_name,
                    sheet.is_active,
                    sheet.each_injection,
                    sheet.query_enabled,
                    sheet.injection_variable,
                    sheet.query_values,
                )
            ) + " |"
        )
    for sheet_name in [sheet.sheet_name for sheet in sheets]:
        items = per_sheet.get(sheet_name, [])
        if not items:
            continue
        lines.extend(
            [
                "",
                f"## Sheet: {sheet_name}",
                "",
                "| Cell / Range | Object Type | Formula | Fixed Channel | Fixed Component |",
                "|---|---|---|---|---|",
            ]
        )
        for item in items:
            lines.append(
                "| " + " | ".join(
                    _cell(value)
                    for value in (
                        item.excel_range,
                        item.object_type,
                        item.formula,
                        item.fixed_channel,
                        item.fixed_component,
                    )
                ) + " |"
            )
    if workbook_formulas:
        by_sheet: dict[str, list[dict[str, object]]] = defaultdict(list)
        for item in workbook_formulas:
            by_sheet[str(item.get("sheet", ""))].append(item)
        lines.extend(
            [
                "",
                "# FormulaOne Workbook Formula Inventory",
                "",
                "These formulas are stored in `SpreadSheetData`. They are Excel-like FormulaOne formulas, not CM `ReportFormulaObject` expressions. The reader exports formula strings only; visible values, formatting, merged cells, dynamic-table schema and print layout remain outside this inventory.",
            ]
        )
        for sheet_name in sorted(by_sheet):
            lines.extend(
                [
                    "",
                    f"## FormulaOne Sheet: {sheet_name}",
                    "",
                    "| Cell | Formula |",
                    "|---|---|",
                ]
            )
            for item in sorted(by_sheet[sheet_name], key=lambda row: (int(row.get("row", 0)), int(row.get("column", 0)))):
                row = int(item.get("row", 0))
                column = int(item.get("column", 0))
                lines.append(f"| {_cell(_a1(row, column))} | {_cell(str(item.get('formula', '')))} |")
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _namespace(formula: str) -> str:
    value = formula.strip().lower()
    for prefix in ("audit.", "precond.", "chm.", "peak.", "seq.", "smp.", "injection.", "gen."):
        if value.startswith(prefix):
            return prefix[:-1]
    if value.startswith("if("):
        return "if"
    if value.startswith("left("):
        return "left"
    return "other"


def _cell(value: str) -> str:
    return (value or "").replace("|", "\\|").replace("\n", "<br>")


def _a1(row: int, column: int) -> str:
    name = ""
    while column:
        column, remainder = divmod(column - 1, 26)
        name = chr(65 + remainder) + name
    return f"{name}{row}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Export CM report formula evidence from a standalone CMBX into Markdown.")
    parser.add_argument("source_cmbx", type=Path)
    parser.add_argument("output_md", type=Path)
    parser.add_argument("--report", default="", help="Exact report-template name when the CMBX contains multiple reports.")
    parser.add_argument("--include-formulaone", action="store_true", help="Also read FormulaOne workbook-cell formulas from SpreadSheetData.")
    args = parser.parse_args()
    export_report_formula_inventory(args.source_cmbx, args.output_md, args.report, args.include_formulaone)
    print(args.output_md)


if __name__ == "__main__":
    main()
