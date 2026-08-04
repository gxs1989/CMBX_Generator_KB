# TCC Original Report Template Evidence

Module: TCC  
Status: PARTIAL - VTCC and PressureEvaluation evidence available; VATCC canonical inventory missing  
Delivery_File: 02_REPORT_ORIGINAL_TEMPLATES.md

## Self Index

| ID | Source | Included |
|---|---|---|
| `VTCC_FULL` | `Report_VTCC_V2_12_full_formula_inventory.md` | Yes |
| `VTCC_FORMULAONE` | `REPORT_VTCC_V2_12_FORMULAONE_INVENTORY.md` | Yes |
| `PRESSURE_EVALUATION` | `PressureEvaluation_FORMULA_INVENTORY.md` | Yes |

---

## Evidence: VTCC_FULL

Source file: `Report_VTCC_V2_12_full_formula_inventory.md`

- **Source CMBX:** `Report_VTCC_V2_12.cmbx`
- **Extraction scope:** `SheetObject` direct CM formulas plus FormulaOne workbook cell formulas.
- **FormulaOne scope:** 640 workbook cell formulas read from `SpreadSheetData`; layout, values and formats are not expanded.
- **Authoring rule:** Retain the sheet/cell binding and fixed channel/component unless a configuration contract approves a change.

## Summary

- Sheets: 19
- Direct CM formula objects: 234
- FormulaOne workbook formulas: 640
- Formula namespaces: `audit` (95), `chm` (106), `gen` (1), `injection` (1), `precond` (14), `seq` (12), `smp` (5)

## Web Authoring Context (Self-Contained)

This section is included so this inventory can be supplied directly to a web-based GPT. It does not require access to local Chromeleon Help files. The formula table below is the carrier-specific evidence; this section explains how to read and safely reuse that evidence.

### Two Calculation Layers

| Layer | Storage / syntax | Use it for | V0.1 standalone-CMBX rule |
|---|---|---|---|
| Direct CM report formula | `ReportFormulaObject` with CM expressions such as `chm.noise(...)`, `AUDIT.*`, `precond.*` | Pulling raw signal, audit, metadata, or peak data into an existing report cell | May replace an existing formula object only when sheet, cell/range and object type match the carrier |
| FormulaOne workbook formula | Embedded `SpreadSheetData`, Excel-like syntax such as `=MAX(...)` | Visible labels, layout, calculated summaries, pass/fail display and print structure | Preserve it. Record requested edits as `workbook_change_request`; do not write them as CM formulas |

Do not put an Excel formula beginning with `=` into a `ReportFormulaObject`. Do not assume every visible result cell appears in this inventory: workbook-derived cells are intentionally outside this direct-CM extraction scope.

### HPLC Report Signal Context

The channel names and audit paths observed in the table are carrier-specific configuration contracts, not generic aliases. Use the exact evidence rows below to decide which of these source categories apply:

| Observed item | Meaning for authoring | Required evidence before reuse |
|---|---|---|
| Raw channel, for example `UV_VIS_1` or `PumpPressureVirtual` | Detector, pump, virtual, or other acquired-signal context used by raw-statistic and peak formulas | The method/config must acquire or create that exact channel with compatible settings |
| Timed audit path, for example `AUDIT.UV.*` or `audit.ColumnComp.*` | Time-resolved settings/events, such as detector state, valve position, flow, or temperature | The selected injection audit must log the exact property path |
| Precondition path, for example `precond.UV.*` | Pre-run device identity/configuration | The device configuration must expose and log the property |
| `peak.*` / `chm.peak(...)` | Processed chromatographic peak/calibration result | A compatible processing method, channel and component must exist |

Time arguments in observed `chm.*` and timed `AUDIT.*` expressions are in minutes. Preserve all observed scale factors: for example `chm.noise(1,2)*1000` and `chm.drift(1,21)*60` are carrier-specific result contracts; do not remove or reinterpret multipliers without an acceptance/report-unit review.

### CM Formula Semantics Used by This Carrier

| Expression family | Meaning | Authoring constraint |
|---|---|---|
| `chm.noise(start,end)` | Signal noise over the stated raw-data time window | Bind the exact fixed channel. Preserve window boundaries and multiplier unless the test specification changes them deliberately |
| `chm.drift(start,end)` | Regression slope across the stated baseline window | Keep the signal channel and any unit conversion such as `*60` explicit |
| `chm.sig_value(stat,start,end)` / `chm.signalStatistic(...)` | Signal statistic over a window, commonly average/min/max | A raw signal channel and minute-based range are required |
| `chm.signalValue(time)` | Signal value at a specific minute | Requires a sampled signal at that point |
| `AUDIT.path(time,"forward"/"backward")` | Audit property selected at/after or at/before the requested minute | Retain the full observed device path unless its abbreviation is proven unambiguous |
| `precond.path` | Pre-run configuration/identity property | It does not read a raw chromatogram and cannot substitute for an audit event |
| `peak.*`, `chm.peak(...)` | Processed peak, calibration or component property | Require the matching processing method and component/channel binding |
| `seq.*`, `smp.*`, `injection.*`, `gen.*` | Sequence, sample, injection or software metadata | Use only fields observed in the selected carrier/config or explicitly verified |

### Direct Formula Object Contract

For every proposed direct-formula change, supply all of: exact existing sheet name, A1 cell/range from this inventory, `object_type: ReportFormulaObject`, CM formula text, `fixed_channel` when the source object uses a channel, `fixed_component` for component/peak context, and the required audit/channel/processing dependencies. If an object is absent from this inventory, it is not safe to invent in V0.1 clone-and-patch generation.

### HPLC Report Authoring Guardrails

1. Choose the data source first: raw VWD signal, detector audit setting, detector precondition, processed peak, or metadata.
2. Reuse the observed sheet/cell/object and fixed channel whenever it has the same semantic role.
3. A report formula can be syntactically valid but evaluate to `n.a.` when the instrument configuration, channel, audit path, wavelength, lamp configuration or processing component is absent.
4. Mark `OPEN VERIFICATION REQUIRED` rather than fabricating an unobserved channel, audit path, FormulaOne formula, acceptance criterion, display format or report-table schema.
5. Report tables (`ReportTableObject`) are structured, pipe-delimited definitions, not scalar cell formulas; preserve them unless a controlled CM before/after pair validates a table write rule.

## Sheet Applicability

| Sheet | Active | Each Injection | Query | Injection Variable | Query Values |
|---|---|---|---|---|---|
| Definitions | N | Y | Y |  |  |
| Title | Y | N | Y | injname | Temperature Precision_and_Fan |
| Test Procedures | Y | N | Y | injname | Temperature Precision_and_Fan |
| Temp Accuracy | Y | N | Y | injname | Temperature Accuracy |
| Temp Precision | Y | N | Y | injname | Temperature Precision_and_Fan |
| Temp Stability_Noise | Y | N | Y | injname | Temperature Stability |
| PCC | Y | N | Y | injname | Temperature Stability_and_PCC_H |
| Preheater Ports_Noise | Y | N | Y | injname | Preheater Connection Test |
| HeatUp&CoolDown | Y | N | Y | injname | HeatUp and CoolDownTime |
| Fan | Y | N | Y | injname | Temperature Precision_and_Fan |
| Valve_Keypad | Y | N | Y | injname | Valve |
| Column ID | Y | N | Y | injname | ColumnIDs |
| Liquid Leak Test | Y | N | Y | injname | LiquidLeaktest |
| COC | Y | N | Y | injname | Factory Default |
| FOQ VTCC History | N | Y | Y |  |  |
| Internal Use | Y | N | Y | injname | Factory Default |
| Temp_Calib_Internal | Y | N | Y | injname | Temperature Calibration |
| Audit Trail | N | Y | Y |  |  |
| Error Log | Y | N | Y | injname | Error Log Check |

## Sheet: Definitions

| Cell / Range | Object Type | Formula | Fixed Channel | Fixed Component |
|---|---|---|---|---|
| C7 | ReportFormulaObject | precond.System.Version |  |  |
| C8 | ReportFormulaObject | precond.System.SerialNo |  |  |
| C9 | ReportFormulaObject | seq.name |  |  |
| C10 | ReportFormulaObject | seq.update_time |  |  |
| C11 | ReportFormulaObject | gen.loggedOnUser.userName |  |  |
| C15 | ReportFormulaObject | AUDIT.ColumnComp.ModelNo |  |  |
| D15 | ReportFormulaObject | precond.ColumnComp.SerialNo |  |  |
| E15 | ReportFormulaObject | precond.ColumnComp.FirmwareVersion |  |  |
| C80 | ReportFormulaObject | seq.customVar("S/N Thermometer Germering") |  |  |
| C81 | ReportFormulaObject | seq.customVar("S/N Thermometer non-Germering") |  |  |
| C6 | ReportFormulaObject | seq.timebase |  |  |
| C83 | ReportFormulaObject | seq.customVar("Location") |  |  |

## Sheet: Temp Accuracy

| Cell / Range | Object Type | Formula | Fixed Channel | Fixed Component |
|---|---|---|---|---|
| E45 | ReportFormulaObject | chm.sig_value("average") | Environment_Temperature |  |
| K66 | ReportFormulaObject | AUDIT.RetTime1(1.000,"forward") |  |  |
| K67 | ReportFormulaObject | AUDIT.RetTime2(1.000,"forward") |  |  |
| K68 | ReportFormulaObject | AUDIT.RetTime3(1.000,"forward") |  |  |
| K69 | ReportFormulaObject | AUDIT.RetTime4(1.000,"forward") |  |  |
| K70 | ReportFormulaObject | AUDIT.RetTime5(1.000,"forward") |  |  |
| L66 | ReportFormulaObject | chm.sig_value("average",AUDIT.RetTime1(1,"forward")-1,AUDIT.RetTime1(1,"forward")-0.2) | ExtTemp_LowerCC |  |
| L67 | ReportFormulaObject | chm.sig_value("average",AUDIT.RetTime2(1,"forward")-1,AUDIT.RetTime2(1,"forward")-0.2) | ExtTemp_LowerCC |  |
| L68 | ReportFormulaObject | chm.sig_value("average",AUDIT.RetTime3(1,"forward")-1,AUDIT.RetTime3(1,"forward")-0.2) | ExtTemp_LowerCC |  |
| L69 | ReportFormulaObject | chm.sig_value("average",AUDIT.RetTime4(1,"forward")-1,AUDIT.RetTime4(1,"forward")-0.2) | ExtTemp_LowerCC |  |
| M66 | ReportFormulaObject | chm.sig_value("average",AUDIT.RetTime1(1,"forward")-1,AUDIT.RetTime1(1,"forward")-0.2) | ExtTemp_UpperCC |  |
| M67 | ReportFormulaObject | chm.sig_value("average",AUDIT.RetTime2(1,"forward")-1,AUDIT.RetTime2(1,"forward")-0.2) | ExtTemp_UpperCC |  |
| M68 | ReportFormulaObject | chm.sig_value("average",AUDIT.RetTime3(1,"forward")-1,AUDIT.RetTime3(1,"forward")-0.2) | ExtTemp_UpperCC |  |
| M69 | ReportFormulaObject | chm.sig_value("average",AUDIT.RetTime4(1,"forward")-1,AUDIT.RetTime4(1,"forward")-0.2) | ExtTemp_UpperCC |  |
| L70 | ReportFormulaObject | chm.sig_value("average",AUDIT.RetTime5(1,"forward")-1,AUDIT.RetTime5(1,"forward")-0.2) | ExtTemp_LowerCC |  |
| M70 | ReportFormulaObject | chm.sig_value("average",AUDIT.RetTime5(1,"forward")-1,AUDIT.RetTime5(1,"forward")-0.2) | ExtTemp_UpperCC |  |
| I66 | ReportFormulaObject | AUDIT.ColumnComp.CC.Temperature.Nominal(AUDIT.RetTime1(1,"forward")-0.1) |  |  |
| I67 | ReportFormulaObject | AUDIT.ColumnComp.CC.Temperature.Nominal(AUDIT.RetTime2(1,"forward")-0.1) |  |  |
| I68 | ReportFormulaObject | AUDIT.ColumnComp.CC.Temperature.Nominal(AUDIT.RetTime3(1,"forward")-0.1) |  |  |
| I69 | ReportFormulaObject | AUDIT.ColumnComp.CC.Temperature.Nominal(AUDIT.RetTime4(1,"forward")-0.1) |  |  |
| I70 | ReportFormulaObject | AUDIT.ColumnComp.CC.Temperature.Nominal(AUDIT.RetTime5(1,"forward")-0.1) |  |  |

## Sheet: Temp Precision

| Cell / Range | Object Type | Formula | Fixed Channel | Fixed Component |
|---|---|---|---|---|
| I66 | ReportFormulaObject | AUDIT.ColumnComp.CC.Temperature.Nominal(36.9,"backward") |  |  |
| I67 | ReportFormulaObject | AUDIT.ColumnComp.CC.Temperature.Nominal(58.9,"backward") |  |  |
| K66 | ReportFormulaObject | chm.sig_value("average",36,36.8) | ExtTemp_LowerCC |  |
| K67 | ReportFormulaObject | chm.sig_value("average",58,58.8) | ExtTemp_LowerCC |  |
| L66 | ReportFormulaObject | chm.sig_value("average",36,36.8) | ExtTemp_UpperCC |  |
| L67 | ReportFormulaObject | chm.sig_value("average",58,58.8) | ExtTemp_UpperCC |  |
| L65 | ReportFormulaObject | chm.sig_value("average",14,14.8) | ExtTemp_UpperCC |  |
| K65 | ReportFormulaObject | chm.sig_value("average",14,14.8) | ExtTemp_LowerCC |  |
| I65 | ReportFormulaObject | AUDIT.ColumnComp.CC.Temperature.Nominal(14.9,"backward") |  |  |

## Sheet: Temp Stability_Noise

| Cell / Range | Object Type | Formula | Fixed Channel | Fixed Component |
|---|---|---|---|---|
| K61 | ReportFormulaObject | chm.sig_value("average",45,46) | ExtTemp_LowerCC |  |
| K62 | ReportFormulaObject | chm.sig_value("average",46,47) | ExtTemp_LowerCC |  |
| K63 | ReportFormulaObject | chm.sig_value("average",47,48) | ExtTemp_LowerCC |  |
| K64 | ReportFormulaObject | chm.sig_value("average",48,49) | ExtTemp_LowerCC |  |
| K65 | ReportFormulaObject | chm.sig_value("average",49,50) | ExtTemp_LowerCC |  |
| K66 | ReportFormulaObject | chm.sig_value("average",50,51) | ExtTemp_LowerCC |  |
| K67 | ReportFormulaObject | chm.sig_value("average",51,52) | ExtTemp_LowerCC |  |
| K68 | ReportFormulaObject | chm.sig_value("average",52,53) | ExtTemp_LowerCC |  |
| K69 | ReportFormulaObject | chm.sig_value("average",53,54) | ExtTemp_LowerCC |  |
| K70 | ReportFormulaObject | chm.sig_value("average",54,55) | ExtTemp_LowerCC |  |
| K71 | ReportFormulaObject | chm.sig_value("average",55,56) | ExtTemp_LowerCC |  |
| K72 | ReportFormulaObject | chm.sig_value("average",56,57) | ExtTemp_LowerCC |  |
| K73 | ReportFormulaObject | chm.sig_value("average",57,58) | ExtTemp_LowerCC |  |
| K74 | ReportFormulaObject | chm.sig_value("average",58,59) | ExtTemp_LowerCC |  |
| K75 | ReportFormulaObject | chm.sig_value("average",59,60) | ExtTemp_LowerCC |  |
| L61 | ReportFormulaObject | chm.sig_value("average",45,46) | ExtTemp_UpperCC |  |
| L62 | ReportFormulaObject | chm.sig_value("average",46,47) | ExtTemp_UpperCC |  |
| L63 | ReportFormulaObject | chm.sig_value("average",47,48) | ExtTemp_UpperCC |  |
| L64 | ReportFormulaObject | chm.sig_value("average",48,49) | ExtTemp_UpperCC |  |
| L65 | ReportFormulaObject | chm.sig_value("average",49,50) | ExtTemp_UpperCC |  |
| L66 | ReportFormulaObject | chm.sig_value("average",50,51) | ExtTemp_UpperCC |  |
| L67 | ReportFormulaObject | chm.sig_value("average",51,52) | ExtTemp_UpperCC |  |
| L68 | ReportFormulaObject | chm.sig_value("average",52,53) | ExtTemp_UpperCC |  |
| L69 | ReportFormulaObject | chm.sig_value("average",53,54) | ExtTemp_UpperCC |  |
| L70 | ReportFormulaObject | chm.sig_value("average",54,55) | ExtTemp_UpperCC |  |
| L71 | ReportFormulaObject | chm.sig_value("average",55,56) | ExtTemp_UpperCC |  |
| L72 | ReportFormulaObject | chm.sig_value("average",56,57) | ExtTemp_UpperCC |  |
| L73 | ReportFormulaObject | chm.sig_value("average",57,58) | ExtTemp_UpperCC |  |
| L74 | ReportFormulaObject | chm.sig_value("average",58,59) | ExtTemp_UpperCC |  |
| L75 | ReportFormulaObject | chm.sig_value("average",59,60) | ExtTemp_UpperCC |  |
| K86 | ReportFormulaObject | chm.noise(59,60) | CC_Temp |  |
| K87 | ReportFormulaObject | chm.noise(59,60) | PCC_Temp |  |

