# CMBX Data Explorer

General-purpose Chromeleon CMBX browser, report reconstruction, FOQ DB export, and SQL upload utility.

## Documentation Map

Feature and structure notes are split under `docs/`:

- `docs/ARCHITECTURE.md`: module boundaries and cleanup direction.
- `docs/FEATURE_CMBX_PACKAGE_BROWSER.md`: package tree and injection/channel browsing.
- `docs/FEATURE_RAW_AUDIT_SIGNAL_EXPORT.md`: raw signal and audit TSV export.
- `docs/FEATURE_METHOD_REPORT_EXTRACTION.md`: embedded method/report extraction.
- `docs/FEATURE_REPORT_FORMULA_EVALUATION.md`: CM formula evaluator and remaining signal-statistic differences.
- `docs/FEATURE_FOQ_CONTRACT_EXPORT.md`: FOQ mapping-driven DB workbook export.
- `docs/TAB_FOQ_DB.md`: FOQ DB candidate selection, preview, export, and candidate upload workflow.
- `docs/TAB_DATABASE_UPLOAD.md`: SQL Server upload configuration and batch workbook upload.
- `docs/TAB_FOQ_KB_TO_RUN.md`: FOQ TD-to-injection/method/report alignment workspace.
- `docs/TAB_KB_INDEX.md`: unified KB browser and classification entry point.
- `docs/CM_METHOD_SCRIPT_MD_FORMAT_SPEC.md`: strict MD method-script authoring SPEC for web AI and local preflight.
- `docs/MD_TO_STANDALONE_METHOD_CMBX_PACKAGING.md`: MD-to-standalone-instrument-method CMBX packaging path.
- `docs/CM_INSTRUMENT_COMMAND_KNOWLEDGE_BASE_V2.md`: CM Instrument Setup tree and instrument-command generation knowledge.
- `docs/FOQ_TD_TEST_LOGIC_KNOWLEDGE_BASE.md`: FOQ TD test logic, method evidence, and report-calculation understanding.
- `docs/CM_METHOD_COMMAND_KNOWLEDGE_BASE.md`: decoded CM instrument-method command patterns.
- `docs/CM_INSTRUMENT_CONFIGURATION_KNOWLEDGE_BASE.md`: CM driver/configuration prerequisites for runnable generated methods.
- `docs/TCC_REQUIRED_SYMBOL_MANIFEST.md`: TCC method-level required symbols for configuration validation.
- `docs/TCC_FOQ_METHOD_REPORT_KNOWLEDGE_BASE.md`: TCC VA/VC/VH FOQ method, sequence, report, and DB calculation knowledge.
- `docs/CMBX_REVERSE_GENERATION_STRATEGY.md`: path from decoded CMBX packages toward generated sequence/method/report packages.

## Current Version

`V1.42` adds a portable LAN Web-server deployment on top of the authenticated business workflows:

- External Report Engine V1 loads one report MD contract and evaluates it against one or more CMBX packages, with compatibility preflight, report preview, dynamic-table, plot, and log surfaces.
- Formula Finder indexes supported external formulas, formulas observed in CMBX reports, and locally extracted Chromeleon Help topics.
- Report-template MD compilation supports Direct CM formulas and verified FormulaOne cell-to-cell calculations, then packages the result as an importable report-template CMBX.
- Method Script Generator compiles strict structural MD into standalone method CMBX packages and can target the older CM 7.2 serialization contract.
- Instrument-method rendering preserves CM row kinds, stage times, trigger payloads, comments, and line alignment.
- KB Index remains the single knowledge entry point, grouped by CMBX reading, CMBX generation, method-script knowledge, report knowledge, FOQ knowledge, and skills.
- The native `Read & analyze` workflow now builds one shared multi-CMBX workset for hierarchical/reverse-match raw export, zoomable channel overlays, and cross-injection custom CM formula evaluation.
- RID is available as a Method & Report Creation module; the RID OQ sequence-template regression package is recognized as four sequences and ten injections without being misreported as missing runtime data.
- CMBX scanning, FOQ DB preview/export, report-display precision normalization, and multi-workbook SQL upload remain available.
- The approved internal deployment includes a minimal, versioned Chromeleon runtime closure, pinned Python server dependencies, FOQ mapping/carrier assets, and install/start/stop/preflight scripts.
- Runtime outputs, caches, local database/AI configuration, passwords, DSN credentials, and personal API keys remain outside the source repository.
- The authenticated Web Workspace provides owner-scoped CMBX/Method MD/Report MD libraries, four-step Method and Report generation, FOQ quick checks, quality-history comparison, raw export, chromatogram/integration review, and Direct CM formula evaluation.
- Administrators can grant each workflow independently, manage automatic-generation quotas, and provide a controlled workspace AI credential without exposing its key to authorized users.

## Launch Modes

Two launchers are intentionally kept during the business-UI migration:

