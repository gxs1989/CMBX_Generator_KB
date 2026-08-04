# FOQ_VASC_Cooled_Temp_Cooling_Performance_BI Instrument Method Script

Source: decoded CMBX instrument method preview
Format: `CM_METHOD_SCRIPT_MD_FORMAT_SPEC.md` / `CM Compiler Rules.MD`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	================================================================		
	Cooling performance for thermostatted Vanquish autosamplers		
	================================================================		
	Pump settings		
	PumpModule.Pump.Pressure.LowerLimit	10 [bar]	
	PumpModule.Pump.Pressure.UpperLimit	700 [bar]	
	PumpModule.Pump.Flow.Nominal	0.600 [ml/min]	
	PumpModule.Pump.%B.Value	0.0 [%]	
	Autosampler settings		
	SamplerModule.Sampler.DrawDelay	3000 [ms]	
	SamplerModule.NeedleHeight	2000 [µm]	
	SamplerModule.Sampler.DrawSpeed	5.000 [µL/s]	
	SamplerModule.Sampler.DispenseSpeed	5.000 [µL/s]	
	SamplerModule.Sampler.PunctureOffset	0	
	SamplerModule.Sampler.InjectWashMode	NoWash	
0.000	Start Run		
0.000	Run	Duration = 30.000 [min]	
	SamplerModule.Sampler.Inject		
	SamplerModule.TableIndexerMode.AcqOn		
	Test description		
	1. Ambient temperature (measured with the VAS internal temperature sensor) is logged.		
	2. The autosampler's nominal temperature is set to ambient temperature.		
	3. The program waits until the cabin air temperature (SamplerModule.Temperature.Value) has reached ambient temperature +/- 0.5 degrees.		
	4. The autosampler's nominal temperature is set to 4°C.		
	5. If the autosampler reaches the ambient (as logged in 1) minus 10°C, Trigger T1 logs the retention time and current temperature value (cabin air temperature = SamplerModule.Temperature.Value).		
	6. After a delay of 30 s the sample is stopped, the autosampler's nominal temperature is set to 20°C.		
	7. The delay allows acquiring the temperature for another 30 s for debugging purposes.		
	8. The duration for cooling the autosampler's cabin air temperature from ambient to ambient-10°C indicates the cooling performance.		
If	SamplerModule.TableIndexerMode.Signal>0		
0.040	SamplerModule.Temperature_Air.AcqOff		
	SamplerModule.Temperature_RightSink.AcqOff		
	SamplerModule.Temperature_LeftSink.AcqOff		
	SamplerModule.Temperature_AmbientSink.AcqOff		
	SamplerModule.Temperature_AmbientAir.AcqOff		
	PumpModule.Pump.Pump_Pressure.AcqOff		
	SamplerModule.TableIndexerMode.AcqOff		
	Delay	1	
	Protocol	"Indexer-Fehler. Bitte Motor des Drehtellers austauschen und den defekten Motor an R&D übergeben."	
	System.AbortQueue		
Else			
End If			
1.000	Log	SamplerModule.Temperature_Ambient	
	Delay	1	
	SamplerModule.Temperature.Nominal	SamplerModule.Temperature_Ambient	
1.100	Wait	(SamplerModule.Temperature.Value-SamplerModule.Temperature.Nominal)< 0.5 and (SamplerModule.Temperature.Nominal-SamplerModule.Temperature.Value)< 0.5	
	Do not change the order of the 'Wait' and 'AcqOn' commands. The current order is necessary to avoid discrepancies between system retention and signal time.		
	SamplerModule.Temperature_Air.AcqOn		
	SamplerModule.Temperature_RightSink.AcqOn		
	SamplerModule.Temperature_LeftSink.AcqOn		
	SamplerModule.Temperature_AmbientSink.AcqOn		
	SamplerModule.Temperature_AmbientAir.AcqOn		
	PumpModule.Pump.Pump_Pressure.AcqOn		
6.150	Log	SamplerModule.Temperature.Value	
	Variables.GenericDouble0	SamplerModule.Temperature.Value	
6.200	SamplerModule.Temperature.Nominal	4	
	Log	system.retention	
Trigger	"T1", (Temperature_Air.Signal<Variables.GenericDouble0-10), TrueTime=1.00, Delay=0.0, Limit=1, Hysteresis=0.0, AllowImmediateExecution=No		
	Log	system.retention	
	Log	SamplerModule.Temperature.Value	
	Delay	30	This ensures that the temperature signals are acquired for another 30 s after the desired temperature is reached
	SamplerModule.Temperature_AmbientAir.AcqOff		
	SamplerModule.Temperature_Air.AcqOff		
	SamplerModule.Temperature_RightSink.AcqOff		
	SamplerModule.Temperature_LeftSink.AcqOff		
	SamplerModule.Temperature_AmbientSink.AcqOff		
	SamplerModule.Temperature.Nominal	20	
	PumpModule.Pump.Pump_Pressure.AcqOff		
	SamplerModule.TableIndexerMode.AcqOff		
	PumpModule.Pump.Flow.Nominal	0.600 [mL/min]	
	Delay	1	
	End		
End Trigger			
30.000	Log	system.retention	
30.000	Stop Run		
	SamplerModule.Temperature_Air.AcqOff		
	SamplerModule.Temperature_RightSink.AcqOff		
	SamplerModule.Temperature_LeftSink.AcqOff		
	SamplerModule.Temperature_AmbientSink.AcqOff		
	SamplerModule.Temperature_AmbientAir.AcqOff		
	PumpModule.Pump.Pump_Pressure.AcqOff		
	SamplerModule.TableIndexerMode.AcqOff		
30.000	Post Run		
	Delay	1	
	PumpModule.Pump.Flow.Nominal	0.600 [mL/min]	
	End		
```
