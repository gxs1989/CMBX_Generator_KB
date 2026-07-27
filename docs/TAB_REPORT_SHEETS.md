# Report Sheets Tab

## Purpose

The Report Sheets tab is the report-output workspace.

- When an injection is selected, the table shows the common report sheets and the sheets that correspond to that injection.
- When a sequence is selected, the table shows the corresponding report sheets for every injection in the sequence.
- Rows are highlighted green when they are directly applicable to the selected injection or detected as a direct name match.

The tab exports filled Chromeleon-style `.xls` reports from the real FormulaOne template stored in CMBX.

## Internal Preview

Selecting a report sheet row builds an internal Excel-like table preview.

- The preview first exports a filled Chromeleon-style `.xls` for the selected row's injection, report template, and report sheet.
- The generated workbook is read back into the internal preview table when `xlrd` is available.
- If workbook reading fails, the preview falls back to the older template-object/formula preview.
- The internal view shows columns `A:P` and the first 160 rows. Double-click/open-in-Excel remains the source of truth for full FormulaOne layout and formatting.

## User Actions

- Click `Export Filled CM Report` with an injection selected to generate that injection's `.xls` report.
- Click `Export Filled CM Report` with a sequence selected to generate one `.xls` containing all corresponding sequence report sheets.
- Double-click a report sheet row to open a filled `.xls` generated from that row's injection, report template, and report sheet.
- Select a report sheet row to preview it internally.

## Output

Injection report exports are written below:

```text
<output folder>/<sequence name>/<injection name>/<injection name>.xls
```

Sequence report-sheet exports are written below:

```text
<output folder>/<sequence name>/<sequence name>_report_sheets.xls
```

## Implementation Boundary

UI behavior lives in `app.py` methods:

- `_build_report_sheets_tab`
- `_populate_report_sheets`
- `_populate_report_sheets_for_sequence`
- `preview_selected_report_sheet`
- `export_report_sheets_workbook`
- `open_report_sheet_workbook`

Filled `.xls` generation is delegated to:

- `export_service.export_filled_report_template_workbook`
- `export_service.export_sequence_report_sheets_workbook`
- `formulaone_report_exporter.export_formulaone_report_template`
# V1.2 Status

- Report Sheets continue to validate decoded report templates and formula evaluation.
- This tab is a key diagnostic surface when FOQ DB fields are missing or a wrong report template is selected.
- The same report-cell evaluator feeds FOQ DB export and SQL upload.
