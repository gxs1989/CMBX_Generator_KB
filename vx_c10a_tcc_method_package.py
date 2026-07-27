from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


OPEN = "🔓 Open Verification Required"


@dataclass(frozen=True)
class SequenceInjectionSpec:
    order: int
    injection: str
    processing_method: str
    instrument_method: str
    report_sheets: tuple[str, ...]
    formula_id: str
    acceptance_criteria: str
    notes: str = ""


SAMPLES = {
    "VA-C10-A": ("VA", "0000003", "Report_VATCC_V1_01"),
    "VC-C10-A": ("VC", "3000004", "Report_VTCC_V2_12"),
    "VH-C10-A": ("VH", "6000001", "Report_VTCC_V2_12"),
}


VA_SEQUENCE = (
    SequenceInjectionSpec(1, "Valve", "No_Integration", "VALVES", ("Valve_Keypad",), "FORMULA_TCC_VALVE_KEYPAD_OPEN", OPEN),
    SequenceInjectionSpec(2, "VTCC_BurnIn", "NO_INTEGRATION", "BURNIN", (), "FORMULA_TCC_BURNIN_OPEN", OPEN),
    SequenceInjectionSpec(3, "Temperature Calibration", "NO_INTEGRATION", "TEMPERATURE_CALIBRATION", ("Temp_Calib_Internal",), "FORMULA_TCC_TEMP_CALIBRATION_OPEN", OPEN),
    SequenceInjectionSpec(4, "Temperature Accuracy_C", "ACCURACY_IRC_STOP_C", "TEMPERATURE_ACCURACY", ("Temp Accuracy",), "FORMULA_TCC_TEMP_ACCURACY_MAX_DEVIATION", "External: max absolute deviation <= report Definitions!Temperature Accuracy."),
    SequenceInjectionSpec(5, "Temperature Precision", "NO_INTEGRATION", "TEMPERATURE_PRECISION", ("Temp Precision",), "FORMULA_TCC_TEMP_PRECISION_SEPARATE_SENSOR_RANGE", "External: max(lower range, upper range) <= report Definitions!Temperature Precision."),
    SequenceInjectionSpec(6, "Temperature Stability_C", "NO_INTEGRATION", "TEMPERATURE_STABILITY_70_C", ("Temp Stability_Noise",), "FORMULA_TCC_TEMP_STABILITY_SEPARATE_SENSOR_RANGE", "External: max(lower range, upper range) <= report Definitions!Temperature Stability."),
    SequenceInjectionSpec(7, "HeatUp and CoolDownTime", "No_Integration", "TEMP_HEAT_UP_DOWN_20_50_20", ("HeatUp&CoolDown",), "FORMULA_TCC_HEATUP_COOLDOWN_RETTIME_DELTA_MINUS_HOLD", "External: heat-up/cool-down time <= report Definitions!HeatUp & Cool Down."),
    SequenceInjectionSpec(8, "LiquidLeaktest", "No_Integration", "LIQUID LEAK", ("Liquid Leak Test",), "FORMULA_TCC_LIQUID_LEAK_OPEN", OPEN),
    SequenceInjectionSpec(9, "Qualification_Service_Done", "No_Integration", "Qualification_Service_Done", ("Internal Use",), "FORMULA_TCC_QUALIFICATION_SERVICE_OPEN", OPEN),
    SequenceInjectionSpec(10, "Factory Default", "No_Integration", "FACTORYDEFAULT", ("Definitions", "Internal Use", "Factory Default"), "FORMULA_TCC_FACTORY_DEFAULT_METADATA", "External/Internal split not fully normalized; values come from audit/precondition metadata."),
    SequenceInjectionSpec(11, "Error Log Check", "No_Integration", "CHECKERRORLOG", ("Error Log", "Internal Use"), "FORMULA_TCC_ERROR_LOG_OPEN", OPEN),
)


