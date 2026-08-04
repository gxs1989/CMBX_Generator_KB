# FOQ_VASA_Cooled_Init Instrument Method Script

Source: decoded CMBX instrument method preview
Format: `CM_METHOD_SCRIPT_MD_FORMAT_SPEC.md` / `CM Compiler Rules.MD`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	================================================================		
	Initialization instrument method for VAS and DVAS		
	================================================================		
	This IM performs an initialization of the VAS.		
	==> DO NOT CHANGE THIS instrument method! <==		
	The following data regarding the drive movement deviations is		
	written to the audit trail for diagnostic purposes:		
	Needle home deviation: vertical needle drive		
	Horizontal home deviation: horizontal needle drive		
	Compression home deviation: compression drive		
	Metering home deviation: metering drive		
	Column oven settings		
	ColumnComp.CC.TempCtrl	On	
	ColumnComp.CC.Temperature.LowerLimit	5.0 [°C]	
	ColumnComp.CC.Temperature.UpperLimit	70.0 [°C]	
	ColumnComp.CC.EquilibrationTime	0.5 [min]	
	ColumnComp.CC.ReadyTempDelta	0.5 [°C]	
	ColumnComp.CC.Mode	ForcedAir	
If	SamplerModule.ModelNo="VA-A12-A"		
	ColumnComp.CC.Temperature.Nominal	30	
	PumpModule.Pump.Pressure.UpperLimit	500	
	Flow through restriction capillary		
	ColumnComp.UpperValve.CurrentPosition	1	
	ColumnComp.LowerValve.CurrentPosition	1	
End If			
	PumpModule.Pump.Pressure.LowerLimit	20 [bar]	
	PumpModule.Pump.MaximumFlowRampDown	5000	
	PumpModule.Pump.MaximumFlowRampUp	5000	
	PumpModule.Pump.%A.Equate	"%A1"	
	PumpModule.Pump.%B.Equate	"%B1"	
	PumpModule.Pump.%A_Selector	%A1	
	PumpModule.Pump.%B_Selector	%B1	
	PumpModule.Pump.Flow.Nominal	Variables.GenericFloat1	
	PumpModule.Pump.%B.Value	0.0 [%]	
	UV detector settings		
	UV.Data_Collection_Rate	25.0 [Hz]	
	UV.TimeConstant	0.60 [s]	
	UV.UV_VIS_1.Wavelength	272 [nm]	
	VAS debug channel settings		
	SamplerModule.Temperature_AmbientAir.Data_Collection_Rate	10	
	SamplerModule.Temperature_Air.Data_Collection_Rate	10	
	SamplerModule.Temperature_RightSink.Data_Collection_Rate	10	
	SamplerModule.Temperature_LeftSink.Data_Collection_Rate	10	
	SamplerModule.Temperature_AmbientSink.Data_Collection_Rate	10	
	Column oven valve settings --> Flow through restriction capillary		
	Autosampler settings (SamplerModule)		
	SamplerModule.Sampler.DrawDelay	3000 [ms]	
	SamplerModule.NeedleHeight	2000 [µm]	
	SamplerModule.Sampler.DrawSpeed	5.000 [µL/s]	
	SamplerModule.Sampler.DispenseSpeed	15.000	
	SamplerModule.Sampler.PunctureOffset	0	
	Autosampler settings (Sampler)		
	SamplerModule.Sampler.InjectWashMode	NoWash	
0.000	Equilibration		
	UV.Autozero		
0.000	Inject Preparation		
	Wait	UV.Ready and Pump.Ready and ColumnComp.Ready and Sampler.Ready	
0.000	Inject		
	SamplerModule.Sampler.Inject		
0.000	Start Run		
	ColumnComp.CC_Temp.AcqOn		
	PumpModule.Pump.Pump_Pressure.AcqOn		
	PumpModule.LCSpeedLeft.AcqOn		
	PumpModule.LCSpeedRight.AcqOn		
	PumpModule.Pump.Pump_Pressure_Blk1_Drv1.AcqOn		
	PumpModule.Pump.Pump_Pressure_Blk1_Drv2.AcqOn		
	PumpModule.Pump.Pump_Pressure_Blk2_Drv1.AcqOn		
	PumpModule.Pump.Pump_Pressure_Blk2_Drv2.AcqOn		
	PumpModule.Pump.Blk1_Drv1_Linenc.AcqOn		
	PumpModule.Pump.Blk1_Drv2_Linenc.AcqOn		
	PumpModule.Pump.Blk2_Drv1_Linenc.AcqOn		
	PumpModule.Pump.Blk2_Drv2_Linenc.AcqOn		
	SamplerModule.Temperature_Air.AcqOn		
	SamplerModule.Temperature_RightSink.AcqOn		
	SamplerModule.Temperature_LeftSink.AcqOn		
	SamplerModule.Temperature_AmbientSink.AcqOn		
	SamplerModule.Temperature_AmbientAir.AcqOn		
	UV.UV_VIS_1.AcqOn		
	SamplerModule.TableIndexerMode.AcqOn		
