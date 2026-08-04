# TCC Test Knowledge Nodes

This document renders the Test Knowledge Node contract used by the FOQ Knowledge Alignment workbench.
Each node connects FOQ intent to CMBX execution evidence, report/formula evidence, and DB output fields.

## Node Index

| Test ID | Test | Injection | Instrument Method | Processing Method | Report Sheets | Formula ID | DB Fields | Coverage |
|---|---|---|---|---|---|---|---|---|
| TCC_COL_01 | Column ID | ColumnIDs | ColumnID | CORRECT_STABILITY_INJ_INSERTION | Column ID | `FORMULA_TCC_COLUMN_ID_AUDIT_DESCRIPTION` | RES_ColumnID_A, RES_ColumnID_B, RES_ColumnID_C, RES_ColumnID_D | complete |
| TCC_PREHEATER_01 | Preheater Connection Test | Preheater Connection Test | PREHEATER | No_Integration | Preheater Ports_Noise | `FORMULA_TCC_PREHEATER_PORT_STATE_AND_DIFF` | Noise_PrehtLeft_Temp, Noise_PrehtRight_Temp, Diff_PhLeft_HtTmp, Diff_PhRight_HtTmp, RES_Preheater_Left_Port, RES_Preheater_Right_Port | partial |
| TCC_VALVE_01 | Valve / Keypad | Valve | VALVES | No_Integration | Valve_Keypad | `FORMULA_TCC_VALVEKEYPAD_OPEN` | (not mapped) | partial |
| TCC_BURNIN_01 | VTCC BurnIn | VTCC_BurnIn | BURNIN | NO_INTEGRATION | (not mapped) | `FORMULA_OPEN_VERIFICATION_REQUIRED` | (not mapped) | open verification |
| TCC_CAL_01 | Temperature Calibration | Temperature Calibration | TEMPERATURE_CALIBRATION | CORRECT_ACCURACY_INJ_INSERTION | Temp Calibration, Internal Use | `FORMULA_TCC_TEMPERATURECALIBRATION_OPEN` | TempCal120_U, TempCal120_L, TempCal100_U, TempCal100_L, TempCal80_U, TempCal80_L, TempCal60_U, TempCal60_L, TempCal40_U, TempCal40_L, TempCal20_U, TempCal20_L, TempCal10_U, TempCal10_L, TempCal5_U, TempCal5_L, TimeCal120, TimeCal100, TimeCal80, TimeCal60, TimeCal40, TimeCal20, TimeCal10, TimeCal05, Slope_Cal120_U, Slope_Cal100_U, Slope_Cal80_U, Slope_Cal60_U, Slope_Cal40_U, Slope_Cal20_U, Slope_Cal10_U, Slope_Cal05_U, Slope_Cal120_L, Slope_Cal100_L, Slope_Cal80_L, Slope_Cal60_L, Slope_Cal40_L, Slope_Cal20_L, Slope_Cal10_L, Slope_Cal05_L, TempCal85_U, TempCal85_L, TempCal70_U, TempCal70_L, TempCal55_U, TempCal55_L, TempCal30_U, TempCal30_L, TimeCal85, TimeCal70, TimeCal55, TimeCal30, Slope_Cal85_U, Slope_Cal70_U, Slope_Cal55_U, Slope_Cal30_U, Slope_Cal85_L, Slope_Cal70_L, Slope_Cal55_L, Slope_Cal30_L | partial |
| TCC_ACC_01 | Temperature Accuracy | Temperature Accuracy_H | TEMPERATURE_ACCURACY | ACCURACY_IRC_STOP_H | Temp Accuracy | `FORMULA_TCC_TEMP_ACCURACY_MAX_DEVIATION` | TempAcc10, TempAcc20, TempAcc40, TempAcc80, TempAcc120, RES_TempAccuracy, TempAcc60, TempAcc85 | partial |
| TCC_PRECISION_01 | Temperature Precision and Fan | Temperature Precision_and_Fan | TEMPERATURE_PRECISION_AND_FAN | CORRECT_STABILITY_INJ_INSERTION | Temp Precision, Fan | `FORMULA_TCC_TEMP_PRECISION_SEPARATE_SENSOR_RANGE` | TempPrecision, RES_TempPrecision | partial |
| TCC_STABILITY_PCC_01 | Temperature Stability and PCC | Temperature Stability_and_PCC_H | TEMPERATURE_STABILITY_AND_PCC_70_H | NO_INTEGRATION | Temp Stability_Noise, PCC | `FORMULA_TCC_TEMP_STABILITY_AND_PCC_COOLDOWN` | TempStability, Noise_CC_Temp, Noise_PCC_Temp, Performance_PCC, RES_TempStability, RES_PCC, PCC_Acc_40_Step1, PCC_Acc_80, PCC_Acc_40_Step2, PCC_Drift | complete |
| TCC_STABILITY_01 | Temperature Stability | Temperature Stability | TEMPERATURE_STABILITY | NO_INTEGRATION | Temp Stability_Noise | `FORMULA_TCC_TEMP_STABILITY_SEPARATE_SENSOR_RANGE` | TempStability, Noise_CC_Temp, RES_TempStability | partial |
| TCC_HEATCOOL_01 | HeatUp and CoolDown | HeatUp and CoolDownTime | TEMP_HEAT_UP_DOWN_20_50_20 | No_Integration | HeatUp&CoolDown | `FORMULA_TCC_HEATUP_COOLDOWN_RETTIME_DELTA_MINUS_HOLD` | HeatUp_Time_20to50, CoolDown_Time_50to20, RES_HeatUp, RES_CoolDown | partial |
| TCC_LEAK_01 | Liquid Leak / Keypad | LiquidLeaktest | LIQUID LEAK | No_Integration | Liquid Leak, Valve_Keypad | `FORMULA_TCC_LIQUIDLEAKKEYPAD_OPEN` | (not mapped) | partial |
| TCC_SERVICE_01 | Qualification Service Done | Qualification_Service_Done | Qualification_Service_Done | No_Integration | Internal Use | `FORMULA_TCC_QUALIFICATIONSERVICEDONE_OPEN` | (not mapped) | partial |
| TCC_FACTORY_01 | Factory Default | Factory Default | FACTORYDEFAULT | No_Integration | Definitions, Internal Use, Factory Default | `FORMULA_TCC_FACTORY_DEFAULT_METADATA` | TestDate, Serial, TimeBase, ModelNo, ModelVariant, HardwareVersion, Firmware, SubmitDate, RES_SN_Check | complete |
| TCC_ERRORLOG_01 | Error Log Check | Error Log Check | CHECKERRORLOG | No_Integration | Error Log, Internal Use | `FORMULA_TCC_ERRORLOGCHECK_OPEN` | (not mapped) | partial |

## Coverage Audit

