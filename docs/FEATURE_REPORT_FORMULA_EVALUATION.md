# Feature: Report Formula Evaluation

## Purpose

Evaluate supported Chromeleon report formulas directly from CMBX raw data, audit trails, and embedded report templates.

## User Workflow

1. Load a CMBX file.
2. Select an injection/report context.
3. Generate a filled CM report workbook or FOQ DB workbook.
4. Review formula cells, evaluated values, source channels, audit RetTimes, and calculation details through the generated workbook trace sheets.

## Main Modules

```text
report_formula_evaluator.py
report_workbook_builder.py
report_calculation_map.py
embedded_report_extractor.py
```

## Inputs

- Embedded report XML.
- Formula objects with cell range, formula text, and fixed channel.
- Injection audit trail.
- Raw signal channels.

## Outputs

- Injection report workbooks.
- FOQ DB contract workbooks.
- Calculation map sheets that describe known derived-cell rules.

## Supported Formula Families

```text
AUDIT.RetTimeN(1,"forward")
AUDIT.<path>(time)
AUDIT.<path>(time,"forward")
precond.<path>
seq.name
seq.update_time
seq.timebase
injection.name
smp.name
chm.sig_value(...)
chm.signalStatistic(...)
chm.signalValue(...)
chm.noise(...)
chm.drift(...)
```

## Important CM Semantics

- `chm.sig_value("average", start, end)` averages raw points in the inclusive window.
- `chm.drift(start, end)` is modeled as a linear regression slope over raw points.
- `chm.sig_value("drift", start, end)` is modeled separately as a coarser 30-second resampled slope for the observed FOQ PCC drift case.
- `chm.noise(start, end)` is modeled as peak-to-peak residual after subtracting a linear regression trend.
- `seq.update_time` is read from the sequence command payload when available and returned as an Excel serial date.

## Remaining Small Differences

Compared with CM-exported reports for `6545327.cmbx`, the remaining differences are small numeric signal-statistic differences:

```text
Noise_CC_Temp:        0.00091460407603 vs 0.000990660936764698
Noise_PCC_Temp:       0.00176461130623 vs 0.0017704562724318862
Noise_PrehtLeft_Temp: 0.00184992326739 vs 0.0019452076008903418
Noise_PrehtRight_Temp:0.0103409251503  vs 0.010308815016429662
PCC_Drift:            0.0665819267633  vs 0.06585877046838409
```

Current classification:

```text
numeric_diff: 0
text_diff: 0
missing: 0
```

These differences are likely caused by CM-internal signal-statistic sampling/interpolation details that are not fully documented yet.

## Verification

- Unit tests cover formula parsing, RetTime lookup, audit property lookup, signal formulas, noise, drift, and derived report-cell rules.
- Current test status: `53 passed`.
