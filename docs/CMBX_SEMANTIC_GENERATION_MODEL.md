# CMBX Semantic Generation Model

This document defines the intermediate model needed to generate CMBX automation packages from either UI selections or natural-language requirements.

The goal is to avoid jumping directly from a sentence such as:

```text
Run a TCC upper/lower valve cycling test and report the valve result.
```

to low-level Chromeleon binary payload edits. Instead, every generated package should pass through explicit, inspectable layers.

## Target Output

The final long-term generator can target several different output levels. These must not be mixed.

### Level A: Runnable Test Sequence

This is the minimal acquisition/execution package.

Required:

```text
sequence
injection rows
instrument method per injection
processing method per injection when IRC behavior is needed
target instrument configuration compatibility
```

For the current TCC work, this is the most important generation target. A TCC test sequence can run without solving report template generation first, as long as the injection rows, instrument methods, and required IRC processing methods are valid.

### Level B: Analysis and DB Output

This layer is for calculating results and uploading/exporting DB-compatible output.

Required:

```text
processing method result behavior when relevant
report template
report formulas
FormulaOne workbook-derived cells
DB mapping
display precision and value type rules
```

### Level C: Full CM-Like Package

This layer tries to reproduce Chromeleon's full visible sequence state.

Additional items:

```text
associated item library
view settings
report/print page layout
custom sequence variables
historical run status/inject time if replaying an existing package
```

This is useful for high-fidelity reverse generation, but not the minimum needed to run a new TCC test.

## Full Long-Term Output

A full generated CMBX package may eventually contain:

1. A sequence.
2. Injection rows.
3. Instrument method payloads.
4. Processing method payloads.
5. Report template payloads.
6. Report formula dependencies.
7. DB mapping/export compatibility.
8. Configuration prerequisites for the target Chromeleon instrument.

## Core Objects

### RequirementSpec

User-facing intent. This may come from UI checkboxes, selected DB fields, selected methods, or natural-language parsing.

Example:

```json
{
  "family": "TCC",
  "device_models": ["VH-C10-A"],
  "tests": ["upper_lower_valve_cycle"],
  "options": {
    "cycles": 10,
    "positions": ["6_1", "1_2"]
  }
}
```

### TestIntent

Normalized test semantics independent of one exact CMBX sample.

Examples:

```text
temperature_accuracy
temperature_precision
temperature_stability
temperature_stability_with_pcc
heatup_cooldown_20_50_20
preheater_connection
upper_lower_valve_cycle
column_id
liquid_leak
factory_default
error_log_check
```

Each `TestIntent` declares:

```text
required capability groups
required method template
required processing strategy
required report sheets/cells
required DB fields
required RetTimes
required raw channels
required audit properties
```

### DeviceConfiguration

The intended target Chromeleon configuration. This is not only the model name.

For TCC, important feature flags include:

```text
has_external_thermometers
has_pcc
has_preheater_left
has_preheater_right
has_upper_valve
has_lower_valve
has_column_id
has_leak_sensor
```

This layer is validated against:

```text
required-symbol manifest
CMBX audit/channel evidence
later: live CM instrument configuration
```

### SequenceBlueprint

Generated sequence plan.

Fields:

```text
sequence_name
device_model
report_template_name
processing_method_library
instrument_method_library
injections[]
```

The blueprint must be per device/model. VA, VC, and VH TCC packages do not use the same injection list or processing method bindings.

### ExecutionSequencePlan

The minimal runnable sequence layer.

Fields:

```text
row_order
injection_name
instrument_method_name
processing_method_name
test_intent
```

`row_order` is the intended Chromeleon sequence-grid order. Current TCC evidence shows that this order should come from the semantic catalog/header order, not from first readable-name occurrence offsets in the sequence `.cmd` payload.

This deliberately excludes:

```text
report template
DB fields
report sheet/cell mappings
FormulaOne workbook rules
print/page layout
historical status/inject time
```

For TCC, this is the first package-generation target.

### InjectionBlueprint

