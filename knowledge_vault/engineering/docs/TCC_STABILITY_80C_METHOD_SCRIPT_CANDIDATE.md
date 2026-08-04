# TCC Stability at 80C - Method Script Candidate

Date: 2026-07-13

Purpose: candidate method-script review for a custom TCC test intent:

```text
stability at 80C
```

Interpretation used here:

```text
Measure CC temperature stability at 80C using the existing TCC stability method role.
```

Important distinction:

- `VC-C10-A` / `VA-C10-A`: clone `TEMPERATURE_STABILITY_70_C`.
- `VH-C10-A`: clone `TEMPERATURE_STABILITY_AND_PCC_70_H`, but only change the CC stability setpoint from 70C to 80C. The PCC 40/80/40 branch is left unchanged unless the requested intent explicitly asks to modify PCC.

## 1. Method Role Map

| Role | Existing stability method evidence | 80C candidate decision |
|---|---|---|
| Model/page guard | `Variables.GenericLong9` branch by `ColumnComp.ModelNo` | Keep unchanged |
| Readiness definition | `ColumnComp.CC.ReadyTempDelta = 0.05 [C]`; `EquilibrationTime = 0.5 [min]` | Keep unchanged |
| CC temperature control | `ColumnComp.CC.TempCtrl = On`, `ColumnComp.CC.Mode = StillAir` | Keep unchanged |
| Stability target | `ColumnComp.CC.Temperature.Nominal = 70.0` | Change to `80.0` |
| Acquisition channels | `CC_Temp`, CC actual/PWM/fan channels, external thermometers, environment, leak diagnostics | Keep unchanged |
| Measurement window | Report uses 45..60 min and 59..60 min windows | Keep original run length unless report is rewritten |
| PCC branch, VH only | PCC setpoints `40 -> 80 -> 40`; RetTimes 2..4 | Keep unchanged unless target is PCC stability/performance |

## 2. Minimal Change Summary

### 2.1 VC/VA Non-PCC Method

Template:

```text
TEMPERATURE_STABILITY_70_C
```

Candidate:

```text
TEMPERATURE_STABILITY_80_C
```

Only required command-value change:

| Stage | Command | Original value | Candidate value | Reason |
|---|---|---:|---:|---|
| Equilibration | `ColumnComp.CC.Temperature.Nominal` | `70.0` | `80.0` | Change CC stability target temperature |

### 2.2 VH PCC Method

Template:

```text
TEMPERATURE_STABILITY_AND_PCC_70_H
```

Candidate:

```text
TEMPERATURE_STABILITY_AND_PCC_80_H`
```

Required command-value change for CC stability:

| Stage | Command | Original value | Candidate value | Reason |
|---|---|---:|---:|---|
| Equilibration | `ColumnComp.CC.Temperature.Nominal` | `70.0` | `80.0` | Change CC stability target temperature |

Do not change these PCC commands for a CC stability-only intent:

| Stage | Command | Existing value | Reason |
|---|---|---:|---|
| Equilibration | `ColumnComp.PCC.Temperature.Nominal` | `40.00` | PCC initial reference state |
| Run | `ColumnComp.PCC.Temperature.Nominal` | `80.0 [C]` | PCC heat-up/performance branch |
| Run | `ColumnComp.PCC.Temperature.Nominal` | `40.0 [C]` | PCC cool-down/end state |

## 3. Candidate Method Flow - VC/VA

```text
Embedded Instrument Method Flow: TEMPERATURE_STABILITY_80_C
Source basis: TEMPERATURE_STABILITY_70_C

[Stage] InstrumentSetup
# =========================================================================================
# IM to measure the temperature stability of the Vanquish VC-C10-A / VA-C10-A at 80C
# =========================================================================================
# HPLC-System:
# -----------
# VC-C10-A or VA-C10-A

