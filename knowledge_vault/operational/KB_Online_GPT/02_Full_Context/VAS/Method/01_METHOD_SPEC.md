# Online VAS Method Script Generation SPEC

Online_KB_Status: CANDIDATE_FOR_WEB_VALIDATION  
Upload_Allowed: Validation only  
Build_Date: 2026-07-23  
Scope: CM instrument-method Markdown authoring for later local preview and CMBX compilation

## Self Index

| Priority | Section | Purpose | Anchor |
|---:|---|---|---|
| 1 | Method MD generation contract | Required output syntax and authoring workflow | `#source-spec` |
| 2 | CM command language | Meaning of executable commands and device symbols | `#source-command` |
| 3 | Compiler/preflight rules | Local structural rejection rules | `#source-preflight` |

## Precedence

When sections overlap, the current Method MD generation contract controls the output format; compiler rules control whether the output can be packaged; command evidence controls semantic meaning. Never invent a command absent from source evidence.

<a id="source-spec"></a>
## Source SPEC: CM Method Script MD Generation SPEC

Build source name: `CM_METHOD_SCRIPT_MD_FORMAT_SPEC.md`

# CM Method Script MD Generation SPEC

KB_Version: 2.2  
Purpose: Single SPEC file for web AI / ChatGPT to generate Markdown method scripts that can be compiled by CMBX Data Explorer into standalone Chromeleon instrument-method CMBX files.  
Primary consumer: AI authoring prompt + Method Script Generator.  
Target copy locations:

```text
[local build source omitted]
[local build source omitted]
```

## 1. How To Use This SPEC With Web AI

Give this entire SPEC to the AI and ask it to generate only one method script in the strict fenced TSV format defined below.

The AI may explain the operation plan before the script, but the executable part must be the first fenced `tsv` code block and must use exactly four tab-separated columns:

```text
Time<TAB>Command<TAB>Value<TAB>Comment
```

Do not generate Markdown tables for executable scripts. Do not align columns with spaces. Use real tab characters.

## 2. Evidence And Official Help Alignment

This SPEC combines three evidence layers:

| Layer | Source | Use |
|---|---|---|
| CM Help | `[local build source omitted]` extracted help folder | Official Script Editor behavior, trigger semantics, custom-variable restrictions, Method Check behavior |
| CM Help printable PDF | `[local build source omitted]`, 8 pages, printed from `mk:@MSITStore:[local build source omitted]` | Complete printable Script Editor topic used for this SPEC |
| Local CM installation | `[local build source omitted]`, `InstrumentConfiguration_EN.chm`, driver command strings in `*.cdd` / `*.dll` | Local official help and command vocabulary |
| Reverse CMBX evidence | Decoded embedded method XML / CM-opened generated methods | Exact row rendering and packaging behavior |

Targeted extracted help topics used:

| Topic | Local help file |
|---|---|
| Script Editor main behavior | `InstrumentMethod_CSH\InstMetEdit_Script_Editor.htm` |
| Script Editor view, stages, time semantics | `InstrumentMethod\InstMetEdit_ScriptEditor_View.htm` |
| Conditional statements | `InstrumentMethod\InstMetEdit_CONDITIONALS.htm` |
| Custom Variables in instrument methods | `InstrumentMethod\InstMet_Custom_Variables.htm` |
| Modify Instrument Method | `InstrumentMethod\InstMetEdit_Modify_Method.htm` |
| Trigger reference | `ReferenceComm\REFERENCE_TRIGGER.htm` |

PDF page coverage:

| PDF pages | Help content captured |
|---|---|
| 1-3 | Script Editor purpose, columns, commands, stages, comments, time steps, negative time steps |
| 4 | Conditional statements and start of Trigger Block description |
| 5-7 | Trigger parameters: Condition, TrueTime, Delay, Limit, Hysteresis, AllowImmediateExecution; CM6 import notes |
| 8 | Find behavior and Method Check validity workflow |

## 3. CM Script Editor Facts From Official Help

The Script Editor is part of the Instrument Method Editor. It shows a chronological list of method steps, also called control commands, defined for an instrument in the Instrument Method Wizard.

Official column meanings:

| Column | Meaning |
|---|---|
| Time | When the command is executed |
| Command | Name of the command |
| Value | Value of a property or command parameter |
| Comment | Optional user information |

Official UI facts that matter for generation:

| Fact | Generation implication |
|---|---|
| Commands are grouped into predefined sections called stages. Stages have an orange background. | Use explicit stage rows for `Instrument Setup`, `Equilibration`, `Run`, `Stop Run`, etc. |
| Commands and properties vary by selected User Level and system configuration. | Unknown device symbols must be marked `Open Verification Required`; do not invent them. |
| A red icon indicates invalid command or value. Tooltip describes the error. | Red preview rows usually mean invalid symbol, invalid value, wrong trigger syntax, or unsupported branch/trigger nesting. |
| Red background indicates a command no longer valid, for example because system configuration changed. | Script validity depends on CM instrument configuration. |
| Script Editor provides autosuggestion in Command and Value; CTRL+SPACE opens suggestions. | AI should use exact known symbols from source CMBX/KB. |
| Custom variables can be used when assigning values and/or properties in the Value column. | Values such as `Variables.GenericDouble1` are valid when source method evidence uses them. |
| Method Check reports errors/warnings and links back to script locations. | Generated CMBX still needs CM Method Check before claiming runnable status. |
| New Command Rows append rows where the user specifies a valid symbol in the Command column. | AI-generated commands must use valid symbols, not descriptive phrases. |
| Find is case-insensitive and partial matches are found. | Useful for human review, but not part of the executable format. |

When the Script Editor view is required:

