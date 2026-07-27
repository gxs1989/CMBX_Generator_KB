# CM Formula Reverse Engineering Notes

This document summarizes how Chromeleon (CM) formulas act inside a CMBX package and how the current CMBX Data Explorer evaluates them without opening Chromeleon. It is intended as a working reference for future reverse generation of instrument methods and report templates.

## 1. Where CM Formulas Live

A CMBX package normally contains one or more sequences. A sequence contains injections, and each injection contains channels and an audit trail. The sequence also carries instrument methods, processing methods, and report templates.

For FOQ-style data, three formula layers matter:

1. **Instrument method logic**
   - Runs the test.
   - Sets nominal temperatures, waits for stability, logs RetTimes, and writes audit events.
   - Example concept: assign `RetTimes.RetTime1 = System.Retention` after a trigger condition.

2. **Report SheetObject formulas**
   - Stored in the report template XML as `ReportFormulaObject`.
   - Have an Excel-like cell/range, a formula string, and often a `FixedChannel`.
   - Example:
     ```text
     Cell L66
     FixedChannel = ExtTemp_LowerCC
     Formula = chm.sig_value("average", AUDIT.RetTime1(1,"forward")-1, AUDIT.RetTime1(1,"forward")-0.2)
     ```

3. **Embedded workbook formulas**
   - Stored inside the report's `SpreadSheetData` / FormulaOne workbook layer.
   - These calculate summary cells, pass/fail cells, lookup cells, and display-formatted report values.
   - They are not always exposed as `ReportFormulaObject`.
   - Current reverse strategy: start from the DB mapping target cell, trace back to SheetObject source cells, Definitions criteria, and raw/audit inputs.

## 2. Main Formula Namespaces

### `chm.*`: Raw Signal Formulas

These formulas read raw channel data from the selected injection.

Common forms:

```text
chm.sig_value("average", start, end)
chm.sig_value("min", start, end)
chm.sig_value("max", start, end)
chm.signalStatistic("min", start, end)
chm.signalValue(time)
chm.noise(start, end)
chm.drift(start, end)
```

Important details:

- The formula object often has a `FixedChannel`; that channel supplies the data.
- Time is in minutes and usually uses audit RetTimes.
- `average` is calculated over all raw points in the inclusive window.
- `chm.drift(start, end)` is calculated as the linear regression slope over raw points in the inclusive window, in signal-units per minute.
- `chm.sig_value("drift", start, end)` has been observed to follow a coarser signal-statistic behavior than `chm.drift`. For FOQ PCC drift, a 30-second resampled linear slope matches the CM export within about `0.001`.
- `chm.noise(start, end)` is not a simple `max - min`. It is best modeled as peak-to-peak residual after subtracting a linear regression trend from the window.
- The raw result may have more precision than the report cell displays.

Example:

```text
FixedChannel = ExtTemp_UpperCC
Formula = chm.sig_value("average", AUDIT.RetTime2(1,"forward")-1, AUDIT.RetTime2(1,"forward")-0.2)
```

This means:

```text
Read ExtTemp_UpperCC raw points from RetTime2 - 1.0 min to RetTime2 - 0.2 min,
then average those points.
```

### `AUDIT.*`: Audit Trail Formulas

These formulas read RetTimes or audit properties from the injection audit trail.

Common forms:

```text
AUDIT.RetTime1(1,"forward")
AUDIT.ColumnComp.CC.Temperature.Nominal(time)
AUDIT.ColumnComp.CC.Temperature.Nominal(time,"backward")
AUDIT.Column_A.Description(0,"forward")
AUDIT.ColumnComp.ModelNo
```

Important details:

- `RetTimeN` is usually logged by the instrument method.
- Property formulas select a value before or after a time depending on `backward` or `forward`.
- Some report templates omit the full device prefix. For example, the report may ask for:
  ```text
  AUDIT.Column_A.Description(0,"forward")
  ```
  while the exported audit row uses:
  ```text
  ColumnComp.Column_A.Description
  ```
  The evaluator therefore supports suffix path matching.

### `precond.*`: Precondition Metadata

These formulas read the precondition block at the start of an injection audit.

Examples:

```text
precond.ColumnComp.SerialNo
precond.ColumnComp.FirmwareVersion
precond.ColumnComp.HardwareVersion
precond.ColumnComp.ModuleHardwareRevision
precond.ColumnComp.PrehtLeft.ModulePresent
precond.ColumnComp.PrehtLeft.MemoryState
```

Use cases:

- Device identity.
- Firmware and hardware revision checks.
- Preheater module presence and memory-state checks.

If an injection has no audit trail, the evaluator can fall back to the nearest injection in the same sequence that does have audit metadata. This is useful for report cells that are linked to a "Factory Default" injection but need sequence-level or device precondition information.

### `seq.*`, `smp.*`, `injection.*`, `gen.*`: Sequence and Sample Metadata

Common examples:

