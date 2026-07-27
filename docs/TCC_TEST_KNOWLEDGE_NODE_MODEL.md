# TCC Test Knowledge Nodes

This document renders the Test Knowledge Node contract used by the FOQ Knowledge Alignment workbench.
Each node connects FOQ intent to CMBX execution evidence, report/formula evidence, and DB output fields.

## Node Index

| Test ID | Test | Injection | Instrument Method | Processing Method | Report Sheets | Formula ID | DB Fields | Coverage |
|---|---|---|---|---|---|---|---|---|
| TCC_COL_01 | Column ID | ColumnIDs | ColumnID | CORRECT_STABILITY_INJ_INSERTION | Column ID | `FORMULA_TCC_COLUMN_ID_AUDIT_DESCRIPTION` | RES_ColumnID_A, RES_ColumnID_B, RES_ColumnID_C, RES_ColumnID_D | partial |
| TCC_PREHEATER_01 | Preheater Connection Test | Preheater Connection Test | PREHEATER | No_Integration | Preheater Ports_Noise | `FORMULA_TCC_PREHEATER_PORT_STATE_AND_DIFF` | Noise_PrehtLeft_Temp, Noise_PrehtRight_Temp, Diff_PhLeft_HtTmp, Diff_PhRight_HtTmp, RES_Preheater_Left_Port, RES_Preheater_Right_Port | partial |
| TCC_VALVE_01 | Valve / Keypad | Valve | VALVES | No_Integration | Valve_Keypad | `FORMULA_TCC_VALVE_KEYPAD_AUDIT_STATE_CHECKS` | (not mapped) | partial |
| TCC_BURNIN_01 | VTCC BurnIn | VTCC_BurnIn | BURNIN | NO_INTEGRATION | Conditioning / no DB output | `FORMULA_NOT_REQUIRED_TCC_BURNIN_CONDITIONING` | (not mapped) | open verification |
| TCC_CAL_01 | Temperature Calibration | Temperature Calibration | TEMPERATURE_CALIBRATION | CORRECT_ACCURACY_INJ_INSERTION | Temp Calibration, Internal Use | `FORMULA_TCC_TEMPERATURECALIBRATION_OPEN` | TempCal120_U, TempCal120_L, TempCal100_U, TempCal100_L, TempCal80_U, TempCal80_L, TempCal60_U, TempCal60_L, TempCal40_U, TempCal40_L, TempCal20_U, TempCal20_L, TempCal10_U, TempCal10_L, TempCal5_U, TempCal5_L, TimeCal120, TimeCal100, TimeCal80, TimeCal60, TimeCal40, TimeCal20, TimeCal10, TimeCal05, Slope_Cal120_U, Slope_Cal100_U, Slope_Cal80_U, Slope_Cal60_U, Slope_Cal40_U, Slope_Cal20_U, Slope_Cal10_U, Slope_Cal05_U, Slope_Cal120_L, Slope_Cal100_L, Slope_Cal80_L, Slope_Cal60_L, Slope_Cal40_L, Slope_Cal20_L, Slope_Cal10_L, Slope_Cal05_L, TempCal85_U, TempCal85_L, TempCal70_U, TempCal70_L, TempCal55_U, TempCal55_L, TempCal30_U, TempCal30_L, TimeCal85, TimeCal70, TimeCal55, TimeCal30, Slope_Cal85_U, Slope_Cal70_U, Slope_Cal55_U, Slope_Cal30_U, Slope_Cal85_L, Slope_Cal70_L, Slope_Cal55_L, Slope_Cal30_L | partial |
| TCC_ACC_01 | Temperature Accuracy | Temperature Accuracy_H | TEMPERATURE_ACCURACY | ACCURACY_IRC_STOP_H | Temp Accuracy | `FORMULA_TCC_TEMP_ACCURACY_MAX_DEVIATION` | TempAcc10, TempAcc20, TempAcc40, TempAcc80, TempAcc120, RES_TempAccuracy, TempAcc60, TempAcc85 | partial |
| TCC_PRECISION_01 | Temperature Precision and Fan | Temperature Precision_and_Fan | TEMPERATURE_PRECISION_AND_FAN | CORRECT_STABILITY_INJ_INSERTION | Temp Precision, Fan | `FORMULA_TCC_TEMP_PRECISION_SEPARATE_SENSOR_RANGE` | TempPrecision, RES_TempPrecision | partial |
| TCC_STABILITY_PCC_01 | Temperature Stability and PCC | Temperature Stability_and_PCC_H | TEMPERATURE_STABILITY_AND_PCC_70_H | NO_INTEGRATION | Temp Stability_Noise, PCC | `FORMULA_TCC_TEMP_STABILITY_AND_PCC_COOLDOWN` | TempStability, Noise_CC_Temp, Noise_PCC_Temp, Performance_PCC, RES_TempStability, RES_PCC, PCC_Acc_40_Step1, PCC_Acc_80, PCC_Acc_40_Step2, PCC_Drift | partial |
| TCC_STABILITY_01 | Temperature Stability | Temperature Stability | TEMPERATURE_STABILITY | NO_INTEGRATION | Temp Stability_Noise | `FORMULA_TCC_TEMP_STABILITY_SEPARATE_SENSOR_RANGE` | TempStability, Noise_CC_Temp, RES_TempStability | open verification |
| TCC_HEATCOOL_01 | HeatUp and CoolDown | HeatUp and CoolDownTime | TEMP_HEAT_UP_DOWN_20_50_20 | No_Integration | HeatUp&CoolDown | `FORMULA_TCC_HEATUP_COOLDOWN_RETTIME_DELTA_MINUS_HOLD` | HeatUp_Time_20to50, CoolDown_Time_50to20, RES_HeatUp, RES_CoolDown | complete |
| TCC_LEAK_01 | Liquid Leak / Keypad | LiquidLeaktest | LIQUID LEAK | No_Integration | Liquid Leak, Valve_Keypad | `FORMULA_TCC_LIQUID_LEAK_AUDIT_PRECOND_CHECK` | (not mapped) | open verification |
| TCC_SERVICE_01 | Qualification Service Done | Qualification_Service_Done | Qualification_Service_Done | No_Integration | Internal Use | `FORMULA_NOT_REQUIRED_TCC_SERVICE_AUDIT_LOG` | (not mapped) | open verification |
| TCC_FACTORY_01 | Factory Default | Factory Default | FACTORYDEFAULT | No_Integration | Definitions, Internal Use, Factory Default | `FORMULA_TCC_FACTORY_DEFAULT_METADATA` | TestDate, Serial, TimeBase, ModelNo, ModelVariant, HardwareVersion, Firmware, SubmitDate, RES_SN_Check | partial |
| TCC_ERRORLOG_01 | Error Log Check | Error Log Check | CHECKERRORLOG | No_Integration | Error Log, Internal Use | `FORMULA_NOT_REQUIRED_TCC_ERROR_LOG_AUDIT_TABLE` | (not mapped) | open verification |
| VDAD_WARMUP_01 | Warm Up | Warm Up | (not bound) | No_Integration | Diagnostic Cell | `FORMULA_VDAD_WARMUP_OPEN` | (not mapped) | open verification |
| VDAD_NOISE_01 | Noise | Noise | (not bound) | No_Integration | Diagnostic Cell, Fluidic Flow Cell | `FORMULA_VDAD_NOISE_OPEN` | Noise, Drift | open verification |
| VDAD_LINEARITY_01 | Linearity | Linearity | (not bound) | No_Integration | Fluidic Flow Cell | `FORMULA_VDAD_LINEARITY_OPEN` | Linearity, System Check | open verification |
| VDAD_WAVELENGTH_01 | Wavelength Accuracy | Wavelength Accuracy | (not bound) | No_Integration | Diagnostic Cell, Fluidic Flow Cell | `FORMULA_VDAD_WAVELENGTHACCURACY_OPEN` | WavelengthAccuracy | open verification |
| VDAD_3DFIELD_01 | 3D Field | 3D Field | (not bound) | (not bound) | 3D Field | `FORMULA_VDAD_3DFIELD_OPEN` | (not mapped) | not applicable |

