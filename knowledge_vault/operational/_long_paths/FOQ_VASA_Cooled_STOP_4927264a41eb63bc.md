# FOQ_VASA_Cooled_STOP Instrument Method Script

Source: decoded CMBX instrument method preview
Format: `CM_METHOD_SCRIPT_MD_FORMAT_SPEC.md` / `CM Compiler Rules.MD`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	PumpModule.Pump.%A_Selector	%A1	
	PumpModule.Pump.%B_Selector	%B1	
	PumpModule.Pump.%B.Value	0	
	PumpModule.Pump.Flow.Nominal	0.100 [ml/min]	
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
0.000	Run	Duration = 2.100 [min]	
	PumpModule.Pump.Pressure.LowerLimit	1	
If	SamplerModule.ModelNo="VA-A12-A"		
	PumpModule.Pump.Pressure.UpperLimit	500	
End If			
	SamplerModule.Sampler_CompressDelay.AcqOn		
	SamplerModule.Sampler_CompressSpeed.AcqOn		
	SamplerModule.Sampler_DecompressDelay.AcqOn		
	SamplerModule.TableIndexerMode.AcqOn		
If	SamplerModule.TableIndexerMode.Signal>0		
0.040	SamplerModule.Sampler_BacklashCompensation.AcqOff		
	SamplerModule.Sampler_CompressSpeed.AcqOff		
	SamplerModule.Sampler_CompressDelay.AcqOff		
	SamplerModule.Sampler_DecompressDelay.AcqOff		
	SamplerModule.TableIndexerMode.AcqOff		
	Delay	1	
	Protocol	"Indexer-Fehler. Bitte Motor des Drehtellers austauschen und den defekten Motor an R&D übergeben."	
	System.AbortQueue		
Else			
End If			
0.100	SamplerModule.SamplerModule_Service.GetServiceCode		
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
0.200	SamplerModule.Sampler.Inject		
	SamplerModule.SamplerModule_Service._SendCommand	"Sampler.SetFactoryDefaults"	
	Delay	2	
	SamplerModule.SamplerModule_Service._SendCommand	"Sampler.SetFactoryInternals"	
	Delay	2	
	Log	SamplerModule.Sampler.DrawSpeed	
	Log	SamplerModule.Sampler.WashTime	
	Log	SamplerModule.Sampler.InjectResponseMode	
	Log	SamplerModule.Sampler.DrawDelay	
	Log	SamplerModule.Sampler.DispenseSpeed	
	Log	SamplerModule.Sampler.WashSpeed	
	Log	SamplerModule.Sampler.InjectWashMode	
	Log	SamplerModule.Sampler.WashTime	
	Log	SamplerModule.Sampler.Sampler_Service.InjectOptimizationMode	
	Log	SamplerModule.Sampler.PunctureOffset	
	Log	SamplerModule.DrainPumpInterval	
	Log	SamplerModule.Sampler.Sampler_Service.WashAirGap	
	Log	SamplerModule.Sampler.Sampler_Service.WashDepth	
	Log	SamplerModule.SamplerModule_Service.SamplerConfig	
	Log	SamplerModule.ModuleHardwareRevision	
	Log	SamplerModule.Sampler.LoopVolume	
	Log	SamplerModule.Sampler.NominalLoopVolume	
	Log	SamplerModule.Light	Ensure, that cabin light is on after using it for carryover test
	Log	SamplerModule.Temperature.Nominal	
	Log	SamplerModule.SamplerModule_Service.TempRegulationMode	
	Log	SamplerModule.Sampler.IdleVolume	
	Log	SamplerModule.NeedleHeight	
	Log	SamplerModule.Sampler.Sampler_Service.BacklashCompensation	
	SamplerModule.SamplerModule_Service._SendCommand	"HardwareRevision="	
0.800	SamplerModule.Sampler_CompressSpeed.AcqOff		
	SamplerModule.Sampler_CompressDelay.AcqOff		
	SamplerModule.Sampler_DecompressDelay.AcqOff		
	SamplerModule.TableIndexerMode.AcqOff		
1.100	PumpModule.Pump.%A_Selector	%A1	
	PumpModule.Pump.%B_Selector	%B1	
	PumpModule.Pump.%B.Value	0	
	PumpModule.Pump.Flow.Nominal	0.050 [ml/min]	
	---------------------------------------------------------------------------------------		
	Set the Qualification and Service Date		
	SamplerModule.SamplerModule_Wellness.QualificationDone		
	SamplerModule.SamplerModule_Wellness.ServiceDone		
1.150	Log	SamplerModule_Wellness.Service.LastDate	
	Log	SamplerModule_Wellness.Qualification.LastDate	
	---------------------------------------------------------------------------------------		
	Commands to log the ErrorQueue		
1.250	SamplerModule.Disconnect		
	SamplerModule.Connect		
	Wait	Sampler.Ready	
	---------------------------------------------------------------------------------------		
	Clear the module's error log		
	Set instrument to Service Level		
	Performed twice to set the instrument reliable into service level		
	DO NOT CHANGE!		
1.400	SamplerModule.SamplerModule_Service.GetServiceCode		
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
1.700	SamplerModule.SamplerModule_Service._SendCommand	CommandString="ErrorLog.Clear"	
	SamplerModule.SamplerModule_Service._SendCommand	CommandString="ExceptionLog.Clear"	
	End		
```
