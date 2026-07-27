# Method/Report Generator Tab

Status: superseded by `TAB_FOQ_KB_TO_RUN.md`.

The earlier generator concept was too close to exporting candidate script
fragments. The current UI direction is `FOQ KB to Run`: align TD items to
injections, methods, processing bindings, and reports first; generate only
after the unresolved design questions are explicit.

The `Method/Report Generator` tab is the first UI surface for semantic TCC
method and report generation.

It is different from the extraction tabs:

```text
Extraction tabs: read an existing CMBX and expose what is inside.
Generator tab: start from a test intent and produce a reviewable method/report design package.
```

## Current Generator

Implemented first target:

```text
Device: VH-C10-A, VC-C10-A, VA-C10-A
Test: Temperature Accuracy
Setpoint: user-selected single setpoint
Baseline: user-confirmed approach/baseline temperature
```

The generator does not simply copy the original multi-point
`TEMPERATURE_ACCURACY` method. It emits a reduced semantic method contract
after the user confirms the approach/baseline temperature:

```text
baseline temperature control
-> wait for CC.TempReady and upper/lower external thermometer stability
-> optionally write the baseline RetTime marker
-> raise nominal to the requested setpoint
-> wait for CC.TempReady and upper/lower external thermometer stability
-> hold enough history for the report window
-> write the requested setpoint RetTime as the report anchor
-> return nominal to the selected safe/baseline temperature
```

The report calculation keeps the Chromeleon report contract:

```text
Lower average = chm.sig_value("average", AUDIT.<RetTimeN>-1.0, AUDIT.<RetTimeN>-0.2)
Upper average = chm.sig_value("average", AUDIT.<RetTimeN>-1.0, AUDIT.<RetTimeN>-0.2)
Observed = external sensor with larger absolute deviation from requested nominal
Deviation = Observed - requested nominal
DB field = matching TempAccXX field and report row, displayed to 2 decimals
Pass/fail = abs(raw deviation) <= Definitions!Temperature Accuracy
```

## UI Controls

- `Device`: CM model from the known TCC semantic catalog.
- `Test`: currently `Temperature Accuracy`.
- `Setpoint C`: requested single setpoint.
- `Baseline C`: approach/baseline temperature confirmed from TD/method design.
- `Preview`: rebuilds the generated method script preview and report calculation preview.
- `Export Excel`: writes the method script workbook and report calculation workbook.
- `Export Full Project`: writes JSON, TXT, MD, TSV, and Excel artifacts for the generated project.

Generated files are written under:

```text
<Output Folder>/generated_projects/<device>_temperature_accuracy_<setpoint>C/
```

## Exported Workbooks

Method workbook:

```text
<generated instrument method>_method_script.xlsx
```

Sheets:

- `Method Script`: stage-by-stage commands and why each command exists.
- `RetTime Contract`: which RetTimes are emitted and which report cells use them.
- `Configuration`: required CM symbols, channels, and method variables.

Report workbook:

```text
<generated report template>_report_calculation.xlsx
```

Sheets:

- `Report Formula Map`: DB field, report cell, fixed channel, and formula/rule.
- `Calculation Contract`: raw formulas, workbook-derived rules, display precision.
- `Single Point Layout`: single-point report cells for the generated test.

## Important Boundary

The generator currently produces reviewable Excel and text assets. It does not
yet produce a Chromeleon-signed binary `CpXm` method payload or a full binary
report template payload.

It also does not infer process intent that is not yet encoded in the knowledge
base. For example, whether a 120 C accuracy test should approach from 80 C or
from 20 C is a design input until the TD/method evidence is encoded.

The intended next bridge is:

```text
semantic generated method/report contract
-> Chromeleon editor copy/paste validation
-> binary payload patching or official CM import path
-> generated CMBX sequence package
```
