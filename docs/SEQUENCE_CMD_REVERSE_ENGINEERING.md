# Sequence CMD Reverse Engineering

This document tracks what is known about the Chromeleon sequence `.cmd` payload inside CMBX packages.

## Why This Matters

The Level 1 clone-and-select generator can filter `header.xml`, but it currently preserves the original sequence `.cmd` payload.

That means a generated candidate can have a clean visible header while the command payload still contains unselected injection, method, processing, and report references.

To generate runnable CMBX packages, the next major task is to either:

```text
edit existing .cmd records safely
or generate a new sequence .cmd object from the semantic blueprint
```

## Current Probe

Code:

```text
cmbx_data_explorer/sequence_cmd_probe.py
```

The probe scans the first sequence `.cmd` payload for readable references to:

```text
injection names
instrument method names
processing method names
report template names
```

It records:

```text
offset
kind
name
encoding
```

It also groups nearby hits into offset clusters.

## VA Production Probe

Source:

```text
C:\ProgramData\CMBX Data Explorer Workspace\packages\TCC Cost Out\Zollner\Production\0000003.cmbx
```

Outputs:

```text
knowledge_base/tcc_sequence_cmd_probe_va_0000003.tsv
knowledge_base/tcc_sequence_cmd_probe_va_0000003_clusters.tsv
```

The VA probe found 103 readable name hits and 32 offset clusters.

## VA/VC/VH Production Comparison

The same probe has now been run across representative production packages:

| Device sample | CMBX | Readable name hits | Offset clusters |
| --- | --- | ---: | ---: |
| VA | `0000003.cmbx` | `103` | `32` |
| VC | `3000004.cmbx` | `116` | `34` |
| VH | `6000001.cmbx` | `144` | `28` |
| VH | `6000003.cmbx` | `111` | `27` |

Generated outputs:

```text
knowledge_base/tcc_sequence_cmd_probe_va_0000003.tsv
knowledge_base/tcc_sequence_cmd_probe_vc_3000004.tsv
knowledge_base/tcc_sequence_cmd_probe_vh_6000001.tsv
knowledge_base/tcc_sequence_cmd_probe_vh_6000003.tsv
knowledge_base/tcc_sequence_cmd_links_va_0000003.tsv
knowledge_base/tcc_sequence_cmd_links_vc_3000004.tsv
knowledge_base/tcc_sequence_cmd_links_vh_6000001.tsv
knowledge_base/tcc_sequence_cmd_links_vh_6000003.tsv
knowledge_base/tcc_sequence_order_vs_cmd_va_0000003.tsv
knowledge_base/tcc_sequence_order_vs_cmd_vc_3000004.tsv
knowledge_base/tcc_sequence_order_vs_cmd_vh_6000001.tsv
knowledge_base/tcc_sequence_order_vs_cmd_vh_6000003.tsv
knowledge_base/tcc_sequence_cmd_row_probe_va_0000003.tsv
knowledge_base/tcc_sequence_cmd_row_probe_vc_3000004.tsv
knowledge_base/tcc_sequence_cmd_row_probe_vh_6000001.tsv
knowledge_base/tcc_sequence_cmd_row_probe_vh_6000003.tsv
```

The link probe confirms that the sequence `.cmd` payload contains compact readable references of the form:

```text
injection name
RelativeUrl -> processing method
RelativeUrl -> instrument method
```

This is the strongest current evidence for reconstructing the execution-critical sequence rows.

## Row Order Finding

Chromeleon's visible sequence-grid order must come from the package/header/sequence model, not from the first occurrence order of readable names inside `.cmd`.

For `VH 6000003`, the visible/header order is:

| Row | Injection | Processing Method | Instrument Method | First `.cmd` occurrence |
| ---: | --- | --- | --- | ---: |
| 1 | `ColumnIDs` | `CORRECT_STABILITY_INJ_INSERTION` | `ColumnID` | `123413` |
| 2 | `Preheater Connection Test` | `No_Integration` | `PREHEATER` | `120294` |
| 3 | `Valve` | `No_Integration` | `VALVES` | `123918` |
| 4 | `VTCC_BurnIn` | `NO_INTEGRATION` | `BURNIN` | `125463` |
| 5 | `Temperature Calibration` | `CORRECT_ACCURACY_INJ_INSERTION` | `TEMPERATURE_CALIBRATION` | `124409` |
| 6 | `Temperature Accuracy_H` | `ACCURACY_IRC_STOP_H` | `TEMPERATURE_ACCURACY` | `122893` |
| 7 | `Temperature Precision_and_Fan` | `CORRECT_STABILITY_INJ_INSERTION` | `TEMPERATURE_PRECISION_AND_FAN` | `125952` |
| 8 | `Temperature Stability_and_PCC_H` | `NO_INTEGRATION` | `TEMPERATURE_STABILITY_AND_PCC_70_H` | `120813` |
| 9 | `HeatUp and CoolDownTime` | `No_Integration` | `TEMP_HEAT_UP_DOWN_20_50_20` | `126501` |
| 10 | `LiquidLeaktest` | `No_Integration` | `LIQUID LEAK` | `122386` |
| 11 | `Qualification_Service_Done` | `No_Integration` | `Qualification_Service_Done` | `121862` |
| 12 | `Factory Default` | `No_Integration` | `FACTORYDEFAULT` | `124953` |
| 13 | `Error Log Check` | `No_Integration` | `CHECKERRORLOG` | `121350` |

Therefore:

```text
header/blueprint injection order -> visible sequence row order
.cmd occurrence offset -> record-location hint only
```

This matters for generation. A writer must preserve the semantic/header row order and use `.cmd` offsets only to locate records or references that need to be edited.

## Injection Row Record Probe

Code:

```text
sequence_cmd_injection_record_probes(...)
sequence_cmd_injection_record_probes_tsv(...)
```

This probe is intentionally conservative. It does not claim to fully decode the binary row record. It extracts stable, directly visible signals around each injection-name occurrence:

```text
header row order
.cmd occurrence rank
estimated row record anchor
name field offset
processing method RelativeUrl
instrument method RelativeUrl
cm6_sample_id custom field
nearby type/status/lock strings when visible
nearby ExtTemp preview string when visible
```

For `VH 6000003`, the row probe aligns with the Chromeleon screenshot:

| Row | Injection | Sample ID | Processing Method | Instrument Method |
| ---: | --- | --- | --- | --- |
| 1 | `ColumnIDs` | blank | `CORRECT_STABILITY_INJ_INSERTION` | `ColumnID` |
| 2 | `Preheater Connection Test` | `Internal 2` | `No_Integration` | `PREHEATER` |
| 3 | `Valve` | `Internal 3` | `No_Integration` | `VALVES` |
| 4 | `VTCC_BurnIn` | blank | `NO_INTEGRATION` | `BURNIN` |
| 5 | `Temperature Calibration` | `Internal 4` | `CORRECT_ACCURACY_INJ_INSERTION` | `TEMPERATURE_CALIBRATION` |
| 6 | `Temperature Accuracy_H` | `4` | `ACCURACY_IRC_STOP_H` | `TEMPERATURE_ACCURACY` |
| 7 | `Temperature Precision_and_Fan` | `4` | `CORRECT_STABILITY_INJ_INSERTION` | `TEMPERATURE_PRECISION_AND_FAN` |
| 8 | `Temperature Stability_and_PCC_H` | `5` | `NO_INTEGRATION` | `TEMPERATURE_STABILITY_AND_PCC_70_H` |
| 9 | `HeatUp and CoolDownTime` | `5` | `No_Integration` | `TEMP_HEAT_UP_DOWN_20_50_20` |
| 10 | `LiquidLeaktest` | `Internal 6` | `No_Integration` | `LIQUID LEAK` |
| 11 | `Qualification_Service_Done` | blank | `No_Integration` | `Qualification_Service_Done` |
| 12 | `Factory Default` | `Internal 7` | `No_Integration` | `FACTORYDEFAULT` |
| 13 | `Error Log Check` | `Internal 8` | `No_Integration` | `CHECKERRORLOG` |

