# Chromeleon Sequence UI Observations

This document records facts observed from Chromeleon's own sequence view after opening a TCC CMBX package. These facts are important because a generated CMBX eventually needs to reproduce not only methods and reports, but also the visible sequence grid state and associated item list.

## Screenshot Source

User-provided Chromeleon screenshot:

```text
Sequence title: 6000003
Instrument/controller selector: <FOQ_VH_03>
Connection state: Not Connected
Run state: Run Finished
```

The screenshot appears to be a `VH-C10-A` FOQ sequence.

## Sequence Grid Columns

Visible top-grid columns include:

```text
#
ExtTemp_L
Name
QC_Comm
Type
Status
Inject Time
Comment
Instrument Method
Processing Method
*Sample
Lock Stat
Replicate
```

User clarification:

| UI column | Meaning for generation |
| --- | --- |
| channel preview column such as `ExtTemp_L` | visual preview of selected channel; not required for generation |
| `Name` | manually entered injection name; required |
| first `Comment` / `QC_Comm` style field | user/comment metadata; optional |
| `Type` | sample type; normally `Unknown` for untested samples |
| `Status` | run state such as `Finished` or `Idle`; default can be `Idle` for generated untested sequences |
| `Inject Time` | automatically filled by CM during execution |
| second `Comment` | user/comment metadata; optional |
| `Instrument Method` | required |
| `Processing Method` | required when IRC or known processing behavior is needed |

Generation implication: these visible columns belong to different layers. The runnable sequence layer needs only the fields required to execute the test:

```text
row order
name
instrument method
processing method when IRC behavior is needed
```

Other sequence-grid columns belong to analysis, display, report, print, or historical replay layers. `InjectionBlueprint` may eventually include fields that map to:

```text
external-temperature preview/thumbnail state
QC comment
injection type
status
inject time
comment
sample binding
lock state
replicate
```

Some of these may correspond to report-template pages, print/report state, sample labels, or historical run state. They should not be treated as hard requirements for a fresh runnable TCC sequence until proven by Chromeleon execution behavior.

Current generation default assumptions:

```text
Type -> Unknown
Status -> Idle for fresh untested sequences
Inject Time -> blank until CM runs the injection
comments -> blank unless user supplies them
channel preview thumbnail -> let CM/UI regenerate or leave absent
```

Observed `Type` dropdown values include:

```text
Unknown
Blank
Check Standard
Calibration Standard
Matrix
Spiked
Unspiked
```

CM symbol metadata observed in extracted help/configuration also maps injection `Type` value `0` to `Unknown`, so generated untested injections should default to `Unknown` unless a workflow explicitly needs another sample type.

The stronger priorities are:

```text
generate executable instrument methods
bind the correct processing methods for IRC behavior
evaluate/generate report calculations correctly
validate target CM instrument configuration
```

## Observed VH Injection Rows

Visible rows:

| Row | Name | Instrument Method | Processing Method | Visible Sample | Replicate |
| --- | --- | --- | --- | --- | --- |
| 1 | `ColumnIDs` | `ColumnID` | `CORRECT_STABILIT...` | blank or not visible | `12` |
| 2 | `Preheater Connectio...` | `PREHEATER` | `No_Integration` | `Internal 2` | `8` |
| 3 | `Valve` | `VALVES` | `No_Integration` | `Internal 3` | `8` |
| 4 | `VTCC_BurnIn` | `BURNIN` | `NO_INTEGRATION` | blank or not visible | `12` |
| 5 | `Temperature Calibrati...` | `TEMPERATURE_CALIBRATION` | `CORRECT_ACCURA...` | `Internal 4` | `8` |
| 6 | `Temperature Accura...` | `TEMPERATURE_ACCURACY` | `ACCURACY_IRC_ST...` | `4` | `12` |
| 7 | `Temperature Precisio...` | `TEMPERATURE_PRECISION_AND_FAN` | `CORRECT_STABILIT...` | `4` | `12` |
| 8 | `Temperature Stability...` | `TEMPERATURE_STABILITY_AND_PCC_70...` | `NO_INTEGRATION` | `5` | `12` |
| 9 | `HeatUp and CoolDow...` | `TEMP_HEAT_UP_DOWN_20_50_20` | `No_Integration` | `5` | `12` |
| 10 | `LiquidLeaktest` | `LIQUID LEAK` | `No_Integration` | `Internal 6` | `8` |
| 11 | `Qualification Service...` | `Qualification_Service_Done` | `No_Integration` | blank or not visible | `12` |
| 12 | `Factory Default` | `FACTORYDEFAULT` | `No_Integration` | `Internal 7` | `8` |
| 13 | `Error Log Check` | `CHECKERRORLOG` | `No_Integration` | `Internal 8` | `8` |

Notes:

- Truncated values must be confirmed from CMBX `.cmd` or a Chromeleon export before being used as exact generator inputs.
- Chromeleon UI may display names with spaces while `header.xml` and decoded payloads often use underscores.
- Status and inject-time values in the screenshot are historical run state and should probably be treated as result metadata, not as fresh-generation inputs.

## Catalog Cross-Check

The current semantic catalog order for `VH-C10-A` matches the screenshot row order:

