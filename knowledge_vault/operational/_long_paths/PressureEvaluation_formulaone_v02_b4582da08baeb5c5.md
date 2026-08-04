---
kind: cm_report_template
spec_version: 0.2
template_name: PressureEvaluation_FormulaOne_Control_V02
reference_template:
  cmbx: C:\ProgramData\CMBX Data Explorer Workspace\KB\Method Script Generator\TCC\report_template_cmbx\PressureEvaluation.cmbx
  template_name: PressureEvaluation
generation_mode: clone_and_patch
workbook_policy: existing_cells_only
---

## Sheet: Sheet2

### Workbook Value: A52
```yaml
operation: replace
value_type: number
value: 1
```

### Workbook Value: B52
```yaml
operation: replace
value_type: number
value: 1
```

### Workbook Formula: C52
```yaml
operation: replace
formula: '=A52+B52'
```

### Workbook Formula: D52
```yaml
operation: replace
formula: '=IF(A52=1,B52=1)'
```