- `launcher/启动CMBX工作台.bat`: opens the new guided business workspace with `Design & adapt`, `Read & analyze`, and `Verify & quality` workflows.
- `launcher/启动CMBX数据浏览器.bat`: opens the complete classic Explorer and all existing tabs.

The new workspace launches large tools in separate processes without a CMD window. The classic Explorer remains unchanged until each workflow has passed its own migration and acceptance tests.

### Web Workspace (First Release)

The browser workspace is a separate service and does not import Tkinter UI state.

1. Run `launcher/安装依赖.bat` as administrator on a new host.
2. Run `launcher/启动CMBX Web服务器.bat`.
3. Open the local or LAN URL printed by the launcher.

See `docs/WEB_SERVER_DEPLOYMENT.md` for migration, security, database-driver,
shared-storage, preflight, and troubleshooting details.

The Web workspace supports controlled CMBX upload, persistent jobs, FOQ checks, Method and Report Template generation, batch raw-data export, chromatogram comparison and external integration, Direct CM formula evaluation, read-only quality-database analysis, per-user quotas, and administrator approval. Personal API keys are protected with Windows DPAPI. AppsLab discovery and controlled production-database writes remain planned. Do not expose trusted identity headers through the Uvicorn port: production identity should enter through IIS Windows Authentication/HTTPS as described in `docs/WEB_WORKSPACE_BUILD_PLAN.md`.

The existing desktop GPT configuration is used once to initialize the designated Web administrator account. Open the Web workspace locally as `xiaoshu.guan`, then choose **Admin** under **OPERATIONS** to review quota requests and usage.

Web sessions use administrator-authorized email/password accounts. Windows sign-in and self-registration are disabled by default. Create, enable, reset, or disable accounts in **Admin Console > Developer accounts**. The owner fallback is `xiaoshu.guan@thermofisher.com` with temporary password `000000` and remains the default administrator.

## Application Scope

- Reads CMBX package entries and `header.xml`.
- Shows sequence, injection, channel, audit, and per-injection method/report context.
- Shows report sheets for the selected injection or sequence, including whether each sheet applies to the injection context.
- Exports filled Chromeleon-style `.xls` reports through the Report Sheets tab.
- Exports blank Chromeleon `.xls` report templates through the Report Templates tab.
- Builds a database-ready FOQ contract workbook through `Export FOQ DB`, using `FOQResultLocations_V2.83.xls` as the source-of-truth field/cell contract.
- Uploads FOQ DB workbooks to SQL Server using FOQ-style target tables.
- Uses one export path: select rows or tree objects, then click `Export Selected`.
- Provides `CMBX Notes` in the UI for the current package parsing assumptions and extension points.
- Provides `KB Index` and `Skills` tabs as the unified access points for formula, method, command, parsing, and generation knowledge.
- Exports selected signal channels to TSV through the local Chromeleon raw-data DLLs.
- Exports selected injection audit trails to TSV through the local Chromeleon audit decoder.
- Extracts package entries such as sequence command files as raw files for later parsers.
- Instrument method objects are extracted from the parent sequence `.cmd` as embedded Chromeleon binary blocks:
  - `*_embedded.instmeth.bin`: metadata plus the CMBX method payload slice
  - `*_embedded_payload.bin`: method payload wrapper
  - `*_embedded_payload.cpxm.bin`: inner `CpXm` payload that appears to contain the Chromeleon-specific method body
  - `*_embedded_method.xml`: readable Chromeleon method XML decoded from `CpXm` through the local Chromeleon `Dionex.DataCommon.dll`, when available
  - `*_embedded_method_flow.txt`: concise flow extracted from the decoded XML, including comments, setpoints, commands, and wait/trigger commands
  - `*_embedded_method_flow.tsv`: Excel-ready flow table with order, nesting level, action, target, value, comments, and conditions
  - `*_embedded_metadata.txt`: byte ranges, payload sizes, and readable strings
- The Instrument Methods tab includes an internal CM-like table reader with `Time / Command / Value / Comment`, using external TXT references when available and decoded embedded methods as fallback.
- Processing method objects can expose gzip-compressed XML editor layout/configuration blocks; those blocks are exported as `_embedded_N.xml`, while SST/IRC row semantics remain a reverse-engineering target.
- Report definition objects are extracted from the parent sequence `.cmd` and exported as blank FormulaOne `.xls` templates:
  - `*_report_template.xls`: the real blank Chromeleon Report Designer workbook exported from CMBX `SpreadSheetData`
  - `<injection name>.xls`: filled Chromeleon-style report for an injection
  - `<sequence name>_report_sheets.xls`: one filled workbook containing the corresponding report sheets for a sequence
- Instrument method TXT exports placed beside the CMBX are treated only as reference material for human comparison; they are not the source for method export.

## Dependencies

The package/header browser can run without Chromeleon. Raw signal export, audit trail decoding, and `CpXm` method/report XML decoding still need Chromeleon runtime DLLs.

Runtime lookup order:

1. `CMBX_CHROMELEON_BIN` environment variable
2. `cmbx_data_explorer/dependencies/chromeleon`
3. `cmbx_data_explorer/dependencies/chromeleon/bin`
4. Local Chromeleon installation folders under `Program Files`

The internal server deployment contains an approved minimal Chromeleon runtime
closure under `deployment/runtime/chromeleon-runtime.zip`. The installer deploys
it to ProgramData and the launcher sets `CMBX_CHROMELEON_BIN`. This bundle is for
internal Thermo Fisher use only and is not a public redistributable or a
replacement for a licensed Chromeleon installation.

## Report Sheets

Audit trails are still exposed as low-level injection audit objects, but the report model now has a first working layer: report template -> sheets -> sheet objects. The UI decodes sequence-level report definitions, lists every sheet, counts formula/object usage, and evaluates simple injection-name rules such as `Contains Temperature Accuracy` against the selected injection.

The Report Sheets tab is now the rendered report-output path. It uses the real FormulaOne template stored in CMBX, fills known calculated values, and exports Excel 5 `.xls`.

The first formula evaluator supports:

- `AUDIT.RetTimeN(1,"forward")`
- `AUDIT.<device>.<property>(time_expression)`, using the most recent audit property value at or before the requested time
- `AUDIT.<device>.<property>(time_expression,"forward")`, using the next audit property value at or after the requested time
- `RetTime` arithmetic such as `AUDIT.RetTime2(...)-AUDIT.RetTime1(...)`
- `chm.sig_value("average" / "min" / "max" / "drift" / "stddev", start, end)`, using the formula object's `FixedChannel`
- `chm.signalStatistic("average" / "min" / "max", start, end)`
- `chm.signalValue(time)`
- `chm.noise(start, end)`, modeled as detrended peak-to-peak noise
- `chm.drift(start, end)`, modeled as a linear regression slope

For `6545327.cmbx`, the current FOQ contract comparison against CM-exported `.xls` reports has:

```text
matched: 76
small_numeric: 5
numeric_diff: 0
text_diff: 0
missing: 0
```

The remaining small numeric differences are limited to CM-internal signal-statistic details for noise and `chm.sig_value("drift", ...)`.

For the tested VTCC temperature accuracy report, this reproduces the nominal temperature cells and the upper/lower external thermometer average cells.

`Export Filled CM Report` writes `.xls` reports. With an injection selected, it exports that injection's report sheets. With a sequence selected, it exports one workbook containing the corresponding report sheets for the sequence.

Report workbooks also include a `Calculation Map` sheet when known calculation relationships are detected. This sheet documents the derived-cell logic separately from raw formula cells, for example:

- `Definitions` criteria decoded from the embedded FormulaOne `SpreadSheetData` table, such as `Temperature Accuracy = 0.5` and `HeatUp & Cool Down = 15`.
- `Temp Accuracy!D26 = max(abs(D66:D70))`, compared with the `Definitions` temperature accuracy criterion.
- `HeatUp&CoolDown!D65` / `D66` as time differences based on start/end RetTime-derived cells with the 2 minute hold-time subtraction, and `D26` / `D27` as the summary pass/fail comparison against the shared criterion.

Workbook filenames are intentionally short, e.g. `Report_VTCC_V2_12_report.xlsx`, because Windows path length limits can be reached quickly under OneDrive project folders. The sequence and injection names are preserved in the folder path.

`Export FOQ DB` reads `FOQResultLocations_V2.83.xls`, resolves the selected device type to its mapping sheet, matches `xlsReportFile` entries to CMBX injections, evaluates only the requested report sheets/cells, applies verified report-display precision, and writes a workbook with:

- `DB Data`: one database-ready row keyed by `dbField`
- `Mapping Coverage`: counts of OK, missing, and unsupported fields
- `Cell Values`: per-field traceability back to report file, sheet, cell, injection, value, status, and detail
- `Dependency Trace`: reverse dependency tiers from final `dbField` cell back to derived cells, CM formula cells, definition criteria, audit records, and raw signal sources

For the tested `VH-C10-A` CMBX, mapped values such as `TempAcc20`, `HeatUp_Time_20to50`, `CoolDown_Time_50to20`, `RES_HeatUp`, and `RES_CoolDown` are populated from the CMBX report data and derived-cell rules. Fields from report sheets that have not yet been mapped to dedicated calculation rules are reported as `missing_cell` or `unsupported` rather than guessed.

Report export now caches decoded report XML and reuses each injection's decoded audit/signal data while building all sheets in the same workbook. The UI status line reports the current stage, such as template decoding, sheet evaluation, and workbook writing, so long exports are easier to diagnose.

`Upload Candidate DB` generates one DB workbook per candidate sequence and uploads those rows to SQL Server. With table set to `AUTO`, TCC C10 devices currently route to `dbo.VTCC` in `QCLab`.

The code is intentionally independent from the TCC temperature control analyzer. TCC CMBX files are used only as validation data.
