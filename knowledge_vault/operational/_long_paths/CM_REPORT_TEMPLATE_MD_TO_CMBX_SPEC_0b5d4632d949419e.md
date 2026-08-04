# CM Report Template Markdown to Standalone CMBX Specification

**Status:** V1.1 - static report creation plus native Audit Trail and Peak Summary tables  
**Authoring goal:** A web model describes a new report in Markdown; CMBX Data Explorer creates the report sheets, cells, CM formulas and FormulaOne formulas and packages them as a standalone report-template CMBX.  
**Important distinction:** The compiler uses an internal neutral CMBX/FormulaOne carrier only for valid binary serialization. The Markdown does not reuse carrier business sheets, cells, formulas or layout.

## 1. Design Principle

The default workflow is `create_from_blank`, not `clone_and_patch`:

```text
instrument-method intent
-> web model designs a small report
-> Markdown declares sheets and cells
-> local compiler creates a new FormulaOne workbook
-> local compiler creates CM ReportFormulaObject bindings
-> standalone report-template CMBX
```

The web model may freely choose new sheet names and new cell locations. It must not search for a convenient old cell merely because an older template used that location.

The word "blank" means **business-level blank**. The compiler retains only a neutral binary carrier needed by Chromeleon to deserialize FormulaOne and CpXm data.

## 2. V1 Capability Boundary

| Capability | V1 status |
|---|---|
| Create one or more new report sheets | Supported |
| Create text and numeric cells | Supported |
| Create FormulaOne cell formulas such as `=A3+A4`, `IF`, `MAX`, cross-cell and cross-sheet references | Supported; Chromeleon recalculates on open |
| Create direct CM `ReportFormulaObject` formulas | Supported |
| Bind a CM formula to a fixed channel/component | Supported |
| Set sheet active/each-injection behavior | Supported |
| Set column widths and row heights | Supported |
| Apply simple style presets and number formats | Supported |
| Create native Audit Trail tables with runtime event rows | Supported |
| Create native Peak Summary tables with formula-defined columns and runtime injection rows | Supported |
| Create Integration tables | Schema recognized; creation blocked until a Processing Method integration contract is supplied |
| Create Consolidated/Component/Calibration/IRC/MS/Fraction tables | Not yet implemented |
| Create charts, images, signatures, complex merged layouts, named ranges or advanced print design | Not in V1 |
| Locally evaluate every CM or FormulaOne formula | Not supported; CM performs final evaluation |

Use static cells for fixed calculations. Use `audittrail` for run commands/messages/events and `peak_summary` for rows defined by injections. Do not use an Integration table merely to obtain dynamic rows: its rows are integrated peaks and require Processing Method results.

## 3. Formula Engines

Never mix the two formula languages.

| Engine | Markdown section | Syntax | Typical use |
|---|---|---|---|
| CM report formula | `### CM Formula:` | No leading `=` | `seq.*`, `injection.*`, `AUDIT.*`, `precond.*`, `chm.*`, report variables |
| FormulaOne workbook | `### Workbook Formula:` | Leading `=` required | Arithmetic, `IF`, lookup, summary, pass/fail, cell-to-cell calculation |

Direct CM formulas fetch run/injection/channel/audit data. FormulaOne formulas calculate from report cells.

## 4. Required Front Matter

```yaml
---
kind: cm_report_template
spec_version: 1.0
template_name: My_New_Report
generation_mode: create_from_blank
workbook_policy: create_static
---
```

Rules:

- `template_name` is the report name shown after import.
- Do not add `reference_template` in `create_from_blank` mode.
- Every declared cell/formula uses `operation: create`.
- Sheet names must be unique.

## 5. Sheet Declaration

````markdown
## Sheet: Summary

### Sheet Settings
```yaml
active: true
each_injection: true
column_widths: [A=24, B=18, C=18, D=14]
row_heights: [1=24, 3=20]
```
````

