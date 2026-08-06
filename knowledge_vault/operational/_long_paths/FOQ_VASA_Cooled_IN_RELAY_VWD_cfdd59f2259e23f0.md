# FOQ_VASA_Cooled_IN_RELAY_VWD Instrument Method Script

Source: decoded CMBX instrument method preview
Format: `CM_METHOD_SCRIPT_MD_FORMAT_SPEC.md` / `CM Compiler Rules.MD`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	================================================================		
	Digital I/O for Vanquish autosamplers		
	================================================================		
	Each possible relay / input combination is tested.		
	Pump Settings		
	PumpModule.Pump.%B_Selector	%B1	
	PumpModule.Pump.%A_Selector	%A1	
	PumpModule.Pump.%B.Value	0	
	PumpModule.Pump.Pressure.LowerLimit	20	
	PumpModule.Pump.%A.Equate	"Water"	
	PumpModule.Pump.Flow.Nominal	0.100 [ml/min]	
	PumpModule.Pump.%B.Value	0	
If	SamplerModule.ModelNo="VA-A12-A"		
	PumpModule.Pump.Pressure.UpperLimit	500	
End If			
0.000	Inject Preparation		
	Wait	Sampler.Ready	
0.000	Start Run		
	Log	SamplerModule.Sampler.Location	
	Delay	1	
	UV.UV_VIS_1.AcqOn		
0.000	Run	Duration = 0.900 [min]	
	SamplerModule.Sampler_Relay_1.State	off	
	SamplerModule.Sampler_Relay_2.State	off	
0.100	SamplerModule.Sampler_Relay_1.State	on	
	SamplerModule.Sampler_Relay_2.State	on	
0.200	Log	Sampler_Input_1.State	
	Log	Sampler_Input_2.State	
0.300	SamplerModule.Sampler_Relay_1.State	off	
	SamplerModule.Sampler_Relay_2.State	off	
0.400	Log	Sampler_Input_1.State	
	Log	Sampler_Input_2.State	
0.500	SamplerModule.Sampler_Relay_1.State	off	
	SamplerModule.Sampler_Relay_2.State	on	
0.600	Log	Sampler_Input_1.State	
	Log	Sampler_Input_2.State	
0.700	SamplerModule.Sampler_Relay_1.State	on	
	SamplerModule.Sampler_Relay_2.State	off	
0.800	Log	Sampler_Input_1.State	
	Log	Sampler_Input_2.State	
0.900	SamplerModule.Sampler_Relay_1.State	off	
	SamplerModule.Sampler_Relay_2.State	off	
0.900	Stop Run		
	UV.UV_VIS_1.AcqOff		
0.900	Post Run		
	End		
```
