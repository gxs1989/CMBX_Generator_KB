# VAS_DVAS_V_3_45 Direct CM Formula Inventory

- **Source CMBX:** `VAS_DVAS_V_3_45.cmbx`
- **Extraction scope:** `SheetObject` direct CM formulas only.
- **Not included:** FormulaOne workbook formulas/layout stored in `SpreadSheetData`.
- **Authoring rule:** Retain the sheet/cell binding and fixed channel/component unless a configuration contract approves a change.

## Summary

- Sheets: 18
- Direct CM formula objects: 139
- Formula namespaces: `audit` (58), `chm` (7), `if` (3), `injection` (4), `left` (1), `peak` (2), `precond` (23), `seq` (11), `smp` (30)

## Sheet Applicability

| Sheet | Active | Each Injection | Query | Injection Variable | Query Values |
|---|---|---|---|---|---|
| History | N | Y | Y |  |  |
| CoC | Y | N | N |  |  |
| Specification | N | Y | Y |  |  |
| Title Page | Y | N | Y |  |  |
| Test Procedures | Y | N | Y |  |  |
| Inj_Precision | Y | N | Y |  |  |
| Inj_Carry_over_RC | Y | N | Y |  |  |
| Inj_Linearity | Y | N | Y |  |  |
| Inj_Linearity_Extended (Int.) | Y | N | Y |  |  |
| Relays_and_Inputs | Y | N | Y |  |  |
| Cooling_Performance | Y | N | Y |  |  |
| Internal_Use_1 | Y | N | Y | injname | Stop |
| Internal_Use_2 | Y | N | Y | injname | Stop |
| Pressure_Test | Y | N | Y | injname | Injector pressure test (Pump) |
| Results_and_Headers | N | Y | Y |  |  |
| Audit Trail | N | Y | Y |  |  |
| Device Configuration | N | Y | N |  |  |
| TA Configuration | N | Y | N |  |  |

## Sheet: CoC

| Cell / Range | Object Type | Formula | Fixed Channel | Fixed Component |
|---|---|---|---|---|
| E34 | ReportFormulaObject | seq.submitOperator.userId |  |  |

## Sheet: Specification

| Cell / Range | Object Type | Formula | Fixed Channel | Fixed Component |
|---|---|---|---|---|
| E15 | ReportFormulaObject | precond.System.serialNo |  |  |
| C14 | ReportFormulaObject | precond.uv.modelno |  | Uracil |
| C16 | ReportFormulaObject | seq.instrument |  |  |
| E14 | ReportFormulaObject | precond.uv.serialno |  |  |
| C13 | ReportFormulaObject | precond.PumpModule.ModelNo |  |  |
| E13 | ReportFormulaObject | precond.PumpModule.SerialNo |  |  |
| E12 | ReportFormulaObject | Precond.SamplerModule.SerialNo |  |  |
| C43 | ReportFormulaObject | seq.update_time |  |  |
| C44 | ReportFormulaObject | precond.System.Version |  |  |
| C45 | ReportFormulaObject | seq.name |  |  |
| C47 | ReportFormulaObject | AUDIT.SamplerModule.Sampler.LoopVolume |  |  |
| C48 | ReportFormulaObject | precond.SamplerModule.Sampler.IdleVolume |  |  |
| C46 | ReportFormulaObject | precond.SamplerModule.Sampler.Location |  |  |
| C12 | ReportFormulaObject | precond.samplermodule.modelno |  |  |
| C42 | ReportFormulaObject | seq.update_operator.userId |  |  |

## Sheet: Title Page

| Cell / Range | Object Type | Formula | Fixed Channel | Fixed Component |
|---|---|---|---|---|
| D35 | ReportFormulaObject | seq.submitOperator.userId |  |  |

## Sheet: Test Procedures

| Cell / Range | Object Type | Formula | Fixed Channel | Fixed Component |
|---|---|---|---|---|
| B75:D80 | ReportTableObject | smp.number \| "No. " \| "" \| "" \| "" \| smp.name \| "Name " \| "" \| "" \| "" \| smp.inject_volume \| "InjVol " \| "µL" \| "" \| "" |  |  |