```text
1  ColumnIDs                         ColumnID                         CORRECT_STABILITY_INJ_INSERTION
2  Preheater Connection Test          PREHEATER                        No_Integration
3  Valve                             VALVES                           No_Integration
4  VTCC_BurnIn                       BURNIN                           NO_INTEGRATION
5  Temperature Calibration            TEMPERATURE_CALIBRATION          CORRECT_ACCURACY_INJ_INSERTION
6  Temperature Accuracy_H             TEMPERATURE_ACCURACY             ACCURACY_IRC_STOP_H
7  Temperature Precision_and_Fan       TEMPERATURE_PRECISION_AND_FAN    CORRECT_STABILITY_INJ_INSERTION
8  Temperature Stability_and_PCC_H     TEMPERATURE_STABILITY_AND_PCC_70_H NO_INTEGRATION
9  HeatUp and CoolDownTime            TEMP_HEAT_UP_DOWN_20_50_20       No_Integration
10 LiquidLeaktest                    LIQUID LEAK                      No_Integration
11 Qualification_Service_Done         QUALIFICATION_SERVICE_DONE        No_Integration
12 Factory Default                   FACTORYDEFAULT                   No_Integration
13 Error Log Check                   CHECKERRORLOG                    No_Integration
```

This confirms that `tcc_semantic_test_catalog.json` already preserves the visible VH sequence order.

The `.cmd` occurrence order is not a reliable source for this visible order. For `VH 6000003`, the first readable `.cmd` occurrence for row 2 appears before row 1, and several later rows are similarly interleaved. Use:

```text
header/semantic catalog order -> visible sequence grid order
.cmd occurrence offset -> record-location hint only
```

The visible sample IDs are now independently confirmed by the row probe in:

```text
knowledge_base/tcc_sequence_cmd_row_probe_vh_6000003.tsv
```

The probe reads them from the nearby `Samples.CustomFieldCollection` / `cm6_sample_id` block inside the sequence `.cmd` payload.

For runnable TCC generation, the current execution-critical row fields are:

```text
Name
Instrument Method
Processing Method
```

The remaining visible columns are tracked as optional/full-fidelity fields.

## Associated Items Pane

The bottom pane shows associated sequence items. Visible item names include:

```text
ACCURACY IRC STOP C
ACCURACY IRC STOP H
BURNIN
CHECKERRORLOG
ColumnID
CORRECT ACCURACY INJ INSERTION
CORRECT STABILITY INJ INSERTION
Default
FACTORYDEFAULT
LIQUID LEAK
NO INTEGRATION
PREHEATER
QUALIFICATION SERVICE DONE
Report VTCC V2 12
Report VTCC V2 12 CIC data output
TEMP HEAT UP DOWN 20 50 20
TEMPERATURE ACCURACY
TEMPERATURE CALIBRATION
TEMPERATURE PRECISION AND FAN
TEMPERATURE STABILITY 70 C
TEMPERATURE STABILITY AND PCC 70 H
VALVES
```

Visible item types include:

```text
Processing Method
Instrument Method
View Settings
Report Template
```

Generation implication: a full generated sequence may need to carry associated items that are not directly used by selected injection rows. For clone-and-select generation, this creates two modes:

```text
execution-only candidate: keep only items required by selected injection execution
analysis candidate: keep selected injection execution items plus report/DB items
CM-like full package: keep the full associated item library for that device family
```

The screenshot suggests Chromeleon presents `Default` as `View Settings`, not as a report template, even though readable `.cmd` probes see many `Default` references.

## Method/Processing Display Normalization

Chromeleon UI appears to display some associated item names with spaces:

```text
NO INTEGRATION
CORRECT ACCURACY INJ INSERTION
TEMP HEAT UP DOWN 20 50 20
Report VTCC V2 12
```

The CMBX parser and semantic catalog currently use package/decode-style names:

```text
NO_INTEGRATION
CORRECT_ACCURACY_INJ_INSERTION
TEMP_HEAT_UP_DOWN_20_50_20
Report_VTCC_V2_12
```

Generator and UI code should treat these as display aliases, not different logical objects.

## New Reverse-Engineering Target

Find where the following UI sequence-grid fields live in `.cmd`:

```text
row order
sample value
replicate count
injection type
lock state
comments
associated item library
view settings binding
```

The current `sequence_cmd_probe.py` only locates object-name references. It should be extended later to inspect nearby bytes around each injection/link cluster and look for sample/replicate values.

These values are useful, but lower priority than decoding the execution-critical injection/method/IRC processing records.

## Custom Sequence Variables

The second screenshot shows three custom sequence variable rows:

| Name | Observed value | Description |
| --- | --- | --- |
| `Location` | blank or not visible | blank or not visible |
| `S/N Thermometer one Germering` | `7551807 0962` as displayed | `Serial Number of the thermometer installed at the instrument` |
| `S/N Thermometer two Germering` | `7552104 1135` as displayed | `Serial Number of the thermometer installed at the instrument` |

These variables appear to describe external thermometer identity. They may be important for report output and traceability, but they are not currently proven to be required for the minimal execution sequence. Treat them as Level C/full-fidelity sequence metadata until method execution or report calculation proves a direct dependency.
