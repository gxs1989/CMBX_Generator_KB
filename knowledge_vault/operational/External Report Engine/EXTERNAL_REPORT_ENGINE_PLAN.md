# External Report Engine Design Plan

**Status:** V1 implemented; integration/quantitation phases remain open  
**Date:** 2026-07-24  
**Target:** A standalone, maximizable analysis tool launched from CMBX Data Explorer  
**Primary input:** Executed CMBX packages containing sequences, injections, raw channels, audit trails and instrument methods

## V1 Implementation Record

Implemented on 2026-07-24:

- Main-window `External Report Engine` command and maximizable standalone window.
- Multiple CMBX files or folders, excluding `deleted` folders during folder import.
- Deterministic Report MD parser and typed operation model.
- Cross-package/injection compatibility matrix.
- Raw scalar formulas, RetTime windows, safe cell-to-cell expressions.
- Filtered/grouped audit event tables and raw threshold event tables.
- Raw plot preview and batch XLSX export.
- Shared result model for preview and export.

Executable syntax is part of the single canonical `CM_REPORT_TEMPLATE_MD_TO_CMBX_SPEC.md`. There is no separate External Report SPEC.

## 1. Objective

Build an external data-processing and reporting engine that does not require a Chromeleon Report Template or Processing Method for its first useful release.

The complete web-authoring contract consists of exactly two specifications:

1. One Method SPEC for Instrument Method MD generation.
2. One universal Report SPEC for Report MD generation.

The Report SPEC is not split into CM and external variants. One task-specific Report MD contains analysis, dynamic tables, plots, acceptance rules and report layout. The local parser converts it to a backend-neutral intermediate representation. A CM report compiler and the External Report Engine consume the same representation according to their verified capabilities.

The program supports two deterministic authoring paths: import/paste the Report MD, or use structured manual controls that edit the same parsed model. Natural-language interpretation and AI execution are outside the program. A web model may use the universal SPEC to draft the MD, but the local program only parses, validates and executes explicit declarations.

```text
Web conversation + Method SPEC + Report SPEC
                -> Instrument Method MD + task-specific Report MD
                                      |
External Report MD ----------------> parser ---------+
                                                      |
Manual builder --------------------> same model ------+--> AnalysisSpec
                                                             |
                                                      Local validation
                                                             |
CMBX raw/audit/method evidence ----------------------> Execution engine
                                                             |
                                                     Unified Result Model
                                                             |
                                              +--------------+-------------+
                                              |              |             |
                                            Tables          Plots       Report files
```

## 2. Product Boundary

### 2.1 First useful release

The first release supports:

- standalone browsing of one or multiple CMBX packages and folders;
- sequence/injection/channel selection;
- raw-channel plots;
- Instrument Audit Trail filtering;
- RetTime and timed audit-property lookup;
- verified CM-compatible signal statistics;
- custom raw-signal and audit-event tables;
- cell-to-cell calculations through structured expressions;
- basic result/acceptance rules;
- XLSX export first, then HTML/PDF;
- complete provenance from output value to package/injection/channel/audit record.

It does not initially support:

- full chromatographic peak integration;
- component identification;
- external/internal-standard quantitation;
- calibration curves;
- SST/IRC execution;
- manual chromatographic integration;
- complete emulation of all CM or FormulaOne formulas;
- writing Processing Methods back to CMBX.

### 2.2 Long-term expansion

Later releases may add:

1. Processing Method read-only semantic decoding.
2. External peak detection and integration.
3. Component identification and calibration.
4. Manual integration overlays with audit history.
5. Optional CM-result comparison and compatibility validation.

## 3. Application Entry

Add one main-window command button:

```text
External Report Engine
```

Behavior:

- opens a separate maximizable window;
- does not depend on the active notebook tab;
- may receive the currently selected CMBX as a convenience;
- always allows browsing to another CMBX;
- does not modify the source package;
- keeps its own project state and output folder.

The tool is independent of the existing CM Report Template Generator. The latter creates report-template CMBX files; this engine reads completed CMBX data and creates external reports.

## 4. UI Workflow

Use a five-step workflow. Show only one step's primary controls at a time.

```text
[1 Data] -> [2 Report MD] -> [3 Analysis] -> [4 Review] -> [5 Report]
```

### 4.1 Step 1 - Data

Purpose: establish exactly which evidence exists before interpreting the request.

Layout:

```text
Source CMBX: [path................................] [Browse]

Sequence / Injection tree       Selected data summary
-------------------------       ---------------------
Sequence                        Device model
  Injection                     Injection duration
    Raw channels                Raw channel count
    Audit Trail                 Audit record count
    Instrument Method           RetTimes found
                                Method name
```

Required operations:

