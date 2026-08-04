# Online Original TCC Method Script Collection

Online_KB_Status: CANDIDATE_FOR_WEB_VALIDATION  
Upload_Allowed: Validation only  
Build_Date: 2026-07-24  
Decoded sources: 64 device/method files  
Core FOQ sources: 42  
Stress-extension sources: 22  
Unique script bodies: 46

## Evidence Rules

These sections are regenerated from the golden VA/VC/VH TCC CMBX packages and the VH stress-test package using the current embedded-method decoder. Identical device variants are stored once and list all applicable devices. Sections marked `VH-STRESS` are experimental execution evidence, not an FOQ acceptance contract. This file is source evidence; interpretation belongs in `03_METHOD_SUMMARIES.md`.

## Self Index

| Stable ID | CM method | Device evidence | Sequence source | Rows | Hash | Section |
|---|---|---|---|---:|---|---|
| `M-TCC-ASYNCHRON1` | `Asynchron1` | VH-STRESS | VH-STRESS:Stress_VH_DVT013_20260529 | 72 | `608541c76729` | [Open](#m-tcc-asynchron1) |
| `M-TCC-ASYNCHRON10` | `Asynchron10` | VH-STRESS | VH-STRESS:Stress_VH_DVT013_20260529 | 72 | `270cd3b79334` | [Open](#m-tcc-asynchron10) |
| `M-TCC-ASYNCHRON8` | `Asynchron8` | VH-STRESS | VH-STRESS:Stress_VH_DVT013_20260529 | 72 | `ae0940789771` | [Open](#m-tcc-asynchron8) |
| `M-TCC-ASYNCHRON8-5` | `Asynchron8_5` | VH-STRESS | VH-STRESS:Stress_VH_DVT013_20260529 | 72 | `38e37f8bb661` | [Open](#m-tcc-asynchron8-5) |
| `M-TCC-ASYNCHRON9-5` | `Asynchron9_5` | VH-STRESS | VH-STRESS:Stress_VH_DVT013_20260529 | 72 | `891ec9a14eda` | [Open](#m-tcc-asynchron9-5) |
| `M-TCC-BURNIN-VA` | `BURNIN` | VA | VA:0000003 | 144 | `978fb12b423d` | [Open](#m-tcc-burnin-va) |
| `M-TCC-BURNIN-VCVH` | `BURNIN` | VC/VH | VC:3000004, VH:6000001 | 144 | `da3a4c81183f` | [Open](#m-tcc-burnin-vcvh) |
| `M-TCC-ERRORLOG-VA` | `CHECKERRORLOG` | VA | VA:0000003 | 8 | `0bd6836bc0b2` | [Open](#m-tcc-errorlog-va) |
| `M-TCC-ERRORLOG-VCVH` | `CHECKERRORLOG` | VC/VH | VC:3000004, VH:6000001 | 14 | `7aa667b8c700` | [Open](#m-tcc-errorlog-vcvh) |
| `M-TCC-COLUMN-ID` | `ColumnID` | VA/VC/VH | VA:0000003, VC:3000004, VH:6000001 | 58 | `0bb7903cc203` | [Open](#m-tcc-column-id) |
| `M-TCC-FACTORY` | `FACTORYDEFAULT` | VA/VC/VH | VA:0000003, VC:3000004, VH:6000001 | 41 | `9285f264d9a3` | [Open](#m-tcc-factory) |
| `M-TCC-LEAK-VA` | `LIQUID LEAK` | VA | VA:0000003 | 133 | `3401a5ccf28a` | [Open](#m-tcc-leak-va) |
| `M-TCC-LEAK-VCVH` | `LIQUID LEAK` | VC/VH | VC:3000004, VH:6000001 | 133 | `7c12001ab1b1` | [Open](#m-tcc-leak-vcvh) |
| `M-TCC-PREHEATER` | `PREHEATER` | VA/VC/VH | VA:0000003, VC:3000004, VH:6000001 | 218 | `97839fca874f` | [Open](#m-tcc-preheater) |
| `M-TCC-SERVICE` | `QUALIFICATION_SERVICE_DONE` | VA/VC/VH | VA:0000003, VC:3000004, VH:6000001 | 9 | `12f1c16ded7c` | [Open](#m-tcc-service) |
| `M-TCC-STRESS-TEST` | `stress test` | VH-STRESS | VH-STRESS:Stress_VH_DVT013_20260529 | 130 | `693b36a7ff03` | [Open](#m-tcc-stress-test) |
| `M-TCC-STRESS-TEST-5S` | `stress test_5s` | VH-STRESS | VH-STRESS:Stress_VH_DVT013_20260529 | 130 | `246c93888c12` | [Open](#m-tcc-stress-test-5s) |
| `M-TCC-STRESS-TEST-5S-PREHEATER-BOX-PCC40C` | `Stress test_5s_Preheater Box_pcc40c` | VH-STRESS | VH-STRESS:Stress_VH_DVT013_20260529 | 131 | `b94af4c4696d` | [Open](#m-tcc-stress-test-5s-preheater-box-pcc40c) |
| `M-TCC-STRESS-TEST-5S-PREHEATER-BOX-PCC60C` | `Stress test_5s_Preheater Box_pcc60c` | VH-STRESS | VH-STRESS:Stress_VH_DVT013_20260529 | 131 | `827cd90fc63f` | [Open](#m-tcc-stress-test-5s-preheater-box-pcc60c) |
| `M-TCC-STRESS-TEST-5S-PREHEATER-BOX-PCC70C` | `Stress test_5s_Preheater Box_pcc70c` | VH-STRESS | VH-STRESS:Stress_VH_DVT013_20260529 | 131 | `5e48889900b4` | [Open](#m-tcc-stress-test-5s-preheater-box-pcc70c) |
| `M-TCC-STRESS-TEST-5S-PREHEATER-BOX-PCC-OFF` | `Stress test_5s_Preheater Box_pcc_off` | VH-STRESS | VH-STRESS:Stress_VH_DVT013_20260529 | 125 | `c0014697d046` | [Open](#m-tcc-stress-test-5s-preheater-box-pcc-off) |
| `M-TCC-STRESS-TEST-5S-REALPREHEATER-PCC-OFF` | `Stress test_5s_RealPreheater_pcc_off` | VH-STRESS | VH-STRESS:Stress_VH_DVT013_20260529 | 132 | `c3e9366b033d` | [Open](#m-tcc-stress-test-5s-realpreheater-pcc-off) |
| `M-TCC-STRESS-TEST-5S-REALPREHEATER-PCC-OFF-10MIN-EQUIBRATION` | `Stress test_5s_RealPreheater_pcc_off_10min equibration` | VH-STRESS | VH-STRESS:Stress_VH_DVT013_20260529 | 131 | `a8ae0bbbfb0e` | [Open](#m-tcc-stress-test-5s-realpreheater-pcc-off-10min-equibration) |
| `M-TCC-STRESS-TEST-5S-REALPREHEATER-PCC-OFF-NO-EQUIBRATION` | `Stress test_5s_RealPreheater_pcc_off_no equibration` | VH-STRESS | VH-STRESS:Stress_VH_DVT013_20260529 | 126 | `86bf99661307` | [Open](#m-tcc-stress-test-5s-realpreheater-pcc-off-no-equibration) |
| `M-TCC-STRESS-TEST-5S-REALPREHEATER-PCC-ON` | `Stress test_5s_RealPreheater_pcc_on` | VH-STRESS | VH-STRESS:Stress_VH_DVT013_20260529 | 133 | `66f0d5788d89` | [Open](#m-tcc-stress-test-5s-realpreheater-pcc-on) |
| `M-TCC-STRESS-TEST-5S-REALPREHEATER-PCC-ON-10MIN-EQUIBRATION` | `Stress test_5s_RealPreheater_pcc_ON_10min equibration` | VH-STRESS | VH-STRESS:Stress_VH_DVT013_20260529 | 132 | `080841adbf78` | [Open](#m-tcc-stress-test-5s-realpreheater-pcc-on-10min-equibration) |
| `M-TCC-STRESS-TEST-TEST` | `stress test_test` | VH-STRESS | VH-STRESS:Stress_VH_DVT013_20260529 | 130 | `9f58389f3b72` | [Open](#m-tcc-stress-test-test) |
| `M-TCC-SYNCHRON1` | `Synchron1` | VH-STRESS | VH-STRESS:Stress_VH_DVT013_20260529 | 72 | `3f8b9ca20d6c` | [Open](#m-tcc-synchron1) |
| `M-TCC-SYNCHRON10` | `Synchron10` | VH-STRESS | VH-STRESS:Stress_VH_DVT013_20260529 | 72 | `498ffee2d8fa` | [Open](#m-tcc-synchron10) |
| `M-TCC-SYNCHRON8` | `Synchron8` | VH-STRESS | VH-STRESS:Stress_VH_DVT013_20260529 | 89 | `b07b5885f11e` | [Open](#m-tcc-synchron8) |
| `M-TCC-SYNCHRON8-5` | `Synchron8_5` | VH-STRESS | VH-STRESS:Stress_VH_DVT013_20260529 | 72 | `9736ca33509d` | [Open](#m-tcc-synchron8-5) |
| `M-TCC-SYNCHRON9-5` | `Synchron9_5` | VH-STRESS | VH-STRESS:Stress_VH_DVT013_20260529 | 72 | `5c445a5bde56` | [Open](#m-tcc-synchron9-5) |
| `M-TCC-HEAT-COOL-VA` | `TEMP_HEAT_UP_DOWN_20_50_20` | VA | VA:0000003 | 170 | `3a1cb1d6bbcf` | [Open](#m-tcc-heat-cool-va) |
| `M-TCC-HEAT-COOL-VCVH` | `TEMP_HEAT_UP_DOWN_20_50_20` | VC/VH | VC:3000004, VH:6000001 | 170 | `b4a39fc89cc7` | [Open](#m-tcc-heat-cool-vcvh) |
| `M-TCC-ACCURACY-VA` | `TEMPERATURE_ACCURACY` | VA | VA:0000003 | 261 | `241e598a758a` | [Open](#m-tcc-accuracy-va) |
| `M-TCC-ACCURACY-VCVH` | `TEMPERATURE_ACCURACY` | VC/VH | VC:3000004, VH:6000001 | 261 | `1d4d55709938` | [Open](#m-tcc-accuracy-vcvh) |
| `M-TCC-CALIBRATION-VA` | `TEMPERATURE_CALIBRATION` | VA | VA:0000003 | 466 | `8856e261f44d` | [Open](#m-tcc-calibration-va) |
| `M-TCC-CALIBRATION-VCVH` | `TEMPERATURE_CALIBRATION` | VC/VH | VC:3000004, VH:6000001 | 466 | `eec8f62b563d` | [Open](#m-tcc-calibration-vcvh) |
| `M-TCC-PRECISION` | `TEMPERATURE_PRECISION` | VA | VA:0000003 | 124 | `9d7697955adb` | [Open](#m-tcc-precision) |
| `M-TCC-PRECISION-FAN` | `TEMPERATURE_PRECISION_AND_FAN` | VC/VH | VC:3000004, VH:6000001 | 135 | `5c8a1bd77a29` | [Open](#m-tcc-precision-fan) |
| `M-TCC-STABILITY-VA` | `TEMPERATURE_STABILITY_70_C` | VA | VA:0000003 | 97 | `cb7c2cbbb4b9` | [Open](#m-tcc-stability-va) |
| `M-TCC-STABILITY-VCVH` | `TEMPERATURE_STABILITY_70_C` | VC/VH | VC:3000004, VH:6000001 | 97 | `2b9d3793ed65` | [Open](#m-tcc-stability-vcvh) |
| `M-TCC-STABILITY-PCC-VA` | `TEMPERATURE_STABILITY_AND_PCC_70_H` | VA | VA:0000003 | 139 | `c463487c272a` | [Open](#m-tcc-stability-pcc-va) |
| `M-TCC-STABILITY-PCC-VCVH` | `TEMPERATURE_STABILITY_AND_PCC_70_H` | VC/VH | VC:3000004, VH:6000001 | 139 | `c996f3cd0b20` | [Open](#m-tcc-stability-pcc-vcvh) |
| `M-TCC-VALVES-VA` | `VALVES` | VA | VA:0000003 | 42 | `33907b3d7960` | [Open](#m-tcc-valves-va) |
| `M-TCC-VALVES-VCVH` | `VALVES` | VC/VH | VC:3000004, VH:6000001 | 50 | `8deefe03c7e3` | [Open](#m-tcc-valves-vcvh) |

<a id="m-tcc-asynchron1"></a>
## M-TCC-ASYNCHRON1: Asynchron1

Applicable device evidence: **VH-STRESS**  
Source sequence(s): `VH-STRESS:Stress_VH_DVT013_20260529`  
Source SHA-256: `608541c7672997a5adc630c8b6f1328e2f2d924074bdf50bc2a9f39a99822e3c`  
Decoded flow rows: `72`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	ColumnComp.CC.TempCtrl	On	
	ColumnComp.CC.Temperature.Nominal	30.0 [°C]	
	ColumnComp.CC.Temperature.LowerLimit	5.0 [°C]	
	ColumnComp.CC.Temperature.UpperLimit	85 [°C]	
	ColumnComp.CC.EquilibrationTime	0.5 [min]	
	ColumnComp.CC.ReadyTempDelta	0.5 [°C]	
	PumpModule.Pump.%A.Equate	Water	
	PumpModule.Pump.Pressure.LowerLimit	0 [bar]	
	PumpModule.Pump.Pressure.UpperLimit	660 [bar]	
	PumpModule.Pump.MaximumFlowRampUp	Infinite	
	PumpModule.Pump.MaximumFlowRampDown	Infinite	
	PumpModule.Pump.Pump_Pressure.UseFilter	Off	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	1_2	
	ColumnComp.LowerValve.CurrentPosition	6_1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Variables.GenericBool1	0	
	Variables.GenericBool2	0	
	Variables.GenericFloat1	0	
0.000	Equilibration		
	PumpModule.Pump.Flow.Nominal	1.00000 [ml/min]	
	PumpModule.Pump.Curve	5	
0.000	InjectPreparation		
	Wait	ColumnComp.CC.TempReady AND PumpModule.Pump.Ready, Run=Hold	
0.000	StartRun		
	PumpModule.Pump.Pump_Pressure.AcqOn		
	ColumnComp.CC_Temp.AcqOn		
	VirtualChannel	PumpPressureVirtual, PumpModule.Pump.Pump_Pressure.Signal, Type=Digital, Unit="bar", Evaluate=Yes	
	Thermometer.Lab_Temperature.AcqOn		
Trigger		"Ping",	
	    Condition	Variables.GenericBool1=1 AND System.Retention>Variables.GenericFloat1	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.5	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	6_1	
	ColumnComp.LowerValve.CurrentPosition	1_2	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Delay	1	
	Variables.GenericBool1	0	
	Delay	1	
	Variables.GenericBool2	1	
End Trigger			
Trigger		"Pong",	
	    Condition	Variables.GenericBool2=1 AND System.Retention>Variables.GenericFloat1	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.5	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	1_2	
	ColumnComp.LowerValve.CurrentPosition	6_1	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Delay	1	
	Variables.GenericBool1	1	
	Delay	1	
	Variables.GenericBool2	0	
End Trigger			
0.000	Run	Duration = 20.500 [min]	
	PumpModule.Pump.Flow.Nominal	1.00000 [ml/min]	
	PumpModule.Pump.Curve	5	
	Variables.GenericBool1	1	
20.500	StopRun		
	Variables.GenericBool1	0	
	Variables.GenericBool2	0	
	PumpModule.Pump.Flow.Nominal	1.00000 [ml/min]	
	PumpModule.Pump.Curve	5	
	PumpModule.Pump.Flow.Nominal	0.000000 [ml/min]	
	PumpModule.Pump.Curve	5	
	PumpModule.Pump.Pump_Pressure.AcqOff		
	ColumnComp.CC_Temp.AcqOff		
	Thermometer.Lab_Temperature.AcqOff		
	End		
```

<a id="m-tcc-asynchron10"></a>
## M-TCC-ASYNCHRON10: Asynchron10

Applicable device evidence: **VH-STRESS**  
Source sequence(s): `VH-STRESS:Stress_VH_DVT013_20260529`  
Source SHA-256: `270cd3b79334c36801421673563a6481d332d4133d63848fa36ef8d86055d048`  
Decoded flow rows: `72`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	ColumnComp.CC.TempCtrl	On	
	ColumnComp.CC.Temperature.Nominal	30.0 [°C]	
	ColumnComp.CC.Temperature.LowerLimit	5.0 [°C]	
	ColumnComp.CC.Temperature.UpperLimit	85 [°C]	
	ColumnComp.CC.EquilibrationTime	0.5 [min]	
	ColumnComp.CC.ReadyTempDelta	0.5 [°C]	
	PumpModule.Pump.%A.Equate	Water	
	PumpModule.Pump.Pressure.LowerLimit	0 [bar]	
	PumpModule.Pump.Pressure.UpperLimit	660 [bar]	
	PumpModule.Pump.MaximumFlowRampUp	Infinite	
	PumpModule.Pump.MaximumFlowRampDown	Infinite	
	PumpModule.Pump.Pump_Pressure.UseFilter	Off	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	1_2	
	ColumnComp.LowerValve.CurrentPosition	6_1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Variables.GenericBool1	0	
	Variables.GenericBool2	0	
	Variables.GenericFloat1	0	
0.000	Equilibration		
	PumpModule.Pump.Flow.Nominal	10 [ml/min]	
	PumpModule.Pump.Curve	5	
0.000	InjectPreparation		
	Wait	ColumnComp.CC.TempReady AND PumpModule.Pump.Ready, Run=Hold	
0.000	StartRun		
	PumpModule.Pump.Pump_Pressure.AcqOn		
	ColumnComp.CC_Temp.AcqOn		
	VirtualChannel	PumpPressureVirtual, PumpModule.Pump.Pump_Pressure.Signal, Type=Digital, Unit="bar", Evaluate=Yes	
	Thermometer.Lab_Temperature.AcqOn		
Trigger		"Ping",	
	    Condition	Variables.GenericBool1=1 AND System.Retention>Variables.GenericFloat1	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.5	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	6_1	
	ColumnComp.LowerValve.CurrentPosition	1_2	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Delay	1	
	Variables.GenericBool1	0	
	Delay	1	
	Variables.GenericBool2	1	
End Trigger			
Trigger		"Pong",	
	    Condition	Variables.GenericBool2=1 AND System.Retention>Variables.GenericFloat1	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.5	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	1_2	
	ColumnComp.LowerValve.CurrentPosition	6_1	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Delay	1	
	Variables.GenericBool1	1	
	Delay	1	
	Variables.GenericBool2	0	
End Trigger			
0.000	Run	Duration = 20.500 [min]	
	PumpModule.Pump.Flow.Nominal	10 [ml/min]	
	PumpModule.Pump.Curve	5	
	Variables.GenericBool1	1	
20.500	StopRun		
	Variables.GenericBool1	0	
	Variables.GenericBool2	0	
	PumpModule.Pump.Flow.Nominal	10 [ml/min]	
	PumpModule.Pump.Curve	5	
	PumpModule.Pump.Flow.Nominal	0.000000 [ml/min]	
	PumpModule.Pump.Curve	5	
	PumpModule.Pump.Pump_Pressure.AcqOff		
	ColumnComp.CC_Temp.AcqOff		
	Thermometer.Lab_Temperature.AcqOff		
	End		
```

<a id="m-tcc-asynchron8"></a>
## M-TCC-ASYNCHRON8: Asynchron8

Applicable device evidence: **VH-STRESS**  
Source sequence(s): `VH-STRESS:Stress_VH_DVT013_20260529`  
Source SHA-256: `ae0940789771da1914bb15f133969248cfa0f4a2f111f7c531b40fe0b42ba50f`  
Decoded flow rows: `72`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	ColumnComp.CC.TempCtrl	On	
	ColumnComp.CC.Temperature.Nominal	30.0 [°C]	
	ColumnComp.CC.Temperature.LowerLimit	5.0 [°C]	
	ColumnComp.CC.Temperature.UpperLimit	85 [°C]	
	ColumnComp.CC.EquilibrationTime	0.5 [min]	
	ColumnComp.CC.ReadyTempDelta	0.5 [°C]	
	PumpModule.Pump.%A.Equate	Water	
	PumpModule.Pump.Pressure.LowerLimit	0 [bar]	
	PumpModule.Pump.Pressure.UpperLimit	660 [bar]	
	PumpModule.Pump.MaximumFlowRampUp	Infinite	
	PumpModule.Pump.MaximumFlowRampDown	Infinite	
	PumpModule.Pump.Pump_Pressure.UseFilter	Off	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	1_2	
	ColumnComp.LowerValve.CurrentPosition	6_1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Variables.GenericBool1	0	
	Variables.GenericBool2	0	
	Variables.GenericFloat1	0	
0.000	Equilibration		
	PumpModule.Pump.Flow.Nominal	8.00000 [ml/min]	
	PumpModule.Pump.Curve	5	
0.000	InjectPreparation		
	Wait	ColumnComp.CC.TempReady AND PumpModule.Pump.Ready, Run=Hold	
0.000	StartRun		
	PumpModule.Pump.Pump_Pressure.AcqOn		
	ColumnComp.CC_Temp.AcqOn		
	VirtualChannel	PumpPressureVirtual, PumpModule.Pump.Pump_Pressure.Signal, Type=Digital, Unit="bar", Evaluate=Yes	
	Thermometer.Environment_Temperature.AcqOn		
Trigger		"Ping",	
	    Condition	Variables.GenericBool1=1 AND System.Retention>Variables.GenericFloat1	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.5	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	6_1	
	ColumnComp.LowerValve.CurrentPosition	1_2	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Delay	1	
	Variables.GenericBool1	0	
	Delay	1	
	Variables.GenericBool2	1	
End Trigger			
Trigger		"Pong",	
	    Condition	Variables.GenericBool2=1 AND System.Retention>Variables.GenericFloat1	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.5	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	1_2	
	ColumnComp.LowerValve.CurrentPosition	6_1	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Delay	1	
	Variables.GenericBool1	1	
	Delay	1	
	Variables.GenericBool2	0	
End Trigger			
0.000	Run	Duration = 20.500 [min]	
	PumpModule.Pump.Flow.Nominal	8.00000 [ml/min]	
	PumpModule.Pump.Curve	5	
	Variables.GenericBool1	1	
20.500	StopRun		
	Variables.GenericBool1	0	
	Variables.GenericBool2	0	
	PumpModule.Pump.Flow.Nominal	8.00000 [ml/min]	
	PumpModule.Pump.Curve	5	
	PumpModule.Pump.Flow.Nominal	0.000000 [ml/min]	
	PumpModule.Pump.Curve	5	
	PumpModule.Pump.Pump_Pressure.AcqOff		
	ColumnComp.CC_Temp.AcqOff		
	Thermometer.Environment_Temperature.AcqOff		
	End		
```

<a id="m-tcc-asynchron8-5"></a>
## M-TCC-ASYNCHRON8-5: Asynchron8_5

Applicable device evidence: **VH-STRESS**  
Source sequence(s): `VH-STRESS:Stress_VH_DVT013_20260529`  
Source SHA-256: `38e37f8bb661edab5c5a74af5f8e4229c0db59dc3cf5cc8fa9ca6ad21a68dc13`  
Decoded flow rows: `72`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	ColumnComp.CC.TempCtrl	On	
	ColumnComp.CC.Temperature.Nominal	30.0 [°C]	
	ColumnComp.CC.Temperature.LowerLimit	5.0 [°C]	
	ColumnComp.CC.Temperature.UpperLimit	85 [°C]	
	ColumnComp.CC.EquilibrationTime	0.5 [min]	
	ColumnComp.CC.ReadyTempDelta	0.5 [°C]	
	PumpModule.Pump.%A.Equate	Water	
	PumpModule.Pump.Pressure.LowerLimit	0 [bar]	
	PumpModule.Pump.Pressure.UpperLimit	660 [bar]	
	PumpModule.Pump.MaximumFlowRampUp	Infinite	
	PumpModule.Pump.MaximumFlowRampDown	Infinite	
	PumpModule.Pump.Pump_Pressure.UseFilter	Off	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	1_2	
	ColumnComp.LowerValve.CurrentPosition	6_1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Variables.GenericBool1	0	
	Variables.GenericBool2	0	
	Variables.GenericFloat1	0	
0.000	Equilibration		
	PumpModule.Pump.Flow.Nominal	8.500000 [ml/min]	
	PumpModule.Pump.Curve	5	
0.000	InjectPreparation		
	Wait	ColumnComp.CC.TempReady AND PumpModule.Pump.Ready, Run=Hold	
0.000	StartRun		
	PumpModule.Pump.Pump_Pressure.AcqOn		
	ColumnComp.CC_Temp.AcqOn		
	VirtualChannel	PumpPressureVirtual, PumpModule.Pump.Pump_Pressure.Signal, Type=Digital, Unit="bar", Evaluate=Yes	
	Thermometer.Lab_Temperature.AcqOn		
Trigger		"Ping",	
	    Condition	Variables.GenericBool1=1 AND System.Retention>Variables.GenericFloat1	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.5	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	6_1	
	ColumnComp.LowerValve.CurrentPosition	1_2	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Delay	1	
	Variables.GenericBool1	0	
	Delay	1	
	Variables.GenericBool2	1	
End Trigger			
Trigger		"Pong",	
	    Condition	Variables.GenericBool2=1 AND System.Retention>Variables.GenericFloat1	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.5	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	1_2	
	ColumnComp.LowerValve.CurrentPosition	6_1	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Delay	1	
	Variables.GenericBool1	1	
	Delay	1	
	Variables.GenericBool2	0	
End Trigger			
0.000	Run	Duration = 20.500 [min]	
	PumpModule.Pump.Flow.Nominal	8.500000 [ml/min]	
	PumpModule.Pump.Curve	5	
	Variables.GenericBool1	1	
20.500	StopRun		
	Variables.GenericBool1	0	
	Variables.GenericBool2	0	
	PumpModule.Pump.Flow.Nominal	8.500000 [ml/min]	
	PumpModule.Pump.Curve	5	
	PumpModule.Pump.Flow.Nominal	0.000000 [ml/min]	
	PumpModule.Pump.Curve	5	
	PumpModule.Pump.Pump_Pressure.AcqOff		
	ColumnComp.CC_Temp.AcqOff		
	Thermometer.Lab_Temperature.AcqOff		
	End		
```

<a id="m-tcc-asynchron9-5"></a>
## M-TCC-ASYNCHRON9-5: Asynchron9_5

Applicable device evidence: **VH-STRESS**  
Source sequence(s): `VH-STRESS:Stress_VH_DVT013_20260529`  
Source SHA-256: `891ec9a14eda52951e0bca425132f354780303cfb866efbb1302141ba288fa44`  
Decoded flow rows: `72`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	ColumnComp.CC.TempCtrl	On	
	ColumnComp.CC.Temperature.Nominal	30.0 [°C]	
	ColumnComp.CC.Temperature.LowerLimit	5.0 [°C]	
	ColumnComp.CC.Temperature.UpperLimit	85 [°C]	
	ColumnComp.CC.EquilibrationTime	0.5 [min]	
	ColumnComp.CC.ReadyTempDelta	0.5 [°C]	
	PumpModule.Pump.%A.Equate	Water	
	PumpModule.Pump.Pressure.LowerLimit	0 [bar]	
	PumpModule.Pump.Pressure.UpperLimit	660 [bar]	
	PumpModule.Pump.MaximumFlowRampUp	Infinite	
	PumpModule.Pump.MaximumFlowRampDown	Infinite	
	PumpModule.Pump.Pump_Pressure.UseFilter	Off	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	1_2	
	ColumnComp.LowerValve.CurrentPosition	6_1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Variables.GenericBool1	0	
	Variables.GenericBool2	0	
	Variables.GenericFloat1	0	
0.000	Equilibration		
	PumpModule.Pump.Flow.Nominal	9.5 [ml/min]	
	PumpModule.Pump.Curve	5	
0.000	InjectPreparation		
	Wait	ColumnComp.CC.TempReady AND PumpModule.Pump.Ready, Run=Hold	
0.000	StartRun		
	PumpModule.Pump.Pump_Pressure.AcqOn		
	ColumnComp.CC_Temp.AcqOn		
	VirtualChannel	PumpPressureVirtual, PumpModule.Pump.Pump_Pressure.Signal, Type=Digital, Unit="bar", Evaluate=Yes	
	Thermometer.Lab_Temperature.AcqOn		
Trigger		"Ping",	
	    Condition	Variables.GenericBool1=1 AND System.Retention>Variables.GenericFloat1	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.5	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	6_1	
	ColumnComp.LowerValve.CurrentPosition	1_2	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Delay	1	
	Variables.GenericBool1	0	
	Delay	1	
	Variables.GenericBool2	1	
End Trigger			
Trigger		"Pong",	
	    Condition	Variables.GenericBool2=1 AND System.Retention>Variables.GenericFloat1	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.5	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	1_2	
	ColumnComp.LowerValve.CurrentPosition	6_1	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Delay	1	
	Variables.GenericBool1	1	
	Delay	1	
	Variables.GenericBool2	0	
End Trigger			
0.000	Run	Duration = 20.500 [min]	
	PumpModule.Pump.Flow.Nominal	9.5 [ml/min]	
	PumpModule.Pump.Curve	5	
	Variables.GenericBool1	1	
20.500	StopRun		
	Variables.GenericBool1	0	
	Variables.GenericBool2	0	
	PumpModule.Pump.Flow.Nominal	9.5 [ml/min]	
	PumpModule.Pump.Curve	5	
	PumpModule.Pump.Flow.Nominal	0.000000 [ml/min]	
	PumpModule.Pump.Curve	5	
	PumpModule.Pump.Pump_Pressure.AcqOff		
	ColumnComp.CC_Temp.AcqOff		
	Thermometer.Lab_Temperature.AcqOff		
	End		
```

<a id="m-tcc-burnin-va"></a>
## M-TCC-BURNIN-VA: BURNIN

Applicable device evidence: **VA**  
Source sequence(s): `VA:0000003`  
Source SHA-256: `978fb12b423d205af4d04935318c87824d979d37e5d516b680cc8d429d199f79`  
Decoded flow rows: `144`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	=========================================================================================		
	IM to condition the temperature sensor and to test the Peltier aging of the Vanquish VH-C10-A, VC-C10-A and VA-C10-A		
	=========================================================================================		
	HPLC-System:		
	-----------		
	VH-C10-A, VC-C10-A or VA-C10-A		
-0.700	Equilibration	Duration = 0.700 [min]	
	=========================================================================================		
	Parameters valid for the whole test.		
	=========================================================================================		
	If the difference between nominal and actual temperature is larger than ReadyTempDelta, the VTCC is not ready.		
	ColumnComp.CC.ReadyTempDelta	3.0 [°C]	
	The Ready property will become Ready only if the difference between the setpoint temperature and the nominal temperature will not exceed the ReadyTempDelta for the  time interval specified by EquilibrationTime.		
	ColumnComp.CC.EquilibrationTime	0.5	
	The VTCC adjusts the temperature only, if TempCtrl is set to ON for each single unit.		
	ColumnComp.CC.TempCtrl	On	
If		ColumnComp.ModelNo="VH-C10-A"	
	    ColumnComp.CmdString	Cmd="PCC.TempCtrl=0"	String necessary, because otherwise a way more complicated solution would be needed for using this IM for both CC types. Is equivalent to ColumnComp.PCC.TempCtrl=Off
Else			
End If			
	Thermostatting Mode		
	ColumnComp.CC.Mode	StillAir	
	Generic variables  for Triggers		
	Variables.GenericFloat1	0	
	Variable for minimum and maximum temperature		
If		ColumnComp.ModelNo="VH-C10-A"	
	    Variables.GenericDouble1	5.0	Minimum temperature for VH-C10-A
	    Variables.GenericDouble2	120.0	Maximum temperature for VH-C10-A                            [Val_FOQ_CM7_ekugelma_07-Jul-2020]: OK
Else If		ColumnComp.ModelNo="VC-C10-A" OR ColumnComp.ModelNo="VA-C10-A"	
	    Variables.GenericDouble1	5.0	Minimum temperature for VC-C10-A and VA-C10-A
	    Variables.GenericDouble2	85.0	Maximum temperature for VC-C10-A and VA-C10-A                       [Val_FOQ_CM7_ekugelma_07-Jul-2020]: OK
Else			
	    Message	Invalid ModelNo! Please reinspect in production!	
	    System.AbortQueue		
End If			
	=========================================================================================		
	Leak Sensor State deactivated to avoide alarms caused by condensation due to fast heat up and cool down during IM		
	=========================================================================================		
	ColumnComp.LiquidLeakSensor	Off	
	===================================================================================		
	Settings for all channels offered for the column compartment by the driver.		
	Also debug channels are aqcuired.		
	====================================================================================		
	Column commpartment		
	ColumnComp.CC_U_Temp_Actual.Data_Collection_Rate	20	
	ColumnComp.CC_L_Temp_Actual.Data_Collection_Rate	20	
	ColumnComp.CC_UCTL_TempRear_Actual.Data_Collection_Rate	20	
	ColumnComp.PWM_CCU_A.Data_Collection_Rate	20	
	ColumnComp.PWM_CCU_B.Data_Collection_Rate	20	
	ColumnComp.PWM_CCL_A.Data_Collection_Rate	20	
	ColumnComp.PWM_CCL_B.Data_Collection_Rate	20	
	ColumnComp.Fan_Rear_ActualRPM.Data_Collection_Rate	20	
	Leak Sensors		
	ColumnComp.LEDBoard_LeakDiff.Data_Collection_Rate	20	
	ColumnComp.LEDBoard_A13.Data_Collection_Rate	20	
	ColumnComp.LEDBoard_A14.Data_Collection_Rate	20	
	===================================================================================		
	Start Temperature		
	===================================================================================		
	ColumnComp.CC.Temperature.Nominal	15.0	
0.000	InjectPreparation		
	Wait	CC.TempReady	
0.000	StartRun		
	ColumnComp.CC_Temp.AcqOn		
	ColumnComp.CC_U_Temp_Actual.AcqOn		
	ColumnComp.CC_L_Temp_Actual.AcqOn		
	ColumnComp.CC_UCTL_TempRear_Actual.AcqOn		
	ColumnComp.PWM_CCU_A.AcqOn		
	ColumnComp.PWM_CCU_B.AcqOn		
	ColumnComp.PWM_CCL_A.AcqOn		
	ColumnComp.PWM_CCL_B.AcqOn		
	ColumnComp.Fan_Rear_ActualRPM.AcqOn		
	External measured temperatures		
	Thermometer1.ExtTemp_UpperCC.AcqOn		
	Thermometer1.ExtTemp_LowerCC.AcqOn		
	Thermometer.Environment_Temperature.AcqOn		
	Leak Sensor Evaluation		
	ColumnComp.LEDBoard_LeakDiff.AcqOn		
	ColumnComp.LEDBoard_A13.AcqOn		
	ColumnComp.LEDBoard_A14.AcqOn		
0.000	Run	Duration = 300.000 [min]	
0.100	ColumnComp.CC.Temperature.Nominal	Variables.GenericDouble2	
0.200			
Trigger		"T_Maximum",	
	    Condition	(CC.Temperature.Value>=(Variables.GenericDouble2-0.5)) AND (CC.Temperature.Nominal=Variables.GenericDouble2)	
	    Limit	2	
	    Hysteresis	5.0 [%]	
	    AllowImmediateExecution	No	
	ColumnComp.CC.Temperature.Nominal	Variables.GenericDouble1	
End Trigger			
Trigger		"T_Minimum",	
	    Condition	(CC.Temperature.Value<=(Variables.GenericDouble1+5.0)) AND (CC.Temperature.Nominal=Variables.GenericDouble1)	
	    Limit	2	
	    Hysteresis	5.0 [%]	
	    AllowImmediateExecution	No	
	ColumnComp.CC.Temperature.Nominal	Variables.GenericDouble2	
	Variables.GenericFloat1	Variables.GenericFloat1+1	
End Trigger			
Trigger		"HoldTemp",	
	    Condition	(Variables.GenericFloat1=2)	
	    TrueTime	1	
	    Limit	1	
	    Hysteresis	0	
	    AllowImmediateExecution	No	
	ColumnComp.CC.Temperature.Nominal	Variables.GenericDouble2	
	Delay	7200.0	
	Column commpartment		
	ColumnComp.CC_Temp.AcqOff		
	ColumnComp.CC_U_Temp_Actual.AcqOff		
	ColumnComp.CC_L_Temp_Actual.AcqOff		
	ColumnComp.CC_UCTL_TempRear_Actual.AcqOff		
	ColumnComp.PWM_CCU_A.AcqOff		
	ColumnComp.PWM_CCU_B.AcqOff		
	ColumnComp.PWM_CCL_A.AcqOff		
	ColumnComp.PWM_CCL_B.AcqOff		
	ColumnComp.Fan_Rear_ActualRPM.AcqOff		
	External measured temperatures		
	Thermometer1.ExtTemp_UpperCC.AcqOff		
	Thermometer1.ExtTemp_LowerCC.AcqOff		
	Thermometer.Environment_Temperature.AcqOff		
	Leak Sensor Evaluation		
	ColumnComp.LEDBoard_LeakDiff.AcqOff		
	ColumnComp.LEDBoard_A13.AcqOff		
	ColumnComp.LEDBoard_A14.AcqOff		
	End		
End Trigger			
	The following check ensures that the external thermometers are mounted properly and that they are configured correct in the instrument configuration manager (not in simmulation mode).		
	The queue is aborted automatically if the temperature of the external temperature sensors is not matching the temperature of the VTCC  withing T - 5 °C		
If		CC.Temperature.Value-Thermometer1.ExtTemp_LowerCC.Signal>5 OR CC.Temperature.Value-Thermometer1.ExtTemp_UpperCC>5	
3.000	    ColumnComp.CmdString	Cmd="LedBar.ForceColor=1"	
	    Message	***Temperature of at least one external thermometer is not increasing. Check for correct mounting of the sensors inside the VTCC and for correct configuration of the thermometers in the Instrument Configuration Manager. The queue will be aborted.***	
	    Delay	1	
	    ColumnComp.CmdString	Cmd="LedBar.ForceColor=0"	
	    Delay	1	
	    System.AbortQueue		
Else			
End If			
300.000	StopRun		
	ColumnComp.CC_Temp.AcqOff		
	ColumnComp.CC_U_Temp_Actual.AcqOff		
	ColumnComp.CC_L_Temp_Actual.AcqOff		
	ColumnComp.CC_UCTL_TempRear_Actual.AcqOff		
	ColumnComp.PWM_CCU_A.AcqOff		
	ColumnComp.PWM_CCU_B.AcqOff		
	ColumnComp.PWM_CCL_A.AcqOff		
	ColumnComp.PWM_CCL_B.AcqOff		
	ColumnComp.Fan_Rear_ActualRPM.AcqOff		
300.000	PostRun		
	External measured temperatures		
	Thermometer1.ExtTemp_UpperCC.AcqOff		
	Thermometer1.ExtTemp_LowerCC.AcqOff		
	Thermometer.Environment_Temperature.AcqOff		
	Leak Sensor Evaluation		
	ColumnComp.LEDBoard_LeakDiff.AcqOff		
	ColumnComp.LEDBoard_A13.AcqOff		
	ColumnComp.LEDBoard_A14.AcqOff		
	End		
```

<a id="m-tcc-burnin-vcvh"></a>
## M-TCC-BURNIN-VCVH: BURNIN

Applicable device evidence: **VC / VH**  
Source sequence(s): `VC:3000004, VH:6000001`  
Source SHA-256: `da3a4c81183f397207ec3be9fb2e879dbf512a01c182549d38657d867cb80f75`  
Decoded flow rows: `144`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	=========================================================================================		
	IM to condition the temperature sensor and to test the Peltier aging of the Vanquish VH-C10-A and VC-C10-A		
	=========================================================================================		
	HPLC-System:		
	-----------		
	VH-C10-A  or VC-C10-A		
-0.700	Equilibration	Duration = 0.700 [min]	
	=========================================================================================		
	Parameters valid for the whole test.		
	=========================================================================================		
	If the difference between nominal and actual temperature is larger than ReadyTempDelta, the VTCC is not ready.		
	ColumnComp.CC.ReadyTempDelta	3.0 [°C]	
	The Ready property will become Ready only if the difference between the setpoint temperature and the nominal temperature will not exceed the ReadyTempDelta for the  time interval specified by EquilibrationTime.		
	ColumnComp.CC.EquilibrationTime	0.5	
	The VTCC adjusts the temperature only, if TempCtrl is set to ON for each single unit.		
	ColumnComp.CC.TempCtrl	On	
If		ColumnComp.ModelNo="VH-C10-A"	
	    ColumnComp.CmdString	Cmd="PCC.TempCtrl=0"	String necessary, because otherwise a way more complicated solution would be needed for using this IM for both CC types. Is equivalent to ColumnComp.PCC.TempCtrl=Off
Else			
End If			
	Thermostatting Mode		
	ColumnComp.CC.Mode	StillAir	
	Generic variables  for Triggers		
	Variables.GenericFloat1	0	
	Variable for minimum and maximum temperature		
If		ColumnComp.ModelNo="VH-C10-A"	
	    Variables.GenericDouble1	5.0	Minimum temperature for VH-C10-A
	    Variables.GenericDouble2	120.0	Maximum temperature for VH-C10-A                            [Val_FOQ_CM7_ekugelma_07-Jul-2020]: OK
Else If		ColumnComp.ModelNo="VC-C10-A"	
	    Variables.GenericDouble1	5.0	Minimum temperature for VC-C10-A
	    Variables.GenericDouble2	85.0	Maximum temperature for VC-C10-A                        [Val_FOQ_CM7_ekugelma_07-Jul-2020]: OK
Else			
	    Message	Invalid ModelNo! Please reinspect in production!	
	    System.AbortQueue		
End If			
	=========================================================================================		
	Leak Sensor State deactivated to avoide alarms caused by condensation due to fast heat up and cool down during IM		
	=========================================================================================		
	ColumnComp.LiquidLeakSensor	Off	
	===================================================================================		
	Settings for all channels offered for the column compartment by the driver.		
	Also debug channels are aqcuired.		
	====================================================================================		
	Column commpartment		
	ColumnComp.CC_U_Temp_Actual.Data_Collection_Rate	20	
	ColumnComp.CC_L_Temp_Actual.Data_Collection_Rate	20	
	ColumnComp.CC_UCTL_TempRear_Actual.Data_Collection_Rate	20	
	ColumnComp.PWM_CCU_A.Data_Collection_Rate	20	
	ColumnComp.PWM_CCU_B.Data_Collection_Rate	20	
	ColumnComp.PWM_CCL_A.Data_Collection_Rate	20	
	ColumnComp.PWM_CCL_B.Data_Collection_Rate	20	
	ColumnComp.Fan_Rear_ActualRPM.Data_Collection_Rate	20	
	Leak Sensors		
	ColumnComp.LEDBoard_LeakDiff.Data_Collection_Rate	20	
	ColumnComp.LEDBoard_A13.Data_Collection_Rate	20	
	ColumnComp.LEDBoard_A14.Data_Collection_Rate	20	
	===================================================================================		
	Start Temperature		
	===================================================================================		
	ColumnComp.CC.Temperature.Nominal	15.0	
0.000	InjectPreparation		
	Wait	CC.TempReady	
0.000	StartRun		
	ColumnComp.CC_Temp.AcqOn		
	ColumnComp.CC_U_Temp_Actual.AcqOn		
	ColumnComp.CC_L_Temp_Actual.AcqOn		
	ColumnComp.CC_UCTL_TempRear_Actual.AcqOn		
	ColumnComp.PWM_CCU_A.AcqOn		
	ColumnComp.PWM_CCU_B.AcqOn		
	ColumnComp.PWM_CCL_A.AcqOn		
	ColumnComp.PWM_CCL_B.AcqOn		
	ColumnComp.Fan_Rear_ActualRPM.AcqOn		
	External measured temperatures		
	Thermometer1.ExtTemp_UpperCC.AcqOn		
	Thermometer1.ExtTemp_LowerCC.AcqOn		
	Thermometer.Environment_Temperature.AcqOn		
	Leak Sensor Evaluation		
	ColumnComp.LEDBoard_LeakDiff.AcqOn		
	ColumnComp.LEDBoard_A13.AcqOn		
	ColumnComp.LEDBoard_A14.AcqOn		
0.000	Run	Duration = 300.000 [min]	
0.100	ColumnComp.CC.Temperature.Nominal	Variables.GenericDouble2	
0.200			
Trigger		"T_Maximum",	
	    Condition	(CC.Temperature.Value>=(Variables.GenericDouble2-0.5)) AND (CC.Temperature.Nominal=Variables.GenericDouble2)	
	    Limit	2	
	    Hysteresis	5.0 [%]	
	    AllowImmediateExecution	No	
	ColumnComp.CC.Temperature.Nominal	Variables.GenericDouble1	
End Trigger			
Trigger		"T_Minimum",	
	    Condition	(CC.Temperature.Value<=(Variables.GenericDouble1+5.0)) AND (CC.Temperature.Nominal=Variables.GenericDouble1)	
	    Limit	2	
	    Hysteresis	5.0 [%]	
	    AllowImmediateExecution	No	
	ColumnComp.CC.Temperature.Nominal	Variables.GenericDouble2	
	Variables.GenericFloat1	Variables.GenericFloat1+1	
End Trigger			
Trigger		"HoldTemp",	
	    Condition	(Variables.GenericFloat1=2)	
	    TrueTime	1	
	    Limit	1	
	    Hysteresis	0	
	    AllowImmediateExecution	No	
	ColumnComp.CC.Temperature.Nominal	Variables.GenericDouble2	
	Delay	7200.0	
	Column commpartment		
	ColumnComp.CC_Temp.AcqOff		
	ColumnComp.CC_U_Temp_Actual.AcqOff		
	ColumnComp.CC_L_Temp_Actual.AcqOff		
	ColumnComp.CC_UCTL_TempRear_Actual.AcqOff		
	ColumnComp.PWM_CCU_A.AcqOff		
	ColumnComp.PWM_CCU_B.AcqOff		
	ColumnComp.PWM_CCL_A.AcqOff		
	ColumnComp.PWM_CCL_B.AcqOff		
	ColumnComp.Fan_Rear_ActualRPM.AcqOff		
	External measured temperatures		
	Thermometer1.ExtTemp_UpperCC.AcqOff		
	Thermometer1.ExtTemp_LowerCC.AcqOff		
	Thermometer.Environment_Temperature.AcqOff		
	Leak Sensor Evaluation		
	ColumnComp.LEDBoard_LeakDiff.AcqOff		
	ColumnComp.LEDBoard_A13.AcqOff		
	ColumnComp.LEDBoard_A14.AcqOff		
	End		
End Trigger			
	The following check ensures that the external thermometers are mounted properly and that they are configured correct in the instrument configuration manager (not in simmulation mode).		
	The queue is aborted automatically if the temperature of the external temperature sensors is not matching the temperature of the VTCC  withing T - 5 °C		
If		CC.Temperature.Value-Thermometer1.ExtTemp_LowerCC.Signal>5 OR CC.Temperature.Value-Thermometer1.ExtTemp_UpperCC>5	
3.000	    ColumnComp.CmdString	Cmd="LedBar.ForceColor=1"	
	    Message	***Temperature of at least one external thermometer is not increasing. Check for correct mounting of the sensors inside the VTCC and for correct configuration of the thermometers in the Instrument Configuration Manager. The queue will be aborted.***	
	    Delay	1	
	    ColumnComp.CmdString	Cmd="LedBar.ForceColor=0"	
	    Delay	1	
	    System.AbortQueue		
Else			
End If			
300.000	StopRun		
	ColumnComp.CC_Temp.AcqOff		
	ColumnComp.CC_U_Temp_Actual.AcqOff		
	ColumnComp.CC_L_Temp_Actual.AcqOff		
	ColumnComp.CC_UCTL_TempRear_Actual.AcqOff		
	ColumnComp.PWM_CCU_A.AcqOff		
	ColumnComp.PWM_CCU_B.AcqOff		
	ColumnComp.PWM_CCL_A.AcqOff		
	ColumnComp.PWM_CCL_B.AcqOff		
	ColumnComp.Fan_Rear_ActualRPM.AcqOff		
300.000	PostRun		
	External measured temperatures		
	Thermometer1.ExtTemp_UpperCC.AcqOff		
	Thermometer1.ExtTemp_LowerCC.AcqOff		
	Thermometer.Environment_Temperature.AcqOff		
	Leak Sensor Evaluation		
	ColumnComp.LEDBoard_LeakDiff.AcqOff		
	ColumnComp.LEDBoard_A13.AcqOff		
	ColumnComp.LEDBoard_A14.AcqOff		
	End		
```

<a id="m-tcc-errorlog-va"></a>
## M-TCC-ERRORLOG-VA: CHECKERRORLOG

Applicable device evidence: **VA**  
Source sequence(s): `VA:0000003`  
Source SHA-256: `0bd6836bc0b2a41b71aa8c15ba2a21a600705d3eb61959a8c41fcea47377ba56`  
Decoded flow rows: `8`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	ColumnComp.CC.TempCtrl	Off	
0.000	InjectPreparation		
0.000	Run	Duration = 0.300 [min]	
0.300	ColumnComp.Disconnect		
	ColumnComp.Connect		
0.500	StopRun		
	End		
```

<a id="m-tcc-errorlog-vcvh"></a>
## M-TCC-ERRORLOG-VCVH: CHECKERRORLOG

Applicable device evidence: **VC / VH**  
Source sequence(s): `VC:3000004, VH:6000001`  
Source SHA-256: `7aa667b8c7007ee90eee7ffc266682baa0af7a73fbd4503e10a6bf18dee4f724`  
Decoded flow rows: `14`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	ColumnComp.PrehtRight.TempCtrl	Off	
	ColumnComp.PrehtLeft.TempCtrl	Off	
	ColumnComp.CC.TempCtrl	Off	
	ColumnComp.Column_A.ActiveColumn	No	
	ColumnComp.Column_B.ActiveColumn	No	
	ColumnComp.Column_C.ActiveColumn	No	
	ColumnComp.Column_D.ActiveColumn	No	
0.000	InjectPreparation		
0.000	Run	Duration = 0.300 [min]	
0.300	ColumnComp.Disconnect		
	ColumnComp.Connect		
0.500	StopRun		
	End		
```

<a id="m-tcc-column-id"></a>
## M-TCC-COLUMN-ID: ColumnID

Applicable device evidence: **VA / VC / VH**  
Source sequence(s): `VA:0000003, VC:3000004, VH:6000001`  
Source SHA-256: `0bb7903cc203520248412dd1cd67e4870c9cef6a67b6761040206309520826df`  
Decoded flow rows: `58`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	=========================================================================================		
	IM to check the correct electronic wiring of the column ID ports		
	=========================================================================================		
	HPLC-System:		
	-----------		
	VTCC		
	=========================================================================================		
	CM needs data from any channel to evaluate the audit trail in the report.		
	=========================================================================================		
	Different total pages counts are used for VH-C10-A and VC-C10-A (no PCC). This is set here		
If		ColumnComp.ModelNo="VH-C10-A"	
	    Variables.GenericLong9	12	
	    Delay	1	[Val_FOQ_CM7_ekugelma_07-Jul-2020]: OK
	    Log	GenericLong9	
Else If		ColumnComp.ModelNo="VC-C10-A"	
	    Variables.GenericLong9	10	
	    Delay	1	[Val_FOQ_CM7_ekugelma_07-Jul-2020]: OK
	    Log	GenericLong9	
Else			
	    Message	Column compartment model unknown, please reinspect in production!	
	    System.AbortQueue		
End If			
	Column commpartment		
	ColumnComp.CC.TempCtrl	On	
	ColumnComp.CC.Temperature.Nominal	15.00 [°C]	Equilibration for BurnIn
	ColumnComp.CC.Mode	StillAir	
	=========================================================================================		
	Settings for the all channels offered for the column compartment by the driver.		
	Also debug channels are aqcuired.		
	=========================================================================================		
	Settings for Trigger Commands		
	Variables.GenericBool1	0	
	Delay	2	
Trigger		"END_RUN",	
	    Condition	Variables.GenericBool1=1	
	    TrueTime	0	
	    Limit	1	
	    Hysteresis	0	
	    AllowImmediateExecution	No	
	ColumnComp.CC_Temp.AcqOff		
	End		
End Trigger			
0.000	StartRun		
	ColumnComp.CC_Temp.AcqOn		
0.000	Run	Duration = 120.000 [min]	
	Message	Please plug the column ID adapters in their designated positions. Please note the correct order!	
	Wait	Column_A.CardState=OK AND Column_B.CardState=OK AND Column_C.CardState=OK AND Column_D.CardState=OK , Timeout=2.00	
	Log	Column_A.Description	
	Log	Column_B.Description	
	Log	Column_C.Description	
	Log	Column_D.Description	
	Delay	2	
If		Column_A.Description<>"A" OR Column_B.Description<>"B" OR Column_C.Description<>"C" OR Column_D.Description<>"D"	
	    Message	Either the cards are plugged into the wrong positions or the ports are electronically wrong connected! Check that the cards are in the correct position. If so, the device must be repaired!	
	    System.AbortQueue		
End If			
	Delay	2	
	Variables.GenericBool1	1	Enables Trigger "END_RUN" and thus stops sample
120.000	StopRun		
	ColumnComp.CC_Temp.AcqOff		
120.000	PostRun		
	End		
```

<a id="m-tcc-factory"></a>
## M-TCC-FACTORY: FACTORYDEFAULT

Applicable device evidence: **VA / VC / VH**  
Source sequence(s): `VA:0000003, VC:3000004, VH:6000001`  
Source SHA-256: `9285f264d9a382f0e374b72474bf99d22c424ea40ba6598019a64f5e8df18317`  
Decoded flow rows: `41`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	IM to set the predictive performance values and counters, which are visible for		
	the customer (Do not run for SERVICE instruments!)		
0.000	Run	Duration = 0.600 [min]	
	Commands to log the ErrorQueue		
0.100	ColumnComp.Disconnect		
	ColumnComp.Connect		
0.110	Wait	ColumnComp.Ready	
	ColumnComp.GetServiceCode		
	Delay	2	
	ColumnComp.ServiceCode	87794	
	Delay	0.01	
	Set the Qualification parameters (Qualification date equal to FOQ date)		
0.120	ColumnComp.ColumnComp_Wellness.Qualification.Interval	None	
	ColumnComp.ColumnComp_Wellness.Qualification.WarningPeriod	None	
	ColumnComp.ColumnComp_Wellness.Qualification.GracePeriod	None	
	Delay	0.01	
0.140	Log	ColumnComp_Wellness.Qualification.LastDate	
0.160	Log	ColumnComp_Wellness.Qualification.LastOperator	
	Set the Service parameters (Service date equal to FOQ date)		
	ColumnComp.ColumnComp_Wellness.Service.Interval	None	
	ColumnComp.ColumnComp_Wellness.Service.WarningPeriod	None	
0.210	Log	ColumnComp_Wellness.Service.LastDate	
0.290	Log	ColumnComp_Wellness.OperatingHours	
0.370	Log	ColumnComp.ColumnComp_Wellness.Workload_CC	
	Clear Error and Exception Log		
0.450	ColumnComp.ExceptionLogClear		
	ColumnComp.CmdString	Cmd="ErrorLog.Clear"	
0.500	ColumnComp.CmdString	Cmd="CC.ThermoUnitRevision="	
	Delay	3	
	ColumnComp.CmdString	ModuleRevision=	
	Final Temperature Setting		
0.600	ColumnComp.CC.Temperature.Nominal	20.00 [°C]	
	ColumnComp.CC.TempCtrl	Off	
	ColumnComp.LiquidLeakSensor	On	
	ColumnComp.CmdString	Cmd="LedBar.ForceColor=1"	
	Message	Please check, that no valves are installed any more, but the corresponding covers!	
	Delay	2	
	Message	Please check if you have choosen the correct serial number of the thermometer and the location from the Custom Sequence Variable list	
	ColumnComp.CmdString	Cmd="LedBar.ForceColor=0"	
	End		
```

<a id="m-tcc-leak-va"></a>
## M-TCC-LEAK-VA: LIQUID LEAK

Applicable device evidence: **VA**  
Source sequence(s): `VA:0000003`  
Source SHA-256: `3401a5ccf28ac0fa35d5e86320c842bb3ce6645db55ba03ea50260d858f2fa5d`  
Decoded flow rows: `133`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	=========================================================================================		
	IM to measure the performance of the Vanquish VH-C10-A, VC-C10-A or VA-C10-A Liquid Leak Sensor		
	=========================================================================================		
	HPLC-System:		
	-----------		
	VH-C10-A, VC-C10-A or VA-C10-A		
-0.250	Equilibration	Duration = 0.250 [min]	
	=========================================================================================		
	Parameters valid for the whole test.		
	=========================================================================================		
	If the difference between nominal and actual temperature is larger than ReadyTempDelta, the VTCC is not ready.		
	ColumnComp.CC.ReadyTempDelta	None	
	The Ready property will become Ready only if the difference between the setpoint temperature and the nominal temperature will not exceed the ReadyTempDelta for the  time interval specified by EquilibrationTime.		
	ColumnComp.CC.EquilibrationTime	0.5	
	The VTCC adjusts the temperature only, if TempCtrl is set to ON for each single unit.		
	ColumnComp.CC.TempCtrl	On	
	To ensure that the leak test is performed at 20°C (nominal temperature of previous run)		
	ColumnComp.CC.Temperature.Nominal	20.0 [°C]	
	Adjusts FanSpeed and switches operating mode		
	ColumnComp.CC.Mode	StillAir	
	=========================================================================================		
	CM needs data from any channel to evaluate the audit trail in the report.		
	=========================================================================================		
	Column commpartment		
	ColumnComp.CC_U_Temp_Actual.Data_Collection_Rate	20	
	ColumnComp.CC_L_Temp_Actual.Data_Collection_Rate	20	
	ColumnComp.CC_UCTL_TempRear_Actual.Data_Collection_Rate	20	
	ColumnComp.PWM_CCU_A.Data_Collection_Rate	20	
	ColumnComp.PWM_CCU_B.Data_Collection_Rate	20	
	ColumnComp.PWM_CCL_A.Data_Collection_Rate	20	
	ColumnComp.PWM_CCL_B.Data_Collection_Rate	20	
	ColumnComp.Fan_Rear_ActualRPM.Data_Collection_Rate	20	
	Leak Sensors		
	ColumnComp.LEDBoard_LeakDiff.Data_Collection_Rate	20	
	ColumnComp.LEDBoard_A13.Data_Collection_Rate	20	
	ColumnComp.LEDBoard_A14.Data_Collection_Rate	20	
	ColumnComp.Oven_Gas_MuteTimeRemain.Data_Collection_Rate	20	
	Settings for Trigger Commands		
	Variables.GenericBool1	0	
Trigger		"END_RUN",	
	    Condition	Variables.GenericBool1=1 AND System.Retention>0.01	
	    TrueTime	10	
	    Limit	1	
	    Hysteresis	0	
	    AllowImmediateExecution	No	
	ColumnComp.CC_Temp.AcqOff		
	ColumnComp.CC_U_Temp_Actual.AcqOff		
	ColumnComp.CC_L_Temp_Actual.AcqOff		
	ColumnComp.CC_UCTL_TempRear_Actual.AcqOff		
	ColumnComp.PWM_CCU_A.AcqOff		
	ColumnComp.PWM_CCU_B.AcqOff		
	ColumnComp.PWM_CCL_A.AcqOff		
	ColumnComp.PWM_CCL_B.AcqOff		
	ColumnComp.Fan_Rear_ActualRPM.AcqOff		
	External measured temperatures		
	Thermometer1.ExtTemp_UpperCC.AcqOff		
	Thermometer1.ExtTemp_LowerCC.AcqOff		
	Thermometer.Environment_Temperature.AcqOff		
	Leak Sensor Evaluation		
	ColumnComp.LEDBoard_LeakDiff.AcqOff		
	ColumnComp.LEDBoard_A13.AcqOff		
	ColumnComp.LEDBoard_A14.AcqOff		
	ColumnComp.Oven_Gas_MuteTimeRemain.AcqOff		
	End		
End Trigger			
	ColumnComp.LiquidLeakSensor	On	
0.000	StartRun		
	Wait	ColumnComp.CC.TempReady	
If		Door=Closed AND LiquidLeak=NoLeak	
	    ColumnComp.CmdString	Cmd="LedBar.ForceColor=1"	
	    Message	Press OK, open compartment door and then inject 5 mL water to bottom of compartment.	
	    ColumnComp.CmdString	Cmd="LedBar.ForceColor=0"	
Else			
	    System.AbortQueue		
End If			
	ColumnComp.CC_Temp.AcqOn		
	ColumnComp.CC_U_Temp_Actual.AcqOn		
	ColumnComp.CC_L_Temp_Actual.AcqOn		
	ColumnComp.CC_UCTL_TempRear_Actual.AcqOn		
	ColumnComp.PWM_CCU_A.AcqOn		
	ColumnComp.PWM_CCU_B.AcqOn		
	ColumnComp.PWM_CCL_A.AcqOn		
	ColumnComp.PWM_CCL_B.AcqOn		
	ColumnComp.Fan_Rear_ActualRPM.AcqOn		
	External measured temperatures		
	Thermometer1.ExtTemp_UpperCC.AcqOn		
	Thermometer1.ExtTemp_LowerCC.AcqOn		
	Thermometer.Environment_Temperature.AcqOn		
	Leak Sensor Evaluation		
	ColumnComp.LEDBoard_LeakDiff.AcqOn		
	ColumnComp.LEDBoard_A13.AcqOn		
	ColumnComp.LEDBoard_A14.AcqOn		
	ColumnComp.Oven_Gas_MuteTimeRemain.AcqOn		
0.000	Run	Duration = 120.000 [min]	
	Wait	LiquidLeak=Leak, Continue, Timeout=2.00	
	Delay	1	
	Log	LiquidLeak	
	Delay	1	
	ColumnComp.CmdString	Cmd="LedBar.ForceColor=1"	
	Message	Confirm the leak alarm by pressing 'MUTE ALARM' on the instruments keypad!	
	ColumnComp.CmdString	Cmd="LedBar.ForceColor=0"	
	Wait	ColumnComp.Alarm = NoAlarm	
If		ColumnComp.Alarm=NoAlarm	
	    ColumnComp.LiquidLeakSensor	Off	
	    Delay	1	
Else			
	    System.AbortQueue		
End If			
	ColumnComp.CmdString	Cmd="LedBar.ForceColor=1"	
	Message	With a cloth or tissue, thoroughly absorb all liquid that has collected under the leak sensor and in compartment. Close door again.	
	Delay	5	
	Message	Please confirm that all liquid under the liquid leak sensor has been removed!	
	ColumnComp.CmdString	Cmd="LedBar.ForceColor=0"	
	Delay	5	
	Variables.GenericBool1	1	Enables Trigger "END_RUN"
	Delay	1	
120.000	StopRun		
	ColumnComp.CC_Temp.AcqOff		
	ColumnComp.CC_U_Temp_Actual.AcqOff		
	ColumnComp.CC_L_Temp_Actual.AcqOff		
	ColumnComp.CC_UCTL_TempRear_Actual.AcqOff		
	ColumnComp.PWM_CCU_A.AcqOff		
	ColumnComp.PWM_CCU_B.AcqOff		
	ColumnComp.PWM_CCL_A.AcqOff		
	ColumnComp.PWM_CCL_B.AcqOff		
	ColumnComp.Fan_Rear_ActualRPM.AcqOff		
	External measured temperatures		
	Thermometer1.ExtTemp_UpperCC.AcqOff		
	Thermometer1.ExtTemp_LowerCC.AcqOff		
	Thermometer.Environment_Temperature.AcqOff		
	Leak Sensor Evaluation		
	ColumnComp.LEDBoard_LeakDiff.AcqOff		
	ColumnComp.LEDBoard_A13.AcqOff		
	ColumnComp.LEDBoard_A14.AcqOff		
	ColumnComp.Oven_Gas_MuteTimeRemain.AcqOff		
120.000	PostRun		
	End		
```

<a id="m-tcc-leak-vcvh"></a>
## M-TCC-LEAK-VCVH: LIQUID LEAK

Applicable device evidence: **VC / VH**  
Source sequence(s): `VC:3000004, VH:6000001`  
Source SHA-256: `7c12001ab1b12bb005b9641ebef8f5b96d32fb32333627956bd31924d09405f3`  
Decoded flow rows: `133`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	=========================================================================================		
	IM to measure the performance of the Vanquish VH-C10-A or VC-C10-A Liquid Leak Sensor		
	=========================================================================================		
	HPLC-System:		
	-----------		
	VH-C10-A or VC-C10-A		
-0.250	Equilibration	Duration = 0.250 [min]	
	=========================================================================================		
	Parameters valid for the whole test.		
	=========================================================================================		
	If the difference between nominal and actual temperature is larger than ReadyTempDelta, the VTCC is not ready.		
	ColumnComp.CC.ReadyTempDelta	None	
	The Ready property will become Ready only if the difference between the setpoint temperature and the nominal temperature will not exceed the ReadyTempDelta for the  time interval specified by EquilibrationTime.		
	ColumnComp.CC.EquilibrationTime	0.5	
	The VTCC adjusts the temperature only, if TempCtrl is set to ON for each single unit.		
	ColumnComp.CC.TempCtrl	On	
	To ensure that the leak test is performed at 20°C (nominal temperature of previous run)		
	ColumnComp.CC.Temperature.Nominal	20.0 [°C]	
	Adjusts FanSpeed and switches operating mode		
	ColumnComp.CC.Mode	StillAir	
	=========================================================================================		
	CM needs data from any channel to evaluate the audit trail in the report.		
	=========================================================================================		
	Column commpartment		
	ColumnComp.CC_U_Temp_Actual.Data_Collection_Rate	20	
	ColumnComp.CC_L_Temp_Actual.Data_Collection_Rate	20	
	ColumnComp.CC_UCTL_TempRear_Actual.Data_Collection_Rate	20	
	ColumnComp.PWM_CCU_A.Data_Collection_Rate	20	
	ColumnComp.PWM_CCU_B.Data_Collection_Rate	20	
	ColumnComp.PWM_CCL_A.Data_Collection_Rate	20	
	ColumnComp.PWM_CCL_B.Data_Collection_Rate	20	
	ColumnComp.Fan_Rear_ActualRPM.Data_Collection_Rate	20	
	Leak Sensors		
	ColumnComp.LEDBoard_LeakDiff.Data_Collection_Rate	20	
	ColumnComp.LEDBoard_A13.Data_Collection_Rate	20	
	ColumnComp.LEDBoard_A14.Data_Collection_Rate	20	
	ColumnComp.Oven_Gas_MuteTimeRemain.Data_Collection_Rate	20	
	Settings for Trigger Commands		
	Variables.GenericBool1	0	
Trigger		"END_RUN",	
	    Condition	Variables.GenericBool1=1 AND System.Retention>0.01	
	    TrueTime	10	
	    Limit	1	
	    Hysteresis	0	
	    AllowImmediateExecution	No	
	ColumnComp.CC_Temp.AcqOff		
	ColumnComp.CC_U_Temp_Actual.AcqOff		
	ColumnComp.CC_L_Temp_Actual.AcqOff		
	ColumnComp.CC_UCTL_TempRear_Actual.AcqOff		
	ColumnComp.PWM_CCU_A.AcqOff		
	ColumnComp.PWM_CCU_B.AcqOff		
	ColumnComp.PWM_CCL_A.AcqOff		
	ColumnComp.PWM_CCL_B.AcqOff		
	ColumnComp.Fan_Rear_ActualRPM.AcqOff		
	External measured temperatures		
	Thermometer1.ExtTemp_UpperCC.AcqOff		
	Thermometer1.ExtTemp_LowerCC.AcqOff		
	Thermometer.Environment_Temperature.AcqOff		
	Leak Sensor Evaluation		
	ColumnComp.LEDBoard_LeakDiff.AcqOff		
	ColumnComp.LEDBoard_A13.AcqOff		
	ColumnComp.LEDBoard_A14.AcqOff		
	ColumnComp.Oven_Gas_MuteTimeRemain.AcqOff		
	End		
End Trigger			
	ColumnComp.LiquidLeakSensor	On	
0.000	StartRun		
	Wait	ColumnComp.CC.TempReady	
If		Door=Closed AND LiquidLeak=NoLeak	
	    ColumnComp.CmdString	Cmd="LedBar.ForceColor=1"	
	    Message	Press OK, open compartment door and then inject 5 mL water to bottom of compartment.	
	    ColumnComp.CmdString	Cmd="LedBar.ForceColor=0"	
Else			
	    System.AbortQueue		
End If			
	ColumnComp.CC_Temp.AcqOn		
	ColumnComp.CC_U_Temp_Actual.AcqOn		
	ColumnComp.CC_L_Temp_Actual.AcqOn		
	ColumnComp.CC_UCTL_TempRear_Actual.AcqOn		
	ColumnComp.PWM_CCU_A.AcqOn		
	ColumnComp.PWM_CCU_B.AcqOn		
	ColumnComp.PWM_CCL_A.AcqOn		
	ColumnComp.PWM_CCL_B.AcqOn		
	ColumnComp.Fan_Rear_ActualRPM.AcqOn		
	External measured temperatures		
	Thermometer1.ExtTemp_UpperCC.AcqOn		
	Thermometer1.ExtTemp_LowerCC.AcqOn		
	Thermometer.Environment_Temperature.AcqOn		
	Leak Sensor Evaluation		
	ColumnComp.LEDBoard_LeakDiff.AcqOn		
	ColumnComp.LEDBoard_A13.AcqOn		
	ColumnComp.LEDBoard_A14.AcqOn		
	ColumnComp.Oven_Gas_MuteTimeRemain.AcqOn		
0.000	Run	Duration = 120.000 [min]	
	Wait	LiquidLeak=Leak, Continue, Timeout=2.00	
	Delay	1	
	Log	LiquidLeak	
	Delay	1	
	ColumnComp.CmdString	Cmd="LedBar.ForceColor=1"	
	Message	Confirm the leak alarm by pressing 'MUTE ALARM' on the instruments keypad!	
	ColumnComp.CmdString	Cmd="LedBar.ForceColor=0"	
	Wait	ColumnComp.Alarm = NoAlarm	
If		ColumnComp.Alarm=NoAlarm	
	    ColumnComp.LiquidLeakSensor	Off	
	    Delay	1	
Else			
	    System.AbortQueue		
End If			
	ColumnComp.CmdString	Cmd="LedBar.ForceColor=1"	
	Message	With a cloth or tissue, thoroughly absorb all liquid that has collected under the leak sensor and in compartment. Close door again.	
	Delay	5	
	Message	Please confirm that all liquid under the liquid leak sensor has been removed!	
	ColumnComp.CmdString	Cmd="LedBar.ForceColor=0"	
	Delay	5	
	Variables.GenericBool1	1	Enables Trigger "END_RUN"
	Delay	1	
120.000	StopRun		
	ColumnComp.CC_Temp.AcqOff		
	ColumnComp.CC_U_Temp_Actual.AcqOff		
	ColumnComp.CC_L_Temp_Actual.AcqOff		
	ColumnComp.CC_UCTL_TempRear_Actual.AcqOff		
	ColumnComp.PWM_CCU_A.AcqOff		
	ColumnComp.PWM_CCU_B.AcqOff		
	ColumnComp.PWM_CCL_A.AcqOff		
	ColumnComp.PWM_CCL_B.AcqOff		
	ColumnComp.Fan_Rear_ActualRPM.AcqOff		
	External measured temperatures		
	Thermometer1.ExtTemp_UpperCC.AcqOff		
	Thermometer1.ExtTemp_LowerCC.AcqOff		
	Thermometer.Environment_Temperature.AcqOff		
	Leak Sensor Evaluation		
	ColumnComp.LEDBoard_LeakDiff.AcqOff		
	ColumnComp.LEDBoard_A13.AcqOff		
	ColumnComp.LEDBoard_A14.AcqOff		
	ColumnComp.Oven_Gas_MuteTimeRemain.AcqOff		
120.000	PostRun		
	End		
```

<a id="m-tcc-preheater"></a>
## M-TCC-PREHEATER: PREHEATER

Applicable device evidence: **VA / VC / VH**  
Source sequence(s): `VA:0000003, VC:3000004, VH:6000001`  
Source SHA-256: `97839fca874f7f19c3eadb8760000d32a35a95af73051ed571b878a30709d273`  
Decoded flow rows: `218`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	=========================================================================================		
	IM to measure the preheater connection ports of the Vanquish TCC.		
	=========================================================================================		
	HPLC-System:		
	-----------		
	VTCC		
	=========================================================================================		
	Parameters valid for the whole test.		
	=========================================================================================		
	If the difference between the setpoint temperature and the actual temperature		
	exeeds ReadyTempDelta, the VTCC is not ready.		
-0.500	Equilibration	Duration = 0.500 [min]	
	ColumnComp.CC.ReadyTempDelta	1.0 [°C]	
	The Ready property will become Ready only if the difference between the		
	setpoint temperature and the nominal temperature will not exceed the ReadyTempDelta for		
	the time interval specified by EquilibrationTime.		
	ColumnComp.CC.EquilibrationTime	0.5 [min]	
	The VTCC controls the temperature only, if TempCtrl is set to ON.		
	ColumnComp.CC.TempCtrl	On	
	ColumnComp.CC.Temperature.Nominal	15 [°C]	Equilibration for Burn-In
	Adjusts FanSpeed and switches operating mode		
	ColumnComp.CC.Mode	StillAir	
	Initialize gereric variables used during preheater triggers		
	Values change during trigger execution and can be used as conditions to stop the sample "regularly"		
	Variables.GenericBool1	0	
	Variables.GenericBool2	0	
	Initialize Retention Times used during preheater triggers		
	RetTimes.RetTime1	0	
	RetTimes.RetTime2	0	
	RetTimes.RetTime3	0	
	RetTimes.RetTime4	0	
	Setting of regulation parameters for preheater simulator only		
	setting are not persistent - after reboot default parameters for real preheaters are set again automatically. However they will be reset at the end of the IM		
	ColumnComp.CmdString	Cmd="PREH.L.PID.Kp=10000"	
	ColumnComp.CmdString	Cmd="PREH.L.PID.Ki=1200"	
	ColumnComp.CmdString	Cmd="PREH.R.PID.Kp=10000"	
	ColumnComp.CmdString	Cmd="PREH.R.PID.Ki=1200"	
	=========================================================================================		
	Preheater settings		
	The settings for ReadyTempDelta and Equil.Time are relatively tight so that the signals		
	are more stable at the beginning of the data aquisition		
	=========================================================================================		
	ColumnComp.PrehtLeft.TempCtrl	On	
	ColumnComp.PrehtRight.TempCtrl	On	
	ColumnComp.PrehtLeft.Temperature.Nominal	40.00 [°C]	
	ColumnComp.PrehtLeft.ReadyTempDelta	0.05 [°C]	
	ColumnComp.PrehtLeft.EquilibrationTime	0.5 [min]	
	ColumnComp.PrehtRight.Temperature.Nominal	40.00 [°C]	
	ColumnComp.PrehtRight.ReadyTempDelta	0.05 [°C]	
	ColumnComp.PrehtRight.EquilibrationTime	0.5 [min]	
	=========================================================================================		
	Settings for the all channels offered for the column compartment by the driver.		
	Also debug channels are aqcuired.		
	=========================================================================================		
	Preheater		
	ColumnComp.PREH_L_HeaterTemp_Actual.Data_Collection_Rate	20	
	ColumnComp.PREH_R_HeaterTemp_Actual.Data_Collection_Rate	20	
	ColumnComp.PREH_L_Temp_Actual.Data_Collection_Rate	20	
	ColumnComp.PREH_R_Temp_Actual.Data_Collection_Rate	20	
	ColumnComp.PWM_LeftPreh.Data_Collection_Rate	20	
	ColumnComp.PWM_RightPreh.Data_Collection_Rate	20	
	ColumnComp.Fan_Rear_ActualRPM.Data_Collection_Rate	20	
	Leak Sensors		
	ColumnComp.LEDBoard_LeakDiff.Data_Collection_Rate	20	
	ColumnComp.LEDBoard_A13.Data_Collection_Rate	20	
	ColumnComp.LEDBoard_A14.Data_Collection_Rate	20	
	ColumnComp.Oven_Gas_MuteTimeRemain.Data_Collection_Rate	20	
	=========================================================================================		
	Start		
	=========================================================================================		
0.000	InjectPreparation		
	Wait	PrehtLeft.TempReady AND PrehtRight.TempReady	
0.000	StartRun		
	ColumnComp.CC_Temp.AcqOn		
	Preheater		
	ColumnComp.PrehtLeft_Temp.AcqOn		
	ColumnComp.PrehtRight_Temp.AcqOn		
	ColumnComp.PREH_L_Temp_Actual.AcqOn		
	ColumnComp.PREH_R_Temp_Actual.AcqOn		
	ColumnComp.PREH_L_HeaterTemp_Actual.AcqOn		
	ColumnComp.PREH_R_HeaterTemp_Actual.AcqOn		
	ColumnComp.PWM_LeftPreh.AcqOn		
	ColumnComp.PWM_RightPreh.AcqOn		
	ColumnComp.Fan_Rear_ActualRPM.AcqOn		
	External measured temperatures		
	Thermometer1.ExtTemp_UpperCC.AcqOn		
	Thermometer1.ExtTemp_LowerCC.AcqOn		
	Thermometer.Environment_Temperature.AcqOn		
	Leak Sensor Evaluation		
	ColumnComp.LEDBoard_LeakDiff.AcqOn		
	ColumnComp.LEDBoard_A13.AcqOn		
	ColumnComp.LEDBoard_A14.AcqOn		
	ColumnComp.Oven_Gas_MuteTimeRemain.AcqOn		
0.000	Run	Duration = 10.100 [min]	
	========================================================================================		
	TempCtrl off/on while the signal is relatively stable to check for signal jumps		
	========================================================================================		
0.500	ColumnComp.PrehtLeft.TempCtrl	Off	
	ColumnComp.PrehtRight.TempCtrl	Off	
0.600	ColumnComp.PrehtLeft.Temperature.Nominal	60.0 [°C]	
	=========================================================================================		
	Trigger for Heat Time measuring 45°C to 55°C (Preheater Temperature)		
	=========================================================================================		
Trigger		"T_UP_Left",	if there is a short ciruit left, the trigger should never start
	    Condition	PrehtLeft.Temperature.Value>=45.0	
	    TrueTime	1	
	    Limit	1	
	    Hysteresis	0	
	    AllowImmediateExecution	No	
	RetTimes.RetTime1	System.Retention	Retention time when start temperature was reached is "logged" for evaluating purposes
	Log	PrehtLeft.Temperature.Value	
	Log	PrehtLeft.TempActual_Heater	
	Delay	1	
If		PrehtLeft.Temperature.Value-PrehtRight.Temperature.Value<5	
	    Protocol	***Temperature increase observed on right pre-heater although TempCtrl.Right is off. There is a short circuit on the pre-heater board. The batch will be aborted!***	
	    Delay	1	
	    ColumnComp.PrehtLeft.TempCtrl	Off	
	    ColumnComp.PrehtRight.TempCtrl	Off	
	    Delay	1	
	    System.AbortQueue		
Else			
	    ColumnComp.PrehtRight.Temperature.Nominal	60.0 [°C]	
End If			
End Trigger			
	Trigger T_UP_Right is similar to Trigger T_UP_Left, just the other side		
Trigger		"T_UP_Right",	
	    Condition	PrehtRight.Temperature.Value>=45.0 AND PrehtRight.TempCtrl=On	
	    TrueTime	1	
	    Limit	1	
	    Hysteresis	0	
	    AllowImmediateExecution	No	
	RetTimes.RetTime2	System.Retention	
	Log	PrehtRight.Temperature.Value	
	Log	PrehtRight.TempActual_Heater	
End Trigger			
Trigger		"Reached_Left",	
	    Condition	PrehtLeft.Temperature.Value>=55.0	
	    TrueTime	1	
	    Limit	1	
	    Hysteresis	0	
	    AllowImmediateExecution	No	
	RetTimes.RetTime3	System.Retention	Retention time when end temperature was reached is "logged" for evaluating purposes
	Log	PrehtLeft.Temperature.Value	
	Log	PrehtLeft.TempActual_Heater	
	Delay	1	
	ColumnComp.PrehtLeft.TempCtrl	Off	
	Variables.GenericBool1	1	
	Delay	10	
End Trigger			
Trigger		"Reached_Right",	
	    Condition	PrehtRight.Temperature.Value>=55.0	
	    TrueTime	1	
	    Limit	1	
	    Hysteresis	0	
	    AllowImmediateExecution	No	
	RetTimes.RetTime4	System.Retention	
	Log	PrehtRight.Temperature.Value	
	Log	PrehtRight.TempActual_Heater	
	Delay	1	
	ColumnComp.PrehtRight.TempCtrl	Off	
	Variables.GenericBool2	1	
	Delay	10	
End Trigger			
	=========================================================================================		
	End Trigger		
	The commands in the trigger are only executed when the preheater temperatures exceeded certain values - see above triggers "Reached_Right/Left"		
	These trigger set the variables GenericBool1 AND GenericBool2 to values different from the initial values		
	Stopping the sample by the "end trigger" is the regular end of the sample		
	=========================================================================================		
Trigger		"END_RUN",	
	    Condition	Variables.GenericBool1=1 AND Variables.GenericBool2=1	
	    TrueTime	10	
	    Limit	1	
	    Hysteresis	0	
	    AllowImmediateExecution	No	
	Switching off the Pre-heater at the end of the IM		
	ColumnComp.PrehtLeft.TempCtrl	Off	
	ColumnComp.PrehtRight.TempCtrl	Off	
	Column commpartment		
	ColumnComp.CC_Temp.AcqOff		
	Preheater		
	ColumnComp.PrehtLeft_Temp.AcqOff		
	ColumnComp.PrehtRight_Temp.AcqOff		
	ColumnComp.PREH_L_Temp_Actual.AcqOff		
	ColumnComp.PREH_R_Temp_Actual.AcqOff		
	ColumnComp.PREH_L_HeaterTemp_Actual.AcqOff		
	ColumnComp.PREH_R_HeaterTemp_Actual.AcqOff		
	ColumnComp.PWM_LeftPreh.AcqOff		
	ColumnComp.PWM_RightPreh.AcqOff		
	ColumnComp.Fan_Rear_ActualRPM.AcqOff		
	External measured temperatures		
	Thermometer1.ExtTemp_UpperCC.AcqOff		
	Thermometer1.ExtTemp_LowerCC.AcqOff		
	Thermometer.Environment_Temperature.AcqOff		
	Leak Sensor Evaluation		
	ColumnComp.LEDBoard_LeakDiff.AcqOff		
	ColumnComp.LEDBoard_A13.AcqOff		
	ColumnComp.LEDBoard_A14.AcqOff		
	ColumnComp.Oven_Gas_MuteTimeRemain.AcqOff		
	Reset of regulation parameters for preheater simulator		
	ColumnComp.CmdString	Cmd="PREH.L.PID.Kp=600000"	
	ColumnComp.CmdString	Cmd="PREH.L.PID.Ki=30000"	
	ColumnComp.CmdString	Cmd="PREH.R.PID.Kp=600000"	
	ColumnComp.CmdString	Cmd="PREH.R.PID.Ki=30000"	
	End		
End Trigger			
10.000	ColumnComp.PrehtLeft.TempCtrl	Off	
	ColumnComp.PrehtRight.TempCtrl	Off	
	The following lines are only executed if trigger "END_RUN" was not executed, i.e. the preheaters did not heat up		
10.100	Message	The nominal temperature on either the left, right or both pre-heater was not reached. Check for loose connections or short circuits on the pre-heater board!	
	Delay	1	
	System.AbortQueue		
	The following lines are required to pass the ready check (each acquisition on command requires an acquistion off command).		
	These lines are never executed, because the previous line will aborts the current sample and the running acquisition.		
11.000	StopRun		
	ColumnComp.CC_Temp.AcqOff		
11.000	PostRun		
	Preheater		
	ColumnComp.PrehtLeft_Temp.AcqOff		
	ColumnComp.PrehtRight_Temp.AcqOff		
	ColumnComp.PREH_L_Temp_Actual.AcqOff		
	ColumnComp.PREH_R_Temp_Actual.AcqOff		
	ColumnComp.PREH_L_HeaterTemp_Actual.AcqOff		
	ColumnComp.PREH_R_HeaterTemp_Actual.AcqOff		
	ColumnComp.PWM_LeftPreh.AcqOff		
	ColumnComp.PWM_RightPreh.AcqOff		
	ColumnComp.Fan_Rear_ActualRPM.AcqOff		
	External measured temperatures		
	Thermometer1.ExtTemp_UpperCC.AcqOff		
	Thermometer1.ExtTemp_LowerCC.AcqOff		
	Thermometer.Environment_Temperature.AcqOff		
	Leak Sensor Evaluation		
	ColumnComp.LEDBoard_LeakDiff.AcqOff		
	ColumnComp.LEDBoard_A13.AcqOff		
	ColumnComp.LEDBoard_A14.AcqOff		
	ColumnComp.Oven_Gas_MuteTimeRemain.AcqOff		
	Reset of regulation parameters for preheater simulator		
	ColumnComp.CmdString	Cmd="PREH.L.PID.Kp=600000"	
	ColumnComp.CmdString	Cmd="PREH.L.PID.Ki=30000"	
	ColumnComp.CmdString	Cmd="PREH.R.PID.Kp=600000"	
	ColumnComp.CmdString	Cmd="PREH.R.PID.Ki=30000"	
	End		
```

<a id="m-tcc-service"></a>
## M-TCC-SERVICE: QUALIFICATION_SERVICE_DONE

Applicable device evidence: **VA / VC / VH**  
Source sequence(s): `VA:0000003, VC:3000004, VH:6000001`  
Source SHA-256: `12f1c16ded7cffa653c09a48e7c0a8c268c1e4cef96cfa223b78820b27ebf134`  
Decoded flow rows: `9`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	Set the Qualification and Service date for service instruments		
	---------------------------------------------------------------------------------------		
0.000	Run	Duration = 0.110 [min]	
0.100	ColumnComp.ColumnComp_Wellness.QualificationDone		
	ColumnComp.ColumnComp_Wellness.ServiceDone		
0.105	Log	ColumnComp_Wellness.Service.LastDate	
	Log	ColumnComp_Wellness.Qualification.LastDate	
	End		
```

<a id="m-tcc-stress-test"></a>
## M-TCC-STRESS-TEST: stress test

Applicable device evidence: **VH-STRESS**  
Source sequence(s): `VH-STRESS:Stress_VH_DVT013_20260529`  
Source SHA-256: `693b36a7ff03011c393fa1ad0aeb2cc3a938d8df12d45ec57127695f2065e3cc`  
Decoded flow rows: `130`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	ColumnComp.CC.Temperature.LowerLimit	5.0 [°C]	
	ColumnComp.CC.Temperature.UpperLimit	85 [°C]	
	ColumnComp.PrehtRight.TempCtrl	On	
	ColumnComp.PrehtRight.Temperature.Nominal	30.00 [°C]	
	ColumnComp.PrehtLeft.TempCtrl	On	
	PumpModule.Pump.%A.Equate	Water	
	PumpModule.Pump.Pressure.LowerLimit	0 [bar]	
	PumpModule.Pump.Pressure.UpperLimit	660 [bar]	
	PumpModule.Pump.MaximumFlowRampUp	Infinite	
	PumpModule.Pump.MaximumFlowRampDown	Infinite	
	ColumnComp.PrehtLeft.Temperature.Nominal	30.00 [°C]	
	ColumnComp.CC.ReadyTempDelta	0.5 [°C]	
	ColumnComp.CC.TempCtrl	On	
	ColumnComp.CC.Temperature.Nominal	70.0 [°C]	
	ColumnComp.CC.EquilibrationTime	0.5 [min]	
	PumpModule.Pump.Pump_Pressure.UseFilter	Off	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	1_2	
	ColumnComp.LowerValve.CurrentPosition	6_1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Variables.GenericBool1	0	
	Variables.GenericBool2	0	
	Variables.GenericFloat1	0	
0.000	Equilibration		
	PumpModule.Pump.Flow.Nominal	2.00000 [ml/min]	
	PumpModule.Pump.Curve	5	
0.000	InjectPreparation		
	Wait	ColumnComp.CC.TempReady AND PumpModule.Pump.Ready, Run=Hold	
0.000	StartRun		
	PumpModule.Pump.Pump_Pressure.AcqOn		
	ColumnComp.PrehtLeft_Temp.AcqOn		
	ColumnComp.PrehtRight_Temp.AcqOn		
	ColumnComp.PREH_L_Temp_Actual.AcqOn		
	ColumnComp.PREH_R_Temp_Actual.AcqOn		
	ColumnComp.PREH_L_HeaterTemp_Actual.AcqOn		
	ColumnComp.PREH_R_HeaterTemp_Actual.AcqOn		
	ColumnComp.PWM_LeftPreh.AcqOn		
	ColumnComp.PWM_RightPreh.AcqOn		
	ColumnComp.CC_Temp.AcqOn		
	VirtualChannel	PumpPressureVirtual, PumpModule.Pump.Pump_Pressure.Signal, Type=Digital, Unit="bar", Evaluate=Yes	
	Thermometer.Environment_Temperature.AcqOn		
Trigger		"Ping",	
	    Condition	Variables.GenericBool1=1 AND System.Retention>Variables.GenericFloat1 and system.Retention>10 and system.Retention<20	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.01	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	6_1	
	ColumnComp.LowerValve.CurrentPosition	1_2	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Log	ColumnComp.CC_Temp	
	Log	ColumnComp.PrehtLeft_Temp	
	Log	ColumnComp.PrehtRight_Temp	
	Delay	1	
	Variables.GenericBool1	0	
	Delay	0	
	Variables.GenericBool2	1	
End Trigger			
Trigger		"Pong",	
	    Condition	Variables.GenericBool2=1 AND System.Retention>Variables.GenericFloat1 and system.Retention>10 and system.Retention<20	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.01	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	1_2	
	ColumnComp.LowerValve.CurrentPosition	6_1	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Log	ColumnComp.CC_Temp	
	Log	ColumnComp.PrehtLeft_Temp	
	Log	ColumnComp.PrehtRight_Temp	
	Delay	1	
	Variables.GenericBool1	1	
	Delay	0	
	Variables.GenericBool2	0	
End Trigger			
0.000	Run	Duration = 20.000 [min]	
	PumpModule.Pump.Flow.Nominal	2.00000 [ml/min]	
	PumpModule.Pump.Curve	5	
	Variables.GenericBool1	1	
20.000			
Trigger		"bing",	
	    Condition	Variables.GenericBool1=1 AND System.Retention>Variables.GenericFloat1 and system.Retention>30 and system.Retention<35	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.05	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	6_1	
	ColumnComp.LowerValve.CurrentPosition	1_2	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Log	ColumnComp.CC_Temp	
	Log	ColumnComp.PrehtLeft_Temp	
	Log	ColumnComp.PrehtRight_Temp	
	Delay	1	
	Variables.GenericBool1	0	
	Delay	0	
	Variables.GenericBool2	1	
End Trigger			
Trigger		"bong",	
	    Condition	Variables.GenericBool2=1 AND System.Retention>Variables.GenericFloat1 and system.Retention>30 and system.Retention<35	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.05	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	1_2	
	ColumnComp.LowerValve.CurrentPosition	6_1	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Log	ColumnComp.CC_Temp	
	Log	ColumnComp.PrehtLeft_Temp	
	Log	ColumnComp.PrehtRight_Temp	
	Delay	1	
	Variables.GenericBool1	1	
	Delay	0	
	Variables.GenericBool2	0	
End Trigger			
45.500	StopRun		
	Variables.GenericBool1	0	
	Variables.GenericBool2	0	
	PumpModule.Pump.Flow.Nominal	2.00000 [ml/min]	
	PumpModule.Pump.Curve	5	
	PumpModule.Pump.Flow.Nominal	0.000000 [ml/min]	
	PumpModule.Pump.Curve	5	
	PumpModule.Pump.Pump_Pressure.AcqOff		
	ColumnComp.CC_Temp.AcqOff		
	ColumnComp.PrehtLeft_Temp.AcqOff		
	ColumnComp.PrehtRight_Temp.AcqOff		
	ColumnComp.PREH_L_Temp_Actual.AcqOff		
	ColumnComp.PREH_R_Temp_Actual.AcqOff		
	ColumnComp.PREH_L_HeaterTemp_Actual.AcqOff		
	ColumnComp.PREH_R_HeaterTemp_Actual.AcqOff		
	ColumnComp.PWM_LeftPreh.AcqOff		
	ColumnComp.PWM_RightPreh.AcqOff		
	Thermometer.Environment_Temperature.AcqOff		
	End		
```

<a id="m-tcc-stress-test-5s"></a>
## M-TCC-STRESS-TEST-5S: stress test_5s

Applicable device evidence: **VH-STRESS**  
Source sequence(s): `VH-STRESS:Stress_VH_DVT013_20260529`  
Source SHA-256: `246c93888c121657548cd0f7a18a3dc8bd16cdfb2abe74197320da9a56a3a529`  
Decoded flow rows: `130`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	ColumnComp.CC.Temperature.LowerLimit	5.0 [°C]	
	ColumnComp.CC.Temperature.UpperLimit	85 [°C]	
	ColumnComp.PrehtRight.TempCtrl	On	
	ColumnComp.PrehtRight.Temperature.Nominal	30.00 [°C]	
	ColumnComp.PrehtLeft.TempCtrl	On	
	PumpModule.Pump.%A.Equate	Water	
	PumpModule.Pump.Pressure.LowerLimit	0 [bar]	
	PumpModule.Pump.Pressure.UpperLimit	660 [bar]	
	PumpModule.Pump.MaximumFlowRampUp	Infinite	
	PumpModule.Pump.MaximumFlowRampDown	Infinite	
	ColumnComp.PrehtLeft.Temperature.Nominal	30.00 [°C]	
	ColumnComp.CC.ReadyTempDelta	0.5 [°C]	
	ColumnComp.CC.TempCtrl	On	
	ColumnComp.CC.Temperature.Nominal	70.0 [°C]	
	ColumnComp.CC.EquilibrationTime	0.5 [min]	
	PumpModule.Pump.Pump_Pressure.UseFilter	Off	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	1_2	
	ColumnComp.LowerValve.CurrentPosition	6_1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Variables.GenericBool1	0	
	Variables.GenericBool2	0	
	Variables.GenericFloat1	0	
0.000	Equilibration		
	PumpModule.Pump.Flow.Nominal	2.00000 [ml/min]	
	PumpModule.Pump.Curve	5	
0.000	InjectPreparation		
	Wait	ColumnComp.CC.TempReady AND PumpModule.Pump.Ready, Run=Hold	
0.000	StartRun		
	PumpModule.Pump.Pump_Pressure.AcqOn		
	ColumnComp.PrehtLeft_Temp.AcqOn		
	ColumnComp.PrehtRight_Temp.AcqOn		
	ColumnComp.PREH_L_Temp_Actual.AcqOn		
	ColumnComp.PREH_R_Temp_Actual.AcqOn		
	ColumnComp.PREH_L_HeaterTemp_Actual.AcqOn		
	ColumnComp.PREH_R_HeaterTemp_Actual.AcqOn		
	ColumnComp.PWM_LeftPreh.AcqOn		
	ColumnComp.PWM_RightPreh.AcqOn		
	ColumnComp.CC_Temp.AcqOn		
	VirtualChannel	PumpPressureVirtual, PumpModule.Pump.Pump_Pressure.Signal, Type=Digital, Unit="bar", Evaluate=Yes	
	Thermometer.Environment_Temperature.AcqOn		
Trigger		"Ping",	
	    Condition	Variables.GenericBool1=1 AND System.Retention>Variables.GenericFloat1 and system.Retention>10 and system.Retention<20	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.1	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	6_1	
	ColumnComp.LowerValve.CurrentPosition	1_2	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Log	ColumnComp.CC_Temp	
	Log	ColumnComp.PrehtLeft_Temp	
	Log	ColumnComp.PrehtRight_Temp	
	Delay	1	
	Variables.GenericBool1	0	
	Delay	0	
	Variables.GenericBool2	1	
End Trigger			
Trigger		"Pong",	
	    Condition	Variables.GenericBool2=1 AND System.Retention>Variables.GenericFloat1 and system.Retention>10 and system.Retention<20	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.1	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	1_2	
	ColumnComp.LowerValve.CurrentPosition	6_1	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Log	ColumnComp.CC_Temp	
	Log	ColumnComp.PrehtLeft_Temp	
	Log	ColumnComp.PrehtRight_Temp	
	Delay	1	
	Variables.GenericBool1	1	
	Delay	0	
	Variables.GenericBool2	0	
End Trigger			
0.000	Run	Duration = 20.000 [min]	
	PumpModule.Pump.Flow.Nominal	2.00000 [ml/min]	
	PumpModule.Pump.Curve	5	
	Variables.GenericBool1	1	
20.000			
Trigger		"bing",	
	    Condition	Variables.GenericBool1=1 AND System.Retention>Variables.GenericFloat1 and system.Retention>30 and system.Retention<35	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.05	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	6_1	
	ColumnComp.LowerValve.CurrentPosition	1_2	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Log	ColumnComp.CC_Temp	
	Log	ColumnComp.PrehtLeft_Temp	
	Log	ColumnComp.PrehtRight_Temp	
	Delay	1	
	Variables.GenericBool1	0	
	Delay	0	
	Variables.GenericBool2	1	
End Trigger			
Trigger		"bong",	
	    Condition	Variables.GenericBool2=1 AND System.Retention>Variables.GenericFloat1 and system.Retention>30 and system.Retention<35	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.05	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	1_2	
	ColumnComp.LowerValve.CurrentPosition	6_1	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Log	ColumnComp.CC_Temp	
	Log	ColumnComp.PrehtLeft_Temp	
	Log	ColumnComp.PrehtRight_Temp	
	Delay	1	
	Variables.GenericBool1	1	
	Delay	0	
	Variables.GenericBool2	0	
End Trigger			
45.500	StopRun		
	Variables.GenericBool1	0	
	Variables.GenericBool2	0	
	PumpModule.Pump.Flow.Nominal	2.00000 [ml/min]	
	PumpModule.Pump.Curve	5	
	PumpModule.Pump.Flow.Nominal	0.000000 [ml/min]	
	PumpModule.Pump.Curve	5	
	PumpModule.Pump.Pump_Pressure.AcqOff		
	ColumnComp.CC_Temp.AcqOff		
	ColumnComp.PrehtLeft_Temp.AcqOff		
	ColumnComp.PrehtRight_Temp.AcqOff		
	ColumnComp.PREH_L_Temp_Actual.AcqOff		
	ColumnComp.PREH_R_Temp_Actual.AcqOff		
	ColumnComp.PREH_L_HeaterTemp_Actual.AcqOff		
	ColumnComp.PREH_R_HeaterTemp_Actual.AcqOff		
	ColumnComp.PWM_LeftPreh.AcqOff		
	ColumnComp.PWM_RightPreh.AcqOff		
	Thermometer.Environment_Temperature.AcqOff		
	End		
```

<a id="m-tcc-stress-test-5s-preheater-box-pcc40c"></a>
## M-TCC-STRESS-TEST-5S-PREHEATER-BOX-PCC40C: Stress test_5s_Preheater Box_pcc40c

Applicable device evidence: **VH-STRESS**  
Source sequence(s): `VH-STRESS:Stress_VH_DVT013_20260529`  
Source SHA-256: `b94af4c4696d9fb868643d72a0b06636734f7fbed76d4b563d76483991cf73b4`  
Decoded flow rows: `131`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	ColumnComp.CC.Temperature.LowerLimit	5.0 [°C]	
	ColumnComp.CC.Temperature.UpperLimit	85 [°C]	
	ColumnComp.PrehtRight.TempCtrl	On	
	ColumnComp.PrehtRight.Temperature.Nominal	30.00 [°C]	
	ColumnComp.PrehtLeft.TempCtrl	On	
	ColumnComp.PCC.ReadyTempDelta	None	
	ColumnComp.PCC.Temperature.Nominal	40.00 [°C]	
	PumpModule.Pump.%A.Equate	Water	
	PumpModule.Pump.Pressure.LowerLimit	0 [bar]	
	PumpModule.Pump.Pressure.UpperLimit	660 [bar]	
	PumpModule.Pump.MaximumFlowRampUp	Infinite	
	PumpModule.Pump.MaximumFlowRampDown	Infinite	
	ColumnComp.PrehtLeft.Temperature.Nominal	30.00 [°C]	
	ColumnComp.CC.ReadyTempDelta	0.5 [°C]	
	ColumnComp.CC.TempCtrl	On	
	ColumnComp.CC.Temperature.Nominal	70.0 [°C]	
	ColumnComp.CC.EquilibrationTime	30 [min]	
	PumpModule.Pump.Pump_Pressure.UseFilter	Off	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	1_2	
	ColumnComp.LowerValve.CurrentPosition	6_1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Setting of regulation parameters for preheater simulator only		
	setting are not persistent - after reboot default parameters for real preheaters are set again automatically. However they will be reset at the end of the IM		
	ColumnComp.CmdString	Cmd="PREH.L.PID.Kp=10000"	
	ColumnComp.CmdString	Cmd="PREH.L.PID.Ki=1200"	
	ColumnComp.CmdString	Cmd="PREH.R.PID.Kp=10000"	
	ColumnComp.CmdString	Cmd="PREH.R.PID.Ki=1200"	
	Variables.GenericBool1	0	
	Variables.GenericBool2	0	
	Variables.GenericFloat1	0	
-30.000	Equilibration	Duration = 30.000 [min]	
	PumpModule.Pump.Flow.Nominal	2.00000 [ml/min]	
	PumpModule.Pump.Curve	5	
0.000	InjectPreparation		
	Wait	ColumnComp.CC.TempReady AND PumpModule.Pump.Ready, Run=Hold	
0.000	StartRun		
	PumpModule.Pump.Pump_Pressure.AcqOn		
	ColumnComp.PrehtLeft_Temp.AcqOn		
	ColumnComp.PrehtRight_Temp.AcqOn		
	ColumnComp.CC_Temp.AcqOn		
	VirtualChannel	PumpPressureVirtual, PumpModule.Pump.Pump_Pressure.Signal, Type=Digital, Unit="bar", Evaluate=Yes	
	Thermometer.Environment_Temperature.AcqOn		
Trigger		"Ping",	
	    Condition	Variables.GenericBool1=1 AND System.Retention>Variables.GenericFloat1 and system.Retention>10 and system.Retention<20	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.1	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	6_1	
	ColumnComp.LowerValve.CurrentPosition	1_2	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Log	ColumnComp.CC_Temp	
	Log	ColumnComp.PrehtLeft_Temp	
	Log	ColumnComp.PrehtRight_Temp	
	Delay	1	
	Variables.GenericBool1	0	
	Delay	0	
	Variables.GenericBool2	1	
End Trigger			
Trigger		"Pong",	
	    Condition	Variables.GenericBool2=1 AND System.Retention>Variables.GenericFloat1 and system.Retention>10 and system.Retention<20	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.1	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	1_2	
	ColumnComp.LowerValve.CurrentPosition	6_1	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Log	ColumnComp.CC_Temp	
	Log	ColumnComp.PrehtLeft_Temp	
	Log	ColumnComp.PrehtRight_Temp	
	Delay	1	
	Variables.GenericBool1	1	
	Delay	0	
	Variables.GenericBool2	0	
End Trigger			
0.000	Run	Duration = 20.000 [min]	
	PumpModule.Pump.Flow.Nominal	2.00000 [ml/min]	
	PumpModule.Pump.Curve	5	
	Variables.GenericBool1	1	
20.000			
Trigger		"bing",	
	    Condition	Variables.GenericBool1=1 AND System.Retention>Variables.GenericFloat1 and system.Retention>30 and system.Retention<35	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.05	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	6_1	
	ColumnComp.LowerValve.CurrentPosition	1_2	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Log	ColumnComp.CC_Temp	
	Log	ColumnComp.PrehtLeft_Temp	
	Log	ColumnComp.PrehtRight_Temp	
	Delay	1	
	Variables.GenericBool1	0	
	Delay	0	
	Variables.GenericBool2	1	
End Trigger			
Trigger		"bong",	
	    Condition	Variables.GenericBool2=1 AND System.Retention>Variables.GenericFloat1 and system.Retention>30 and system.Retention<35	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.05	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	1_2	
	ColumnComp.LowerValve.CurrentPosition	6_1	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Log	ColumnComp.CC_Temp	
	Log	ColumnComp.PrehtLeft_Temp	
	Log	ColumnComp.PrehtRight_Temp	
	Delay	1	
	Variables.GenericBool1	1	
	Delay	0	
	Variables.GenericBool2	0	
End Trigger			
45.500	StopRun		
	Variables.GenericBool1	0	
	Variables.GenericBool2	0	
	PumpModule.Pump.Flow.Nominal	2.00000 [ml/min]	
	PumpModule.Pump.Curve	5	
	PumpModule.Pump.Flow.Nominal	0.000000 [ml/min]	
	PumpModule.Pump.Curve	5	
	PumpModule.Pump.Pump_Pressure.AcqOff		
	ColumnComp.CC_Temp.AcqOff		
	ColumnComp.PrehtLeft_Temp.AcqOff		
	ColumnComp.PrehtRight_Temp.AcqOff		
	Reset of regulation parameters for preheater simulator		
	ColumnComp.CmdString	Cmd="PREH.L.PID.Kp=600000"	
	ColumnComp.CmdString	Cmd="PREH.L.PID.Ki=30000"	
	ColumnComp.CmdString	Cmd="PREH.R.PID.Kp=600000"	
	ColumnComp.CmdString	Cmd="PREH.R.PID.Ki=30000"	
	Thermometer.Environment_Temperature.AcqOff		
	End		
```

<a id="m-tcc-stress-test-5s-preheater-box-pcc60c"></a>
## M-TCC-STRESS-TEST-5S-PREHEATER-BOX-PCC60C: Stress test_5s_Preheater Box_pcc60c

Applicable device evidence: **VH-STRESS**  
Source sequence(s): `VH-STRESS:Stress_VH_DVT013_20260529`  
Source SHA-256: `827cd90fc63f7169527fd0b8aa52667e865ec2593e011d290fd8f2869096e197`  
Decoded flow rows: `131`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	ColumnComp.CC.Temperature.LowerLimit	5.0 [°C]	
	ColumnComp.CC.Temperature.UpperLimit	85 [°C]	
	ColumnComp.PrehtRight.TempCtrl	On	
	ColumnComp.PrehtRight.Temperature.Nominal	30.00 [°C]	
	ColumnComp.PrehtLeft.TempCtrl	On	
	ColumnComp.PCC.ReadyTempDelta	None	
	ColumnComp.PCC.Temperature.Nominal	70.00 [°C]	
	PumpModule.Pump.%A.Equate	Water	
	PumpModule.Pump.Pressure.LowerLimit	0 [bar]	
	PumpModule.Pump.Pressure.UpperLimit	660 [bar]	
	PumpModule.Pump.MaximumFlowRampUp	Infinite	
	PumpModule.Pump.MaximumFlowRampDown	Infinite	
	ColumnComp.PrehtLeft.Temperature.Nominal	30.00 [°C]	
	ColumnComp.CC.ReadyTempDelta	0.5 [°C]	
	ColumnComp.CC.TempCtrl	On	
	ColumnComp.CC.Temperature.Nominal	70.0 [°C]	
	ColumnComp.CC.EquilibrationTime	0.5 [min]	
	PumpModule.Pump.Pump_Pressure.UseFilter	Off	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	1_2	
	ColumnComp.LowerValve.CurrentPosition	6_1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Setting of regulation parameters for preheater simulator only		
	setting are not persistent - after reboot default parameters for real preheaters are set again automatically. However they will be reset at the end of the IM		
	ColumnComp.CmdString	Cmd="PREH.L.PID.Kp=10000"	
	ColumnComp.CmdString	Cmd="PREH.L.PID.Ki=1200"	
	ColumnComp.CmdString	Cmd="PREH.R.PID.Kp=10000"	
	ColumnComp.CmdString	Cmd="PREH.R.PID.Ki=1200"	
	Variables.GenericBool1	0	
	Variables.GenericBool2	0	
	Variables.GenericFloat1	0	
0.000	Equilibration		
	PumpModule.Pump.Flow.Nominal	2.00000 [ml/min]	
	PumpModule.Pump.Curve	5	
0.000	InjectPreparation		
	Wait	ColumnComp.CC.TempReady AND PumpModule.Pump.Ready, Run=Hold	
0.000	StartRun		
	PumpModule.Pump.Pump_Pressure.AcqOn		
	ColumnComp.PrehtLeft_Temp.AcqOn		
	ColumnComp.PrehtRight_Temp.AcqOn		
	ColumnComp.CC_Temp.AcqOn		
	VirtualChannel	PumpPressureVirtual, PumpModule.Pump.Pump_Pressure.Signal, Type=Digital, Unit="bar", Evaluate=Yes	
	Thermometer.Environment_Temperature.AcqOn		
Trigger		"Ping",	
	    Condition	Variables.GenericBool1=1 AND System.Retention>Variables.GenericFloat1 and system.Retention>10 and system.Retention<20	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.1	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	6_1	
	ColumnComp.LowerValve.CurrentPosition	1_2	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Log	ColumnComp.CC_Temp	
	Log	ColumnComp.PrehtLeft_Temp	
	Log	ColumnComp.PrehtRight_Temp	
	Delay	1	
	Variables.GenericBool1	0	
	Delay	0	
	Variables.GenericBool2	1	
End Trigger			
Trigger		"Pong",	
	    Condition	Variables.GenericBool2=1 AND System.Retention>Variables.GenericFloat1 and system.Retention>10 and system.Retention<20	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.1	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	1_2	
	ColumnComp.LowerValve.CurrentPosition	6_1	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Log	ColumnComp.CC_Temp	
	Log	ColumnComp.PrehtLeft_Temp	
	Log	ColumnComp.PrehtRight_Temp	
	Delay	1	
	Variables.GenericBool1	1	
	Delay	0	
	Variables.GenericBool2	0	
End Trigger			
0.000	Run	Duration = 20.000 [min]	
	PumpModule.Pump.Flow.Nominal	2.00000 [ml/min]	
	PumpModule.Pump.Curve	5	
	Variables.GenericBool1	1	
20.000			
Trigger		"bing",	
	    Condition	Variables.GenericBool1=1 AND System.Retention>Variables.GenericFloat1 and system.Retention>30 and system.Retention<35	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.05	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	6_1	
	ColumnComp.LowerValve.CurrentPosition	1_2	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Log	ColumnComp.CC_Temp	
	Log	ColumnComp.PrehtLeft_Temp	
	Log	ColumnComp.PrehtRight_Temp	
	Delay	1	
	Variables.GenericBool1	0	
	Delay	0	
	Variables.GenericBool2	1	
End Trigger			
Trigger		"bong",	
	    Condition	Variables.GenericBool2=1 AND System.Retention>Variables.GenericFloat1 and system.Retention>30 and system.Retention<35	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.05	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	1_2	
	ColumnComp.LowerValve.CurrentPosition	6_1	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Log	ColumnComp.CC_Temp	
	Log	ColumnComp.PrehtLeft_Temp	
	Log	ColumnComp.PrehtRight_Temp	
	Delay	1	
	Variables.GenericBool1	1	
	Delay	0	
	Variables.GenericBool2	0	
End Trigger			
45.500	StopRun		
	Variables.GenericBool1	0	
	Variables.GenericBool2	0	
	PumpModule.Pump.Flow.Nominal	2.00000 [ml/min]	
	PumpModule.Pump.Curve	5	
	PumpModule.Pump.Flow.Nominal	0.000000 [ml/min]	
	PumpModule.Pump.Curve	5	
	PumpModule.Pump.Pump_Pressure.AcqOff		
	ColumnComp.CC_Temp.AcqOff		
	ColumnComp.PrehtLeft_Temp.AcqOff		
	ColumnComp.PrehtRight_Temp.AcqOff		
	Reset of regulation parameters for preheater simulator		
	ColumnComp.CmdString	Cmd="PREH.L.PID.Kp=600000"	
	ColumnComp.CmdString	Cmd="PREH.L.PID.Ki=30000"	
	ColumnComp.CmdString	Cmd="PREH.R.PID.Kp=600000"	
	ColumnComp.CmdString	Cmd="PREH.R.PID.Ki=30000"	
	Thermometer.Environment_Temperature.AcqOff		
	End		
```

<a id="m-tcc-stress-test-5s-preheater-box-pcc70c"></a>
## M-TCC-STRESS-TEST-5S-PREHEATER-BOX-PCC70C: Stress test_5s_Preheater Box_pcc70c

Applicable device evidence: **VH-STRESS**  
Source sequence(s): `VH-STRESS:Stress_VH_DVT013_20260529`  
Source SHA-256: `5e48889900b4178df898af6c7d6dff6bea200422eb952ddec612b82645c47887`  
Decoded flow rows: `131`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	ColumnComp.CC.Temperature.LowerLimit	5.0 [°C]	
	ColumnComp.CC.Temperature.UpperLimit	85 [°C]	
	ColumnComp.PrehtRight.TempCtrl	On	
	ColumnComp.PrehtRight.Temperature.Nominal	30.00 [°C]	
	ColumnComp.PrehtLeft.TempCtrl	On	
	ColumnComp.PCC.ReadyTempDelta	None	
	ColumnComp.PCC.Temperature.Nominal	70.00 [°C]	
	PumpModule.Pump.%A.Equate	Water	
	PumpModule.Pump.Pressure.LowerLimit	0 [bar]	
	PumpModule.Pump.Pressure.UpperLimit	660 [bar]	
	PumpModule.Pump.MaximumFlowRampUp	Infinite	
	PumpModule.Pump.MaximumFlowRampDown	Infinite	
	ColumnComp.PrehtLeft.Temperature.Nominal	30.00 [°C]	
	ColumnComp.CC.ReadyTempDelta	0.5 [°C]	
	ColumnComp.CC.TempCtrl	On	
	ColumnComp.CC.Temperature.Nominal	70.0 [°C]	
	ColumnComp.CC.EquilibrationTime	0.5 [min]	
	PumpModule.Pump.Pump_Pressure.UseFilter	Off	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	1_2	
	ColumnComp.LowerValve.CurrentPosition	6_1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Setting of regulation parameters for preheater simulator only		
	setting are not persistent - after reboot default parameters for real preheaters are set again automatically. However they will be reset at the end of the IM		
	ColumnComp.CmdString	Cmd="PREH.L.PID.Kp=10000"	
	ColumnComp.CmdString	Cmd="PREH.L.PID.Ki=1200"	
	ColumnComp.CmdString	Cmd="PREH.R.PID.Kp=10000"	
	ColumnComp.CmdString	Cmd="PREH.R.PID.Ki=1200"	
	Variables.GenericBool1	0	
	Variables.GenericBool2	0	
	Variables.GenericFloat1	0	
0.000	Equilibration		
	PumpModule.Pump.Flow.Nominal	2.00000 [ml/min]	
	PumpModule.Pump.Curve	5	
0.000	InjectPreparation		
	Wait	ColumnComp.CC.TempReady AND PumpModule.Pump.Ready, Run=Hold	
0.000	StartRun		
	PumpModule.Pump.Pump_Pressure.AcqOn		
	ColumnComp.PrehtLeft_Temp.AcqOn		
	ColumnComp.PrehtRight_Temp.AcqOn		
	ColumnComp.CC_Temp.AcqOn		
	VirtualChannel	PumpPressureVirtual, PumpModule.Pump.Pump_Pressure.Signal, Type=Digital, Unit="bar", Evaluate=Yes	
	Thermometer.Environment_Temperature.AcqOn		
Trigger		"Ping",	
	    Condition	Variables.GenericBool1=1 AND System.Retention>Variables.GenericFloat1 and system.Retention>10 and system.Retention<20	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.1	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	6_1	
	ColumnComp.LowerValve.CurrentPosition	1_2	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Log	ColumnComp.CC_Temp	
	Log	ColumnComp.PrehtLeft_Temp	
	Log	ColumnComp.PrehtRight_Temp	
	Delay	1	
	Variables.GenericBool1	0	
	Delay	0	
	Variables.GenericBool2	1	
End Trigger			
Trigger		"Pong",	
	    Condition	Variables.GenericBool2=1 AND System.Retention>Variables.GenericFloat1 and system.Retention>10 and system.Retention<20	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.1	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	1_2	
	ColumnComp.LowerValve.CurrentPosition	6_1	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Log	ColumnComp.CC_Temp	
	Log	ColumnComp.PrehtLeft_Temp	
	Log	ColumnComp.PrehtRight_Temp	
	Delay	1	
	Variables.GenericBool1	1	
	Delay	0	
	Variables.GenericBool2	0	
End Trigger			
0.000	Run	Duration = 20.000 [min]	
	PumpModule.Pump.Flow.Nominal	2.00000 [ml/min]	
	PumpModule.Pump.Curve	5	
	Variables.GenericBool1	1	
20.000			
Trigger		"bing",	
	    Condition	Variables.GenericBool1=1 AND System.Retention>Variables.GenericFloat1 and system.Retention>30 and system.Retention<35	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.05	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	6_1	
	ColumnComp.LowerValve.CurrentPosition	1_2	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Log	ColumnComp.CC_Temp	
	Log	ColumnComp.PrehtLeft_Temp	
	Log	ColumnComp.PrehtRight_Temp	
	Delay	1	
	Variables.GenericBool1	0	
	Delay	0	
	Variables.GenericBool2	1	
End Trigger			
Trigger		"bong",	
	    Condition	Variables.GenericBool2=1 AND System.Retention>Variables.GenericFloat1 and system.Retention>30 and system.Retention<35	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.05	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	1_2	
	ColumnComp.LowerValve.CurrentPosition	6_1	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Log	ColumnComp.CC_Temp	
	Log	ColumnComp.PrehtLeft_Temp	
	Log	ColumnComp.PrehtRight_Temp	
	Delay	1	
	Variables.GenericBool1	1	
	Delay	0	
	Variables.GenericBool2	0	
End Trigger			
45.500	StopRun		
	Variables.GenericBool1	0	
	Variables.GenericBool2	0	
	PumpModule.Pump.Flow.Nominal	2.00000 [ml/min]	
	PumpModule.Pump.Curve	5	
	PumpModule.Pump.Flow.Nominal	0.000000 [ml/min]	
	PumpModule.Pump.Curve	5	
	PumpModule.Pump.Pump_Pressure.AcqOff		
	ColumnComp.CC_Temp.AcqOff		
	ColumnComp.PrehtLeft_Temp.AcqOff		
	ColumnComp.PrehtRight_Temp.AcqOff		
	Reset of regulation parameters for preheater simulator		
	ColumnComp.CmdString	Cmd="PREH.L.PID.Kp=600000"	
	ColumnComp.CmdString	Cmd="PREH.L.PID.Ki=30000"	
	ColumnComp.CmdString	Cmd="PREH.R.PID.Kp=600000"	
	ColumnComp.CmdString	Cmd="PREH.R.PID.Ki=30000"	
	Thermometer.Environment_Temperature.AcqOff		
	End		
```

<a id="m-tcc-stress-test-5s-preheater-box-pcc-off"></a>
## M-TCC-STRESS-TEST-5S-PREHEATER-BOX-PCC-OFF: Stress test_5s_Preheater Box_pcc_off

Applicable device evidence: **VH-STRESS**  
Source sequence(s): `VH-STRESS:Stress_VH_DVT013_20260529`  
Source SHA-256: `c0014697d046397c34b3f56d23a022106874fc516f898ea13721fc13e4f9a5af`  
Decoded flow rows: `125`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	ColumnComp.CC.Temperature.LowerLimit	5.0 [°C]	
	ColumnComp.CC.Temperature.UpperLimit	85 [°C]	
	ColumnComp.PrehtRight.TempCtrl	On	
	ColumnComp.PrehtRight.Temperature.Nominal	30.00 [°C]	
	ColumnComp.PrehtLeft.TempCtrl	On	
	ColumnComp.PCC.ReadyTempDelta	None	
	ColumnComp.PCC.Temperature.Nominal	Off	
	PumpModule.Pump.%A.Equate	Water	
	PumpModule.Pump.Pressure.LowerLimit	0 [bar]	
	PumpModule.Pump.Pressure.UpperLimit	660 [bar]	
	PumpModule.Pump.MaximumFlowRampUp	Infinite	
	PumpModule.Pump.MaximumFlowRampDown	Infinite	
	ColumnComp.PrehtLeft.Temperature.Nominal	30.00 [°C]	
	ColumnComp.CC.ReadyTempDelta	0.5 [°C]	
	ColumnComp.CC.TempCtrl	On	
	ColumnComp.CC.Temperature.Nominal	70.0 [°C]	
	ColumnComp.CC.EquilibrationTime	30 [min]	
	PumpModule.Pump.Pump_Pressure.UseFilter	Off	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	1_2	
	ColumnComp.LowerValve.CurrentPosition	6_1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Variables.GenericBool1	0	
	Variables.GenericBool2	0	
	Variables.GenericFloat1	0	
-30.000	Equilibration	Duration = 30.000 [min]	
	PumpModule.Pump.Flow.Nominal	2.00000 [ml/min]	
	PumpModule.Pump.Curve	5	
0.000	InjectPreparation		
	Wait	ColumnComp.CC.TempReady AND PumpModule.Pump.Ready, Run=Hold	
0.000	StartRun		
	PumpModule.Pump.Pump_Pressure.AcqOn		
	ColumnComp.PrehtLeft_Temp.AcqOn		
	ColumnComp.PrehtRight_Temp.AcqOn		
	ColumnComp.CC_Temp.AcqOn		
	VirtualChannel	PumpPressureVirtual, PumpModule.Pump.Pump_Pressure.Signal, Type=Digital, Unit="bar", Evaluate=Yes	
	Thermometer.Environment_Temperature.AcqOn		
Trigger		"Ping",	
	    Condition	Variables.GenericBool1=1 AND System.Retention>Variables.GenericFloat1 and system.Retention>10 and system.Retention<20	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.1	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	6_1	
	ColumnComp.LowerValve.CurrentPosition	1_2	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Log	ColumnComp.CC_Temp	
	Log	ColumnComp.PrehtLeft_Temp	
	Log	ColumnComp.PrehtRight_Temp	
	Delay	1	
	Variables.GenericBool1	0	
	Delay	0	
	Variables.GenericBool2	1	
End Trigger			
Trigger		"Pong",	
	    Condition	Variables.GenericBool2=1 AND System.Retention>Variables.GenericFloat1 and system.Retention>10 and system.Retention<20	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.1	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	1_2	
	ColumnComp.LowerValve.CurrentPosition	6_1	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Log	ColumnComp.CC_Temp	
	Log	ColumnComp.PrehtLeft_Temp	
	Log	ColumnComp.PrehtRight_Temp	
	Delay	1	
	Variables.GenericBool1	1	
	Delay	0	
	Variables.GenericBool2	0	
End Trigger			
0.000	Run	Duration = 20.000 [min]	
	PumpModule.Pump.Flow.Nominal	2.00000 [ml/min]	
	PumpModule.Pump.Curve	5	
	Variables.GenericBool1	1	
20.000			
Trigger		"bing",	
	    Condition	Variables.GenericBool1=1 AND System.Retention>Variables.GenericFloat1 and system.Retention>30 and system.Retention<35	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.05	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	6_1	
	ColumnComp.LowerValve.CurrentPosition	1_2	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Log	ColumnComp.CC_Temp	
	Log	ColumnComp.PrehtLeft_Temp	
	Log	ColumnComp.PrehtRight_Temp	
	Delay	1	
	Variables.GenericBool1	0	
	Delay	0	
	Variables.GenericBool2	1	
End Trigger			
Trigger		"bong",	
	    Condition	Variables.GenericBool2=1 AND System.Retention>Variables.GenericFloat1 and system.Retention>30 and system.Retention<35	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.05	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	1_2	
	ColumnComp.LowerValve.CurrentPosition	6_1	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Log	ColumnComp.CC_Temp	
	Log	ColumnComp.PrehtLeft_Temp	
	Log	ColumnComp.PrehtRight_Temp	
	Delay	1	
	Variables.GenericBool1	1	
	Delay	0	
	Variables.GenericBool2	0	
End Trigger			
45.500	StopRun		
	Variables.GenericBool1	0	
	Variables.GenericBool2	0	
	PumpModule.Pump.Flow.Nominal	2.00000 [ml/min]	
	PumpModule.Pump.Curve	5	
	PumpModule.Pump.Flow.Nominal	0.000000 [ml/min]	
	PumpModule.Pump.Curve	5	
	PumpModule.Pump.Pump_Pressure.AcqOff		
	ColumnComp.CC_Temp.AcqOff		
	ColumnComp.PrehtLeft_Temp.AcqOff		
	ColumnComp.PrehtRight_Temp.AcqOff		
	Reset of regulation parameters for preheater simulator		
	ColumnComp.CmdString	Cmd="PREH.L.PID.Kp=600000"	
	ColumnComp.CmdString	Cmd="PREH.L.PID.Ki=30000"	
	ColumnComp.CmdString	Cmd="PREH.R.PID.Kp=600000"	
	ColumnComp.CmdString	Cmd="PREH.R.PID.Ki=30000"	
	Thermometer.Environment_Temperature.AcqOff		
	End		
```

<a id="m-tcc-stress-test-5s-realpreheater-pcc-off"></a>
## M-TCC-STRESS-TEST-5S-REALPREHEATER-PCC-OFF: Stress test_5s_RealPreheater_pcc_off

Applicable device evidence: **VH-STRESS**  
Source sequence(s): `VH-STRESS:Stress_VH_DVT013_20260529`  
Source SHA-256: `c3e9366b033df3ea3b00471d8a30a8e8eec336f835446ecf5fd51a088aeaa43e`  
Decoded flow rows: `132`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	ColumnComp.CC.Temperature.LowerLimit	5.0 [°C]	
	ColumnComp.CC.Temperature.UpperLimit	85 [°C]	
	ColumnComp.PrehtRight.TempCtrl	On	
	ColumnComp.PrehtRight.Temperature.Nominal	30.00 [°C]	
	ColumnComp.PrehtRight.ReadyTempDelta	1.0 [°C]	
	ColumnComp.PrehtLeft.TempCtrl	On	
	ColumnComp.PrehtLeft.Temperature.Nominal	30.00 [°C]	
	ColumnComp.PrehtLeft.ReadyTempDelta	1.0 [°C]	
	IF VHTCC		
	ColumnComp.PCC.ReadyTempDelta = None		
	ColumnComp.PCC.TempCtrl = OFF		
	ColumnComp.PCC.Temperature.Nominal = off		
	ColumnComp.PCC.TempCtrl	Off	
	ColumnComp.PCC.ReadyTempDelta	None	
	PumpModule.Pump.%A.Equate	Water	
	PumpModule.Pump.Pressure.LowerLimit	0 [bar]	
	PumpModule.Pump.Pressure.UpperLimit	660 [bar]	
	PumpModule.Pump.MaximumFlowRampUp	Infinite	
	PumpModule.Pump.MaximumFlowRampDown	Infinite	
	ColumnComp.CC.TempCtrl	On	
	ColumnComp.CC.Temperature.Nominal	70.0 [°C]	
	PumpModule.Pump.Pump_Pressure.UseFilter	Off	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	6_1	
	ColumnComp.LowerValve.CurrentPosition	6_1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Variables.GenericBool1	0	
	Variables.GenericBool2	0	
	Variables.GenericFloat1	0	
-30.000	Equilibration	Duration = 30.000 [min]	
	PumpModule.Pump.Flow.Nominal	2.00000 [ml/min]	
	PumpModule.Pump.Curve	5	
0.000	InjectPreparation		
	ColumnComp.CC.Temperature.Nominal	70.0 [°C]	
	ColumnComp.CC.EquilibrationTime	0.5 [min]	
	ColumnComp.CC.ReadyTempDelta	0.5 [°C]	
	Wait	ColumnComp.CC.TempReady AND PumpModule.Pump.Ready, Run=Hold	
0.000	StartRun		
	PumpModule.Pump.Pump_Pressure.AcqOn		
	ColumnComp.PrehtLeft_Temp.AcqOn		
	ColumnComp.PrehtRight_Temp.AcqOn		
	ColumnComp.CC_Temp.AcqOn		
	VirtualChannel	PumpPressureVirtual, PumpModule.Pump.Pump_Pressure.Signal, Type=Digital, Unit="bar", Evaluate=Yes	
	Thermometer.Environment_Temperature.AcqOn		
Trigger		"Ping",	
	    Condition	Variables.GenericBool1=1 AND System.Retention>Variables.GenericFloat1 and system.Retention>10 and system.Retention<20	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.1	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	6_1	
	ColumnComp.LowerValve.CurrentPosition	1_2	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Log	ColumnComp.CC_Temp	
	Log	ColumnComp.PrehtLeft_Temp	
	Log	ColumnComp.PrehtRight_Temp	
	Delay	1	
	Variables.GenericBool1	0	
	Delay	0	
	Variables.GenericBool2	1	
End Trigger			
Trigger		"Pong",	
	    Condition	Variables.GenericBool2=1 AND System.Retention>Variables.GenericFloat1 and system.Retention>10 and system.Retention<20	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.1	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	1_2	
	ColumnComp.LowerValve.CurrentPosition	6_1	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Log	ColumnComp.CC_Temp	
	Log	ColumnComp.PrehtLeft_Temp	
	Log	ColumnComp.PrehtRight_Temp	
	Delay	1	
	Variables.GenericBool1	1	
	Delay	0	
	Variables.GenericBool2	0	
End Trigger			
0.000	Run	Duration = 20.000 [min]	
	PumpModule.Pump.Flow.Nominal	2.00000 [ml/min]	
	PumpModule.Pump.Curve	5	
	Variables.GenericBool1	1	
20.000			
Trigger		"bing",	
	    Condition	Variables.GenericBool1=1 AND System.Retention>Variables.GenericFloat1 and system.Retention>30 and system.Retention<35	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.05	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	6_1	
	ColumnComp.LowerValve.CurrentPosition	1_2	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Log	ColumnComp.CC_Temp	
	Log	ColumnComp.PrehtLeft_Temp	
	Log	ColumnComp.PrehtRight_Temp	
	Delay	1	
	Variables.GenericBool1	0	
	Delay	0	
	Variables.GenericBool2	1	
End Trigger			
Trigger		"bong",	
	    Condition	Variables.GenericBool2=1 AND System.Retention>Variables.GenericFloat1 and system.Retention>30 and system.Retention<35	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.05	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	1_2	
	ColumnComp.LowerValve.CurrentPosition	6_1	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Log	ColumnComp.CC_Temp	
	Log	ColumnComp.PrehtLeft_Temp	
	Log	ColumnComp.PrehtRight_Temp	
	Delay	1	
	Variables.GenericBool1	1	
	Delay	0	
	Variables.GenericBool2	0	
End Trigger			
45.500	StopRun		
	Variables.GenericBool1	0	
	Variables.GenericBool2	0	
	PumpModule.Pump.Flow.Nominal	2.00000 [ml/min]	
	PumpModule.Pump.Curve	5	
	PumpModule.Pump.Flow.Nominal	0.000000 [ml/min]	
	PumpModule.Pump.Curve	5	
	PumpModule.Pump.Pump_Pressure.AcqOff		
	ColumnComp.CC_Temp.AcqOff		
	ColumnComp.PrehtLeft_Temp.AcqOff		
	ColumnComp.PrehtRight_Temp.AcqOff		
	Reset of regulation parameters for preheater simulator		
	ColumnComp.CmdString	Cmd="PREH.L.PID.Kp=600000"	
	ColumnComp.CmdString	Cmd="PREH.L.PID.Ki=30000"	
	ColumnComp.CmdString	Cmd="PREH.R.PID.Kp=600000"	
	ColumnComp.CmdString	Cmd="PREH.R.PID.Ki=30000"	
	Thermometer.Environment_Temperature.AcqOff		
	End		
```

<a id="m-tcc-stress-test-5s-realpreheater-pcc-off-10min-equibration"></a>
## M-TCC-STRESS-TEST-5S-REALPREHEATER-PCC-OFF-10MIN-EQUIBRATION: Stress test_5s_RealPreheater_pcc_off_10min equibration

Applicable device evidence: **VH-STRESS**  
Source sequence(s): `VH-STRESS:Stress_VH_DVT013_20260529`  
Source SHA-256: `a8ae0bbbfb0e1357ce3b3898479d82f9770ef7d9df06ceb713edbd2af2f7dcbd`  
Decoded flow rows: `131`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	ColumnComp.CC.Temperature.LowerLimit	5.0 [°C]	
	ColumnComp.CC.Temperature.UpperLimit	85 [°C]	
	ColumnComp.PrehtRight.TempCtrl	On	
	ColumnComp.PrehtRight.Temperature.Nominal	30.00 [°C]	
	ColumnComp.PrehtRight.ReadyTempDelta	1.0 [°C]	
	ColumnComp.PrehtLeft.TempCtrl	On	
	ColumnComp.PrehtLeft.Temperature.Nominal	30.00 [°C]	
	ColumnComp.PrehtLeft.ReadyTempDelta	1.0 [°C]	
	IF VHTCC		
	ColumnComp.PCC.ReadyTempDelta = None		
	ColumnComp.PCC.Temperature.Nominal = off		
	ColumnComp.PCC.TempCtrl	Off	
	ColumnComp.PCC.ReadyTempDelta	None	
	PumpModule.Pump.%A.Equate	Water	
	PumpModule.Pump.Pressure.LowerLimit	0 [bar]	
	PumpModule.Pump.Pressure.UpperLimit	660 [bar]	
	PumpModule.Pump.MaximumFlowRampUp	Infinite	
	PumpModule.Pump.MaximumFlowRampDown	Infinite	
	ColumnComp.CC.TempCtrl	On	
	ColumnComp.CC.Temperature.Nominal	70.0 [°C]	
	PumpModule.Pump.Pump_Pressure.UseFilter	Off	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	6_1	
	ColumnComp.LowerValve.CurrentPosition	6_1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Variables.GenericBool1	0	
	Variables.GenericBool2	0	
	Variables.GenericFloat1	0	
-10.000	Equilibration	Duration = 10.000 [min]	
	PumpModule.Pump.Flow.Nominal	2.00000 [ml/min]	
	PumpModule.Pump.Curve	5	
0.000	InjectPreparation		
	ColumnComp.CC.Temperature.Nominal	70.0 [°C]	
	ColumnComp.CC.EquilibrationTime	0.5 [min]	
	ColumnComp.CC.ReadyTempDelta	0.5 [°C]	
	Wait	ColumnComp.CC.TempReady AND PumpModule.Pump.Ready, Run=Hold	
0.000	StartRun		
	PumpModule.Pump.Pump_Pressure.AcqOn		
	ColumnComp.PrehtLeft_Temp.AcqOn		
	ColumnComp.PrehtRight_Temp.AcqOn		
	ColumnComp.CC_Temp.AcqOn		
	VirtualChannel	PumpPressureVirtual, PumpModule.Pump.Pump_Pressure.Signal, Type=Digital, Unit="bar", Evaluate=Yes	
	Thermometer.Environment_Temperature.AcqOn		
Trigger		"Ping",	
	    Condition	Variables.GenericBool1=1 AND System.Retention>Variables.GenericFloat1 and system.Retention>10 and system.Retention<20	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.1	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	6_1	
	ColumnComp.LowerValve.CurrentPosition	1_2	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Log	ColumnComp.CC_Temp	
	Log	ColumnComp.PrehtLeft_Temp	
	Log	ColumnComp.PrehtRight_Temp	
	Delay	1	
	Variables.GenericBool1	0	
	Delay	0	
	Variables.GenericBool2	1	
End Trigger			
Trigger		"Pong",	
	    Condition	Variables.GenericBool2=1 AND System.Retention>Variables.GenericFloat1 and system.Retention>10 and system.Retention<20	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.1	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	1_2	
	ColumnComp.LowerValve.CurrentPosition	6_1	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Log	ColumnComp.CC_Temp	
	Log	ColumnComp.PrehtLeft_Temp	
	Log	ColumnComp.PrehtRight_Temp	
	Delay	1	
	Variables.GenericBool1	1	
	Delay	0	
	Variables.GenericBool2	0	
End Trigger			
0.000	Run	Duration = 20.000 [min]	
	PumpModule.Pump.Flow.Nominal	2.00000 [ml/min]	
	PumpModule.Pump.Curve	5	
	Variables.GenericBool1	1	
20.000			
Trigger		"bing",	
	    Condition	Variables.GenericBool1=1 AND System.Retention>Variables.GenericFloat1 and system.Retention>30 and system.Retention<35	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.05	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	6_1	
	ColumnComp.LowerValve.CurrentPosition	1_2	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Log	ColumnComp.CC_Temp	
	Log	ColumnComp.PrehtLeft_Temp	
	Log	ColumnComp.PrehtRight_Temp	
	Delay	1	
	Variables.GenericBool1	0	
	Delay	0	
	Variables.GenericBool2	1	
End Trigger			
Trigger		"bong",	
	    Condition	Variables.GenericBool2=1 AND System.Retention>Variables.GenericFloat1 and system.Retention>30 and system.Retention<35	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.05	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	1_2	
	ColumnComp.LowerValve.CurrentPosition	6_1	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Log	ColumnComp.CC_Temp	
	Log	ColumnComp.PrehtLeft_Temp	
	Log	ColumnComp.PrehtRight_Temp	
	Delay	1	
	Variables.GenericBool1	1	
	Delay	0	
	Variables.GenericBool2	0	
End Trigger			
45.500	StopRun		
	Variables.GenericBool1	0	
	Variables.GenericBool2	0	
	PumpModule.Pump.Flow.Nominal	2.00000 [ml/min]	
	PumpModule.Pump.Curve	5	
	PumpModule.Pump.Flow.Nominal	0.000000 [ml/min]	
	PumpModule.Pump.Curve	5	
	PumpModule.Pump.Pump_Pressure.AcqOff		
	ColumnComp.CC_Temp.AcqOff		
	ColumnComp.PrehtLeft_Temp.AcqOff		
	ColumnComp.PrehtRight_Temp.AcqOff		
	Reset of regulation parameters for preheater simulator		
	ColumnComp.CmdString	Cmd="PREH.L.PID.Kp=600000"	
	ColumnComp.CmdString	Cmd="PREH.L.PID.Ki=30000"	
	ColumnComp.CmdString	Cmd="PREH.R.PID.Kp=600000"	
	ColumnComp.CmdString	Cmd="PREH.R.PID.Ki=30000"	
	Thermometer.Environment_Temperature.AcqOff		
	End		
```

<a id="m-tcc-stress-test-5s-realpreheater-pcc-off-no-equibration"></a>
## M-TCC-STRESS-TEST-5S-REALPREHEATER-PCC-OFF-NO-EQUIBRATION: Stress test_5s_RealPreheater_pcc_off_no equibration

Applicable device evidence: **VH-STRESS**  
Source sequence(s): `VH-STRESS:Stress_VH_DVT013_20260529`  
Source SHA-256: `86bf99661307a4083990feece32c41dfddec5edafe98973a9f6bf9205f1f9df5`  
Decoded flow rows: `126`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	ColumnComp.CC.Temperature.LowerLimit	5.0 [°C]	
	ColumnComp.CC.Temperature.UpperLimit	85 [°C]	
	ColumnComp.PrehtRight.TempCtrl	On	
	ColumnComp.PrehtRight.Temperature.Nominal	30.00 [°C]	
	ColumnComp.PrehtRight.ReadyTempDelta	1.0 [°C]	
	ColumnComp.PrehtLeft.TempCtrl	On	
	ColumnComp.PrehtLeft.Temperature.Nominal	30.00 [°C]	
	ColumnComp.PrehtLeft.ReadyTempDelta	1.0 [°C]	
	IF VHTCC		
	ColumnComp.PCC.ReadyTempDelta = None		
	ColumnComp.PCC.Temperature.Nominal = off		
	PumpModule.Pump.%A.Equate	Water	
	PumpModule.Pump.Pressure.LowerLimit	0 [bar]	
	PumpModule.Pump.Pressure.UpperLimit	660 [bar]	
	PumpModule.Pump.MaximumFlowRampUp	Infinite	
	PumpModule.Pump.MaximumFlowRampDown	Infinite	
	ColumnComp.CC.TempCtrl	On	
	ColumnComp.CC.Temperature.Nominal	70.0 [°C]	
	PumpModule.Pump.Pump_Pressure.UseFilter	Off	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	6_1	
	ColumnComp.LowerValve.CurrentPosition	6_1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Variables.GenericBool1	0	
	Variables.GenericBool2	0	
	Variables.GenericFloat1	0	
0.000	InjectPreparation		
	ColumnComp.CC.Temperature.Nominal	70.0 [°C]	
	ColumnComp.CC.EquilibrationTime	0.5 [min]	
	ColumnComp.CC.ReadyTempDelta	0.5 [°C]	
	Wait	ColumnComp.CC.TempReady AND PumpModule.Pump.Ready, Run=Hold	
0.000	StartRun		
	PumpModule.Pump.Pump_Pressure.AcqOn		
	ColumnComp.PrehtLeft_Temp.AcqOn		
	ColumnComp.PrehtRight_Temp.AcqOn		
	ColumnComp.CC_Temp.AcqOn		
	VirtualChannel	PumpPressureVirtual, PumpModule.Pump.Pump_Pressure.Signal, Type=Digital, Unit="bar", Evaluate=Yes	
	Thermometer.Environment_Temperature.AcqOn		
Trigger		"Ping",	
	    Condition	Variables.GenericBool1=1 AND System.Retention>Variables.GenericFloat1 and system.Retention>10 and system.Retention<20	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.1	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	6_1	
	ColumnComp.LowerValve.CurrentPosition	1_2	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Log	ColumnComp.CC_Temp	
	Log	ColumnComp.PrehtLeft_Temp	
	Log	ColumnComp.PrehtRight_Temp	
	Delay	1	
	Variables.GenericBool1	0	
	Delay	0	
	Variables.GenericBool2	1	
End Trigger			
Trigger		"Pong",	
	    Condition	Variables.GenericBool2=1 AND System.Retention>Variables.GenericFloat1 and system.Retention>10 and system.Retention<20	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.1	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	1_2	
	ColumnComp.LowerValve.CurrentPosition	6_1	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Log	ColumnComp.CC_Temp	
	Log	ColumnComp.PrehtLeft_Temp	
	Log	ColumnComp.PrehtRight_Temp	
	Delay	1	
	Variables.GenericBool1	1	
	Delay	0	
	Variables.GenericBool2	0	
End Trigger			
0.000	Run	Duration = 20.000 [min]	
	PumpModule.Pump.Flow.Nominal	2.00000 [ml/min]	
	PumpModule.Pump.Curve	5	
	Variables.GenericBool1	1	
20.000			
Trigger		"bing",	
	    Condition	Variables.GenericBool1=1 AND System.Retention>Variables.GenericFloat1 and system.Retention>30 and system.Retention<35	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.05	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	6_1	
	ColumnComp.LowerValve.CurrentPosition	1_2	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Log	ColumnComp.CC_Temp	
	Log	ColumnComp.PrehtLeft_Temp	
	Log	ColumnComp.PrehtRight_Temp	
	Delay	1	
	Variables.GenericBool1	0	
	Delay	0	
	Variables.GenericBool2	1	
End Trigger			
Trigger		"bong",	
	    Condition	Variables.GenericBool2=1 AND System.Retention>Variables.GenericFloat1 and system.Retention>30 and system.Retention<35	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.05	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	1_2	
	ColumnComp.LowerValve.CurrentPosition	6_1	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Log	ColumnComp.CC_Temp	
	Log	ColumnComp.PrehtLeft_Temp	
	Log	ColumnComp.PrehtRight_Temp	
	Delay	1	
	Variables.GenericBool1	1	
	Delay	0	
	Variables.GenericBool2	0	
End Trigger			
45.500	StopRun		
	Variables.GenericBool1	0	
	Variables.GenericBool2	0	
	PumpModule.Pump.Flow.Nominal	2.00000 [ml/min]	
	PumpModule.Pump.Curve	5	
	PumpModule.Pump.Flow.Nominal	0.000000 [ml/min]	
	PumpModule.Pump.Curve	5	
	PumpModule.Pump.Pump_Pressure.AcqOff		
	ColumnComp.CC_Temp.AcqOff		
	ColumnComp.PrehtLeft_Temp.AcqOff		
	ColumnComp.PrehtRight_Temp.AcqOff		
	Reset of regulation parameters for preheater simulator		
	ColumnComp.CmdString	Cmd="PREH.L.PID.Kp=600000"	
	ColumnComp.CmdString	Cmd="PREH.L.PID.Ki=30000"	
	ColumnComp.CmdString	Cmd="PREH.R.PID.Kp=600000"	
	ColumnComp.CmdString	Cmd="PREH.R.PID.Ki=30000"	
	Thermometer.Environment_Temperature.AcqOff		
	End		
```

<a id="m-tcc-stress-test-5s-realpreheater-pcc-on"></a>
## M-TCC-STRESS-TEST-5S-REALPREHEATER-PCC-ON: Stress test_5s_RealPreheater_pcc_on

Applicable device evidence: **VH-STRESS**  
Source sequence(s): `VH-STRESS:Stress_VH_DVT013_20260529`  
Source SHA-256: `66f0d5788d8933767f2d5cf95510746ceff5995e08223fc37e4aae4098c667e4`  
Decoded flow rows: `133`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	ColumnComp.CC.Temperature.LowerLimit	5.0 [°C]	
	ColumnComp.CC.Temperature.UpperLimit	85 [°C]	
	ColumnComp.PrehtRight.TempCtrl	On	
	ColumnComp.PrehtRight.Temperature.Nominal	30.00 [°C]	
	ColumnComp.PrehtRight.ReadyTempDelta	1.0 [°C]	
	ColumnComp.PrehtLeft.TempCtrl	On	
	ColumnComp.PrehtLeft.Temperature.Nominal	30.00 [°C]	
	ColumnComp.PrehtLeft.ReadyTempDelta	1.0 [°C]	
	IF VHTCC		
	ColumnComp.PCC.ReadyTempDelta = None		
	ColumnComp.PCC.TempCtrl = OFF		
	ColumnComp.PCC.Temperature.Nominal = off		
	ColumnComp.PCC.TempCtrl	On	
	ColumnComp.PCC.ReadyTempDelta	None	
	ColumnComp.PCC.Temperature.Nominal	40	
	PumpModule.Pump.%A.Equate	Water	
	PumpModule.Pump.Pressure.LowerLimit	0 [bar]	
	PumpModule.Pump.Pressure.UpperLimit	660 [bar]	
	PumpModule.Pump.MaximumFlowRampUp	Infinite	
	PumpModule.Pump.MaximumFlowRampDown	Infinite	
	ColumnComp.CC.TempCtrl	On	
	ColumnComp.CC.Temperature.Nominal	70.0 [°C]	
	PumpModule.Pump.Pump_Pressure.UseFilter	Off	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	6_1	
	ColumnComp.LowerValve.CurrentPosition	6_1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Variables.GenericBool1	0	
	Variables.GenericBool2	0	
	Variables.GenericFloat1	0	
-30.000	Equilibration	Duration = 30.000 [min]	
	PumpModule.Pump.Flow.Nominal	2.00000 [ml/min]	
	PumpModule.Pump.Curve	5	
0.000	InjectPreparation		
	ColumnComp.CC.Temperature.Nominal	70.0 [°C]	
	ColumnComp.CC.EquilibrationTime	0.5 [min]	
	ColumnComp.CC.ReadyTempDelta	0.5 [°C]	
	Wait	ColumnComp.CC.TempReady AND PumpModule.Pump.Ready, Run=Hold	
0.000	StartRun		
	PumpModule.Pump.Pump_Pressure.AcqOn		
	ColumnComp.PrehtLeft_Temp.AcqOn		
	ColumnComp.PrehtRight_Temp.AcqOn		
	ColumnComp.CC_Temp.AcqOn		
	VirtualChannel	PumpPressureVirtual, PumpModule.Pump.Pump_Pressure.Signal, Type=Digital, Unit="bar", Evaluate=Yes	
	Thermometer.Environment_Temperature.AcqOn		
Trigger		"Ping",	
	    Condition	Variables.GenericBool1=1 AND System.Retention>Variables.GenericFloat1 and system.Retention>10 and system.Retention<20	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.1	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	6_1	
	ColumnComp.LowerValve.CurrentPosition	1_2	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Log	ColumnComp.CC_Temp	
	Log	ColumnComp.PrehtLeft_Temp	
	Log	ColumnComp.PrehtRight_Temp	
	Delay	1	
	Variables.GenericBool1	0	
	Delay	0	
	Variables.GenericBool2	1	
End Trigger			
Trigger		"Pong",	
	    Condition	Variables.GenericBool2=1 AND System.Retention>Variables.GenericFloat1 and system.Retention>10 and system.Retention<20	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.1	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	1_2	
	ColumnComp.LowerValve.CurrentPosition	6_1	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Log	ColumnComp.CC_Temp	
	Log	ColumnComp.PrehtLeft_Temp	
	Log	ColumnComp.PrehtRight_Temp	
	Delay	1	
	Variables.GenericBool1	1	
	Delay	0	
	Variables.GenericBool2	0	
End Trigger			
0.000	Run	Duration = 20.000 [min]	
	PumpModule.Pump.Flow.Nominal	2.00000 [ml/min]	
	PumpModule.Pump.Curve	5	
	Variables.GenericBool1	1	
20.000			
Trigger		"bing",	
	    Condition	Variables.GenericBool1=1 AND System.Retention>Variables.GenericFloat1 and system.Retention>30 and system.Retention<35	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.05	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	6_1	
	ColumnComp.LowerValve.CurrentPosition	1_2	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Log	ColumnComp.CC_Temp	
	Log	ColumnComp.PrehtLeft_Temp	
	Log	ColumnComp.PrehtRight_Temp	
	Delay	1	
	Variables.GenericBool1	0	
	Delay	0	
	Variables.GenericBool2	1	
End Trigger			
Trigger		"bong",	
	    Condition	Variables.GenericBool2=1 AND System.Retention>Variables.GenericFloat1 and system.Retention>30 and system.Retention<35	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.05	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	1_2	
	ColumnComp.LowerValve.CurrentPosition	6_1	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Log	ColumnComp.CC_Temp	
	Log	ColumnComp.PrehtLeft_Temp	
	Log	ColumnComp.PrehtRight_Temp	
	Delay	1	
	Variables.GenericBool1	1	
	Delay	0	
	Variables.GenericBool2	0	
End Trigger			
45.500	StopRun		
	Variables.GenericBool1	0	
	Variables.GenericBool2	0	
	PumpModule.Pump.Flow.Nominal	2.00000 [ml/min]	
	PumpModule.Pump.Curve	5	
	PumpModule.Pump.Flow.Nominal	0.000000 [ml/min]	
	PumpModule.Pump.Curve	5	
	PumpModule.Pump.Pump_Pressure.AcqOff		
	ColumnComp.CC_Temp.AcqOff		
	ColumnComp.PrehtLeft_Temp.AcqOff		
	ColumnComp.PrehtRight_Temp.AcqOff		
	Reset of regulation parameters for preheater simulator		
	ColumnComp.CmdString	Cmd="PREH.L.PID.Kp=600000"	
	ColumnComp.CmdString	Cmd="PREH.L.PID.Ki=30000"	
	ColumnComp.CmdString	Cmd="PREH.R.PID.Kp=600000"	
	ColumnComp.CmdString	Cmd="PREH.R.PID.Ki=30000"	
	Thermometer.Environment_Temperature.AcqOff		
	End		
```

<a id="m-tcc-stress-test-5s-realpreheater-pcc-on-10min-equibration"></a>
## M-TCC-STRESS-TEST-5S-REALPREHEATER-PCC-ON-10MIN-EQUIBRATION: Stress test_5s_RealPreheater_pcc_ON_10min equibration

Applicable device evidence: **VH-STRESS**  
Source sequence(s): `VH-STRESS:Stress_VH_DVT013_20260529`  
Source SHA-256: `080841adbf78ee929a0f5412e18fe809fc45192ef773634c138f72c98c1a1f1e`  
Decoded flow rows: `132`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	ColumnComp.CC.Temperature.LowerLimit	5.0 [°C]	
	ColumnComp.CC.Temperature.UpperLimit	85 [°C]	
	ColumnComp.PrehtRight.TempCtrl	On	
	ColumnComp.PrehtRight.Temperature.Nominal	30.00 [°C]	
	ColumnComp.PrehtRight.ReadyTempDelta	1.0 [°C]	
	ColumnComp.PrehtLeft.TempCtrl	On	
	ColumnComp.PrehtLeft.Temperature.Nominal	30.00 [°C]	
	ColumnComp.PrehtLeft.ReadyTempDelta	1.0 [°C]	
	IF VHTCC		
	ColumnComp.PCC.ReadyTempDelta = None		
	ColumnComp.PCC.Temperature.Nominal = off		
	ColumnComp.PCC.TempCtrl	On	
	ColumnComp.PCC.ReadyTempDelta	None	
	ColumnComp.PCC.Temperature.Nominal	40	
	PumpModule.Pump.%A.Equate	Water	
	PumpModule.Pump.Pressure.LowerLimit	0 [bar]	
	PumpModule.Pump.Pressure.UpperLimit	660 [bar]	
	PumpModule.Pump.MaximumFlowRampUp	Infinite	
	PumpModule.Pump.MaximumFlowRampDown	Infinite	
	ColumnComp.CC.TempCtrl	On	
	ColumnComp.CC.Temperature.Nominal	70.0 [°C]	
	PumpModule.Pump.Pump_Pressure.UseFilter	Off	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	6_1	
	ColumnComp.LowerValve.CurrentPosition	6_1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Variables.GenericBool1	0	
	Variables.GenericBool2	0	
	Variables.GenericFloat1	0	
-10.000	Equilibration	Duration = 10.000 [min]	
	PumpModule.Pump.Flow.Nominal	2.00000 [ml/min]	
	PumpModule.Pump.Curve	5	
0.000	InjectPreparation		
	ColumnComp.CC.Temperature.Nominal	70.0 [°C]	
	ColumnComp.CC.EquilibrationTime	0.5 [min]	
	ColumnComp.CC.ReadyTempDelta	0.5 [°C]	
	Wait	ColumnComp.CC.TempReady AND PumpModule.Pump.Ready, Run=Hold	
0.000	StartRun		
	PumpModule.Pump.Pump_Pressure.AcqOn		
	ColumnComp.PrehtLeft_Temp.AcqOn		
	ColumnComp.PrehtRight_Temp.AcqOn		
	ColumnComp.CC_Temp.AcqOn		
	VirtualChannel	PumpPressureVirtual, PumpModule.Pump.Pump_Pressure.Signal, Type=Digital, Unit="bar", Evaluate=Yes	
	Thermometer.Environment_Temperature.AcqOn		
Trigger		"Ping",	
	    Condition	Variables.GenericBool1=1 AND System.Retention>Variables.GenericFloat1 and system.Retention>10 and system.Retention<20	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.1	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	6_1	
	ColumnComp.LowerValve.CurrentPosition	1_2	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Log	ColumnComp.CC_Temp	
	Log	ColumnComp.PrehtLeft_Temp	
	Log	ColumnComp.PrehtRight_Temp	
	Delay	1	
	Variables.GenericBool1	0	
	Delay	0	
	Variables.GenericBool2	1	
End Trigger			
Trigger		"Pong",	
	    Condition	Variables.GenericBool2=1 AND System.Retention>Variables.GenericFloat1 and system.Retention>10 and system.Retention<20	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.1	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	1_2	
	ColumnComp.LowerValve.CurrentPosition	6_1	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Log	ColumnComp.CC_Temp	
	Log	ColumnComp.PrehtLeft_Temp	
	Log	ColumnComp.PrehtRight_Temp	
	Delay	1	
	Variables.GenericBool1	1	
	Delay	0	
	Variables.GenericBool2	0	
End Trigger			
0.000	Run	Duration = 20.000 [min]	
	PumpModule.Pump.Flow.Nominal	2.00000 [ml/min]	
	PumpModule.Pump.Curve	5	
	Variables.GenericBool1	1	
20.000			
Trigger		"bing",	
	    Condition	Variables.GenericBool1=1 AND System.Retention>Variables.GenericFloat1 and system.Retention>30 and system.Retention<35	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.05	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	6_1	
	ColumnComp.LowerValve.CurrentPosition	1_2	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Log	ColumnComp.CC_Temp	
	Log	ColumnComp.PrehtLeft_Temp	
	Log	ColumnComp.PrehtRight_Temp	
	Delay	1	
	Variables.GenericBool1	0	
	Delay	0	
	Variables.GenericBool2	1	
End Trigger			
Trigger		"bong",	
	    Condition	Variables.GenericBool2=1 AND System.Retention>Variables.GenericFloat1 and system.Retention>30 and system.Retention<35	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.05	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	1_2	
	ColumnComp.LowerValve.CurrentPosition	6_1	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Log	ColumnComp.CC_Temp	
	Log	ColumnComp.PrehtLeft_Temp	
	Log	ColumnComp.PrehtRight_Temp	
	Delay	1	
	Variables.GenericBool1	1	
	Delay	0	
	Variables.GenericBool2	0	
End Trigger			
45.500	StopRun		
	Variables.GenericBool1	0	
	Variables.GenericBool2	0	
	PumpModule.Pump.Flow.Nominal	2.00000 [ml/min]	
	PumpModule.Pump.Curve	5	
	PumpModule.Pump.Flow.Nominal	0.000000 [ml/min]	
	PumpModule.Pump.Curve	5	
	PumpModule.Pump.Pump_Pressure.AcqOff		
	ColumnComp.CC_Temp.AcqOff		
	ColumnComp.PrehtLeft_Temp.AcqOff		
	ColumnComp.PrehtRight_Temp.AcqOff		
	Reset of regulation parameters for preheater simulator		
	ColumnComp.CmdString	Cmd="PREH.L.PID.Kp=600000"	
	ColumnComp.CmdString	Cmd="PREH.L.PID.Ki=30000"	
	ColumnComp.CmdString	Cmd="PREH.R.PID.Kp=600000"	
	ColumnComp.CmdString	Cmd="PREH.R.PID.Ki=30000"	
	Thermometer.Environment_Temperature.AcqOff		
	End		
```

<a id="m-tcc-stress-test-test"></a>
## M-TCC-STRESS-TEST-TEST: stress test_test

Applicable device evidence: **VH-STRESS**  
Source sequence(s): `VH-STRESS:Stress_VH_DVT013_20260529`  
Source SHA-256: `9f58389f3b72c394ba10d695eec48f0e98147989c523d76da4729ed822604b60`  
Decoded flow rows: `130`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	ColumnComp.CC.Temperature.LowerLimit	5.0 [°C]	
	ColumnComp.CC.Temperature.UpperLimit	85 [°C]	
	ColumnComp.PrehtRight.TempCtrl	On	
	ColumnComp.PrehtRight.Temperature.Nominal	30.00 [°C]	
	ColumnComp.PrehtLeft.TempCtrl	On	
	PumpModule.Pump.%A.Equate	Water	
	PumpModule.Pump.Pressure.LowerLimit	0 [bar]	
	PumpModule.Pump.Pressure.UpperLimit	660 [bar]	
	PumpModule.Pump.MaximumFlowRampUp	Infinite	
	PumpModule.Pump.MaximumFlowRampDown	Infinite	
	ColumnComp.PrehtLeft.Temperature.Nominal	30.00 [°C]	
	ColumnComp.CC.ReadyTempDelta	0.5 [°C]	
	ColumnComp.CC.TempCtrl	On	
	ColumnComp.CC.Temperature.Nominal	70.0 [°C]	
	ColumnComp.CC.EquilibrationTime	0.5 [min]	
	PumpModule.Pump.Pump_Pressure.UseFilter	Off	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	1_2	
	ColumnComp.LowerValve.CurrentPosition	6_1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Variables.GenericBool1	0	
	Variables.GenericBool2	0	
	Variables.GenericFloat1	0	
0.000	Equilibration		
	PumpModule.Pump.Flow.Nominal	2.00000 [ml/min]	
	PumpModule.Pump.Curve	5	
0.000	InjectPreparation		
	Wait	ColumnComp.CC.TempReady AND PumpModule.Pump.Ready, Run=Hold	
0.000	StartRun		
	PumpModule.Pump.Pump_Pressure.AcqOn		
	ColumnComp.PrehtLeft_Temp.AcqOn		
	ColumnComp.PrehtRight_Temp.AcqOn		
	ColumnComp.PREH_L_Temp_Actual.AcqOn		
	ColumnComp.PREH_R_Temp_Actual.AcqOn		
	ColumnComp.PREH_L_HeaterTemp_Actual.AcqOn		
	ColumnComp.PREH_R_HeaterTemp_Actual.AcqOn		
	ColumnComp.PWM_LeftPreh.AcqOn		
	ColumnComp.PWM_RightPreh.AcqOn		
	ColumnComp.CC_Temp.AcqOn		
	VirtualChannel	PumpPressureVirtual, PumpModule.Pump.Pump_Pressure.Signal, Type=Digital, Unit="bar", Evaluate=Yes	
	Thermometer.Environment_Temperature.AcqOn		
Trigger		"Ping",	
	    Condition	Variables.GenericBool1=1 AND System.Retention>Variables.GenericFloat1	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.1	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	6_1	
	ColumnComp.LowerValve.CurrentPosition	1_2	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Log	ColumnComp.CC_Temp	
	Log	ColumnComp.PrehtLeft_Temp	
	Log	ColumnComp.PrehtRight_Temp	
	Delay	1	
	Variables.GenericBool1	0	
	Delay	0	
	Variables.GenericBool2	1	
End Trigger			
Trigger		"Pong",	
	    Condition	Variables.GenericBool2=1 AND System.Retention>Variables.GenericFloat1	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.1	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	1_2	
	ColumnComp.LowerValve.CurrentPosition	6_1	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Log	ColumnComp.CC_Temp	
	Log	ColumnComp.PrehtLeft_Temp	
	Log	ColumnComp.PrehtRight_Temp	
	Delay	1	
	Variables.GenericBool1	1	
	Delay	0	
	Variables.GenericBool2	0	
End Trigger			
0.000	Run	Duration = 20.000 [min]	
	PumpModule.Pump.Flow.Nominal	2.00000 [ml/min]	
	PumpModule.Pump.Curve	5	
	Variables.GenericBool1	1	
20.000			
Trigger		"bing",	
	    Condition	Variables.GenericBool1=1 AND System.Retention>Variables.GenericFloat1 and system.Retention>30 and system.Retention<35	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.05	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	6_1	
	ColumnComp.LowerValve.CurrentPosition	1_2	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Log	ColumnComp.CC_Temp	
	Log	ColumnComp.PrehtLeft_Temp	
	Log	ColumnComp.PrehtRight_Temp	
	Delay	1	
	Variables.GenericBool1	0	
	Delay	0	
	Variables.GenericBool2	1	
End Trigger			
Trigger		"bong",	
	    Condition	Variables.GenericBool2=1 AND System.Retention>Variables.GenericFloat1 and system.Retention>30 and system.Retention<35	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.05	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	1_2	
	ColumnComp.LowerValve.CurrentPosition	6_1	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Log	ColumnComp.CC_Temp	
	Log	ColumnComp.PrehtLeft_Temp	
	Log	ColumnComp.PrehtRight_Temp	
	Delay	1	
	Variables.GenericBool1	1	
	Delay	0	
	Variables.GenericBool2	0	
End Trigger			
45.500	StopRun		
	Variables.GenericBool1	0	
	Variables.GenericBool2	0	
	PumpModule.Pump.Flow.Nominal	2.00000 [ml/min]	
	PumpModule.Pump.Curve	5	
	PumpModule.Pump.Flow.Nominal	0.000000 [ml/min]	
	PumpModule.Pump.Curve	5	
	PumpModule.Pump.Pump_Pressure.AcqOff		
	ColumnComp.CC_Temp.AcqOff		
	ColumnComp.PrehtLeft_Temp.AcqOff		
	ColumnComp.PrehtRight_Temp.AcqOff		
	ColumnComp.PREH_L_Temp_Actual.AcqOff		
	ColumnComp.PREH_R_Temp_Actual.AcqOff		
	ColumnComp.PREH_L_HeaterTemp_Actual.AcqOff		
	ColumnComp.PREH_R_HeaterTemp_Actual.AcqOff		
	ColumnComp.PWM_LeftPreh.AcqOff		
	ColumnComp.PWM_RightPreh.AcqOff		
	Thermometer.Environment_Temperature.AcqOff		
	End		
```

<a id="m-tcc-synchron1"></a>
## M-TCC-SYNCHRON1: Synchron1

Applicable device evidence: **VH-STRESS**  
Source sequence(s): `VH-STRESS:Stress_VH_DVT013_20260529`  
Source SHA-256: `3f8b9ca20d6cf2fe465410edea58db192c4ab5f83f9995efb59da11b50b1d39e`  
Decoded flow rows: `72`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	ColumnComp.CC.TempCtrl	On	
	ColumnComp.CC.Temperature.Nominal	30.0 [°C]	
	ColumnComp.CC.Temperature.LowerLimit	5.0 [°C]	
	ColumnComp.CC.Temperature.UpperLimit	85 [°C]	
	ColumnComp.CC.EquilibrationTime	0.5 [min]	
	ColumnComp.CC.ReadyTempDelta	0.5 [°C]	
	PumpModule.Pump.%A.Equate	Water	
	PumpModule.Pump.Pressure.LowerLimit	0 [bar]	
	PumpModule.Pump.Pressure.UpperLimit	660 [bar]	
	PumpModule.Pump.MaximumFlowRampUp	Infinite	
	PumpModule.Pump.MaximumFlowRampDown	Infinite	
	PumpModule.Pump.Pump_Pressure.UseFilter	Off	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	1_2	
	ColumnComp.LowerValve.CurrentPosition	1_2	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Variables.GenericBool1	0	
	Variables.GenericBool2	0	
	Variables.GenericFloat1	0	
0.000	Equilibration		
	PumpModule.Pump.Flow.Nominal	1.00000 [ml/min]	
	PumpModule.Pump.Curve	5	
0.000	InjectPreparation		
	Wait	ColumnComp.CC.TempReady AND PumpModule.Pump.Ready, Run=Hold	
0.000	StartRun		
	PumpModule.Pump.Pump_Pressure.AcqOn		
	ColumnComp.CC_Temp.AcqOn		
	VirtualChannel	PumpPressureVirtual, PumpModule.Pump.Pump_Pressure.Signal, Type=Digital, Unit="bar", Evaluate=Yes	
	Thermometer.Lab_Temperature.AcqOn		
Trigger		"Ping",	
	    Condition	Variables.GenericBool1=1 AND System.Retention>Variables.GenericFloat1	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.5	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	6_1	
	ColumnComp.LowerValve.CurrentPosition	6_1	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Delay	1	
	Variables.GenericBool1	0	
	Delay	1	
	Variables.GenericBool2	1	
End Trigger			
Trigger		"Pong",	
	    Condition	Variables.GenericBool2=1 AND System.Retention>Variables.GenericFloat1	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.5	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	1_2	
	ColumnComp.LowerValve.CurrentPosition	1_2	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Delay	1	
	Variables.GenericBool1	1	
	Delay	1	
	Variables.GenericBool2	0	
End Trigger			
0.000	Run	Duration = 20.500 [min]	
	PumpModule.Pump.Flow.Nominal	1.00000 [ml/min]	
	PumpModule.Pump.Curve	5	
	Variables.GenericBool1	1	
20.500	StopRun		
	Variables.GenericBool1	0	
	Variables.GenericBool2	0	
	PumpModule.Pump.Flow.Nominal	1.00000 [ml/min]	
	PumpModule.Pump.Curve	5	
	PumpModule.Pump.Flow.Nominal	0.000000 [ml/min]	
	PumpModule.Pump.Curve	5	
	PumpModule.Pump.Pump_Pressure.AcqOff		
	ColumnComp.CC_Temp.AcqOff		
	Thermometer.Lab_Temperature.AcqOff		
	End		
```

<a id="m-tcc-synchron10"></a>
## M-TCC-SYNCHRON10: Synchron10

Applicable device evidence: **VH-STRESS**  
Source sequence(s): `VH-STRESS:Stress_VH_DVT013_20260529`  
Source SHA-256: `498ffee2d8fa34ea1b3d83f9edc4d065baac74d65ff010210e180a9a90a1f0e2`  
Decoded flow rows: `72`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	ColumnComp.CC.TempCtrl	On	
	ColumnComp.CC.Temperature.Nominal	30.0 [°C]	
	ColumnComp.CC.Temperature.LowerLimit	5.0 [°C]	
	ColumnComp.CC.Temperature.UpperLimit	85 [°C]	
	ColumnComp.CC.EquilibrationTime	0.5 [min]	
	ColumnComp.CC.ReadyTempDelta	0.5 [°C]	
	PumpModule.Pump.%A.Equate	Water	
	PumpModule.Pump.Pressure.LowerLimit	0 [bar]	
	PumpModule.Pump.Pressure.UpperLimit	660 [bar]	
	PumpModule.Pump.MaximumFlowRampUp	Infinite	
	PumpModule.Pump.MaximumFlowRampDown	Infinite	
	PumpModule.Pump.Pump_Pressure.UseFilter	Off	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	1_2	
	ColumnComp.LowerValve.CurrentPosition	1_2	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Variables.GenericBool1	0	
	Variables.GenericBool2	0	
	Variables.GenericFloat1	0	
0.000	Equilibration		
	PumpModule.Pump.Flow.Nominal	10 [ml/min]	
	PumpModule.Pump.Curve	5	
0.000	InjectPreparation		
	Wait	ColumnComp.CC.TempReady AND PumpModule.Pump.Ready, Run=Hold	
0.000	StartRun		
	PumpModule.Pump.Pump_Pressure.AcqOn		
	ColumnComp.CC_Temp.AcqOn		
	VirtualChannel	PumpPressureVirtual, PumpModule.Pump.Pump_Pressure.Signal, Type=Digital, Unit="bar", Evaluate=Yes	
	Thermometer.Lab_Temperature.AcqOn		
Trigger		"Ping",	
	    Condition	Variables.GenericBool1=1 AND System.Retention>Variables.GenericFloat1	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.5	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	6_1	
	ColumnComp.LowerValve.CurrentPosition	6_1	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Delay	1	
	Variables.GenericBool1	0	
	Delay	1	
	Variables.GenericBool2	1	
End Trigger			
Trigger		"Pong",	
	    Condition	Variables.GenericBool2=1 AND System.Retention>Variables.GenericFloat1	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.5	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	1_2	
	ColumnComp.LowerValve.CurrentPosition	1_2	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Delay	1	
	Variables.GenericBool1	1	
	Delay	1	
	Variables.GenericBool2	0	
End Trigger			
0.000	Run	Duration = 20.500 [min]	
	PumpModule.Pump.Flow.Nominal	10 [ml/min]	
	PumpModule.Pump.Curve	5	
	Variables.GenericBool1	1	
20.500	StopRun		
	Variables.GenericBool1	0	
	Variables.GenericBool2	0	
	PumpModule.Pump.Flow.Nominal	10 [ml/min]	
	PumpModule.Pump.Curve	5	
	PumpModule.Pump.Flow.Nominal	0.000000 [ml/min]	
	PumpModule.Pump.Curve	5	
	PumpModule.Pump.Pump_Pressure.AcqOff		
	ColumnComp.CC_Temp.AcqOff		
	Thermometer.Lab_Temperature.AcqOff		
	End		
```

<a id="m-tcc-synchron8"></a>
## M-TCC-SYNCHRON8: Synchron8

Applicable device evidence: **VH-STRESS**  
Source sequence(s): `VH-STRESS:Stress_VH_DVT013_20260529`  
Source SHA-256: `b07b5885f11e7cf884f2c2cec78f65262d1c0b91c1a5f19d5b31dd79e5fe1904`  
Decoded flow rows: `89`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	ColumnComp.CC.TempCtrl	On	
	ColumnComp.CC.Temperature.Nominal	70.0 [°C]	
	ColumnComp.CC.Temperature.LowerLimit	5.0 [°C]	
	ColumnComp.CC.Temperature.UpperLimit	85 [°C]	
	ColumnComp.CC.EquilibrationTime	0.5 [min]	
	ColumnComp.CC.ReadyTempDelta	0.5 [°C]	
	PumpModule.Pump.%A.Equate	Water	
	PumpModule.Pump.Pressure.LowerLimit	0 [bar]	
	PumpModule.Pump.Pressure.UpperLimit	660 [bar]	
	PumpModule.Pump.MaximumFlowRampUp	Infinite	
	PumpModule.Pump.MaximumFlowRampDown	Infinite	
	PumpModule.Pump.Pump_Pressure.UseFilter	Off	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	1_2	
	ColumnComp.LowerValve.CurrentPosition	1_2	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Variables.GenericBool1	0	
	Variables.GenericBool2	0	
	Variables.GenericFloat1	0	
-5.000	Equilibration	Duration = 5.000 [min]	
	PumpModule.Pump.Flow.Nominal	2.00000 [ml/min]	
	PumpModule.Pump.Curve	5	
0.000	InjectPreparation		
	Wait	ColumnComp.CC.TempReady AND PumpModule.Pump.Ready, Run=Hold	
0.000	StartRun		
	PumpModule.Pump.Pump_Pressure.AcqOn		
	ColumnComp.PrehtLeft_Temp.AcqOn		
	ColumnComp.PrehtRight_Temp.AcqOn		
	ColumnComp.PREH_L_Temp_Actual.AcqOn		
	ColumnComp.PREH_R_Temp_Actual.AcqOn		
	ColumnComp.PREH_L_HeaterTemp_Actual.AcqOn		
	ColumnComp.PREH_R_HeaterTemp_Actual.AcqOn		
	ColumnComp.PWM_LeftPreh.AcqOn		
	ColumnComp.PWM_RightPreh.AcqOn		
	ColumnComp.CC_Temp.AcqOn		
	ColumnComp.CC_Temp.AcqOn		
	VirtualChannel	PumpPressureVirtual, PumpModule.Pump.Pump_Pressure.Signal, Type=Digital, Unit="bar", Evaluate=Yes	
	Thermometer.Environment_Temperature.AcqOn		
Trigger		"Ping",	
	    Condition	Variables.GenericBool1=1 AND System.Retention>Variables.GenericFloat1 AND system.Retention<10	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.5	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	6_1	
	ColumnComp.LowerValve.CurrentPosition	6_1	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Delay	1	
	Variables.GenericBool1	0	
	Delay	1	
	Variables.GenericBool2	1	
End Trigger			
Trigger		"Pong",	
	    Condition	Variables.GenericBool2=1 AND System.Retention>Variables.GenericFloat1 and system.Retention<10	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.5	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	1_2	
	ColumnComp.LowerValve.CurrentPosition	1_2	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Delay	1	
	Variables.GenericBool1	1	
	Delay	1	
	Variables.GenericBool2	0	
End Trigger			
0.000	Run	Duration = 20.500 [min]	
	PumpModule.Pump.Flow.Nominal	2.00000 [ml/min]	
	PumpModule.Pump.Curve	5	
	Variables.GenericBool1	1	
20.500	StopRun		
	Variables.GenericBool1	0	
	Variables.GenericBool2	0	
	PumpModule.Pump.Flow.Nominal	2.00000 [ml/min]	
	PumpModule.Pump.Curve	5	
	PumpModule.Pump.Flow.Nominal	0.000000 [ml/min]	
	PumpModule.Pump.Curve	5	
	PumpModule.Pump.Pump_Pressure.AcqOff		
	ColumnComp.CC_Temp.AcqOff		
	ColumnComp.PrehtLeft_Temp.AcqOff		
	ColumnComp.PrehtRight_Temp.AcqOff		
	ColumnComp.PREH_L_Temp_Actual.AcqOff		
	ColumnComp.PREH_R_Temp_Actual.AcqOff		
	ColumnComp.PREH_L_HeaterTemp_Actual.AcqOff		
	ColumnComp.PREH_R_HeaterTemp_Actual.AcqOff		
	ColumnComp.PWM_LeftPreh.AcqOff		
	ColumnComp.PWM_RightPreh.AcqOff		
	Thermometer.Environment_Temperature.AcqOff		
	End		
```

<a id="m-tcc-synchron8-5"></a>
## M-TCC-SYNCHRON8-5: Synchron8_5

Applicable device evidence: **VH-STRESS**  
Source sequence(s): `VH-STRESS:Stress_VH_DVT013_20260529`  
Source SHA-256: `9736ca33509d29df50ef05903b68a82156190e3be7f2112aab63b1613ef73c42`  
Decoded flow rows: `72`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	ColumnComp.CC.TempCtrl	On	
	ColumnComp.CC.Temperature.Nominal	30.0 [°C]	
	ColumnComp.CC.Temperature.LowerLimit	5.0 [°C]	
	ColumnComp.CC.Temperature.UpperLimit	85 [°C]	
	ColumnComp.CC.EquilibrationTime	0.5 [min]	
	ColumnComp.CC.ReadyTempDelta	0.5 [°C]	
	PumpModule.Pump.%A.Equate	Water	
	PumpModule.Pump.Pressure.LowerLimit	0 [bar]	
	PumpModule.Pump.Pressure.UpperLimit	660 [bar]	
	PumpModule.Pump.MaximumFlowRampUp	Infinite	
	PumpModule.Pump.MaximumFlowRampDown	Infinite	
	PumpModule.Pump.Pump_Pressure.UseFilter	Off	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	1_2	
	ColumnComp.LowerValve.CurrentPosition	1_2	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Variables.GenericBool1	0	
	Variables.GenericBool2	0	
	Variables.GenericFloat1	0	
0.000	Equilibration		
	PumpModule.Pump.Flow.Nominal	8.500000 [ml/min]	
	PumpModule.Pump.Curve	5	
0.000	InjectPreparation		
	Wait	ColumnComp.CC.TempReady AND PumpModule.Pump.Ready, Run=Hold	
0.000	StartRun		
	PumpModule.Pump.Pump_Pressure.AcqOn		
	ColumnComp.CC_Temp.AcqOn		
	VirtualChannel	PumpPressureVirtual, PumpModule.Pump.Pump_Pressure.Signal, Type=Digital, Unit="bar", Evaluate=Yes	
	Thermometer.Lab_Temperature.AcqOn		
Trigger		"Ping",	
	    Condition	Variables.GenericBool1=1 AND System.Retention>Variables.GenericFloat1	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.5	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	6_1	
	ColumnComp.LowerValve.CurrentPosition	6_1	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Delay	1	
	Variables.GenericBool1	0	
	Delay	1	
	Variables.GenericBool2	1	
End Trigger			
Trigger		"Pong",	
	    Condition	Variables.GenericBool2=1 AND System.Retention>Variables.GenericFloat1	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.5	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	1_2	
	ColumnComp.LowerValve.CurrentPosition	1_2	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Delay	1	
	Variables.GenericBool1	1	
	Delay	1	
	Variables.GenericBool2	0	
End Trigger			
0.000	Run	Duration = 20.500 [min]	
	PumpModule.Pump.Flow.Nominal	8.500000 [ml/min]	
	PumpModule.Pump.Curve	5	
	Variables.GenericBool1	1	
20.500	StopRun		
	Variables.GenericBool1	0	
	Variables.GenericBool2	0	
	PumpModule.Pump.Flow.Nominal	8.500000 [ml/min]	
	PumpModule.Pump.Curve	5	
	PumpModule.Pump.Flow.Nominal	0.000000 [ml/min]	
	PumpModule.Pump.Curve	5	
	PumpModule.Pump.Pump_Pressure.AcqOff		
	ColumnComp.CC_Temp.AcqOff		
	Thermometer.Lab_Temperature.AcqOff		
	End		
```

<a id="m-tcc-synchron9-5"></a>
## M-TCC-SYNCHRON9-5: Synchron9_5

Applicable device evidence: **VH-STRESS**  
Source sequence(s): `VH-STRESS:Stress_VH_DVT013_20260529`  
Source SHA-256: `5c445a5bde56ece8c50555c70a53cf9e1984994be9e4faf0a147e312f6f584bb`  
Decoded flow rows: `72`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	ColumnComp.CC.TempCtrl	On	
	ColumnComp.CC.Temperature.Nominal	30.0 [°C]	
	ColumnComp.CC.Temperature.LowerLimit	5.0 [°C]	
	ColumnComp.CC.Temperature.UpperLimit	85 [°C]	
	ColumnComp.CC.EquilibrationTime	0.5 [min]	
	ColumnComp.CC.ReadyTempDelta	0.5 [°C]	
	PumpModule.Pump.%A.Equate	Water	
	PumpModule.Pump.Pressure.LowerLimit	0 [bar]	
	PumpModule.Pump.Pressure.UpperLimit	660 [bar]	
	PumpModule.Pump.MaximumFlowRampUp	Infinite	
	PumpModule.Pump.MaximumFlowRampDown	Infinite	
	PumpModule.Pump.Pump_Pressure.UseFilter	Off	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	1_2	
	ColumnComp.LowerValve.CurrentPosition	1_2	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Variables.GenericBool1	0	
	Variables.GenericBool2	0	
	Variables.GenericFloat1	0	
0.000	Equilibration		
	PumpModule.Pump.Flow.Nominal	9.5 [ml/min]	
	PumpModule.Pump.Curve	5	
0.000	InjectPreparation		
	Wait	ColumnComp.CC.TempReady AND PumpModule.Pump.Ready, Run=Hold	
0.000	StartRun		
	PumpModule.Pump.Pump_Pressure.AcqOn		
	ColumnComp.CC_Temp.AcqOn		
	VirtualChannel	PumpPressureVirtual, PumpModule.Pump.Pump_Pressure.Signal, Type=Digital, Unit="bar", Evaluate=Yes	
	Thermometer.Lab_Temperature.AcqOn		
Trigger		"Ping",	
	    Condition	Variables.GenericBool1=1 AND System.Retention>Variables.GenericFloat1	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.5	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	6_1	
	ColumnComp.LowerValve.CurrentPosition	6_1	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Delay	1	
	Variables.GenericBool1	0	
	Delay	1	
	Variables.GenericBool2	1	
End Trigger			
Trigger		"Pong",	
	    Condition	Variables.GenericBool2=1 AND System.Retention>Variables.GenericFloat1	
	    TrueTime	0.1	
	    Delay	0	
	    AllowImmediateExecution	Yes	
	Variables.GenericFloat1	System.Retention+0.5	
	Delay	1	
	ColumnComp.UpperValve.CurrentPosition	1_2	
	ColumnComp.LowerValve.CurrentPosition	1_2	
	Delay	1	
	Log	ColumnComp.UpperValve.CurrentPosition	
	Log	ColumnComp.LowerValve.CurrentPosition	
	Delay	1	
	Variables.GenericBool1	1	
	Delay	1	
	Variables.GenericBool2	0	
End Trigger			
0.000	Run	Duration = 20.500 [min]	
	PumpModule.Pump.Flow.Nominal	9.5 [ml/min]	
	PumpModule.Pump.Curve	5	
	Variables.GenericBool1	1	
20.500	StopRun		
	Variables.GenericBool1	0	
	Variables.GenericBool2	0	
	PumpModule.Pump.Flow.Nominal	9.5 [ml/min]	
	PumpModule.Pump.Curve	5	
	PumpModule.Pump.Flow.Nominal	0.000000 [ml/min]	
	PumpModule.Pump.Curve	5	
	PumpModule.Pump.Pump_Pressure.AcqOff		
	ColumnComp.CC_Temp.AcqOff		
	Thermometer.Lab_Temperature.AcqOff		
	End		
```

<a id="m-tcc-heat-cool-va"></a>
## M-TCC-HEAT-COOL-VA: TEMP_HEAT_UP_DOWN_20_50_20

Applicable device evidence: **VA**  
Source sequence(s): `VA:0000003`  
Source SHA-256: `3a1cb1d6bbcf11ad0a343aaecd83489331399e5536c7096b77962008bd25710e`  
Decoded flow rows: `170`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	=========================================================================================		
	IM to measure HeatUp time from 20°C to 50°C and CoolDown time from 50°C to 20°C of the Vanquish VH-C10-A, VC-C10-A and VA-C10-A		
	=========================================================================================		
	HPLC-System:		
	-----------		
	VH-C10-A, VC-C10-A or VA-C10-A		
-0.700	Equilibration	Duration = 0.700 [min]	
	Different total pages counts are used for VH-C10-A and VA-C10-A (no PCC). This is set here		
If		ColumnComp.ModelNo="VH-C10-A"	
	    Variables.GenericLong9	12	
	    Delay	1	[Val_FOQ_CM7_ekugelma_07-Jul-2020]: OK
	    Log	GenericLong9	
Else If		ColumnComp.ModelNo="VC-C10-A" OR ColumnComp.ModelNo="VA-C10-A"	
	    Variables.GenericLong9	10	
	    Delay	1	[Val_FOQ_CM7_ekugelma_07-Jul-2020]: OK
	    Log	GenericLong9	
Else			
	    Message	Column compartment model unknown, please reinspect in production!	
	    System.AbortQueue		
End If			
	=========================================================================================		
	Parameters valid for the whole test.		
	=========================================================================================		
	If the difference between nominal and actual temperature is larger than ReadyTempDelta, the oven is not ready.		
	ColumnComp.CC.ReadyTempDelta	0.5 [°C]	
	The Ready property will become Ready only if the difference between the actual and the nominal temperature will not exceed the ReadyTempDelta for the  time interval specified by EquilibrationTime.		
	ColumnComp.CC.EquilibrationTime	0.5 [min]	
	The VTCC controls the temperature only, if TempCtrl is set to ON.		
	ColumnComp.CC.TempCtrl	On	
	Adjusts FanSpeed and switches operating mode		
	ColumnComp.CC.Mode	StillAir	
	Generic variables  to activate Trigger		
	Variables.GenericLong0	0	
	Variables.GenericLong1	0	
	Variables.GenericLong2	0	
	Variables.GenericLong3	0	
	Initialize Retention Times used during IM		
	RetTimes.RetTime1	0	
	RetTimes.RetTime2	0	
	RetTimes.RetTime3	0	
	RetTimes.RetTime4	0	
	RetTimes.RetTime5	0	
	RetTimes.RetTime6	0	
	=========================================================================================		
	Settings for the all channels offered for the column compartment by the driver.		
	Also debug channels are aqcuired.		
	=========================================================================================		
	Column commpartment		
	ColumnComp.CC_U_Temp_Actual.Data_Collection_Rate	20	
	ColumnComp.CC_L_Temp_Actual.Data_Collection_Rate	20	
	ColumnComp.CC_UCTL_TempRear_Actual.Data_Collection_Rate	20	
	ColumnComp.PWM_CCU_A.Data_Collection_Rate	20	
	ColumnComp.PWM_CCU_B.Data_Collection_Rate	20	
	ColumnComp.PWM_CCL_A.Data_Collection_Rate	20	
	ColumnComp.PWM_CCL_B.Data_Collection_Rate	20	
	ColumnComp.Fan_Rear_ActualRPM.Data_Collection_Rate	20	
	Leak Sensors		
	ColumnComp.LEDBoard_LeakDiff.Data_Collection_Rate	20	
	ColumnComp.LEDBoard_A13.Data_Collection_Rate	20	
	ColumnComp.LEDBoard_A14.Data_Collection_Rate	20	
	ColumnComp.Oven_Gas_MuteTimeRemain.Data_Collection_Rate	20	
	=========================================================================================		
	Start Temperature		
	=========================================================================================		
	ColumnComp.CC.Temperature.Nominal	17.0	As the specification for the heat up/ cool down times is given for a temperature range of +/- 1°C the start temperature should be reached during data aquisition. Therfore the temperature is set below the starting temperature
0.000	InjectPreparation		
	Wait	CC.TempReady	
0.000	StartRun		
	ColumnComp.CC_Temp.AcqOn		
	ColumnComp.CC_U_Temp_Actual.AcqOn		
	ColumnComp.CC_L_Temp_Actual.AcqOn		
	ColumnComp.CC_UCTL_TempRear_Actual.AcqOn		
	ColumnComp.PWM_CCU_A.AcqOn		
	ColumnComp.PWM_CCU_B.AcqOn		
	ColumnComp.PWM_CCL_A.AcqOn		
	ColumnComp.PWM_CCL_B.AcqOn		
	ColumnComp.Fan_Rear_ActualRPM.AcqOn		
	External measured temperatures		
	Thermometer1.ExtTemp_UpperCC.AcqOn		
	Thermometer1.ExtTemp_LowerCC.AcqOn		
	Thermometer.Environment_Temperature.AcqOn		
	Leak Sensor Evaluation		
	ColumnComp.LEDBoard_LeakDiff.AcqOn		
	ColumnComp.LEDBoard_A13.AcqOn		
	ColumnComp.LEDBoard_A14.AcqOn		
	ColumnComp.Oven_Gas_MuteTimeRemain.AcqOn		
0.000	Run	Duration = 240.000 [min]	
0.700	ColumnComp.CC.Temperature.Nominal	20.0	
	Trigger "T_Start_Ext" and "T_Start_Int" ensure that the evaluation of heat up and cool down time are starting from the same equilibration conditions (T +/- 1 °C, True Time: 120 sec for external and internal temperature signals)		
1.000			
Trigger		"T_Start_Ext",	
	    Condition	ExtTemp_UpperCC<=21.0 AND ExtTemp_UpperCC>=19.0 AND CC.Temperature.Nominal=20 AND Variables.GenericLong0=0	
	    TrueTime	120	
	    Limit	1	
	    Hysteresis	0	
	    AllowImmediateExecution	No	
	Variables.GenericLong3	1	Activation of trigger "T_UP"
End Trigger			
Trigger		"T_Start_Int",	
	    Condition	CC.Temperature.Value<=21.0 AND CC.Temperature.Value>=19.0 AND CC.Temperature.Nominal=20 AND Variables.GenericLong0=0	
	    TrueTime	120	
	    Limit	1	
	    Hysteresis	0	
	    AllowImmediateExecution	No	
	Variables.GenericLong2	1	Activation of trigger "T_UP"
End Trigger			
	Trigger for heating up the CC from 20 to 50 °C after equilibration		
Trigger		"T_UP",	
	    Condition	Variables.GenericLong2=1 AND Variables.GenericLong3=1	
	    TrueTime	30	
	    Limit	1	
	    Hysteresis	0	
	    AllowImmediateExecution	No	
	ColumnComp.CC.Temperature.Nominal	50.0 [°C]	
	RetTimes.RetTime1	System.Retention	
	Variables.GenericLong0	1	
End Trigger			
	Trigger for evaluation of HeatUp Time based on external temperature signal		
Trigger		"T_50_Ext",	
	    Condition	ExtTemp_UpperCC<=51.0 AND ExtTemp_UpperCC>=49.0 AND CC.Temperature.Nominal=50	
	    TrueTime	120	
	    Limit	1	
	    Hysteresis	0	
	    AllowImmediateExecution	No	
	RetTimes.RetTime2	System.Retention	
	Variables.GenericLong0	2	activation of Trigger T_DOWN and Trigger T_20_Ext
End Trigger			
	Trigger for evaluation of HeatUp Time based on internal temperature signal		
Trigger		"T_50_Int",	
	    Condition	CC.Temperature.Value<=51.0 AND CC.Temperature.Value>=49.0 AND CC.Temperature.Nominal=50	
	    TrueTime	120	
	    Limit	1	
	    Hysteresis	0	
	    AllowImmediateExecution	No	
	RetTimes.RetTime3	System.Retention	
	Variables.GenericLong1	2	activation of Trigger T_DOWN
End Trigger			
	Trigger for cooling down the CC from 50 to 20 °C after equilibration		
Trigger		"T_DOWN",	
	    Condition	Variables.GenericLong0=2 AND Variables.GenericLong1=2	
	    TrueTime	30	
	    Limit	1	
	    Hysteresis	0	
	    AllowImmediateExecution	No	
	RetTimes.RetTime4	System.Retention	
	ColumnComp.CC.Temperature.Nominal	20.0 [°C]	
End Trigger			
	Trigger for evaluation of CoolDown Time based on external temperature signal		
Trigger		"T_20_Ext",	
	    Condition	ExtTemp_UpperCC<=21.0 AND ExtTemp_UpperCC>=19.0 AND CC.Temperature.Nominal=20 AND Variables.GenericLong0=2	
	    TrueTime	120	
	    Limit	1	
	    Hysteresis	0	
	    AllowImmediateExecution	No	
	RetTimes.RetTime5	System.Retention	
	Variables.GenericLong0	3	activation of Trigger END_RUN
End Trigger			
	Trigger for evaluation of CoolDown Time based on internal temperature signal		
Trigger		"T_20_Int",	
	    Condition	CC.Temperature.Value<=21.0 AND CC.Temperature.Value>=19.0 AND CC.Temperature.Nominal=20 AND Variables.GenericLong1=2	
	    TrueTime	120	
	    Limit	1	
	    Hysteresis	0	
	    AllowImmediateExecution	No	
	RetTimes.RetTime6	System.Retention	
	Variables.GenericLong1	3	activation of Trigger END_RUN
End Trigger			
Trigger		"END_RUN",	
	    Condition	Variables.GenericLong0=3 AND Variables.GenericLong1=3	
	    TrueTime	30	
	    Limit	1	
	    Hysteresis	0	
	    AllowImmediateExecution	No	
	Column commpartment		
	ColumnComp.CC_Temp.AcqOff		
	ColumnComp.CC_U_Temp_Actual.AcqOff		
	ColumnComp.CC_L_Temp_Actual.AcqOff		
	ColumnComp.CC_UCTL_TempRear_Actual.AcqOff		
	ColumnComp.PWM_CCU_A.AcqOff		
	ColumnComp.PWM_CCU_B.AcqOff		
	ColumnComp.PWM_CCL_A.AcqOff		
	ColumnComp.PWM_CCL_B.AcqOff		
	ColumnComp.Fan_Rear_ActualRPM.AcqOff		
	External measured temperatures		
	Thermometer1.ExtTemp_UpperCC.AcqOff		
	Thermometer1.ExtTemp_LowerCC.AcqOff		
	Thermometer.Environment_Temperature.AcqOff		
	Leak Sensor Evaluation		
	ColumnComp.LEDBoard_LeakDiff.AcqOff		
	ColumnComp.LEDBoard_A13.AcqOff		
	ColumnComp.LEDBoard_A14.AcqOff		
	ColumnComp.Oven_Gas_MuteTimeRemain.AcqOff		
	End		
End Trigger			
240.000	StopRun		
	ColumnComp.CC_Temp.AcqOff		
	ColumnComp.CC_U_Temp_Actual.AcqOff		
	ColumnComp.CC_L_Temp_Actual.AcqOff		
	ColumnComp.CC_UCTL_TempRear_Actual.AcqOff		
	ColumnComp.PWM_CCU_A.AcqOff		
	ColumnComp.PWM_CCU_B.AcqOff		
	ColumnComp.PWM_CCL_A.AcqOff		
	ColumnComp.PWM_CCL_B.AcqOff		
	ColumnComp.Fan_Rear_ActualRPM.AcqOff		
240.000	PostRun		
	External measured temperatures		
	Thermometer1.ExtTemp_UpperCC.AcqOff		
	Thermometer1.ExtTemp_LowerCC.AcqOff		
	Thermometer.Environment_Temperature.AcqOff		
	Leak Sensor Evaluation		
	ColumnComp.LEDBoard_LeakDiff.AcqOff		
	ColumnComp.LEDBoard_A13.AcqOff		
	ColumnComp.LEDBoard_A14.AcqOff		
	ColumnComp.Oven_Gas_MuteTimeRemain.AcqOff		
	End		
```

<a id="m-tcc-heat-cool-vcvh"></a>
## M-TCC-HEAT-COOL-VCVH: TEMP_HEAT_UP_DOWN_20_50_20

Applicable device evidence: **VC / VH**  
Source sequence(s): `VC:3000004, VH:6000001`  
Source SHA-256: `b4a39fc89cc759740da5d964c24b92f926ef5a4455b951f1e8b7964f43a72b5e`  
Decoded flow rows: `170`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	=========================================================================================		
	IM to measure HeatUp time from 20°C to 50°C and CoolDown time from 50°C to 20°C of the Vanquish VH-C10-A and VC-C10-A		
	=========================================================================================		
	HPLC-System:		
	-----------		
	VH-C10-A or VC-C10-A		
-0.700	Equilibration	Duration = 0.700 [min]	
	Different total pages counts are used for VH-C10-A and VC-C10-A (no PCC). This is set here		
If		ColumnComp.ModelNo="VH-C10-A"	
	    Variables.GenericLong9	12	
	    Delay	1	[Val_FOQ_CM7_ekugelma_07-Jul-2020]: OK
	    Log	GenericLong9	
Else If		ColumnComp.ModelNo="VC-C10-A"	
	    Variables.GenericLong9	10	
	    Delay	1	[Val_FOQ_CM7_ekugelma_07-Jul-2020]: OK
	    Log	GenericLong9	
Else			
	    Message	Column compartment model unknown, please reinspect in production!	
	    System.AbortQueue		
End If			
	=========================================================================================		
	Parameters valid for the whole test.		
	=========================================================================================		
	If the difference between nominal and actual temperature is larger than ReadyTempDelta, the oven is not ready.		
	ColumnComp.CC.ReadyTempDelta	0.5 [°C]	
	The Ready property will become Ready only if the difference between the actual and the nominal temperature will not exceed the ReadyTempDelta for the  time interval specified by EquilibrationTime.		
	ColumnComp.CC.EquilibrationTime	0.5 [min]	
	The VTCC controls the temperature only, if TempCtrl is set to ON.		
	ColumnComp.CC.TempCtrl	On	
	Adjusts FanSpeed and switches operating mode		
	ColumnComp.CC.Mode	StillAir	
	Generic variables  to activate Trigger		
	Variables.GenericLong0	0	
	Variables.GenericLong1	0	
	Variables.GenericLong2	0	
	Variables.GenericLong3	0	
	Initialize Retention Times used during IM		
	RetTimes.RetTime1	0	
	RetTimes.RetTime2	0	
	RetTimes.RetTime3	0	
	RetTimes.RetTime4	0	
	RetTimes.RetTime5	0	
	RetTimes.RetTime6	0	
	=========================================================================================		
	Settings for the all channels offered for the column compartment by the driver.		
	Also debug channels are aqcuired.		
	=========================================================================================		
	Column commpartment		
	ColumnComp.CC_U_Temp_Actual.Data_Collection_Rate	20	
	ColumnComp.CC_L_Temp_Actual.Data_Collection_Rate	20	
	ColumnComp.CC_UCTL_TempRear_Actual.Data_Collection_Rate	20	
	ColumnComp.PWM_CCU_A.Data_Collection_Rate	20	
	ColumnComp.PWM_CCU_B.Data_Collection_Rate	20	
	ColumnComp.PWM_CCL_A.Data_Collection_Rate	20	
	ColumnComp.PWM_CCL_B.Data_Collection_Rate	20	
	ColumnComp.Fan_Rear_ActualRPM.Data_Collection_Rate	20	
	Leak Sensors		
	ColumnComp.LEDBoard_LeakDiff.Data_Collection_Rate	20	
	ColumnComp.LEDBoard_A13.Data_Collection_Rate	20	
	ColumnComp.LEDBoard_A14.Data_Collection_Rate	20	
	ColumnComp.Oven_Gas_MuteTimeRemain.Data_Collection_Rate	20	
	=========================================================================================		
	Start Temperature		
	=========================================================================================		
	ColumnComp.CC.Temperature.Nominal	17.0	As the specification for the heat up/ cool down times is given for a temperature range of +/- 1°C the start temperature should be reached during data aquisition. Therfore the temperature is set below the starting temperature
0.000	InjectPreparation		
	Wait	CC.TempReady	
0.000	StartRun		
	ColumnComp.CC_Temp.AcqOn		
	ColumnComp.CC_U_Temp_Actual.AcqOn		
	ColumnComp.CC_L_Temp_Actual.AcqOn		
	ColumnComp.CC_UCTL_TempRear_Actual.AcqOn		
	ColumnComp.PWM_CCU_A.AcqOn		
	ColumnComp.PWM_CCU_B.AcqOn		
	ColumnComp.PWM_CCL_A.AcqOn		
	ColumnComp.PWM_CCL_B.AcqOn		
	ColumnComp.Fan_Rear_ActualRPM.AcqOn		
	External measured temperatures		
	Thermometer1.ExtTemp_UpperCC.AcqOn		
	Thermometer1.ExtTemp_LowerCC.AcqOn		
	Thermometer.Environment_Temperature.AcqOn		
	Leak Sensor Evaluation		
	ColumnComp.LEDBoard_LeakDiff.AcqOn		
	ColumnComp.LEDBoard_A13.AcqOn		
	ColumnComp.LEDBoard_A14.AcqOn		
	ColumnComp.Oven_Gas_MuteTimeRemain.AcqOn		
0.000	Run	Duration = 240.000 [min]	
0.700	ColumnComp.CC.Temperature.Nominal	20.0	
	Trigger "T_Start_Ext" and "T_Start_Int" ensure that the evaluation of heat up and cool down time are starting from the same equilibration conditions (T +/- 1 °C, True Time: 120 sec for external and internal temperature signals)		
1.000			
Trigger		"T_Start_Ext",	
	    Condition	ExtTemp_UpperCC<=21.0 AND ExtTemp_UpperCC>=19.0 AND CC.Temperature.Nominal=20 AND Variables.GenericLong0=0	
	    TrueTime	120	
	    Limit	1	
	    Hysteresis	0	
	    AllowImmediateExecution	No	
	Variables.GenericLong3	1	Activation of trigger "T_UP"
End Trigger			
Trigger		"T_Start_Int",	
	    Condition	CC.Temperature.Value<=21.0 AND CC.Temperature.Value>=19.0 AND CC.Temperature.Nominal=20 AND Variables.GenericLong0=0	
	    TrueTime	120	
	    Limit	1	
	    Hysteresis	0	
	    AllowImmediateExecution	No	
	Variables.GenericLong2	1	Activation of trigger "T_UP"
End Trigger			
	Trigger for heating up the CC from 20 to 50 °C after equilibration		
Trigger		"T_UP",	
	    Condition	Variables.GenericLong2=1 AND Variables.GenericLong3=1	
	    TrueTime	30	
	    Limit	1	
	    Hysteresis	0	
	    AllowImmediateExecution	No	
	ColumnComp.CC.Temperature.Nominal	50.0 [°C]	
	RetTimes.RetTime1	System.Retention	
	Variables.GenericLong0	1	
End Trigger			
	Trigger for evaluation of HeatUp Time based on external temperature signal		
Trigger		"T_50_Ext",	
	    Condition	ExtTemp_UpperCC<=51.0 AND ExtTemp_UpperCC>=49.0 AND CC.Temperature.Nominal=50	
	    TrueTime	120	
	    Limit	1	
	    Hysteresis	0	
	    AllowImmediateExecution	No	
	RetTimes.RetTime2	System.Retention	
	Variables.GenericLong0	2	activation of Trigger T_DOWN and Trigger T_20_Ext
End Trigger			
	Trigger for evaluation of HeatUp Time based on internal temperature signal		
Trigger		"T_50_Int",	
	    Condition	CC.Temperature.Value<=51.0 AND CC.Temperature.Value>=49.0 AND CC.Temperature.Nominal=50	
	    TrueTime	120	
	    Limit	1	
	    Hysteresis	0	
	    AllowImmediateExecution	No	
	RetTimes.RetTime3	System.Retention	
	Variables.GenericLong1	2	activation of Trigger T_DOWN
End Trigger			
	Trigger for cooling down the CC from 50 to 20 °C after equilibration		
Trigger		"T_DOWN",	
	    Condition	Variables.GenericLong0=2 AND Variables.GenericLong1=2	
	    TrueTime	30	
	    Limit	1	
	    Hysteresis	0	
	    AllowImmediateExecution	No	
	RetTimes.RetTime4	System.Retention	
	ColumnComp.CC.Temperature.Nominal	20.0 [°C]	
End Trigger			
	Trigger for evaluation of CoolDown Time based on external temperature signal		
Trigger		"T_20_Ext",	
	    Condition	ExtTemp_UpperCC<=21.0 AND ExtTemp_UpperCC>=19.0 AND CC.Temperature.Nominal=20 AND Variables.GenericLong0=2	
	    TrueTime	120	
	    Limit	1	
	    Hysteresis	0	
	    AllowImmediateExecution	No	
	RetTimes.RetTime5	System.Retention	
	Variables.GenericLong0	3	activation of Trigger END_RUN
End Trigger			
	Trigger for evaluation of CoolDown Time based on internal temperature signal		
Trigger		"T_20_Int",	
	    Condition	CC.Temperature.Value<=21.0 AND CC.Temperature.Value>=19.0 AND CC.Temperature.Nominal=20 AND Variables.GenericLong1=2	
	    TrueTime	120	
	    Limit	1	
	    Hysteresis	0	
	    AllowImmediateExecution	No	
	RetTimes.RetTime6	System.Retention	
	Variables.GenericLong1	3	activation of Trigger END_RUN
End Trigger			
Trigger		"END_RUN",	
	    Condition	Variables.GenericLong0=3 AND Variables.GenericLong1=3	
	    TrueTime	30	
	    Limit	1	
	    Hysteresis	0	
	    AllowImmediateExecution	No	
	Column commpartment		
	ColumnComp.CC_Temp.AcqOff		
	ColumnComp.CC_U_Temp_Actual.AcqOff		
	ColumnComp.CC_L_Temp_Actual.AcqOff		
	ColumnComp.CC_UCTL_TempRear_Actual.AcqOff		
	ColumnComp.PWM_CCU_A.AcqOff		
	ColumnComp.PWM_CCU_B.AcqOff		
	ColumnComp.PWM_CCL_A.AcqOff		
	ColumnComp.PWM_CCL_B.AcqOff		
	ColumnComp.Fan_Rear_ActualRPM.AcqOff		
	External measured temperatures		
	Thermometer1.ExtTemp_UpperCC.AcqOff		
	Thermometer1.ExtTemp_LowerCC.AcqOff		
	Thermometer.Environment_Temperature.AcqOff		
	Leak Sensor Evaluation		
	ColumnComp.LEDBoard_LeakDiff.AcqOff		
	ColumnComp.LEDBoard_A13.AcqOff		
	ColumnComp.LEDBoard_A14.AcqOff		
	ColumnComp.Oven_Gas_MuteTimeRemain.AcqOff		
	End		
End Trigger			
240.000	StopRun		
	ColumnComp.CC_Temp.AcqOff		
	ColumnComp.CC_U_Temp_Actual.AcqOff		
	ColumnComp.CC_L_Temp_Actual.AcqOff		
	ColumnComp.CC_UCTL_TempRear_Actual.AcqOff		
	ColumnComp.PWM_CCU_A.AcqOff		
	ColumnComp.PWM_CCU_B.AcqOff		
	ColumnComp.PWM_CCL_A.AcqOff		
	ColumnComp.PWM_CCL_B.AcqOff		
	ColumnComp.Fan_Rear_ActualRPM.AcqOff		
240.000	PostRun		
	External measured temperatures		
	Thermometer1.ExtTemp_UpperCC.AcqOff		
	Thermometer1.ExtTemp_LowerCC.AcqOff		
	Thermometer.Environment_Temperature.AcqOff		
	Leak Sensor Evaluation		
	ColumnComp.LEDBoard_LeakDiff.AcqOff		
	ColumnComp.LEDBoard_A13.AcqOff		
	ColumnComp.LEDBoard_A14.AcqOff		
	ColumnComp.Oven_Gas_MuteTimeRemain.AcqOff		
	End		
```

<a id="m-tcc-accuracy-va"></a>
## M-TCC-ACCURACY-VA: TEMPERATURE_ACCURACY

Applicable device evidence: **VA**  
Source sequence(s): `VA:0000003`  
Source SHA-256: `241e598a758acac7202ac75f5795d5f29a51d5dc0908404286059e7424c9c8f7`  
Decoded flow rows: `261`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	=========================================================================================		
	IM to measure the temperature accuracy of the Vanquish VH-C10-A, VC-C10-A and VA-C10-A		
	=========================================================================================		
	HPLC-System:		
	-----------		
	VH-C10-A, VC-C10-A or VA-C10-A		
-0.700	Equilibration	Duration = 0.700 [min]	
	Different total pages counts are used for VH-C10-A and VA-C10-A (no PCC). This is set here		
If		ColumnComp.ModelNo="VH-C10-A"	
	    Variables.GenericLong9	12	
	    Delay	1	
	    Log	GenericLong9	
Else If		ColumnComp.ModelNo="VC-C10-A" OR ColumnComp.ModelNo="VA-C10-A"	
	    Variables.GenericLong9	10	
	    Delay	1	
	    Log	GenericLong9	
Else			
	    Message	Column compartment model unknown, please reinspect in production!	
	    System.AbortQueue		
End If			
	=========================================================================================		
	Parameters valid for the whole test.		
	=========================================================================================		
	If the difference between nominal and actual temperature is larger than ReadyTempDelta, the VTCC is not ready.		
	ColumnComp.CC.ReadyTempDelta	1.0 [°C]	
	The Ready property will become Ready only if the difference between the setpoint temperature and the nominal temperature will not exceed the ReadyTempDelta forthe  time interval specified by EquilibrationTime.		
	ColumnComp.CC.EquilibrationTime	0.5	
	The VTCC adjusts the temperature only, if TempCtrl is set to ON for each single unit.		
	ColumnComp.CC.TempCtrl	On	
If		ColumnComp.ModelNo="VH-C10-A"	
	    ColumnComp.CmdString	Cmd="PCC.TempCtrl=0"	String necessary, because otherwise a way more complicated solution would be needed for using this IM for both CC types. Is equivalent to ColumnComp.PCC.TempCtrl=Off
Else			
End If			
	Adjusts FanSpeed and switches operating mode		
	ColumnComp.CC.Mode	StillAir	
	Liquid Leak Sensor remains switched off in order to avoid false alarms after great temperature changes		
	=========================================================================================		
	ColumnComp.LiquidLeakSensor	Off	
	=========================================================================================		
	Settings for the all channels offered for the column compartment by the driver.		
	Also debug channels are aqcuired.		
	=========================================================================================		
	Column commpartment		
	ColumnComp.CC_U_Temp_Actual.Data_Collection_Rate	20	
	ColumnComp.CC_L_Temp_Actual.Data_Collection_Rate	20	
	ColumnComp.CC_UCTL_TempRear_Actual.Data_Collection_Rate	20	
	ColumnComp.PWM_CCU_A.Data_Collection_Rate	20	
	ColumnComp.PWM_CCU_B.Data_Collection_Rate	20	
	ColumnComp.PWM_CCL_A.Data_Collection_Rate	20	
	ColumnComp.PWM_CCL_B.Data_Collection_Rate	20	
	ColumnComp.Fan_Rear_ActualRPM.Data_Collection_Rate	20	
	Leak Sensors		
	ColumnComp.LEDBoard_LeakDiff.Data_Collection_Rate	20	
	ColumnComp.LEDBoard_A13.Data_Collection_Rate	20	
	ColumnComp.LEDBoard_A14.Data_Collection_Rate	20	
	ColumnComp.Oven_Gas_MuteTimeRemain.Data_Collection_Rate	20	
	============================================================================================		
	Set test temperatures for different CC types to variables, because otherwise ready check for VC-C10-A and VA-C10-A would fail for highest VH-C10-A temperatures		
	============================================================================================		
If		ColumnComp.ModelNo="VH-C10-A"	
	    Variables.GenericDouble1	10.0	First test temperature
	    Variables.GenericDouble2	20.0	Second test temperature
	    Variables.GenericDouble3	40.0	Third test temperature
	    Variables.GenericDouble4	80.0	Fourth test temperature
	    Variables.GenericDouble5	120.0	Fifth test temperature
	    Variables.GenericBool1	0	Will be changed to 1 if first test temperature is skipped due to high ambient.
Else If		ColumnComp.ModelNo="VC-C10-A" OR ColumnComp.ModelNo="VA-C10-A"	
	    Variables.GenericDouble1	10.0	First test temperature
	    Variables.GenericDouble2	20.0	Second test temperature
	    Variables.GenericDouble3	40.0	Third test temperature
	    Variables.GenericDouble4	60.0	Fourth test temperature
	    Variables.GenericDouble5	85.0	Fifth test temperature
	    Variables.GenericBool1	0	Will be changed to 1 if first test temperature is skipped due to high ambient.
Else			
	    Message	Invalid ModelNo! Please reinspect in production!	
	    System.AbortQueue		
End If			
	=========================================================================================		
	Start Temperature - Either 10°C TCC temperature or, for room temperatures higher than 28.5°C, 20°C TCC temperature.		
	=========================================================================================		
	Delay	3	
	TempVars.Ambient_Temp	Thermometer.Measure_1	
	Delay	3	
If		TempVars.Ambient_Temp>28.49	
	    ColumnComp.CC.Temperature.Nominal	Variables.GenericDouble2	
	    Variables.GenericBool1	1	
Else			
	    ColumnComp.CC.Temperature.Nominal	Variables.GenericDouble1	
End If			
	Delay	5	
0.000	InjectPreparation		
	Delay	5	
	Wait	CC.TempReady	
	=============================================================================================================================		
	Reset of all Retention Times		
	=============================================================================================================================		
	RetTimes.RetTime1	0	
	RetTimes.RetTime2	0	
	RetTimes.RetTime3	0	
	RetTimes.RetTime4	0	
	RetTimes.RetTime5	0	
	=============================================================================================================================		
	Preparations for gradient measurement of external temperatures		
	=============================================================================================================================		
	StabVars.TriggerStab1	0	
	StabVars.TriggerStab2	0	
	StabVars.TempUpperHigh	0	
	StabVars.TempUpperLow	0	
	StabVars.TempLowerHigh	0	
	StabVars.TempLowerLow	0	
	StabVars.CounterUpper	0	
	StabVars.CounterLower	0	
	StabVars.UpperReady	0	
	StabVars.LowerReady	0	
	ColumnComp.CC.ReadyTempDelta	0.2	
	ColumnComp.CC.EquilibrationTime	3	
	=============================================================================================================================		
	Delay	1	
	=============================================================================================================================		
	Triggers for stability of external temperatures		
	=============================================================================================================================		
Trigger		"Gradient_1",	
	    Condition	(StabVars.TriggerStab1=1) AND CC.TempReady	
	    TrueTime	30	
	    Delay	0	
	StabVars.TriggerStab1	0	
	StabVars.TriggerStab2	1	
	Is external temperature stabilization evaluation running and in the allowed range? This is the case when TempDifLast<>0		
If		(StabVars.TempUpperHigh<>0) and ((Thermometer1.ExtTemp_UpperCC<=StabVars.TempUpperHigh) AND (Thermometer1.ExtTemp_UpperCC>=StabVars.TempUpperLow))	
	    Yes, increment counter		
	    StabVars.CounterUpper	StabVars.CounterUpper+1	
Else			
	    No, reset evaluation variables		
	    StabVars.CounterUpper	0	
	    StabVars.TempUpperHigh	Thermometer1.ExtTemp_UpperCC+0.05	
	    StabVars.TempUpperLow	Thermometer1.ExtTemp_UpperCC-0.05	
End If			
If		(StabVars.TempLowerHigh<>0) and ((Thermometer1.ExtTemp_LowerCC<=StabVars.TempLowerHigh) AND (Thermometer1.ExtTemp_LowerCC>=StabVars.TempLowerLow))	
	    Yes, increment counter		
	    StabVars.CounterLower	StabVars.CounterLower+1	
Else			
	    No, reset evaluation variables		
	    StabVars.CounterLower	0	
	    StabVars.TempLowerHigh	Thermometer1.ExtTemp_LowerCC+0.05	
	    StabVars.TempLowerLow	Thermometer1.ExtTemp_LowerCC-0.05	
End If			
	Check if equilibration time is finished		
	Delay	1	
If		StabVars.CounterUpper>=4	
	    StabVars.UpperReady	1	
Else			
	    StabVars.UpperReady	0	
End If			
If		StabVars.CounterLower>=4	
	    StabVars.LowerReady	1	
Else			
	    StabVars.LowerReady	0	
End If			
End Trigger			
Trigger		"Gradient_2",	
	    Condition	StabVars.TriggerStab2=1	
	    TrueTime	30	
	    Delay	0	
	StabVars.TriggerStab1	1	
	StabVars.TriggerStab2	0	
End Trigger			
	The trigger will be executed when TempDiffULast is defined (<>0) and the external temperature is leaving the allowed range.		
	Then TempDiffULast is set to 0.		
	True Time of 5 sec will ensure, that the trigger is not activated by single temperature spikes of the external temperature sensor		
Trigger		"ExitRange_Upper",	
	    Condition	(StabVars.TempUpperHigh<>0) AND ((ColumnComp.CC.TempReady=0) OR (Thermometer1.ExtTemp_UpperCC>StabVars.TempUpperHigh) OR (Thermometer1.ExtTemp_UpperCC<StabVars.TempUpperLow))	
	    TrueTime	5	
	StabVars.TempUpperHigh	0	
	StabVars.TempUpperLow	0	
	StabVars.UpperReady	0	
End Trigger			
Trigger		"ExitRange_Lower",	
	    Condition	(StabVars.TempLowerHigh<>0) AND ((ColumnComp.CC.TempReady=0) OR (Thermometer1.ExtTemp_LowerCC>StabVars.TempLowerHigh) OR (Thermometer1.ExtTemp_LowerCC<StabVars.TempLowerLow))	
	    TrueTime	5	
	StabVars.TempLowerHigh	0	
	StabVars.TempLowerLow	0	
	StabVars.LowerReady	0	
End Trigger			
	=============================================================================================================================		
Trigger		"Abort",	
	    Condition	((System.Retention>40 AND ColumnComp.CC.Temperature.Nominal=Variables.GenericDouble1) OR (System.Retention>RetTimes.RetTime1+40 AND ColumnComp.CC.Temperature.Nominal=Variables.GenericDouble2) OR (System.Retention>RetTimes.RetTime2+40 AND ColumnComp.CC.Temperature.Nominal=Variables.GenericDouble3) OR (System.Retention>RetTimes.RetTime3+40 AND ColumnComp.CC.Temperature.Nominal=Variables.GenericDouble4) OR (System.Retention>RetTimes.RetTime4+40 AND ColumnComp.CC.Temperature.Nominal=Variables.GenericDouble5)) AND (RetTimes.RetTime5=0)	
	    TrueTime	0	
	    AllowImmediateExecution	Yes	
	ColumnComp.CmdString	Cmd="LedBar.ForceColor=1"	
	Message	QUEUE WAS ABORTED! Please check your test setup and repeat the temperature calibration and accuracy test.	
	Delay	1	
	ColumnComp.CmdString	Cmd="LedBar.ForceColor=0"	
	System.AbortQueue		
End Trigger			
0.000	StartRun		
	ColumnComp.CC_Temp.AcqOn		
	ColumnComp.CC_U_Temp_Actual.AcqOn		
	ColumnComp.CC_L_Temp_Actual.AcqOn		
	ColumnComp.CC_UCTL_TempRear_Actual.AcqOn		
	ColumnComp.PWM_CCU_A.AcqOn		
	ColumnComp.PWM_CCU_B.AcqOn		
	ColumnComp.PWM_CCL_A.AcqOn		
	ColumnComp.PWM_CCL_B.AcqOn		
	ColumnComp.Fan_Rear_ActualRPM.AcqOn		
	External measured temperatures		
	Thermometer1.ExtTemp_UpperCC.AcqOn		
	Thermometer1.ExtTemp_LowerCC.AcqOn		
	Thermometer.Environment_Temperature.AcqOn		
	Leak Sensor Evaluation		
	ColumnComp.LEDBoard_LeakDiff.AcqOn		
	ColumnComp.LEDBoard_A13.AcqOn		
	ColumnComp.LEDBoard_A14.AcqOn		
	ColumnComp.Oven_Gas_MuteTimeRemain.AcqOn		
0.000	Run	Duration = 250.000 [min]	
	Delay	5	
	If temperature accuracy determination at 10°C is skipped, a message is saved in the audit trail and the test starts with the second test temperature.		
If		Variables.GenericBool1=1	
	    Protocol	Evaluation at 10°C is skipped, as the room temperature is too high at the moment!	
	    Delay	3	
	    ColumnComp.CC.Temperature.Nominal	Variables.GenericDouble2	
	    Delay	60	
	    StabVars.TriggerStab1	1	
	    Delay	3	
Else			
	    StabVars.TriggerStab1	1	
	    Delay	3	
	    Wait	ColumnComp.CC.TempReady AND StabVars.LowerReady AND StabVars.UpperReady, Run=Continue	
	    RetTimes.RetTime1	System.Retention	
	    ColumnComp.CC.Temperature.Nominal	Variables.GenericDouble2	
	    Delay	60	
End If			
	Wait	ColumnComp.CC.TempReady AND StabVars.LowerReady AND StabVars.UpperReady, Run=Continue	
	RetTimes.RetTime2	System.Retention	
	ColumnComp.CC.Temperature.Nominal	Variables.GenericDouble3	
	Delay	60	
	Wait	ColumnComp.CC.TempReady AND StabVars.LowerReady AND StabVars.UpperReady, Run=Continue	
	RetTimes.RetTime3	System.Retention	
	ColumnComp.CC.Temperature.Nominal	Variables.GenericDouble4	
	Delay	60	
	Wait	ColumnComp.CC.TempReady AND StabVars.LowerReady AND StabVars.UpperReady, Run=Continue	
	RetTimes.RetTime4	System.Retention	
	ColumnComp.CC.Temperature.Nominal	Variables.GenericDouble5	
	Delay	60	
	Wait	ColumnComp.CC.TempReady AND StabVars.LowerReady AND StabVars.UpperReady, Run=Continue	
	RetTimes.RetTime5	System.Retention	
	Delay	2	
	ColumnComp.CC.Temperature.Nominal	20.0 [°C]	
	Stop external temperatures stability evaluatin triggers		
	StabVars.TriggerStab1	0	
	StabVars.TriggerStab2	0	
	Delay	2	
	Stop Run		
	ColumnComp.CC_Temp.AcqOff		
	ColumnComp.CC_U_Temp_Actual.AcqOff		
	ColumnComp.CC_L_Temp_Actual.AcqOff		
	ColumnComp.CC_UCTL_TempRear_Actual.AcqOff		
	ColumnComp.PWM_CCU_A.AcqOff		
	ColumnComp.PWM_CCU_B.AcqOff		
	ColumnComp.PWM_CCL_A.AcqOff		
	ColumnComp.PWM_CCL_B.AcqOff		
	ColumnComp.Fan_Rear_ActualRPM.AcqOff		
	External measured temperatures		
	Thermometer1.ExtTemp_UpperCC.AcqOff		
	Thermometer1.ExtTemp_LowerCC.AcqOff		
	Thermometer.Environment_Temperature.AcqOff		
	Leak Sensor Evaluation		
	ColumnComp.LEDBoard_LeakDiff.AcqOff		
	ColumnComp.LEDBoard_A13.AcqOff		
	ColumnComp.LEDBoard_A14.AcqOff		
	ColumnComp.Oven_Gas_MuteTimeRemain.AcqOff		
	End		
250.000	StopRun		
	End		
```

<a id="m-tcc-accuracy-vcvh"></a>
## M-TCC-ACCURACY-VCVH: TEMPERATURE_ACCURACY

Applicable device evidence: **VC / VH**  
Source sequence(s): `VC:3000004, VH:6000001`  
Source SHA-256: `1d4d557099385e2a8138c242ad4d2624895339a854e4a6125e49efdd522a47d6`  
Decoded flow rows: `261`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	=========================================================================================		
	IM to measure the temperature accuracy of the Vanquish VH-C10-A  and VC-C10-A		
	=========================================================================================		
	HPLC-System:		
	-----------		
	VH-C10-A or VC-C10-A		
-0.700	Equilibration	Duration = 0.700 [min]	
	Different total pages counts are used for VH-C10-A and VC-C10-A (no PCC). This is set here		
If		ColumnComp.ModelNo="VH-C10-A"	
	    Variables.GenericLong9	12	
	    Delay	1	
	    Log	GenericLong9	
Else If		ColumnComp.ModelNo="VC-C10-A"	
	    Variables.GenericLong9	10	
	    Delay	1	
	    Log	GenericLong9	
Else			
	    Message	Column compartment model unknown, please reinspect in production!	
	    System.AbortQueue		
End If			
	=========================================================================================		
	Parameters valid for the whole test.		
	=========================================================================================		
	If the difference between nominal and actual temperature is larger than ReadyTempDelta, the VTCC is not ready.		
	ColumnComp.CC.ReadyTempDelta	1.0 [°C]	
	The Ready property will become Ready only if the difference between the setpoint temperature and the nominal temperature will not exceed the ReadyTempDelta forthe  time interval specified by EquilibrationTime.		
	ColumnComp.CC.EquilibrationTime	0.5	
	The VTCC adjusts the temperature only, if TempCtrl is set to ON for each single unit.		
	ColumnComp.CC.TempCtrl	On	
If		ColumnComp.ModelNo="VH-C10-A"	
	    ColumnComp.CmdString	Cmd="PCC.TempCtrl=0"	String necessary, because otherwise a way more complicated solution would be needed for using this IM for both CC types. Is equivalent to ColumnComp.PCC.TempCtrl=Off
Else			
End If			
	Adjusts FanSpeed and switches operating mode		
	ColumnComp.CC.Mode	StillAir	
	Liquid Leak Sensor remains switched off in order to avoid false alarms after great temperature changes		
	=========================================================================================		
	ColumnComp.LiquidLeakSensor	Off	
	=========================================================================================		
	Settings for the all channels offered for the column compartment by the driver.		
	Also debug channels are aqcuired.		
	=========================================================================================		
	Column commpartment		
	ColumnComp.CC_U_Temp_Actual.Data_Collection_Rate	20	
	ColumnComp.CC_L_Temp_Actual.Data_Collection_Rate	20	
	ColumnComp.CC_UCTL_TempRear_Actual.Data_Collection_Rate	20	
	ColumnComp.PWM_CCU_A.Data_Collection_Rate	20	
	ColumnComp.PWM_CCU_B.Data_Collection_Rate	20	
	ColumnComp.PWM_CCL_A.Data_Collection_Rate	20	
	ColumnComp.PWM_CCL_B.Data_Collection_Rate	20	
	ColumnComp.Fan_Rear_ActualRPM.Data_Collection_Rate	20	
	Leak Sensors		
	ColumnComp.LEDBoard_LeakDiff.Data_Collection_Rate	20	
	ColumnComp.LEDBoard_A13.Data_Collection_Rate	20	
	ColumnComp.LEDBoard_A14.Data_Collection_Rate	20	
	ColumnComp.Oven_Gas_MuteTimeRemain.Data_Collection_Rate	20	
	============================================================================================		
	Set test temperatures for different CC types to variables, because otherwise ready check for VC-C10-A would fail for highest VH-C10-A temperatures		
	============================================================================================		
If		ColumnComp.ModelNo="VH-C10-A"	
	    Variables.GenericDouble1	10.0	First test temperature
	    Variables.GenericDouble2	20.0	Second test temperature
	    Variables.GenericDouble3	40.0	Third test temperature
	    Variables.GenericDouble4	80.0	Fourth test temperature
	    Variables.GenericDouble5	120.0	Fifth test temperature
	    Variables.GenericBool1	0	Will be changed to 1 if first test temperature is skipped due to high ambient.
Else If		ColumnComp.ModelNo="VC-C10-A"	
	    Variables.GenericDouble1	10.0	First test temperature
	    Variables.GenericDouble2	20.0	Second test temperature
	    Variables.GenericDouble3	40.0	Third test temperature
	    Variables.GenericDouble4	60.0	Fourth test temperature
	    Variables.GenericDouble5	85.0	Fifth test temperature
	    Variables.GenericBool1	0	Will be changed to 1 if first test temperature is skipped due to high ambient.
Else			
	    Message	Invalid ModelNo! Please reinspect in production!	
	    System.AbortQueue		
End If			
	=========================================================================================		
	Start Temperature - Either 10°C TCC temperature or, for room temperatures higher than 28.5°C, 20°C TCC temperature.		
	=========================================================================================		
	Delay	3	
	TempVars.Ambient_Temp	Thermometer.Measure_1	
	Delay	3	
If		TempVars.Ambient_Temp>28.49	
	    ColumnComp.CC.Temperature.Nominal	Variables.GenericDouble2	
	    Variables.GenericBool1	1	
Else			
	    ColumnComp.CC.Temperature.Nominal	Variables.GenericDouble1	
End If			
	Delay	5	
0.000	InjectPreparation		
	Delay	5	
	Wait	CC.TempReady	
	=============================================================================================================================		
	Reset of all Retention Times		
	=============================================================================================================================		
	RetTimes.RetTime1	0	
	RetTimes.RetTime2	0	
	RetTimes.RetTime3	0	
	RetTimes.RetTime4	0	
	RetTimes.RetTime5	0	
	=============================================================================================================================		
	Preparations for gradient measurement of external temperatures		
	=============================================================================================================================		
	StabVars.TriggerStab1	0	
	StabVars.TriggerStab2	0	
	StabVars.TempUpperHigh	0	
	StabVars.TempUpperLow	0	
	StabVars.TempLowerHigh	0	
	StabVars.TempLowerLow	0	
	StabVars.CounterUpper	0	
	StabVars.CounterLower	0	
	StabVars.UpperReady	0	
	StabVars.LowerReady	0	
	ColumnComp.CC.ReadyTempDelta	0.2	
	ColumnComp.CC.EquilibrationTime	3	
	=============================================================================================================================		
	Delay	1	
	=============================================================================================================================		
	Triggers for stability of external temperatures		
	=============================================================================================================================		
Trigger		"Gradient_1",	
	    Condition	(StabVars.TriggerStab1=1) AND CC.TempReady	
	    TrueTime	30	
	    Delay	0	
	StabVars.TriggerStab1	0	
	StabVars.TriggerStab2	1	
	Is external temperature stabilization evaluation running and in the allowed range? This is the case when TempDifLast<>0		
If		(StabVars.TempUpperHigh<>0) and ((Thermometer1.ExtTemp_UpperCC<=StabVars.TempUpperHigh) AND (Thermometer1.ExtTemp_UpperCC>=StabVars.TempUpperLow))	
	    Yes, increment counter		
	    StabVars.CounterUpper	StabVars.CounterUpper+1	
Else			
	    No, reset evaluation variables		
	    StabVars.CounterUpper	0	
	    StabVars.TempUpperHigh	Thermometer1.ExtTemp_UpperCC+0.05	
	    StabVars.TempUpperLow	Thermometer1.ExtTemp_UpperCC-0.05	
End If			
If		(StabVars.TempLowerHigh<>0) and ((Thermometer1.ExtTemp_LowerCC<=StabVars.TempLowerHigh) AND (Thermometer1.ExtTemp_LowerCC>=StabVars.TempLowerLow))	
	    Yes, increment counter		
	    StabVars.CounterLower	StabVars.CounterLower+1	
Else			
	    No, reset evaluation variables		
	    StabVars.CounterLower	0	
	    StabVars.TempLowerHigh	Thermometer1.ExtTemp_LowerCC+0.05	
	    StabVars.TempLowerLow	Thermometer1.ExtTemp_LowerCC-0.05	
End If			
	Check if equilibration time is finished		
	Delay	1	
If		StabVars.CounterUpper>=4	
	    StabVars.UpperReady	1	
Else			
	    StabVars.UpperReady	0	
End If			
If		StabVars.CounterLower>=4	
	    StabVars.LowerReady	1	
Else			
	    StabVars.LowerReady	0	
End If			
End Trigger			
Trigger		"Gradient_2",	
	    Condition	StabVars.TriggerStab2=1	
	    TrueTime	30	
	    Delay	0	
	StabVars.TriggerStab1	1	
	StabVars.TriggerStab2	0	
End Trigger			
	The trigger will be executed when TempDiffULast is defined (<>0) and the external temperature is leaving the allowed range.		
	Then TempDiffULast is set to 0.		
	True Time of 5 sec will ensure, that the trigger is not activated by single temperature spikes of the external temperature sensor		
Trigger		"ExitRange_Upper",	
	    Condition	(StabVars.TempUpperHigh<>0) AND ((ColumnComp.CC.TempReady=0) OR (Thermometer1.ExtTemp_UpperCC>StabVars.TempUpperHigh) OR (Thermometer1.ExtTemp_UpperCC<StabVars.TempUpperLow))	
	    TrueTime	5	
	StabVars.TempUpperHigh	0	
	StabVars.TempUpperLow	0	
	StabVars.UpperReady	0	
End Trigger			
Trigger		"ExitRange_Lower",	
	    Condition	(StabVars.TempLowerHigh<>0) AND ((ColumnComp.CC.TempReady=0) OR (Thermometer1.ExtTemp_LowerCC>StabVars.TempLowerHigh) OR (Thermometer1.ExtTemp_LowerCC<StabVars.TempLowerLow))	
	    TrueTime	5	
	StabVars.TempLowerHigh	0	
	StabVars.TempLowerLow	0	
	StabVars.LowerReady	0	
End Trigger			
	=============================================================================================================================		
Trigger		"Abort",	
	    Condition	((System.Retention>40 AND ColumnComp.CC.Temperature.Nominal=Variables.GenericDouble1) OR (System.Retention>RetTimes.RetTime1+40 AND ColumnComp.CC.Temperature.Nominal=Variables.GenericDouble2) OR (System.Retention>RetTimes.RetTime2+40 AND ColumnComp.CC.Temperature.Nominal=Variables.GenericDouble3) OR (System.Retention>RetTimes.RetTime3+40 AND ColumnComp.CC.Temperature.Nominal=Variables.GenericDouble4) OR (System.Retention>RetTimes.RetTime4+40 AND ColumnComp.CC.Temperature.Nominal=Variables.GenericDouble5)) AND (RetTimes.RetTime5=0)	
	    TrueTime	0	
	    AllowImmediateExecution	Yes	
	ColumnComp.CmdString	Cmd="LedBar.ForceColor=1"	
	Message	QUEUE WAS ABORTED! Please check your test setup and repeat the temperature calibration and accuracy test.	
	Delay	1	
	ColumnComp.CmdString	Cmd="LedBar.ForceColor=0"	
	System.AbortQueue		
End Trigger			
0.000	StartRun		
	ColumnComp.CC_Temp.AcqOn		
	ColumnComp.CC_U_Temp_Actual.AcqOn		
	ColumnComp.CC_L_Temp_Actual.AcqOn		
	ColumnComp.CC_UCTL_TempRear_Actual.AcqOn		
	ColumnComp.PWM_CCU_A.AcqOn		
	ColumnComp.PWM_CCU_B.AcqOn		
	ColumnComp.PWM_CCL_A.AcqOn		
	ColumnComp.PWM_CCL_B.AcqOn		
	ColumnComp.Fan_Rear_ActualRPM.AcqOn		
	External measured temperatures		
	Thermometer1.ExtTemp_UpperCC.AcqOn		
	Thermometer1.ExtTemp_LowerCC.AcqOn		
	Thermometer.Environment_Temperature.AcqOn		
	Leak Sensor Evaluation		
	ColumnComp.LEDBoard_LeakDiff.AcqOn		
	ColumnComp.LEDBoard_A13.AcqOn		
	ColumnComp.LEDBoard_A14.AcqOn		
	ColumnComp.Oven_Gas_MuteTimeRemain.AcqOn		
0.000	Run	Duration = 250.000 [min]	
	Delay	5	
	If temperature accuracy determination at 10°C is skipped, a message is saved in the audit trail and the test starts with the second test temperature.		
If		Variables.GenericBool1=1	
	    Protocol	Evaluation at 10°C is skipped, as the room temperature is too high at the moment!	
	    Delay	3	
	    ColumnComp.CC.Temperature.Nominal	Variables.GenericDouble2	
	    Delay	60	
	    StabVars.TriggerStab1	1	
	    Delay	3	
Else			
	    StabVars.TriggerStab1	1	
	    Delay	3	
	    Wait	ColumnComp.CC.TempReady AND StabVars.LowerReady AND StabVars.UpperReady, Run=Continue	
	    RetTimes.RetTime1	System.Retention	
	    ColumnComp.CC.Temperature.Nominal	Variables.GenericDouble2	
	    Delay	60	
End If			
	Wait	ColumnComp.CC.TempReady AND StabVars.LowerReady AND StabVars.UpperReady, Run=Continue	
	RetTimes.RetTime2	System.Retention	
	ColumnComp.CC.Temperature.Nominal	Variables.GenericDouble3	
	Delay	60	
	Wait	ColumnComp.CC.TempReady AND StabVars.LowerReady AND StabVars.UpperReady, Run=Continue	
	RetTimes.RetTime3	System.Retention	
	ColumnComp.CC.Temperature.Nominal	Variables.GenericDouble4	
	Delay	60	
	Wait	ColumnComp.CC.TempReady AND StabVars.LowerReady AND StabVars.UpperReady, Run=Continue	
	RetTimes.RetTime4	System.Retention	
	ColumnComp.CC.Temperature.Nominal	Variables.GenericDouble5	
	Delay	60	
	Wait	ColumnComp.CC.TempReady AND StabVars.LowerReady AND StabVars.UpperReady, Run=Continue	
	RetTimes.RetTime5	System.Retention	
	Delay	2	
	ColumnComp.CC.Temperature.Nominal	20.0 [°C]	
	Stop external temperatures stability evaluatin triggers		
	StabVars.TriggerStab1	0	
	StabVars.TriggerStab2	0	
	Delay	2	
	Stop Run		
	ColumnComp.CC_Temp.AcqOff		
	ColumnComp.CC_U_Temp_Actual.AcqOff		
	ColumnComp.CC_L_Temp_Actual.AcqOff		
	ColumnComp.CC_UCTL_TempRear_Actual.AcqOff		
	ColumnComp.PWM_CCU_A.AcqOff		
	ColumnComp.PWM_CCU_B.AcqOff		
	ColumnComp.PWM_CCL_A.AcqOff		
	ColumnComp.PWM_CCL_B.AcqOff		
	ColumnComp.Fan_Rear_ActualRPM.AcqOff		
	External measured temperatures		
	Thermometer1.ExtTemp_UpperCC.AcqOff		
	Thermometer1.ExtTemp_LowerCC.AcqOff		
	Thermometer.Environment_Temperature.AcqOff		
	Leak Sensor Evaluation		
	ColumnComp.LEDBoard_LeakDiff.AcqOff		
	ColumnComp.LEDBoard_A13.AcqOff		
	ColumnComp.LEDBoard_A14.AcqOff		
	ColumnComp.Oven_Gas_MuteTimeRemain.AcqOff		
	End		
250.000	StopRun		
	End		
```

<a id="m-tcc-calibration-va"></a>
## M-TCC-CALIBRATION-VA: TEMPERATURE_CALIBRATION

Applicable device evidence: **VA**  
Source sequence(s): `VA:0000003`  
Source SHA-256: `8856e261f44db81952b5df0b40aee3e70749d0f6665ba839984b8aaf3dac29bd`  
Decoded flow rows: `466`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	=========================================================================================		
	IM to calibrate temperature of the VH-C10-A, VC-C10-A and VA-C10-A		
	=========================================================================================		
	HPLC-System:		
	-----------		
	VH-C10-A, VC-C10-A or VA-C10-A		
-2.700	Equilibration	Duration = 0.700 [min]	
	=========================================================================================		
	Parameters valid for the whole test.		
	=========================================================================================		
	If the difference between nominal and actual temperature is larger than ReadyTempDelta, the column compartement is not ready.		
	ColumnComp.CC.ReadyTempDelta	0.3 [°C]	Limit is set to 0.3 °C to use CC.TempReady for activating the trigger of the IM
	The Ready property will become Ready only if the difference between the actual and the nominal temperature will not exceed the ReadyTempDelta for the  time interval specified by EquilibrationTime.		
	ColumnComp.CC.EquilibrationTime	0.1 [min]	Time is so short to use CC.TempReady for activating the trigger of the IM (avoid unneccessary prolongation of temperature steps)
	The VTCC controls the temperature only, if TempCtrl is set to ON.		
	ColumnComp.CC.TempCtrl	On	
If		ColumnComp.ModelNo="VH-C10-A"	
	    ColumnComp.CmdString	Cmd="PCC.TempCtrl=0"	String necessary, because otherwise a way more complicated solution would be needed for using this IM for both CC types. Is equivalent to ColumnComp.PCC.TempCtrl=Off
Else			
End If			
	Adjusts FanSpeed and switches operating mode		
	ColumnComp.CC.Mode	StillAir	
	=========================================================================================		
	Liquid Leak Sensor remains switched off in order to avoid false alarms after great temperature changes		
	=========================================================================================		
	ColumnComp.LiquidLeakSensor	Off	
	=========================================================================================		
	Settings for the all channels offered for the column compartment by the driver.		
	Also debug channels are aqcuired.		
	=========================================================================================		
	Column commpartment		
	ColumnComp.CC_U_Temp_Actual.Data_Collection_Rate	20	
	ColumnComp.CC_L_Temp_Actual.Data_Collection_Rate	20	
	ColumnComp.CC_UCTL_TempRear_Actual.Data_Collection_Rate	20	
	ColumnComp.PWM_CCU_A.Data_Collection_Rate	20	
	ColumnComp.PWM_CCU_B.Data_Collection_Rate	20	
	ColumnComp.PWM_CCL_A.Data_Collection_Rate	20	
	ColumnComp.PWM_CCL_B.Data_Collection_Rate	20	
	ColumnComp.Fan_Rear_ActualRPM.Data_Collection_Rate	20	
	Leak Sensors		
	ColumnComp.LEDBoard_LeakDiff.Data_Collection_Rate	20	
	ColumnComp.LEDBoard_A13.Data_Collection_Rate	20	
	ColumnComp.LEDBoard_A14.Data_Collection_Rate	20	
	ColumnComp.Oven_Gas_MuteTimeRemain.Data_Collection_Rate	20	
	=========================================================================================		
	Disable all TempCalibration settings before starting the test		
	=========================================================================================		
	ColumnComp.CC.TempCalibrationPointUpper1	Off	
	ColumnComp.CC.TempCalibrationPointUpper2	Off	
	ColumnComp.CC.TempCalibrationPointUpper3	Off	
	ColumnComp.CC.TempCalibrationPointUpper4	Off	
	ColumnComp.CC.TempCalibrationPointUpper5	Off	
	ColumnComp.CC.TempCalibrationPointUpper6	Off	
	ColumnComp.CC.TempCalibrationPointUpper7	Off	
	ColumnComp.CC.TempCalibrationPointUpper8	Off	
	ColumnComp.CC.TempCalibrationPointUpper9	Off	
	ColumnComp.CC.TempCalibrationPointUpper10	Off	
	ColumnComp.CC.TempCalibrationPointLower1	Off	
	ColumnComp.CC.TempCalibrationPointLower2	Off	
	ColumnComp.CC.TempCalibrationPointLower3	Off	
	ColumnComp.CC.TempCalibrationPointLower4	Off	
	ColumnComp.CC.TempCalibrationPointLower5	Off	
	ColumnComp.CC.TempCalibrationPointLower6	Off	
	ColumnComp.CC.TempCalibrationPointLower7	Off	
	ColumnComp.CC.TempCalibrationPointLower8	Off	
	ColumnComp.CC.TempCalibrationPointLower9	Off	
	ColumnComp.CC.TempCalibrationPointLower10	Off	
	=========================================================================================		
	Set all variables that will store calibration settings temporarely to 0		
	=========================================================================================		
	CCCalib.CalPointU01	0	
	CCCalib.CalDevU01	0	
	CCCalib.CalPointL01	0	
	CCCalib.CalDevL01	0	
	CCCalib.CalPointU02	0	
	CCCalib.CalDevU02	0	
	CCCalib.CalPointL02	0	
	CCCalib.CalDevL02	0	
	CCCalib.CalPointU03	0	
	CCCalib.CalDevU03	0	
	CCCalib.CalPointL03	0	
	CCCalib.CalDevL03	0	
	CCCalib.CalPointU04	0	
	CCCalib.CalDevU04	0	
	CCCalib.CalPointL04	0	
	CCCalib.CalDevL04	0	
	CCCalib.CalPointU05	0	
	CCCalib.CalDevU05	0	
	CCCalib.CalPointL05	0	
	CCCalib.CalDevL05	0	
	CCCalib.CalPointU06	0	
	CCCalib.CalDevU06	0	
	CCCalib.CalPointL06	0	
	CCCalib.CalDevL06	0	
	CCCalib.CalPointU07	0	
	CCCalib.CalDevU07	0	
	CCCalib.CalPointL07	0	
	CCCalib.CalDevL07	0	
	CCCalib.CalPointU08	0	
	CCCalib.CalDevU08	0	
	CCCalib.CalPointL08	0	
	CCCalib.CalDevL08	0	
	===========================================================================================		
	Reset of all Retention Times		
	===========================================================================================		
	RetTimes.RetTime1	0	
	RetTimes.RetTime2	0	
	RetTimes.RetTime3	0	
	RetTimes.RetTime4	0	
	RetTimes.RetTime5	0	
	RetTimes.RetTime6	0	
	RetTimes.RetTime7	0	
	RetTimes.RetTime8	0	
	============================================================================================		
	Set calibration temperatures for different CC types to variables, because otherwise ready check for VC-C10-A and VA-C10-A would fail for highest VH-C10-A temperatures		
	============================================================================================		
If		ColumnComp.ModelNo="VH-C10-A"	
	    Variables.GenericDouble0	115.0	Temperature before test start
	    Variables.GenericDouble1	120.0	First test temperature
	    Variables.GenericDouble2	100.0	Second test temperature
	    Variables.GenericDouble3	80.0	Third test temperature
	    Variables.GenericDouble4	60.0	Fourth test temperature
	    Variables.GenericDouble5	40.0	Fifth test temperature
	    Variables.GenericDouble6	20.0	Sixth test temperature
	    Variables.GenericDouble7	10.0	Seventh test temperature
	    Variables.GenericDouble8	5.0	Eighth test temperature
	    Variables.GenericBool0	1	Identificator for IRC insertion of correct temperature accuracy injection.
Else If		ColumnComp.ModelNo="VC-C10-A" OR ColumnComp.ModelNo="VA-C10-A"	
	    Variables.GenericDouble0	80.0	Temperature before test start
	    Variables.GenericDouble1	85.0	First test temperature
	    Variables.GenericDouble2	70.0	Second test temperature
	    Variables.GenericDouble3	55.0	Third test temperature
	    Variables.GenericDouble4	40.0	Fourth test temperature
	    Variables.GenericDouble5	30.0	Fifth test temperature
	    Variables.GenericDouble6	20.0	Sixth test temperature
	    Variables.GenericDouble7	10.0	Seventh test temperature
	    Variables.GenericDouble8	5.0	Eighth test temperature
	    Variables.GenericBool0	0	Identificator for IRC insertion of correct temperature accuracy injection.
Else			
	    Message	Invalid ModelNo! Please reinspect in production!	
	    System.AbortQueue		
End If			
	=========================================================================================		
	The first trigger works only, if the trigger conditions are not TRUE at the time the trigger is		
	activated. Therefore, at program start the temperature is set to the first test temperature minus 5 °C		
	to ensure, that temperature is more than 0.3 °C below the first test temperature when the trigger starts.		
	=========================================================================================		
-2.000	ColumnComp.CC.Temperature.Nominal	Variables.GenericDouble0	
	Wait	CC.TempReady	
0.000	StartRun		
	ColumnComp.CC_Temp.AcqOn		
	ColumnComp.CC_U_Temp_Actual.AcqOn		
	ColumnComp.CC_L_Temp_Actual.AcqOn		
	ColumnComp.CC_UCTL_TempRear_Actual.AcqOn		
	ColumnComp.PWM_CCU_A.AcqOn		
	ColumnComp.PWM_CCU_B.AcqOn		
	ColumnComp.PWM_CCL_A.AcqOn		
	ColumnComp.PWM_CCL_B.AcqOn		
	ColumnComp.Fan_Rear_ActualRPM.AcqOn		
	External measured temperatures		
	Thermometer1.ExtTemp_UpperCC.AcqOn		
	Thermometer1.ExtTemp_LowerCC.AcqOn		
	Thermometer.Environment_Temperature.AcqOn		
	Leak Sensor Evaluation		
	ColumnComp.LEDBoard_LeakDiff.AcqOn		
	ColumnComp.LEDBoard_A13.AcqOn		
	ColumnComp.LEDBoard_A14.AcqOn		
	ColumnComp.Oven_Gas_MuteTimeRemain.AcqOn		
0.000	Run	Duration = 500.000 [min]	
	ColumnComp.CC.Temperature.Nominal	Variables.GenericDouble1	
	Log	Variables.GenericBool0	
	=============================================================================================================================		
	The triggers are executed only if the difference between the temperature set point and the temperature reading on the VTCC		
	does not exceed 0.3°C.		
	When sample processing has been completed successfully, all DVar(n) correction factors are assigned to the related TCal(n)		
	temperature calibration values.		
	Calibration is automatically aborted when a calibration parameter is out of range. The valid range is -4K to +4K.		
	=============================================================================================================================		
Trigger		"T120/85",	Condition=Temp Ready and first test temperature set
	    Condition	(CC.TempReady) AND (CC.Temperature.Nominal=Variables.GenericDouble1)	
	    TrueTime	850.00	
	    Limit	1	
	    Hysteresis	0.0	
	    AllowImmediateExecution	No	
	CCCalib.CalPointU01	CC.TempActual_Upper	
	CCCalib.CalDevU01	ExtTemp_UpperCC.Signal-CC.TempActual_Upper	
	CCCalib.CalPointL01	CC.TempActual_Lower	
	CCCalib.CalDevL01	ExtTemp_LowerCC.Signal-CC.TempActual_Lower	
	RetTimes.RetTime1	System.Retention	
	Delay	1.0	
If		(CCCalib.CalDevU01>4) Or (CCCalib.CalDevU01<-4) OR (CCCalib.CalDevL01>4) OR (CCCalib.CalDevL01<-4)	
	    ColumnComp.CC.Temperature.Nominal	25.0	
	    ColumnComp.CC.TempCtrl	Off	
	    ColumnComp.CmdString	Cmd="LedBar.ForceColor=1"	
	    Message	Temperature calibration error! One calibration deviation is greater than 4°C.	
	    Message	QUEUE WILL BE ABORTED! Please check your test setup and repeat the calibration.	
	    ColumnComp.CmdString	Cmd="LedBar.ForceColor=0"	
	    System.AbortQueue		
End If			
	ColumnComp.CC.Temperature.Nominal	Variables.GenericDouble2	
End Trigger			
Trigger		"T100/70",	Condition=Temp Ready and second test temperature set
	    Condition	(CC.TempReady) AND (CC.Temperature.Nominal=Variables.GenericDouble2)	
	    TrueTime	850.00	
	    Limit	1	
	    Hysteresis	0.0	
	    AllowImmediateExecution	No	
	CCCalib.CalPointU02	CC.TempActual_Upper	
	CCCalib.CalDevU02	ExtTemp_UpperCC.Signal-CC.TempActual_Upper	
	CCCalib.CalPointL02	CC.TempActual_Lower	
	CCCalib.CalDevL02	ExtTemp_LowerCC.Signal-CC.TempActual_Lower	
	RetTimes.RetTime2	System.Retention	
	Delay	1.0	
If		(CCCalib.CalDevU02>4) Or (CCCalib.CalDevU02<-4) OR (CCCalib.CalDevL02>4) OR (CCCalib.CalDevL02<-4)	
	    ColumnComp.CC.Temperature.Nominal	25.0	
	    ColumnComp.CC.TempCtrl	Off	
	    ColumnComp.CmdString	Cmd="LedBar.ForceColor=1"	
	    Message	Temperature calibration error! One calibration deviation is greater than 4°C.	
	    Message	QUEUE WILL BE ABORTED! Please check your test setup and repeat the calibration.	
	    ColumnComp.CmdString	Cmd="LedBar.ForceColor=0"	
	    System.AbortQueue		
End If			
	ColumnComp.CC.Temperature.Nominal	Variables.GenericDouble3	
End Trigger			
Trigger		"T80/55",	Condition=Temp Ready and third test temperature set
	    Condition	(CC.TempReady) AND (CC.Temperature.Nominal=Variables.GenericDouble3)	
	    TrueTime	850.00	
	    Limit	1	
	    Hysteresis	0.0	
	    AllowImmediateExecution	No	
	CCCalib.CalPointU03	CC.TempActual_Upper	
	CCCalib.CalDevU03	ExtTemp_UpperCC.Signal-CC.TempActual_Upper	
	CCCalib.CalPointL03	CC.TempActual_Lower	
	CCCalib.CalDevL03	ExtTemp_LowerCC.Signal-CC.TempActual_Lower	
	RetTimes.RetTime3	System.Retention	
	Delay	1.0	
If		(CCCalib.CalDevU03>4) Or (CCCalib.CalDevU03<-4) OR (CCCalib.CalDevL03>4) OR (CCCalib.CalDevL03<-4)	
	    ColumnComp.CC.Temperature.Nominal	25.0	
	    ColumnComp.CC.TempCtrl	Off	
	    ColumnComp.CmdString	Cmd="LedBar.ForceColor=1"	
	    Message	Temperature calibration error! One calibration deviation is greater than 4°C.	
	    Message	QUEUE WILL BE ABORTED! Please check your test setup and repeat the calibration.	
	    ColumnComp.CmdString	Cmd="LedBar.ForceColor=0"	
	    System.AbortQueue		
End If			
	ColumnComp.CC.Temperature.Nominal	Variables.GenericDouble4	
End Trigger			
Trigger		"T60/40",	Condition=Temp Ready and fourth test temperature set
	    Condition	(CC.TempReady) AND (CC.Temperature.Nominal=Variables.GenericDouble4)	
	    TrueTime	850.00	
	    Limit	1	
	    Hysteresis	0.0	
	    AllowImmediateExecution	No	
	CCCalib.CalPointU04	CC.TempActual_Upper	
	CCCalib.CalDevU04	ExtTemp_UpperCC.Signal-CC.TempActual_Upper	
	CCCalib.CalPointL04	CC.TempActual_Lower	
	CCCalib.CalDevL04	ExtTemp_LowerCC.Signal-CC.TempActual_Lower	
	RetTimes.RetTime4	System.Retention	
	Delay	1.0	
If		(CCCalib.CalDevU04>4) Or (CCCalib.CalDevU04<-4) OR (CCCalib.CalDevL04>4) OR (CCCalib.CalDevL04<-4)	
	    ColumnComp.CC.Temperature.Nominal	25.0	
	    ColumnComp.CC.TempCtrl	Off	
	    ColumnComp.CmdString	Cmd="LedBar.ForceColor=1"	
	    Message	Temperature calibration error! One calibration deviation is greater than 4°C.	
	    Message	QUEUE WILL BE ABORTED! Please check your test setup and repeat the calibration.	
	    ColumnComp.CmdString	Cmd="LedBar.ForceColor=0"	
	    System.AbortQueue		
End If			
	ColumnComp.CC.Temperature.Nominal	Variables.GenericDouble5	
End Trigger			
Trigger		"T40/30",	Condition=Temp Ready and fifth test temperature set, the third condition was already implemented but not further explained.
	    Condition	(CC.TempReady) AND (CC.TempActual_Lower>=(Variables.GenericDouble5-0.3)) AND (CC.Temperature.Nominal=Variables.GenericDouble5)	
	    TrueTime	1150.00	
	    Limit	1	
	    Hysteresis	0.0	
	    AllowImmediateExecution	No	
	CCCalib.CalPointU05	CC.TempActual_Upper	
	CCCalib.CalDevU05	ExtTemp_UpperCC.Signal-CC.TempActual_Upper	
	CCCalib.CalPointL05	CC.TempActual_Lower	
	CCCalib.CalDevL05	ExtTemp_LowerCC.Signal-CC.TempActual_Lower	
	RetTimes.RetTime5	System.Retention	
	Delay	1.0	
If		(CCCalib.CalDevU05>4) Or (CCCalib.CalDevU05<-4) OR (CCCalib.CalDevL05>4) OR (CCCalib.CalDevL05<-4)	
	    ColumnComp.CC.Temperature.Nominal	25.0	
	    ColumnComp.CC.TempCtrl	Off	
	    ColumnComp.CmdString	Cmd="LedBar.ForceColor=1"	
	    Message	Temperature calibration error! One calibration deviation is greater than 4°C.	
	    Message	QUEUE WILL BE ABORTED! Please check your test setup and repeat the calibration.	
	    ColumnComp.CmdString	Cmd="LedBar.ForceColor=0"	
	    System.AbortQueue		
End If			
	ColumnComp.CC.Temperature.Nominal	Variables.GenericDouble6	
End Trigger			
Trigger		"T20",	Condition=Temp Ready and sixth test temperature set
	    Condition	(CC.TempReady) AND (CC.Temperature.Nominal=GenericDouble6)	
	    TrueTime	850.00	
	    Limit	1	
	    Hysteresis	0.0	
	    AllowImmediateExecution	No	
	CCCalib.CalPointU06	CC.TempActual_Upper	
	CCCalib.CalDevU06	ExtTemp_UpperCC.Signal-CC.TempActual_Upper	
	CCCalib.CalPointL06	CC.TempActual_Lower	
	CCCalib.CalDevL06	ExtTemp_LowerCC.Signal-CC.TempActual_Lower	
	RetTimes.RetTime6	System.Retention	
	Delay	1.0	
If		(CCCalib.CalDevU06>4) Or (CCCalib.CalDevU06<-4) OR (CCCalib.CalDevL06>4) OR (CCCalib.CalDevL06<-4)	
	    ColumnComp.CC.Temperature.Nominal	25.0	
	    ColumnComp.CC.TempCtrl	Off	
	    ColumnComp.CmdString	Cmd="LedBar.ForceColor=1"	
	    Message	Temperature calibration error! One calibration deviation is greater than 4°C.	
	    Message	QUEUE WILL BE ABORTED! Please check your test setup and repeat the calibration.	
	    ColumnComp.CmdString	Cmd="LedBar.ForceColor=0"	
	    System.AbortQueue		
End If			
	ColumnComp.CC.Temperature.Nominal	Variables.GenericDouble7	
End Trigger			
Trigger		"T10",	Condition=Temp Ready and seventh test temperature set
	    Condition	(CC.TempReady) AND (CC.Temperature.Nominal=GenericDouble7)	
	    TrueTime	850.00	
	    Limit	1	
	    Hysteresis	0.0	
	    AllowImmediateExecution	No	
	CCCalib.CalPointU07	CC.TempActual_Upper	
	CCCalib.CalDevU07	ExtTemp_UpperCC.Signal-CC.TempActual_Upper	
	CCCalib.CalPointL07	CC.TempActual_Lower	
	CCCalib.CalDevL07	ExtTemp_LowerCC.Signal-CC.TempActual_Lower	
	RetTimes.RetTime7	System.Retention	
	Delay	1.0	
If		(CCCalib.CalDevU07>4) Or (CCCalib.CalDevU07<-4) OR (CCCalib.CalDevL07>4) OR (CCCalib.CalDevL07<-4)	
	    ColumnComp.CC.Temperature.Nominal	25.0	
	    ColumnComp.CC.TempCtrl	Off	
	    ColumnComp.CmdString	Cmd="LedBar.ForceColor=1"	
	    Message	Temperature calibration error! One calibration deviation is greater than 4°C.	
	    Message	QUEUE WILL BE ABORTED! Please check your test setup and repeat the calibration.	
	    ColumnComp.CmdString	Cmd="LedBar.ForceColor=0"	
	    System.AbortQueue		
End If			
	ColumnComp.CC.Temperature.Nominal	Variables.GenericDouble8	
End Trigger			
Trigger		"T05",	Condition=Temp Ready and eighth test temperature set
	    Condition	(CC.TempReady) AND (CC.Temperature.Nominal=GenericDouble8)	
	    TrueTime	850.00	
	    Limit	1	
	    Hysteresis	0.0	
	    AllowImmediateExecution	No	
	CCCalib.CalPointU08	CC.TempActual_Upper	
	CCCalib.CalDevU08	ExtTemp_UpperCC.Signal-CC.TempActual_Upper	
	CCCalib.CalPointL08	CC.TempActual_Lower	
	CCCalib.CalDevL08	ExtTemp_LowerCC.Signal-CC.TempActual_Lower	
	RetTimes.RetTime8	System.Retention	
	Delay	1.0	
If		(CCCalib.CalDevU08>4) Or (CCCalib.CalDevU08<-4) OR (CCCalib.CalDevL08>4) OR (CCCalib.CalDevL08<-4)	
	    ColumnComp.CC.Temperature.Nominal	25.0	
	    ColumnComp.CC.TempCtrl	Off	
	    ColumnComp.CmdString	Cmd="LedBar.ForceColor=1"	
	    Message	Temperature calibration error! One calibration deviation is greater than 4°C.	
	    Message	QUEUE WILL BE ABORTED! Please check your test setup and repeat the calibration.	
	    ColumnComp.CmdString	Cmd="LedBar.ForceColor=0"	
	    System.AbortQueue		
End If			
	Set calibration parameters		
	ColumnComp.CC.TempCalibrationPointUpper1	CCCalib.CalPointU01	
	ColumnComp.CC.TempCalibrationDeviationUpper1	CCCalib.CalDevU01	
	ColumnComp.CC.TempCalibrationPointLower1	CCCalib.CalPointL01	
	ColumnComp.CC.TempCalibrationDeviationLower1	CCCalib.CalDevL01	
	ColumnComp.CC.TempCalibrationPointUpper2	CCCalib.CalPointU02	
	ColumnComp.CC.TempCalibrationDeviationUpper2	CCCalib.CalDevU02	
	ColumnComp.CC.TempCalibrationPointLower2	CCCalib.CalPointL02	
	ColumnComp.CC.TempCalibrationDeviationLower2	CCCalib.CalDevL02	
	ColumnComp.CC.TempCalibrationPointUpper3	CCCalib.CalPointU03	
	ColumnComp.CC.TempCalibrationDeviationUpper3	CCCalib.CalDevU03	
	ColumnComp.CC.TempCalibrationPointLower3	CCCalib.CalPointL03	
	ColumnComp.CC.TempCalibrationDeviationLower3	CCCalib.CalDevL03	
	ColumnComp.CC.TempCalibrationPointUpper4	CCCalib.CalPointU04	
	ColumnComp.CC.TempCalibrationDeviationUpper4	CCCalib.CalDevU04	
	ColumnComp.CC.TempCalibrationPointLower4	CCCalib.CalPointL04	
	ColumnComp.CC.TempCalibrationDeviationLower4	CCCalib.CalDevL04	
	ColumnComp.CC.TempCalibrationPointUpper5	CCCalib.CalPointU05	
	ColumnComp.CC.TempCalibrationDeviationUpper5	CCCalib.CalDevU05	
	ColumnComp.CC.TempCalibrationPointLower5	CCCalib.CalPointL05	
	ColumnComp.CC.TempCalibrationDeviationLower5	CCCalib.CalDevL05	
	ColumnComp.CC.TempCalibrationPointUpper6	CCCalib.CalPointU06	
	ColumnComp.CC.TempCalibrationDeviationUpper6	CCCalib.CalDevU06	
	ColumnComp.CC.TempCalibrationPointLower6	CCCalib.CalPointL06	
	ColumnComp.CC.TempCalibrationDeviationLower6	CCCalib.CalDevL06	
	ColumnComp.CC.TempCalibrationPointUpper7	CCCalib.CalPointU07	
	ColumnComp.CC.TempCalibrationDeviationUpper7	CCCalib.CalDevU07	
	ColumnComp.CC.TempCalibrationPointLower7	CCCalib.CalPointL07	
	ColumnComp.CC.TempCalibrationDeviationLower7	CCCalib.CalDevL07	
	ColumnComp.CC.TempCalibrationPointUpper8	CCCalib.CalPointU08	
	ColumnComp.CC.TempCalibrationDeviationUpper8	CCCalib.CalDevU08	
	ColumnComp.CC.TempCalibrationPointLower8	CCCalib.CalPointL08	
	ColumnComp.CC.TempCalibrationDeviationLower8	CCCalib.CalDevL08	
	Column commpartment		
	ColumnComp.CC_Temp.AcqOff		
	ColumnComp.CC_U_Temp_Actual.AcqOff		
	ColumnComp.CC_L_Temp_Actual.AcqOff		
	ColumnComp.CC_UCTL_TempRear_Actual.AcqOff		
	ColumnComp.PWM_CCU_A.AcqOff		
	ColumnComp.PWM_CCU_B.AcqOff		
	ColumnComp.PWM_CCL_A.AcqOff		
	ColumnComp.PWM_CCL_B.AcqOff		
	ColumnComp.Fan_Rear_ActualRPM.AcqOff		
	External measured temperatures		
	Thermometer1.ExtTemp_UpperCC.AcqOff		
	Thermometer1.ExtTemp_LowerCC.AcqOff		
	Thermometer.Environment_Temperature.AcqOff		
	Leak Sensor Evaluation		
	ColumnComp.LEDBoard_LeakDiff.AcqOff		
	ColumnComp.LEDBoard_A13.AcqOff		
	ColumnComp.LEDBoard_A14.AcqOff		
	ColumnComp.Oven_Gas_MuteTimeRemain.AcqOff		
	End		
End Trigger			
	=========================================================================================		
	These lines ensure that the column compartment is calibrated even if the triggers at 5 or 10 °C		
	where not activated. This happens most likely at high ambient temperature. We use the same deviations		
	than evaluated for 20 °C in this case.		
	When the trigger at nominal temperature of 20 °C or higher was not activated the sample is		
	aborted and the column compartment is not calibrated at all.		
	=========================================================================================		
If		(CCCalib.CalPointU06<>0) AND (CCCalib.CalPointL06)<>0	
500.000	    ColumnComp.CC.TempCalibrationPointUpper1	CCCalib.CalPointU01	
	    ColumnComp.CC.TempCalibrationDeviationUpper1	CCCalib.CalDevU01	
	    ColumnComp.CC.TempCalibrationPointLower1	CCCalib.CalPointL01	
	    ColumnComp.CC.TempCalibrationDeviationLower1	CCCalib.CalDevL01	
	    ColumnComp.CC.TempCalibrationPointUpper2	CCCalib.CalPointU02	
	    ColumnComp.CC.TempCalibrationDeviationUpper2	CCCalib.CalDevU02	
	    ColumnComp.CC.TempCalibrationPointLower2	CCCalib.CalPointL02	
	    ColumnComp.CC.TempCalibrationDeviationLower2	CCCalib.CalDevL02	
	    ColumnComp.CC.TempCalibrationPointUpper3	CCCalib.CalPointU03	
	    ColumnComp.CC.TempCalibrationDeviationUpper3	CCCalib.CalDevU03	
	    ColumnComp.CC.TempCalibrationPointLower3	CCCalib.CalPointL03	
	    ColumnComp.CC.TempCalibrationDeviationLower3	CCCalib.CalDevL03	
	    ColumnComp.CC.TempCalibrationPointUpper4	CCCalib.CalPointU04	
	    ColumnComp.CC.TempCalibrationDeviationUpper4	CCCalib.CalDevU04	
	    ColumnComp.CC.TempCalibrationPointLower4	CCCalib.CalPointL04	
	    ColumnComp.CC.TempCalibrationDeviationLower4	CCCalib.CalDevL04	
	    ColumnComp.CC.TempCalibrationPointUpper5	CCCalib.CalPointU05	
	    ColumnComp.CC.TempCalibrationDeviationUpper5	CCCalib.CalDevU05	
	    ColumnComp.CC.TempCalibrationPointLower5	CCCalib.CalPointL05	
	    ColumnComp.CC.TempCalibrationDeviationLower5	CCCalib.CalDevL05	
	    ColumnComp.CC.TempCalibrationPointUpper6	CCCalib.CalPointU06	
	    ColumnComp.CC.TempCalibrationDeviationUpper6	CCCalib.CalDevU06	
	    ColumnComp.CC.TempCalibrationPointLower6	CCCalib.CalPointL06	
	    ColumnComp.CC.TempCalibrationDeviationLower6	CCCalib.CalDevL06	
Else			
	    ColumnComp.CC.Temperature.Nominal	25.0	
	    ColumnComp.CC.TempCtrl	Off	
	    ColumnComp.CmdString	Cmd="LedBar.ForceColor=1"	
	    Message	Temperature calibration error! Column oven could not be calibrated at 20°C or higher.	
	    Message	QUEUE WILL BE ABORTED!	
	    ColumnComp.CmdString	Cmd="LedBar.ForceColor=0"	
	    System.AbortQueue		
End If			
If		CCCalib.CalPointU07<>0	
	    ColumnComp.CC.TempCalibrationPointUpper7	CCCalib.CalPointU07	
	    ColumnComp.CC.TempCalibrationDeviationUpper7	CCCalib.CalDevU07	
Else			
	    ColumnComp.CC.TempCalibrationPointUpper7	10	
	    ColumnComp.CC.TempCalibrationDeviationUpper7	CCCalib.CalDevU06	
End If			
If		CCCalib.CalPointL07<>0	
	    ColumnComp.CC.TempCalibrationPointLower7	CCCalib.CalPointL07	
	    ColumnComp.CC.TempCalibrationDeviationLower7	CCCalib.CalDevL07	
Else			
	    ColumnComp.CC.TempCalibrationPointLower7	10	
	    ColumnComp.CC.TempCalibrationDeviationLower7	CCCalib.CalDevL06	
End If			
If		CCCalib.CalPointU08<>0	
	    ColumnComp.CC.TempCalibrationPointUpper8	CCCalib.CalPointU08	
	    ColumnComp.CC.TempCalibrationDeviationUpper8	CCCalib.CalDevU08	
Else			
	    ColumnComp.CC.TempCalibrationPointUpper8	5	
	    ColumnComp.CC.TempCalibrationDeviationUpper8	CCCalib.CalDevU06	
End If			
If		CCCalib.CalPointL08<>0	
	    ColumnComp.CC.TempCalibrationPointLower8	CCCalib.CalPointL08	
	    ColumnComp.CC.TempCalibrationDeviationLower8	CCCalib.CalDevL08	
Else			
	    ColumnComp.CC.TempCalibrationPointLower8	5	
	    ColumnComp.CC.TempCalibrationDeviationLower8	CCCalib.CalDevL06	
End If			
	Column commpartment		
500.000	StopRun		
	ColumnComp.CC_Temp.AcqOff		
	ColumnComp.CC_U_Temp_Actual.AcqOff		
	ColumnComp.CC_L_Temp_Actual.AcqOff		
	ColumnComp.CC_UCTL_TempRear_Actual.AcqOff		
	ColumnComp.PWM_CCU_A.AcqOff		
	ColumnComp.PWM_CCU_B.AcqOff		
	ColumnComp.PWM_CCL_A.AcqOff		
	ColumnComp.PWM_CCL_B.AcqOff		
	ColumnComp.Fan_Rear_ActualRPM.AcqOff		
	External measured temperatures		
	Thermometer1.ExtTemp_UpperCC.AcqOff		
	Thermometer1.ExtTemp_LowerCC.AcqOff		
	Thermometer.Environment_Temperature.AcqOff		
	Leak Sensor Evaluation		
	ColumnComp.LEDBoard_LeakDiff.AcqOff		
	ColumnComp.LEDBoard_A13.AcqOff		
	ColumnComp.LEDBoard_A14.AcqOff		
	ColumnComp.Oven_Gas_MuteTimeRemain.AcqOff		
	ColumnComp.CC.Temperature.Nominal	25.0	
	End		
```

<a id="m-tcc-calibration-vcvh"></a>
## M-TCC-CALIBRATION-VCVH: TEMPERATURE_CALIBRATION

Applicable device evidence: **VC / VH**  
Source sequence(s): `VC:3000004, VH:6000001`  
Source SHA-256: `eec8f62b563d1d04cddf4be4174cacf98ca330df803098fc2d64bdaf90b3b163`  
Decoded flow rows: `466`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	=========================================================================================		
	IM to calibrate temperature of the VH-C10-A and VC-C10-A		
	=========================================================================================		
	HPLC-System:		
	-----------		
	VH-C10-A or VC-C10-A		
-2.700	Equilibration	Duration = 0.700 [min]	
	=========================================================================================		
	Parameters valid for the whole test.		
	=========================================================================================		
	If the difference between nominal and actual temperature is larger than ReadyTempDelta, the column compartement is not ready.		
	ColumnComp.CC.ReadyTempDelta	0.3 [°C]	Limit is set to 0.3 °C to use CC.TempReady for activating the trigger of the IM
	The Ready property will become Ready only if the difference between the actual and the nominal temperature will not exceed the ReadyTempDelta for the  time interval specified by EquilibrationTime.		
	ColumnComp.CC.EquilibrationTime	0.1 [min]	Time is so short to use CC.TempReady for activating the trigger of the IM (avoid unneccessary prolongation of temperature steps)
	The VTCC controls the temperature only, if TempCtrl is set to ON.		
	ColumnComp.CC.TempCtrl	On	
If		ColumnComp.ModelNo="VH-C10-A"	
	    ColumnComp.CmdString	Cmd="PCC.TempCtrl=0"	String necessary, because otherwise a way more complicated solution would be needed for using this IM for both CC types. Is equivalent to ColumnComp.PCC.TempCtrl=Off
Else			
End If			
	Adjusts FanSpeed and switches operating mode		
	ColumnComp.CC.Mode	StillAir	
	=========================================================================================		
	Liquid Leak Sensor remains switched off in order to avoid false alarms after great temperature changes		
	=========================================================================================		
	ColumnComp.LiquidLeakSensor	Off	
	=========================================================================================		
	Settings for the all channels offered for the column compartment by the driver.		
	Also debug channels are aqcuired.		
	=========================================================================================		
	Column commpartment		
	ColumnComp.CC_U_Temp_Actual.Data_Collection_Rate	20	
	ColumnComp.CC_L_Temp_Actual.Data_Collection_Rate	20	
	ColumnComp.CC_UCTL_TempRear_Actual.Data_Collection_Rate	20	
	ColumnComp.PWM_CCU_A.Data_Collection_Rate	20	
	ColumnComp.PWM_CCU_B.Data_Collection_Rate	20	
	ColumnComp.PWM_CCL_A.Data_Collection_Rate	20	
	ColumnComp.PWM_CCL_B.Data_Collection_Rate	20	
	ColumnComp.Fan_Rear_ActualRPM.Data_Collection_Rate	20	
	Leak Sensors		
	ColumnComp.LEDBoard_LeakDiff.Data_Collection_Rate	20	
	ColumnComp.LEDBoard_A13.Data_Collection_Rate	20	
	ColumnComp.LEDBoard_A14.Data_Collection_Rate	20	
	ColumnComp.Oven_Gas_MuteTimeRemain.Data_Collection_Rate	20	
	=========================================================================================		
	Disable all TempCalibration settings before starting the test		
	=========================================================================================		
	ColumnComp.CC.TempCalibrationPointUpper1	Off	
	ColumnComp.CC.TempCalibrationPointUpper2	Off	
	ColumnComp.CC.TempCalibrationPointUpper3	Off	
	ColumnComp.CC.TempCalibrationPointUpper4	Off	
	ColumnComp.CC.TempCalibrationPointUpper5	Off	
	ColumnComp.CC.TempCalibrationPointUpper6	Off	
	ColumnComp.CC.TempCalibrationPointUpper7	Off	
	ColumnComp.CC.TempCalibrationPointUpper8	Off	
	ColumnComp.CC.TempCalibrationPointUpper9	Off	
	ColumnComp.CC.TempCalibrationPointUpper10	Off	
	ColumnComp.CC.TempCalibrationPointLower1	Off	
	ColumnComp.CC.TempCalibrationPointLower2	Off	
	ColumnComp.CC.TempCalibrationPointLower3	Off	
	ColumnComp.CC.TempCalibrationPointLower4	Off	
	ColumnComp.CC.TempCalibrationPointLower5	Off	
	ColumnComp.CC.TempCalibrationPointLower6	Off	
	ColumnComp.CC.TempCalibrationPointLower7	Off	
	ColumnComp.CC.TempCalibrationPointLower8	Off	
	ColumnComp.CC.TempCalibrationPointLower9	Off	
	ColumnComp.CC.TempCalibrationPointLower10	Off	
	=========================================================================================		
	Set all variables that will store calibration settings temporarely to 0		
	=========================================================================================		
	CCCalib.CalPointU01	0	
	CCCalib.CalDevU01	0	
	CCCalib.CalPointL01	0	
	CCCalib.CalDevL01	0	
	CCCalib.CalPointU02	0	
	CCCalib.CalDevU02	0	
	CCCalib.CalPointL02	0	
	CCCalib.CalDevL02	0	
	CCCalib.CalPointU03	0	
	CCCalib.CalDevU03	0	
	CCCalib.CalPointL03	0	
	CCCalib.CalDevL03	0	
	CCCalib.CalPointU04	0	
	CCCalib.CalDevU04	0	
	CCCalib.CalPointL04	0	
	CCCalib.CalDevL04	0	
	CCCalib.CalPointU05	0	
	CCCalib.CalDevU05	0	
	CCCalib.CalPointL05	0	
	CCCalib.CalDevL05	0	
	CCCalib.CalPointU06	0	
	CCCalib.CalDevU06	0	
	CCCalib.CalPointL06	0	
	CCCalib.CalDevL06	0	
	CCCalib.CalPointU07	0	
	CCCalib.CalDevU07	0	
	CCCalib.CalPointL07	0	
	CCCalib.CalDevL07	0	
	CCCalib.CalPointU08	0	
	CCCalib.CalDevU08	0	
	CCCalib.CalPointL08	0	
	CCCalib.CalDevL08	0	
	===========================================================================================		
	Reset of all Retention Times		
	===========================================================================================		
	RetTimes.RetTime1	0	
	RetTimes.RetTime2	0	
	RetTimes.RetTime3	0	
	RetTimes.RetTime4	0	
	RetTimes.RetTime5	0	
	RetTimes.RetTime6	0	
	RetTimes.RetTime7	0	
	RetTimes.RetTime8	0	
	============================================================================================		
	Set calibration temperatures for different CC types to variables, because otherwise ready check for VC-C10-A would fail for highest VH-C10-A temperatures		
	============================================================================================		
If		ColumnComp.ModelNo="VH-C10-A"	
	    Variables.GenericDouble0	115.0	Temperature before test start
	    Variables.GenericDouble1	120.0	First test temperature
	    Variables.GenericDouble2	100.0	Second test temperature
	    Variables.GenericDouble3	80.0	Third test temperature
	    Variables.GenericDouble4	60.0	Fourth test temperature
	    Variables.GenericDouble5	40.0	Fifth test temperature
	    Variables.GenericDouble6	20.0	Sixth test temperature
	    Variables.GenericDouble7	10.0	Seventh test temperature
	    Variables.GenericDouble8	5.0	Eighth test temperature
	    Variables.GenericBool0	1	Identificator for IRC insertion of correct temperature accuracy injection.
Else If		ColumnComp.ModelNo="VC-C10-A"	
	    Variables.GenericDouble0	80.0	Temperature before test start
	    Variables.GenericDouble1	85.0	First test temperature
	    Variables.GenericDouble2	70.0	Second test temperature
	    Variables.GenericDouble3	55.0	Third test temperature
	    Variables.GenericDouble4	40.0	Fourth test temperature
	    Variables.GenericDouble5	30.0	Fifth test temperature
	    Variables.GenericDouble6	20.0	Sixth test temperature
	    Variables.GenericDouble7	10.0	Seventh test temperature
	    Variables.GenericDouble8	5.0	Eighth test temperature
	    Variables.GenericBool0	0	Identificator for IRC insertion of correct temperature accuracy injection.
Else			
	    Message	Invalid ModelNo! Please reinspect in production!	
	    System.AbortQueue		
End If			
	=========================================================================================		
	The first trigger works only, if the trigger conditions are not TRUE at the time the trigger is		
	activated. Therefore, at program start the temperature is set to the first test temperature minus 5 °C		
	to ensure, that temperature is more than 0.3 °C below the first test temperature when the trigger starts.		
	=========================================================================================		
-2.000	ColumnComp.CC.Temperature.Nominal	Variables.GenericDouble0	
	Wait	CC.TempReady	
0.000	StartRun		
	ColumnComp.CC_Temp.AcqOn		
	ColumnComp.CC_U_Temp_Actual.AcqOn		
	ColumnComp.CC_L_Temp_Actual.AcqOn		
	ColumnComp.CC_UCTL_TempRear_Actual.AcqOn		
	ColumnComp.PWM_CCU_A.AcqOn		
	ColumnComp.PWM_CCU_B.AcqOn		
	ColumnComp.PWM_CCL_A.AcqOn		
	ColumnComp.PWM_CCL_B.AcqOn		
	ColumnComp.Fan_Rear_ActualRPM.AcqOn		
	External measured temperatures		
	Thermometer1.ExtTemp_UpperCC.AcqOn		
	Thermometer1.ExtTemp_LowerCC.AcqOn		
	Thermometer.Environment_Temperature.AcqOn		
	Leak Sensor Evaluation		
	ColumnComp.LEDBoard_LeakDiff.AcqOn		
	ColumnComp.LEDBoard_A13.AcqOn		
	ColumnComp.LEDBoard_A14.AcqOn		
	ColumnComp.Oven_Gas_MuteTimeRemain.AcqOn		
0.000	Run	Duration = 500.000 [min]	
	ColumnComp.CC.Temperature.Nominal	Variables.GenericDouble1	
	Log	Variables.GenericBool0	
	=============================================================================================================================		
	The triggers are executed only if the difference between the temperature set point and the temperature reading on the VTCC		
	does not exceed 0.3°C.		
	When sample processing has been completed successfully, all DVar(n) correction factors are assigned to the related TCal(n)		
	temperature calibration values.		
	Calibration is automatically aborted when a calibration parameter is out of range. The valid range is -4K to +4K.		
	=============================================================================================================================		
Trigger		"T120/85",	Condition=Temp Ready and first test temperature set
	    Condition	(CC.TempReady) AND (CC.Temperature.Nominal=Variables.GenericDouble1)	
	    TrueTime	850.00	
	    Limit	1	
	    Hysteresis	0.0	
	    AllowImmediateExecution	No	
	CCCalib.CalPointU01	CC.TempActual_Upper	
	CCCalib.CalDevU01	ExtTemp_UpperCC.Signal-CC.TempActual_Upper	
	CCCalib.CalPointL01	CC.TempActual_Lower	
	CCCalib.CalDevL01	ExtTemp_LowerCC.Signal-CC.TempActual_Lower	
	RetTimes.RetTime1	System.Retention	
	Delay	1.0	
If		(CCCalib.CalDevU01>4) Or (CCCalib.CalDevU01<-4) OR (CCCalib.CalDevL01>4) OR (CCCalib.CalDevL01<-4)	
	    ColumnComp.CC.Temperature.Nominal	25.0	
	    ColumnComp.CC.TempCtrl	Off	
	    ColumnComp.CmdString	Cmd="LedBar.ForceColor=1"	
	    Message	Temperature calibration error! One calibration deviation is greater than 4°C.	
	    Message	QUEUE WILL BE ABORTED! Please check your test setup and repeat the calibration.	
	    ColumnComp.CmdString	Cmd="LedBar.ForceColor=0"	
	    System.AbortQueue		
End If			
	ColumnComp.CC.Temperature.Nominal	Variables.GenericDouble2	
End Trigger			
Trigger		"T100/70",	Condition=Temp Ready and second test temperature set
	    Condition	(CC.TempReady) AND (CC.Temperature.Nominal=Variables.GenericDouble2)	
	    TrueTime	850.00	
	    Limit	1	
	    Hysteresis	0.0	
	    AllowImmediateExecution	No	
	CCCalib.CalPointU02	CC.TempActual_Upper	
	CCCalib.CalDevU02	ExtTemp_UpperCC.Signal-CC.TempActual_Upper	
	CCCalib.CalPointL02	CC.TempActual_Lower	
	CCCalib.CalDevL02	ExtTemp_LowerCC.Signal-CC.TempActual_Lower	
	RetTimes.RetTime2	System.Retention	
	Delay	1.0	
If		(CCCalib.CalDevU02>4) Or (CCCalib.CalDevU02<-4) OR (CCCalib.CalDevL02>4) OR (CCCalib.CalDevL02<-4)	
	    ColumnComp.CC.Temperature.Nominal	25.0	
	    ColumnComp.CC.TempCtrl	Off	
	    ColumnComp.CmdString	Cmd="LedBar.ForceColor=1"	
	    Message	Temperature calibration error! One calibration deviation is greater than 4°C.	
	    Message	QUEUE WILL BE ABORTED! Please check your test setup and repeat the calibration.	
	    ColumnComp.CmdString	Cmd="LedBar.ForceColor=0"	
	    System.AbortQueue		
End If			
	ColumnComp.CC.Temperature.Nominal	Variables.GenericDouble3	
End Trigger			
Trigger		"T80/55",	Condition=Temp Ready and third test temperature set
	    Condition	(CC.TempReady) AND (CC.Temperature.Nominal=Variables.GenericDouble3)	
	    TrueTime	850.00	
	    Limit	1	
	    Hysteresis	0.0	
	    AllowImmediateExecution	No	
	CCCalib.CalPointU03	CC.TempActual_Upper	
	CCCalib.CalDevU03	ExtTemp_UpperCC.Signal-CC.TempActual_Upper	
	CCCalib.CalPointL03	CC.TempActual_Lower	
	CCCalib.CalDevL03	ExtTemp_LowerCC.Signal-CC.TempActual_Lower	
	RetTimes.RetTime3	System.Retention	
	Delay	1.0	
If		(CCCalib.CalDevU03>4) Or (CCCalib.CalDevU03<-4) OR (CCCalib.CalDevL03>4) OR (CCCalib.CalDevL03<-4)	
	    ColumnComp.CC.Temperature.Nominal	25.0	
	    ColumnComp.CC.TempCtrl	Off	
	    ColumnComp.CmdString	Cmd="LedBar.ForceColor=1"	
	    Message	Temperature calibration error! One calibration deviation is greater than 4°C.	
	    Message	QUEUE WILL BE ABORTED! Please check your test setup and repeat the calibration.	
	    ColumnComp.CmdString	Cmd="LedBar.ForceColor=0"	
	    System.AbortQueue		
End If			
	ColumnComp.CC.Temperature.Nominal	Variables.GenericDouble4	
End Trigger			
Trigger		"T60/40",	Condition=Temp Ready and fourth test temperature set
	    Condition	(CC.TempReady) AND (CC.Temperature.Nominal=Variables.GenericDouble4)	
	    TrueTime	850.00	
	    Limit	1	
	    Hysteresis	0.0	
	    AllowImmediateExecution	No	
	CCCalib.CalPointU04	CC.TempActual_Upper	
	CCCalib.CalDevU04	ExtTemp_UpperCC.Signal-CC.TempActual_Upper	
	CCCalib.CalPointL04	CC.TempActual_Lower	
	CCCalib.CalDevL04	ExtTemp_LowerCC.Signal-CC.TempActual_Lower	
	RetTimes.RetTime4	System.Retention	
	Delay	1.0	
If		(CCCalib.CalDevU04>4) Or (CCCalib.CalDevU04<-4) OR (CCCalib.CalDevL04>4) OR (CCCalib.CalDevL04<-4)	
	    ColumnComp.CC.Temperature.Nominal	25.0	
	    ColumnComp.CC.TempCtrl	Off	
	    ColumnComp.CmdString	Cmd="LedBar.ForceColor=1"	
	    Message	Temperature calibration error! One calibration deviation is greater than 4°C.	
	    Message	QUEUE WILL BE ABORTED! Please check your test setup and repeat the calibration.	
	    ColumnComp.CmdString	Cmd="LedBar.ForceColor=0"	
	    System.AbortQueue		
End If			
	ColumnComp.CC.Temperature.Nominal	Variables.GenericDouble5	
End Trigger			
Trigger		"T40/30",	Condition=Temp Ready and fifth test temperature set, the third condition was already implemented but not further explained.
	    Condition	(CC.TempReady) AND (CC.TempActual_Lower>=(Variables.GenericDouble5-0.3)) AND (CC.Temperature.Nominal=Variables.GenericDouble5)	
	    TrueTime	1150.00	
	    Limit	1	
	    Hysteresis	0.0	
	    AllowImmediateExecution	No	
	CCCalib.CalPointU05	CC.TempActual_Upper	
	CCCalib.CalDevU05	ExtTemp_UpperCC.Signal-CC.TempActual_Upper	
	CCCalib.CalPointL05	CC.TempActual_Lower	
	CCCalib.CalDevL05	ExtTemp_LowerCC.Signal-CC.TempActual_Lower	
	RetTimes.RetTime5	System.Retention	
	Delay	1.0	
If		(CCCalib.CalDevU05>4) Or (CCCalib.CalDevU05<-4) OR (CCCalib.CalDevL05>4) OR (CCCalib.CalDevL05<-4)	
	    ColumnComp.CC.Temperature.Nominal	25.0	
	    ColumnComp.CC.TempCtrl	Off	
	    ColumnComp.CmdString	Cmd="LedBar.ForceColor=1"	
	    Message	Temperature calibration error! One calibration deviation is greater than 4°C.	
	    Message	QUEUE WILL BE ABORTED! Please check your test setup and repeat the calibration.	
	    ColumnComp.CmdString	Cmd="LedBar.ForceColor=0"	
	    System.AbortQueue		
End If			
	ColumnComp.CC.Temperature.Nominal	Variables.GenericDouble6	
End Trigger			
Trigger		"T20",	Condition=Temp Ready and sixth test temperature set
	    Condition	(CC.TempReady) AND (CC.Temperature.Nominal=GenericDouble6)	
	    TrueTime	850.00	
	    Limit	1	
	    Hysteresis	0.0	
	    AllowImmediateExecution	No	
	CCCalib.CalPointU06	CC.TempActual_Upper	
	CCCalib.CalDevU06	ExtTemp_UpperCC.Signal-CC.TempActual_Upper	
	CCCalib.CalPointL06	CC.TempActual_Lower	
	CCCalib.CalDevL06	ExtTemp_LowerCC.Signal-CC.TempActual_Lower	
	RetTimes.RetTime6	System.Retention	
	Delay	1.0	
If		(CCCalib.CalDevU06>4) Or (CCCalib.CalDevU06<-4) OR (CCCalib.CalDevL06>4) OR (CCCalib.CalDevL06<-4)	
	    ColumnComp.CC.Temperature.Nominal	25.0	
	    ColumnComp.CC.TempCtrl	Off	
	    ColumnComp.CmdString	Cmd="LedBar.ForceColor=1"	
	    Message	Temperature calibration error! One calibration deviation is greater than 4°C.	
	    Message	QUEUE WILL BE ABORTED! Please check your test setup and repeat the calibration.	
	    ColumnComp.CmdString	Cmd="LedBar.ForceColor=0"	
	    System.AbortQueue		
End If			
	ColumnComp.CC.Temperature.Nominal	Variables.GenericDouble7	
End Trigger			
Trigger		"T10",	Condition=Temp Ready and seventh test temperature set
	    Condition	(CC.TempReady) AND (CC.Temperature.Nominal=GenericDouble7)	
	    TrueTime	850.00	
	    Limit	1	
	    Hysteresis	0.0	
	    AllowImmediateExecution	No	
	CCCalib.CalPointU07	CC.TempActual_Upper	
	CCCalib.CalDevU07	ExtTemp_UpperCC.Signal-CC.TempActual_Upper	
	CCCalib.CalPointL07	CC.TempActual_Lower	
	CCCalib.CalDevL07	ExtTemp_LowerCC.Signal-CC.TempActual_Lower	
	RetTimes.RetTime7	System.Retention	
	Delay	1.0	
If		(CCCalib.CalDevU07>4) Or (CCCalib.CalDevU07<-4) OR (CCCalib.CalDevL07>4) OR (CCCalib.CalDevL07<-4)	
	    ColumnComp.CC.Temperature.Nominal	25.0	
	    ColumnComp.CC.TempCtrl	Off	
	    ColumnComp.CmdString	Cmd="LedBar.ForceColor=1"	
	    Message	Temperature calibration error! One calibration deviation is greater than 4°C.	
	    Message	QUEUE WILL BE ABORTED! Please check your test setup and repeat the calibration.	
	    ColumnComp.CmdString	Cmd="LedBar.ForceColor=0"	
	    System.AbortQueue		
End If			
	ColumnComp.CC.Temperature.Nominal	Variables.GenericDouble8	
End Trigger			
Trigger		"T05",	Condition=Temp Ready and eighth test temperature set
	    Condition	(CC.TempReady) AND (CC.Temperature.Nominal=GenericDouble8)	
	    TrueTime	850.00	
	    Limit	1	
	    Hysteresis	0.0	
	    AllowImmediateExecution	No	
	CCCalib.CalPointU08	CC.TempActual_Upper	
	CCCalib.CalDevU08	ExtTemp_UpperCC.Signal-CC.TempActual_Upper	
	CCCalib.CalPointL08	CC.TempActual_Lower	
	CCCalib.CalDevL08	ExtTemp_LowerCC.Signal-CC.TempActual_Lower	
	RetTimes.RetTime8	System.Retention	
	Delay	1.0	
If		(CCCalib.CalDevU08>4) Or (CCCalib.CalDevU08<-4) OR (CCCalib.CalDevL08>4) OR (CCCalib.CalDevL08<-4)	
	    ColumnComp.CC.Temperature.Nominal	25.0	
	    ColumnComp.CC.TempCtrl	Off	
	    ColumnComp.CmdString	Cmd="LedBar.ForceColor=1"	
	    Message	Temperature calibration error! One calibration deviation is greater than 4°C.	
	    Message	QUEUE WILL BE ABORTED! Please check your test setup and repeat the calibration.	
	    ColumnComp.CmdString	Cmd="LedBar.ForceColor=0"	
	    System.AbortQueue		
End If			
	Set calibration parameters		
	ColumnComp.CC.TempCalibrationPointUpper1	CCCalib.CalPointU01	
	ColumnComp.CC.TempCalibrationDeviationUpper1	CCCalib.CalDevU01	
	ColumnComp.CC.TempCalibrationPointLower1	CCCalib.CalPointL01	
	ColumnComp.CC.TempCalibrationDeviationLower1	CCCalib.CalDevL01	
	ColumnComp.CC.TempCalibrationPointUpper2	CCCalib.CalPointU02	
	ColumnComp.CC.TempCalibrationDeviationUpper2	CCCalib.CalDevU02	
	ColumnComp.CC.TempCalibrationPointLower2	CCCalib.CalPointL02	
	ColumnComp.CC.TempCalibrationDeviationLower2	CCCalib.CalDevL02	
	ColumnComp.CC.TempCalibrationPointUpper3	CCCalib.CalPointU03	
	ColumnComp.CC.TempCalibrationDeviationUpper3	CCCalib.CalDevU03	
	ColumnComp.CC.TempCalibrationPointLower3	CCCalib.CalPointL03	
	ColumnComp.CC.TempCalibrationDeviationLower3	CCCalib.CalDevL03	
	ColumnComp.CC.TempCalibrationPointUpper4	CCCalib.CalPointU04	
	ColumnComp.CC.TempCalibrationDeviationUpper4	CCCalib.CalDevU04	
	ColumnComp.CC.TempCalibrationPointLower4	CCCalib.CalPointL04	
	ColumnComp.CC.TempCalibrationDeviationLower4	CCCalib.CalDevL04	
	ColumnComp.CC.TempCalibrationPointUpper5	CCCalib.CalPointU05	
	ColumnComp.CC.TempCalibrationDeviationUpper5	CCCalib.CalDevU05	
	ColumnComp.CC.TempCalibrationPointLower5	CCCalib.CalPointL05	
	ColumnComp.CC.TempCalibrationDeviationLower5	CCCalib.CalDevL05	
	ColumnComp.CC.TempCalibrationPointUpper6	CCCalib.CalPointU06	
	ColumnComp.CC.TempCalibrationDeviationUpper6	CCCalib.CalDevU06	
	ColumnComp.CC.TempCalibrationPointLower6	CCCalib.CalPointL06	
	ColumnComp.CC.TempCalibrationDeviationLower6	CCCalib.CalDevL06	
	ColumnComp.CC.TempCalibrationPointUpper7	CCCalib.CalPointU07	
	ColumnComp.CC.TempCalibrationDeviationUpper7	CCCalib.CalDevU07	
	ColumnComp.CC.TempCalibrationPointLower7	CCCalib.CalPointL07	
	ColumnComp.CC.TempCalibrationDeviationLower7	CCCalib.CalDevL07	
	ColumnComp.CC.TempCalibrationPointUpper8	CCCalib.CalPointU08	
	ColumnComp.CC.TempCalibrationDeviationUpper8	CCCalib.CalDevU08	
	ColumnComp.CC.TempCalibrationPointLower8	CCCalib.CalPointL08	
	ColumnComp.CC.TempCalibrationDeviationLower8	CCCalib.CalDevL08	
	Column commpartment		
	ColumnComp.CC_Temp.AcqOff		
	ColumnComp.CC_U_Temp_Actual.AcqOff		
	ColumnComp.CC_L_Temp_Actual.AcqOff		
	ColumnComp.CC_UCTL_TempRear_Actual.AcqOff		
	ColumnComp.PWM_CCU_A.AcqOff		
	ColumnComp.PWM_CCU_B.AcqOff		
	ColumnComp.PWM_CCL_A.AcqOff		
	ColumnComp.PWM_CCL_B.AcqOff		
	ColumnComp.Fan_Rear_ActualRPM.AcqOff		
	External measured temperatures		
	Thermometer1.ExtTemp_UpperCC.AcqOff		
	Thermometer1.ExtTemp_LowerCC.AcqOff		
	Thermometer.Environment_Temperature.AcqOff		
	Leak Sensor Evaluation		
	ColumnComp.LEDBoard_LeakDiff.AcqOff		
	ColumnComp.LEDBoard_A13.AcqOff		
	ColumnComp.LEDBoard_A14.AcqOff		
	ColumnComp.Oven_Gas_MuteTimeRemain.AcqOff		
	End		
End Trigger			
	=========================================================================================		
	These lines ensure that the column compartment is calibrated even if the triggers at 5 or 10 °C		
	where not activated. This happens most likely at high ambient temperature. We use the same deviations		
	than evaluated for 20 °C in this case.		
	When the trigger at nominal temperature of 20 °C or higher was not activated the sample is		
	aborted and the column compartment is not calibrated at all.		
	=========================================================================================		
If		(CCCalib.CalPointU06<>0) AND (CCCalib.CalPointL06)<>0	
500.000	    ColumnComp.CC.TempCalibrationPointUpper1	CCCalib.CalPointU01	
	    ColumnComp.CC.TempCalibrationDeviationUpper1	CCCalib.CalDevU01	
	    ColumnComp.CC.TempCalibrationPointLower1	CCCalib.CalPointL01	
	    ColumnComp.CC.TempCalibrationDeviationLower1	CCCalib.CalDevL01	
	    ColumnComp.CC.TempCalibrationPointUpper2	CCCalib.CalPointU02	
	    ColumnComp.CC.TempCalibrationDeviationUpper2	CCCalib.CalDevU02	
	    ColumnComp.CC.TempCalibrationPointLower2	CCCalib.CalPointL02	
	    ColumnComp.CC.TempCalibrationDeviationLower2	CCCalib.CalDevL02	
	    ColumnComp.CC.TempCalibrationPointUpper3	CCCalib.CalPointU03	
	    ColumnComp.CC.TempCalibrationDeviationUpper3	CCCalib.CalDevU03	
	    ColumnComp.CC.TempCalibrationPointLower3	CCCalib.CalPointL03	
	    ColumnComp.CC.TempCalibrationDeviationLower3	CCCalib.CalDevL03	
	    ColumnComp.CC.TempCalibrationPointUpper4	CCCalib.CalPointU04	
	    ColumnComp.CC.TempCalibrationDeviationUpper4	CCCalib.CalDevU04	
	    ColumnComp.CC.TempCalibrationPointLower4	CCCalib.CalPointL04	
	    ColumnComp.CC.TempCalibrationDeviationLower4	CCCalib.CalDevL04	
	    ColumnComp.CC.TempCalibrationPointUpper5	CCCalib.CalPointU05	
	    ColumnComp.CC.TempCalibrationDeviationUpper5	CCCalib.CalDevU05	
	    ColumnComp.CC.TempCalibrationPointLower5	CCCalib.CalPointL05	
	    ColumnComp.CC.TempCalibrationDeviationLower5	CCCalib.CalDevL05	
	    ColumnComp.CC.TempCalibrationPointUpper6	CCCalib.CalPointU06	
	    ColumnComp.CC.TempCalibrationDeviationUpper6	CCCalib.CalDevU06	
	    ColumnComp.CC.TempCalibrationPointLower6	CCCalib.CalPointL06	
	    ColumnComp.CC.TempCalibrationDeviationLower6	CCCalib.CalDevL06	
Else			
	    ColumnComp.CC.Temperature.Nominal	25.0	
	    ColumnComp.CC.TempCtrl	Off	
	    ColumnComp.CmdString	Cmd="LedBar.ForceColor=1"	
	    Message	Temperature calibration error! Column oven could not be calibrated at 20°C or higher.	
	    Message	QUEUE WILL BE ABORTED!	
	    ColumnComp.CmdString	Cmd="LedBar.ForceColor=0"	
	    System.AbortQueue		
End If			
If		CCCalib.CalPointU07<>0	
	    ColumnComp.CC.TempCalibrationPointUpper7	CCCalib.CalPointU07	
	    ColumnComp.CC.TempCalibrationDeviationUpper7	CCCalib.CalDevU07	
Else			
	    ColumnComp.CC.TempCalibrationPointUpper7	10	
	    ColumnComp.CC.TempCalibrationDeviationUpper7	CCCalib.CalDevU06	
End If			
If		CCCalib.CalPointL07<>0	
	    ColumnComp.CC.TempCalibrationPointLower7	CCCalib.CalPointL07	
	    ColumnComp.CC.TempCalibrationDeviationLower7	CCCalib.CalDevL07	
Else			
	    ColumnComp.CC.TempCalibrationPointLower7	10	
	    ColumnComp.CC.TempCalibrationDeviationLower7	CCCalib.CalDevL06	
End If			
If		CCCalib.CalPointU08<>0	
	    ColumnComp.CC.TempCalibrationPointUpper8	CCCalib.CalPointU08	
	    ColumnComp.CC.TempCalibrationDeviationUpper8	CCCalib.CalDevU08	
Else			
	    ColumnComp.CC.TempCalibrationPointUpper8	5	
	    ColumnComp.CC.TempCalibrationDeviationUpper8	CCCalib.CalDevU06	
End If			
If		CCCalib.CalPointL08<>0	
	    ColumnComp.CC.TempCalibrationPointLower8	CCCalib.CalPointL08	
	    ColumnComp.CC.TempCalibrationDeviationLower8	CCCalib.CalDevL08	
Else			
	    ColumnComp.CC.TempCalibrationPointLower8	5	
	    ColumnComp.CC.TempCalibrationDeviationLower8	CCCalib.CalDevL06	
End If			
	Column commpartment		
500.000	StopRun		
	ColumnComp.CC_Temp.AcqOff		
	ColumnComp.CC_U_Temp_Actual.AcqOff		
	ColumnComp.CC_L_Temp_Actual.AcqOff		
	ColumnComp.CC_UCTL_TempRear_Actual.AcqOff		
	ColumnComp.PWM_CCU_A.AcqOff		
	ColumnComp.PWM_CCU_B.AcqOff		
	ColumnComp.PWM_CCL_A.AcqOff		
	ColumnComp.PWM_CCL_B.AcqOff		
	ColumnComp.Fan_Rear_ActualRPM.AcqOff		
	External measured temperatures		
	Thermometer1.ExtTemp_UpperCC.AcqOff		
	Thermometer1.ExtTemp_LowerCC.AcqOff		
	Thermometer.Environment_Temperature.AcqOff		
	Leak Sensor Evaluation		
	ColumnComp.LEDBoard_LeakDiff.AcqOff		
	ColumnComp.LEDBoard_A13.AcqOff		
	ColumnComp.LEDBoard_A14.AcqOff		
	ColumnComp.Oven_Gas_MuteTimeRemain.AcqOff		
	ColumnComp.CC.Temperature.Nominal	25.0	
	End		
```

<a id="m-tcc-precision"></a>
## M-TCC-PRECISION: TEMPERATURE_PRECISION

Applicable device evidence: **VA**  
Source sequence(s): `VA:0000003`  
Source SHA-256: `9d7697955adb75a40d179db9373ea9b669cf5379d916deb6a938fd4177e52baa`  
Decoded flow rows: `124`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	=========================================================================================		
	IM to measure the temperature precision of the Vanquish VH-C10-A, VC-C10-A and VA-C10-A		
	=========================================================================================		
	HPLC-System:		
	-----------		
	VH-C10-A, VC-C10-A or VA-C10-A		
-30.000	Equilibration	Duration = 30.000 [min]	
	Different total pages counts are used for VH-C10-A, VC-C10-A (no PCC) and VA-C10-A. This is set here		
If		ColumnComp.ModelNo="VH-C10-A"	
	    Variables.GenericLong9	12	
	    Delay	1	[Val_FOQ_CM7_ekugelma_07-Jul-2020]: OK
	    Log	GenericLong9	
Else If		ColumnComp.ModelNo="VC-C10-A" OR ColumnComp.ModelNo="VA-C10-A"	
	    Variables.GenericLong9	10	
	    Delay	1	[Val_FOQ_CM7_ekugelma_07-Jul-2020]: OK
	    Log	GenericLong9	
Else			
	    Message	Column compartment model unknown, please reinspect in production!	
	    System.AbortQueue		
End If			
	Determine IM for next injection		
If		ColumnComp.ModelNo="VH-C10-A"	
	    Variables.GenericBool0	1	Identificator for IRC insertion of correct temperature stability injection.
Else If		ColumnComp.ModelNo="VC-C10-A" OR ColumnComp.ModelNo="VA-C10-A"	
	    Variables.GenericBool0	0	Identificator for IRC insertion of correct temperature stability injection.
Else			
	    Message	Invalid ModelNo! Please reinspect in production!	
	    System.AbortQueue		
End If			
	=========================================================================================		
	Parameters valid for the whole test.		
	=========================================================================================		
	If the difference between nominal and actual temperature is larger than		
	ReadyTempDelta, the oven is not ready.		
	ColumnComp.CC.ReadyTempDelta	0.1 [°C]	
	The Ready property will become Ready only if the difference between the		
	actual and the nominal temperature will not exceed the ReadyTempDelta for		
	the  time interval specified by EquilibrationTime.		
	ColumnComp.CC.EquilibrationTime	0.5 [min]	
	The VTCC adjusts the temperature only, if TempCtrl is set to ON.		
	ColumnComp.CC.TempCtrl	On	
	Adjusts FanSpeed and switches operating mode		
	ColumnComp.CC.Mode	StillAir	
	Liquid Leak Sensor remains switched off in order to avoid false alarms after great temperature changes. It is switched on during this IM and calibrated afterwards		
	=========================================================================================		
	ColumnComp.LiquidLeakSensor	Off	
	=========================================================================================		
	Settings for the all channels offered for the column compartment by the driver.		
	Also debug channels are aqcuired.		
	=========================================================================================		
	Column commpartment		
	ColumnComp.CC_U_Temp_Actual.Data_Collection_Rate	20	
	ColumnComp.CC_L_Temp_Actual.Data_Collection_Rate	20	
	ColumnComp.CC_UCTL_TempRear_Actual.Data_Collection_Rate	20	
	ColumnComp.PWM_CCU_A.Data_Collection_Rate	20	
	ColumnComp.PWM_CCU_B.Data_Collection_Rate	20	
	ColumnComp.PWM_CCL_A.Data_Collection_Rate	20	
	ColumnComp.PWM_CCL_B.Data_Collection_Rate	20	
	ColumnComp.Fan_Rear_ActualRPM.Data_Collection_Rate	20	
	Leak Sensors		
	ColumnComp.LEDBoard_LeakDiff.Data_Collection_Rate	20	
	ColumnComp.LEDBoard_A13.Data_Collection_Rate	20	
	ColumnComp.LEDBoard_A14.Data_Collection_Rate	20	
	ColumnComp.Oven_Gas_MuteTimeRemain.Data_Collection_Rate	20	
	=========================================================================================		
	The temperature the oven is set before the temperature of 50°C is set		
	should be the same for the three set points.		
	=========================================================================================		
	Start Temperature		
	=========================================================================================		
	ColumnComp.CC.Temperature.Nominal	45.0	
-29.000	Wait	CC.TempReady	
-22.000	ColumnComp.CC.Temperature.Nominal	50.0	
-7.000	ColumnComp.CC.Temperature.Nominal	45.0	
0.000	ColumnComp.CC.Temperature.Nominal	50.0	
0.000	StartRun		
	ColumnComp.CC_Temp.AcqOn		
	ColumnComp.CC_U_Temp_Actual.AcqOn		
	ColumnComp.CC_L_Temp_Actual.AcqOn		
	ColumnComp.CC_UCTL_TempRear_Actual.AcqOn		
	ColumnComp.PWM_CCU_A.AcqOn		
	ColumnComp.PWM_CCU_B.AcqOn		
	ColumnComp.PWM_CCL_A.AcqOn		
	ColumnComp.PWM_CCL_B.AcqOn		
	ColumnComp.Fan_Rear_ActualRPM.AcqOn		
	External measured temperatures		
	Thermometer1.ExtTemp_UpperCC.AcqOn		
	Thermometer1.ExtTemp_LowerCC.AcqOn		
	Thermometer.Environment_Temperature.AcqOn		
	Leak Sensor Evaluation		
	ColumnComp.LEDBoard_LeakDiff.AcqOn		
	ColumnComp.LEDBoard_A13.AcqOn		
	ColumnComp.LEDBoard_A14.AcqOn		
	ColumnComp.Oven_Gas_MuteTimeRemain.AcqOn		
0.000	Run	Duration = 61.000 [min]	
	Log	Variables.GenericBool0	
15.000	ColumnComp.CC.Temperature.Nominal	45.0	
22.000	ColumnComp.CC.Temperature.Nominal	50.0	
37.000	ColumnComp.CC.Temperature.Nominal	45.0	
44.000	ColumnComp.CC.Temperature.Nominal	50.0	
	Liquid Leak Sensor is switched on and calibrated afterwards		
59.100	ColumnComp.LiquidLeakSensor	On	
61.000	ColumnComp.LiquidLeakSensorCalibrate		
62.000	StopRun		
	ColumnComp.CC_Temp.AcqOff		
	ColumnComp.CC_U_Temp_Actual.AcqOff		
	ColumnComp.CC_L_Temp_Actual.AcqOff		
	ColumnComp.CC_UCTL_TempRear_Actual.AcqOff		
	ColumnComp.PWM_CCU_A.AcqOff		
	ColumnComp.PWM_CCU_B.AcqOff		
	ColumnComp.PWM_CCL_A.AcqOff		
	ColumnComp.PWM_CCL_B.AcqOff		
	ColumnComp.Fan_Rear_ActualRPM.AcqOff		
	External measured temperatures		
	Thermometer1.ExtTemp_UpperCC.AcqOff		
	Thermometer1.ExtTemp_LowerCC.AcqOff		
	Thermometer.Environment_Temperature.AcqOff		
	Leak Sensor Evaluation		
	ColumnComp.LEDBoard_LeakDiff.AcqOff		
	ColumnComp.LEDBoard_A13.AcqOff		
	ColumnComp.LEDBoard_A14.AcqOff		
	ColumnComp.Oven_Gas_MuteTimeRemain.AcqOff		
	End		
```

<a id="m-tcc-precision-fan"></a>
## M-TCC-PRECISION-FAN: TEMPERATURE_PRECISION_AND_FAN

Applicable device evidence: **VC / VH**  
Source sequence(s): `VC:3000004, VH:6000001`  
Source SHA-256: `5c8a1bd77a2983106000199a6d0c98245f631672379c5fd812e3bc71727c5570`  
Decoded flow rows: `135`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	=========================================================================================		
	IM to measure the temperature precision of the Vanquish VH-C10-A and VC-C10-A		
	=========================================================================================		
	HPLC-System:		
	-----------		
	VH-C10-A or VC-C10-A		
-30.000	Equilibration	Duration = 30.000 [min]	
	Different total pages counts are used for VH-C10-A and VC-C10-A (no PCC). This is set here		
If		ColumnComp.ModelNo="VH-C10-A"	
	    Variables.GenericLong9	12	
	    Delay	1	[Val_FOQ_CM7_ekugelma_07-Jul-2020]: OK
	    Log	GenericLong9	
Else If		ColumnComp.ModelNo="VC-C10-A"	
	    Variables.GenericLong9	10	
	    Delay	1	[Val_FOQ_CM7_ekugelma_07-Jul-2020]: OK
	    Log	GenericLong9	
Else			
	    Message	Column compartment model unknown, please reinspect in production!	
	    System.AbortQueue		
End If			
	Determine IM for next injection		
If		ColumnComp.ModelNo="VH-C10-A"	
	    Variables.GenericBool0	1	Identificator for IRC insertion of correct temperature stability injection.
Else If		ColumnComp.ModelNo="VC-C10-A"	
	    Variables.GenericBool0	0	Identificator for IRC insertion of correct temperature stability injection.
Else			
	    Message	Invalid ModelNo! Please reinspect in production!	
	    System.AbortQueue		
End If			
	=========================================================================================		
	Parameters valid for the whole test.		
	=========================================================================================		
	If the difference between nominal and actual temperature is larger than		
	ReadyTempDelta, the oven is not ready.		
	ColumnComp.CC.ReadyTempDelta	0.1 [°C]	
	The Ready property will become Ready only if the difference between the		
	actual and the nominal temperature will not exceed the ReadyTempDelta for		
	the  time interval specified by EquilibrationTime.		
	ColumnComp.CC.EquilibrationTime	0.5 [min]	
	The VTCC adjusts the temperature only, if TempCtrl is set to ON.		
	ColumnComp.CC.TempCtrl	On	
	Adjusts FanSpeed and switches operating mode		
	ColumnComp.CC.Mode	StillAir	
	Liquid Leak Sensor remains switched off in order to avoid false alarms after great temperature changes. It is switched on during this IM and calibrated afterwards		
	=========================================================================================		
	ColumnComp.LiquidLeakSensor	Off	
	=========================================================================================		
	Settings for the all channels offered for the column compartment by the driver.		
	Also debug channels are aqcuired.		
	=========================================================================================		
	Column commpartment		
	ColumnComp.CC_U_Temp_Actual.Data_Collection_Rate	20	
	ColumnComp.CC_L_Temp_Actual.Data_Collection_Rate	20	
	ColumnComp.CC_UCTL_TempRear_Actual.Data_Collection_Rate	20	
	ColumnComp.PWM_CCU_A.Data_Collection_Rate	20	
	ColumnComp.PWM_CCU_B.Data_Collection_Rate	20	
	ColumnComp.PWM_CCL_A.Data_Collection_Rate	20	
	ColumnComp.PWM_CCL_B.Data_Collection_Rate	20	
	ColumnComp.Fan_Rear_ActualRPM.Data_Collection_Rate	20	
	Leak Sensors		
	ColumnComp.LEDBoard_LeakDiff.Data_Collection_Rate	20	
	ColumnComp.LEDBoard_A13.Data_Collection_Rate	20	
	ColumnComp.LEDBoard_A14.Data_Collection_Rate	20	
	ColumnComp.Oven_Gas_MuteTimeRemain.Data_Collection_Rate	20	
	=========================================================================================		
	The temperature the oven is set before the temperature of 50°C is set		
	should be the same for the three set points.		
	=========================================================================================		
	Start Temperature		
	=========================================================================================		
	ColumnComp.CC.Temperature.Nominal	45.0	
-29.000	Wait	CC.TempReady	
-22.000	ColumnComp.CC.Temperature.Nominal	50.0	
-7.000	ColumnComp.CC.Temperature.Nominal	45.0	
0.000	ColumnComp.CC.Temperature.Nominal	50.0	
0.000	StartRun		
	ColumnComp.CC_Temp.AcqOn		
	ColumnComp.CC_U_Temp_Actual.AcqOn		
	ColumnComp.CC_L_Temp_Actual.AcqOn		
	ColumnComp.CC_UCTL_TempRear_Actual.AcqOn		
	ColumnComp.PWM_CCU_A.AcqOn		
	ColumnComp.PWM_CCU_B.AcqOn		
	ColumnComp.PWM_CCL_A.AcqOn		
	ColumnComp.PWM_CCL_B.AcqOn		
	ColumnComp.Fan_Rear_ActualRPM.AcqOn		
	External measured temperatures		
	Thermometer1.ExtTemp_UpperCC.AcqOn		
	Thermometer1.ExtTemp_LowerCC.AcqOn		
	Thermometer.Environment_Temperature.AcqOn		
	Leak Sensor Evaluation		
	ColumnComp.LEDBoard_LeakDiff.AcqOn		
	ColumnComp.LEDBoard_A13.AcqOn		
	ColumnComp.LEDBoard_A14.AcqOn		
	ColumnComp.Oven_Gas_MuteTimeRemain.AcqOn		
0.000	Run	Duration = 76.000 [min]	
	Log	Variables.GenericBool0	
15.000	ColumnComp.CC.Temperature.Nominal	45.0	
22.000	ColumnComp.CC.Temperature.Nominal	50.0	
37.000	ColumnComp.CC.Temperature.Nominal	45.0	
44.000	ColumnComp.CC.Temperature.Nominal	50.0	
	Liquid Leak Sensor is switched on and calibrated afterwards		
59.100	ColumnComp.LiquidLeakSensor	On	
61.000	ColumnComp.LiquidLeakSensorCalibrate		
	=========================================================================================		
	Test of funtionality of fan for switching between two operating modes		
	=========================================================================================		
64.100	ColumnComp.CC.ReadyTempDelta	0.1 [°C]	
	ColumnComp.CC.EquilibrationTime	0.0 [min]	
	ColumnComp.CC.Mode	ForcedAir	
	Log	CC.TempReady	
64.600	Log	CC.TempReady	
75.000	Log	CC.TempReady	
	ColumnComp.CC.Mode	StillAir	
75.500	Log	CC.TempReady	
76.000	StopRun		
	ColumnComp.CC_Temp.AcqOff		
	ColumnComp.CC_U_Temp_Actual.AcqOff		
	ColumnComp.CC_L_Temp_Actual.AcqOff		
	ColumnComp.CC_UCTL_TempRear_Actual.AcqOff		
	ColumnComp.PWM_CCU_A.AcqOff		
	ColumnComp.PWM_CCU_B.AcqOff		
	ColumnComp.PWM_CCL_A.AcqOff		
	ColumnComp.PWM_CCL_B.AcqOff		
	ColumnComp.Fan_Rear_ActualRPM.AcqOff		
	External measured temperatures		
	Thermometer1.ExtTemp_UpperCC.AcqOff		
	Thermometer1.ExtTemp_LowerCC.AcqOff		
	Thermometer.Environment_Temperature.AcqOff		
	Leak Sensor Evaluation		
	ColumnComp.LEDBoard_LeakDiff.AcqOff		
	ColumnComp.LEDBoard_A13.AcqOff		
	ColumnComp.LEDBoard_A14.AcqOff		
	ColumnComp.Oven_Gas_MuteTimeRemain.AcqOff		
	End		
```

<a id="m-tcc-stability-va"></a>
## M-TCC-STABILITY-VA: TEMPERATURE_STABILITY_70_C

Applicable device evidence: **VA**  
Source sequence(s): `VA:0000003`  
Source SHA-256: `cb7c2cbbb4b97f8e383d63e115d975151089036527c645f9d87931c2aea4950e`  
Decoded flow rows: `97`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	=========================================================================================		
	IM to measure the temperature stability of the Vanquish VC-C10-A and VA-C10-A		
	=========================================================================================		
	HPLC-System:		
	-----------		
	VC-C10-A or VA-C10-A		
-0.700	Equilibration	Duration = 0.700 [min]	
	Different total pages counts are used for VH-C10-A, VC-C10-A (no PCC) and VA-C10-A. This is set here		
If		ColumnComp.ModelNo="VH-C10-A"	
	    Variables.GenericLong9	12	
	    Delay	1	[Val_FOQ_CM7_ekugelma_07-Jul-2020]: OK
	    Log	GenericLong9	
Else If		ColumnComp.ModelNo="VC-C10-A" OR ColumnComp.ModelNo="VA-C10-A"	
	    Variables.GenericLong9	10	
	    Delay	1	[Val_FOQ_CM7_ekugelma_07-Jul-2020]: OK
	    Log	GenericLong9	
Else			
	    Message	Column compartment model unknown, please reinspect in production!	
	    System.AbortQueue		
End If			
	=========================================================================================		
	Parameters valid for the whole test.		
	=========================================================================================		
	If the difference between the setpoint temperture and the actual temperature exeeds ReadyTempDelta, the VTCC is not ready.		
	ColumnComp.CC.ReadyTempDelta	0.05 [°C]	
	The Ready property will become Ready only if the difference between the setpoint temperature and the nominal temperature will not exceed the ReadyTempDelta for the time interval specified by EquilibrationTime.		
	ColumnComp.CC.EquilibrationTime	0.5 [min]	
	The VTCC controls the temperature only, if TempCtrl is set to ON.		
	ColumnComp.CC.TempCtrl	On	
	adjusts FanSpeed and switches operating mode		
	ColumnComp.CC.Mode	StillAir	
	=========================================================================================		
	Settings for the all channels offered for the column compartment by the driver.		
	Also debug channels are aqcuired.		
	=========================================================================================		
	Column commpartment		
	ColumnComp.CC_U_Temp_Actual.Data_Collection_Rate	20	
	ColumnComp.CC_L_Temp_Actual.Data_Collection_Rate	20	
	ColumnComp.CC_UCTL_TempRear_Actual.Data_Collection_Rate	20	
	ColumnComp.PWM_CCU_A.Data_Collection_Rate	20	
	ColumnComp.PWM_CCU_B.Data_Collection_Rate	20	
	ColumnComp.PWM_CCL_A.Data_Collection_Rate	20	
	ColumnComp.PWM_CCL_B.Data_Collection_Rate	20	
	ColumnComp.Fan_Rear_ActualRPM.Data_Collection_Rate	20	
	Leak Sensors		
	ColumnComp.LEDBoard_LeakDiff.Data_Collection_Rate	20	
	ColumnComp.LEDBoard_A13.Data_Collection_Rate	20	
	ColumnComp.LEDBoard_A14.Data_Collection_Rate	20	
	ColumnComp.Oven_Gas_MuteTimeRemain.Data_Collection_Rate	20	
	=========================================================================================		
	Start Temperature		
	=========================================================================================		
	ColumnComp.CC.Temperature.Nominal	70.0	
0.000	InjectPreparation		
	Wait	CC.TempReady	
0.000	StartRun		
	ColumnComp.CC_Temp.AcqOn		
	ColumnComp.CC_U_Temp_Actual.AcqOn		
	ColumnComp.CC_L_Temp_Actual.AcqOn		
	ColumnComp.CC_UCTL_TempRear_Actual.AcqOn		
	ColumnComp.PWM_CCU_A.AcqOn		
	ColumnComp.PWM_CCU_B.AcqOn		
	ColumnComp.PWM_CCL_A.AcqOn		
	ColumnComp.PWM_CCL_B.AcqOn		
	ColumnComp.Fan_Rear_ActualRPM.AcqOn		
	External measured temperatures		
	Thermometer1.ExtTemp_UpperCC.AcqOn		
	Thermometer1.ExtTemp_LowerCC.AcqOn		
	Thermometer.Environment_Temperature.AcqOn		
	Leak Sensor Evaluation		
	ColumnComp.LEDBoard_LeakDiff.AcqOn		
	ColumnComp.LEDBoard_A13.AcqOn		
	ColumnComp.LEDBoard_A14.AcqOn		
	ColumnComp.Oven_Gas_MuteTimeRemain.AcqOn		
0.000	Run	Duration = 60.000 [min]	
60.000	StopRun		
	ColumnComp.CC_Temp.AcqOff		
	ColumnComp.CC_U_Temp_Actual.AcqOff		
	ColumnComp.CC_L_Temp_Actual.AcqOff		
	ColumnComp.CC_UCTL_TempRear_Actual.AcqOff		
	ColumnComp.PWM_CCU_A.AcqOff		
	ColumnComp.PWM_CCU_B.AcqOff		
	ColumnComp.PWM_CCL_A.AcqOff		
	ColumnComp.PWM_CCL_B.AcqOff		
	ColumnComp.Fan_Rear_ActualRPM.AcqOff		
60.000	PostRun		
	External measured temperatures		
	Thermometer1.ExtTemp_UpperCC.AcqOff		
	Thermometer1.ExtTemp_LowerCC.AcqOff		
	Thermometer.Environment_Temperature.AcqOff		
	Leak Sensor Evaluation		
	ColumnComp.LEDBoard_LeakDiff.AcqOff		
	ColumnComp.LEDBoard_A13.AcqOff		
	ColumnComp.LEDBoard_A14.AcqOff		
	ColumnComp.Oven_Gas_MuteTimeRemain.AcqOff		
	End		
```

<a id="m-tcc-stability-vcvh"></a>
## M-TCC-STABILITY-VCVH: TEMPERATURE_STABILITY_70_C

Applicable device evidence: **VC / VH**  
Source sequence(s): `VC:3000004, VH:6000001`  
Source SHA-256: `2b9d3793ed654ba32167051f0cbabf1ddb5ec42c71857e9a472199f68e46bc2f`  
Decoded flow rows: `97`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	=========================================================================================		
	IM to measure the temperature stability of the Vanquish VC-C10-A		
	=========================================================================================		
	HPLC-System:		
	-----------		
	VC-C10-A		
-0.700	Equilibration	Duration = 0.700 [min]	
	Different total pages counts are used for VH-C10-A and VC-C10-A (no PCC). This is set here		
If		ColumnComp.ModelNo="VH-C10-A"	
	    Variables.GenericLong9	12	
	    Delay	1	[Val_FOQ_CM7_ekugelma_07-Jul-2020]: OK
	    Log	GenericLong9	
Else If		ColumnComp.ModelNo="VC-C10-A"	
	    Variables.GenericLong9	10	
	    Delay	1	[Val_FOQ_CM7_ekugelma_07-Jul-2020]: OK
	    Log	GenericLong9	
Else			
	    Message	Column compartment model unknown, please reinspect in production!	
	    System.AbortQueue		
End If			
	=========================================================================================		
	Parameters valid for the whole test.		
	=========================================================================================		
	If the difference between the setpoint temperture and the actual temperature exeeds ReadyTempDelta, the VTCC is not ready.		
	ColumnComp.CC.ReadyTempDelta	0.05 [°C]	
	The Ready property will become Ready only if the difference between the setpoint temperature and the nominal temperature will not exceed the ReadyTempDelta for the time interval specified by EquilibrationTime.		
	ColumnComp.CC.EquilibrationTime	0.5 [min]	
	The VTCC controls the temperature only, if TempCtrl is set to ON.		
	ColumnComp.CC.TempCtrl	On	
	adjusts FanSpeed and switches operating mode		
	ColumnComp.CC.Mode	StillAir	
	=========================================================================================		
	Settings for the all channels offered for the column compartment by the driver.		
	Also debug channels are aqcuired.		
	=========================================================================================		
	Column commpartment		
	ColumnComp.CC_U_Temp_Actual.Data_Collection_Rate	20	
	ColumnComp.CC_L_Temp_Actual.Data_Collection_Rate	20	
	ColumnComp.CC_UCTL_TempRear_Actual.Data_Collection_Rate	20	
	ColumnComp.PWM_CCU_A.Data_Collection_Rate	20	
	ColumnComp.PWM_CCU_B.Data_Collection_Rate	20	
	ColumnComp.PWM_CCL_A.Data_Collection_Rate	20	
	ColumnComp.PWM_CCL_B.Data_Collection_Rate	20	
	ColumnComp.Fan_Rear_ActualRPM.Data_Collection_Rate	20	
	Leak Sensors		
	ColumnComp.LEDBoard_LeakDiff.Data_Collection_Rate	20	
	ColumnComp.LEDBoard_A13.Data_Collection_Rate	20	
	ColumnComp.LEDBoard_A14.Data_Collection_Rate	20	
	ColumnComp.Oven_Gas_MuteTimeRemain.Data_Collection_Rate	20	
	=========================================================================================		
	Start Temperature		
	=========================================================================================		
	ColumnComp.CC.Temperature.Nominal	70.0	
0.000	InjectPreparation		
	Wait	CC.TempReady	
0.000	StartRun		
	ColumnComp.CC_Temp.AcqOn		
	ColumnComp.CC_U_Temp_Actual.AcqOn		
	ColumnComp.CC_L_Temp_Actual.AcqOn		
	ColumnComp.CC_UCTL_TempRear_Actual.AcqOn		
	ColumnComp.PWM_CCU_A.AcqOn		
	ColumnComp.PWM_CCU_B.AcqOn		
	ColumnComp.PWM_CCL_A.AcqOn		
	ColumnComp.PWM_CCL_B.AcqOn		
	ColumnComp.Fan_Rear_ActualRPM.AcqOn		
	External measured temperatures		
	Thermometer1.ExtTemp_UpperCC.AcqOn		
	Thermometer1.ExtTemp_LowerCC.AcqOn		
	Thermometer.Environment_Temperature.AcqOn		
	Leak Sensor Evaluation		
	ColumnComp.LEDBoard_LeakDiff.AcqOn		
	ColumnComp.LEDBoard_A13.AcqOn		
	ColumnComp.LEDBoard_A14.AcqOn		
	ColumnComp.Oven_Gas_MuteTimeRemain.AcqOn		
0.000	Run	Duration = 60.000 [min]	
60.000	StopRun		
	ColumnComp.CC_Temp.AcqOff		
	ColumnComp.CC_U_Temp_Actual.AcqOff		
	ColumnComp.CC_L_Temp_Actual.AcqOff		
	ColumnComp.CC_UCTL_TempRear_Actual.AcqOff		
	ColumnComp.PWM_CCU_A.AcqOff		
	ColumnComp.PWM_CCU_B.AcqOff		
	ColumnComp.PWM_CCL_A.AcqOff		
	ColumnComp.PWM_CCL_B.AcqOff		
	ColumnComp.Fan_Rear_ActualRPM.AcqOff		
60.000	PostRun		
	External measured temperatures		
	Thermometer1.ExtTemp_UpperCC.AcqOff		
	Thermometer1.ExtTemp_LowerCC.AcqOff		
	Thermometer.Environment_Temperature.AcqOff		
	Leak Sensor Evaluation		
	ColumnComp.LEDBoard_LeakDiff.AcqOff		
	ColumnComp.LEDBoard_A13.AcqOff		
	ColumnComp.LEDBoard_A14.AcqOff		
	ColumnComp.Oven_Gas_MuteTimeRemain.AcqOff		
	End		
```

<a id="m-tcc-stability-pcc-va"></a>
## M-TCC-STABILITY-PCC-VA: TEMPERATURE_STABILITY_AND_PCC_70_H

Applicable device evidence: **VA**  
Source sequence(s): `VA:0000003`  
Source SHA-256: `c463487c272abb6d0e16df66164351068025b8d2292011c740ca1fe34571c102`  
Decoded flow rows: `139`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	=========================================================================================		
	IM to measure the temperature stability of the Vanquish VH-C10-A, VC-C10-A and VA-C10-A		
	=========================================================================================		
	HPLC-System:		
	-----------		
	VH-C10-A, VC-C10-A or VA-C10-A		
-0.700	Equilibration	Duration = 0.700 [min]	
	Different total pages counts are used for VH-C10-A, VC-C10-A (no PCC) and VA-C10-A. This is set here		
If		ColumnComp.ModelNo="VH-C10-A"	
	    Variables.GenericLong9	12	
	    Delay	1	[Val_FOQ_CM7_ekugelma_07-Jul-2020]: OK
	    Log	GenericLong9	
Else If		ColumnComp.ModelNo="VC-C10-A" OR ColumnComp.ModelNo="VA-C10-A"	
	    Variables.GenericLong9	10	
	    Delay	1	[Val_FOQ_CM7_ekugelma_07-Jul-2020]: OK
	    Log	GenericLong9	
Else			
	    Message	Column compartment model unknown, please reinspect in production!	
	    System.AbortQueue		
End If			
	=========================================================================================		
	Parameters valid for the whole test.		
	=========================================================================================		
	If the difference between the setpoint temperture and the actual temperature exeeds ReadyTempDelta, the VTCC is not ready.		
	ColumnComp.CC.ReadyTempDelta	0.05 [°C]	
	The Ready property will become Ready only if the difference between the setpoint temperature and the nominal temperature will not exceed the ReadyTempDelta for the time interval specified by EquilibrationTime.		
	ColumnComp.CC.EquilibrationTime	0.5 [min]	
	The VTCC controls the temperature only, if TempCtrl is set to ON.		
	ColumnComp.CC.TempCtrl	On	
	ColumnComp.PCC.TempCtrl	On	
	adjusts FanSpeed and switches operating mode		
	ColumnComp.CC.Mode	StillAir	
	Settings for Post Column Cooler Trigger Commands		
	Variables.GenericBool1	0	
	Variables.GenericBool2	0	
	Initialize Retention Times used during IM		
	RetTimes.RetTime1	0	
	RetTimes.RetTime2	0	
	RetTimes.RetTime3	0	
	RetTimes.RetTime4	0	
	=========================================================================================		
	Post Column Cooler settings.		
	=========================================================================================		
	ColumnComp.PCC.Temperature.Nominal	40.00	
	=========================================================================================		
	Settings for the all channels offered for the column compartment by the driver.		
	Also debug channels are aqcuired.		
	=========================================================================================		
	Column commpartment		
	ColumnComp.CC_U_Temp_Actual.Data_Collection_Rate	20	
	ColumnComp.CC_L_Temp_Actual.Data_Collection_Rate	20	
	ColumnComp.CC_UCTL_TempRear_Actual.Data_Collection_Rate	20	
	ColumnComp.PWM_CCU_A.Data_Collection_Rate	20	
	ColumnComp.PWM_CCU_B.Data_Collection_Rate	20	
	ColumnComp.PWM_CCL_A.Data_Collection_Rate	20	
	ColumnComp.PWM_CCL_B.Data_Collection_Rate	20	
	ColumnComp.Fan_Rear_ActualRPM.Data_Collection_Rate	20	
	Post column cooler		
	ColumnComp.PWM_PCC_A.Data_Collection_Rate	20	
	ColumnComp.PWM_PCC_B.Data_Collection_Rate	20	
	Leak Sensors		
	ColumnComp.LEDBoard_LeakDiff.Data_Collection_Rate	20	
	ColumnComp.LEDBoard_A13.Data_Collection_Rate	20	
	ColumnComp.LEDBoard_A14.Data_Collection_Rate	20	
	ColumnComp.Oven_Gas_MuteTimeRemain.Data_Collection_Rate	20	
	=========================================================================================		
	Start Temperature		
	=========================================================================================		
	ColumnComp.CC.Temperature.Nominal	70.0	
0.000	InjectPreparation		
	Wait	CC.TempReady AND PCC.TempReady	
0.000	StartRun		
	ColumnComp.CC_Temp.AcqOn		
	ColumnComp.CC_U_Temp_Actual.AcqOn		
	ColumnComp.CC_L_Temp_Actual.AcqOn		
	ColumnComp.CC_UCTL_TempRear_Actual.AcqOn		
	ColumnComp.PWM_CCU_A.AcqOn		
	ColumnComp.PWM_CCU_B.AcqOn		
	ColumnComp.PWM_CCL_A.AcqOn		
	ColumnComp.PWM_CCL_B.AcqOn		
	ColumnComp.Fan_Rear_ActualRPM.AcqOn		
	Post column cooler		
	ColumnComp.PCC_Temp.AcqOn		
	ColumnComp.PWM_PCC_A.AcqOn		
	ColumnComp.PWM_PCC_B.AcqOn		
	External measured temperatures		
	Thermometer1.ExtTemp_UpperCC.AcqOn		
	Thermometer1.ExtTemp_LowerCC.AcqOn		
	Thermometer.Environment_Temperature.AcqOn		
	Leak Sensor Evaluation		
	ColumnComp.LEDBoard_LeakDiff.AcqOn		
	ColumnComp.LEDBoard_A13.AcqOn		
	ColumnComp.LEDBoard_A14.AcqOn		
	ColumnComp.Oven_Gas_MuteTimeRemain.AcqOn		
0.000	Run	Duration = 25.000 [min]	
	Trigger for Heat Time measuring 50°C to 60°C (Post Column Cooler Temperature)		
3.500			
Trigger		"T60UP",	
	    Condition	PCC.Temperature.Value>=60.0	
	    Limit	1	
	    Hysteresis	5.0 [%]	
	    AllowImmediateExecution	No	
	RetTimes.RetTime2	System.Retention	
	Variables.GenericBool1	1	activation of Trigger T50Down
End Trigger			
5.000	ColumnComp.PCC.Temperature.Nominal	80.0 [°C]	
	Trigger for Cool Down Time measuring 50°C to 40°C (Post Column Cooler Temperature)		
14.500			
Trigger		"T50Down",	
	    Condition	PCC.Temperature.Value<=50.0 AND Variables.GenericBool1	
	    Limit	1	
	    Hysteresis	5.0 [%]	
	    AllowImmediateExecution	No	
	RetTimes.RetTime3	System.Retention	
	Log	PCC.Temperature.Value	
	Variables.GenericBool2	1	activation of Trigger T40Down
End Trigger			
Trigger		"T40Down",	
	    Condition	PCC.Temperature.Value<=40.0 AND Variables.GenericBool2	
	    Limit	1	
	    Hysteresis	5.0 [%]	
	    AllowImmediateExecution	No	
	RetTimes.RetTime4	System.Retention	
	Log	PCC.Temperature.Value	
End Trigger			
15.000	ColumnComp.PCC.Temperature.Nominal	40.0 [°C]	
25.000	ColumnComp.PCC.TempCtrl	Off	
60.000	StopRun		
	ColumnComp.CC_Temp.AcqOff		
	ColumnComp.CC_U_Temp_Actual.AcqOff		
	ColumnComp.CC_L_Temp_Actual.AcqOff		
	ColumnComp.CC_UCTL_TempRear_Actual.AcqOff		
	ColumnComp.PWM_CCU_A.AcqOff		
	ColumnComp.PWM_CCU_B.AcqOff		
	ColumnComp.PWM_CCL_A.AcqOff		
	ColumnComp.PWM_CCL_B.AcqOff		
	ColumnComp.Fan_Rear_ActualRPM.AcqOff		
60.000	PostRun		
	Post column cooler		
	ColumnComp.PCC_Temp.AcqOff		
	ColumnComp.PWM_PCC_A.AcqOff		
	ColumnComp.PWM_PCC_B.AcqOff		
	External measured temperatures		
	Thermometer1.ExtTemp_UpperCC.AcqOff		
	Thermometer1.ExtTemp_LowerCC.AcqOff		
	Thermometer.Environment_Temperature.AcqOff		
	Leak Sensor Evaluation		
	ColumnComp.LEDBoard_LeakDiff.AcqOff		
	ColumnComp.LEDBoard_A13.AcqOff		
	ColumnComp.LEDBoard_A14.AcqOff		
	ColumnComp.Oven_Gas_MuteTimeRemain.AcqOff		
	End		
```

<a id="m-tcc-stability-pcc-vcvh"></a>
## M-TCC-STABILITY-PCC-VCVH: TEMPERATURE_STABILITY_AND_PCC_70_H

Applicable device evidence: **VC / VH**  
Source sequence(s): `VC:3000004, VH:6000001`  
Source SHA-256: `c996f3cd0b202fe7b1b5c58e2ce2f6ab3e2182f8ae5a76c8c6ec8365c50693fd`  
Decoded flow rows: `139`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	=========================================================================================		
	IM to measure the temperature stability of the Vanquish VH-C10-A		
	=========================================================================================		
	HPLC-System:		
	-----------		
	VH-C10-A		
-0.700	Equilibration	Duration = 0.700 [min]	
	Different total pages counts are used for VH-C10-A and VC-C10-A (no PCC). This is set here		
If		ColumnComp.ModelNo="VH-C10-A"	
	    Variables.GenericLong9	12	
	    Delay	1	[Val_FOQ_CM7_ekugelma_07-Jul-2020]: OK
	    Log	GenericLong9	
Else If		ColumnComp.ModelNo="VC-C10-A"	
	    Variables.GenericLong9	10	
	    Delay	1	[Val_FOQ_CM7_ekugelma_07-Jul-2020]: OK
	    Log	GenericLong9	
Else			
	    Message	Column compartment model unknown, please reinspect in production!	
	    System.AbortQueue		
End If			
	=========================================================================================		
	Parameters valid for the whole test.		
	=========================================================================================		
	If the difference between the setpoint temperture and the actual temperature exeeds ReadyTempDelta, the VTCC is not ready.		
	ColumnComp.CC.ReadyTempDelta	0.05 [°C]	
	The Ready property will become Ready only if the difference between the setpoint temperature and the nominal temperature will not exceed the ReadyTempDelta for the time interval specified by EquilibrationTime.		
	ColumnComp.CC.EquilibrationTime	0.5 [min]	
	The VTCC controls the temperature only, if TempCtrl is set to ON.		
	ColumnComp.CC.TempCtrl	On	
	ColumnComp.PCC.TempCtrl	On	
	adjusts FanSpeed and switches operating mode		
	ColumnComp.CC.Mode	StillAir	
	Settings for Post Column Cooler Trigger Commands		
	Variables.GenericBool1	0	
	Variables.GenericBool2	0	
	Initialize Retention Times used during IM		
	RetTimes.RetTime1	0	
	RetTimes.RetTime2	0	
	RetTimes.RetTime3	0	
	RetTimes.RetTime4	0	
	=========================================================================================		
	Post Column Cooler settings.		
	=========================================================================================		
	ColumnComp.PCC.Temperature.Nominal	40.00	
	=========================================================================================		
	Settings for the all channels offered for the column compartment by the driver.		
	Also debug channels are aqcuired.		
	=========================================================================================		
	Column commpartment		
	ColumnComp.CC_U_Temp_Actual.Data_Collection_Rate	20	
	ColumnComp.CC_L_Temp_Actual.Data_Collection_Rate	20	
	ColumnComp.CC_UCTL_TempRear_Actual.Data_Collection_Rate	20	
	ColumnComp.PWM_CCU_A.Data_Collection_Rate	20	
	ColumnComp.PWM_CCU_B.Data_Collection_Rate	20	
	ColumnComp.PWM_CCL_A.Data_Collection_Rate	20	
	ColumnComp.PWM_CCL_B.Data_Collection_Rate	20	
	ColumnComp.Fan_Rear_ActualRPM.Data_Collection_Rate	20	
	Post column cooler		
	ColumnComp.PWM_PCC_A.Data_Collection_Rate	20	
	ColumnComp.PWM_PCC_B.Data_Collection_Rate	20	
	Leak Sensors		
	ColumnComp.LEDBoard_LeakDiff.Data_Collection_Rate	20	
	ColumnComp.LEDBoard_A13.Data_Collection_Rate	20	
	ColumnComp.LEDBoard_A14.Data_Collection_Rate	20	
	ColumnComp.Oven_Gas_MuteTimeRemain.Data_Collection_Rate	20	
	=========================================================================================		
	Start Temperature		
	=========================================================================================		
	ColumnComp.CC.Temperature.Nominal	70.0	
0.000	InjectPreparation		
	Wait	CC.TempReady AND PCC.TempReady	
0.000	StartRun		
	ColumnComp.CC_Temp.AcqOn		
	ColumnComp.CC_U_Temp_Actual.AcqOn		
	ColumnComp.CC_L_Temp_Actual.AcqOn		
	ColumnComp.CC_UCTL_TempRear_Actual.AcqOn		
	ColumnComp.PWM_CCU_A.AcqOn		
	ColumnComp.PWM_CCU_B.AcqOn		
	ColumnComp.PWM_CCL_A.AcqOn		
	ColumnComp.PWM_CCL_B.AcqOn		
	ColumnComp.Fan_Rear_ActualRPM.AcqOn		
	Post column cooler		
	ColumnComp.PCC_Temp.AcqOn		
	ColumnComp.PWM_PCC_A.AcqOn		
	ColumnComp.PWM_PCC_B.AcqOn		
	External measured temperatures		
	Thermometer1.ExtTemp_UpperCC.AcqOn		
	Thermometer1.ExtTemp_LowerCC.AcqOn		
	Thermometer.Environment_Temperature.AcqOn		
	Leak Sensor Evaluation		
	ColumnComp.LEDBoard_LeakDiff.AcqOn		
	ColumnComp.LEDBoard_A13.AcqOn		
	ColumnComp.LEDBoard_A14.AcqOn		
	ColumnComp.Oven_Gas_MuteTimeRemain.AcqOn		
0.000	Run	Duration = 25.000 [min]	
	Trigger for Heat Time measuring 50°C to 60°C (Post Column Cooler Temperature)		
3.500			
Trigger		"T60UP",	
	    Condition	PCC.Temperature.Value>=60.0	
	    Limit	1	
	    Hysteresis	5.0 [%]	
	    AllowImmediateExecution	No	
	RetTimes.RetTime2	System.Retention	
	Variables.GenericBool1	1	activation of Trigger T50Down
End Trigger			
5.000	ColumnComp.PCC.Temperature.Nominal	80.0 [°C]	
	Trigger for Cool Down Time measuring 50°C to 40°C (Post Column Cooler Temperature)		
14.500			
Trigger		"T50Down",	
	    Condition	PCC.Temperature.Value<=50.0 AND Variables.GenericBool1	
	    Limit	1	
	    Hysteresis	5.0 [%]	
	    AllowImmediateExecution	No	
	RetTimes.RetTime3	System.Retention	
	Log	PCC.Temperature.Value	
	Variables.GenericBool2	1	activation of Trigger T40Down
End Trigger			
Trigger		"T40Down",	
	    Condition	PCC.Temperature.Value<=40.0 AND Variables.GenericBool2	
	    Limit	1	
	    Hysteresis	5.0 [%]	
	    AllowImmediateExecution	No	
	RetTimes.RetTime4	System.Retention	
	Log	PCC.Temperature.Value	
End Trigger			
15.000	ColumnComp.PCC.Temperature.Nominal	40.0 [°C]	
25.000	ColumnComp.PCC.TempCtrl	Off	
60.000	StopRun		
	ColumnComp.CC_Temp.AcqOff		
	ColumnComp.CC_U_Temp_Actual.AcqOff		
	ColumnComp.CC_L_Temp_Actual.AcqOff		
	ColumnComp.CC_UCTL_TempRear_Actual.AcqOff		
	ColumnComp.PWM_CCU_A.AcqOff		
	ColumnComp.PWM_CCU_B.AcqOff		
	ColumnComp.PWM_CCL_A.AcqOff		
	ColumnComp.PWM_CCL_B.AcqOff		
	ColumnComp.Fan_Rear_ActualRPM.AcqOff		
60.000	PostRun		
	Post column cooler		
	ColumnComp.PCC_Temp.AcqOff		
	ColumnComp.PWM_PCC_A.AcqOff		
	ColumnComp.PWM_PCC_B.AcqOff		
	External measured temperatures		
	Thermometer1.ExtTemp_UpperCC.AcqOff		
	Thermometer1.ExtTemp_LowerCC.AcqOff		
	Thermometer.Environment_Temperature.AcqOff		
	Leak Sensor Evaluation		
	ColumnComp.LEDBoard_LeakDiff.AcqOff		
	ColumnComp.LEDBoard_A13.AcqOff		
	ColumnComp.LEDBoard_A14.AcqOff		
	ColumnComp.Oven_Gas_MuteTimeRemain.AcqOff		
	End		
```

<a id="m-tcc-valves-va"></a>
## M-TCC-VALVES-VA: VALVES

Applicable device evidence: **VA**  
Source sequence(s): `VA:0000003`  
Source SHA-256: `33907b3d79606e98c88fad2f2c7665f89c6d17b17993d9cbde8734c84206957a`  
Decoded flow rows: `42`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	=========================================================================================		
	IM to measure the valve performance of the Vanquish TCC		
	=========================================================================================		
	HPLC-System:		
	-----------		
	VTCC		
-0.100	Equilibration	Duration = 0.080 [min]	
	=========================================================================================		
	Parameters valid for the whole test.		
	=========================================================================================		
	If the difference between nominal and actual temperature is larger than ReadyTempDelta, the VTCC is not ready.		
	ColumnComp.CC.ReadyTempDelta	1.0 [°C]	
	The Ready property will become Ready only if the difference between the setpoint temperature and the nominal temperature will not exceed the ReadyTempDelta for the time interval specified by EquilibrationTime.		
	ColumnComp.CC.EquilibrationTime	0.5	
	The VTCC adjusts the temperature only, if TempCtrl is set to ON for each single unit.		
	ColumnComp.CC.TempCtrl	On	
	Adjusts FanSpeed and switches operating mode		
	ColumnComp.CC.Mode	StillAir	
	ColumnComp.LowerValve.CurrentPosition	6_1	
	Delay	0.1	
-0.020	Log	LowerValve.Precision	
0.000	Run	Duration = 0.900 [min]	
	=========================================================================================		
	CM needs data from any channel to evaluate the audit trail in the report.		
	=========================================================================================		
	ColumnComp.CC_Temp.AcqOn		
0.050	ColumnComp.LowerValve.CurrentPosition	1_2	
	Delay	0.1	
0.100	Log	LowerValve.Precision	
0.120	ColumnComp.LowerValve.CurrentPosition	6_1	
	Delay	0.1	
0.200	Log	LowerValve.Precision	
	Message	By pressing 'OK', the device will be disconnected automatically in order to check the keypad functionality. Please click 'OK' and press each button for 'FAST COOL' and 'Upper/Lower Valve' once within 30 seconds! Check that the LEDs work as expected!	
0.210	ColumnComp.CC_Temp.AcqOff		
0.300	ColumnComp.Disconnect		
0.800	ColumnComp.Connect		
	Wait	ColumnComp.Connected = Connected	
0.900	ColumnComp.FastCoolActive	Off	
	Delay	1	
1.000	StopRun		
	End		
```

<a id="m-tcc-valves-vcvh"></a>
## M-TCC-VALVES-VCVH: VALVES

Applicable device evidence: **VC / VH**  
Source sequence(s): `VC:3000004, VH:6000001`  
Source SHA-256: `8deefe03c7e3bffe3a0df1e2d1d0eb512662fd20e4e6d275343e4ee31ef865e6`  
Decoded flow rows: `50`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	=========================================================================================		
	IM to measure the valve performance of the Vanquish TCC		
	=========================================================================================		
	HPLC-System:		
	-----------		
	VTCC		
-0.100	Equilibration	Duration = 0.080 [min]	
	=========================================================================================		
	Parameters valid for the whole test.		
	=========================================================================================		
	If the difference between nominal and actual temperature is larger than ReadyTempDelta, the VTCC is not ready.		
	ColumnComp.CC.ReadyTempDelta	1.0 [°C]	
	The Ready property will become Ready only if the difference between the setpoint temperature and the nominal temperature will not exceed the ReadyTempDelta for the time interval specified by EquilibrationTime.		
	ColumnComp.CC.EquilibrationTime	0.5	
	The VTCC adjusts the temperature only, if TempCtrl is set to ON for each single unit.		
	ColumnComp.CC.TempCtrl	On	
	Adjusts FanSpeed and switches operating mode		
	ColumnComp.CC.Mode	StillAir	
	ColumnComp.UpperValve.CurrentPosition	6_1	
	Delay	0.2	
	ColumnComp.LowerValve.CurrentPosition	6_1	
	Delay	0.1	
-0.020	Log	UpperValve.Precision	
	Log	LowerValve.Precision	
0.000	Run	Duration = 0.900 [min]	
	=========================================================================================		
	CM needs data from any channel to evaluate the audit trail in the report.		
	=========================================================================================		
	ColumnComp.CC_Temp.AcqOn		
0.050	ColumnComp.UpperValve.CurrentPosition	1_2	
	ColumnComp.LowerValve.CurrentPosition	1_2	
	Delay	0.1	
0.100	Log	UpperValve.Precision	
	Log	LowerValve.Precision	
0.120	ColumnComp.UpperValve.CurrentPosition	6_1	
	Delay	0.2	
	ColumnComp.LowerValve.CurrentPosition	6_1	
	Delay	0.1	
0.200	Log	UpperValve.Precision	
	Log	LowerValve.Precision	
	Message	By pressing 'OK', the device will be disconnected automatically in order to check the keypad functionality. Please click 'OK' and press each button for 'FAST COOL' and 'Upper/Lower Valve' once within 30 seconds! Check that the LEDs work as expected!	
0.210	ColumnComp.CC_Temp.AcqOff		
0.300	ColumnComp.Disconnect		
0.800	ColumnComp.Connect		
	Wait	ColumnComp.Connected = Connected	
0.900	ColumnComp.FastCoolActive	Off	
	Delay	1	
1.000	StopRun		
	End		
```