VC_SEQUENCE = (
    SequenceInjectionSpec(1, "ColumnIDs", "CORRECT_ACCURACY_INJ_INSERTION", "ColumnID", ("Column ID",), "FORMULA_TCC_COLUMN_ID_AUDIT_DESCRIPTION", "External: Column_A/B/C/D descriptions must match A/B/C/D."),
    SequenceInjectionSpec(2, "Preheater Connection Test", "CORRECT_ACCURACY_INJ_INSERTION", "PREHEATER", ("Preheater Ports_Noise",), "FORMULA_TCC_PREHEATER_PORT_STATE_AND_DIFF", "External: RetTimes present, ModulePresent=Yes, MemoryState=OK."),
    SequenceInjectionSpec(3, "Valve", "CORRECT_ACCURACY_INJ_INSERTION", "VALVES", ("Valve_Keypad",), "FORMULA_TCC_VALVE_KEYPAD_OPEN", OPEN),
    SequenceInjectionSpec(4, "VTCC_BurnIn", "NO_INTEGRATION", "BURNIN", (), "FORMULA_TCC_BURNIN_OPEN", OPEN),
    SequenceInjectionSpec(5, "Temperature Calibration", "CORRECT_ACCURACY_INJ_INSERTION", "TEMPERATURE_CALIBRATION", ("Temp_Calib_Internal",), "FORMULA_TCC_TEMP_CALIBRATION_OPEN", OPEN),
    SequenceInjectionSpec(6, "Temperature Accuracy_C", "ACCURACY_IRC_STOP_C", "TEMPERATURE_ACCURACY", ("Temp Accuracy",), "FORMULA_TCC_TEMP_ACCURACY_MAX_DEVIATION", "External: max absolute deviation <= report Definitions!Temperature Accuracy."),
    SequenceInjectionSpec(7, "Temperature Precision_and_Fan", "CORRECT_STABILITY_INJ_INSERTION", "TEMPERATURE_PRECISION_AND_FAN", ("Temp Precision", "Fan"), "FORMULA_TCC_TEMP_PRECISION_SEPARATE_SENSOR_RANGE", "External: max(lower range, upper range) <= report Definitions!Temperature Precision."),
    SequenceInjectionSpec(8, "Temperature Stability_C", "NO_INTEGRATION", "TEMPERATURE_STABILITY_70_C", ("Temp Stability_Noise",), "FORMULA_TCC_TEMP_STABILITY_SEPARATE_SENSOR_RANGE", "External: max(lower range, upper range) <= report Definitions!Temperature Stability."),
    SequenceInjectionSpec(9, "HeatUp and CoolDownTime", "CORRECT_ACCURACY_INJ_INSERTION", "TEMP_HEAT_UP_DOWN_20_50_20", ("HeatUp&CoolDown",), "FORMULA_TCC_HEATUP_COOLDOWN_RETTIME_DELTA_MINUS_HOLD", "External: heat-up/cool-down time <= report Definitions!HeatUp & Cool Down."),
    SequenceInjectionSpec(10, "LiquidLeaktest", "CORRECT_ACCURACY_INJ_INSERTION", "LIQUID LEAK", ("Liquid Leak Test",), "FORMULA_TCC_LIQUID_LEAK_OPEN", OPEN),
    SequenceInjectionSpec(11, "Qualification_Service_Done", "CORRECT_ACCURACY_INJ_INSERTION", "Qualification_Service_Done", ("Internal Use",), "FORMULA_TCC_QUALIFICATION_SERVICE_OPEN", OPEN),
    SequenceInjectionSpec(12, "Factory Default", "CORRECT_ACCURACY_INJ_INSERTION", "FACTORYDEFAULT", ("Definitions", "Internal Use", "Factory Default"), "FORMULA_TCC_FACTORY_DEFAULT_METADATA", "External/Internal split not fully normalized; values come from audit/precondition metadata."),
    SequenceInjectionSpec(13, "Error Log Check", "CORRECT_ACCURACY_INJ_INSERTION", "CHECKERRORLOG", ("Error Log", "Internal Use"), "FORMULA_TCC_ERROR_LOG_OPEN", OPEN),
)