| Test ID | Method | Processing | Report/Formula | DB | RetTimes | Channels | Audit/Metadata | Config | Overall | Gaps |
|---|---|---|---|---|---|---|---|---|---|---|
| TCC_COL_01 | bound to instrument method evidence | IRC/corrective binding documented | report sheet and formula family mapped | DB fields mapped with evidence | not required | not required | audit/property contract documented | configuration contract documented | closed | none |
| TCC_PREHEATER_01 | bound to instrument method evidence | bound | report sheet and formula family mapped | DB fields mapped with evidence | RetTime contract documented | channel contract documented | audit/property contract documented | configuration contract documented | open verification | Confirm exact channel names for VA/VC/VH variants from loaded CMBX evidence. |
| TCC_VALVE_01 | bound to instrument method evidence | bound | report bound; formula open | no DB contract expected | not required | not required | audit/property contract documented | configuration contract documented | open verification | Keypad-specific workbook/report trace still needs exact formula confirmation.; report/formula: report bound; formula open |
| TCC_BURNIN_01 | bound to instrument method evidence | bound | report bound; formula open | no DB contract expected | not required | channel contract documented | audit/property expected; evidence open | configuration contract documented | open verification | TD purpose and detailed command stages need method-script interpretation before generation.; report/formula: report bound; formula open; audit/property: audit/property expected; evidence open |
| TCC_CAL_01 | bound to instrument method evidence | IRC/corrective binding documented | report bound; formula open | DB fields mapped with evidence | RetTime contract documented | channel contract documented | audit/property contract documented | configuration contract documented | open verification | Need complete report formula trace for every TempCal DB field and display precision.; report/formula: report bound; formula open |
| TCC_ACC_01 | bound to instrument method evidence | IRC/corrective binding documented | report sheet and formula family mapped | DB fields mapped with evidence | RetTime contract documented | channel contract documented | audit/property contract documented | configuration contract documented | open verification | Confirm VA/VC/VH template-specific row coverage from loaded CMBX before generation. |
| TCC_PRECISION_01 | bound to instrument method evidence | IRC/corrective binding documented | report sheet and formula family mapped | DB fields mapped with evidence | RetTime contract documented | channel contract documented | audit/property contract documented | configuration contract documented | open verification | Fan report formula and DB field exact names need trace confirmation. |
| TCC_STABILITY_PCC_01 | bound to instrument method evidence | bound | report sheet and formula family mapped | DB fields mapped with evidence | RetTime contract documented | channel contract documented | audit/property contract documented | configuration contract documented | closed | none |
| TCC_STABILITY_01 | bound to instrument method evidence | bound | report sheet and formula family mapped | DB fields mapped with evidence | RetTime contract documented | channel contract documented | audit/property contract documented | configuration contract documented | open verification | Exact VC/VA injection and method names need loaded CMBX confirmation. |
| TCC_HEATCOOL_01 | bound to instrument method evidence | bound | report sheet and formula family mapped | DB fields mapped with evidence | RetTime contract documented | channel contract documented | not required | configuration contract documented | open verification | Keep row-65/row-66 workbook rule distinction visible until full FormulaOne parsing is complete. |
| TCC_LEAK_01 | bound to instrument method evidence | bound | report bound; formula open | no DB contract expected | not required | not required | audit/property contract documented | configuration contract documented | open verification | Need report formula and DB trace for leak sensor result.; report/formula: report bound; formula open |
| TCC_SERVICE_01 | bound to instrument method evidence | bound | report bound; formula open | no DB contract expected | not required | not required | audit/property contract documented | configuration contract documented | open verification | Need TD/service command meaning and report trace.; report/formula: report bound; formula open |
| TCC_FACTORY_01 | bound to instrument method evidence | bound | report sheet and formula family mapped | DB fields mapped with evidence | not required | not required | audit/property contract documented | configuration contract documented | closed | none |
| TCC_ERRORLOG_01 | bound to instrument method evidence | bound | report bound; formula open | no DB contract expected | not required | not required | audit/property contract documented | configuration contract documented | open verification | Need command semantics and report formula trace for pass/fail criteria.; report/formula: report bound; formula open |

## DB Mapping Audit

Mapping source: `C:\Users\xiaoshu.guan\OneDrive - Thermo Fisher Scientific\Documents\Trae Work Project\HPLC Analysis Tool Hub V1.0\foq\FOQResultLocations_V2.83.xls`