```text
seq.name
seq.update_time
seq.timebase
injection.name
smp.name
```

Currently implemented:

- `seq.name`
- `seq.update_time`
- `seq.timebase`
- `injection.name`
- `smp.name`

Observed but not fully implemented everywhere:

- `seq.creation_time`
- `seq.submitTime`
- `seq.submitOperator`
- `seq.dataVault`
- `seq.signStatus`
- `gen.loggedOnUser.userName`

These are metadata sources, not raw signal calculations.

## 3. How Report Evaluation Works

The current evaluator follows this flow:

1. Load CMBX header and sequence structure.
2. Select the report template associated with the sequence.
3. For each injection/sheet required by the FOQ DB mapping:
   - Parse report sheets and SheetObject formulas.
   - Build an injection context:
     - audit records
     - RetTimes
     - raw signal cache
     - sequence/package metadata
   - Evaluate direct SheetObject formulas.
   - Apply known workbook-derived rules for summary and pass/fail cells.
4. Resolve the FOQ DB mapping fields against the generated report-cell value map.
5. Write a workbook with:
   - `DB Data`
   - `Mapping Coverage`
   - `Cell Values`
   - `Dependency Trace`

The important point: DB fields usually point to final report cells, not always to raw formula cells. Some final cells are calculated by embedded workbook formulas, so they must be reconstructed from source cells.

## 4. Verified FOQ Calculation Rules

### Temperature Accuracy

Source cells:

```text
I66:I70 or J66:J70 = nominal setpoint
K66:K70 = RetTime
L66:L70 = observed Lower CC
M66:M70 = observed Upper CC
```

Rules:

```text
Observed max-deviation temperature = lower/upper value with larger abs(value - nominal)
Observed and deviation report cells store raw numeric values
The report number format displays those values to 2 decimals
Deviation = raw observed temperature - nominal
D26 = max(abs(D66:D70))
E26 = Test passed if D26 <= Definitions!Temperature Accuracy
```

Important precision note:

- CM/Excel exported cells may contain binary float tails such as `0.03999999999999915`.
- The contract output normalizes these artifacts, e.g. `0.04`.
- For cells such as `Temp Accuracy!C66:D70`, the `.xls` cell value can retain raw precision even when Excel displays two decimals.

### Temperature Precision

Do not calculate this as one combined range across both sensors.

Correct rule:

```text
LowerRange = max(K65:K67) - min(K65:K67)
UpperRange = max(L65:L67) - min(L65:L67)
RawPrecision = max(LowerRange, UpperRange)
Displayed TempPrecision = RawPrecision displayed to 2 decimals
Pass/fail uses RawPrecision <= Definitions!Temperature Precision
```

Reason:

- Combining `K65:L67` includes the offset between two external thermometers.
- CM report evaluates repeatability of each sensor, then uses the worse sensor.

Example from `6545327.cmbx`:

```text
Combined sensor range = 0.0177178423
LowerRange = 0.003112...
UpperRange = 0.004523...
Displayed TempPrecision = 0.00
```

### Temperature Stability

Same family as Temperature Precision.

Correct rule:

```text
LowerRange = max(K61:K75) - min(K61:K75)
UpperRange = max(L61:L75) - min(L61:L75)
RawStability = max(LowerRange, UpperRange)
Displayed TempStability = RawStability displayed to 2 decimals
Pass/fail uses RawStability <= Definitions!Temperature Stability
```

This avoids mixing Lower/Upper thermometer offset into a stability result.

### HeatUp and CoolDown

Source cells:

```text
J66 = RetTime1 heat-up start
K66 = RetTime3 heat-up stable/end
L66 = RetTime4 cool-down start
M66 = RetTime6 cool-down stable/end
```

Rules:

```text
HeatUp_Time_20to50 = K66 - J66 - 2.0 min, displayed to 1 decimal
CoolDown_Time_50to20 = M66 - L66 - 2.0 min, displayed to 1 decimal
Result = Test passed if observed time <= Definitions!HeatUp & Cool Down
```

Note:

- The `2.0 min` subtraction represents the stable-hold time included in the trigger sequence.
- Related row-65 cells also exist in the layout. CM report summary cells D26/D27 for `6545327.cmbx` use the row-66 RetTimes, then display the result to one decimal place.

### PCC CoolDown

Source cells:

```text
K105 = RetTime3
L105 = RetTime4
```

Rule:

```text
Performance_PCC = L105 - K105, displayed to 2 decimals
Result = Test passed if Performance_PCC <= Definitions!PCC CoolDownTime
```

### Preheater Ports

Port result source cells:

```text
J72/J73 = start RetTimes
K72/K73 = end RetTimes
J117/J118 = ModulePresent
K117/K118 = MemoryState
```

Rules:

```text
Left port passes if RetTimes are present, ModulePresent = Yes, MemoryState = OK
Right port passes if RetTimes are present, ModulePresent = Yes, MemoryState = OK
```

Temperature-difference source cells:

