from __future__ import annotations

import base64
import math
import re
import struct
import xml.etree.ElementTree as ET
from dataclasses import dataclass

from report_formula_evaluator import FormulaEvaluation


@dataclass(frozen=True)
class DefinitionCriterion:
    name: str
    value: float
    source: str


@dataclass(frozen=True)
class ReportCellCalculation:
    sheet_name: str
    cell: str
    label: str
    expression: str
    dependencies: str
    criterion: str
    rule: str
    source: str
    note: str = ""


DEFINITION_LABELS = [
    "Temperature Accuracy",
    "Temperature Stability",
    "Temperature Precision",
    "HeatUp & Cool Down",
    "PCC T Accuracy",
    "PCC T Drift",
    "PCC CoolDownTime",
    "Pre-Heater Simulator Heat-Up Time",
    "Pre-Heater Simulator Signal Diff",
]


def extract_definition_criteria(report_xml: str) -> dict[str, DefinitionCriterion]:
    raw = _spreadsheet_data(report_xml)
    if not raw:
        return {}
    criteria: dict[str, DefinitionCriterion] = {}
    for label in DEFINITION_LABELS:
        pos = raw.find(label.encode("latin1", errors="ignore"))
        if pos < 0:
            continue
        values = _nearby_numeric_values(raw[pos + len(label) : pos + len(label) + 96])
        if not values:
            continue
        criteria[label] = DefinitionCriterion(
            name=label,
            value=values[0],
            source="Definitions sheet / embedded FormulaOne SpreadSheetData",
        )
    return criteria


def build_report_calculation_map(
    report_xml: str,
    sheets: dict[str, list[FormulaEvaluation]],
) -> list[ReportCellCalculation]:
    criteria = extract_definition_criteria(report_xml)
    rows: list[ReportCellCalculation] = []
    for name, criterion in criteria.items():
        rows.append(
            ReportCellCalculation(
                sheet_name="Definitions",
                cell="",
                label=name,
                expression=_format_number(criterion.value),
                dependencies="Embedded report workbook static criterion table",
                criterion="",
                rule="Shared criterion used by applicable report sheets",
                source=criterion.source,
            )
        )
    for sheet_name, evaluations in sheets.items():
        normalized = sheet_name.lower()
        if normalized == "temp accuracy":
            rows.extend(_temp_accuracy_map(criteria))
        elif "heatup" in normalized and "cooldown" in normalized:
            rows.extend(_heatup_cooldown_map(criteria, evaluations))
        elif normalized == "temp precision":
            rows.extend(_temp_precision_map(criteria))
        elif normalized == "temp stability_noise":
            rows.extend(_temp_stability_map(criteria))
    return rows


def _temp_accuracy_map(criteria: dict[str, DefinitionCriterion]) -> list[ReportCellCalculation]:
    criterion = _criterion_text(criteria, "Temperature Accuracy", 0.5)
    return [
        ReportCellCalculation(
            sheet_name="Temp Accuracy",
            cell="N66:N70",
            label="Observed temperature with maximum deviation",
            expression="value from {Lower CC, Upper CC} with largest abs(value - adjusted temperature)",
            dependencies="I/J adjusted temperature cells; L observed Lower CC; M observed Upper CC",
            criterion="",
            rule="Choose the thermometer reading farthest from the nominal setpoint",
            source="Reconstructed from Chromeleon report layout and verified against exported accuracy report",
        ),
        ReportCellCalculation(
            sheet_name="Temp Accuracy",
            cell="D66:D70",
            label="Deviation",
            expression="round(N row, 2) - adjusted temperature",
            dependencies="B adjusted temperature; C/N observed max-deviation temperature",
            criterion=criterion,
            rule=f"abs(deviation) <= {criterion}",
            source="Report workbook calculation layer",
        ),
        ReportCellCalculation(
            sheet_name="Temp Accuracy",
            cell="D26",
            label="Observed Max. Deviation",
            expression="max(abs(D66:D70))",
            dependencies="D66:D70",
            criterion=criterion,
            rule=f"D26 <= {criterion}",
            source="Report workbook summary calculation",
        ),
    ]


