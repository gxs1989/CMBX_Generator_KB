# FOQ_VASA_Cooled_Linearity_SetIdleVolume Instrument Method Script

Source: decoded CMBX instrument method preview
Format: `CM_METHOD_SCRIPT_MD_FORMAT_SPEC.md` / `CM Compiler Rules.MD`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	================================================================		
	Linearity and reproducibility with caffeine (single injector)		
	================================================================		
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
	Pump settings		
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
	SamplerModule.Sampler.DispenseSpeed	15	
	SamplerModule.Sampler.PunctureOffset	0	
	Autosampler settings (Temperature)		
	SamplerModule.TempCtrl	On	
	SamplerModule.Temperature.Nominal	20.0	
	Autosampler settings (Sampler)		
	SamplerModule.Sampler.InjectWashMode	NoWash	
	Preparation of extended linearity test		
0.000	Inject Preparation		
	Wait	Sampler.Ready	
0.000	Run		
	SamplerModule.SamplerModule_Service._SendCommand	"Sampler.SetIdleVolume="+System.Injection.CustomVariables.IdleVolume	
1.500	Stop Run		
	Log	SamplerModule.Sampler.IdleVolume	
	End		
```