[Stage] Equilibration
# Different total pages counts are used for VH-C10-A and VC-C10-A (no PCC). This is set here
IF
  IF Variables.GenericLong9 12 [Val_FOQ_CM7_ekugelma_07-Jul-2020]: OK Delay 1 Log GenericLong9 ColumnComp.ModelNo="VH-C10-A"
    SET Variables.GenericLong9 = 12
    RUN Delay 1
    RUN Log GenericLong9
  SET Variables.GenericLong9 = 10
  RUN Delay 1
  RUN Log GenericLong9
  else
    RUN Message "Column compartment model unknown, please reinspect in production!"
    RUN System.AbortQueue

# Parameters valid for the whole test.
SET ColumnComp.CC.ReadyTempDelta = 0.05 [C]
SET ColumnComp.CC.EquilibrationTime = 0.5 [min]
SET ColumnComp.CC.TempCtrl = On
SET ColumnComp.CC.Mode = StillAir

# Settings for all channels offered for the column compartment by the driver.
SET ColumnComp.CC_U_Temp_Actual.Data_Collection_Rate = 20
SET ColumnComp.CC_L_Temp_Actual.Data_Collection_Rate = 20
SET ColumnComp.CC_UCTL_TempRear_Actual.Data_Collection_Rate = 20
SET ColumnComp.PWM_CCU_A.Data_Collection_Rate = 20
SET ColumnComp.PWM_CCU_B.Data_Collection_Rate = 20
SET ColumnComp.PWM_CCL_A.Data_Collection_Rate = 20
SET ColumnComp.PWM_CCL_B.Data_Collection_Rate = 20
SET ColumnComp.Fan_Rear_ActualRPM.Data_Collection_Rate = 20
SET ColumnComp.LEDBoard_LeakDiff.Data_Collection_Rate = 20
SET ColumnComp.LEDBoard_A13.Data_Collection_Rate = 20
SET ColumnComp.LEDBoard_A14.Data_Collection_Rate = 20
SET ColumnComp.Oven_Gas_MuteTimeRemain.Data_Collection_Rate = 20

# Start Temperature
SET ColumnComp.CC.Temperature.Nominal = 80.0

[Stage] InjectPreparation
RUN Wait CC.TempReady

[Stage] StartRun
RUN ColumnComp.CC_Temp.AcqOn
RUN ColumnComp.CC_U_Temp_Actual.AcqOn
RUN ColumnComp.CC_L_Temp_Actual.AcqOn
RUN ColumnComp.CC_UCTL_TempRear_Actual.AcqOn
RUN ColumnComp.PWM_CCU_A.AcqOn
RUN ColumnComp.PWM_CCU_B.AcqOn
RUN ColumnComp.PWM_CCL_A.AcqOn
RUN ColumnComp.PWM_CCL_B.AcqOn
RUN ColumnComp.Fan_Rear_ActualRPM.AcqOn
RUN Thermometer1.ExtTemp_UpperCC.AcqOn
RUN Thermometer1.ExtTemp_LowerCC.AcqOn
RUN Thermometer.Environment_Temperature.AcqOn
RUN ColumnComp.LEDBoard_LeakDiff.AcqOn
RUN ColumnComp.LEDBoard_A13.AcqOn
RUN ColumnComp.LEDBoard_A14.AcqOn
RUN ColumnComp.Oven_Gas_MuteTimeRemain.AcqOn

[Stage] Run
# Hold/acquire long enough for report windows 45..60 min and 59..60 min.

[Stage] StopRun
RUN ColumnComp.CC_Temp.AcqOff
RUN ColumnComp.CC_U_Temp_Actual.AcqOff
RUN ColumnComp.CC_L_Temp_Actual.AcqOff
RUN ColumnComp.CC_UCTL_TempRear_Actual.AcqOff
RUN ColumnComp.PWM_CCU_A.AcqOff
RUN ColumnComp.PWM_CCU_B.AcqOff
RUN ColumnComp.PWM_CCL_A.AcqOff
RUN ColumnComp.PWM_CCL_B.AcqOff
RUN ColumnComp.Fan_Rear_ActualRPM.AcqOff

[Stage] PostRun
RUN Thermometer1.ExtTemp_UpperCC.AcqOff
RUN Thermometer1.ExtTemp_LowerCC.AcqOff
RUN Thermometer.Environment_Temperature.AcqOff
RUN ColumnComp.LEDBoard_LeakDiff.AcqOff
RUN ColumnComp.LEDBoard_A13.AcqOff
RUN ColumnComp.LEDBoard_A14.AcqOff
RUN ColumnComp.Oven_Gas_MuteTimeRemain.AcqOff

