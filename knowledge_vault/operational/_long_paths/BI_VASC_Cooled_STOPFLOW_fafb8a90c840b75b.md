# BI_VASC_Cooled_STOPFLOW Instrument Method Script

Source: decoded CMBX instrument method preview
Format: `CM_METHOD_SCRIPT_MD_FORMAT_SPEC.md` / `CM Compiler Rules.MD`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
-0.100	Equilibration		
	PumpModule.Pump.Pressure.LowerLimit	10 [bar]	
	PumpModule.Pump.Pressure.UpperLimit	700 [bar]	
	PumpDevice =  "Pump"		
	PumpModule.Pump.%A_Selector	%A1	
	PumpModule.Pump.%B_Selector	%B1	
	PumpModule.Pump.Flow.Nominal	0.600 [ml/min]	
	SamplerModule.Sampler.DrawSpeed	15.000 [µl/s]	
	SamplerModule.Sampler.DispenseSpeed	15.000 [µl/s]	
	SamplerModule.Sampler.DrawDelay	0.1 [s]	
	SamplerModule.Sampler.WashSpeed	17 [µl/s]	
	SamplerModule.NeedleHeight	Safe	
	InjectWashMode = BeforeInject		
	InjectMode = Normal		
	SamplerModule.Sampler.PunctureOffset	0 [µm]	
	Sampler.PunctureSpeed = 25000 [µm/s]		
0.000	Start Run		
0.000	Run	Duration = 1.600 [min]	
	SamplerModule.Init		
	Delay	3	
	Wait	Sampler.Ready	
	SamplerModule.Sampler.Inject		Avoid ready check warnings
	PumpModule.Pump.Flow.Nominal	0.600 [ml/min]	
1.100	---------------------------------------------------------------------------------------		
	Commands to log the ErrorQueue		
1.150	SamplerModule.Disconnect		
	SamplerModule.Connect		
	Wait	Sampler.Ready	
	---------------------------------------------------------------------------------------		
	Switch valve to bypass and move needle out of the needle seat to avoid transport damage.		
1.200	SamplerModule.Sampler.SwitchValve	Bypass	
	Delay	1	
	SamplerModule.SamplerModule_Service._SendCommand	CommandString="Sampler.MoveNeedleUp=1"	
	---------------------------------------------------------------------------------------		
	Clear the module's error log		
1.400	==============================================================================		
	Set instrument to Service Level		
	Performed twice to set the instrument reliable into service level		
	SamplerModule.SamplerModule_Service.GetServiceCode		
	Delay	5	
	SamplerModule.SamplerModule_Service.ServiceCode	87794	
	Delay	1	
	Log	SamplerModule_Service.ServiceCode	
	Delay	1	
If	SamplerModule_Service.ServiceCode=Service		
Else			
	SamplerModule.SamplerModule_Service.GetServiceCode		
	Delay	5	
	SamplerModule.SamplerModule_Service.ServiceCode	87794	
	Delay	1	
	Log	SamplerModule_Service.ServiceCode	
	Delay	1	
End If			
1.600	SamplerModule.SamplerModule_Service._SendCommand	CommandString="ErrorLog.Clear"	
2.000	Stop Run		
2.000	Post Run		
	End		
```
