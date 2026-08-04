# Universal HPLC Report Template MD Specification

KB_Profile: Online Web Model  
Scope: Chromeleon report-template Markdown authoring and MD-to-CMBX static/native dynamic-table report creation  
Module_Scope: Shared by TCC, VAS, detector, pump and future HPLC modules  
Source_Policy: Self-contained; no access to local Chromeleon Help is required

## Upload and Routing Rule

Use this one SPEC for every HPLC module. It is sufficient for syntax and
compiler structure. Pair it with up to two module-specific evidence files
when the report must follow an existing method/test contract:

1. `02_REPORT_ORIGINAL_TEMPLATES.md` - decoded carrier objects, formulas and workbook evidence;
2. `03_REPORT_SUMMARIES.md` - semantic roles, method/report dependencies and safe-change guidance.

The universal SPEC defines the language and compiler contract. Module files
decide which channel, audit path, RetTime and processing result are actually
available. The model may create new sheets/cells, a new static layout, and the
native dynamic table types explicitly enabled by Part A. It must not invent
unavailable run data merely because the formula or table syntax exists.

## Embedded Source Index

| Part | Embedded content | Authority |
|---|---|---|
| A | MD-to-CMBX report-template contract, including supported native dynamic tables | Current compiler/write boundary |
| B | CM report formula language reference | HPLC authoring semantics and observed templates |
| C | HPLC-relevant official Help catalog | FormulaOne functions and report-variable lookup |



# Part A - Report Template Generation Contract

**Status:** V1.7 - one universal Report MD contract for CM report CMBX and External Report Engine execution  
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

# Part B - CM Report Formula Language

**Purpose:** Reference for authoring or reviewing Chromeleon `ReportFormulaObject` expressions in Markdown report-template specifications.  
**Sources:** Chromeleon report-variable/report-designer behaviour distilled from the official documentation, plus decoded standalone templates `Report_VTCC_V2_12`, `VAS_DVAS_V_3_45`, `FOQ_REPORT_VVWD_V2_31`, and `Report_VAPump_FOQ_V1_01_02`.  
**Scope:** CM report-variable language and object-binding rules. FormulaOne workbook syntax is intentionally separate.

**Companion sources:** `CM_REPORT_FORMULA_HELP_CATALOG.md` is the complete local CM7 Help index (128 FormulaOne function topics and 994 report-variable topics). `REPORT_VTCC_V2_12_FORMULAONE_INVENTORY.md` is the carrier-level FormulaOne evidence and V0.2 verification matrix for TCC.

## 1. Two Formula Engines

| Engine | Where it is stored | Syntax | Responsibility |
|---|---|---|---|
| CM report formula | XML `SheetDescription/SheetObject[type=ReportFormulaObject]/Formula/@value` | `audit.*`, `precond.*`, `chm.*`, `peak.*`, `seq.*`, `if(...)`, etc. | Pulls data and metadata from the selected injection/context |
| FormulaOne workbook formula | `SpreadsheetDefinition/.../SpreadSheetData/@value` | Excel / FormulaOne cell formulas such as `=MAX(...)` | Combines displayed cells, formatting, lookup and pass/fail layout |

Do not put an Excel formula (for example `=MAX(A1:A5)`) into a CM `ReportFormulaObject`. Do not put `AUDIT.*` directly into an ordinary FormulaOne cell; declare a CM Formula cell so the compiler creates a `ReportFormulaObject`. The V1 writer can create new sheets and arbitrary numeric, text, FormulaOne-formula, and CM-formula cells through its x86 STA host.

## 1.1 HPLC Report Context: What a Formula Can Read

This section is intentionally self-contained for web-GPT authoring. A report is evaluated in an injection/sequence context. Formula validity requires the referenced device, signal, audit record and processing result to exist in that context.

| HPLC area | Common report sources | What it represents | Do not assume |
|---|---|---|---|
| Pump | `precond.PumpModule.*`, `AUDIT.PumpModule.*`, pressure-channel `chm.*` | Pump identity/configuration, commanded/recorded flow or pressure, raw pressure signal | That every system calls the pump `PumpModule`, or that a pressure channel is acquired |
| Sampler | `precond.Sampler.*`, `AUDIT.Sampler.*`, `smp.*`, `injection.*` | Sampler configuration/events, sample metadata, injection-list properties | That an injection event property exists in every audit |
| Column oven / TCC | `precond.ColumnComp.*`, `AUDIT.ColumnComp.*`, temperature-channel `chm.*` | Column compartment identity, nominal/actual temperature and external-thermometer data | That an external thermometer exists, or that an abbreviated audit path is unique |
| UV/VWD/DAD detector | `precond.UV.*`, `AUDIT.UV.*`, `UV_VIS_1`, `UV_VIS_2`, `chm.*`, `peak.*` | Detector configuration, lamp/wavelength/DCR events, raw absorbance signal and processed peaks | That channel names, lamp configuration or wavelength are available on another detector/model |
| General context | `seq.*`, `smp.*`, `injection.*`, `gen.*`, `precond.System.*` | Sequence, sample, injection, user/system and pre-run metadata | That metadata is a substitute for a measured signal or audit event |

### Data-source selection rule

1. Use `precond.*` for the state captured before the analysis starts.
2. Use timed `AUDIT.*` for a setting/event that can change during analysis.
3. Use `chm.*` for raw channel data in minutes.
4. Use `peak.*` / `chm.peak(...)` only after a compatible processing method has produced the relevant peak/component result.
5. Use FormulaOne only to combine already placed report-cell values, display a summary or control workbook layout.

If the author cannot name the source channel, audit path or component from a carrier/configuration contract, the formula is not ready to generate and must be `OPEN VERIFICATION REQUIRED`.

### Virtual channels: method output versus report dependency

A CM `VirtualChannel` command can create a named calculated/acquired signal during the method. It is a method-level dependency and must not be confused with its source raw channel.

```text
VirtualChannel
"PumpPressureVirtual", PumpModule.Pump.Pump_Pressure.Signal,
Type=Digital, Unit="bar", Evaluate=Yes
```

| Case | Report rule |
|---|---|
| Formula `FixedChannel` is the source channel, for example `Pump_Pressure` | The report depends on source-channel acquisition. The virtual channel may be useful for data display or downstream logic, but is not a direct report-formula dependency. |
| Formula `FixedChannel` or formula text names the virtual channel | The report depends on both: (1) the source signal is acquired and (2) the method creates the virtual channel with the exact name, unit/type and expression. |
| An `integration` `ReportTableObject` names the virtual channel in its pipe-delimited column definition | The report depends on a compatible processing method that produces peaks on that virtual channel, in addition to the source acquisition and virtual-channel creation. The table body may be blank before report evaluation. |
| Virtual channel appears only in the method | Do not add it to the report MD merely because it exists. Record it as a method/configuration note only. |

For report generation, record each required virtual channel explicitly: name, source expression, unit/type, acquisition/evaluation behaviour, creating stage, and every report cell that consumes it. If any of those cannot be proven by the selected carrier method/report pair, emit `OPEN VERIFICATION REQUIRED`.

## 2. Formula Object Binding

Each direct CM formula must be represented by one existing or explicitly created `ReportFormulaObject`.

| XML property | Meaning | Authoring rule |
|---|---|---|
| `Range/Left, Top, Right, Bottom` | Zero-based worksheet rectangle | Markdown uses A1 notation; compiler converts and confirms the resulting XML range |
| `Formula/@value` | CM expression | Must follow this document and the selected template/config inventory |
| `FixedChannel/@value` | Channel context for signal/peak formulas | Required whenever formula semantics depend on a channel; must exist in selected configuration |
| `FixedComponentName/@value` | Component context for peak formulas | Required for component-specific `peak.*` values |
| `SheetDescription/SheetName` | Owning report sheet | Exact reference-sheet name; no fuzzy match |

### Report tables are a separate direct-CM object type

Templates can also contain `ReportTableObject`, for example `peak_summary` and `audittrail` tables. Their `Formula` field is a pipe-delimited column definition rather than one scalar cell formula. It may contain multiple variable expressions, labels, units, fixed channel/component entries and empty positional fields.

```text
smp.name | "Sample Name" | "" | ... | peak.area | "Area" | chm.sig_dim+"*min" | ...
```

Treat a report table as a structured object, not as a normal `ReportFormulaObject`. V1 simple-report generation does not create dynamic report tables. Adding or editing table columns requires a separately validated table-object schema.

For an `integration` table, the exported blank template may contain only headers while Chromeleon creates the repeating body when it evaluates an injection with processed peaks. This is expected behaviour, not missing static report-cell data. The author must keep the processing dependency explicit: a method/report package can preserve the table structure, but it cannot promise populated rows unless the selected processing method creates compatible peak results.

Chromeleon Report Designer selects the current channel/component by default. A template generator must write an explicit fixed channel/component wherever the source template does so. This prevents a formula from silently following a different selected channel after import.

### Report Designer / sheet behaviour

| Report item | Purpose | Authoring rule |
|---|---|---|
| `SheetDescription` | Defines one named report sheet plus direct report objects | V1 creates one for every declared new Sheet |
| `SheetSetupCondition` / query fields | Determines whether the sheet is included for an injection or selected context | Treat injection-query changes as a distinct verified change; a correct formula on a non-applicable sheet will not produce a report value |
| `ReportFormulaObject` | Evaluates one CM expression into an existing A1 range | The MD must bind exact sheet, A1 range, formula, object type and fixed context |
| `ReportTableObject` | Repeating, structured report output such as peaks/audit data | Its pipe-delimited formula is not an ordinary cell formula; preserve unless a controlled write rule exists |
| FormulaOne `SpreadSheetData` | Workbook formatting, labels, images, Excel-like formulas and summary cells | V1 creates a new logical workbook with declared sheets/cells; advanced graphics and dynamic tables remain outside V1 |

The direct CM formula layer and FormulaOne layer cooperate: CM objects populate report cells from data/audits; FormulaOne formulas can subsequently reference those cells. Do not reverse the direction by putting a CM expression into a workbook formula cell.

## 3. Formula Categories Available to Web Authoring

The official Help groups report variables by these prefixes/categories. Availability remains configuration and context dependent.

| Prefix / category | Typical purpose |
|---|---|
| `audit.*` | Property/event value from injection audit trail, resolved at a requested time and direction |
| `precond.*` | Instrument state logged before analysis starts |
| `chm.*` | Chromatogram / raw signal values, statistics, noise, drift, peak counts and units |
| `peak.*` | Peak results and calibration data; normally needs fixed channel and often component |
| `component.*` | Processing-method component settings |
| `procMeth.*` | Processing-method properties |
| `seq.*` | Sequence metadata and custom variables |
| `injection.*` | Injection-list metadata |
| `smp.*` | Sample metadata |
| `gen.*` | General software/user metadata |
| `instMeth.*` | Instrument-method metadata |
| `rdf.*` | Report-template metadata |
| `cf.*` | User-defined custom formula |
| `table.*`, `sst.*`, `sstResult.*` | Integration / system suitability tables and IRC results |
| `frac.*`, `tube.*` | Fraction collection data |
| `ms.*`, `*.msExt.*`, `*.msSettings.*`, `*.sls.*` | Mass-spectrometry-specific contexts |
| `history.*`, `data_audit.*`, `audit_event.*` | History and audit-table contexts |

For web-based authoring, this document and the selected carrier's formula inventory are intended to be self-contained context. Use the category table and carrier evidence below; do not require a local Help installation. If an expression or device path is not represented here or in the selected carrier, label it `OPEN VERIFICATION REQUIRED` rather than inventing it.

### 3.1 Coverage Boundary

