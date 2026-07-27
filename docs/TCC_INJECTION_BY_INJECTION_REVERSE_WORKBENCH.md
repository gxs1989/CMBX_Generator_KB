# TCC Injection-by-Injection Reverse Workbench

This document advances TCC reverse understanding one sequence injection at a
time. Each injection should become a complete method/report contract before we
use it for generation.

The working unit is:

```text
injection row
-> instrument method
-> processing method
-> required CM configuration
-> method command groups
-> raw/audit evidence created
-> report formulas that consume that evidence
-> DB/result meaning
```

## Current Reference Sequence

Reference package:

```text
C:\ProgramData\CMBX Data Explorer Workspace\packages\TCC Cost Out\Zollner\Production\6000001.cmbx
```

Device:

```text
VH-C10-A
```

Sequence rows:

| Row | Injection | Instrument Method | Processing Method | Reverse Status |
| ---: | --- | --- | --- | --- |
| 1 | `ColumnIDs` | `ColumnID` | `CORRECT_STABILITY_INJ_INSERTION` | detailed below |
| 2 | `Preheater Connection Test` | `PREHEATER` | `No_Integration` | first-pass mapped |
| 3 | `Valve` | `VALVES` | `No_Integration` | first-pass mapped |
| 4 | `VTCC_BurnIn` | `BURNIN` | `NO_INTEGRATION` | first-pass mapped |
| 5 | `Temperature Calibration` | `TEMPERATURE_CALIBRATION` | `CORRECT_ACCURACY_INJ_INSERTION` | first-pass mapped |
| 6 | `Temperature Accuracy_H` | `TEMPERATURE_ACCURACY` | `ACCURACY_IRC_STOP_H` | first-pass mapped |
| 7 | `Temperature Precision_and_Fan` | `TEMPERATURE_PRECISION_AND_FAN` | `CORRECT_STABILITY_INJ_INSERTION` | first-pass mapped |
| 8 | `Temperature Stability_and_PCC_H` | `TEMPERATURE_STABILITY_AND_PCC_70_H` | `NO_INTEGRATION` | first-pass mapped |
| 9 | `HeatUp and CoolDownTime` | `TEMP_HEAT_UP_DOWN_20_50_20` | `No_Integration` | first-pass mapped |
| 10 | `LiquidLeaktest` | `LIQUID LEAK` | `No_Integration` | first-pass mapped |
| 11 | `Qualification_Service_Done` | `Qualification_Service_Done` | `No_Integration` | first-pass mapped |
| 12 | `Factory Default` | `FACTORYDEFAULT` | `No_Integration` | first-pass mapped |
| 13 | `Error Log Check` | `CHECKERRORLOG` | `No_Integration` | first-pass mapped |

## Row 1: ColumnIDs

### Test Intent

TD meaning:

```text
Verify that the four column ID ports are electronically assigned correctly.
The tester inserts chip cards labeled A, B, C, and D into the matching slots.
The test passes when each slot reports the expected description.
```

This is not a raw temperature measurement. It is an audit/configuration test.

### Sequence Binding

```text
Injection name:      ColumnIDs
Instrument method:  ColumnID
Processing method:  CORRECT_STABILITY_INJ_INSERTION
Report sheet:       Column ID
```

Processing method note:

```text
The method itself performs the Column ID check and aborts on mismatch.
The production sequence binds CORRECT_STABILITY_INJ_INSERTION. Until the IRC
payload is fully reconstructed, preserve this binding when cloning the full VH
sequence. For a standalone Column ID test, the instrument method/report pair is
the main contract.
```

### Required CM Configuration

Core:

```text
ColumnComp
ColumnComp.ModelNo
ColumnComp.CC
ColumnComp.CC.TempCtrl
ColumnComp.CC.Temperature.Nominal
ColumnComp.CC.Mode
ColumnComp.CC_Temp
System.Trigger
System.AbortQueue
```

Column ID ports:

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

TD configuration prerequisite:

```text
Column ID system enabled.
All four column-ID slots enabled using the default device names.
Four chip cards exist and have description fields saved as A, B, C, and D.
```

