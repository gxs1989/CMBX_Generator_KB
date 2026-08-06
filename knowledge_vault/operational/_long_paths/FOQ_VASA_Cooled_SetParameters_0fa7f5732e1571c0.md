# FOQ_VASA_Cooled_SetParameters Instrument Method Script

Source: decoded CMBX instrument method preview
Format: `CM_METHOD_SCRIPT_MD_FORMAT_SPEC.md` / `CM Compiler Rules.MD`

```tsv
Time	Command	Value	Comment
{Initial Time}	Instrument Setup		
	PumpModule.Pump.Pressure.LowerLimit	0 [bar]	
	SamplerModule.Temperature.Nominal	20	
	ColumnComp.CC.Mode	ForcedAir	
	================================================================		
	Set of Service, Qualification and Wellness Parameters		
	================================================================		
If	SamplerModule.ModelNo="VA-A12-A"		
	ColumnComp.CC.Temperature.Nominal	30	
	PumpModule.Pump.Pressure.UpperLimit	500	
	Flow through restriction capillary		
	ColumnComp.UpperValve.CurrentPosition	1	
	ColumnComp.LowerValve.CurrentPosition	1	
Else If	SamplerModule.ModelNo="VC-A13-A"		
	SamplerModule.SamplerModule_Service._SendCommand	"LedBar.ForceColor=1"	Led bar red
	Delay	1	
	Message	"Wrong FOQ template: Please use template for uncooled version of VAS-C. "	
	Delay	1	
	SamplerModule.SamplerModule_Service._SendCommand	"LedBar.ForceColor=0"	Led bar auto
	Delay	1	
	System.AbortQueue		
Else If	SamplerModule.ModelNo="VH-A10-A" or SamplerModule.ModelNo="VF-A10-A" or SamplerModule.ModelNo="VH-A40-A" or SamplerModule.ModelNo="VF-A40-A"		
	SamplerModule.SamplerModule_Service._SendCommand	"LedBar.ForceColor=1"	Led bar red
	Delay	1	
	Message	"Wrong FOQ template: Please use VAS or DVAS template."	
	Delay	1	
	SamplerModule.SamplerModule_Service._SendCommand	"LedBar.ForceColor=0"	Led bar auto
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
If	SamplerModule_Service.ServiceCode=Service		
Else			
	SamplerModule.SamplerModule_Service.GetServiceCode		
	Delay	5	
	SamplerModule.SamplerModule_Service.ServiceCode	87794	
	Delay	1	
	Log	SamplerModule_Service.ServiceCode	
	Delay	1	
End If			
	==============================================================================		
0.100	---------------------------------------------------------------------------------------		
	Set the Qualification parameters (Qualification date equal to FOQ date)		
	---------------------------------------------------------------------------------------		
	SamplerModule.SamplerModule_Wellness.Qualification.Interval	None	
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
	SamplerModule.SamplerModule_Service._SendCommand	"Sampler.SetFactoryDefaults"	
	Delay	2	
	SamplerModule.SamplerModule_Service._SendCommand	"Sampler.SetFactoryInternals"	
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
If	SamplerModule.Sampler.Sampler_Service.InjectOptimizationMode=Firmware		
Else			
	SamplerModule.SamplerModule_Service._SendCommand	"LedBar.ForceColor=1"	
	Message	"The Inject Optimization is turned off. Please repeat the Factory Defaults injection"	
	SamplerModule.SamplerModule_Service._SendCommand	"LedBar.ForceColor=0"	
	System.AbortQueue		
End If			
0.300	SamplerModule.SamplerModule_Wellness.DrainPumpTubeHours.Warning	Off	
	SamplerModule.SamplerModule_Wellness.DrainPumpTubeHours.Limit	Off	
0.350	SamplerModule.Sampler.Sampler_Wellness.NeedleMovements.Warning	Off	
	SamplerModule.Sampler.Sampler_Wellness.NeedleMovements.Limit	Off	
0.400	Log	NeedleMovements.Value	
0.600	SamplerModule.SamplerModule_Service._SendCommand	CommandString="Sampler.LoopVol=130000"	
	SamplerModule.SamplerModule_Service._SendCommand	CommandString="Sampler.NominalLoopVol=100000"	
0.650	Protocol	"Sampler is disconnected and reconnected to send the default sample loop volume to CM."	
0.700	SamplerModule.Disconnect		
1.000	SamplerModule.Connect		
1.300	Log	Sampler.LoopVolume	
	End		
```