This is a **formula-family reference**, not a complete formal grammar for all Chromeleon installations.

| Layer | What is covered | What is not yet complete |
|---|---|---|
| Direct CM formulas | Observed namespaces, common raw-signal/audit/metadata/peak patterns, and the listed global-function examples | Every proprietary namespace, device-specific property path, function overload, processing result and report-table schema |
| Direct CM formula extraction | Stored `ReportFormulaObject` strings, fixed context, sheet and range from decoded XML | Semantic correctness for a different instrument configuration or a local evaluator for every expression |
| FormulaOne cell-to-cell formulas | Workbook-wide formula inventory extraction, existing-cell write/read path, the VTCC observed function-family matrix, and direct cross-sheet references | All 128 Help-listed functions as runtime-verified patterns, array behavior, volatile functions, workbook names, and a local calculation engine |

Therefore, a web author may place a FormulaOne formula in any newly declared cell. Prefer observed formula patterns or a CM-created control pair. If it relies only on a Help-listed but unobserved function family, label it `OPEN VERIFICATION REQUIRED`. The compiler can persist the string; it does not certify every FormulaOne function as valid or calculate the whole workbook locally.

### 3.2 TCC FormulaOne Verified Function Set

The `Report_VTCC_V2_12` inventory contains 640 FormulaOne cell formulas across 18 populated sheets. A controlled V0.2 write/read/repack matrix verified all function families actually observed in that carrier:

```text
IF, ROUND, AND, ABS, ISNUMBER, INDIRECT, ADDRESS, AVERAGE, OR, ROW,
MATCH, CONCATENATE, COUNTIF, MAX, MIN, SUM, ISNA, VALUE, NOT, LEFT,
SEARCH, TIME, ISERROR, FIND
```

Direct cross-sheet references such as `Definitions!A2` were also persisted and read back. This verifies the TCC carrier's observed formula vocabulary, not all 128 FormulaOne Help functions or every possible argument/range combination. The generic inventory exporter can reproduce the carrier evidence with:

```powershell
python cmbx_data_explorer\tools\export_report_formula_inventory.py `
  "Report_VTCC_V2_12.cmbx" `
  "Report_VTCC_V2_12_full_formula_inventory.md" `
  --include-formulaone