0.000	Run	Duration = 0.200 [min]	
If	SamplerModule.TableIndexerMode.Signal>0		
0.040	ColumnComp.CC_Temp.AcqOff		
	PumpModule.Pump.Pump_Pressure.AcqOff		
	PumpModule.LCSpeedLeft.AcqOff		
	PumpModule.LCSpeedRight.AcqOff		
	PumpModule.Pump.Pump_Pressure_Blk1_Drv1.AcqOff		
	PumpModule.Pump.Pump_Pressure_Blk1_Drv2.AcqOff		
	PumpModule.Pump.Pump_Pressure_Blk2_Drv1.AcqOff		
	PumpModule.Pump.Pump_Pressure_Blk2_Drv2.AcqOff		
	PumpModule.Pump.Blk1_Drv1_Linenc.AcqOff		
	PumpModule.Pump.Blk1_Drv2_Linenc.AcqOff		
	PumpModule.Pump.Blk2_Drv1_Linenc.AcqOff		
	PumpModule.Pump.Blk2_Drv2_Linenc.AcqOff		
	SamplerModule.Temperature_Air.AcqOff		
	SamplerModule.Temperature_RightSink.AcqOff		
	SamplerModule.Temperature_LeftSink.AcqOff		
	SamplerModule.Temperature_AmbientSink.AcqOff		
	SamplerModule.Temperature_AmbientAir.AcqOff		
	UV.UV_VIS_1.AcqOff		
	SamplerModule.TableIndexerMode.AcqOff		
	Delay	1	
	Protocol	"Indexer-Fehler. Bitte Motor des Drehtellers austauschen und den defekten Motor an R&D übergeben."	
	System.AbortQueue		
Else			
End If			
0.100	Sampler is initialized to check for drive movement step deviations		
	SamplerModule.Init		
0.200	Wait	Sampler.Ready	
	Log	SamplerModule.Sampler.Sampler_Service.CompressionDrvHomeDeviation	
	Log	SamplerModule.Sampler.Sampler_Service.MeteringDrvHomeDeviation	
	Log	SamplerModule.Sampler.Sampler_Service.NeedleDrvHomeDeviation	
	Log	SamplerModule.Sampler.Sampler_Service.HorizontalDrvHomeDeviation	
2.500	Stop Run		
	ColumnComp.CC_Temp.AcqOff		
	PumpModule.Pump.Pump_Pressure.AcqOff		
	PumpModule.LCSpeedLeft.AcqOff		
	PumpModule.LCSpeedRight.AcqOff		
	PumpModule.Pump.Pump_Pressure_Blk1_Drv1.AcqOff		
	PumpModule.Pump.Pump_Pressure_Blk1_Drv2.AcqOff		
	PumpModule.Pump.Pump_Pressure_Blk2_Drv1.AcqOff		
	PumpModule.Pump.Pump_Pressure_Blk2_Drv2.AcqOff		
	PumpModule.Pump.Blk1_Drv1_Linenc.AcqOff		
	PumpModule.Pump.Blk1_Drv2_Linenc.AcqOff		
	PumpModule.Pump.Blk2_Drv1_Linenc.AcqOff		
	PumpModule.Pump.Blk2_Drv2_Linenc.AcqOff		
	SamplerModule.Temperature_Air.AcqOff		
	SamplerModule.Temperature_RightSink.AcqOff		
	SamplerModule.Temperature_LeftSink.AcqOff		
	SamplerModule.Temperature_AmbientSink.AcqOff		
	SamplerModule.Temperature_AmbientAir.AcqOff		
	UV.UV_VIS_1.AcqOff		
	SamplerModule.TableIndexerMode.AcqOff		
2.500	Post Run		
	End		
```
