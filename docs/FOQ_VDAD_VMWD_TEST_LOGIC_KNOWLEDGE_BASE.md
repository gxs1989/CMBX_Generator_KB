# Vanquish VDAD/VMWD FOQ TD Test Logic Knowledge Base

Source TD:

```text
C:\ProgramData\CMBX Data Explorer Workspace\KB\FOQ TD\FOQ_TestDescription_VDAD-F_VDAD-C_VMWD-C_AgRev_002_00.pdf
```

Document metadata extracted from the PDF:

```text
Title: FOQ_TestDescription_VDAD-F_VDAD-C_VMWD-Cm
Source title in document: FOQ Test Description (FOQ_TD) for VDAD-F, VDAD-C and VMWD-C
Agile number: DOC0000731
Revision: 2.00
Date: 26-Aug-2019
Owner: Veronika Kainhuber
Author metadata: EKugelma
```

## Scope

Affected instruments:

```text
VF-D11-A
VC-D11-A
VC-D12-A
```

中文理解：

```text
这份 TD 描述 Vanquish DAD/MWD 类检测器 FOQ。测试结构和 VVWD 很相似：
一部分是内部/诊断池光学测试，一部分是 flow cell 加标准品/溶剂梯度的响应测试。
VDAD/VMWD 的差异重点在多波长/二极管阵列相关的通道、扫描和报告计算。
```

## Current Reverse Status

This KB is TD-first. It captures test intent and likely report calculation families. Exact method command syntax and report formulas need representative VDAD/VMWD CMBX packages.

Generation readiness:

```text
TD test principle: high
Detector optical logic: medium-high
Method command details: partial
Report formula alignment: pending CMBX evidence
Direct CMBX generation: not ready
```

## Test Groups

### Tests With Diagnostic Cell

```text
Warm Up
Noise
Internal Wavelength Accuracy
Dark Current Drift
Stray Light Test
Spectral Scan
Intensity Test
Spectral Resolution Test
Holmium Filter Test
Second Order Filter Test
```

### Tests With Flow Cell

```text
Linearity, including system check
Saturation
RI Sensitivity
Wavelength Accuracy with injection of standard compounds
Noise and Drift
Wavelength Repeatability with D-alpha line
PPP check and set
Factory Defaults
```

## Diagnostic-Cell Test Logic

| Test | What it proves | Method/report meaning |
|---|---|---|
| Warm Up | Lamp and optics stabilize before qualification. | Method controls lamp state and calibration/validation routines; report checks warmup-related readiness values. |
| Noise | Baseline noise under diagnostic conditions is within limit. | Method records diagnostic signal; report evaluates noise using TD/Chromeleon noise semantics. |
| Internal wavelength accuracy | Internal D-alpha and/or HoFi references are found at correct positions. | Method performs validation/peak finding; report compares found peaks to nominal reference values. |
| Dark current drift | Detector dark-current related properties do not drift excessively. | Method records start/end dark-current values; report calculates drift. |
| Stray light | Internal filters and optical blocking behavior meet criteria. | Method uses specific lamp/filter/wavelength/ADC conditions; report evaluates response ratios or limits. |
| Spectral scan | The spectral response is valid over defined ranges. | Method performs scan; report checks expected spectral features. |
| Intensity | Lamp and optical path intensity are sufficient. | Report checks absolute/relative intensity values. |
| Spectral resolution | Reference peaks have acceptable peak width/resolution. | Report calculates FWHM or similar resolution metrics. |
| Holmium filter | HoFi lines and transmission behavior are correct. | Report evaluates line positions/transmission values. |
| Second order filter | Second-order filter behavior is correct. | Report compares transmission/response with filter states. |

## Flow-Cell Test Logic

| Test | What it proves | Method/report meaning |
|---|---|---|
| Linearity | Detector response is linear across standard concentrations. | Report performs regression and system check before accepting linearity. |
| Saturation | Detector saturation behavior is detected and controlled. | Report evaluates signal max/min windows at relevant wavelengths. |
| RI sensitivity | Baseline response to refractive-index changes stays within limits. | Method creates solvent composition changes; report evaluates dynamic/static peaks. |
| Wavelength accuracy with standards | Injected caffeine/erbium standards produce correct wavelength maxima. | Report fits local response around expected maxima and derives observed wavelength. |
| Noise and drift | Flow-cell baseline is stable. | Report evaluates interval noise and drift with Chromeleon-style formulas. |
| Wavelength repeatability | D-alpha line finding is repeatable. | Report evaluates repeated found wavelengths. |
| PPP check and set | Qualification/service protection state is correct. | Method checks/sets service state. |
| Factory defaults | Detector defaults and logs are set/verified. | Report checks final property state. |

## VDAD/VMWD-Specific Generation Notes

Potential additional model-specific dependencies:

```text
Single-wavelength vs multi-wavelength acquisition
DAD scan/channel setup
UV and/or VIS lamp availability
Diagnostic cell vs flow cell installation
Holmium and second-order filter availability
ADC mode and signal range configuration
Wavelength validation permissions
Service-level commands for optical diagnostics
```

## Report Calculation Themes

Expected report calculations:

```text
Chromeleon noise and drift
Reference peak wavelength deviation
Dark current drift
Stray-light response/ratio
Spectral scan peak/shape checks
Intensity and transmission ratios
Spectral resolution / FWHM
Linearity regression
Saturation max/min response
RI sensitivity peaks
Wavelength repeatability
```

## Method/Report Alignment Work

Next reverse steps:

```text
1. Extract representative VDAD-F, VDAD-C, and VMWD-C CMBX packages.
2. Align every TD test with injection name, instrument method, processing method, and report sheet.
3. Capture exact commands for lamp, wavelength, scan, filter, ADC, validation, and peak-find behavior.
4. Extract report formulas and identify DB mapping fields.
5. Split generation rules by detector family and installed optical options.
```