```

## 4. Core Syntax and Semantics

### 4.1 Audit and precondition data

```text
precond.ColumnComp.SerialNo
AUDIT.ColumnComp.ModelNo
AUDIT.ColumnComp.CC.Temperature.Nominal(6,"forward")
audit.Sampler_INPUT_1.State(0.25,"backward")
```

- `precond.*` reads settings logged before analysis.
- `audit.*` reads an audit-trail property. Its time is in minutes.
- `"backward"` selects the last value at/before the requested time; `"forward"` selects the first at/after that time.
- Abbreviated device paths are only safe when unambiguous. Generated files must retain the full observed path unless a configuration contract explicitly proves an abbreviated path is unique.

### 4.2 Signal and chromatogram data

```text
chm.signalValue(0.5)
chm.signalStatistic("min", 0, 1.5)
chm.sig_value("average", AUDIT.RetTime1(1,"forward")-1, AUDIT.RetTime1(1,"forward")-0.2)
chm.noise(start, end)
chm.drift(start, end)
```

Signal statistics are min/max/average over a selected time range; `signalValue` returns a value at a specific time. Drift is the regression-line slope across the selected baseline range. In FOQ TCC evidence, the fixed channel supplies the raw signal context.

Use an explicit time range for FOQ work. Whole-chromatogram defaults are rarely a safe contract for a qualification report.

CM expressions can combine signal functions arithmetically. The VA Pump reference uses, for example, an average of normalized noise windows:

```text
(chm.noise(1,2)/chm.sig_value("average",1,2)+...)/5*100
```

This is a valid **CM** scalar expression when bound to the appropriate fixed pressure channel. It is not a FormulaOne expression.

### 4.3 Peak and processing results

```text
peak.retention_time
peak.area
peak.height
peak.calCoefficient(1)
peak.rQuadrat / 100
```

These values depend on the current/FixedChannel and, where relevant, `FixedComponentName`. They are only valid when the processing method produces the referenced peak/component.

### 4.4 Metadata and text

```text
seq.name
seq.update_time
seq.customVar("Location")
injection.name
smp.name
gen.loggedOnUser.userName
left(smp.name, 30)
```

### 4.5 Global functions

CM has Excel-like global functions. Common safe forms are:

```text
abs(value)
if(condition, true_value, false_value)
round(value, digits)
text(value, format, unit="")
left(text, length)
mid(text, start, length)
right(text, length)
find(text_to_search, text, startpos=1)
iserror(value)
time(year, month, day, hour=0, minutes=0, seconds=0)
```

`if(...)` must return compatible display values. FOQ VAS evidence uses it to return either a measured numeric value or `"not evaluated"`; that cell must therefore be treated as text-or-number by downstream FormulaOne formulas.

## 5. Formula Selection Rules for GPT

1. Identify the requested data source first: pre-run configuration, time-resolved audit state, raw signal, processed peak, or metadata.
2. Retrieve the matching category in this document and the selected carrier template's direct formula inventory.
3. Reuse an observed device path/channel/component if one fits the same semantic role.
4. Bind the formula to an explicit sheet/cell and fixed channel/component.
5. List all required channels, RetTimes, audit paths and processing prerequisites in the report contract.
6. If a formula uses an unknown device path, channel or component, emit `OPEN VERIFICATION REQUIRED`; do not fabricate it solely because a general formula category exists.
7. Use V1 `Workbook Value`, `Workbook Text`, or `Workbook Formula` for new single cells. New sheets, basic widths/heights, style presets and number formats are supported; dynamic tables, charts, images and advanced layout remain separate contracts.

## 6. Observed Template Evidence

| Carrier | Direct CM formulas | Dominant namespaces | Evidence |
|---|---:|---|---|
| `Report_VTCC_V2_12` | 234 | `chm` 106, `AUDIT` 95, `precond` 14, `seq` 12 | External thermometer signal windows, RetTimes, TCC metadata |
| `VAS_DVAS_V_3_45` | 139 | `AUDIT` 58, `smp` 30, `precond` 23, `seq` 11, `peak`, `chm`, `if` | Sampler states, peak calibration, pressure test, carry-over |
| `FOQ_REPORT_VVWD_V2_31` | 323 | `precond` 127, `chm` 95, `AUDIT` 42, report tables | VWD noise/drift, saturation, wavelength, spectral and stray-light evidence |
| `Report_VAPump_FOQ_V1_01_02` | 284 | `AUDIT` 127, `precond` 59, `chm.sig_value` 42, `chm.noise` 10, report tables | Flow, gradient, pulsation and pressure calculations |

This evidence demonstrates that one report family cannot define the full language. The selected carrier provides layout/object placement; this reference provides the formula-family semantics; the selected device/method config limits what can actually run.

## 7. Formula Preflight

For every proposed formula, report all of the following before packaging:

| Check | Result to record |
|---|---|
| Engine | `cm_report_formula` or `formulaone_workbook` |
| Location | Sheet + A1 range + zero-based XML range |
| Formula | Exact source string |
| Context | Fixed channel/component or `none` |
| Dependencies | Audit path, RetTime, raw channel, component, processing method |
| Source evidence | This reference section + observed template object, or open verification |
| Result type | numeric, text, boolean, date/time, or mixed |
| Display | number/date format and whether raw or rounded output is required |

## 8. Known Constraints

- A syntactically accepted CM formula may evaluate as `n.a.` if its variable does not exist in the selected system/configuration.
- Formula validity also depends on processing algorithm where applicable (for example Cobra versus Chromeleon 6 peak detection).
- FormulaOne workbook functions are not the same authoring surface as CM global functions, even where names overlap.
- The generated standalone CMBX must be opened/imported in CM before a new report is claimed production-ready.

# Part C - Embedded HPLC Formula Help Catalog

The following entries are embedded from the local CM7 Help extraction. They are lookup evidence, not proof that every variable is available in every configuration.

## FormulaOne Function Topics

These function names come from the FormulaOne Help collection. The V1 report compiler can persist a formula in a newly declared cell, but only functions marked verified by a control matrix have end-to-end evidence in this project.

| Function | Help summary | Help topic |
|---|---|---|
| `ABS` | ABS returns the absolute value of a number. | `FormulaFunctions/IDH_ABS.htm` |
| `ACOS` | ACOS returns the arc cosine of a number. | `FormulaFunctions/IDH_ACOS.htm` |
| `ACOSH` | ACOSH returns the inverse hyperbolic cosine of a number. | `FormulaFunctions/IDH_ACOSH.htm` |
| `ADDRESS` | ADDRESS creates a cell address as text. | `FormulaFunctions/IDH_ADDRESS.htm` |
| `AND` | AND returns True if all arguments are true; AND returns False if at least one argument is false. | `FormulaFunctions/IDH_AND.htm` |
| `ASC` | ASC returns a copy of text in which the double-byte characters (if any) have been converted to single-byte. Any double-byte characters that do not have single-byte equivalents are left in their original form. | `FormulaFunctions/IDH_ASC.htm` |
| `ASIN` | ASIN returns the arcsine of a number. | `FormulaFunctions/IDH_ASIN.htm` |
| `ASINH` | ASINH returns the inverse hyperbolic sine of a number. | `FormulaFunctions/IDH_ASINH.htm` |
| `ATAN` | ATAN returns the arctangent of a number. | `FormulaFunctions/IDH_ATAN.htm` |
| `ATAN2` | ATAN2 returns the arctangent of the specified coordinates. | `FormulaFunctions/IDH_ATAN2.htm` |
| `ATANH` | ATANH returns the inverse hyperbolic tangent of a number. | `FormulaFunctions/IDH_ATANH.htm` |
| `AVERAGE` | AVERAGE returns the average of the supplied numbers. The result of AVERAGE is also known as the arithmetic mean. | `FormulaFunctions/IDH_AVERAGE.htm` |
| `CEILING` | CEILING rounds a number up to the nearest multiple of a specified value. | `FormulaFunctions/IDH_CEILING.htm` |
| `CHAR` | CHAR returns a character that corresponds to the supplied ASCII code. | `FormulaFunctions/IDH_CHAR.htm` |
| `CHOOSE` | CHOOSE returns a value from a list of numbers based on the index number supplied. | `FormulaFunctions/IDH_CHOOSE.htm` |
| `CLEAN` | CLEAN removes all nonprintable characters from the supplied text. | `FormulaFunctions/IDH_CLEAN.htm` |
| `CODE` | CODE returns a numeric code representing the first character of the supplied string. | `FormulaFunctions/IDH_CODE.htm` |
| `COLUMN` | COLUMN returns the column number of the supplied reference. | `FormulaFunctions/IDH_COLUMN.htm` |
| `COLUMNS` | COLUMNS returns the number of columns in a range reference. | `FormulaFunctions/IDH_COLUMNS.htm` |
| `CONCATENATE` | CONCATENATE joins several text strings into one string. | `FormulaFunctions/IDH_CONCATENATE.htm` |
| `CORREL` | CORREL returns the correlation coefficient of the array1 and array2 cell ranges. Use the correlation coefficient to determine the relationship between two properties. | `FormulaFunctions/IDH_CORREL.htm` |
| `COS` | COS returns the cosine of an angle. | `FormulaFunctions/IDH_COS.htm` |
| `COSH` | COSH returns the hyperbolic cosine of a number. | `FormulaFunctions/IDH_COSH.htm` |
| `COUNT` | COUNT returns the number of values in the supplied list. | `FormulaFunctions/IDH_COUNT.htm` |
| `COUNTA` | COUNTA returns the number of nonblank values in the supplied list. | `FormulaFunctions/IDH_COUNTA.htm` |
| `COUNTIF` | COUNTIF returns the number of cells within a range, which meet the given criteria. | `FormulaFunctions/IDH_COUNTIF.htm` |
| `DATE` | DATE returns the serial number of the supplied date. | `FormulaFunctions/IDH_DATE.htm` |
| `DATEVALUE` | DATEVALUE returns the serial number of a date supplied as a text string. | `FormulaFunctions/IDH_DATEVALUE.htm` |
| `DAY` | DAY returns the day of the month that corresponds to the date represented by the supplied number. | `FormulaFunctions/IDH_DAY.htm` |
| `DAYS360` | DAYS360 returns the number of days between two dates based on a 360-day year (twelve 30-day months). Use this function to help compute payments if your accounting system is based on twelve 30-day months. | `FormulaFunctions/IDH_DAYS360.htm` |
| `DBCS` | DBCS returns a copy of text in which the single-byte characters (if any) have been converted to double-byte characters. Any single-byte characters that do not have double-byte equivalents are left in their original (single-byte) form. | `FormulaFunctions/IDH_DBCS.htm` |
| `ERROR.TYPE` | ERROR.TYPE returns a number corresponding to an error. | `FormulaFunctions/IDH_ERROR_TYPE.htm` |
| `EVEN` | With positive values the specified number is rounded up to the nearest even integer. Negative numbers are rounded down. | `FormulaFunctions/IDH_EVEN.htm` |
| `EXACT` | EXACT compares two expressions for identical, case-sensitive matches. True is returned if the expressions are identical; False is returned if they are not. | `FormulaFunctions/IDH_EXACT.htm` |
| `EXP` | EXP returns e raised to the specified power. The constant e is 2.71828182845904 (the base of the natural logarithm). | `FormulaFunctions/IDH_EXP.htm` |
| `FACT` | FACT returns the factorial of a specified number. | `FormulaFunctions/IDH_FACT.htm` |
| `FALSE` | F ALSE returns the logical value False. This function always requires the trailing parentheses. | `FormulaFunctions/IDH_FALSE.htm` |
| `FIND` | FIND searches for a string of text within another text string and returns the character position at which the search string first occurs. | `FormulaFunctions/IDH_FIND.htm` |
| `FINDB` | FINDB searches for a string of text within another text string and returns the byte position at which the search string first occurs. FINDB is intended for use with languages that use the double-byte character set (DBCS). | `FormulaFunctions/IDH_FINDB.htm` |
| `FIXED` | FIXED rounds a number to the supplied precision, formats the number in decimal format, and returns the result as text. | `FormulaFunctions/IDH_FIXED_1.htm` |
| `FLOOR` | FLOOR rounds a number down to the nearest multiple of a specified precision. | `FormulaFunctions/IDH_FLOOR.htm` |
| `Formula Functions` | Formulas are equations that perform calculations on values in your worksheet. A formula always starts with an equal sign (=). You may know these functions from Microsoft Excel. They can be grouped in the following categories: | `FormulaFunctions/IDH_FORMULA_OVERVIEW.htm` |
| `HLOOKUP` | HLOOKUP searches the top row of a table for a value and returns the contents of a cell in that table that corresponds to the location of the search value. | `FormulaFunctions/IDH_HLOOKUP.htm` |
| `HOUR` | HOUR returns the hour component of the specified time in 24-hour format. | `FormulaFunctions/IDH_HOUR.htm` |
| `IF` | IF tests the condition and returns the specified value. | `FormulaFunctions/IDH_IF.htm` |
| `INDEX` | INDEX returns the contents of a cell from a specified range. | `FormulaFunctions/IDH_INDEX.htm` |
| `INDIRECT` | INDIRECT returns the contents of the cell referenced by the specified cell. | `FormulaFunctions/IDH_INDIRECT.htm` |
| `INT` | INT rounds the supplied number down to the nearest integer. | `FormulaFunctions/IDH_INT.htm` |
| `INTERCEPT` | INTERCEPT calculates the value at which the linear regression line based on known_y's and known_x's intersects the y-axis. If known_y's and known_x's are empty or have a different number of data points, INTERCEPT returns the #N/A error value. | `FormulaFunctions/IDH_INTERCEPT.htm` |
| `ISBLANK` | ISBLANK determines if the specified cell is blank. | `FormulaFunctions/IDH_ISBLANK.htm` |
| `ISERR` | ISERR determines if the specified expression returns an error value. | `FormulaFunctions/IDH_ISERR.htm` |
| `ISERROR` | ISERROR determines if the specified expression returns an error value. | `FormulaFunctions/IDH_ISERROR.htm` |
| `ISLOGICAL` | ISLOGICAL determines if the specified expression returns a logical value. | `FormulaFunctions/IDH_ISLOGICAL.htm` |
| `ISNA` | ISNA determines if the specified expression returns the "value not available" error. | `FormulaFunctions/IDH_ISNA.htm` |
| `ISNONTEXT` | ISNONTEXT determines if the specified expression is not text. | `FormulaFunctions/IDH_ISNONTEXT.htm` |
| `ISNUMBER` | ISNUMBER determines if the specified expression is a number. | `FormulaFunctions/IDH_ISNUMBER.htm` |
| `ISREF` | ISREF determines if the specified expression is a range reference. | `FormulaFunctions/IDH_ISREF.htm` |
| `ISTEXT` | ISTEXT determines if the specified expression is text. | `FormulaFunctions/IDH_ISTEXT.htm` |
| `LEFT` | LEFT returns the leftmost characters from the specified text string. | `FormulaFunctions/IDH_LEFT.htm` |
| `LEFTB` | LEFTB returns the leftmost byte from the specified text string. | `FormulaFunctions/IDH_LEFTB.htm` |
| `LEN` | LEN returns the number of characters in the supplied text string. | `FormulaFunctions/IDH_LEN.htm` |
| `LENB` | LENB returns the number of bytes in the supplied text string. | `FormulaFunctions/IDH_LENB.htm` |
| `LN` | LN returns the natural logarithm (based on the constant e) of a number. | `FormulaFunctions/IDH_LN.htm` |
| `LOG` | LOG returns the logarithm of a number to the specified base. | `FormulaFunctions/IDH_LOG.htm` |
| `LOG10` | LGO10 returns the base-10 logarithm of a number. | `FormulaFunctions/IDH_LOG10.htm` |
| `LOOKUP` | LOOKUP searches for a value in one range and returns the contents of the corresponding position in a second range. Use the function when you have a large list of values to look up or when the values may change over time. | `FormulaFunctions/IDH_LOOKUP.htm` |
| `LOWER` | LOWER changes the characters in the specified string to lowercase characters. Numeric characters in the string are not changed. | `FormulaFunctions/IDH_LOWER.htm` |
| `MATCH` | A specified value is compared against values in a range. The position of the matching value in the search range is returned. | `FormulaFunctions/IDH_MATCH.htm` |
| `MAX` | MAX returns the largest value in the specified list of numbers. | `FormulaFunctions/IDH_MAX.htm` |
| `MID` | MID returns the specified number of characters from a text string, beginning with the specified starting position. | `FormulaFunctions/IDH_MID.htm` |
| `MIDB` | MIDB returns the specified number of bytes from a text string, beginning with the specified starting position. | `FormulaFunctions/IDH_MIDB.htm` |
| `MIN` | MIN returns the smallest value in the specified list of numbers. | `FormulaFunctions/IDH_MIN.htm` |
| `MINUTE` | MINUTE returns the minute that corresponds to the supplied date. | `FormulaFunctions/IDH_MINUTE.htm` |
| `MOD` | MOD returns the remainder after dividing a number by a specified divisor. | `FormulaFunctions/IDH_MOD.htm` |
| `MONTH` | MONTH returns the month that corresponds to the supplied date. | `FormulaFunctions/IDH_MONTH.htm` |
| `N` | N tests the supplied value and returns the value if it is a number. | `FormulaFunctions/IDH_N.htm` |
| `NA` | NA returns the error value #N/A, which represents not available. | `FormulaFunctions/IDH_NA.htm` |
| `NOT` | NOT returns a logical value that is the opposite of its value. | `FormulaFunctions/IDH_NOT.htm` |
| `NOW` | NOW returns the current date and time as a serial number. | `FormulaFunctions/IDH_NOW.htm` |
| `ODD` | ODD rounds the specified number up to the nearest odd integer. | `FormulaFunctions/IDH_ODD.htm` |
| `OFFSET` | OFFSET returns the contents of a range that is offset from a starting point in the spreadsheet. | `FormulaFunctions/IDH_OFFSET.htm` |
| `OR` | OR returns True if at least one of a series of logical arguments is true. | `FormulaFunctions/IDH_OR.htm` |
| `PI` | PI returns the value of pi (p), which is approximately 3.14159265358979 when calculated to 15 significant digits. | `FormulaFunctions/IDH_PI.htm` |
| `PRODUCT` | PRODUCT multiplies a list of numbers and returns the result. | `FormulaFunctions/IDH_PRODUCT.htm` |
| `PROPER` | PROPER returns the specified string in proper-case format. | `FormulaFunctions/IDH_PROPER.htm` |
| `RAND` | RAND returns a number selected randomly from a uniform distribution greater than or equal to 0 and less than 1. | `FormulaFunctions/IDH_RAND.htm` |
| `REPLACE` | REPLACE replaces part of a text string with another text string. | `FormulaFunctions/IDH_REPLACE.htm` |
| `REPLACEB` | REPLACEB replaces part of a text string with another text string. | `FormulaFunctions/IDH_REPLACEB.htm` |
| `REPT` | REPT repeats a text string the specified number of times. | `FormulaFunctions/IDH_REPT.htm` |
| `RIGHT` | RIGHT returns the rightmost characters from the given text string. | `FormulaFunctions/IDH_RIGHT.htm` |
| `RIGHTB` | RIGHTB returns the rightmost bytes from the given text string. | `FormulaFunctions/IDH_RIGHTB.htm` |
| `ROUND` | ROUND rounds the given number to the supplied number of decimal places. | `FormulaFunctions/IDH_ROUND.htm` |
| `ROUNDDOWN` | ROUNDDOWN rounds a number down. | `FormulaFunctions/IDH_ROUNDDOWN.htm` |
| `ROUNDUP` | ROUNDUP rounds the given number up to the supplied number of decimal places. | `FormulaFunctions/IDH_ROUNDUP.htm` |
| `ROW` | ROW returns the row number of the supplied reference. | `FormulaFunctions/IDH_ROW.htm` |
| `ROWS` | ROW returns the number of rows in a range reference. | `FormulaFunctions/IDH_ROWS.htm` |
| `SEARCH` | SEARCH locates the position of the first character of a specified text string within another text string. | `FormulaFunctions/IDH_SEARCH.htm` |
| `SEARCHB` | SERACHB locates the position of the first byte of a specified text string within another text string. | `FormulaFunctions/IDH_SEARCHB.htm` |
| `SECOND` | SECOND returns the second that corresponds to the supplied date. | `FormulaFunctions/IDH_SECOND.htm` |
| `SIGN` | SIGN determines the sign of the specified number. | `FormulaFunctions/IDH_SIGN.htm` |
| `SIN` | SIN returns the sine of the supplied angle. | `FormulaFunctions/IDH_SIN.htm` |
| `SINH` | SINH returns the hyperbolic sine of the specified number. | `FormulaFunctions/IDH_SINH.htm` |
| `SLOPE` | SLOPE returns the slope of the linear regression line through data points in known_y's and known_x's. The slope is the vertical distance divided by the horizontal distance between any two points on the line, which is the rate of change along the regression line. | `FormulaFunctions/IDH_SLOPE.htm` |
| `SQRT` | SQRT returns the square root of the specified number. | `FormulaFunctions/IDH_SQRT.htm` |
| `STDEV` | STDEV estimates the standard deviation based on a random sample. The standard deviation is a measure for the deviation from the average value (the mean). | `FormulaFunctions/IDH_STDEV.htm` |
| `STDEVP` | STDEVP returns the standard deviation based on the entire population of values. The standard deviation is a measure for the deviation from the average value (the mean). | `FormulaFunctions/IDH_STDEVP.htm` |
| `SUBSTITUTE` | SUBSTITUTE replaces a specified part of a text string with another text string. | `FormulaFunctions/IDH_SUBSTITUTE.htm` |
| `SUM` | SUM returns the sum of the supplied numbers. | `FormulaFunctions/IDH_SUM.htm` |
| `SUMIF` | SUMIF returns the sum of the specified cells based on the given criteria. | `FormulaFunctions/IDH_SUMIF.htm` |
| `SUMSQ` | SUMSQ squares each of the supplied numbers and returns the sum of the squares. | `FormulaFunctions/IDH_SUMSQ.htm` |
| `T` | T tests the supplied value and returns the value if it is text. | `FormulaFunctions/IDH_T.htm` |
| `TAN` | TAN returns the tangent of the specified angle. | `FormulaFunctions/IDH_TAN.htm` |
| `TANH` | TANH returns the hyperbolic tangent of a number. | `FormulaFunctions/IDH_TANH.htm` |
| `TEXT` | TEXT returns the given number as text, using the specified formatting. | `FormulaFunctions/IDH_TEXT.htm` |
| `TIME` | TIME returns a serial number for the supplied time. | `FormulaFunctions/IDH_TIME.htm` |
| `TIMEVALUE` | TIMEVALUE returns a serial number for the supplied text representation of time. | `FormulaFunctions/IDH_TIMEVALUE.htm` |
| `TODAY` | TODAY returns the current date as a serial number. | `FormulaFunctions/IDH_TODAY.htm` |
| `TRIM` | TRIM removes all spaces from text except single spaces between words. | `FormulaFunctions/IDH_TRIM.htm` |
| `TRUE` | TRUE returns the logical value True. This function always requires the trailing parentheses. | `FormulaFunctions/IDH_TRUE.htm` |
| `TRUNC` | TRUNC truncates the given number to an integer. | `FormulaFunctions/IDH_TRUNC.htm` |
| `TYPE` | TYPE returns the argument type of the given expression. | `FormulaFunctions/IDH_TYPE.htm` |
| `UPPER` | UPPER changes the characters in the specified string to uppercase characters. | `FormulaFunctions/IDH_UPPER.htm` |
| `VALUE` | VALUE returns the specified text as a number. | `FormulaFunctions/IDH_VALUE.htm` |
| `VAR` | VAR returns the variance of a population based on a sample of values. | `FormulaFunctions/IDH_VAR.htm` |
| `VARP` | VARP returns the variance of a population based on an entire population of values. | `FormulaFunctions/IDH_VARP.htm` |
| `VLOOKUP` | VLOOKUP searches the first column of a table for a value and returns the contents of a cell in that table that corresponds to the location of the search value. | `FormulaFunctions/IDH_VLOOKUP.htm` |
| `WEEKDAY` | WEEKDAY returns the day of the week that corresponds to the supplied date. | `FormulaFunctions/IDH_WEEKDAY.htm` |
| `YEAR` | YEAR returns the year that corresponds to the supplied date. | `FormulaFunctions/IDH_YEAR.htm` |

### Peak

**Official Help topics:** 120

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Peak Calibration Category | The Peak Calibration category includes variables that provide information about calibration values and settings. The following table lists the variables in the Peak Calibration category. Click a variable name to read the full description. | `ReportVariables_CSH/RepVar_Peak_Calibration.htm` |
| Calibration Coefficient | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Calibration_calCoefficient.htm` |
| Calibration Type | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Calibration_calibration_type.htm` |
| Weights | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Calibration_calibration_weight.htm` |
| Calibration Mode | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Calibration_calMode.htm` |
| Residual of Calibration Point X | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Calibration_calPointDist.htm` |
| Evaluation of Calibration Function for x | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Calibration_calPointFX.htm` |
| Calibration Point Status | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Calibration_calPointStatus.htm` |
| Calibration Point Weight | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Calibration_calPointWeight.htm` |
| Calibration Point X/Y | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Calibration_calPointX.htm` |
| Calibration Point: X Unit | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Calibration_calPointXUnit.htm` |
| Calibration Point: Y Unit | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Calibration_calPointYUnit.htm` |
| Lower/Upper Confidence Limit | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Calibration_confUpperLimit.htm` |
| Correlation Coefficient (Linear) | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Calibration_correlation_coefficient.htm` |
| Hubaux-Vos Limit of Detection | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Calibration_hvlod.htm` |
| Number of Disabled Calibration Points | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Calibration_nCalDisabled.htm` |
| Number of Calibration Points | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Calibration_nCalpoints.htm` |
| Lower/Upper Prediction Limit | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Calibration_predUpperLimit.htm` |
| Reference Inject Volume | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Calibration_reference_inject_volume.htm` |
| Relative Standard Deviation | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Calibration_rel_standard_deviation.htm` |
| Relative Standard Error | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Calibration_rel_standard_error.htm` |
| RF Value (Amount/Area) | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Calibration_rf_value.htm` |
| Coefficient of Determination | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Calibration_rQuadrat.htm` |
| DOF-Adjusted Coefficient of Determination | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Calibration_rQuadratAdj.htm` |
| Standard Deviation | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Calibration_standard_deviation.htm` |
| Variance | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Calibration_variance.htm` |
| Variance Coefficient | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Calibration_variance_coefficient.htm` |
| Peak Purity and Identification Category | The Peak Purity and Identification category includes variables that provide information about the comparison of peak spectra with reference spectra. These variables will work only if a 3D field is available for the current injection. The following table lists the available variables in the Peak Purity and Identification category. Click a variable name to rea | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification.htm` |
| Amount Difference | Peak Purity and Identification Variables | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_amountDifference.htm` |
| Peak Apex Alignment Within Charge State | Peak Purity and Identification / Peptide Variables | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_apexStdDevWithinChargeState.htm` |
| Peak Apex Alignment Within Charge State And Isotope | Peak Purity and Identification / Peptide Variables | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_apexStdDevWithinChargeStateAndIstope.htm` |
| Peak Apex Alignment Within Isotope | Peak Purity and Identification / Peptide Variables | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_apexStdDevWithInIsotope.htm` |
| Composite Score | Peak Purity and Identification / Peptide Variables | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_compScore.htm` |
| Confirmation Chromatogram | Peak Purity and Identification Variable | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_confirmationChm.htm` |
| Confirmation Peak | Peak Purity and Identification Variable | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_confirmationPeak.htm` |
| Peak Confirmation Ratio | Peak Purity and Identification Variable | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_confirmationRatio.htm` |
| Peak Confirmation Result | Peak Purity and Identification Variable | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_confirmationResult.htm` |
| Fluorescence Spectrum | Peak Purity and Identification Variable | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_flSpectrum.htm` |
| MSLS Hit | Peak Purity and Identification Variable | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_hitMassSpec.htm` |
| SLS Hit | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_hitSpec.htm` |
| Confirmation peak excluded? | Peak Purity and Identification Variable | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_isExcluded.htm` |
| Isotopic Dot Product | Peak Purity and Identification / Peptide Variables | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_isoDotProduct.htm` |
| ISTD Chromatogram | Peak Purity and Identification Variable | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_istdChm.htm` |
| ISTD Peak | Peak Purity and Identification Variable | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_istdPeak.htm` |
| Mass Accuracy | Peak Purity and Identification / Peptide Variables | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_massAccuracy.htm` |
| Mass Accuracy Mass | Peak Purity and Identification Variables | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_massAccuracyMass.htm` |
| Peak Mass Spectrum Parameters | Peak Purity and Identification Variable | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_massSpectrum.htm` |
| Peak Purity Match | Peak Purity and Identification Variable | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_match.htm` |
| Number of MSLS Hit | Peak Purity and Identification Variable | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_nMSlsHits.htm` |
| Number of SLS Hits | Peak Purity and Identification Variable | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_nSlsHits.htm` |
| Peak Apex Alignment | Peak Purity and Identification Variable/Peptide Variable | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_peakApexStdDev.htm` |
| Peak Purity Index | Peak Purity and Identification Variable | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_ppi.htm` |
| Peak Ratio Mean Value | Peak Purity and Identification Variable | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_ratio.htm` |
| Reference Spectrum Match | Peak Purity and Identification Variable | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_refMatch.htm` |
| Reference Mass Spectrum Match | Peak Purity and Identification Variable | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_refMsMatch.htm` |
| RSD Peak Purity Match | Peak Purity and Identification Variable | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_rsd_match.htm` |
| RSD Peak Purity Index | Peak Purity and Identification Variable | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_rsd_ppi.htm` |
| RSD Peak Ratio | Peak Purity and Identification Variable | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_rsd_ratio.htm` |
| Peak UV Spectrum | Peak Purity and Identification Variable | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_spectrum.htm` |
| Summed Charge State Confirming Peak Area | Peak Purity and Identification Variable | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_summedChargeStateConfirmingPeakArea.htm` |
| Summed Confirming Peak Area | Peak Purity and Identification Variable | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_summedConfirmingPeakArea.htm` |
| Peak Results Category | The following table lists the available variables in the Peak Results category. Click a variable name to read the full description. | `ReportVariables_CSH/RepVar_Peak_Results.htm` |
| Amount | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_amount.htm` |
| Amount Deviation | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_amount_deviation.htm` |
| Area | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_area.htm` |
| Manually Assigned | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_assigned.htm` |
| Asymmetry | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_asymmetry.htm` |
| Capillary Electrophoresis Area (CE Area) | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_ceArea.htm` |
| Concentration | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_concentration.htm` |
| Group | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_group.htm` |
| Group Amount | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_groupAmount.htm` |
| Group Area | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_groupArea.htm` |
| Group Height | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_groupHeight.htm` |
| K' (Capacity Factor) | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_kValue.htm` |
| Level Check | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_level_check.htm` |
| Level Tolerance High Amount | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_level_tolerance_high_amount.htm` |
| Level Tolerance High Response | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_level_tolerance_high_response.htm` |
| Level Tolerance Low Amount | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_level_tolerance_low_amount.htm` |
| Level Tolerance Low Response | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_level_tolerance_low_response.htm` |
| Manipulated? | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_modified.htm` |
| Statistical Moments | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_moment.htm` |
| Name | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_name.htm` |
| Number | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_number.htm` |
| Peak to Valley Ratio | In the Report Table, double-click a column header. | `ReportVariables_CSH/RepVar_Peak_Results_peakToValleyRatio.htm` |
| Rank | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_rank.htm` |
| Relative Amount/Area/CE Area/Height | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_rel_amount.htm` |
| Relative Retention Time | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_rel_retention_time.htm` |
| Resolution | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_resolution.htm` |
| Retention Deviation | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_retention_deviation.htm` |
| Retention Time | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_retention_time.htm` |
| Retention Window Width | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_retention_window.htm` |
| Retention Index | In the Report Table, double-click a column header. | `ReportVariables_CSH/RepVar_Peak_Results_ri.htm` |
| Baseline/Signal Value at Peak Retention | In the Report Table, double-click a column header. | `ReportVariables_CSH/RepVar_Peak_Results_sig_value_baseline.htm` |
| Skewness | In the Report Table, double-click a column header. | `ReportVariables_CSH/RepVar_Peak_Results_skewness.htm` |
| Signal-to-Noise Ratio | In the Report Table, double-click a column header. | `ReportVariables_CSH/RepVar_Peak_Results_sn.htm` |
| Detection Code at Peak Start or Peak End (AIA Peak Type) | In the Report Table, double-click a column header. | `ReportVariables_CSH/RepVar_Peak_Results_start_detection_code.htm` |
| Peak Start/Stop Time | In the Report Table, double-click a column header. | `ReportVariables_CSH/RepVar_Peak_Results_start_time.htm` |
| Baseline/Signal Value at Peak Start/End | In the Report Table, double-click a column header. | `ReportVariables_CSH/RepVar_Peak_Results_start_value_baseline.htm` |
| Theoretical Plates | In the Report Table, double-click a column header. | `ReportVariables_CSH/RepVar_Peak_Results_theoretical_plates.htm` |
| Type | In the Report Table, double-click a column header. | `ReportVariables_CSH/RepVar_Peak_Results_type.htm` |
| Width/Left Width/Right Width | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_width.htm` |
| Signal to Noise Ratio | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_Peak_SN.htm` |
| SN Intermediate Results | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_Peak_SNIntermediate.htm` |
| Noise Value | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_Peak_SNIntermediate_noise.htm` |
| Noise End Time | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_Peak_SNIntermediate_noise_end_time.htm` |
| Noise Start Time | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_Peak_SNIntermediate_noise_start_time.htm` |
| Noise Regression Offset | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_Peak_SNIntermediate_offset.htm` |
| Ratio | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_Peak_SNIntermediate_ratio.htm` |
| Signal Value | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_Peak_SNIntermediate_signal.htm` |
| Noise Regression Slope | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_Peak_SNIntermediate_slope.htm` |
| Number of Noise Points | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_Peak_SNIntermediatenum_noise_points.htm` |
| CAS Number | Peak Tentative Identification Variable | `ReportVariables_CSH/RepVar_Peak_Tentative_ID_CAS_Number.htm` |
| Peak Tentative Identification Category | The following table lists the available variables in the Peak Tentative Identification category, which is a sub-category of the Peak Purity and Identification category. Click a variable name to read the full description. | `ReportVariables_CSH/RepVar_Peak_TentativeID.htm` |
| Amount | Peak Tentative Identification Variable | `ReportVariables_CSH/RepVar_Peak_TentativeID_Amount.htm` |
| Internal Standard Name | Peak Tentative Identification Variable | `ReportVariables_CSH/RepVar_Peak_TentativeID_ISTD.htm` |
| Library Name | Peak Tentative Identification Variable | `ReportVariables_CSH/RepVar_Peak_TentativeID_LibName.htm` |
| Match | Peak Tentative Identification Variable | `ReportVariables_CSH/RepVar_Peak_TentativeID_Match.htm` |
| Name | Peak Tentative Identification Variable | `ReportVariables_CSH/RepVar_Peak_TentativeID_Name.htm` |
| Probability | Peak Tentative Identification Variable | `ReportVariables_CSH/RepVar_Peak_TentativeID_Probability.htm` |
| Reverse Match | Peak Tentative Identification Variable | `ReportVariables_CSH/RepVar_Peak_TentativeID_ReverseMatch.htm` |

### DetectionParameter

**Official Help topics:** 46

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Detection Parameters | The Detection Parameters category includes variables that give information about the value set in the processing method for the related detection parameter at a defined retention time (detection parameters can be set on the Detection tab page in the Processing Method Editor). A variable will only be listed if it is a variable of the detection algorithm set i | `ReportVariables_CSH/RepVar_DetectionParameter.htm` |
| Bunch Size (Atlas) | Detection / MS Detection Parameters Variable | `ReportVariables_CSH/RepVar_DetectionParameter_atlasBunchSize.htm` |
| End Threshold (Atlas) | Detection / MS Detection Parameters Variable | `ReportVariables_CSH/RepVar_DetectionParameter_atlasEndThreshold.htm` |
| End Trend (Atlas) | Detection / MS Detection Parameters Variable | `ReportVariables_CSH/RepVar_DetectionParameter_atlasEndTrend.htm` |
| Force Baseline (Atlas) | Detection / MS Detection Parameters Variable | `ReportVariables_CSH/RepVar_DetectionParameter_atlasForceBase.htm` |
| Shoulder Sensitivity (Atlas) | Detection / MS Detection Parameters Variable | `ReportVariables_CSH/RepVar_DetectionParameter_atlasShoulder.htm` |
| Skim Sensitivity (Atlas) | Detection / MS Detection Parameters Variable | `ReportVariables_CSH/RepVar_DetectionParameter_atlasSkimSens.htm` |
| Start Threshold (Atlas) | Detection / MS Detection Parameters Variable | `ReportVariables_CSH/RepVar_DetectionParameter_atlasStartThreshold.htm` |
| Start Trend (Atlas) | Detection / MS Detection Parameters Variable | `ReportVariables_CSH/RepVar_DetectionParameter_atlasStartTrend.htm` |
| Suppress (Atlas) | Detection / MS Detection Parameters Variable | `ReportVariables_CSH/RepVar_DetectionParameter_atlasSuppress.htm` |
| Threshold (Atlas) | Detection / MS Detection Parameters Variable | `ReportVariables_CSH/RepVar_DetectionParameter_atlasThreshold.htm` |
| Baseline Noise Auto Range | (MS) Detection Parameter Variable | `ReportVariables_CSH/RepVar_DetectionParameter_baselineNoiseAutoRange.htm` |
| Baseline Noise Start/End Time | (MS) Detection Parameter Variable | `ReportVariables_CSH/RepVar_DetectionParameter_baselineStartTime.htm` |
| Baseline Type | Detection Parameter Variable | `ReportVariables_CSH/RepVar_DetectionParameter_baselineType.htm` |
| Consider Void Peak | (MS) Detection Parameter Variable | `ReportVariables_CSH/RepVar_DetectionParameter_considerVoidPeak.htm` |
| Detect Shoulder Peaks | Detection Parameter Variable | `ReportVariables_CSH/RepVar_DetectionParameter_detShoulderPeaks.htm` |
| Peak Slice | (MS) Detection Parameters Variable | `ReportVariables_CSH/RepVar_DetectionParameter_filter.htm` |
| Fronting Sensitivity Factor | (MS) Detection Parameter Variable | `ReportVariables_CSH/RepVar_DetectionParameter_frontFac.htm` |
| Front Riders to Main Peak | (MS) Detection Parameters Variable | `ReportVariables_CSH/RepVar_DetectionParameter_frontRiderToMain.htm` |
| Has a Fixed Baseline? | (MS) Detection Parameters Variable | `ReportVariables_CSH/RepVar_DetectionParameter_hasFixedBaseline.htm` |
| Part of Peak Group? | (MS) Detection Parameters Variable | `ReportVariables_CSH/RepVar_DetectionParameter_isInGruop.htm` |
| Lock Baseline | (MS) Detection Parameters Variable | `ReportVariables_CSH/RepVar_DetectionParameter_lockBl.htm` |
| Maximum Area Reject | (MS) Detection Parameters Variable | `ReportVariables_CSH/RepVar_DetectionParameter_maxAreaRj.htm` |
| Maximum Height Reject | (MS) Detection Parameters Variable | `ReportVariables_CSH/RepVar_DetectionParameter_maxHeightRj.htm` |
| Maximum Width | (MS) Detection Parameters Variable | `ReportVariables_CSH/RepVar_DetectionParameter_maxWidth.htm` |
| Minimum Area | Detection / MS Detection Parameters Variable | `ReportVariables_CSH/RepVar_DetectionParameter_minArea.htm` |
| Minimum Baseline Box Width | Detection Parameter Variable | `ReportVariables_CSH/RepVar_DetectionParameter_minBaselineBoxWidth.htm` |
| Minimum Height | Detection / MS Detection Parameters Variable | `ReportVariables_CSH/RepVar_DetectionParameter_minHeight.htm` |
| Minimum Relative Area | Detection Parameter Variable | `ReportVariables_CSH/RepVar_DetectionParameter_minRelativeArea.htm` |
| Minimum Relative Height | Detection Parameter Variable | `ReportVariables_CSH/RepVar_DetectionParameter_minRelativeHeight.htm` |
| Minimum Rider Ratio | Detection Parameter Variable | `ReportVariables_CSH/RepVar_DetectionParameter_minRiderRatio.htm` |
| Minimum Signal To Noise Ratio | Detection Parameter Variable | `ReportVariables_CSH/RepVar_DetectionParameter_minSignalNoiseRatio.htm` |
| Minimum Width | Detection / MS Detection Parameters Variable | `ReportVariables_CSH/RepVar_DetectionParameter_minWidth.htm` |
| Detect Negative Peaks | Detection / MS Detection Parameters Variable | `ReportVariables_CSH/RepVar_DetectionParameter_negDetect.htm` |
| Inhibit Integration | (MS) Detection Parameters Variable | `ReportVariables_CSH/RepVar_DetectionParameter_noInteg.htm` |
| Sensitivity | (MS) Detection Parameter Variable | `ReportVariables_CSH/RepVar_DetectionParameter_noise.htm` |
| Rider Detection | (MS) Detection Parameter Variable | `ReportVariables_CSH/RepVar_DetectionParameter_riderDetection.htm` |
| Rider Threshold | Detection Parameter Variable | `ReportVariables_CSH/RepVar_DetectionParameter_riderMin.htm` |
| Maximum Rider Ratio | (MS) Detection Parameters Variable | `ReportVariables_CSH/RepVar_DetectionParameter_riderRatio.htm` |
| Rider Skimming | (MS) Detection Parameter Variable | `ReportVariables_CSH/RepVar_DetectionParameter_riderSkim.htm` |
| Peak Shoulder Threshold | Detection Parameters Variable | `ReportVariables_CSH/RepVar_DetectionParameter_shoulderThrshld.htm` |
| Cobra Smoothing Width | (MS) Detection Parameter Variable | `ReportVariables_CSH/RepVar_DetectionParameter_smoothingWidth.htm` |
| Snap Baseline | Detection Parameter Variable | `ReportVariables_CSH/RepVar_DetectionParameter_snapBaseline.htm` |
| Tailing Sensitivity Factor | MS Detection Parameter Variable | `ReportVariables_CSH/RepVar_DetectionParameter_tailFac.htm` |
| Valley to Valley | (MS) Detection Parameter Variable | `ReportVariables_CSH/RepVar_DetectionParameter_valval.htm` |
| Void Volume Treatment | (MS) Detection Parameter Variable | `ReportVariables_CSH/RepVar_DetectionParameter_voidVolumeTreatment.htm` |

### Component

**Official Help topics:** 45

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Component Category | The Component category includes variables that provide information about the values in the component table of the processing method. The following table lists the available variables in the Component category. Click a variable name to read the full description. | `ReportVariables_CSH/RepVar_Component.htm` |
| Amount | Component/Peak Group Variable | `ReportVariables_CSH/RepVar_Component_amount.htm` |
| Concentration Unit | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Component_amount_unit.htm` |
| Manual C0/C1/C2/C3 | Component/Peak Group Variable | `ReportVariables_CSH/RepVar_Component_C0.htm` |
| Calculated Mass | Injection Variable/Component Variable | `ReportVariables_CSH/RepVar_Component_calculated_mass.htm` |
| Calibration Type | Component/Peak Group Variable | `ReportVariables_CSH/RepVar_Component_calibration_type.htm` |
| CAS ID | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Component_casNumber.htm` |
| Channel | Component/Peak Group Variable | `ReportVariables_CSH/RepVar_Component_channel.htm` |
| Charge | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Component_charge.htm` |
| Chemical Formula | Component Variable/Peptide Variable | `ReportVariables_CSH/RepVar_Component_chemFormula.htm` |
| Comment | Component/Peak Group Variable | `ReportVariables_CSH/RepVar_Component_comment.htm` |
| Lower/Upper Confidence Probability | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Component_confLowerProbability.htm` |
| Group | Component/Peak Group Variable | `ReportVariables_CSH/RepVar_Component_group.htm` |
| Group Type | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Component_grouptype.htm` |
| Include Identified Peak | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Component_includeidentifiedpeak.htm` |
| Individual MS Detection Parameters | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Component_indvMsDet.htm` |
| Evaluation Type | Component/Peak Group Variable | `ReportVariables_CSH/RepVar_Component_integration_type.htm` |
| Left Limit/Right Limit | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Component_left_limit.htm` |
| Level Tolerance | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Component_level_tolerance.htm` |
| Level Tolerance High Amount | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Component_level_tolerance_high_amount.htm` |
| Level Tolerance Low Amount | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Component_level_tolerance_low_amount.htm` |
| Molecular Mass | Component Variable/Peptide Variable | `ReportVariables_CSH/RepVar_Component_massToChargeRatio.htm` |
| Mass Tolerance | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Component_massTolerance.htm` |
| MS Detection Parameters | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Component_MsDetectionParameters.htm` |
| MS Extraction Parameters | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Component_msExt.htm` |
| Name | Component Variable/Peak Group Variable/Peptide Variable | `ReportVariables_CSH/RepVar_Component_name.htm` |
| Number | Component/Peak Group Variable | `ReportVariables_CSH/RepVar_Component_number.htm` |
| Peptide Group | Component Variable/Peptide Variable | `ReportVariables_CSH/RepVar_Component_peptideGroup.htm` |
| Reference Spectrum | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Component_reference_spectrum.htm` |
| Reference Mass Spectrum Settings | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Component_RefMsSettings.htm` |
| Factor | Component/Peak Group Variable | `ReportVariables_CSH/RepVar_Component_response_factor.htm` |
| Retention Time | Component Variable/Peptide Variable | `ReportVariables_CSH/RepVar_Component_retention_time.htm` |
| Retention Time Interpretation | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Component_retention_type.htm` |
| Retention Index | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Component_ri.htm` |
| Check Extrema | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Component_spec_check_extrema.htm` |
| Match Criterion | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Component_spec_compare_method.htm` |
| Spectrum Derivative | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Component_spec_derivative.htm` |
| Minimum/Maximum Wavelength | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Component_spec_max_wavelength.htm` |
| Relative Maximum Deviation | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Component_spec_relmaxdev.htm` |
| Threshold | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Component_spec_threshold.htm` |
| Standard Method | Component/Peak Group Variable | `ReportVariables_CSH/RepVar_Component_standard_method.htm` |
| Peak Type | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Component_type.htm` |
| Previous Retention | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Component_use_previous_rettime.htm` |
| Window/(Component) Identification | Component Variable/Peptide Variable | `ReportVariables_CSH/RepVar_Component_window.htm` |
| XIC Detection Reference Rule | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Component_xicdetectionreferencerule.htm` |

