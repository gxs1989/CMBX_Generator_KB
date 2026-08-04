# TCC Temperature Accuracy Principle

This note defines what a generated TCC temperature accuracy test must prove before a method script can be considered correct.

## Test Meaning

Temperature accuracy verifies how far the real column-compartment temperature is from the requested nominal setpoint.

For a VH-C10-A 40 degC-only request, the test asks:

```text
When the VH TCC is commanded to 40 degC and has reached a stable condition,
what is the measured deviation between the external thermometer temperature and 40 degC?
```

This is not a temperature stability test and not a heat-up/cool-down performance test. It is a setpoint accuracy check.

## Measurement Source

The report calculation must use external thermometer channels, not only the TCC internal control temperature:

```text
Thermometer1.ExtTemp_LowerCC
Thermometer1.ExtTemp_UpperCC
```

The internal controller readiness signal is still needed because it tells the method when the TCC believes it is at the setpoint:

```text
ColumnComp.CC.TempReady
```

The accuracy value is based on external measurement:

```text
lower_avg = average external lower thermometer in the stable window
upper_avg = average external upper thermometer in the stable window
observed = lower_avg or upper_avg, whichever has the larger absolute deviation from nominal
deviation = observed - nominal
```

## Why RetTime3 For 40 degC

The source VH `TEMPERATURE_ACCURACY` method defines the five VH accuracy setpoints as:

```text
RetTime1 -> 10 degC
RetTime2 -> 20 degC
RetTime3 -> 40 degC
RetTime4 -> 80 degC
RetTime5 -> 120 degC
```

Therefore a single-point 40 degC method should still write:

```text
RetTimes.RetTime3 = System.Retention
```

Rebinding 40 degC to `RetTime1` would break compatibility with the existing report and FOQ DB mapping.

## RetTime Semantics

For report formulas such as:

```text
chm.sig_value("average", AUDIT.RetTime3(1,"forward")-1, AUDIT.RetTime3(1,"forward")-0.2)
```

`RetTime3` is not the start of the measurement. It is the anchor near the end of the stable measurement window.

The method must therefore:

1. Set the nominal temperature to 40 degC.
2. Wait for `ColumnComp.CC.TempReady`.
3. Wait for upper and lower external thermometer stability.
4. Continue collecting enough settled data before writing `RetTimes.RetTime3`.
5. Write `RetTimes.RetTime3 = System.Retention`.

The report then looks backward from RetTime3 and averages the already-collected stable window.

## FOQ DB Mapping

For VH-C10-A:

```text
DB field: TempAcc40
Report file: Temperature Accuracy_H.XLS
Report sheet: Temp Accuracy
Report cell: D68
Unit: K
```

Source cells for the 40 degC row:

```text
J68 = nominal 40 degC
K68 = AUDIT.RetTime3
L68 = lower external thermometer average
M68 = upper external thermometer average
D68 = deviation at 40 degC
```

## Method Generation Rule

A generated 40 degC-only method may remove transitions for 10, 20, 80, and 120 degC, but it must preserve:

- TCC temperature control setup.
- VH PCC temperature-control disable command, if applicable.
- external thermometer acquisition.
- external thermometer stability logic.
- `RetTimes.RetTime3` as the report anchor.
- enough settled acquisition before `RetTimes.RetTime3` is written.

The method should return the TCC nominal temperature to a benign state such as 20 degC at the end.
