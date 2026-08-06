# FOQ_VASA_Cooled_equilibration Instrument Method Script

Source: decoded CMBX instrument method preview
Format: `CM_METHOD_SCRIPT_MD_FORMAT_SPEC.md` / `CM Compiler Rules.MD`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	================================================================		
	Equilibration of Oven Temperatures		
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
	PumpModule.Pump.MaximumFlowRampDown	5000 [ml/min²]	
	PumpModule.Pump.MaximumFlowRampUp	5000	
	PumpModule.Pump.%A.Equate	"%A1"	
	PumpModule.Pump.%B.Equate	"%B1"	
	PumpModule.Pump.%A_Selector	%A1	
	PumpModule.Pump.%B_Selector	%B1	
	PumpModule.Pump.Flow.Nominal	0.5	
	PumpModule.Pump.%B.Value	0.0 [%]	
	UV detector settings		
	UV.Data_Collection_Rate	25.0 [Hz]	
	UV.TimeConstant	0.60 [s]	
	UV.UV_VIS_1.Wavelength	272 [nm]	
	Autosampler settings (SamplerModule)		
	SamplerModule.Sampler.DrawDelay	3000 [ms]	
	SamplerModule.NeedleHeight	2000 [µm]	
	SamplerModule.Sampler.DrawSpeed	5.000 [µL/s]	
	SamplerModule.Sampler.DispenseSpeed	15	
	SamplerModule.Sampler.PunctureOffset	0	
	Autosampler settings (Sampler)		
	SamplerModule.Sampler.InjectWashMode	NoWash	
	Generic Variables		
	Variables.GenericBool9	0	important for insertion of additional linearity samples if linearity-standard is empty
0.000	Equilibration		
0.000	Inject Preparation		
	Wait	UV.Ready and Pump.Ready and ColumnComp.Ready and Sampler.Ready	
0.000	Run		
	Delay	0.5	
	PumpModule.Pump.Flow.Nominal	1	
	Delay	0.5	
	End		
2.000	Stop Run		
	End		
```