## Sheet: PCC

| Cell / Range | Object Type | Formula | Fixed Channel | Fixed Component |
|---|---|---|---|---|
| K89 | ReportFormulaObject | AUDIT.PCC.Temperature.Nominal (4.000) |  |  |
| K90 | ReportFormulaObject | AUDIT.PCC.Temperature.Nominal(12.000) |  |  |
| K91 | ReportFormulaObject | AUDIT.PCC.Temperature.Nominal(20.000) |  |  |
| L89 | ReportFormulaObject | chm.sig_value("average", 0, 5) | PCC_Temp |  |
| L90 | ReportFormulaObject | chm.sig_value("average", 10, 15) | PCC_Temp |  |
| L91 | ReportFormulaObject | chm.sig_value("average", 19, 24) | PCC_Temp |  |
| K97 | ReportFormulaObject | chm.sig_value("drift", 19, 24) | PCC_Temp |  |
| K105 | ReportFormulaObject | AUDIT.RetTime3(1.000,"forward") |  |  |
| L105 | ReportFormulaObject | AUDIT.RetTime4(1.000,"forward") |  |  |
| L110 | ReportFormulaObject | audit.ColumnComp.PCC.Temperature.Value(AUDIT.RetTime3(1,"forward")-1,"forward") | Environment_Temperature |  |
| L111 | ReportFormulaObject | audit.ColumnComp.PCC.Temperature.Value(AUDIT.RetTime4(1,"forward")+1,"backward") | Environment_Temperature |  |

## Sheet: Preheater Ports_Noise

| Cell / Range | Object Type | Formula | Fixed Channel | Fixed Component |
|---|---|---|---|---|
| J82 | ReportFormulaObject | chm.sig_value("average", 0.25, 0.5) | PrehtLeft_Temp |  |
| K82 | ReportFormulaObject | chm.sig_value("average", 0.25, 0.5) | PREH_L_HeaterTemp_Actual |  |
| J83 | ReportFormulaObject | chm.sig_value("average", 0.25, 0.5) | PrehtRight_Temp |  |
| K83 | ReportFormulaObject | chm.sig_value("average",0.25, 0.5) | PREH_R_HeaterTemp_Actual |  |
| J92 | ReportFormulaObject | chm.noise(0, 0.5) | PrehtLeft_Temp |  |
| J93 | ReportFormulaObject | chm.noise(0, 0.5) | PrehtRight_Temp |  |
| K92 | ReportFormulaObject | chm.noise(0, 0.5) | PREH_L_HeaterTemp_Actual |  |
| K93 | ReportFormulaObject | chm.noise(0, 0.5) | PREH_R_HeaterTemp_Actual |  |
| J102 | ReportFormulaObject | chm.sig_value("average",0.25,0.5) | PrehtLeft_Temp |  |
| K102 | ReportFormulaObject | chm.sig_value("max", 0.5, 0.6) | PrehtLeft_Temp |  |
| J103 | ReportFormulaObject | chm.sig_value("average",0.25,0.5) | PrehtRight_Temp |  |
| K103 | ReportFormulaObject | chm.sig_value("max", 0.5, 0.6) | PrehtRight_Temp |  |
| J110 | ReportFormulaObject | chm.sig_value("average", 0.4, 0.5) | PREH_L_HeaterTemp_Actual |  |
| K110 | ReportFormulaObject | chm.sig_value("max", 0.5, 0.6) | PREH_L_HeaterTemp_Actual |  |
| J111 | ReportFormulaObject | chm.sig_value("average", 0.4, 0.5) | PREH_R_HeaterTemp_Actual |  |
| K111 | ReportFormulaObject | chm.sig_value("max", 0.5, 0.6) | PREH_R_HeaterTemp_Actual |  |
| J72 | ReportFormulaObject | AUDIT.RetTime1("forward") |  |  |
| J73 | ReportFormulaObject | AUDIT.RetTime2("forward") |  |  |
| K72 | ReportFormulaObject | AUDIT.RetTime3("forward") |  |  |
| K73 | ReportFormulaObject | AUDIT.RetTime4("forward") |  |  |
| J117 | ReportFormulaObject | precond.ColumnComp.PrehtLeft.ModulePresent |  |  |
| J118 | ReportFormulaObject | precond.ColumnComp.PrehtRight.ModulePresent |  |  |
| K117 | ReportFormulaObject | precond.ColumnComp.PrehtLeft.MemoryState |  |  |
| K118 | ReportFormulaObject | precond.ColumnComp.PrehtRight.MemoryState |  |  |

## Sheet: HeatUp&CoolDown

| Cell / Range | Object Type | Formula | Fixed Channel | Fixed Component |
|---|---|---|---|---|
| J65 | ReportFormulaObject | AUDIT.RetTime1(1.000,"forward") |  |  |
| K65 | ReportFormulaObject | AUDIT.RetTime3(1.000,"forward") |  |  |
| K66 | ReportFormulaObject | AUDIT.RetTime2(1.000,"forward") |  |  |
| L65 | ReportFormulaObject | AUDIT.RetTime4(1.000,"forward") |  |  |
| M65 | ReportFormulaObject | AUDIT.RetTime6(1.000,"forward") |  |  |
| L66 | ReportFormulaObject | AUDIT.RetTime4(1.000,"forward") |  |  |
| M66 | ReportFormulaObject | AUDIT.RetTime5(1.000,"forward") |  |  |
| J66 | ReportFormulaObject | AUDIT.RetTime1(1.000,"forward") |  |  |
| L57 | ReportFormulaObject | AUDIT.ColumnComp.CC.Temperature.Nominal(AUDIT.RetTime1(1,"forward")-0.1) |  |  |
| L58 | ReportFormulaObject | AUDIT.ColumnComp.CC.Temperature.Nominal(AUDIT.RetTime2(1,"forward")-0.1) |  |  |

## Sheet: Fan

| Cell / Range | Object Type | Formula | Fixed Channel | Fixed Component |
|---|---|---|---|---|
| J49 | ReportFormulaObject | chm.signalStatistic("average",63.1,64.1) | CC_Temp |  |
| J50 | ReportFormulaObject | chm.signalStatistic("min",64.1,74) | CC_Temp |  |
| J51 | ReportFormulaObject | chm.signalStatistic("average",74,75) | CC_Temp |  |
| J52 | ReportFormulaObject | chm.signalStatistic("max",75,76) | CC_Temp |  |
| W57 | ReportFormulaObject | chm.signalStatistic("min",63.1,64.1) | CC_Temp |  |
| X57 | ReportFormulaObject | chm.signalStatistic("max",63.1,64.1) | CC_Temp |  |
| W58 | ReportFormulaObject | chm.signalStatistic("min",74,75) | CC_Temp |  |
| X58 | ReportFormulaObject | chm.signalStatistic("max",74,75) | CC_Temp |  |

## Sheet: Valve_Keypad

| Cell / Range | Object Type | Formula | Fixed Channel | Fixed Component |
|---|---|---|---|---|
| K49 | ReportFormulaObject | AUDIT.UpperValve.CurrentPosition(-0.05) |  |  |
| L49 | ReportFormulaObject | AUDIT.LowerValve.CurrentPosition(-0.05) |  |  |
| K50 | ReportFormulaObject | AUDIT.UpperValve.CurrentPosition(0.095) |  |  |
| K51 | ReportFormulaObject | AUDIT.UpperValve.CurrentPosition(0.19) |  |  |
| L50 | ReportFormulaObject | AUDIT.LowerValve.CurrentPosition(0.095) |  |  |
| L51 | ReportFormulaObject | AUDIT.LowerValve.CurrentPosition(0.19) |  |  |
| K60 | ReportFormulaObject | AUDIT.UpperValve.CurrentPosition(0.9) |  |  |
| L60 | ReportFormulaObject | AUDIT.LowerValve.CurrentPosition(0.9) |  |  |
| N60 | ReportFormulaObject | AUDIT.ColumnComp.FastCoolState(0.9,"backward") |  |  |
| U49 | ReportFormulaObject | AUDIT.UpperValve.Precision(-0.05,"forward") |  |  |
| U50 | ReportFormulaObject | AUDIT.UpperValve.Precision(0.095,"forward") |  |  |
| U51 | ReportFormulaObject | AUDIT.UpperValve.Precision(0.19,"forward") |  |  |
| V49 | ReportFormulaObject | AUDIT.LowerValve.Precision(-0.05,"forward") |  |  |
| V50 | ReportFormulaObject | AUDIT.LowerValve.Precision(0.095,"forward") |  |  |
| V51 | ReportFormulaObject | AUDIT.LowerValve.Precision(0.19,"forward") |  |  |

## Sheet: Column ID

| Cell / Range | Object Type | Formula | Fixed Channel | Fixed Component |
|---|---|---|---|---|
| L46 | ReportFormulaObject | AUDIT.Column_A.Description(0,"forward") |  |  |
| L47 | ReportFormulaObject | AUDIT.Column_B.Description(0,"forward") |  |  |
| L48 | ReportFormulaObject | AUDIT.Column_C.Description(0,"forward") |  |  |
| L49 | ReportFormulaObject | AUDIT.Column_D.Description(0,"forward") |  |  |

## Sheet: Liquid Leak Test

| Cell / Range | Object Type | Formula | Fixed Channel | Fixed Component |
|---|---|---|---|---|
| M47 | ReportFormulaObject | AUDIT.LiquidLeak(100.000,"backward") |  |  |
| K47 | ReportFormulaObject | precond.LiquidLeakCalibrationValue |  |  |

## Sheet: Internal Use

| Cell / Range | Object Type | Formula | Fixed Channel | Fixed Component |
|---|---|---|---|---|
| B20 | ReportFormulaObject | seq.name |  |  |
| D20 | ReportFormulaObject | seq.creation_time |  |  |
| F20 | ReportFormulaObject | seq.submitTime |  |  |
| E9 | ReportFormulaObject | precond.ColumnComp.FirmwareVersion |  |  |
| E11 | ReportFormulaObject | precond.ColumnComp.HardwareVersion |  |  |
| E12 | ReportFormulaObject | precond.ColumnComp.ModuleHardwareRevision |  |  |
| E13 | ReportFormulaObject | precond.ColumnComp.cc.HardwareVersion |  |  |
| E14 | ReportFormulaObject | precond.ColumnComp.pcc.HardwareVersion |  |  |
| B29:D34 | ReportTableObject | injection.number \| "No. " \| "" \| injection.name \| "" \| "" \| injection.name \| "Injection Name" \| "" \| injection.name \| "" \| "" \| injection.time \| "Inject Time " \| "" \| injection.name \| "" \| "" |  |  |
| F24 | ReportFormulaObject | seq.submitOperator |  |  |
| B24 | ReportFormulaObject | seq.dataVault |  |  |
| D24 | ReportFormulaObject | seq.signStatus |  |  |

## Sheet: Temp_Calib_Internal

| Cell / Range | Object Type | Formula | Fixed Channel | Fixed Component |
|---|---|---|---|---|
| B15 | ReportFormulaObject | chm.signalValue(AUDIT.RetTime1(1,"forward")) | CC_Temp |  |
| B16 | ReportFormulaObject | chm.signalValue(AUDIT.RetTime2(1,"forward")) | CC_Temp |  |
| B17 | ReportFormulaObject | chm.signalValue(AUDIT.RetTime3(1,"forward")) | CC_Temp |  |
| B19 | ReportFormulaObject | chm.signalValue(AUDIT.RetTime5(1,"forward")) | CC_Temp |  |
| B18 | ReportFormulaObject | chm.signalValue(AUDIT.RetTime4(1,"forward")) | CC_Temp |  |
| B20 | ReportFormulaObject | chm.signalValue(AUDIT.RetTime6(1,"forward")) | CC_Temp |  |
| B21 | ReportFormulaObject | chm.signalValue(AUDIT.RetTime7(1,"forward")) | CC_Temp |  |
| C15 | ReportFormulaObject | AUDIT.RetTime1(1,"forward") |  |  |
| C16 | ReportFormulaObject | AUDIT.RetTime2(1,"forward")-AUDIT.RetTime1(1,"forward") |  |  |
| C17 | ReportFormulaObject | AUDIT.RetTime3(1,"forward")-AUDIT.RetTime2(1,"forward") |  |  |
| C18 | ReportFormulaObject | AUDIT.RetTime4(1,"forward")-AUDIT.RetTime3(1,"forward") |  |  |
| C19 | ReportFormulaObject | AUDIT.RetTime5(1,"forward")-AUDIT.RetTime4(1,"forward") |  |  |
| C20 | ReportFormulaObject | AUDIT.RetTime6(1,"forward")-AUDIT.RetTime5(1,"forward") |  |  |
| C21 | ReportFormulaObject | AUDIT.RetTime7(1,"forward")-AUDIT.RetTime6(1,"forward") |  |  |
| D15 | ReportFormulaObject | chm.drift(AUDIT.RetTime1(1,"forward")-0.5,AUDIT.RetTime1(1,"forward")) | ExtTemp_UpperCC |  |
| D16 | ReportFormulaObject | chm.drift(AUDIT.RetTime2(1,"forward")-0.5,AUDIT.RetTime2(1,"forward")) | ExtTemp_UpperCC |  |
| D17 | ReportFormulaObject | chm.drift(AUDIT.RetTime3(1,"forward")-0.5,AUDIT.RetTime3(1,"forward")) | ExtTemp_UpperCC |  |
| D18 | ReportFormulaObject | chm.drift(AUDIT.RetTime4(1,"forward")-0.5,AUDIT.RetTime4(1,"forward")) | ExtTemp_UpperCC |  |
| D19 | ReportFormulaObject | chm.drift(AUDIT.RetTime5(1,"forward")-0.5,AUDIT.RetTime5(1,"forward")) | ExtTemp_UpperCC |  |
| D20 | ReportFormulaObject | chm.drift(AUDIT.RetTime6(1,"forward")-0.5,AUDIT.RetTime6(1,"forward")) | ExtTemp_UpperCC |  |
| D21 | ReportFormulaObject | chm.drift(AUDIT.RetTime7(1,"forward")-0.5,AUDIT.RetTime7(1,"forward")) | ExtTemp_UpperCC |  |
| E15 | ReportFormulaObject | chm.drift(AUDIT.RetTime1(1,"forward")-0.5,AUDIT.RetTime1(1,"forward")) | ExtTemp_LowerCC |  |
| E16 | ReportFormulaObject | chm.drift(AUDIT.RetTime2(1,"forward")-0.5,AUDIT.RetTime2(1,"forward")) | ExtTemp_LowerCC |  |
| E17 | ReportFormulaObject | chm.drift(AUDIT.RetTime3(1,"forward")-0.5,AUDIT.RetTime3(1,"forward")) | ExtTemp_LowerCC |  |
| E18 | ReportFormulaObject | chm.drift(AUDIT.RetTime4(1,"forward")-0.5,AUDIT.RetTime4(1,"forward")) | ExtTemp_LowerCC |  |
| E19 | ReportFormulaObject | chm.drift(AUDIT.RetTime5(1,"forward")-0.5,AUDIT.RetTime5(1,"forward")) | ExtTemp_LowerCC |  |
| E20 | ReportFormulaObject | chm.drift(AUDIT.RetTime6(1,"forward")-0.5,AUDIT.RetTime6(1,"forward")) | ExtTemp_LowerCC |  |
| E21 | ReportFormulaObject | chm.drift(AUDIT.RetTime7(1,"forward")-0.5,AUDIT.RetTime7(1,"forward")) | ExtTemp_LowerCC |  |
| B27 | ReportFormulaObject | audit.ColumnComp.CC.TempCalibrationPointUpper1(1000,"backward") | ExtTemp_UpperCC |  |
| D27 | ReportFormulaObject | audit.ColumnComp.CC.TempCalibrationDeviationUpper1(1000,"backward") |  |  |
| D29 | ReportFormulaObject | audit.ColumnComp.CC.TempCalibrationDeviationUpper3(1000,"backward") |  |  |
| B28 | ReportFormulaObject | audit.ColumnComp.CC.TempCalibrationPointUpper2(1000,"backward") |  |  |
| B30 | ReportFormulaObject | audit.ColumnComp.CC.TempCalibrationPointUpper4(1000,"backward") |  |  |
| D28 | ReportFormulaObject | audit.ColumnComp.CC.TempCalibrationDeviationUpper2(1000,"backward") |  |  |
| D30 | ReportFormulaObject | audit.ColumnComp.CC.TempCalibrationDeviationUpper4(1000,"backward") |  |  |
| B31 | ReportFormulaObject | audit.ColumnComp.CC.TempCalibrationPointUpper5(1000,"backward") |  |  |
| B33 | ReportFormulaObject | audit.ColumnComp.CC.TempCalibrationPointUpper7(1000,"backward") |  |  |
| D31 | ReportFormulaObject | audit.ColumnComp.CC.TempCalibrationDeviationUpper5(1000,"backward") |  |  |
| D33 | ReportFormulaObject | audit.ColumnComp.CC.TempCalibrationDeviationUpper7(1000,"backward") |  |  |
| B32 | ReportFormulaObject | audit.ColumnComp.CC.TempCalibrationPointUpper6(1000,"backward") |  |  |
| B34 | ReportFormulaObject | audit.ColumnComp.CC.TempCalibrationPointUpper8(1000,"backward") |  |  |
| D32 | ReportFormulaObject | audit.ColumnComp.CC.TempCalibrationDeviationUpper6(1000,"backward") |  |  |
| B36 | ReportFormulaObject | audit.ColumnComp.CC.TempCalibrationPointLower1(1000,"backward") |  |  |
| B38 | ReportFormulaObject | audit.ColumnComp.CC.TempCalibrationPointLower3(1000,"backward") |  |  |
| D36 | ReportFormulaObject | audit.ColumnComp.CC.TempCalibrationDeviationLower1(1000,"backward") |  |  |
| D38 | ReportFormulaObject | audit.ColumnComp.CC.TempCalibrationDeviationLower3(1000,"backward") |  |  |
| B37 | ReportFormulaObject | audit.ColumnComp.CC.TempCalibrationPointLower2(1000,"backward") |  |  |
| B39 | ReportFormulaObject | audit.ColumnComp.CC.TempCalibrationPointLower4(1000,"backward") |  |  |
| D37 | ReportFormulaObject | audit.ColumnComp.CC.TempCalibrationDeviationLower2(1000,"backward") |  |  |
| D39 | ReportFormulaObject | audit.ColumnComp.CC.TempCalibrationDeviationLower4(1000,"backward") |  |  |
| B40 | ReportFormulaObject | audit.ColumnComp.CC.TempCalibrationPointLower5(1000,"backward") |  |  |
| B42 | ReportFormulaObject | audit.ColumnComp.CC.TempCalibrationPointLower7(1000,"backward") |  |  |
| D40 | ReportFormulaObject | audit.ColumnComp.CC.TempCalibrationDeviationLower5(1000,"backward") |  |  |
| D42 | ReportFormulaObject | audit.ColumnComp.CC.TempCalibrationDeviationLower7(1000,"backward") |  |  |
| B41 | ReportFormulaObject | audit.ColumnComp.CC.TempCalibrationPointLower6(1000,"backward") |  |  |
| B43 | ReportFormulaObject | audit.ColumnComp.CC.TempCalibrationPointLower8(1000,"backward") |  |  |
| D41 | ReportFormulaObject | audit.ColumnComp.CC.TempCalibrationDeviationLower6(1000,"backward") |  |  |
| D43 | ReportFormulaObject | audit.ColumnComp.CC.TempCalibrationDeviationLower8(1000,"backward") |  |  |
| B29 | ReportFormulaObject | audit.ColumnComp.CC.TempCalibrationPointUpper3(1000,"backward") |  |  |
| C45 | ReportFormulaObject | chm.sig_value("average") | Environment_Temperature |  |
| K46 | ReportFormulaObject | chm.sig_value("min") | ExtTemp_LowerCC |  |
| K45 | ReportFormulaObject | chm.sig_value("min") | ExtTemp_UpperCC |  |
| D34 | ReportFormulaObject | audit.ColumnComp.CC.TempCalibrationDeviationUpper8(1000,"backward") |  |  |
| J14 | ReportFormulaObject | chm.signalValue(AUDIT.RetTime8(1,"forward")-1) | CC_Temp |  |
| J15 | ReportFormulaObject | AUDIT.RetTime8(1,"forward")-AUDIT.RetTime7(1,"forward") |  |  |
| J16 | ReportFormulaObject | chm.drift(AUDIT.RetTime8(1,"forward")-0.5,AUDIT.RetTime8(1,"forward")) | ExtTemp_UpperCC |  |
| J17 | ReportFormulaObject | chm.drift(AUDIT.RetTime8(1,"forward")-0.5,AUDIT.RetTime8(1,"forward")) | ExtTemp_LowerCC |  |

