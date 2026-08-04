# TCC Method Script and Report Formula Alignment

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
