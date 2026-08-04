# Vanquish Pumps FOQ TD Test Logic Knowledge Base

Source TD:

```text
C:\ProgramData\CMBX Data Explorer Workspace\KB\FOQ TD\FOQ_Testdescription_VPump.docm
```

Document metadata extracted from the TD:

```text
Title: FOQ Test Description (FOQ_TD)
Subject: Vanquish Pumps
Agile number: DOC0000271
Revision: 8.02
Date: 31-Aug-2023
Owner: Markus Chlup
```

## Scope

Affected instruments listed in the TD extraction:

```text
VH-P10-A-02
VF-P20-A
VF-P10-A-01
VF-P32-A-01
VC-P10-A-01
VC-P20-A-01
VC-P21-A-01
VC-P32-A-01
VC-P33-A-01
VC-P40-A-01
VA-P21-A-01
```

Note:

```text
The extracted approval text also mentions VA-P20-A-01. Treat VA pump model coverage as
requiring CMBX/report confirmation before generation.
```

中文理解：

```text
这份 TD 描述 Vanquish 泵模块 FOQ。泵 FOQ 的核心是压力、流速、脉动、梯度、
溶剂选择和脱气机等行为。它比 TCC 更依赖系统流路、溶剂、压力传感器、混合器、
泵头类型和 LPG/HPG/DGP 配置。
```

## Current Reverse Status

This KB is TD-first. It captures the pump FOQ test principles and known dependency structure. Exact CM command sequences and report formulas need representative pump CMBX packages.

Generation readiness:

```text
TD test principle: high
Required hardware/config awareness: high
Method command details: partial
Report formula alignment: pending CMBX evidence
Direct CMBX generation: not ready
```

## FOQ Process Shape

Main TD areas:

```text
Test setup and specification
Schematic test setup
Chromatographic test conditions
Hardware requirements
Solvents
CM instrument configuration
Acceptance criteria
Instrument preparation
Calibration
Shipping status / maintenance
FOQ tests
Appendix: Chromeleon signal-noise calculation
```

## Instrument Preparation and Calibration

| Step | Purpose | Generation implication |
|---|---|---|
| Burn-In | Exercises pump mechanics/fluidics before qualification. | Method needs long-running pressure/flow/solvent actions, with correct solvent and waste setup. |
| Reset logging counters | Clears or standardizes pump counters/log state before tests. | Requires service or diagnostic commands and audit trace. |
| Purge pump | Removes air and prepares solvent path. | Requires purge commands and correct solvent line setup. |
| Tightness test | Verifies fluidic tightness under pressure. | Requires pressure control, valve/flow restrictions, and pressure decay evaluation. |
| Balance check | Checks mechanical/hydraulic balance behavior. | Likely pressure or piston-related diagnostics. |
| Pressure transducer calibration | HPG-specific pressure transducer calibration. | Depends on pump family and available calibration commands. |
| Pressure sensor calibration | VF/VC pressure sensor calibration. | Depends on pump family and sensor command set. |
| Flow rate calibration | Calibrates measured/actual flow behavior. | Requires flow measurement reference or TD-defined calibration flow path. |
| X-value calibration | LPG/DGP proportioning calibration. | Requires solvent channels and composition logic. |

## FOQ Test Logic

| FOQ test | What the test proves | Method/report meaning |
|---|---|---|
| Flow rate accuracy and precision | Pump delivers correct and repeatable flow. | Method creates stable flow steps; report evaluates measured flow/pressure-derived values against limits. |
| Pulsation | Pump pressure ripple stays within limits. | Method records pressure signal at stable flow; report calculates noise/pulsation statistics. |
| Pressure sensor check | Pressure reading is plausible and within tolerance. | Report uses pressure sensor values, possibly against expected pressure under known restriction. |
| Filter permeability | Flow restriction/filter is not blocked beyond allowed pressure behavior. | Method holds flow through filter path; report evaluates pressure/permeability criteria. |
| Gradient accuracy | Solvent proportioning matches programmed gradient. | Requires detector or concentration-sensitive response; report evaluates response/gradient curve. |
| Solvent selector test | HPG solvent selector ports switch correctly. | Applies only to HPG pump variants; report checks expected solvent channel response/state. |
| Relays / digital inputs | Pump I/O functions are correct. | Method toggles/reads I/O; report uses audit/property states. |
| Qualification service | Service state and qualification metadata are recorded. | Method/report writes or checks service-done status. |
| Degasser pressure test | Degasser reaches and holds pressure/vacuum behavior. | Applies to LPG/HPG/DGP variants with degasser; report evaluates pressure/vacuum trace. |

## Key Pump Dependencies

Pump FOQ is configuration-sensitive:

```text
Pump family: HPG / LPG / DGP / isocratic / binary / quaternary
Pump head and piston configuration
Pressure sensor/transducer type
Solvent lines and solvent selector availability
Degasser availability
Static mixer configuration
Restriction/filter/capillary setup
Detector availability for gradient tests
Chromeleon instrument configuration and service-level command access
```

## Report Calculation Themes

Expected report calculations from TD topics:

```text
Pressure drift / pressure drop
Pressure ripple / pulsation
Flow accuracy and precision
Gradient response linearity or deviation
Solvent selector state or response verification
Degasser pressure/vacuum behavior
Signal noise calculation using Chromeleon noise semantics
```

## Method/Report Alignment Work

Next reverse steps:

```text
1. Collect representative CMBX packages for HPG, LPG, DGP, and quaternary variants.
2. Extract each injection and method script.
3. Map method commands to TD sections:
   - purge
   - tightness
   - pressure calibration
   - flow calibration
   - gradient
   - degasser
4. Extract report templates and identify formulas used for pump DB fields.
5. Split generation rules by pump hardware family.
```

