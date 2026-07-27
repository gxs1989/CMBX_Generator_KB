# CM Compiler Rules

KB_Version: 1.0  
Status: Supplementary notes for Method Script Generator.

## Rule Priority

Use these documents in this order:

1. `CM_METHOD_SCRIPT_MD_FORMAT_SPEC.md` is the single strict SPEC for AI authoring and app compilation.
2. This file only records compiler-facing reminders and migration notes.

If this file conflicts with the strict format spec, the strict format spec wins.

## Compiler-Facing Rules

| Topic | Rule |
|---|---|
| Columns | Executable MD uses four tab-separated columns: `Time`, `Command`, `Value`, `Comment`. |
| Branch | `If`, `Else If`, `Else`, `End If` belong in `Time`; condition belongs on the same branch row. |
| Trigger | Trigger name and parameters are compiled into one CM trigger value block. |
| Trigger parameters | Use `Condition`, `TrueTime`, `Limit`, `Hysteresis`, `AllowImmediateExecution` inside the Trigger block. |
| Comments | Comment rows have text in `Command` and empty `Value`; they are not executable. |
| End | Generated production MD should include an explicit `End` row. |
| Units | Stage `Duration` is minutes; trigger `TrueTime` is seconds; command `Delay` is source-method-specific and must not be used for long holds without evidence. |

## Known Red-Cell Patterns

| Pattern | Safer alternative |
|---|---|
| Empty `If` row followed by condition as a normal row | Put condition on the same `If` row. |
| `Log "some text"` | Use `Protocol "some text"` or `Message "some text"`. |
| Trigger type words such as `External`, `Second`, `Reset` emitted as ordinary rows | Encode trigger name/condition/parameters in the strict Trigger block. |
| Free nested `If` inside a Trigger block | Use separate trigger conditions or move branch logic outside the trigger unless source evidence proves the structure. |