## Sheet: Audit Trail

| Cell / Range | Object Type | Formula | Fixed Channel | Fixed Component |
|---|---|---|---|---|
| C4 | ReportFormulaObject | smp.name |  |  |
| C5 | ReportFormulaObject | smp.type |  |  |
| C6 | ReportFormulaObject | smp.program |  |  |
| C7 | ReportFormulaObject | smp.method |  |  |
| C8 | ReportFormulaObject | smp.time |  |  |
| C9 | ReportFormulaObject | chm.end_time - chm.start_time |  |  |
| C10 | ReportFormulaObject | chm.channel |  |  |

# FormulaOne Workbook Formula Inventory

These formulas are stored in `SpreadSheetData`. They are Excel-like FormulaOne formulas, not CM `ReportFormulaObject` expressions. The reader exports formula strings only; visible values, formatting, merged cells, dynamic-table schema and print layout remain outside this inventory.

## FormulaOne Sheet: Audit Trail

| Cell | Formula |
|---|---|
| J6 | IF(ISNUMBER(MATCH("*Alarm muted by key*",$C$14:$C$16,0)),Definitions!$B$61,Definitions!$B$62) |

## FormulaOne Sheet: COC

| Cell | Formula |
|---|---|
| E16 | Definitions!$B$15 |
| E17 | Definitions!$C$15 |
| E18 | Definitions!$D$15 |
| E33 | IF(Internal Use!D40="Test Passed","","Check Internal_Use page!!!") |
| B34 | Definitions!C10 |

## FormulaOne Sheet: Column ID

| Cell | Formula |
|---|---|
| A5 | Definitions!$A$2 |
| B14 | Definitions!$B$15 |
| C14 | Definitions!$C$15 |
| D14 | Definitions!$D$15 |
| B15 | Definitions!$B$16 |
| C15 | Definitions!$C$16 |
| D15 | Definitions!$D$16 |
| B16 | Definitions!$B$17 |
| C16 | Definitions!$C$17 |
| D16 | Definitions!$D$17 |
| B17 | Definitions!$B$7 |
| C17 | Definitions!$D$7 |
| D17 | Definitions!$C$8 |
| B19 | Definitions!$B$10 |
| C19 | Definitions!$C$10 |
| B20 | Definitions!$B$11 |
| C20 | Definitions!$C$11 |
| C25 | Definitions!$B$53 |
| B26 | J46 |
| C26 | IF($M46=1,Definitions!$B$54,Definitions!$B$55) |
| B27 | J47 |
| C27 | IF($M47=1,Definitions!$B$54,Definitions!$B$55) |
| B28 | J48 |
| C28 | IF($M48=1,Definitions!$B$54,Definitions!$B$55) |
| B29 | J49 |
| C29 | IF($M49=1,Definitions!$B$54,Definitions!$B$55) |
| M46 | IF($K46=$L46,1,0) |
| M47 | IF($K47=$L47,1,0) |
| M48 | IF($K48=$L48,1,0) |
| M49 | IF($K49=$L49,1,0) |

## FormulaOne Sheet: Definitions

| Cell | Formula |
|---|---|
| J5 | C15 |
| J6 | INDIRECT(ADDRESS($J$1+ROW(),(11+MATCH($J$5,$L$5:$Q$5,0)),1)) |
| D7 | LEFT(C7,SEARCH("B",$C$7)-1) |
| J7 | INDIRECT(ADDRESS($J$1+ROW(),(11+MATCH($J$5,$L$5:$Q$5,0)),1)) |
| J8 | INDIRECT(ADDRESS($J$1+ROW(),(11+MATCH($J$5,$L$5:$Q$5,0)),1)) |
| J9 | INDIRECT(ADDRESS($J$1+ROW(),(11+MATCH($J$5,$L$5:$Q$5,0)),1)) |
| J10 | INDIRECT(ADDRESS($J$1+ROW(),(11+MATCH($J$5,$L$5:$Q$5,0)),1)) |
| D16 | IF($C$83="non-Germering",$C$81,IF($C$83="Germering",$C$80,"#N/A")) |
| D17 | IF($C$83="non-Germering",$C$88,IF($C$83="Germering",$C$87,"#N/A")) |
| D80 | IF(C80="n.a.","-",IF(ISNA(MATCH(VALUE($C80),$B$93:$B$171,0)),$B$62,$B$61)) |
| D81 | IF(C81="n.a.","-",IF(ISNA(MATCH(VALUE($C81),$C$93:$C$300,0)),$B$62,$B$61)) |
| C85 | IF($C$83="Germering",IF($D80=$B$61,$B$61,$B$62),IF($C$83="non-Germering",IF($D81=$B$61,$B$61,$B$62),$B$62)) |

## FormulaOne Sheet: Error Log

| Cell | Formula |
|---|---|
| A5 | Definitions!$A$2 |
| E19 | IF(ISERROR(FIND("No audit trail messages",INDIRECT(ADDRESS(13,4)))),Definitions!B62,Definitions!B61) |

## FormulaOne Sheet: Fan

| Cell | Formula |
|---|---|
| A5 | Definitions!$A$2 |
| B14 | Definitions!$B$15 |
| C14 | Definitions!$C$15 |
| D14 | Definitions!$D$15 |
| B15 | Definitions!$B$16 |
| C15 | Definitions!$C$16 |
| D15 | Definitions!$D$16 |
| B16 | Definitions!$B$17 |
| C16 | Definitions!$C$17 |
| D16 | Definitions!$D$17 |
| B17 | Definitions!$B$7 |
| C17 | Definitions!$D$7 |
| D17 | Definitions!$C$8 |
| B19 | Definitions!$B$10 |
| C19 | Definitions!$C$10 |
| B20 | Definitions!$B$11 |
| C20 | Definitions!$C$11 |
| C25 | Definitions!$B$53 |
| C26 | K53 |
| K47 | Definitions!B53 |
| K49 | IF((X57-W57)<Definitions!$C$26/4,Definitions!$B$61,Definitions!$B$62) |
| K50 | IF((J49-J50)>=Definitions!$C$26/2,Definitions!$B$61,Definitions!$B$62) |
| K51 | IF((X58-W58)<Definitions!$C$26/4,Definitions!$B$61,Definitions!$B$62) |
| K52 | IF((J52-J51)>=Definitions!$C$26/2,Definitions!$B$61,Definitions!$B$62) |
| J53 | Definitions!$B$53 |
| K53 | IF(COUNTIF(K49:K52,Definitions!B61)=4,Definitions!B54,Definitions!B55) |

## FormulaOne Sheet: HeatUp&CoolDown

| Cell | Formula |
|---|---|
| A5 | Definitions!$A$2 |
| B9 | CONCATENATE(" •  Heat Up / Cool Down Time (",K57," °C to ",K58," °C to ",K57," °C)") |
| B14 | Definitions!$B$15 |
| C14 | Definitions!$C$15 |
| D14 | Definitions!$D$15 |
| B15 | Definitions!$B$16 |
| C15 | Definitions!$C$16 |
| D15 | Definitions!$D$16 |
| B16 | Definitions!$B$17 |
| C16 | Definitions!$C$17 |
| D16 | Definitions!$D$17 |
| B17 | Definitions!$B$7 |
| C17 | Definitions!$D$7 |
| D17 | Definitions!$C$8 |
| B19 | Definitions!$B$10 |
| C19 | Definitions!$C$10 |
| B20 | Definitions!$B$11 |
| C20 | Definitions!$C$11 |
| C25 | Definitions!$B$51 |
| D25 | Definitions!B70 |
| E25 | Definitions!$B$53 |
| B26 | Definitions!$B$71 |
| C26 | Definitions!C27 |
| D26 | E65 |
| E26 | IF(ROUND(D26,1)<C26,Definitions!$B$54,Definitions!$B$55) |
| B27 | Definitions!$B$69 |
| C27 | Definitions!C27 |
| D27 | E66 |
| E27 | IF(ROUND(D27,1)<C27,Definitions!$B$54,Definitions!$B$55) |
| K57 | ROUND(L57,0) |
| K58 | ROUND(L58,0) |
| B65 | CONCATENATE(K57," °C to ",K58," °C") |
| C65 | ROUND(J66,1) |
| D65 | ROUND(K66-2,1) |
| E65 | D65-C65 |
| B66 | CONCATENATE(K58," °C to ",K57," °C") |
| C66 | ROUND(L66,1) |
| D66 | ROUND(M66-2,1) |
| E66 | D66-C66 |
| D67 | Definitions!B53 |
| E67 | IF(AND(E65<Definitions!C27,E66<Definitions!C27),Definitions!$B61,Definitions!$B62) |

## FormulaOne Sheet: Internal Use

| Cell | Formula |
|---|---|
| A5 | Definitions!$A$2 |
| C9 | Definitions!$J$6 |
| F9 | IF(C9=E9,Definitions!$B$61,Definitions!$B$62) |
| C10 | Definitions!$D$15 |
| E10 | Definitions!$C$9 |
| F10 | IF(C10=E10,Definitions!$B$61,Definitions!$B$62) |
| C11 | Definitions!$J$7 |
| F11 | IF(C11=E11,Definitions!$B$61,Definitions!$B$62) |
| C12 | Definitions!$J$8 |
| F12 | IF(OR(E12=C12,E12="n.a."),Definitions!$B$61,Definitions!$B$62) |
| C13 | Definitions!$J$9 |
| F13 | IF(OR(E13=C13,E13="n.a."),Definitions!$B$61,Definitions!$B$62) |
| C14 | Definitions!$J$10 |
| F14 | IF(OR(E14=C14,E14="n.a."),Definitions!$B$61,Definitions!$B$62) |
| J33 | IF(INDIRECT(ADDRESS(ROW(),4))>INDIRECT(ADDRESS(46,4)),1,0) |
| K33 | IF(INDIRECT(ADDRESS(ROW(),4))>INDIRECT(ADDRESS(47,4)),1,0) |
| J34 | IF(INDIRECT(ADDRESS(ROW(),4))>INDIRECT(ADDRESS(46,4)),1,0) |
| K34 | IF(INDIRECT(ADDRESS(ROW(),4))>INDIRECT(ADDRESS(47,4)),1,0) |
| D35 | INDIRECT(ADDRESS(ROW(D32)+MATCH("Factory Default",C33:C34,0),4)) |
| D36 | INDIRECT(ADDRESS(ROW(D32)+MATCH("Error Log Check",C33:C34,0),4)) |
| D37 | SUM($J$33:$J$34) |
| D38 | SUM($K$33:$K$34) |
| D40 | IF(AND(COUNTIF($F$9:$F$14,"ok")=6,$D$37=1,$D$38=0),Definitions!$B$54,Definitions!$B$55) |
| B41 | IF(OR($D$37>1,$D$38>0),"Injections 'Factory Default' and 'Error Log Check' were not performed at last.","") |
| B42 | IF(OR($D$37>1,$D$38>0),"Repeat injections to ensure clearing of error log and setting of factory defaults!","") |
| B43 | IF(OR($D$37>1,$D$38>0),"Maybe a repeated injection was also not set to type 'matrix' in sequence table!","") |

## FormulaOne Sheet: Liquid Leak Test

| Cell | Formula |
|---|---|
| A5 | Definitions!$A$2 |
| B14 | Definitions!$B$15 |
| C14 | Definitions!$C$15 |
| D14 | Definitions!$D$15 |
| B15 | Definitions!$B$16 |
| C15 | Definitions!$C$16 |
| D15 | Definitions!$D$16 |
| B16 | Definitions!$B$17 |
| C16 | Definitions!$C$17 |
| D16 | Definitions!$D$17 |
| B17 | Definitions!$B$7 |
| C17 | Definitions!$D$7 |
| D17 | Definitions!$C$8 |
| B21 | Definitions!$B$10 |
| C21 | Definitions!$C$10 |
| B22 | Definitions!$B$11 |
| C22 | Definitions!$C$11 |
| C26 | Definitions!$B$53 |
| C27 | IF(AND(N47=Definitions!B61,J53=Definitions!B61),Definitions!$B$54,IF(AND(N47=Definitions!B74,J53=Definitions!B61),Definitions!B74,Definitions!$B$55)) |
| L46 | Definitions!B51 |
| L47 | Definitions!$C$37 |
| N47 | IF(AND(ABS(K47)<=Definitions!$E$37,M47="Leak"),Definitions!B61,IF(AND(ABS(K47)<=L47,M47="LEAK"),Definitions!$B$74,Definitions!$B$62)) |
| J53 | Audit Trail!J6 |

