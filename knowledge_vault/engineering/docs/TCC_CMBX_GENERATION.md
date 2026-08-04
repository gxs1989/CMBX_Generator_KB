# TCC CMBX Generation Notes

This document records the current reverse-generation path for TCC-focused CMBX creation.

## Goal

Generate runnable Chromeleon assets from a semantic test request, starting with TCC modules:

```text
user intent
-> device model and configuration
-> sequence row
-> instrument method contract
-> processing method link for IRC, if required
-> report calculation contract
-> CMBX package
```

The first concrete target is:

```text
Device: VH-C10-A
Test: Temperature Accuracy
Setpoint: 40 degC only
DB field: TempAcc40
```

## Current Standalone Project Output

`tcc_project_generator.py` can generate a standalone project folder containing:

- `project_spec.json`
- `instrument_method_draft.txt`
- `method_script_40C_only.txt`
- `required_configuration.md`
- `report_calculation_spec.md`
- `report_formula_map_40C.tsv`
- `generation_notes.md`

These files are generation contracts and source-controlled project items. They are not yet a signed or binary-compatible Chromeleon CpXm method payload.

The import candidates in `outputs/import_candidates` are different: they expose source method/report assets from a known-good CMBX and therefore still contain the original multi-point payload unless the filename explicitly says it is only a header alias experiment.

## VH Temperature Accuracy 40 degC Binding

The extracted VH `TEMPERATURE_ACCURACY` method proves the 40 degC point is the third accuracy point:

```text
Variables.GenericDouble3 = 40.0
ColumnComp.CC.Temperature.Nominal = Variables.GenericDouble3
Wait ColumnComp.CC.TempReady AND StabVars.LowerReady AND StabVars.UpperReady
RetTimes.RetTime3 = System.Retention
```

Therefore:

```text
TempAcc40 -> Temp Accuracy report row for 40 degC -> AUDIT.RetTime3
```

This is important because a one-point method must still preserve the original report/DB anchor. Rebinding 40 degC to `RetTime1` would make the generated result incompatible with existing FOQ mapping conventions.

## Generated Method Contract

The generated single-point method draft keeps the proven setup pattern:

- turn CC temperature control on
- for VH, disable PCC temperature control with `ColumnComp.CmdString Cmd="PCC.TempCtrl=0"`
- set `ColumnComp.CC.Mode = StillAir`
- acquire `ColumnComp.CC_Temp`
- acquire `Thermometer1.ExtTemp_UpperCC`
- acquire `Thermometer1.ExtTemp_LowerCC`
- wait for `ColumnComp.CC.TempReady` and external thermometer stability
- write `RetTimes.RetTime3 = System.Retention`

The method returns the CC nominal temperature to 20 degC at the end.

The reduced script removes the other VH accuracy transitions:

```text
removed: 10 degC, 20 degC, 80 degC, 120 degC
preserved: 40 degC, RetTimes.RetTime3, upper/lower external thermometer stability logic
```

`RetTimes.RetTime3` is intentionally preserved because the DB/report mapping for 40 degC expects the third accuracy row.

## Generated Report Contract

For the 40 degC single-point report:

```text
Lower = chm.sig_value("average", AUDIT.RetTime3(1,"forward")-1, AUDIT.RetTime3(1,"forward")-0.2)
Upper = chm.sig_value("average", AUDIT.RetTime3(1,"forward")-1, AUDIT.RetTime3(1,"forward")-0.2)
Observed = lower/upper value with larger abs(value - 40)
Deviation = Observed - 40
DB field = TempAcc40
```

Observed and deviation values display to 2 decimals. Pass/fail uses the raw absolute deviation against `Definitions!Temperature Accuracy`.

The FOQ DB mapping has been verified:

```text
Device: VH-C10-A
DB field: TempAcc40
Report file: Temperature Accuracy_H.XLS
Report sheet: Temp Accuracy
Report cell: D68
Unit: K
```

## Remaining Encoder Work

To create a fully runnable generated CMBX, the next work items are:

1. Clone the source `TEMPERATURE_ACCURACY` CpXm payload.
2. Disable or remove the non-40 degC temperature transitions while preserving setup, acquisition, and stability triggers.
3. Clone `Report_VTCC_V2_12` into a single-point report template or preserve the original template and export only `TempAcc40`.
4. Create a sequence row:

```text
Name = Temperature Accuracy_H
Instrument Method = TEMPERATURE_ACCURACY__single_40C
Processing Method = ACCURACY_IRC_STOP_H
Type = Unknown
Status = Idle
```

5. Repack the generated method, report, sequence row, and required package metadata into CMBX.

Until the binary encoder is implemented, generated standalone projects are the safest authoring surface.
