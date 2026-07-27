# CMBX Import Asset Candidates

This note documents the first importable-asset generator.

## Why Method/Report Assets Need Sequence Payload

Observed TCC CMBX packages store instrument methods and report templates as header elements under a sequence:

```xml
<ChromeleonElement Name="TEMPERATURE_ACCURACY" ItemType="Dionex.Chromeleon.Data.InstrumentMethod" />
<ChromeleonElement Name="Report_VTCC_V2_12" ItemType="Dionex.Chromeleon.Data.ReportDefinition" />
```

These elements do not carry independent `Filename` or `RawDataFilename` attributes. Their binary bodies are embedded inside the sequence command payload, such as:

```text
6000001.seq_2.cmd
```

So an import candidate for a single method or report must keep that sequence `.cmd` payload. A header-only CMBX would be an empty shell.

## Generator

`cmbx_import_asset_generator.py` writes a minimal CMBX containing:

- `header.xml`
- one sequence element
- one visible asset element, either an instrument method or report template
- the original sequence `.cmd` payload that contains the embedded object

The generator can expose:

```text
TEMPERATURE_ACCURACY
Report_VTCC_V2_12
```

from a real source package such as `6000001.cmbx`.

## Current Limitation

This is an import candidate, not a semantic binary rewrite.

For the VH 40 degC single-point target:

- the standalone project/spec can define `TEMPERATURE_ACCURACY__single_40C`
- the report contract can define `Report_VTCC_V2_12__single_40C`
- but the binary sequence command payload still needs a safe CpXm/command encoder before the generated asset is a true one-point Chromeleon method

Until that encoder exists, the safest import candidate is the exact source method/report asset exposed from a known-good CMBX.

## Request Package

For semantic generation requests, the preferred handoff artifact is now:

```text
VH-C10-A_accuracy_40C_request_package.cmbx
```

This package contains one injection and generated 40C asset names in `header.xml`, plus generated request assets embedded under:

```text
CMBX_DATA_EXPLORER_GENERATION/
```

The embedded assets are:

```text
project_spec.json
required_configuration.md
method_script_40C_only.txt
report_calculation_spec.md
report_formula_map_40C.tsv
README.md
```

This is closer to the intended semantic contract:

```text
need VH-C10-A accuracy at 40 degC
-> one injection
-> one generated method name
-> one generated report name
-> configuration checklist
-> 40C-only method script
-> report formula map for TempAcc40
```

Chromeleon may ignore `CMBX_DATA_EXPLORER_GENERATION` because these files are not native CM objects. They are included so the CMBX carries the complete generation contract while the CpXm binary encoder is still under development.