### Method Command Groups

Source:

```text
knowledge_base/tcc_reverse_probe/VH/6000001/ColumnID_embedded_method_flow.tsv
```

#### 1. Device/page-count branch

The method logs `Variables.GenericLong9` based on device model:

```text
IF ColumnComp.ModelNo = "VH-C10-A":
    Variables.GenericLong9 = 12
    Delay 1
    Log GenericLong9
ELSE IF supported non-VH branch:
    Variables.GenericLong9 = 10
    Delay 1
    Log GenericLong9
ELSE:
    Message "Column compartment model unknown, please reinspect in production!"
    System.AbortQueue
```

Interpretation:

```text
GenericLong9 is a report/page-count helper and device-branch evidence.
It is not the physical Column ID test result, but it must be preserved if the
report template expects total page count/device branch context.
```

#### 2. Minimal CC setup

```text
ColumnComp.CC.TempCtrl = On
ColumnComp.CC.Temperature.Nominal = 15.00 C
ColumnComp.CC.Mode = StillAir
```

Interpretation:

```text
The comment says CM needs data from any channel to evaluate the audit trail in
the report. The method therefore acquires CC_Temp even though Column ID itself
is audit-property based.
```

#### 3. End-run trigger state

```text
Variables.GenericBool1 = 0
Delay 2
System.Trigger "END_RUN", Variables.GenericBool1=1, TrueTime=0, Limit=1,
  Hysteresis=0, AllowImmediateExecution=No
ColumnComp.CC_Temp.AcqOff
End
```

Interpretation:

```text
GenericBool1 is the run-end gate. The method sets it to 1 after the column
descriptions pass the check.
```

#### 4. Acquisition

```text
ColumnComp.CC_Temp.AcqOn
```

Report reason:

```text
This provides at least one acquired channel so the report/audit trail can be
evaluated consistently.
```

#### 5. Manual prompt and card-state wait

```text
Message "Please plug the column ID adapters in their designated positions. Please note the correct order!"
Wait Column_A.CardState=OK AND Column_B.CardState=OK AND Column_C.CardState=OK AND Column_D.CardState=OK, Timeout=2.00
```

Interpretation:

```text
The method assumes the tester inserts all four cards. The CardState wait proves
that all four ports can see a card.
```

#### 6. Audit logging

```text
Log Column_A.Description
Log Column_B.Description
Log Column_C.Description
Log Column_D.Description
Delay 2
```

Interpretation:

```text
These Log commands create the audit evidence consumed by the report formulas.
```

#### 7. Immediate method-side pass/fail guard

```text
IF Column_A.Description <> "A"
   OR Column_B.Description <> "B"
   OR Column_C.Description <> "C"
   OR Column_D.Description <> "D":
    Message "Either the cards are plugged into the wrong positions or the ports are electronically wrong connected! Check that the cards are in the correct position. If so, the device must be repaired!"
    System.AbortQueue
```

Interpretation:

```text
The method itself enforces the result, not only the report.
```

#### 8. End and cleanup

```text
Delay 2
Variables.GenericBool1 = 1
ColumnComp.CC_Temp.AcqOff
```

### Report Formula Contract

Source:

```text
knowledge_base/tcc_report_formula_objects_vh_6000001_all_sheets.tsv
```

Sheet `Column ID`:

```text
L46 = AUDIT.Column_A.Description(0,"forward")
L47 = AUDIT.Column_B.Description(0,"forward")
L48 = AUDIT.Column_C.Description(0,"forward")
L49 = AUDIT.Column_D.Description(0,"forward")
```

Workbook/result meaning:

```text
RES_ColumnID_A passes if L46 == "A"
RES_ColumnID_B passes if L47 == "B"
RES_ColumnID_C passes if L48 == "C"
RES_ColumnID_D passes if L49 == "D"
```

### Copy-Ready Script Skeleton

This is a semantic skeleton, not yet a binary CMBX method encoder:

```text
InstrumentSetup
  IF ColumnComp.ModelNo = "VH-C10-A"
    SET Variables.GenericLong9 = 12
    RUN Delay 1
    RUN Log GenericLong9
  ELSE
    SET Variables.GenericLong9 = 10
    RUN Delay 1
    RUN Log GenericLong9
  ELSE_UNKNOWN
    RUN Message "Column compartment model unknown, please reinspect in production!"
    RUN System.AbortQueue

  SET ColumnComp.CC.TempCtrl = On
  SET ColumnComp.CC.Temperature.Nominal = 15.00 C
  SET ColumnComp.CC.Mode = StillAir
  SET Variables.GenericBool1 = 0
  RUN Delay 2
  RUN System.Trigger "END_RUN", Variables.GenericBool1=1, TrueTime=0, Limit=1, Hysteresis=0, AllowImmediateExecution=No
  RUN ColumnComp.CC_Temp.AcqOff
  RUN End

StartRun
  RUN ColumnComp.CC_Temp.AcqOn

Run
  RUN Message "Please plug the column ID adapters in their designated positions. Please note the correct order!"
  RUN Wait Column_A.CardState=OK AND Column_B.CardState=OK AND Column_C.CardState=OK AND Column_D.CardState=OK, Timeout=2.00
  RUN Log Column_A.Description
  RUN Log Column_B.Description
  RUN Log Column_C.Description
  RUN Log Column_D.Description
  RUN Delay 2
  IF Column_A.Description<>"A" OR Column_B.Description<>"B" OR Column_C.Description<>"C" OR Column_D.Description<>"D"
    RUN Message "Either the cards are plugged into the wrong positions or the ports are electronically wrong connected! Check that the cards are in the correct position. If so, the device must be repaired!"
    RUN System.AbortQueue
  RUN Delay 2
  SET Variables.GenericBool1 = 1

StopRun
  RUN ColumnComp.CC_Temp.AcqOff
```

### Generation Rule

For generated Column ID:

```text
Do not invent RetTimes.
Do not use raw temperature formulas for the result.
Preserve audit logging of Column_A-D.Description.
Preserve the method-side abort guard unless intentionally making a non-aborting diagnostic method.
Keep a simple acquired channel, typically CC_Temp, so the report can evaluate audit context.
```

### Open Checks

- Confirm whether `GenericLong9` is used by workbook formulas for total page
  count or only displayed as audit evidence.
- Confirm whether standalone Column ID can safely use `No_Integration` or
  should preserve the production `CORRECT_STABILITY_INJ_INSERTION` binding.
- Compare `ColumnID` flow between VC and VH to confirm if the method body is
  identical except page-count/device branch context.

## Row 2: Preheater Connection Test

Sequence binding:

```text
Injection name: Preheater Connection Test
Instrument method: PREHEATER
Processing method: No_Integration
Primary report sheet: Preheater Ports_Noise
```

Test intent:

```text
Verify left and right preheater port presence, memory state, thermal response,
heater feedback plausibility, and preheater temperature noise.
```

Method command groups:

```text
Setup:
  Set CC to 15 C, StillAir, TempCtrl On.
  Initialize GenericBool1/2 = 0.
  Initialize RetTime1..4 = 0.
  Temporarily tune left/right preheater PID:
    PREH.L.PID.Kp=10000, Ki=1200
    PREH.R.PID.Kp=10000, Ki=1200
  Set left/right preheater TempCtrl On, nominal 40 C,
  ReadyTempDelta 0.05 C, EquilibrationTime 0.5 min.
  Wait until both preheaters are ready.

Acquisition:
  Acquire CC_Temp, PrehtLeft_Temp, PrehtRight_Temp,
  PREH_L/R_Temp_Actual, PREH_L/R_HeaterTemp_Actual,
  PWM_LeftPreh/PWM_RightPreh, fan RPM, external thermometers,
  environment and leak-related channels.

Run:
  Start left heat-up toward 60 C.
  RetTime1 = left reaches 45 C.
  Start right heat-up toward 60 C.
  RetTime2 = right reaches 45 C.
  RetTime3 = left reaches 55 C, then switch left preheater off.
  RetTime4 = right reaches 55 C, then switch right preheater off.
  END_RUN when both sides have reached their terminal condition.

Cleanup:
  AcqOff all relevant channels.
  Restore preheater PID to production/default values:
    Kp=600000, Ki=30000.
```