```text
J82/J83 = external preheater temperature average
K82/K83 = heater temperature average
```

Rules:

```text
Diff_PhLeft_HtTmp = K82 - J82, displayed to 1 decimal
Diff_PhRight_HtTmp = K83 - J83, displayed to 1 decimal
```

### Column ID

Source cells:

```text
L46 = AUDIT.Column_A.Description(0,"forward")
L47 = AUDIT.Column_B.Description(0,"forward")
L48 = AUDIT.Column_C.Description(0,"forward")
L49 = AUDIT.Column_D.Description(0,"forward")
```

Rules:

```text
RES_ColumnID_A = Test passed if L46 == "A"
RES_ColumnID_B = Test passed if L47 == "B"
RES_ColumnID_C = Test passed if L48 == "C"
RES_ColumnID_D = Test passed if L49 == "D"
```

### Factory Default Metadata

Model variant:

```text
ModelVariant = Internal Use!E12 displayed as a two-digit variant/revision code
Definitions!C15 = ColumnComp.ModelNo
Internal Use!E12 = ColumnComp.ModuleHardwareRevision
```

Example:

```text
03
```

Serial number check:

```text
RES_SN_Check = ok if ColumnComp.SerialNo matches seq.name
```

Date/time note:

```text
seq.update_time in CM reports may point to the original sequence/injection update timestamp as an Excel serial date.
The CMBX package DateCreated header can instead be the CMBX export/package creation date, so it should not be treated as the validated report date without another timestamp source.
```

## 5. Precision and Display Rules

CM formulas can produce raw numeric values with more precision than the report displays. DB mapping often points to the final report cell, so the output should follow the report cell's effective display/calculation level when known.

Current approach:

- Normalize binary float artifacts globally.
- Use report-cell display rounding only where verified:
  - Temperature Accuracy observed/deviation cells use 2 decimals.
  - Temperature Precision summary D26 displays 2 decimals but pass/fail uses raw precision range.
  - Temperature Stability summary D26 displays 2 decimals but pass/fail uses raw stability range.
  - HeatUp/CoolDown summary cells D26/D27 display 1 decimal.
  - PCC performance D26 displays 2 decimals.
  - Preheater heater-temperature difference cells L82/L83 display 1 decimal.
- Avoid forcing all calculated values to 2 decimals, because some database fields intentionally preserve more precision.

Examples:

```text
CM/Excel raw: 0.03999999999999915
Normalized output: 0.04

Raw precision range: 0.004523...
Displayed TempPrecision: 0.00
Pass/fail input: raw 0.004523...
```

## 6. Implications for Reverse Generation

To reverse-generate report templates:

1. Rebuild direct SheetObject formulas:
   - cell/range
   - formula string
   - fixed channel
   - sheet applicability to injection

2. Rebuild workbook-derived cells:
   - summary formulas
   - pass/fail formulas
   - lookup formulas
   - display precision / number format
   - cell dependencies

3. Preserve Definitions:
   - criteria values
   - model/variant lookup tables
   - internal vs external acceptance limits

4. Treat formatting as part of the calculation contract:
   - Some DB values correspond to displayed report-cell precision, not raw formula precision.
   - Some pass/fail cells compare raw values even when the displayed cell is rounded.

To reverse-generate instrument methods:

1. Start from report formula dependencies:
   - `AUDIT.RetTimeN` tells which RetTimes must be logged.
   - `chm.sig_value` windows tell which stable periods or measurement windows the method must create.
   - `precond.*` tells which device metadata must exist at injection start.

2. Reconstruct test steps:
   - set nominal temperatures
   - wait for readiness/stability triggers
   - log RetTimes
   - collect channels required by report formulas

3. Validate method reconstruction against report formulas:
   - Every `AUDIT.RetTimeN` referenced by the report should be generated by the method.
   - Every `FixedChannel` referenced by a report formula should be collected by the injection.
   - Every pass/fail criterion should trace back to a Definitions value.

## 7. Current Evaluator Boundaries

Implemented:

- `chm.sig_value`
- `chm.signalStatistic`
- `chm.signalValue`
- `chm.noise`
- `chm.drift`
- `AUDIT.RetTimeN`
- timed `AUDIT.<path>(time, direction)` property lookup
- no-argument `AUDIT.<path>` metadata lookup
- `precond.<path>` metadata lookup
- selected `seq.*`, `smp.*`, and `injection.*` metadata
- known workbook-derived FOQ cells required by `FOQResultLocations_V2.83.xls`

Not fully implemented:

- Full FormulaOne workbook formula parsing.
- General `IF`, lookup, string concatenation, and cell reference formulas from `SpreadSheetData`.
- Complete `seq.*`, `gen.*`, and signature/electronic report metadata.
- Processing method logic.

The current reliable path is therefore:

```text
DB mapping target cell
-> known workbook-derived rule or direct SheetObject formula
-> AUDIT/precond/seq/chm source formula
-> audit trail or raw channel data
```
