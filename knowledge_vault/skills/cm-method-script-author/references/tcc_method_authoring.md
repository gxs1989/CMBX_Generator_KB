# TCC Method Authoring Reference

Use this reference when authoring TCC FOQ Chromeleon method scripts manually from user intent.

## Evidence Sources

Prefer these sources in order:

| Evidence | Path / Source | Use |
|---|---|---|
| Full method scripts | `C:\ProgramData\CMBX Data Explorer Workspace\KB\CMBX Method Scripts\TCC\knowledge_base\tcc_reverse_probe\{VA,VC,VH}\*\*_embedded_method_flow.tsv` | Source of executable CM command patterns and roles |
| Stress / trigger methods | `C:\ProgramData\CMBX Data Explorer Workspace\KB\CMBX Method Scripts\TCC\cmbx_data_explorer\outputs\stress_probe\Stress_VH_DVT013_20260529\*_embedded_method_flow.tsv` | Valve switching and trigger command evidence |
| Script descriptions | `C:\ProgramData\CMBX Data Explorer Workspace\KB\FOQ\TCC\Script Description\*.md` | Human-readable method mechanism analysis; use this between raw TSV rows and authoring decisions, especially for trigger/state-machine explanations |
| TCC TD / FOQ KB | `C:\ProgramData\CMBX Data Explorer Workspace\KB` and workspace `cmbx_data_explorer\docs\TCC_*` | Test purpose, order, dependencies, acceptance criteria |
| Command KB | workspace `cmbx_data_explorer\docs\CM_METHOD_COMMAND_KNOWLEDGE_BASE.md` and `cmbx_data_explorer\docs\CM_METHOD_RENDERING_CONTRACT.md` | CM table rendering and command semantics |
| Report/formula KB | workspace `cmbx_data_explorer\CM_FORMULA_REVERSE_ENGINEERING.md`, report/formula docs, DB mapping | Report feasibility and DB/output constraints |
| Role contracts | workspace `cmbx_data_explorer\docs\TCC_*BLACK_BOX*`, `TCC_METHOD_REPORT_ALIGNMENT.md`, `TCC_TEST_KNOWLEDGE_NODE_MODEL.md` when present | Meaning of method blocks and locked roles |
| Method Script Generator SPEC | `C:\ProgramData\CMBX Data Explorer Workspace\KB\Method Script Generator\Generator Spec\CM_METHOD_SCRIPT_MD_FORMAT_SPEC.md`, workspace `cmbx_data_explorer\docs\CM_METHOD_SCRIPT_MD_FORMAT_SPEC.md` | Strict MD authoring/preflight rules for MD-to-CMBX output |
| MD packaging KB | `C:\ProgramData\CMBX Data Explorer Workspace\KB\FOQ Template\MD_TO_STANDALONE_METHOD_CMBX_PACKAGING.md`, workspace `cmbx_data_explorer\docs\MD_TO_STANDALONE_METHOD_CMBX_PACKAGING.md` | Roundtrip acceptance and packaging constraints |

If the exact evidence file is missing, search by method name with `rg --files` and inspect nearby KB files.

## CM Table Rendering Contract

Use columns:

```text
# | Kind | Time | Command | Value | Comment
```

Rules:

- `Stage`: Time is stage start time; Command is stage name; Value may contain `Duration = ... [min]`.
- `Comment`: green CM comments remain `Kind=Comment`; do not execute or edit as commands.
- `Branch`: Time contains `If`, `Else If`, `Else`, or `End If`; Value contains the condition.
- `Command`: Command contains CM symbol/command; Value contains expression/value; Comment carries validation notes.
- `End`: terminate with `End` when source script does.
- Numeric `Time` rows must be stages or executable CM command/property rows. Do not write timed prose-only comments such as `5.000<TAB>Static measurement starts`; attach that explanation to the `Comment` column of a real command at that time.
- `Run` stage `Duration = X [min]` must match the explicit `Stop Run` stage time. No Run-stage row may have a time later than `Stop Run`.

## TCC Intent Routing Heuristics

| Natural-language clue | Primary method family | Notes |
|---|---|---|
| accuracy, accurate, å‡†ç¡®æ€§, å‡†ç¡®åº¦ | `TEMPERATURE_ACCURACY` | Uses temperature ladder variables and RetTime/report anchors. New target temperatures may require report redesign. |
| stability, ç¨³å®šæ€§ | `TEMPERATURE_STABILITY_70_C` or `TEMPERATURE_STABILITY_AND_PCC_70_H` | Stability windows are report-sensitive. Distinguish baseline/precondition from measurement window. |
| precision, ç²¾å¯†åº¦, repeatability | `TEMPERATURE_PRECISION` / `TEMPERATURE_PRECISION_AND_FAN` | Precision is repeatability, not simply stability. |
| heatup, cooldown, å‡æ¸©, é™æ¸©, çˆ¬å¡ | `TEMP_HEAT_UP_DOWN_20_50_20` | Time/duration report rules may assume specific RetTimes. |
| valve, é˜€, switch every, trigger, å‘¨æœŸåˆ‡æ¢ | `VALVES` plus stress-test method scripts | Requires trigger/valve evidence, not just temperature command edits. |
| combine, merge, å åŠ , åˆå¹¶, after X do Y, ä¹‹åŽ | Composite method | Route sub-intents first; define transition, shared setup, RetTime separation, and report limitations. |

