# FOQ_VASA_Cooled_ExceptionLog_Clear Instrument Method Script

Source: decoded CMBX instrument method preview
Format: `CM_METHOD_SCRIPT_MD_FORMAT_SPEC.md` / `CM Compiler Rules.MD`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	PumpModule.Pump.%A_Selector	%A1	
	PumpModule.Pump.%B_Selector	%B1	
	PumpModule.Pump.%B.Value	0	
	PumpModule.Pump.Flow.Nominal	0.050 [ml/min]	
	PumpModule.Pump.Pressure.LowerLimit	20 [bar]	
	================================================================		
	Slow down to standby conditions: 50 µl/min		
	================================================================		
	Pump Settings		
	SamplerModule.Sampler_BacklashCompensation.Data_Collection_Rate	1	
	SamplerModule.Sampler_CompressDelay.Data_Collection_Rate	1	
	SamplerModule.Sampler_CompressSpeed.Data_Collection_Rate	1	
	SamplerModule.Sampler_DecompressDelay.Data_Collection_Rate	1	
	SamplerModule.Sampler.DispenseSpeed	5.000 [µL/s]	
0.000	Run	Duration = 0.300 [min]	
	PumpModule.Pump.Pressure.LowerLimit	1	
If	SamplerModule.ModelNo="VA-A12-A"		
	PumpModule.Pump.Pressure.UpperLimit	500	
End If			
0.100	SamplerModule.Sampler.Inject		
0.150	Commands to log the ErrorQueue		
	SamplerModule.Disconnect		
	SamplerModule.Connect		
	Wait	Sampler.Ready	
	---------------------------------------------------------------------------------------		
	Switch valve to bypass and move needle out of the needle seat to avoid transport damage.		
0.300	SamplerModule.Sampler.SwitchValve	Bypass	
	Delay	1	
	SamplerModule.SamplerModule_Service._SendCommand	CommandString="Sampler.MoveNeedleUp=1"	
0.500	Stop Run		
	End		
```
