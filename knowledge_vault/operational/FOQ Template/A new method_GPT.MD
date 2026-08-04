{Initial Time}    Instrument Setup
=========================================================================================
 IM to measure temperature accuracy at 60 °C and 80 °C,
 after 30 min stabilization at 40 °C.
 At 80 °C, temperature stability is measured in parallel after accuracy point is valid.
=========================================================================================
 HPLC-System:
 ------------
 VH-C10-A or VC-C10-A

=========================================================================================
 Model check and report page count
=========================================================================================

If        ColumnComp.ModelNo="VH-C10-A"
    Variables.GenericLong9        12
    Delay                         1
    Log                           Variables.GenericLong9
Else If   ColumnComp.ModelNo="VC-C10-A"
    Variables.GenericLong9        10
    Delay                         1
    Log                           Variables.GenericLong9
Else
    Message "Column compartment model unknown. Queue will be aborted."
    System.AbortQueue
End If


=========================================================================================
 Test temperature definitions
=========================================================================================

Variables.GenericDouble1          40.0      ; Start / conditioning temperature
Variables.GenericDouble2          60.0      ; Accuracy point 1
Variables.GenericDouble3          80.0      ; Accuracy point 2 + stability point

Log Variables.GenericDouble1
Log Variables.GenericDouble2
Log Variables.GenericDouble3


=========================================================================================
 General temperature control settings
=========================================================================================

ColumnComp.CC.ReadyTempDelta      1.0 [°C]
ColumnComp.CC.EquilibrationTime   0.5 [min]
ColumnComp.CC.TempCtrl            On
ColumnComp.CC.Mode                StillAir

; For VH-C10-A only: switch PCC temperature control off
If        ColumnComp.ModelNo="VH-C10-A"
    ColumnComp.CmdString Cmd="PCC.TempCtrl=0"
    Delay 1
End If

; Avoid false liquid leak alarms during larger temperature changes
ColumnComp.LiquidLeakSensor       Off


=========================================================================================
 Reset RetTimes
=========================================================================================

RetTimes.RetTime1                 0.0       ; 60 °C accuracy point
RetTimes.RetTime2                 0.0       ; 80 °C accuracy point / stability start
RetTimes.RetTime3                 0.0       ; 80 °C stability end
RetTimes.RetTime4                 0.0       ; optional end marker

Log RetTimes.RetTime1
Log RetTimes.RetTime2
Log RetTimes.RetTime3
Log RetTimes.RetTime4


=========================================================================================
 Reset external stability variables
=========================================================================================

StabVars.TriggerStab1             0
StabVars.TriggerStab2             0

StabVars.TempUpperHigh            0.0
StabVars.TempUpperLow             0.0
StabVars.TempLowerHigh            0.0
StabVars.TempLowerLow             0.0

StabVars.CounterUpper             0
StabVars.CounterLower             0

StabVars.UpperReady               0
StabVars.LowerReady               0


=========================================================================================
 Data collection rates
=========================================================================================

ColumnComp.CC_U_Temp_Actual.Data_Collection_Rate         20
ColumnComp.CC_L_Temp_Actual.Data_Collection_Rate         20
ColumnComp.CC_UCTL_TempRear_Actual.Data_Collection_Rate  20

ColumnComp.PWM_CCU_A.Data_Collection_Rate                20
ColumnComp.PWM_CCU_B.Data_Collection_Rate                20
ColumnComp.PWM_CCL_A.Data_Collection_Rate                20
ColumnComp.PWM_CCL_B.Data_Collection_Rate                20

ColumnComp.Fan_Rear_ActualRPM.Data_Collection_Rate       20

ColumnComp.LEDBoard_LeakDiff.Data_Collection_Rate        20
ColumnComp.LEDBoard_A13.Data_Collection_Rate             20
ColumnComp.LEDBoard_A14.Data_Collection_Rate             20
ColumnComp.Oven_Gas_MuteTimeRemain.Data_Collection_Rate  20


