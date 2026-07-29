# RID OQ Method and Report Evidence Inventory

This file is the evidence appendix for `RID_OQ_TEST_KNOWLEDGE_BASE.md`. It records the exact CMBX object names and the report calculation chain needed for later parser, external-report, or generation work.

## 1. Package Identity

| Package | Generator | Container | CM compatibility metadata | Content |
|---|---|---|---|---|
| `OQ 2026-07-28.cmbx` | 7.3.1.6535 | 2.0 | 7.2.3 | 4 sequences, 10 injections, 6 instrument-method definitions, processing methods, shared report |
| `PQ_OQ_Report_9_7.cmbx` | 7.3.1.6535 | 2.0 | 7.2.3 | Standalone report template |

## 2. Injection Binding Matrix

| Sequence | Injection | Instrument Method | Processing Method |
|---|---|---|---|
| OQ_RI_LINEARITY | RI_Detector linearity_1 | RI_DET_LINEARITY | RI_DET_LINEARITY |
| OQ_RI_LINEARITY | RI_Detector linearity_2 | RI_DET_LINEARITY | RI_DET_LINEARITY |
| OQ_RI_LINEARITY | RI_Detector linearity_3 | RI_DET_LINEARITY | RI_DET_LINEARITY |
| OQ_RI_LINEARITY | RI_Detector linearity_4 | RI_DET_LINEARITY | RI_DET_LINEARITY |
| OQ_RI_LINEARITY | RI_Detector linearity_5 | RI_DET_LINEARITY | RI_DET_LINEARITY |
| OQ_RI_NOISE_DRIFT | Equilibration | EQUILIBRATION_RI_AND RF | NOINT |
| OQ_RI_NOISE_DRIFT | RI-Detector noise drift | RI_DET_NOISE_AND_DRIFT | NOINT |
| OQ_STOP | Stop | STOP | NOINT |
| OQ_STOP | Restore | RESTORE | NOINT |
| OQ_WARM_UP | Warm up | WARM_UP | NOINT |

## 3. Instrument Method Evidence

### 3.1 RI_DET_LINEARITY

```text
Instrument Setup:
  RI.Data_Collection_Rate = 5
  RI.Temperature.Nominal = 35
  RI.Purge = off
  RI.Recorder_Range = 512.00
  RI.Integrator_Range = 500
  RI.Rise_Time = 0.50
  RI.Polarity = plus
  RI.Baseline_Shift = 0

0.000 Equilibration: RI.Autozero
0.000 Inject Preparation: Wait RI.Ready
0.000 Start Run: RI.RI_1.AcqOn
2.000 Stop Run: RI.RI_1.AcqOff
```

Method comments specify:

- pressure regulator: 15 m, 0.18 mm ID SST restriction capillary;
- glycerine samples: 5, 10, 15, 25, 35 mg/mL;
- legacy device family: Shodex RI-101 / ERC RefractoMax520.

### 3.2 EQUILIBRATION_RI_AND RF

```text
Solvent: HPLC-grade water
Degassing: online degasser
0.000 Inject Preparation: Wait RI.Ready
0.000 Run: Duration = 1.000 min
```

The method states that correct pump conditions must already exist at the measured injection's negative retention times. No concrete pump property command is present in the decoded generic payload.

### 3.3 RI_DET_NOISE_AND_DRIFT

```text
Instrument Setup:
  RI.Data_Collection_Rate = 0.67
  RI.Temperature.Nominal = 35
  RI.Purge = off
  RI.Rise_Time = 0.50
  RI.Polarity = Minus
  RI.Baseline_Shift = 0

-40.000 Equilibration: Duration = 40.000 min
-40.000 RI.Autozero
-40.000 Wait RI.Ready
-40.000 RI.Purge = On
-39.500 RI.Purge = Off
-39.000 RI.Purge = On
-38.500 RI.Purge = Off
-38.000 RI.Purge = On
-20.000 RI.Purge = Off
-03.000 RI.Autozero
  0.000 Wait RI.Ready
  0.000 RI.RI_1.AcqOn
 22.000 RI.RI_1.AcqOff
```

### 3.4 WARM_UP

```text
RI.Temperature.Nominal = 35
Protocol "Unsupported detector."
0.000 RI.RI_1.AcqOn
Run Duration text = 1.500 min
5.000 RI.RI_1.AcqOff
```

### 3.5 STOP / RESTORE