| Need | Rule |
|---|---|
| Add stages, time steps, or commands not available in module views | Use Script Editor syntax, not module-view prose |
| Create virtual channels | Use Script Editor; source evidence is required before generating unsupported virtual-channel rows |
| Add conditional statements | Use Script Editor branch rows (`If`, `Else If`, `Else`, `End If`) |
| Insert trigger blocks | Use Script Editor trigger-block syntax |

## 4. Strict Executable MD Format

Preferred source format:

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	==============================		
	IM to measure a TCC test		
	==============================		
{Initial Time}	Equilibration	Duration = 30.000 [min]	Equilibrate before run
0.000	Run		
120.000	Stop Run		
	End		
```

Rules:

| Rule | Required |
|---|---|
| First fenced code block | Must be `tsv` and must be the executable script |
| Columns | `Time`, `Command`, `Value`, `Comment` in this exact order |
| Separator | Real tab characters |
| Method name | Derived from MD filename unless generator overrides it |
| End row | Always include explicit `End` |

Accepted compatibility input:

If no fenced code block exists, the parser treats the whole MD/text file as raw script. This is only for legacy/DS-style input. For web AI output, always use strict fenced TSV.

## 5. Stage Rows

Stages are CM Script Editor sections and render with an orange background.

Common stages:

| Stage display | Meaning |
|---|---|
| `Instrument Setup` | Pre-run setup and global method configuration |
| `Equilibration` | Pre-run preparation, often negative-time setup |
| `Inject Preparation` | Commands required before injection, for example Wait or Autozero |
| `Inject` | Injection commands |
| `Start Run` | Commands immediately before the run, including default `AcqOn` commands |
| `Run` | Main run-time commands, triggers, waits, RetTimes |
| `Stop Run` | Cleanup, acquisition off, resets |
| `Post Run` | Post-run equilibration; may contain `AcqOff` if data acquisition extends the method run |

### 5.0 Exact Stage Display Names

Web-AI output must use the exact CM Script Editor display names shown in the
table above. In particular, always write:

```text
Instrument Setup
Inject Preparation
Start Run
Stop Run
Post Run
```

Do not emit the compact embedded-XML identifiers `InstrumentSetup`,
`InjectPreparation`, `StartRun`, `StopRun`, or `PostRun` in generated TSV.
Those compact forms are accepted by the local parser only as legacy input and
are normalized before preview/compilation. They are not the online authoring
contract. A numeric-time row whose stage name is misspelled or compact may be
classified as a Comment by strict consumers.

TSV:

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
-30.000	Equilibration	Duration = 30.000 [min]	Negative-time equilibration
0.000	Run		
120.000	Stop Run		
```

Time rules from CM Help:

| Rule | Meaning |
|---|---|
| Time column is decimal minutes | `2.500` means 2.5 min after injection / run time zero |
| Injection is performed at retention time 0 | Commands before injection have negative times; commands after injection have positive times |
| Time step can be inserted before an existing time step or stage | Use explicit time rows/stage rows, not free text |
| Negative time steps are allowed for equilibration | The value must be equal to or greater than the negative value of the equilibration stage |
| Stage `Duration = ... [min]` is minutes | Use this for long pre-run holds |

### 5.1 Time Anchors Must Be Executable

Do not create a row that has a numeric `Time` and only explanatory prose in
`Command`. A timed row is a CM time anchor and must be either:

| Valid timed row type | Example |
|---|---|
| Stage row | `13.000<TAB>Stop Run<TAB><TAB>` |
| Executable command/property row | `5.000<TAB>Variables.GenericBool8<TAB>0<TAB>Deactivate valve loop` |
| Trigger row | `0.010<TAB>Trigger<TAB>"LowPressureAbort",<TAB>Abort if pressure collapses` |

**A numeric value in `Time` must never appear alone.** The same TSV row must
also contain a valid stage, Trigger, executable command, or executable
property. A later row does not inherit a bare numeric time anchor.

Forbidden:

```tsv
1.000			Wrong: bare time row; it will be classified as a Comment
5.000	Stop dynamic stress loop and prepare static measurement state		Wrong: timed prose-only comment
7.000	Static leak-rate measurement starts		Wrong: timed prose-only comment
```

Correct pattern:

```tsv
1.000	Variables.GenericFloat1	System.Retention	Initialize the periodic-switch schedule
	Variables.GenericBool1	1	Arm Ping at the same time step
5.000	Variables.GenericBool8	0	Stop dynamic stress loop and prepare static measurement state
7.000	Variables.GenericDouble1	System.Retention	Static leak-rate measurement starts
```

If only an explanation is needed, attach it to the `Comment` column of the
nearest real timed command. Untimed comment rows are allowed before or after
the executable row.

### 5.2 Run Duration Must Cover All Run-Time Rows

The `Run` stage duration and the `Stop Run` stage start time must describe the
same run end.

Rules:

| Rule | Required behavior |
|---|---|
| `Run` has `Duration = X [min]` and `Stop Run` starts at `Y` | `X` must equal `Y` |
| A row inside `Run` has time `T` | `T` must be `<= Run Duration` and `<= Stop Run time` |
| Need a command at `13.500` | Set `Run Duration = 13.500 [min]` and `13.500<TAB>Stop Run` |
| Need `Stop Run` at `13.000` | Do not place Run-stage commands/comments after `13.000` |

The Method Script Generator treats a mismatch as a preflight error. Do not rely
on compiler-side normalization in authored MD.

## 6. Comment Rows

Comments are optional user information and are not commands.

TSV:

```tsv
Time	Command	Value	Comment
	External measured temperatures		
	Trigger 1: wait until 40 C is stable for 30 min		
```

Do not put executable commands into comment rows. Do not put explanatory text into command rows if it is not a CM command/property.

