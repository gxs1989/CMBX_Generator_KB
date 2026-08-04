# Online Original VAS Method Script Collection

Online_KB_Status: DECODED_FROM_GOLDEN_CMBX  
Build_Date: 2026-07-23  
Source_CMBX: 9318349.cmbx  
Instrument_Method_Count: 19

This file is regenerated from embedded instrument-method payloads in the VAS CMBX. It is executable evidence, not interpretation. Preserve command spelling, stage timing, branch structure, service-command strings, and acquisition symmetry unless a reviewed change contract explicitly permits modification.

## Self Index

| Stable ID | CM method | Rows | Hash | Section |
|---|---|---:|---|---|
| `M-VAS-BI-VASC-COOLED-STOPFLOW` | `BI_VASC_Cooled_STOPFLOW` | 58 | `285de44b95d7` | [Open](#m-vas-bi-vasc-cooled-stopflow) |
| `M-VAS-FOQ-VASA-AUTO-LEAK-TEST` | `FOQ_VASA_Auto_Leak_Test` | 309 | `80e1763dabfc` | [Open](#m-vas-foq-vasa-auto-leak-test) |
| `M-VAS-FOQ-VASA-COOLED-CO-END` | `FOQ_VASA_Cooled_CO_End` | 102 | `d049d11b8669` | [Open](#m-vas-foq-vasa-cooled-co-end) |
| `M-VAS-FOQ-VASA-COOLED-CO-RC` | `FOQ_VASA_Cooled_CO_RC` | 130 | `a269979adf84` | [Open](#m-vas-foq-vasa-cooled-co-rc) |
| `M-VAS-FOQ-VASA-COOLED-CO-RC-FILL-REF-VIALS` | `FOQ_VASA_Cooled_CO_RC_Fill_Ref_Vials` | 142 | `702200efd45b` | [Open](#m-vas-foq-vasa-cooled-co-rc-fill-ref-vials) |
| `M-VAS-FOQ-VASA-COOLED-CO-RC-SOLV-REF` | `FOQ_VASA_Cooled_CO_RC_Solv_Ref` | 130 | `c00f80141f81` | [Open](#m-vas-foq-vasa-cooled-co-rc-solv-ref) |
| `M-VAS-FOQ-VASA-COOLED-EQUILIBRATION` | `FOQ_VASA_Cooled_equilibration` | 52 | `c50e91089cc8` | [Open](#m-vas-foq-vasa-cooled-equilibration) |
| `M-VAS-FOQ-VASA-COOLED-EXCEPTIONLOG-CLEAR` | `FOQ_VASA_Cooled_ExceptionLog_Clear` | 32 | `920484fef1ca` | [Open](#m-vas-foq-vasa-cooled-exceptionlog-clear) |
| `M-VAS-FOQ-VASA-COOLED-FLOW-ADJUSTMENT-RESTRICTION-CAPILLARY` | `FOQ_VASA_Cooled_Flow_adjustment_restriction_capillary` | 122 | `76c2aa359f8f` | [Open](#m-vas-foq-vasa-cooled-flow-adjustment-restriction-capillary) |
| `M-VAS-FOQ-VASA-COOLED-INIT` | `FOQ_VASA_Cooled_Init` | 135 | `615fc5c2ee31` | [Open](#m-vas-foq-vasa-cooled-init) |
| `M-VAS-FOQ-VASA-COOLED-IN-RELAY-VWD` | `FOQ_VASA_Cooled_IN_RELAY_VWD` | 47 | `9096dd717d49` | [Open](#m-vas-foq-vasa-cooled-in-relay-vwd) |
| `M-VAS-FOQ-VASA-COOLED-LINEARITY-SETIDLEVOLUME` | `FOQ_VASA_Cooled_Linearity_SetIdleVolume` | 58 | `d60f375e7844` | [Open](#m-vas-foq-vasa-cooled-linearity-setidlevolume) |
| `M-VAS-FOQ-VASA-COOLED-MH-MAX-RANGE-IN-ONEINJ-NOUDP` | `FOQ_VASA_Cooled_MH_Max_Range_in_oneInj - NoUdp` | 162 | `25f09550f6f5` | [Open](#m-vas-foq-vasa-cooled-mh-max-range-in-oneinj-noudp) |
| `M-VAS-FOQ-VASA-COOLED-PRECISION-LINEARITY` | `FOQ_VASA_Cooled_Precision_Linearity` | 128 | `b2a758439fd7` | [Open](#m-vas-foq-vasa-cooled-precision-linearity) |
| `M-VAS-FOQ-VASA-COOLED-SETPARAMETERS` | `FOQ_VASA_Cooled_SetParameters` | 112 | `e3dfa9c74a83` | [Open](#m-vas-foq-vasa-cooled-setparameters) |
| `M-VAS-FOQ-VASA-COOLED-STOP` | `FOQ_VASA_Cooled_STOP` | 121 | `749aab58ae06` | [Open](#m-vas-foq-vasa-cooled-stop) |
| `M-VAS-FOQ-VASA-COOLED-SYSTEM-FLUSH` | `FOQ_VASA_Cooled_System_Flush` | 76 | `4cacd11b3cac` | [Open](#m-vas-foq-vasa-cooled-system-flush) |
| `M-VAS-FOQ-VASC-COOLED-MH-MAX-RANGE-IN-ONEINJ` | `FOQ_VASC_Cooled_MH_Max_Range_in_oneInj` | 149 | `4821b1a429b7` | [Open](#m-vas-foq-vasc-cooled-mh-max-range-in-oneinj) |
| `M-VAS-FOQ-VASC-COOLED-TEMP-COOLING-PERFORMANCE-BI` | `FOQ_VASC_Cooled_Temp_Cooling_Performance_BI` | 86 | `d67dd1c78fac` | [Open](#m-vas-foq-vasc-cooled-temp-cooling-performance-bi) |

<a id="m-vas-bi-vasc-cooled-stopflow"></a>
## M-VAS-BI-VASC-COOLED-STOPFLOW: BI_VASC_Cooled_STOPFLOW

Source CMBX: `9318349.cmbx`  
Decoded flow SHA-256: `285de44b95d7f6f9d8fe306cd7f815035dacd19ea8b4e0be8ad190901f70b4fa`  
Decoded rows: `58`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
-0.100	Equilibration	Duration = 0.100 [min]	
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
0.000	StartRun		
0.000	Run	Duration = 1.600 [min]	
	SamplerModule.Init		
	Delay	3	
	Wait	Sampler.Ready	
	SamplerModule.Sampler.Inject		Avoid ready check warnings
	PumpModule.Pump.Flow.Nominal	0.600 [ml/min]	
	---------------------------------------------------------------------------------------		
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
	==============================================================================		
	Set instrument to Service Level		
	Performed twice to set the instrument reliable into service level		
1.400	SamplerModule.SamplerModule_Service.GetServiceCode		
	Delay	5	
	SamplerModule.SamplerModule_Service.ServiceCode	87794	
	Delay	1	
	Log	SamplerModule_Service.ServiceCode	
	Delay	1	
If		SamplerModule_Service.ServiceCode=Service	
Else			
	    SamplerModule.SamplerModule_Service.GetServiceCode		
	    Delay	5	
	    SamplerModule.SamplerModule_Service.ServiceCode	87794	
	    Delay	1	
	    Log	SamplerModule_Service.ServiceCode	
	    Delay	1	
End If			
1.600	SamplerModule.SamplerModule_Service._SendCommand	CommandString="ErrorLog.Clear"	
2.000	StopRun		
2.000	PostRun		
	End		
```

<a id="m-vas-foq-vasa-auto-leak-test"></a>
## M-VAS-FOQ-VASA-AUTO-LEAK-TEST: FOQ_VASA_Auto_Leak_Test

Source CMBX: `9318349.cmbx`  
Decoded flow SHA-256: `80e1763dabfcfdab05674d5f946c8db888ddf741606b939574cd446a2dca577c`  
Decoded rows: `309`

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
	SamplerModule.SamplerModule_Service._SendCommand	LedBar.ForceColor=0	Led bar auto
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
If		System.Injection.Name="Injector pressure test (System)"	
	    Variables.GenericFloat1	0	
End If			
If		SamplerModule.ModelNo="VA-A12-A"	
	    Variables.GenericString0	49500,	pressure for leak test. First three digits in bar
	    Variables.GenericLong9	495	pressure of leak test in bar for display in the report
	    PumpModule.Pump.Pressure.UpperLimit	500	
	    Variables.GenericBool7	0	
Else			
	    SamplerModule.SamplerModule_Service._SendCommand	LedBar.ForceColor=1	
	    Variables.GenericBool7	1	
	    Delay	1 [s]	
	    System.AbortQueue		
End If			
-2.000	Equilibration	Duration = 1.800 [min]	
	GenericFloat1 decides whether or not to test VAS bypass		
If		Variables.GenericFloat1=1	
	    Variables.GenericFloat1	0	
	    End		
Else If		Variables.GenericFloat1=2	
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
	PumpModule.PumpModule_Service._SendCommand	Flow1.Blk1.CtrlOff	
	Delay	1 [s]	
	Pulling back measuring pistons		
If		System.Sequence.CustomVariables.chooseDrive="A1"	
	    PumpModule.PumpModule_Service._SendCommand	Flow1.Blk1.Drv1.PositionMode=200000,6000,66000	This takes about 3 s
	    Delay	5 [s]	
Else			
	    PumpModule.PumpModule_Service._SendCommand	Flow1.Blk1.Drv2.PositionMode=200000,6000,66000	This takes about 3 s
	    Delay	5 [s]	
End If			
0.000	StartRun		
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
	VirtualChannel	Volume_Blk1_Drv1, 3.141*1.5875*1.5875*PumpModule.Pump.Blk1_Drv1_Linenc.Signal	calculation of volume the piston displaces [nL]. Maximum volume = 134500 nL
	VirtualChannel	Volume_Blk1_Drv2, 3.141*1.5875*1.5875*PumpModule.Pump.Blk1_Drv2_Linenc.Signal	calculation of volume the piston displaces [nL]. Maximum volume = 134500 nL
	SamplerModule.TableIndexerMode.AcqOn		
0.000	Run	Duration = 12.000 [min]	
	Switch VAS valve to test position ...		
If		Variables.GenericFloat1=2	
	    ... to bypass		
    If		(SamplerModule.ModelNo="VH-A40-A" or SamplerModule.ModelNo="VF-A40-A") and SamplerModule.Sampler.Location=Right	
	        SamplerModule.SamplerModule_Service._SendCommand	Sampler2.Valve=7	
    Else			
	        SamplerModule.SamplerModule_Service._SendCommand	Sampler.Valve=7	
    End If			
Else			
	    ... to inject		
    If		(SamplerModule.ModelNo="VH-A40-A" or SamplerModule.ModelNo="VF-A40-A") and SamplerModule.Sampler.Location=Right	
	        SamplerModule.SamplerModule_Service._SendCommand	Sampler2.Valve=6	
    Else			
	        SamplerModule.SamplerModule_Service._SendCommand	Sampler.Valve=6	
    End If			
End If			
	Delay	1 [s]	
	Choose Drive for the test		
	Build up pressure to test for leak		
If		System.Sequence.CustomVariables.chooseDrive="A1"	
	    PumpModule.PumpModule_Service._SendCommand	Flow1.Blk1.Drv1.BuildupPressure=+Variables.GenericString0	
Else			
	    PumpModule.PumpModule_Service._SendCommand	Flow1.Blk1.Drv2.BuildupPressure=+Variables.GenericString0	
End If			
	Trigger defined to terminate run, if measurement pressure is not reached or cannot be maintained.		
0.010			
Trigger		"CannotBuildUpPressure",	
	    Condition	PumpModule.Pump.Blk1_Drv1_Linenc>17000 or PumpModule.Pump.Blk1_Drv2_Linenc>17000	
	    Limit	1	
If		System.Retention<13	
	    PumpModule.Pump.Pump_Service.AbortModalCommand		
	    PumpModule.Pump.Pump_Service.PurgeValve	Open	
	    SamplerModule.Sampler.SwitchValve	Position=Bypass	
	    Delay	5 [s]	
	    PumpModule.Pump.Pump_Service.PurgeValve	Closed	
	    Delay	5 [s]	
    If		Variables.GenericFloat1=0	
	        Variables.GenericDouble7	99999.99	
	        Variables.GenericFloat1	2	
	        Variables.GenericBool0	1	
	        Delay	1 [s]	
	        System.AbortInjection		
    Else If		Variables.GenericFloat1=2	
	        Variables.GenericDouble8	99999.99	
	        Variables.GenericBool1	1	
	        Delay	1 [s]	
	        SamplerModule.SamplerModule_Service._SendCommand	LedBar.ForceColor=1	Led bar red
	        Delay	1 [s]	
	        System.AbortQueue		
    End If			
End If			
End Trigger			
If		SamplerModule.TableIndexerMode.Signal>0	
0.040	    PumpModule.Pump.Pump_Pressure.AcqOff		
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
	    Protocol	Indexer-Fehler. Bitte Motor des Drehtellers austauschen und den defekten Motor an R&D übergeben.	
	    System.AbortQueue		
Else			
End If			
Trigger		"LiveDrucktest",	Execute trigger every minute (start at 5.0 min)
	    Condition	System.Retention>Variables.GenericFloat8+1 AND System.Retention<12.900	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat5	Variables.GenericFloat8	Shift retention time of last cycle
	Variables.GenericFloat6	Variables.GenericFloat9	Shift Volume of last cycle
	Variables.GenericFloat8	System.Retention	Save current retention time
	Variables.GenericFloat9	3.141*1.5875*1.5875*PumpModule.Pump.Blk1_Drv1_Linenc.Signal	Save current volume
	Variables.GenericFloat7	(Variables.GenericFloat9-Variables.GenericFloat6)/(Variables.GenericFloat8-Variables.GenericFloat5)	Calculate the difference to the last cycle
If		System.Retention>7.00	
	    Variables.GenericFloat4	(Variables.GenericFloat9-(3.1415*1.5875*1.5875*Variables.GenericDouble0))/(Variables.GenericFloat8-Variables.GenericDouble1)	Calculation of the average leak rate (like in the report)
End If			
End Trigger			
5.000	VirtualChannel	Volume_Loss, Variables.GenericFloat9-3.141*1.5875*1.5875*PumpModule.Pump.Blk1_Drv1_Linenc.Signal	Total volume loss since last interval (1 minute)
	VirtualChannel	Volume_Loss_per_Time, Variables.GenericFloat7	Differential loss of last interval
	Leak rate measurement.		
	Find the maximum piston position @ t ~ 7 min		
If		System.Sequence.CustomVariables.chooseDrive="A1"	
    If		PumpModule.Pump.Blk1_Drv1_Linenc.Signal>Variables.GenericDouble0	
7.000	        Variables.GenericDouble0	PumpModule.Pump.Blk1_Drv1_Linenc.Signal	
	        Variables.GenericDouble1	System.Retention	
    End If			
	    Delay	0.1 [s]	Otherwise IF-block is executed every 100 ms
Else			
    If		PumpModule.Pump.Blk1_Drv2_Linenc.Signal>Variables.GenericDouble0	
	        Variables.GenericDouble0	PumpModule.Pump.Blk1_Drv2_Linenc.Signal	
	        Variables.GenericDouble1	System.Retention	
    End If			
	    Delay	0.1 [s]	Otherwise IF-block is executed every 100 ms
End If			
	Find the maximum piston position @ t ~ 12.5 min		
If		System.Sequence.CustomVariables.chooseDrive="A1"	
    If		PumpModule.Pump.Blk1_Drv1_Linenc.Signal>Variables.GenericDouble2	
12.000	        Variables.GenericDouble2	PumpModule.Pump.Blk1_Drv1_Linenc.Signal	
	        Variables.GenericDouble3	System.Retention	
    End If			
	    Delay	0.1 [s]	Otherwise IF-block is executed every 100 ms
Else			
    If		PumpModule.Pump.Blk1_Drv2_Linenc.Signal>Variables.GenericDouble2	
	        Variables.GenericDouble2	PumpModule.Pump.Blk1_Drv2_Linenc.Signal	
	        Variables.GenericDouble3	System.Retention	
    End If			
	    Delay	0.1 [s]	Otherwise IF-block is executed every 100 ms
End If			
13.000	StopRun		
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
13.000	PostRun	Duration = 1.100 [min]	
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
If		Variables.GenericFloat1=0 and Variables.GenericDouble6<Variables.GenericFloat0 and Variables.GenericDouble6>Variables.GenericFloat3	
	    1. Injection only: Leak test passed with only system leak tested		
	    Test passed		
	    Variables.GenericDouble7	Variables.GenericDouble6	
	    Variables.GenericFloat1	1	
	    Variables.GenericBool2	1	Report: System leak evaluated (1 = yes)
Else If		Variables.GenericFloat1=0 and (Variables.GenericDouble6>Variables.GenericFloat0 or Variables.GenericDouble6<Variables.GenericFloat3)	
	    1. Injection only: Leak test has to go on. System leak is higher than VAS limit. Bypass has to be tested to evaluate the inject path leak.		
	    Variables.GenericDouble7	Variables.GenericDouble6	
	    Variables.GenericFloat1	2	
	    Variables.GenericBool2	1	Report: System leak evaluated (1 = yes)
	    Variables.GenericBool3	1	Report: VAS leak evaluated (1 = yes)
Else If		Variables.GenericFloat1=2 and Variables.GenericDouble7-Variables.GenericDouble6<Variables.GenericFloat0 and Variables.GenericDouble6<Variables.GenericFloat2 and Variables.GenericDouble7-Variables.GenericDouble6>Variables.GenericFloat3	
	    2.Bypass only: Inject path leak is evaluated		
	    Test passed (if VAS leak is < VAS limit, Pump leak < Pump limit and difference between Inject and Bypass leak > -50 nL/min)		
	    Variables.GenericDouble8	Variables.GenericDouble6	
	    Delay	1 [s]	
	    Variables.GenericDouble9	Variables.GenericDouble7-Variables.GenericDouble8	
	    Variables.GenericFloat1	0	
	    Variables.GenericBool4	1	
Else			
    If		Variables.GenericFloat1=2 and (Variables.GenericDouble7-Variables.GenericDouble6>Variables.GenericFloat0 or Variables.GenericDouble7-Variables.GenericDouble6<Variables.GenericFloat3 or Variables.GenericDouble6>Variables.GenericFloat2)	
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
	    SamplerModule.SamplerModule_Service._SendCommand	LedBar.ForceColor=1	Led bar red
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
	Queue is aborted if leak test fails.		
13.970			
Trigger		"Abort Queue",	
	    Condition	Variables.GenericBool9=1	
	    Limit	1	
	SamplerModule.SamplerModule_Service._SendCommand	LedBar.ForceColor=1	
	Delay	1 [s]	
	System.AbortQueue		
End Trigger			
	End		
```

<a id="m-vas-foq-vasa-cooled-co-end"></a>
## M-VAS-FOQ-VASA-COOLED-CO-END: FOQ_VASA_Cooled_CO_End

Source CMBX: `9318349.cmbx`  
Decoded flow SHA-256: `d049d11b8669e2e9e696457d9fa5b7c6ce2c7d5e9c596fb778d60c49cd93f32b`  
Decoded rows: `102`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	================================================================		
	End of carry-over test, set settings back to general settings (single injector)		
	================================================================		
	Column oven settings		
	ColumnComp.CC.TempCtrl	On	
	ColumnComp.CC.Temperature.LowerLimit	5.0 [°C]	
	ColumnComp.CC.Temperature.UpperLimit	70.0 [°C]	
	ColumnComp.CC.EquilibrationTime	0.5 [min]	
	ColumnComp.CC.ReadyTempDelta	0.5 [°C]	
	ColumnComp.CC.Mode	ForcedAir	
If		SamplerModule.ModelNo="VA-A12-A"	
	    ColumnComp.CC.Temperature.Nominal	30	
	    PumpModule.Pump.Pressure.UpperLimit	500	
	    Flow through restriction capillary		
	    ColumnComp.UpperValve.CurrentPosition	1	
	    ColumnComp.LowerValve.CurrentPosition	1	
End If			
	Pump settings		
	PumpModule.Pump.%A1_Equate	Water	
	PumpModule.Pump.%A2_Equate	Water/Acetontrile=92/8	
	PumpModule.Pump.Pressure.LowerLimit	20 [bar]	
	PumpModule.Pump.MaximumFlowRampDown	5000	
	PumpModule.Pump.MaximumFlowRampUp	5000	
	Delay	1	
	PumpModule.Pump.%A_Selector	%A1	
	PumpModule.Pump.%B_Selector	%B1	
	PumpModule.Pump.Flow.Nominal	0.500 [ml/min]	
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
	SamplerModule.Sampler.WashSpeed	17	
	SamplerModule.Sampler.PunctureOffset	0	
	Autosampler settings (Sampler)		
	SamplerModule.Sampler.InjectWashMode	NoWash	
	SamplerModule.Sampler.WashTime	2.000 [s]	
0.000	Equilibration		
	UV.Autozero		
0.000	InjectPreparation		
	Wait	UV.Ready and Pump.Ready and ColumnComp.Ready and Sampler.Ready	
0.000	Inject		
	SamplerModule.Sampler.Inject		
0.000	StartRun		
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
	UV.UV_VIS_1.AcqOn		
	SamplerModule.TableIndexerMode.AcqOn		
0.000	Run	Duration = 0.040 [min]	
If		SamplerModule.TableIndexerMode.Signal>0	
0.040	    ColumnComp.CC_Temp.AcqOff		
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
	    UV.UV_VIS_1.AcqOff		
	    SamplerModule.TableIndexerMode.AcqOff		
	    Delay	1	
	    Protocol	Indexer-Fehler. Bitte Motor des Drehtellers austauschen und den defekten Motor an R&D übergeben.	
	    System.AbortQueue		
Else			
End If			
1.000	StopRun		
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
	UV.UV_VIS_1.AcqOff		
	SamplerModule.TableIndexerMode.AcqOff		
1.000	PostRun		
	End		
```

<a id="m-vas-foq-vasa-cooled-co-rc"></a>
## M-VAS-FOQ-VASA-COOLED-CO-RC: FOQ_VASA_Cooled_CO_RC

Source CMBX: `9318349.cmbx`  
Decoded flow SHA-256: `a269979adf84e034fd6de2bcbfeb37bfb10d9309f498198a2070c16b6a0e06dd`  
Decoded rows: `130`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	================================================================		
	Carry over (restriction capillary) with caffeine (single injector)		
	================================================================		
	Column oven settings		
	ColumnComp.CC.TempCtrl	On	
	ColumnComp.CC.Temperature.LowerLimit	5.0 [°C]	
	ColumnComp.CC.Temperature.UpperLimit	70.0 [°C]	
	ColumnComp.CC.EquilibrationTime	0.5 [min]	
	ColumnComp.CC.ReadyTempDelta	0.5 [°C]	
	ColumnComp.CC.Mode	ForcedAir	
If		SamplerModule.ModelNo="VA-A12-A"	
	    ColumnComp.CC.Temperature.Nominal	30	
	    PumpModule.Pump.Pressure.UpperLimit	500	
	    Flow through restriction capillary		
	    ColumnComp.UpperValve.CurrentPosition	1	
	    ColumnComp.LowerValve.CurrentPosition	1	
End If			
	Pump settings		
	PumpModule.Pump.Pressure.LowerLimit	20 [bar]	
	PumpModule.Pump.MaximumFlowRampDown	5000.00 [ml/min²]	
	PumpModule.Pump.MaximumFlowRampUp	5000.00 [ml/min²]	
	PumpModule.Pump.%A.Equate	%A1	
	PumpModule.Pump.%B.Equate	%B1	
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
	SamplerModule.Sampler.InjectWashMode	AfterDraw	
	SamplerModule.Sampler.WashTime	2	
	SamplerModule.Sampler.WashSpeed	17	
0.000	Equilibration		
	UV.Autozero		
0.000	InjectPreparation		
	Wait	UV.Ready and Pump.Ready and ColumnComp.Ready and Sampler.Ready	
0.000	Inject		
	SamplerModule.Sampler.Inject		
0.000	StartRun		
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
If		SamplerModule.TableIndexerMode.Signal>0	
0.040	    ColumnComp.CC_Temp.AcqOff		
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
	    Protocol	Indexer-Fehler. Bitte Motor des Drehtellers austauschen und den defekten Motor an R&D übergeben.	
	    System.AbortQueue		
Else			
End If			
0.900	Log	Sampler_Service.MeteringPos	
	SamplerModule.SamplerModule_Service._SendCommand	CommandString="Sampler.CompressVol="	
	SamplerModule.SamplerModule_Service._SendCommand	CommandString="Sampler.CompressPos="	
	SamplerModule.SamplerModule_Service._SendCommand	CommandString="Sampler.DecompressVol="	
7.000	StopRun		
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
7.000	PostRun		
	End		
```

<a id="m-vas-foq-vasa-cooled-co-rc-fill-ref-vials"></a>
## M-VAS-FOQ-VASA-COOLED-CO-RC-FILL-REF-VIALS: FOQ_VASA_Cooled_CO_RC_Fill_Ref_Vials

Source CMBX: `9318349.cmbx`  
Decoded flow SHA-256: `702200efd45b2ef597c82e55d726350f45483431bd7892a37b895a93cb7087e2`  
Decoded rows: `142`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	================================================================		
	Carry over (restriction capillary) with caffeine (single injector)		
	================================================================		
	Column oven settings		
	ColumnComp.CC.TempCtrl	On	
	ColumnComp.CC.Temperature.LowerLimit	5.0 [°C]	
	ColumnComp.CC.Temperature.UpperLimit	70.0 [°C]	
	ColumnComp.CC.EquilibrationTime	0.5 [min]	
	ColumnComp.CC.ReadyTempDelta	0.5 [°C]	
	ColumnComp.CC.Mode	ForcedAir	
If		SamplerModule.ModelNo="VA-A12-A"	
	    ColumnComp.CC.Temperature.Nominal	30	
	    PumpModule.Pump.Pressure.UpperLimit	500	
	    Flow through restriction capillary		
	    ColumnComp.UpperValve.CurrentPosition	1	
	    ColumnComp.LowerValve.CurrentPosition	1	
End If			
	Pump settings		
	PumpModule.Pump.Pressure.LowerLimit	0 [bar]	
	PumpModule.Pump.MaximumFlowRampDown	5000.00 [ml/min²]	
	PumpModule.Pump.MaximumFlowRampUp	5000.00 [ml/min²]	
	PumpModule.Pump.%A.Equate	%A1	
	PumpModule.Pump.%B.Equate	%B1	
	PumpModule.Pump.%A_Selector	%A1	
	PumpModule.Pump.%B_Selector	%B1	
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
0.000	Equilibration		
	UV.Autozero		
	PumpModule.Pump.Motor	Off	Stop the pump
0.000	InjectPreparation		
	Wait	UV.Ready and Pump.Ready and ColumnComp.Ready and Sampler.Ready	
0.000	StartRun		
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
0.000	Run	Duration = 2.000 [min]	
	Wait here to ensure that restrictor back pressure has dropped, to avoid back flow into the open needle seat		
If		SamplerModule.TableIndexerMode.Signal>0	
0.040	    ColumnComp.CC_Temp.AcqOff		
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
	    Protocol	Indexer-Fehler. Bitte Motor des Drehtellers austauschen und den defekten Motor an R&D übergeben.	
	    System.AbortQueue		
Else			
End If			
0.300	SamplerModule.SamplerModule_Service._SendCommand	Sampler.GotoPosition=2	Move needle to the purge position
	Delay	6	
	PumpModule.Pump.Flow.Nominal	3.000 [ml/min]	Needle tip purge flow
	Delay	10	Purge the needle tip, push "old" solvent into waste
	PumpModule.Pump.Motor	Off	Stop the pump
	Delay	2	Wait until the pump is stopped
	SamplerModule.SamplerModule_Service._SendCommand	Sampler.GotoPosition=0x010501	Move needle to R:E1
	Delay	6	Wait until the needle is on position of the solvent reference vial/well
	PumpModule.Pump.Flow.Nominal	3.000 [ml/min]	Activate the pump to fill up the solvent reference vial
	Delay	30	Wait until the vial or well is filled up to the desired level
	PumpModule.Pump.Motor	Off	Stop the pump
	SamplerModule.Sampler.Wash		Remove solvent droplets filling up the needle seat
	Log	Sampler_Service.MeteringPos	
	SamplerModule.SamplerModule_Service._SendCommand	CommandString="Sampler.CompressVol="	
	SamplerModule.SamplerModule_Service._SendCommand	CommandString="Sampler.CompressPos="	
	SamplerModule.SamplerModule_Service._SendCommand	CommandString="Sampler.DecompressVol="	
2.000	PumpModule.Pump.Flow.Nominal	3.000 [ml/min]	Needle tip purge flow, command neede here to avoid the driver from creating a flow gradient
If		1=1	
	    PumpModule.Pump.Flow.Nominal	Variables.GenericFloat1	Restore to calculated flow
End If			
4.000	StopRun		
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
4.000	PostRun		
	End		
```

<a id="m-vas-foq-vasa-cooled-co-rc-solv-ref"></a>
## M-VAS-FOQ-VASA-COOLED-CO-RC-SOLV-REF: FOQ_VASA_Cooled_CO_RC_Solv_Ref

Source CMBX: `9318349.cmbx`  
Decoded flow SHA-256: `c00f80141f81ab636fd4c202a4778693f64a1d1866db3e425a8192126c1bc1e6`  
Decoded rows: `130`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	================================================================		
	Carry over (restriction capillary) with caffeine (single injector)		
	================================================================		
	Column oven settings		
	ColumnComp.CC.TempCtrl	On	
	ColumnComp.CC.Temperature.LowerLimit	5.0 [°C]	
	ColumnComp.CC.Temperature.UpperLimit	70.0 [°C]	
	ColumnComp.CC.EquilibrationTime	0.5 [min]	
	ColumnComp.CC.ReadyTempDelta	0.5 [°C]	
	ColumnComp.CC.Mode	ForcedAir	
If		SamplerModule.ModelNo="VA-A12-A"	
	    ColumnComp.CC.Temperature.Nominal	30	
	    PumpModule.Pump.Pressure.UpperLimit	500	
	    Flow through restriction capillary		
	    ColumnComp.UpperValve.CurrentPosition	1	
	    ColumnComp.LowerValve.CurrentPosition	1	
End If			
	Pump settings		
	PumpModule.Pump.Pressure.LowerLimit	20 [bar]	
	PumpModule.Pump.MaximumFlowRampDown	5000.00 [ml/min²]	
	PumpModule.Pump.MaximumFlowRampUp	5000.00 [ml/min²]	
	PumpModule.Pump.%A.Equate	%A1	
	PumpModule.Pump.%B.Equate	%B1	
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
	SamplerModule.Sampler.InjectWashMode	AfterDraw	
	SamplerModule.Sampler.WashTime	2	
	SamplerModule.Sampler.WashSpeed	17	
0.000	Equilibration		
	UV.Autozero		
0.000	InjectPreparation		
	Wait	UV.Ready and Pump.Ready and ColumnComp.Ready and Sampler.Ready	
0.000	Inject		
	SamplerModule.Sampler.Inject		
0.000	StartRun		
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
If		SamplerModule.TableIndexerMode.Signal>0	
0.040	    ColumnComp.CC_Temp.AcqOff		
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
	    Protocol	Indexer-Fehler. Bitte Motor des Drehtellers austauschen und den defekten Motor an R&D übergeben.	
	    System.AbortQueue		
Else			
End If			
0.900	Log	Sampler_Service.MeteringPos	
	SamplerModule.SamplerModule_Service._SendCommand	CommandString="Sampler.CompressVol="	
	SamplerModule.SamplerModule_Service._SendCommand	CommandString="Sampler.CompressPos="	
	SamplerModule.SamplerModule_Service._SendCommand	CommandString="Sampler.DecompressVol="	
1.500	StopRun		
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
1.500	PostRun		
	End		
```

<a id="m-vas-foq-vasa-cooled-equilibration"></a>
## M-VAS-FOQ-VASA-COOLED-EQUILIBRATION: FOQ_VASA_Cooled_equilibration

Source CMBX: `9318349.cmbx`  
Decoded flow SHA-256: `c50e91089cc8bc45b17ead04d8708583206639ab06792597c32e96ff0810ed68`  
Decoded rows: `52`

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
If		SamplerModule.ModelNo="VA-A12-A"	
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
	PumpModule.Pump.%A.Equate	%A1	
	PumpModule.Pump.%B.Equate	%B1	
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
0.000	InjectPreparation		
	Wait	UV.Ready and Pump.Ready and ColumnComp.Ready and Sampler.Ready	
0.000	Run	Duration = 2.000 [min]	
	Delay	0.5	
	PumpModule.Pump.Flow.Nominal	1	
	Delay	0.5	
	End		
2.000	StopRun		
	End		
```

<a id="m-vas-foq-vasa-cooled-exceptionlog-clear"></a>
## M-VAS-FOQ-VASA-COOLED-EXCEPTIONLOG-CLEAR: FOQ_VASA_Cooled_ExceptionLog_Clear

Source CMBX: `9318349.cmbx`  
Decoded flow SHA-256: `920484fef1ca66cc558ad94b5b2e2e81dd09af0f7a1b66e3afb2039d1ee51b4a`  
Decoded rows: `32`

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
If		SamplerModule.ModelNo="VA-A12-A"	
	    PumpModule.Pump.Pressure.UpperLimit	500	
End If			
0.100	SamplerModule.Sampler.Inject		
	Commands to log the ErrorQueue		
0.150	SamplerModule.Disconnect		
	SamplerModule.Connect		
	Wait	Sampler.Ready	
	---------------------------------------------------------------------------------------		
	Switch valve to bypass and move needle out of the needle seat to avoid transport damage.		
0.300	SamplerModule.Sampler.SwitchValve	Bypass	
	Delay	1	
	SamplerModule.SamplerModule_Service._SendCommand	CommandString="Sampler.MoveNeedleUp=1"	
0.500	StopRun		
	End		
```

<a id="m-vas-foq-vasa-cooled-flow-adjustment-restriction-capillary"></a>
## M-VAS-FOQ-VASA-COOLED-FLOW-ADJUSTMENT-RESTRICTION-CAPILLARY: FOQ_VASA_Cooled_Flow_adjustment_restriction_capillary

Source CMBX: `9318349.cmbx`  
Decoded flow SHA-256: `76c2aa359f8f22b60c458b0b8ae95945bd319d194da5e5ecd15b48b45d476103`  
Decoded rows: `122`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	PumpModule.Pump.%B_Selector	%B1	
	PumpModule.Pump.%A_Selector	%A1	
	PumpModule.Pump.%B.Value	0	
	Generic Variables		
	Variables.GenericDouble0	0	logged system pressure after 30 s for calculation of new flow
	Variables.GenericDouble1	0	logged system pressure after 45 s for calculation of new flow
	Variables.GenericDouble2	0	logged system pressure after 60 s for calculation of new flow
	Variables.GenericDouble3	0	average of system pressure (GenericDouble0-2) for calculatiion of new flow
	Variables.GenericDouble4	0	logged pressure if calculated flow is below 1 mL/min or above 1.4 mL/min
	Variables.GenericFloat0	0.7	set flow in the beginning of the method for restriction capillary path ; VAccess
	Variables.GenericFloat1	0	new calculated flow through restriction capillary (Repor/Lin)
	Variables.GenericFloat2	0	set flow in the beginning of the method for column/restricition capillary waste path (CO)
	Variables.GenericFloat3	0	new, calculated flow through column (CO)
	Variables.GenericFloat4	0	new, calculated flow through restricition capillary to waste (CO high conc. sample)
	Pump settings		
	PumpModule.Pump.Pressure.LowerLimit	20 [bar]	
	PumpModule.Pump.MaximumFlowRampUp	Infinite	
	PumpModule.Pump.MaximumFlowRampDown	Infinite	
	Delay	1	
	PumpModule.Pump.Flow.Nominal	Variables.GenericFloat0	
	Column oven settings		
	ColumnComp.CC.Mode	ForcedAir	
	ColumnComp.CC.TempCtrl	On	
	ColumnComp.CC.Temperature.LowerLimit	5.0 [°C]	
	ColumnComp.CC.Temperature.UpperLimit	70.0 [°C]	
	ColumnComp.CC.EquilibrationTime	0.5 [min]	
	ColumnComp.CC.ReadyTempDelta	0.5 [°C]	
If		SamplerModule.ModelNo="VA-A12-A"	
	    ColumnComp.CC.Temperature.Nominal	30	
	    PumpModule.Pump.Pressure.UpperLimit	500	
	    Variables.GenericLong0	450	wanted system pressure
	    Variables.GenericLong1	410	minimum system pressure
	    Variables.GenericLong2	480	maximum system pressure
	    Delay	0.5	
	    Column oven valve settings --> Flow through restriction capillary		
	    ColumnComp.UpperValve.CurrentPosition	1	
	    ColumnComp.LowerValve.CurrentPosition	1	
End If			
	==============================================================================		
	Set instrument to Service Level		
	Performed twice to set the instrument reliably into service level		
	DO NOT CHANGE!		
	==============================================================================		
	SamplerModule.SamplerModule_Service.GetServiceCode		
	Delay	5	
	SamplerModule.SamplerModule_Service.ServiceCode	87794	
	Delay	1	
	Log	SamplerModule_Service.ServiceCode	
	Delay	1	
If		SamplerModule_Service.ServiceCode=Service	
Else			
	    SamplerModule.SamplerModule_Service.GetServiceCode		
	    Delay	5	
	    SamplerModule.SamplerModule_Service.ServiceCode	87794	
	    Delay	1	
	    Log	SamplerModule_Service.ServiceCode	
	    Delay	1	
End If			
0.000	StartRun		
	Wait	Pump.Ready and ColumnComp.Ready and Sampler.Ready	
0.000	Run	Duration = 0.040 [min]	
	PumpModule.Pump.Pump_Pressure.AcqOn		
	SamplerModule.TableIndexerMode.AcqOn		
	Delay	30	
	Variables.GenericDouble0	PumpModule.Pump.Pump_Pressure.Signal	System pressure at 1 mL/min
	Delay	15	
	Variables.GenericDouble1	PumpModule.Pump.Pump_Pressure.Signal	System pressure at 1 mL/min
	Delay	15	
	Variables.GenericDouble2	PumpModule.Pump.Pump_Pressure.Signal	System pressure at 1 mL/min
	Delay	1	
	Variables.GenericDouble3	(Variables.GenericDouble0+Variables.GenericDouble1+Variables.GenericDouble2)/3	Average of GenericDouble0-2
	Delay	1	
	Log	Variables.GenericDouble3	Averaged system pressure
	Delay	1	
	Variables.GenericFloat1	(GenericLong0*Variables.GenericFloat0)/Variables.GenericDouble3	New flow rate
	Delay	1	
	Log	Variables.GenericFloat1	
If		GenericFloat1>=0.70 AND Variables.GenericFloat1<=1.10	
	    PumpModule.Pump.Flow.Nominal	Variables.GenericFloat1	
	    End		
Else If		Variables.GenericFloat1>=1.10	
	    PumpModule.Pump.Flow.Nominal	1.10	
	    Delay	30	
	    Variables.GenericDouble4	PumpModule.Pump.Pump_Pressure.Signal	
	    Delay	1	
	    Log	Variables.GenericDouble4	
    If		Variables.GenericDouble4>=Variables.GenericLong1 AND Variables.GenericDouble4<=Variables.GenericLong2	
	        Variables.GenericFloat1	1.1	
	        End		
    Else			
	        Protocol	System Pressure out of Limit - Pressure to low	
	        Variables.GenericFloat1	0.005	Set this variable to a very low value. If the queue is continued by accident, the following injection will be interrupted due to the lower pump pressure limit.
	        System.AbortQueue		
    End If			
Else If		Variables.GenericFloat1<=0.7	
	    PumpModule.Pump.Flow.Nominal	0.7	
	    Delay	30	
	    Variables.GenericDouble4	PumpModule.Pump.Pump_Pressure.Signal	
	    Delay	1	
	    Log	Variables.GenericDouble4	
    If		Variables.GenericDouble4>=Variables.GenericLong1 AND Variables.GenericDouble4<=Variables.GenericLong2	
	        Variables.GenericFloat1	0.7	
	        End		
    Else			
	        Protocol	System Pressure out of Limit - Pressure to high	
	        Variables.GenericFloat1	0.005	Set this variable to a very low value. If the queue is continued by accident, the following injection will be interrupted due to the lower pump pressure limit.
	        System.AbortQueue		
    End If			
End If			
If		SamplerModule.TableIndexerMode.Signal>0	
0.040	    PumpModule.Pump.Pump_Pressure.AcqOff		
	    SamplerModule.TableIndexerMode.AcqOff		
	    Delay	1	
	    Protocol	Indexer-Fehler. Bitte Motor des Drehtellers austauschen und den defekten Motor an R&D übergeben.	
	    System.AbortQueue		
Else			
End If			
4.000	StopRun		
	PumpModule.Pump.Pump_Pressure.AcqOff		
	SamplerModule.TableIndexerMode.AcqOff		
	End		
```

<a id="m-vas-foq-vasa-cooled-init"></a>
## M-VAS-FOQ-VASA-COOLED-INIT: FOQ_VASA_Cooled_Init

Source CMBX: `9318349.cmbx`  
Decoded flow SHA-256: `615fc5c2ee310d2842aab14dfd3dfeda67f09d0ad8699e23f2c1dade90a0e921`  
Decoded rows: `135`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	================================================================		
	Initialization instrument method for VAS and DVAS		
	================================================================		
	This IM performs an initialization of the VAS.		
	==> DO NOT CHANGE THIS instrument method! <==		
	The following data regarding the drive movement deviations is		
	written to the audit trail for diagnostic purposes:		
	Needle home deviation: vertical needle drive		
	Horizontal home deviation: horizontal needle drive		
	Compression home deviation: compression drive		
	Metering home deviation: metering drive		
	Column oven settings		
	ColumnComp.CC.TempCtrl	On	
	ColumnComp.CC.Temperature.LowerLimit	5.0 [°C]	
	ColumnComp.CC.Temperature.UpperLimit	70.0 [°C]	
	ColumnComp.CC.EquilibrationTime	0.5 [min]	
	ColumnComp.CC.ReadyTempDelta	0.5 [°C]	
	ColumnComp.CC.Mode	ForcedAir	
If		SamplerModule.ModelNo="VA-A12-A"	
	    ColumnComp.CC.Temperature.Nominal	30	
	    PumpModule.Pump.Pressure.UpperLimit	500	
	    Flow through restriction capillary		
	    ColumnComp.UpperValve.CurrentPosition	1	
	    ColumnComp.LowerValve.CurrentPosition	1	
End If			
	PumpModule.Pump.Pressure.LowerLimit	20 [bar]	
	PumpModule.Pump.MaximumFlowRampDown	5000	
	PumpModule.Pump.MaximumFlowRampUp	5000	
	PumpModule.Pump.%A.Equate	%A1	
	PumpModule.Pump.%B.Equate	%B1	
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
	SamplerModule.Sampler.DispenseSpeed	15.000	
	SamplerModule.Sampler.PunctureOffset	0	
	Autosampler settings (Sampler)		
	SamplerModule.Sampler.InjectWashMode	NoWash	
0.000	Equilibration		
	UV.Autozero		
0.000	InjectPreparation		
	Wait	UV.Ready and Pump.Ready and ColumnComp.Ready and Sampler.Ready	
0.000	Inject		
	SamplerModule.Sampler.Inject		
0.000	StartRun		
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
0.000	Run	Duration = 0.200 [min]	
If		SamplerModule.TableIndexerMode.Signal>0	
0.040	    ColumnComp.CC_Temp.AcqOff		
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
	    Protocol	Indexer-Fehler. Bitte Motor des Drehtellers austauschen und den defekten Motor an R&D übergeben.	
	    System.AbortQueue		
Else			
End If			
	Sampler is initialized to check for drive movement step deviations		
0.100	SamplerModule.Init		
0.200	Wait	Sampler.Ready	
	Log	SamplerModule.Sampler.Sampler_Service.CompressionDrvHomeDeviation	
	Log	SamplerModule.Sampler.Sampler_Service.MeteringDrvHomeDeviation	
	Log	SamplerModule.Sampler.Sampler_Service.NeedleDrvHomeDeviation	
	Log	SamplerModule.Sampler.Sampler_Service.HorizontalDrvHomeDeviation	
2.500	StopRun		
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
2.500	PostRun		
	End		
```

<a id="m-vas-foq-vasa-cooled-in-relay-vwd"></a>
## M-VAS-FOQ-VASA-COOLED-IN-RELAY-VWD: FOQ_VASA_Cooled_IN_RELAY_VWD

Source CMBX: `9318349.cmbx`  
Decoded flow SHA-256: `9096dd717d490214b4e972d96c84a712b390d1c3d992fc7fe0fde80dc49a5d8f`  
Decoded rows: `47`

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
	PumpModule.Pump.%A.Equate	Water	
	PumpModule.Pump.Flow.Nominal	0.100 [ml/min]	
	PumpModule.Pump.%B.Value	0	
If		SamplerModule.ModelNo="VA-A12-A"	
	    PumpModule.Pump.Pressure.UpperLimit	500	
End If			
0.000	InjectPreparation		
	Wait	Sampler.Ready	
0.000	StartRun		
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
0.900	StopRun		
	UV.UV_VIS_1.AcqOff		
0.900	PostRun		
	End		
```

<a id="m-vas-foq-vasa-cooled-linearity-setidlevolume"></a>
## M-VAS-FOQ-VASA-COOLED-LINEARITY-SETIDLEVOLUME: FOQ_VASA_Cooled_Linearity_SetIdleVolume

Source CMBX: `9318349.cmbx`  
Decoded flow SHA-256: `d60f375e784402f17ce777048971a6b36891a68ff78b9043492a679da228c034`  
Decoded rows: `58`

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
If		SamplerModule.ModelNo="VA-A12-A"	
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
	PumpModule.Pump.%A.Equate	%A1	
	PumpModule.Pump.%B.Equate	%B1	
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
0.000	InjectPreparation		
	Wait	Sampler.Ready	
0.000	Run	Duration = 1.500 [min]	
	SamplerModule.SamplerModule_Service._SendCommand	Sampler.SetIdleVolume=+System.Injection.CustomVariables.IdleVolume	
1.500	StopRun		
	Log	SamplerModule.Sampler.IdleVolume	
	End		
```

<a id="m-vas-foq-vasa-cooled-mh-max-range-in-oneinj-noudp"></a>
## M-VAS-FOQ-VASA-COOLED-MH-MAX-RANGE-IN-ONEINJ-NOUDP: FOQ_VASA_Cooled_MH_Max_Range_in_oneInj - NoUdp

Source CMBX: `9318349.cmbx`  
Decoded flow SHA-256: `25f09550f6f560aff2eee8deaffb0f5cc2ac1311a87437615a334cb30a65ecb5`  
Decoded rows: `162`

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
If		SamplerModule.ModelNo="VA-A12-A"	
	    ColumnComp.CC.Temperature.Nominal	30	
	    PumpModule.Pump.Pressure.UpperLimit	500	
	    Flow through restriction capillary		
	    ColumnComp.UpperValve.CurrentPosition	1	
	    ColumnComp.LowerValve.CurrentPosition	1	
End If			
	Pump settings		
	PumpModule.PumpModule_Service.GetServiceCode		
	PumpModule.PumpModule_Service.ServiceCode	87794	
	PumpModule.Pump.Pressure.LowerLimit	20 [bar]	
	PumpModule.Pump.MaximumFlowRampDown	5000.00 [ml/min²]	
	PumpModule.Pump.MaximumFlowRampUp	5000.00 [ml/min²]	
	PumpModule.Pump.%A.Equate	%A1	
	PumpModule.Pump.%B.Equate	%B1	
	PumpModule.Pump.%A_Selector	%A1	
	PumpModule.Pump.%B_Selector	%B1	
	PumpModule.Pump.Flow.Nominal	0.83	
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
0.000	Equilibration		
	UV.Autozero		
0.000	InjectPreparation		
	Wait	UV.Ready and Pump.Ready and ColumnComp.Ready and Sampler.Ready	
0.000	StartRun		
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
	SamplerModule.SamplerModule_Service._SendCommand	Sampler.MDMove=1,256250	MD out of the way
	Delay	5	
	SamplerModule.SamplerModule_Service._SendCommand	Sampler.MDMove=0,237000	CD new artificial idle volume
	Delay	5	
	SamplerModule.SamplerModule_Service._SendCommand	Sampler.Valve=3	Valve Compress/Decompress/Draw
	Delay	5	
	SamplerModule.SamplerModule_Service._SendCommand	Sampler.MDMove=0,251000	CD Decompress
	Delay	5	
	SamplerModule.SamplerModule_Service._SendCommand	Sampler.Valve=1	Valve Bypass
	Delay	5	
	SamplerModule.SamplerModule_Service._SendCommand	Sampler.MDMove=0,248500	CD move to draw position - backlash compensation
	Delay	5	
	SamplerModule.SamplerModule_Service._SendCommand	Sampler.MDMove=1,248500	MD move to draw position - backlash compensation
	Delay	5	
	SamplerModule.SamplerModule_Service._SendCommand	Sampler.MDMove=0,256250	CD turn over to MD drive move out of the way
	Delay	5	
	SamplerModule.SamplerModule_Service._SendCommand	Sampler.MDMove=1,249000	MD move to draw position
	Delay	5	
	SamplerModule.SamplerModule_Service._SendCommand	Sampler.Valve=3	Valve Compress/Decompress/Draw
	Delay	5	
	SamplerModule.SamplerModule_Service._SendCommand	Sampler.CabinFan=0	Turns the cabin fan off during injection as is done in normal injections
	Delay	5	
	SamplerModule.SamplerModule_Service._SendCommand	Sampler.GotoPosition=0x010001	go to vial SR:1
	Delay	5	
	SamplerModule.SamplerModule_Service._SendCommand	Sampler.MDMove=1,252000	MD aspirate
	Delay	3	
	SamplerModule.SamplerModule_Service._SendCommand	Sampler.GotoPosition=0	go to needle seat
	Delay	5	
	SamplerModule.SamplerModule_Service._SendCommand	Sampler.CabinFan=1	Turns the cabin fan back on after injection as is done in normal injections
	Delay	5	
	SamplerModule.SamplerModule_Service._SendCommand	Sampler.MDMove=0,237000	CD precompress
	Delay	5	
	SamplerModule.SamplerModule_Service._SendCommand	Sampler.Valve=2	Inject
	Delay	5	
If		SamplerModule.TableIndexerMode.Signal>0	
0.800	    ColumnComp.CC_Temp.AcqOff		
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
	    Protocol	Indexer-Fehler. Bitte Motor des Drehtellers austauschen und den defekten Motor an R&D übergeben.	
	    System.AbortQueue		
Else			
End If			
0.900	Log	Sampler_Service.MeteringPos	
	SamplerModule.SamplerModule_Service._SendCommand	CommandString="Sampler.CompressVol="	
	SamplerModule.SamplerModule_Service._SendCommand	CommandString="Sampler.CompressPos="	
	SamplerModule.SamplerModule_Service._SendCommand	CommandString="Sampler.DecompressVol="	
2.500	StopRun		
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
2.500	PostRun		
	End		
```

<a id="m-vas-foq-vasa-cooled-precision-linearity"></a>
## M-VAS-FOQ-VASA-COOLED-PRECISION-LINEARITY: FOQ_VASA_Cooled_Precision_Linearity

Source CMBX: `9318349.cmbx`  
Decoded flow SHA-256: `b2a758439fd7121ab23d078844df104ec19a7f2fde48f420ab90f233bf908372`  
Decoded rows: `128`

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
If		SamplerModule.ModelNo="VA-A12-A"	
	    ColumnComp.CC.Temperature.Nominal	25	
	    PumpModule.Pump.Pressure.UpperLimit	500	
	    Flow through restriction capillary		
	    ColumnComp.UpperValve.CurrentPosition	1	
	    ColumnComp.LowerValve.CurrentPosition	1	
End If			
	Pump settings		
	PumpModule.Pump.Pressure.LowerLimit	20 [bar]	
	PumpModule.Pump.MaximumFlowRampDown	5000.00 [ml/min²]	
	PumpModule.Pump.MaximumFlowRampUp	5000.00 [ml/min²]	
	PumpModule.Pump.%A.Equate	%A1	
	PumpModule.Pump.%B.Equate	%B1	
	PumpModule.Pump.%A_Selector	%A1	
	PumpModule.Pump.%B_Selector	%B1	
	PumpModule.Pump.Flow.Nominal	0.7	
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
0.000	Equilibration		
	UV.Autozero		
0.000	InjectPreparation		
	Wait	UV.Ready and Pump.Ready and ColumnComp.Ready and Sampler.Ready	
0.000	Inject		
	SamplerModule.Sampler.Inject		
0.000	StartRun		
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
If		SamplerModule.TableIndexerMode.Signal>0	
0.040	    ColumnComp.CC_Temp.AcqOff		
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
	    Protocol	Indexer-Fehler. Bitte Motor des Drehtellers austauschen und den defekten Motor an R&D übergeben.	
	    System.AbortQueue		
Else			
End If			
0.900	Log	Sampler_Service.MeteringPos	
	SamplerModule.SamplerModule_Service._SendCommand	CommandString="Sampler.CompressVol="	
	SamplerModule.SamplerModule_Service._SendCommand	CommandString="Sampler.CompressPos="	
	SamplerModule.SamplerModule_Service._SendCommand	CommandString="Sampler.DecompressVol="	
1.800	StopRun		
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
1.800	PostRun		
	End		
```

<a id="m-vas-foq-vasa-cooled-setparameters"></a>
## M-VAS-FOQ-VASA-COOLED-SETPARAMETERS: FOQ_VASA_Cooled_SetParameters

Source CMBX: `9318349.cmbx`  
Decoded flow SHA-256: `e3dfa9c74a83f7e490736624736c70c7ddc0721d8093569bb550c28fb6b5ba63`  
Decoded rows: `112`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	PumpModule.Pump.Pressure.LowerLimit	0 [bar]	
	SamplerModule.Temperature.Nominal	20	
	ColumnComp.CC.Mode	ForcedAir	
	================================================================		
	Set of Service, Qualification and Wellness Parameters		
	================================================================		
If		SamplerModule.ModelNo="VA-A12-A"	
	    ColumnComp.CC.Temperature.Nominal	30	
	    PumpModule.Pump.Pressure.UpperLimit	500	
	    Flow through restriction capillary		
	    ColumnComp.UpperValve.CurrentPosition	1	
	    ColumnComp.LowerValve.CurrentPosition	1	
Else If		SamplerModule.ModelNo="VC-A13-A"	
	    SamplerModule.SamplerModule_Service._SendCommand	LedBar.ForceColor=1	Led bar red
	    Delay	1	
	    Message	Wrong FOQ template: Please use template for uncooled version of VAS-C. 	
	    Delay	1	
	    SamplerModule.SamplerModule_Service._SendCommand	LedBar.ForceColor=0	Led bar auto
	    Delay	1	
	    System.AbortQueue		
Else If		SamplerModule.ModelNo="VH-A10-A" or SamplerModule.ModelNo="VF-A10-A" or SamplerModule.ModelNo="VH-A40-A" or SamplerModule.ModelNo="VF-A40-A"	
	    SamplerModule.SamplerModule_Service._SendCommand	LedBar.ForceColor=1	Led bar red
	    Delay	1	
	    Message	Wrong FOQ template: Please use VAS or DVAS template.	
	    Delay	1	
	    SamplerModule.SamplerModule_Service._SendCommand	LedBar.ForceColor=0	Led bar auto
	    Delay	1	
	    System.AbortQueue		
End If			
0.000	Run	Duration = 1.300 [min]	
	==============================================================================		
	Set instrument to Service Level		
	Performed twice to set the instrument reliably into service level		
	DO NOT CHANGE!		
	==============================================================================		
	SamplerModule.SamplerModule_Service.GetServiceCode		
	Delay	5	
	SamplerModule.SamplerModule_Service.ServiceCode	87794	
	Delay	1	
	Log	SamplerModule_Service.ServiceCode	
	Delay	1	
If		SamplerModule_Service.ServiceCode=Service	
Else			
	    SamplerModule.SamplerModule_Service.GetServiceCode		
	    Delay	5	
	    SamplerModule.SamplerModule_Service.ServiceCode	87794	
	    Delay	1	
	    Log	SamplerModule_Service.ServiceCode	
	    Delay	1	
End If			
	==============================================================================		
	---------------------------------------------------------------------------------------		
	Set the Qualification parameters (Qualification date equal to FOQ date)		
	---------------------------------------------------------------------------------------		
0.100	SamplerModule.SamplerModule_Wellness.Qualification.Interval	None	
	SamplerModule.SamplerModule_Wellness.Qualification.WarningPeriod	None	
	SamplerModule.SamplerModule_Wellness.Qualification.GracePeriod	None	
	SamplerModule.SamplerModule_Wellness.DrainPumpTubeChanged		
	SamplerModule.Sampler.Sampler_Wellness.NeedleSeatChanged		
	SamplerModule.Sampler.Sampler_Wellness.NeedleChanged		
	---------------------------------------------------------------------------------------		
	Set the Service parameters (Service date equal to FOQ date)		
	---------------------------------------------------------------------------------------		
	SamplerModule.SamplerModule_Wellness.Service.Interval	None	
	SamplerModule.SamplerModule_Wellness.Service.WarningPeriod	None	
	SamplerModule.Sampler.Sampler_Wellness.NeedleSeatCounter.Warning	Off	
	SamplerModule.Sampler.Sampler_Wellness.NeedleSeatCounter.Limit	Off	
	---------------------------------------------------------------------------------------		
	Set the parameters back to standardvalues after burn in		
	---------------------------------------------------------------------------------------		
	SamplerModule.SamplerModule_Service._SendCommand	Sampler.SetFactoryDefaults	
	Delay	2	
	SamplerModule.SamplerModule_Service._SendCommand	Sampler.SetFactoryInternals	
	Delay	2	
0.150	Log	SamplerModule_Wellness.PowerOnTime	
	Log	SamplerModule_Wellness.OperatingHours	
	Log	DrainPumpHours	
	Log	DrainPumpTubeHours.Value	
	Log	TrayDriveMovements	
	Log	BCR_ScanCounter	
	Log	SamplerModule_Wellness.HeatingWorkLoad	
	Log	SamplerModule_Wellness.CoolingWorkLoad	
	Log	NeedleSeatCounter.Value	
	Log	NeedleMovements.Value	
	Log	HorizontalDriveMovements	
	Log	NeedleDriveMovements	
	Log	MeteringDriveMovements	
	Log	InjectValveSwitches	
	Log	TotalInjections	
	Log	NeedleObstructions	
	Log	WashPumpHours	
	Log	InjectOptimizationMode	
If		SamplerModule.Sampler.Sampler_Service.InjectOptimizationMode=Firmware	
Else			
	    SamplerModule.SamplerModule_Service._SendCommand	LedBar.ForceColor=1	
	    Message	The Inject Optimization is turned off. Please repeat the Factory Defaults injection	
	    SamplerModule.SamplerModule_Service._SendCommand	LedBar.ForceColor=0	
	    System.AbortQueue		
End If			
0.300	SamplerModule.SamplerModule_Wellness.DrainPumpTubeHours.Warning	Off	
	SamplerModule.SamplerModule_Wellness.DrainPumpTubeHours.Limit	Off	
0.350	SamplerModule.Sampler.Sampler_Wellness.NeedleMovements.Warning	Off	
	SamplerModule.Sampler.Sampler_Wellness.NeedleMovements.Limit	Off	
0.400	Log	NeedleMovements.Value	
0.600	SamplerModule.SamplerModule_Service._SendCommand	CommandString="Sampler.LoopVol=130000"	
	SamplerModule.SamplerModule_Service._SendCommand	CommandString="Sampler.NominalLoopVol=100000"	
0.650	Protocol	Sampler is disconnected and reconnected to send the default sample loop volume to CM.	
0.700	SamplerModule.Disconnect		
1.000	SamplerModule.Connect		
1.300	Log	Sampler.LoopVolume	
	End		
```

<a id="m-vas-foq-vasa-cooled-stop"></a>
## M-VAS-FOQ-VASA-COOLED-STOP: FOQ_VASA_Cooled_STOP

Source CMBX: `9318349.cmbx`  
Decoded flow SHA-256: `749aab58ae068bf81cb8accdf76f95b10234a17e6f7b6f81de3229dcfad3ba76`  
Decoded rows: `121`

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
If		SamplerModule.ModelNo="VA-A12-A"	
	    PumpModule.Pump.Pressure.UpperLimit	500	
End If			
	SamplerModule.Sampler_CompressDelay.AcqOn		
	SamplerModule.Sampler_CompressSpeed.AcqOn		
	SamplerModule.Sampler_DecompressDelay.AcqOn		
	SamplerModule.TableIndexerMode.AcqOn		
If		SamplerModule.TableIndexerMode.Signal>0	
0.040	    SamplerModule.Sampler_BacklashCompensation.AcqOff		
	    SamplerModule.Sampler_CompressSpeed.AcqOff		
	    SamplerModule.Sampler_CompressDelay.AcqOff		
	    SamplerModule.Sampler_DecompressDelay.AcqOff		
	    SamplerModule.TableIndexerMode.AcqOff		
	    Delay	1	
	    Protocol	Indexer-Fehler. Bitte Motor des Drehtellers austauschen und den defekten Motor an R&D übergeben.	
	    System.AbortQueue		
Else			
End If			
0.100	SamplerModule.SamplerModule_Service.GetServiceCode		
	Delay	5	
	SamplerModule.SamplerModule_Service.ServiceCode	87794	
	Delay	1	
	Log	SamplerModule_Service.ServiceCode	
	Delay	1	
If		SamplerModule_Service.ServiceCode=Service	
Else			
	    SamplerModule.SamplerModule_Service.GetServiceCode		
	    Delay	5	
	    SamplerModule.SamplerModule_Service.ServiceCode	87794	
	    Delay	1	
	    Log	SamplerModule_Service.ServiceCode	
	    Delay	1	
End If			
0.200	SamplerModule.Sampler.Inject		
	SamplerModule.SamplerModule_Service._SendCommand	Sampler.SetFactoryDefaults	
	Delay	2	
	SamplerModule.SamplerModule_Service._SendCommand	Sampler.SetFactoryInternals	
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
	SamplerModule.SamplerModule_Service._SendCommand	HardwareRevision=	
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
If		SamplerModule_Service.ServiceCode=Service	
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

<a id="m-vas-foq-vasa-cooled-system-flush"></a>
## M-VAS-FOQ-VASA-COOLED-SYSTEM-FLUSH: FOQ_VASA_Cooled_System_Flush

Source CMBX: `9318349.cmbx`  
Decoded flow SHA-256: `4cacd11b3cacc4e4624987f4dd68938587506bcb41d16979577ba1c8af7501da`  
Decoded rows: `76`

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
If		SamplerModule.ModelNo="VA-A12-A"	
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
	PumpModule.Pump.%A.Equate	%A1	
	PumpModule.Pump.%B.Equate	%B1	
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
0.000	InjectPreparation		
	Wait	UV.Ready and Pump.Ready and ColumnComp.Ready and Sampler.Ready	
0.000	Inject		
0.000	StartRun		
	PumpModule.Pump.Pump_Pressure.AcqOn		
	SamplerModule.TableIndexerMode.AcqOn		
0.000	Run	Duration = 10.000 [min]	
Trigger		"Injection",	
	    Condition	Variables.GenericBool0=1	
	    TrueTime	0	
	    Delay	0	
	    Limit	Infinite	
	    Hysteresis	0.0 [%]	
	    AllowImmediateExecution	Yes	
	Delay	1	
	SamplerModule.Sampler.Inject		
	Wait	SamplerModule.Sampler.Ready	
	Delay	0.5	
	Variables.GenericLong1	Variables.GenericLong1+1	
	Variables.GenericBool0	0	
	Variables.GenericBool1	1	
End Trigger			
	End-Trigger		
Trigger		"Toggle",	
	    Condition	Variables.GenericBool1=1	
	    TrueTime	0	
	    Delay	0	
	    Limit	Infinite	
	    Hysteresis	0	
	    AllowImmediateExecution	No	
	Delay	0.5	
	Variables.GenericBool0	1	
	Variables.GenericBool1	0	
If		Variables.GenericLong1>=System.Injection.CustomVariables.Injectionnumber_Flush	
	    Delay	90	
	    PumpModule.Pump.Pump_Pressure.AcqOff		
	    SamplerModule.TableIndexerMode.AcqOff		
	    End		
End If			
End Trigger			
10.000	StopRun		
	PumpModule.Pump.Pump_Pressure.AcqOff		
	SamplerModule.TableIndexerMode.AcqOff		
	End		
```

<a id="m-vas-foq-vasc-cooled-mh-max-range-in-oneinj"></a>
## M-VAS-FOQ-VASC-COOLED-MH-MAX-RANGE-IN-ONEINJ: FOQ_VASC_Cooled_MH_Max_Range_in_oneInj

Source CMBX: `9318349.cmbx`  
Decoded flow SHA-256: `4821b1a429b7792dc347ca4fd272e00793dbaa07d49d4168ca5660b57085070f`  
Decoded rows: `149`

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
If		SamplerModule.ModelNo="VA-A12-A"	
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
	PumpModule.Pump.%A.Equate	%A1	
	PumpModule.Pump.%B.Equate	%B1	
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
	SamplerModule.SamplerModule_Service._SendCommand	Sampler.UdpBegin=0	
	SamplerModule.SamplerModule_Service._SendCommand	Sampler.MDMove=1,256250	MD out of the way
	SamplerModule.SamplerModule_Service._SendCommand	Sampler.MDMove=0,237000	CD new artificial idle volume
	SamplerModule.SamplerModule_Service._SendCommand	Sampler.UdpWait=5000	
	SamplerModule.SamplerModule_Service._SendCommand	Sampler.Valve=3	Valve Compress/Decompress/Draw
	SamplerModule.SamplerModule_Service._SendCommand	Sampler.MDMove=0,251000	CD Decompress
	SamplerModule.SamplerModule_Service._SendCommand	Sampler.Valve=1	Valve Bypass
	SamplerModule.SamplerModule_Service._SendCommand	Sampler.MDMove=0,248500	CD move to draw position - backlash compensation
	SamplerModule.SamplerModule_Service._SendCommand	Sampler.MDMove=1,248500	MD move to draw position - backlash compensation
	SamplerModule.SamplerModule_Service._SendCommand	Sampler.MDMove=0,256250	CD turn over to MD drive move out of the way
	SamplerModule.SamplerModule_Service._SendCommand	Sampler.MDMove=1,249000	MD move to draw position
	SamplerModule.SamplerModule_Service._SendCommand	Sampler.Valve=3	Valve Compress/Decompress/Draw
	SamplerModule.SamplerModule_Service._SendCommand	Sampler.CabinFan=0	Turns the cabin fan off during injection as is done in normal injections
	SamplerModule.SamplerModule_Service._SendCommand	Sampler.GotoPosition=0x010001	go to vial SR:1
	SamplerModule.SamplerModule_Service._SendCommand	Sampler.MDMove=1,252000	MD aspirate
	SamplerModule.SamplerModule_Service._SendCommand	Sampler.UdpWait=3000	Wait after draw
	SamplerModule.SamplerModule_Service._SendCommand	Sampler.GotoPosition=0	go to needle seat
	SamplerModule.SamplerModule_Service._SendCommand	Sampler.CabinFan=1	Turns the cabin fan back on after injection as is done in normal injections
	SamplerModule.SamplerModule_Service._SendCommand	Sampler.MDMove=0,237000	CD precompress
	SamplerModule.SamplerModule_Service._SendCommand	Sampler.Valve=2	Inject
	SamplerModule.SamplerModule_Service._SendCommand	Sampler.UdpEnd	
0.000	Equilibration		
	UV.Autozero		
0.000	InjectPreparation		
	Wait	UV.Ready and Pump.Ready and ColumnComp.Ready and Sampler.Ready	
0.000	StartRun		
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
	SamplerModule.SamplerModule_Service._SendCommand	Sampler.UdpExecute	Execute the udp
If		SamplerModule.TableIndexerMode.Signal>0	
0.800	    ColumnComp.CC_Temp.AcqOff		
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
	    Protocol	Indexer-Fehler. Bitte Motor des Drehtellers austauschen und den defekten Motor an R&D übergeben.	
	    System.AbortQueue		
Else			
End If			
0.900	Log	Sampler_Service.MeteringPos	
	SamplerModule.SamplerModule_Service._SendCommand	CommandString="Sampler.CompressVol="	
	SamplerModule.SamplerModule_Service._SendCommand	CommandString="Sampler.CompressPos="	
	SamplerModule.SamplerModule_Service._SendCommand	CommandString="Sampler.DecompressVol="	
2.500	StopRun		
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
2.500	PostRun		
	End		
```

<a id="m-vas-foq-vasc-cooled-temp-cooling-performance-bi"></a>
## M-VAS-FOQ-VASC-COOLED-TEMP-COOLING-PERFORMANCE-BI: FOQ_VASC_Cooled_Temp_Cooling_Performance_BI

Source CMBX: `9318349.cmbx`  
Decoded flow SHA-256: `d67dd1c78face1f7ab7a8194e1b4c0dca7464b3a82bd2b142f07b5de81b834f0`  
Decoded rows: `86`

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
0.000	StartRun		
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
If		SamplerModule.TableIndexerMode.Signal>0	
0.040	    SamplerModule.Temperature_Air.AcqOff		
	    SamplerModule.Temperature_RightSink.AcqOff		
	    SamplerModule.Temperature_LeftSink.AcqOff		
	    SamplerModule.Temperature_AmbientSink.AcqOff		
	    SamplerModule.Temperature_AmbientAir.AcqOff		
	    PumpModule.Pump.Pump_Pressure.AcqOff		
	    SamplerModule.TableIndexerMode.AcqOff		
	    Delay	1	
	    Protocol	Indexer-Fehler. Bitte Motor des Drehtellers austauschen und den defekten Motor an R&D übergeben.	
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
7.000			
Trigger		"T1",	
	    Condition	(Temperature_Air.Signal<Variables.GenericDouble0-10)	
	    TrueTime	1.00	
	    Delay	0.0	
	    Limit	1	
	    Hysteresis	0.0	
	    AllowImmediateExecution	No	
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
30.000	StopRun		
	SamplerModule.Temperature_Air.AcqOff		
	SamplerModule.Temperature_RightSink.AcqOff		
	SamplerModule.Temperature_LeftSink.AcqOff		
	SamplerModule.Temperature_AmbientSink.AcqOff		
	SamplerModule.Temperature_AmbientAir.AcqOff		
	PumpModule.Pump.Pump_Pressure.AcqOff		
	SamplerModule.TableIndexerMode.AcqOff		
30.000	PostRun		
	Delay	1	
	PumpModule.Pump.Flow.Nominal	0.600 [mL/min]	
	End		
```
