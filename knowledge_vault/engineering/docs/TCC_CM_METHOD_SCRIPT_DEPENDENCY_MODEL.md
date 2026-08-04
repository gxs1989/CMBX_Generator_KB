# TCC CM Method Script Dependency Model

This document describes how to understand and generate TCC Chromeleon method
script snippets safely. It complements the symbol manifest and the
method/report alignment notes.

The key point: a CM method script line is rarely independent. A line normally
belongs to a dependency group. Generated scripts must preserve the group
semantics, not only the visible command text.

## Evidence Used

Decoded VH production methods:

```text
knowledge_base/tcc_reverse_probe/VH/6000001/*_embedded_method_flow.tsv
```

Report formula bridge:

```text
knowledge_base/tcc_report_formula_objects_vh_6000001_all_sheets.tsv
```

TD extraction:

```text
knowledge_base/tcc_td_vx_c10_a_text.txt
```

Related docs:

```text
cmbx_data_explorer/docs/TCC_REQUIRED_SYMBOL_MANIFEST.md
cmbx_data_explorer/docs/TCC_METHOD_REPORT_ALIGNMENT.md
cmbx_data_explorer/docs/CM_INSTRUMENT_CONFIGURATION_KNOWLEDGE_BASE.md
```

## Dependency Layers

### 1. Configuration Symbols

These are the CM instrument tree symbols that must exist before a script can
run. Examples:

```text
ColumnComp.CC
ColumnComp.PCC
ColumnComp.PrehtLeft
ColumnComp.PrehtRight
ColumnComp.UpperValve
ColumnComp.LowerValve
Thermometer1.ExtTemp_UpperCC
Thermometer1.ExtTemp_LowerCC
Thermometer.Environment_Temperature
Column_A / Column_B / Column_C / Column_D
```

Generation rule:

```text
Never emit a command for an optional subdevice unless the target device/profile
requires that test and exposes the symbol.
```

Example:

```text
ColumnComp.PCC.Temperature.Nominal
```

is valid for the VH PCC branch, but it must not be emitted into a VC-only
stability method.

### 2. Setup State

These commands make later waits/triggers meaningful:

```text
ColumnComp.CC.TempCtrl = On
ColumnComp.CC.Mode = StillAir
ColumnComp.CC.ReadyTempDelta = ...
ColumnComp.CC.EquilibrationTime = ...
ColumnComp.LiquidLeakSensor = Off/On depending on the test phase
Data_Collection_Rate = 20 on acquired diagnostic channels
```

Generation rule:

```text
Do not copy a wait or trigger without the setup properties that define when the
device becomes ready and which channel values are meaningful.
```

### 3. Acquisition Contract

Report formulas can only read raw data from channels that were acquired. These
commands are a contract with report formulas:

```text
Thermometer1.ExtTemp_UpperCC.AcqOn
Thermometer1.ExtTemp_LowerCC.AcqOn
ColumnComp.CC_Temp.AcqOn
ColumnComp.PCC_Temp.AcqOn
ColumnComp.PrehtLeft_Temp.AcqOn
ColumnComp.PrehtRight_Temp.AcqOn
```

Every generated script needs matching cleanup:

```text
*.AcqOff
```

Generation rule:

```text
For each report FixedChannel, there must be a corresponding AcqOn window that
covers the formula time interval.
```

Examples:

```text
Temp Accuracy row 68:
  report reads ExtTemp_LowerCC and ExtTemp_UpperCC at RetTime3-1 .. RetTime3-0.2
  method must have acquired both channels before that window

Temp Stability:
  report reads ExtTemp_* from 45..60 min
  method must keep those channels acquired through at least 60 min
```

### 4. Variables As Internal State

Variables in these methods are not arbitrary scratch cells. They usually encode
method state, model-dependent constants, or trigger gates.

Important groups:

```text
Variables.GenericDouble*  -> temperature setpoints or thresholds
Variables.GenericLong*    -> phase counters / page counts / trigger gates
Variables.GenericBool*    -> device branch, trigger gate, or result flag
TempVars.*                -> ambient and temperature helper values
StabVars.*                -> external thermometer stability state
CCCalib.*                 -> calibration values and acceptance checks
RetTimes.RetTime*         -> report-visible event anchors
```

Generation rule:

```text
Variables may be renamed only if every command, condition, trigger, report
dependency, and processing-method dependency is also updated. In practice, keep
the original variable names until the full dependency graph is known.
```

### 5. Triggers

`System.Trigger` is not just a wait. It defines asynchronous event logic.

Common trigger roles:

```text
stability sampling loop
temperature boundary detection
heat/cool phase transition
PCC 50 C / 40 C crossing
preheater 45 C / 55 C crossing
run-end gate
abort-on-timeout
```

Generation rule:

```text
If a RetTime is set by a trigger branch, the trigger condition and the state
variables around it are part of the RetTime contract.
```

Example from temperature accuracy:

```text
StabVars.CounterUpper >= 4 -> StabVars.UpperReady = 1
StabVars.CounterLower >= 4 -> StabVars.LowerReady = 1
Wait ColumnComp.CC.TempReady AND StabVars.LowerReady AND StabVars.UpperReady
RetTimes.RetTime3 = System.Retention
```

The report later assumes `RetTime3` means:

```text
40 C setpoint is reached and both external thermometers are stable.
```

### 6. RetTime Semantics

RetTimes are the most important bridge from method to report. Their numbers are
not interchangeable.

Examples:

```text
TEMPERATURE_ACCURACY, VH:
  RetTime1 -> 10 C stable point
  RetTime2 -> 20 C stable point
  RetTime3 -> 40 C stable point
  RetTime4 -> 80 C stable point
  RetTime5 -> 120 C stable point

TEMP_HEAT_UP_DOWN_20_50_20:
  RetTime1..6 -> heat/cool boundary and hold events

PREHEATER:
  RetTime1 -> left reaches 45 C
  RetTime2 -> right reaches 45 C
  RetTime3 -> left reaches 55 C
  RetTime4 -> right reaches 55 C

TEMPERATURE_STABILITY_AND_PCC_70_H:
  RetTime3 -> PCC reaches/crosses 50 C on cool-down
  RetTime4 -> PCC reaches/crosses 40 C on cool-down
```

Generation rule:

```text
If using existing report formulas, keep RetTime numbering and meaning exactly.
If changing RetTime numbering, rewrite the report formulas and DB mapping.
```

### 7. Audit Evidence

Some tests are not raw-signal tests. They depend mostly on audit properties
written by `Log`, state changes, or user/keypad events.

Examples:

```text
Column ID:
  Log Column_A.Description ... Column_D.Description
  report reads AUDIT.Column_A.Description(0,"forward") etc.

Valve:
  set upper/lower position
  Log UpperValve.Precision and LowerValve.Precision
  report reads AUDIT.UpperValve.CurrentPosition and Precision at fixed times

Liquid Leak:
  wait for LiquidLeak=Leak
  report reads AUDIT.LiquidLeak(100,"backward")
```

Generation rule:

```text
Audit-based tests require preserving command timing and logged property names.
They cannot be validated by raw channels alone.
```

### 8. Manual Interaction

Some method sections intentionally pause for user actions:

```text
Message "Please plug the column ID adapters..."
Message "Please provoke a liquid leak..."
Message "Please press keypad buttons..."
```

Generation rule:

```text
Manual interactions are part of the method contract. A generated method may
remove them only if the corresponding report/audit check is also removed.
```

### 9. Abort and Cleanup

Abort branches are not decoration. They protect invalid runs and make results
meaningful:

```text
System.AbortQueue
timeout if stable point not reached
abort if device ModelNo is unknown
abort if calibration deviation is impossible
abort if column ID descriptions are wrong
```

Cleanup commands restore the TCC to a safe state:

```text
ColumnComp.CC.Temperature.Nominal = 20 C
ColumnComp.CC.TempCtrl = Off
ColumnComp.PCC.TempCtrl = Off
ColumnComp.PrehtLeft.TempCtrl = Off
ColumnComp.PrehtRight.TempCtrl = Off
*.AcqOff
LiquidLeakSensor = On/Off according to sequence phase
```

Generation rule:

```text
A reduced single-test method still needs relevant abort and cleanup behavior.
```

## Method Complexity Summary

Decoded VH production package `6000001.cmbx`:

| Method | Main role | SET | RUN | Triggers | RetTime SETs | AcqOn | Logs | Waits | Abort | Messages |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `BURNIN` | stress and setup consistency | 27 | 60 | 3 | 0 | 15 | 0 | 1 | 2 | 2 |
| `CHECKERRORLOG` | reconnect/error-log context | 7 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `ColumnID` | column chip/card verification | 7 | 22 | 1 | 0 | 1 | 6 | 1 | 2 | 3 |
| `FACTORYDEFAULT` | service/log/factory cleanup | 9 | 22 | 0 | 0 | 0 | 5 | 1 | 0 | 2 |
| `LIQUID LEAK` | leak sensor and keypad mute | 21 | 72 | 1 | 0 | 16 | 1 | 3 | 2 | 4 |
| `PREHEATER` | preheater port heat/noise check | 48 | 90 | 5 | 8 | 17 | 8 | 1 | 2 | 1 |
| `QUALIFICATION_SERVICE_DONE` | wellness/service metadata | 0 | 4 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| `TEMP_HEAT_UP_DOWN_20_50_20` | CC heat/cool performance | 45 | 65 | 9 | 12 | 16 | 2 | 1 | 1 | 1 |
| `TEMPERATURE_ACCURACY` | setpoint accuracy | 89 | 76 | 5 | 10 | 16 | 2 | 6 | 3 | 3 |
| `TEMPERATURE_CALIBRATION` | internal sensor calibration | 237 | 115 | 8 | 16 | 16 | 1 | 1 | 10 | 19 |
| `TEMPERATURE_PRECISION_AND_FAN` | repeatability and fan response | 34 | 47 | 0 | 0 | 16 | 7 | 1 | 2 | 2 |
| `TEMPERATURE_STABILITY_70_C` | CC stability/noise | 19 | 39 | 0 | 0 | 16 | 2 | 1 | 1 | 1 |
| `TEMPERATURE_STABILITY_AND_PCC_70_H` | VH CC stability plus PCC | 37 | 50 | 3 | 7 | 19 | 4 | 1 | 1 | 1 |
| `VALVES` | valve precision/keypad | 11 | 18 | 0 | 0 | 1 | 6 | 1 | 0 | 1 |

