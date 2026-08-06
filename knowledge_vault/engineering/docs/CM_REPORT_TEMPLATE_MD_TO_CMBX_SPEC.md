# CM Report Template Markdown to Standalone CMBX Specification

**Status:** V1.8 - one universal Report MD contract for CM report CMBX and External Report Engine execution
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

The user prompt may be short because the uploaded SPEC and module summary carry the detailed contract. A normal request can be as small as:

```text
Create the method and report MD for the TCC 20 -> 50 -> 20 heat-up/cool-down test.
```

The model must resolve RetTime meaning, channels, result formulas and display precision from the supplied KB. Do not require the user to restate those facts. When module evidence distinguishes a production result from a diagnostic value, the production contract takes precedence. Never promote a diagnostic endpoint to the primary result merely because both values are available.

The word "blank" means **business-level blank**. The compiler retains only a neutral binary carrier needed by Chromeleon to deserialize FormulaOne and CpXm data.

### 1.1 Multiple Method MD / Shared Sequence Report Contract

A report-generation request may provide one Method MD or an ordered collection of
Method MD files. When multiple Method MD files are supplied, they represent separate
Instrument Methods and normally separate Injection rows in one planned Sequence. The
required output remains **one shared Report Template MD** unless the user explicitly
requests separate templates.

Method contracts and Injection instances are different layers. One Method MD may be
assigned to one, two, or many Injection rows. Reusing the same Method MD does **not**
require duplicate Method MD inputs and must not block Report or Sequence generation.
The shared Report Template binds that Method contract once, then evaluates each runtime
Injection through `each_injection: true`, an explicit supported Injection query, or a
verified sequence-level row source. Duplicate Injection instances do not create new
channels, RetTime meanings, variables, or formulas; they create additional runtime
contexts for the same contract.

Before writing report cells, the web model must build an internal coverage map:

| Binding scope | Required interpretation |
|---|---|
| Method MD file | One independently executed Instrument Method contract |
| Injection | One runtime instance of a Method contract; multiple rows may reuse the same Method MD |
| `RetTimes.RetTimeN` | Injection-local anchor; the same number in another Method MD is not the same event |
| Acquired channel | Available only in injections whose Method MD enables that channel |
| Logged property / Protocol | Available only where the corresponding Method explicitly produces it |
| Shared Report Template | May contain method-specific sheets plus verified sequence/injection summary sheets |

Authoring rules:

1. Read **every** binding Method MD before designing the report. Do not derive the
   shared report from only the first file.
2. Keep the source Method/Injection explicit in sheet titles, labels or source columns
   whenever two methods reuse the same RetTime number, channel name or variable name
   with different meanings.
3. A sheet with `each_injection: true` is evaluated in the current Injection context.
   Its Direct CM formulas must use evidence produced by the Method bound to that
   Injection. It must not assume that another Injection's RetTime or raw channel is in
   the same formula context.
4. Prefer separate method/test sheets when the selected methods expose different
   channels, RetTime semantics, windows or acceptance criteria. Reuse a common sheet
   only when the contracts are genuinely identical.
5. FormulaOne cell references calculate within the instantiated workbook/sheet. They
   do not by themselves fetch a value from another Injection. Cross-Injection summaries
   require a verified native row source (for example an injection-based Peak Summary
   table), a verified sequence/report variable, or an External Report Engine design.
6. If the requested cross-Injection result has no supported row source, write
   `OPEN VERIFICATION REQUIRED` in the report design instead of inventing a workbook
   reference that appears to work.
7. Setup, calibration or precondition Methods may legitimately contribute no final
   metric, but their role and any data consumed by later report sections must remain
   explicit. Do not silently omit a selected Method MD.
8. The report must preserve the user-requested method order when presenting
   Injection-level results unless a documented test order requires otherwise.
9. Do not infer that one Method MD means one Injection. If Injection count or names are
   not supplied during report authoring, design an Injection-reusable sheet and leave
   instance count to Sequence Generation. If exact Injection names are supplied, they
   may be used only through a supported report query mechanism.