| Test ID | Device | Injection | Mapped Report File(s) | Expected DB Fields | Mapped DB Fields | Missing Expected | Extra Mapped | Status |
|---|---|---|---|---|---|---|---|---|
| TCC_COL_01 | VH-C10-A | ColumnIDs | ColumnIDs.XLS | RES_ColumnID_A, RES_ColumnID_B, RES_ColumnID_C, RES_ColumnID_D | RES_ColumnID_A, RES_ColumnID_B, RES_ColumnID_C, RES_ColumnID_D | (none) | (none) | closed |
| TCC_COL_01 | VC-C10-A | ColumnIDs | ColumnIDs.XLS | RES_ColumnID_A, RES_ColumnID_B, RES_ColumnID_C, RES_ColumnID_D | RES_ColumnID_A, RES_ColumnID_B, RES_ColumnID_C, RES_ColumnID_D | (none) | (none) | closed |
| TCC_PREHEATER_01 | VH-C10-A | Preheater Connection Test | Preheater Connection Test.XLS | Noise_PrehtLeft_Temp, Noise_PrehtRight_Temp, Diff_PhLeft_HtTmp, Diff_PhRight_HtTmp, RES_Preheater_Left_Port, RES_Preheater_Right_Port | Noise_PrehtLeft_Temp, Noise_PrehtRight_Temp, Diff_PhLeft_HtTmp, Diff_PhRight_HtTmp, RES_Preheater_Left_Port, RES_Preheater_Right_Port | (none) | (none) | closed |
| TCC_PREHEATER_01 | VC-C10-A | Preheater Connection Test | Preheater Connection Test.XLS | Noise_PrehtLeft_Temp, Noise_PrehtRight_Temp, Diff_PhLeft_HtTmp, Diff_PhRight_HtTmp, RES_Preheater_Left_Port, RES_Preheater_Right_Port | Noise_PrehtLeft_Temp, Noise_PrehtRight_Temp, Diff_PhLeft_HtTmp, Diff_PhRight_HtTmp, RES_Preheater_Left_Port, RES_Preheater_Right_Port | (none) | (none) | closed |
| TCC_VALVE_01 | VH-C10-A | Valve | (none) | (none) | (none) | (none) | (none) | no DB contract expected |
| TCC_VALVE_01 | VC-C10-A | Valve | (none) | (none) | (none) | (none) | (none) | no DB contract expected |
| TCC_VALVE_01 | VA-C10-A | Valve | (none) | (none) | (none) | (none) | (none) | no DB contract expected |
| TCC_BURNIN_01 | VH-C10-A | VTCC_BurnIn | (none) | (none) | (none) | (none) | (none) | no DB contract expected |
| TCC_BURNIN_01 | VC-C10-A | VTCC_BurnIn | (none) | (none) | (none) | (none) | (none) | no DB contract expected |
| TCC_BURNIN_01 | VA-C10-A | VTCC_BurnIn | (none) | (none) | (none) | (none) | (none) | no DB contract expected |
| TCC_CAL_01 | VH-C10-A | Temperature Calibration | Temperature Calibration.xls, Temperature Calibration.XLS | TempCal120_U, TempCal120_L, TempCal100_U, TempCal100_L, TempCal80_U, TempCal80_L, TempCal60_U, TempCal60_L, TempCal40_U, TempCal40_L, TempCal20_U, TempCal20_L, TempCal10_U, TempCal10_L, TempCal5_U, TempCal5_L, TimeCal120, TimeCal100, TimeCal80, TimeCal60, TimeCal40, TimeCal20, TimeCal10, TimeCal05, Slope_Cal120_U, Slope_Cal100_U, Slope_Cal80_U, Slope_Cal60_U, Slope_Cal40_U, Slope_Cal20_U, Slope_Cal10_U, Slope_Cal05_U, Slope_Cal120_L, Slope_Cal100_L, Slope_Cal80_L, Slope_Cal60_L, Slope_Cal40_L, Slope_Cal20_L, Slope_Cal10_L, Slope_Cal05_L | TempCal120_U, TempCal120_L, TempCal100_U, TempCal100_L, TempCal80_U, TempCal80_L, TempCal60_U, TempCal60_L, TempCal40_U, TempCal40_L, TempCal20_U, TempCal20_L, TempCal10_U, TempCal10_L, TempCal5_U, TempCal5_L, TimeCal120, TimeCal100, TimeCal80, TimeCal60, TimeCal40, TimeCal20, TimeCal10, TimeCal05, Slope_Cal120_U, Slope_Cal100_U, Slope_Cal80_U, Slope_Cal60_U, Slope_Cal40_U, Slope_Cal20_U, Slope_Cal10_U, Slope_Cal05_U, Slope_Cal120_L, Slope_Cal100_L, Slope_Cal80_L, Slope_Cal60_L, Slope_Cal40_L, Slope_Cal20_L, Slope_Cal10_L, Slope_Cal05_L | (none) | (none) | closed |
| TCC_CAL_01 | VC-C10-A | Temperature Calibration | Temperature Calibration.xls, Temperature Calibration.XLS | TempCal85_U, TempCal85_L, TempCal70_U, TempCal70_L, TempCal55_U, TempCal55_L, TempCal40_U, TempCal40_L, TempCal30_U, TempCal30_L, TempCal20_U, TempCal20_L, TempCal10_U, TempCal10_L, TempCal5_U, TempCal5_L, TimeCal85, TimeCal70, TimeCal55, TimeCal40, TimeCal30, TimeCal20, TimeCal10, TimeCal05, Slope_Cal85_U, Slope_Cal70_U, Slope_Cal55_U, Slope_Cal40_U, Slope_Cal30_U, Slope_Cal20_U, Slope_Cal10_U, Slope_Cal05_U, Slope_Cal85_L, Slope_Cal70_L, Slope_Cal55_L, Slope_Cal40_L, Slope_Cal30_L, Slope_Cal20_L, Slope_Cal10_L, Slope_Cal05_L | TempCal85_U, TempCal85_L, TempCal70_U, TempCal70_L, TempCal55_U, TempCal55_L, TempCal40_U, TempCal40_L, TempCal30_U, TempCal30_L, TempCal20_U, TempCal20_L, TempCal10_U, TempCal10_L, TempCal5_U, TempCal5_L, TimeCal85, TimeCal70, TimeCal55, TimeCal40, TimeCal30, TimeCal20, TimeCal10, TimeCal05, Slope_Cal85_U, Slope_Cal70_U, Slope_Cal55_U, Slope_Cal40_U, Slope_Cal30_U, Slope_Cal20_U, Slope_Cal10_U, Slope_Cal05_U, Slope_Cal85_L, Slope_Cal70_L, Slope_Cal55_L, Slope_Cal40_L, Slope_Cal30_L, Slope_Cal20_L, Slope_Cal10_L, Slope_Cal05_L | (none) | (none) | closed |
| TCC_CAL_01 | VA-C10-A | Temperature Calibration | Temperature Calibration.xls, Temperature Calibration.XLS | TempCal85_U, TempCal85_L, TempCal70_U, TempCal70_L, TempCal55_U, TempCal55_L, TempCal40_U, TempCal40_L, TempCal30_U, TempCal30_L, TempCal20_U, TempCal20_L, TempCal10_U, TempCal10_L, TempCal5_U, TempCal5_L, TimeCal85, TimeCal70, TimeCal55, TimeCal40, TimeCal30, TimeCal20, TimeCal10, TimeCal05, Slope_Cal85_U, Slope_Cal70_U, Slope_Cal55_U, Slope_Cal40_U, Slope_Cal30_U, Slope_Cal20_U, Slope_Cal10_U, Slope_Cal05_U, Slope_Cal85_L, Slope_Cal70_L, Slope_Cal55_L, Slope_Cal40_L, Slope_Cal30_L, Slope_Cal20_L, Slope_Cal10_L, Slope_Cal05_L | TempCal85_U, TempCal85_L, TempCal70_U, TempCal70_L, TempCal55_U, TempCal55_L, TempCal40_U, TempCal40_L, TempCal30_U, TempCal30_L, TempCal20_U, TempCal20_L, TempCal10_U, TempCal10_L, TempCal5_U, TempCal5_L, TimeCal85, TimeCal70, TimeCal55, TimeCal40, TimeCal30, TimeCal20, TimeCal10, TimeCal05, Slope_Cal85_U, Slope_Cal70_U, Slope_Cal55_U, Slope_Cal40_U, Slope_Cal30_U, Slope_Cal20_U, Slope_Cal10_U, Slope_Cal05_U, Slope_Cal85_L, Slope_Cal70_L, Slope_Cal55_L, Slope_Cal40_L, Slope_Cal30_L, Slope_Cal20_L, Slope_Cal10_L, Slope_Cal05_L | (none) | (none) | closed |
| TCC_ACC_01 | VH-C10-A | Temperature Accuracy_H | Temperature Accuracy_H.XLS | TempAcc10, TempAcc20, TempAcc40, TempAcc80, TempAcc120, RES_TempAccuracy | TempAcc10, TempAcc20, TempAcc40, TempAcc80, TempAcc120, RES_TempAccuracy | (none) | (none) | closed |
| TCC_ACC_01 | VC-C10-A | Temperature Accuracy_C | Temperature Accuracy_C.XLS | TempAcc10, TempAcc20, TempAcc40, TempAcc60, TempAcc85, RES_TempAccuracy | TempAcc10, TempAcc20, TempAcc40, TempAcc60, TempAcc85, RES_TempAccuracy | (none) | (none) | closed |
| TCC_ACC_01 | VA-C10-A | Temperature Accuracy_C | Temperature Accuracy_C.XLS | TempAcc10, TempAcc20, TempAcc40, TempAcc60, TempAcc85, RES_TempAccuracy | TempAcc10, TempAcc20, TempAcc40, TempAcc60, TempAcc85, RES_TempAccuracy | (none) | (none) | closed |
| TCC_PRECISION_01 | VH-C10-A | Temperature Precision_and_Fan | Temperature Precision_and_Fan.XLS | TempPrecision, RES_TempPrecision | TempPrecision, RES_TempPrecision | (none) | (none) | closed |
| TCC_PRECISION_01 | VC-C10-A | Temperature Precision_and_Fan | Temperature Precision_and_Fan.XLS | TempPrecision, RES_TempPrecision | TempPrecision, RES_TempPrecision | (none) | (none) | closed |
| TCC_PRECISION_01 | VA-C10-A | Temperature Precision | Temperature Precision_and_Fan.XLS | TempPrecision, RES_TempPrecision | TempPrecision, RES_TempPrecision | (none) | (none) | closed |
| TCC_STABILITY_PCC_01 | VH-C10-A | Temperature Stability_and_PCC_H | Temperature Stability_and_PCC_H.XLS | TempStability, Noise_CC_Temp, Noise_PCC_Temp, Performance_PCC, RES_TempStability, RES_PCC, PCC_Acc_40_Step1, PCC_Acc_80, PCC_Acc_40_Step2, PCC_Drift | TempStability, Noise_CC_Temp, Noise_PCC_Temp, Performance_PCC, RES_TempStability, RES_PCC, PCC_Acc_40_Step1, PCC_Acc_80, PCC_Acc_40_Step2, PCC_Drift | (none) | (none) | closed |
| TCC_STABILITY_01 | VC-C10-A | Temperature Stability_C | Temperature Stability_C.XLS | TempStability, Noise_CC_Temp, RES_TempStability | TempStability, Noise_CC_Temp, RES_TempStability | (none) | (none) | closed |
| TCC_STABILITY_01 | VA-C10-A | Temperature Stability_C | Temperature Stability_C.XLS | TempStability, Noise_CC_Temp, RES_TempStability | TempStability, Noise_CC_Temp, RES_TempStability | (none) | (none) | closed |
| TCC_HEATCOOL_01 | VH-C10-A | HeatUp and CoolDownTime | HeatUp and CoolDownTime.XLS | HeatUp_Time_20to50, CoolDown_Time_50to20, RES_HeatUp, RES_CoolDown | HeatUp_Time_20to50, CoolDown_Time_50to20, RES_HeatUp, RES_CoolDown | (none) | (none) | closed |
| TCC_HEATCOOL_01 | VC-C10-A | HeatUp and CoolDownTime | HeatUp and CoolDownTime.XLS | HeatUp_Time_20to50, CoolDown_Time_50to20, RES_HeatUp, RES_CoolDown | HeatUp_Time_20to50, CoolDown_Time_50to20, RES_HeatUp, RES_CoolDown | (none) | (none) | closed |
| TCC_HEATCOOL_01 | VA-C10-A | HeatUp and CoolDownTime | HeatUp and CoolDownTime.XLS | HeatUp_Time_20to50, CoolDown_Time_50to20, RES_HeatUp, RES_CoolDown | HeatUp_Time_20to50, CoolDown_Time_50to20, RES_HeatUp, RES_CoolDown | (none) | (none) | closed |
| TCC_LEAK_01 | VH-C10-A | LiquidLeaktest | (none) | (none) | (none) | (none) | (none) | no DB contract expected |
| TCC_LEAK_01 | VC-C10-A | LiquidLeaktest | (none) | (none) | (none) | (none) | (none) | no DB contract expected |
| TCC_LEAK_01 | VA-C10-A | LiquidLeaktest | (none) | (none) | (none) | (none) | (none) | no DB contract expected |
| TCC_SERVICE_01 | VH-C10-A | Qualification_Service_Done | (none) | (none) | (none) | (none) | (none) | no DB contract expected |
| TCC_SERVICE_01 | VC-C10-A | Qualification_Service_Done | (none) | (none) | (none) | (none) | (none) | no DB contract expected |
| TCC_SERVICE_01 | VA-C10-A | Qualification_Service_Done | (none) | (none) | (none) | (none) | (none) | no DB contract expected |
| TCC_FACTORY_01 | VH-C10-A | Factory Default | Factory Default.xls | TestDate, Serial, TimeBase, ModelNo, ModelVariant, HardwareVersion, Firmware, SubmitDate, RES_SN_Check | TestDate, Serial, TimeBase, ModelNo, ModelVariant, HardwareVersion, Firmware, SubmitDate, RES_SN_Check | (none) | (none) | closed |
| TCC_FACTORY_01 | VC-C10-A | Factory Default | Factory Default.xls | TestDate, Serial, TimeBase, ModelNo, ModelVariant, HardwareVersion, Firmware, SubmitDate, RES_SN_Check | TestDate, Serial, TimeBase, ModelNo, ModelVariant, HardwareVersion, Firmware, SubmitDate, RES_SN_Check | (none) | (none) | closed |
| TCC_FACTORY_01 | VA-C10-A | Factory Default | Factory Default.xls | TestDate, Serial, TimeBase, ModelNo, ModelVariant, HardwareVersion, Firmware, SubmitDate, RES_SN_Check | TestDate, Serial, TimeBase, ModelNo, ModelVariant, HardwareVersion, Firmware, SubmitDate, RES_SN_Check | (none) | (none) | closed |
| TCC_ERRORLOG_01 | VH-C10-A | Error Log Check | (none) | (none) | (none) | (none) | (none) | no DB contract expected |
| TCC_ERRORLOG_01 | VC-C10-A | Error Log Check | (none) | (none) | (none) | (none) | (none) | no DB contract expected |
| TCC_ERRORLOG_01 | VA-C10-A | Error Log Check | (none) | (none) | (none) | (none) | (none) | no DB contract expected |

