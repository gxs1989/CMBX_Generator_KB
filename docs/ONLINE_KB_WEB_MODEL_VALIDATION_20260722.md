# Online Method KB Web-Model Validation

Validation_Date: 2026-07-22  
Profile: Small context, three files below 200 KB each  
Intent: Hold CC at 20 C for one hour; after minute 1 switch upper/lower valves every 6 seconds for 30 minutes

## Result

The small-context evidence profile remains usable. Doubao expert mode routed
the intent to the correct temperature and periodic-Trigger mechanisms and
produced a mostly correct script. Its defect was local and diagnosable: bare
`1.000` and `31.000` rows were emitted without a stage or executable command,
so they were classified as comments.

| Model | Structural result | Semantic result | Main finding |
|---|---|---|---|
| Doubao expert | Mostly valid | Mostly correct | Bare numeric time rows are not executable anchors |
| GPT-5.5 Instant | Invalid TSV serialization | Strong mechanism reasoning | Space-aligned text was used instead of real tabs |
| GPT-5.6 Medium | Valid | Correct for the requested same-position synchronous switching interpretation | Best directly usable output in this trial |
| DeepSeek | Structurally readable | Incorrect timeline | Interpreted switching as starting after the one-hour hold |

## Maintenance Implication

1. Keep the small-context package as a first-class delivery profile.
2. Keep a complete SPEC in that profile; compact ORIGINAL and SUMMARY only.
3. Explicitly prohibit a numeric `Time` value without a stage/Trigger/command
   on the same TSV row.
4. Local preview and preflight remain mandatory. A model producing no red rows
   is not sufficient evidence that test semantics are correct.

## Validation Addendum: 2026-07-24 TCC Valve Report

Intent: generate a paired VH-C10-A valve method/report for synchronous
`6_1 -> 1_2 -> 6_1` switching and display only switch time plus upper/lower
valve position.

### Result

- The Method MD passed local preflight and correctly switched and logged both
  `CurrentPosition` properties.
- The Report MD passed structural preflight and created a native Audit Trail
  table that populated successfully against a real injection in Chromeleon.
- The business result was not acceptable: the table displayed the complete
  run audit stream, not only valve-position records.

### Root Cause

Chromeleon's Instrument Audit Trail table supports audit-level,
run/precondition, Day Time and Device options. It does not expose a row filter
for command text, device name, property path or regular expressions. The web
model selected a valid native object but overstated its filtering behavior.

### Maintenance Implication

1. Do not describe `audittrail` as an exact event-only business table.
2. For a finite known switch schedule, generate normal report rows using the
   method's known times/RetTime anchors and timed
   `AUDIT.UpperValve.CurrentPosition(...)` /
   `AUDIT.LowerValve.CurrentPosition(...)` formulas.
3. For a runtime-variable number of valve-only rows, require an additional
   verified dynamic row source (for example integrated virtual-channel peaks
   plus a Processing Method) or external filtering.
4. This finding is incorporated into Report SPEC V1.4.

## Validation Addendum: 2026-07-24 Valve Integration Compiler

The native Integration-table compiler path is now enabled and structurally
verified. The evidence-backed valve chain is:

```text
PumpModule.Pump.Pump_Pressure.Signal
-> VirtualChannel PumpPressureVirtual
-> Processing Method PressureSpikeEval
-> IntegrationReportTable
-> switch time + upper/lower valve position
```

Validation artifacts:

- `outputs/valve_integration_research/VALVE_SWITCH_INTEGRATION_REPORT.md`
- `outputs/valve_integration_research/VALVE_SWITCH_INTEGRATION_REPORT.cmbx`

The generated CMBX reopens in the local decoder as an `integration` table with
three formula columns and fixed channel `PumpPressureVirtual`. CM runtime row
population remains the final validation step because it depends on the selected
injection actually using `PressureSpikeEval` and containing integrated pressure
spikes. This compiler contract is incorporated into Report SPEC V1.5.