Minimal multi-method design pattern:

```text
Binding Method MD 1 -> Injection/Test A -> Sheet A -> Direct CM sources from Method 1
Binding Method MD 2 -> Injection/Test B -> Sheet B -> Direct CM sources from Method 2
All selected methods -> optional Summary sheet -> only verified cross-Injection source
```

The compiler packages one Report Template; it does not automatically prove that every
formula is valid for every Injection. That validity comes from this Method-to-Injection
coverage contract and must be checked before CMBX generation.

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
| Create native Audit Trail table objects | Structurally verified by compile + reverse decode; runtime row population still requires CM validation |
| Create native Peak Summary table objects with formula-defined columns | Structurally verified by compile + reverse decode; runtime row population still requires CM validation |
| Create Integration tables | Supported when the MD declares the Processing Method and integrated fixed channel; compile + reverse-decode verified |
| Create a runtime-variable table directly from ordinary chromatogram raw points | Not supported by CM native Report Tables or the V1 compiler |
| Create an arbitrary `event -> row` table without a native CM row source | Not supported as a CM report; declare it as an external-report requirement |
| Create Consolidated/Component/Calibration/IRC/MS/Fraction tables | Not yet implemented |
| Create charts, images, signatures, complex merged layouts, named ranges or advanced print design | Not in V1 |
| Locally evaluate every CM or FormulaOne formula | Not supported; CM performs final evaluation |

Use static cells for fixed calculations. Use `audittrail` for run commands/messages/events and `peak_summary` for rows defined by injections. Do not use an Integration table merely to obtain dynamic rows: its rows are integrated peaks and require Processing Method results.

**Critical row-source rule:** A CM report-column formula calculates a value for an existing row. It does not create rows. Every runtime-variable table must use a native row source such as audit entries, injections, integrated peaks, fractions, or tubes. Formula freedom and row-generation freedom are separate capabilities.

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

Layout rules for reports created from blank:

- Size columns for their longest declared content. Typical starting widths are 24-32 characters for labels, 36-48 for formula/explanation columns, 16-22 for numeric results, and 18-26 for status/source columns.
- Keep long explanations out of narrow result columns. Prefer a dedicated Notes/Source column.
- Give title and section-header rows 24-30 points and data rows enough height for the selected font.
- V1 styles do not create a production print layout automatically. A compact but readable grid is required; complex merging, borders and print-area design remain an open item.

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

**Filtering boundary:** the native Instrument Audit Trail table can filter only by audit level, run/preconditions, and the Day Time/Device display options. It cannot filter rows by command text, device name, property path, or a regular expression. Therefore an `audittrail` table is an audit-event view, not a valve-only or milestone-only business table.

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

With `show_day_time: true` and `show_device: false`, use three columns. Logging a valve property makes that event available in the table, but the table will also contain every other run entry admitted by its audit-level filter. The table neither invents missing events nor isolates requested events from the rest of the audit stream.

### 8.1.1 Paired Method/Report Event Contract

When a web model generates an Instrument Method MD and Report MD together, every requested dynamic event must have a method-side producer and a report-side consumer:

| Requested report evidence | Required method producer | Report consumer |
|---|---|---|
| Full audit evidence including valve position and switch time | Switch the verified valve property, then `Log` that same property after each switch | `audittrail`; unrelated entries at the selected audit level remain visible |
| Exact finite valve-event table | Use a fixed, known schedule or dedicated RetTime anchors | Normal report rows with verified `AUDIT.UpperValve.CurrentPosition(time)` and `AUDIT.LowerValve.CurrentPosition(time)` formulas |
| A named milestone | A quoted `Protocol` or `Log` record at the milestone | `audittrail` |
| RetTime-based scalar result | Assign the required `RetTimes.RetTimeN = System.Retention` anchor | Direct CM formula or FormulaOne formula using the mapped source cells |
| Raw signal statistic | Enable acquisition for the verified channel during the measurement window | Direct CM formula with the verified `fixed_channel` |