VH_SEQUENCE = (
    SequenceInjectionSpec(1, "ColumnIDs", "CORRECT_STABILITY_INJ_INSERTION", "ColumnID", ("Column ID",), "FORMULA_TCC_COLUMN_ID_AUDIT_DESCRIPTION", "External: Column_A/B/C/D descriptions must match A/B/C/D."),
    SequenceInjectionSpec(2, "Preheater Connection Test", "No_Integration", "PREHEATER", ("Preheater Ports_Noise",), "FORMULA_TCC_PREHEATER_PORT_STATE_AND_DIFF", "External: RetTimes present, ModulePresent=Yes, MemoryState=OK."),
    SequenceInjectionSpec(3, "Valve", "No_Integration", "VALVES", ("Valve_Keypad",), "FORMULA_TCC_VALVE_KEYPAD_OPEN", OPEN),
    SequenceInjectionSpec(4, "VTCC_BurnIn", "NO_INTEGRATION", "BURNIN", (), "FORMULA_TCC_BURNIN_OPEN", OPEN),
    SequenceInjectionSpec(5, "Temperature Calibration", "CORRECT_ACCURACY_INJ_INSERTION", "TEMPERATURE_CALIBRATION", ("Temp_Calib_Internal",), "FORMULA_TCC_TEMP_CALIBRATION_OPEN", OPEN),
    SequenceInjectionSpec(6, "Temperature Accuracy_H", "ACCURACY_IRC_STOP_H", "TEMPERATURE_ACCURACY", ("Temp Accuracy",), "FORMULA_TCC_TEMP_ACCURACY_MAX_DEVIATION", "External: max absolute deviation <= report Definitions!Temperature Accuracy."),
    SequenceInjectionSpec(7, "Temperature Precision_and_Fan", "CORRECT_STABILITY_INJ_INSERTION", "TEMPERATURE_PRECISION_AND_FAN", ("Temp Precision", "Fan"), "FORMULA_TCC_TEMP_PRECISION_SEPARATE_SENSOR_RANGE", "External: max(lower range, upper range) <= report Definitions!Temperature Precision."),
    SequenceInjectionSpec(8, "Temperature Stability_and_PCC_H", "NO_INTEGRATION", "TEMPERATURE_STABILITY_AND_PCC_70_H", ("Temp Stability_Noise", "PCC"), "FORMULA_TCC_TEMP_STABILITY_AND_PCC_COOLDOWN", "External: stability <= Definitions!Temperature Stability; PCC cooldown <= Definitions!PCC CoolDownTime."),
    SequenceInjectionSpec(9, "HeatUp and CoolDownTime", "No_Integration", "TEMP_HEAT_UP_DOWN_20_50_20", ("HeatUp&CoolDown",), "FORMULA_TCC_HEATUP_COOLDOWN_RETTIME_DELTA_MINUS_HOLD", "External: heat-up/cool-down time <= report Definitions!HeatUp & Cool Down."),
    SequenceInjectionSpec(10, "LiquidLeaktest", "No_Integration", "LIQUID LEAK", ("Liquid Leak Test",), "FORMULA_TCC_LIQUID_LEAK_OPEN", OPEN),
    SequenceInjectionSpec(11, "Qualification_Service_Done", "No_Integration", "Qualification_Service_Done", ("Internal Use",), "FORMULA_TCC_QUALIFICATION_SERVICE_OPEN", OPEN),
    SequenceInjectionSpec(12, "Factory Default", "No_Integration", "FACTORYDEFAULT", ("Definitions", "Internal Use", "Factory Default"), "FORMULA_TCC_FACTORY_DEFAULT_METADATA", "External/Internal split not fully normalized; values come from audit/precondition metadata."),
    SequenceInjectionSpec(13, "Error Log Check", "No_Integration", "CHECKERRORLOG", ("Error Log", "Internal Use"), "FORMULA_TCC_ERROR_LOG_OPEN", OPEN),
)


