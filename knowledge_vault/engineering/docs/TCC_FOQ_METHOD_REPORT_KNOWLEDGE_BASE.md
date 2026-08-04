# TCC FOQ Method and Report Knowledge Base

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