This table shows why generating a script by copying a few visible lines is not
safe. `TEMPERATURE_CALIBRATION`, `TEMPERATURE_ACCURACY`, and
`TEMP_HEAT_UP_DOWN_20_50_20` are state machines.

## Dependency Groups By Test

### Temperature Accuracy

Must preserve:

```text
device branch by ColumnComp.ModelNo
model-specific setpoint variables
CC readiness setup
external thermometer AcqOn/AcqOff
StabVars stability loop
timeout abort trigger
RetTimeN emitted after stable wait
report row mapping for RetTimeN
```

Cannot safely omit:

```text
StabVars counter logic
external thermometer acquisition
RetTime numbering
```

### Temperature Calibration

Must preserve:

```text
model-specific calibration setpoints
CCCalib variables
RetTime1..8 anchors
drift checks around each RetTime
calibration value transfer to ColumnComp calibration properties
abort branches for impossible deviation
ambient/low-temperature skip rules
```

This is currently the highest-risk method for synthesis.

### Temperature Precision and Fan

Must preserve:

```text
fixed timing windows used by report formulas
external upper/lower channels
CC_Temp channel for fan response
mode switch StillAir <-> ForcedAir
```

Because the report formulas use fixed time windows rather than RetTimes, any
shortened method requires rewritten report formulas.

### Temperature Stability

Must preserve:

```text
70 C setpoint
external channels through 45..60 min
CC_Temp noise channel through 59..60 min
```

The report uses fixed windows, so method duration is part of the contract.

### PCC Branch

Must preserve:

```text
VH-only ModelNo branch
PCC TempCtrl and TempReady setup
PCC_Temp acquisition
RetTime3 = PCC 50 C cool-down event
RetTime4 = PCC 40 C cool-down event
19..24 min drift/accuracy window if existing report is reused
```

### Heat-Up/Cool-Down

Must preserve:

```text
upper external thermometer acquisition
20 C and 50 C external/internal trigger gates
120 s hold periods
RetTime1..6 phase anchors
2.0 min subtraction in report calculation
```

### Preheater

Must preserve:

```text
left/right preheater TempCtrl
initial 40 C ready state
left/right 60 C drive
RetTime1/2 for 45 C events
RetTime3/4 for 55 C events
left/right heater temperature channels
precondition ModulePresent and MemoryState report checks
```

### Valve

Must preserve:

```text
upper/lower position sequence 6_1 -> 1_2 -> 6_1
Log UpperValve.Precision and LowerValve.Precision after each move
disconnect/reconnect keypad section if keypad report cells remain
fixed timing of audit reads if using existing report
```

### Column ID

Must preserve:

```text
message prompting insertion of A-D tags
wait for Column_A/B/C/D CardState=OK
Log Column_A/B/C/D.Description
abort if descriptions are not A/B/C/D
```

### Liquid Leak

Must preserve:

```text
manual leak prompt
wait for LiquidLeak=Leak
alarm/mute/cleanup prompt and alarm-state check
precondition LiquidLeakCalibrationValue report dependency
```

## Generation Discipline

Before writing any copy-ready CM method snippet, answer these questions:

1. Which report cells must this method satisfy?
2. Are those report cells RetTime-anchored or fixed-time?
3. Which raw channels must be acquired for those cells?
4. Which audit properties must be logged or state-changed?
5. Which variables are branch constants, and which are trigger state?
6. Which optional subdevices are required by the selected test?
7. Which abort/cleanup steps must remain to make the run meaningful?
8. If shortening the method, which report formulas must be rewritten?

Only after these answers are explicit should we generate script text.

## Practical Conclusion For 40 C Accuracy

For the example request:

```text
VH-C10-A temperature accuracy at 40 C only
```

the method can be reduced from the full `TEMPERATURE_ACCURACY` method, but it
cannot be reduced to:

```text
set 40 C
wait ready
write RetTime
```

The minimum safe dependency group is:

```text
verify/branch VH-C10-A
initialize CC setup
disable PCC TempCtrl by VH-compatible command if needed
initialize and acquire external thermometer channels
initialize StabVars
run external stability trigger loop
wait CC.TempReady AND StabVars.UpperReady AND StabVars.LowerReady
write RetTimes.RetTime3 = System.Retention
keep enough acquired data for RetTime3-1 .. RetTime3-0.2
return CC to 20 C and turn off/cleanup appropriate acquisition
```

The corresponding report can reuse `Temp Accuracy` row 68, or a new one-point
report must recreate the row-68 formulas around `RetTime3`.
