# Feature: Raw Signal and Audit Export

## Purpose

Extract injection raw channel data and audit trail data from CMBX files into readable TSV files.

## User Workflow

1. Load a CMBX file.
2. Select signal channels or audit trail objects.
3. Click `Export Selected`.
4. Use the exported TSV files for formula evaluation, debugging, or external analysis.
5. Use the `Raw Plot` tab to compare selected channels visually and mark one channel as benchmark.

## Main Modules

```text
chromeleon_runtime.py
chromeleon_bridge.py
chromeleon_signal_exporter.cs
chromeleon_audit_exporter.cs
report_formula_evaluator.py
```

## Inputs

- Raw `.raw` payloads extracted from CMBX entries.
- Chromeleon runtime DLLs, either from local installation or approved dependency folder.

## Outputs

- Signal TSV files with retention time and signal value columns.
- Audit TSV files with RetTime, device, message, trigger, property, and value columns.

## Current Behavior

- Signal export is used by CM formula evaluation for `chm.*` expressions.
- Raw plot preview caches decoded channel points per package/signal/raw file to make repeated comparisons faster.
- Audit export is used by `AUDIT.*`, `precond.*`, RetTime lookup, and sequence timebase extraction.
- Evaluation contexts cache decoded signal and audit data while processing one injection/report.

## Known Limits

- Signal and audit decoding still require Chromeleon runtime DLLs.
- The tool does not bundle Thermo/Chromeleon DLLs.
- Without DLLs, package browsing and embedded structure inspection can still work, but raw formula evaluation cannot be complete.

## Verification

- Validated by reproducing FOQ temperature accuracy, heatup/cooldown, stability, PCC, preheater, and calibration values from `6545327.cmbx`.