[End]
```

## 4. Candidate Method Flow - VH

```text
Embedded Instrument Method Flow: TEMPERATURE_STABILITY_AND_PCC_80_H
Source basis: TEMPERATURE_STABILITY_AND_PCC_70_H

[Stage] InstrumentSetup
# =========================================================================================
# IM to measure the temperature stability of the Vanquish VH-C10-A at 80C
# =========================================================================================
# HPLC-System:
# -----------
# VH-C10-A

[Stage] Equilibration
IF
  IF Variables.GenericLong9 12 [Val_FOQ_CM7_ekugelma_07-Jul-2020]: OK Delay 1 Log GenericLong9 ColumnComp.ModelNo="VH-C10-A"
    SET Variables.GenericLong9 = 12
    RUN Delay 1
    RUN Log GenericLong9
  SET Variables.GenericLong9 = 10
  RUN Delay 1
  RUN Log GenericLong9
  else
    RUN Message "Column compartment model unknown, please reinspect in production!"
    RUN System.AbortQueue

SET ColumnComp.CC.ReadyTempDelta = 0.05 [C]
SET ColumnComp.CC.EquilibrationTime = 0.5 [min]
SET ColumnComp.CC.TempCtrl = On
SET ColumnComp.PCC.TempCtrl = On
SET ColumnComp.CC.Mode = StillAir
SET Variables.GenericBool1 = 0
SET Variables.GenericBool2 = 0
SET RetTimes.RetTime1 = 0
SET RetTimes.RetTime2 = 0
SET RetTimes.RetTime3 = 0
SET RetTimes.RetTime4 = 0

# Post Column Cooler settings.
SET ColumnComp.PCC.Temperature.Nominal = 40.00

# Column compartment and PCC diagnostic channel rates.
SET ColumnComp.CC_U_Temp_Actual.Data_Collection_Rate = 20
SET ColumnComp.CC_L_Temp_Actual.Data_Collection_Rate = 20
SET ColumnComp.CC_UCTL_TempRear_Actual.Data_Collection_Rate = 20
SET ColumnComp.PWM_CCU_A.Data_Collection_Rate = 20
SET ColumnComp.PWM_CCU_B.Data_Collection_Rate = 20
SET ColumnComp.PWM_CCL_A.Data_Collection_Rate = 20
SET ColumnComp.PWM_CCL_B.Data_Collection_Rate = 20
SET ColumnComp.Fan_Rear_ActualRPM.Data_Collection_Rate = 20
SET ColumnComp.PWM_PCC_A.Data_Collection_Rate = 20
SET ColumnComp.PWM_PCC_B.Data_Collection_Rate = 20
SET ColumnComp.LEDBoard_LeakDiff.Data_Collection_Rate = 20
SET ColumnComp.LEDBoard_A13.Data_Collection_Rate = 20
SET ColumnComp.LEDBoard_A14.Data_Collection_Rate = 20
SET ColumnComp.Oven_Gas_MuteTimeRemain.Data_Collection_Rate = 20

# Start Temperature for CC stability
SET ColumnComp.CC.Temperature.Nominal = 80.0

[Stage] InjectPreparation
RUN Wait CC.TempReady AND PCC.TempReady