## Coverage Audit

| Test ID | Method | Processing | Report/Formula | DB | RetTimes | Channels | Audit/Metadata | Config | Overall | Gaps |
|---|---|---|---|---|---|---|---|---|---|---|
| TCC_COL_01 | bound to instrument method evidence | IRC/corrective binding documented | report sheet and formula family mapped | DB fields mapped with evidence | not required | not required | audit/property contract documented | configuration contract documented | open verification | coverage status is partial; detailed proof gap not recorded |
| TCC_PREHEATER_01 | bound to instrument method evidence | bound | report sheet and formula family mapped | DB fields mapped with evidence | RetTime contract documented | channel contract documented | audit/property contract documented | configuration contract documented | open verification | Confirm exact channel names for VA/VC/VH variants from loaded CMBX evidence. |
| TCC_VALVE_01 | bound to instrument method evidence | bound | report sheet and formula family mapped | no DB contract expected | not required | not required | audit/property contract documented | configuration contract documented | open verification | Workbook pass/fail cells for Valve_Keypad are mapped as audit-state checks but not yet reconstructed as FormulaOne expressions. |
| TCC_BURNIN_01 | bound to instrument method evidence | bound | no report formula contract expected | no DB contract expected | not required | channel contract documented | audit/property contract documented | configuration contract documented | open verification | Exact BURNIN trigger names and abort guard thresholds need method-script line-level extraction before generation. |
| TCC_CAL_01 | bound to instrument method evidence | IRC/corrective binding documented | report bound; formula open | DB fields mapped with evidence | RetTime contract documented | channel contract documented | audit/property contract documented | configuration contract documented | open verification | Need workbook-derived low-temperature reach pass/fail trace; VTCC display precision and VA Report_VATCC_V1_01 direct formula-object parity are verified.; report/formula: report bound; formula open |
| TCC_ACC_01 | bound to instrument method evidence | IRC/corrective binding documented | report sheet and formula family mapped | DB fields mapped with evidence | RetTime contract documented | channel contract documented | audit/property contract documented | configuration contract documented | open verification | Confirm VA/VC/VH template-specific row coverage from loaded CMBX before generation. |
| TCC_PRECISION_01 | bound to instrument method evidence | IRC/corrective binding documented | report sheet and formula family mapped | DB fields mapped with evidence | RetTime contract documented | channel contract documented | audit/property contract documented | configuration contract documented | open verification | Fan pass/fail workbook formula and whether it has any DB fields outside current mapping need trace confirmation; VA Precision/Fan branch behavior is verified from real VATCC report XML. |
| TCC_STABILITY_PCC_01 | bound to instrument method evidence | bound | report sheet and formula family mapped | DB fields mapped with evidence | RetTime contract documented | channel contract documented | audit/property contract documented | configuration contract documented | open verification | coverage status is partial; detailed proof gap not recorded |
| TCC_STABILITY_01 | bound to instrument method evidence | bound | report sheet and formula family mapped | DB fields mapped with evidence | RetTime contract documented | channel contract documented | audit/property contract documented | configuration contract documented | open verification | Whether Stability has any hidden IRC insertion path in production workflows still needs processing-method action-row evidence; VA Report_VATCC_V1_01 Temp Stability_Noise layout is verified. |
| TCC_HEATCOOL_01 | bound to instrument method evidence | bound | report sheet and formula family mapped | DB fields mapped with evidence | RetTime contract documented | channel contract documented | not required | configuration contract documented | closed | none |
| TCC_LEAK_01 | bound to instrument method evidence | bound | report sheet and formula family mapped | no DB contract expected | not required | not required | audit/property contract documented | configuration contract documented | open verification | Manual operator message timing and alarm-confirmation wait semantics need line-level method extraction before generation. |
| TCC_SERVICE_01 | bound to instrument method evidence | bound | no report formula contract expected | no DB contract expected | not required | not required | audit/property contract documented | configuration contract documented | open verification | Need line-level confirmation whether method only logs service state or also writes completion state in some variants. |
| TCC_FACTORY_01 | bound to instrument method evidence | bound | report sheet and formula family mapped | DB fields mapped with evidence | not required | not required | audit/property contract documented | configuration contract documented | open verification | coverage status is partial; detailed proof gap not recorded |
| TCC_ERRORLOG_01 | bound to instrument method evidence | bound | no report formula contract expected | no DB contract expected | not required | not required | audit/property contract documented | configuration contract documented | open verification | Need line-level confirmation of error-log inspect/clear behavior and any variant-specific connection reset commands. |
| VDAD_WARMUP_01 | missing | bound | report bound; formula open | no DB contract expected | not required | not required | not required | configuration contract documented | missing evidence | Load a VDAD CMBX and bind the actual injection, method, and report template.; method command: missing; report/formula: report bound; formula open |
| VDAD_NOISE_01 | missing | bound | report bound; formula open | DB fields mapped with evidence | not required | channel contract documented | not required | configuration contract documented | missing evidence | VDAD/VMWD report template formula extraction is still required.; method command: missing; report/formula: report bound; formula open |
| VDAD_LINEARITY_01 | missing | bound | report bound; formula open | DB fields mapped with evidence | not required | channel contract documented | not required | configuration contract documented | missing evidence | Processing/report integration logic must be decoded before this can become a generation template.; method command: missing; report/formula: report bound; formula open |
| VDAD_WAVELENGTH_01 | missing | bound | report bound; formula open | DB fields mapped with evidence | not required | channel contract documented | not required | configuration contract documented | missing evidence | Bind actual VDAD report template and formula objects from a loaded CMBX.; method command: missing; report/formula: report bound; formula open |
| VDAD_3DFIELD_01 | missing | missing | report bound; formula open | no DB contract expected | not required | channel contract documented | not required | configuration contract documented | not applicable | VMWD-C does not support 3D Field; do not mark this as missing for VMWD-C.; method command: missing; processing method: missing; report/formula: report bound; formula open |

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
| VDAD_WARMUP_01 | VF-D11-A | Warm Up | (none) | (none) | (none) | (none) | (none) | no DB contract expected |
| VDAD_WARMUP_01 | VC-D11-A | Warm Up | (none) | (none) | (none) | (none) | (none) | no DB contract expected |
| VDAD_WARMUP_01 | VC-D12-A | Warm Up | (none) | (none) | (none) | (none) | (none) | no DB contract expected |
| VDAD_NOISE_01 | VF-D11-A | Noise | (none) | Noise, Drift | (none) | Noise, Drift | (none) | missing mapping rows |
| VDAD_NOISE_01 | VC-D11-A | Noise | (none) | Noise, Drift | (none) | Noise, Drift | (none) | missing mapping rows |
| VDAD_NOISE_01 | VC-D12-A | Noise | (none) | Noise, Drift | (none) | Noise, Drift | (none) | missing mapping rows |
| VDAD_NOISE_01 | VMWD-C | Noise | (none) | Noise, Drift | (none) | Noise, Drift | (none) | mapping unavailable: 'Device type not found in FOQResultLocations DeviceTypes: VMWD-C' |
| VDAD_LINEARITY_01 | VF-D11-A | Linearity | (none) | Linearity, System Check | (none) | Linearity, System Check | (none) | missing mapping rows |
| VDAD_LINEARITY_01 | VC-D11-A | Linearity | (none) | Linearity, System Check | (none) | Linearity, System Check | (none) | missing mapping rows |
| VDAD_LINEARITY_01 | VC-D12-A | Linearity | (none) | Linearity, System Check | (none) | Linearity, System Check | (none) | missing mapping rows |
| VDAD_LINEARITY_01 | VMWD-C | Linearity | (none) | Linearity, System Check | (none) | Linearity, System Check | (none) | mapping unavailable: 'Device type not found in FOQResultLocations DeviceTypes: VMWD-C' |
| VDAD_WAVELENGTH_01 | VF-D11-A | Wavelength Accuracy | (none) | WavelengthAccuracy | (none) | WavelengthAccuracy | (none) | missing mapping rows |
| VDAD_WAVELENGTH_01 | VC-D11-A | Wavelength Accuracy | (none) | WavelengthAccuracy | (none) | WavelengthAccuracy | (none) | missing mapping rows |
| VDAD_WAVELENGTH_01 | VC-D12-A | Wavelength Accuracy | (none) | WavelengthAccuracy | (none) | WavelengthAccuracy | (none) | missing mapping rows |
| VDAD_WAVELENGTH_01 | VMWD-C | Wavelength Accuracy | (none) | WavelengthAccuracy | (none) | WavelengthAccuracy | (none) | mapping unavailable: 'Device type not found in FOQResultLocations DeviceTypes: VMWD-C' |
| VDAD_3DFIELD_01 | VF-D11-A | 3D Field | (none) | (none) | (none) | (none) | (none) | no DB contract expected |
| VDAD_3DFIELD_01 | VC-D11-A | 3D Field | (none) | (none) | (none) | (none) | (none) | no DB contract expected |
| VDAD_3DFIELD_01 | VC-D12-A | 3D Field | (none) | (none) | (none) | (none) | (none) | no DB contract expected |

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
- Coverage: partial

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
- Formula ID: `FORMULA_TCC_VALVE_KEYPAD_AUDIT_STATE_CHECKS`
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

