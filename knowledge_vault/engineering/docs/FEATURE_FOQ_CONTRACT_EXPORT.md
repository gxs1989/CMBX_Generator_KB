# Feature: FOQ Contract DB Export

## Purpose

Generate a database-ready FOQ contract workbook from CMBX data and the FOQ result-location mapping file.

The main export action is `Export Candidate DB`. The direct SQL action is `Upload Candidate DB`. Both mean:

```text
CMBX report/raw/audit data + FOQResultLocations mapping -> database-oriented Excel workbook
```

It is not a raw-file export. It reconstructs report-cell values needed by the database contract.

This workbook is intended to become the SQL database import source. For human-readable report review, use the Report Templates tab to export a filled Excel report template; both paths use the same reconstructed report-cell calculation engine.

## User Workflow

1. Load one or more FOQ CMBX packages.
2. Confirm the FOQ mapping workbook.
3. Select device and DB field filters from the mapping workbook.
4. Add candidate sequences.
5. Confirm the report template per candidate sequence.
6. Click `Export Candidate DB` or `Upload Candidate DB`.
4. Review the generated workbook:
   - `DB Data`
   - `Mapping Coverage`
   - `Cell Values`
   - `Dependency Trace`

## Main Modules

```text
foq_result_locations.py
foq_contract_report.py
export_service.py
report_formula_evaluator.py
report_calculation_map.py
```

## Inputs

- One or more CMBX packages.
- Embedded report template.
- Injection raw channels and audit trails.
- FOQ mapping workbook:

```text
foq\FOQResultLocations_V2.83.xls
```

## Outputs

Generated workbook, one per CMBX package:

```text
<output folder>/<sequence name>/
<sequence name>_FOQ_contract_DB.xlsx
```

Workbook sheets:

- `DB Data`: one database-ready row keyed by `dbField`.
- `Mapping Coverage`: status summary for mapped fields.
- `Cell Values`: final resolved value and source report cell.
- `Dependency Trace`: reverse trace from DB field to report cell, derived rule, CM formula cell, definitions criterion, audit data, and raw signal source.

`DB Data` values are normalized to verified report-display precision before workbook save and SQL upload. The cells remain numeric where the source value is numeric.

## Current Derived Rules

Implemented FOQ-derived cell families:

- Temperature Accuracy
- Temperature Precision
- Temperature Stability
- HeatUp and CoolDown
- PCC CoolDown and PCC drift inputs
- Preheater port checks and temperature differences
- Column ID checks
- Factory Default metadata and serial number checks
- Temperature Calibration drift cells

## Current 6545327 Comparison Status

Reference reports:

```text
cmbx_data_explorer\outputs\foq_contract_6545327_logic_audit\6545327\6545327.seq\*.xls
```

Generated workbook:

```text
cmbx_data_explorer\outputs\foq_contract_6545327_cm_compare_after_remaining_diff_check\6545327\6545327_FOQ_contract_DB.xlsx
```

Comparison result:

```text
matched: 76
small_numeric: 5
numeric_diff: 0
text_diff: 0
missing: 0
```

Remaining small numeric differences are all in CM signal-statistic cells, not final workbook structure or report-cell mapping.

## Known Limits

- The FOQ contract layer is specialized and should stay separate from the generic CMBX parser.
- Full FormulaOne workbook formula parsing is not implemented; known derived-cell rules are reconstructed explicitly.
- New FOQ report versions may require adding or adjusting derived-cell rules.
- SQL upload currently creates or writes FOQ-style wide tables. TCC C10 devices route to `dbo.VTCC` when table is `AUTO`.

## Verification

- Validated against `6545327.cmbx` and CM-exported `.xls` reports.
- Unit tests currently pass: `52 passed`.
