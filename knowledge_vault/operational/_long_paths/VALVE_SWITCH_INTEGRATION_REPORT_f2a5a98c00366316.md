---
kind: cm_report_template
spec_version: 1.0
template_name: Valve_Switch_Integration
generation_mode: create_from_blank
workbook_policy: create_static
---

# Runtime Contract

- Instrument Method must create and acquire `PumpPressureVirtual` from `PumpModule.Pump.Pump_Pressure.Signal`.
- Injection Processing Method must be exactly `PressureSpikeEval` and integrate `PumpPressureVirtual`.
- The report CMBX does not install or assign the Processing Method.

## Sheet: Valve Switches

### Sheet Settings
```yaml
active: true
each_injection: true
column_widths: A=18,B=22,C=22
row_heights: 1=26,3=20
```

### Workbook Text: A1
```yaml
operation: create
value_type: text
value: Valve Switch Events
style: title
```

### Workbook Text: A3
```yaml
operation: create
value_type: text
value: Integration source
style: label
```

### Workbook Text: B3
```yaml
operation: create
value_type: text
value: PumpPressureVirtual / PressureSpikeEval
style: result
```

### Dynamic Table: A6:C45
```yaml
operation: create
table_type: integration
body_rows: 38
requires_processing: true
processing_method: PressureSpikeEval
fixed_channel: PumpPressureVirtual
sort_formula: peak.group
include_identified_peaks: true
include_unidentified_peaks: true
```

#### Table Column: Switch Time
```yaml
formula: peak.retention_time("detected")*60
header: Switch Time
unit: s
channel: PumpPressureVirtual
```

#### Table Column: Upper Position
```yaml
formula: audit.ColumnComp.UpperValve.CurrentPosition
header: Upper Position
unit: ''
channel: PumpPressureVirtual
```

#### Table Column: Lower Position
```yaml
formula: audit.ColumnComp.LowerValve.CurrentPosition
header: Lower Position
unit: ''
channel: PumpPressureVirtual
```