```text
STOP:
  comment: Slow down to standby conditions: 50 µL/min
  run duration: 1.000 min
  concrete pump command: not present in generic decoded payload

RESTORE:
  comment: Restore Customer Settings
  run duration: 1.000 min
  concrete restored properties: not present in generic decoded payload
```

## 4. Processing Evidence

| Method | Binary evidence | Contract status |
|---|---|---|
| `NOINT` | `Inhibit integration` | Sufficient for direct-signal noise/drift; no peak contract required. |
| `RI_DET_LINEARITY` | Component `Glycerine`, concentration-level structures, linear calibration structures | Partial. Exact integration and calibration settings are not decoded. |

## 5. Report Sheet Selection

| Sheet | IsActive | Query |
|---|---|---|
| RI_NOISE_AND_DRIFT | Y | `injname EndsWith "RI-Detector noise drift"` |
| RI_LINEARITY | Y | `injname Equal "RI_Detector linearity_5"` |
| SPECIFICATION | Y | Shared definitions and runtime metadata; visible query is tied to Warm up |
| RESULTS_AND_HEADERS | N / each injection | Hidden shared text/formula support |
| Audit Trail | N / each injection | Generic audit table |

## 6. RI Noise and Drift Formula Trace

### 6.1 Direct CM cells

For rows 149–168, let `k = row - 147`, producing windows 2–3 through 21–22 min:

| Cell | Formula |
|---|---|
| `F149:F168` | `chm.sig_value("drift", k, k+1)*60` |
| `G149:G168` | `chm.noise(k, k+1)` |
| `C172` | `chm.sig_dim` |

### 6.2 Unit normalization and absolute drift

```text
C149:C168 = IF(C172="nRIU",ABS(Frow),ABS(Frow*1000))
D149:D168 = IF(C172="nRIU",Grow,Grow*1000)
```

### 6.3 Display table and aggregate

```text
C53:C72 = D149:D168                  # Noise [nRIU]
D53:D72 = C149:C168                  # Amount of Drift [nRIU/h]
C73 = IF(COUNT(C53:C72)<>20,"Test incomplete",ROUND(AVERAGE(C53:C72),1))
D73 = IF(COUNT(D53:D72)<>20,"Test incomplete",ROUND(AVERAGE(D53:D72),1))
C75 = IF(C73<=50,"ok","not ok")
D75 = IF(D73<=2500,"ok","not ok")
```

### 6.4 OQ definition cells

| Cell | Label | Value |
|---|---|---:|
| SPECIFICATION!C159/D159 | Noise (RI) | 50 |
| SPECIFICATION!C160/D160 | Drift (RI) | 2500 |

## 7. RI Linearity Formula Trace

### 7.1 Dynamic peak table

`RI_LINEARITY!B53:E58` is a `peak_summary` table:

| Column | Formula / binding |
|---|---|
| B | `smp.name` |
| C | `peakTab.amount`, component Glycerine, channel `$RI_1` |
| D | `peak.area`, component Glycerine, channel `$RI_1` |
| E | `peak.height`, component Glycerine, channel `$RI_1` |

### 7.2 Calibration cells

| Cell | Direct CM formula | Binding |
|---|---|---|
| B80 | `peak.calibration_type` | `$RI_1`, Glycerine |
| C80 | `peak.nCalpoints` | `$RI_1`, Glycerine |
| D80 | `peak.offset` | `$RI_1`, Glycerine |
| E80 | `peak.slope` | `$RI_1`, Glycerine |
| C84 | `peak.correlation_coefficient` | `$RI_1`, Glycerine |

### 7.3 FormulaOne result

```text
C41 = 99.9
D41 = IF(C80=5,ROUND(C84,3),"Test incomplete")
C86 = IF(
          AND(ISNUMBER(C84),C80=5),
          IF(ROUND(C84,3)>=C85,"ok","not ok"),
          "not ok"
       )
F41 = IF(C86="ok","Test passed","Test failed")
```

## 8. FormulaOne Extraction Note

This report contains a 3,932,160-byte FormulaOne workbook and 2,588 non-empty workbook formulas. The .NET inventory host input limit was raised to `Int32.MaxValue`; without that change, the base64 workbook exceeded the default `JavaScriptSerializer` input size.

## 9. Evidence Gaps

1. Processing Method `RI_DET_LINEARITY` integration/calibration parameters.
2. Pump flow and composition commands in configured rather than generic methods.
3. Sampler injection volume and sequence amount/custom-column values.
4. Runtime channel binding for noise/drift objects with empty `FixedChannel`.
5. Completed raw-data comparison against Chromeleon output.
6. Controlled OQ TD/SOP classification of each criterion.