## Node Contracts

### TCC_COL_01 - Column ID

- FOQ Section: TCC FOQ sequence row 01 / TD Column ID
- Injection: ColumnIDs
- Instrument Method: ColumnID
- Processing Method: CORRECT_STABILITY_INJ_INSERTION
- Report Template: Device-specific: Report_VTCC_V2_12 for VC/VH, Report_VATCC_V1_01 for VA
- Report Sheets: Column ID
- Formula ID: `FORMULA_TCC_COLUMN_ID_AUDIT_DESCRIPTION`
- DB Fields: RES_ColumnID_A, RES_ColumnID_B, RES_ColumnID_C, RES_ColumnID_D
- Model Applicability: VH-C10-A, VC-C10-A
- IRC Injected: Yes
- Coverage: complete

**Device Bindings**

| Device | Injection | Instrument Method | Processing Method | Report Template | Report Sheets | Report Files | DB Fields |
|---|---|---|---|---|---|---|---|
| VH-C10-A | ColumnIDs | ColumnID | CORRECT_STABILITY_INJ_INSERTION | Report_VTCC_V2_12 | Column ID | (follows injection) | RES_ColumnID_A, RES_ColumnID_B, RES_ColumnID_C, RES_ColumnID_D |
| VC-C10-A | ColumnIDs | ColumnID | CORRECT_ACCURACY_INJ_INSERTION | Report_VTCC_V2_12 | Column ID | (follows injection) | RES_ColumnID_A, RES_ColumnID_B, RES_ColumnID_C, RES_ColumnID_D |

**Purpose**

Verify that the four column ID channels/positions are recognized and reported as A/B/C/D.

**Acceptance Criteria**

- External: Column_A/B/C/D descriptions must match A/B/C/D.

**Method Command Contract**

Expected RetTimes:
- not recorded

Expected Channels:
- not recorded

Expected Audit / Metadata Properties:
- ColumnComp.Column_A.Description
- ColumnComp.Column_B.Description
- ColumnComp.Column_C.Description
- ColumnComp.Column_D.Description

Required Configuration:
- ColumnComp
- AUDIT.ColumnComp.ModelNo is the device source of truth
- Column ID option/configuration enabled

Method Evidence:
- CMBX sequence row should bind ColumnIDs -> ColumnID / CORRECT_STABILITY_INJ_INSERTION.

**Report / DB Contract**

Report Evidence:
- Report cells L46:L49 read AUDIT.Column_A/B/C/D.Description with suffix path matching.

DB Evidence:
- DB fields resolve from Column ID report cells and pass when A/B/C/D descriptions match.

**Open Gaps**

- not recorded

### TCC_PREHEATER_01 - Preheater Connection Test

- FOQ Section: TCC FOQ sequence row 02 / TD Preheater Connection Test
- Injection: Preheater Connection Test
- Instrument Method: PREHEATER
- Processing Method: No_Integration
- Report Template: Device-specific: Report_VTCC_V2_12 for VC/VH, Report_VATCC_V1_01 for VA
- Report Sheets: Preheater Ports_Noise
- Formula ID: `FORMULA_TCC_PREHEATER_PORT_STATE_AND_DIFF`
- DB Fields: Noise_PrehtLeft_Temp, Noise_PrehtRight_Temp, Diff_PhLeft_HtTmp, Diff_PhRight_HtTmp, RES_Preheater_Left_Port, RES_Preheater_Right_Port
- Model Applicability: VH-C10-A, VC-C10-A
- IRC Injected: No
- Coverage: partial

**Device Bindings**

| Device | Injection | Instrument Method | Processing Method | Report Template | Report Sheets | Report Files | DB Fields |
|---|---|---|---|---|---|---|---|
| VH-C10-A | Preheater Connection Test | PREHEATER | No_Integration | Report_VTCC_V2_12 | Preheater Ports_Noise | (follows injection) | Noise_PrehtLeft_Temp, Noise_PrehtRight_Temp, Diff_PhLeft_HtTmp, Diff_PhRight_HtTmp, RES_Preheater_Left_Port, RES_Preheater_Right_Port |
| VC-C10-A | Preheater Connection Test | PREHEATER | CORRECT_ACCURACY_INJ_INSERTION | Report_VTCC_V2_12 | Preheater Ports_Noise | (follows injection) | Noise_PrehtLeft_Temp, Noise_PrehtRight_Temp, Diff_PhLeft_HtTmp, Diff_PhRight_HtTmp, RES_Preheater_Left_Port, RES_Preheater_Right_Port |

**Purpose**

Check that left/right preheater connection ports are present, have valid memory state, and can generate expected heater/external temperature evidence.

**Acceptance Criteria**

- External: Preheater port RetTimes are present.
- External: ModulePresent = Yes and MemoryState = OK for configured preheater ports.

**Method Command Contract**

Expected RetTimes:
- RetTime1
- RetTime2
- RetTime3
- RetTime4

Expected Channels:
- ExtTemp_PrehtLeft
- ExtTemp_PrehtRight
- PREH_L_HeaterTemp_Actual
- PREH_R_HeaterTemp_Actual

Expected Audit / Metadata Properties:
- precond.ColumnComp.PrehtLeft.ModulePresent
- precond.ColumnComp.PrehtLeft.MemoryState
- precond.ColumnComp.PrehtRight.ModulePresent
- precond.ColumnComp.PrehtRight.MemoryState

Required Configuration:
- ColumnComp
- AUDIT.ColumnComp.ModelNo is the device source of truth
- Preheater left/right modules present in instrument configuration

Method Evidence:
- CMBX sequence row should bind Preheater Connection Test -> PREHEATER / No_Integration.

**Report / DB Contract**

Report Evidence:
- Report uses RetTime windows and precond.ColumnComp.PrehtLeft/PrehtRight metadata.
- Temperature-difference cells compare heater temperature average against external preheater temperature average.

DB Evidence:
- Left/right port pass requires RetTimes plus ModulePresent=Yes and MemoryState=OK.

**Open Gaps**

- Confirm exact channel names for VA/VC/VH variants from loaded CMBX evidence.

### TCC_VALVE_01 - Valve / Keypad

- FOQ Section: TCC FOQ sequence row 03 / TD Valve and Keypad
- Injection: Valve
- Instrument Method: VALVES
- Processing Method: No_Integration
- Report Template: Device-specific: Report_VTCC_V2_12 for VC/VH, Report_VATCC_V1_01 for VA
- Report Sheets: Valve_Keypad
- Formula ID: `FORMULA_TCC_VALVEKEYPAD_OPEN`
- DB Fields: (not mapped)
- Model Applicability: VH-C10-A, VC-C10-A, VA-C10-A
- IRC Injected: No
- Coverage: partial

**Device Bindings**

| Device | Injection | Instrument Method | Processing Method | Report Template | Report Sheets | Report Files | DB Fields |
|---|---|---|---|---|---|---|---|
| VH-C10-A | Valve | VALVES | No_Integration | Report_VTCC_V2_12 | Valve_Keypad | (follows injection) | (not mapped) |
| VC-C10-A | Valve | VALVES | CORRECT_ACCURACY_INJ_INSERTION | Report_VTCC_V2_12 | Valve_Keypad | (follows injection) | (not mapped) |
| VA-C10-A | Valve | VALVES | No_Integration | Report_VATCC_V1_01 | Valve_Keypad | (follows injection) | (not mapped) |

**Purpose**

Verify upper/lower valve switching behavior and keypad/FastCool related audit behavior where the device configuration supports it.

**Acceptance Criteria**

- Not normalized from FOQ KB yet: Exact DB field names depend on mapping file and module variant.

**Method Command Contract**

Expected RetTimes:
- not recorded

Expected Channels:
- not recorded

Expected Audit / Metadata Properties:
- UpperValve.CurrentPosition
- LowerValve.CurrentPosition
- UpperValve.Precision
- LowerValve.Precision

Required Configuration:
- ColumnComp
- AUDIT.ColumnComp.ModelNo is the device source of truth
- ColumnComp.UpperValve and/or ColumnComp.LowerValve configured

