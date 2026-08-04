# Online Original RID OQ Method Script Collection

Online_KB_Status: DECODED_FROM_OQ_CMBX  
Build_Date: 2026-07-28  
Source_CMBX: OQ 2026-07-28.cmbx  
Instrument_Method_Count: 6

This file contains the decoded executable method evidence from the RID OQ sequence template. Preserve command spelling, stage time, purge/autozero order, acquisition symmetry, and device macros. Interpretive summaries never override these rows.

## Self Index

| Stable ID | CM method | Rows | Hash | Section |
|---|---|---:|---|---|
| `M-RID-EQUILIBRATION-RI-AND-RF` | `EQUILIBRATION_RI_AND RF` | 64 | `ebd9d423a953` | [Open](#m-rid-equilibration-ri-and-rf) |
| `M-RID-RESTORE` | `RESTORE` | 15 | `014dab8776fa` | [Open](#m-rid-restore) |
| `M-RID-RI-DET-LINEARITY` | `RI_DET_LINEARITY` | 78 | `bf4c245023a9` | [Open](#m-rid-ri-det-linearity) |
| `M-RID-RI-DET-NOISE-AND-DRIFT` | `RI_DET_NOISE_AND_DRIFT` | 83 | `46fbffbbe4ef` | [Open](#m-rid-ri-det-noise-and-drift) |
| `M-RID-STOP` | `STOP` | 20 | `bdd803cf34a0` | [Open](#m-rid-stop) |
| `M-RID-WARM-UP` | `WARM_UP` | 93 | `76f833f716de` | [Open](#m-rid-warm-up) |

<a id="m-rid-equilibration-ri-and-rf"></a>
## M-RID-EQUILIBRATION-RI-AND-RF: EQUILIBRATION_RI_AND RF

Source CMBX: `OQ 2026-07-28.cmbx`  
Decoded flow SHA-256: `ebd9d423a95336e76df503003e4906253b5d0d792dd8f3b3ef32cc01cc7939c1`  
Decoded rows: `64`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	================================================================================		
	Equilibration of the system		
	-------------------------------------------------------------------------------		
	This instrument method is used to equilibrate your system for the RI noise test		
	and FLD tests to ensure the correct pump conditions at sample's start that		
	is at negative retention times for the RI noise test.		
	For the Alliance system the pump commands can		
	not be set at negative retention times (RI noise test).		
	Solvent: Water (HPLC-purity)		
	Solvents degassed via online degasser		
	==================================================================		
	Macros used for pump modules		
	System.WriteReportMacro	Name="PumpModule", Value="$PumpModule"	
	Pump		
	System.WriteReportMacro	Name="Pump", Value="$Pump"	
	System.WriteReportMacro	Name="Pump_Pressure", Value="$Pump_Pressure"	
	Pump DGP		
	System.WriteReportMacro	Name="PumpLeft", Value="$PumpLeft"	
	System.WriteReportMacro	Name="Pump_Pressure_LeftBlock", Value="$Pump_Pressure_LeftBlock"	
	System.WriteReportMacro	Name="PumpRight", Value="$PumpRight"	
	System.WriteReportMacro	Name="Pump_Pressure_RightBlock", Value="$Pump_Pressure_RightBlock"	
	Macros used for inject devices		
	System.WriteReportMacro	Name="SamplerModule", Value="$SamplerModule"	
	System.WriteReportMacro	Name="Sampler", Value="$Sampler"	
	Macros used for column compartements / ovens		
	ColumnOven without autosampler, e.g. TCC-3000		
	System.WriteReportMacro	Name="ColumnOven", Value="$ColumnOven"	
	System.WriteReportMacro	Name="CC", Value="$CC"	
	System.WriteReportMacro	Name="ColumnOven_Temp", Value="$ColumnOven_Temp"	
	Macros used for detectors		
	System.WriteReportMacro	Name="UV", Value="$UV"	
	System.WriteReportMacro	Name="UV_VIS_1", Value="$UV_VIS_1"	
	System.WriteReportMacro	Name="UV_VIS_2", Value="$UV_VIS_2"	
	System.WriteReportMacro	Name="UV_VIS_3", Value="$UV_VIS_3"	
	System.WriteReportMacro	Name="FLD", Value="$FLD"	
	System.WriteReportMacro	Name="FLD_FlowCell", Value="$FLD_FlowCell"	
	System.WriteReportMacro	Name="Emission_1", Value="$Emission_1"	
	System.WriteReportMacro	Name="Emission_2", Value="$Emission_2"	
	System.WriteReportMacro	Name="Emission_3", Value="$Emission_3"	
	System.WriteReportMacro	Name="Emission_4", Value="$Emission_4"	
	System.WriteReportMacro	Name="Emission", Value="$Emission"	
	Dionex RF-2000		
	System.WriteReportMacro	Name="RI", Value="RI"	
	System.WriteReportMacro	Name="RI_1", Value="RI_1"	
	System.WriteReportMacro	Name="ELSD", Value="$ELSD"	
	System.WriteReportMacro	Name="ELS_1", Value="$ELS_1"	
	Macros used for HPLC_Systems		
	System.WriteReportMacro	Name="HPLC_System", Value="$HPLC_System"	
	Macros used for HPLC_Systems		
	System.WriteReportMacro	Name="Valve", Value="$Valve"	
	==================================================================		
	Column oven valve specific settings - for method transfer kit - not supported for dual pumps		
	Pump specific settings		
	Agilent ICF specific LC system settings		
0.000	Equilibration		
	Settings specific for complete systems		
	Pump specific settings		
	Column Oven specific settings		
0.000	InjectPreparation		
	Wait	RI.Ready	
0.000	Inject		
0.000	Run	Duration = 1.000 [min]	
	End		
```

<a id="m-rid-restore"></a>
## M-RID-RESTORE: RESTORE

Source CMBX: `OQ 2026-07-28.cmbx`  
Decoded flow SHA-256: `014dab8776fa2399eb2cc0a4c9fcb16979f5c39caf18982e259875d75f586b36`  
Decoded rows: `15`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	================================================================		
	Restore Customer Settings		
	---------------------------------------------------------------		
	This instrument method is used to restore specific customer settings.		
	==================================================================		
	Sampler specific settings		
	Agilent ICF specific LC system settings		
0.000	Equilibration		
	Settings specific for complete systems		
	Pump specific settings		
	Column Oven specific settings		
0.000	Inject		
0.000	Run	Duration = 1.000 [min]	
	End		
```

<a id="m-rid-ri-det-linearity"></a>
## M-RID-RI-DET-LINEARITY: RI_DET_LINEARITY

Source CMBX: `OQ 2026-07-28.cmbx`  
Decoded flow SHA-256: `bf4c245023a97934f3da131aa20ba3f0ebea0e533140352473f3c4aa6d55c4d7`  
Decoded rows: `78`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	================================================================		
	RI Detector Linearity		
	---------------------------------------------------------------		
	Pressure regulator:    SST-Restriction capillary (ID: 0.18 mm; L: 15 m)		
	Eluent A :             Water (HPLC quality)		
	Solvent degassed via online degasser		
	Samples:               Glycerine 5 mg/ml, 10 mg/ml, 15 mg/ml, 25 mg/ml, 35 mg/ml		
	==================================================================		
	Macros used for pump modules		
	System.WriteReportMacro	Name="PumpModule", Value="$PumpModule"	
	Pump		
	System.WriteReportMacro	Name="Pump", Value="$Pump"	
	System.WriteReportMacro	Name="Pump_Pressure", Value="$Pump_Pressure"	
	Pump DGP		
	System.WriteReportMacro	Name="PumpLeft", Value="$PumpLeft"	
	System.WriteReportMacro	Name="Pump_Pressure_LeftBlock", Value="$Pump_Pressure_LeftBlock"	
	System.WriteReportMacro	Name="PumpRight", Value="$PumpRight"	
	System.WriteReportMacro	Name="Pump_Pressure_RightBlock", Value="$Pump_Pressure_RightBlock"	
	Macros used for inject devices		
	System.WriteReportMacro	Name="SamplerModule", Value="$SamplerModule"	
	System.WriteReportMacro	Name="Sampler", Value="$Sampler"	
	Macros used for column compartements / ovens		
	ColumnOven without autosampler, e.g. TCC-3000		
	System.WriteReportMacro	Name="ColumnOven", Value="$ColumnOven"	
	System.WriteReportMacro	Name="CC", Value="$CC"	
	System.WriteReportMacro	Name="ColumnOven_Temp", Value="$ColumnOven_Temp"	
	Macros used for detectors		
	System.WriteReportMacro	Name="UV", Value="$UV"	
	System.WriteReportMacro	Name="UV_VIS_1", Value="$UV_VIS_1"	
	System.WriteReportMacro	Name="UV_VIS_2", Value="$UV_VIS_2"	
	System.WriteReportMacro	Name="UV_VIS_3", Value="$UV_VIS_3"	
	System.WriteReportMacro	Name="FLD", Value="$FLD"	
	System.WriteReportMacro	Name="Emission_1", Value="$Emission_1"	
	System.WriteReportMacro	Name="Emission_2", Value="$Emission_2"	
	System.WriteReportMacro	Name="Emission_3", Value="$Emission_3"	
	System.WriteReportMacro	Name="Emission_4", Value="$Emission_4"	
	System.WriteReportMacro	Name="Emission", Value="$Emission"	
	Dionex RF-2000		
	System.WriteReportMacro	Name="RI", Value="RI"	
	System.WriteReportMacro	Name="RI_1", Value="RI_1"	
	System.WriteReportMacro	Name="ELSD", Value="$ELSD"	
	System.WriteReportMacro	Name="ELS_1", Value="$ELS_1"	
	Macros used for HPLC_Systems		
	System.WriteReportMacro	Name="HPLC_System", Value="$HPLC_System"	
	Macros used for HPLC_Systems		
	System.WriteReportMacro	Name="Valve", Value="$Valve"	
	==================================================================		
	Column oven valve specific settings - for method transfer kit - not supported for dual pumps		
	Pump specific settings		
	Detector specific settings		
	Settings specific for the Shodex RI-101, ERC RefratoMax520		
	RI.Data_Collection_Rate	5	
	RI.Temperature.Nominal	35	
	RI.Purge	off	
	RI.Recorder_Range	512.00	
	RI.Integrator_Range	500	
	RI.Rise_Time	0.50	
	RI.Polarity	plus	
	RI.Baseline_Shift	0	
	Agilent ICF specific LC system settings		
	Sampler specific settings		
0.000	Equilibration		
	Detector specific settings		
	RI.Autozero		
	Settings specific for complete systems		
	Pump specific settings		
	Column Oven specific settings		
0.000	InjectPreparation		
	Wait	RI.Ready	
0.000	Inject		
0.000	StartRun		
	RI.RI_1.AcqOn		
0.000	Run	Duration = 2.000 [min]	
2.000	StopRun		
	RI.RI_1.AcqOff		
2.000	PostRun		
	End		
```

<a id="m-rid-ri-det-noise-and-drift"></a>
## M-RID-RI-DET-NOISE-AND-DRIFT: RI_DET_NOISE_AND_DRIFT

Source CMBX: `OQ 2026-07-28.cmbx`  
Decoded flow SHA-256: `46fbffbbe4ef91a0e4792cd086718fee40e7183f3d6136cc9cec5aa34bf6dee4`  
Decoded rows: `83`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	===========================================================================		
	Noise and Drift for RI Detctors		
	--------------------------------------------------------------------------		
	Pressure regulator:    SST-Restriction capillary (ID: 0.18 mm; L: 15 m)		
	Solvent A :             Water (HPLC quality)		
	Solvent degassed via online degasser		
	============================================================================		
	Macros used for pump modules		
	System.WriteReportMacro	Name="PumpModule", Value="$PumpModule"	
	Pump		
	System.WriteReportMacro	Name="Pump", Value="$Pump"	
	System.WriteReportMacro	Name="Pump_Pressure", Value="$Pump_Pressure"	
	Pump DGP		
	System.WriteReportMacro	Name="PumpLeft", Value="$PumpLeft"	
	System.WriteReportMacro	Name="Pump_Pressure_LeftBlock", Value="$Pump_Pressure_LeftBlock"	
	System.WriteReportMacro	Name="PumpRight", Value="$PumpRight"	
	System.WriteReportMacro	Name="Pump_Pressure_RightBlock", Value="$Pump_Pressure_RightBlock"	
	Macros used for inject devices		
	System.WriteReportMacro	Name="SamplerModule", Value="$SamplerModule"	
	System.WriteReportMacro	Name="Sampler", Value="$Sampler"	
	Macros used for column compartements / ovens		
	ColumnOven without autosampler, e.g. TCC-3000		
	System.WriteReportMacro	Name="ColumnOven", Value="$ColumnOven"	
	System.WriteReportMacro	Name="CC", Value="$CC"	
	System.WriteReportMacro	Name="ColumnOven_Temp", Value="$ColumnOven_Temp"	
	Macros used for detectors		
	System.WriteReportMacro	Name="UV", Value="$UV"	
	System.WriteReportMacro	Name="UV_VIS_1", Value="$UV_VIS_1"	
	System.WriteReportMacro	Name="UV_VIS_2", Value="$UV_VIS_2"	
	System.WriteReportMacro	Name="UV_VIS_3", Value="$UV_VIS_3"	
	System.WriteReportMacro	Name="FLD", Value="$FLD"	
	System.WriteReportMacro	Name="Emission_1", Value="$Emission_1"	
	System.WriteReportMacro	Name="Emission_2", Value="$Emission_2"	
	System.WriteReportMacro	Name="Emission_3", Value="$Emission_3"	
	System.WriteReportMacro	Name="Emission_4", Value="$Emission_4"	
	System.WriteReportMacro	Name="Emission", Value="$Emission"	
	Dionex RF-2000		
	System.WriteReportMacro	Name="RI", Value="RI"	
	System.WriteReportMacro	Name="RI_1", Value="RI_1"	
	System.WriteReportMacro	Name="ELSD", Value="$ELSD"	
	System.WriteReportMacro	Name="ELS_1", Value="$ELS_1"	
	Macros used for HPLC_Systems		
	System.WriteReportMacro	Name="HPLC_System", Value="$HPLC_System"	
	Macros used for HPLC_Systems		
	System.WriteReportMacro	Name="Valve", Value="$Valve"	
	==================================================================		
	Column oven valve specific settings - for method transfer kit - not supported for dual pumps		
	Pump specific settings		
	Detector specific settings		
	Settings specific for the Shodex RI-101, ERC RefratoMax520		
	RI.Data_Collection_Rate	0.67	
	RI.Temperature.Nominal	35	
	RI.Purge	off	
	RI.Rise_Time	0.50	
	RI.Polarity	Minus	
	RI.Baseline_Shift	0	
	Agilent ICF specific LC system settings		
-40.000	Equilibration	Duration = 40.000 [min]	
	Detector specific settings		
	RI.Autozero		
	Wait	RI.Ready	
	RI.Purge	on	
-39.500	RI.Purge	off	
-39.000	RI.Purge	On	
-38.500	RI.Purge	Off	
-38.000	RI.Purge	On	
-20.000	RI.Purge	Off	
-3.000	RI.Autozero		
	Settings specific for complete systems		
	Column Oven specific settings		
	Pump specific settings		
0.000	InjectPreparation		
	Wait	RI.Ready	
	Pump specific settings		
0.000	Inject		
0.000	StartRun		
	RI.RI_1.AcqOn		
0.000	Run	Duration = 22.000 [min]	
22.000	StopRun		
	RI.RI_1.AcqOff		
22.000	PostRun		
	End		
```

<a id="m-rid-stop"></a>
## M-RID-STOP: STOP

Source CMBX: `OQ 2026-07-28.cmbx`  
Decoded flow SHA-256: `bdd803cf34a0f8e99f97f36341d4e4a2d018a658b70fa47199d46f328b17ed4f`  
Decoded rows: `20`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	================================================================		
	Slow down to standby conditions: 50 µl/min		
	---------------------------------------------------------------		
	This instrument method is used to set the flow to standby conditions.		
	Eluent A : Water (HPLC quality)		
	Solvent degassed via online degasser		
	==================================================================		
	Sampler specific settings		
	Agilent ICF specific LC system settings		
	Pump specific settings		
0.000	Equilibration		
	Settings specific for complete systems		
	Pump specific settings		
	Column Oven specific settings		
0.000	Inject		
	Pump specific settings		
0.000	Run	Duration = 1.000 [min]	
	Pump specific settings		
	End		
```

<a id="m-rid-warm-up"></a>
## M-RID-WARM-UP: WARM_UP

Source CMBX: `OQ 2026-07-28.cmbx`  
Decoded flow SHA-256: `76f833f716def5a55a40e3cce04413ea31bb14dd123f558ee9bfea756efb53a6`  
Decoded rows: `93`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	=========================================================================		
	Warm-Up		
	------------------------------------------------------------------------		
	This instrument method is used to prepare your system for the qualification.		
	Eluent: Methanol or Water (HPLC-purity), depends on the tests to perform		
	Solvents degassed via online degasser		
	============================================================================		
	Macros used for pump modules		
	System.WriteReportMacro	Name="PumpModule", Value="$PumpModule"	
	Pump		
	System.WriteReportMacro	Name="Pump", Value="$Pump"	
	System.WriteReportMacro	Name="Pump_Pressure", Value="$Pump_Pressure"	
	Pump DGP		
	System.WriteReportMacro	Name="PumpLeft", Value="$PumpLeft"	
	System.WriteReportMacro	Name="Pump_Pressure_LeftBlock", Value="$Pump_Pressure_LeftBlock"	
	System.WriteReportMacro	Name="PumpRight", Value="$PumpRight"	
	System.WriteReportMacro	Name="Pump_Pressure_RightBlock", Value="$Pump_Pressure_RightBlock"	
	Macros used for inject devices		
	System.WriteReportMacro	Name="SamplerModule", Value="$SamplerModule"	
	System.WriteReportMacro	Name="Sampler", Value="$Sampler"	
	Macros used for chargers		
	System.WriteReportMacro	Name="Charger", Value="$Charger"	
	Macros used for column compartements / ovens		
	ColumnOven without autosampler, e.g. TCC-3000		
	System.WriteReportMacro	Name="ColumnOven", Value="$ColumnOven"	
	System.WriteReportMacro	Name="CC", Value="$CC"	
	System.WriteReportMacro	Name="ColumnOven_Temp", Value="$ColumnOven_Temp"	
	Macros used for detectors		
	System.WriteReportMacro	Name="UV", Value="$UV"	
	System.WriteReportMacro	Name="UV_VIS_1", Value="$UV_VIS_1"	
	System.WriteReportMacro	Name="UV_VIS_2", Value="$UV_VIS_2"	
	System.WriteReportMacro	Name="UV_VIS_3", Value="$UV_VIS_3"	
	System.WriteReportMacro	Name="FLD", Value="$FLD"	
	System.WriteReportMacro	Name="FLD_FlowCell", Value="$FLD_FlowCell"	
	System.WriteReportMacro	Name="Emission_1", Value="$Emission_1"	
	System.WriteReportMacro	Name="Emission_2", Value="$Emission_2"	
	System.WriteReportMacro	Name="Emission_3", Value="$Emission_3"	
	System.WriteReportMacro	Name="Emission_4", Value="$Emission_4"	
	System.WriteReportMacro	Name="Emission", Value="$Emission"	
	Dionex RF-2000		
	System.WriteReportMacro	Name="RI", Value="RI"	
	System.WriteReportMacro	Name="RI_1", Value="RI_1"	
	System.WriteReportMacro	Name="ELSD", Value="$ELSD"	
	System.WriteReportMacro	Name="ELS_1", Value="$ELS_1"	
	System.WriteReportMacro	Name="CAD", Value="$CAD"	
	System.WriteReportMacro	Name="CAD_1", Value="$CAD_1"	
	System.WriteReportMacro	Name="ECDRS", Value="$ECDRS"	
	System.WriteReportMacro	Name="ECDRS_1", Value="$ECDRS_1"	
	System.WriteReportMacro	Name="ECDRS_2", Value="$ECDRS_2"	
	System.WriteReportMacro	Name="ECDRS_3", Value="$ECDRS_3"	
	System.WriteReportMacro	Name="ECDRS_4", Value="$ECDRS_4"	
	System.WriteReportMacro	Name="ECDRS_5", Value="$ECDRS_5"	
	System.WriteReportMacro	Name="ECDRS_6", Value="$ECDRS_6"	
	System.WriteReportMacro	Name="ECDRS_7", Value="$ECDRS_7"	
	System.WriteReportMacro	Name="ECDRS_8", Value="$ECDRS_8"	
	System.WriteReportMacro	Name="VMD", Value="$VMD"	
	System.WriteReportMacro	Name="VMD_UserConfiguration", Value="$VMD_UserConfiguration"	
	Macros used for HPLC_Systems		
	System.WriteReportMacro	Name="HPLC_System", Value="$HPLC_System"	
	Macros used for Valves		
	System.WriteReportMacro	Name="Valve", Value="$Valve"	
	==================================================================		
	Column oven valve specific settings - for method transfer kit - not supported for dual pumps		
	Column oven specific settings		
	Agilent ICF specific settings		
	Pump specific settings		
	Fluorescence detector specific settings		
	RI-Detector specific settings		
	RI.Temperature.Nominal	35	
	ELS-Detector specific settings		
	Corona-Detector specific settings		
	EC-Detector specific settings		
	UV-Detector settings		
	Detector specific settings		
	Protocol	Unsupported detector.	
	User may add commands specific to his detector model here.		
	Agilent ICF specific LC system settings		
	Sampler specific settings		
0.000	Equilibration		
	Settings specific for complete systems		
	Pump specific settings		
	Column Oven specific settings		
0.000	Inject		
	Detector specific settings		
0.000	StartRun		
	RI.RI_1.AcqOn		
0.000	Run	Duration = 1.500 [min]	
	Detector specific settings		
5.000	StopRun		
	RI.RI_1.AcqOff		
5.000	PostRun		
	End		
```