One injection row in the sequence.

Fields:

```text
injection_name
sample_name
replicate_count
sequence_row_order
sequence_type
sequence_status
sequence_comment
instrument_method_name
processing_method_name
report_sheet_scope
test_intent
expected_ret_times
expected_channels
expected_audit_properties
db_fields
```

Some of these fields are generation inputs and some are run-history outputs. Chromeleon's sequence grid displays historical state such as status and inject time after opening a run-finished CMBX. A fresh generator should preserve or set only the fields required for a runnable sequence, while treating historical state as optional replay/report metadata.

For generated untested TCC sequences, sequence-grid UI fields should default conservatively:

```text
sequence_type -> Unknown
sequence_status -> Idle
inject_time -> blank until CM execution
sequence_comment -> blank unless user supplies it
channel preview thumbnail -> omitted or regenerated by CM
```

These fields are intentionally lower priority than the instrument method and report calculation contract.

### InstrumentMethodBlueprint

A method-level command model.

Current generation mode:

```text
golden method payload
-> decoded flow table
-> controlled parameter edits or payload swaps
-> preserved binary method payload
```

Future generation mode:

```text
semantic method graph
-> command flow table
-> CpXm/method XML
-> Chromeleon method payload
```

For TCC, a method blueprint must expose command requirements such as:

```text
ColumnComp.CC.Temperature.Nominal
ColumnComp.CC.TempReady
ColumnComp.UpperValve.CurrentPosition
ColumnComp.LowerValve.CurrentPosition
ColumnComp.PrehtLeft.Temperature.Nominal
RetTimes.RetTimeN = System.Retention
channel.AcqOn / channel.AcqOff
```

This is now the main reverse-generation target: understand enough of the method command flow to generate or select methods that Chromeleon can actually execute on a compatible target configuration.

### ProcessingMethodStrategy

How to bind or generate the processing method.

For execution, processing methods matter primarily when they drive IRC behavior, such as stopping or inserting injections. For report/DB calculation, processing methods may also carry result behavior, but the current report calculation path mostly comes from report templates and raw/audit formulas.

Current status:

```text
preserve known-good processing method payloads from golden CMBX
bind the correct payload by name
```

Reason: current processing-method XML extraction exposes editor layout and SST/IRC column definitions, but not the actual SST/IRC row logic.

Future status:

```text
decode SST/IRC row payload
represent pass/fail and injection insertion rules as structured logic
generate processing method payloads directly
```

### ReportTemplateBinding

The report template is not optional metadata. It determines the SheetObject formulas, FormulaOne workbook calculations, display precision, pass/fail cells, and DB mapping coverage.

However, it is not part of the minimal execution-only sequence requirement. It belongs to the analysis/report/DB layer.

This is the second main target: once an instrument method creates the necessary raw channels, RetTimes, and audit properties, the report template/formula layer must calculate the same values CM would calculate.

Fields:

```text
template_name
sheet_names
report_formula_objects
workbook_derived_rules
formatting_rules
db_mapping_file
```

For TCC:

```text
VA-C10-A -> Report_VATCC_V1_01
VC-C10-A -> Report_VTCC_V2_12
VH-C10-A -> Report_VTCC_V2_12
```

### DBMappingBinding

Maps final report cells to database fields. This must stay aligned with the report template and device.

Fields:

```text
device_model
db_table
db_field
report_sheet
report_cell
source_formula
display_precision
sql_type
```

Device identity must be taken from:

```text
AUDIT.ColumnComp.ModelNo
```

## Generation Pipeline

The intended pipeline is:

```text
RequirementSpec
-> TestIntent set
-> DeviceConfiguration
-> capability validation
-> SequenceBlueprint
-> InjectionBlueprint list
-> method/report/processing payload binding
-> CMBX package assembly
-> static validation
-> formula evaluation validation
-> optional live CM validation
```

## Validation Gates

### Gate 1: Requirement Coverage

Every requested test must resolve to a known `TestIntent`.

### Gate 2: Device Capability

