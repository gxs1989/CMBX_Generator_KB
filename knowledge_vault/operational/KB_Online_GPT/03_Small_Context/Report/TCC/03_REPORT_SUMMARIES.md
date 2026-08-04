# TCC Report Understanding Summaries

Module: TCC  
Status: PARTIAL - VTCC and PressureEvaluation evidence available; VATCC canonical inventory missing  
Delivery_File: 03_REPORT_SUMMARIES.md

## Self Index

| ID | Source | Included |
|---|---|---|
| `TCC_METHOD_REPORT_KB` | `TCC_FOQ_METHOD_REPORT_KNOWLEDGE_BASE.md` | Yes |
| `TCC_ALIGNMENT` | `TCC_METHOD_REPORT_ALIGNMENT.md` | Yes |
| `VALVE_PRESSURE_CONTRACT` | `VALVE_SHIFT_SYNCHRON_PRESSURE_EVALUATION_REPORT_CONTRACT.md` | Yes |

---

## Evidence: TCC_METHOD_REPORT_KB

Source file: `TCC_FOQ_METHOD_REPORT_KNOWLEDGE_BASE.md`

This note summarizes the first verified knowledge layer for Vanquish TCC FOQ method understanding and future method generation.

## Local Sources

Test description:

```text
C:\ProgramData\CMBX Data Explorer Workspace\KB\FOQ TD\FOQ_Testdescription_VX-C10-A.docm
```

CMBX samples:

```text
C:\ProgramData\CMBX Data Explorer Workspace\packages\TCC Cost Out\Shipping Test\DVT011_VATCC.cmbx
C:\ProgramData\CMBX Data Explorer Workspace\packages\TCC Cost Out\Shipping Test\3000003_VCTCC.cmbx
C:\ProgramData\CMBX Data Explorer Workspace\packages\TCC Cost Out\Shipping Test\6000001_VHTCC.cmbx
C:\ProgramData\CMBX Data Explorer Workspace\packages\TCC Cost Out\Zollner\Production\0000003.cmbx
C:\ProgramData\CMBX Data Explorer Workspace\packages\TCC Cost Out\Zollner\Production\3000004.cmbx
C:\ProgramData\CMBX Data Explorer Workspace\packages\TCC Cost Out\Zollner\Production\6000001.cmbx
```

Decoded method evidence:

```text
knowledge_base/method_extract_probe/3000004/VALVES_embedded_method_flow.txt
knowledge_base/method_extract_probe/3000004/PREHEATER_embedded_method_flow.txt
knowledge_base/method_extract_probe/3000004/TEMPERATURE_ACCURACY_embedded_method_flow.txt
knowledge_base/method_extract_probe/3000004/TEMPERATURE_PRECISION_AND_FAN_embedded_method_flow.txt
knowledge_base/method_extract_probe/3000004/TEMPERATURE_STABILITY_AND_PCC_70_H_embedded_method_flow.txt
knowledge_base/method_extract_probe/3000004/TEMP_HEAT_UP_DOWN_20_50_20_embedded_method_flow.txt
```

Processing method probe output:

```text
knowledge_base/tcc_processing_probe/VA/0000003
knowledge_base/tcc_processing_probe/VC/3000004
knowledge_base/tcc_processing_probe/VH/6000001
```

Method/report alignment:

```text
cmbx_data_explorer/docs/TCC_INJECTION_BY_INJECTION_REVERSE_WORKBENCH.md
cmbx_data_explorer/docs/TCC_CM_METHOD_SCRIPT_DEPENDENCY_MODEL.md
cmbx_data_explorer/docs/TCC_METHOD_REPORT_ALIGNMENT.md
knowledge_base/tcc_report_formula_objects_vh_6000001_all_sheets.tsv
knowledge_base/tcc_td_vx_c10_a_text.txt
```

Instrument configuration evidence:

```text
C:\Program Files (x86)\Thermo\Chromeleon\bin\FOQVTCC.GEN
C:\Program Files (x86)\Thermo\Chromeleon\bin\TCC100.CDD
C:\Program Files (x86)\Thermo\Chromeleon\bin\UM3_TCC.CDD
C:\Program Files (x86)\Thermo\Chromeleon\bin\QualificationTemplates\Instrument\IQ\HPLC_Templates\Checks.xml
C:\Program Files (x86)\Thermo\Chromeleon\bin\QualificationTemplates\Instrument\OQ_PQ\HPLC_Templates\Checks.xml
```

## Device Family

The TD document uses `VX-C10-A` as the family name and splits the tested modules into:

- `VA-C10-A`: Vanquish Access TCC.
- `VC-C10-A`: Vanquish Core TCC.
- `VH-C10-A`: Vanquish Horizon TCC.

Device identity for DB output must come from:

```text
AUDIT.ColumnComp.ModelNo
```

Verified sample mapping:

```text
0000003.cmbx -> VA-C10-A
3000004.cmbx -> VC-C10-A
6000001.cmbx -> VH-C10-A
```

## Report Templates

Observed template selection:

```text
VA-C10-A -> Report_VATCC_V1_01
VC-C10-A -> Report_VTCC_V2_12
VH-C10-A -> Report_VTCC_V2_12
```

Some VH packages also contain:

```text
Report_VTCC_V2_12_CIC data output
```

The standard FOQ report sheets decoded from these templates include:

```text
Definitions
Title
Test Procedures
Temp Accuracy
Temp Precision
Temp Stability_Noise
PCC
Preheater Ports_Noise
HeatUp&CoolDown
Fan
Valve_Keypad
Column ID
Liquid Leak Test
COC
FOQ VTCC History
Internal Use
Temp_Calib_Internal
Audit Trail
Error Log
```

Each decoded standard template currently exposes 234 report formula objects.

## Test Sequence Structure

TD test matrix:

```text
ColumnIDs                       VH/VC only in the TD matrix; absent from current VA sample
Preheater Connection Test        VH/VC/VA
Valve                            VH/VC/VA
VATCC_BurnIn                     VH/VC/VA
Temperature Calibration          VH/VC/VA
Temperature Accuracy             VH/VC/VA
Temperature Precision_and_Fan    VH/VC/VA
Temperature Stability_and_PCC    VH only
Temperature Stability            VC/VA
HeatUp and CoolDownTime          VH/VC/VA
Liquid Leak Test                 VH/VC/VA
Qualification_Service_Done       VH/VC/VA
Factory Default                  VH/VC/VA
```