`column_widths` uses `COLUMN=WIDTH`; `row_heights` uses `ROW=HEIGHT`.

## 6. Workbook Cells

### 6.1 Text

````markdown
### Workbook Text: A1
```yaml
operation: create
value_type: text
value: TCC Test Summary
style: title
```
````

### 6.2 Number

````markdown
### Workbook Value: A4
```yaml
operation: create
value_type: number
value: 1
number_format: '0.00'
```
````

### 6.3 Cell-to-cell Formula

````markdown
### Workbook Formula: C4
```yaml
operation: create
value_type: formula
formula: '=A4+B4'
number_format: '0.00'
style: result
```
````

Formula rules:

- keep the leading `=` in Markdown;
- use FormulaOne/Excel-style addresses;
- reference a cell only after its source meaning is declared;
- final calculation is performed by Chromeleon after import/open;
- a Help-listed function is syntax evidence, not proof that the business calculation is correct.

## 7. Direct CM Formula Cells

````markdown
### CM Formula: B2
```yaml
operation: create
object_type: ReportFormulaObject
formula: seq.name
fixed_channel: ''
fixed_component: ''
style: label
```
````

Channel example:

````markdown
### CM Formula: B6
```yaml
operation: create
object_type: ReportFormulaObject
formula: 'chm.sig_value("average", AUDIT.RetTime1(1,"forward")-1, AUDIT.RetTime1(1,"forward")-0.2)'
fixed_channel: ExtTemp_LowerCC
fixed_component: ''
number_format: '0.00'
style: result
```
````

Rules:

- CM formulas never start with `=`;
- every `AUDIT.RetTimeN` must be produced by the method;
- every `fixed_channel` must exist in the method/configuration;
- do not invent a CM variable because its name sounds plausible;
- use the embedded CM formula language/help catalog as syntax evidence.

## 8. Native Dynamic Tables

Dynamic tables are runtime row generators. Their declared A1 range is the design-time table area; Chromeleon expands or contracts the body when the report is evaluated.

### 8.1 Audit Trail Table

Use this table for commands, messages, warnings, errors and logged properties from the current injection. It does not require peak integration. The native columns are controlled by table options and cannot be replaced by `Table Column` blocks.

````markdown
### Dynamic Table: A3:C10
```yaml
operation: create
table_type: audittrail
body_rows: 6
audit_level: Expert
show_run: true
show_preconditions: false
show_day_time: true
day_time_format: hh:mm:ss
show_device: false
```
````

Width rule:

```text
column count = 2 + show_day_time + show_device
```

With `show_day_time: true` and `show_device: false`, use three columns. To report valve position changes, the Instrument Method must write the position to the audit trail, for example by logging the relevant valve property. The table does not invent an event that the method did not log.

`audit_level` accepts the native CM levels used by the source table, such as `Normal`, `Advanced`, `Expert`, `Performance`, `Diagnostics`, or `ErrorsAndWarnings` when verified by the target CM version.

### 8.2 Peak Summary Table

A Peak Summary table uses injections as runtime rows. Each `Table Column` is a CM report formula, not a FormulaOne cell formula.

````markdown
### Dynamic Table: A3:C9
```yaml
operation: create
table_type: peak_summary
body_rows: 3
sort_formula: injection.number
show_unknown: true
show_standard: true
show_validation: true
show_matrix: true
show_blank: true
show_spiked: true
show_unspiked: true
fixed_channel: ''
requires_processing: false
```

#### Table Column: Injection
```yaml
formula: injection.name
header: Injection
unit: ''
channel: ''
component: ''
```

#### Table Column: Model
```yaml
formula: AUDIT.ColumnComp.ModelNo
header: Device Model
unit: ''
channel: ''
component: ''
```

#### Table Column: Sequence
```yaml
formula: seq.name
header: Sequence
unit: ''
channel: ''
component: ''
```
````

Rules:

- The A1 range width must equal the number of `Table Column` blocks.
- Column formulas do not start with `=`.
- `injection.*`, `seq.*`, verified `AUDIT.*`, and other injection-level formulas can be used without peak integration.
- Any `peak.*` column changes the dependency: the report needs a Processing Method that creates matching peak results and may also need a fixed channel/component or peak selection.
- `body_rows` is the design-time preview body size, not a limit on runtime injection rows.
- V1.1 does not yet compile custom injection-query trees or additional Channel/Component header rows.

### 8.3 Integration Table Boundary

`table_type: integration` is recognized during parsing but deliberately blocked. An Integration table's rows are peaks of the current injection. Before enabling it, the MD must eventually declare and validate:

- Processing Method identity and integration availability;
- selected/fixed channel rules;
- unknown/identified peak inclusion;
- peak/component selection;
- each column's peak formula and header formula.

This is a data-contract requirement, not only an XML serialization issue.

## 9. Style Presets

| Style | Intended use |
|---|---|
| `title` | Main report title |
| `header` | Table/header row |
| `label` | Normal labels |
| `result` | Calculated/output values |
| `warning` | Review or failure indicator |

Keep V1 layout simple. Use widths, heights, styles and number formats rather than complex graphics.

## 10. Complete Example

````markdown
---
kind: cm_report_template
spec_version: 1.0
template_name: Simple_TCC_Report
generation_mode: create_from_blank
workbook_policy: create_static
---

## Sheet: Summary

### Sheet Settings
```yaml
active: true
each_injection: true
column_widths: [A=24, B=18, C=18]
row_heights: [1=24]
```

### Workbook Text: A1
```yaml
operation: create
value_type: text
value: Simple TCC Report
style: title
```

### Workbook Text: A2
```yaml
operation: create
value_type: text
value: Sequence
style: header
```

### CM Formula: B2
```yaml
operation: create
object_type: ReportFormulaObject
formula: seq.name
fixed_channel: ''
fixed_component: ''
style: result
```

### Workbook Value: A4
```yaml
operation: create
value_type: number
value: 1
```

### Workbook Value: B4
```yaml
operation: create
value_type: number
value: 2
```

### Workbook Formula: C4
```yaml
operation: create
value_type: formula
formula: '=A4+B4'
style: result
```
````

## 11. Preflight and Validation

The compiler must reject:

- duplicate sheet names;
- cells assigned more than once;
- formulas targeting undeclared sheets;
- dynamic tables overlapping declared cells or other dynamic tables;
- Peak Summary ranges whose width does not equal the declared column count;
- Audit Trail ranges whose width does not match the selected Day Time/Device columns;
- custom columns on an Audit Trail table;
- Integration table creation without a verified Processing Method contract;
- invalid A1 addresses;
- FormulaOne formulas without `=`;
- CM formulas beginning with `=`;
- missing fixed-channel evidence when the test requires it;
- unsupported dynamic-table/chart/layout requests represented as if V1 could compile them.

After packaging, the program must reopen the CMBX and verify:

1. report name;
2. FormulaOne SheetList;
3. Report `SheetDescription` names;
4. print-sheet setup names;
5. CM formula objects, ranges and fixed channels;
6. FormulaOne formulas read back from the runtime.

## 12. Legacy Compatibility

`spec_version: 0.2` with `generation_mode: clone_and_patch` remains available for controlled edits to an existing report. It is not the default authoring workflow for new reports.

## 13. Open Items

- Integration, Consolidated, Component, Calibration, IRC and other specialized `ReportTableObject` schemas;
- custom injection-query trees and fixed-peak selection for Peak Summary;
- dynamic table column number/date formatting and additional header-row formatting;
- charts and images;
- merged ranges and advanced border/print-layout control;
- complete local evaluation of CM and FormulaOne formulas;
- end-to-end CM 7.2 compatibility for generated report templates.
