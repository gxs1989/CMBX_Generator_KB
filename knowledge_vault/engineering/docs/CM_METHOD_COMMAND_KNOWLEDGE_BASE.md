# CM Method Command Knowledge Base

This document records Chromeleon instrument-method command patterns observed in local TCC data. It is intended to become the method-generation side of the formula knowledge base.

## Source Status

Verified local sources:

- `tcc_temperature_control_analyzer_staging/CM_Method/Accuracy_method.txt`
- Decoded embedded method XML handled by `method_xml_flow.py`
- Sequence command links handled by `sequence_cmd_parser.py`
- Audit/report dependencies documented in `CM_FORMULA_KNOWLEDGE_BASE.md`

Important boundary:

- We can parse and summarize method commands.
- We can generate CM-like method tables as drafts.
- We do not yet write validated binary `.instmeth` payloads back into CMBX.
- Valve actuation is now confirmed from a decoded real TCC `VALVES` method: write `ColumnComp.UpperValve.CurrentPosition` and `ColumnComp.LowerValve.CurrentPosition` with values such as `6_1` and `1_2`.

## CM-Like Method Table Shape

Chromeleon displays method scripts as a line-numbered table. The application now preserves that review contract:

```text
#    Kind       Time    Command    Value    Comment
```

Examples:

```text
0    Stage      {Initial Time}    Instrument Setup
1    Comment                    =========================================================================
7    Stage      -30.000          Equilibration       Duration = 30.000 [min]
9    Branch     If                                   ColumnComp.ModelNo="VH-C10-A"
10   Command                    Variables.GenericLong9    12
11   Command                    Delay                    1                 [Val_FOQ_CM7...]: OK
13   Branch     Else If                              ColumnComp.ModelNo="VC-C10-A"
20   Branch     End If
98   End                         End
```

Rows with an empty `Time` usually belong to the current time/stage block. Rows whose `Time` is `If`, `Else If`, `Else`, `Trigger`, or `End Trigger` define control flow.

Important rendering rules:

- The first column is the CM row index and must be preserved for manual alignment with screenshots, Excel exports, and future edit plans.
- `Kind` is structural metadata. It must be used by future copy/paste, generation, and AI-edit workflows:
  - `Comment`: CM comment/header row. It may display its text in the visual `Command` column, but it is not a runnable command.
  - `Command`: executable property assignment or command step.
  - `Stage`: stage boundary such as `Instrument Setup`, `Equilibration`, `Run`, or `Stop Run`.
  - `Branch`: control-flow rows such as `If`, `Else If`, `Else`, and `End If`.
  - `End`: terminal method boundary.
- Stage rows use `Time` for the stage start time and `Command` for the stage name.
- Timetable stage rows may show `Duration = <minutes> [min]` in the `Value` column. For example, an `Equilibration` stage from `-30.000` to `0.000` renders `Duration = 30.000 [min]`.
- `If`, `Else If`, `Else`, and `End If` are control-flow rows in the `Time` column. The readable condition is placed in the `Value` column.
- Child commands inside an `If` branch must remain separate rows. They must not be concatenated into the `If` condition.
- Some decoded embedded-flow TSV files contain an `IfBlockNode` container row with no readable condition, followed by the real `IfNode` row. The container row is not a visible CM method-script row and must be skipped during rendering.
- If a decoded branch condition accidentally contains child command text before the real condition, keep the final readable CM condition such as `ColumnComp.ModelNo="VH-C10-A"` and leave the child commands as their own rows.
- The terminal `End` row is part of the CM-like method script and must be preserved.
- Comment/header rows are rendered in the `Command` column with blank `Value`.

Copy/paste implication:

- A plain four-column table cannot fully preserve whether a green row is a CM comment or a runnable command.
- The exported workbook therefore includes the `Kind` column. When converting back to a CM method table or generating a new method script, `Kind=Comment` rows must be recreated as comment rows, not as command rows.

## Verified Command Families

### Property Assignment

Pattern:

```text
<empty time>    <symbol path>    <value>    <comment>
```

Observed examples:

```text
ColumnComp.CC.TempCtrl                 On
ColumnComp.CC.Mode                     StillAir
ColumnComp.CC.Temperature.Nominal      Variables.GenericDouble2
Variables.GenericDouble1               10.0
StabVars.TriggerStab1                  1
```