Observed CMBX examples:

```text
VA: Valve, VTCC_BurnIn, Temperature Calibration, Temperature Accuracy_C,
    Temperature Precision, Temperature Stability_C, HeatUp and CoolDownTime,
    LiquidLeaktest, Qualification_Service_Done, Factory Default, Error Log Check

VC: ColumnIDs, Preheater Connection Test, Valve, VTCC_BurnIn,
    Temperature Calibration, Temperature Accuracy_C, Temperature Precision_and_Fan,
    Temperature Stability_C, HeatUp and CoolDownTime, LiquidLeaktest,
    Qualification_Service_Done, Factory Default, Error Log Check

VH: ColumnIDs, Preheater Connection Test, Valve, VTCC_BurnIn,
    Temperature Calibration, Temperature Accuracy_H, Temperature Precision_and_Fan,
    Temperature Stability_and_PCC_H, HeatUp and CoolDownTime, LiquidLeaktest,
    Qualification_Service_Done, Factory Default, Error Log Check
```

## Sequence Binding Blueprint

The execution target is not only a list of injections. Each injection must bind to one instrument method, and to a processing method when IRC behavior is needed.

For TCC acquisition-only generation, the minimum sequence contract is:

```text
injection name
instrument method
processing method for IRC/no-integration behavior
```

Report templates and report formulas are required for FOQ DB output and report calculation, but they are not the first blocker for running the TCC test sequence itself.

Current production samples decode as follows.

VA `0000003.cmbx`:

| Injection | Processing Method | Instrument Method |
| --- | --- | --- |
| Valve | No_Integration | VALVES |
| VTCC_BurnIn | NO_INTEGRATION | BURNIN |
| Temperature Calibration | NO_INTEGRATION | TEMPERATURE_CALIBRATION |
| Temperature Accuracy_C | ACCURACY_IRC_STOP_C | TEMPERATURE_ACCURACY |
| Temperature Precision | NO_INTEGRATION | TEMPERATURE_PRECISION |
| Temperature Stability_C | NO_INTEGRATION | TEMPERATURE_STABILITY_70_C |
| HeatUp and CoolDownTime | No_Integration | TEMP_HEAT_UP_DOWN_20_50_20 |
| LiquidLeaktest | No_Integration | LIQUID LEAK |
| Qualification_Service_Done | No_Integration | Qualification_Service_Done |
| Factory Default | No_Integration | FACTORYDEFAULT |
| Error Log Check | No_Integration | CHECKERRORLOG |

VC `3000004.cmbx`:

| Injection | Processing Method | Instrument Method |
| --- | --- | --- |
| ColumnIDs | CORRECT_ACCURACY_INJ_INSERTION | ColumnID |
| Preheater Connection Test | CORRECT_ACCURACY_INJ_INSERTION | PREHEATER |
| Valve | CORRECT_ACCURACY_INJ_INSERTION | VALVES |
| VTCC_BurnIn | NO_INTEGRATION | BURNIN |
| Temperature Calibration | CORRECT_ACCURACY_INJ_INSERTION | TEMPERATURE_CALIBRATION |
| Temperature Accuracy_C | ACCURACY_IRC_STOP_C | TEMPERATURE_ACCURACY |
| Temperature Precision_and_Fan | CORRECT_STABILITY_INJ_INSERTION | TEMPERATURE_PRECISION_AND_FAN |
| Temperature Stability_C | NO_INTEGRATION | TEMPERATURE_STABILITY_70_C |
| HeatUp and CoolDownTime | CORRECT_ACCURACY_INJ_INSERTION | TEMP_HEAT_UP_DOWN_20_50_20 |
| LiquidLeaktest | CORRECT_ACCURACY_INJ_INSERTION | LIQUID LEAK |
| Qualification_Service_Done | CORRECT_ACCURACY_INJ_INSERTION | Qualification_Service_Done |
| Factory Default | CORRECT_ACCURACY_INJ_INSERTION | FACTORYDEFAULT |
| Error Log Check | CORRECT_ACCURACY_INJ_INSERTION | CHECKERRORLOG |

VH `6000001.cmbx`:

| Injection | Processing Method | Instrument Method |
| --- | --- | --- |
| ColumnIDs | CORRECT_STABILITY_INJ_INSERTION | ColumnID |
| Preheater Connection Test | No_Integration | PREHEATER |
| Valve | No_Integration | VALVES |
| VTCC_BurnIn | NO_INTEGRATION | BURNIN |
| Temperature Calibration | CORRECT_ACCURACY_INJ_INSERTION | TEMPERATURE_CALIBRATION |
| Temperature Accuracy_H | ACCURACY_IRC_STOP_H | TEMPERATURE_ACCURACY |
| Temperature Precision_and_Fan | CORRECT_STABILITY_INJ_INSERTION | TEMPERATURE_PRECISION_AND_FAN |
| Temperature Stability_and_PCC_H | NO_INTEGRATION | TEMPERATURE_STABILITY_AND_PCC_70_H |
| HeatUp and CoolDownTime | No_Integration | TEMP_HEAT_UP_DOWN_20_50_20 |
| LiquidLeaktest | No_Integration | LIQUID LEAK |
| Qualification_Service_Done | No_Integration | Qualification_Service_Done |
| Factory Default | No_Integration | FACTORYDEFAULT |
| Error Log Check | No_Integration | CHECKERRORLOG |

Important implication: a reverse generator needs a per-device sequence blueprint. It cannot use one universal injection list and simply swap the model name.

The TD notes that Temperature Accuracy and Temperature Stability injections can be inserted by Intelligent Run Control depending on device type:

```text
Temperature Accuracy:
  VH-C10-A -> Temperature Accuracy_H
  VC-C10-A -> Temperature Accuracy_C

Temperature Stability:
  VH-C10-A -> Temperature Stability_and_PCC_H
  VC-C10-A -> Temperature Stability_C
```

The current VA sample also uses the `_C` style accuracy/stability injections.

## Processing Method Findings