## Sheet: Inj_Precision

| Cell / Range | Object Type | Formula | Fixed Channel | Fixed Component |
|---|---|---|---|---|
| B53:C58 | ReportTableObject | smp.name \| "Injection Name " \| "" \| "" \| "" \| peak.area \| "Area " \| "mAU*min" \| "UV_VIS_1" \| "Caffeine" |  |  |
| D50 | ReportFormulaObject | smp.inject_volume |  |  |
| B86:D91 | ReportTableObject | smp.name \| "Sample Name " \| "" \| "" \| "" \| chm.sig_value("min") \| "Signal Min. " \| chm.sig_dim \| "Pump_Pressure" \| "" \| chm.sig_value("average",0.1,1) \| "Signal Av. (0.1-1.0 min)" \| chm.sig_dim \| "Pump_Pressure" \| "" |  |  |
| B111:D116 | ReportTableObject | smp.name \| "Sample Name " \| "" \| "" \| "" \| peak.area \| "Area " \| chm.sig_dim+"*min" \| "UV_VIS_1" \| "Caffeine" \| peak.height \| "Height " \| chm.sig_dim \| "UV_VIS_1" \| "Caffeine" |  |  |
| B129:D134 | ReportTableObject | smp.name \| "Sample Name " \| "" \| "" \| "" \| chm.sig_value("average",0,0.1)*1000 \| "Av. Signal 0 to 0.1 min " \| "µAU" \| "UV_VIS_1" \| "" \| chm.sig_value("average",1.4,1.5)*1000 \| "Av. Signal 1.4 to 1.5 min " \| "µAU" \| injection.name \| "UV_VIS_1" \| "" |  |  |
| B144:C149 | ReportTableObject | smp.name \| "Sample Name " \| "" \| "" \| "" \| precond.SamplerModule.Sampler.IdleVolume \| "Idle Volume" \| "µl" \| injection.name \| "" \| "" |  |  |

## Sheet: Inj_Carry_over_RC

| Cell / Range | Object Type | Formula | Fixed Channel | Fixed Component |
|---|---|---|---|---|
| E108 | ReportFormulaObject | audit.Variables.GenericFloat1(0.5,"backward") |  |  |
| J78 | ReportFormulaObject | peak.calCoefficient(1) | UV_VIS_1 | Caffeine |
| J79 | ReportFormulaObject | peak.rQuadrat/100 | UV_VIS_1 | Caffeine |
| B92:J97 | ReportTableObject | Left(smp.name,30) \| "Sample Name " \| "" \| injection.name \| "" \| "" \| peak.retention_time \| "Ret.Time " \| "min" \| "UV_VIS_1" \| "Caffeine" \| peak.area \| "Area " \| chm.sig_dim+"*min" \| "UV_VIS_1" \| "Caffeine" \| chm.nPeaks \| "Number of peaks " \| "" \| injection.name \| "UV_VIS_1" \| "" \| "" \| "" \| "" \| "" \| "" \| chm.signalStatistic("min") \| "Min. Pump Pressure " \| chm.signalUnit \| "Pump_Pressure" \| "" \| chm.signalStatistic("max",0,1.5) \| "Maximum Signal Value (0-1,5)" \| chm.signalUnit \| "UV_VIS_1" \| "" \| peak.height \| "Peak Height " \| chm.signalUnit \| "UV_VIS_1" \| "Caffeine" \| peak.sig_value_baseline \| "BL-Value (RT) " \| chm.signalUnit \| "UV_VIS_1" \| "Caffeine" |  |  |

## Sheet: Inj_Linearity

