---
kind: cm_report_template
spec_version: 1.0
template_name: TCC Temperature External Review
generation_mode: create_from_blank
execution_backends: [external]
---

## Data Requirements
```yaml
channels: [CC_Temp, ExtTemp_UpperCC, ExtTemp_LowerCC]
audit_paths: []
ret_times: []
```

### Scalar: MeanCC
```yaml
label: Mean internal CC temperature
channel: CC_Temp
formula: chm.sig_value("average", 0, 5)
number_format: 0.00
```

### Scalar: MeanUpper
```yaml
label: Mean upper thermometer
channel: ExtTemp_UpperCC
formula: chm.sig_value("average", 0, 5)
number_format: 0.00
```

### Scalar: MeanLower
```yaml
label: Mean lower thermometer
channel: ExtTemp_LowerCC
formula: chm.sig_value("average", 0, 5)
number_format: 0.00
```

### Formula: SensorDifference
```yaml
label: Upper minus lower thermometer
expression: MeanUpper - MeanLower
number_format: 0.000
```

### Formula: InternalDeviation
```yaml
label: Internal minus external mean
expression: MeanCC - ((MeanUpper + MeanLower) / 2)
number_format: 0.000
```

### Plot: InternalTemperature
```yaml
label: Internal CC temperature
channel: CC_Temp
start_min: 0
end_min: 60
```