## FormulaOne Sheet: PCC

| Cell | Formula |
|---|---|
| A5 | Definitions!$A$2 |
| B14 | Definitions!$B$15 |
| C14 | Definitions!$C$15 |
| D14 | Definitions!$D$15 |
| B15 | Definitions!$B$16 |
| C15 | Definitions!$C$16 |
| D15 | Definitions!$D$16 |
| B16 | Definitions!$B$17 |
| C16 | Definitions!$C$17 |
| D16 | Definitions!$D$17 |
| B17 | Definitions!$B$7 |
| C17 | Definitions!$D$7 |
| D17 | Definitions!$C$8 |
| B19 | Definitions!$B$10 |
| C19 | Definitions!$C$10 |
| B20 | Definitions!$B$11 |
| C20 | Definitions!$C$11 |
| C25 | Definitions!$B$51 |
| D25 | Definitions!B70 |
| E25 | Definitions!$B$53 |
| B26 | Definitions!B69 |
| C26 | Definitions!C30 |
| D26 | E65 |
| E26 | IF(Definitions!C15="VC-C10-A",Definitions!B75,IF(L118=Definitions!$B61,Definitions!$B54,Definitions!$B55)) |
| B28 | IF(AND((COUNTIF(L115:L116,Definitions!$B$62)>=1),Definitions!C15="VH-C10-A"),"Result Internal Test:","") |
| D28 | IF(AND((COUNTIF(L115:L116,Definitions!$B$62)>=1),Definitions!C15="VH-C10-A"),Definitions!$B$55,"") |
| B65 | CONCATENATE(K110," °C to ",K111," °C") |
| C65 | ROUND(K105,2) |
| D65 | ROUND(L105,2) |
| E65 | D65-C65 |
| D66 | Definitions!$B$51 |
| E66 | Definitions!C30 |
| D67 | Definitions!$B$53 |
| E67 | IF($E$65<$E$66,Definitions!$B$61,Definitions!$B$62) |
| M89 | ROUND(L89,2)-(ROUND(K89,2)) |
| N89 | IF(ABS($M89)<=$M$92,Definitions!$B61,Definitions!$B62) |
| M90 | ROUND(L90,2)-(ROUND(K90,2)) |
| N90 | IF(ABS($M90)<=$M$92,Definitions!$B61,Definitions!$B62) |
| M91 | ROUND(L91,2)-(ROUND(K91,2)) |
| N91 | IF(ABS($M91)<=$M$92,Definitions!$B61,Definitions!$B62) |
| J92 | Definitions!B51 |
| M92 | Definitions!C28 |
| N92 | IF(COUNTIF(N89:N91,Definitions!$B61)<3,Definitions!$B62,Definitions!$B61) |
| L97 | IF(ABS($K97)<=$K98,Definitions!$B61,Definitions!$B62) |
| J98 | Definitions!B51 |
| K98 | Definitions!C29 |
| J105 | CONCATENATE(K110," °C to ",K111," °C") |
| K110 | ROUND(L110,0) |
| K111 | ROUND(L111,0) |
| J115 | J85 |
| L115 | N92 |
| J116 | J94 |
| L116 | L97 |
| J117 | J101 |
| L117 | E67 |
| L118 | IF(COUNTIF(L115:L117,Definitions!$B61)<3,Definitions!$B62,Definitions!$B61) |

## FormulaOne Sheet: Preheater Ports_Noise

| Cell | Formula |
|---|---|
| A5 | Definitions!$A$2 |
| B14 | Definitions!$B$15 |
| C14 | Definitions!$C$15 |
| D14 | Definitions!$D$15 |
| B15 | Definitions!$B$16 |
| C15 | Definitions!$C$16 |
| D15 | Definitions!$D$16 |
| B16 | Definitions!$B$17 |
| C16 | Definitions!$C$17 |
| D16 | Definitions!$D$17 |
| B17 | Definitions!$B$7 |
| C17 | Definitions!$D$7 |
| D17 | Definitions!$C$8 |
| B19 | Definitions!$B$10 |
| C19 | Definitions!$C$10 |
| B20 | Definitions!$B$11 |
| C20 | Definitions!$C$11 |
| C25 | Definitions!$B$53 |
| C26 | IF(AND(M72=Definitions!B61,M82=Definitions!B61,L92=Definitions!B61,L117=Definitions!B61),Definitions!$B$54,Definitions!$B$55) |
| C27 | IF(AND(M73=Definitions!B61,M83=Definitions!B61,L93=Definitions!B61,L118=Definitions!B61),Definitions!$B$54,Definitions!$B$55) |
| L72 | K72-J72 |
| M72 | IF((L72<=$L$74),Definitions!$B$61,Definitions!$B$62) |
| L73 | K73-J73 |
| M73 | IF((L73<=$L$74),Definitions!$B$61,Definitions!$B$62) |
| K74 | Definitions!$B$51 |
| L74 | Definitions!$C$32 |
| L82 | ROUND(K82-J82,1) |
| M82 | IF((ABS(L82))<=$L$84,Definitions!$B$61,Definitions!$B$62) |
| L83 | ROUND(K83-J83,1) |
| M83 | IF((ABS(L83))<=$L$84,Definitions!$B$61,Definitions!$B$62) |
| K84 | Definitions!$B$51 |
| L84 | Definitions!$C33 |
| L92 | IF(J92<=$L$94,Definitions!$B$61,Definitions!$B$62) |
| M92 | IF(K92<=$L$94,Definitions!$B$61,Definitions!$B$62) |
| L93 | IF(J93<=$L$94,Definitions!$B$61,Definitions!$B$62) |
| M93 | IF(K93<=$L$94,Definitions!$B$61,Definitions!$B$62) |
| K94 | Definitions!$B$51 |
| L94 | Definitions!D36 |
| L102 | K102-J102 |
| M102 | IF(L102<=$L$104,Definitions!$B$61,Definitions!$B$62) |
| L103 | K103-J103 |
| M103 | IF(L103<=$L$104,Definitions!$B$61,Definitions!$B$62) |
| K104 | Definitions!$B$51 |
| L104 | Definitions!D34 |
| L110 | K110-J110 |
| M110 | IF(L110<$L$112,Definitions!$B$61,Definitions!$B$62) |
| L111 | K111-J111 |
| M111 | IF(L111<$L$112,Definitions!$B$61,Definitions!$B$62) |
| K112 | Definitions!$B$51 |
| L112 | Definitions!D34 |
| L117 | IF(AND(J117="Yes",K117=Definitions!B61),Definitions!B61,Definitions!B62) |
| L118 | IF(AND(J118="Yes",K118=Definitions!B61),Definitions!B61,Definitions!B62) |
| L119 | IF(AND(L117=Definitions!B61,L118=Definitions!B61),Definitions!B61,Definitions!B62) |

## FormulaOne Sheet: Temp Accuracy

| Cell | Formula |
|---|---|
| A5 | Definitions!$A$2 |
| B14 | Definitions!$B$15 |
| C14 | Definitions!$C$15 |
| D14 | Definitions!$D$15 |
| B15 | Definitions!$B$16 |
| C15 | Definitions!$C$16 |
| D15 | Definitions!$D$16 |
| B16 | Definitions!$B$17 |
| C16 | Definitions!$C$17 |
| D16 | Definitions!$D$17 |
| B17 | Definitions!$B$7 |
| C17 | Definitions!$D$7 |
| D17 | Definitions!$C$8 |
| B19 | Definitions!$B$10 |
| C19 | Definitions!$C$10 |
| B20 | Definitions!$B$11 |
| C20 | Definitions!$C$11 |
| C25 | Definitions!$B$51 |
| D25 | Definitions!$B$52 |
| E25 | Definitions!$B$53 |
| B26 | Definitions!$B$24 |
| C26 | Definitions!C24 |
| D26 | D71 |
| E26 | IF(AND(E71=Definitions!$B$61,$B$75=""),Definitions!$B$54,IF(E71=Definitions!$B$63,CONCATENATE(Definitions!$B$54,"      (see comment)"),Definitions!$B$55)) |
| B29 | B74 |
| B30 | B75 |
| B31 | B76 |
| B32 | B77 |
| D45 | CONCATENATE(Definitions!$B$60,":") |
| J56 | IF(D66="n.a.",0.001,D66) |
| B66 | ROUND($J$66,2) |
| C66 | $N$66 |
| D66 | IF($C$66="n.a.","n.a.",C66-B66) |
| E66 | IF($D$66="n.a.",Definitions!$B$63,IF(ABS($D$66)<=$D$72,Definitions!$B$61,Definitions!$B$62)) |
| J66 | IF($I$66=$I$67,10,$I$66) |
| N66 | IF(L66="n.a.","n.a.",IF(ABS(L66-J66)>ABS(M66-J66),L66,M66)) |
| B67 | ROUND($J$67,2) |
| C67 | ROUND($N$67,2) |
| D67 | C67-B67 |
| E67 | IF(ABS($D$67)<=$D$72,Definitions!$B$61,Definitions!$B$62) |
| J67 | $I$67 |
| N67 | IF(ABS(L67-J67)>ABS(M67-J67),L67,M67) |
| B68 | ROUND($J$68,2) |
| C68 | ROUND($N$68,2) |
| D68 | C68-B68 |
| E68 | IF(ABS($D$68)<=$D$72,Definitions!$B$61,Definitions!$B$62) |
| J68 | $I$68 |
| N68 | IF(ABS(L68-J68)>ABS(M68-J68),L68,M68) |
| B69 | ROUND($J$69,2) |
| C69 | ROUND($N$69,2) |
| D69 | C69-B69 |
| E69 | IF(ABS($D$69)<=$D$72,Definitions!$B$61,Definitions!$B$62) |
| J69 | $I$69 |
| N69 | IF(ABS(L69-J69)>ABS(M69-J69),L69,M69) |
| B70 | ROUND($J$70,2) |
| C70 | ROUND($N$70,2) |
| D70 | C70-B70 |
| E70 | IF(ABS($D$70)<=$D$72,Definitions!$B$61,Definitions!$B$62) |
| J70 | $I$70 |
| N70 | IF(ABS(L70-J70)>ABS(M70-J70),L70,M70) |
| C71 | Definitions!B52 |
| D71 | IF(ABS(MAX(D66:D70))>ABS(MIN(D66:D70)),MAX(D66:D70),MIN(D66:D70)) |
| E71 | IF(OR(Definitions!C15="VH-C10-A",Definitions!C15="VC-C10-A"),$L$74,Definitions!B62) |
| C72 | Definitions!B51 |
| D72 | Definitions!C24 |
| B74 | IF(E71=Definitions!B63,"Comment:","") |
| L74 | IF(COUNTIF(E66:E70,Definitions!B61)=5,Definitions!B61,IF(AND(COUNTIF(E67:E70,Definitions!B61)=4,E66=Definitions!$B$63,E45>28.49),Definitions!B63,Definitions!B62)) |
| B75 | IF(E71=Definitions!B63,"The ambient temperature during the test was more than 18°C above the setpoint of 10°C and thus,","") |
| B76 | IF(E71=Definitions!B63,"the determination of the temperature accuracy at 10°C is skipped.","") |
| B77 | IF(E71=Definitions!B63,"Therefore, the test is nevertheless passed.","") |

## FormulaOne Sheet: Temp Precision

| Cell | Formula |
|---|---|
| A5 | Definitions!$A$2 |
| B14 | Definitions!$B$15 |
| C14 | Definitions!$C$15 |
| D14 | Definitions!$D$15 |
| B15 | Definitions!$B$16 |
| C15 | Definitions!$C$16 |
| D15 | Definitions!$D$16 |
| B16 | Definitions!$B$17 |
| C16 | Definitions!$C$17 |
| D16 | Definitions!$D$17 |
| B17 | Definitions!$B$7 |
| C17 | Definitions!$D$7 |
| D17 | Definitions!$C$8 |
| B19 | Definitions!$B$10 |
| C19 | Definitions!$C$10 |
| B20 | Definitions!$B$11 |
| C20 | Definitions!$C$11 |
| C25 | Definitions!$B$51 |
| D25 | Definitions!B52 |
| E25 | Definitions!$B$53 |
| B26 | Definitions!B26 |
| C26 | Definitions!$C26 |
| D26 | C68 |
| E26 | IF(C70=Definitions!$B$61,Definitions!$B$54,Definitions!$B$55) |
| B65 | I65 |
| C65 | ROUND(M65,2) |
| M65 | IF($K$68>$L$68,K65,L65) |
| B66 | I66 |
| C66 | ROUND(M66,2) |
| M66 | IF($K$68>$L$68,K66,L66) |
| B67 | I67 |
| C67 | ROUND(M67,2) |
| M67 | IF($K$68>$L$68,K67,L67) |
| B68 | Definitions!B52 |
| C68 | ROUND(MAX(C65:C67)-MIN(C65:C67),2) |
| K68 | (MAX(K65:K67)-MIN(K65:K67)) |
| L68 | (MAX(L65:L67)-MIN(L65:L67)) |
| B69 | Definitions!B51 |
| C69 | Definitions!$C26 |
| B70 | Definitions!B53 |
| C70 | IF(AND(C65>48,C66>48,C67>48,C68<=Definitions!D26),Definitions!$B$61,Definitions!$B$62) |
| C71 | IF(OR(C65<=48,C66<=48,C67<=48),"At least one observed temperature is below 48 °C!","") |

## FormulaOne Sheet: Temp Stability_Noise