| Cell / Range | Object Type | Formula | Fixed Channel | Fixed Component |
|---|---|---|---|---|
| B125:D130 | ReportTableObject | smp.name \| "Sample Name " \| "" \| "" \| "" \| chm.sig_value("min") \| "Signal Min. " \| chm.sig_dim \| "Pump_Pressure" \| "" \| chm.sig_value("average",0.1,1) \| "Signal Average " \| chm.sig_dim \| "Pump_Pressure" \| "" |  |  |
| B98:N103 | ReportTableObject | injection.name \| "Injection Name" \| "" \| "" \| "" \| peak.retention_time \| "Ret.Time" \| "min" \| "UV_VIS_1" \| "Caffeine" \| smp.inject_volume \| "Inj.Vol." \| "µL" \| "" \| "" \| peak.area \| "Area" \| chm.signalUnit+"*min" \| "UV_VIS_1" \| "Caffeine" \| peak.correlation_coefficient \| "Corr. Coefficient" \| "%" \| injection.name \| "UV_VIS_1" \| "Caffeine" \| peak.rel_standard_deviation \| "RSD" \| "%" \| "UV_VIS_1" \| "Caffeine" \| peak.calibration_type \| "Cal.Type" \| "" \| "UV_VIS_1" \| "Caffeine" \| peak.nCalpoints \| "Number of Points" \| "" \| "UV_VIS_1" \| "Caffeine" \| peak.calCoefficient(0) \| "Offset" \| "" \| "UV_VIS_1" \| "Caffeine" \| peak.calCoefficient(1) \| "Slope" \| chm.signalUnit+"*min" \| "UV_VIS_1" \| "Caffeine" \| audit.MeteringPos \| "Metering Pos" \| "nL" \| injection.name \| chm.channel \| peak.name \| peak.asymmetry("ep") \| "Asymmetry (EP)" \| "" \| injection.name \| "UV_VIS_1" \| "Caffeine" \| precond.SamplerModule.Sampler.IdleVolume \| "Idle Volume" \| "µl" \| injection.name \| "" \| "" |  |  |

## Sheet: Inj_Linearity_Extended (Int.)

