# TCC Required Symbol Manifest

This document is the first configuration-validation manifest for TCC reverse generation. It converts decoded TCC instrument-method flow into capability groups that can be checked before generating or running a CMBX package.

## Scope

Evidence source:

```text
knowledge_base/tcc_reverse_probe/<VA|VC|VH>/<sequence>/<method>_embedded_method_flow.tsv
```

Important distinction:

- The CMBX method library may contain methods that are not used by the current sequence.
- A runnable generated sequence only needs the symbols required by the injections it actually binds.
- A complete reusable method library needs the union of all symbols in this manifest.

All three representative production packages contain 14 decoded instrument methods:

```text
BURNIN
CHECKERRORLOG
ColumnID
FACTORYDEFAULT
LIQUID LEAK
PREHEATER
QUALIFICATION_SERVICE_DONE
TEMP_HEAT_UP_DOWN_20_50_20
TEMPERATURE_ACCURACY
TEMPERATURE_CALIBRATION
TEMPERATURE_PRECISION / TEMPERATURE_PRECISION_AND_FAN
TEMPERATURE_STABILITY_70_C
TEMPERATURE_STABILITY_AND_PCC_70_H
VALVES
```

The sequence blueprint decides which of these methods are actually used for VA, VC, and VH.

## Core TCC Capability

Required by almost every TCC FOQ method:

```text
ColumnComp
ColumnComp.ModelNo
ColumnComp.CC
ColumnComp.CC.TempCtrl
ColumnComp.CC.Mode
ColumnComp.CC.ReadyTempDelta
ColumnComp.CC.EquilibrationTime
ColumnComp.CC.TempReady
ColumnComp.CC.Temperature.Nominal
ColumnComp.CC_Temp
System.Retention
System.Trigger
System.AbortQueue
```

Common internal raw channels:

```text
ColumnComp.CC_Temp
ColumnComp.CC_U_Temp_Actual
ColumnComp.CC_L_Temp_Actual
ColumnComp.CC_UCTL_TempRear_Actual
ColumnComp.Fan_Rear_ActualRPM
ColumnComp.LEDBoard_A13
ColumnComp.LEDBoard_A14
ColumnComp.LEDBoard_LeakDiff
ColumnComp.PWM_CCU_A
ColumnComp.PWM_CCU_B
ColumnComp.PWM_CCL_A
ColumnComp.PWM_CCL_B
ColumnComp.Oven_Gas_MuteTimeRemain
```

The decoded methods use `.AcqOn`, `.AcqOff`, and `.Data_Collection_Rate` on many of these channels.

## External Thermometer Capability

Required by temperature accuracy, precision, stability, heat-up/cool-down, preheater, and liquid leak methods:

```text
Thermometer1.ExtTemp_UpperCC
Thermometer1.ExtTemp_LowerCC
Thermometer.Environment_Temperature
```

Observed method operations:

```text
Thermometer1.ExtTemp_UpperCC.AcqOn
Thermometer1.ExtTemp_UpperCC.AcqOff
Thermometer1.ExtTemp_LowerCC.AcqOn
Thermometer1.ExtTemp_LowerCC.AcqOff
Thermometer.Environment_Temperature.AcqOn
Thermometer.Environment_Temperature.AcqOff
```

Report dependency:

```text
FixedChannel = ExtTemp_UpperCC
FixedChannel = ExtTemp_LowerCC
```

Configuration note: official Chromeleon qualification checks also refer to `TemperatureOven` or an external/manual thermometer path. FOQ TCC uses the more specific factory-test channel names above.

## Method Capability Matrix

