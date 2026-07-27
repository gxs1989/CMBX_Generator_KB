# CMBX Parsing Notes

This note documents the CMBX structures currently understood by CMBX Data Explorer.

## Package Structure

- A `.cmbx` file is a ZIP-like Chromeleon package.
- `header.xml` describes the visible object tree:
  - Sequence
  - Injection
  - Signal channels
  - Audit trails
  - Instrument methods
  - Processing methods
  - Report templates
- Signal and audit objects usually point to raw data entries through `RawDataFilename`.
- The sequence object points to a `.seq_*.cmd` entry. This command object contains important relationship data that is not fully visible in `header.xml`.

## Local Chromeleon Dependency

The tool is only partially independent from a local Chromeleon installation today.

Can run without Chromeleon DLLs:

- Open the CMBX container.
- Read `header.xml`.
- List sequences, injections, channels, audit objects, method objects, processing methods, and report templates.
- Inspect package entries and some embedded gzip/XML fragments.
- Discover some injection-to-method links from the sequence `.cmd` object.

Still depends on Chromeleon runtime DLLs:

- Raw signal decoding/export from `.raw` files.
- Audit trail decoding/export from audit `.raw` files.
- `CpXm` instrument method and report definition body decoding through `Dionex.DataCommon.dll`.

Runtime resolution order:

1. `CMBX_CHROMELEON_BIN` environment variable.
2. `cmbx_data_explorer/dependencies/chromeleon`.
3. `cmbx_data_explorer/dependencies/chromeleon/bin`.
4. Local Chromeleon installation folders under `Program Files`.

This means the code can run from a standalone dependency folder if an approved runtime package is provided. A full local Chromeleon installation is not technically required once the needed DLLs are available through one of the paths above.

To make the tool legally and operationally standalone, we would need either:

- an independently implemented decoder for Chromeleon raw signal, audit trail, and `CpXm` method bodies, or
- a small redistributable/runtime dependency approved for these Chromeleon libraries.

The current code does not bundle Thermo/Chromeleon DLLs. It calls DLLs from a local Chromeleon installation when they are present.

## Sequence, Injection, And Channel Mapping

- Sequence and injection names are read from `header.xml`.
- Raw signal exports use the local Chromeleon raw-data DLL bridge.
- Audit trail exports use the local Chromeleon audit decoder.
- Injection-to-method links are discovered from the sequence `.cmd` object by scanning nearby relative URL/name records.

## Report Template And Audit Trail Relationship

Audit trails should be treated as report data, not only as an independent injection object.

Current behavior:

- The UI lists audit raw objects under each injection.
- The UI lists report templates linked at the sequence/report-template level.
- The UI decodes report definitions from embedded sequence `.cmd` `CpXm` payloads and lists all workbook-like report sheets for the selected injection.
- The report sheet parser reads `SheetList` plus `PrintSheetSetups`, including `IsActive`, `EachInjection`, and common injection-name query rules.
- The report object parser reads `SheetDescription` plus direct `SheetObject` entries. It exports object type, decoded range, formulas, fixed channel, plot type, and table type.
- Audit export is currently a direct audit raw TSV export.

Current report model:

- Treat each injection report as a workbook-like object.
- A report template can contain multiple sheets.
- The audit trail is expected to be one sheet/view inside that report output.
- Other report sheets are now discovered and exposed next to the audit sheet.

This means the current `Audit Trails` tab is a useful low-level raw view, while the `Report Sheets` tab is the higher-level structural report view. The tool does not yet render the full Chromeleon report workbook or export individual sheet output exactly as Chromeleon would print it.

Report object export:

- `ReportFormulaObject` entries expose formulas such as `chm.sig_value("average",AUDIT.RetTime1(1,"forward")-1,AUDIT.RetTime1(1,"forward")-0.2)` with `FixedChannel` values such as `ExtTemp_LowerCC` and `ExtTemp_UpperCC`.
- `PlotObject` entries expose plot metadata such as `PlotType`.
- `ReportTableObject` entries expose table metadata such as `ReportTableType` and nested formulas.
- Coordinates are exported as raw zero-based `Left/Top/Right/Bottom` plus an Excel-style range approximation for review.

Formula evaluation layer:

- The low-level evaluator calculates supported report formulas for the selected injection.
- The app UI now uses these values through filled CM report export and the FOQ DB workbook export rather than exposing a separate formula-values button.
- It decodes the injection audit raw file to recover `RetTimes.RetTime1..5` and audit property history.
- It decodes fixed raw signal channels on demand, then calculates `chm.sig_value("average", start, end)` over the exported `Time (min)` axis.
- It models `chm.drift(start, end)` as a linear regression slope over raw points in the requested window.
- It models `chm.noise(start, end)` as peak-to-peak residual after subtracting a linear trend.
- It reads `seq.update_time` from the sequence command payload when available, returning the Excel serial date used by CM reports.
- For the tested `Temp Accuracy` sheet:
  - `I66:I70` are reproduced from `AUDIT.ColumnComp.CC.Temperature.Nominal(AUDIT.RetTimeN(...) - 0.1)`.
  - `L66:L70` are reproduced from `ExtTemp_LowerCC` average windows.
  - `M66:M70` are reproduced from `ExtTemp_UpperCC` average windows.
  - The average windows are `RetTimeN - 1.0` to `RetTimeN - 0.2` min.

Supported formula types in the first evaluator:

- `AUDIT.RetTimeN(1,"forward")`
- `AUDIT.<device>.<property>(time_expression)`
- `AUDIT.<device>.<property>(time_expression,"forward")`
- `AUDIT.RetTimeN(...)-AUDIT.RetTimeM(...)`
- `chm.sig_value("average" / "min" / "max" / "drift" / "stddev", start, end)`
- `chm.signalStatistic("average" / "min" / "max", start, end)`
- `chm.signalValue(time)`
- `chm.noise(start, end)` as detrended peak-to-peak noise
- `chm.drift(start, end)` as linear regression slope
- literal quoted text and simple metadata such as `injection.name` and `seq.name`

Unsupported report formulas are exported with `unsupported` status rather than silently ignored.

Workbook report export:

- The Report Templates tab exports only the blank FormulaOne `.xls` report template stored in CMBX.
- The Report Sheets tab exports filled FormulaOne `.xls` reports.
- With an injection selected, Report Sheets exports that injection's matching report sheets.
- With a sequence selected, Report Sheets exports one workbook containing the corresponding report sheets for the sequence.
- The exporter expands `SpreadSheetData` through Chromeleon's 32-bit FormulaOne runtime, writes calculated values back into the original template cells, and exports selected sheets as Excel 5 `.xls`.
- The verified `Temperature Accuracy_H` export from `6545327.cmbx` matches the CM-exported sheet set:
  - `Definitions`
  - `Title`
  - `Test Procedures`
  - `Temp Accuracy`
  - `Temp Precision`
  - `COC`
  - `FOQ VTCC History`
- Key cells such as `Temp Accuracy!D26/E26/L66/M66/N66` match the CM export within normal floating-point tail differences. The remaining work is to generalize all sheet-selection rules beyond the current FOQ heuristics.

Report calculation layers:

- Direct raw-data formulas are exposed as `SheetDescription/SheetObject` XML entries. These are the cells we already evaluate from audit trails and raw channels.
- Derived cells such as `HeatUp&CoolDown!D65` and summary/pass-fail cells such as `D26` are not exposed as `SheetObject` formulas. They live in the embedded FormulaOne workbook payload under `SpreadSheetData`.
- The tool now reads the `SpreadSheetData` payload enough to recover known `Definitions` criteria, for example:
  - `Temperature Accuracy = 0.5`
  - `Temperature Stability = 0.05`
  - `Temperature Precision = 0.1`
  - `HeatUp & Cool Down = 15`
  - `PCC CoolDownTime = 2`
- Generated workbooks include a `Calculation Map` sheet when known relationships are recognized. This maps raw formula cells, derived cells, shared definition criteria, and pass/fail rules.
- For `HeatUp&CoolDown`, the mapped relationship is:
  - `D65 = End Time - Start Time - 2.0 min stable-hold time`
  - `D66 = End Time - Start Time - 2.0 min stable-hold time`
  - `D26` summarizes `D65` and compares it with `Definitions!HeatUp & Cool Down`
  - `D27` summarizes `D66` and compares it with `Definitions!HeatUp & Cool Down`
- A fully general FormulaOne formula parser is still a future step. The current reliable path is to evaluate known report formulas and workbook-derived rules in Python, then write those values into the real FormulaOne template before Excel export.

FOQ database target mapping:

- `foq/FOQResultLocations_V2.83.xls` is the existing FOQ database field/location contract.
- `DeviceTypes` maps a device type such as `VH-C10-A`, `VC-C10-A`, or `VN-C10-A` to a device-specific mapping sheet.
- Device-specific sheets use a stable table structure:
  - `dbField`
  - `Description`
  - `ReportValue`
  - `LowerLimit`
  - `UpperLimit`
  - `LimitCheck`
  - `xlsReportFile`
  - `xlsReportSheet`
  - `xlsReportCell`
  - `ValueType`
  - `Unit`
- Traditional FOQ export reads finished `.xls` report files by `xlsReportFile + xlsReportSheet + xlsReportCell`.
- CMBX Data Explorer should reuse the same contract as a target schema:
  - identify the device type,
  - load the corresponding FOQ mapping sheet,
  - evaluate only the mapped report cells that are expected to enter the database,
  - emit a database-ready row keyed by `dbField`.
- For the tested VTCC mapping (`VH-C10-A`), important mapped cells include:
  - `Temp Accuracy!D67:D70` for temperature accuracy deviations and `E26` for `RES_TempAccuracy`
  - `HeatUp&CoolDown!D26:D27` for heat-up/cool-down observed time and `E26:E27` for pass/fail
  - `Temp Stability_Noise!D26`, `K86`, `K87`
  - `PCC!D26`, `L89:L91`, `K97`
- A parser module (`foq_result_locations.py`) now reads this workbook into structured mapping rows. The next CMBX report intelligence layer can use those rows to decide which compact layouts or derived-cell rules are required.
- `Export FOQ DB` now applies this contract directly:
  - one output workbook is generated per CMBX package/device type,
  - `xlsReportFile` is matched to the closest CMBX injection name,
  - only mapped `xlsReportSheet` values are evaluated,
  - direct `SheetObject` formulas and known derived-cell rules are converted into a report cell value map,
  - the final `DB Data` sheet is keyed by `dbField`,
  - unresolved fields remain visible in `Cell Values` with `missing_cell`, `missing_injection`, or formula `unsupported` status.
- The output also includes `Dependency Trace`, which follows the reverse workflow:
  - start from the final DB field and `xlsReportSheet!xlsReportCell`,
  - identify whether the value is a direct CM `SheetObject` formula, a known derived workbook cell, or an unresolved FormulaOne cell,
  - list any definition/criterion dependency,
  - list intermediate cells such as `Temp Accuracy!D66:D70` or `HeatUp&CoolDown!D65`,
  - list CM formula cells such as `chm.sig_value(...)` or `AUDIT.RetTimeN(...)`,
  - list raw data sources such as audit RetTimes, audit property history, or raw signal channels.
- This makes the contract table the source of truth for what must eventually enter the database. New report-specific calculation rules should be prioritized by looking at unresolved mapped fields, not by trying to render every report cell.

Observed sheets in the tested VTCC report include:

- `Definitions`
- `Title`
- `Test Procedures`
- `Temp Accuracy`
- `Temp Precision`
- `Temp Stability_Noise`
- `PCC`
- `Preheater Ports_Noise`
- `HeatUp&CoolDown`
- `Fan`
- `Valve_Keypad`
- `Column ID`
- `Liquid Leak Test`
- `COC`
- `FOQ VTCC History`
- `Internal Use`
- `Temp_Calib_Internal`
- `Audit Trail`
- `Error Log`

For injection `Temperature Accuracy_H`, the parser identifies `Temp Accuracy` as applicable through the report setup rule `injname Contains Temperature Accuracy`.

## Embedded Instrument Method Extraction

Instrument method header objects in `header.xml` do not normally expose a standalone method file. The real method body is embedded in the sequence `.cmd` binary.

Observed layout in the tested Chromeleon package:

1. Method definition headers contain fields such as:
   - method name
   - Chromeleon version
   - method description
2. The actual method body is stored as a nested field-11 payload near the method definition boundary.
3. For the tested package, the payload for a method is linked to the next readable method header boundary, so extraction first looks for the previous parseable record whose field-11 payload ends exactly at the selected method header.
4. The method payload contains an inner field-3 block beginning with `CpXm`.
5. The `CpXm` block is decoded through the installed Chromeleon `Dionex.DataCommon.dll` internal `XmlCompressor.Uncompress(byte[])` method.

Exported method files:

- `*_embedded.instmeth.bin`: extracted binary method block
- `*_embedded_payload.bin`: nested method payload wrapper
- `*_embedded_payload.cpxm.bin`: inner `CpXm` method body
- `*_embedded_method.xml`: decoded Chromeleon method XML
- `*_embedded_method_flow.txt`: readable flow summary
- `*_embedded_method_flow.tsv`: Excel-friendly flow table
- `*_embedded_metadata.txt`: byte ranges, sizes, readable strings, and decode status

## Method Flow Table

The TSV flow table is intended for review, filtering, and copy/paste through Excel. It does not claim to be a native Chromeleon import format.

Columns:

- `Method`
- `Order`
- `Level`
- `Stage`
- `Time`
- `NodeType`
- `Action`
- `Target`
- `Value`
- `Comment`
- `Condition`

Typical rows:

- `COMMENT`: method comments
- `SET`: property assignments such as temperature setpoints
- `RUN`: command steps such as `Wait` or `System.Trigger`
- `IF` / `ELSE IF` / `ELSE` / `END IF`: branch structure
- `STAGE` / `TIME`: method grouping markers when present in XML
- `END`: terminal CM method boundary row

CM-like preview rendering:

- The app-level preview renders `# / Kind / Time / Command / Value / Comment`.
- `Kind` is structural metadata. `Kind=Comment` means the green/header row is a CM comment row even when its text is displayed in the visual `Command` column. `Kind=Command` means an executable command/property row.
- Stage duration is calculated from the first and last finite `TimeStepNode` inside the stage and rendered as `Duration = ... [min]` on the stage row.
- The readable `Condition` value is taken from the branch node's direct `Condition` child, not from descendant command values.
- Descendant commands inside branches remain separate rows.

## Known Limits

- Processing method decoding is still treated as generic embedded object/XML extraction.
- The method flow TSV is a readable reconstruction from decoded XML, not a guaranteed one-to-one Chromeleon script export.
- Some condition expressions may still have editor-specific formatting not represented in decoded XML, but descendant command values are no longer folded into the condition line.
- The `CpXm` decoder depends on local Chromeleon DLLs being installed.
- Plain four-column Markdown/Excel method script exports are a display layer. They are not currently a lossless method-authoring source because CM branch/trigger node type, node nesting, node IDs, and some editor metadata live in decoded method XML.

## Standalone Instrument Method CMBX Repack

Chromeleon can export a single instrument method as a small CMBX containing only:

- `header.xml`
- `<method>.instmeth_1.cmd`

For `TEMP_HEAT_UP_DOWN_20_50_20.cmbx`, the standalone method CMBX has one `Dionex.Chromeleon.Data.InstrumentMethod` element and no sequence/injection/channel/audit entries.

Validated local round trip:

```text
standalone CMBX
-> extract .instmeth_1.cmd
-> locate nested method payload field 19 / field 11
-> locate inner field 3 CpXm payload
-> decode CpXm through Dionex.DataCommon.dll XmlCompressor.Uncompress(byte[])
-> edit decoded method XML
-> encode XML through XmlCompressor.Compress(string)
-> rebuild nested protobuf length fields
-> write a new two-entry CMBX
```

Validation results for the HEATUP template:

- Unmodified XML recompressed to byte-identical CpXm.
- Repacked unmodified `.instmeth_1.cmd` was byte-identical to the original.
- A comment edit changed `.cmd` length from `22492` to `22510` bytes and decoded back successfully with the edited comment present.

Prototype tooling:

- `cmbx_data_explorer/chromeleon_method_encoder.py`
- `cmbx_data_explorer/tools/repack_standalone_instmeth_cmbx.py`

Important boundary:

- The proven write path is **decoded XML -> CpXm -> standalone instrument-method CMBX**.
- The unproven path is **plain MD/Excel method script -> decoded XML**.
- A safe MD-to-CMBX workflow should therefore be template-guided:
  1. decode a real exported method CMBX to XML,
  2. apply edits to XML nodes using stable role IDs or node IDs,
  3. repack the XML into the standalone CMBX carrier,
  4. import into CM and verify on the target instrument configuration.

## Extension Points

- Add parsers for processing method objects.
- Add rendered report sheet extraction/export once the Chromeleon report workbook output format is mapped.
- Continue comparing the Chromeleon-style method script renderer against additional method XML variants.
- Use the same CMBX package reader for non-TCC workflows by adding analysis modules on top of exported raw signal/audit/method data.