Method Evidence:
- CMBX sequence row should bind Valve -> VALVES / No_Integration.

**Report / DB Contract**

Report Evidence:
- Report reads valve CurrentPosition and Precision audit properties.

DB Evidence:
- Exact DB field names depend on mapping file and module variant.

**Open Gaps**

- Keypad-specific workbook/report trace still needs exact formula confirmation.

### TCC_BURNIN_01 - VTCC BurnIn

- FOQ Section: TCC FOQ sequence row 04 / TD BurnIn
- Injection: VTCC_BurnIn
- Instrument Method: BURNIN
- Processing Method: NO_INTEGRATION
- Report Template: Device-specific: Report_VTCC_V2_12 for VC/VH, Report_VATCC_V1_01 for VA
- Report Sheets: (not mapped)
- Formula ID: `FORMULA_OPEN_VERIFICATION_REQUIRED`
- DB Fields: (not mapped)
- Model Applicability: VH-C10-A, VC-C10-A, VA-C10-A
- IRC Injected: No
- Coverage: open verification

**Device Bindings**

| Device | Injection | Instrument Method | Processing Method | Report Template | Report Sheets | Report Files | DB Fields |
|---|---|---|---|---|---|---|---|
| VH-C10-A | VTCC_BurnIn | BURNIN | NO_INTEGRATION | Report_VTCC_V2_12 | (not mapped) | (follows injection) | (not mapped) |
| VC-C10-A | VTCC_BurnIn | BURNIN | NO_INTEGRATION | Report_VTCC_V2_12 | (not mapped) | (follows injection) | (not mapped) |
| VA-C10-A | VTCC_BurnIn | BURNIN | NO_INTEGRATION | Report_VATCC_V1_01 | (not mapped) | (follows injection) | (not mapped) |

**Purpose**

Condition the module and exercise thermal/control behavior before the final measurement-oriented tests.

**Acceptance Criteria**

- Not normalized from FOQ KB yet.

**Method Command Contract**

Expected RetTimes:
- not recorded

Expected Channels:
- CC_Temp

Expected Audit / Metadata Properties:
- ColumnComp.CC.Temperature.Nominal

Required Configuration:
- ColumnComp
- AUDIT.ColumnComp.ModelNo is the device source of truth
- Column oven/temperature control configured

Method Evidence:
- CMBX sequence row should bind VTCC_BurnIn -> BURNIN / NO_INTEGRATION.

**Report / DB Contract**

Report Evidence:
- not recorded

DB Evidence:
- not recorded

**Open Gaps**

- TD purpose and detailed command stages need method-script interpretation before generation.

### TCC_CAL_01 - Temperature Calibration

- FOQ Section: TCC FOQ sequence row 05 / TD Temperature Calibration
- Injection: Temperature Calibration
- Instrument Method: TEMPERATURE_CALIBRATION
- Processing Method: CORRECT_ACCURACY_INJ_INSERTION
- Report Template: Device-specific: Report_VTCC_V2_12 for VC/VH, Report_VATCC_V1_01 for VA
- Report Sheets: Temp Calibration, Internal Use
- Formula ID: `FORMULA_TCC_TEMPERATURECALIBRATION_OPEN`
- DB Fields: TempCal120_U, TempCal120_L, TempCal100_U, TempCal100_L, TempCal80_U, TempCal80_L, TempCal60_U, TempCal60_L, TempCal40_U, TempCal40_L, TempCal20_U, TempCal20_L, TempCal10_U, TempCal10_L, TempCal5_U, TempCal5_L, TimeCal120, TimeCal100, TimeCal80, TimeCal60, TimeCal40, TimeCal20, TimeCal10, TimeCal05, Slope_Cal120_U, Slope_Cal100_U, Slope_Cal80_U, Slope_Cal60_U, Slope_Cal40_U, Slope_Cal20_U, Slope_Cal10_U, Slope_Cal05_U, Slope_Cal120_L, Slope_Cal100_L, Slope_Cal80_L, Slope_Cal60_L, Slope_Cal40_L, Slope_Cal20_L, Slope_Cal10_L, Slope_Cal05_L, TempCal85_U, TempCal85_L, TempCal70_U, TempCal70_L, TempCal55_U, TempCal55_L, TempCal30_U, TempCal30_L, TimeCal85, TimeCal70, TimeCal55, TimeCal30, Slope_Cal85_U, Slope_Cal70_U, Slope_Cal55_U, Slope_Cal30_U, Slope_Cal85_L, Slope_Cal70_L, Slope_Cal55_L, Slope_Cal30_L
- Model Applicability: VH-C10-A, VC-C10-A, VA-C10-A
- IRC Injected: Yes
- Coverage: partial

**Device Bindings**

| Device | Injection | Instrument Method | Processing Method | Report Template | Report Sheets | Report Files | DB Fields |
|---|---|---|---|---|---|---|---|
| VH-C10-A | Temperature Calibration | TEMPERATURE_CALIBRATION | CORRECT_ACCURACY_INJ_INSERTION | Report_VTCC_V2_12 | Temp_Calib_Internal | (follows injection) | TempCal120_U, TempCal120_L, TempCal100_U, TempCal100_L, TempCal80_U, TempCal80_L, TempCal60_U, TempCal60_L, TempCal40_U, TempCal40_L, TempCal20_U, TempCal20_L, TempCal10_U, TempCal10_L, TempCal5_U, TempCal5_L, TimeCal120, TimeCal100, TimeCal80, TimeCal60, TimeCal40, TimeCal20, TimeCal10, TimeCal05, Slope_Cal120_U, Slope_Cal100_U, Slope_Cal80_U, Slope_Cal60_U, Slope_Cal40_U, Slope_Cal20_U, Slope_Cal10_U, Slope_Cal05_U, Slope_Cal120_L, Slope_Cal100_L, Slope_Cal80_L, Slope_Cal60_L, Slope_Cal40_L, Slope_Cal20_L, Slope_Cal10_L, Slope_Cal05_L |
| VC-C10-A | Temperature Calibration | TEMPERATURE_CALIBRATION | CORRECT_ACCURACY_INJ_INSERTION | Report_VTCC_V2_12 | Temp_Calib_Internal | (follows injection) | TempCal85_U, TempCal85_L, TempCal70_U, TempCal70_L, TempCal55_U, TempCal55_L, TempCal40_U, TempCal40_L, TempCal30_U, TempCal30_L, TempCal20_U, TempCal20_L, TempCal10_U, TempCal10_L, TempCal5_U, TempCal5_L, TimeCal85, TimeCal70, TimeCal55, TimeCal40, TimeCal30, TimeCal20, TimeCal10, TimeCal05, Slope_Cal85_U, Slope_Cal70_U, Slope_Cal55_U, Slope_Cal40_U, Slope_Cal30_U, Slope_Cal20_U, Slope_Cal10_U, Slope_Cal05_U, Slope_Cal85_L, Slope_Cal70_L, Slope_Cal55_L, Slope_Cal40_L, Slope_Cal30_L, Slope_Cal20_L, Slope_Cal10_L, Slope_Cal05_L |
| VA-C10-A | Temperature Calibration | TEMPERATURE_CALIBRATION | NO_INTEGRATION | Report_VATCC_V1_01 | Temp_Calib_Internal | (follows injection) | TempCal85_U, TempCal85_L, TempCal70_U, TempCal70_L, TempCal55_U, TempCal55_L, TempCal40_U, TempCal40_L, TempCal30_U, TempCal30_L, TempCal20_U, TempCal20_L, TempCal10_U, TempCal10_L, TempCal5_U, TempCal5_L, TimeCal85, TimeCal70, TimeCal55, TimeCal40, TimeCal30, TimeCal20, TimeCal10, TimeCal05, Slope_Cal85_U, Slope_Cal70_U, Slope_Cal55_U, Slope_Cal40_U, Slope_Cal30_U, Slope_Cal20_U, Slope_Cal10_U, Slope_Cal05_U, Slope_Cal85_L, Slope_Cal70_L, Slope_Cal55_L, Slope_Cal40_L, Slope_Cal30_L, Slope_Cal20_L, Slope_Cal10_L, Slope_Cal05_L |

**Purpose**

Collect calibration evidence that supports subsequent temperature accuracy/stability interpretation.

**Acceptance Criteria**

- Not normalized from FOQ KB yet: DB mapping contains multiple TempCal setpoint fields for upper/lower sensors.

**Method Command Contract**

Expected RetTimes:
- RetTime1
- RetTime2
- RetTime3
- RetTime4
- RetTime5
- RetTime6
- RetTime7
- RetTime8

