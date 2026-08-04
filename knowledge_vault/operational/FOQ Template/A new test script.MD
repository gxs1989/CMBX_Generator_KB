Time	Command	Value
	Instrument Setup	
	=========================================================================================	
	 IM to measure Temperature Accuracy at 60°C/80°C and Stability at 80°C	
	=========================================================================================	
	 HPLC-System:	
	 -----------	
	 VH-C10-A or VC-C10-A	
	=========================================================================================	
	 Parameters valid for the whole test.	
	=========================================================================================	
	 If the difference between nominal and actual temperature is larger than ReadyTempDelta, the VTCC is not ready.	
	ColumnComp.CC.ReadyTempDelta	0.1 [°C]
	 The Ready property will become Ready only if the difference between the actual and the nominal temperature will not exceed the ReadyTempDelta for the time interval specified by EquilibrationTime.	
	ColumnComp.CC.EquilibrationTime	0.5 [min]
	 The VTCC controls the temperature only, if TempCtrl is set to ON.	
	ColumnComp.CC.TempCtrl	On
	 Adjusts FanSpeed and switches operating mode	
	ColumnComp.CC.Mode	StillAir
	 Liquid Leak Sensor remains switched off in order to avoid false alarms during temperature changes.	
	ColumnComp.LiquidLeakSensor	Off
	=========================================================================================	
	 Variable Initialization	
	=========================================================================================	
	Variables.GenericDouble1	40.0	First test temperature (Start)
	Variables.GenericDouble2	60.0	Second test temperature (Accuracy)
	Variables.GenericDouble3	80.0	Third test temperature (Accuracy & Stability)
	 Initialize Retention Times used during IM	
	RetTimes.RetTime1	0	Time when 60°C accuracy is logged
	RetTimes.RetTime2	0	Time when 80°C accuracy is logged
	RetTimes.RetTime3	0	Time when 80°C stability measurement starts
	RetTimes.RetTime4	0	Time when 80°C stability measurement ends
	=========================================================================================	
	 Settings for all channels offered for the column compartment by the driver.	
	=========================================================================================	
	 Column compartment	
	ColumnComp.CC_U_Temp_Actual.Data_Collection_Rate	20
	ColumnComp.CC_L_Temp_Actual.Data_Collection_Rate	20
	ColumnComp.CC_UCTL_TempRear_Actual.Data_Collection_Rate	20
	ColumnComp.PWM_CCU_A.Data_Collection_Rate	20
	ColumnComp.PWM_CCU_B.Data_Collection_Rate	20
	ColumnComp.PWM_CCL_A.Data_Collection_Rate	20
	ColumnComp.PWM_CCL_B.Data_Collection_Rate	20
	ColumnComp.Fan_Rear_ActualRPM.Data_Collection_Rate	20
	 External measured temperatures	
	Thermometer1.ExtTemp_UpperCC.Data_Collection_Rate	20
	Thermometer1.ExtTemp_LowerCC.Data_Collection_Rate	20
	Thermometer.Environment_Temperature.Data_Collection_Rate	20
	=========================================================================================	
	 Pre-Run: Set to 40°C and wait for initial ready before starting the 30-minute hold.	
	=========================================================================================	
	ColumnComp.CC.Temperature.Nominal	Variables.GenericDouble1
	Wait	CC.TempReady
0.000	Inject Preparation	
	Delay	1
0.000	Start Run	
	 Column compartment	
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
0.000	Run	Duration = 120.000 [min]
	=============================================================================================================================   	
	Trigger 1: Stabilize at 40°C for 30 minutes, then heat to 60°C.	
	=============================================================================================================================   	
Trigger		"T_HOLD_40",
(CC.Temperature.Nominal=Variables.GenericDouble1) AND CC.TempReady,
TrueTime=1800.00,	30 minutes hold time
Limit=1,
Hysteresis=0.0,
AllowImmediateExecution=No	
	Protocol	"40°C stabilized for 30 minutes. Now heating to 60°C."
	ColumnComp.CC.Temperature.Nominal	Variables.GenericDouble2
End Trigger	
	=============================================================================================================================   	
	Trigger 2: Accuracy at 60°C. Stabilize for 2 minutes, log external temperatures, then heat to 80°C.	
	=============================================================================================================================   	
Trigger		"T_60_ACC",
(CC.Temperature.Nominal=Variables.GenericDouble2) AND CC.TempReady,
TrueTime=120.00,	2 minutes stabilization for accuracy
Limit=1,
Hysteresis=0.0,
AllowImmediateExecution=No	
	Protocol	"60°C stabilized. Logging Accuracy data."
	RetTimes.RetTime1	System.Retention
	Log	Thermometer1.ExtTemp_UpperCC.Signal	External Upper sensor reading for 60°C accuracy
	Log	Thermometer1.ExtTemp_LowerCC.Signal	External Lower sensor reading for 60°C accuracy
	Protocol	"Heating to 80°C."
	ColumnComp.CC.Temperature.Nominal	Variables.GenericDouble3
End Trigger	
	=============================================================================================================================   	
	Trigger 3: Accuracy at 80°C. Stabilize for 2 minutes, log external temperatures, then start Stability hold.	
	=============================================================================================================================   	
Trigger		"T_80_ACC",
(CC.Temperature.Nominal=Variables.GenericDouble3) AND CC.TempReady,
TrueTime=120.00,	2 minutes stabilization for accuracy
Limit=1,
Hysteresis=0.0,
AllowImmediateExecution=No	
	Protocol	"80°C stabilized. Logging Accuracy data."
	RetTimes.RetTime2	System.Retention
	Log	Thermometer1.ExtTemp_UpperCC.Signal	External Upper sensor reading for 80°C accuracy
	Log	Thermometer1.ExtTemp_LowerCC.Signal	External Lower sensor reading for 80°C accuracy
	Protocol	"Starting 15-minute Stability measurement at 80°C."
	RetTimes.RetTime3	System.Retention	Mark the start of stability hold period
End Trigger	
	=============================================================================================================================   	
	Trigger 4: Stability at 80°C. Hold for 15 minutes after accuracy log, then stop acquisition.	
	=============================================================================================================================   	
Trigger		"T_80_STAB",
(CC.Temperature.Nominal=Variables.GenericDouble3) AND CC.TempReady AND (System.Retention>=RetTimes.RetTime3+15.00),
TrueTime=60.00,	Brief confirmation period after the 15-minute hold
Limit=1,
Hysteresis=0.0,
AllowImmediateExecution=No	
	Protocol	"15-minute Stability measurement at 80°C completed."
	RetTimes.RetTime4	System.Retention
	Log	"Stability End"
	 Stop all data acquisition and end the run	
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
	End	Stop Run Trigger execution
End Trigger	
120.000	Stop Run	Fallback stop in case trigger fails, but Trigger 4 should stop it earlier.
End