### ProcessingMethod

**Official Help topics:** 45

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Processing Method Category | The Processing Method category includes variables that provide information about settings selected in the Processing Method . The following table lists the variables available in the Processing Method category. Click a variable name to read the full description. | `ReportVariables_CSH/RepVar_ProcessingMethod.htm` |
| Available Algorithm Version | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_availAlgVer.htm` |
| Blank Run Injection Record | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_blankRunInjection.htm` |
| Subtraction Mode | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_blankRunSubtraction.htm` |
| Calibration Level Name | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_calLevelName.htm` |
| Calibration Mode | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_calMode.htm` |
| Comment | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_comment.htm` |
| Creation Operator | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_creation_operator.htm` |
| Creation Date & Time | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_creation_time.htm` |
| Curve Fitting | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_curveFitting.htm` |
| Data Vault | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_dataVault.htm` |
| Dead Time | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_deadTime.htm` |
| Delay Time | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_delayTime.htm` |
| Delay Time Detector | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_delayTimeDetector.htm` |
| Detection Algorithm | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_detAlgorithm.htm` |
| Directory | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_directory.htm` |
| Effective Algorithm Version | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_effAlgVer.htm` |
| Origin of Fixed Calibration Standards | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_fixedCalibrationStandardsOrigin.htm` |
| Last Fixed Calibration Update Operator | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_FixedCalibrationUpdateOperator.htm` |
| Last Fixed Calibration Update Date & Time | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_FixedCalibrationUpdateTime.htm` |
| Is Latest Algorithm Version | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_isLatestAlgVer.htm` |
| Matrix Correction Enabled | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_matrixCorrection.htm` |
| MS Library Screening Parameters | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_msls.htm` |
| MS Settings | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_MsSettings.htm` |
| Name | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_name.htm` |
| Number of Calibration Levels | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_numOfCalLevels.htm` |
| Number of Components | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_numOfComponents.htm` |
| Number of Detection Parameters | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_numOfDetParams.htm` |
| Number of Peak Groups | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_numOfPeakGroups.htm` |
| Select Peak Group | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_PeakGroup.htm` |
| Peak Width Determination | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_peakWidthDetermination.htm` |
| MS Detection Algorithm | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_procMeth.msDetAlgorithm.htm` |
| Reference Inject Volume | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_referenceInjectVolume.htm` |
| Retention Time Determination | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_retTimeDetermination.htm` |
| Select Component in the Component Table | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_selectComponent.htm` |
| Separate Calibration | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_sepCalibration.htm` |
| Parent Sequence Name | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_seqName.htm` |
| Parent Sequence Header Record | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_sequence.htm` |
| Spectra Library Screening Parameters | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_sls.htm` |
| Number of Test Cases | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_sst_rows.htm` |
| Select Test Case | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_sst_tc.htm` |
| Last Update Operator | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_update_operator.htm` |
| Last Update Date & Time | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_update_time.htm` |
| Use Amount Ratio for Var. ISTD | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_useAmountRatioForVarIstd.htm` |
| UV Spectra Settings | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_uv_settings.htm` |

