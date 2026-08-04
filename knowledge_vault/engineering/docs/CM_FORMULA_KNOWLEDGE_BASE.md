# CM Formula Knowledge Base

This is the in-app reference for Chromeleon formula behavior used by CMBX Data Explorer.

## Source Status

Current verified sources:

- CMBX report template XML and FormulaOne workbook payloads.
- CM-exported `.xls` reports used as comparison references.
- Method/report formulas observed in FOQ validation packages.

Local help search status:

- The local Chromeleon installation contains driver `.chm` help files and troubleshooting HTML.
- Readable local HTML did not contain `sig_value`, `signalStatistic`, `AUDIT`, or report formula references.
- Official formula-help excerpts should be added here later when an accessible CM help export is available.

This file therefore separates verified reverse-engineered behavior from future official-help additions.

## Formula Layers

Chromeleon report output is reconstructed from three layers:

1. Instrument method logic creates the test flow and writes audit values such as `RetTimes.RetTime1`.
2. Report sheet objects evaluate formulas against an injection context.
3. FormulaOne workbook cells apply report-layout formulas, criteria comparisons, number formats, and final pass/fail text.

## Raw Signal Formulas

Observed raw-signal formulas use a fixed channel from the report formula object.

Common patterns:

```text
chm.sig_value("average", start, end)
chm.sig_value("min", start, end)
chm.sig_value("max", start, end)
chm.sig_value("drift", start, end)
chm.signalStatistic("average", start, end)
chm.signalStatistic("min", start, end)
chm.signalStatistic("max", start, end)
chm.signalValue(time)
chm.noise(start, end)
chm.drift(start, end)
```

Current verified behavior:

- Time is in minutes.
- `start` and `end` often use `AUDIT.RetTimeN(...)` arithmetic.
- `average`, `min`, and `max` are evaluated over raw points inside the requested time window.
- `chm.drift(start, end)` is modeled as a linear regression slope in signal units per minute.
- `chm.noise(start, end)` is best matched as peak-to-peak residual after removing a linear trend.
- `chm.sig_value("drift", ...)` appears to follow a coarser CM signal-statistic behavior than direct `chm.drift`.

## Audit Formulas

Audit formulas read event, RetTime, and precondition-like values from the injection audit trail.

Common patterns:

```text
AUDIT.RetTime1(1,"forward")
AUDIT.ColumnComp.CC.Temperature.Nominal(time)
AUDIT.ColumnComp.CC.Temperature.Nominal(time,"backward")
AUDIT.Column_A.Description(0,"forward")
AUDIT.ColumnComp.ModelNo
```

Current verified behavior:

- `AUDIT.RetTimeN(1,"forward")` resolves RetTime values written by the instrument method.
- Timed audit property lookup supports forward/backward direction.
- Some templates omit the leading device path. The evaluator supports suffix path matching.

## Precondition Formulas

Precondition formulas read device state near the start of an injection audit.

Examples:

```text
precond.ColumnComp.SerialNo
precond.ColumnComp.FirmwareVersion
precond.ColumnComp.HardwareVersion
precond.ColumnComp.ModuleHardwareRevision
precond.ColumnComp.PrehtLeft.ModulePresent
precond.ColumnComp.PrehtLeft.MemoryState
```

These values are used for identity, firmware/hardware checks, preheater presence, and memory state.

## Sequence and Sample Metadata

Implemented metadata formulas:

```text
seq.name
seq.update_time
seq.timebase
injection.name
smp.name
```

Observed but not complete:

```text
seq.creation_time
seq.submitTime
seq.submitOperator
seq.dataVault
seq.signStatus
gen.loggedOnUser.userName
```

## FormulaOne Workbook Formulas

Report templates contain a FormulaOne workbook layer. This layer is important because DB mapping often points to final visible report cells, not raw formula cells.

Currently reconstructed by known rule maps:

- Temperature Accuracy summary and pass/fail.
- Temperature Precision summary and pass/fail.
- Temperature Stability summary and pass/fail.
- HeatUp/CoolDown summary and pass/fail.
- PCC CoolDown.
- Preheater port and heater-temperature difference checks.
- Column ID checks.
- Factory default metadata checks.

Future work should parse workbook formulas directly where possible.

## Method Generation Interface

Formula knowledge is now opened through the unified `KB Index` tab rather than
a standalone Formula KB button. Method/report generation work should reference
this file through KB Index classification and the Skills tab.

Companion method-command notes are maintained in:

```text
docs/CM_METHOD_COMMAND_KNOWLEDGE_BASE.md
```

Planned reverse-generation path:

1. Start from DB mapping fields and final report cells.
2. Trace final cells back to workbook formulas, report formula objects, Definitions criteria, and raw/audit sources.
3. Derive required instrument method outputs:
   - RetTimes that must be logged.
   - Channels that must be collected.
   - Stability windows and trigger conditions that must exist.
   - Device properties and preconditions that must be available.
4. Generate or validate a method flow against the report dependencies.

## V1.2 Formula Research Plan

The next step is comprehensive CM formula understanding. The work should proceed as an evidence table rather than isolated fixes:

1. Inventory every unique formula string from all loaded report templates.
2. Classify each formula by namespace:
   - `chm.*`
   - `AUDIT.*`
   - `precond.*`
   - `seq.*`, `smp.*`, `injection.*`, `gen.*`
   - FormulaOne workbook formulas
3. For each unique formula, store:
   - report template name
   - sheet/cell
   - fixed channel
   - injection/report applicability rule
   - observed CM exported value when available
   - evaluator output
   - mismatch class
4. Expand FormulaOne workbook extraction so final DB cells can be traced through real workbook formulas, not only known FOQ rules.
5. Build official-help references when accessible and keep them separate from reverse-engineered observations.
6. Add a small formula conformance test for every newly implemented formula family.

The target is a formula registry that can answer:

```text
Which report formulas exist?
Which are implemented?
Which are approximated?
Which need official CM behavior or more validation data?
```

## Current Boundary

The knowledge base is descriptive. It does not change calculation behavior by itself.

Implemented formula execution remains in:

```text
report_formula_evaluator.py
report_calculation_map.py
foq_contract_report.py
formulaone_report_exporter.py
```