Processing method objects in the tested TCC CMBX packages do not expose independent package entries in `header.xml`; their definitions are embedded in the parent sequence `.cmd` object.

The current extractor finds gzip-compressed `ProcessingMethodRootControl` XML blocks. These XML blocks are mostly Processing Method editor UI state:

```text
General tab controls
Detection settings column visibility
Peak table column visibility
SSTGrid control layout
SST column visibility, including:
  Injection Condition
  Pass Actions
  Fail Actions
  Condition_TestValueFormula_LocalizedFormula
```

Important boundary: the decoded `SSTGrid` nodes currently contain control properties and column definitions, but no SST/IRC row data. The relevant XML shape is:

```text
Item type="SSTGrid"
  Controls              # empty
  Properties
    ColumnManagment type="SSTColumnManagement"
```

Observed processing roots in production samples:

| Sample | Processing XML Roots | Notes |
| --- | ---: | --- |
| VA `0000003.cmbx` | 4 | `ACCURACY_IRC_STOP_C`, `ACCURACY_IRC_STOP_H`, `CORRECT_ACCURACY_INJ_INSERTION`, `CORRECT_STABILITY_INJ_INSERTION`; `NO_INTEGRATION` appears as references/context rather than a clearly independent root |
| VC `3000004.cmbx` | 4 | Same named root families; larger XML payloads appear where extra columns/options are enabled |
| VH `6000001.cmbx` | 4 | Same root families plus additional large compressed report/workbook-like binary sections later in the sequence command object |

Working interpretation:

- `NO_INTEGRATION` inhibits integration for all channels and has no observed data-calculation role in the FOQ DB path.
- `ACCURACY_IRC_STOP_C/H` likely carry intelligent run control behavior for accuracy injections.
- `CORRECT_ACCURACY_INJ_INSERTION` and `CORRECT_STABILITY_INJ_INSERTION` appear near sequence context that references inserted or corrected injections.
- Processing methods currently matter more for run control and sequence correction than for the report DB numeric calculations.

Reverse-generation implication:

1. Preserve processing method payloads from a golden CMBX for the same module family whenever possible.
2. Do not attempt to synthesize processing method rows from the exported XML alone.
3. Continue reverse work on the non-XML sequence command payload if IRC row reconstruction becomes required.

## Method Principles

Common setup patterns:

```text
ColumnComp.CC.ReadyTempDelta
ColumnComp.CC.EquilibrationTime
ColumnComp.CC.TempCtrl
ColumnComp.CC.Mode = StillAir
ColumnComp.LiquidLeakSensor = Off
```

Common data channels:

```text
ColumnComp.CC_Temp
ColumnComp.CC_U_Temp_Actual
ColumnComp.CC_L_Temp_Actual
ColumnComp.CC_UCTL_TempRear_Actual
ColumnComp.PWM_CCU_A
ColumnComp.PWM_CCU_B
ColumnComp.PWM_CCL_A
ColumnComp.PWM_CCL_B
ColumnComp.Fan_Rear_ActualRPM
ColumnComp.LEDBoard_LeakDiff
ColumnComp.LEDBoard_A13
ColumnComp.LEDBoard_A14
ColumnComp.Oven_Gas_MuteTimeRemain
Thermometer1.ExtTemp_UpperCC
Thermometer1.ExtTemp_LowerCC
Thermometer.Environment_Temperature
```

## Instrument Configuration Prerequisites

The instrument method can execute only when the CM instrument configuration exposes the required driver symbols. This is separate from the CMBX package structure.

Official Chromeleon qualification checks identify Vanquish TCC through:

```text
DriverID = Thermo.Vanquish.TCC
```

They also identify TCC subdevices by internal names:

```text
0:CC          -> column compartment controller
0:sCC         -> column oven temperature signal
0:PCC         -> post-column cooler
0:LowerValve  -> lower valve
0:UpperValve  -> upper valve
```

Driver evidence in `UM3_TCC.CDD` includes left/right valve type, positions, ports, and switch/error counters. The generated valve method therefore needs not only `ColumnComp`, but the actual upper/lower valve subdevices and compatible position strings.

External thermometer data is also configuration-dependent. Official OQ/PQ checks require a `TemperatureOven` channel for column oven temperature accuracy, using either analog/Integrator acquisition or a controlled thermometer/virtual channel. The FOQ TCC packages use factory-test channel names:

```text
Thermometer1.ExtTemp_UpperCC
Thermometer1.ExtTemp_LowerCC
Thermometer.Environment_Temperature
```

Generation implication: package generation needs a configuration validation gate before claiming a method is runnable in CM. See `CM_INSTRUMENT_CONFIGURATION_KNOWLEDGE_BASE.md`.

Method timing and report linkage:

- Methods write `RetTimes.RetTimeN = System.Retention`.
- Report formulas read those markers with `AUDIT.RetTimeN(1,"forward")`.
- Raw report calculations use `chm.*` formulas over the RetTime windows.
- Audit metadata and device setup are read through `AUDIT.*` and `precond.*`.

Decoded method complexity:

| Instrument Method | Key Report Events |
| --- | --- |
| `TEMPERATURE_CALIBRATION` | `RetTime1` to `RetTime8`, 8 triggers, broadest setpoint/calibration logic |
| `TEMPERATURE_ACCURACY` | `RetTime1` to `RetTime5`, model-dependent accuracy setpoints |
| `TEMP_HEAT_UP_DOWN_20_50_20` | `RetTime1` to `RetTime6`, heat/cool boundary timing |
| `PREHEATER` | `RetTime1` to `RetTime4`, left/right 45 deg C and 55 deg C events |
| `TEMPERATURE_STABILITY_AND_PCC_70_H` | initializes `RetTime1` to `RetTime4`, emits `RetTime2` to `RetTime4`; PCC timing and stability/PCC channels |
| `VALVES` | no RetTimes; audit logs of valve precision and position are the evidence |

The current decoded method flow source is:

```text
knowledge_base/tcc_reverse_probe/<VA|VC|VH>/<sequence>/<method>_embedded_method_flow.txt
```

## Temperature Tests

Burn-in:

- Purpose: first high-temperature exposure can shift compartment sensor behavior.
- TD describes repeated heating to T1 and cooling to T2 before temperature-related FOQ tests.
- Burn-in setpoints from TD:
  - VH: T1 120, T2 10.
  - VC: T1 85, T2 10.
  - VA: T1 85, T2 10.