## Role Identification Before Editing

Before editing a method script, classify relevant rows into roles:

| Role | Typical evidence | Editable? |
|---|---|---|
| device branch | `ColumnComp.ModelNo=...` | Locked unless target model changes |
| page/report count | `Variables.GenericLong9` etc. | Usually locked; report layout dependency |
| test setpoint variable | `Variables.GenericDoubleN` assigned temperatures | Editable after mapping to specific temperature-point role |
| baseline/precondition setpoint | initial `Temperature.Nominal`, equilibrium steps | Editable only if intent explicitly changes baseline |
| measurement setpoint | setpoint immediately tied to Wait/RetTime/report anchor | Editable for test target |
| ready/wait gate | `Wait ColumnComp.CC.TempReady...` | Usually locked, but duration may require review |
| RetTime anchor | `RetTimes.RetTimeN = System.Retention` | Locked unless report formula is redesigned |
| trigger gate | `StabVars.Trigger...`, `System.Trigger...` | Locked unless trigger mechanism is the intent |
| final reset / cleanup | acquisition off, temp reset, leak sensor reset | Usually locked |
| valve/trigger block | stress-test evidence | Editable only from trigger KB evidence |

Never replace all rows with the same command name. Edit only rows whose role matches the intent.

## Common TCC Composition Patterns

### Single target accuracy after baseline

User example: `æ¸©åº¦å‡†ç¡®æ€§æµ‹è¯•ï¼Œä»Ž40åº¦å¼€å§‹ï¼Œç¨³å®š30åˆ†é’ŸåŽä¸Šå‡åˆ°60åº¦ï¼Œåœ¨60åº¦æµ‹è¯•å‡†ç¡®æ€§`.

Interpretation:

- Primary test: Temperature Accuracy.
- Baseline/precondition: hold 40 C for 30 min before measurement transition.
- Measurement target: 60 C accuracy point.
- Method may be drafted from `TEMPERATURE_ACCURACY` by selecting/reassigning ladder roles, but existing report DB fields may not include 60 C for VH mapping; report redesign may be required.
- Required output must separate: method script draft vs report blocked.

### Stability then accuracy

User example: `30åº¦ç¨³å®šæ€§10åˆ†é’ŸåŽåˆ°40åº¦æµ‹å‡†ç¡®æ€§`.

Interpretation:

- Composite intent: Stability pre-block at 30 C for 10 min, then Accuracy measurement at 40 C.
- Do not route only to Accuracy or only to Stability.
- Existing stability report windows may not support 10 min; method can log data, report requires new calculation window.

### Accuracy plus simultaneous stability

User example: `æ¸©åº¦å‡†ç¡®æ€§æµ‹è¯•ï¼Œä»Ž40åº¦å¼€å§‹ï¼Œç¨³å®š30åˆ†é’ŸåŽä¸Šå‡åˆ°60åº¦ï¼Œåœ¨60åº¦æµ‹è¯•å‡†ç¡®æ€§ï¼Œç„¶åŽå†æµ‹80åº¦å‡†ç¡®æ€§ï¼Œåœ¨80åº¦åŒæ—¶æµ‹ç¨³å®šæ€§`.

Interpretation:

- Composite intent: Accuracy baseline at 40 C, accuracy at 60 C, accuracy at 80 C, plus stability acquisition during the 80 C hold.
- Do not route this as a simple standard accuracy ladder.
- 60 C may be outside the existing VH DB/report contract; 80 C may be mapped but RetTime remapping still needs report review.
- Stability at 80 C requires either a stability report window anchored to the 80 C block or a new report formula. Existing TCC stability reports may be fixed to standard windows/points.

### Precision plus stability

User example: `æµ‹è¯•TCCçš„ç²¾å¯†åº¦ï¼Œä½†æ˜¯åœ¨æµ‹è¯•ä¹‹åŽè¿˜è¦å åŠ åœ¨50Cçš„ç¨³å®šæ€§`.

Interpretation:

- Composite intent: Precision method followed by stability block at 50 C.
- Need preserve precision RetTimes/report anchors and create a separate stability RetTime/channel/report plan.
- If report cannot merge both outputs, provide method script and report redesign checklist.