| Cell | Formula |
|---|---|
| A5 | Definitions!$A$2 |
| B14 | Definitions!$B$15 |
| C14 | Definitions!$C$15 |
| D14 | Definitions!$D$15 |
| B15 | Definitions!$B$16 |
| C15 | Definitions!$C$16 |
| D15 | Definitions!$D$16 |
| B16 | Definitions!$B$17 |
| C16 | Definitions!$C$17 |
| D16 | Definitions!$D$17 |
| B17 | Definitions!$B$7 |
| C17 | Definitions!$D$7 |
| D17 | Definitions!$C$8 |
| B19 | Definitions!$B$10 |
| C19 | Definitions!$C$10 |
| B20 | Definitions!$B$11 |
| C20 | Definitions!$C$11 |
| C25 | Definitions!$B$51 |
| D25 | Definitions!B52 |
| E25 | Definitions!$B$53 |
| B26 | Definitions!B25 |
| C26 | Definitions!$C25 |
| D26 | C77-C76 |
| E26 | IF(Definitions!C15="VC-C10-A",IF(AND(C78="ok",L86="ok"),Definitions!$B$54,Definitions!$B$55),IF(AND(C78="ok",L86="ok",L87="ok"),Definitions!$B$54,Definitions!$B$55)) |
| B60 | Definitions!B65 |
| C60 | Definitions!B66 |
| C61 | IF($K$78>=$L$78,K61,L61) |
| U61 | ROUND(C61,2) |
| V61 | ROUND(AVERAGE($U$61:$U$75),3) |
| W61 | V61+$C$26 |
| X61 | V61-$C$26 |
| B62 | B61+1 |
| C62 | IF($K$78>=$L$78,K62,L62) |
| T62 | T61+1 |
| U62 | ROUND(C62,2) |
| V62 | ROUND(AVERAGE($U$61:$U$75),3) |
| W62 | V62+$C$26 |
| X62 | V62-$C$26 |
| B63 | B62+1 |
| C63 | IF($K$78>=$L$78,K63,L63) |
| T63 | T62+1 |
| U63 | ROUND(C63,2) |
| V63 | ROUND(AVERAGE($U$61:$U$75),3) |
| W63 | V63+$C$26 |
| X63 | V63-$C$26 |
| B64 | B63+1 |
| C64 | IF($K$78>=$L$78,K64,L64) |
| T64 | T63+1 |
| U64 | ROUND(C64,2) |
| V64 | ROUND(AVERAGE($U$61:$U$75),3) |
| W64 | V64+$C$26 |
| X64 | V64-$C$26 |
| B65 | B64+1 |
| C65 | IF($K$78>=$L$78,K65,L65) |
| T65 | T64+1 |
| U65 | ROUND(C65,2) |
| V65 | ROUND(AVERAGE($U$61:$U$75),3) |
| W65 | V65+$C$26 |
| X65 | V65-$C$26 |
| B66 | B65+1 |
| C66 | IF($K$78>=$L$78,K66,L66) |
| T66 | T65+1 |
| U66 | ROUND(C66,2) |
| V66 | ROUND(AVERAGE($U$61:$U$75),3) |
| W66 | V66+$C$26 |
| X66 | V66-$C$26 |
| B67 | B66+1 |
| C67 | IF($K$78>=$L$78,K67,L67) |
| T67 | T66+1 |
| U67 | ROUND(C67,2) |
| V67 | ROUND(AVERAGE($U$61:$U$75),3) |
| W67 | V67+$C$26 |
| X67 | V67-$C$26 |
| B68 | B67+1 |
| C68 | IF($K$78>=$L$78,K68,L68) |
| T68 | T67+1 |
| U68 | ROUND(C68,2) |
| V68 | ROUND(AVERAGE($U$61:$U$75),3) |
| W68 | V68+$C$26 |
| X68 | V68-$C$26 |
| B69 | B68+1 |
| C69 | IF($K$78>=$L$78,K69,L69) |
| T69 | T68+1 |
| U69 | ROUND(C69,2) |
| V69 | ROUND(AVERAGE($U$61:$U$75),3) |
| W69 | V69+$C$26 |
| X69 | V69-$C$26 |
| B70 | B69+1 |
| C70 | IF($K$78>=$L$78,K70,L70) |
| T70 | T69+1 |
| U70 | ROUND(C70,2) |
| V70 | ROUND(AVERAGE($U$61:$U$75),3) |
| W70 | V70+$C$26 |
| X70 | V70-$C$26 |
| B71 | B70+1 |
| C71 | IF($K$78>=$L$78,K71,L71) |
| T71 | T70+1 |
| U71 | ROUND(C71,2) |
| V71 | ROUND(AVERAGE($U$61:$U$75),3) |
| W71 | V71+$C$26 |
| X71 | V71-$C$26 |
| B72 | B71+1 |
| C72 | IF($K$78>=$L$78,K72,L72) |
| T72 | T71+1 |
| U72 | ROUND(C72,2) |
| V72 | ROUND(AVERAGE($U$61:$U$75),3) |
| W72 | V72+$C$26 |
| X72 | V72-$C$26 |
| B73 | B72+1 |
| C73 | IF($K$78>=$L$78,K73,L73) |
| T73 | T72+1 |
| U73 | ROUND(C73,2) |
| V73 | ROUND(AVERAGE($U$61:$U$75),3) |
| W73 | V73+$C$26 |
| X73 | V73-$C$26 |
| B74 | B73+1 |
| C74 | IF($K$78>=$L$78,K74,L74) |
| T74 | T73+1 |
| U74 | ROUND(C74,2) |
| V74 | ROUND(AVERAGE($U$61:$U$75),3) |
| W74 | V74+$C$26 |
| X74 | V74-$C$26 |
| B75 | B74+1 |
| C75 | IF($K$78>=$L$78,K75,L75) |
| T75 | T74+1 |
| U75 | ROUND(C75,2) |
| V75 | ROUND(AVERAGE($U$61:$U$75),3) |
| W75 | V75+$C$26 |
| X75 | V75-$C$26 |
| B76 | Definitions!$B$67 |
| C76 | ROUND(MIN(C61:C75),2) |
| J76 | Definitions!$B67 |
| K76 | ROUND(MIN(K61:K75),2) |
| L76 | ROUND(MIN(L61:L75),2) |
| B77 | Definitions!$B$68 |
| C77 | ROUND(MAX(C61:C75),2) |
| J77 | Definitions!$B68 |
| K77 | ROUND(MAX(K61:K75),2) |
| L77 | ROUND(MAX(L61:L75),2) |
| B78 | Definitions!B53 |
| C78 | IF(ABS(C76-C77)<=2*C26,Definitions!$B61,Definitions!$B62) |
| J78 | D25 |
| K78 | K77-K76 |
| L78 | L77-L76 |
| L86 | IF(K86<=$L$88,Definitions!$B61,Definitions!$B62) |
| L87 | IF(K87<=$L$88,Definitions!$B61,IF(Definitions!C15="VC-C10-A",Definitions!B75,Definitions!$B62)) |
| K88 | Definitions!$B51 |
| L88 | Definitions!$D35 |

## FormulaOne Sheet: Temp_Calib_Internal

| Cell | Formula |
|---|---|
| A5 | Definitions!$A$2 |
| B22 | IF(AND(J14="n.a.",C45>23),J18,J14) |
| C22 | IF(AND(J14="n.a.",C45>23),J18,J15) |
| D22 | IF(AND(J14="n.a.",C45>23),J18,J16) |
| E22 | IF(AND(J14="n.a.",C45>23),J18,J17) |
| F27 | IF(AND(ISNUMBER(B27),B27<>0),Definitions!$B$61,Definitions!$B$62) |
| F28 | IF(AND(ISNUMBER(B28),B28<>0),Definitions!$B$61,Definitions!$B$62) |
| F29 | IF(AND(ISNUMBER(B29),B29<>0),Definitions!$B$61,Definitions!$B$62) |
| F30 | IF(AND(ISNUMBER(B30),B30<>0),Definitions!$B$61,Definitions!$B$62) |
| K30 | IF(AND(D34=D32,D43=D41,B43=B34=5),"YES","NO") |
| F31 | IF(AND(ISNUMBER(B31),B31<>0),Definitions!$B$61,Definitions!$B$62) |
| F32 | IF(AND(ISNUMBER(B32),B32<>0),Definitions!$B$61,Definitions!$B$62) |
| F33 | IF(AND(ISNUMBER(B33),B33<>0),Definitions!$B$61,Definitions!$B$62) |
| F34 | IF(AND(ISNUMBER(B34),B34<>0),Definitions!$B$61,Definitions!$B$62) |
| F36 | IF(AND(ISNUMBER(B36),B36<>0),Definitions!$B$61,Definitions!$B$62) |
| F37 | IF(AND(ISNUMBER(B37),B37<>0),Definitions!$B$61,Definitions!$B$62) |
| F38 | IF(AND(ISNUMBER(B38),B38<>0),Definitions!$B$61,Definitions!$B$62) |
| F39 | IF(AND(ISNUMBER(B39),B39<>0),Definitions!$B$61,Definitions!$B$62) |
| F40 | IF(AND(ISNUMBER(B40),B40<>0),Definitions!$B$61,Definitions!$B$62) |
| F41 | IF(AND(ISNUMBER(B41),B41<>0),Definitions!$B$61,Definitions!$B$62) |
| F42 | IF(AND(ISNUMBER(B42),B42<>0),Definitions!$B$61,Definitions!$B$62) |
| F43 | IF(AND(ISNUMBER(B43),B43<>0),Definitions!$B$61,Definitions!$B$62) |
| F45 | IF(AND(K30="NO",OR(D34>0,D43>0)),K45-D34,K45) |
| F46 | IF(AND(K30="NO",OR(D34>0,D43>0)),K46-D43,K46) |
| B47 | IF(OR(AND(F45<5,F46<5),AND(C45-F45>18,C45-F46>18)),"","5°C or 18°C lower ambient were not reached! Peltier not working or not installed properly!") |
| E48 | IF(COUNTIF($F$27:$F$43,"ok")=16,IF(OR(AND(F45<5,F46<5),AND(C45-F45>18,C45-F46>18)),Definitions!$B$54,Definitions!$B$55),Definitions!$B$55) |

## FormulaOne Sheet: Test Procedures

| Cell | Formula |
|---|---|
| A5 | Definitions!$A$2 |
| A6 | Definitions!$A$3 |
| B10 | CONCATENATE("Five measuring points (",$J$10,") are used to check the temperature accuracy of the column compartment.") |
| J10 | IF(Definitions!$C$15="VH-C10-A",R10,IF(Definitions!$C$15="VC-C10-A",R11,n.a.)) |
| B20 | CONCATENATE("The column compartment is set to ",$J$21,". The temperature is measured with an external, calibrated thermometer. The signal is split") |
| J21 | IF(Definitions!$C$15="VH-C10-A",R20,IF(Definitions!$C$15="VC-C10-A",R21,n.a.)) |
| B30 | IF(Definitions!C15="VC-C10-A","","Post-Column Cooler Cool Down Time") |
| B31 | IF(Definitions!C15="VC-C10-A","","The post-column cooler (PCC) is set to T1 (T1=40°C). After 5 minutes, a different temperature T2 (T2=80°C) is set.") |
| B32 | IF(Definitions!C15="VC-C10-A","","After another 15 minutes, the first temperature T1 is set again. While the PCC cools down from 80°C to 40°C, the time required") |
| B33 | IF(Definitions!C15="VC-C10-A","","to cool from 50°C to 40°C is determined as cool down time.") |

## FormulaOne Sheet: Title

| Cell | Formula |
|---|---|
| A5 | Definitions!$A$2 |
| A6 | Definitions!$A$3 |
| B12 | Definitions!$B$15 |
| C12 | Definitions!$C$15 |
| D12 | Definitions!$D$15 |
| B13 | Definitions!$B$16 |
| C13 | Definitions!$C$16 |
| D13 | Definitions!$D$16 |
| B14 | Definitions!$B$17 |
| C14 | Definitions!$C$17 |
| D14 | Definitions!$D$17 |
| B15 | Definitions!$B$7 |
| C15 | Definitions!$D$7 |
| D15 | Definitions!$C$8 |
| B19 | Definitions!$B$10 |
| C19 | Definitions!$C$10 |
| C27 | IF(NOT(Definitions!C85=Definitions!B61),"Serial number of thermometer is missing!",IF(Test Procedures!J10="n.a.","Model of the VTCC is unknown! Do not ship!",IF(Fan!C26=Definitions!B55,"Fan test failed!",""))) |
| C28 | "Operator's signature "&"("&Definitions!$C$11&")" |

## FormulaOne Sheet: Valve_Keypad

| Cell | Formula |
|---|---|
| A5 | Definitions!$A$2 |
| B14 | Definitions!$B$15 |
| C14 | Definitions!$C$15 |
| D14 | Definitions!$D$15 |
| B15 | Definitions!$B$16 |
| C15 | Definitions!$C$16 |
| D15 | Definitions!$D$16 |
| B16 | Definitions!$B$17 |
| C16 | Definitions!$C$17 |
| D16 | Definitions!$D$17 |
| B17 | Definitions!$B$7 |
| C17 | Definitions!$D$7 |
| D17 | Definitions!$C$8 |
| B19 | Definitions!$B$10 |
| C19 | Definitions!$C$10 |
| B20 | Definitions!$B$11 |
| C20 | Definitions!$C$11 |
| C25 | Definitions!$B$53 |
| C26 | IF(O52=Definitions!$B$61,Definitions!$B$54,Definitions!$B$55) |
| C27 | IF(P52=Definitions!$B$61,Definitions!$B$54,Definitions!$B$55) |
| C28 | IF(P61=Definitions!$B$61,Definitions!$B$54,Definitions!$B$55) |
| M49 | IF(ABS(U49)<=Definitions!$D$31,U49,IF(ABS(W49)<=Definitions!$D$31,W49,IF(ABS(Y49)<=Definitions!$D$31,Y49,U49))) |
| N49 | IF(ABS(V49)<=Definitions!$D$31,V49,IF(ABS(X49)<=Definitions!$D$31,X49,IF(ABS(Z49)<=Definitions!$D$31,Z49,V49))) |
| O49 | IF(AND(ABS($M49)<=Definitions!$D$31,$J49=$K49),1,0) |
| P49 | IF(AND(ABS($N49)<=Definitions!$D$31,$J49=$L49),1,0) |
| W49 | U49+$W$44 |
| X49 | V49+$W$44 |
| Y49 | U49-$W$44 |
| Z49 | V49-$W$44 |
| M50 | IF(ABS(U50)<=Definitions!$D$31,U50,IF(ABS(W50)<=Definitions!$D$31,W50,IF(ABS(Y50)<=Definitions!$D$31,Y50,U50))) |
| N50 | IF(ABS(V50)<=Definitions!$D$31,V50,IF(ABS(X50)<=Definitions!$D$31,X50,IF(ABS(Z50)<=Definitions!$D$31,Z50,V50))) |
| O50 | IF(AND(ABS($M50)<=Definitions!$D$31,$J50=$K50),1,0) |
| P50 | IF(AND(ABS($N50)<=Definitions!$D$31,$J50=$L50),1,0) |
| W50 | U50+$W$44 |
| X50 | V50+$W$44 |
| Y50 | U50-$W$44 |
| Z50 | V50-$W$44 |
| M51 | IF(ABS(U51)<=Definitions!$D$31,U51,IF(ABS(W51)<=Definitions!$D$31,W51,IF(ABS(Y51)<=Definitions!$D$31,Y51,U51))) |
| N51 | IF(ABS(V51)<=Definitions!$D$31,V51,IF(ABS(X51)<=Definitions!$D$31,X51,IF(ABS(Z51)<=Definitions!$D$31,Z51,V51))) |
| O51 | IF(AND(ABS($M51)<=Definitions!$D$31,$J51=$K51),1,0) |
| P51 | IF(AND(ABS($N51)<=Definitions!$D$31,$J51=$L51),1,0) |
| W51 | U51+$W$44 |
| X51 | V51+$W$44 |
| Y51 | U51-$W$44 |
| Z51 | V51-$W$44 |
| O52 | IF(SUM(O49:O51)=3,Definitions!$B$61,Definitions!$B$62) |
| P52 | IF(SUM(P49:P51)=3,Definitions!$B$61,Definitions!$B$62) |
| O60 | IF($J60=$K60,1,0) |
| P60 | IF($J60=$L60,1,0) |
| Q60 | IF(AND(NOT($N60="n.a."),$M60<>$N60),1,0) |
| P61 | IF(SUM(O60:Q60)=3,Definitions!$B$61,Definitions!$B$62) |

---

## Evidence: VTCC_FORMULAONE

Source file: `REPORT_VTCC_V2_12_FORMULAONE_INVENTORY.md`

**Carrier:** `Report_VTCC_V2_12.cmbx`  
**Extraction:** FormulaOne x86 runtime, every cell from each sheet `LastRow` / `LastCol` boundary  
**Formula cells found:** 640 across 18 sheets  
**Cross-sheet-reference formulas found:** 390  

## Verification Scope

The matrix below was written into unused existing cells on the carrier `Internal Use` sheet, persisted with the V0.2 x86 STA writer, repacked into a standalone CMBX, and read back through the Chromeleon FormulaOne runtime. It verifies FormulaOne engine acceptance and calculated result for the function family, not every argument combination.

| Function | Used in VTCC cells | V0.2 write/read/repack |
|---|---:|---|
| `IF` | 166 | Verified |
| `ROUND` | 66 | Verified |
| `AND` | 47 | Verified |
| `ABS` | 31 | Verified |
| `ISNUMBER` | 17 | Verified |
| `INDIRECT` | 12 | Verified |
| `ADDRESS` | 12 | Verified |
| `AVERAGE` | 15 | Verified |
| `OR` | 12 | Verified |
| `ROW` | 11 | Verified |
| `MATCH` | 10 | Verified |
| `CONCATENATE` | 9 | Verified |
| `COUNTIF` | 8 | Verified |
| `MAX` | 7 | Verified |
| `MIN` | 7 | Verified |
| `SUM` | 5 | Verified |
| `ISNA` | 2 | Verified |
| `VALUE` | 2 | Verified |
| `NOT` | 2 | Verified |
| `LEFT` | 1 | Verified |
| `SEARCH` | 1 | Verified |
| `TIME` | 1 | Verified |
| `ISERROR` | 1 | Verified |
| `FIND` | 1 | Verified |

## FormulaOne Cell Formulas by Sheet

### Audit Trail

| Cell | FormulaOne formula source |
|---|---|
| `J6` | `IF(ISNUMBER(MATCH("*Alarm muted by key*",$C$14:$C$16,0)),Definitions!$B$61,Definitions!$B$62)` |

### COC

| Cell | FormulaOne formula source |
|---|---|
| `E16` | `Definitions!$B$15` |
| `E17` | `Definitions!$C$15` |
| `E18` | `Definitions!$D$15` |
| `E33` | `IF(Internal Use!D40="Test Passed","","Check Internal_Use page!!!")` |
| `B34` | `Definitions!C10` |

### Column ID

