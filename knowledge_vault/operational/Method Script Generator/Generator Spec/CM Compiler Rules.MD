# CM Compiler Rules

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
