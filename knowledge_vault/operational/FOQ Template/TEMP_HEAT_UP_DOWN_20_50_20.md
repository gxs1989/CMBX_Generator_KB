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
	Message	"Column compartment model unknown, please reinspect in production!"		
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
0.000	Inject Preparation			
	Wait	CC.TempReady		
0.000	Start Run			
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
0.700				
	ColumnComp.CC.Temperature.Nominal	20.0		
1.000				
	Trigger "T_Start_Ext" and "T_Start_Int" ensure that the evaluation of heat up and cool down time are starting from the same equilibration conditions (T +/- 1 °C, True Time: 120 sec for external and internal temperature signals)			
Trigger		"T_Start_Ext",
ExtTemp_UpperCC<=21.0 AND ExtTemp_UpperCC>=19.0 AND CC.Temperature.Nominal=20 AND Variables.GenericLong0=0,
TrueTime=120,
Limit=1,
Hysteresis=0,
AllowImmediateExecution=No		
	Variables.GenericLong3	1	Activation of trigger "T_UP"	
End Trigger				
Trigger		"T_Start_Int",
CC.Temperature.Value<=21.0 AND CC.Temperature.Value>=19.0 AND CC.Temperature.Nominal=20 AND Variables.GenericLong0=0,
TrueTime=120,
Limit=1,
Hysteresis=0,
AllowImmediateExecution=No		
	Variables.GenericLong2	1	Activation of trigger "T_UP"	
End Trigger				
	Trigger for heating up the CC from 20 to 50 °C after equilibration			
Trigger		"T_UP",
Variables.GenericLong2=1 AND Variables.GenericLong3=1,
TrueTime=30,
Limit=1,
Hysteresis=0,
AllowImmediateExecution=No		
	ColumnComp.CC.Temperature.Nominal	50.0 [°C]		
	RetTimes.RetTime1	System.Retention		
	Variables.GenericLong0	1		
End Trigger				
	 Trigger for evaluation of HeatUp Time based on external temperature signal			
Trigger		"T_50_Ext",
ExtTemp_UpperCC<=51.0 AND ExtTemp_UpperCC>=49.0 AND CC.Temperature.Nominal=50,
TrueTime=120,
Limit=1,
Hysteresis=0,
AllowImmediateExecution=No		
	RetTimes.RetTime2	System.Retention		
	Variables.GenericLong0	2	activation of Trigger T_DOWN and Trigger T_20_Ext 	
End Trigger				
	 Trigger for evaluation of HeatUp Time based on internal temperature signal			
Trigger		"T_50_Int",
CC.Temperature.Value<=51.0 AND CC.Temperature.Value>=49.0 AND CC.Temperature.Nominal=50,
TrueTime=120,
Limit=1,
Hysteresis=0,
AllowImmediateExecution=No		
	RetTimes.RetTime3	System.Retention		
	Variables.GenericLong1	2	activation of Trigger T_DOWN	
End Trigger				
	Trigger for cooling down the CC from 50 to 20 °C after equilibration			
Trigger		"T_DOWN",
Variables.GenericLong0=2 AND Variables.GenericLong1=2,
TrueTime=30,
Limit=1,
Hysteresis=0,
AllowImmediateExecution=No		
	RetTimes.RetTime4	System.Retention		
	ColumnComp.CC.Temperature.Nominal	20.0 [°C]		
End Trigger				
	 Trigger for evaluation of CoolDown Time based on external temperature signal			
Trigger		"T_20_Ext",
ExtTemp_UpperCC<=21.0 AND ExtTemp_UpperCC>=19.0 AND CC.Temperature.Nominal=20 AND Variables.GenericLong0=2,
TrueTime=120,
Limit=1,
Hysteresis=0,
AllowImmediateExecution=No		
	RetTimes.RetTime5	System.Retention		
	Variables.GenericLong0	3	activation of Trigger END_RUN 	
End Trigger				
	 Trigger for evaluation of CoolDown Time based on internal temperature signal			
Trigger		"T_20_Int",
CC.Temperature.Value<=21.0 AND CC.Temperature.Value>=19.0 AND CC.Temperature.Nominal=20 AND Variables.GenericLong1=2,
TrueTime=120,
Limit=1,
Hysteresis=0,
AllowImmediateExecution=No		
	RetTimes.RetTime6	System.Retention		
	Variables.GenericLong1	3	activation of Trigger END_RUN 	
End Trigger				
Trigger		"END_RUN",
Variables.GenericLong0=3 AND Variables.GenericLong1=3,
TrueTime=30,
Limit=1,
Hysteresis=0,
AllowImmediateExecution=No		
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
240.000				
240.000	Stop Run			
	ColumnComp.CC_Temp.AcqOff			
	ColumnComp.CC_U_Temp_Actual.AcqOff			
	ColumnComp.CC_L_Temp_Actual.AcqOff			
	ColumnComp.CC_UCTL_TempRear_Actual.AcqOff			
	ColumnComp.PWM_CCU_A.AcqOff			
	ColumnComp.PWM_CCU_B.AcqOff			
	ColumnComp.PWM_CCL_A.AcqOff			
	ColumnComp.PWM_CCL_B.AcqOff			
	ColumnComp.Fan_Rear_ActualRPM.AcqOff			
240.000	Post Run	Duration = 0.000 [min]		
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