### Valve stress plus stability

User example: `70Cç¨³å®šæ€§ï¼Œå‰10åˆ†é’Ÿä¸è½¬é˜€ï¼Œä¹‹åŽ10åˆ†é’Ÿä¸Šä¸‹é˜€æ¯5ç§’åˆ‡æ¢ï¼Œå†10åˆ†é’Ÿåœæ­¢ï¼Œå†10åˆ†é’Ÿæ¯3ç§’åˆ‡æ¢ï¼Œlogé˜€ä½ç½®`.

Interpretation:

- Composite intent: Temperature stability + valve stress trigger module.
- Must inspect stress-test method scripts for trigger commands and valve-position logging.
- Do not invent periodic switching syntax without evidence.
- If trigger command evidence exists, compose blocks: equilibrate 70 C -> acquisition/logging -> no-switch segment -> trigger 5 s segment -> no-switch segment -> trigger 3 s segment -> cleanup.

## TCC Accuracy Authoring Guardrails

These rules are mandatory when authoring or modifying `TEMPERATURE_ACCURACY`.

### Long holds are not ordinary Delay rows

A pre-run hold such as 30 minutes must normally be represented by the CM stage time/duration pattern, for example `Equilibration` at `Time=-30.000` with `Duration = 30.000 [min]`. Do not add `Delay 30 [min]` unless a real source method proves that exact syntax. In decoded TCC methods, numeric `Delay` rows such as `1`, `2`, `3`, `5`, or `60` are local waits/transition waits; do not infer that they are minutes.

### An Accuracy point is a stability-gated macro

Do not collapse Temperature Accuracy to `set target -> wait -> RetTime`. A valid Accuracy point requires the external-temperature stability machinery from the stock method:

1. Reset `StabVars.TriggerStab1/2`, upper/lower ranges, counters, and ready flags.
2. Define/run `System.Trigger` blocks `Gradient_1`, `Gradient_2`, `ExitRange_Upper`, `ExitRange_Lower`, and the abort safety trigger.
3. Track `Thermometer1.ExtTemp_UpperCC` and `Thermometer1.ExtTemp_LowerCC` within the local +/-0.05 C band.
4. Set `StabVars.UpperReady` and `StabVars.LowerReady` only after the counter criteria are satisfied.
5. Only then wait on `ColumnComp.CC.TempReady AND StabVars.LowerReady AND StabVars.UpperReady, Run=Continue` and write `RetTimes.RetTimeN = System.Retention`.

If a generated script does not inline or explicitly inherit this trigger/counter macro, mark the Accuracy point as incomplete.

## Compiler Preflight Rules

When producing MD intended for `Method Script Generator`, the authored table must pass the same structural preflight used by the app and CMBX compiler:

- Numeric `Time` rows must be Stage, Trigger, or executable command/property rows. Do not create timed prose-only comments.
- `Run` stage `Duration = X [min]` must equal explicit `Stop Run` time `X`.
- No Run-stage row may occur later than `Stop Run`.
- Trigger parameters (`Condition`, `TrueTime`, `Delay`, `Limit`, `Hysteresis`, `AllowImmediateExecution`) must stay inside `Trigger` / `End Trigger`.
- Trigger `Limit` must be numeric or blank, not `Infinite`, `inf`, or `unlimited`.
- Free `If` / `Else` branch rows inside Trigger blocks are blocked unless source CMBX evidence proves the exact nested trigger-action shape.

If an AI-authored script violates these rules, fix the MD structure before discussing CMBX packaging.
## Report Constraint Rules

- Accuracy DB/report mappings may be fixed to known points such as 20/40/80/120 or 10/20/40/60/85 depending on device/template. If target point is absent, report redesign is required.
- Stability/precision reports may use fixed windows and specific RetTimes. If duration changes, report formulas must be checked before claiming a final DB output.
- Method script can be useful even when report is blocked, but say so explicitly.
- External vs internal sensor choice changes both channel acquisition and report formulas.

## Validation Checklist

Before finalizing, answer yes/no:

1. Did I identify every sub-intent?
2. Did I load the source method script(s) for each sub-intent?
3. Did I classify the edited rows by role before changing them?
4. Does the method actually execute the requested baseline, transition, measurement duration, triggers, and cleanup?
5. Are RetTime anchors still compatible with the report, or is report redesign required?
6. Are required devices/channels/variables listed?
7. Are all invented or uncertain commands marked as Open Verification Required?

## How to Update This Reference

When a generated script is wrong, add a minimal failure rule here:

- failing user intent
- wrong interpretation or wrong edited role
- correct CM mechanism
- evidence file proving the mechanism
- new guardrail



