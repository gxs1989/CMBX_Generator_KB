# Vanquish Autosamplers FOQ TD Test Logic Knowledge Base

Source TD:

```text
C:\ProgramData\CMBX Data Explorer Workspace\KB\FOQ TD\FOQ_Testdescription_VAS.docm
```

Document metadata extracted from the TD:

```text
Title: FOQ Test Description (FOQ_TD)
Subject: Vanquish Autosamplers
Agile number: DOC0000273
Revision: 8.01
Date: 28-Apr-2023
Owner: Dominik Schuler
```

## Scope

Affected instruments:

```text
VH-A10-A
VH-A40-A
VF-A10-A
VF-A40-A
VC-A12-A
VC-A13-A
VA-A12-A
```

中文理解：

```text
这份 TD 描述 Vanquish 自动进样器 FOQ。核心不是单个色谱结果，而是通过一组
有依赖关系的 injection 来验证自动进样器的流路密封、进样体积、机械驱动、冷却、
继电器/输入和工厂默认值。
```

## Current Reverse Status

This KB is TD-first. It captures the test intent and the expected method/report contract. The exact Chromeleon method command script and report cell formulas still need to be aligned from representative CMBX packages for each autosampler family.

Generation readiness:

```text
TD test principle: high
Required sequence/injection order: medium-high
Method command details: partial
Report formula alignment: pending CMBX evidence
Direct CMBX generation: not ready
```

## FOQ Process Shape

The TD states that the sequence order matters. Several later injections depend on preparations, equilibrations, standards, or state changes from earlier injections.

Main functional blocks:

```text
Instrument preparation
Burn-In
Factory default / equilibration / system flush / flow adjustment
Automatic leakage check
Carry-over with caffeine
Drive functionality
Injection volume precision
Injection volume linearity
Cooling performance
Relays and inputs
Factory defaults / final checks
```

## Injection Logic

| FOQ area | What the injection proves | Method/report meaning |
|---|---|---|
| Instrument preparation | The autosampler, fluidics, vials, solvents, and restriction setup are ready. | Mostly setup-dependent. The sequence must assume the correct external LC system and vial/rack positions. |
| Burn-In | Repeated autosampler actions exercise fluidics and mechanical drives before measured tests. | Method commands likely drive injections, needle/metering movements, valve actions, and temperature/control initialization. Report use is usually limited or diagnostic. |
| Factory default | Autosampler property values are reset to defined defaults. | Uses a factory-default command such as `SetFactoryDefault`; report checks expected property values, often on internal-use sheets. |
| Equilibration / system flush | The fluidic system is brought to stable flow and solvent state. | Creates a stable baseline for carry-over, precision, and linearity tests. |
| Flow adjustment | Flow is adjusted to reach the pressure/flow condition required by later tests. | Report may use pressure/flow diagnostics and internal variables, not only chromatographic peak results. |
| Automatic leakage check | The autosampler fluidic path must not show significant leakage. | Two pressure-test style injections are described: injector pressure test by system and by pump. Valve positions block flow similar to a plug while pump maintains pressure. |
| Carry-over | After a high caffeine sample, blank solvent must not contain unacceptable residual caffeine. | Report calculates carry-over in ppm from standard/background response and carry-over sample/blank response. |
| Drive functionality | Needle, compression, metering, and horizontal/vertical drives initialize and return within allowed home deviations. | Method invokes initialization or drive-related firmware actions; report evaluates drive properties/deviations. |
| Injection volume precision | Ten repeated injections should have acceptable repeatability. | Report evaluates peak area precision, generally RSD/SD from replicate injections. |
| Injection volume linearity | Different injected or idle-volume settings must produce a linear response. | Report evaluates regression/correlation/RSD and compares slopes, including extended linearity for metering-drive mounting/lead-screw issues. |
| Cooling performance | Autosampler cooling reaches and holds required behavior. | Method controls tray/sample cooling; report evaluates temperature behavior over timed windows. |
| Relays / digital inputs | I/O functions are exercised. | Method toggles or reads I/O states; report likely checks audit/property values. |

## Important TD Details

### Automatic Leakage Check

TD interpretation:

```text
The leakage check is not a chromatographic peak test. It puts the autosampler valve/fluidic path
into blocked or pressure-test positions and observes whether pressure can be maintained.
```

Expected method elements:

```text
Set valve/fluidic position for injector pressure test
Coordinate with pump pressure control
Wait or monitor pressure behavior
Record audit/property values needed by report
Use live leak test logic for high leak rate detection
```

Expected report elements:

```text
Pressure decay / leak-rate related values
Pass/fail against TD criteria
Audit/property trace of pressure-test state
```

### Carry-Over

TD interpretation:

```text
Carry-over is built from an ordered caffeine sequence: flow adjustment/equilibration,
low standards, high sample, then solvent blank. The blank after the high sample reveals
residual carry-over.
```

Expected method/report contract:

```text
Standards provide calibration/background response
High concentration sample stresses the flow path
Following solvent blank measures carry-over residue
Report calculates ppm using response slope/background logic
```

### Drive Functionality

TD interpretation:

```text
Drive functionality verifies mechanical home positions and initialization behavior, not only
successful injection completion.
```

Expected method elements:

```text
Sampler initialization command
Drive initialization or movement commands
Audit/property logging for drive deviations
```

Expected report elements:

```text
Needle vertical drive home deviation
Needle horizontal drive home deviation
Compression drive home deviation
Metering drive home deviation
Pass/fail against TD limits
```

### Injection Volume Precision

TD interpretation:

```text
Precision uses replicate injections of the same sample. The autosampler should deliver the
same volume repeatedly.
```

Expected report elements:

```text
Peak area list from replicate injections
Average / standard deviation / RSD
Pass/fail against precision limit
```

### Injection Volume Linearity

TD interpretation:

```text
Linearity checks whether response changes linearly with programmed volume or idle-volume
related settings. Extended linearity is intended to reveal mechanical mounting or lead-screw
issues along the metering device.
```

Expected report elements:

```text
Volume-response regression
Correlation coefficient
Slope and intercept
RSD or residual criteria
Comparison between standard and extended linearity slope
```

## Generation Prerequisites

To generate a runnable autosampler FOQ CMBX, the generator must know:

```text
Autosampler model and option set
Needle/loop/seat configuration
Rack and vial positions
External pump and detector configuration
Solvents and caffeine standards
Restriction capillary / pressure-test setup
Cooling availability
Relays / digital input wiring
Required processing methods and report templates
```

## Method/Report Alignment Work

Next reverse steps:

```text
1. Locate representative VAS CMBX packages for each supported model family.
2. Extract injection list, instrument methods, processing methods, and report templates.
3. Align each TD test block to:
   - injection name
   - instrument method name
   - processing method name
   - report template/sheet
   - key CM commands
   - report formulas and DB mapping fields
4. Convert the alignment into reusable generation rules.
```