### Sequence

**Official Help topics:** 43

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Sequence Category | The Sequence category includes variables that give information about the sequence. The following table lists the available variables in the Sequence category. Click a variable name to read the full description. | `ReportVariables_CSH/RepVar_Sequence.htm` |
| Add To Queue Operator | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_addToQueue_Operator.htm` |
| Approve Comment | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_approveComment.htm` |
| Approve Operator | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_approveOperator.htm` |
| Approve Date & Time | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_approveTime.htm` |
| Comment | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_comment.htm` |
| Created by Qualification | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_createdByQualification.htm` |
| Creation Operator | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_creation_operator.htm` |
| Creation Date & Time | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_creation_time.htm` |
| Data Vault | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_dataVault.htm` |
| Default Channel | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_defaultChannel.htm` |
| Default Report Template | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_defaultReportDefinition.htm` |
| Default View Settings | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_defaultViewSettings.htm` |
| Directory | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_directory.htm` |
| eWorkflow Name | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_eWorkflowName.htm` |
| Imported Data | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_imported.htm` |
| Displaying Imported Results | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_importedResults.htm` |
| Include Canceller | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_includeCanceller.htm` |
| Include Creator | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_includeCreator.htm` |
| Include Queue Starter | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_includeQueueStarter.htm` |
| Select Injection | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_injection.htm` |
| Instrument | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_instrument.htm` |
| Name | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_name.htm` |
| Number of Injections | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_nInjections.htm` |
| Notifications Enabled | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_notificationsEnabled.htm` |
| Notify Aborted Recipient | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_notifyAbortedRecipient.htm` |
| Notify Cancelled Recipient | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_notifyCancelledRecipient.htm` |
| Notify Finished Recipient | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_notifyFinishedRecipient.htm` |
| Notify Sequence Aborted | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_notifySequenceAborted.htm` |
| Notify Sequence Cancelled | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_notifySequenceCancelled.htm` |
| Notify Sequence Finished | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_notifySequenceFinished.htm` |
| NTMS New Peak Detection Algorithm | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_NTMSPeakDetectionAlgorithm.htm` |
| Peptide Display Mode | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_peptideDisplayMode.htm` |
| Review Comment | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_reviewComment.htm` |
| Review Operator | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_reviewOperator.htm` |
| Review Date & Time | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_reviewTime.htm` |
| Required Signature Steps | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_signatureSteps.htm` |
| Signature Status | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_signStatus.htm` |
| Submit Comment | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_submitComment.htm` |
| Submit Operator | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_submitOperator.htm` |
| Submit Date & Time | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_submitTime.htm` |
| Last Update Operator | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_update_operator.htm` |
| Last Update Date & Time | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_update_time.htm` |