| Cell | FormulaOne formula source |
|---|---|
| `A5` | `Definitions!$A$2` |
| `B14` | `Definitions!$B$15` |
| `C14` | `Definitions!$C$15` |
| `D14` | `Definitions!$D$15` |
| `B15` | `Definitions!$B$16` |
| `C15` | `Definitions!$C$16` |
| `D15` | `Definitions!$D$16` |
| `B16` | `Definitions!$B$17` |
| `C16` | `Definitions!$C$17` |
| `D16` | `Definitions!$D$17` |
| `B17` | `Definitions!$B$7` |
| `C17` | `Definitions!$D$7` |
| `D17` | `Definitions!$C$8` |
| `B19` | `Definitions!$B$10` |
| `C19` | `Definitions!$C$10` |
| `B20` | `Definitions!$B$11` |
| `C20` | `Definitions!$C$11` |
| `C25` | `Definitions!$B$53` |
| `B26` | `J46` |
| `C26` | `IF($M46=1,Definitions!$B$54,Definitions!$B$55)` |
| `B27` | `J47` |
| `C27` | `IF($M47=1,Definitions!$B$54,Definitions!$B$55)` |
| `B28` | `J48` |
| `C28` | `IF($M48=1,Definitions!$B$54,Definitions!$B$55)` |
| `B29` | `J49` |
| `C29` | `IF($M49=1,Definitions!$B$54,Definitions!$B$55)` |
| `M46` | `IF($K46=$L46,1,0)` |
| `M47` | `IF($K47=$L47,1,0)` |
| `M48` | `IF($K48=$L48,1,0)` |
| `M49` | `IF($K49=$L49,1,0)` |

### Definitions

| Cell | FormulaOne formula source |
|---|---|
| `J5` | `C15` |
| `J6` | `INDIRECT(ADDRESS($J$1+ROW(),(11+MATCH($J$5,$L$5:$Q$5,0)),1))` |
| `D7` | `LEFT(C7,SEARCH("B",$C$7)-1)` |
| `J7` | `INDIRECT(ADDRESS($J$1+ROW(),(11+MATCH($J$5,$L$5:$Q$5,0)),1))` |
| `J8` | `INDIRECT(ADDRESS($J$1+ROW(),(11+MATCH($J$5,$L$5:$Q$5,0)),1))` |
| `J9` | `INDIRECT(ADDRESS($J$1+ROW(),(11+MATCH($J$5,$L$5:$Q$5,0)),1))` |
| `J10` | `INDIRECT(ADDRESS($J$1+ROW(),(11+MATCH($J$5,$L$5:$Q$5,0)),1))` |
| `D16` | `IF($C$83="non-Germering",$C$81,IF($C$83="Germering",$C$80,"#N/A"))` |
| `D17` | `IF($C$83="non-Germering",$C$88,IF($C$83="Germering",$C$87,"#N/A"))` |
| `D80` | `IF(C80="n.a.","-",IF(ISNA(MATCH(VALUE($C80),$B$93:$B$171,0)),$B$62,$B$61))` |
| `D81` | `IF(C81="n.a.","-",IF(ISNA(MATCH(VALUE($C81),$C$93:$C$300,0)),$B$62,$B$61))` |
| `C85` | `IF($C$83="Germering",IF($D80=$B$61,$B$61,$B$62),IF($C$83="non-Germering",IF($D81=$B$61,$B$61,$B$62),$B$62))` |

### Error Log

| Cell | FormulaOne formula source |
|---|---|
| `A5` | `Definitions!$A$2` |
| `E19` | `IF(ISERROR(FIND("No audit trail messages",INDIRECT(ADDRESS(13,4)))),Definitions!B62,Definitions!B61)` |

### Fan

| Cell | FormulaOne formula source |
|---|---|
| `A5` | `Definitions!$A$2` |
| `B14` | `Definitions!$B$15` |
| `C14` | `Definitions!$C$15` |
| `D14` | `Definitions!$D$15` |
| `B15` | `Definitions!$B$16` |
| `C15` | `Definitions!$C$16` |
| `D15` | `Definitions!$D$16` |
| `B16` | `Definitions!$B$17` |
| `C16` | `Definitions!$C$17` |
| `D16` | `Definitions!$D$17` |
| `B17` | `Definitions!$B$7` |
| `C17` | `Definitions!$D$7` |
| `D17` | `Definitions!$C$8` |
| `B19` | `Definitions!$B$10` |
| `C19` | `Definitions!$C$10` |
| `B20` | `Definitions!$B$11` |
| `C20` | `Definitions!$C$11` |
| `C25` | `Definitions!$B$53` |
| `C26` | `K53` |
| `K47` | `Definitions!B53` |
| `K49` | `IF((X57-W57)<Definitions!$C$26/4,Definitions!$B$61,Definitions!$B$62)` |
| `K50` | `IF((J49-J50)>=Definitions!$C$26/2,Definitions!$B$61,Definitions!$B$62)` |
| `K51` | `IF((X58-W58)<Definitions!$C$26/4,Definitions!$B$61,Definitions!$B$62)` |
| `K52` | `IF((J52-J51)>=Definitions!$C$26/2,Definitions!$B$61,Definitions!$B$62)` |
| `J53` | `Definitions!$B$53` |
| `K53` | `IF(COUNTIF(K49:K52,Definitions!B61)=4,Definitions!B54,Definitions!B55)` |

### HeatUp&CoolDown

| Cell | FormulaOne formula source |
|---|---|
| `A5` | `Definitions!$A$2` |
| `B9` | `CONCATENATE(" •  Heat Up / Cool Down Time (",K57," °C to ",K58," °C to ",K57," °C)")` |
| `B14` | `Definitions!$B$15` |
| `C14` | `Definitions!$C$15` |
| `D14` | `Definitions!$D$15` |
| `B15` | `Definitions!$B$16` |
| `C15` | `Definitions!$C$16` |
| `D15` | `Definitions!$D$16` |
| `B16` | `Definitions!$B$17` |
| `C16` | `Definitions!$C$17` |
| `D16` | `Definitions!$D$17` |
| `B17` | `Definitions!$B$7` |
| `C17` | `Definitions!$D$7` |
| `D17` | `Definitions!$C$8` |
| `B19` | `Definitions!$B$10` |
| `C19` | `Definitions!$C$10` |
| `B20` | `Definitions!$B$11` |
| `C20` | `Definitions!$C$11` |
| `C25` | `Definitions!$B$51` |
| `D25` | `Definitions!B70` |
| `E25` | `Definitions!$B$53` |
| `B26` | `Definitions!$B$71` |
| `C26` | `Definitions!C27` |
| `D26` | `E65` |
| `E26` | `IF(ROUND(D26,1)<C26,Definitions!$B$54,Definitions!$B$55)` |
| `B27` | `Definitions!$B$69` |
| `C27` | `Definitions!C27` |
| `D27` | `E66` |
| `E27` | `IF(ROUND(D27,1)<C27,Definitions!$B$54,Definitions!$B$55)` |
| `K57` | `ROUND(L57,0)` |
| `K58` | `ROUND(L58,0)` |
| `B65` | `CONCATENATE(K57," °C to ",K58," °C")` |
| `C65` | `ROUND(J66,1)` |
| `D65` | `ROUND(K66-2,1)` |
| `E65` | `D65-C65` |
| `B66` | `CONCATENATE(K58," °C to ",K57," °C")` |
| `C66` | `ROUND(L66,1)` |
| `D66` | `ROUND(M66-2,1)` |
| `E66` | `D66-C66` |
| `D67` | `Definitions!B53` |
| `E67` | `IF(AND(E65<Definitions!C27,E66<Definitions!C27),Definitions!$B61,Definitions!$B62)` |

### Internal Use

| Cell | FormulaOne formula source |
|---|---|
| `A5` | `Definitions!$A$2` |
| `C9` | `Definitions!$J$6` |
| `F9` | `IF(C9=E9,Definitions!$B$61,Definitions!$B$62)` |
| `C10` | `Definitions!$D$15` |
| `E10` | `Definitions!$C$9` |
| `F10` | `IF(C10=E10,Definitions!$B$61,Definitions!$B$62)` |
| `C11` | `Definitions!$J$7` |
| `F11` | `IF(C11=E11,Definitions!$B$61,Definitions!$B$62)` |
| `C12` | `Definitions!$J$8` |
| `F12` | `IF(OR(E12=C12,E12="n.a."),Definitions!$B$61,Definitions!$B$62)` |
| `C13` | `Definitions!$J$9` |
| `F13` | `IF(OR(E13=C13,E13="n.a."),Definitions!$B$61,Definitions!$B$62)` |
| `C14` | `Definitions!$J$10` |
| `F14` | `IF(OR(E14=C14,E14="n.a."),Definitions!$B$61,Definitions!$B$62)` |
| `J33` | `IF(INDIRECT(ADDRESS(ROW(),4))>INDIRECT(ADDRESS(46,4)),1,0)` |
| `K33` | `IF(INDIRECT(ADDRESS(ROW(),4))>INDIRECT(ADDRESS(47,4)),1,0)` |
| `J34` | `IF(INDIRECT(ADDRESS(ROW(),4))>INDIRECT(ADDRESS(46,4)),1,0)` |
| `K34` | `IF(INDIRECT(ADDRESS(ROW(),4))>INDIRECT(ADDRESS(47,4)),1,0)` |
| `D35` | `INDIRECT(ADDRESS(ROW(D32)+MATCH("Factory Default",C33:C34,0),4))` |
| `D36` | `INDIRECT(ADDRESS(ROW(D32)+MATCH("Error Log Check",C33:C34,0),4))` |
| `D37` | `SUM($J$33:$J$34)` |
| `D38` | `SUM($K$33:$K$34)` |
| `D40` | `IF(AND(COUNTIF($F$9:$F$14,"ok")=6,$D$37=1,$D$38=0),Definitions!$B$54,Definitions!$B$55)` |
| `B41` | `IF(OR($D$37>1,$D$38>0),"Injections 'Factory Default' and 'Error Log Check' were not performed at last.","")` |
| `B42` | `IF(OR($D$37>1,$D$38>0),"Repeat injections to ensure clearing of error log and setting of factory defaults!","")` |
| `B43` | `IF(OR($D$37>1,$D$38>0),"Maybe a repeated injection was also not set to type 'matrix' in sequence table!","")` |

### Liquid Leak Test

| Cell | FormulaOne formula source |
|---|---|
| `A5` | `Definitions!$A$2` |
| `B14` | `Definitions!$B$15` |
| `C14` | `Definitions!$C$15` |
| `D14` | `Definitions!$D$15` |
| `B15` | `Definitions!$B$16` |
| `C15` | `Definitions!$C$16` |
| `D15` | `Definitions!$D$16` |
| `B16` | `Definitions!$B$17` |
| `C16` | `Definitions!$C$17` |
| `D16` | `Definitions!$D$17` |
| `B17` | `Definitions!$B$7` |
| `C17` | `Definitions!$D$7` |
| `D17` | `Definitions!$C$8` |
| `B21` | `Definitions!$B$10` |
| `C21` | `Definitions!$C$10` |
| `B22` | `Definitions!$B$11` |
| `C22` | `Definitions!$C$11` |
| `C26` | `Definitions!$B$53` |
| `C27` | `IF(AND(N47=Definitions!B61,J53=Definitions!B61),Definitions!$B$54,IF(AND(N47=Definitions!B74,J53=Definitions!B61),Definitions!B74,Definitions!$B$55))` |
| `L46` | `Definitions!B51` |
| `L47` | `Definitions!$C$37` |
| `N47` | `IF(AND(ABS(K47)<=Definitions!$E$37,M47="Leak"),Definitions!B61,IF(AND(ABS(K47)<=L47,M47="LEAK"),Definitions!$B$74,Definitions!$B$62))` |
| `J53` | `Audit Trail!J6` |

### PCC

| Cell | FormulaOne formula source |
|---|---|
| `A5` | `Definitions!$A$2` |
| `B14` | `Definitions!$B$15` |
| `C14` | `Definitions!$C$15` |
| `D14` | `Definitions!$D$15` |
| `B15` | `Definitions!$B$16` |
| `C15` | `Definitions!$C$16` |
| `D15` | `Definitions!$D$16` |
| `B16` | `Definitions!$B$17` |
| `C16` | `Definitions!$C$17` |
| `D16` | `Definitions!$D$17` |
| `B17` | `Definitions!$B$7` |
| `C17` | `Definitions!$D$7` |
| `D17` | `Definitions!$C$8` |
| `B19` | `Definitions!$B$10` |
| `C19` | `Definitions!$C$10` |
| `B20` | `Definitions!$B$11` |
| `C20` | `Definitions!$C$11` |
| `C25` | `Definitions!$B$51` |
| `D25` | `Definitions!B70` |
| `E25` | `Definitions!$B$53` |
| `B26` | `Definitions!B69` |
| `C26` | `Definitions!C30` |
| `D26` | `E65` |
| `E26` | `IF(Definitions!C15="VC-C10-A",Definitions!B75,IF(L118=Definitions!$B61,Definitions!$B54,Definitions!$B55))` |
| `B28` | `IF(AND((COUNTIF(L115:L116,Definitions!$B$62)>=1),Definitions!C15="VH-C10-A"),"Result Internal Test:","")` |
| `D28` | `IF(AND((COUNTIF(L115:L116,Definitions!$B$62)>=1),Definitions!C15="VH-C10-A"),Definitions!$B$55,"")` |
| `B65` | `CONCATENATE(K110," °C to ",K111," °C")` |
| `C65` | `ROUND(K105,2)` |
| `D65` | `ROUND(L105,2)` |
| `E65` | `D65-C65` |
| `D66` | `Definitions!$B$51` |
| `E66` | `Definitions!C30` |
| `D67` | `Definitions!$B$53` |
| `E67` | `IF($E$65<$E$66,Definitions!$B$61,Definitions!$B$62)` |
| `M89` | `ROUND(L89,2)-(ROUND(K89,2))` |
| `N89` | `IF(ABS($M89)<=$M$92,Definitions!$B61,Definitions!$B62)` |
| `M90` | `ROUND(L90,2)-(ROUND(K90,2))` |
| `N90` | `IF(ABS($M90)<=$M$92,Definitions!$B61,Definitions!$B62)` |
| `M91` | `ROUND(L91,2)-(ROUND(K91,2))` |
| `N91` | `IF(ABS($M91)<=$M$92,Definitions!$B61,Definitions!$B62)` |
| `J92` | `Definitions!B51` |
| `M92` | `Definitions!C28` |
| `N92` | `IF(COUNTIF(N89:N91,Definitions!$B61)<3,Definitions!$B62,Definitions!$B61)` |
| `L97` | `IF(ABS($K97)<=$K98,Definitions!$B61,Definitions!$B62)` |
| `J98` | `Definitions!B51` |
| `K98` | `Definitions!C29` |
| `J105` | `CONCATENATE(K110," °C to ",K111," °C")` |
| `K110` | `ROUND(L110,0)` |
| `K111` | `ROUND(L111,0)` |
| `J115` | `J85` |
| `L115` | `N92` |
| `J116` | `J94` |
| `L116` | `L97` |
| `J117` | `J101` |
| `L117` | `E67` |
| `L118` | `IF(COUNTIF(L115:L117,Definitions!$B61)<3,Definitions!$B62,Definitions!$B61)` |

### Preheater Ports_Noise

| Cell | FormulaOne formula source |
|---|---|
| `A5` | `Definitions!$A$2` |
| `B14` | `Definitions!$B$15` |
| `C14` | `Definitions!$C$15` |
| `D14` | `Definitions!$D$15` |
| `B15` | `Definitions!$B$16` |
| `C15` | `Definitions!$C$16` |
| `D15` | `Definitions!$D$16` |
| `B16` | `Definitions!$B$17` |
| `C16` | `Definitions!$C$17` |
| `D16` | `Definitions!$D$17` |
| `B17` | `Definitions!$B$7` |
| `C17` | `Definitions!$D$7` |
| `D17` | `Definitions!$C$8` |
| `B19` | `Definitions!$B$10` |
| `C19` | `Definitions!$C$10` |
| `B20` | `Definitions!$B$11` |
| `C20` | `Definitions!$C$11` |
| `C25` | `Definitions!$B$53` |
| `C26` | `IF(AND(M72=Definitions!B61,M82=Definitions!B61,L92=Definitions!B61,L117=Definitions!B61),Definitions!$B$54,Definitions!$B$55)` |
| `C27` | `IF(AND(M73=Definitions!B61,M83=Definitions!B61,L93=Definitions!B61,L118=Definitions!B61),Definitions!$B$54,Definitions!$B$55)` |
| `L72` | `K72-J72` |
| `M72` | `IF((L72<=$L$74),Definitions!$B$61,Definitions!$B$62)` |
| `L73` | `K73-J73` |
| `M73` | `IF((L73<=$L$74),Definitions!$B$61,Definitions!$B$62)` |
| `K74` | `Definitions!$B$51` |
| `L74` | `Definitions!$C$32` |
| `L82` | `ROUND(K82-J82,1)` |
| `M82` | `IF((ABS(L82))<=$L$84,Definitions!$B$61,Definitions!$B$62)` |
| `L83` | `ROUND(K83-J83,1)` |
| `M83` | `IF((ABS(L83))<=$L$84,Definitions!$B$61,Definitions!$B$62)` |
| `K84` | `Definitions!$B$51` |
| `L84` | `Definitions!$C33` |
| `L92` | `IF(J92<=$L$94,Definitions!$B$61,Definitions!$B$62)` |
| `M92` | `IF(K92<=$L$94,Definitions!$B$61,Definitions!$B$62)` |
| `L93` | `IF(J93<=$L$94,Definitions!$B$61,Definitions!$B$62)` |
| `M93` | `IF(K93<=$L$94,Definitions!$B$61,Definitions!$B$62)` |
| `K94` | `Definitions!$B$51` |
| `L94` | `Definitions!D36` |
| `L102` | `K102-J102` |
| `M102` | `IF(L102<=$L$104,Definitions!$B$61,Definitions!$B$62)` |
| `L103` | `K103-J103` |
| `M103` | `IF(L103<=$L$104,Definitions!$B$61,Definitions!$B$62)` |
| `K104` | `Definitions!$B$51` |
| `L104` | `Definitions!D34` |
| `L110` | `K110-J110` |
| `M110` | `IF(L110<$L$112,Definitions!$B$61,Definitions!$B$62)` |
| `L111` | `K111-J111` |
| `M111` | `IF(L111<$L$112,Definitions!$B$61,Definitions!$B$62)` |
| `K112` | `Definitions!$B$51` |
| `L112` | `Definitions!D34` |
| `L117` | `IF(AND(J117="Yes",K117=Definitions!B61),Definitions!B61,Definitions!B62)` |
| `L118` | `IF(AND(J118="Yes",K118=Definitions!B61),Definitions!B61,Definitions!B62)` |
| `L119` | `IF(AND(L117=Definitions!B61,L118=Definitions!B61),Definitions!B61,Definitions!B62)` |