The stable observed row shape is:

```text
row metadata fields
name field marker: e2 01 <length> <injection name>
RelativeUrl[0] -> processing method
RelativeUrl[1] -> instrument method
Samples.CustomFieldCollection
cm6_sample_id -> visible sample ID
additional status/result/raw/embed data
```

The estimated record anchor is currently the nearest preceding length-prefixed ExtTemp preview field, commonly:

```text
72 04 4e 6f 6e 65  ->  r\04 "None"
```

This anchor is useful for inspection, but it is not yet a safe delete/rewrite boundary. Some VA records quickly continue into additional channel/raw-like payload sections after the row metadata, so mutation must wait until true enclosing message boundaries are known.

## Early Interpretation

The first group is broad and contains `Default`, `Valve`, `VALVES`, `VTCC_BurnIn`, `NO_INTEGRATION`, and `BURNIN`.

After that, the sequence injection/link area appears as compact clusters:

| Offset Range | Names |
| --- | --- |
| `108134-108373` | `Temperature Calibration`, `NO_INTEGRATION`, `TEMPERATURE_CALIBRATION` |
| `122997-123240` | `Temperature Accuracy_C`, `ACCURACY_IRC_STOP_C`, `TEMPERATURE_ACCURACY` |
| `137991-138228` | `Temperature Precision`, `NO_INTEGRATION`, `TEMPERATURE_PRECISION` |
| `152840-153079` | `Temperature Stability_C`, `NO_INTEGRATION`, `TEMPERATURE_STABILITY_70_C` |
| `167692-167931` | `HeatUp and CoolDownTime`, `TEMP_HEAT_UP_DOWN_20_50_20` |
| `182549-182779` | `LiquidLeaktest`, `LIQUID LEAK` |
| `197369-202600` | `Qualification_Service_Done`, `Factory Default`, `FACTORYDEFAULT`, `Error Log Check`, `CHECKERRORLOG`, plus a processing reference |

Later clusters appear to represent processing method sections, default/report layout sections, embedded instrument method payloads, and report payloads:

| Offset | Name |
| --- | --- |
| `315785` | `BURNIN` |
| `331766` | `CHECKERRORLOG` |
| `348690` | `ColumnID` |
| `365204` | `FACTORYDEFAULT` |
| `382490` | `LIQUID LEAK` |
| `401002` | `PREHEATER` |
| `415784` | `QUALIFICATION_SERVICE_DONE` |
| `435022` | `TEMPERATURE_ACCURACY` |
| `455289` | `TEMPERATURE_CALIBRATION` |
| `472884` | `TEMPERATURE_PRECISION` |
| `490097` | `TEMPERATURE_STABILITY_70_C` |
| `509035` | `TEMPERATURE_STABILITY_AND_PCC_70_H` |
| `527276` | `TEMP_HEAT_UP_DOWN_20_50_20` |
| `545420` | `VALVES` |
| `690905` | `Report_VATCC_V1_01` |

## Implication For Generation

The visible injection/link references are much earlier than the embedded instrument method payloads.

This suggests sequence `.cmd` has at least these logical regions:

```text
sequence/injection row definitions and RelativeUrl links
processing method sections
embedded instrument method payload sections
report template payload sections
```

The next safe reverse step is to compare the same clusters across VA, VC, and VH, then locate byte ranges that can be removed or rewritten without damaging preserved embedded method/report payloads.

The Chromeleon sequence UI also shows fields that are not yet decoded from `.cmd`, such as sample value, replicate count, type, status, comments, lock state, and associated view settings. See:

```text
cmbx_data_explorer/docs/CM_SEQUENCE_UI_OBSERVATIONS.md
```

## Current Boundary

Do not yet remove `.cmd` byte ranges automatically.

The current evidence is strong enough to guide reverse engineering, but not yet enough to guarantee a valid Chromeleon sequence command after mutation.
