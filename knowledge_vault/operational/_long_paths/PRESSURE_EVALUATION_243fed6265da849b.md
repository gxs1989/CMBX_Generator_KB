# PressureEvaluation Direct CM Formula Inventory

- **Source CMBX:** `PressureEvaluation.cmbx`
- **Extraction scope:** `SheetObject` direct CM formulas only.
- **Not included:** FormulaOne workbook formulas/layout stored in `SpreadSheetData`.
- **Authoring rule:** Retain the sheet/cell binding and fixed channel/component unless a configuration contract approves a change.

## Summary

- Sheets: 1
- Direct CM formula objects: 1
- Formula namespaces: `peak` (1)

## Web Authoring Context (Self-Contained)

This section is included so this inventory can be supplied directly to a web-based GPT. It does not require access to local Chromeleon Help files. The formula table below is the carrier-specific evidence; this section explains how to read and safely reuse that evidence.

### Two Calculation Layers

| Layer | Storage / syntax | Use it for | V0.1 standalone-CMBX rule |
|---|---|---|---|
| Direct CM report formula | `ReportFormulaObject` with CM expressions such as `chm.noise(...)`, `AUDIT.*`, `precond.*` | Pulling raw signal, audit, metadata, or peak data into an existing report cell | May replace an existing formula object only when sheet, cell/range and object type match the carrier |
| FormulaOne workbook formula | Embedded `SpreadSheetData`, Excel-like syntax such as `=MAX(...)` | Visible labels, layout, calculated summaries, pass/fail display and print structure | Preserve it. Record requested edits as `workbook_change_request`; do not write them as CM formulas |

Do not put an Excel formula beginning with `=` into a `ReportFormulaObject`. Do not assume every visible result cell appears in this inventory: workbook-derived cells are intentionally outside this direct-CM extraction scope.

### HPLC Report Signal Context

The channel names and audit paths observed in the table are carrier-specific configuration contracts, not generic aliases. Use the exact evidence rows below to decide which of these source categories apply:

| Observed item | Meaning for authoring | Required evidence before reuse |
|---|---|---|
| Raw channel, for example `UV_VIS_1` or `PumpPressureVirtual` | Detector, pump, virtual, or other acquired-signal context used by raw-statistic and peak formulas | The method/config must acquire or create that exact channel with compatible settings |
| Timed audit path, for example `AUDIT.UV.*` or `audit.ColumnComp.*` | Time-resolved settings/events, such as detector state, valve position, flow, or temperature | The selected injection audit must log the exact property path |
| Precondition path, for example `precond.UV.*` | Pre-run device identity/configuration | The device configuration must expose and log the property |
| `peak.*` / `chm.peak(...)` | Processed chromatographic peak/calibration result | A compatible processing method, channel and component must exist |

Time arguments in observed `chm.*` and timed `AUDIT.*` expressions are in minutes. Preserve all observed scale factors: for example `chm.noise(1,2)*1000` and `chm.drift(1,21)*60` are carrier-specific result contracts; do not remove or reinterpret multipliers without an acceptance/report-unit review.

### CM Formula Semantics Used by This Carrier

| Expression family | Meaning | Authoring constraint |
|---|---|---|
| `chm.noise(start,end)` | Signal noise over the stated raw-data time window | Bind the exact fixed channel. Preserve window boundaries and multiplier unless the test specification changes them deliberately |
| `chm.drift(start,end)` | Regression slope across the stated baseline window | Keep the signal channel and any unit conversion such as `*60` explicit |
| `chm.sig_value(stat,start,end)` / `chm.signalStatistic(...)` | Signal statistic over a window, commonly average/min/max | A raw signal channel and minute-based range are required |
| `chm.signalValue(time)` | Signal value at a specific minute | Requires a sampled signal at that point |
| `AUDIT.path(time,"forward"/"backward")` | Audit property selected at/after or at/before the requested minute | Retain the full observed device path unless its abbreviation is proven unambiguous |
| `precond.path` | Pre-run configuration/identity property | It does not read a raw chromatogram and cannot substitute for an audit event |
| `peak.*`, `chm.peak(...)` | Processed peak, calibration or component property | Require the matching processing method and component/channel binding |
| `seq.*`, `smp.*`, `injection.*`, `gen.*` | Sequence, sample, injection or software metadata | Use only fields observed in the selected carrier/config or explicitly verified |

### Direct Formula Object Contract

For every proposed direct-formula change, supply all of: exact existing sheet name, A1 cell/range from this inventory, `object_type: ReportFormulaObject`, CM formula text, `fixed_channel` when the source object uses a channel, `fixed_component` for component/peak context, and the required audit/channel/processing dependencies. If an object is absent from this inventory, it is not safe to invent in V0.1 clone-and-patch generation.

### HPLC Report Authoring Guardrails

1. Choose the data source first: raw VWD signal, detector audit setting, detector precondition, processed peak, or metadata.
2. Reuse the observed sheet/cell/object and fixed channel whenever it has the same semantic role.
3. A report formula can be syntactically valid but evaluate to `n.a.` when the instrument configuration, channel, audit path, wavelength, lamp configuration or processing component is absent.
4. Mark `OPEN VERIFICATION REQUIRED` rather than fabricating an unobserved channel, audit path, FormulaOne formula, acceptance criterion, display format or report-table schema.
5. Report tables (`ReportTableObject`) are structured, pipe-delimited definitions, not scalar cell formulas; preserve them unless a controlled CM before/after pair validates a table write rule.

## Sheet Applicability

| Sheet | Active | Each Injection | Query | Injection Variable | Query Values |
|---|---|---|---|---|---|
| Sheet2 | N | Y | N |  |  |

## Sheet: Sheet2

| Cell / Range | Object Type | Formula | Fixed Channel | Fixed Component |
|---|---|---|---|---|
| A1:H43 | ReportTableObject | peak.number \| "No. " \| chm.channel \| peak.retention_time("detected")*60 \| "Retention Time" \| "s" \| injection.name \| "PumpPressureVirtual" \| peak.name \| peak.start_time*60 \| "Peak Start " \| "s" \| injection.name \| "PumpPressureVirtual" \| peak.name \| (peak.retention_time("detected")-(peak.start_time))*60*1000 \| "Valve Switching Time" \| "ms" \| injection.name \| "PumpPressureVirtual" \| peak.name \| peak.height \| "PeakMaxPressureEnhancement" \| chm.signalUnit \| chm.channel \| audit.ColumnComp.UpperValve.CurrentPosition \| "UpperValvePosition" \| "" \| injection.name \| "PumpPressureVirtual" \| peak.name \| audit.ColumnComp.LowerValve.CurrentPosition \| "LowerValvePosition" \| "" \| "PumpPressureVirtual" \| audit.PumpModule.Pump.Flow.Nominal \| "Flow.Nominal" \| "ml/min" \| injection.name \| chm.channel \| peak.name |  |  |