Expected Channels:
- CC_Temp
- ExtTemp_LowerCC
- ExtTemp_UpperCC

Expected Audit / Metadata Properties:
- ColumnComp.CC.Temperature.Nominal

Required Configuration:
- ColumnComp
- AUDIT.ColumnComp.ModelNo is the device source of truth
- External upper/lower thermometers configured

Method Evidence:
- CMBX sequence row should bind Temperature Calibration -> TEMPERATURE_CALIBRATION / CORRECT_ACCURACY_INJ_INSERTION.

**Report / DB Contract**

Report Evidence:
- Report and DB usage depends on calibration workbook-derived cells.

DB Evidence:
- DB mapping contains multiple TempCal setpoint fields for upper/lower sensors.

**Open Gaps**

- Need complete report formula trace for every TempCal DB field and display precision.

### TCC_ACC_01 - Temperature Accuracy

- FOQ Section: TCC FOQ sequence row 06 / TD Temperature Accuracy
- Injection: Temperature Accuracy_H
- Instrument Method: TEMPERATURE_ACCURACY
- Processing Method: ACCURACY_IRC_STOP_H
- Report Template: Device-specific: Report_VTCC_V2_12 for VC/VH, Report_VATCC_V1_01 for VA
- Report Sheets: Temp Accuracy
- Formula ID: `FORMULA_TCC_TEMP_ACCURACY_MAX_DEVIATION`
- DB Fields: TempAcc10, TempAcc20, TempAcc40, TempAcc80, TempAcc120, RES_TempAccuracy, TempAcc60, TempAcc85
- Model Applicability: VH-C10-A, VC-C10-A, VA-C10-A
- IRC Injected: Yes
- Coverage: partial

**Device Bindings**

| Device | Injection | Instrument Method | Processing Method | Report Template | Report Sheets | Report Files | DB Fields |
|---|---|---|---|---|---|---|---|
| VH-C10-A | Temperature Accuracy_H | TEMPERATURE_ACCURACY | ACCURACY_IRC_STOP_H | Report_VTCC_V2_12 | Temp Accuracy | (follows injection) | TempAcc10, TempAcc20, TempAcc40, TempAcc80, TempAcc120, RES_TempAccuracy |
| VC-C10-A | Temperature Accuracy_C | TEMPERATURE_ACCURACY | ACCURACY_IRC_STOP_C | Report_VTCC_V2_12 | Temp Accuracy | (follows injection) | TempAcc10, TempAcc20, TempAcc40, TempAcc60, TempAcc85, RES_TempAccuracy |
| VA-C10-A | Temperature Accuracy_C | TEMPERATURE_ACCURACY | ACCURACY_IRC_STOP_C | Report_VATCC_V1_01 | Temp Accuracy | (follows injection) | TempAcc10, TempAcc20, TempAcc40, TempAcc60, TempAcc85, RES_TempAccuracy |

**Purpose**

At each nominal setpoint, compare upper/lower external thermometer readings against nominal and use the larger absolute deviation.

**Acceptance Criteria**

- External: max absolute temperature deviation <= Definitions!Temperature Accuracy.

**Method Command Contract**

Expected RetTimes:
- RetTime1
- RetTime2
- RetTime3
- RetTime4
- RetTime5

Expected Channels:
- ExtTemp_LowerCC
- ExtTemp_UpperCC

Expected Audit / Metadata Properties:
- ColumnComp.CC.Temperature.Nominal
- ColumnComp.ModelNo

Required Configuration:
- ColumnComp
- AUDIT.ColumnComp.ModelNo is the device source of truth
- External upper/lower thermometers configured

Method Evidence:
- RetTime3 is the known 40 C anchor for VH evidence.

**Report / DB Contract**

Report Evidence:
- K66:K70 use AUDIT.RetTime1..5.
- L/M rows average ExtTemp_LowerCC and ExtTemp_UpperCC over RetTimeN-1.0..RetTimeN-0.2.
- Workbook selects the larger absolute deviation from nominal.

DB Evidence:
- DB cells resolve through Temp Accuracy report cells and display precision rules.

**Open Gaps**

- Confirm VA/VC/VH template-specific row coverage from loaded CMBX before generation.

### TCC_PRECISION_01 - Temperature Precision and Fan

- FOQ Section: TCC FOQ sequence row 07 / TD Temperature Precision and Fan
- Injection: Temperature Precision_and_Fan
- Instrument Method: TEMPERATURE_PRECISION_AND_FAN
- Processing Method: CORRECT_STABILITY_INJ_INSERTION
- Report Template: Device-specific: Report_VTCC_V2_12 for VC/VH, Report_VATCC_V1_01 for VA
- Report Sheets: Temp Precision, Fan
- Formula ID: `FORMULA_TCC_TEMP_PRECISION_SEPARATE_SENSOR_RANGE`
- DB Fields: TempPrecision, RES_TempPrecision
- Model Applicability: VH-C10-A, VC-C10-A, VA-C10-A
- IRC Injected: Yes
- Coverage: partial

**Device Bindings**

| Device | Injection | Instrument Method | Processing Method | Report Template | Report Sheets | Report Files | DB Fields |
|---|---|---|---|---|---|---|---|
| VH-C10-A | Temperature Precision_and_Fan | TEMPERATURE_PRECISION_AND_FAN | CORRECT_STABILITY_INJ_INSERTION | Report_VTCC_V2_12 | Temp Precision, Fan | (follows injection) | TempPrecision, RES_TempPrecision |
| VC-C10-A | Temperature Precision_and_Fan | TEMPERATURE_PRECISION_AND_FAN | CORRECT_STABILITY_INJ_INSERTION | Report_VTCC_V2_12 | Temp Precision, Fan | (follows injection) | TempPrecision, RES_TempPrecision |
| VA-C10-A | Temperature Precision | TEMPERATURE_PRECISION | NO_INTEGRATION | Report_VATCC_V1_01 | Temp Precision, Fan | Temperature Precision_and_Fan.XLS | TempPrecision, RES_TempPrecision |

**Purpose**

Measure repeatability/precision of upper and lower external thermometer readings and verify fan-related behavior where applicable.

**Acceptance Criteria**

- External: max(lower sensor range, upper sensor range) <= Definitions!Temperature Precision.

**Method Command Contract**

Expected RetTimes:
- RetTime1
- RetTime2
- RetTime3

Expected Channels:
- ExtTemp_LowerCC
- ExtTemp_UpperCC
- FanSpeed

Expected Audit / Metadata Properties:
- ColumnComp.CC.Temperature.Nominal

Required Configuration:
- ColumnComp
- AUDIT.ColumnComp.ModelNo is the device source of truth
- External upper/lower thermometers configured
- Fan symbol available if checked

Method Evidence:
- CMBX sequence row should bind Temperature Precision_and_Fan -> TEMPERATURE_PRECISION_AND_FAN / CORRECT_STABILITY_INJ_INSERTION.

**Report / DB Contract**

Report Evidence:
- Correct rule: max range of lower sensor and upper sensor separately, not combined K:L range.

DB Evidence:
- Pass/fail uses raw precision range; displayed summary uses two decimals.

**Open Gaps**

- Fan report formula and DB field exact names need trace confirmation.

### TCC_STABILITY_PCC_01 - Temperature Stability and PCC

- FOQ Section: TCC FOQ sequence row 08 / TD Temperature Stability and PCC
- Injection: Temperature Stability_and_PCC_H
- Instrument Method: TEMPERATURE_STABILITY_AND_PCC_70_H
- Processing Method: NO_INTEGRATION
- Report Template: Device-specific: Report_VTCC_V2_12 for VC/VH, Report_VATCC_V1_01 for VA
- Report Sheets: Temp Stability_Noise, PCC
- Formula ID: `FORMULA_TCC_TEMP_STABILITY_AND_PCC_COOLDOWN`
- DB Fields: TempStability, Noise_CC_Temp, Noise_PCC_Temp, Performance_PCC, RES_TempStability, RES_PCC, PCC_Acc_40_Step1, PCC_Acc_80, PCC_Acc_40_Step2, PCC_Drift
- Model Applicability: VH-C10-A
- IRC Injected: No
- Coverage: complete

**Device Bindings**

| Device | Injection | Instrument Method | Processing Method | Report Template | Report Sheets | Report Files | DB Fields |
|---|---|---|---|---|---|---|---|
| VH-C10-A | Temperature Stability_and_PCC_H | TEMPERATURE_STABILITY_AND_PCC_70_H | NO_INTEGRATION | Report_VTCC_V2_12 | Temp Stability_Noise, PCC | (follows injection) | TempStability, Noise_CC_Temp, Noise_PCC_Temp, Performance_PCC, RES_TempStability, RES_PCC, PCC_Acc_40_Step1, PCC_Acc_80, PCC_Acc_40_Step2, PCC_Drift |

