---
name: cmbx-method-script-generator
description: Deprecated compatibility skill. Use only to recognize old CMBX Method Script Generator requests and redirect them to cm-method-script-author plus the current CM_METHOD_SCRIPT_MD_FORMAT_SPEC / MD-to-CMBX preflight workflow. Do not use the old local UI natural-language generator flow as source of truth.
---

# CMBX Method Script Generator - Deprecated Compatibility Wrapper

This skill is retained only so older prompts that mention `cmbx-method-script-generator` do not trigger stale behavior.

## Current Direction

Use `cm-method-script-author` for expert/manual method-script authoring. For generated MD intended for the app's `Method Script Generator` tab, follow:

```text
natural-language test intent
-> expert interpretation using FOQ / method-script / command / report KB
-> strict structural MD following CM_METHOD_SCRIPT_MD_FORMAT_SPEC.md
-> local preflight linter
-> standalone method CMBX packaging
-> Chromeleon import/editor validation
```

## Hard Redirect Rules

- Do not rely on the old local natural-language generator window as proof that a method script is correct.
- Do not perform string replacement on method rows.
- Do not skip role/mechanism reasoning.
- Do not emit MD that violates current preflight rules:
  - no timed prose-only comments;
  - `Run Duration` must equal explicit `Stop Run` time;
  - trigger parameters must stay inside trigger blocks;
  - trigger `Limit` must be numeric or blank;
  - no unsupported branch rows inside trigger blocks.

## Evidence To Use

- `C:\Users\xiaoshu.guan\.codex\skills\cm-method-script-author\SKILL.md`
- `C:\Users\xiaoshu.guan\.codex\skills\cm-method-script-author\references\tcc_method_authoring.md`
- `C:\ProgramData\CMBX Data Explorer Workspace\KB\Method Script Generator\Generator Spec\CM_METHOD_SCRIPT_MD_FORMAT_SPEC.md`
- `C:\ProgramData\CMBX Data Explorer Workspace\KB\FOQ Template\MD_TO_STANDALONE_METHOD_CMBX_PACKAGING.md`

## Output

If invoked, say that this compatibility skill redirects to `cm-method-script-author`, then use the current authoring/preflight workflow.