### Chromatogram

**Official Help topics:** 40

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Chromatogram Category | The following table lists the available variables in the Chromatogram category. Click a variable name to read the full description. Some variables can only be used if the Cobra detection algorithm was selected. | `ReportVariables_CSH/RepVar_Chromatogram.htm` |
| Auto Noise | In the Chromeleon Studio, navigate into the Report Designer category. | `ReportVariables_CSH/RepVar_Chromatogram_autoNoise.htm` |
| Baseline Threshold | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_baselineThreshold.htm` |
| Channel | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_channel.htm` |
| Count Peaks if ... | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_countif.htm` |
| Curvature | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_curvature.htm` |
| Curvature Noise | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_curvatureNoise.htm` |
| Delay Time | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_delayTime.htm` |
| Detection Algorithm | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_detAlgorithm.htm` |
| Detection Reference XIC? | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_detectionreferencexic.htm` |
| Detector | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_detector.htm` |
| Signal Drift | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_drift.htm` |
| Effective Min. Peak Area | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_effMinArea.htm` |
| Effective Min. Peak Height | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_effMinHeight.htm` |
| Effective Smoothing Width | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_effSmoothingWidth.htm` |
| End Time (relative to Inject Time) | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_end_time.htm` |
| Fluorescence Spectrum | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_flSpectrum.htm` |
| Import Type | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_import_type.htm` |
| Modification Operator | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_manip_operator.htm` |
| Modification Time | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_manip_time.htm` |
| Manipulated? | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_manipulated.htm` |
| Mass Detected | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_mass_detected.htm` |
| Mass Spectrum Parameters | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_massSpectrum.htm` |
| Metadata | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_metadata.htm` |
| MS Signal Extraction Parameters | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_msExt.htm` |
| Signal Noise | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_noise.htm` |
| Noise Determination Range Start/End Time | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_noiseDetStart.htm` |
| Number of Peaks | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_npeaks.htm` |
| Select Peak | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_peak.htm` |
| Peak Threshold | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_peakThreshold.htm` |
| Sample Rate | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_sig_rate.htm` |
| Sample Step | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_sig_step.htm` |
| Signal Description | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_signalDesc.htm` |
| Signal Statistic | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_signalStatistic.htm` |
| Signal Unit | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_signalUnit.htm` |
| Signal Value | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_signalValue.htm` |
| Slope | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_slope.htm` |
| Start Time (relative to Inject Time) | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_start_time.htm` |
| Sum Peak Results if ... | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_sumif.htm` |
| UV Spectrum | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_uvSpectrum.htm` |

### Injection

