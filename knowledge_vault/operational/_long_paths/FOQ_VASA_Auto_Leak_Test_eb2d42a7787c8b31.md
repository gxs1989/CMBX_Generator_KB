# FOQ_VASA_Auto_Leak_Test Instrument Method Script

Source: decoded CMBX instrument method preview
Format: `CM_METHOD_SCRIPT_MD_FORMAT_SPEC.md` / `CM Compiler Rules.MD`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	PumpModule.PumpModule_Service.GetServiceCode		
	PumpModule.PumpModule_Service.ServiceCode	87794	
	PumpModule.Pump.MaximumFlowRampDown	infinite	
	PumpModule.Pump.MaximumFlowRampUp	infinite	
	PumpModule.Degasser	On	
	PumpModule.Pump.Pump_Pressure.UseFilter	Off	
	PumpModule.Pump.Pump_Pressure_Blk1_Drv1.UseFilter	Off	
	PumpModule.Pump.Pump_Pressure_Blk1_Drv2.UseFilter	Off	
	PumpModule.Pump.Pump_Pressure_Blk2_Drv1.UseFilter	Off	
	PumpModule.Pump.Pump_Pressure_Blk2_Drv2.UseFilter	Off	
	PumpModule.Pump.%A_Selector	%A1	
	ColumnComp.UpperValve.CurrentPosition	4	
	SamplerModule.SamplerModule_Service._SendCommand	"LedBar.ForceColor=0"	Led bar auto
	Initializing variables		
	Variables.GenericBool1	0	Internal indicator. Set 1 when block-bypass position is additionally tested
	Variables.GenericBool4	0	Internal indicator. Set 1 when block-bypass position passes the test
	Variables.GenericBool5	0	Internal indicator. Set 1 when block-bypass position fails for high leakage
	Variables.GenericBool6	0	Internal indicator. Set 1 when block-bypass position fails for unknown reasons
	Variables.GenericBool9	0	Internal indicator. Set 1 when test fails for unknown reasons
	Variables.GenericDouble0	0	Stores piston position for measurement (start)
	Variables.GenericDouble1	0	Stores time for measurement (start)
	Variables.GenericDouble2	0	Stores piston position for measurement (end)
	Variables.GenericDouble3	0	Stores time for measurement (end)
	Variables.GenericDouble4	0	Used for calculation. Difference in piston position (see above)
	Variables.GenericDouble5	0	Used for calculation. Difference in time (see above)
	Variables.GenericDouble6	0	leak rate of current test
	Variables.GenericDouble7 = leak rate of system test		
	Variables.GenericDouble8	99999.99	leak rate of bypass
	Variables.GenericDouble9	99999.99	leak rate of inject path
	Variables.GenericFloat0	150	maximum leak rate of the VAS
	Variables.GenericFloat1 decides whether or not to test VAS bypass (1 = system test passed; 2 = system test failed, pump test needs to be executed		
	Variables.GenericFloat2	600	maximum pump leak
	Variables.GenericFloat3	-50	maximum negative leak rate for all pump and autosampler
	Variables.GenericFloat8	4	Used for beginning of live pressure test (+1 Minute)
	Variables.GenericFloat7	0	Reset Live Leak Rate at beginning
	Variables.GenericFloat4	0	Reset average leak rate at beginning
	Variables.GenericFloat6	0	Used for estimation of live leak rate
	Variables.GenericFloat9	0	Used for estimation of live leak rate
	Variables.GenericFloat5	0	Used for estimation of live leak rate
If	System.Injection.Name="Injector pressure test (System)"		
	Variables.GenericFloat1	0	
End If			
If	SamplerModule.ModelNo="VA-A12-A"		
	Variables.GenericString0	"49500,"	pressure for leak test. First three digits in bar
	Variables.GenericLong9	495	pressure of leak test in bar for display in the report
	PumpModule.Pump.Pressure.UpperLimit	500	
	Variables.GenericBool7	0	
Else			
	SamplerModule.SamplerModule_Service._SendCommand	"LedBar.ForceColor=1"	
	Variables.GenericBool7	1	
	Delay	1 [s]	
	System.AbortQueue		
End If			
-2.000	Equilibration	Duration = 1.800 [min]	
	GenericFloat1 decides whether or not to test VAS bypass		
If	Variables.GenericFloat1=1		
	Variables.GenericFloat1	0	
	End		
Else If	Variables.GenericFloat1=2		
Else			
	Variables.GenericDouble7	99999.99	leak rate system
	Variables.GenericBool0	0	
	Variables.GenericBool2	0	
	Variables.GenericBool3	0	
End If			
	PumpModule.Pump.Flow.Nominal	0.300 [ml/min]	
	PumpModule.Pump.%B.Value	0.0 [%]	
-0.200	PumpModule.Pump.Flow.Nominal	0.30 [ml/min]	
	PumpModule.Pump.%B.Value	0.0 [%]	
	Following command is needed to enable CM to control the pistons individually		
	Delay	1 [s]	
	PumpModule.PumpModule_Service._SendCommand	"Flow1.Blk1.CtrlOff"	
	Delay	1 [s]	
	Pulling back measuring pistons		
If	System.Sequence.CustomVariables.chooseDrive="A1"		
	PumpModule.PumpModule_Service._SendCommand	"Flow1.Blk1.Drv1.PositionMode=200000,6000,66000"	This takes about 3 s
	Delay	5 [s]	
Else			
	PumpModule.PumpModule_Service._SendCommand	"Flow1.Blk1.Drv2.PositionMode=200000,6000,66000"	This takes about 3 s
	Delay	5 [s]	
End If			
0.000	Start Run		
	PumpModule.Pump.Pump_Pressure.AcqOn		
	PumpModule.Pump.Pump_Pressure_Blk1_Drv1.AcqOn		
	PumpModule.Pump.Pump_Pressure_Blk1_Drv2.AcqOn		
	PumpModule.Pump.Pump_Pressure_Blk2_Drv1.AcqOn		
	PumpModule.Pump.Pump_Pressure_Blk2_Drv2.AcqOn		
	PumpModule.Pump.Blk1_Drv1_Linenc.AcqOn		
	PumpModule.Pump.Blk1_Drv2_Linenc.AcqOn		
	PumpModule.Pump.Blk2_Drv1_Linenc.AcqOn		
	PumpModule.Pump.Blk2_Drv2_Linenc.AcqOn		
	PumpModule.RecentDrops.AcqOn		
	VirtualChannel	"Volume_Blk1_Drv1", 3.141*1.5875*1.5875*PumpModule.Pump.Blk1_Drv1_Linenc.Signal	calculation of volume the piston displaces [nL]. Maximum volume = 134500 nL
	VirtualChannel	"Volume_Blk1_Drv2", 3.141*1.5875*1.5875*PumpModule.Pump.Blk1_Drv2_Linenc.Signal	calculation of volume the piston displaces [nL]. Maximum volume = 134500 nL
	SamplerModule.TableIndexerMode.AcqOn		
0.000	Run	Duration = 12.000 [min]	
	Switch VAS valve to test position ...		
If	Variables.GenericFloat1=2		
	... to bypass		
If	(SamplerModule.ModelNo="VH-A40-A" or SamplerModule.ModelNo="VF-A40-A") and SamplerModule.Sampler.Location=Right		
	SamplerModule.SamplerModule_Service._SendCommand	"Sampler2.Valve=7"	
Else			
	SamplerModule.SamplerModule_Service._SendCommand	"Sampler.Valve=7"	
End If			
Else			
	... to inject		
If	(SamplerModule.ModelNo="VH-A40-A" or SamplerModule.ModelNo="VF-A40-A") and SamplerModule.Sampler.Location=Right		
	SamplerModule.SamplerModule_Service._SendCommand	"Sampler2.Valve=6"	
Else			
	SamplerModule.SamplerModule_Service._SendCommand	"Sampler.Valve=6"	
End If			
End If			
	Delay	1 [s]	
	Choose Drive for the test		
	Build up pressure to test for leak		
If	System.Sequence.CustomVariables.chooseDrive="A1"		
	PumpModule.PumpModule_Service._SendCommand	"Flow1.Blk1.Drv1.BuildupPressure="+Variables.GenericString0	
Else			
	PumpModule.PumpModule_Service._SendCommand	"Flow1.Blk1.Drv2.BuildupPressure="+Variables.GenericString0	
End If			
0.010	Trigger defined to terminate run, if measurement pressure is not reached or cannot be maintained.		
Trigger	"CannotBuildUpPressure", PumpModule.Pump.Blk1_Drv1_Linenc>17000 or PumpModule.Pump.Blk1_Drv2_Linenc>17000, Limit=1		
If	System.Retention<13		
	PumpModule.Pump.Pump_Service.AbortModalCommand		
	PumpModule.Pump.Pump_Service.PurgeValve	Open	
	SamplerModule.Sampler.SwitchValve	Position=Bypass	
	Delay	5 [s]	
	PumpModule.Pump.Pump_Service.PurgeValve	Closed	
	Delay	5 [s]	
If	Variables.GenericFloat1=0		
	Variables.GenericDouble7	99999.99	
	Variables.GenericFloat1	2	
	Variables.GenericBool0	1	
	Delay	1 [s]	
	System.AbortInjection		
Else If	Variables.GenericFloat1=2		
	Variables.GenericDouble8	99999.99	
	Variables.GenericBool1	1	
	Delay	1 [s]	
	SamplerModule.SamplerModule_Service._SendCommand	"LedBar.ForceColor=1"	Led bar red
	Delay	1 [s]	
	System.AbortQueue		
End If			
End If			
End Trigger			
If	SamplerModule.TableIndexerMode.Signal>0		
0.040	PumpModule.Pump.Pump_Pressure.AcqOff		
	PumpModule.Pump.Pump_Pressure_Blk1_Drv1.AcqOff		
	PumpModule.Pump.Pump_Pressure_Blk1_Drv2.AcqOff		
	PumpModule.Pump.Pump_Pressure_Blk2_Drv1.AcqOff		
	PumpModule.Pump.Pump_Pressure_Blk2_Drv2.AcqOff		
	PumpModule.Pump.Blk1_Drv1_Linenc.AcqOff		
	PumpModule.Pump.Blk1_Drv2_Linenc.AcqOff		
	PumpModule.Pump.Blk2_Drv1_Linenc.AcqOff		
	PumpModule.Pump.Blk2_Drv2_Linenc.AcqOff		
	PumpModule.RecentDrops.AcqOff		
	SamplerModule.TableIndexerMode.AcqOff		
	Delay	1	
	Protocol	"Indexer-Fehler. Bitte Motor des Drehtellers austauschen und den defekten Motor an R&D übergeben."	
	System.AbortQueue		
Else			
End If			
Trigger	"LiveDrucktest", System.Retention>Variables.GenericFloat8+1 AND System.Retention<12.900, AllowImmediateExecution=Yes		Execute trigger every minute (start at 5.0 min)
	Variables.GenericFloat5	Variables.GenericFloat8	Shift retention time of last cycle
	Variables.GenericFloat6	Variables.GenericFloat9	Shift Volume of last cycle
	Variables.GenericFloat8	System.Retention	Save current retention time
	Variables.GenericFloat9	3.141*1.5875*1.5875*PumpModule.Pump.Blk1_Drv1_Linenc.Signal	Save current volume
	Variables.GenericFloat7	(Variables.GenericFloat9-Variables.GenericFloat6)/(Variables.GenericFloat8-Variables.GenericFloat5)	Calculate the difference to the last cycle
If	System.Retention>7.00		
	Variables.GenericFloat4	(Variables.GenericFloat9-(3.1415*1.5875*1.5875*Variables.GenericDouble0))/(Variables.GenericFloat8-Variables.GenericDouble1)	Calculation of the average leak rate (like in the report)
End If			
End Trigger			
5.000	VirtualChannel	"Volume_Loss", Variables.GenericFloat9-3.141*1.5875*1.5875*PumpModule.Pump.Blk1_Drv1_Linenc.Signal	Total volume loss since last interval (1 minute)
	VirtualChannel	"Volume_Loss_per_Time", Variables.GenericFloat7	Differential loss of last interval
7.000	Leak rate measurement.		
	Find the maximum piston position @ t ~ 7 min		
If	System.Sequence.CustomVariables.chooseDrive="A1"		
If	PumpModule.Pump.Blk1_Drv1_Linenc.Signal>Variables.GenericDouble0		
	Variables.GenericDouble0	PumpModule.Pump.Blk1_Drv1_Linenc.Signal	
	Variables.GenericDouble1	System.Retention	
End If			
	Delay	0.1 [s]	Otherwise IF-block is executed every 100 ms
Else			
If	PumpModule.Pump.Blk1_Drv2_Linenc.Signal>Variables.GenericDouble0		
	Variables.GenericDouble0	PumpModule.Pump.Blk1_Drv2_Linenc.Signal	
	Variables.GenericDouble1	System.Retention	
End If			
	Delay	0.1 [s]	Otherwise IF-block is executed every 100 ms
End If			
12.000	Find the maximum piston position @ t ~ 12.5 min		
If	System.Sequence.CustomVariables.chooseDrive="A1"		
If	PumpModule.Pump.Blk1_Drv1_Linenc.Signal>Variables.GenericDouble2		
	Variables.GenericDouble2	PumpModule.Pump.Blk1_Drv1_Linenc.Signal	
	Variables.GenericDouble3	System.Retention	
End If			
	Delay	0.1 [s]	Otherwise IF-block is executed every 100 ms
Else			
If	PumpModule.Pump.Blk1_Drv2_Linenc.Signal>Variables.GenericDouble2		
	Variables.GenericDouble2	PumpModule.Pump.Blk1_Drv2_Linenc.Signal	
	Variables.GenericDouble3	System.Retention	
End If			
	Delay	0.1 [s]	Otherwise IF-block is executed every 100 ms
End If			
13.000	Stop Run		
	PumpModule.Pump.Pump_Pressure.AcqOff		
	PumpModule.Pump.Pump_Pressure_Blk1_Drv1.AcqOff		
	PumpModule.Pump.Pump_Pressure_Blk1_Drv2.AcqOff		
	PumpModule.Pump.Pump_Pressure_Blk2_Drv1.AcqOff		
	PumpModule.Pump.Pump_Pressure_Blk2_Drv2.AcqOff		
	PumpModule.Pump.Blk1_Drv1_Linenc.AcqOff		
	PumpModule.Pump.Blk1_Drv2_Linenc.AcqOff		
	PumpModule.Pump.Blk2_Drv1_Linenc.AcqOff		
	PumpModule.Pump.Blk2_Drv2_Linenc.AcqOff		
	PumpModule.RecentDrops.AcqOff		
	SamplerModule.TableIndexerMode.AcqOff		
13.000	Post Run	Duration = 1.100 [min]	
	Pump is set back to normal operation. System is depressureized.		
	PumpModule.Pump.Pump_Service.AbortModalCommand		
	PumpModule.Pump.Pump_Service.PurgeValve	Open	
	SamplerModule.Sampler.SwitchValve	Position=Bypass	
	Delay	1 [s]	
	PumpModule.Pump.Motor	On	
	PumpModule.Pump.Flow.Nominal	0.400	
	Delay	1 [s]	
	Calculate piston movement during measurement		
	Variables.GenericDouble4	Variables.GenericDouble2-Variables.GenericDouble0	
	Delay	1 [s]	
	Calculate time delta during measurement		
	Variables.GenericDouble5	Variables.GenericDouble3-Variables.GenericDouble1	
	Delay	1 [s]	
	Calculate leak flow (piston area * piston movement / time)		
	Variables.GenericDouble6	(3.1415*1.5875*1.5875*Variables.GenericDouble4)/Variables.GenericDouble5	
	PumpModule.Pump.Pump_Service.PurgeValve	Closed	
	SamplerModule.Sampler.SwitchValve	Position=Inject	
	Delay	1 [s]	
	Leak test is evaluated.		
If	Variables.GenericFloat1=0 and Variables.GenericDouble6<Variables.GenericFloat0 and Variables.GenericDouble6>Variables.GenericFloat3		
	1. Injection only: Leak test passed with only system leak tested		
	Test passed		
	Variables.GenericDouble7	Variables.GenericDouble6	
	Variables.GenericFloat1	1	
	Variables.GenericBool2	1	Report: System leak evaluated (1 = yes)
Else If	Variables.GenericFloat1=0 and (Variables.GenericDouble6>Variables.GenericFloat0 or Variables.GenericDouble6<Variables.GenericFloat3)		
	1. Injection only: Leak test has to go on. System leak is higher than VAS limit. Bypass has to be tested to evaluate the inject path leak.		
	Variables.GenericDouble7	Variables.GenericDouble6	
	Variables.GenericFloat1	2	
	Variables.GenericBool2	1	Report: System leak evaluated (1 = yes)
	Variables.GenericBool3	1	Report: VAS leak evaluated (1 = yes)
Else If	Variables.GenericFloat1=2 and Variables.GenericDouble7-Variables.GenericDouble6<Variables.GenericFloat0 and Variables.GenericDouble6<Variables.GenericFloat2 and Variables.GenericDouble7-Variables.GenericDouble6>Variables.GenericFloat3		
	2.Bypass only: Inject path leak is evaluated		
	Test passed (if VAS leak is < VAS limit, Pump leak < Pump limit and difference between Inject and Bypass leak > -50 nL/min)		
	Variables.GenericDouble8	Variables.GenericDouble6	
	Delay	1 [s]	
	Variables.GenericDouble9	Variables.GenericDouble7-Variables.GenericDouble8	
	Variables.GenericFloat1	0	
	Variables.GenericBool4	1	
Else			
If	Variables.GenericFloat1=2 and (Variables.GenericDouble7-Variables.GenericDouble6>Variables.GenericFloat0 or Variables.GenericDouble7-Variables.GenericDouble6<Variables.GenericFloat3 or Variables.GenericDouble6>Variables.GenericFloat2)		
	2. Bypass only: Inject path leak is evaluated		
	Test failed: Leak to high		
	Variables.GenericDouble8	Variables.GenericDouble6	
	Delay	1 [s]	
	Variables.GenericDouble9	Variables.GenericDouble7-Variables.GenericDouble8	
	Variables.GenericFloat1	0	
	Variables.GenericBool5	1	
Else			
	Variables.GenericBool6	1	
	Variables.GenericBool9	1	
End If			
	SamplerModule.SamplerModule_Service._SendCommand	"LedBar.ForceColor=1"	Led bar red
	Delay	1	
	Variables.GenericFloat1	0	
	Variables.GenericBool9	1	
End If			
	All variables are logged for debugging purposes.		
	Delay	1 [s]	
	Log	Variables.GenericBool0	
	Log	Variables.GenericBool1	
	Log	Variables.GenericBool2	
	Log	Variables.GenericBool3	
	Log	Variables.GenericBool4	
	Log	Variables.GenericBool5	
	Log	Variables.GenericBool6	
	Log	Variables.GenericBool7	
	Log	Variables.GenericBool9	
	Log	Variables.GenericDouble0	
	Log	Variables.GenericDouble1	
	Log	Variables.GenericDouble2	
	Log	Variables.GenericDouble3	
	Log	Variables.GenericDouble4	
	Log	Variables.GenericDouble5	
	Log	Variables.GenericDouble6	
	Log	Variables.GenericDouble7	
	Log	Variables.GenericDouble8	
	Log	Variables.GenericDouble9	
	Log	Variables.GenericFloat0	
	Log	Variables.GenericFloat1	
	Log	Variables.GenericFloat2	
	Log	Variables.GenericFloat3	
13.950	PumpModule.Pump.Flow.Nominal	0.400	
13.960	PumpModule.Pump.Flow.Nominal	0.000	
13.970	Queue is aborted if leak test fails.		
Trigger	"Abort Queue", Variables.GenericBool9=1, Limit=1		
	SamplerModule.SamplerModule_Service._SendCommand	"LedBar.ForceColor=1"	
	Delay	1 [s]	
	System.AbortQueue		
End Trigger			
	End		
```