Calibration:

- Upper and lower internal compartment sensors are calibrated individually against external thermometers.
- Calibration setpoints:
  - VH: 120 / 100 / 80 / 60 / 40 / 20 / 10 / 5.
  - VC: 85 / 70 / 55 / 40 / 30 / 20 / 10 / 5.
  - VA: 85 / 70 / 55 / 40 / 30 / 20 / 10 / 5.
- If low-temperature points cannot be reached because ambient is too high, the 20 deg C calibration parameter may be reused according to the TD rule.

Temperature Accuracy:

- Method sets model-dependent nominal temperatures.
- External upper and lower thermometer values are measured after stability.
- Report picks the sensor value with the larger absolute deviation from nominal.
- Acceptance criterion from TD: +/- 0.5 deg C.

Temperature Precision:

- Same T1 is reached three times.
- Report compares upper readings only with upper readings, lower readings only with lower readings.
- Precision is the worse of the two sensor ranges.
- Acceptance criterion from TD: <= 0.1 deg C.

Temperature Stability and Noise:

- Nominal compartment temperature is 70 deg C.
- External temperatures are measured for 15 one-minute intervals.
- Stability is the worse of upper/lower max-min ranges over the 15 averaged intervals.
- Acceptance criterion from TD: +/- 0.05 deg C, represented in report as max difference <= 0.1 deg C.
- Signal noise follows Chromeleon's detrended peak-to-peak style over the defined time range.

Heat-Up and Cool-Down:

- Temperature changes between 20 deg C and 50 deg C.
- Method includes 120 s hold periods, but report subtracts 2.0 min from heat-up and cool-down durations.
- Report uses the upper external thermometer for the final time result.
- Acceptance criterion from TD: less than 15 min for each direction.

## PCC Test

Applies only to `VH-C10-A`.

Method principle:

- PCC starts at 40 deg C.
- PCC is driven to 80 deg C.
- PCC is then driven back to 40 deg C.

Report principles:

- Cool-down performance is time from 50 deg C to 40 deg C.
- Drift is the linear regression slope from 19 min to 24 min.
- Accuracy uses average PCC temperature over 0-5, 10-15, and 19-24 min windows.
- Noise is evaluated at the end of the run.

Known acceptance criteria from TD:

```text
PCC temperature accuracy: +/- 2 deg C up to 80 deg C
PCC cool-down: less than 2.0 min from 50 deg C to 40 deg C
PCC drift: +/- 0.2 deg C/min
PCC noise: <= 0.05 deg C
```

## Preheater Connection Test

Purpose:

- Test preheater electronics with a simulator box for left and right ports.
- Check for short circuits by heating one side before the other.

Decoded method evidence:

```text
ColumnComp.CmdString Cmd="PREH.L.PID.Kp=10000"
ColumnComp.CmdString Cmd="PREH.L.PID.Ki=1200"
ColumnComp.CmdString Cmd="PREH.R.PID.Kp=10000"
ColumnComp.CmdString Cmd="PREH.R.PID.Ki=1200"
ColumnComp.PrehtLeft.TempCtrl = On
ColumnComp.PrehtRight.TempCtrl = On
ColumnComp.PrehtLeft.Temperature.Nominal = 40.00
ColumnComp.PrehtRight.Temperature.Nominal = 40.00
Wait PrehtLeft.TempReady AND PrehtRight.TempReady
```

Heat-up RetTimes:

```text
RetTime1: left reaches 45 deg C
RetTime2: right reaches 45 deg C
RetTime3: left reaches 55 deg C
RetTime4: right reaches 55 deg C
```

Report principles:

- Heat-up time is evaluated from 45 deg C to 55 deg C.
- Heater-vs-internal-sensor difference is checked at 40 deg C.
- Preheater signal noise is evaluated near the beginning of the run.

## Valve and Keypad Test

Purpose:

- Check upper and lower column switching valve electronics.
- Confirm valve movement by method.
- Confirm keypad functions by disconnecting from CM and asking the tester to press buttons.

Confirmed method write paths:

```text
ColumnComp.UpperValve.CurrentPosition = 6_1
ColumnComp.LowerValve.CurrentPosition = 6_1
ColumnComp.UpperValve.CurrentPosition = 1_2
ColumnComp.LowerValve.CurrentPosition = 1_2
Log UpperValve.Precision
Log LowerValve.Precision
```

The decoded FOQ method then prompts the user, turns acquisition off, disconnects/reconnects ColumnComp, waits for connection, and sets `ColumnComp.FastCoolActive = Off`.

For generated periodic valve cycling, the core command is the direct `CurrentPosition` property assignment; keypad/disconnect behavior is optional and requirement-specific.

## Column ID, Leak, Factory Default

Column ID:

- Uses four chip cards labeled A-D.
- Report checks that descriptions match slots A-D.
- Report formulas use paths like `AUDIT.Column_A.Description(0,"forward")`.

Liquid leak:

- Tester provokes a liquid leak.
- Report checks leak detection and liquid leak calibration value.
- Mute alarm keypad behavior is also checked.

Factory Default:

- Ensures service and qualification reminder functionality is disabled.
- Error and exception logs are cleared.
- Report also uses factory default metadata such as serial, model, model variant, hardware, and firmware.

## Report Calculation Contract

The DB output path is:

```text
DB mapping field
-> report template sheet/cell
-> direct report formula or known workbook-derived formula
-> audit/precondition/raw signal source
-> displayed/DB-formatted value
```

Important rules already implemented:

- `AUDIT.ColumnComp.ModelNo` is the device key.
- Temperature Accuracy observed/deviation cells display to 2 decimals.
- Temperature Precision and Stability pass/fail use raw precision/range, while displayed summary values use report precision.
- HeatUp/CoolDown summary values display to 1 decimal.
- PCC performance displays to 2 decimals.
- Preheater heater-temperature difference displays to 1 decimal.

## Method Command Contract

Decoded instrument method flows are now summarized into command contracts:

```text
cmbx_data_explorer/docs/TCC_METHOD_COMMAND_CONTRACTS.md
knowledge_base/tcc_method_contracts
```

