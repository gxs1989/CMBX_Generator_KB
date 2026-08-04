# CM Method Script MD Format Specification

KB_Version: 1.0  
Scope: Markdown source format for CMBX Data Explorer Method Script Generator  
Target Folder: `C:\ProgramData\CMBX Data Explorer Workspace\KB\FOQ Template`

## 1. Purpose

This document defines the supported Markdown/text formats for generating a standalone Chromeleon instrument-method CMBX from a method script.

The goal is to avoid GPT/free-form Markdown ambiguity. The preferred source is a strict TSV table inside the first fenced code block. The parser also accepts DS-style raw script files where the whole file is the executable script and no code fence/header is present.

## 2. File Naming Rule

The generated method name is derived from the MD filename unless the generator UI or CLI explicitly overrides it.

Example:

| MD filename | Default generated method name |
|---|---|
| `A new method.md` | `A new method` |
| `TCC_Stability_70C_ValveStress.md` | `TCC Stability 70C ValveStress` |

If CM still displays the carrier/template method name, the CMBX packer must update both:

- CMBX header item name / filename / URL
- embedded `.instmeth_1.cmd` method-name payload

## 3. Script Source Forms

### 3.1 Preferred: fenced TSV block

If the MD file contains a fenced code block, the first fenced code block is the compiled source. Use `tsv` as the code fence language.

Required columns, in this exact order:

```text
Time<TAB>Command<TAB>Value<TAB>Comment
```

Do not use Markdown tables for the executable script. Do not align columns with spaces. Use real tab characters.

Minimal structure:

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	==============================		
	IM to measure a TCC test		
{Initial Time}	Equilibration	Duration = 30.000 [min]	
0.000	Run		
120.000	Stop Run		
	End		
```

### 3.2 Accepted: DS-style raw script

If the MD file has no fenced code block, the whole file is parsed as the method script. This supports direct DS/GPT output such as:

```text
==========================================================================================
IM to measure TCC stability at 70 C, then cool down to 40 C for accuracy
==========================================================================================
If	ColumnComp.ModelNo="VH-C10-A"
	Variables.GenericLong9	12
Else
	Message	"Column compartment model unknown. Please reinspect in production!"
	System.AbortQueue
End If
Trigger 1: 70 C stability - 15 min hold after internal ready
Trigger	"STAB_70C",
	(CC.Temperature.Nominal=Variables.GenericDouble1) AND CC.TempReady,
	TrueTime=900.00,
	Limit=1,
	Hysteresis=0.0,
	AllowImmediateExecution=No
	RetTimes.RetTime1	System.Retention
End Trigger
End
```

Recognition rules for this raw form:

| Source pattern | Rendered row |
|---|---|
| `Trigger 1: description` | Comment row, not a Trigger node |
| `Trigger<TAB>"NAME",` | Trigger stage row |
| `End Trigger` | `Time = End Trigger`, empty `Command` |
| `If<TAB>condition` | `Time = If`, condition remains in `Command` |
| Trigger parameter lines such as `TrueTime=900.00,` | Parameter text remains in `Command` |

## 4. Row Semantics

### 4.1 Stage Rows

Stage rows have a stage name in `Command`.

Supported stage names:

| Stage display | Meaning |
|---|---|
| `Instrument Setup` | Pre-run method setup |
| `Equilibration` | Equilibration stage |
| `Inject Preparation` | Injection preparation stage |
| `Start Run` | Start-run stage |
| `Run` | Run stage |
| `Stop Run` | Stop-run stage |

Examples:

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
{Initial Time}	Equilibration	Duration = 30.000 [min]	Hold before run starts
0.000	Run		
120.000	Stop Run		
```

Important unit rule:

| Construct | Unit meaning |
|---|---|
| stage time such as `-30.000`, `0.000`, `120.000` | minutes in the method timeline |
| `Duration = 30.000 [min]` | minutes |
| `Delay` command value | CM command value from source method; for TCC methods this is commonly seconds unless source evidence says otherwise |

Do not express a 30-minute stability hold as `Delay 30` unless the source method proves that command value is minutes. Prefer a stage timeline or trigger `TrueTime=1800` for a 30-minute condition.

### 4.2 Comment Rows

A comment row has free text in `Command` and empty `Value`.

Examples:

```tsv
Time	Command	Value	Comment
	==============================		
	External measured temperatures		
	Trigger 1: Wait until 40 C has been stable for 30 min		
```

Comments are rendered as green italic CM comment rows.

### 4.3 Command Rows

A command row has a CM command/property path in `Command`. Put the assigned value in `Value`.

Examples:

```tsv
Time	Command	Value	Comment
	ColumnComp.CC.ReadyTempDelta	0.1 [°C]	
	ColumnComp.CC.EquilibrationTime	0.5 [min]	
	ColumnComp.CC.Temperature.Nominal	Variables.GenericDouble1	Set target temperature from variable
	Delay	3	
	Wait	ColumnComp.CC.TempReady AND StabVars.TriggerStab1=0	
	RetTimes.RetTime1	System.Retention	Log report anchor
```