| Cell / Range | Object Type | Formula | Fixed Channel | Fixed Component |
|---|---|---|---|---|
| B55:O60 | ReportTableObject | smp.name \| "Sample Name " \| "" \| "" \| "" \| precond.SamplerModule.Sampler.IdleVolume \| "Idle Volume (Sampler Module.Sampler)" \| "µl" \| injection.name \| "" \| "" \| Audit.MeteringPos \| "Metering Pos" \| "nL" \| chm.channel \| peak.name \| peak.retention_time \| "Ret.Time " \| "min" \| "UV_VIS_1" \| "Caffeine" \| smp.inject_volume \| "Inj.Vol. " \| "µl" \| "" \| "" \| peak.area \| "Area " \| chm.sig_dim+"*min" \| "UV_VIS_1" \| "Caffeine" \| peak.correlation_coefficient \| "Corr.Coeff. " \| "%" \| "UV_VIS_1" \| "Caffeine" \| peak.rel_standard_deviation \| "Rel.Std.Dev. " \| "%" \| "UV_VIS_1" \| "Caffeine" \| "Volume Offset " \| "nL" \| injection.name \| chm.channel \| peak.name \| peak.slope \| "Slope " \| "" \| "UV_VIS_1" \| "Caffeine" \| peak.offset \| "Offset " \| "mAU*min" \| "UV_VIS_1" \| "Caffeine" \| chm.sig_value("average",0.1,1) \| "Signal Average " \| chm.sig_dim \| "Pump_Pressure" \| "" \| peak.nCalpoints \| "#Points " \| "" \| "UV_VIS_1" \| "Caffeine" \| peak.asymmetry("ep") \| "Asymmetry (EP)" \| "" \| injection.name \| "UV_VIS_1" \| "Caffeine" |  |  |
| B83:E88 | ReportTableObject | smp.name \| "Sample Name " \| "" \| "" \| "" \| AUDIT.SamplerModule.Sampler.IdleVolume \| "Idle Volume" \| "µL" \| injection.name \| chm.channel \| peak.name \| chm.sig_value("min") \| "Signal Min. " \| chm.sig_dim \| "Pump_Pressure" \| "" \| chm.sig_value("average",0.1,1) \| "Signal Average " \| chm.sig_dim \| "Pump_Pressure" \| "" |  |  |
| B109:E114 | ReportTableObject | smp.name \| "Sample Name " \| "" \| "" \| "" \| AUDIT.SamplerModule.Sampler.IdleVolume \| "Idle Volume" \| "µL" \| chm.channel \| peak.name \| chm.sig_value("min") \| "Signal Min. " \| chm.sig_dim \| "Pump_Pressure" \| "" \| chm.sig_value("average",0.1,1) \| "Signal Average " \| chm.sig_dim \| "Pump_Pressure" \| "" |  |  |
| B96:E101 | ReportTableObject | smp.name \| "Sample Name " \| "" \| "" \| "" \| AUDIT.SamplerModule.Sampler.IdleVolume \| "Idle Volume" \| "µL" \| injection.name \| chm.channel \| peak.name \| chm.sig_value("min") \| "Signal Min. " \| chm.sig_dim \| "Pump_Pressure" \| "" \| chm.sig_value("average",0.1,1) \| "Signal Average " \| chm.sig_dim \| "Pump_Pressure" \| "" |  |  |
| B71:O76 | ReportTableObject | smp.name \| "Sample Name " \| "" \| "" \| "" \| precond.SamplerModule.Sampler.IdleVolume \| "Idle Volume " \| "µL" \| "" \| "" \| AUDIT.MeteringPos \| "Metering Pos" \| "nL" \| chm.channel \| peak.name \| peak.retention_time \| "Ret.Time " \| "min" \| "UV_VIS_1" \| "Caffeine" \| smp.inject_volume \| "Inj.Vol. " \| "µl" \| "" \| "" \| peak.area \| "Area " \| chm.sig_dim+"*min" \| "UV_VIS_1" \| "Caffeine" \| peak.correlation_coefficient \| "Corr.Coeff. " \| "%" \| "UV_VIS_1" \| "Caffeine" \| peak.rel_standard_deviation \| "Rel.Std.Dev. " \| "%" \| "UV_VIS_1" \| "Caffeine" \| "Volume Offset " \| "nL" \| chm.channel \| peak.name \| peak.slope \| "Slope " \| "" \| "UV_VIS_1" \| "Caffeine" \| peak.offset \| "Offset " \| "mAU*min" \| "UV_VIS_1" \| "Caffeine" \| chm.sig_value("average",0.1,1) \| "Signal Average " \| chm.sig_dim \| "Pump_Pressure" \| "" \| peak.nCalpoints \| "#Points " \| "" \| "UV_VIS_1" \| "Caffeine" \| peak.asymmetry("ep") \| "Asymmetry (EP)" \| "" \| injection.name \| "UV_VIS_1" \| "Caffeine" |  |  |
| B63:O68 | ReportTableObject | smp.name \| "Sample Name " \| "" \| "" \| "" \| precond.SamplerModule.Sampler.IdleVolume \| "Idle Volume " \| "µL" \| "" \| "" \| AUDIT.MeteringPos \| "Metering Pos" \| "nL" \| chm.channel \| peak.name \| peak.retention_time \| "Ret.Time " \| "min" \| "UV_VIS_1" \| "Caffeine" \| smp.inject_volume \| "Inj.Vol. " \| "µl" \| "" \| "" \| peak.area \| "Area " \| chm.sig_dim+"*min" \| "UV_VIS_1" \| "Caffeine" \| peak.correlation_coefficient \| "Corr.Coeff. " \| "%" \| "UV_VIS_1" \| "Caffeine" \| peak.rel_standard_deviation \| "Rel.Std.Dev. " \| "%" \| "UV_VIS_1" \| "Caffeine" \| "Volume Offset " \| "nL" \| chm.channel \| peak.name \| peak.slope \| "Slope " \| "" \| "UV_VIS_1" \| "Caffeine" \| peak.offset \| "Offset " \| "mAU*min" \| "UV_VIS_1" \| "Caffeine" \| chm.sig_value("average",0.1,1) \| "Signal Average " \| chm.sig_dim \| "Pump_Pressure" \| "" \| peak.nCalpoints \| "#Points " \| "" \| "UV_VIS_1" \| "Caffeine" \| peak.asymmetry("ep") \| "Asymmetry (EP)" \| "" \| injection.name \| "UV_VIS_1" \| "Caffeine" |  |  |
| B128:E133 | ReportTableObject | smp.name \| "Sample Name " \| "" \| "" \| "" \| peak.retention_time \| "Retention" \| "min" \| injection.name \| "UV_VIS_1" \| "Caffeine" \| peak.area \| "Area " \| chm.signalUnit+"*min" \| injection.name \| "UV_VIS_1" \| "Caffeine" \| peak.height \| "Height " \| chm.signalUnit \| injection.name \| "UV_VIS_1" \| "Caffeine" |  |  |
| B134:E139 | ReportTableObject | smp.name \| "Sample Name " \| "" \| "" \| "" \| peak.retention_time \| "Retention" \| "min" \| injection.name \| "UV_VIS_1" \| "Caffeine" \| peak.area \| "Area " \| chm.signalUnit+"*min" \| injection.name \| "UV_VIS_1" \| "Caffeine" \| peak.height \| "Height " \| chm.signalUnit \| injection.name \| "UV_VIS_1" \| "Caffeine" |  |  |
| B152:E157 | ReportTableObject | smp.name \| "Sample Name References" \| "" \| "" \| "" \| AUDIT.SamplerModule.Sampler.IdleVolume \| "Idle Volume" \| "µL" \| injection.name \| chm.channel \| peak.name \| peak.area \| "Area " \| chm.signalUnit+"*min" \| injection.name \| "UV_VIS_1" \| "Caffeine" \| peak.height \| "Height " \| chm.signalUnit \| injection.name \| "UV_VIS_1" \| "Caffeine" |  |  |
| B162:E167 | ReportTableObject | smp.name \| "Sample Name " \| "" \| "" \| "" \| AUDIT.SamplerModule.Sampler.IdleVolume \| "Idle Volume" \| "µL" \| injection.name \| chm.channel \| peak.name \| peak.area \| "Area " \| chm.signalUnit+"*min" \| injection.name \| "UV_VIS_1" \| "Caffeine" \| peak.height \| "Height " \| chm.signalUnit \| injection.name \| "UV_VIS_1" \| "Caffeine" |  |  |

