# TCC Method Command Contracts

This document summarizes the structured contract layer extracted from decoded TCC instrument method flows.

## Purpose

The command contract is the bridge between:

```text
semantic test intent
-> executable Chromeleon instrument method
-> raw channels, RetTimes, and audit evidence
-> report formulas and DB output
```

It intentionally ignores sequence-grid UI metadata such as status, injection time, comments, and preview thumbnails.

## Extractor

Code:

```text
cmbx_data_explorer/method_contract.py
```

Inputs:

```text
*_embedded_method_flow.tsv
```

Outputs:

```text
knowledge_base/tcc_method_contracts/VA_0000003_method_contracts.tsv
knowledge_base/tcc_method_contracts/VC_3000004_method_contracts.tsv
knowledge_base/tcc_method_contracts/VH_6000001_method_contracts.tsv
knowledge_base/tcc_method_contracts/VA-C10-A_test_intent_method_report_coverage.tsv
knowledge_base/tcc_method_contracts/VC-C10-A_test_intent_method_report_coverage.tsv
knowledge_base/tcc_method_contracts/VH-C10-A_test_intent_method_report_coverage.tsv
```

Selected per-method summaries:

```text
knowledge_base/tcc_method_contracts/VH_6000001_VALVES_contract.md
knowledge_base/tcc_method_contracts/VH_6000001_TEMPERATURE_ACCURACY_contract.md
knowledge_base/tcc_method_contracts/VH_6000001_TEMP_HEAT_UP_DOWN_20_50_20_contract.md
knowledge_base/tcc_method_contracts/VH_6000001_TEMPERATURE_STABILITY_AND_PCC_70_H_contract.md
```

## Contract Fields

Each `MethodContract` records:

```text
method_name
stages
set_symbols
run_commands
acquisition_on
acquisition_off
ret_time_initializations
ret_time_emissions
logged_properties
wait_conditions
trigger_definitions
temperature_setpoints
required_symbol_roots
```

The first pass is conservative. It does not generate Chromeleon payloads yet; it only records what the decoded method already does.

## Example: VALVES

`VALVES` is an important simple method because it does not rely on RetTimes.

Observed contract:

```text
sets ColumnComp.UpperValve.CurrentPosition
sets ColumnComp.LowerValve.CurrentPosition
runs ColumnComp.CC_Temp.AcqOn / AcqOff
logs UpperValve.Precision
logs LowerValve.Precision
disconnects and reconnects ColumnComp for keypad checks
waits for ColumnComp.Connected = Connected
```

Generation implication:

```text
required configuration:
  ColumnComp
  ColumnComp.CC_Temp
  ColumnComp.UpperValve
  ColumnComp.LowerValve

report evidence:
  audit log entries for UpperValve.Precision
  audit log entries for LowerValve.Precision
```

No `RetTimes.RetTimeN` are emitted by this method.

## Example: HeatUp/CoolDown

`TEMP_HEAT_UP_DOWN_20_50_20` emits the key RetTimes used by the report.

Observed contract:

```text
acquires ColumnComp.CC_Temp and CC internal/debug channels
acquires Thermometer1.ExtTemp_UpperCC
acquires Thermometer1.ExtTemp_LowerCC
acquires Thermometer.Environment_Temperature
sets ColumnComp.CC.Temperature.Nominal to 17, 20, 50, and 20 C phases
uses System.Trigger for external/internal 20 C and 50 C windows
emits RetTimes.RetTime1 through RetTimes.RetTime6
waits for CC.TempReady
```

Report dependency bridge:

```text
HeatUp report source cells read RetTime1, RetTime3, RetTime4, RetTime6
summary workbook rule calculates:
  HeatUp_Time_20to50 = RetTime2 - RetTime1 - 2.0 min
  CoolDown_Time_50to20 = RetTime5 - RetTime4 - 2.0 min
  RetTime3/6 remain required as internal endpoint evidence in the visible report
  layout.
```

This is the exact pattern needed for semantic generation:

```text
method emits RetTimes
report reads RetTimes
DB mapping exports workbook-derived result
```

## Example: Temperature Accuracy

`TEMPERATURE_ACCURACY` is a richer method:

```text
sets CC readiness and equilibration parameters
sets model-dependent temperature targets
acquires CC internal/debug channels
acquires external thermometer channels
waits for CC.TempReady
waits for external stability variables
emits RetTimes.RetTime1 through RetTimes.RetTime5
```

Report dependency bridge:

```text
report formulas read ExtTemp_UpperCC and ExtTemp_LowerCC windows around RetTimes
workbook rules compare observed values to nominal setpoints
DB fields export observed temperatures, deviations, and pass/fail result
```

## Example: Temperature Stability With PCC

`TEMPERATURE_STABILITY_AND_PCC_70_H` adds PCC-specific requirements:

```text
requires ColumnComp.PCC
acquires ColumnComp.PCC_Temp
acquires ColumnComp.PWM_PCC_A
acquires ColumnComp.PWM_PCC_B
sets ColumnComp.PCC.Temperature.Nominal
waits for CC.TempReady AND PCC.TempReady
initializes RetTimes.RetTime1 through RetTimes.RetTime4
emits RetTimes.RetTime2, RetTimes.RetTime3, RetTimes.RetTime4
logs PCC.Temperature.Value
```

Generation implication:

```text
this method must only be generated for configurations with PCC support
report formulas and DB mapping must use the PCC-compatible template branch
```

## Next Reverse Step

The first method/report coverage check now passes for all catalogued TCC intents:

| Device | Covered intents | Passed |
| --- | ---: | ---: |
| `VA-C10-A` | `11` | `11` |
| `VC-C10-A` | `13` | `13` |
| `VH-C10-A` | `13` | `13` |

This means the current semantic catalog's expected RetTimes, raw channels, and direct AUDIT dependencies are supported by the decoded method contracts.

Important correction from this check:

```text
TEMPERATURE_STABILITY_AND_PCC_70_H initializes RetTime1 but does not emit it with System.Retention.
The PCC/stability report dependency contract should use RetTime2, RetTime3, and RetTime4.
```

For each TCC `TestIntent`, create a durable contract:

```text
test_intent
instrument_method
processing_method
required configuration symbols
channels acquired
RetTimes emitted
audit properties logged
report sheets/cells satisfied
DB fields satisfied
```

This should become the central source for both:

```text
UI/semantic CMBX generation
report/DB validation
```