- Not normalized from FOQ KB yet: FOQResultLocations has no DB output rows for Valve; report/audit evidence remains procedure-facing.

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
- ColumnComp.FastCoolState

Required Configuration:
- ColumnComp
- AUDIT.ColumnComp.ModelNo is the device source of truth
- ColumnComp.UpperValve and/or ColumnComp.LowerValve configured
- Front-panel/keypad actions available to operator

Method Evidence:
- VALVES setup: set CC TempCtrl On, set StillAir, set UpperValve and LowerValve to 6_1, log upper/lower valve precision.
- VALVES run: acquire CC_Temp as audit/time carrier, switch both valves 6_1 -> 1_2 -> 6_1, log precision after each switch.
- VALVES operator branch: prompt disconnect/reconnect and FAST COOL / upper valve / lower valve keypad actions.

**Report / DB Contract**

Report Evidence:
- Valve_Keypad audit position checks: K49/L49 at -0.05 min, K50/L50 at 0.095 min, K51/L51 at 0.19 min, K60/L60 at 0.9 min.
- Valve_Keypad precision checks: U49:U51 read AUDIT.UpperValve.Precision and V49:V51 read AUDIT.LowerValve.Precision.
- N60 reads AUDIT.ColumnComp.FastCoolState(0.9,"backward") for keypad/FastCool evidence.