## Sheet: Relays_and_Inputs

| Cell / Range | Object Type | Formula | Fixed Channel | Fixed Component |
|---|---|---|---|---|
| L49 | ReportFormulaObject | AUDIT.Sampler_INPUT_1.State(0.25,"backward") |  |  |
| L50 | ReportFormulaObject | AUDIT.Sampler_INPUT_1.State(0.45,"backward") |  |  |
| L51 | ReportFormulaObject | AUDIT.Sampler_INPUT_1.State(0.65,"backward") |  |  |
| L52 | ReportFormulaObject | AUDIT.Sampler_INPUT_1.State(0.85,"backward") |  |  |
| O49 | ReportFormulaObject | AUDIT.Sampler_INPUT_2.State(0.25,"backward") |  |  |
| O50 | ReportFormulaObject | AUDIT.Sampler_INPUT_2.State(0.45,"backward") |  |  |
| O51 | ReportFormulaObject | AUDIT.Sampler_INPUT_2.State(0.65,"backward") |  |  |
| O52 | ReportFormulaObject | AUDIT.Sampler_INPUT_2.State(0.85,"backward") |  |  |

## Sheet: Cooling_Performance

| Cell / Range | Object Type | Formula | Fixed Channel | Fixed Component |
|---|---|---|---|---|
| H51 | ReportFormulaObject | AUDIT.SamplerModule.Temperature.Value(6,"forward") |  |  |
| I51 | ReportFormulaObject | AUDIT.SamplerModule.Temperature.Value(7.000,"forward") |  |  |
| J51 | ReportFormulaObject | AUDIT.System.Retention(6.25,"backward") |  |  |
| K51 | ReportFormulaObject | AUDIT.System.Retention(7.000,"forward") |  |  |