The Report MD must not invent custom Audit Trail columns or claim that an unlogged property will appear. If the exact method symbol is unknown, mark it `OPEN VERIFICATION REQUIRED`; do not create a plausible-looking replacement.

For verified TCC valve/stress methods in the supplied method corpus, the source evidence includes:

```text
ColumnComp.UpperValve.CurrentPosition = 6_1 or 1_2
ColumnComp.LowerValve.CurrentPosition = 6_1 or 1_2
Log ColumnComp.UpperValve.CurrentPosition
Log ColumnComp.LowerValve.CurrentPosition
```

This is sufficient for valve events to appear in an Audit Trail table without Processing Method integration. It is not sufficient to suppress unrelated audit entries.

For a finite known switch schedule, prefer a normal report table with one row per expected switch. Existing TCC report evidence uses formulas such as:

```text
AUDIT.UpperValve.CurrentPosition(0.095)
AUDIT.LowerValve.CurrentPosition(0.095)
AUDIT.UpperValve.CurrentPosition(0.19)
AUDIT.LowerValve.CurrentPosition(0.19)
```

Use times or RetTime anchors derived from the paired method; do not copy these example times into a different schedule. A runtime-variable number of valve-only rows is not supported by the V1 report compiler. It requires either a verified dynamic row source such as integrated virtual-channel peaks plus a Processing Method, or external post-processing.

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

### 8.3 Integration Table

An Integration table creates one runtime row per integrated peak of the current injection. It is the verified solution for a runtime-variable valve-event list when the Instrument Method converts every valve switch into a peak on a virtual pressure channel and the assigned Processing Method integrates those peaks.

Verified valve chain:

```text
Instrument Method:
  VirtualChannel PumpPressureVirtual,
    PumpModule.Pump.Pump_Pressure.Signal,
    Type=Digital, Unit="bar", Evaluate=Yes
        -> injection Processing Method: PressureSpikeEval
        -> one integrated pressure peak per valve switch
        -> IntegrationReportTable row
```

The report CMBX does not install or assign the Processing Method. `processing_method` is an enforced runtime contract and must exactly match the injection's Processing Method.

````markdown
### Dynamic Table: A6:C45
```yaml
operation: create
table_type: integration
body_rows: 38
requires_processing: true
processing_method: PressureSpikeEval
fixed_channel: PumpPressureVirtual
sort_formula: peak.group
include_identified_peaks: true
include_unidentified_peaks: true
```

#### Table Column: Switch Time
```yaml
formula: peak.retention_time("detected")*60
header: Switch Time
unit: s
channel: PumpPressureVirtual
```

#### Table Column: Upper Position
```yaml
formula: audit.ColumnComp.UpperValve.CurrentPosition
header: Upper Position
unit: ''
channel: PumpPressureVirtual
```

#### Table Column: Lower Position
```yaml
formula: audit.ColumnComp.LowerValve.CurrentPosition
header: Lower Position
unit: ''
channel: PumpPressureVirtual
```
````

Rules:

- `requires_processing: true`, exact `processing_method`, and non-empty `fixed_channel` are mandatory.
- The A1 range width must equal the number of `Table Column` blocks.
- `body_rows` is only the design-time size; CM expands/contracts the rows to the integrated peak count.
- Every column is evaluated in the peak row context. `audit.*` therefore resolves the valve state associated with that peak time.
- `fixed_channel` must be produced by the Instrument Method and integrated by the named Processing Method.
- Include both identified and unidentified peaks for pressure-spike events unless a validated component naming contract exists.
- A report that compiles and imports can still contain no rows if the injection lacks `PumpPressureVirtual`, uses the wrong Processing Method, or its integration settings do not detect the spikes.

### 8.4 Row-Source Decision and External Report Handoff

Before writing any `Dynamic Table` block, classify the requested rows:

| Requested row meaning | CM-native choice | Processing Method | Authoring rule |
|---|---|---:|---|
| One row per accepted instrument audit entry | `audittrail` | No | Native filtering is coarse; unrelated accepted entries remain visible. |
| One row per injection | `peak_summary` with injection/sequence/audit formulas | No for metadata | Do not describe these rows as signal events. |
| One row per integrated signal event/peak | `integration` | Yes | Declare the exact processing method and fixed channel. |
| A known finite schedule of measurements/events | Normal fixed worksheet rows | No | Use explicit times or verified RetTime/audit anchors; row count is fixed at design time. |
| One row per ordinary chromatogram raw point | No ordinary CM report-table type | N/A | Use a plot, a fixed sampling grid, raw export, or an external report. |
| One row whenever an arbitrary condition becomes true | No generic CM report-table type | N/A | Use a verified native eventization mechanism or hand off to external processing. |
| Only selected valve-switch records from a noisy audit stream | No exact native Audit Trail predicate | No | Use a finite fixed schedule, integrated event signal, or external audit filtering. |

Chromeleon Help defines report tables as typed row sources. Report-column formulas may combine report variables arithmetically, but they operate in the current table-row context. They cannot return a list, append a row, perform a raw-point loop, or convert an arbitrary Boolean condition into a runtime row.

If the user asks for an unsupported native row source, the web model must not invent a new `table_type`. Add this review section instead:

````markdown
## External Report Requirement

```yaml
status: EXTERNAL_PROCESSING_REQUIRED
row_semantics: one row per verified upper/lower valve position change
source: instrument audit trail
event_predicate: property path is UpperValve.CurrentPosition or LowerValve.CurrentPosition
grouping: pair upper/lower changes belonging to the same switch operation
required_columns: [event_time, retention_time, upper_position, lower_position, interval_seconds]
cm_native_reason: Instrument Audit Trail filtering cannot isolate rows by property path or command text
```
````

This block is a design handoff for CMBX Data Explorer or another external report engine. It is **not** compiled into a CM `ReportTableObject` by V1. The CM portion of the same MD may still contain titles, fixed summary cells, direct CM formulas, or a complete Audit Trail table.

For external raw-channel processing, specify the acquired channel, time window, event condition, edge direction, hysteresis/debounce, minimum event spacing, requested columns, aggregation and acceptance rule. If any of these are unknown, mark them `OPEN VERIFICATION REQUIRED` rather than guessing.

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
- Peak Summary or Integration ranges whose width does not equal the declared column count;
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

Preview validation has two paths. Native XLS export is preferred, but a .NET export failure must fall back to the embedded FormulaOne/Markdown cell map. A fallback preview verifies declared cells and formulas; it is not proof of final CM print rendering.

For native dynamic tables, validation has two levels:

1. **Structural validation:** compile, reopen, and reverse-decode `ReportTableObject` sheet/range/type. For Integration tables, column formulas and fixed-channel properties are also verified. This is implemented for Audit Trail, Peak Summary, and Integration.
2. **Runtime validation:** open/evaluate against a real injection in CM and confirm row population, filtering, sorting and values. This remains required before calling a new dynamic-table design production-ready.

## 12. Legacy Compatibility

`spec_version: 0.2` with `generation_mode: clone_and_patch` remains available for controlled edits to an existing report. It is not the default authoring workflow for new reports.

## 13. Open Items

- Integration runtime validation against CM injections using the declared Processing Method/channel contract;
- Consolidated, Component, Calibration, IRC and other specialized `ReportTableObject` schemas;
- custom injection-query trees and fixed-peak selection for Peak Summary;
- dynamic table column number/date formatting and additional header-row formatting;
- charts and images;
- merged ranges and advanced border/print-layout control;
- complete local evaluation of CM and FormulaOne formulas;
- end-to-end CM 7.2 compatibility for generated report templates.

## 14. External Report Engine Backend

This is the only Report SPEC. Do not create or upload a separate external-report specification. A task-specific Report MD may target CM, the External Report Engine, or both:

```yaml
---
kind: cm_report_template
spec_version: 1.0
template_name: My_Report
generation_mode: create_from_blank
execution_backends: [cm, external]
---
```

The CM compiler consumes sheets, workbook cells, CM formulas, and native CM table declarations. The External Report Engine consumes the data contract and external operation blocks below. Both backends describe the same report intent. A backend must explicitly report unsupported declarations; it must not silently approximate them.

### 14.1 External Data Requirements

The engine applies one Report MD to every selected CMBX/injection satisfying this contract:

````text
## Data Requirements
```yaml
channels: [CC_Temp, ExtTemp_UpperCC]
audit_paths: [ColumnComp.UpperValve.CurrentPosition]
ret_times: [1, 2]
```
````

Channels used by operation blocks and RetTimes referenced by formulas are also inferred automatically. An empty list means no requirement of that type.

### 14.2 External Scalar Formula

Supported V1 functions are `chm.sig_value` / `chm.signalStatistic` with `average`, `min`, `max`, `stddev`, and `drift`; `chm.signalValue`; `chm.noise`; and `chm.drift`. Time expressions may use `AUDIT.RetTimeN`.

````text
### Scalar: MeanUpper
```yaml
label: Upper thermometer average
channel: ExtTemp_UpperCC
formula: chm.sig_value("average", AUDIT.RetTime1-1, AUDIT.RetTime1-0.2)
number_format: 0.00
```
````

### 14.3 External Cell-to-cell Formula

An operation ID becomes a variable available to later operations:

````text
### Formula: Difference
```yaml
label: Upper minus lower
expression: MeanUpper - MeanLower
number_format: 0.000
```
````

Supported expressions: constants, `+ - * / % **`, comparisons, `and/or/not`, conditional expressions, and `abs`, `min`, `max`, `round`, `sum`. Arbitrary Python, filesystem, process, or network access is prohibited.

### 14.4 Filtered Audit Event Table

Unlike a native CM Audit Trail table, this external table creates rows only for matching events:

````text
### Audit Event Table: ValveChanges
```yaml
label: Valve position changes
property_paths: [ColumnComp.UpperValve.CurrentPosition, ColumnComp.LowerValve.CurrentPosition]
message_contains: []
value_changes_only: true
group_within_seconds: 1.0
columns: [time_min, device, property, value, message]
```
````

Property paths use suffix matching. `group_within_seconds` can combine related upper/lower valve records into one row.

### 14.5 Raw Event Table

This external-only row source detects threshold crossings directly from raw channel points and does not require Chromeleon integration:

````text
### Raw Event Table: ThresholdCrossings
```yaml
label: Threshold crossings
channel: LeakSignal
threshold: 1.0
edge: both
hysteresis: 0.05
debounce_seconds: 1.0
start_min: 0
end_min: 30
columns: [time_min, value, edge]
```
````

`edge` is `rising`, `falling`, or `both`.

### 14.6 External Raw Plot

````text
### Plot: TemperaturePlot
```yaml
label: Column compartment temperature
channel: CC_Temp
start_min: 0
end_min: 60
```
````

### 14.7 External Backend V1 Boundary

| Capability | External V1 |
|---|---|
| Multiple CMBX/injection compatibility matrix | Supported |
| Raw signal statistics and point lookup | Supported |
| RetTime-based windows | Supported |
| Safe cell-to-cell arithmetic and conditions | Supported subset above |
| Filtered/grouped audit event tables | Supported |
| Raw threshold event tables | Supported |
| Raw channel plot preview | Supported |
| Batch XLSX output | Supported |
| Peak integration and Processing Method integration parameters | Not implemented |
| Components and calibration curves | Not implemented |
| External/internal-standard quantification | Not implemented |
| Manual chromatographic integration | Not implemented |
| Full FormulaOne language | Not implemented |
| Layout-perfect CM print rendering | CM backend only |

Report MD authors may combine CM sections and external sections in one document. Backend-specific limits must be reported during preflight.