These contracts record:

```text
channels acquired
RetTimes emitted
audit properties logged
wait/trigger conditions
temperature setpoints
required CM symbol roots
```

This is the preferred bridge from method execution to report and DB dependencies.

## Open Knowledge Items

1. Fully map every DB field for VA/VC/VH to its report sheet, workbook formula, and source formula.
2. Extract and compare VA, VC, and VH instrument methods, not only the current VC probe.
3. Decode processing method IRC row data beyond editor-layout XML, or define a safe golden-payload preservation strategy.
4. Build a CM configuration validation manifest for each TCC test family.
5. Expand FormulaOne workbook formula parsing beyond known FOQ-derived cells.
6. Build a method-generation schema that can emit:
   - CM-like TXT draft.
   - validated command table.
   - eventually Chromeleon-compatible method payloads, if the binary write path becomes available.

---

## Evidence: TCC_ALIGNMENT

Source file: `TCC_METHOD_REPORT_ALIGNMENT.md`

This document is the working bridge between the TCC test description, Chromeleon
instrument method commands, and report formula calculations.

The current focus is not CMBX generation. The focus is understanding what each
TCC test proves, what evidence the instrument method must create, and how the
report template turns that evidence into report or database values.

## Evidence Sources

TD:

```text
C:\ProgramData\CMBX Data Explorer Workspace\KB\FOQ TD\FOQ_Testdescription_VX-C10-A.docm
```

Golden VH package used for this pass:

```text
C:\ProgramData\CMBX Data Explorer Workspace\packages\TCC Cost Out\Zollner\Production\6000001.cmbx
```

Decoded method flows:

```text
knowledge_base/tcc_reverse_probe/VH/6000001/*_embedded_method_flow.tsv
```

Decoded VH report formula objects:

```text
knowledge_base/tcc_report_formula_objects_vh_6000001_all_sheets.tsv
```

The standard VH/VC report template in this package is:

```text
Report_VTCC_V2_12
```

## Core Pattern

The reliable reverse path is:

```text
test intent
-> instrument method command sequence
-> acquired raw channels, audit properties, and RetTimes
-> report SheetObject formula cells
-> workbook summary formulas and DB mapped fields
```

For future generation, the important object is not only the CMBX package. The
first reusable unit is a method/report contract that can be copied into CM:

```text
instrument method script section
report formula cells and workbook logic
required CM configuration symbols
```

## Shared Configuration Assumptions

Most temperature tests require:

```text
ColumnComp.CC
ColumnComp.CC_Temp
ColumnComp.CC_U_Temp_Actual
ColumnComp.CC_L_Temp_Actual
Thermometer1.ExtTemp_UpperCC
Thermometer1.ExtTemp_LowerCC
Thermometer.Environment_Temperature
```

`VH-C10-A`-only PCC calculations additionally require:

```text
ColumnComp.PCC
ColumnComp.PCC_Temp
ColumnComp.PWM_PCC_A
ColumnComp.PWM_PCC_B
```

Preheater calculations require:

```text
ColumnComp.PrehtLeft
ColumnComp.PrehtRight
ColumnComp.PrehtLeft_Temp
ColumnComp.PrehtRight_Temp
ColumnComp.PREH_L_HeaterTemp_Actual
ColumnComp.PREH_R_HeaterTemp_Actual
```

Valve calculations require:

```text
ColumnComp.UpperValve
ColumnComp.LowerValve
```

Device identity for DB alignment must come from:

```text
AUDIT.ColumnComp.ModelNo
```

## Temperature Accuracy

TD meaning:

```text
Set model-dependent column-compartment temperatures.
After both external thermometers are stable, compare external measured
temperature to the nominal setpoint. The maximum observed deviation is the
accuracy result.
```

Method evidence from `TEMPERATURE_ACCURACY`:

```text
VH setpoints:
  Variables.GenericDouble1 = 10
  Variables.GenericDouble2 = 20
  Variables.GenericDouble3 = 40
  Variables.GenericDouble4 = 80
  Variables.GenericDouble5 = 120

VC/VA setpoints:
  Variables.GenericDouble1 = 10
  Variables.GenericDouble2 = 20
  Variables.GenericDouble3 = 40
  Variables.GenericDouble4 = 60
  Variables.GenericDouble5 = 85
```

The method uses external stability variables:

```text
StabVars.TempUpperHigh = Thermometer1.ExtTemp_UpperCC + 0.05
StabVars.TempUpperLow  = Thermometer1.ExtTemp_UpperCC - 0.05
StabVars.TempLowerHigh = Thermometer1.ExtTemp_LowerCC + 0.05
StabVars.TempLowerLow  = Thermometer1.ExtTemp_LowerCC - 0.05
StabVars.CounterUpper >= 4 -> StabVars.UpperReady = 1
StabVars.CounterLower >= 4 -> StabVars.LowerReady = 1
```

The method waits for:

```text
ColumnComp.CC.TempReady AND StabVars.LowerReady AND StabVars.UpperReady
```

Then it emits RetTimes:

```text
RetTimes.RetTime1 -> first setpoint
RetTimes.RetTime2 -> second setpoint
RetTimes.RetTime3 -> third setpoint
RetTimes.RetTime4 -> fourth setpoint
RetTimes.RetTime5 -> fifth setpoint
```

For VH, `RetTime3` is therefore the 40 C accuracy anchor.

Report formula bridge on sheet `Temp Accuracy`:

```text
K66:K70 = AUDIT.RetTime1..5
L66:L70 = chm.sig_value("average", RetTimeN - 1, RetTimeN - 0.2), FixedChannel ExtTemp_LowerCC
M66:M70 = chm.sig_value("average", RetTimeN - 1, RetTimeN - 0.2), FixedChannel ExtTemp_UpperCC
I66:I70 = AUDIT.ColumnComp.CC.Temperature.Nominal(RetTimeN - 0.1)
```

Workbook/report meaning:

```text
Observed temperature = lower or upper value with larger abs(value - nominal)
Deviation = observed temperature - nominal
Pass/fail compares max absolute deviation to Definitions!Temperature Accuracy
```

Generation implication for a 40 C-only VH accuracy test:

