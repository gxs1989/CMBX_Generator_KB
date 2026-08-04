# CM Instrument Configuration Knowledge Base

This note records configuration evidence that affects whether a generated Chromeleon instrument method can run on a real instrument. It complements the report/formula and method-command knowledge bases.

## Why Configuration Matters

Instrument method commands are not globally available CM symbols. They depend on the configured instrument tree, driver, module options, subdevices, and virtual channels.

For TCC generation, this means a valid method payload is not enough. The target CM instrument must expose the required devices and properties, for example:

```text
ColumnComp.CC.Temperature.Nominal
ColumnComp.CC.TempReady
ColumnComp.UpperValve.CurrentPosition
ColumnComp.LowerValve.CurrentPosition
ColumnComp.PrehtLeft.TempCtrl
ColumnComp.PrehtRight.TempCtrl
Thermometer1.ExtTemp_UpperCC
Thermometer1.ExtTemp_LowerCC
Thermometer.Environment_Temperature
```

If the configured CM instrument lacks a device, subdevice, property, command, or channel, the generated method may load but cannot execute correctly.

## Local Evidence Sources

Chromeleon installation files:

```text
C:\Program Files (x86)\Thermo\Chromeleon\bin\FOQVTCC.GEN
C:\Program Files (x86)\Thermo\Chromeleon\bin\TCC100.CDD
C:\Program Files (x86)\Thermo\Chromeleon\bin\UM3_TCC.CDD
C:\Program Files (x86)\Thermo\Chromeleon\bin\QualificationTemplates\Instrument\IQ\HPLC_Templates\Checks.xml
C:\Program Files (x86)\Thermo\Chromeleon\bin\QualificationTemplates\Instrument\OQ_PQ\HPLC_Templates\Checks.xml
```

CMBX evidence:

```text
C:\ProgramData\CMBX Data Explorer Workspace\packages\TCC Cost Out\Zollner\Production\0000003.cmbx
C:\ProgramData\CMBX Data Explorer Workspace\packages\TCC Cost Out\Zollner\Production\3000004.cmbx
C:\ProgramData\CMBX Data Explorer Workspace\packages\TCC Cost Out\Zollner\Production\6000001.cmbx
```

Decoded method evidence:

```text
knowledge_base/tcc_reverse_probe/<VA|VC|VH>/<sequence>/<method>_embedded_method_flow.txt
```

## TCC Driver and Device Macros

Chromeleon qualification checks identify Vanquish TCC with:

```xml
//Device[Property[@Name='DriverID' and @Value='Thermo.Vanquish.TCC']][1]/@Name
```

The same checks define Vanquish TCC subdevices:

```xml
//Device[Property[@Name='InternalName' and @Value='0:CC']][1]/@Name
//Device[Property[@Name='InternalName' and @Value='0:sCC']][1]/@Name
//Device[Property[@Name='InternalName' and @Value='0:PCC']][1]/@Name
```

Working interpretation:

```text
ColumnOven -> Vanquish TCC main module, mapped in FOQ methods as ColumnComp
CC         -> column compartment controller
sCC        -> column oven temperature signal subdevice
PCC        -> post-column cooler, VH-only for FOQ PCC tests
```

## Valve Configuration

Official qualification checks detect valves through `CurrentPosition` and internal names:

```xml
//Device[((Property[@Name='Position'] or
  (Property[@Name='CurrentPosition'] and Property[@Name='InternalName' and @Value='0:LowerValve']))
  and not(Command[@Name='Inject']))][1]/@Name

//Device[((Property[@Name='Position'] or
  (Property[@Name='CurrentPosition'] and Property[@Name='InternalName' and @Value='0:UpperValve']))
  and not(Command[@Name='Inject']))][1]/@Name
```

Decoded TCC FOQ valve methods use:

```text
ColumnComp.UpperValve.CurrentPosition = 6_1
ColumnComp.LowerValve.CurrentPosition = 6_1
ColumnComp.UpperValve.CurrentPosition = 1_2
ColumnComp.LowerValve.CurrentPosition = 1_2
Log UpperValve.Precision
Log LowerValve.Precision
```

Driver strings in `UM3_TCC.CDD` include:

```text
ValveRight
ValveLeft
RightValveErrors
RightValveSwitches
RightValveDesc
RightValveType
RightValvePositions
RightValvePorts
LeftValveErrors
LeftValveSwitches
LeftValveDesc
LeftValveType
LeftValvePositions
LeftValvePorts
rotor seal of the left valve
rotor seal of the right valve
```

Generation implication:

- A valve method requires configured upper/lower valve subdevices, not only a TCC main module.
- The allowed position values must come from the actual configured valve type/ports.
- For the current FOQ examples, `6_1` and `1_2` are verified position strings.

## External Temperature Channels

Official OQ/PQ checks state that automated data acquisition for column oven temperature accuracy requires either:

```text
an analog channel / Integrator driver
or a controlled thermometer with a Temperature_1 property assigned to a virtual channel
```

Manual data acquisition uses:

```text
STH_manual.External_Temperature
```

The checks also emit this requirement when the required virtual channel is missing:

```text
$ColumnOven Temp. Acc. test: A channel 'TemperatureOven' is required!
```

TCC FOQ reports and methods currently use more specific factory-test channel names:

```text
Thermometer1.ExtTemp_UpperCC
Thermometer1.ExtTemp_LowerCC
Thermometer.Environment_Temperature
```

Generation implication:

- A generated FOQ package must either target a CM configuration that already exposes these channels, or include a validated setup/import step that creates the equivalent virtual channels.
- Report formulas that reference `FixedChannel = ExtTemp_UpperCC` or `ExtTemp_LowerCC` only work if those raw channels are collected during the injection.

## PCC and VH-Specific Configuration

Official OQ/PQ checks identify the post-column cooler through:

```xml
//Device[Property[@Name='InternalName' and @Value='0:PCC']][1]/@Name
```

For full-range column oven temperature accuracy, the checks warn:

```text
$ColumnOven Temp. Acc. test: Full range! Connected Post-Column-Cooler required!
```

Decoded FOQ confirms PCC is only part of the VH sequence:

```text
VH-C10-A -> Temperature Stability_and_PCC_H
VC/VA    -> Temperature Stability_C
```

Generation implication:

- VH methods that touch PCC command paths require a configured PCC subdevice.
- VC/VA packages should not blindly include VH PCC checks.

## Column ID and Preheater Options

FOQ report formulas read column IDs through audit paths such as:

```text
AUDIT.Column_A.Description(0,"forward")
AUDIT.Column_B.Description(0,"forward")
AUDIT.Column_C.Description(0,"forward")
AUDIT.Column_D.Description(0,"forward")
```

FOQ preheater methods use:

```text
ColumnComp.PrehtLeft.TempCtrl
ColumnComp.PrehtRight.TempCtrl
ColumnComp.PrehtLeft.Temperature.Nominal
ColumnComp.PrehtRight.Temperature.Nominal
ColumnComp.PrehtLeft.TempReady
ColumnComp.PrehtRight.TempReady
```

Generation implication:

- Column ID checks require the instrument configuration and inserted chip cards to expose the expected audit properties.
- Preheater connection tests require left/right preheater subdevices and simulator/test hardware.

## Proposed Configuration Validation Gate

Before generating or running a method, validate a required-symbol manifest:

```text
device_model: AUDIT.ColumnComp.ModelNo
required_devices:
  ColumnComp
  ColumnComp.CC
required_optional_devices:
  ColumnComp.PCC                 # VH only
  ColumnComp.UpperValve          # valve test only
  ColumnComp.LowerValve          # valve test only
  ColumnComp.PrehtLeft           # preheater test only
  ColumnComp.PrehtRight          # preheater test only
required_channels:
  Thermometer1.ExtTemp_UpperCC
  Thermometer1.ExtTemp_LowerCC
  Thermometer.Environment_Temperature
required_audit_properties:
  ColumnComp.ModelNo
  ColumnComp.SerialNo
  ColumnComp.FirmwareVersion
  ColumnComp.HardwareVersion
```

The first implementation can validate this against decoded CMBX audit/precondition/channel evidence. A later Chromeleon-connected validator should validate against the live CM instrument configuration before package generation.

The first concrete TCC manifest is documented in:

```text
TCC_REQUIRED_SYMBOL_MANIFEST.md
knowledge_base/tcc_required_symbol_manifest.json
```