Every `TestIntent` capability group must be supported by the target device configuration.

Example:

```text
temperature_stability_with_pcc requires pcc
preheater_connection requires preheater
upper_lower_valve_cycle requires upper_lower_valves
```

### Gate 3A: Execution Sequence Completeness

Every injection must bind to:

```text
instrument method
processing method
test intent
```

This is the runnable TCC layer. It does not require a report template.

### Gate 3B: Analysis Sequence Completeness

Every DB/report-capable candidate must additionally bind to:

```text
report template
DB mapping
report formula/workbook dependencies
display precision rules
```

### Gate 4: Report/DB Coverage

Every selected DB field must resolve to a report template cell and trace back to formulas, raw channels, audit properties, or workbook-derived rules.

### Gate 5: Method/Report Agreement

Every report dependency must be produced by the method/sequence.

Examples:

```text
Report references AUDIT.RetTime3 -> method must log RetTimes.RetTime3
Report fixed channel ExtTemp_UpperCC -> sequence must acquire ExtTemp_UpperCC
Report reads AUDIT.ColumnComp.ModelNo -> audit/precondition must contain ModelNo
```

The first automated version of this gate is:

```text
cmbx_data_explorer/test_intent_contract.py
knowledge_base/tcc_method_contracts/*_test_intent_method_report_coverage.tsv
```

It checks that each selected TCC `TestIntent` has method support for expected RetTimes, acquired raw channels, and direct `AUDIT.*` dependencies.

### Gate 6: Target CM Configuration

The target instrument must expose the devices, properties, commands, and channels needed by all selected tests.

## Current TCC Implementation Level

Implemented knowledge:

```text
device model extraction from AUDIT.ColumnComp.ModelNo
TCC VA/VC/VH report template mapping
TCC sequence/injection/method binding from golden CMBX
TCC required-symbol manifest
TCC DB field calculation via report formulas and raw/audit data
```

Current generation strategy:

```text
golden-CMBX first
preserve method/report/processing payloads
swap or select known-good payloads by device and test intent
validate against formulas and DB output
```

TCC Temperature Accuracy single-point drafts must preserve the device-specific
FOQ ladder used by the black-box contract:

| Device branch | Accuracy ladder | DB fields |
|---|---|---|
| `VH-C10-A` | `10, 20, 40, 80, 120 deg C` | `TempAcc10`, `TempAcc20`, `TempAcc40`, `TempAcc80`, `TempAcc120`, `RES_TempAccuracy` |
| `VC-C10-A` | `10, 20, 40, 60, 85 deg C` | `TempAcc10`, `TempAcc20`, `TempAcc40`, `TempAcc60`, `TempAcc85`, `RES_TempAccuracy` |
| `VA-C10-A` | `10, 20, 40, 60, 85 deg C` | `TempAcc10`, `TempAcc20`, `TempAcc40`, `TempAcc60`, `TempAcc85`, `RES_TempAccuracy` |

The single-point generator therefore rejects branch-incompatible setpoints, for
example `80 C` on `VC-C10-A`, instead of silently emitting a mismatched
RetTime/report-cell contract.

Still missing:

```text
full binary CMBX writer
direct processing method row decoder/writer
full FormulaOne workbook formula writer
live Chromeleon configuration reader
semantic-to-method compiler for arbitrary new method logic
```

## Practical Next Step

For TCC, build a semantic catalog that maps:

```text
TestIntent
-> injection name per device
-> instrument method name
-> processing method name
-> report template
-> DB fields
-> capability groups
-> validation formulas/channels/RetTimes
```

The first catalog is:

```text
knowledge_base/tcc_semantic_test_catalog.json
```

The first validation against production VA/VC/VH golden CMBX samples is:

```text
knowledge_base/tcc_semantic_blueprint_validation_20260708.md
```

Chromeleon UI observations for the visible sequence grid and associated items are tracked in:

```text
cmbx_data_explorer/docs/CM_SEQUENCE_UI_OBSERVATIONS.md
```
