# Report_VTCC_V2_12 Direct CM Formula Inventory

- **Source CMBX:** `Report_VTCC_V2_12.cmbx`
- **Extraction scope:** `SheetObject` direct CM formulas only.
- **Not included:** FormulaOne workbook formulas/layout stored in `SpreadSheetData`.
- **Authoring rule:** Retain the sheet/cell binding and fixed channel/component unless a configuration contract approves a change.

## Summary

- Sheets: 19
- Direct CM formula objects: 234
- Formula namespaces: `audit` (95), `chm` (106), `gen` (1), `injection` (1), `precond` (14), `seq` (12), `smp` (5)

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