SEQUENCES = {
    "VA-C10-A": VA_SEQUENCE,
    "VC-C10-A": VC_SEQUENCE,
    "VH-C10-A": VH_SEQUENCE,
}


def build_vx_c10a_tcc_method_package_markdown() -> str:
    lines: list[str] = [
        "# VX-C10-A TCC FOQ CMBX Test Method Package",
        "",
        "Status: review package specification, not a newly validated runnable CMBX binary.",
        "",
        "This package is generated from the current FOQ/TCC knowledge alignment, decoded CMBX method evidence, report/formula mappings, and generation strategy rules. Missing mappings are marked `Open Verification Required` and must not be guessed.",
        "",
        "## Input Knowledge Sources",
        "",
        "| Source | Resolved local evidence | Status |",
        "|---|---|---|",
        "| FOQ KB | `C:\\ProgramData\\CMBX Data Explorer Workspace\\KB\\FOQ\\TCC\\FOQ_TCC_VX_C10_A_TD_KNOWLEDGE_MANAGEMENT.md` | available |",
        "| CMBX Method KB | `knowledge_base/tcc_reverse_probe/{VA,VC,VH}/*_embedded_method_flow.tsv` and `*_embedded.instmeth.bin` | available |",
        "| CMBX Report KB | `Report_VATCC_V1_01`, `Report_VTCC_V2_12`, decoded report sheet/formula evidence | partial |",
        "| Formula KB | `cmbx_data_explorer/docs/CM_FORMULA_KNOWLEDGE_BASE.md` and TCC formula evaluator rules | partial |",
        "| Generation Strategy KB | `cmbx_data_explorer/docs/CMBX_GENERATION_STRATEGY_KB.md` | available |",
        "",
        "## Step 1: FOQ Test Checklist",
        "",
        "| Order | FOQ Test | VH-C10-A | VC-C10-A | VA-C10-A | Note |",
        "|---:|---|---|---|---|---|",
        "| 1 | Column IDs | yes | yes | open | VA applicability is not explicit in extracted TD table; current VA sample omits it. |",
        "| 2 | Preheater Connection Test | yes | yes | yes | Hardware/config sensitive. |",
        "| 3 | Valve / Keypad part 1 | yes | yes | yes | Valve hardware/config sensitive. |",
        "| 4 | VTCC_BurnIn | yes | yes | yes | Preparation/stress phase. |",
        "| 5 | Temperature Calibration | yes | yes | yes | Sets calibration and IRC context. |",
        "| 6 | Temperature Accuracy | yes | yes | yes | Model-specific IRC branch. |",
        "| 7 | Temperature Precision and Fan | yes | yes | yes | VA sample uses `Temperature Precision`; VC/VH use `_and_Fan`. |",
        "| 8 | Temperature Stability and PCC | yes | no | no | VH-only. |",
        "| 9 | Temperature Stability | no | yes | yes | VC/VA no-PCC branch. |",
        "| 10 | HeatUp and CoolDown Time | yes | yes | yes | Timing performance. |",
        "| 11 | Liquid Leak / Keypad part 2 | yes | yes | yes | Leak sensor + keypad. |",
        "| 12 | Qualification Service | yes | yes | yes | Final service state. |",
        "| 13 | Factory Default | yes | yes | yes | Metadata/default state. |",
        "| 14 | Error Log Check | yes | yes | yes | Present in current CMBX sequence evidence. |",
        "",
        "## Step 2-4: Method, Report, and Formula Mapping",
        "",
    ]
    for model, sequence in SEQUENCES.items():
        lines.extend(_sequence_table(model, sequence))
    lines.extend(
        [
            "",
            "## Step 5: Model Branch Decision Tree",
            "",
            "```mermaid",
            "flowchart TD",
            '    A["Read device from AUDIT.ColumnComp.ModelNo"] --> B{Model}',
            '    B -->|VH-C10-A| VH["Use Report_VTCC_V2_12; include PCC stability branch"]',
            '    B -->|VC-C10-A| VC["Use Report_VTCC_V2_12; use C accuracy/stability branch"]',
            '    B -->|VA-C10-A| VA["Use Report_VATCC_V1_01; use VA sequence evidence; ColumnID applicability open"]',
            '    VH --> VH1["Temperature Accuracy_H / ACCURACY_IRC_STOP_H"]',
            '    VH --> VH2["Temperature Stability_and_PCC_H / TEMPERATURE_STABILITY_AND_PCC_70_H"]',
            '    VC --> VC1["Temperature Accuracy_C / ACCURACY_IRC_STOP_C"]',
            '    VC --> VC2["Temperature Stability_C / TEMPERATURE_STABILITY_70_C"]',
            '    VA --> VA1["Temperature Accuracy_C / ACCURACY_IRC_STOP_C"]',
            '    VA --> VA2["Temperature Stability_C / TEMPERATURE_STABILITY_70_C"]',
            "```",
            "",
            "## Step 6: IRC / Processing Method Configuration",
            "",
            "| Model | Injection | Processing Method | Required behavior | Status |",
            "|---|---|---|---|---|",
            "| VH-C10-A | `Temperature Accuracy_H` | `ACCURACY_IRC_STOP_H` | Preserve IRC/stop behavior for VH accuracy branch. | sequence link verified; pass-action decode partial |",
            "| VC-C10-A | `Temperature Accuracy_C` | `ACCURACY_IRC_STOP_C` | Preserve IRC/stop behavior for VC accuracy branch. | sequence link verified; pass-action decode partial |",
            "| VA-C10-A | `Temperature Accuracy_C` | `ACCURACY_IRC_STOP_C` | Preserve IRC/stop behavior for VA accuracy branch. | sequence link verified; pass-action decode partial |",
            "| VC-C10-A | multiple injections | `CORRECT_ACCURACY_INJ_INSERTION` | Correct/insert accuracy related injections. | sequence link verified; pass-action decode partial |",
            "| VH-C10-A | ColumnID / Precision | `CORRECT_STABILITY_INJ_INSERTION` | Correct/insert stability related injections. | sequence link verified; pass-action decode partial |",
            "",
            "## Step 7: Dependency Validation Checklist",
            "",
            "| Check | Required for | How to verify | Failure handling |",
            "|---|---|---|---|",
            "| Device source of truth | all branches | `AUDIT.ColumnComp.ModelNo` | Stop generation if model cannot be read. |",
            "| External thermometers | accuracy, precision, stability, heat/cool | channels `ExtTemp_UpperCC`, `ExtTemp_LowerCC` in CMBX/CM config | Add/configure Generic Device thermometers. |",
            "| PCC symbols | VH stability/PCC | `ColumnComp.PCC`, `PCC_Temp`, PCC PWM channels | Use non-PCC branch only if model is not VH; otherwise stop. |",
            "| Preheater symbols | preheater test | `ColumnComp.PrehtLeft/Right` and heater temp channels | Mark test not runnable until configured. |",
            "| Valve symbols | valve test | `ColumnComp.UpperValve`, `ColumnComp.LowerValve` | Remove/disable valve test only with approved variant logic. |",
            "| Column ID config | ColumnIDs | Column A-D audit descriptions | Mark `Open Verification Required` for VA unless confirmed. |",
            "| Processing/IRC links | accuracy/stability correction | sequence command links and processing method XML | Reassign processing method or stop. |",
            "| Report template | DB/report output | model branch table below | Do not export DB if template branch is unresolved. |",
            "| Numeric criteria | acceptance decisions | report `Definitions` cells / FOQ section 4.3 | Do not hard-code new numeric values; use source definitions only. |",
            "",
            "## Report Template List",
            "",
            "| Model | Report Template | Report role | Status |",
            "|---|---|---|---|",
            "| VA-C10-A | `Report_VATCC_V1_01` | Standard VA TCC FOQ report template. | template name verified; full formula trace partial |",
            "| VC-C10-A | `Report_VTCC_V2_12` | Standard VC TCC FOQ report template. | verified template family |",
            "| VH-C10-A | `Report_VTCC_V2_12` | Standard VH TCC FOQ report template, including PCC sheet. | verified template family |",
            "",
            "## Method Asset Inventory",
            "",
            "| Method | Exported method asset pattern | Status |",
            "|---|---|---|",
        ]
    )
    for method in _all_methods():
        lines.append(f"| `{method}` | `{_method_asset_pattern(method)}` | decoded method payload exists in TCC reverse probe for at least one branch, or mark open during packaging |")
    lines.extend(
        [
            "",
            "## Package Validation Checklist",
            "",
            "- [ ] Device model is read from `AUDIT.ColumnComp.ModelNo`.",
            "- [ ] Selected branch is VA, VC, or VH only.",
            "- [ ] Every injection has one instrument method and one processing method.",
            "- [ ] Method names exactly match decoded CMBX names.",
            "- [ ] Report template branch matches device model.",
            "- [ ] Accuracy and stability formulas resolve to report cells and Definitions criteria.",
            "- [ ] Numeric acceptance criteria are loaded from FOQ/report Definitions, not manually changed.",
            "- [ ] IRC/corrective processing methods are linked to the correct injections.",
            "- [ ] Required CM symbols/channels exist in target configuration.",
            "- [ ] Any `Open Verification Required` row is resolved or explicitly excluded before runnable CMBX generation.",
            "",
            "## Output Status",
            "",
            "This Markdown file is the complete review specification for a VX-C10-A TCC FOQ method package. It does not by itself prove that a newly packed binary CMBX is runnable in Chromeleon.",
            "",
        ]
    )
    return "\n".join(lines)