Timed comments are forbidden. A row such as `5.000<TAB>Some explanation` is
not a valid executable time anchor. Move the explanation to a real command's
`Comment` field.

## 7. Command / Property Rows

Command rows represent CM commands or property assignments.

TSV:

```tsv
Time	Command	Value	Comment
	ColumnComp.CC.ReadyTempDelta	0.1 [°C]	
	ColumnComp.CC.EquilibrationTime	0.5 [min]	
	ColumnComp.CC.Temperature.Nominal	Variables.GenericDouble1	Set target temperature
	Delay	3	Short local delay
	Wait	ColumnComp.CC.TempReady AND StabVars.TriggerStab1=0	Wait for ready gate
	RetTimes.RetTime1	System.Retention	Report time anchor
```

Use exact symbols from source CMBX/KB. Examples of currently known TCC command families:

| Family | Example |
|---|---|
| Column compartment | `ColumnComp.CC.Temperature.Nominal` |
| Acquisition on/off | `ColumnComp.CC_Temp.AcqOn`, `ColumnComp.CC_Temp.AcqOff` |
| Thermometer channels | `Thermometer1.ExtTemp_UpperCC.AcqOn` |
| RetTimes | `RetTimes.RetTime1` |
| StabVars | `StabVars.TriggerStab1` |
| TempVars | `TempVars.Ambient_Temp` |
| Variables | `Variables.GenericDouble1` |
| System | `System.Retention`, `System.AbortQueue` |

## 8. Custom Variables And Method Variables

Official CM Help distinguishes custom variables from ordinary device/method
properties. Custom injection and sequence variables may be used in the Script
Editor Value column, either directly or in expressions, for:

| Use | Allowed |
|---|---|
| Non-gradient properties | Yes |
| Command parameters | Yes |
| Conditional statements | Yes |
| Gradient properties | No |
| Stage time / time-step time | No |
| Creating or modifying custom variables inside an instrument method | No |
| `VirtualChannel` parameters `Name`, `Type`, `Unit`, `Evaluate` | No; constants only |
| `Wait` command parameters `Run` and `Timeout` | No; constants only |

Official custom-variable container form:

```text
System.Injection.CustomVariables.<name>
System.NextInjection.CustomVariables.<name>
System.PrevInjection.CustomVariables.<name>
System.PrevStandard.CustomVariables.<name>
System.Sequence.CustomVariables.<name>
```

If a referenced custom variable is not defined during sequence execution, the
Instrument Controller can abort. Therefore, AI output must not invent custom
variables. Use only variables explicitly present in the source method / user
contract, or mark `Open Verification Required`.

Important distinction:

| Symbol form | Meaning for generation |
|---|---|
| `System.Injection.CustomVariables.X` | Official CM custom variable; must exist in the injection list |
| `System.Sequence.CustomVariables.X` | Official CM custom sequence variable; must exist in the sequence |
| `Variables.GenericDouble1`, `Variables.GenericLong9`, `StabVars.*`, `TempVars.*` | Existing method/device variable symbols observed in TCC CMBX evidence; use only according to the source method role map |

## 9. Protocol, Message, And Log

Use these commands according to intent:

| Intent | Command | Example |
|---|---|---|
| Write a protocol/audit-style note | `Protocol` | `Protocol	"Stability End"` |
| Show/record a user message | `Message` | `Message	"Invalid ModelNo!"` |
| Log a variable/property value | `Log` | `Log	GenericLong9` |

Avoid:

```tsv
Time	Command	Value	Comment
	Log	"Stability End"	Wrong: string literal is not a variable/property log target
```

Prefer:

```tsv
Time	Command	Value	Comment
	Protocol	"Stability End"	Text note
```

## 10. Conditional Blocks

Official Help:

Conditional statements are `If`, `Else If`, `Else`, and `End If`. They ensure Chromeleon executes commands only if a condition is true. Chromeleon executes commands after an `If` until the next `Else`, `Else If`, or `End If`.

Logical conditions usually consist of:

```text
parameter / device property + comparison operator + value
```

Operators:

```text
<, >, =, <=, >=, <>
```

Expressions:

```text
Any expression that results in a numerical value can be used as a logical condition.
Zero is false; non-zero is true.
```

Strict TSV form:

```tsv
Time	Command	Value	Comment
If		ColumnComp.ModelNo="VH-C10-A"	VH branch
	Variables.GenericLong9	12	
Else If		ColumnComp.ModelNo="VC-C10-A"	VC branch
	Variables.GenericLong9	10	
Else			
	Message	"Invalid ModelNo! Please reinspect in production!"	
	System.AbortQueue		
End If			
```

Rules:

| Rule | Required |
|---|---|
| Branch keyword | Put `If`, `Else If`, `Else`, `End If` in `Time` |
| Condition | Put condition in `Value` on the same branch row |
| `Else` / `End If` | Leave `Command` and `Value` empty |
| Else If position | After `If`, before `Else` |
| Number of Else If | No limit in CM Help |

Conditional execution cautions from CM Help:

| Caution | Generation implication |
|---|---|
| If commands that change flow can interrupt gradients and continue isocratically | Do not add flow-gradient conditionals without module-specific evidence |
| Signal values cannot be evaluated when data acquisition is disabled or interrupted | Any conditional depending on signal/channel value requires acquisition to be on before evaluation |
| Method settings for certain modules cannot be changed during the injection run; such If commands may be ignored | For run-time module setting changes, use source-method evidence or mark `Open Verification Required` |

Compatibility note:

Raw input such as `If<TAB>ColumnComp.ModelNo="VH-C10-A"` may be normalized by the parser, but web AI should output the strict TSV form above.

## 11. Trigger Blocks

Official Help:

A trigger block consists of a trigger step and a block of method steps. Commands in the trigger block are executed if the trigger condition becomes true. Trigger commands execute upon each transition from false to true, i.e. edge triggering.

Trigger blocks are displayed with a green background and are closed by an `End Trigger` row.

Strict TSV form for the Method Script Generator:

```tsv
Time	Command	Value	Comment
Trigger		"T_HOLD_40",	Hold 40 C until stable for 30 min
	Condition	(CC.Temperature.Nominal=Variables.GenericDouble1) AND CC.TempReady,	
	TrueTime	1800	
	Delay	0	
	Limit	1	
	Hysteresis	0	
	AllowImmediateExecution	No	
	Protocol	"40 C stable hold complete"	Trigger action
	ColumnComp.CC.Temperature.Nominal	Variables.GenericDouble2	Trigger action
End Trigger			
```

The generator compiles the trigger name and trigger parameters into the CM Trigger row's expandable Value text. Trigger action rows remain actions inside the trigger block.

### 11.1 Trigger Parameter Rules From CM Help

| Parameter | Meaning | Symbol references |
|---|---|---|
| Name | Literal string in double quotes, for example `"Trigger1"`; each trigger name must be unique | No |
| Condition | Trigger condition; can use parameters, properties, signals, deltas, logical/arithmetic operators | Yes |
| TrueTime | Seconds the condition must be true before activation; absolute time, not paused by hold | Yes, evaluated once when trigger is created |
| Delay | Delay time in seconds between fulfilled condition and command execution | No; constant numeric expression only |
| Limit | Upper limit for trigger executions; default is 1000; the trigger is automatically deleted after the corresponding number of activations | Yes, evaluated once when trigger is created |
| Hysteresis | Percent fraction around comparison value; reduces noise sensitivity | No; constant numeric expression only |
| AllowImmediateExecution | Whether to execute immediately if condition is true at definition time | No; valid values `No`/`Yes` or `0`/`1`; default is `Yes` |

Never write `Limit Infinite`, `Limit=Infinite`, `Limit Unlimited`, or similar
text. CM Help defines `Limit` as a numeric expression. If the trigger should
repeat throughout the run, either omit the `Limit` row and accept the CM default
limit, or use an explicit numeric limit large enough for the run, for example
`Limit	1000`.

Autosuggest note from CM Help:

```text
Autosuggest for symbol references works only for Condition, Limit, and TrueTime.
All other trigger parameters do not accept symbol references.
```

### 11.2 Trigger Condition Syntax

Examples from CM Help:

```text
(UV_VIS_1>100) AND (UV_VIS_2>100)
(UV_VIS_1+UV_VIS_2)>200
(UV_VIS_1>100) AND NOT (UV_VIS_2>200)
```

Operators:

```text
Arithmetic: +, -, *, /, **
Logical: AND, OR, NOT, XOR
Comparison: <, >, =, <=, >=, <>
```

Use parentheses for clarity.

### 11.3 Trigger Timing Semantics

Important:

| Parameter | Unit |
|---|---|
| `TrueTime` | seconds |
| Trigger `Delay` | seconds |
| Stage `Duration = ... [min]` | minutes |

If `Delay` is used with `TrueTime`, the command executes after:

```text
TrueTime + Delay
```

TrueTime is also used as false time after activation, or if the condition is initially true and `AllowImmediateExecution=No`.

### 11.4 Trigger Limits And Nesting

Do not reuse a trigger name. CM Method Check rejects duplicate trigger names.

Do not generate nested trigger blocks. CM Help states that nested triggers are not allowed in Chromeleon 7; imported nested triggers are converted to comment lines and an error is issued.

Do not place free `If / Else / End If` blocks inside a trigger unless a decoded CM7 CMBX source method proves the exact structure. Prefer:

| Safer pattern | Use when |
|---|---|
| Separate triggers with more specific conditions | Conditional logic can be moved into trigger condition |
| Trigger sets a state variable, ordinary branch outside trigger uses that state | Need procedural branching |
| `Open Verification Required` | Structure is not proven |

## 12. Time And Unit Rules

| Construct | Unit / meaning |
|---|---|
| Stage time such as `-30.000`, `0.000`, `120.000` | decimal minutes in the method timeline |
| Stage `Duration = 30.000 [min]` | minutes |
| Trigger `TrueTime=1800` | seconds |
| Trigger `Delay=5` | seconds |
| Command `Delay 30` | command value from source method; unit must be verified from source method context |

Do not express a 30-minute stability hold as ordinary command `Delay 30` unless source method evidence proves that exact meaning. Prefer stage duration or trigger `TrueTime=1800`.

### 12.1 Periodic Trigger Scheduling

For source-grounded TCC valve stress methods, periodic switching is scheduled
against `System.Retention`, which is in minutes. Use an absolute next-edge
variable, for example:

```text
6 s period: Variables.GenericFloat1 = System.Retention+0.1
3 s period: Variables.GenericFloat1 = System.Retention+0.05
```

Do not describe ordinary command `Delay 0.1` as a 6-second cycle. Do not use
Trigger `TrueTime=0.1` as the cycle period. Trigger `TrueTime` and trigger
`Delay` are seconds; the verified recurring schedule is controlled by the
`System.Retention` comparison and next-edge assignment. Preserve the complete
source Ping/Pong state handoff and the source Delay rows around valve movement.

## 13. Method Check And Red Cells

Official Help:

After creating a method, use `Check Method`. Errors and warnings are shown in the Method Check Results pane with source links.

Likely causes for red cells:

| Red pattern | Likely cause |
|---|---|
| Unknown command/property | Symbol not available for current instrument config/user level |
| Trigger parameter rows rendered as ordinary commands | Trigger syntax not packed into Trigger value |
| `Log "text"` | `Log` expects property/variable, not arbitrary string |
| Empty `If` followed by condition row | Branch condition not on same branch row |
| Custom variable undefined at sequence run time | Instrument Controller may abort |
| Custom variable used for stage/time-step time | Not supported by CM Help |
| Nested trigger | Not allowed in CM7 |
| Duplicate trigger name | Rejected by Method Check |
| Symbol references in trigger `Delay`, `Hysteresis`, or `AllowImmediateExecution` | Not accepted by CM Help |

## 14. Compiler Contract For Structural MD -> CMBX

The first executable fenced `tsv` block is structural compiler input, not free
Markdown prose and not raw Chromeleon XML. The local compiler maps rows into CM
method nodes using these contracts:

| MD row pattern | Compiler meaning |
|---|---|
| `Kind=Stage` or known stage name in `Command` | CM `StageNode` plus a `TimeStepNode` |
| `Time=If / Else If / Else / End If` | CM branch block |
| `Time=Trigger` through `End Trigger` | One `System.Trigger` command with folded trigger parameters and child commands |
| `Kind=Comment` with empty `Time` | CM green comment node |
| `Kind=Comment` with numeric `Time` | Preflight error; timed prose is not executable |
| `Command=Condition/TrueTime/Delay/Limit/Hysteresis/AllowImmediateExecution` inside Trigger | Trigger parameter row |
| Trigger parameter outside Trigger | Preflight error |
| `Run Duration` != `Stop Run` time | Preflight error |
| Run-stage row later than `Stop Run` | Preflight error |

Compiler behavior is intentionally strict. If a generated MD is rejected, correct
the MD so the CM structure is explicit; do not expect the compiler to infer what
the author meant.

## 15. AI Authoring Workflow

Before producing the TSV block, the AI must internally perform:

1. Interpret the user intent as a CM operation contract.
2. Identify device model, test type, setpoints, baseline, target, duration, sensors, RetTimes, triggers, and report expectations.
3. Choose known command families from source KB / CMBX evidence.
4. Decide if the existing report can calculate the requested output.
5. Generate a strict TSV script.
6. Mark unknown commands/config/report constraints as `Open Verification Required`.

The final answer to the user may include explanation, but the executable script must be one strict TSV block.

## 16. Validation Checklist For Web AI Output

| Check | Must pass |
|---|---|
| First fenced executable block is `tsv` | Yes |
| Columns are exactly `Time`, `Command`, `Value`, `Comment` | Yes |
| Uses tabs, not Markdown table pipes | Yes |
| Stage rows use known stage names | Yes |
| Branch rows have keyword in `Time` and condition in `Value` | Yes |
| Trigger rows have unique quoted names | Yes |
| Trigger parameter rows stay inside Trigger block | Yes |
| Trigger `TrueTime` and trigger `Delay` are seconds | Yes |
| Trigger `Delay`, `Hysteresis`, `AllowImmediateExecution` do not use symbol references | Yes |
| Numeric `Time` rows are stages, triggers, or executable commands | Yes |
| No timed prose-only comments | Yes |
| `Run Duration = X [min]` equals `Stop Run` time `X` | Yes |
| No Run-stage row occurs after `Stop Run` | Yes |
| Custom variables are not invented and are not used for stage/time-step time | Yes |
| Branch/signal conditions only evaluate signals after acquisition is enabled | Yes |
| No nested triggers | Yes |
| No arbitrary text passed to `Log` | Yes |
| Long holds use stage duration or trigger TrueTime, not ambiguous command Delay | Yes |
| Method ends with `End` | Yes |
| Unknown device/config/report dependencies are marked | Yes |

## 17. Minimal Valid Template

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	==============================		
	Example generated CM method		
	==============================		
If		ColumnComp.ModelNo="VH-C10-A"	
	Variables.GenericDouble1	40.0 [°C]	Baseline temperature
	Variables.GenericDouble2	60.0 [°C]	Target temperature
Else			
	Message	"Invalid ModelNo! Please reinspect in production!"	
	System.AbortQueue		
End If			
-30.000	Equilibration	Duration = 30.000 [min]	Equilibrate at baseline before run
	ColumnComp.CC.Temperature.Nominal	Variables.GenericDouble1	
0.000	Run		
	ColumnComp.CC_Temp.AcqOn		
	Thermometer1.ExtTemp_UpperCC.AcqOn		
	Thermometer1.ExtTemp_LowerCC.AcqOn		
	ColumnComp.CC.Temperature.Nominal	Variables.GenericDouble2	
Trigger		"T_TARGET_READY",	Wait until target is ready for 2 min
	Condition	(CC.Temperature.Nominal=Variables.GenericDouble2) AND CC.TempReady,	
	TrueTime	120	
	Delay	0	
	Limit	1	
	Hysteresis	0	
	AllowImmediateExecution	No	
	RetTimes.RetTime1	System.Retention	Report anchor
	Protocol	"Target temperature ready"	
End Trigger			
120.000	Stop Run		
	ColumnComp.CC_Temp.AcqOff		
	Thermometer1.ExtTemp_UpperCC.AcqOff		
	Thermometer1.ExtTemp_LowerCC.AcqOff		
	End		
```

<a id="source-command"></a>
## Source COMMAND: CM Instrument Command Knowledge Base

Build source name: `CM_INSTRUMENT_COMMAND_KNOWLEDGE_BASE_V2.md`

# CM Instrument Command Knowledge Base

This document is the working knowledge base for Chromeleon instrument-method
commands. It focuses on the method-script side, not report formulas.

中文目的：把 CM instrument method 里可执行的命令、设备树、变量、触发器和
报告证据之间的关系整理出来，作为以后生成 instrument method 的基础。

## Source Status

Current evidence sources:

```text
User screenshot:
  Instrument Setup tree:
    ColumnOven
    PumpModule
    SamplerModule
    Thermometer
    UV
    Variables
    System
    End

