# Report Templates Tab

## Purpose

The Report Templates tab separates report template context from sequence, injection, and method context.

- When a sequence is selected, all sequence report templates are shown.
- When an injection is selected, report templates applicable to that injection are shown.

The Report Sheets tab is used for filled report output. This tab is only for blank report templates.

## Internal Preview

Selecting a report template row builds an internal Excel-like preview from the blank `.xls` template export when possible.

- The preview first exports the real blank FormulaOne workbook and reads the workbook back through `xlrd`.
- The sheet selector above the preview lists workbook sheets when they can be read and re-renders the selected sheet.
- If workbook reading fails, the preview falls back to decoded XML objects.
- Formula cells are not filled with injection values in this tab.
- The preview shows columns `A:P` and is intended for quick structure review. The exported blank `.xls` remains the source of truth for complete FormulaOne layout and formatting.

## User Actions

- Click `Export Blank Template` to generate the blank Chromeleon `.xls` template.
- Double-click a row to export and open the blank template.
- Select a row to preview the template internally.
- Use the sheet selector to switch template sheets in the internal preview.

Open priority after export:

```text
report template XLS
```

## Output

Report template exports are written below:

```text
<output folder>/<sequence name>/<report template>_report_template.xls
```

The workbook is the real FormulaOne workbook from CMBX exported as Excel 5 `.xls`. It is not filled with injection values.

## FormulaOne Runtime

CMBX report templates store the real Report Designer workbook in `SpreadSheetData` as a FormulaOne binary payload. The exporter currently uses the local 32-bit Chromeleon runtime:

```text
C:\Program Files (x86)\Thermo\Chromeleon\bin\Dionex.Controls.dll
C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe
```

The runtime flow is:

```text
SpreadSheetData blob
-> FormulaOne Workbook.ReadFromBlob
-> Workbook.WriteToXml / ReadFromXml to expand all template sheets
-> write calculated values with set_NumberSRC / set_TextSRC
-> Workbook.Export(..., Excel5, selected sheets)
```

This means the current implementation can reproduce the blank `.xls` template when the Chromeleon FormulaOne runtime is present. A portable dependency bundle is still future work.

## Implementation Boundary

UI behavior lives in `app.py` methods:

- `_build_report_templates_tab`
- `_populate_report_templates`
- `_populate_report_templates_for_injection`
- `preview_selected_report_template`
- `export_selected_templates`
- `open_selected_templates`

Blank template generation is delegated to `export_service.export_embedded_report_template` and `formulaone_report_exporter.export_formulaone_report_template`.
# V1.2 Status

- Report Templates remains the place to inspect embedded report definitions carried by a CMBX.
- FOQ DB candidate rows now allow per-sequence report template selection because one CMBX can contain multiple templates.
- Use this tab when verifying whether a module uses templates such as `REPORT_VATCC_V1_01` or `report_vtcc_2_12`.