```text
Keep the same readiness and external stability logic.
Acquire both external channels.
Write RetTimes.RetTime3 = System.Retention for the 40 C stable point.
Keep the report formulas for row 68 or create a one-point report that preserves
the same RetTime3 formula semantics.
```

## Temperature Precision and Fan

TD meaning:

```text
Reach the same temperature T1 three times. Compare the three upper external
readings to each other and the three lower external readings to each other.
The worse range is the precision result.

Fan functionality is checked separately by switching thermostatting mode and
looking for the expected direction and magnitude in CC_Temp.
```

Method evidence from `TEMPERATURE_PRECISION_AND_FAN`:

```text
ColumnComp.CC.Temperature.Nominal = 45
ColumnComp.CC.Temperature.Nominal = 50
External channels are acquired.
CC_Temp is acquired for the fan response section.
```

Report formula bridge:

```text
Temp Precision!K65 = chm.sig_value("average", 14, 14.8), ExtTemp_LowerCC
Temp Precision!K66 = chm.sig_value("average", 36, 36.8), ExtTemp_LowerCC
Temp Precision!K67 = chm.sig_value("average", 58, 58.8), ExtTemp_LowerCC
Temp Precision!L65:L67 use the same windows on ExtTemp_UpperCC
```

Workbook/report meaning:

```text
LowerRange = max(K65:K67) - min(K65:K67)
UpperRange = max(L65:L67) - min(L65:L67)
RawPrecision = max(LowerRange, UpperRange)
```

Fan formulas on sheet `Fan` use `CC_Temp` statistics around fixed time windows:

```text
average/min/max over 63.1..76 min windows
```

Generation implication:

```text
The method must reproduce the timing windows if the existing report is reused.
If a shorter generated method is desired, the report formulas must be rewritten
to the new timing anchors.
```

## Temperature Stability and Noise

TD meaning:

```text
Set CC to 70 C. Measure external upper and lower temperatures for 15 one-minute
intervals. Stability is the maximum range of the 15 averages for either sensor.
Noise is evaluated on the internal CC_Temp signal at the end of the run.
```

Report formula bridge on `Temp Stability_Noise`:

```text
K61:K75 = chm.sig_value("average", 45..60 one-minute windows), ExtTemp_LowerCC
L61:L75 = chm.sig_value("average", 45..60 one-minute windows), ExtTemp_UpperCC
K86 = chm.noise(59,60), FixedChannel CC_Temp
K87 = chm.noise(59,60), FixedChannel PCC_Temp
```

Workbook/report meaning:

```text
LowerRange = max(K61:K75) - min(K61:K75)
UpperRange = max(L61:L75) - min(L61:L75)
RawStability = max(LowerRange, UpperRange)
```

Generation implication:

```text
If using this report unchanged, the generated method must keep the 45..60 min
stability measurement window. A shorter generated method requires rewritten
stability formulas.
```

## PCC Performance, Accuracy, Drift, and Noise

TD meaning:

```text
VH only. Start PCC at 40 C, drive to 80 C, then cool to 40 C.
Report evaluates PCC cool-down from 50 C to 40 C, drift from 19 to 24 min,
accuracy over three fixed windows, and noise at the end.
```

Method evidence from `TEMPERATURE_STABILITY_AND_PCC_70_H`:

```text
ColumnComp.PCC.Temperature.Nominal = 40
ColumnComp.CC.Temperature.Nominal = 70
wait for CC.TempReady AND PCC.TempReady
trigger PCC >= 60 C -> RetTimes.RetTime2
set PCC nominal 80 C
trigger PCC <= 50 C -> RetTimes.RetTime3
trigger PCC <= 40 C -> RetTimes.RetTime4
set PCC nominal 40 C and PCC TempCtrl Off
```

Report formula bridge on `PCC`:

```text
L89 = chm.sig_value("average", 0, 5), PCC_Temp
L90 = chm.sig_value("average", 10, 15), PCC_Temp
L91 = chm.sig_value("average", 19, 24), PCC_Temp
K97 = chm.sig_value("drift", 19, 24), PCC_Temp
K105 = AUDIT.RetTime3
L105 = AUDIT.RetTime4
```

Workbook/report meaning:

```text
PCC cool-down performance = RetTime4 - RetTime3
PCC accuracy compares L89/L90/L91 to nominal values read from AUDIT.PCC.Temperature.Nominal
```

Generation implication:

```text
Only generate this branch for VH configurations with PCC symbols.
The RetTime3/RetTime4 event semantics are mandatory for the PCC cool-down cell.
```

## Heat-Up and Cool-Down

TD meaning:

```text
Measure time from 20 C to 50 C and back from 50 C to 20 C using the upper
external thermometer. The method includes 2 minute hold periods that are not
part of the final performance time.
```

Method evidence from `TEMP_HEAT_UP_DOWN_20_50_20`:

```text
Start near 17 C, then 20 C.
Trigger upper external thermometer in 19..21 C window for 120 s.
Set CC nominal to 50 C.
Trigger upper external thermometer in 49..51 C window for 120 s.
Set CC nominal back to 20 C.
Trigger upper external thermometer in 19..21 C window for 120 s.
Emit RetTimes.RetTime1..6 during the phase boundaries.
```

Report formula bridge on `HeatUp&CoolDown`:

```text
J66 = AUDIT.RetTime1
K66 = AUDIT.RetTime2
L66 = AUDIT.RetTime4
M66 = AUDIT.RetTime5
```

Current evaluator rule verified against CM export:

```text
HeatUp_Time_20to50 = RetTime2 - RetTime1 - 2.0 min
CoolDown_Time_50to20 = RetTime5 - RetTime4 - 2.0 min

The exported VTCC workbook confirms that the summary/DB route uses the row-66
external endpoint cells. RetTime3 and RetTime6 remain row-65 internal endpoint
evidence and must remain in the full method/report contract.
```

Note:

```text
The report sheet exposes both row 65 and row 66 RetTime cells. Existing CM
summary cells in the verified VH package use the row-66 style calculation.
Keep both method RetTime emissions until the workbook formula parser is fully
generalized.
```

## Preheater Ports

TD meaning:

```text
Use a preheater simulator. Heat left and right preheater ports from 40 C to
60 C. Evaluate heat-up time from 45 C to 55 C, port presence/memory state,
temperature plausibility, and signal noise.
```