**Purpose**

Measure long-window temperature stability and PCC cool-down performance on VH configurations with PCC support.

**Acceptance Criteria**

- External: max(lower sensor range, upper sensor range) <= Definitions!Temperature Stability.
- External: PCC cool-down delta <= Definitions!PCC CoolDownTime.

**Method Command Contract**

Expected RetTimes:
- RetTime1
- RetTime2
- RetTime3
- RetTime4

Expected Channels:
- ExtTemp_LowerCC
- ExtTemp_UpperCC
- PCC_Temp

Expected Audit / Metadata Properties:
- ColumnComp.CC.Temperature.Nominal

Required Configuration:
- ColumnComp
- AUDIT.ColumnComp.ModelNo is the device source of truth
- PCC hardware/configuration available

Method Evidence:
- CMBX sequence row should bind Temperature Stability_and_PCC_H -> TEMPERATURE_STABILITY_AND_PCC_70_H / NO_INTEGRATION.

**Report / DB Contract**

Report Evidence:
- Correct stability rule: max range of lower sensor and upper sensor separately.
- PCC CoolDown uses K105/L105 RetTime3/RetTime4 delta.

DB Evidence:
- PCC performance summary displays two decimals.

**Open Gaps**

- not recorded

### TCC_STABILITY_01 - Temperature Stability

- FOQ Section: TCC FOQ non-PCC branch / TD Temperature Stability
- Injection: Temperature Stability
- Instrument Method: TEMPERATURE_STABILITY
- Processing Method: NO_INTEGRATION
- Report Template: Device-specific: Report_VTCC_V2_12 for VC/VH, Report_VATCC_V1_01 for VA
- Report Sheets: Temp Stability_Noise
- Formula ID: `FORMULA_TCC_TEMP_STABILITY_SEPARATE_SENSOR_RANGE`
- DB Fields: TempStability, Noise_CC_Temp, RES_TempStability
- Model Applicability: VC-C10-A, VA-C10-A
- IRC Injected: No
- Coverage: partial

**Device Bindings**

| Device | Injection | Instrument Method | Processing Method | Report Template | Report Sheets | Report Files | DB Fields |
|---|---|---|---|---|---|---|---|
| VC-C10-A | Temperature Stability_C | TEMPERATURE_STABILITY_70_C | NO_INTEGRATION | Report_VTCC_V2_12 | Temp Stability_Noise | (follows injection) | TempStability, Noise_CC_Temp, RES_TempStability |
| VA-C10-A | Temperature Stability_C | TEMPERATURE_STABILITY_70_C | NO_INTEGRATION | Report_VATCC_V1_01 | Temp Stability_Noise | (follows injection) | TempStability, Noise_CC_Temp, RES_TempStability |

**Purpose**

Measure long-window temperature stability on configurations without the VH PCC performance path.

**Acceptance Criteria**

- External: max(lower sensor range, upper sensor range) <= Definitions!Temperature Stability.

**Method Command Contract**

Expected RetTimes:
- RetTime1
- RetTime2
- RetTime3

Expected Channels:
- ExtTemp_LowerCC
- ExtTemp_UpperCC

Expected Audit / Metadata Properties:
- ColumnComp.CC.Temperature.Nominal

Required Configuration:
- ColumnComp
- AUDIT.ColumnComp.ModelNo is the device source of truth
- Non-PCC TCC configuration

Method Evidence:
- Binding must be confirmed from VC/VA CMBX evidence.

**Report / DB Contract**

Report Evidence:
- Expected to share the same separate-sensor stability workbook rule without PCC cells.

DB Evidence:
- DB mapping should omit PCC fields for non-PCC module variants.

**Open Gaps**

- Exact VC/VA injection and method names need loaded CMBX confirmation.

### TCC_HEATCOOL_01 - HeatUp and CoolDown

- FOQ Section: TCC FOQ sequence row 09 / TD HeatUp and CoolDown
- Injection: HeatUp and CoolDownTime
- Instrument Method: TEMP_HEAT_UP_DOWN_20_50_20
- Processing Method: No_Integration
- Report Template: Device-specific: Report_VTCC_V2_12 for VC/VH, Report_VATCC_V1_01 for VA
- Report Sheets: HeatUp&CoolDown
- Formula ID: `FORMULA_TCC_HEATUP_COOLDOWN_RETTIME_DELTA_MINUS_HOLD`
- DB Fields: HeatUp_Time_20to50, CoolDown_Time_50to20, RES_HeatUp, RES_CoolDown
- Model Applicability: VH-C10-A, VC-C10-A, VA-C10-A
- IRC Injected: No
- Coverage: partial

**Device Bindings**

| Device | Injection | Instrument Method | Processing Method | Report Template | Report Sheets | Report Files | DB Fields |
|---|---|---|---|---|---|---|---|
| VH-C10-A | HeatUp and CoolDownTime | TEMP_HEAT_UP_DOWN_20_50_20 | No_Integration | Report_VTCC_V2_12 | HeatUp&CoolDown | (follows injection) | HeatUp_Time_20to50, CoolDown_Time_50to20, RES_HeatUp, RES_CoolDown |
| VC-C10-A | HeatUp and CoolDownTime | TEMP_HEAT_UP_DOWN_20_50_20 | CORRECT_ACCURACY_INJ_INSERTION | Report_VTCC_V2_12 | HeatUp&CoolDown | (follows injection) | HeatUp_Time_20to50, CoolDown_Time_50to20, RES_HeatUp, RES_CoolDown |
| VA-C10-A | HeatUp and CoolDownTime | TEMP_HEAT_UP_DOWN_20_50_20 | No_Integration | Report_VATCC_V1_01 | HeatUp&CoolDown | (follows injection) | HeatUp_Time_20to50, CoolDown_Time_50to20, RES_HeatUp, RES_CoolDown |

**Purpose**

Measure 20->50 C heat-up and 50->20 C cool-down time and subtract the method-script stable hold time.

**Acceptance Criteria**

- External: HeatUp_Time_20to50 <= Definitions!HeatUp & Cool Down.
- External: CoolDown_Time_50to20 <= Definitions!HeatUp & Cool Down.

**Method Command Contract**

Expected RetTimes:
- RetTime1
- RetTime3
- RetTime4
- RetTime6

Expected Channels:
- ExtTemp_UpperCC

Expected Audit / Metadata Properties:
- not recorded

Required Configuration:
- ColumnComp
- AUDIT.ColumnComp.ModelNo is the device source of truth
- External upper thermometer configured

Method Evidence:
- CMBX sequence row should bind HeatUp and CoolDownTime -> TEMP_HEAT_UP_DOWN_20_50_20 / No_Integration.

**Report / DB Contract**

Report Evidence:
- Verified evaluator rule: heat-up = RetTime3 - RetTime1 - 2.0; cool-down = RetTime6 - RetTime4 - 2.0.

DB Evidence:
- DB output uses one-decimal display for time fields.

**Open Gaps**

- Keep row-65/row-66 workbook rule distinction visible until full FormulaOne parsing is complete.

### TCC_LEAK_01 - Liquid Leak / Keypad

- FOQ Section: TCC FOQ sequence row 10 / TD Liquid Leak and Keypad
- Injection: LiquidLeaktest
- Instrument Method: LIQUID LEAK
- Processing Method: No_Integration
- Report Template: Device-specific: Report_VTCC_V2_12 for VC/VH, Report_VATCC_V1_01 for VA
- Report Sheets: Liquid Leak, Valve_Keypad
- Formula ID: `FORMULA_TCC_LIQUIDLEAKKEYPAD_OPEN`
- DB Fields: (not mapped)
- Model Applicability: VH-C10-A, VC-C10-A, VA-C10-A
- IRC Injected: No
- Coverage: partial

**Device Bindings**

| Device | Injection | Instrument Method | Processing Method | Report Template | Report Sheets | Report Files | DB Fields |
|---|---|---|---|---|---|---|---|
| VH-C10-A | LiquidLeaktest | LIQUID LEAK | No_Integration | Report_VTCC_V2_12 | Liquid Leak, Valve_Keypad | (follows injection) | (not mapped) |
| VC-C10-A | LiquidLeaktest | LIQUID LEAK | CORRECT_ACCURACY_INJ_INSERTION | Report_VTCC_V2_12 | Liquid Leak, Valve_Keypad | (follows injection) | (not mapped) |
| VA-C10-A | LiquidLeaktest | LIQUID LEAK | No_Integration | Report_VATCC_V1_01 | Liquid Leak, Valve_Keypad | (follows injection) | (not mapped) |

**Purpose**