**Official Help topics:** 35

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Injection Category | The Injection category includes variables that give information about the injection taken from the columns of the injection list. The following table lists the available variables in the Injection category. Click a variable name to read the full description. | `ReportVariables_CSH/RepVar_Injection.htm` |
| Adduct Masses | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_adduct_masses.htm` |
| Adducts | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_adducts.htm` |
| IntStd | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_amount.htm` |
| AutoDilution Ratio | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_autodilution_ratio.htm` |
| Level | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_calLevel.htm` |
| Chemical Formula and Adduct Masses | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_chemical_formula_and_adduct_masse.htm` |
| Chemical Formula and Adducts | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_chemical_formula_and_adducts).htm` |
| Select Chromatogram | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_chm.htm` |
| Comment | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_comment.htm` |
| Dilution Factor | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_dilution_factor.htm` |
| GUID | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_guid.htm` |
| ID | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_id.htm` |
| Volume | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_inject_volume.htm` |
| Level Check | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_level_check.htm` |
| Lock Status | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_lockStatus.htm` |
| Lock Version | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_lockVersion.htm` |
| Processing Method | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_method.htm` |
| Name | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_name.htm` |
| Number | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_number.htm` |
| Position | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_position.htm` |
| Instrument Method | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_program.htm` |
| Reference Retention Time Standard | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_Reference_Retention_Time_Standard.htm` |
| Relative Position | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_relativePosition.htm` |
| Replicate ID | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_replicate.htm` |
| Retention Time Standard Error | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_Retention_Time_Standard_Error.htm` |
| Retention Time Standard Status | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_Retention_Time_Standard_Status.htm` |
| Weight | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_sample_weight.htm` |
| Spike Group | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_spike_group.htm` |
| Number of Re-injections | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_sst_num_reinjects.htm` |
| Test Case Overall Result | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_sst_result .htm` |
| Test Case Specific Result | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_sst_tc_result.htm` |
| Status | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_status.htm` |
| Inject Time | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_time.htm` |
| Type | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_type.htm` |

### DataAuditTrail

**Official Help topics:** 18

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Data Audit Trail Category | The Data Audit Trail category includes variables that give information about the values in the Data Audit Trail Report table. The following table lists the available variables in the Data Audit Trail category. Click a variable name to read the full description. | `ReportVariables_CSH/RepVar_DataAuditTrail.htm` |
| Additional Information | Data Audit Trail Variables | `ReportVariables_CSH/RepVar_DataAuditTrail_additional_information.htm` |
| Comment | Data Audit Trail Variables | `ReportVariables_CSH/RepVar_DataAuditTrail_comment.htm` |
| Show Details | Data Audit Trail Variables | `ReportVariables_CSH/RepVar_DataAuditTrail_details.htm` |
| New Value (details sub-category) | Data Audit Trail Variables | `ReportVariables_CSH/RepVar_DataAuditTrail_details_newvalue.htm` |
| Number (details sub-category) | Data Audit Trail Variables | `ReportVariables_CSH/RepVar_DataAuditTrail_details_number.htm` |
| Object Path (details sub-category) | Data Audit Trail Variables | `ReportVariables_CSH/RepVar_DataAuditTrail_details_objectpath.htm` |
| Old Value (details sub-category) | Data Audit Trail Variables | `ReportVariables_CSH/RepVar_DataAuditTrail_details_oldvalue.htm` |
| Operation (details sub-category) | Data Audit Trail Variables | `ReportVariables_CSH/RepVar_DataAuditTrail_details_operation.htm` |
| Property (details sub-category) | Data Audit Trail Variables | `ReportVariables_CSH/RepVar_DataAuditTrail_details_property.htm` |
| Object Name | Data Audit Trail Variables | `ReportVariables_CSH/RepVar_DataAuditTrail_name.htm` |
| Number of Events | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_DataAuditTrail_numOfEvents.htm` |
| Operation | Data Audit Trail Variables | `ReportVariables_CSH/RepVar_DataAuditTrail_operation.htm` |
| Operator | Data Audit Trail Variables | `ReportVariables_CSH/RepVar_DataAuditTrail_operator.htm` |
| Select Event | Data Audit Trail Variables | `ReportVariables_CSH/RepVar_DataAuditTrail_SelectEvent.htm` |
| Date/Time | Data Audit Trail Variables | `ReportVariables_CSH/RepVar_DataAuditTrail_time.htm` |
| Type | Data Audit Trail Variables | `ReportVariables_CSH/RepVar_DataAuditTrail_type.htm` |
| Object Version | Data Audit Trail Variables | `ReportVariables_CSH/RepVar_DataAuditTrail_version.htm` |

### SSTDefinition

**Official Help topics:** 17

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Test Case Category | The Test Case category includes variables that give information about the conditions defined for a specific test case. The following table lists the available variables in this category. Click a variable name to read the full description. | `ReportVariables_CSH/RepVar_SSTDefinition.htm` |
| Channel | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_SSTDefinition_channel.htm` |
| Evaluation Formula | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_SSTDefinition_eval_formula.htm` |
| Injection Condition | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_SSTDefinition_injection_condition.htm` |
| Fail Actions | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_SSTDefinition_irc_fail_action_list.htm` |
| Number of Fail Actions | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_SSTDefinition_irc_number_fail_actions.htm` |
| Number of Pass Actions | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_SSTDefinition_irc_number_pass_actions.htm` |
| Pass Actions | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_SSTDefinition_irc_pass_action_list.htm` |
| Name | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_SSTDefinition_name.htm` |
| Incomputable Interpretation (N.A.) | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_SSTDefinition_not_available.htm` |
| Number | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_SSTDefinition_number.htm` |
| Operator | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_SSTDefinition_operator.htm` |
| Peak Specification | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_SSTDefinition_peak_condition.htm` |
| Reference Value Formula | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_SSTDefinition_reference_value.htm` |
| Number of Decimal Places | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_SSTDefinition_round_digits.htm` |
| Statistics | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_SSTDefinition_statistics.htm` |
| Minimum/Maximum Number of Injections | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_SSTDefinition_statistics_min_injections.htm` |

### GlobalFunctions

**Official Help topics:** 14

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Global Functions Category | The Global Functions category includes global functions that are similar to the related functions in Microsoft Excel. The following table lists the available functions in the Global Functions category. Click a function name to read the full description. The functions are also available outside this category. | `ReportVariables_CSH/RepVar_GlobalFunctions.htm` |
| Absolute Value | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_GlobalFunctions_abs.htm` |
| Exponential Function | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_GlobalFunctions_exp.htm` |
| Find Position of Text | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_GlobalFunctions_find.htm` |
| If | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_GlobalFunctions_if.htm` |
| Is Error | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_GlobalFunctions_iserror.htm` |
| Select Left Text | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_GlobalFunctions_left.htm` |
| Natural Logarithm | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_GlobalFunctions_ln.htm` |
| Logarithm | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_GlobalFunctions_log.htm` |
| Select Middle Text | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_GlobalFunctions_mid.htm` |
| Select Right Text | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_GlobalFunctions_right.htm` |
| Round Value | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_GlobalFunctions_round.htm` |
| Convert to Text | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_GlobalFunctions_text.htm` |
| Time | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_GlobalFunctions_time.htm` |

### Fraction

**Official Help topics:** 12

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Fraction Category | The Fraction category includes variables that give information about the fraction, a group of tubes, in a tray collected during a sequence run. This is referred to as 'fraction collection'. Depending on whether time-based or peak-based fractionation has been used, a value is reported for the fraction defined by the corresponding detection channel settings fo | `ReportVariables_CSH/RepVar_Fraction.htm` |
| Channel Parameter | Open the Report Column dialog box (for example, by double-clicking a column header in the Interactive Results Table or other report table). | `ReportVariables_CSH/RepVar_Fraction_channel.htm` |
| End Time | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Fraction_endTime.htm` |
| Number of Peaks | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Fraction_nPeaks.htm` |
| Number of Tubes | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Fraction_nTubes.htm` |
| Number | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Fraction_number.htm` |
| Select Peak | Open the Report Column dialog box (for example, by double-clicking a column header in the Interactive Results Table or other report table). | `ReportVariables_CSH/RepVar_Fraction_peak.htm` |
| Start Time | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Fraction_startTime.htm` |
| Select Tube | Open the Report Column dialog box (for example, by double-clicking a column header in the Interactive Results Table or other report table). | `ReportVariables_CSH/RepVar_Fraction_tube.htm` |
| Tube Positions | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Fraction_tubePosition.htm` |
| Tube Position Range | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Fraction_tubePositionRange.htm` |
| Volume | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Fraction_volume.htm` |

### General

**Official Help topics:** 11