Method evidence from `PREHEATER`:

```text
Set PrehtLeft and PrehtRight TempCtrl On.
Set both preheaters to 40 C and wait for PrehtLeft.TempReady AND PrehtRight.TempReady.
Acquire PrehtLeft_Temp, PrehtRight_Temp, heater temp channels, and external channels.
Set left preheater to 60 C and trigger:
  RetTime1 at left >= 45 C
  RetTime3 at left >= 55 C
Set right preheater to 60 C and trigger:
  RetTime2 at right >= 45 C
  RetTime4 at right >= 55 C
```

Report formula bridge on `Preheater Ports_Noise`:

```text
J72/J73 = AUDIT.RetTime1/2
K72/K73 = AUDIT.RetTime3/4
J82/J83 = average PrehtLeft/Right_Temp over 0.25..0.5 min
K82/K83 = average PREH_L/R_HeaterTemp_Actual over 0.25..0.5 min
J92/J93 = chm.noise(0,0.5), PrehtLeft/Right_Temp
K92/K93 = chm.noise(0,0.5), PREH_L/R_HeaterTemp_Actual
J117/J118 = precond ColumnComp.PrehtLeft/Right.ModulePresent
K117/K118 = precond ColumnComp.PrehtLeft/Right.MemoryState
```

Generation implication:

```text
The generated method must expose RetTime1..4 with left/right 45/55 C meaning.
The report must preserve the left/right mapping; swapping RetTimes changes the
port result.
```

## Valve and Keypad

TD meaning:

```text
Switch upper and lower valves from 6_1 to 1_2 and back by instrument method.
Evaluate valve precision and audit trail position changes. Then disconnect the
device so the tester can press keypad buttons.
```

Method evidence from `VALVES`:

```text
ColumnComp.UpperValve.CurrentPosition = 6_1
ColumnComp.LowerValve.CurrentPosition = 6_1
Log UpperValve.Precision
Log LowerValve.Precision
ColumnComp.UpperValve.CurrentPosition = 1_2
ColumnComp.LowerValve.CurrentPosition = 1_2
Log UpperValve.Precision
Log LowerValve.Precision
ColumnComp.UpperValve.CurrentPosition = 6_1
ColumnComp.LowerValve.CurrentPosition = 6_1
Log UpperValve.Precision
Log LowerValve.Precision
Wait ColumnComp.Connected = Connected after keypad section
```

Report formula bridge on `Valve_Keypad`:

```text
K49:K51 = AUDIT.UpperValve.CurrentPosition at fixed early times
L49:L51 = AUDIT.LowerValve.CurrentPosition at fixed early times
U49:U51 = AUDIT.UpperValve.Precision at matching times
V49:V51 = AUDIT.LowerValve.Precision at matching times
K60/L60/N60 = keypad-related position and FastCool audit state around 0.9 min
```

Generation implication:

```text
Valve generation is primarily audit-driven. It does not need RetTimes, but the
timing of position changes must still match the report's fixed-time audit reads
unless the report formulas are rewritten.
```

## Column ID

TD meaning:

```text
Verify that column ID tags A, B, C, and D are detected in the correct slots.
```

Method evidence from `ColumnID`:

```text
Wait Column_A.CardState=OK AND Column_B.CardState=OK AND Column_C.CardState=OK AND Column_D.CardState=OK
```

Report formula bridge on `Column ID`:

```text
L46 = AUDIT.Column_A.Description(0,"forward")
L47 = AUDIT.Column_B.Description(0,"forward")
L48 = AUDIT.Column_C.Description(0,"forward")
L49 = AUDIT.Column_D.Description(0,"forward")
```

Workbook/report meaning:

```text
Slot A passes if L46 == "A"
Slot B passes if L47 == "B"
Slot C passes if L48 == "C"
Slot D passes if L49 == "D"
```

## Liquid Leak

TD meaning:

```text
Prompt tester to provoke a leak. The leak sensor must enter Leak state.
Tester mutes the alarm and cleans the compartment.
```

Method evidence from `LIQUID LEAK`:

```text
Sets CC nominal around 20 C.
Acquires CC/leak-related channels.
Waits for LiquidLeak=Leak with timeout.
Checks ColumnComp.Alarm = NoAlarm after mute/cleanup.
```

Report formula bridge on `Liquid Leak Test`:

```text
K47 = precond.LiquidLeakCalibrationValue
M47 = AUDIT.LiquidLeak(100.000,"backward")
```

Generation implication:

```text
This test has an unavoidable manual action. The report is mostly audit/precond
based, not raw-temperature based.
```

## Factory Default and Qualification Service

TD meaning:

```text
Qualification service updates qualification/service properties.
Factory default confirms service/qualification reminders and logs/exceptions are
cleared or disabled according to current FOQ rules.
```

Report bridge:

```text
Definitions and Internal Use sheets read precond metadata such as:
  precond.ColumnComp.SerialNo
  precond.ColumnComp.FirmwareVersion
  precond.ColumnComp.HardwareVersion
  precond.ColumnComp.ModuleHardwareRevision

Definitions!C15 reads:
  AUDIT.ColumnComp.ModelNo
```

Generation implication:

```text
These injections are metadata/audit oriented. They are important for a full FOQ
sequence but are not a good first target for semantic method synthesis.
```

## What This Means For Method/Report Generation

When the request is:

```text
VH TCC temperature accuracy at 40 C only
```

the generated method/report pair should not simply copy the full accuracy
method unchanged. The method can be reduced, but it must preserve:

```text
VH configuration validation through ColumnComp.ModelNo
CC setup and TempCtrl
PCC TempCtrl disable for VH if the symbol exists
external thermometer acquisition
external stability trigger/counter logic
40 C nominal setpoint
RetTimes.RetTime3 = System.Retention as the stable 40 C anchor
return to a benign final temperature such as 20 C
```

The corresponding report can take either of two safe shapes:

```text
Option A: reuse the existing Temp Accuracy sheet and only trust row 68.
Option B: create a one-point report sheet where nominal, lower average, upper
average, observed value, deviation, and pass/fail all reference RetTime3.
```

Option B is cleaner for generated single-test artifacts, but it requires us to
copy or recreate the report workbook style and formulas directly in CM.

