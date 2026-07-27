# Vanquish VVWD FOQ TD Test Logic Knowledge Base

Source TD:

```text
C:\ProgramData\CMBX Data Explorer Workspace\KB\FOQ TD\FOQ_Testdescription_VVWD.docm
```

Document metadata extracted from the TD:

```text
Title: FOQ Test Description (FOQ_TD)
Subject: VVWD
Agile number: DOC0000395
Revision: 2.05
Date: 27-Apr-2021
Owner: Veronika Kainhuber
```

## Scope

Affected instruments:

```text
VF-D40-A
VC-D40-A
VA-D40-A
```

中文理解：

```text
这份 TD 描述 Vanquish Variable Wavelength Detector 的 FOQ。检测器 FOQ 分成两大类：
使用诊断池/内部光学路径的光学诊断测试，以及使用 flow cell 和标准品进样的色谱响应测试。
```

## Current Reverse Status

This KB is TD-first. It captures detector test intent and likely report calculation families. Exact method commands and report formulas need representative VVWD CMBX packages.

Generation readiness:

```text
TD test principle: high
Optical diagnostic logic: medium-high
Method command details: partial
Report formula alignment: pending CMBX evidence
Direct CMBX generation: not ready
```

## Test Groups

### Tests With Diagnostic Cell

```text
Warm Up
Noise and Drift
Wavelength Accuracy with D-alpha and Holmium Oxide Filter lines
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
| Warm Up | UV lamp and optics become stable enough for qualification. | Method turns lamp on, waits, performs wavelength calibration/validation and D-alpha peak finding. |
| Noise and Drift | Low-frequency detector noise and baseline drift stay within limits after warmup. | Method records signal for about 21 minutes; report splits into one-minute intervals and ignores the first interval. |
| Wavelength accuracy | Internal D-alpha and HoFi references produce expected wavelength positions. | Method invokes wavelength validation and find-peak functions; report compares observed peaks to nominal wavelengths. |
| Dark current drift | Dark current/reference/slope are stable over time. | Method records dark-current properties at start/end; report calculates differences and pass/fail. |
| Stray light | Optical blocking/filter behavior stays within limits. | Method uses service-level or fixed ADC/filter/wavelength states; report evaluates measured stray-light response. |
| Spectral scan | Spectral behavior across defined wavelength ranges is plausible. | Method scans wavelengths; report checks scan response features. |
| Intensity | Lamp/filter intensities meet criteria. | Report evaluates measured intensity values or ratios. |
| Spectral resolution | Optical resolution is adequate. | Report likely calculates FWHM or peak width around reference lines. |
| Holmium filter | HoFi transmission and line positions are correct. | Method inserts/uses HoFi; report checks line/ratio values. |
| Second order filter | Second-order filter transmission/ratio is correct. | Method toggles filter states; report compares response with/without filter. |

## Flow-Cell Test Logic

| Test | What it proves | Method/report meaning |
|---|---|---|
| Linearity | Detector response is linear for caffeine concentration/response range. | Report performs regression over standards and rejects wrong data sets or insufficient high-standard response. |
| Saturation | Detector saturation behavior is detected and bounded. | Report evaluates max/min signal in saturation windows for UV/VIS or UV-only cases. |
| RI sensitivity | Detector response to refractive-index changes stays within limits. | Method creates solvent-gradient steps; report evaluates dynamic and static RI peaks. |
| Wavelength accuracy with standards | Injected caffeine and erbium standards produce correct spectral maxima. | Report fits a second-order polynomial around measured wavelengths and derives peak position. |
| Noise and Drift | Detector baseline with flow cell stays stable. | Report evaluates one-minute intervals and drift at selected wavelengths. |
| Wavelength repeatability | D-alpha line can be found repeatedly with acceptable repeatability. | Method repeats D-alpha peak finding; report evaluates repeatability range/SD. |
| PPP check and set | Qualification/service state and protection parameters are correct. | Method sets or verifies PPP/qualification service state. |
| Factory defaults | Detector defaults and logs are reset/verified. | Method sets defaults and clears/checks logs; report verifies expected properties. |

## Likely CM Command Families

Commands and properties to search in method scripts:

```text
Lamp On/Off or UV/VIS lamp state
Wavelength setpoints
WavelengthValidation
FindPeak
Dark current logging
ADC mode
Filter / shutter state
Spectral scan commands
Signal acquisition channels
AcqOn / AcqOff
RetTimes logging
Audit property logging
SetFactoryDefault
Qualification service state
```

## Report Calculation Themes

Expected report calculations:

```text
One-minute interval noise and drift
Linear regression and residual/noise logic
Peak maximum / wavelength position
Second-order polynomial vertex for wavelength accuracy with standards
FWHM / spectral resolution
Intensity and transmission ratios
Dark-current drift
Linearity regression and correlation
Saturation max/min windows
RI dynamic/static response
```

## Method/Report Alignment Work

Next reverse steps:

```text
1. Extract representative VVWD CMBX packages.
2. Align each diagnostic and flow-cell injection to its instrument method and report sheet.
3. Capture exact CM command syntax for lamp, wavelength, filter, scan, and peak-find actions.
4. Capture report formulas for interval noise, polynomial wavelength position, and linearity.
5. Split generation rules by UV-only and UV/VIS configuration.
```

