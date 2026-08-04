# FOQ_VASA_Cooled_System_Flush Instrument Method Script

Source: decoded CMBX instrument method preview
Format: `CM_METHOD_SCRIPT_MD_FORMAT_SPEC.md` / `CM Compiler Rules.MD`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	================================================================		
	System Flushing		
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
	PumpModule.Pump.Flow.Nominal	0.5	
	PumpModule.Pump.%B.Value	0.0 [%]	
	Autosampler settings (SamplerModule)		
	SamplerModule.Sampler.DrawDelay	3000 [ms]	
	SamplerModule.NeedleHeight	2000 [µm]	
	SamplerModule.Sampler.DrawSpeed	5.000 [µL/s]	
	SamplerModule.Sampler.DispenseSpeed	15	
	SamplerModule.Sampler.PunctureOffset	0	
	SamplerModule.Sampler.Position	R:A3	
	SamplerModule.Sampler.Volume	1	
	Autosampler settings (Sampler)		
	SamplerModule.Sampler.InjectWashMode	NoWash	
	Generic Variables		
	Variables.GenericBool0	1	
	Variables.GenericBool1	0	
	Variables.GenericLong1	0	
0.000	Equilibration		
	UV.Autozero		
0.000	Inject Preparation		
	Wait	UV.Ready and Pump.Ready and ColumnComp.Ready and Sampler.Ready	
0.000	Inject		
0.000	Start Run		
	PumpModule.Pump.Pump_Pressure.AcqOn		
	SamplerModule.TableIndexerMode.AcqOn		
0.000	Run		
Trigger	"Injection", Variables.GenericBool0=1, TrueTime=0, Delay=0, Limit=Infinite, Hysteresis=0.0 [%], AllowImmediateExecution=Yes		
	Delay	1	
	SamplerModule.Sampler.Inject		
	Wait	SamplerModule.Sampler.Ready	
	Delay	0.5	
	Variables.GenericLong1	Variables.GenericLong1+1	
	Variables.GenericBool0	0	
	Variables.GenericBool1	1	
End Trigger			
	End-Trigger		
Trigger	"Toggle", Variables.GenericBool1=1, TrueTime=0, Delay=0, Limit=Infinite, Hysteresis=0, AllowImmediateExecution=No		
	Delay	0.5	
	Variables.GenericBool0	1	
	Variables.GenericBool1	0	
If	Variables.GenericLong1>=System.Injection.CustomVariables.Injectionnumber_Flush		
	Delay	90	
	PumpModule.Pump.Pump_Pressure.AcqOff		
	SamplerModule.TableIndexerMode.AcqOff		
	End		
End If			
End Trigger			
10.000	Stop Run		
	PumpModule.Pump.Pump_Pressure.AcqOff		
	SamplerModule.TableIndexerMode.AcqOff		
	End		
```
