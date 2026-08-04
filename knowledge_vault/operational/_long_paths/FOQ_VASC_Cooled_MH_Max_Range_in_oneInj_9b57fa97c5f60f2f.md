# FOQ_VASC_Cooled_MH_Max_Range_in_oneInj Instrument Method Script

Source: decoded CMBX instrument method preview
Format: `CM_METHOD_SCRIPT_MD_FORMAT_SPEC.md` / `CM Compiler Rules.MD`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	================================================================		
	MH Max Range Test in one Injection for Cooled Samplers VC-A12-A		
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
	PumpModule.Pump.Pressure.UpperLimit	700	
	Flow through restriction capillary		
	ColumnComp.UpperValve.CurrentPosition	1	
	ColumnComp.LowerValve.CurrentPosition	1	
End If			
	Pump settings		
	PumpModule.Pump.Pressure.LowerLimit	20 [bar]	
	PumpModule.Pump.MaximumFlowRampDown	5000.00 [ml/min²]	
	PumpModule.Pump.MaximumFlowRampUp	5000.00 [ml/min²]	
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
	The following send commands draw 3 µL from vial SR:1 at a Metering position 248 to 251µL making sure the way of the piston is free all the way back. The precompression volume ist fixed to 15µL		
	SamplerModule.SamplerModule_Service._SendCommand	"Sampler.UdpBegin=0"	
	SamplerModule.SamplerModule_Service._SendCommand	"Sampler.MDMove=1,256250"	MD out of the way
	SamplerModule.SamplerModule_Service._SendCommand	"Sampler.MDMove=0,237000"	CD new artificial idle volume
	SamplerModule.SamplerModule_Service._SendCommand	"Sampler.UdpWait=5000"	
	SamplerModule.SamplerModule_Service._SendCommand	"Sampler.Valve=3"	Valve Compress/Decompress/Draw
	SamplerModule.SamplerModule_Service._SendCommand	"Sampler.MDMove=0,251000"	CD Decompress
	SamplerModule.SamplerModule_Service._SendCommand	"Sampler.Valve=1"	Valve Bypass
	SamplerModule.SamplerModule_Service._SendCommand	"Sampler.MDMove=0,248500"	CD move to draw position - backlash compensation
	SamplerModule.SamplerModule_Service._SendCommand	"Sampler.MDMove=1,248500"	MD move to draw position - backlash compensation
	SamplerModule.SamplerModule_Service._SendCommand	"Sampler.MDMove=0,256250"	CD turn over to MD drive move out of the way
	SamplerModule.SamplerModule_Service._SendCommand	"Sampler.MDMove=1,249000"	MD move to draw position
	SamplerModule.SamplerModule_Service._SendCommand	"Sampler.Valve=3"	Valve Compress/Decompress/Draw
	SamplerModule.SamplerModule_Service._SendCommand	"Sampler.CabinFan=0"	Turns the cabin fan off during injection as is done in normal injections
	SamplerModule.SamplerModule_Service._SendCommand	"Sampler.GotoPosition=0x010001"	go to vial SR:1
	SamplerModule.SamplerModule_Service._SendCommand	"Sampler.MDMove=1,252000"	MD aspirate
	SamplerModule.SamplerModule_Service._SendCommand	"Sampler.UdpWait=3000"	Wait after draw
	SamplerModule.SamplerModule_Service._SendCommand	"Sampler.GotoPosition=0"	go to needle seat
	SamplerModule.SamplerModule_Service._SendCommand	"Sampler.CabinFan=1"	Turns the cabin fan back on after injection as is done in normal injections
	SamplerModule.SamplerModule_Service._SendCommand	"Sampler.MDMove=0,237000"	CD precompress
	SamplerModule.SamplerModule_Service._SendCommand	"Sampler.Valve=2"	Inject
	SamplerModule.SamplerModule_Service._SendCommand	"Sampler.UdpEnd"	
0.000	Equilibration		
	UV.Autozero		
0.000	Inject Preparation		
	Wait	UV.Ready and Pump.Ready and ColumnComp.Ready and Sampler.Ready	
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
0.000	Run	Duration = 0.900 [min]	
	SamplerModule.SamplerModule_Service._SendCommand	"Sampler.UdpExecute"	Execute the udp
If	SamplerModule.TableIndexerMode.Signal>0		
0.800	ColumnComp.CC_Temp.AcqOff		
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
0.900	Log	Sampler_Service.MeteringPos	
	SamplerModule.SamplerModule_Service._SendCommand	CommandString="Sampler.CompressVol="	
	SamplerModule.SamplerModule_Service._SendCommand	CommandString="Sampler.CompressPos="	
	SamplerModule.SamplerModule_Service._SendCommand	CommandString="Sampler.DecompressVol="	
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