### Temp Accuracy

| Cell | FormulaOne formula source |
|---|---|
| `A5` | `Definitions!$A$2` |
| `B14` | `Definitions!$B$15` |
| `C14` | `Definitions!$C$15` |
| `D14` | `Definitions!$D$15` |
| `B15` | `Definitions!$B$16` |
| `C15` | `Definitions!$C$16` |
| `D15` | `Definitions!$D$16` |
| `B16` | `Definitions!$B$17` |
| `C16` | `Definitions!$C$17` |
| `D16` | `Definitions!$D$17` |
| `B17` | `Definitions!$B$7` |
| `C17` | `Definitions!$D$7` |
| `D17` | `Definitions!$C$8` |
| `B19` | `Definitions!$B$10` |
| `C19` | `Definitions!$C$10` |
| `B20` | `Definitions!$B$11` |
| `C20` | `Definitions!$C$11` |
| `C25` | `Definitions!$B$51` |
| `D25` | `Definitions!$B$52` |
| `E25` | `Definitions!$B$53` |
| `B26` | `Definitions!$B$24` |
| `C26` | `Definitions!C24` |
| `D26` | `D71` |
| `E26` | `IF(AND(E71=Definitions!$B$61,$B$75=""),Definitions!$B$54,IF(E71=Definitions!$B$63,CONCATENATE(Definitions!$B$54,"      (see comment)"),Definitions!$B$55))` |
| `B29` | `B74` |
| `B30` | `B75` |
| `B31` | `B76` |
| `B32` | `B77` |
| `D45` | `CONCATENATE(Definitions!$B$60,":")` |
| `J56` | `IF(D66="n.a.",0.001,D66)` |
| `B66` | `ROUND($J$66,2)` |
| `C66` | `$N$66` |
| `D66` | `IF($C$66="n.a.","n.a.",C66-B66)` |
| `E66` | `IF($D$66="n.a.",Definitions!$B$63,IF(ABS($D$66)<=$D$72,Definitions!$B$61,Definitions!$B$62))` |
| `J66` | `IF($I$66=$I$67,10,$I$66)` |
| `N66` | `IF(L66="n.a.","n.a.",IF(ABS(L66-J66)>ABS(M66-J66),L66,M66))` |
| `B67` | `ROUND($J$67,2)` |
| `C67` | `ROUND($N$67,2)` |
| `D67` | `C67-B67` |
| `E67` | `IF(ABS($D$67)<=$D$72,Definitions!$B$61,Definitions!$B$62)` |
| `J67` | `$I$67` |
| `N67` | `IF(ABS(L67-J67)>ABS(M67-J67),L67,M67)` |
| `B68` | `ROUND($J$68,2)` |
| `C68` | `ROUND($N$68,2)` |
| `D68` | `C68-B68` |
| `E68` | `IF(ABS($D$68)<=$D$72,Definitions!$B$61,Definitions!$B$62)` |
| `J68` | `$I$68` |
| `N68` | `IF(ABS(L68-J68)>ABS(M68-J68),L68,M68)` |
| `B69` | `ROUND($J$69,2)` |
| `C69` | `ROUND($N$69,2)` |
| `D69` | `C69-B69` |
| `E69` | `IF(ABS($D$69)<=$D$72,Definitions!$B$61,Definitions!$B$62)` |
| `J69` | `$I$69` |
| `N69` | `IF(ABS(L69-J69)>ABS(M69-J69),L69,M69)` |
| `B70` | `ROUND($J$70,2)` |
| `C70` | `ROUND($N$70,2)` |
| `D70` | `C70-B70` |
| `E70` | `IF(ABS($D$70)<=$D$72,Definitions!$B$61,Definitions!$B$62)` |
| `J70` | `$I$70` |
| `N70` | `IF(ABS(L70-J70)>ABS(M70-J70),L70,M70)` |
| `C71` | `Definitions!B52` |
| `D71` | `IF(ABS(MAX(D66:D70))>ABS(MIN(D66:D70)),MAX(D66:D70),MIN(D66:D70))` |
| `E71` | `IF(OR(Definitions!C15="VH-C10-A",Definitions!C15="VC-C10-A"),$L$74,Definitions!B62)` |
| `C72` | `Definitions!B51` |
| `D72` | `Definitions!C24` |
| `B74` | `IF(E71=Definitions!B63,"Comment:","")` |
| `L74` | `IF(COUNTIF(E66:E70,Definitions!B61)=5,Definitions!B61,IF(AND(COUNTIF(E67:E70,Definitions!B61)=4,E66=Definitions!$B$63,E45>28.49),Definitions!B63,Definitions!B62))` |
| `B75` | `IF(E71=Definitions!B63,"The ambient temperature during the test was more than 18°C above the setpoint of 10°C and thus,","")` |
| `B76` | `IF(E71=Definitions!B63,"the determination of the temperature accuracy at 10°C is skipped.","")` |
| `B77` | `IF(E71=Definitions!B63,"Therefore, the test is nevertheless passed.","")` |

### Temp Precision

| Cell | FormulaOne formula source |
|---|---|
| `A5` | `Definitions!$A$2` |
| `B14` | `Definitions!$B$15` |
| `C14` | `Definitions!$C$15` |
| `D14` | `Definitions!$D$15` |
| `B15` | `Definitions!$B$16` |
| `C15` | `Definitions!$C$16` |
| `D15` | `Definitions!$D$16` |
| `B16` | `Definitions!$B$17` |
| `C16` | `Definitions!$C$17` |
| `D16` | `Definitions!$D$17` |
| `B17` | `Definitions!$B$7` |
| `C17` | `Definitions!$D$7` |
| `D17` | `Definitions!$C$8` |
| `B19` | `Definitions!$B$10` |
| `C19` | `Definitions!$C$10` |
| `B20` | `Definitions!$B$11` |
| `C20` | `Definitions!$C$11` |
| `C25` | `Definitions!$B$51` |
| `D25` | `Definitions!B52` |
| `E25` | `Definitions!$B$53` |
| `B26` | `Definitions!B26` |
| `C26` | `Definitions!$C26` |
| `D26` | `C68` |
| `E26` | `IF(C70=Definitions!$B$61,Definitions!$B$54,Definitions!$B$55)` |
| `B65` | `I65` |
| `C65` | `ROUND(M65,2)` |
| `M65` | `IF($K$68>$L$68,K65,L65)` |
| `B66` | `I66` |
| `C66` | `ROUND(M66,2)` |
| `M66` | `IF($K$68>$L$68,K66,L66)` |
| `B67` | `I67` |
| `C67` | `ROUND(M67,2)` |
| `M67` | `IF($K$68>$L$68,K67,L67)` |
| `B68` | `Definitions!B52` |
| `C68` | `ROUND(MAX(C65:C67)-MIN(C65:C67),2)` |
| `K68` | `(MAX(K65:K67)-MIN(K65:K67))` |
| `L68` | `(MAX(L65:L67)-MIN(L65:L67))` |
| `B69` | `Definitions!B51` |
| `C69` | `Definitions!$C26` |
| `B70` | `Definitions!B53` |
| `C70` | `IF(AND(C65>48,C66>48,C67>48,C68<=Definitions!D26),Definitions!$B$61,Definitions!$B$62)` |
| `C71` | `IF(OR(C65<=48,C66<=48,C67<=48),"At least one observed temperature is below 48 °C!","")` |

### Temp Stability_Noise

| Cell | FormulaOne formula source |
|---|---|
| `A5` | `Definitions!$A$2` |
| `B14` | `Definitions!$B$15` |
| `C14` | `Definitions!$C$15` |
| `D14` | `Definitions!$D$15` |
| `B15` | `Definitions!$B$16` |
| `C15` | `Definitions!$C$16` |
| `D15` | `Definitions!$D$16` |
| `B16` | `Definitions!$B$17` |
| `C16` | `Definitions!$C$17` |
| `D16` | `Definitions!$D$17` |
| `B17` | `Definitions!$B$7` |
| `C17` | `Definitions!$D$7` |
| `D17` | `Definitions!$C$8` |
| `B19` | `Definitions!$B$10` |
| `C19` | `Definitions!$C$10` |
| `B20` | `Definitions!$B$11` |
| `C20` | `Definitions!$C$11` |
| `C25` | `Definitions!$B$51` |
| `D25` | `Definitions!B52` |
| `E25` | `Definitions!$B$53` |
| `B26` | `Definitions!B25` |
| `C26` | `Definitions!$C25` |
| `D26` | `C77-C76` |
| `E26` | `IF(Definitions!C15="VC-C10-A",IF(AND(C78="ok",L86="ok"),Definitions!$B$54,Definitions!$B$55),IF(AND(C78="ok",L86="ok",L87="ok"),Definitions!$B$54,Definitions!$B$55))` |
| `B60` | `Definitions!B65` |
| `C60` | `Definitions!B66` |
| `C61` | `IF($K$78>=$L$78,K61,L61)` |
| `U61` | `ROUND(C61,2)` |
| `V61` | `ROUND(AVERAGE($U$61:$U$75),3)` |
| `W61` | `V61+$C$26` |
| `X61` | `V61-$C$26` |
| `B62` | `B61+1` |
| `C62` | `IF($K$78>=$L$78,K62,L62)` |
| `T62` | `T61+1` |
| `U62` | `ROUND(C62,2)` |
| `V62` | `ROUND(AVERAGE($U$61:$U$75),3)` |
| `W62` | `V62+$C$26` |
| `X62` | `V62-$C$26` |
| `B63` | `B62+1` |
| `C63` | `IF($K$78>=$L$78,K63,L63)` |
| `T63` | `T62+1` |
| `U63` | `ROUND(C63,2)` |
| `V63` | `ROUND(AVERAGE($U$61:$U$75),3)` |
| `W63` | `V63+$C$26` |
| `X63` | `V63-$C$26` |
| `B64` | `B63+1` |
| `C64` | `IF($K$78>=$L$78,K64,L64)` |
| `T64` | `T63+1` |
| `U64` | `ROUND(C64,2)` |
| `V64` | `ROUND(AVERAGE($U$61:$U$75),3)` |
| `W64` | `V64+$C$26` |
| `X64` | `V64-$C$26` |
| `B65` | `B64+1` |
| `C65` | `IF($K$78>=$L$78,K65,L65)` |
| `T65` | `T64+1` |
| `U65` | `ROUND(C65,2)` |
| `V65` | `ROUND(AVERAGE($U$61:$U$75),3)` |
| `W65` | `V65+$C$26` |
| `X65` | `V65-$C$26` |
| `B66` | `B65+1` |
| `C66` | `IF($K$78>=$L$78,K66,L66)` |
| `T66` | `T65+1` |
| `U66` | `ROUND(C66,2)` |
| `V66` | `ROUND(AVERAGE($U$61:$U$75),3)` |
| `W66` | `V66+$C$26` |
| `X66` | `V66-$C$26` |
| `B67` | `B66+1` |
| `C67` | `IF($K$78>=$L$78,K67,L67)` |
| `T67` | `T66+1` |
| `U67` | `ROUND(C67,2)` |
| `V67` | `ROUND(AVERAGE($U$61:$U$75),3)` |
| `W67` | `V67+$C$26` |
| `X67` | `V67-$C$26` |
| `B68` | `B67+1` |
| `C68` | `IF($K$78>=$L$78,K68,L68)` |
| `T68` | `T67+1` |
| `U68` | `ROUND(C68,2)` |
| `V68` | `ROUND(AVERAGE($U$61:$U$75),3)` |
| `W68` | `V68+$C$26` |
| `X68` | `V68-$C$26` |
| `B69` | `B68+1` |
| `C69` | `IF($K$78>=$L$78,K69,L69)` |
| `T69` | `T68+1` |
| `U69` | `ROUND(C69,2)` |
| `V69` | `ROUND(AVERAGE($U$61:$U$75),3)` |
| `W69` | `V69+$C$26` |
| `X69` | `V69-$C$26` |
| `B70` | `B69+1` |
| `C70` | `IF($K$78>=$L$78,K70,L70)` |
| `T70` | `T69+1` |
| `U70` | `ROUND(C70,2)` |
| `V70` | `ROUND(AVERAGE($U$61:$U$75),3)` |
| `W70` | `V70+$C$26` |
| `X70` | `V70-$C$26` |
| `B71` | `B70+1` |
| `C71` | `IF($K$78>=$L$78,K71,L71)` |
| `T71` | `T70+1` |
| `U71` | `ROUND(C71,2)` |
| `V71` | `ROUND(AVERAGE($U$61:$U$75),3)` |
| `W71` | `V71+$C$26` |
| `X71` | `V71-$C$26` |
| `B72` | `B71+1` |
| `C72` | `IF($K$78>=$L$78,K72,L72)` |
| `T72` | `T71+1` |
| `U72` | `ROUND(C72,2)` |
| `V72` | `ROUND(AVERAGE($U$61:$U$75),3)` |
| `W72` | `V72+$C$26` |
| `X72` | `V72-$C$26` |
| `B73` | `B72+1` |
| `C73` | `IF($K$78>=$L$78,K73,L73)` |
| `T73` | `T72+1` |
| `U73` | `ROUND(C73,2)` |
| `V73` | `ROUND(AVERAGE($U$61:$U$75),3)` |
| `W73` | `V73+$C$26` |
| `X73` | `V73-$C$26` |
| `B74` | `B73+1` |
| `C74` | `IF($K$78>=$L$78,K74,L74)` |
| `T74` | `T73+1` |
| `U74` | `ROUND(C74,2)` |
| `V74` | `ROUND(AVERAGE($U$61:$U$75),3)` |
| `W74` | `V74+$C$26` |
| `X74` | `V74-$C$26` |
| `B75` | `B74+1` |
| `C75` | `IF($K$78>=$L$78,K75,L75)` |
| `T75` | `T74+1` |
| `U75` | `ROUND(C75,2)` |
| `V75` | `ROUND(AVERAGE($U$61:$U$75),3)` |
| `W75` | `V75+$C$26` |
| `X75` | `V75-$C$26` |
| `B76` | `Definitions!$B$67` |
| `C76` | `ROUND(MIN(C61:C75),2)` |
| `J76` | `Definitions!$B67` |
| `K76` | `ROUND(MIN(K61:K75),2)` |
| `L76` | `ROUND(MIN(L61:L75),2)` |
| `B77` | `Definitions!$B$68` |
| `C77` | `ROUND(MAX(C61:C75),2)` |
| `J77` | `Definitions!$B68` |
| `K77` | `ROUND(MAX(K61:K75),2)` |
| `L77` | `ROUND(MAX(L61:L75),2)` |
| `B78` | `Definitions!B53` |
| `C78` | `IF(ABS(C76-C77)<=2*C26,Definitions!$B61,Definitions!$B62)` |
| `J78` | `D25` |
| `K78` | `K77-K76` |
| `L78` | `L77-L76` |
| `L86` | `IF(K86<=$L$88,Definitions!$B61,Definitions!$B62)` |
| `L87` | `IF(K87<=$L$88,Definitions!$B61,IF(Definitions!C15="VC-C10-A",Definitions!B75,Definitions!$B62))` |
| `K88` | `Definitions!$B51` |
| `L88` | `Definitions!$D35` |

### Temp_Calib_Internal