=========================================================================================
 Set start temperature to 40 °C before run
=========================================================================================

ColumnComp.CC.Temperature.Nominal Variables.GenericDouble1



0.000    Inject Preparation
=========================================================================================

Wait      ColumnComp.CC.TempReady


; After reaching 40 °C, use stricter ready settings for accuracy points
ColumnComp.CC.ReadyTempDelta      0.2 [°C]
ColumnComp.CC.EquilibrationTime   3.0 [min]



0.000    Start Run
=========================================================================================

ColumnComp.CC_Temp.AcqOn

ColumnComp.CC_U_Temp_Actual.AcqOn
ColumnComp.CC_L_Temp_Actual.AcqOn
ColumnComp.CC_UCTL_TempRear_Actual.AcqOn

ColumnComp.PWM_CCU_A.AcqOn
ColumnComp.PWM_CCU_B.AcqOn
ColumnComp.PWM_CCL_A.AcqOn
ColumnComp.PWM_CCL_B.AcqOn

ColumnComp.Fan_Rear_ActualRPM.AcqOn

Thermometer1.ExtTemp_UpperCC.AcqOn
Thermometer1.ExtTemp_LowerCC.AcqOn
Thermometer.Environment_Temperature.AcqOn

ColumnComp.LEDBoard_LeakDiff.AcqOn
ColumnComp.LEDBoard_A13.AcqOn
ColumnComp.LEDBoard_A14.AcqOn
ColumnComp.Oven_Gas_MuteTimeRemain.AcqOn

Log ColumnComp.ModelNo
Log ColumnComp.CC.Temperature.Nominal
Log Thermometer.Environment_Temperature



0.000    Run
=========================================================================================
Duration = 150.000 [min]


=========================================================================================
 External temperature stability trigger logic
 Purpose:
   UpperReady / LowerReady become 1 only after external Upper / Lower temperatures
   remain within +/- 0.05 °C windows for four 30 s checks.
=========================================================================================

Trigger "Gradient_1",
    (StabVars.TriggerStab1=1) AND (ColumnComp.CC.TempReady),
    TrueTime=30.000 [s],
    Limit=NoLimit,
    Hysteresis=0.0,
    AllowImmediateExecution=No

    StabVars.TriggerStab1 0
    StabVars.TriggerStab2 1

    If Thermometer1.ExtTemp_UpperCC.Signal<=StabVars.TempUpperHigh AND Thermometer1.ExtTemp_UpperCC.Signal>=StabVars.TempUpperLow
        StabVars.CounterUpper StabVars.CounterUpper+1
    Else
        StabVars.TempUpperHigh Thermometer1.ExtTemp_UpperCC.Signal+0.05
        StabVars.TempUpperLow  Thermometer1.ExtTemp_UpperCC.Signal-0.05
        StabVars.CounterUpper  0
        StabVars.UpperReady    0
    End If

    If Thermometer1.ExtTemp_LowerCC.Signal<=StabVars.TempLowerHigh AND Thermometer1.ExtTemp_LowerCC.Signal>=StabVars.TempLowerLow
        StabVars.CounterLower StabVars.CounterLower+1
    Else
        StabVars.TempLowerHigh Thermometer1.ExtTemp_LowerCC.Signal+0.05
        StabVars.TempLowerLow  Thermometer1.ExtTemp_LowerCC.Signal-0.05
        StabVars.CounterLower  0
        StabVars.LowerReady    0
    End If

    If StabVars.CounterUpper>=4
        StabVars.UpperReady 1
    End If

    If StabVars.CounterLower>=4
        StabVars.LowerReady 1
    End If

    Log StabVars.CounterUpper
    Log StabVars.CounterLower
    Log StabVars.UpperReady
    Log StabVars.LowerReady

End Trigger