Verify the liquid leak sensor and related keypad behavior used by the module service check.

**Acceptance Criteria**

- Not normalized from FOQ KB yet: Exact field name depends on mapping file.

**Method Command Contract**

Expected RetTimes:
- not recorded

Expected Channels:
- not recorded

Expected Audit / Metadata Properties:
- LiquidLeak
- LeakSensor

Required Configuration:
- ColumnComp
- AUDIT.ColumnComp.ModelNo is the device source of truth
- Liquid leak sensor configured

Method Evidence:
- CMBX sequence row should bind LiquidLeaktest -> LIQUID LEAK / No_Integration.

**Report / DB Contract**

Report Evidence:
- Expected to evaluate leak sensor status from audit or report workbook state.

DB Evidence:
- Exact field name depends on mapping file.

**Open Gaps**

- Need report formula and DB trace for leak sensor result.

### TCC_SERVICE_01 - Qualification Service Done

- FOQ Section: TCC FOQ sequence row 11 / TD Qualification Service Done
- Injection: Qualification_Service_Done
- Instrument Method: Qualification_Service_Done
- Processing Method: No_Integration
- Report Template: Device-specific: Report_VTCC_V2_12 for VC/VH, Report_VATCC_V1_01 for VA
- Report Sheets: Internal Use
- Formula ID: `FORMULA_TCC_QUALIFICATIONSERVICEDONE_OPEN`
- DB Fields: (not mapped)
- Model Applicability: VH-C10-A, VC-C10-A, VA-C10-A
- IRC Injected: No
- Coverage: partial

**Device Bindings**

| Device | Injection | Instrument Method | Processing Method | Report Template | Report Sheets | Report Files | DB Fields |
|---|---|---|---|---|---|---|---|
| VH-C10-A | Qualification_Service_Done | Qualification_Service_Done | No_Integration | Report_VTCC_V2_12 | Internal Use | (follows injection) | (not mapped) |
| VC-C10-A | Qualification_Service_Done | Qualification_Service_Done | CORRECT_ACCURACY_INJ_INSERTION | Report_VTCC_V2_12 | Internal Use | (follows injection) | (not mapped) |
| VA-C10-A | Qualification_Service_Done | Qualification_Service_Done | No_Integration | Report_VATCC_V1_01 | Internal Use | (follows injection) | (not mapped) |

**Purpose**

Mark or verify that the qualification service completion action/state has been performed.

**Acceptance Criteria**

- Not normalized from FOQ KB yet: Exact DB contract needs mapping confirmation.

**Method Command Contract**

Expected RetTimes:
- not recorded

Expected Channels:
- not recorded

Expected Audit / Metadata Properties:
- Qualification_Service_Done

Required Configuration:
- ColumnComp
- AUDIT.ColumnComp.ModelNo is the device source of truth
- Service-level command access if required

Method Evidence:
- CMBX sequence row should bind Qualification_Service_Done -> Qualification_Service_Done / No_Integration.

**Report / DB Contract**

Report Evidence:
- not recorded

DB Evidence:
- Exact DB contract needs mapping confirmation.

**Open Gaps**

- Need TD/service command meaning and report trace.

### TCC_FACTORY_01 - Factory Default

- FOQ Section: TCC FOQ sequence row 12 / TD Factory Default
- Injection: Factory Default
- Instrument Method: FACTORYDEFAULT
- Processing Method: No_Integration
- Report Template: Device-specific: Report_VTCC_V2_12 for VC/VH, Report_VATCC_V1_01 for VA
- Report Sheets: Definitions, Internal Use, Factory Default
- Formula ID: `FORMULA_TCC_FACTORY_DEFAULT_METADATA`
- DB Fields: TestDate, Serial, TimeBase, ModelNo, ModelVariant, HardwareVersion, Firmware, SubmitDate, RES_SN_Check
- Model Applicability: VH-C10-A, VC-C10-A, VA-C10-A
- IRC Injected: No
- Coverage: complete

**Device Bindings**

| Device | Injection | Instrument Method | Processing Method | Report Template | Report Sheets | Report Files | DB Fields |
|---|---|---|---|---|---|---|---|
| VH-C10-A | Factory Default | FACTORYDEFAULT | No_Integration | Report_VTCC_V2_12 | Definitions, Internal Use, Factory Default | (follows injection) | TestDate, Serial, TimeBase, ModelNo, ModelVariant, HardwareVersion, Firmware, SubmitDate, RES_SN_Check |
| VC-C10-A | Factory Default | FACTORYDEFAULT | CORRECT_ACCURACY_INJ_INSERTION | Report_VTCC_V2_12 | Definitions, Internal Use, Factory Default | (follows injection) | TestDate, Serial, TimeBase, ModelNo, ModelVariant, HardwareVersion, Firmware, SubmitDate, RES_SN_Check |
| VA-C10-A | Factory Default | FACTORYDEFAULT | No_Integration | Report_VATCC_V1_01 | Definitions, Internal Use, Factory Default | (follows injection) | TestDate, Serial, TimeBase, ModelNo, ModelVariant, HardwareVersion, Firmware, SubmitDate, RES_SN_Check |

**Purpose**

Verify factory default and identity metadata, including model number, model variant, serial number, firmware, and hardware revision.

**Acceptance Criteria**

- External/Internal split not fully normalized: ModelNo, firmware, hardware, model variant, and serial-number checks come from audit/precondition metadata.

**Method Command Contract**

Expected RetTimes:
- not recorded

Expected Channels:
- not recorded

Expected Audit / Metadata Properties:
- AUDIT.ColumnComp.ModelNo
- precond.ColumnComp.SerialNo
- precond.ColumnComp.FirmwareVersion
- precond.ColumnComp.HardwareVersion
- precond.ColumnComp.ModuleHardwareRevision

Required Configuration:
- ColumnComp
- AUDIT.ColumnComp.ModelNo is the device source of truth
- Module identity metadata available in precondition/audit trail

Method Evidence:
- CMBX sequence row should bind Factory Default -> FACTORYDEFAULT / No_Integration.

**Report / DB Contract**

Report Evidence:
- ModelVariant comes from Internal Use / ModuleHardwareRevision style metadata.
- Serial number check compares ColumnComp.SerialNo with sequence name.

DB Evidence:
- Device detection and upload table selection use AUDIT.ColumnComp.ModelNo as source of truth.

**Open Gaps**

- not recorded

### TCC_ERRORLOG_01 - Error Log Check

- FOQ Section: TCC FOQ sequence row 13 / TD Error Log Check
- Injection: Error Log Check
- Instrument Method: CHECKERRORLOG
- Processing Method: No_Integration
- Report Template: Device-specific: Report_VTCC_V2_12 for VC/VH, Report_VATCC_V1_01 for VA
- Report Sheets: Error Log, Internal Use
- Formula ID: `FORMULA_TCC_ERRORLOGCHECK_OPEN`
- DB Fields: (not mapped)
- Model Applicability: VH-C10-A, VC-C10-A, VA-C10-A
- IRC Injected: No
- Coverage: partial

**Device Bindings**

| Device | Injection | Instrument Method | Processing Method | Report Template | Report Sheets | Report Files | DB Fields |
|---|---|---|---|---|---|---|---|
| VH-C10-A | Error Log Check | CHECKERRORLOG | No_Integration | Report_VTCC_V2_12 | Error Log, Internal Use | (follows injection) | (not mapped) |
| VC-C10-A | Error Log Check | CHECKERRORLOG | CORRECT_ACCURACY_INJ_INSERTION | Report_VTCC_V2_12 | Error Log, Internal Use | (follows injection) | (not mapped) |
| VA-C10-A | Error Log Check | CHECKERRORLOG | No_Integration | Report_VATCC_V1_01 | Error Log, Internal Use | (follows injection) | (not mapped) |

**Purpose**

Verify that the module error log state is acceptable at the end of the FOQ run.

**Acceptance Criteria**

- Not normalized from FOQ KB yet: Exact error-log DB field needs mapping confirmation.

**Method Command Contract**

Expected RetTimes:
- not recorded

Expected Channels:
- not recorded

Expected Audit / Metadata Properties:
- ErrorLog
- CheckErrorLog

Required Configuration:
- ColumnComp
- AUDIT.ColumnComp.ModelNo is the device source of truth
- Error log/service command access

Method Evidence:
- CMBX sequence row should bind Error Log Check -> CHECKERRORLOG / No_Integration.

**Report / DB Contract**

Report Evidence:
- Expected to inspect error-log audit/service state rather than channel data.

DB Evidence:
- Exact error-log DB field needs mapping confirmation.

**Open Gaps**

- Need command semantics and report formula trace for pass/fail criteria.