## Sheet: Internal_Use_1

| Cell / Range | Object Type | Formula | Fixed Channel | Fixed Component |
|---|---|---|---|---|
| E11 | ReportFormulaObject | precond.SamplerModule.SerialNo |  |  |
| E12 | ReportFormulaObject | AUDIT.Samplermodule_Wellness.Service.Lastdate(0.300,"forward") |  |  |
| C45 | ReportFormulaObject | seq.name |  |  |
| C52 | ReportFormulaObject | precond.samplermodule.modelno |  |  |
| E10 | ReportFormulaObject | precond.SamplerModule.Firmware |  |  |
| C53 | ReportFormulaObject | seq.timebase |  | Uracil |
| C54 | ReportFormulaObject | seq.update_time |  |  |
| C46 | ReportFormulaObject | seq.directory |  |  |
| B71:F76 | ReportTableObject | injection.number \| "No. " \| "" \| "" \| "" \| audit.samplermodule.sampler.sampler_service.HorizontalDrvHomeDeviation(0,"forward") \| "Hor. Drv. Home Dev." \| "steps" \| injection.name \| "" \| "" \| audit.samplermodule.sampler.sampler_service.NeedleDrvHomeDeviation(0,"forward") \| "Needle Drv. Home Dev." \| "steps" \| injection.name \| "" \| "" \| audit.samplermodule.sampler.sampler_service.MeteringDrvHomeDeviation(0,"forward") \| "Met. Drv. Home Dev." \| "steps" \| "" \| "" \| audit.samplermodule.sampler.sampler_service.CompressionDrvHomeDeviation(0,"forward") \| "Comp. Drv. Home Dev." \| "steps" \| "" \| "" |  |  |
| E17 | ReportFormulaObject | precond.UVLampOperationTime.Value |  |  |
| C16 | ReportFormulaObject | precond.SamplerModule.Sampler.Sampler_Wellness.NeedleMovements.Value |  |  |
| C23 | ReportFormulaObject | AUDIT.SamplerModule.Sampler.Sampler_Wellness.NeedleObstructions |  |  |
| C24 | ReportFormulaObject | AUDIT.SamplerModule.Sampler.Sampler_Wellness.WashPumpHours |  |  |
| C18 | ReportFormulaObject | AUDIT.SamplerModule.Sampler.Sampler_Wellness.InjectValveSwitches |  |  |
| C19 | ReportFormulaObject | AUDIT.SamplerModule.Sampler.Sampler_Wellness.HorizontalDriveMovements |  |  |
| C20 | ReportFormulaObject | AUDIT.SamplerModule.Sampler.Sampler_Wellness.NeedleDriveMovements |  |  |
| C17 | ReportFormulaObject | AUDIT.SamplerModule.Sampler.Sampler_Wellness.NeedleSeatCounter.Value |  |  |
| C21 | ReportFormulaObject | AUDIT.SamplerModule.Sampler.Sampler_Wellness.MeteringDriveMovements |  |  |
| C22 | ReportFormulaObject | AUDIT.SamplerModule.Sampler.Sampler_Wellness.TotalInjections |  |  |
| C25 | ReportFormulaObject | AUDIT.SamplerModule.SamplerModule_Wellness.DrainPumpHours |  |  |
| C27 | ReportFormulaObject | AUDIT.SamplerModule.SamplerModule_Wellness.TrayDriveMovements |  |  |
| C28 | ReportFormulaObject | AUDIT.SamplerModule.SamplerModule_Wellness.BCR_ScanCounter |  |  |
| C29 | ReportFormulaObject | AUDIT.SamplerModule.SamplerModule_Wellness.HeatingWorkload |  |  |
| C30 | ReportFormulaObject | AUDIT.SamplerModule.SamplerModule_Wellness.CoolingWorkload |  |  |
| C26 | ReportFormulaObject | Audit.SamplerModule.SamplerModule_Wellness.DrainPumpTubeHours.Value |  |  |
| C35 | ReportFormulaObject | precond.SamplerModule.Sampler.Sampler_Wellness.NeedleSeatChangeDate |  |  |
| C37 | ReportFormulaObject | precond.SamplerModule.Sampler.Sampler_Wellness.NeedleChangeDate |  |  |
| C31 | ReportFormulaObject | AUDIT.SamplerModule_Wellness.PowerOnTime |  |  |
| C32 | ReportFormulaObject | AUDIT.SamplerModule_Wellness.OperatingHours |  |  |
| C36 | ReportFormulaObject | precond.SamplerModule.SamplerModule_Wellness.DrainPumpTubeChangeDate |  |  |
| E9 | ReportFormulaObject | precond.SamplerModule.ModuleHardwareRevision |  |  |