def write_vx_c10a_tcc_method_package_markdown(output_path: str | Path) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(build_vx_c10a_tcc_method_package_markdown(), encoding="utf-8")
    return output_path


def _sequence_table(model: str, sequence: tuple[SequenceInjectionSpec, ...]) -> list[str]:
    branch, sample, report_template = SAMPLES[model]
    lines = [
        f"### {model}",
        "",
        f"Report template: `{report_template}`",
        "",
        "| Order | Injection | Processing Method | Instrument Method | Method asset | Report Sheet(s) | Formula ID | Acceptance criteria |",
        "|---:|---|---|---|---|---|---|---|",
    ]
    for item in sequence:
        method_asset = f"knowledge_base/tcc_reverse_probe/{branch}/{sample}/{_asset_method_name(item.instrument_method)}_embedded.instmeth.bin"
        sheets = ", ".join(f"`{sheet}`" for sheet in item.report_sheets) or f"`{OPEN}`"
        lines.append(
            f"| {item.order} | `{item.injection}` | `{item.processing_method}` | `{item.instrument_method}` | `{method_asset}` | {sheets} | `{item.formula_id}` | {item.acceptance_criteria} |"
        )
    lines.append("")
    return lines


def _asset_method_name(method_name: str) -> str:
    known = {
        "Qualification_Service_Done": "QUALIFICATION_SERVICE_DONE",
    }
    return known.get(method_name, method_name)


def _all_methods() -> tuple[str, ...]:
    methods = {item.instrument_method for sequence in SEQUENCES.values() for item in sequence}
    return tuple(sorted(methods))


def _method_asset_pattern(method: str) -> str:
    return f"knowledge_base/tcc_reverse_probe/<VA|VC|VH>/<sample>/{_asset_method_name(method)}_embedded.instmeth.bin"