Report dependencies:

```text
Port presence:
  J72 = AUDIT.RetTime1("forward")
  J73 = AUDIT.RetTime2("forward")
  K72 = AUDIT.RetTime3("forward")
  K73 = AUDIT.RetTime4("forward")
  J117/J118 = precond.ColumnComp.PrehtLeft/Right.ModulePresent
  K117/K118 = precond.ColumnComp.PrehtLeft/Right.MemoryState

Thermal difference:
  J82/J83 = average PrehtLeft/Right_Temp, 0.25..0.5 min
  K82/K83 = average PREH_L/R_HeaterTemp_Actual, 0.25..0.5 min

Noise and response:
  J92/J93 = chm.noise(PrehtLeft/Right_Temp, 0..0.5)
  K92/K93 = chm.noise(PREH_L/R_HeaterTemp_Actual, 0..0.5)
  J102/J103 = preheater average 0.25..0.5 min
  K102/K103 = preheater max 0.5..0.6 min
  J110/J111 = heater average 0.4..0.5 min
  K110/K111 = heater max 0.5..0.6 min
```

Generation rule:

```text
A generated preheater test must create RetTime1..4 in this exact thermal
sequence. The report does not infer a port pass from raw temperature alone:
it also depends on precondition ModulePresent and MemoryState.
```

## Row 3: Valve

Sequence binding:

```text
Injection name: Valve
Instrument method: VALVES
Processing method: No_Integration
Primary report sheet: Valve_Keypad
```

Test intent:

```text
Verify upper/lower valve switching between configured positions and verify
front-panel/keypad actions for valve and fast-cool controls.
```

Method command groups:

```text
Setup:
  Set CC TempCtrl On, nominal operating condition, StillAir.
  Set UpperValve and LowerValve to 6_1.
  Log UpperValve.Precision and LowerValve.Precision.

Run:
  Acquire CC_Temp as time/audit carrier.
  Switch both valves to 1_2 and log precision.
  Switch both valves back to 6_1 and log precision.
  Prompt operator to disconnect the device and press front-panel FAST COOL,
  Upper Valve and Lower Valve actions within the method window.
  Wait until ColumnComp reconnects.

Cleanup:
  Stop CC_Temp acquisition.
```

Report dependencies:

```text
Audit position checks:
  K49/L49 = AUDIT.UpperValve/LowerValve.CurrentPosition(-0.05)
  K50/L50 = AUDIT.UpperValve/LowerValve.CurrentPosition(0.095)
  K51/L51 = AUDIT.UpperValve/LowerValve.CurrentPosition(0.19)
  K60/L60 = AUDIT.UpperValve/LowerValve.CurrentPosition(0.9)
  N60 = AUDIT.ColumnComp.FastCoolState(0.9,"backward")

Precision checks:
  U49:U51 = AUDIT.UpperValve.Precision(...)
  V49:V51 = AUDIT.LowerValve.Precision(...)
```

Generation rule:

```text
Only generate this method when the instrument configuration has the relevant
upper/lower valve options. The report is audit-driven, so valve commands must
write position and precision audit properties at the expected time order.
```

## Row 4: VTCC_BurnIn

Sequence binding:

```text
Injection name: VTCC_BurnIn
Instrument method: BURNIN
Processing method: NO_INTEGRATION
Primary report role: setup/evidence, not a formula-heavy DB output sheet
```

Test intent:

```text
Exercise the compartment through high/low/high thermal cycles before precision
and accuracy measurements, because temperature sensor behavior can change after
heating.
```

Method command groups:

```text
Setup:
  Set CC ReadyTempDelta to a broad value, EquilibrationTime 0.5.
  Turn CC TempCtrl On.
  Turn PCC TempCtrl Off for VH-style devices.
  Set StillAir and LiquidLeakSensor Off.
  Determine model-dependent thermal limits:
    VH: min 5 C, max 120 C.
    VA/VC family: lower high limit, typically max 85 C.

Run:
  Stabilize initially around 15 C.
  Acquire common temperature, external thermometer, environment and leak data.
  Heat to maximum; trigger T_Maximum near high limit.
  Cool to minimum; trigger T_Minimum near low limit.
  Heat to maximum again and increment GenericFloat1.
  Hold/end after completing the required cycles.

Abort behavior:
  Abort if device model is unknown or external thermometer behavior does not
  support the expected heating evidence.
```

Report dependencies:

```text
No direct high-value DB mapping formula was found for this row in the report
formula objects. Its main role is conditioning and audit evidence for the
sequence context.
```

Generation rule:

```text
Burn-in is not a standalone report-calculation test. Include it when the
qualification procedure requires thermal conditioning before downstream tests.
For a custom single-point accuracy method, it may be omitted only if the test
definition explicitly allows skipping preconditioning.
```

## Row 5: Temperature Calibration

Sequence binding:

```text
Injection name: Temperature Calibration
Instrument method: TEMPERATURE_CALIBRATION
Processing method: CORRECT_ACCURACY_INJ_INSERTION
Primary report sheet: Temp_Calib_Internal
```

Test intent:

```text
Create/update CC calibration point and deviation audit properties by comparing
internal CC sensor values to external upper/lower thermometer channels at a
model-specific setpoint ladder.
```

Method command groups:

```text
Setup:
  Set ReadyTempDelta 0.3 C, EquilibrationTime 0.1 min.
  Turn CC TempCtrl On, StillAir, LiquidLeakSensor Off.
  Initialize CCCalib.CalPointU/L01..08 and CalDevU/L01..08 to 0.
  Initialize RetTime1..8 to 0.

Model-specific setpoints:
  VH:
    120, 100, 80, 60, 40, 20, 10, 5 C family.
  VA/VC:
    85, 70, 55, 40, 30, 20, 10, 5 C family.

Run:
  For each calibration point:
    set CC nominal,
    wait until CC.TempReady plus stabilization,
    write RetTimeN,
    write internal upper/lower calibration point,
    write deviation upper/lower = external thermometer - internal value.
  Abort if deviation exceeds the hard guard, e.g. > 4 C.
```

Report dependencies:

```text
Raw/evidence values:
  B15:B21 = CC_Temp signalValue at RetTime1..7
  C15:C21 = RetTime deltas between adjacent calibration points
  D15:D21 = ExtTemp_UpperCC drift in RetTimeN-0.5..RetTimeN
  E15:E21 = ExtTemp_LowerCC drift in RetTimeN-0.5..RetTimeN
  J14 = CC_Temp signalValue at RetTime8-1
  J15 = RetTime8 - RetTime7
  J16/J17 = external upper/lower drift near RetTime8

Calibration audit values:
  TempCalibrationPointUpper/LowerN(1000,"backward")
  TempCalibrationDeviationUpper/LowerN(1000,"backward")

Environment:
  Environment_Temperature average.
```

Generation rule:

```text
Do not generate calibration by only copying report formulas. The method must
write calibration audit properties and RetTimes. Report formulas are the
verification view over those audit writes.
```

## Row 6: Temperature Accuracy_H

Sequence binding:

```text
Injection name: Temperature Accuracy_H
Instrument method: TEMPERATURE_ACCURACY
Processing method: ACCURACY_IRC_STOP_H
Primary report sheet: Temp Accuracy
```

Test intent:

```text
At selected nominal CC temperatures, wait until external upper/lower
thermometers are stable, then compare external observed temperature against
the CC nominal setpoint.
```

Method command groups:

```text
Setup:
  Determine model-specific setpoint list.
  Initialize RetTime1..5.
  Configure CC TempCtrl, StillAir, and readiness/stability tolerances.
  Enable external thermometer channels.

Run:
  For each nominal setpoint:
    set ColumnComp.CC.Temperature.Nominal,
    wait for CC.TempReady,
    wait until stability logic says both upper and lower external probes are
    ready,
    write RetTimeN.
```