### Delay

Pattern:

```text
Delay    <minutes>
```

Observed examples:

```text
Delay    1
Delay    3
Delay    60
```

Current assumption: method table values are minutes unless CM display/export states a unit.

### Wait

Pattern:

```text
Wait    <condition>
```

Observed examples:

```text
Wait    CC.TempReady
Wait    ColumnComp.CC.TempReady AND StabVars.LowerReady AND StabVars.UpperReady,
```

The optional trailing `Run=Continue` appears on the line after the condition in exported TXT for some rows.

## Generation Guardrails

Method generation must edit semantic roles, not all rows with the same command
suffix. A row such as `ColumnComp.PCC.Temperature.Nominal` is not equivalent to
`ColumnComp.CC.Temperature.Nominal`.

### TCC Stability Example

For `TEMPERATURE_STABILITY_AND_PCC_70_H`:

| Role | Row pattern | Generation rule |
|---|---|---|
| CC stability target | `ColumnComp.CC.Temperature.Nominal = 70.0` before `InjectPreparation` | This is the main stability target and may be changed for a custom stability point. |
| Baseline / pre-equilibration | User intent such as `40 C stable for 30 min, then 70 C stability` | Insert a pre-equilibration block before the CC target setpoint: set `ColumnComp.CC.Temperature.Nominal`, wait for ready, then delay. |
| VH PCC branch | `ColumnComp.PCC.Temperature.Nominal`, PCC triggers, and PCC RetTimes | Preserve unless the user explicitly designs a new PCC/report branch. Do not change these rows merely because the stability target changed. |

This is why a text-level replacement of every `Temperature.Nominal` row is
unsafe. The generator must first classify each command row by method role, then
apply the user's intent to the matching role only.

### RetTime Logging

Pattern:

```text
RetTimes.RetTimeN    System.Retention
```

Report formulas then read these values with:

```text
AUDIT.RetTimeN(1,"forward")
```

Reset pattern:

```text
RetTimes.RetTimeN    0
```

### Command String

Pattern:

```text
ColumnComp.CmdString    Cmd="<driver command>"
```

Observed examples:

```text
ColumnComp.CmdString    Cmd="PCC.TempCtrl=0"
ColumnComp.CmdString    Cmd="LedBar.ForceColor=1"
ColumnComp.CmdString    Cmd="LedBar.ForceColor=0"
```

This is useful when a direct method symbol is not available or when one method must work across multiple TCC variants. It is also the likely escape hatch for valve commands, but the exact valve command string must be verified.

### TCC Valve Position

Confirmed from decoded embedded method `VALVES` in `3000004.cmbx`:

```text
ColumnComp.UpperValve.CurrentPosition    6_1
ColumnComp.LowerValve.CurrentPosition    6_1
ColumnComp.UpperValve.CurrentPosition    1_2
ColumnComp.LowerValve.CurrentPosition    1_2
Log                                      UpperValve.Precision
Log                                      LowerValve.Precision
```

Observed sequence:

1. Set both valves to `6_1`.
2. Delay briefly.
3. Log `UpperValve.Precision` and `LowerValve.Precision`.
4. During the run, switch both valves to `1_2`.
5. Delay briefly.
6. Log precision.
7. Switch both valves back to `6_1`.
8. Delay and log precision again.

The same decoded method also uses:

```text
ColumnComp.CC_Temp.AcqOn
ColumnComp.CC_Temp.AcqOff
ColumnComp.Disconnect
ColumnComp.Connect
Wait    ColumnComp.Connected = Connected
ColumnComp.FastCoolActive    Off
```

These keypad/disconnect steps belong to the FOQ keypad functionality test and are not required for a pure periodic valve cycling method unless keypad behavior is part of the requirement.

### Acquisition On/Off

Pattern:

```text
<channel>.AcqOn
<channel>.AcqOff
```

Observed examples:

```text
ColumnComp.CC_Temp.AcqOn
ColumnComp.CC_U_Temp_Actual.AcqOn
ColumnComp.CC_L_Temp_Actual.AcqOn
ColumnComp.PWM_CCU_A.AcqOn
ColumnComp.PWM_CCL_A.AcqOn
Thermometer1.ExtTemp_UpperCC.AcqOn
Thermometer1.ExtTemp_LowerCC.AcqOn
```

