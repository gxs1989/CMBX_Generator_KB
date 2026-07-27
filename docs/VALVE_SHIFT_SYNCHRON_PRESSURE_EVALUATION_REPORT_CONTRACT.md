# EP01_6_2_valves -> PressureEvaluation Report Contract

**Purpose:** Define the verified method, processing, virtual-channel, and report-table contract for a GPT-authored valve-pressure test report.

## 1. Evidence Scope

| Role | Source | Verified object |
|---|---|---|
| Complete sequence | `EP01_6_2_valves.cmbx` | Six valve-test injections, ten instrument methods, `PressureSpikeEval`, and three report templates |
| Standalone report carrier | `PressureEvaluation.cmbx` | `PressureEvaluation` |
| Processing method | `EP01_6_2_valves.cmbx` | `PressureSpikeEval` |
| Related method family | `EP01_6_2_valves.cmbx` | `Synchron*` and `Asynchron*` |

Do not confuse this report with `PressureEvaluation Vanquish` in the same sequence. They are different templates with different sheets, sources, and layouts.

## 2. Verified Execution Contract

Every observed `Synchron*` / `Asynchron*` method contains these Start Run requirements:

| Method command | Verified value | Why the report needs it |
|---|---|---|
| `PumpModule.Pump.Pump_Pressure.AcqOn` | enabled | Acquires the raw pressure source. |
| `VirtualChannel` | `"PumpPressureVirtual", PumpModule.Pump.Pump_Pressure.Signal, Type=Digital, Unit="bar", Evaluate=Yes` | Exposes the pressure signal as an integrable/evaluable channel. |
| `ColumnComp.CC_Temp.AcqOn` | enabled | Method evidence only; not a direct `PressureEvaluation` table source. |
| `Thermometer.Lab_Temperature.AcqOn` | enabled | Method evidence only; not a direct `PressureEvaluation` table source. |

The virtual channel is essential: the pressure source is acquired first, then `PumpPressureVirtual` makes it available to the peak/integration result context used by the report table. A method variant must preserve this exact virtual-channel name, source expression, type, unit, and `Evaluate=Yes` unless its report table is redesigned too.

The selected injections are bound to `PressureSpikeEval`. The current decoder verifies that this processing method contains the Chromeleon processing-method/SST-IRC structure, but does not yet decode its business rows. For this report, the operational requirement is that it produces integration results for `PumpPressureVirtual`.

## 3. Verified Dynamic Report Table

`PressureEvaluation` contains **one active sheet only**:

| Sheet | Range | Object | Table type | Runtime source |
|---|---|---|---|---|
| `Sheet2` | `A1:H43` | `ReportTableObject` | `integration` | Processed peaks on `PumpPressureVirtual` |

The table definition is dynamic. It contains table headers and a column schema in the template, while its body has no static peak rows before report evaluation. This is normal. Chromeleon populates rows after `PressureSpikeEval` has generated compatible peak/integration results.

| Visible result | Formula source in table definition | Context |
|---|---|---|
| No. | `peak.number` | Peak enumeration |
| Retention Time | `peak.retention_time("detected")*60` | Seconds; virtual pressure channel |
| Peak Start | `peak.start_time*60` | Seconds; virtual pressure channel |
| Valve Switching Time | `(peak.retention_time("detected")-(peak.start_time))*60*1000` | Milliseconds; virtual pressure channel |
| PeakMaxPressureEnhancement | `peak.height` | Pressure-unit result |
| UpperValvePosition | `audit.ColumnComp.UpperValve.CurrentPosition` | Valve audit at peak context |
| LowerValvePosition | `audit.ColumnComp.LowerValve.CurrentPosition` | Valve audit at peak context |
| Flow.Nominal | `audit.PumpModule.Pump.Flow.Nominal` | Pump audit at peak context |

## 4. What a GPT-Generated Report MD Can Implement Now

### Supported: clone and preserve

A GPT-generated MD can select `PressureEvaluation.cmbx` as its carrier and declare the dynamic table as preserved:

````markdown
### Dynamic Report Table: Sheet2!A1:H43
```yaml
object_type: ReportTableObject
operation: preserve
table_type: integration
runtime_source: peak results on PumpPressureVirtual
required_virtual_channel:
  name: PumpPressureVirtual
  source_expression: PumpModule.Pump.Pump_Pressure.Signal
  type: Digital
  unit: bar
  evaluate: true
required_processing_method: PressureSpikeEval
```
````

The current report compiler preserves this table and its FormulaOne layout unchanged. If the generated method preserves the virtual channel and compatible integration behaviour, Chromeleon can populate the table at report runtime.

### Not yet supported: table redesign

The current compiler cannot create a new `ReportTableObject`, alter its pipe-delimited column schema, add/remove/reorder columns, alter its body range, or author its FormulaOne layout. These requests require a CM-created before/after control pair and remain `OPEN VERIFICATION REQUIRED`.

## 5. Generation Preconditions

1. Acquire `PumpModule.Pump.Pump_Pressure` for the entire required run.
2. Create `PumpPressureVirtual` exactly as observed, before processing/integration needs it.
3. Bind a processing method demonstrated to integrate that virtual channel; currently `PressureSpikeEval` is the evidence-backed choice.
4. Keep the valve audit paths used by the table, or redesign the table only after a validated schema write rule exists.
5. Ensure run duration and switching behaviour produce peaks compatible with the processing method; preserving the table alone cannot manufacture peak rows.

## 6. Web-GPT Evidence Packet Rule

For web GPT, provide this document, the formula inventory generated from `PressureEvaluation.cmbx`, and the relevant method MD/library. The binary CMBX files stay local. A generated report MD must never claim that the dynamic body will populate unless all five generation preconditions are stated as satisfied.