DB Evidence:
- FOQResultLocations has no DB output rows for Valve; report/audit evidence remains procedure-facing.

**Open Gaps**

- Workbook pass/fail cells for Valve_Keypad are mapped as audit-state checks but not yet reconstructed as FormulaOne expressions.

### TCC_BURNIN_01 - VTCC BurnIn

- FOQ Section: TCC FOQ sequence row 04 / TD BurnIn
- Injection: VTCC_BurnIn
- Instrument Method: BURNIN
- Processing Method: NO_INTEGRATION
- Report Template: Device-specific: Report_VTCC_V2_12 for VC/VH, Report_VATCC_V1_01 for VA
- Report Sheets: Conditioning / no DB output
- Formula ID: `FORMULA_NOT_REQUIRED_TCC_BURNIN_CONDITIONING`
- DB Fields: (not mapped)
- Model Applicability: VH-C10-A, VC-C10-A, VA-C10-A
- IRC Injected: No
- Coverage: open verification

**Device Bindings**

| Device | Injection | Instrument Method | Processing Method | Report Template | Report Sheets | Report Files | DB Fields |
|---|---|---|---|---|---|---|---|
| VH-C10-A | VTCC_BurnIn | BURNIN | NO_INTEGRATION | Report_VTCC_V2_12 | Conditioning / no DB output | (follows injection) | (not mapped) |
| VC-C10-A | VTCC_BurnIn | BURNIN | NO_INTEGRATION | Report_VTCC_V2_12 | Conditioning / no DB output | (follows injection) | (not mapped) |
| VA-C10-A | VTCC_BurnIn | BURNIN | NO_INTEGRATION | Report_VATCC_V1_01 | Conditioning / no DB output | (follows injection) | (not mapped) |

**Purpose**

Condition the module and exercise thermal/control behavior before the final measurement-oriented tests.

**Acceptance Criteria**

- Not normalized from FOQ KB yet.

**Method Command Contract**

Expected RetTimes:
- not recorded

Expected Channels:
- CC_Temp
- ExtTemp_LowerCC
- ExtTemp_UpperCC

Expected Audit / Metadata Properties:
- ColumnComp.CC.Temperature.Nominal
- ColumnComp.ModelNo

Required Configuration:
- ColumnComp
- AUDIT.ColumnComp.ModelNo is the device source of truth
- Column oven/temperature control configured
- External thermometers available for heating evidence

Method Evidence:
- BURNIN setup: ReadyTempDelta broad, EquilibrationTime 0.5, CC TempCtrl On, StillAir, LiquidLeakSensor Off.
- BURNIN model branch: VH uses approximately 5..120 C thermal range; VA/VC use lower high-limit range, typically up to 85 C.
- BURNIN run: stabilize, acquire temperature channels, heat to max, cool to min, heat again, and end after required cycles.

