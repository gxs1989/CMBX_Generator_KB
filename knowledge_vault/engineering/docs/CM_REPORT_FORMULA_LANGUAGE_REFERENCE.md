# CM Report Formula Language Reference

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