def _heatup_cooldown_map(
    criteria: dict[str, DefinitionCriterion],
    evaluations: list[FormulaEvaluation],
) -> list[ReportCellCalculation]:
    criterion = _criterion_text(criteria, "HeatUp & Cool Down", 15.0)
    raw_cells = _ok_cells(evaluations)
    heatup_raw = ", ".join(cell for cell in ["J65", "K65"] if cell in raw_cells) or "RetTime start/end cells"
    cooldown_raw = ", ".join(cell for cell in ["L65", "M65"] if cell in raw_cells) or "RetTime start/end cells"
    return [
        ReportCellCalculation(
            sheet_name="HeatUp&CoolDown",
            cell="D65",
            label="Heat Up Time / observed time",
            expression="End Time - Start Time - 2.0 min stable-hold time",
            dependencies=f"same-row Start Time and End Time cells; raw RetTime cells: {heatup_raw}",
            criterion=criterion,
            rule=f"D65 <= {criterion}",
            source="Embedded FormulaOne workbook cell formula area; RetTime values come from SheetObject formulas",
            note="The report template history states that the 2 min hold time is subtracted for heat-up/cool-down evaluation.",
        ),
        ReportCellCalculation(
            sheet_name="HeatUp&CoolDown",
            cell="D66",
            label="Cool Down Time / observed time",
            expression="End Time - Start Time - 2.0 min stable-hold time",
            dependencies=f"same-row Start Time and End Time cells; raw RetTime cells: {cooldown_raw}",
            criterion=criterion,
            rule=f"D66 <= {criterion}",
            source="Embedded FormulaOne workbook cell formula area; RetTime values come from SheetObject formulas",
            note="The same Definitions criterion is reused for both heat-up and cool-down rows.",
        ),
        ReportCellCalculation(
            sheet_name="HeatUp&CoolDown",
            cell="D26",
            label="Observed Time summary",
            expression="D65",
            dependencies="D65; Definitions!HeatUp & Cool Down",
            criterion=criterion,
            rule=f"D26 <= {criterion} -> Test passed, otherwise Test failed",
            source="Report workbook summary calculation",
        ),
        ReportCellCalculation(
            sheet_name="HeatUp&CoolDown",
            cell="D27",
            label="Observed Time summary",
            expression="D66",
            dependencies="D66; Definitions!HeatUp & Cool Down",
            criterion=criterion,
            rule=f"D27 <= {criterion} -> Test passed, otherwise Test failed",
            source="Report workbook summary calculation",
        ),
    ]


def _temp_precision_map(criteria: dict[str, DefinitionCriterion]) -> list[ReportCellCalculation]:
    criterion = _criterion_text(criteria, "Temperature Precision", 0.1)
    return [
        ReportCellCalculation(
            sheet_name="Temp Precision",
            cell="D26",
            label="Observed Max. Deviation",
            expression="max(max(K65:K67)-min(K65:K67), max(L65:L67)-min(L65:L67))",
            dependencies="K65:K67 Lower CC replicate averages; L65:L67 Upper CC replicate averages",
            criterion=criterion,
            rule=f"raw D26 <= {criterion}; report cell displayed with 2 decimals",
            source="Report workbook calculation layer",
        ),
    ]


def _temp_stability_map(criteria: dict[str, DefinitionCriterion]) -> list[ReportCellCalculation]:
    criterion = _criterion_text(criteria, "Temperature Stability", 0.05)
    return [
        ReportCellCalculation(
            sheet_name="Temp Stability_Noise",
            cell="D26",
            label="Observed Max. Deviation",
            expression="max(max(K61:K75)-min(K61:K75), max(L61:L75)-min(L61:L75))",
            dependencies="K61:K75 Lower CC segment averages; L61:L75 Upper CC segment averages",
            criterion=criterion,
            rule=f"raw D26 <= {criterion}; report cell displayed with 2 decimals",
            source="Report workbook calculation layer",
        ),
    ]


def _spreadsheet_data(report_xml: str) -> bytes:
    try:
        root = ET.fromstring(report_xml)
    except ET.ParseError:
        return b""
    for node in root.iter():
        if node.tag == "SpreadSheetData":
            value = node.attrib.get("value", "")
            try:
                return base64.b64decode(value)
            except ValueError:
                return b""
    return b""


def _nearby_numeric_values(data: bytes) -> list[float]:
    values: list[float] = []
    seen: set[float] = set()
    for match in re.finditer(rb"[\xd0-\xdf]\x00(?P<tail>.{5})", data, flags=re.DOTALL):
        value = _decode_truncated_double(match.group("tail"))
        if value is not None and value not in seen:
            values.append(value)
            seen.add(value)
    for index in range(0, max(0, len(data) - 7)):
        value = _decode_double(data[index : index + 8])
        if value is not None and value not in seen:
            values.append(value)
            seen.add(value)
    return values


def _decode_truncated_double(tail: bytes) -> float | None:
    if len(tail) != 5:
        return None
    return _decode_double(b"\x00\x00\x00" + tail)


def _decode_double(data: bytes) -> float | None:
    try:
        value = struct.unpack("<d", data)[0]
    except struct.error:
        return None
    if not math.isfinite(value) or value <= 0 or value > 1000:
        return None
    rounded = round(value, 6)
    if rounded == 0:
        return None
    return rounded


def _criterion_text(criteria: dict[str, DefinitionCriterion], name: str, fallback: float) -> str:
    criterion = criteria.get(name)
    return _format_number(criterion.value if criterion else fallback)


def _format_number(value: float) -> str:
    text = f"{value:.6f}".rstrip("0").rstrip(".")
    return text or "0"


def _ok_cells(evaluations: list[FormulaEvaluation]) -> set[str]:
    return {row.excel_range for row in evaluations if row.status == "ok" and row.excel_range}