**Report / DB Contract**

Report Evidence:
- BurnIn is a conditioning/evidence method rather than a formula-heavy DB output injection.
- No direct high-value DB mapping formula was found for this row in FOQResultLocations.

DB Evidence:
- not recorded

**Open Gaps**

- Exact BURNIN trigger names and abort guard thresholds need method-script line-level extraction before generation.

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

- Need workbook-derived low-temperature reach pass/fail trace; VTCC display precision and VA Report_VATCC_V1_01 direct formula-object parity are verified.

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
| VA-C10-A | Temperature Precision | TEMPERATURE_PRECISION | NO_INTEGRATION | Report_VATCC_V1_01 | Temp Precision | Temperature Precision_and_Fan.XLS | TempPrecision, RES_TempPrecision |

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

- Fan pass/fail workbook formula and whether it has any DB fields outside current mapping need trace confirmation; VA Precision/Fan branch behavior is verified from real VATCC report XML.

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
- Coverage: partial

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
- Coverage: open verification

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

- Whether Stability has any hidden IRC insertion path in production workflows still needs processing-method action-row evidence; VA Report_VATCC_V1_01 Temp Stability_Noise layout is verified.

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
- Coverage: complete

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
- RetTime2
- RetTime3
- RetTime4
- RetTime5
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
- CMBX sequence row should bind HeatUp and CoolDownTime -> TEMP_HEAT_UP_DOWN_20_50_20; VH/VA use No_Integration.
- Real VC 3000004.cmbx binds CORRECT_ACCURACY_INJ_INSERTION to many VC sequence rows, so HeatUp inherits VC sequence processing context rather than needing HeatUp-specific IRC logic.
- Keep the row-65 internal endpoint / row-66 external endpoint distinction visible when regenerating a binary-equivalent report template.

**Report / DB Contract**

Report Evidence:
- Verified evaluator rule: heat-up = RetTime2 - RetTime1 - 2.0; cool-down = RetTime5 - RetTime4 - 2.0.
- RetTime3 and RetTime6 remain required for the visible row-65 internal endpoint layout.

DB Evidence:
- DB output uses one-decimal display for time fields.

**Open Gaps**

- not recorded

### TCC_LEAK_01 - Liquid Leak / Keypad

- FOQ Section: TCC FOQ sequence row 10 / TD Liquid Leak and Keypad
- Injection: LiquidLeaktest
- Instrument Method: LIQUID LEAK
- Processing Method: No_Integration
- Report Template: Device-specific: Report_VTCC_V2_12 for VC/VH, Report_VATCC_V1_01 for VA
- Report Sheets: Liquid Leak, Valve_Keypad
- Formula ID: `FORMULA_TCC_LIQUID_LEAK_AUDIT_PRECOND_CHECK`
- DB Fields: (not mapped)
- Model Applicability: VH-C10-A, VC-C10-A, VA-C10-A
- IRC Injected: No
- Coverage: open verification

**Device Bindings**

| Device | Injection | Instrument Method | Processing Method | Report Template | Report Sheets | Report Files | DB Fields |
|---|---|---|---|---|---|---|---|
| VH-C10-A | LiquidLeaktest | LIQUID LEAK | No_Integration | Report_VTCC_V2_12 | Liquid Leak, Valve_Keypad | (follows injection) | (not mapped) |
| VC-C10-A | LiquidLeaktest | LIQUID LEAK | CORRECT_ACCURACY_INJ_INSERTION | Report_VTCC_V2_12 | Liquid Leak, Valve_Keypad | (follows injection) | (not mapped) |
| VA-C10-A | LiquidLeaktest | LIQUID LEAK | No_Integration | Report_VATCC_V1_01 | Liquid Leak, Valve_Keypad | (follows injection) | (not mapped) |

**Purpose**

Verify the liquid leak sensor and related keypad behavior used by the module service check.

**Acceptance Criteria**

- Not normalized from FOQ KB yet: FOQResultLocations has no DB output rows for LiquidLeaktest; this is a manual/audit report check.

**Method Command Contract**

Expected RetTimes:
- not recorded

Expected Channels:
- not recorded

Expected Audit / Metadata Properties:
- LiquidLeak
- LeakSensor
- ColumnComp.Alarm
- precond.LiquidLeakCalibrationValue

Required Configuration:
- ColumnComp
- AUDIT.ColumnComp.ModelNo is the device source of truth
- Liquid leak sensor configured
- Operator can inject/remove test liquid and confirm/mute alarm

Method Evidence:
- LIQUID LEAK setup: set safe CC nominal around 20 C, enable LiquidLeakSensor, initialize END_RUN trigger.
- LIQUID LEAK run: prompt operator to inject water, wait for LiquidLeak=Leak, log LiquidLeak, prompt alarm mute/confirmation.
- LIQUID LEAK cleanup: wait until ColumnComp.Alarm=NoAlarm, switch LiquidLeakSensor Off, prompt liquid removal, end run.

**Report / DB Contract**

Report Evidence:
- Liquid Leak report evidence: M47 = AUDIT.LiquidLeak(100.000,"backward").
- Liquid Leak report evidence: K47 = precond.LiquidLeakCalibrationValue.
- Valve_Keypad may contribute keypad/alarm context but FOQResultLocations has no DB output row for LiquidLeaktest.