### Trigger

Pattern:

```text
Trigger        "<name>",
<condition>,
TrueTime=<seconds>,
Delay=<minutes>
    <commands>
End Trigger
```

Observed use:

- Periodic stability checks using `TrueTime=30`.
- Range-exit checks using `TrueTime=5`.
- Abort logic using `AllowImmediateExecution=Yes`.

### Messages and Abort

Observed:

```text
Message          "Invalid ModelNo! Please reinspect in production!"
Protocol         "Evaluation at 10 deg C is skipped..."
System.AbortQueue
```

## Formula-To-Method Generation Rules

When generating a method from a report requirement:

1. Every `AUDIT.RetTimeN(...)` in a report formula implies that the method must write `RetTimes.RetTimeN = System.Retention`.
2. Every `chm.*` formula with `FixedChannel` implies that the method/injection must acquire that raw channel.
3. Every timed `AUDIT.<path>(time, direction)` implies that the method or device must write audit rows for that path.
4. Every pass/fail report criterion should map to a Definitions value or a known workbook formula.
5. Method generation must preserve device applicability:
   - `ColumnComp.ModelNo="VH-C10-A"`
   - `ColumnComp.ModelNo="VC-C10-A"`
   - additional variants as discovered.

## TCC Valve-Cycling Requirement Template

Requirement:

```text
TCC module periodically rotates upper and lower valves.
```

Method-generation interpretation:

- Device: TCC / ColumnComp.
- Control targets: upper valve and lower valve.
- Motion: alternate positions A/B, or position set defined by the module.
- Cycle count: user parameter.
- Dwell time per position: user parameter.
- Verification: audit rows should show `UpperValve.CurrentPosition` and `LowerValve.CurrentPosition` changes, if the driver logs them.

Known evidence:

```text
AUDIT.UpperValve.CurrentPosition(time,"backward/forward")
```

Confirmed write paths:

```text
ColumnComp.UpperValve.CurrentPosition    6_1
ColumnComp.UpperValve.CurrentPosition    1_2
ColumnComp.LowerValve.CurrentPosition    6_1
ColumnComp.LowerValve.CurrentPosition    1_2
```

Verified FOQ timing example:

```text
ColumnComp.UpperValve.CurrentPosition    1_2
ColumnComp.LowerValve.CurrentPosition    1_2
Delay                                    0.1
Log                                      UpperValve.Precision
Log                                      LowerValve.Precision
ColumnComp.UpperValve.CurrentPosition    6_1
Delay                                    0.2
ColumnComp.LowerValve.CurrentPosition    6_1
Delay                                    0.1
Log                                      UpperValve.Precision
Log                                      LowerValve.Precision
```

For a generated periodic valve-cycle method, use the direct property paths above rather than `ColumnComp.CmdString`.

## Decoded TCC Method Evidence

The following local probe output was generated from `C:\ProgramData\CMBX Data Explorer Workspace\packages\TCC Cost Out\Zollner\Production\3000004.cmbx`:

```text
knowledge_base/method_extract_probe/3000004/VALVES_embedded_method_flow.txt
knowledge_base/method_extract_probe/3000004/PREHEATER_embedded_method_flow.txt
knowledge_base/method_extract_probe/3000004/TEMPERATURE_ACCURACY_embedded_method_flow.txt
knowledge_base/method_extract_probe/3000004/TEMPERATURE_PRECISION_AND_FAN_embedded_method_flow.txt
knowledge_base/method_extract_probe/3000004/TEMPERATURE_STABILITY_AND_PCC_70_H_embedded_method_flow.txt
knowledge_base/method_extract_probe/3000004/TEMP_HEAT_UP_DOWN_20_50_20_embedded_method_flow.txt
```

## Next Evidence Tasks

1. Compare the decoded `VALVES` method with the `Valve_Keypad` report sheet and audit trail.
2. Extract equivalent VA and VH `VALVES` methods and confirm that the same valve write paths are stable across all TCC variants.
3. Promote the draft valve-cycle method into a validated reusable template.