| Cell | FormulaOne formula source |
|---|---|
| `A5` | `Definitions!$A$2` |
| `B22` | `IF(AND(J14="n.a.",C45>23),J18,J14)` |
| `C22` | `IF(AND(J14="n.a.",C45>23),J18,J15)` |
| `D22` | `IF(AND(J14="n.a.",C45>23),J18,J16)` |
| `E22` | `IF(AND(J14="n.a.",C45>23),J18,J17)` |
| `F27` | `IF(AND(ISNUMBER(B27),B27<>0),Definitions!$B$61,Definitions!$B$62)` |
| `F28` | `IF(AND(ISNUMBER(B28),B28<>0),Definitions!$B$61,Definitions!$B$62)` |
| `F29` | `IF(AND(ISNUMBER(B29),B29<>0),Definitions!$B$61,Definitions!$B$62)` |
| `F30` | `IF(AND(ISNUMBER(B30),B30<>0),Definitions!$B$61,Definitions!$B$62)` |
| `K30` | `IF(AND(D34=D32,D43=D41,B43=B34=5),"YES","NO")` |
| `F31` | `IF(AND(ISNUMBER(B31),B31<>0),Definitions!$B$61,Definitions!$B$62)` |
| `F32` | `IF(AND(ISNUMBER(B32),B32<>0),Definitions!$B$61,Definitions!$B$62)` |
| `F33` | `IF(AND(ISNUMBER(B33),B33<>0),Definitions!$B$61,Definitions!$B$62)` |
| `F34` | `IF(AND(ISNUMBER(B34),B34<>0),Definitions!$B$61,Definitions!$B$62)` |
| `F36` | `IF(AND(ISNUMBER(B36),B36<>0),Definitions!$B$61,Definitions!$B$62)` |
| `F37` | `IF(AND(ISNUMBER(B37),B37<>0),Definitions!$B$61,Definitions!$B$62)` |
| `F38` | `IF(AND(ISNUMBER(B38),B38<>0),Definitions!$B$61,Definitions!$B$62)` |
| `F39` | `IF(AND(ISNUMBER(B39),B39<>0),Definitions!$B$61,Definitions!$B$62)` |
| `F40` | `IF(AND(ISNUMBER(B40),B40<>0),Definitions!$B$61,Definitions!$B$62)` |
| `F41` | `IF(AND(ISNUMBER(B41),B41<>0),Definitions!$B$61,Definitions!$B$62)` |
| `F42` | `IF(AND(ISNUMBER(B42),B42<>0),Definitions!$B$61,Definitions!$B$62)` |
| `F43` | `IF(AND(ISNUMBER(B43),B43<>0),Definitions!$B$61,Definitions!$B$62)` |
| `F45` | `IF(AND(K30="NO",OR(D34>0,D43>0)),K45-D34,K45)` |
| `F46` | `IF(AND(K30="NO",OR(D34>0,D43>0)),K46-D43,K46)` |
| `B47` | `IF(OR(AND(F45<5,F46<5),AND(C45-F45>18,C45-F46>18)),"","5°C or 18°C lower ambient were not reached! Peltier not working or not installed properly!")` |
| `E48` | `IF(COUNTIF($F$27:$F$43,"ok")=16,IF(OR(AND(F45<5,F46<5),AND(C45-F45>18,C45-F46>18)),Definitions!$B$54,Definitions!$B$55),Definitions!$B$55)` |

### Test Procedures

| Cell | FormulaOne formula source |
|---|---|
| `A5` | `Definitions!$A$2` |
| `A6` | `Definitions!$A$3` |
| `B10` | `CONCATENATE("Five measuring points (",$J$10,") are used to check the temperature accuracy of the column compartment.")` |
| `J10` | `IF(Definitions!$C$15="VH-C10-A",R10,IF(Definitions!$C$15="VC-C10-A",R11,n.a.))` |
| `B20` | `CONCATENATE("The column compartment is set to ",$J$21,". The temperature is measured with an external, calibrated thermometer. The signal is split")` |
| `J21` | `IF(Definitions!$C$15="VH-C10-A",R20,IF(Definitions!$C$15="VC-C10-A",R21,n.a.))` |
| `B30` | `IF(Definitions!C15="VC-C10-A","","Post-Column Cooler Cool Down Time")` |
| `B31` | `IF(Definitions!C15="VC-C10-A","","The post-column cooler (PCC) is set to T1 (T1=40°C). After 5 minutes, a different temperature T2 (T2=80°C) is set.")` |
| `B32` | `IF(Definitions!C15="VC-C10-A","","After another 15 minutes, the first temperature T1 is set again. While the PCC cools down from 80°C to 40°C, the time required")` |
| `B33` | `IF(Definitions!C15="VC-C10-A","","to cool from 50°C to 40°C is determined as cool down time.")` |

### Title

| Cell | FormulaOne formula source |
|---|---|
| `A5` | `Definitions!$A$2` |
| `A6` | `Definitions!$A$3` |
| `B12` | `Definitions!$B$15` |
| `C12` | `Definitions!$C$15` |
| `D12` | `Definitions!$D$15` |
| `B13` | `Definitions!$B$16` |
| `C13` | `Definitions!$C$16` |
| `D13` | `Definitions!$D$16` |
| `B14` | `Definitions!$B$17` |
| `C14` | `Definitions!$C$17` |
| `D14` | `Definitions!$D$17` |
| `B15` | `Definitions!$B$7` |
| `C15` | `Definitions!$D$7` |
| `D15` | `Definitions!$C$8` |
| `B19` | `Definitions!$B$10` |
| `C19` | `Definitions!$C$10` |
| `C27` | `IF(NOT(Definitions!C85=Definitions!B61),"Serial number of thermometer is missing!",IF(Test Procedures!J10="n.a.","Model of the VTCC is unknown! Do not ship!",IF(Fan!C26=Definitions!B55,"Fan test failed!","")))` |
| `C28` | `Operator's signature &"("&Definitions!$C$11&")"` |

### Valve_Keypad

| Cell | FormulaOne formula source |
|---|---|
| `A5` | `Definitions!$A$2` |
| `B14` | `Definitions!$B$15` |
| `C14` | `Definitions!$C$15` |
| `D14` | `Definitions!$D$15` |
| `B15` | `Definitions!$B$16` |
| `C15` | `Definitions!$C$16` |
| `D15` | `Definitions!$D$16` |
| `B16` | `Definitions!$B$17` |
| `C16` | `Definitions!$C$17` |
| `D16` | `Definitions!$D$17` |
| `B17` | `Definitions!$B$7` |
| `C17` | `Definitions!$D$7` |
| `D17` | `Definitions!$C$8` |
| `B19` | `Definitions!$B$10` |
| `C19` | `Definitions!$C$10` |
| `B20` | `Definitions!$B$11` |
| `C20` | `Definitions!$C$11` |
| `C25` | `Definitions!$B$53` |
| `C26` | `IF(O52=Definitions!$B$61,Definitions!$B$54,Definitions!$B$55)` |
| `C27` | `IF(P52=Definitions!$B$61,Definitions!$B$54,Definitions!$B$55)` |
| `C28` | `IF(P61=Definitions!$B$61,Definitions!$B$54,Definitions!$B$55)` |
| `M49` | `IF(ABS(U49)<=Definitions!$D$31,U49,IF(ABS(W49)<=Definitions!$D$31,W49,IF(ABS(Y49)<=Definitions!$D$31,Y49,U49)))` |
| `N49` | `IF(ABS(V49)<=Definitions!$D$31,V49,IF(ABS(X49)<=Definitions!$D$31,X49,IF(ABS(Z49)<=Definitions!$D$31,Z49,V49)))` |
| `O49` | `IF(AND(ABS($M49)<=Definitions!$D$31,$J49=$K49),1,0)` |
| `P49` | `IF(AND(ABS($N49)<=Definitions!$D$31,$J49=$L49),1,0)` |
| `W49` | `U49+$W$44` |
| `X49` | `V49+$W$44` |
| `Y49` | `U49-$W$44` |
| `Z49` | `V49-$W$44` |
| `M50` | `IF(ABS(U50)<=Definitions!$D$31,U50,IF(ABS(W50)<=Definitions!$D$31,W50,IF(ABS(Y50)<=Definitions!$D$31,Y50,U50)))` |
| `N50` | `IF(ABS(V50)<=Definitions!$D$31,V50,IF(ABS(X50)<=Definitions!$D$31,X50,IF(ABS(Z50)<=Definitions!$D$31,Z50,V50)))` |
| `O50` | `IF(AND(ABS($M50)<=Definitions!$D$31,$J50=$K50),1,0)` |
| `P50` | `IF(AND(ABS($N50)<=Definitions!$D$31,$J50=$L50),1,0)` |
| `W50` | `U50+$W$44` |
| `X50` | `V50+$W$44` |
| `Y50` | `U50-$W$44` |
| `Z50` | `V50-$W$44` |
| `M51` | `IF(ABS(U51)<=Definitions!$D$31,U51,IF(ABS(W51)<=Definitions!$D$31,W51,IF(ABS(Y51)<=Definitions!$D$31,Y51,U51)))` |
| `N51` | `IF(ABS(V51)<=Definitions!$D$31,V51,IF(ABS(X51)<=Definitions!$D$31,X51,IF(ABS(Z51)<=Definitions!$D$31,Z51,V51)))` |
| `O51` | `IF(AND(ABS($M51)<=Definitions!$D$31,$J51=$K51),1,0)` |
| `P51` | `IF(AND(ABS($N51)<=Definitions!$D$31,$J51=$L51),1,0)` |
| `W51` | `U51+$W$44` |
| `X51` | `V51+$W$44` |
| `Y51` | `U51-$W$44` |
| `Z51` | `V51-$W$44` |
| `O52` | `IF(SUM(O49:O51)=3,Definitions!$B$61,Definitions!$B$62)` |
| `P52` | `IF(SUM(P49:P51)=3,Definitions!$B$61,Definitions!$B$62)` |
| `O60` | `IF($J60=$K60,1,0)` |
| `P60` | `IF($J60=$L60,1,0)` |
| `Q60` | `IF(AND(NOT($N60="n.a."),$M60<>$N60),1,0)` |
| `P61` | `IF(SUM(O60:Q60)=3,Definitions!$B$61,Definitions!$B$62)` |

---

## Evidence: PRESSURE_EVALUATION

Source file: `PressureEvaluation_FORMULA_INVENTORY.md`

- **Source CMBX:** `PressureEvaluation.cmbx`
- **Extraction scope:** `SheetObject` direct CM formulas only.
- **Not included:** FormulaOne workbook formulas/layout stored in `SpreadSheetData`.
- **Authoring rule:** Retain the sheet/cell binding and fixed channel/component unless a configuration contract approves a change.

## Summary

- Sheets: 1
- Direct CM formula objects: 1
- Formula namespaces: `peak` (1)

## Web Authoring Context (Self-Contained)

This section is included so this inventory can be supplied directly to a web-based GPT. It does not require access to local Chromeleon Help files. The formula table below is the carrier-specific evidence; this section explains how to read and safely reuse that evidence.

### Two Calculation Layers

| Layer | Storage / syntax | Use it for | V0.1 standalone-CMBX rule |
|---|---|---|---|
| Direct CM report formula | `ReportFormulaObject` with CM expressions such as `chm.noise(...)`, `AUDIT.*`, `precond.*` | Pulling raw signal, audit, metadata, or peak data into an existing report cell | May replace an existing formula object only when sheet, cell/range and object type match the carrier |
| FormulaOne workbook formula | Embedded `SpreadSheetData`, Excel-like syntax such as `=MAX(...)` | Visible labels, layout, calculated summaries, pass/fail display and print structure | Preserve it. Record requested edits as `workbook_change_request`; do not write them as CM formulas |

Do not put an Excel formula beginning with `=` into a `ReportFormulaObject`. Do not assume every visible result cell appears in this inventory: workbook-derived cells are intentionally outside this direct-CM extraction scope.

### HPLC Report Signal Context

The channel names and audit paths observed in the table are carrier-specific configuration contracts, not generic aliases. Use the exact evidence rows below to decide which of these source categories apply:

| Observed item | Meaning for authoring | Required evidence before reuse |
|---|---|---|
| Raw channel, for example `UV_VIS_1` or `PumpPressureVirtual` | Detector, pump, virtual, or other acquired-signal context used by raw-statistic and peak formulas | The method/config must acquire or create that exact channel with compatible settings |
| Timed audit path, for example `AUDIT.UV.*` or `audit.ColumnComp.*` | Time-resolved settings/events, such as detector state, valve position, flow, or temperature | The selected injection audit must log the exact property path |
| Precondition path, for example `precond.UV.*` | Pre-run device identity/configuration | The device configuration must expose and log the property |
| `peak.*` / `chm.peak(...)` | Processed chromatographic peak/calibration result | A compatible processing method, channel and component must exist |

Time arguments in observed `chm.*` and timed `AUDIT.*` expressions are in minutes. Preserve all observed scale factors: for example `chm.noise(1,2)*1000` and `chm.drift(1,21)*60` are carrier-specific result contracts; do not remove or reinterpret multipliers without an acceptance/report-unit review.

### CM Formula Semantics Used by This Carrier

| Expression family | Meaning | Authoring constraint |
|---|---|---|
| `chm.noise(start,end)` | Signal noise over the stated raw-data time window | Bind the exact fixed channel. Preserve window boundaries and multiplier unless the test specification changes them deliberately |
| `chm.drift(start,end)` | Regression slope across the stated baseline window | Keep the signal channel and any unit conversion such as `*60` explicit |
| `chm.sig_value(stat,start,end)` / `chm.signalStatistic(...)` | Signal statistic over a window, commonly average/min/max | A raw signal channel and minute-based range are required |
| `chm.signalValue(time)` | Signal value at a specific minute | Requires a sampled signal at that point |
| `AUDIT.path(time,"forward"/"backward")` | Audit property selected at/after or at/before the requested minute | Retain the full observed device path unless its abbreviation is proven unambiguous |
| `precond.path` | Pre-run configuration/identity property | It does not read a raw chromatogram and cannot substitute for an audit event |
| `peak.*`, `chm.peak(...)` | Processed peak, calibration or component property | Require the matching processing method and component/channel binding |
| `seq.*`, `smp.*`, `injection.*`, `gen.*` | Sequence, sample, injection or software metadata | Use only fields observed in the selected carrier/config or explicitly verified |

### Direct Formula Object Contract

For every proposed direct-formula change, supply all of: exact existing sheet name, A1 cell/range from this inventory, `object_type: ReportFormulaObject`, CM formula text, `fixed_channel` when the source object uses a channel, `fixed_component` for component/peak context, and the required audit/channel/processing dependencies. If an object is absent from this inventory, it is not safe to invent in V0.1 clone-and-patch generation.

### HPLC Report Authoring Guardrails

1. Choose the data source first: raw VWD signal, detector audit setting, detector precondition, processed peak, or metadata.
2. Reuse the observed sheet/cell/object and fixed channel whenever it has the same semantic role.
3. A report formula can be syntactically valid but evaluate to `n.a.` when the instrument configuration, channel, audit path, wavelength, lamp configuration or processing component is absent.
4. Mark `OPEN VERIFICATION REQUIRED` rather than fabricating an unobserved channel, audit path, FormulaOne formula, acceptance criterion, display format or report-table schema.
5. Report tables (`ReportTableObject`) are structured, pipe-delimited definitions, not scalar cell formulas; preserve them unless a controlled CM before/after pair validates a table write rule.

## Sheet Applicability

| Sheet | Active | Each Injection | Query | Injection Variable | Query Values |
|---|---|---|---|---|---|
| Sheet2 | N | Y | N |  |  |

## Sheet: Sheet2

| Cell / Range | Object Type | Formula | Fixed Channel | Fixed Component |
|---|---|---|---|---|
| A1:H43 | ReportTableObject | peak.number \| "No. " \| chm.channel \| peak.retention_time("detected")*60 \| "Retention Time" \| "s" \| injection.name \| "PumpPressureVirtual" \| peak.name \| peak.start_time*60 \| "Peak Start " \| "s" \| injection.name \| "PumpPressureVirtual" \| peak.name \| (peak.retention_time("detected")-(peak.start_time))*60*1000 \| "Valve Switching Time" \| "ms" \| injection.name \| "PumpPressureVirtual" \| peak.name \| peak.height \| "PeakMaxPressureEnhancement" \| chm.signalUnit \| chm.channel \| audit.ColumnComp.UpperValve.CurrentPosition \| "UpperValvePosition" \| "" \| injection.name \| "PumpPressureVirtual" \| peak.name \| audit.ColumnComp.LowerValve.CurrentPosition \| "LowerValvePosition" \| "" \| "PumpPressureVirtual" \| audit.PumpModule.Pump.Flow.Nominal \| "Flow.Nominal" \| "ml/min" \| injection.name \| chm.channel \| peak.name |  |  |