| Method | Core TCC | External Thermometers | RetTimes | Special Capability |
| --- | --- | --- | --- | --- |
| `BURNIN` | yes | yes | no report RetTimes observed | broad internal channel acquisition, `ColumnComp.CmdString`, PCC off command seen in some variants |
| `TEMPERATURE_CALIBRATION` | yes | yes | `RetTime1`-`RetTime8` | writes CC calibration point/deviation properties |
| `TEMPERATURE_ACCURACY` | yes | yes | `RetTime1`-`RetTime5` | stabilization variables and model-dependent setpoints |
| `TEMPERATURE_PRECISION` / `TEMPERATURE_PRECISION_AND_FAN` | yes | yes | no direct RetTimes in decoded flow summary | fan/internal PWM/leak channels; precision is report-derived from external readings |
| `TEMPERATURE_STABILITY_70_C` | yes | yes | no direct RetTimes in decoded flow summary | 70 deg C stability/noise acquisition |
| `TEMP_HEAT_UP_DOWN_20_50_20` | yes | yes | `RetTime1`-`RetTime6` | heat/cool timing from 20/50 deg C boundaries |
| `TEMPERATURE_STABILITY_AND_PCC_70_H` | yes | yes | emits `RetTime2`-`RetTime4`; initializes `RetTime1` | PCC subdevice and PCC raw channels |
| `PREHEATER` | yes | yes | `RetTime1`-`RetTime4` | left/right preheater subdevices and heater channels |
| `VALVES` | yes | no | no | upper/lower valve subdevices, keypad disconnect/reconnect behavior |
| `ColumnID` | yes | no | no | column chip/card properties for A-D slots |
| `LIQUID LEAK` | yes | yes | may log `System.Retention` events | leak sensor, alarm, mute/alarm channels |
| `FACTORYDEFAULT` | yes | no | no | service/wellness/qualification and log-clear commands |
| `CHECKERRORLOG` | partial | no | no | connect/disconnect and error-log context |
| `QUALIFICATION_SERVICE_DONE` | partial | no | no | wellness service/qualification done properties |

## Special Capability Groups

### PCC

Required by `TEMPERATURE_STABILITY_AND_PCC_70_H` and any VH PCC performance/report generation:

```text
ColumnComp.PCC
ColumnComp.PCC.TempCtrl
ColumnComp.PCC.TempReady
ColumnComp.PCC.Temperature.Nominal
ColumnComp.PCC_Temp
ColumnComp.PWM_PCC_A
ColumnComp.PWM_PCC_B
```

Official qualification checks identify PCC through `InternalName = 0:PCC`.

### Preheater

Required by `PREHEATER`:

```text
ColumnComp.PrehtLeft
ColumnComp.PrehtRight
ColumnComp.PrehtLeft.TempCtrl
ColumnComp.PrehtRight.TempCtrl
ColumnComp.PrehtLeft.ReadyTempDelta
ColumnComp.PrehtRight.ReadyTempDelta
ColumnComp.PrehtLeft.EquilibrationTime
ColumnComp.PrehtRight.EquilibrationTime
ColumnComp.PrehtLeft.Temperature.Nominal
ColumnComp.PrehtRight.Temperature.Nominal
ColumnComp.PrehtLeft_Temp
ColumnComp.PrehtRight_Temp
ColumnComp.PREH_L_Temp_Actual
ColumnComp.PREH_R_Temp_Actual
ColumnComp.PREH_L_HeaterTemp_Actual
ColumnComp.PREH_R_HeaterTemp_Actual
ColumnComp.PWM_LeftPreh
ColumnComp.PWM_RightPreh
```

Decoded command-string parameters:

```text
PREH.L.PID.Kp
PREH.L.PID.Ki
PREH.R.PID.Kp
PREH.R.PID.Ki
```

### Upper/Lower Valves

Required by `VALVES`:

```text
ColumnComp.UpperValve.CurrentPosition
ColumnComp.LowerValve.CurrentPosition
UpperValve.Precision
LowerValve.Precision
ColumnComp.Connect
ColumnComp.Disconnect
ColumnComp.Connected
ColumnComp.FastCoolActive
```

Verified position values in FOQ:

```text
6_1
1_2
```

Official qualification checks identify these subdevices through:

```text
InternalName = 0:UpperValve
InternalName = 0:LowerValve
```

### Column ID

Required by `ColumnID` and report Column ID checks:

```text
Column_A.CardState
Column_A.Description
Column_B.CardState
Column_B.Description
Column_C.CardState
Column_C.Description
Column_D.CardState
Column_D.Description
```

Report formulas use audit paths:

```text
AUDIT.Column_A.Description(0,"forward")
AUDIT.Column_B.Description(0,"forward")
AUDIT.Column_C.Description(0,"forward")
AUDIT.Column_D.Description(0,"forward")
```

### Leak Test

Required by `LIQUID LEAK`:

```text
ColumnComp.LiquidLeakSensor
ColumnComp.LiquidLeakSensorCalibrate
ColumnComp.Alarm
ColumnComp.LEDBoard_LeakDiff
ColumnComp.Oven_Gas_MuteTimeRemain
```

The method also uses `ColumnComp.CmdString` and LED/alarm-related behavior.

### Factory Default / Service

Required by `FACTORYDEFAULT` and `QUALIFICATION_SERVICE_DONE`:

```text
ColumnComp.ColumnComp_Wellness.Qualification.Interval
ColumnComp.ColumnComp_Wellness.Qualification.WarningPeriod
ColumnComp.ColumnComp_Wellness.Qualification.GracePeriod
ColumnComp.ColumnComp_Wellness.Service.Interval
ColumnComp.ColumnComp_Wellness.Service.WarningPeriod
ColumnComp.ColumnComp_Wellness.Workload_CC
ColumnComp.ColumnComp_Wellness.QualificationDone
ColumnComp.ColumnComp_Wellness.ServiceDone
ColumnComp.ExceptionLogClear
ColumnComp.GetServiceCode
ColumnComp.ServiceCode
ErrorLog.Clear
```

Report metadata also depends on:

```text
AUDIT.ColumnComp.SerialNo
AUDIT.ColumnComp.ModelNo
AUDIT.ColumnComp.FirmwareVersion
AUDIT.ColumnComp.HardwareVersion
AUDIT.ColumnComp.ModuleHardwareRevision
```

## Device-Specific Validation

### VA-C10-A

Observed production sequence does not include `ColumnIDs` or `Preheater Connection Test`, but the package method library still contains `ColumnID` and `PREHEATER` payloads.

Sequence-level validation should follow the actual VA blueprint:

```text
VALVES
BURNIN
TEMPERATURE_CALIBRATION
TEMPERATURE_ACCURACY
TEMPERATURE_PRECISION
TEMPERATURE_STABILITY_70_C
TEMP_HEAT_UP_DOWN_20_50_20
LIQUID LEAK
QUALIFICATION_SERVICE_DONE
FACTORYDEFAULT
CHECKERRORLOG
```

### VC-C10-A

Observed production sequence includes Column ID, preheater, valve, temperature, leak, service, factory-default, and error-log checks.

VC does not require PCC for the current FOQ stability sequence.

### VH-C10-A

Observed production sequence includes PCC-capable method payloads and uses `Temperature Stability_and_PCC_H`.

VH validation must include PCC when generating the full FOQ sequence:

```text
ColumnComp.PCC
ColumnComp.PCC.TempCtrl
ColumnComp.PCC_Temp
ColumnComp.PWM_PCC_A
ColumnComp.PWM_PCC_B
```

## Manifest Implementation Direction

The first validator can run against a loaded CMBX package:

1. Use `AUDIT.ColumnComp.ModelNo` to identify VA/VC/VH.
2. Read the selected sequence blueprint and method links.
3. Build the union of required capability groups for those methods.
4. Check package channels and audit/precondition evidence for matching symbols.
5. Emit warnings for capabilities that cannot be proven from the CMBX.

The later CM-connected validator should run against live Chromeleon instrument configuration before package generation, because some capabilities are configuration-only and may not be fully represented by a completed CMBX.

The first machine-readable draft and validation notes are:

```text
knowledge_base/tcc_required_symbol_manifest.json
knowledge_base/tcc_required_symbol_validation_20260708.md
```
