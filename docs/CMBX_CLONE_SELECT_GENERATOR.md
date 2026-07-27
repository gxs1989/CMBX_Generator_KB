# CMBX Clone-and-Select Generator

This document describes the first practical CMBX generation prototype.

## Purpose

The clone-and-select generator creates a candidate CMBX from a known-good golden CMBX and a semantic `CloneSelectPlan`.

It is the first bridge between:

```text
semantic test catalog
-> SequenceBlueprint
-> execution or analysis package compatibility validation
-> generated candidate CMBX
```

## Current Implementation

Code:

```text
cmbx_data_explorer/clone_select_generator.py
```

Main function:

```text
write_clone_select_cmbx(package, plan, output_path, sequence_name=None)
```

Current behavior:

1. Read the golden CMBX `header.xml`.
2. Find the source sequence that contains the selected injections.
3. Create a filtered sequence header.
4. Keep selected:
   - injections
   - instrument methods
   - processing methods needed for IRC/execution
   - optionally report template for analysis/DB candidates
5. Preserve selected injection raw/audit entries.
6. Preserve the original sequence `.cmd` payload.
7. Write a new candidate CMBX.

## Why It Preserves the Sequence Command Payload

The sequence `.cmd` payload contains Chromeleon-specific binary structure:

```text
injection-to-method links
embedded instrument methods
embedded processing methods
embedded report payloads
sequence command metadata
```

The current generator does not yet rewrite that binary payload. It filters the visible header structure while preserving the underlying command payload from the known-good package.

This makes the candidate useful for CMBX Data Explorer validation and for incremental reverse engineering, but not yet a guaranteed runnable Chromeleon package.

## Validated Example

Source:

```text
C:\ProgramData\CMBX Data Explorer Workspace\packages\TCC Cost Out\Zollner\Production\0000003.cmbx
```

Requirement:

```text
VA-C10-A upper_lower_valve_cycle
```

Output:

```text
cmbx_data_explorer/outputs/generated_candidates/VA-C10-A_0000003_candidate.cmbx
```

Generated structure:

```text
sequences: 1
injections: 1
channels: 1
audits: 1
instrument_methods: 1
processing_methods: 1
report_templates: 1
```

Clone-select plan:

```text
source package: 0000003.cmbx
device model: VA-C10-A
report template: Report_VATCC_V1_01
injections: Valve
instrument methods: VALVES
processing methods: No_Integration
required capability groups: core_tcc, upper_lower_valves
```

Candidate validation:

```text
Header Passed: True
Command Payload Passed: False
```

The header is clean, but the preserved sequence `.cmd` payload still contains readable references to unselected injections, methods, and processing methods, including:

```text
VTCC_BurnIn
Temperature Calibration
Temperature Accuracy_C
Temperature Precision
Temperature Stability_C
HeatUp and CoolDownTime
LiquidLeaktest
Qualification_Service_Done
Factory Default
Error Log Check
BURNIN
CHECKERRORLOG
ColumnID
LIQUID LEAK
PREHEATER
TEMPERATURE_ACCURACY
TEMPERATURE_STABILITY_70_C
TEMPERATURE_STABILITY_AND_PCC_70_H
TEMP_HEAT_UP_DOWN_20_50_20
ACCURACY_IRC_STOP_C
ACCURACY_IRC_STOP_H
CORRECT_ACCURACY_INJ_INSERTION
CORRECT_STABILITY_INJ_INSERTION
```

This confirms the current generator is structurally useful but does not yet produce a clean sequence command payload.

## Validation Before Writing

The generator should only run after:

```text
build_sequence_blueprint(...)
validate_blueprint_capabilities(...)
build_execution_sequence_plan(...)
validate_execution_plan_against_package(...) for runnable-only candidates
validate_blueprint_against_package(...) for analysis/DB candidates
build_clone_select_plan(...)
```

The package compatibility gate checks:

```text
expected injection exists
expected instrument method exists
expected processing method exists
expected report template exists
existing injection-to-method link matches the semantic blueprint
```

For an execution-only generator, the report-template check is intentionally skipped. The core runnable gate is:

```text
expected injection exists
expected instrument method exists
expected IRC processing method exists when needed
existing injection-to-method link matches the semantic blueprint
```

## Boundary

This is a Level 1 generator:

```text
clone known-good CMBX
select known-good package parts
preserve Chromeleon binary payloads
```

It does not yet:

```text
rewrite sequence .cmd records
write new instrument method binary payloads
write new processing method binary payloads
write FormulaOne workbook/report payloads
prove Chromeleon can run the generated package
```

## Next Step

Add a validation command/report that loads the generated candidate and compares:

```text
generated header structure
expected CloneSelectPlan
decoded method links
available report template
available raw/audit sources
```

After that, the next technical risk is sequence `.cmd` editing:

```text
remove unselected injection command records
or generate a new sequence command object from blueprint
```

The next reverse-engineering task is to identify stable `.cmd` record boundaries for:

```text
injection rows
instrument method embedded payloads
processing method embedded payloads
report template embedded payloads
RelativeUrl link blocks
```

Current `.cmd` probe notes are tracked in:

```text
cmbx_data_explorer/docs/SEQUENCE_CMD_REVERSE_ENGINEERING.md
```
