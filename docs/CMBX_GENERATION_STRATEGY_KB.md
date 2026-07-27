# CMBX Generation Strategy KB

This KB connects FOQ intent, CMBX execution evidence, report formulas, and generation guardrails.
It is a strategy layer, not proof that a generated method/report/CMBX is runnable.

## 1. Method Generation Rules

| Rule ID | Family | Rule | Basis | Evidence Status |
|---|---|---|---|---|
| TCC_METH_01 | TCC | Temperature Accuracy and Stability branches that use corrective processing must preserve IRC/corrective processing bindings. | FOQ KB + CMBX sequence links: `ACCURACY_IRC_STOP_H` and `CORRECT_*` processing methods are bound to relevant injections. | verified for TCC reference CMBX; exact pass action still needs deeper processing-method decode |
| TCC_METH_02 | TCC | If target model is `VH-C10-A`, include the PCC stability/performance branch. | FOQ KB comparison + TCC alignment: VH maps Temperature Stability and PCC to `TEMPERATURE_STABILITY_AND_PCC_70_H`. | verified for TCC alignment; generation command details still require method-flow validation |
| TCC_METH_03 | TCC | External thermometer channels must exist in the CM instrument configuration before temperature tests are runnable. | FOQ KB key conditions + report formulas depend on `ExtTemp_UpperCC` and `ExtTemp_LowerCC`. | verified as required symbol evidence; live CM config check still manual |
| VDAD_METH_01 | VDAD | Slit-width-specific tests apply only to VDAD-F where adjustable slit behavior exists. | VDAD FOQ KB comparison analysis. | knowledge-only; reference CMBX binding not decoded yet |
| VDAD_METH_02 | VDAD | 3D Field tests are not applicable to VMWD-C. | VDAD FOQ KB process overview and model applicability. | knowledge-only; represented as not applicable in alignment |
| VDAD_METH_03 | VDAD | Noise testing must distinguish Diagnostic Cell and Fluidic Flow Cell evidence. | VDAD FOQ KB test flow overview and troubleshooting logic. | knowledge-only; reference report/method evidence not decoded yet |

## 2. Report Generation Rules

### 2.1 Report Formula Mapping

| Test | Formula ID | Formula | Parameter Sources | Evidence Status |
|---|---|---|---|---|
| TCC Temperature Accuracy | `FORMULA_TCC_TEMP_ACCURACY_MAX_DEVIATION` | `ObservedDeviation = Observed - Nominal`; result uses the larger absolute deviation from upper/lower external thermometers. | Observed: `ExtTemp_LowerCC` and `ExtTemp_UpperCC` average over `RetTimeN-1.0..RetTimeN-0.2`; Nominal: `ColumnComp.CC.Temperature.Nominal`. | verified in TCC evaluator |
| TCC Temperature Stability | `FORMULA_TCC_TEMP_STABILITY_SEPARATE_SENSOR_RANGE` | `RawStability = max(max(Lower)-min(Lower), max(Upper)-min(Upper))`. | Lower/upper ranges from external thermometer raw channels in the report window. | verified in TCC evaluator |
| TCC HeatUp/CoolDown | `FORMULA_TCC_HEATUP_COOLDOWN_RETTIME_DELTA_MINUS_HOLD` | Heat-up and cool-down durations are RetTime deltas minus the 2.0 min stable hold. | HeatUp: `RetTime2 - RetTime1 - 2.0`; CoolDown: `RetTime5 - RetTime4 - 2.0`. RetTime3/6 remain internal endpoint evidence in the report layout. | verified in TCC evaluator and exported workbook |
| VDAD Noise | `FORMULA_VDAD_NOISE_REGRESSION_DEVIATION_OPEN` | Average of interval maximum deviations from regression line. | Expected signal source is UV/VIS detector channel such as `UV_VIS_1`; exact channel and report formula need VDAD CMBX evidence. | open verification |
| VDAD Linearity | `FORMULA_VDAD_LINEARITY_REGRESSION_OPEN` | Regression coefficient r must satisfy the FOQ linearity limit. | Peak area or height versus concentration regression; exact integration/report source requires processing/report decode. | open verification |

### 2.2 Report Template Selection Rules

| Test | Model Branch | Report Template | Report Sheets | Evidence Status |
|---|---|---|---|---|
| TCC Temperature Stability | VH-C10-A | `Report_VTCC_V2_12` | `Temp Stability_Noise`, `PCC` | verified alignment; conceptual alias `TCC_Stability_PCC.rpt` remains unverified |
| TCC Temperature Stability | VC-C10-A / VA-C10-A | `Report_VTCC_V2_12` for VC; `Report_VATCC_V1_01` for VA | `Temp Stability_Noise` | partial; VC/VA no-PCC branch needs loaded CMBX confirmation |
| TCC Temperature Accuracy | VH/VC/VA C10-A | `Report_VTCC_V2_12` for VC/VH; `Report_VATCC_V1_01` for VA | `Temp Accuracy` | verified for VH/VC family, VA template named from evidence but needs full formula trace |
| VDAD Noise | VDAD-F narrow slit | `VDAD_Noise_Narrow.rpt` | `Noise` | strategy placeholder; not verified from CMBX |
| VDAD Noise | VDAD-C / VMWD-C wide slit | `VDAD_Noise_Wide.rpt` | `Noise` | strategy placeholder; not verified from CMBX |

## 3. Cross-Module Test Dependencies

| Dependency | Impact | Evidence Status |
|---|---|---|
| TCC temperature stability -> VDAD Noise | TCC temperature fluctuation can change mobile-phase refractive index and contribute to detector baseline noise. | knowledge hypothesis from module physics; needs system-level validation |
| Pump flow pulsation -> VDAD Noise | Pump pulsation can superimpose periodic noise on detector baseline. | knowledge hypothesis from VDAD troubleshooting; needs pump evidence in system CMBX |
| TCC temperature accuracy -> VDAD wavelength accuracy | Temperature can affect optical/mechanical stability and therefore wavelength accuracy interpretation. | open verification; likely secondary effect and not direct method dependency |

## 4. Configuration Validation Rules

| Validation Item | Check Method | Failure Handling | Evidence Status |
|---|---|---|---|
| IRC assignment | Check sequence injection processing method link and processing-method pass/action semantics. | Reassign the correct processing method or stop generation until confirmed. | sequence link verified; pass/action decode still partial |
| Debug/raw diagnostic channels enabled | Check required channels in CMBX evidence and later in live CM configuration. | Enable required acquisition/debug configuration before running generated method. | partial; CMBX evidence available, live CM check manual |
| External thermometers exist | Check required symbols/channels: `ExtTemp_UpperCC` and `ExtTemp_LowerCC`. | Add/configure Generic Device thermometer channels before running TCC temperature tests. | verified as TCC method/report dependency |

## 5. Generation Guardrail

Rows marked `open verification`, `partial`, or `strategy placeholder` must not be used as runnable generation rules until a reference CMBX method/report/formula trace confirms them.