### 4.4 Protocol, Message, and Log

Use these correctly:

| Command | Allowed use |
|---|---|
| `Protocol` | Write a text entry to the protocol/audit-style record |
| `Message` | Show or record a message |
| `Log` | Log a variable/property, not arbitrary text |

Correct:

```tsv
Time	Command	Value	Comment
	Protocol	"Stability End"	Text note
	Log	GenericLong9	Log variable value
	Log	RetTime1	Log RetTime variable if supported by source method
```

Avoid:

```tsv
Time	Command	Value	Comment
	Log	"Stability End"	Wrong: string literal is not a variable/property log target
```

If CM shows a red cell for `Log "text"`, change it to `Protocol "text"` or `Message "text"` depending on intended behavior.

## 5. Branch Blocks

Branch rows use the `Time` column for the branch keyword and the `Value` column for the condition.

Valid branch keywords:

- `If`
- `Else If`
- `Else`
- `End If`

Example:

```tsv
Time	Command	Value	Comment
If		ColumnComp.ModelNo="VH-C10-A"	
	Variables.GenericLong9	12	Page count for VH
	Delay	1	
	Log	GenericLong9	
Else If		ColumnComp.ModelNo="VC-C10-A"	
	Variables.GenericLong9	10	Page count for VC
	Delay	1	
	Log	GenericLong9	
Else			
	Message	"Invalid ModelNo! Please reinspect in production!"	
	System.AbortQueue		
End If			
```

Do not write an empty `If` row followed by a second condition row. The condition must be on the same branch row.

## 6. Trigger Blocks

Trigger rows use a strict block. The trigger name and all trigger parameters are compiled into the Trigger row's value in CM.

Required structure:

```tsv
Time	Command	Value	Comment
Trigger		"T_TRIGGER_NAME",	
	Condition	(<condition expression>),	
	TrueTime	120	
	Limit	1	
	Hysteresis	0	
	AllowImmediateExecution	No	
	RetTimes.RetTime1	System.Retention	Command executed by trigger
End Trigger			
```

The `Comment` column on the `Trigger` row is only a human-readable description. It must not become part of the trigger name or trigger configuration.

Correct:

```tsv
Time	Command	Value	Comment
Trigger		"T_ACC_60",	External stability evaluator for 60 C accuracy
```

Incorrect:

```tsv
Time	Command	Value	Comment
Trigger		External stability evaluator for 60 C accuracy	
```

The generated CM Trigger value should appear as one expandable text block similar to:

```text
"T_TRIGGER_NAME",
(<condition expression>),
TrueTime=120,
Limit=1,
Hysteresis=0,
AllowImmediateExecution=No
```

### 6.1 Trigger Parameter Rows

Use these command names inside a Trigger block:

| Command | Value example | Notes |
|---|---|---|
| `Condition` | `(CC.Temperature.Nominal=Variables.GenericDouble1) AND CC.TempReady` | condition expression |
| `TrueTime` | `1800` | seconds for trigger condition time |
| `Limit` | `1` | trigger fire count |
| `Hysteresis` | `0` | trigger hysteresis |
| `AllowImmediateExecution` | `No` | CM trigger option |

Do not split `Condition`, `TrueTime`, `Limit`, `Hysteresis`, or `AllowImmediateExecution` into separate command rows after the trigger if the intent is to edit the trigger settings. They belong to the Trigger's expandable value.

### 6.2 Trigger Action Rows

Rows after the trigger parameters and before `End Trigger` are actions executed when the trigger fires.

Example:

```tsv
Time	Command	Value	Comment
Trigger		"T_ACC_60",	
	Condition	(CC.Temperature.Nominal=60) AND CC.TempReady AND StabVars.TriggerStab1=0,	
	TrueTime	120	
	Limit	1	
	Hysteresis	0	
	AllowImmediateExecution	No	
	RetTimes.RetTime3	System.Retention	Report anchor for 60 C accuracy
	Protocol	"Accuracy at 60 C reached"	
	StabVars.TriggerStab1	1	Close trigger gate
End Trigger			
```

### 6.3 Branch Rows Inside Trigger Blocks

Do not place free `If / Else / End If` branch blocks inside a Trigger block unless there is matching source-CMBX evidence for that exact structure.

Current high-confidence TCC source methods use `System.Trigger` with:

- one trigger configuration string, and
- a simple list of executable trigger actions.

They do not establish a general, safe pattern for nested `IfBlockNode` structures inside trigger actions. If an AI-generated method needs conditional logic inside a trigger, prefer one of these patterns:

| Preferred pattern | Use when |
|---|---|
| Separate `System.Trigger` blocks with more specific conditions | The condition can be moved into the trigger condition itself |
| Trigger action sets a state variable, followed by normal method logic outside the trigger | The branch needs ordinary CM procedural control |
| Mark `Open Verification Required` | The conditional trigger mechanism cannot be proven from CMBX evidence |

Avoid:

```tsv
Time	Command	Value	Comment
Trigger		"T_BAD_NESTED_IF",	
	Condition	StabVars.TriggerStab1=1,	
	TrueTime	30	
	Limit	0	
	Hysteresis	0	
	AllowImmediateExecution	No	
If		StabVars.CounterUpper>=4	
	StabVars.UpperReady	1	
Else			
	StabVars.UpperReady	0	
End If			
End Trigger			
```

This may import but appear red in the CM method editor.

## 7. Time Rows

A row with only `Time` creates a time step inside the current stage.

Example:

```tsv
Time	Command	Value	Comment
0.000	Run		
120.000			
	ColumnComp.CC_Temp.AcqOff		
```

Prefer explicit stage rows for major stage changes:

```tsv
Time	Command	Value	Comment
120.000	Stop Run		
```

## 8. End Row

End the method with:

```tsv
Time	Command	Value	Comment
	End		
```

The renderer may insert an End row if missing, but generated production MD should always include it explicitly.

## 9. Supported CM Command Families

The current generator is designed around known source-method prototypes. Use command families already present in the carrier/template CMBX or method KB.

Common TCC families:

| Family | Example |
|---|---|
| Column compartment properties | `ColumnComp.CC.Temperature.Nominal` |
| Acquisition on/off | `ColumnComp.CC_Temp.AcqOn`, `ColumnComp.CC_Temp.AcqOff` |
| Thermometer channels | `Thermometer1.ExtTemp_UpperCC.AcqOn` |
| RetTimes | `RetTimes.RetTime1` |
| StabVars | `StabVars.TriggerStab1` |
| TempVars | `TempVars.Ambient_Temp` |
| Variables | `Variables.GenericDouble1` |
| System | `System.Retention`, `System.AbortQueue` |
| Trigger | `Trigger` block compiled as `System.Trigger` |

If a new command family is not in KB/source evidence, mark it as `Open Verification Required` instead of inventing it.

## 10. Validation Checklist Before Generating CMBX

Before using the Method Script Generator:

| Check | Required |
|---|---|
| First fenced code block is `tsv` | yes |
| Columns are `Time`, `Command`, `Value`, `Comment` | yes |
| Columns are separated by real tab characters | yes |
| Branch condition is on the same `If` / `Else If` row | yes |
| Trigger parameters are inside the Trigger block | yes |
| `Log` does not use arbitrary string literals | yes |
| 30-minute holds are represented by stage time/duration or trigger `TrueTime=1800`, not ambiguous `Delay 30` | yes |
| Method ends with `End` | yes |
| MD filename matches desired method name | yes |

## 11. Full Mini Example

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	==============================		
	Example TCC method		
	==============================		
If		ColumnComp.ModelNo="VH-C10-A"	
	Variables.GenericDouble1	40.0 [°C]	Baseline temperature
	Variables.GenericDouble2	60.0 [°C]	Accuracy temperature
Else			
	Message	"Invalid ModelNo! Please reinspect in production!"	
	System.AbortQueue		
End If			
{Initial Time}	Equilibration	Duration = 30.000 [min]	Equilibrate at baseline before run
	ColumnComp.CC.Temperature.Nominal	Variables.GenericDouble1	
0.000	Run		
	ColumnComp.CC_Temp.AcqOn		
	Thermometer1.ExtTemp_UpperCC.AcqOn		
	Thermometer1.ExtTemp_LowerCC.AcqOn		
	ColumnComp.CC.Temperature.Nominal	Variables.GenericDouble2	
Trigger		"T_ACC_60",	
	Condition	(CC.Temperature.Nominal=Variables.GenericDouble2) AND CC.TempReady,	
	TrueTime	120	
	Limit	1	
	Hysteresis	0	
	AllowImmediateExecution	No	
	RetTimes.RetTime1	System.Retention	
	Protocol	"Accuracy at target temperature reached"	
End Trigger			
120.000	Stop Run		
	ColumnComp.CC_Temp.AcqOff		
	Thermometer1.ExtTemp_UpperCC.AcqOff		
	Thermometer1.ExtTemp_LowerCC.AcqOff		
	End		
```

## 12. Notes for AI Authors

When an AI generates this MD:

1. Generate the operation plan first.
2. Generate only this strict TSV script block for executable output.
3. Do not invent units. State unit assumptions in comments only when source evidence supports them.
4. Keep trigger settings inside the trigger value block.
5. Use existing method-script KB command families.
6. If report formulas cannot support the changed temperatures or windows, still generate the method only if requested, but label report redesign separately.