Trigger "Gradient_2",
    StabVars.TriggerStab2=1,
    TrueTime=30.000 [s],
    Limit=NoLimit,
    Hysteresis=0.0,
    AllowImmediateExecution=No

    StabVars.TriggerStab1 1
    StabVars.TriggerStab2 0

End Trigger


Trigger "ExitRange_Upper",
    (StabVars.TempUpperHigh<>0) AND
    (
        (ColumnComp.CC.TempReady=0) OR
        (Thermometer1.ExtTemp_UpperCC.Signal>StabVars.TempUpperHigh) OR
        (Thermometer1.ExtTemp_UpperCC.Signal<StabVars.TempUpperLow)
    ),
    TrueTime=5.000 [s],
    Limit=NoLimit,
    Hysteresis=0.0,
    AllowImmediateExecution=No

    StabVars.TempUpperHigh 0.0
    StabVars.TempUpperLow  0.0
    StabVars.CounterUpper  0
    StabVars.UpperReady    0

End Trigger


Trigger "ExitRange_Lower",
    (StabVars.TempLowerHigh<>0) AND
    (
        (ColumnComp.CC.TempReady=0) OR
        (Thermometer1.ExtTemp_LowerCC.Signal>StabVars.TempLowerHigh) OR
        (Thermometer1.ExtTemp_LowerCC.Signal<StabVars.TempLowerLow)
    ),
    TrueTime=5.000 [s],
    Limit=NoLimit,
    Hysteresis=0.0,
    AllowImmediateExecution=No

    StabVars.TempLowerHigh 0.0
    StabVars.TempLowerLow  0.0
    StabVars.CounterLower  0
    StabVars.LowerReady    0

End Trigger


=========================================================================================
 Timeout protection
 60 °C point: max 40 min after switching from 40 °C to 60 °C
 80 °C point: max 40 min after valid 60 °C accuracy point
=========================================================================================

Trigger "Abort_Timeout",
    (
        (ColumnComp.CC.Temperature.Nominal=Variables.GenericDouble2 AND System.Retention>70.000 AND RetTimes.RetTime1=0)
        OR
        (ColumnComp.CC.Temperature.Nominal=Variables.GenericDouble3 AND RetTimes.RetTime1>0 AND System.Retention>(RetTimes.RetTime1+40.000) AND RetTimes.RetTime2=0)
    ),
    TrueTime=0.000 [s],
    Limit=1,
    Hysteresis=0.0,
    AllowImmediateExecution=Yes

    Message "QUEUE WAS ABORTED! Temperature accuracy point was not stable within 40 min."
    ColumnComp.CC.Temperature.Nominal 40.0 [°C]
    System.AbortQueue

End Trigger



=========================================================================================
 40 °C conditioning phase
 Start condition:
   40 °C was reached before run by Inject Preparation.
 Run now collects 30 min at 40 °C before heating to 60 °C.
=========================================================================================

Delay 30.000 [min]


=========================================================================================
 60 °C accuracy point
=========================================================================================

ColumnComp.CC.Temperature.Nominal Variables.GenericDouble2
Log ColumnComp.CC.Temperature.Nominal

Delay 60.000 [s]

; reset external stability state for 60 °C
StabVars.TriggerStab1             0
StabVars.TriggerStab2             0
StabVars.TempUpperHigh            0.0
StabVars.TempUpperLow             0.0
StabVars.TempLowerHigh            0.0
StabVars.TempLowerLow             0.0
StabVars.CounterUpper             0
StabVars.CounterLower             0
StabVars.UpperReady               0
StabVars.LowerReady               0

StabVars.TriggerStab1             1

Wait ColumnComp.CC.TempReady AND StabVars.UpperReady=1 AND StabVars.LowerReady=1,
    Run=Continue

RetTimes.RetTime1                 System.Retention
Log RetTimes.RetTime1
Log Thermometer1.ExtTemp_UpperCC
Log Thermometer1.ExtTemp_LowerCC


=========================================================================================
 80 °C accuracy point and stability start
=========================================================================================