DB Evidence:
- FOQResultLocations has no DB output rows for LiquidLeaktest; this is a manual/audit report check.

**Open Gaps**

- Manual operator message timing and alarm-confirmation wait semantics need line-level method extraction before generation.

### TCC_SERVICE_01 - Qualification Service Done

- FOQ Section: TCC FOQ sequence row 11 / TD Qualification Service Done
- Injection: Qualification_Service_Done
- Instrument Method: Qualification_Service_Done
- Processing Method: No_Integration
- Report Template: Device-specific: Report_VTCC_V2_12 for VC/VH, Report_VATCC_V1_01 for VA
- Report Sheets: Internal Use
- Formula ID: `FORMULA_NOT_REQUIRED_TCC_SERVICE_AUDIT_LOG`
- DB Fields: (not mapped)
- Model Applicability: VH-C10-A, VC-C10-A, VA-C10-A
- IRC Injected: No
- Coverage: open verification

**Device Bindings**

| Device | Injection | Instrument Method | Processing Method | Report Template | Report Sheets | Report Files | DB Fields |
|---|---|---|---|---|---|---|---|
| VH-C10-A | Qualification_Service_Done | Qualification_Service_Done | No_Integration | Report_VTCC_V2_12 | Internal Use | (follows injection) | (not mapped) |
| VC-C10-A | Qualification_Service_Done | Qualification_Service_Done | CORRECT_ACCURACY_INJ_INSERTION | Report_VTCC_V2_12 | Internal Use | (follows injection) | (not mapped) |
| VA-C10-A | Qualification_Service_Done | Qualification_Service_Done | No_Integration | Report_VATCC_V1_01 | Internal Use | (follows injection) | (not mapped) |

**Purpose**

Mark or verify that the qualification service completion action/state has been performed.

**Acceptance Criteria**

- Not normalized from FOQ KB yet: FOQResultLocations has no DB output rows for Qualification_Service_Done.

**Method Command Contract**

Expected RetTimes:
- not recorded

Expected Channels:
- not recorded

Expected Audit / Metadata Properties:
- ColumnComp_Wellness.Service.LastDate
- ColumnComp_Wellness.Qualification.LastDate

Required Configuration:
- ColumnComp
- AUDIT.ColumnComp.ModelNo is the device source of truth
- Service-level command access if required

Method Evidence:
- Qualification_Service_Done run: log ColumnComp_Wellness.Service.LastDate.
- Qualification_Service_Done run: log ColumnComp_Wellness.Qualification.LastDate.
- Preserve this as a separate procedure-state/audit evidence injection.

**Report / DB Contract**

Report Evidence:
- Qualification_Service_Done is metadata/audit driven and has no heavy raw channel calculation.
- Report role is qualification/service completion evidence rather than DB field output.

DB Evidence:
- FOQResultLocations has no DB output rows for Qualification_Service_Done.

**Open Gaps**

- Need line-level confirmation whether method only logs service state or also writes completion state in some variants.

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
- Coverage: partial

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
- Formula ID: `FORMULA_NOT_REQUIRED_TCC_ERROR_LOG_AUDIT_TABLE`
- DB Fields: (not mapped)
- Model Applicability: VH-C10-A, VC-C10-A, VA-C10-A
- IRC Injected: No
- Coverage: open verification

**Device Bindings**

| Device | Injection | Instrument Method | Processing Method | Report Template | Report Sheets | Report Files | DB Fields |
|---|---|---|---|---|---|---|---|
| VH-C10-A | Error Log Check | CHECKERRORLOG | No_Integration | Report_VTCC_V2_12 | Error Log, Internal Use | (follows injection) | (not mapped) |
| VC-C10-A | Error Log Check | CHECKERRORLOG | CORRECT_ACCURACY_INJ_INSERTION | Report_VTCC_V2_12 | Error Log, Internal Use | (follows injection) | (not mapped) |
| VA-C10-A | Error Log Check | CHECKERRORLOG | No_Integration | Report_VATCC_V1_01 | Error Log, Internal Use | (follows injection) | (not mapped) |

**Purpose**

Verify that the module error log state is acceptable at the end of the FOQ run.

**Acceptance Criteria**

- Not normalized from FOQ KB yet: FOQResultLocations has no DB output rows for Error Log Check.

**Method Command Contract**

Expected RetTimes:
- not recorded

Expected Channels:
- not recorded

Expected Audit / Metadata Properties:
- ErrorLog
- CheckErrorLog
- ColumnComp.CC.TempCtrl
- PrehtLeft.TempCtrl
- PrehtRight.TempCtrl

Required Configuration:
- ColumnComp
- AUDIT.ColumnComp.ModelNo is the device source of truth
- Error log/service command access
- Safe end-state control over CC and preheater temp controls

Method Evidence:
- CHECKERRORLOG run: turn PrehtRight.TempCtrl Off, PrehtLeft.TempCtrl Off, and CC.TempCtrl Off.
- CHECKERRORLOG role: inspect final error-log/audit state and leave device in a safe non-running condition.

**Report / DB Contract**

Report Evidence:
- Error Log sheet is an audit table endpoint rather than a formula-object-heavy calculation sheet.
- Report formula extraction does not expose significant cell-level formulas for this sheet.

DB Evidence:
- FOQResultLocations has no DB output rows for Error Log Check.

**Open Gaps**