[Stage] StartRun
RUN ColumnComp.CC_Temp.AcqOn
RUN ColumnComp.CC_U_Temp_Actual.AcqOn
RUN ColumnComp.CC_L_Temp_Actual.AcqOn
RUN ColumnComp.CC_UCTL_TempRear_Actual.AcqOn
RUN ColumnComp.PWM_CCU_A.AcqOn
RUN ColumnComp.PWM_CCU_B.AcqOn
RUN ColumnComp.PWM_CCL_A.AcqOn
RUN ColumnComp.PWM_CCL_B.AcqOn
RUN ColumnComp.Fan_Rear_ActualRPM.AcqOn
RUN ColumnComp.PCC_Temp.AcqOn
RUN ColumnComp.PWM_PCC_A.AcqOn
RUN ColumnComp.PWM_PCC_B.AcqOn
RUN Thermometer1.ExtTemp_UpperCC.AcqOn
RUN Thermometer1.ExtTemp_LowerCC.AcqOn
RUN Thermometer.Environment_Temperature.AcqOn
RUN ColumnComp.LEDBoard_LeakDiff.AcqOn
RUN ColumnComp.LEDBoard_A13.AcqOn
RUN ColumnComp.LEDBoard_A14.AcqOn
RUN ColumnComp.Oven_Gas_MuteTimeRemain.AcqOn

[Stage] Run
# PCC branch retained from original VH method.
RUN System.Trigger "T60UP", PCC.Temperature.Value>=60.0, Limit=1, Hysteresis=5.0 [%], AllowImmediateExecution=No
SET RetTimes.RetTime2 = System.Retention
SET Variables.GenericBool1 = 1
SET ColumnComp.PCC.Temperature.Nominal = 80.0 [C]
RUN System.Trigger "T50Down", PCC.Temperature.Value<=50.0 AND Variables.GenericBool1, Limit=1, Hysteresis=5.0 [%], AllowImmediateExecution=No
SET RetTimes.RetTime3 = System.Retention
RUN Log PCC.Temperature.Value
SET Variables.GenericBool2 = 1
RUN System.Trigger "T40Down", PCC.Temperature.Value<=40.0 AND Variables.GenericBool2, Limit=1, Hysteresis=5.0 [%], AllowImmediateExecution=No
SET RetTimes.RetTime4 = System.Retention
RUN Log PCC.Temperature.Value
SET ColumnComp.PCC.Temperature.Nominal = 40.0 [C]
SET ColumnComp.PCC.TempCtrl = Off

[Stage] StopRun
RUN ColumnComp.CC_Temp.AcqOff
RUN ColumnComp.CC_U_Temp_Actual.AcqOff
RUN ColumnComp.CC_L_Temp_Actual.AcqOff
RUN ColumnComp.CC_UCTL_TempRear_Actual.AcqOff
RUN ColumnComp.PWM_CCU_A.AcqOff
RUN ColumnComp.PWM_CCU_B.AcqOff
RUN ColumnComp.PWM_CCL_A.AcqOff
RUN ColumnComp.PWM_CCL_B.AcqOff
RUN ColumnComp.Fan_Rear_ActualRPM.AcqOff

[Stage] PostRun
RUN ColumnComp.PCC_Temp.AcqOff
RUN ColumnComp.PWM_PCC_A.AcqOff
RUN ColumnComp.PWM_PCC_B.AcqOff
RUN Thermometer1.ExtTemp_UpperCC.AcqOff
RUN Thermometer1.ExtTemp_LowerCC.AcqOff
RUN Thermometer.Environment_Temperature.AcqOff
RUN ColumnComp.LEDBoard_LeakDiff.AcqOff
RUN ColumnComp.LEDBoard_A13.AcqOff
RUN ColumnComp.LEDBoard_A14.AcqOff
RUN ColumnComp.Oven_Gas_MuteTimeRemain.AcqOff

[End]
```

## 5. Report / DB Follow-Up

The existing report logic can still compute stability if the runtime stays long enough:

```text
LowerRange = max(K61:K75) - min(K61:K75)
UpperRange = max(L61:L75) - min(L61:L75)
RawStability = max(LowerRange, UpperRange)
Noise_CC_Temp = chm.noise(59,60)
```

Open verification before production use:

| Item | Status | Reason |
|---|---|---|
| Report label says 70C or generic stability | Open verification required | Existing report template may show original 70C title/labels. |
| DB field name | Open verification required | Existing DB contract uses stability fields, not a temperature-specific 80C field. |
| Acceptance criterion at 80C | Open verification required | Existing TCC FOQ stability criterion is known for the FOQ stability method; custom 80C criterion must be confirmed. |
| Run length | Must keep original | Report uses 45..60 and 59..60 minute windows. |

