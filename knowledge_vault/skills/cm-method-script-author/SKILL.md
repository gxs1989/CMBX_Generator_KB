---
name: cm-method-script-author
description: Author Chromeleon/CMBX instrument method scripts from natural-language FOQ test intent using local KB evidence and manual expert reasoning. Use when the user asks to generate, modify, cut, merge, or explain TCC/VDAD/FOQ method scripts; when programmatic Method Script Generator output is not trusted; when a request includes phrases such as "stability at 80C", "accuracy from 40 to 60", "merge precision and stability", "valve switching", "trigger", "method script", "report constraint", or "configuration checklist".
---

# CM Method Script Author

## Mission

Turn a natural-language FOQ/test intent into an evidence-grounded Chromeleon method-script design. Prefer expert reasoning from KB/CMBX evidence over programmatic string replacement. Output the complete method script or a precise script patch only when the CM execution mechanism is understood.

## Required First Step

For TCC tasks, read `references/tcc_method_authoring.md` before producing a script. If the output is intended for Method Script Generator / MD-to-CMBX packaging, also follow the current `CM_METHOD_SCRIPT_MD_FORMAT_SPEC.md` and compiler preflight rules referenced there. If the request is for another family, inspect the matching FOQ KB, method-script KB, and report/formula KB first; if those evidence sources do not exist, say what is missing.

## Core Workflow

1. **Restate the intent as an operation contract.** Identify primary test intent, related tests, baseline/preconditioning, target setpoints, duration/window, sensors/channels, triggers, valves, RetTime anchors, report expectations, and device model.
2. **Route to evidence.** Load only the relevant KB/CMBX method scripts, TD interpretation, command KB, method role contracts, and report/formula constraints. Do not rely on memory alone.
3. **Explain CM mechanism before editing.** Describe which method blocks implement setup, variables, ladder/setpoints, waiting, trigger gates, RetTime logging, acquisition, cleanup, and report anchors.
4. **Decide whether the intent is script-only or report-impacting.** If report formulas/DB fields cannot support the changed output, still generate a method draft only when useful, but label report redesign as blocked.
5. **Generate the script using CM table semantics.** Preserve row categories: Stage, Comment, Branch, Command, End. Branch keywords belong in Time; conditions belong in Value. Comments stay comments. For MD-to-CMBX use, emit strict structural MD that would pass local preflight: no timed prose-only comments, no Run/Stop mismatch, no trigger parameters outside Trigger blocks.
6. **Validate locally by reasoning.** Check that the generated script actually performs the user intent, not merely changes matching words. Verify baseline, target, duration, sensor scope, triggers, RetTimes, final reset, and report windows.
7. **Expose uncertainty.** Every unknown must be marked `Open Verification Required` with the exact evidence needed.

## Output Contract

For each response, provide:

1. **Intent interpretation**: what the request means operationally.
2. **Evidence used**: KB files / method scripts / report constraints consulted.
3. **Configuration checklist**: required CM device config, external devices, variables, channels, trigger dependencies.
4. **CM mechanism plan**: ordered blocks and why they exist.
5. **Method script**: full table or precise patch in columns `# | Kind | Time | Command | Value | Comment`.
6. **Report constraints**: what the existing report can/cannot calculate after this change.
7. **Open verification**: unresolved facts and how to close them.

## Hard Rules

- Do not claim a script is runnable unless method commands, config dependencies, and report implications are verified.
- Do not use global string replacement as an editing strategy.
- Do not treat all `Temperature.Nominal` commands as the same role; identify each command's role first.
- Do not invent CM commands when a required command family is absent from KB evidence. For trigger/valve work, use stress-test evidence when available, otherwise mark missing evidence.
- If the task is a composite intent, route each sub-intent separately and then design the merge points.
- If the existing report contract is incompatible with a new temperature or duration, separate `method script can be drafted` from `report output is blocked`.

## Failure Update Rule

When the user says the output is wrong, identify whether the failure is in intent interpretation, evidence routing, CM mechanism understanding, script rendering, or report constraint reasoning. Update the skill reference guidance accordingly before retrying.