- browse one or more CMBX packages or add all packages from a selected folder;
- select one or multiple injections;
- inspect available channels and units;
- inspect Audit Trail property paths;
- identify device from `AUDIT.<device>.ModelNo` evidence when available;
- display acquisition range, sample rate and missing evidence;
- cache decoded raw/audit metadata for subsequent steps.

For multiple packages, show a compatibility matrix before loading full raw arrays:

| CMBX | Sequence | Injection | Device | Required channels | Required audit paths | RetTimes | Applicable |
|---|---|---|---|---|---|---|---|
| Package A | ... | ... | ... | complete | complete | complete | yes |
| Package B | ... | ... | ... | missing one | complete | complete | partial |
| Package C | ... | ... | ... | complete | missing | complete | no |

The Report MD is bound to a data contract, not a package filename. A different CMBX is applicable when its selected injection satisfies the same declared requirements.

The engine must not ask AI to guess channel names, device paths or RetTimes.

### 4.2 Step 2 - Report MD

- paste Markdown;
- browse/import `.md`;
- syntax preview;
- parse and preflight;
- show unsupported declarations before execution.

The imported MD and later manual edits populate the same editable structured summary:

| Item | Detected value | Evidence | Status |
|---|---|---|---|
| Injection scope | ... | CMBX | bound |
| Required channel | ... | raw inventory | bound/missing |
| Event source | ... | audit/raw | bound/missing |
| Time window | ... | intent/RetTime | bound/review |
| Calculation | ... | formula registry | supported/review |
| Acceptance rule | ... | TD/KB/user | bound/missing |

Preflight runs independently for every selected package/injection. One incompatible package must not block compatible packages unless the Report MD explicitly requires an all-or-nothing batch.

### 4.3 Step 3 - Analysis

This is the manual builder and structured spec editor. It must use domain controls, not one large text box.

Analysis blocks:

| Block | Purpose | MVP |
|---|---|---:|
| Signal Window | Select channel and start/end or RetTime-relative window | Yes |
| Signal Statistic | Average, min, max, range, standard deviation, drift, noise | Yes |
| Signal Sample | Signal value at an explicit/derived time | Yes |
| Audit Lookup | Property value forward/backward from a time | Yes |
| Audit Event Table | Filter property/message events and create rows | Yes |
| Raw Event Detector | Threshold crossing, edge, debounce, hysteresis, minimum spacing | Yes |
| Formula | Arithmetic, Boolean and supported functions over prior results | Yes |
| Acceptance Rule | Limit and pass/fail classification | Yes |
| Plot | Raw series, selected windows, event markers and limit lines | Yes |
| Peak Integration | Chromatographic peak detection/integration | Later |
| Calibration | External/internal standard and curve fitting | Later |

Every block shows:

- inputs;
- output name and type;
- units;
- compatibility level;
- validation result;
- downstream dependents.

### 4.4 Step 4 - Review

Review calculated evidence before arranging the report.

Views:

1. Results table.
2. Dynamic event tables.
3. Raw plots with selected windows and detected events.
4. Formula/dependency trace.
5. Validation and warnings.

Provide three preview levels:

1. **Structure Preview:** report sheets/blocks, columns, formulas and plots with placeholders; no CMBX calculation required.
2. **Data Preview:** execute against one selected injection and show real values, dynamic rows, plots and source trace.
3. **Batch Preview:** execute selected headline outputs across all compatible packages/injections and show comparison, missing-data and error columns.

Preview must use the same parser, execution engine and result model as final export. It must not maintain a separate simplified calculation path.

Manual operations in the MVP:

- include/exclude a detected event without altering raw data;
- adjust event detector parameters;
- change a calculation window;
- add or remove an output column;
- rename labels and set number format;
- rerun and compare before/after values.

Every edit updates `AnalysisSpec` and invalidates dependent calculations. No displayed result may remain stale.

### 4.5 Step 5 - Report

Use a block-based layout editor:

- title and metadata block;
- scalar result table;
- dynamic event table;
- raw-signal plot;
- acceptance summary;
- source/provenance appendix.

First outputs:

- XLSX with calculated values and plots;
- project file containing specs and review edits;
- calculation trace workbook/sheet.

Batch output modes:

- one workbook per injection;
- one workbook per CMBX package;
- one combined workbook with one summary row per package/injection and optional detail sheets;
- export only compatible items, with a separate exclusions/error sheet.

Later outputs:

- HTML;
- PDF;
- JSON/CSV data package;
- optional database upload contract.

## 5. Universal Report SPEC and Report MD

Only one universal Report SPEC teaches report syntax and execution semantics. It is module-neutral, backend-neutral and versioned with the program. It includes:

- document grammar;
- supported operation registry;
- CM compatibility names and levels;
- dynamic-event semantics;
- table and plot declarations;
- acceptance-rule grammar;
- validation and provenance requirements;
- unsupported-operation behavior.

