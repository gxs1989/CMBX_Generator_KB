# FOQ_VASA_Cooled_Flow_adjustment_restriction_capillary Instrument Method Script

Source: decoded CMBX instrument method preview
Format: `CM_METHOD_SCRIPT_MD_FORMAT_SPEC.md` / `CM Compiler Rules.MD`

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
If	SamplerModule.ModelNo="VA-A12-A"		
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
If	SamplerModule_Service.ServiceCode=Service		
Else			
	SamplerModule.SamplerModule_Service.GetServiceCode		
	Delay	5	
	SamplerModule.SamplerModule_Service.ServiceCode	87794	
	Delay	1	
	Log	SamplerModule_Service.ServiceCode	
	Delay	1	
End If			
0.000	Start Run		
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
	Variables.GenericFloat1	(GenericLong0*Variables.GenericFloat0)/Variables.GenericDouble3	"New" flow rate
	Delay	1	
	Log	Variables.GenericFloat1	
If	GenericFloat1>=0.70 AND Variables.GenericFloat1<=1.10		
	PumpModule.Pump.Flow.Nominal	Variables.GenericFloat1	
	End		
Else If	Variables.GenericFloat1>=1.10		
	PumpModule.Pump.Flow.Nominal	1.10	
	Delay	30	
	Variables.GenericDouble4	PumpModule.Pump.Pump_Pressure.Signal	
	Delay	1	
	Log	Variables.GenericDouble4	
If	Variables.GenericDouble4>=Variables.GenericLong1 AND Variables.GenericDouble4<=Variables.GenericLong2		
	Variables.GenericFloat1	1.1	
	End		
Else			
	Protocol	"System Pressure out of Limit - Pressure to low"	
	Variables.GenericFloat1	0.005	Set this variable to a very low value. If the queue is continued by accident, the following injection will be interrupted due to the lower pump pressure limit.
	System.AbortQueue		
End If			
Else If	Variables.GenericFloat1<=0.7		
	PumpModule.Pump.Flow.Nominal	0.7	
	Delay	30	
	Variables.GenericDouble4	PumpModule.Pump.Pump_Pressure.Signal	
	Delay	1	
	Log	Variables.GenericDouble4	
If	Variables.GenericDouble4>=Variables.GenericLong1 AND Variables.GenericDouble4<=Variables.GenericLong2		
	Variables.GenericFloat1	0.7	
	End		
Else			
	Protocol	"System Pressure out of Limit - Pressure to high"	
	Variables.GenericFloat1	0.005	Set this variable to a very low value. If the queue is continued by accident, the following injection will be interrupted due to the lower pump pressure limit.
	System.AbortQueue		
End If			
End If			
If	SamplerModule.TableIndexerMode.Signal>0		
0.040	PumpModule.Pump.Pump_Pressure.AcqOff		
	SamplerModule.TableIndexerMode.AcqOff		
	Delay	1	
	Protocol	"Indexer-Fehler. Bitte Motor des Drehtellers austauschen und den defekten Motor an R&D übergeben."	
	System.AbortQueue		
Else			
End If			
4.000	Stop Run		
	PumpModule.Pump.Pump_Pressure.AcqOff		
	SamplerModule.TableIndexerMode.AcqOff		
	End		
```