Local Chromeleon installation:
  [local build source omitted]
  [local build source omitted]
  [local build source omitted]
  [local build source omitted]
  [local build source omitted]
  [local build source omitted]

Decoded CMBX methods:
  knowledge_base/tcc_reverse_probe/VH/6000001/*_embedded_method_flow.txt
  knowledge_base/tcc_reverse_probe/VC/3000004/*_embedded_method_flow.txt
  knowledge_base/tcc_reverse_probe/VA/0000003/*_embedded_method_flow.txt

Existing project notes:
  cmbx_data_explorer/docs/CM_METHOD_COMMAND_KNOWLEDGE_BASE.md
  cmbx_data_explorer/docs/CM_INSTRUMENT_CONFIGURATION_KNOWLEDGE_BASE.md
  cmbx_data_explorer/docs/TCC_CM_METHOD_SCRIPT_DEPENDENCY_MODEL.md
```

Boundary:

```text
已确认：
  可以从 CMBX 中解出 CM-like method flow。
  可以识别 set/wait/trigger/log/acq/abort/message 等命令族。
  可以建立 method command -> audit/raw data -> report formula 的合同。

未确认：
  CHM help 还没有完整文本化。
  还不能保证生成二进制 .instmeth payload 后可被 CM 原生导入。
  每个设备树节点下的完整命令清单仍需要继续从 CM help / driver definition / 实测 CMBX 补齐。
```

## Mental Model

CM instrument method commands are not one flat language. They are selected from
an instrument setup tree. The visible script line depends on both:

```text
configured instrument tree
-> selected device node
-> command/property/channel under that node
-> method stage and timing
-> report/audit evidence expected later
```

截图里的框架应理解为：

| Instrument Setup Node | 中文解释 | TCC FOQ 当前映射 | 作用 |
| --- | --- | --- | --- |
| `ColumnOven` | 柱温箱/温控模块 | `ColumnComp` | TCC 主设备，包含 CC/PCC/preheater/valve/leak 等子设备 |
| `PumpModule` | 泵模块 | not used in standalone TCC FOQ | 以后扩展 HPLC 系统 FOQ 时需要 |
| `SamplerModule` | 自动进样器 | not used in standalone TCC FOQ | 以后扩展 HPLC 系统 FOQ 时需要 |
| `Thermometer` | 外部温度计 | `Thermometer`, `Thermometer1` | 外部温度传感器和环境温度通道 |
| `UV` | UV 检测器 | not used in TCC FOQ | 以后扩展 detector FOQ 时需要 |
| `Variables` | 方法变量 | `Variables.*`, `RetTimes.*`, `StabVars.*`, `TempVars.*` | 脚本状态、阈值、RetTime、触发器状态 |
| `System` | CM 系统命令 | `System.Trigger`, `System.Retention`, `System.AbortQueue` | 触发器、当前保留时间、停止队列 |
| `End` | 方法终止 | `End`, stage end | 方法阶段结束 |

## Method Stages

Decoded methods show these stage names:

```text
InstrumentSetup
Equilibration
InjectPreparation
StartRun
Run
StopRun
```

中文理解：

- `InstrumentSetup`: 方法说明和全局设置入口。
- `Equilibration`: 进样前设备状态准备，如温控、模式、变量、采集率。
- `InjectPreparation`: 真正 run 前的等待和 RetTime/trigger 初始化。
- `StartRun`: 打开采集通道，开始记录 raw data。
- `Run`: 执行测试动作、等待、触发器、记录 audit/RetTime。
- `StopRun`: 关闭采集、关闭温控、恢复安全状态。

生成方法时不能只复制 `Run` 部分。很多 `Run` 命令依赖前面阶段设置好的
变量、ReadyTempDelta、EquilibrationTime、AcqOn 通道和 trigger gate。

## Command Families

### Property Assignment

Pattern:

```text
SET <device/property> = <value>
```

Examples:

```text
SET ColumnComp.CC.TempCtrl = On
SET ColumnComp.CC.Mode = StillAir
SET ColumnComp.CC.Temperature.Nominal = Variables.GenericDouble3
SET ColumnComp.PrehtLeft.TempCtrl = On
SET ColumnComp.UpperValve.CurrentPosition = 6_1
```

中文解释：这是最常见的设备控制方式。它要求 CM 配置里确实存在该设备/属性。

Generation rule:

```text
Before emitting a SET line, validate the target symbol exists for the selected device profile.
```

### Delay

Pattern:

```text
RUN Delay <minutes>
```

Examples:

```text
RUN Delay 0.1
RUN Delay 1
RUN Delay 5
RUN Delay 60
```

中文解释：延时本身不产生测试证据，但它决定 audit 时间、raw data window 和
operator prompt 的相对位置。

### Wait

Pattern:

```text
RUN Wait <condition>
```

Examples:

```text
RUN Wait CC.TempReady
RUN Wait PrehtLeft.TempReady AND PrehtRight.TempReady
RUN Wait ColumnComp.Connected = Connected
RUN Wait Column_A.CardState=OK AND Column_B.CardState=OK AND Column_C.CardState=OK AND Column_D.CardState=OK
```

中文解释：Wait 不是普通暂停，它定义“下一步测试证据有效”的条件。

### System.Trigger

Pattern:

```text
RUN System.Trigger "<name>", <condition>, TrueTime=<seconds>, Limit=<n>, Hysteresis=<x>, AllowImmediateExecution=<Yes/No>
  commands executed when trigger fires
```

Observed roles:

| Role | 中文解释 | Example |
| --- | --- | --- |
| stability loop | 周期性检查外部温度计是否稳定 | `Gradient_1`, `Gradient_2` |
| boundary crossing | 到达温度边界时写 RetTime | preheater 45/55 C, PCC 50/40 C |
| run-end gate | 满足结束条件后结束 run | `END_RUN` |
| abort guard | 超时或异常时中止队列 | `Abort` |

Important rule:

```text
If a trigger writes a RetTime, the trigger condition is part of the report calculation contract.
```

### RetTime Logging

Pattern:

```text
SET RetTimes.RetTimeN = 0
SET RetTimes.RetTimeN = System.Retention
```

中文解释：RetTime 是 method 和 report 之间最重要的桥。报告公式里
`AUDIT.RetTimeN(...)` 读的就是这里写出的时间锚点。

Examples:

```text
TEMPERATURE_ACCURACY:
  RetTime1 -> first stable setpoint
  RetTime2 -> second stable setpoint
  RetTime3 -> 40 C stable point in VH/VC/VA accuracy ladder

PREHEATER:
  RetTime1 -> left reaches 45 C
  RetTime2 -> right reaches 45 C
  RetTime3 -> left reaches 55 C
  RetTime4 -> right reaches 55 C

TEMP_HEAT_UP_DOWN_20_50_20:
  RetTime1/3 -> heat-up start/end
  RetTime4/6 -> cool-down start/end
```

Generation rule:

```text
If reusing an existing report template, keep RetTime numbering and meaning unchanged.
If changing RetTime numbering, rewrite report formulas and DB mapping together.
```

### Acquisition On/Off

Pattern:

```text
RUN <channel>.AcqOn
RUN <channel>.AcqOff
```

Examples:

```text
RUN ColumnComp.CC_Temp.AcqOn
RUN Thermometer1.ExtTemp_UpperCC.AcqOn
RUN Thermometer1.ExtTemp_LowerCC.AcqOn
RUN ColumnComp.PCC_Temp.AcqOn
RUN ColumnComp.PrehtLeft_Temp.AcqOn
```

中文解释：报告里的 `chm.*` raw signal formula 只能读取已经采集的通道。

Generation rule:

```text
Every report FixedChannel must be covered by an AcqOn window that spans the formula time range.
```

### Log

Pattern:

```text
RUN Log <audit/property>
```

Examples:

```text
RUN Log Column_A.Description
RUN Log UpperValve.Precision
RUN Log LowerValve.Precision
RUN Log PrehtLeft.Temperature.Value
```

中文解释：Log 产生 audit evidence。Column ID、Valve、Liquid Leak 这类测试
很多结果不是 raw signal 算出来的，而是 audit property 被记录后由报告读取。

### Message and Protocol

Examples:

```text
RUN Message "Please plug the column ID adapters..."
RUN Message "QUEUE WAS ABORTED! Please check your test setup..."
RUN Protocol "***Temperature increase observed on right pre-heater...***"
```

中文解释：这些不是装饰文字。对手动测试项，Message/Protocol 是测试流程的一部分，
提示操作者插卡、加水、按 keypad 或处理异常。

### System.AbortQueue

Pattern:

```text
RUN System.AbortQueue
```

Observed use:

- unsupported device model
- column ID mismatch
- timeout / stability not reached
- preheater short-circuit condition

中文解释：很多 FOQ method 自己就有 pass/fail guard，并不是只靠 report 判断。

### CmdString

Pattern:

```text
RUN ColumnComp.CmdString Cmd="<driver command>"
```

Examples:

```text
RUN ColumnComp.CmdString Cmd="PCC.TempCtrl=0"
RUN ColumnComp.CmdString Cmd="PREH.L.PID.Kp=10000"
RUN ColumnComp.CmdString Cmd="PREH.L.PID.Ki=1200"
RUN ColumnComp.CmdString Cmd="LedBar.ForceColor=1"
```

中文解释：`CmdString` 是 driver-level escape hatch。它常用于没有直接方法符号
或需要兼容不同 TCC 型号的底层命令。生成时要谨慎，因为它比普通 SET 更依赖
driver 内部命令名。

## TCC Command Groups

### ColumnComp / ColumnOven

Core paths:

```text
ColumnComp.CC.TempCtrl
ColumnComp.CC.Temperature.Nominal
ColumnComp.CC.TempReady
ColumnComp.CC.ReadyTempDelta
ColumnComp.CC.EquilibrationTime
ColumnComp.CC.Mode
ColumnComp.CC_Temp
ColumnComp.LiquidLeakSensor
```

中文解释：TCC FOQ 里的 `ColumnOven` 在 CMBX/method 中主要表现为
`ColumnComp`。`CC` 是 column compartment controller。

### Preheater

Required paths:

```text
ColumnComp.PrehtLeft.TempCtrl
ColumnComp.PrehtRight.TempCtrl
ColumnComp.PrehtLeft.Temperature.Nominal
ColumnComp.PrehtRight.Temperature.Nominal
ColumnComp.PrehtLeft.TempReady
ColumnComp.PrehtRight.TempReady
ColumnComp.PrehtLeft_Temp
ColumnComp.PrehtRight_Temp
ColumnComp.PREH_L_HeaterTemp_Actual
ColumnComp.PREH_R_HeaterTemp_Actual
```

Key command idea:

```text
set both preheaters to 40 C
wait ready
heat left/right toward 60 C
write RetTimes at 45 C and 55 C
restore/turn off controls
```

### Valve

Confirmed direct write paths:

```text
SET ColumnComp.UpperValve.CurrentPosition = 6_1
SET ColumnComp.LowerValve.CurrentPosition = 6_1
SET ColumnComp.UpperValve.CurrentPosition = 1_2
SET ColumnComp.LowerValve.CurrentPosition = 1_2
RUN Log UpperValve.Precision
RUN Log LowerValve.Precision
```

中文解释：周期性转阀方法应优先用 `CurrentPosition` 直接属性，而不是猜
`CmdString`。但位置字符串必须来自实际阀类型/端口配置。

### Thermometer

Current TCC FOQ factory-test channels:

```text
Thermometer1.ExtTemp_UpperCC
Thermometer1.ExtTemp_LowerCC
Thermometer.Environment_Temperature
```

中文解释：这些不是默认每台 CM 都一定有的通道，通常依赖外部温度计和虚拟通道配置。

### Variables

Observed groups:

```text
Variables.GenericDouble*  -> setpoints / thresholds
Variables.GenericLong*    -> counters / page count / branch context
Variables.GenericBool*    -> trigger gates / state flags
TempVars.*                -> ambient and temporary temperature values
StabVars.*                -> external thermometer stability logic
CCCalib.*                 -> calibration point and deviation values
RetTimes.*                -> report-visible time anchors
```

中文解释：变量名不能随便改。它们连接 IF 条件、Trigger、RetTime、report 和
processing/IRC 行为。

### System

Important paths:

```text
System.Retention
System.Trigger
System.AbortQueue
```

中文解释：

- `System.Retention`: 当前 run 时间，用来写 RetTime。
- `System.Trigger`: 异步事件/边界检测/稳定性循环。
- `System.AbortQueue`: 中止当前队列。

## Generation Checklist

Before generating or editing a CM instrument method:

1. Identify the target Instrument Setup node: `ColumnOven`, `Thermometer`, `Variables`, `System`, etc.
2. Validate required symbols against the target device configuration.
3. Preserve stage context: setup, acquisition, run, cleanup.
4. Preserve RetTime semantics if reusing report formulas.
5. Preserve AcqOn windows for every report raw channel.
6. Preserve Log commands for audit-based report formulas.
7. Treat `CmdString` as driver-specific and verify before reuse.
8. Keep operator `Message` steps when TD requires manual action.
9. Add a safe cleanup path: `AcqOff`, `TempCtrl Off`, reset flags where required.

## Open Work

1. Extract searchable text from `CM7Help_EN.CHM` and `InstrumentConfiguration_EN.chm`.
2. Build a per-node command catalog for the screenshot tree:
   - `ColumnOven`
   - `PumpModule`
   - `SamplerModule`
   - `Thermometer`
   - `UV`
   - `Variables`
   - `System`
3. Link every command catalog entry to:
   - source CM help or driver evidence,
   - observed CMBX method usage,
   - required configuration symbols,
   - report/audit evidence created.
4. Convert the current method-flow knowledge into a schema that can emit:
   - CM-like method script Excel/text,
   - required configuration checklist,
   - report formula contract.

<a id="source-preflight"></a>
## Source PREFLIGHT: CM Compiler Rules

Build source name: `CM Compiler Rules.MD`

﻿# CM Compiler Rules

KB_Version: 1.1  
Status: Supplementary notes for Method Script Generator.

## Rule Priority

Use these documents in this order:

1. `CM_METHOD_SCRIPT_MD_FORMAT_SPEC.md` is the single strict SPEC for AI authoring and app compilation.
2. `MD_TO_STANDALONE_METHOD_CMBX_PACKAGING.md` explains the CMBX packaging and roundtrip validation path.
3. This file only records compiler-facing reminders and migration notes.

If this file conflicts with the strict format spec, the strict format spec wins.

## Compiler-Facing Rules

| Topic | Rule |
|---|---|
| Columns | Executable MD uses four tab-separated columns: `Time`, `Command`, `Value`, `Comment`. |
| Branch | `If`, `Else If`, `Else`, `End If` belong in `Time`; condition belongs on the same branch row. |
| Trigger | Trigger name and parameters are compiled into one CM trigger value block. |
| Trigger parameters | Use `Condition`, `TrueTime`, `Delay`, `Limit`, `Hysteresis`, `AllowImmediateExecution` inside the Trigger block. |
| Trigger limit | `Limit` must be numeric or blank; do not write `Infinite`, `inf`, or `unlimited`. |
| Comments | Comment rows have text in `Command` and empty `Value`; they are not executable. |
| Timed comments | Numeric `Time` on a comment/prose row is a preflight error. Move the prose to a real command row's `Comment` field. |
| Run duration | `Run` stage `Duration = X [min]` must equal explicit `Stop Run` time `X`. |
| Run rows | No Run-stage row may occur later than `Stop Run`. |
| End | Generated production MD should include an explicit `End` row. |
| Units | Stage `Duration` is minutes; trigger `TrueTime` and trigger `Delay` are seconds; command `Delay` is source-method-specific and must not be used for long holds without evidence. |

## Preflight Severity

| Severity | Effect |
|---|---|
| Error | Preview marks the row red and CMBX generation is blocked. |
| Warning | CMBX generation is allowed, but the script remains configuration-specific or needs source evidence. |

## Known Red-Cell / Blocked Patterns

| Pattern | Safer alternative |
|---|---|
| Empty `If` row followed by condition as a normal row | Put condition on the same `If` row. |
| `Log "some text"` | Use `Protocol "some text"` or `Message "some text"`. |
| Trigger type words such as `External`, `Second`, `Reset` emitted as ordinary rows | Encode trigger name/condition/parameters in the strict Trigger block. |
| Free nested `If` inside a Trigger block | Use separate trigger conditions or move branch logic outside the trigger unless source evidence proves the structure. |
| Timed prose-only row, such as `5.000<TAB>Static measurement starts` | Put a real executable command at `5.000` and place the explanation in its `Comment`. |
| `Run Duration = 13.5 [min]` with `13.000<TAB>Stop Run` | Make both values identical or move the later rows before `Stop Run`. |
