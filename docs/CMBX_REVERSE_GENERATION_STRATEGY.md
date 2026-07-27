# CMBX Reverse Generation Strategy

This document describes the working reverse path from existing CMBX packages toward generated automation packages containing sequence, injections, instrument methods, processing methods, and reports.

The first target family is TCC because VA/VC/VH samples, TD documentation, report templates, method flows, audit data, and raw data are now available locally.

## Final Goal

Generate a runnable CMBX-style automation package that contains:

1. Sequence structure.
2. Injection list.
3. Instrument method logic.
4. Processing method logic.
5. Report templates and report-sheet formulas.
6. Raw/audit/report dependency expectations.
7. DB mapping compatibility.

The immediate practical path is not to invent binary payloads from scratch. The first generator should operate from a known-good golden CMBX structure, then make controlled substitutions.

For the first runnable TCC milestone, do not block on recreating every visible sequence-grid field. Fresh generated injections can rely on CM defaults or later user editing for preview thumbnails, injection type, status, injection time, comments, and similar UI metadata. The execution-critical fields are:

```text
injection name
instrument method
processing method where needed
target instrument configuration compatibility
```

The higher-value reverse path is:

```text
instrument method command generation
-> generated raw/audit/RetTime evidence
-> report formula/workbook calculation
-> DB output/upload compatibility
```

## Why Golden-CMBX First

CMBX files contain Chromeleon-specific binary method payloads, FormulaOne workbook payloads, report XML, sequence command objects, audit and raw-data references, and hierarchy metadata. Some of these payloads can be decoded, but writing every binary format from scratch is not yet validated.

Therefore the safer first generation mode is:

```text
golden CMBX
-> decode sequence/method/report structure
-> apply controlled edits or swaps
-> re-pack with preserved binary payload families
-> validate in CMBX Data Explorer and then Chromeleon
```

This lets us generate useful packages while the deeper binary writer is still being reverse engineered.

## Reverse Path

### 1. Inventory

For each source CMBX:

```text
header.xml
-> sequence tree
-> injection elements
-> sequence command object
-> instrument method objects
-> processing method objects
-> report template objects
-> raw channel and audit objects
```

Current local parser:

```text
cmbx_container.py
sequence_cmd_parser.py
embedded_method_extractor.py
embedded_report_extractor.py
```

### 2. Decode Method Logic

Instrument methods are extracted from the sequence command object, the CpXm payload is decoded through the local Chromeleon `Dionex.DataCommon.dll`, and the XML is converted into a flow table.

Current output shape:

```text
*_embedded_method.xml
*_embedded_method_flow.txt
*_embedded_method_flow.tsv
```

The flow rows expose:

```text
stage
order
action
target symbol path
value
condition
comments
```

Generation implication:

```text
method requirement
-> command graph
-> CM-like flow table
-> eventually CpXm/binary payload
```

### 3. Decode Report Logic

Report templates contain:

```text
ReportDefinition XML
FormulaOne workbook SpreadSheetData
ReportFormulaObject formulas
ReportTableObject definitions
sheet print/layout settings
```

Current report calculation path:

```text
DB mapping field
-> report sheet/cell
-> direct ReportFormulaObject or known workbook-derived formula
-> AUDIT/precond/seq/chm source
-> raw channel or audit row
```

Generation implication:

```text
DB requirement
-> report output cell
-> formula dependencies
-> required method RetTimes/channels/audit properties
```

### 4. Bind Sequence to Methods

The sequence command object stores the injection-to-method links. A generated package needs a sequence blueprint such as:

```text
Injection name
Processing method name
Instrument method name
Report template applicability
Expected raw channels
Expected audit source
```

TCC already proves this is device-specific: VA, VC, and VH do not have identical injection lists or processing-method links.

### 5. Validate Round Trip

For each generated candidate:

1. Load package in CMBX Data Explorer.
2. Verify sequence tree and injection links.
3. Decode method flows.
4. Decode report templates.
5. Evaluate report formulas against known raw/audit samples where available.
6. Build FOQ DB output.
7. Compare to known DB/report values.

### 6. Validate Target Instrument Configuration

Before a generated package can be considered runnable in Chromeleon, validate that the target CM instrument configuration exposes every required device, property, command, and channel.

For TCC this includes, depending on selected tests:

```text
ColumnComp
ColumnComp.CC
ColumnComp.PCC
ColumnComp.UpperValve
ColumnComp.LowerValve
ColumnComp.PrehtLeft
ColumnComp.PrehtRight
Thermometer1.ExtTemp_UpperCC
Thermometer1.ExtTemp_LowerCC
Thermometer.Environment_Temperature
```

Official qualification checks identify Vanquish TCC via `DriverID = Thermo.Vanquish.TCC`, and identify the CC/sCC/PCC and upper/lower valve subdevices by internal names such as `0:CC`, `0:sCC`, `0:PCC`, `0:UpperValve`, and `0:LowerValve`.

Generation implication:

```text
method blueprint
-> required-symbol manifest
-> validate against CMBX audit/channel evidence
-> later validate against live CM configuration
-> only then generate runnable package
```