ColumnComp.CC.Temperature.Nominal Variables.GenericDouble3
Log ColumnComp.CC.Temperature.Nominal

Delay 60.000 [s]

; reset external stability state for 80 °C
StabVars.TriggerStab1             0
StabVars.TriggerStab2             0
StabVars.TempUpperHigh            0.0
StabVars.TempUpperLow             0.0
StabVars.TempLowerHigh            0.0
StabVars.TempLowerLow             0.0
StabVars.CounterUpper             0
StabVars.CounterLower             0
StabVars.UpperReady               0
StabVars.LowerReady               0

StabVars.TriggerStab1             1

Wait ColumnComp.CC.TempReady AND StabVars.UpperReady=1 AND StabVars.LowerReady=1,
    Run=Continue

RetTimes.RetTime2                 System.Retention
Log RetTimes.RetTime2
Log Thermometer1.ExtTemp_UpperCC
Log Thermometer1.ExtTemp_LowerCC


=========================================================================================
 80 °C stability window
 Report should evaluate temperature stability from RetTime2 to RetTime3.
 Suggested report logic:
   - Split RetTime2 to RetTime3 into 15 intervals of 1 min.
   - Calculate average Upper and Lower external temperature per interval.
   - Stability = max(max-min Upper, max-min Lower).
=========================================================================================

Delay 15.000 [min]

RetTimes.RetTime3                 System.Retention
Log RetTimes.RetTime3


=========================================================================================
 Finish
=========================================================================================

RetTimes.RetTime4                 System.Retention
Log RetTimes.RetTime4

StabVars.TriggerStab1             0
StabVars.TriggerStab2             0

ColumnComp.CC.Temperature.Nominal 40.0 [°C]
Log ColumnComp.CC.Temperature.Nominal

ColumnComp.CC_Temp.AcqOff

ColumnComp.CC_U_Temp_Actual.AcqOff
ColumnComp.CC_L_Temp_Actual.AcqOff
ColumnComp.CC_UCTL_TempRear_Actual.AcqOff

ColumnComp.PWM_CCU_A.AcqOff
ColumnComp.PWM_CCU_B.AcqOff
ColumnComp.PWM_CCL_A.AcqOff
ColumnComp.PWM_CCL_B.AcqOff

ColumnComp.Fan_Rear_ActualRPM.AcqOff

Thermometer1.ExtTemp_UpperCC.AcqOff
Thermometer1.ExtTemp_LowerCC.AcqOff
Thermometer.Environment_Temperature.AcqOff

ColumnComp.LEDBoard_LeakDiff.AcqOff
ColumnComp.LEDBoard_A13.AcqOff
ColumnComp.LEDBoard_A14.AcqOff
ColumnComp.Oven_Gas_MuteTimeRemain.AcqOff

End



150.000    Stop Run
=========================================================================================

StabVars.TriggerStab1             0
StabVars.TriggerStab2             0

ColumnComp.CC_Temp.AcqOff

ColumnComp.CC_U_Temp_Actual.AcqOff
ColumnComp.CC_L_Temp_Actual.AcqOff
ColumnComp.CC_UCTL_TempRear_Actual.AcqOff

ColumnComp.PWM_CCU_A.AcqOff
ColumnComp.PWM_CCU_B.AcqOff
ColumnComp.PWM_CCL_A.AcqOff
ColumnComp.PWM_CCL_B.AcqOff

ColumnComp.Fan_Rear_ActualRPM.AcqOff

Thermometer1.ExtTemp_UpperCC.AcqOff
Thermometer1.ExtTemp_LowerCC.AcqOff
Thermometer.Environment_Temperature.AcqOff

ColumnComp.LEDBoard_LeakDiff.AcqOff
ColumnComp.LEDBoard_A13.AcqOff
ColumnComp.LEDBoard_A14.AcqOff
ColumnComp.Oven_Gas_MuteTimeRemain.AcqOff

End