Report dependencies:

```text
Per setpoint:
  K66:K70 = AUDIT.RetTime1..5
  I66:I70 = AUDIT.ColumnComp.CC.Temperature.Nominal(RetTimeN-0.1)
  L66:L70 = ExtTemp_LowerCC average RetTimeN-1.0..RetTimeN-0.2
  M66:M70 = ExtTemp_UpperCC average RetTimeN-1.0..RetTimeN-0.2

Workbook rule:
  Observed value = upper/lower value with larger absolute deviation from nominal.
  Deviation = observed - nominal.
  Result = max(abs(deviation)) <= Definitions!Temperature Accuracy.
```

Generation rule:

```text
For a custom "accuracy 40 C only" method, this is the key row. The generated
script should keep the same stability and RetTime contract, but reduce the
setpoint ladder to a single 40 C nominal and produce the corresponding report
cell/formula block for that one RetTime.
```

## Row 7: Temperature Precision_and_Fan

Sequence binding:

```text
Injection name: Temperature Precision_and_Fan
Instrument method: TEMPERATURE_PRECISION_AND_FAN
Processing method: CORRECT_STABILITY_INJ_INSERTION
Primary report sheets: Temp Precision, Fan
```

Test intent:

```text
Exercise repeated external thermometer measurements under repeated setpoint
conditions and verify fan-related mode behavior.
```

Method command groups:

```text
Setup:
  Branch on device model for page/report context.
  Set ReadyTempDelta 0.1 C, EquilibrationTime 0.5 min.
  Turn CC TempCtrl On, StillAir, LiquidLeakSensor Off.

Run:
  Precondition around 45/50 C.
  Acquire CC_Temp, fan, external thermometer, environment and leak channels.
  Toggle nominal values 45/50/45/50.
  Switch LiquidLeakSensor On.
  Change CC mode to ForcedAir, log ready states, then return to StillAir.
```

Report dependencies:

```text
Temperature precision:
  K65/K66/K67 = ExtTemp_LowerCC average at 14..14.8, 36..36.8, 58..58.8 min
  L65/L66/L67 = ExtTemp_UpperCC same windows
  I65/I66/I67 = CC nominal at 14.9, 36.9, 58.9 min

Workbook rule:
  LowerRange = max(K65:K67) - min(K65:K67)
  UpperRange = max(L65:L67) - min(L65:L67)
  RawPrecision = max(LowerRange, UpperRange)

Fan:
  Fan and CC mode report blocks use fixed windows later in the method timeline.
```

Generation rule:

```text
Precision depends on repeated windows, not one RetTime. If reducing the test,
preserve enough repeated windows for a meaningful range calculation.
```

## Row 8: Temperature Stability_and_PCC_H

Sequence binding:

```text
Injection name: Temperature Stability_and_PCC_H
Instrument method: TEMPERATURE_STABILITY_AND_PCC_70_H
Processing method: NO_INTEGRATION
Primary report sheets: Temp Stability_Noise, PCC
```

Test intent:

```text
Measure CC temperature stability at 70 C and, for VH, test PCC thermal behavior
including accuracy windows, drift and cooldown timing.
```

Method command groups:

```text
Setup:
  ReadyTempDelta 0.05 C, EquilibrationTime 0.5 min.
  Turn CC and PCC TempCtrl On.
  Set CC nominal 70 C and PCC nominal 40 C.
  Wait until CC.TempReady and PCC.TempReady.

Run:
  Acquire CC_Temp, PCC_Temp, PWM_PCC_A/B, external thermometers, environment
  and leak-related channels.
  PCC heat/cool sequence:
    RetTime2 when PCC reaches 60 C.
    Set PCC nominal to 80 C.
    RetTime3 when PCC cools to 50 C after heat event.
    RetTime4 when PCC cools to 40 C; switch PCC off or back to safe nominal.
```

Report dependencies:

```text
CC stability:
  K61:K75 = ExtTemp_LowerCC one-minute averages from 45..60 min
  L61:L75 = ExtTemp_UpperCC one-minute averages from 45..60 min
  Stability = max(range(lower), range(upper))

Noise:
  K86 = CC_Temp chm.noise(59,60)
  K87 = PCC_Temp chm.noise(59,60)

PCC:
  Nominal audit at 4, 12, 20 min.
  PCC_Temp averages at 0..5, 10..15, 19..24 min.
  PCC drift = chm.sig_value("drift", 19, 24).
  PCC cooldown = RetTime4 - RetTime3.
```

Generation rule:

```text
This injection is two tests sharing a timeline: CC stability and PCC. For a
non-PCC device variant, the PCC branch must be removed rather than left as a
dead report dependency.
```

## Row 9: HeatUp and CoolDownTime

Sequence binding:

```text
Injection name: HeatUp and CoolDownTime
Instrument method: TEMP_HEAT_UP_DOWN_20_50_20
Processing method: No_Integration
Primary report sheet: HeatUp&CoolDown
```

Test intent:

```text
Measure time to heat from 20 C to 50 C and cool from 50 C back to 20 C, using
both internal CC temperature and external upper thermometer guards.
```

Method command groups:

```text
Setup:
  Set ReadyTempDelta 0.5 C and EquilibrationTime 0.5 min.
  Turn CC TempCtrl On, StillAir.
  Initialize GenericLong0..3 and RetTime1..6.
  Stabilize around 17/20 C.

Run:
  Wait until internal and external sensors are around 20 C.
  RetTime1 = start heat-up after both sensors are ready.
  Set nominal 50 C.
  RetTime2 = external upper thermometer around 50 C after hold.
  RetTime3 = internal CC around 50 C after hold.
  RetTime4 = start cooldown after both 50 C conditions are satisfied.
  Set nominal 20 C.
  RetTime5 = external upper thermometer around 20 C after hold.
  RetTime6 = internal CC around 20 C after hold.
```

Report dependencies:

```text
J66 = RetTime1
K66 = RetTime3
L66 = RetTime4
M66 = RetTime6

Workbook rule:
  HeatUp_Time_20to50 = RetTime2 - RetTime1 - 2.0 min
  CoolDown_Time_50to20 = RetTime5 - RetTime4 - 2.0 min
  RetTime3/6 remain row-65 internal endpoint evidence; exported workbook
  summary/DB timing uses the row-66 external endpoint route.
```

Generation rule:

```text
The 2.0 min subtraction is part of the report contract because the trigger
sequence includes a stable-hold window. Do not remove it when generating a
report for this method shape.
```

## Row 10: LiquidLeaktest

Sequence binding:

```text
Injection name: LiquidLeaktest
Instrument method: LIQUID LEAK
Processing method: No_Integration
Primary report sheet: Liquid Leak Test
```

Test intent:

```text
Verify the liquid leak sensor and alarm/mute workflow using a manual water
injection into the compartment.
```

Method command groups:

```text
Setup:
  Set CC to a safe nominal temperature around 20 C.
  Turn LiquidLeakSensor On after initial safe setup.
  Initialize GenericBool1 = 0 and an END_RUN trigger tied to GenericBool1.

Run:
  Prompt operator to inject water to the bottom of the compartment.
  Wait for LiquidLeak = Leak.
  Log LiquidLeak.
  Prompt operator to mute/confirm alarm.
  Wait until ColumnComp.Alarm = NoAlarm.
  Switch LiquidLeakSensor Off.
  Prompt operator to remove remaining liquid.
  Set GenericBool1 = 1.
```

Report dependencies:

```text
M47 = AUDIT.LiquidLeak(100.000,"backward")
K47 = precond.LiquidLeakCalibrationValue
```

Generation rule:

```text
This is a manual-interaction test. A generated method must preserve operator
messages and alarm confirmation steps; otherwise the report can show evidence
without actually validating the sensor workflow.
```

## Row 11: Qualification_Service_Done

Sequence binding:

```text
Injection name: Qualification_Service_Done
Instrument method: Qualification_Service_Done
Processing method: No_Integration
Primary report role: qualification/service audit evidence
```

Test intent:

```text
Write or log qualification and service completion evidence after the functional
tests have completed.
```

Method command groups:

```text
Run:
  Log ColumnComp_Wellness.Service.LastDate.
  Log ColumnComp_Wellness.Qualification.LastDate.
  Preserve audit evidence for operator/service completion state.
```

Report dependencies:

```text
No heavy raw channel calculation is expected. This row is metadata/audit driven
and supports final qualification/service state in the report package.
```

Generation rule:

```text
Keep this row separate from functional tests. It is a procedure-state write/log
operation, not a temperature or signal calculation method.
```

## Row 12: Factory Default

Sequence binding:

```text
Injection name: Factory Default
Instrument method: FACTORYDEFAULT
Processing method: No_Integration
Primary report sheets: Definitions, Internal Use, Factory Default metadata blocks
```

Test intent:

```text
Return relevant service/qualification configuration and device state to the
expected factory/default state, while recording identity and final metadata.
```

Method command groups:

```text
Setup/run:
  Wait ColumnComp.Ready.
  Enter service code.
  Disable or clear qualification/service interval warnings and grace periods.
  Log qualification/service last-date/operator fields.
  Log operating hours and workload.
  Clear ErrorLog.
  Clear selected revision strings.
  Set CC nominal 20 C, TempCtrl Off.
  Turn LiquidLeakSensor On.
  Prompt/check valve covers and thermometer serial/location information.
```

Report dependencies:

```text
Definitions:
  C7/C8 = system version/serial
  C9 = seq.name
  C10 = seq.update_time
  C15 = AUDIT.ColumnComp.ModelNo
  D15 = precond.ColumnComp.SerialNo
  E15 = precond.ColumnComp.FirmwareVersion
  C80/C81/C83 = sequence custom variables for thermometer/location

Internal Use:
  Hardware/firmware/module revisions from precond.ColumnComp...
  Submit/data vault/sign status fields where available.
```

Generation rule:

```text
Factory Default is not interchangeable with a data test. It mutates service and
configuration state, so generated packages should include it only when the
requested procedure needs final production/default cleanup.
```

## Row 13: Error Log Check

Sequence binding:

```text
Injection name: Error Log Check
Instrument method: CHECKERRORLOG
Processing method: No_Integration
Primary report sheet: Error Log / audit table, not formula-object heavy
```

Test intent:

```text
Stop active thermal controls, check the final error-log state and leave the
device in a safe non-running condition.
```

Method command groups:

```text
Run:
  Turn PrehtRight.TempCtrl Off.
  Turn PrehtLeft.TempCtrl Off.
  Turn CC.TempCtrl Off.
  In the full production context, also reset column activity / connection state
  and inspect or clear error-log evidence as required by the template.
```

Report dependencies:

```text
The exported report formula object list does not expose significant cell-level
formulas for this sheet. Treat it as an error-log/audit table endpoint rather
than a raw signal calculation.
```

Generation rule:

```text
Always include a safe stop/end-state method when generating a complete FOQ-like
sequence. For a single custom diagnostic injection, include equivalent cleanup
commands in StopRun or as a final injection.
```

## Cross-Injection Generation Notes

The executable sequence is mostly defined by:

```text
Injection name
Instrument method
Processing method only where IRC/report correction is required
Report template/report sheet for calculation and display
```

The reverse path for generation should therefore be:

```text
requested test intent
-> choose required injection row(s)
-> choose compatible device/config branches
-> generate method script with the same RetTime/audit/channel contract
-> generate or select report sheet formulas that consume that contract
-> optionally generate sequence rows and processing method bindings
```

For the user's example, "VHTCC temperature accuracy at 40 C only", the starting
point is Row 6. The reduced method should keep the original stability wait,
external thermometer channels and RetTime contract, but collapse the production
setpoint ladder to one 40 C measurement window and pair it with a one-row
accuracy report block.