- Need line-level confirmation of error-log inspect/clear behavior and any variant-specific connection reset commands.

### VDAD_WARMUP_01 - Warm Up

- FOQ Section: VDAD TD item: Warm Up
- Injection: Warm Up
- Instrument Method: (not bound)
- Processing Method: No_Integration
- Report Template: (not bound)
- Report Sheets: Diagnostic Cell
- Formula ID: `FORMULA_VDAD_WARMUP_OPEN`
- DB Fields: (not mapped)
- Model Applicability: VF-D11-A, VC-D11-A, VC-D12-A
- IRC Injected: No
- Coverage: open verification

**Device Bindings**

| Device | Injection | Instrument Method | Processing Method | Report Template | Report Sheets | Report Files | DB Fields |
|---|---|---|---|---|---|---|---|
| VF-D11-A | Warm Up | (not bound) | No_Integration | (not bound) | Diagnostic Cell | (follows injection) | (not mapped) |
| VC-D11-A | Warm Up | (not bound) | No_Integration | (not bound) | Diagnostic Cell | (follows injection) | (not mapped) |
| VC-D12-A | Warm Up | (not bound) | No_Integration | (not bound) | Diagnostic Cell | (follows injection) | (not mapped) |

**Purpose**

确认检测器 lamp 和 optical system 在正式测试前达到可重复、稳定的工作状态。

**Acceptance Criteria**

- Not normalized from FOQ KB yet.

**Method Command Contract**

Expected RetTimes:
- not recorded

Expected Channels:
- not recorded

Expected Audit / Metadata Properties:
- not recorded

Required Configuration:
- Detector
- UV lamp
- VIS lamp where applicable
- flow cell or diagnostic cell

Method Evidence:
- not recorded

**Report / DB Contract**

Report Evidence:
- TD defines warm-up as a prerequisite evidence step; CMBX method/report binding must be confirmed from a loaded VDAD package.

DB Evidence:
- not recorded

**Open Gaps**

- Load a VDAD CMBX and bind the actual injection, method, and report template.

### VDAD_NOISE_01 - Noise

- FOQ Section: VDAD TD item: Noise
- Injection: Noise
- Instrument Method: (not bound)
- Processing Method: No_Integration
- Report Template: (not bound)
- Report Sheets: Diagnostic Cell, Fluidic Flow Cell
- Formula ID: `FORMULA_VDAD_NOISE_OPEN`
- DB Fields: Noise, Drift
- Model Applicability: VF-D11-A, VC-D11-A, VC-D12-A, VMWD-C
- IRC Injected: No
- Coverage: open verification

**Device Bindings**

| Device | Injection | Instrument Method | Processing Method | Report Template | Report Sheets | Report Files | DB Fields |
|---|---|---|---|---|---|---|---|
| VF-D11-A | Noise | (not bound) | No_Integration | (not bound) | Diagnostic Cell, Fluidic Flow Cell | (follows injection) | Noise, Drift |
| VC-D11-A | Noise | (not bound) | No_Integration | (not bound) | Diagnostic Cell, Fluidic Flow Cell | (follows injection) | Noise, Drift |
| VC-D12-A | Noise | (not bound) | No_Integration | (not bound) | Diagnostic Cell, Fluidic Flow Cell | (follows injection) | Noise, Drift |
| VMWD-C | Noise | (not bound) | No_Integration | (not bound) | Diagnostic Cell, Fluidic Flow Cell | (follows injection) | Noise, Drift |

**Purpose**

评估 detector baseline 噪声和漂移；故障排查时可区分 cell、lamp、pump/flow 等来源。

**Acceptance Criteria**

- Not normalized from FOQ KB yet: DB mapping expected to contain detector noise/drift fields; exact field names require mapping confirmation.

**Method Command Contract**

Expected RetTimes:
- not recorded

Expected Channels:
- UV signal

Expected Audit / Metadata Properties:
- not recorded

Required Configuration:
- Detector
- UV lamp
- VIS lamp where applicable
- flow cell or diagnostic cell

Method Evidence:
- not recorded

**Report / DB Contract**

Report Evidence:
- Report formula and workbook calculation must be confirmed from VDAD/VMWD report template.

DB Evidence:
- DB mapping expected to contain detector noise/drift fields; exact field names require mapping confirmation.

**Open Gaps**

- VDAD/VMWD report template formula extraction is still required.

### VDAD_LINEARITY_01 - Linearity

- FOQ Section: VDAD TD item: Linearity
- Injection: Linearity
- Instrument Method: (not bound)
- Processing Method: No_Integration
- Report Template: (not bound)
- Report Sheets: Fluidic Flow Cell
- Formula ID: `FORMULA_VDAD_LINEARITY_OPEN`
- DB Fields: Linearity, System Check
- Model Applicability: VF-D11-A, VC-D11-A, VC-D12-A, VMWD-C
- IRC Injected: No
- Coverage: open verification

**Device Bindings**

| Device | Injection | Instrument Method | Processing Method | Report Template | Report Sheets | Report Files | DB Fields |
|---|---|---|---|---|---|---|---|
| VF-D11-A | Linearity | (not bound) | No_Integration | (not bound) | Fluidic Flow Cell | (follows injection) | Linearity, System Check |
| VC-D11-A | Linearity | (not bound) | No_Integration | (not bound) | Fluidic Flow Cell | (follows injection) | Linearity, System Check |
| VC-D12-A | Linearity | (not bound) | No_Integration | (not bound) | Fluidic Flow Cell | (follows injection) | Linearity, System Check |
| VMWD-C | Linearity | (not bound) | No_Integration | (not bound) | Fluidic Flow Cell | (follows injection) | Linearity, System Check |