| Variable / topic | Help summary | Help topic |
|---|---|---|
| General Category | The General category includes variables that give information about the computer, Chromeleon, or the user. The following table lists the available variables in the General category. Click a variable name to read the full description. | `ReportVariables_CSH/RepVar_General.htm` |
| Computer Name | In the Report Designer, right-click a cell and select Insert > Report Variables to insert a variable, or select Report Formula Properties to modify one. The Formula Properties Report dialog opens. –OR– If creating or modifying a report table column in the Report Designer or in Interactive Results, double-click the column (or select Column Properties from the | `ReportVariables_CSH/RepVar_General_computerName.htm` |
| Current Printer | In the Report Designer, right-click a cell and select Insert > Report Variables to insert a variable, or select Report Formula Properties to modify one. The Formula Properties Report dialog opens. –OR– If creating or modifying a report table column in the Report Designer or in Interactive Results, double-click the column (or select Column Properties from the | `ReportVariables_CSH/RepVar_General_currentPrinter.htm` |
| Current Time | In the Report Designer, right-click a cell and select Insert > Report Variables to insert a variable, or select Report Formula Properties to modify one. The Formula Properties Report dialog opens. –OR– If creating or modifying a report table column in the Report Designer or in Interactive Results, double-click the column (or select Column Properties from the | `ReportVariables_CSH/RepVar_General_currentTime.htm` |
| Logged on User | In the Report Designer, right-click a cell and select Insert > Report Variables to insert a variable, or select Report Formula Properties to modify one. The Formula Properties Report dialog opens. –OR– If creating or modifying a report table column in the Report Designer or in Interactive Results, double-click the column (or select Column Properties from the | `ReportVariables_CSH/RepVar_General_loggedOnUser.htm` |
| My Documents Folder | In the Report Designer, right-click a cell and select Insert > Report Variables to insert a variable, or select Report Formula Properties to modify one. The Formula Properties Report dialog opens. –OR– If creating or modifying a report table column in the Report Designer or in Interactive Results, double-click the column (or select Column Properties from the | `ReportVariables_CSH/RepVar_General_mydocumentsfolder.htm` |
| Report Mode | In the Report Designer, right-click a cell and select Insert > Report Variables to insert a variable, or select Report Formula Properties to modify one. The Formula Properties Report dialog opens. –OR– If creating or modifying a report table column in the Report Designer or in Interactive Results, double-click the column (or select Column Properties from the | `ReportVariables_CSH/RepVar_General_reportMode.htm` |
| Report Operator | In the Report Designer, right-click a cell and select Insert > Report Variables to insert a variable, or select Report Formula Properties to modify one. The Formula Properties Report dialog opens. –OR– If creating or modifying a report table column in the Report Designer or in Interactive Results, double-click the column (or select Column Properties from the | `ReportVariables_CSH/RepVar_General_reportOperator.htm` |
| Report Time | In the Report Designer, right-click a cell and select Insert > Report Variables to insert a variable, or select Report Formula Properties to modify one. The Formula Properties Report dialog opens. –OR– If creating or modifying a report table column in the Report Designer or in Interactive Results, double-click the column (or select Column Properties from the | `ReportVariables_CSH/RepVar_General_reportTime.htm` |
| Serial Number | In the Report Designer, right-click a cell and select Insert > Report Variables to insert a variable, or select Report Formula Properties to modify one. The Formula Properties Report dialog opens. –OR– If creating or modifying a report table column in the Report Designer or in Interactive Results, double-click the column (or select Column Properties from the | `ReportVariables_CSH/RepVar_General_serialNo.htm` |
| Version Number | In the Report Designer, right-click a cell and select Insert > Report Variables to insert a variable, or select Report Formula Properties to modify one. The Formula Properties Report dialog opens. –OR– If creating or modifying a report table column in the Report Designer or in Interactive Results, double-click the column (or select Column Properties from the | `ReportVariables_CSH/RepVar_General_version.htm` |

### InstrumentMethod

**Official Help topics:** 11

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Instrument Method Category | The Instrument Method category includes variables that give information about the instrument method. The following table lists the available variables in the Instrument Method category. Click a variable name to read the full description. | `ReportVariables_CSH/RepVar_InstrumentMethod.htm` |
| Comment | Instrument Method Variable | `ReportVariables_CSH/RepVar_InstrumentMethod_comment.htm` |
| Creation Operator | Instrument Method Variable | `ReportVariables_CSH/RepVar_InstrumentMethod_creation_operator.htm` |
| Creation Date & Time | Instrument Method Variable | `ReportVariables_CSH/RepVar_InstrumentMethod_creation_time.htm` |
| Data Vault | Instrument Method Variable | `ReportVariables_CSH/RepVar_InstrumentMethod_dataVault.htm` |
| Directory | Instrument Method Variable | `ReportVariables_CSH/RepVar_InstrumentMethod_directory.htm` |
| Instrument | Instrument Method Variable | `ReportVariables_CSH/RepVar_InstrumentMethod_instrument.htm` |
| Name | Instrument Method Variable | `ReportVariables_CSH/RepVar_InstrumentMethod_name.htm` |
| Server | Instrument Method Variable | `ReportVariables_CSH/RepVar_InstrumentMethod_server.htm` |
| Last Update Operator | Instrument Method Variable | `ReportVariables_CSH/RepVar_InstrumentMethod_update_operator.htm` |
| Last Update Date & Time | Instrument Method Variable | `ReportVariables_CSH/RepVar_InstrumentMethod_update_time.htm` |

### ReportTemplate

**Official Help topics:** 11

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Report Template | The Report Template category includes variables that give information about the report template used. It is only available in the Report Designer (not in report tables). The following table lists the available variables in the Report Template category. Click a variable name to read the full description. | `ReportVariables_CSH/RepVar_ReportTemplate.htm` |
| Creation Operator | In the Report Designer , right-click an empty cell. | `ReportVariables_CSH/RepVar_ReportTemplate_creation_operator.htm` |
| Creation Date & Time | In the Report Designer , right-click an empty cell. | `ReportVariables_CSH/RepVar_ReportTemplate_creation_time.htm` |
| Current Sheet Name | In the Report Designer , right-click an empty cell. | `ReportVariables_CSH/RepVar_ReportTemplate_curSheetName.htm` |
| Current Sheet Number | In the Report Designer , right-click an empty cell. | `ReportVariables_CSH/RepVar_ReportTemplate_curSheetNo.htm` |
| Data Vault | In the Report Designer , right-click an empty cell. | `ReportVariables_CSH/RepVar_ReportTemplate_dataVault.htm` |
| Directory | In the Report Designer , right-click an empty cell. | `ReportVariables_CSH/RepVar_ReportTemplate_directory.htm` |
| Name | In the Report Designer , right-click an empty cell. | `ReportVariables_CSH/RepVar_ReportTemplate_name.htm` |
| Number of Sheets | In the Report Designer , right-click an empty cell. | `ReportVariables_CSH/RepVar_ReportTemplate_sheets.htm` |
| Last Update Operator | In the Report Designer , right-click an empty cell. | `ReportVariables_CSH/RepVar_ReportTemplate_update_operator.htm` |
| Last Update Date & Time | In the Report Designer , right-click an empty cell. | `ReportVariables_CSH/RepVar_ReportTemplate_update_time.htm` |

### ReportValueList

**Official Help topics:** 9

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Statistics Category | Open the Statistics category by selecting the Statistics variable of the Test Case Result category. The variables in the Statistics category return the result of a statistics function used to calculate the evaluation formula (system suitability test case only). | `ReportVariables_CSH/RepVar_ReportValueList.htm` |
| Average | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_ReportValueList_average.htm` |
| Count | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_ReportValueList_count.htm` |
| Minimum/Maximum | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_ReportValueList_minimum.htm` |
| Range | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_ReportValueList_range.htm` |
| Relative Range | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_ReportValueList_rel_range.htm` |
| Relative Standard Deviation | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_ReportValueList_rel_stddev.htm` |
| Standard Deviation | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_ReportValueList_stdev.htm` |
| Sum | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_ReportValueList_sum.htm` |

### SSTResults

**Official Help topics:** 9

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Test Case Result Category | The Test Case Result category includes variables that give information about the results of a specific test case. The following table lists the available variables in this category. Click a variable name to read the full description. | `ReportVariables_CSH/RepVar_SSTResults.htm` |
| Evaluation Result | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_SSTResults_eval_result.htm` |
| Injection Evaluation Result | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_SSTResults_injection_eval_result.htm` |
| Injection Condition Result | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_SSTResults_injection_match.htm` |
| Message | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_SSTResults_message.htm` |
| Peak Result | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_SSTResults_peak_result.htm` |
| Reference Value | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_SSTResults_reference_value.htm` |
| Result | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_SSTResults_result.htm` |
| Statistics | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_SSTResults_statistics.htm` |

### Table

**Official Help topics:** 9

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Group Average | Integration/Summary Table Variable | `ReportVariables_CSH/RepVar_Table_groupaverage.htm` |
| Group Count | Integration/Summary Table Variable | `ReportVariables_CSH/RepVar_Table_groupcount.htm` |
| Group Maximum | Integration/Summary Table Variable | `ReportVariables_CSH/RepVar_Table_groupmax.htm` |
| Group Minimum | Integration/Summary Table Variable | `ReportVariables_CSH/RepVar_Table_groupmin.htm` |
| Group Range | Integration/Summary Table Variable | `ReportVariables_CSH/RepVar_Table_grouprange.htm` |
| Group Relative Range | Integration/Summary Table Variable | `ReportVariables_CSH/RepVar_Table_grouprelrange.htm` |
| Group Relative Standard Deviation | Integration/Summary Table Variable | `ReportVariables_CSH/RepVar_Table_grouprelstdev.htm` |
| Group Standard Deviation | Integration/Summary Table Variable | `ReportVariables_CSH/RepVar_Table_groupstdev.htm` |
| Group Sum | Integration/Summary Table Variable | `ReportVariables_CSH/RepVar_Table_groupsum.htm` |

### UvSettings

**Official Help topics:** 9

| Variable / topic | Help summary | Help topic |
|---|---|---|
| UV Settings Category | Open the UV Settings category by selecting the UV Spectra Settings variable of the Processing Method category. The variables in the UV Settings category give information about the settings selected on the UV Spectra Settings and UV Spectra Comparison Defaults dialog boxes of the Processing Method Editor. The following table lists the available variables in t | `ReportVariables_CSH/RepVar_UvSettings.htm` |
| Baseline Correction | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_UvSettings_baseline_correction.htm` |
| Spectrum Derivative | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_UvSettings_derivative.htm` |
| Minimum/Maximum of Fixed Baseline Correction Range | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_UvSettings_fixed_blcorrection_range_max.htm` |
| Left/Right Region Bunch | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_UvSettings_left_region_bunch.htm` |
| Match Criterion | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_UvSettings_match.htm` |
| Peak Spectrum Bunch | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_UvSettings_peak_spectrum_bunch.htm` |
| Peak Purity Threshold | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_UvSettings_threshold.htm` |
| Wavelength Range Minimum/Maximum | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_UvSettings_wavelength_max.htm` |

### AuditTrailEvent

**Official Help topics:** 6

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Description | Audit Trail Event Variables | `ReportVariables_CSH/RepVar_AuditTrailEvent_description.htm` |
| Object Name | Audit Trail Event Variables | `ReportVariables_CSH/RepVar_AuditTrailEvent_name.htm` |
| Operator | Audit Trail Event Variables | `ReportVariables_CSH/RepVar_AuditTrailEvent_operator.htm` |
| Role | Audit Trail Event Variables | `ReportVariables_CSH/RepVar_AuditTrailEvent_role.htm` |
| Date/Time | Audit Trail Event Variables | `ReportVariables_CSH/RepVar_AuditTrailEvent_time.htm` |
| Event Type | Audit Trail Event Variables | `ReportVariables_CSH/RepVar_AuditTrailEvent_type.htm` |

### TimeFunctions

**Official Help topics:** 5

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Date & Time | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_TimeFunctions.htm` |
| Format Date & Time | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_TimeFunctions_format.htm` |
| Local Time | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_TimeFunctions_local.htm` |
| Time Offset | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_TimeFunctions_offset.htm` |
| Coordinated Universal Time | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_TimeFunctions_utc.htm` |

### AuditTrail

**Official Help topics:** 1

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Audit Trail Category | The Audit Trail category includes variables that give information about all events that are logged in the Injection = 4 && typeof(BSPSPopupOnMouseOver) == 'function') BSPSPopupOnMouseOver(event);" class="BSSCPopup" onclick="BSSCPopup('../Glossary/GLOSSARY_AUDIT_TRAIL.htm');return false;">Audit Trail . The available variables depend on the installed system an | `ReportVariables_CSH/RepVar_AuditTrail.htm` |

### AuditTrailEvents

**Official Help topics:** 1

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Audit Trail Event Category | Variables of the audit trail event report category are used in the Audit Trail Event report table . Below is a list of available variables in the Audit Trail Event category. Click a variable name to read the full description. | `ReportVariables_CSH/RepVar_AuditTrailEvents.htm` |

### CellFormula

**Official Help topics:** 1

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Formula | Report Variable Properties Dialog | `ReportVariables_CSH/RepVar_CellFormula.htm` |

### CustomFormulas

**Official Help topics:** 1

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Custom Formulas Category | The Custom Formulas category lets you evaluate your own bespoke expressions created using the Custom Formula Wizard . | `ReportVariables_CSH/RepVar_CustomFormulas.htm` |

### CustomVar

**Official Help topics:** 1

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Custom Variable | Component/Injection/Sequence/Peak Group Variable | `ReportVariables_CSH/RepVar_CustomVar.htm` |

### Evaluate

**Official Help topics:** 1

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Evaluate | Chromatogram/Injection/Peak Result Variable | `ReportVariables_CSH/RepVar_Evaluate.htm` |

### IntegrationTable

**Official Help topics:** 1

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Integration Table and Summary Table Categories | Note: On the Summary tab page, the Summary Table category is available. On all other tab pages, the Integration Table category is available. | `ReportVariables_CSH/RepVar_IntegrationTable_SummaryTable.htm` |

### Precondition

**Official Help topics:** 1

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Preconditions Category | The Preconditions category includes variables that give information about the instrument settings that were logged in the Injection = 4 && typeof(BSPSPopupOnMouseOver) == 'function') BSPSPopupOnMouseOver(event);" class="BSSCPopup" onclick="BSSCPopup('../Glossary/GLOSSARY_AUDIT_TRAIL.htm');return false;">Audit Trail before the analysis. The available variable | `ReportVariables_CSH/RepVar_Precondition.htm` |

### repvar

**Official Help topics:** 1

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Height (Peak Height) | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/repvar_peak_results_height.htm` |