Each analysis uses one task-specific Report MD. It must be self-contained after the source CMBX is selected: all channels, audit paths, windows, parameters, formulas, event grouping, acceptance limits and report blocks must be explicit. For jointly generated methods/reports, these bindings come from the Method MD's Produced Data Contract. Module knowledge may help a web model author the files, but hidden KB assumptions are not allowed during local execution.

The MD describes report semantics, not CM binary report objects and not implementation-specific external code.

Example outline:

````markdown
---
kind: cmbx_report
spec_version: 1.0
report_name: Valve Switch Review
---

## Data Scope
```yaml
packages: selected
sequences: selected
injections: selected
batch_policy: continue_compatible
```

## Data Requirements
```yaml
audit_paths:
  - ColumnComp.LiquidLeakCalibrationValue
channels: []
ret_times: []
```

## Audit Event Table: Valve Switches
```yaml
source: instrument_audit
property_paths:
  - ColumnComp.UpperValve.CurrentPosition
  - ColumnComp.LowerValve.CurrentPosition
group_within_seconds: 2
columns: [retention_time, upper_position, lower_position, interval_seconds]
```

## Plot: Temperature
```yaml
channels: [CC_Temp, ExtTemp_UpperCC, ExtTemp_LowerCC]
x_axis: retention_time_min
event_markers: Valve Switches
```
````

The final grammar must be versioned and parsed into typed objects. Unknown keys are errors or review warnings, never silently ignored.

### 5.1 Shared Intermediate Representation

```text
Report MD
-> universal parser
-> ReportIR + AnalysisSpec
   |-> CM Report CMBX backend (supported CM subset)
   `-> External Report Engine backend (full external operation set)
```

The user chooses the output in the program. The Report MD does not need separate CM/external versions.

Every parsed operation receives backend capability results:

| Status | Meaning |
|---|---|
| `CM_AND_EXTERNAL` | Can be compiled to CM and executed externally |
| `CM_ONLY` | Requires a native CM object/runtime not reproduced externally |
| `EXTERNAL_ONLY` | Uses behavior CM cannot represent, such as arbitrary event-generated rows |
| `UNSUPPORTED` | Neither backend has a verified implementation |

If CM output is requested and an operation is `EXTERNAL_ONLY`, the compiler must report the exact incompatible operation. It must not silently replace it. External output may still proceed.

## 6. AnalysisSpec

Suggested top-level model:

```yaml
project:
  name: string
  spec_version: string

sources:
  packages: []
  sequences: []
  injections: []

operations:
  - id: string
    type: signal_statistic | signal_sample | audit_lookup | audit_events | raw_events | formula
    inputs: {}
    parameters: {}
    output_type: scalar | series | table
    unit: string