**Purpose**

通过不同浓度标准品的峰面积/峰高响应评估检测器在信号范围内的线性。

**Acceptance Criteria**

- Not normalized from FOQ KB yet: DB mapping expected to include linearity-related result fields; exact report cells require mapping trace.

**Method Command Contract**

Expected RetTimes:
- not recorded

Expected Channels:
- UV signal

Expected Audit / Metadata Properties:
- not recorded

Required Configuration:
- Pump flow
- Autosampler injection volume
- Detector
- UV lamp
- VIS lamp where applicable
- flow cell or diagnostic cell

Method Evidence:
- not recorded

**Report / DB Contract**

Report Evidence:
- Linearity depends on report integration/calibration logic that must be decoded from the report template.

DB Evidence:
- DB mapping expected to include linearity-related result fields; exact report cells require mapping trace.

**Open Gaps**

- Processing/report integration logic must be decoded before this can become a generation template.

### VDAD_WAVELENGTH_01 - Wavelength Accuracy

- FOQ Section: VDAD TD item: Wavelength Accuracy
- Injection: Wavelength Accuracy
- Instrument Method: (not bound)
- Processing Method: No_Integration
- Report Template: (not bound)
- Report Sheets: Diagnostic Cell, Fluidic Flow Cell
- Formula ID: `FORMULA_VDAD_WAVELENGTHACCURACY_OPEN`
- DB Fields: WavelengthAccuracy
- Model Applicability: VF-D11-A, VC-D11-A, VC-D12-A, VMWD-C
- IRC Injected: No
- Coverage: open verification

**Device Bindings**

| Device | Injection | Instrument Method | Processing Method | Report Template | Report Sheets | Report Files | DB Fields |
|---|---|---|---|---|---|---|---|
| VF-D11-A | Wavelength Accuracy | (not bound) | No_Integration | (not bound) | Diagnostic Cell, Fluidic Flow Cell | (follows injection) | WavelengthAccuracy |
| VC-D11-A | Wavelength Accuracy | (not bound) | No_Integration | (not bound) | Diagnostic Cell, Fluidic Flow Cell | (follows injection) | WavelengthAccuracy |
| VC-D12-A | Wavelength Accuracy | (not bound) | No_Integration | (not bound) | Diagnostic Cell, Fluidic Flow Cell | (follows injection) | WavelengthAccuracy |
| VMWD-C | Wavelength Accuracy | (not bound) | No_Integration | (not bound) | Diagnostic Cell, Fluidic Flow Cell | (follows injection) | WavelengthAccuracy |

**Purpose**

用标准品或 filter/diagnostic evidence 验证检测器波长轴准确度。

**Acceptance Criteria**

- Not normalized from FOQ KB yet: Exact DB fields and report cells require VDAD mapping trace.

**Method Command Contract**

Expected RetTimes:
- not recorded

Expected Channels:
- UV signal

Expected Audit / Metadata Properties:
- not recorded

Required Configuration:
- Detector
- UV lamp
- VIS lamp where applicable
- flow cell or diagnostic cell

Method Evidence:
- not recorded

**Report / DB Contract**

Report Evidence:
- Shared standard and spectrum evaluation logic must be bound to actual report formulas.

DB Evidence:
- Exact DB fields and report cells require VDAD mapping trace.

**Open Gaps**

- Bind actual VDAD report template and formula objects from a loaded CMBX.

### VDAD_3DFIELD_01 - 3D Field

- FOQ Section: VDAD TD item: 3D Field
- Injection: 3D Field
- Instrument Method: (not bound)
- Processing Method: (not bound)
- Report Template: (not bound)
- Report Sheets: 3D Field
- Formula ID: `FORMULA_VDAD_3DFIELD_OPEN`
- DB Fields: (not mapped)
- Model Applicability: VF-D11-A, VC-D11-A, VC-D12-A
- IRC Injected: No
- Coverage: not applicable

**Device Bindings**

| Device | Injection | Instrument Method | Processing Method | Report Template | Report Sheets | Report Files | DB Fields |
|---|---|---|---|---|---|---|---|
| VF-D11-A | 3D Field | (not bound) | (not bound) | (not bound) | 3D Field | (follows injection) | (not mapped) |
| VC-D11-A | 3D Field | (not bound) | (not bound) | (not bound) | 3D Field | (follows injection) | (not mapped) |
| VC-D12-A | 3D Field | (not bound) | (not bound) | (not bound) | 3D Field | (follows injection) | (not mapped) |

**Purpose**

DAD-specific 3D field behavior; the TD explicitly distinguishes this from VMWD-C capability.

**Acceptance Criteria**

- Not normalized from FOQ KB yet.

**Method Command Contract**

Expected RetTimes:
- not recorded

Expected Channels:
- 3D Field signal

Expected Audit / Metadata Properties:
- not recorded

Required Configuration:
- DAD detector model

Method Evidence:
- not recorded

**Report / DB Contract**

Report Evidence:
- DAD-only report/method evidence still needs CMBX binding.

DB Evidence:
- not recorded

**Open Gaps**

- VMWD-C does not support 3D Field; do not mark this as missing for VMWD-C.