## Sheet: Internal_Use_2

| Cell / Range | Object Type | Formula | Fixed Channel | Fixed Component |
|---|---|---|---|---|
| D14 | ReportFormulaObject | AUDIT.SamplerModule.Sampler.DrawSpeed(0.2,"forward") |  |  |
| D15 | ReportFormulaObject | AUDIT.SamplerModule.Sampler.DrawDelay(0.2,"forward") |  |  |
| D16 | ReportFormulaObject | AUDIT.SamplerModule.Sampler.DispenseSpeed(0.2,"forward") |  |  |
| D17 | ReportFormulaObject | AUDIT.SamplerModule.Sampler.WashSpeed(0.2,"forward") |  |  |
| D18 | ReportFormulaObject | AUDIT.SamplerModule.Sampler.WashTime(0.2,"forward") |  |  |
| D19 | ReportFormulaObject | AUDIT.Sampler.InjectResponseMode(0.2,"forward") |  |  |
| D22 | ReportFormulaObject | AUDIT.SamplerModule.Sampler.InjectWashMode(0.2,"forward") |  |  |
| D23 | ReportFormulaObject | AUDIT.SamplerModule.Sampler.Sampler_Service.InjectOptimizationMode(0.2,"forward") |  |  |
| D29 | ReportFormulaObject | audit.SamplerModule.Sampler.LoopVolume(0.2,"forward") |  |  |
| D24 | ReportFormulaObject | AUDIT.SamplerModule.Sampler.PunctureOffset(0.2,"forward") |  |  |
| D25 | ReportFormulaObject | precond.SamplerModule.RackType_Red |  |  |
| D26 | ReportFormulaObject | precond.SamplerModule.RackType_Green |  |  |
| D27 | ReportFormulaObject | precond.SamplerModule.RackType_Blue |  |  |
| D28 | ReportFormulaObject | precond.SamplerModule.RackType_Yellow |  |  |
| D30 | ReportFormulaObject | AUDIT.SamplerModule.Sampler.Sampler_Service.WashAirGap(0.2,"forward") |  |  |
| D31 | ReportFormulaObject | AUDIT.SamplerModule.Sampler.Sampler_Service.WashDepth(0.2,"forward") |  |  |
| D32 | ReportFormulaObject | audit.SamplerModule.Temperature.Nominal(0.2,"forward") |  |  |
| D33 | ReportFormulaObject | chm.signalValue(0.5) | Sampler_CompressDelay |  |
| D34 | ReportFormulaObject | chm.signalValue(0.5) | Sampler_CompressSpeed |  |
| D35 | ReportFormulaObject | audit.SamplerModule.Sampler.Sampler_Service.BacklashCompensation(0.2,"forward") | Sampler_BacklashCompensation |  |
| D36 | ReportFormulaObject | chm.signalValue(0.5) | Sampler_DecompressDelay |  |
| D37 | ReportFormulaObject | audit.SamplerModule.SamplerModule_Service.TempRegulationMode(0.2,"forward") |  |  |
| K59:M64 | ReportTableObject | injection.number \| "No. " \| "" \| injection.name \| "" \| "" \| injection.name \| "Injection Name" \| "" \| injection.name \| "" \| "" \| injection.time \| "Inject Time " \| "" \| injection.name \| "" \| "" |  |  |
| D38 | ReportFormulaObject | audit.SamplerModule.Sampler.IdleVolume(0.2,"forward") |  |  |
| D20 | ReportFormulaObject | AUDIT.SamplerModule.NeedleHeight(0.2,"forward") |  |  |
| D39 | ReportFormulaObject | AUDIT.SamplerModule.SamplerModule_Service.SamplerConfig |  |  |
| D21 | ReportFormulaObject | AUDIT.SamplerModule.DrainPumpInterval(0.2,"forward") |  |  |
| D40 | ReportFormulaObject | audit.SamplerModule.Sampler.NominalLoopVolume(0.2,"forward") |  |  |
| D41 | ReportFormulaObject | audit.SamplerModule.Light(0.2,"forward") |  |  |