acceptance_rules: []
plots: []
report_blocks: []
```

Operations form a directed acyclic dependency graph. Execution order comes from dependencies, not document order alone.

## 7. Formula and Operation Registry

Do not evaluate arbitrary text with Python `eval` or an equivalent mechanism.

Each operation must be registered with:

- canonical name;
- aliases, including verified CM formula names;
- typed parameters;
- allowed input/output types;
- unit behavior;
- deterministic implementation;
- CM compatibility status;
- test vectors and source evidence.

Compatibility levels:

| Level | Meaning |
|---|---|
| `CM_VERIFIED` | Compared with a real CM result within a declared tolerance |
| `CM_MODELED` | Intended to reproduce known CM semantics but not fully verified |
| `EXTERNAL_DEFINED` | Deliberately external behavior; no CM-equivalence claim |
| `OPEN_VERIFICATION` | Insufficient evidence; cannot be production result |

Initial compatible operations:

- `chm.sig_value` / `chm.signalStatistic`: average, min, max, standard deviation and modeled drift;
- `chm.signalValue`;
- `chm.noise`;
- `chm.drift`;
- `AUDIT.RetTimeN`;
- timed `AUDIT.<path>` forward/backward lookup;
- selected `seq.*`, `injection.*`, `smp.*` and `precond.*` metadata;
- validated TCC workbook-derived calculations.

## 8. Dynamic Event Engine

### 8.1 Audit events

Capabilities:

- filter by normalized property path;
- filter by device, message or value;
- identify property-value changes;
- pair related upper/lower valve events within a tolerance;
- calculate intervals and switching speed;
- preserve links to original audit-record indices.

### 8.2 Raw-signal events

Capabilities:

- rising/falling/either threshold crossing;
- hysteresis;
- debounce/true-time;
- minimum event spacing;
- local extrema;
- change magnitude/rate;
- event window statistics;
- event markers on plots.

These are external operations. They must not be described as CM Report Table behavior unless separately verified.

## 9. Unified Result Model

Every result carries:

```text
value or table/series
unit
status
source package
sequence and injection
channel/audit path
source time range/records
operation ID and parameters
software/algorithm version
manual overlays
warnings
```

This model separates calculation from XLSX/PDF formatting and lets downstream reports update after a manual change.

## 10. Manual Review and Future Manual Integration

MVP manual event edits are non-destructive overlays.

Future chromatographic manual integration must use the same principle:

```text
immutable raw signal
+ automatic integration result
+ manual edit overlay
= current effective result
```

The overlay must record peak delimiters, baseline nodes/segments, split/merge/add/delete operations, component assignment, user, timestamp, reason and before/after results. Quantitation and reports must recalculate from the current effective result.

## 11. Processing Method Parallel Track

Continue read-only Processing Method reverse engineering without blocking the MVP.

Recommended order:

1. Processing Method payload/object inventory.
2. Detection algorithm and time-dependent detection parameters.
3. Baseline and peak boundary semantics.
4. Component table and identification windows.
5. Calibration model, levels, weighting and standard method.
6. SST/IRC.
7. Manual integration evidence.

Processing Method evidence serves as parameter semantics and a validation oracle. The first External Report Engine release does not generate Processing Methods.

## 12. Project Persistence

Suggested project extension:

```text
.cmbxreport
```

It may be a ZIP container with:

```text
project.json
analysis_spec.yaml
report_spec.yaml
manual_overlays.json
source_manifest.json
cached_results/
```

Do not embed the original CMBX by default. Store absolute path, package identity, size, timestamp and hash; optionally support a portable project with the source package included.

## 13. Performance and Safety

- Decode package metadata first; load raw arrays lazily.
- Cache raw/audit extraction by package/injection/channel identity.
- Execute long operations in a worker process or thread without blocking Tk UI.
- Show current stage, elapsed time and item count rather than a decorative progress bar.
- Support cancellation between operations.
- Keep the source CMBX read-only.
- Reject missing channels, ambiguous units and unsupported formulas before execution.
- Never label `CM_MODELED` or `EXTERNAL_DEFINED` values as CM-equivalent.

## 14. Validation Strategy

### Unit validation

- formula parser and typed operation registry;
- RetTime/time-expression handling;
- audit filtering and valve-event pairing;
- signal windowing, interpolation and statistics;
- dependency invalidation;
- unit and number-format behavior.

### Golden CMBX validation

- TCC Temperature Accuracy;
- Temperature Stability/Precision;
- HeatUp/CoolDown;
- valve-switch audit table;
- pressure/raw event detection;
- VDAD noise/drift as later signal-analysis cases.

For every CM-compatible operation, store expected CM values, tolerance, package identity and source formula.

## 15. Delivery Phases

### Phase E1 - Framework

- launch button and standalone window;
- CMBX source explorer;
- External Report MD parser;
- `AnalysisSpec`, result model and project persistence;
- validation/status UI.

### Phase E2 - Current formula subset

- move existing raw/audit formula evaluators behind the operation registry;
- scalar results and dependency trace;
- XLSX export.

### Phase E3 - Dynamic events and plots

- audit event tables;
- raw event detector;
- valve-event pairing and interval calculations;
- interactive plot and event review.

### Phase E4 - Authoring interoperability

- publish one complete universal SPEC for web-model authoring;
- keep one task-specific Report MD as the portable project definition;
- serialize structured manual changes back to the same MD grammar;
- provide actionable preflight errors that can be returned to a web conversation for correction.

### Phase E5 - Processing and integration research

- Processing Method semantic decode;
- external integration prototype;
- CM comparison harness;
- manual integration overlay design and validation.

## 16. First Acceptance Scenario

Input:

- one executed valve-cycle CMBX;
- user intent: show only each valve switch time, upper/lower positions, interval and switching speed;
- no Processing Method integration dependency.

Expected result:

1. Engine selects upper/lower valve audit property paths.
2. It detects value-change records.
3. It pairs upper/lower changes for each operation.
4. It calculates the interval from the previous switch and switching speed.
5. It renders a clean dynamic table and overlays markers on a selected raw plot.
6. Every row links back to original audit records.
7. XLSX export contains report, event data and provenance sheets.

This scenario proves the reason for building the external engine without first solving chromatographic integration.

## 17. Decisions Before Implementation

The following decisions should be confirmed before coding begins:

1. Whether one project may combine multiple CMBX packages in E1 or only one package.
2. Whether the first report output is XLSX only.
3. Whether structured manual edits overwrite the imported MD or save a revised copy.
4. Whether external report MD and project files are stored under the current workspace output folder by default.

Recommended defaults: one package with multiple injections, XLSX first, save manual edits as a revised MD copy, and use a dedicated `exports/External Reports` folder.