## TCC First Milestone

TCC sources now decoded:

```text
knowledge_base/tcc_reverse_probe/VA
knowledge_base/tcc_reverse_probe/VC
knowledge_base/tcc_reverse_probe/VH
```

All three current production samples decoded 14 instrument methods successfully.

Known TCC report templates:

```text
VA-C10-A -> Report_VATCC_V1_01
VC-C10-A -> Report_VTCC_V2_12
VH-C10-A -> Report_VTCC_V2_12
```

Known device key:

```text
AUDIT.ColumnComp.ModelNo
```

Known sequence blueprint:

```text
cmbx_data_explorer/docs/TCC_FOQ_METHOD_REPORT_KNOWLEDGE_BASE.md
```

Known configuration evidence:

```text
cmbx_data_explorer/docs/CM_INSTRUMENT_CONFIGURATION_KNOWLEDGE_BASE.md
cmbx_data_explorer/docs/TCC_REQUIRED_SYMBOL_MANIFEST.md
```

## Method Generation Schema Draft

A generated method can be represented as:

```text
MethodDefinition
  name
  device_applicability
  stages
    stage_name
    steps
      action: SET | RUN | IF | ELSE | END_IF | TRIGGER | COMMENT
      target
      value
      condition
      timing
      comment
  required_channels
  emitted_ret_times
  emitted_audit_properties
  report_dependencies
```

Example, TCC valve cycle:

```text
SET ColumnComp.UpperValve.CurrentPosition = 6_1
SET ColumnComp.LowerValve.CurrentPosition = 6_1
RUN Log UpperValve.Precision
RUN Log LowerValve.Precision
SET ColumnComp.UpperValve.CurrentPosition = 1_2
SET ColumnComp.LowerValve.CurrentPosition = 1_2
```

The command paths above are verified from decoded TCC `VALVES` methods.

## Package Generation Levels

### Level 1: Clone and Select

Use a golden CMBX for the same module family.

Allowed operations:

- choose device blueprint
- choose existing report template
- choose existing injection list
- choose existing method payloads
- rename sequence/package
- update metadata where safe
- validate required instrument symbols against the target module/configuration

This is the safest near-term path.

### Level 2: Clone and Swap

Use a golden CMBX, but replace one or more method payloads with payloads from another known CMBX or method library.

Allowed operations:

- swap `VALVES`
- swap `PREHEATER`
- swap `TEMPERATURE_*`
- adjust injection-to-method links
- preserve report template and workbook payloads

This requires reliable sequence command editing.

### Level 3: Flow-to-Method

Generate a method from a method-flow schema, then encode it back into Chromeleon method payload format.

Current status:

- Decoding works.
- Semantic flow representation works.
- Encoding decoded XML back to CpXm through local Chromeleon `Dionex.DataCommon.dll` is validated for standalone exported instrument-method CMBX files.
- Rebuilding a standalone two-entry method CMBX from edited decoded XML is validated with `TEMP_HEAT_UP_DOWN_20_50_20.cmbx`.
- Plain Markdown/Excel script rows are not yet a validated authoring source because they do not preserve every CM XML node type, node ID, nesting relationship, and editor metadata required for lossless XML reconstruction.
- A generated method must also pass target-instrument configuration validation before it is considered runnable.

### Level 4: Full Synthetic CMBX

Generate every major CMBX component from structured definitions.

Open items:

- binary method writer
- processing method writer
- FormulaOne workbook writer with full style/layout fidelity
- report-template XML writer
- sequence command writer
- Chromeleon validation workflow

## Immediate Next Tasks

The semantic generation layer is now documented in:

```text
cmbx_data_explorer/docs/CMBX_SEMANTIC_GENERATION_MODEL.md
cmbx_data_explorer/docs/CMBX_CLONE_SELECT_GENERATOR.md
cmbx_data_explorer/docs/SEQUENCE_CMD_REVERSE_ENGINEERING.md
cmbx_data_explorer/docs/CM_SEQUENCE_UI_OBSERVATIONS.md
knowledge_base/tcc_semantic_test_catalog.json
knowledge_base/tcc_semantic_blueprint_validation_20260708.md
```

Method command contracts are tracked in:

```text
cmbx_data_explorer/docs/TCC_METHOD_COMMAND_CONTRACTS.md
knowledge_base/tcc_method_contracts
```

1. Compare VA/VC/VH decoded method flows method-by-method and record stable vs device-specific command paths.
2. For each TCC test intent, define the method command contract:
   - required symbols and channels
   - command sequence
   - RetTimes emitted
   - audit properties logged
   - report dependencies satisfied
3. Decode processing method IRC row data beyond the currently extracted editor-layout XML, or preserve golden processing payloads by module family.
4. Use `tcc_semantic_test_catalog.json` to generate candidate execution plans from selected tests or DB fields.
5. Validate every candidate against `tcc_required_symbol_manifest.json`.
6. Add a generator prototype that creates a candidate folder/package from a golden TCC CMBX without changing binary method payloads.
7. Add validation reports:
   - structure match
   - method flow match
   - report template match
   - DB mapping coverage
   - required CM configuration symbols