## Open Reverse Tasks

- Extract workbook formulas, not only SheetObject formulas, for each report
  sheet summary/pass-fail cell.
- Build a reusable CM-script template language that keeps RetTime semantics
  explicit.
- Separate fixed-time report formulas from RetTime-anchored report formulas.
- Confirm VA/VC sheet formula differences against `Report_VATCC_V1_01` and
  `Report_VTCC_V2_12`.
- Build copy-ready method-script snippets for the first generated pair:
  `VH-C10-A / Temperature Accuracy / 40 C`.

---

## Evidence: VALVE_PRESSURE_CONTRACT

Source file: `VALVE_SHIFT_SYNCHRON_PRESSURE_EVALUATION_REPORT_CONTRACT.md`

**Purpose:** Define the verified method, processing, virtual-channel, and report-table contract for a GPT-authored valve-pressure test report.

## 1. Evidence Scope

| Role | Source | Verified object |
|---|---|---|
| Complete sequence | `EP01_6_2_valves.cmbx` | Six valve-test injections, ten instrument methods, `PressureSpikeEval`, and three report templates |
| Standalone report carrier | `PressureEvaluation.cmbx` | `PressureEvaluation` |
| Processing method | `EP01_6_2_valves.cmbx` | `PressureSpikeEval` |
| Related method family | `EP01_6_2_valves.cmbx` | `Synchron*` and `Asynchron*` |

Do not confuse this report with `PressureEvaluation Vanquish` in the same sequence. They are different templates with different sheets, sources, and layouts.

## 2. Verified Execution Contract

Every observed `Synchron*` / `Asynchron*` method contains these Start Run requirements:

| Method command | Verified value | Why the report needs it |
|---|---|---|
| `PumpModule.Pump.Pump_Pressure.AcqOn` | enabled | Acquires the raw pressure source. |
| `VirtualChannel` | `"PumpPressureVirtual", PumpModule.Pump.Pump_Pressure.Signal, Type=Digital, Unit="bar", Evaluate=Yes` | Exposes the pressure signal as an integrable/evaluable channel. |
| `ColumnComp.CC_Temp.AcqOn` | enabled | Method evidence only; not a direct `PressureEvaluation` table source. |
| `Thermometer.Lab_Temperature.AcqOn` | enabled | Method evidence only; not a direct `PressureEvaluation` table source. |

The virtual channel is essential: the pressure source is acquired first, then `PumpPressureVirtual` makes it available to the peak/integration result context used by the report table. A method variant must preserve this exact virtual-channel name, source expression, type, unit, and `Evaluate=Yes` unless its report table is redesigned too.

The selected injections are bound to `PressureSpikeEval`. The current decoder verifies that this processing method contains the Chromeleon processing-method/SST-IRC structure, but does not yet decode its business rows. For this report, the operational requirement is that it produces integration results for `PumpPressureVirtual`.

## 3. Verified Dynamic Report Table

`PressureEvaluation` contains **one active sheet only**:

| Sheet | Range | Object | Table type | Runtime source |
|---|---|---|---|---|
| `Sheet2` | `A1:H43` | `ReportTableObject` | `integration` | Processed peaks on `PumpPressureVirtual` |

The table definition is dynamic. It contains table headers and a column schema in the template, while its body has no static peak rows before report evaluation. This is normal. Chromeleon populates rows after `PressureSpikeEval` has generated compatible peak/integration results.

| Visible result | Formula source in table definition | Context |
|---|---|---|
| No. | `peak.number` | Peak enumeration |
| Retention Time | `peak.retention_time("detected")*60` | Seconds; virtual pressure channel |
| Peak Start | `peak.start_time*60` | Seconds; virtual pressure channel |
| Valve Switching Time | `(peak.retention_time("detected")-(peak.start_time))*60*1000` | Milliseconds; virtual pressure channel |
| PeakMaxPressureEnhancement | `peak.height` | Pressure-unit result |
| UpperValvePosition | `audit.ColumnComp.UpperValve.CurrentPosition` | Valve audit at peak context |
| LowerValvePosition | `audit.ColumnComp.LowerValve.CurrentPosition` | Valve audit at peak context |
| Flow.Nominal | `audit.PumpModule.Pump.Flow.Nominal` | Pump audit at peak context |

## 4. What a GPT-Generated Report MD Can Implement Now

### Supported: clone and preserve

A GPT-generated MD can select `PressureEvaluation.cmbx` as its carrier and declare the dynamic table as preserved:

````markdown
### Dynamic Report Table: Sheet2!A1:H43
```yaml
object_type: ReportTableObject
operation: preserve
table_type: integration
runtime_source: peak results on PumpPressureVirtual
required_virtual_channel:
  name: PumpPressureVirtual
  source_expression: PumpModule.Pump.Pump_Pressure.Signal
  type: Digital
  unit: bar
  evaluate: true
required_processing_method: PressureSpikeEval
```
````

The current report compiler preserves this table and its FormulaOne layout unchanged. If the generated method preserves the virtual channel and compatible integration behaviour, Chromeleon can populate the table at report runtime.

### Not yet supported: table redesign

The current compiler cannot create a new `ReportTableObject`, alter its pipe-delimited column schema, add/remove/reorder columns, alter its body range, or author its FormulaOne layout. These requests require a CM-created before/after control pair and remain `OPEN VERIFICATION REQUIRED`.

## 5. Generation Preconditions

1. Acquire `PumpModule.Pump.Pump_Pressure` for the entire required run.
2. Create `PumpPressureVirtual` exactly as observed, before processing/integration needs it.
3. Bind a processing method demonstrated to integrate that virtual channel; currently `PressureSpikeEval` is the evidence-backed choice.
4. Keep the valve audit paths used by the table, or redesign the table only after a validated schema write rule exists.
5. Ensure run duration and switching behaviour produce peaks compatible with the processing method; preserving the table alone cannot manufacture peak rows.

## 6. Web-GPT Evidence Packet Rule

For web GPT, provide this document, the formula inventory generated from `PressureEvaluation.cmbx`, and the relevant method MD/library. The binary CMBX files stay local. A generated report MD must never claim that the dynamic body will populate unless all five generation preconditions are stated as satisfied.