## Sheet: Pressure_Test

| Cell / Range | Object Type | Formula | Fixed Channel | Fixed Component |
|---|---|---|---|---|
| G63 | ReportFormulaObject | audit.Variables.GenericBool7(14,"backward") |  |  |
| E62 | ReportFormulaObject | seq.customVar("chooseDrive") |  |  |
| E61 | ReportFormulaObject | audit.Variables.GenericLong9(14,"backward") |  |  |
| H65 | ReportFormulaObject | audit.Variables.GenericBool5(14,"backward") |  |  |
| G66 | ReportFormulaObject | audit.Variables.GenericBool3(-2,"backward") |  |  |
| G65 | ReportFormulaObject | audit.Variables.GenericBool4(14,"backward") |  |  |
| G64 | ReportFormulaObject | audit.Variables.GenericBool2(-2,"backward") |  |  |
| C70 | ReportFormulaObject | if(audit.Variables.GenericDouble8(14,"backward")<90000,audit.Variables.GenericDouble8(14,"backward"),"not evaluated") |  |  |
| C69 | ReportFormulaObject | if(audit.Variables.GenericDouble7(14,"backward")<90000,audit.Variables.GenericDouble7(14,"backward"),"not evaluated") |  |  |
| C71 | ReportFormulaObject | if(audit.Variables.GenericDouble9(14,"backward")<90000,audit.Variables.GenericDouble9(14,"backward"),"not evaluated") |  |  |

## Sheet: Audit Trail

| Cell / Range | Object Type | Formula | Fixed Channel | Fixed Component |
|---|---|---|---|---|
| C3 | ReportFormulaObject | smp.name |  |  |
| C4 | ReportFormulaObject | smp.position |  |  |
| C5 | ReportFormulaObject | smp.type |  |  |
| C6 | ReportFormulaObject | smp.program |  |  |
| C7 | ReportFormulaObject | smp.method |  |  |
| C8 | ReportFormulaObject | injection.time |  |  |
| H3 | ReportFormulaObject | smp.inject_volume |  |  |
| H7 | ReportFormulaObject | smp.dilution_factor |  |  |
| C9 | ReportFormulaObject | chm.end_time - chm.start_time |  |  |
| H8 | ReportFormulaObject | smp.sample_weight |  |  |
| H9 | ReportFormulaObject | smp.amount |  |  |
| H4 | ReportFormulaObject | chm.channel |  |  |
| B1 | ReportFormulaObject | smp.name |  |  |
| A1 | ReportFormulaObject | smp.number |  |  |
| H5 | ReportFormulaObject | chm.wavelength |  |  |
| H6 | ReportFormulaObject | chm.bandwidth |  |  |
| A2 | ReportFormulaObject | smp.comment |  |  |
