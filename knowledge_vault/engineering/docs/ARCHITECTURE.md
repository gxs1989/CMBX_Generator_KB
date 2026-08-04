# CMBX Data Explorer Architecture

This document describes the current program structure and the intended module boundaries. It is the working guide for future cleanup before merging the tool into a larger Hub.

## Design Goal

CMBX Data Explorer is a general Chromeleon CMBX inspection, export, and report-reconstruction tool. It should not depend on TCC-specific assumptions at the package/parsing layer. TCC and FOQ files are validation data and specialized report contracts layered on top of the general CMBX parser.

## Main Layers

### UI Layer

Entry point:

```text
app.py
```

Responsibilities:

- Load one or more CMBX packages into the `Sequence Data` tree at the same time.
- Display package structure, injections, channels, methods, reports, and report details.
- Route user actions to export services.
- Keep UI behavior thin; avoid embedding calculation rules here.

Tab-level behavior is documented separately so each UI area can be refactored into a dedicated view class later without changing the export/calculation layers:

- `TAB_RAW_CHANNELS.md`
- `TAB_RAW_PLOT.md`
- `TAB_FOQ_DB.md`
- `TAB_DATABASE_UPLOAD.md`
- `TAB_AUDIT_TRAILS.md`
- `TAB_REPORT_SHEETS.md`
- `TAB_INSTRUMENT_METHODS.md`
- `TAB_PROCESSING_METHODS.md`
- `TAB_REPORT_TEMPLATES.md`
- `TAB_CMBX_INFO.md`
- `TAB_FOQ_KB_TO_RUN.md`
- `CM_FORMULA_KNOWLEDGE_BASE.md`
- `CM_INSTRUMENT_COMMAND_KNOWLEDGE_BASE_V2.md`
- `CM_METHOD_COMMAND_KNOWLEDGE_BASE.md`
- `CM_INSTRUMENT_CONFIGURATION_KNOWLEDGE_BASE.md`
- `FOQ_TD_TEST_LOGIC_KNOWLEDGE_BASE.md`
- `TCC_REQUIRED_SYMBOL_MANIFEST.md`
- `TCC_FOQ_METHOD_REPORT_KNOWLEDGE_BASE.md`
- `CMBX_REVERSE_GENERATION_STRATEGY.md`

### CMBX Container Layer

Core module:

```text
cmbx_container.py
```

Responsibilities:

- Read CMBX local ZIP-like entries.
- Extract `header.xml`.
- Build `CmbxPackage` and `CmbxElement` trees.
- Classify elements as sequence, injection, signal, audit, instrument method, processing method, or report template.
- Cache commonly accessed element lists and avoid repeated full-file reads during package load.

This layer should stay generic.

### Chromeleon Runtime Bridge

Core modules:

```text
chromeleon_runtime.py
chromeleon_bridge.py
chromeleon_signal_exporter.cs
chromeleon_audit_exporter.cs
chromeleon_method_decoder.py
```

Responsibilities:

- Locate approved Chromeleon runtime DLLs.
- Decode raw signal data into TSV.
- Decode audit trail data into TSV.
- Decode CpXm method/report payloads when the runtime is available.

This layer is optional at runtime. Basic package inspection can work without Chromeleon DLLs; raw signal, audit, and CpXm decoding need them.

### Embedded Method and Report Extraction

Core modules:

```text
embedded_method_extractor.py
instrument_method_parser.py
method_xml_flow.py
sequence_cmd_parser.py
embedded_report_extractor.py
```

Responsibilities:

- Locate embedded method/report blocks inside sequence command payloads.
- Decode embedded XML where possible.
- Produce readable method flow and report sheet/object tables.
- Keep extraction generic and independent from FOQ contract logic.

### Report Formula Evaluation

Core module:

```text
report_formula_evaluator.py
```

Responsibilities:

- Evaluate supported CM report formulas against one injection.
- Resolve audit RetTimes, audit properties, precondition metadata, sequence metadata, and raw signal windows.
- Cache decoded audit and signal data during one report evaluation.

Important implemented formula families:

- `AUDIT.RetTimeN(...)`
- timed `AUDIT.<path>(time, direction)`
- `precond.<path>`
- `seq.*`, `smp.*`, `injection.*`
- `chm.sig_value(...)`
- `chm.signalStatistic(...)`
- `chm.signalValue(...)`
- `chm.noise(...)`
- `chm.drift(...)`

### Report Workbook Reconstruction

Core modules:

```text
report_workbook_builder.py
report_calculation_map.py
```

Responsibilities:

- Build injection-level report workbooks from evaluated formula values.
- Detect and document known derived-cell logic from report templates.
- Provide readable report-like layouts for sheets that have been mapped.

### FOQ Contract Export

Core modules:

```text
foq_result_locations.py
foq_contract_report.py
foq_preview_worker.py
```

Responsibilities:

- Read `FOQResultLocations_V2.83.xls`.
- Map DB fields to report file/sheet/cell targets.
- Reconstruct final report-cell values from direct CM formula cells and known workbook-derived rules.
- Write database-ready FOQ contract workbooks.
- Apply verified report-display precision to DB workbook values before SQL upload.

This layer is intentionally specialized. It can depend on FOQ mapping rules, but it should not leak FOQ assumptions into generic CMBX parsing.

### Export Orchestration

Core module:

```text
export_service.py
```

### Database Upload

Core module:

```text
db_upload_service.py
```

Responsibilities:

- Read exported FOQ DB workbooks.
- Resolve SQL target tables from `DeviceType` / `MappingSheet`.
- Create FOQ-style SQL tables when needed.
- Insert one row per sequence workbook into SQL Server.

### Reverse Generation Knowledge Layer

Core documents:

```text
CM_FORMULA_KNOWLEDGE_BASE.md
CM_METHOD_COMMAND_KNOWLEDGE_BASE.md
CM_INSTRUMENT_CONFIGURATION_KNOWLEDGE_BASE.md
TCC_REQUIRED_SYMBOL_MANIFEST.md
TCC_FOQ_METHOD_REPORT_KNOWLEDGE_BASE.md
CMBX_REVERSE_GENERATION_STRATEGY.md
```

Responsibilities:

- Record decoded method command paths and report formula behavior.
- Record target-instrument configuration prerequisites that decide whether generated method commands are runnable in CM.
- Connect TD requirements to CMBX sequence/injection/method/report structure.
- Define per-device sequence blueprints, starting with TCC VA/VC/VH.
- Keep generation knowledge separate from the generic parser until binary writing is validated.
- Prefer a first-stage golden-CMBX clone/select/swap strategy before attempting full synthetic CMBX creation.

The upload layer is specialized for FOQ DB output, but it is separate from formula evaluation and CMBX parsing.

Responsibilities:

- Provide UI-friendly operations for exporting selected items.
- Coordinate package extraction, method/report extraction, formula evaluation, report workbook generation, and FOQ contract generation.
- Batch FOQ contract export can write one database-ready workbook per loaded CMBX package.

## Current Validation Data

Primary validation package:

```text
C:\Users\xiaoshu.guan\OneDrive - Thermo Fisher Scientific\Documents\TCC Temperature Control Analyzer\DATA\20260701_New\6545327.cmbx
```

CM reference reports:

```text
cmbx_data_explorer\outputs\foq_contract_6545327_logic_audit\6545327\6545327.seq\*.xls
```

Latest generated comparison workbook:

```text
cmbx_data_explorer\outputs\foq_contract_6545327_cm_compare_after_remaining_diff_check\6545327\VH-C10-A_FOQ_contract_DB.xlsx
```

Current comparison status:

```text
matched: 76
small_numeric: 5
numeric_diff: 0
text_diff: 0
missing: 0
```

The remaining small numeric differences are limited to CM signal-statistic details for `chm.noise(...)` and `chm.sig_value("drift", ...)`.

## Cleanup Direction

Recommended next structural step:

1. Keep `cmbx_container.py`, runtime bridge, and embedded extraction generic.
2. Move FOQ-only rule tables and derived-cell rules under a clearly named contract package when the file count grows.
3. Keep tests grouped by layer:
   - package parsing
   - runtime bridge stubs
   - embedded method/report extraction
   - formula evaluation
   - report workbook rules
   - FOQ contract export
4. Keep output folders out of source assumptions. They are validation artifacts, not source data.
