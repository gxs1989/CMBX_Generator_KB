# Pump Original Report Template Evidence

Module: Pump  
Status: ORIGINAL AVAILABLE - semantic report summary not complete  
Delivery_File: 02_REPORT_ORIGINAL_TEMPLATES.md

## Self Index

| ID | Source | Included |
|---|---|---|
| `VA_PUMP_1_01_02` | `Report_VAPump_FOQ_V1_01_02_FORMULA_INVENTORY.md` | Yes |

---

## Evidence: VA_PUMP_1_01_02

Source file: `Report_VAPump_FOQ_V1_01_02_FORMULA_INVENTORY.md`

- **Source CMBX:** `Report_VAPump_FOQ_V1_01_02.cmbx`
- **Extraction scope:** `SheetObject` direct CM formulas only.
- **Not included:** FormulaOne workbook formulas/layout stored in `SpreadSheetData`.
- **Authoring rule:** Retain the sheet/cell binding and fixed channel/component unless a configuration contract approves a change.

## Summary

- Sheets: 19
- Direct CM formula objects: 284
- Formula namespaces: `audit` (127), `chm` (53), `gen` (1), `injection` (4), `other` (8), `precond` (59), `seq` (11), `smp` (21)

## Sheet Applicability

| Sheet | Active | Each Injection | Query | Injection Variable | Query Values |
|---|---|---|---|---|---|
| Default Page | N | Y | Y |  |  |
| Title Page | Y | N | Y | injname | Matrix, Qualif |
| COC | Y | N | Y |  |  |
| Specifications | N | Y | Y |  |  |
| Test Procedures | Y | N | Y | injname | Matrix, Qualif |
| Flow Accuracy | Y | N | Y | injname | Matrix, Flow_Acc |
| Pulsation | Y | N | Y | injname | Matrix, Pulsation |
| Solvent Purity | Y | N | Y | injname | Matrix, Gradient_AB |
| Gradient Accuracy | Y | N | Y | injname | Matrix, Gradient_AB |
| Gradient CD | Y | N | Y | injname | Matrix, Gradient_CD |
| Gradient AC | Y | N | Y | injname | Matrix, Gradient_AC |
| Solvent Selector | Y | N | Y | injname | Matrix, Solvent |
| Digital IO | Y | N | Y | injname | Matrix, Digital_IO |
| Definitions | N | Y | Y |  |  |
| Audit Trail | N | Y | Y |  |  |
| Pump Data | Y | N | Y |  |  |
| Device Configuration | N | Y | N |  |  |
| TA Configuration | N | Y | N |  |  |
| Report History | N | Y | Y |  |  |

## Sheet: Flow Accuracy

| Cell / Range | Object Type | Formula | Fixed Channel | Fixed Component |
|---|---|---|---|---|
| J7 | ReportFormulaObject | smp.program |  |  |
| J12 | ReportFormulaObject | AUDIT.WaterDensity(0.200,"backward") |  |  |
| J13 | ReportFormulaObject | AUDIT.Scale_Drift(0.000,"backward") |  |  |
| J14 | ReportFormulaObject | AUDIT.Separator_Interval(100.000,"backward") |  |  |
| J45 | ReportFormulaObject | AUDIT.scale.weight( AUDIT.RetTime1(100.000,"backward")+0.1,"backward") |  |  |
| I45 | ReportFormulaObject | AUDIT.RetTime1(100.000,"backward") |  |  |
| I46 | ReportFormulaObject | AUDIT.RetTime2(100.000,"backward") |  |  |
| I47 | ReportFormulaObject | AUDIT.RetTime3(100.000,"backward") |  |  |
| I48 | ReportFormulaObject | AUDIT.RetTime4(100.000,"backward") |  |  |
| I49 | ReportFormulaObject | AUDIT.RetTime5(100.000,"backward") |  |  |
| I50 | ReportFormulaObject | AUDIT.RetTime6(100.000,"backward") |  |  |
| I51 | ReportFormulaObject | AUDIT.RetTime7(100.000,"backward") |  |  |
| I52 | ReportFormulaObject | AUDIT.RetTime8(100.000,"backward") |  |  |
| I53 | ReportFormulaObject | AUDIT.RetTime9(100.000,"backward") |  |  |
| I54 | ReportFormulaObject | AUDIT.RetTime10(100.000,"backward") |  |  |
| I55 | ReportFormulaObject | AUDIT.RetTime11(100.000,"backward") |  |  |
| J46 | ReportFormulaObject | AUDIT.scale.weight( AUDIT.RetTime2(100.000,"backward")+0.1,"backward") |  |  |
| J47 | ReportFormulaObject | AUDIT.scale.weight( AUDIT.RetTime3(100.000,"backward")+0.1,"backward") |  |  |
| J48 | ReportFormulaObject | AUDIT.scale.weight( AUDIT.RetTime4(100.000,"backward")+0.1,"backward") |  |  |
| J49 | ReportFormulaObject | AUDIT.scale.weight( AUDIT.RetTime5(100.000,"backward")+0.1,"backward") |  |  |
| J50 | ReportFormulaObject | AUDIT.scale.weight( AUDIT.RetTime6(100.000,"backward")+0.1,"backward") |  |  |
| J51 | ReportFormulaObject | AUDIT.scale.weight( AUDIT.RetTime7(100.000,"backward")+0.1,"backward") |  |  |
| J52 | ReportFormulaObject | AUDIT.scale.weight( AUDIT.RetTime8(100.000,"backward")+0.1,"backward") |  |  |
| J53 | ReportFormulaObject | AUDIT.scale.weight( AUDIT.RetTime9(100.000,"backward")+0.1,"backward") |  |  |
| J54 | ReportFormulaObject | AUDIT.scale.weight( AUDIT.RetTime10(100.000,"backward")+0.1,"backward") |  |  |
| J55 | ReportFormulaObject | AUDIT.scale.weight( AUDIT.RetTime11(100.000,"backward")+0.1,"backward") |  |  |
| H82:J87 | ReportTableObject | smp.name \| "Name " \| "" \| "" \| "" \| chm.sig_value("max",Audit.RetTime_End-2,Audit.RetTime_End)-chm.sig_value("min",Audit.RetTime_End-2,Audit.RetTime_End) \| "Difference Max. - Min." \| "%" \| "Compression_Blk1_Drv1" \| peak.name \| chm.sig_value("max",Audit.RetTime_End-2,Audit.RetTime_End)-chm.sig_value("min",Audit.RetTime_End-2,Audit.RetTime_End) \| "Difference Max. - Min." \| "%" \| "Compression_Blk1_Drv2" \| peak.name |  |  |
| H91:J96 | ReportTableObject | smp.name \| "Name " \| "" \| "" \| "" \| chm.sig_value("max",Audit.RetTime_End-2,Audit.RetTime_End)-chm.sig_value("min",Audit.RetTime_End-2,Audit.RetTime_End) \| "Difference Max. - Min." \| "%" \| "Compression_Blk2_Drv1" \| peak.name \| chm.sig_value("max",Audit.RetTime_End-2,Audit.RetTime_End)-chm.sig_value("min",Audit.RetTime_End-2,Audit.RetTime_End) \| "Difference Max. - Min." \| "%" \| "Compression_Blk2_Drv2" \| peak.name |  |  |
| H103:K108 | ReportTableObject | smp.name \| "Name " \| "" \| "" \| "" \| audit.Variables.GenericDouble0(0,"forward") \| "Compression Variation" \| "%" \| injection.name \| "" \| "" \| injection.name \| "" \| "" \| "" \| "" |  |  |
| H121:I126 | ReportTableObject | smp.name \| "Name " \| "" \| "" \| "" \| AUDIT.GenericLong9(1.8,"forward") \| "FlowCalib" \| "ppm" \| injection.name \| "" \| "" |  |  |
| J15 | ReportFormulaObject | AUDIT.GenericLong1(11.000,"backward") |  |  |
| H134:I139 | ReportTableObject | smp.name \| "Name " \| "" \| "" \| "" \| AUDIT.GenericLong9(1.8,"forward") \| "FlowCalib Left" \| "ppm" \| injection.name \| "" \| "" |  |  |
| H146:I151 | ReportTableObject | smp.name \| "Name " \| "" \| "" \| "" \| AUDIT.GenericLong9(1.8,"forward") \| "FlowCalib Right" \| "ppm" \| injection.name \| "" \| "" |  |  |
| L11 | ReportFormulaObject | chm.sig_value(0.11) | Temp |  |
| M11 | ReportFormulaObject | chm.sig_value(0.11) | TempHeadLeft |  |
| N11 | ReportFormulaObject | chm.sig_value(0.11) | TempHeadRight |  |
| P9 | ReportFormulaObject | audit.PumpModule.Pump.Flow.Nominal |  |  |
| P10 | ReportFormulaObject | chm.sig_value("average", 1, 6) | Pump_Pressure |  |
| Q9 | ReportFormulaObject | audit.PumpModule.PumpLeft.Flow.Nominal |  |  |
| Q10 | ReportFormulaObject | chm.sig_value("average",1,6) | PumpLeft_Pressure |  |
| R9 | ReportFormulaObject | audit.PumpModule.PumpRight.Flow.Nominal |  |  |
| R10 | ReportFormulaObject | chm.sig_value("average",1,6) | PumpRight_Pressure |  |

## Sheet: Pulsation

| Cell / Range | Object Type | Formula | Fixed Channel | Fixed Component |
|---|---|---|---|---|
| J7 | ReportFormulaObject | smp.program |  |  |
| J13 | ReportFormulaObject | chm.sig_value("average", 1, 6) | Press_Ref |  |
| J14 | ReportFormulaObject | (chm.noise(1, 2)/chm.sig_value("average", 1, 2)+chm.noise(2, 3)/chm.sig_value("average", 2, 3)+chm.noise(3, 4)/chm.sig_value("average", 3, 4)+chm.noise(4, 5)/chm.sig_value("average", 4, 5)+chm.noise(5, 6)/chm.sig_value("average", 5, 6))/5*100 | Press_Ref |  |
| J15 | ReportFormulaObject | (chm.noise(1, 2)+chm.noise(2, 3)+chm.noise(3, 4)+chm.noise(4, 5)+chm.noise(5, 6))/5 | Press_Ref |  |
| N9 | ReportFormulaObject | audit.PumpModule.Pump.Flow.Nominal |  |  |
| N10 | ReportFormulaObject | chm.sig_value("average", 1, 6) | Pump_Pressure |  |
| N11 | ReportFormulaObject | AUDIT.Pump_Pressure.Ripple.Value(0.000,"forward") |  |  |
| O9 | ReportFormulaObject | audit.PumpModule.PumpLeft.Flow.Nominal |  |  |
| O10 | ReportFormulaObject | chm.sig_value("average",1,6) | PumpLeft_Pressure |  |
| O11 | ReportFormulaObject | AUDIT.PumpLeft_Pressure.Ripple.Value(0,"forward") |  |  |
| P9 | ReportFormulaObject | audit.PumpModule.PumpRight.Flow.Nominal |  |  |
| P10 | ReportFormulaObject | chm.sig_value("average",1,6) | PumpRight_Pressure |  |
| P11 | ReportFormulaObject | AUDIT.PumpRight_Pressure.Ripple.Value(0,"forward") |  |  |
| N16 | ReportFormulaObject | (chm.noise(1,2)/chm.sig_value("average",1,2)+chm.noise(2,3)/chm.sig_value("average",2,3)+chm.noise(3,4)/chm.sig_value("average",3,4)+chm.noise(4,5)/chm.sig_value("average",4,5)+chm.noise(5,6)/chm.sig_value("average",5,6))/5*100 | Pump_Pressure |  |
| N17 | ReportFormulaObject | (chm.noise(8,9)/chm.sig_value("average",8,9)+chm.noise(9,10)/chm.sig_value("average",9,10)+chm.noise(10,11)/chm.sig_value("average",10,11)+chm.noise(11,12)/chm.sig_value("average",11,12)+chm.noise(12,13)/chm.sig_value("average",12,13))/5*100 | Pump_Pressure |  |
| O16 | ReportFormulaObject | (chm.noise(1,2)/chm.sig_value("average",1,2)+chm.noise(2,3)/chm.sig_value("average",2,3)+chm.noise(3,4)/chm.sig_value("average",3,4)+chm.noise(4,5)/chm.sig_value("average",4,5)+chm.noise(5,6)/chm.sig_value("average",5,6))/5*100 | PumpLeft_Pressure |  |
| O17 | ReportFormulaObject | (chm.noise(8,9)/chm.sig_value("average",8,9)+chm.noise(9,10)/chm.sig_value("average",9,10)+chm.noise(10,11)/chm.sig_value("average",10,11)+chm.noise(11,12)/chm.sig_value("average",11,12)+chm.noise(12,13)/chm.sig_value("average",12,13))/5*100 | PumpLeft_Pressure |  |
| P16 | ReportFormulaObject | (chm.noise(1,2)/chm.sig_value("average",1,2)+chm.noise(2,3)/chm.sig_value("average",2,3)+chm.noise(3,4)/chm.sig_value("average",3,4)+chm.noise(4,5)/chm.sig_value("average",4,5)+chm.noise(5,6)/chm.sig_value("average",5,6))/5*100 | PumpRight_Pressure |  |
| P17 | ReportFormulaObject | (chm.noise(8,9)/chm.sig_value("average",8,9)+chm.noise(9,10)/chm.sig_value("average",9,10)+chm.noise(10,11)/chm.sig_value("average",10,11)+chm.noise(11,12)/chm.sig_value("average",11,12)+chm.noise(12,13)/chm.sig_value("average",12,13))/5*100 | PumpRight_Pressure |  |

## Sheet: Solvent Purity

| Cell / Range | Object Type | Formula | Fixed Channel | Fixed Component |
|---|---|---|---|---|
| J7 | ReportFormulaObject | smp.program |  |  |
| L9 | ReportFormulaObject | audit.PumpModule.Pump.Flow.Nominal |  |  |
| L10 | ReportFormulaObject | chm.sig_value("average", 1, 6) | Pump_Pressure |  |
| M9 | ReportFormulaObject | audit.PumpModule.PumpLeft.Flow.Nominal |  |  |
| M10 | ReportFormulaObject | chm.sig_value("average",1,6) | PumpLeft_Pressure |  |
| N9 | ReportFormulaObject | audit.PumpModule.PumpRight.Flow.Nominal |  |  |
| N10 | ReportFormulaObject | chm.sig_value("average",1,6) | PumpRight_Pressure |  |
| J13 | ReportFormulaObject | chm.noise(18.5,20) | UV_VIS_1_D1 |  |

## Sheet: Gradient Accuracy

| Cell / Range | Object Type | Formula | Fixed Channel | Fixed Component |
|---|---|---|---|---|
| K7 | ReportFormulaObject | smp.program |  |  |
| K11 | ReportFormulaObject | AUDIT.RetTime1("forward") |  |  |
| K12 | ReportFormulaObject | AUDIT.RetTime2("forward") |  |  |
| K13 | ReportFormulaObject | AUDIT.RetTime3("forward") |  |  |
| K14 | ReportFormulaObject | AUDIT.RetTime4("forward") |  |  |
| K15 | ReportFormulaObject | AUDIT.RetTime5("forward") |  |  |
| J45 | ReportFormulaObject | AUDIT.RetTime1("forward") |  |  |
| J46 | ReportFormulaObject | AUDIT.RetTime6("forward") |  |  |
| K45 | ReportFormulaObject | chm.sig_value("average", AUDIT.RetTime1("forward")+Audit.TimeDiff_1, AUDIT.RetTime1("forward")+Audit.TimeDiff_2) | UV_VIS_1 |  |
| K46 | ReportFormulaObject | chm.sig_value("average", AUDIT.RetTime6("forward")+Audit.TimeDiff_3, AUDIT.RetTime6("forward")+Audit.TimeDiff_4) | UV_VIS_1 |  |
| K60 | ReportFormulaObject | AUDIT.RetTime1("forward") |  |  |
| L60 | ReportFormulaObject | AUDIT.RetTime2("forward") |  |  |
| M60 | ReportFormulaObject | AUDIT.RetTime3("forward") |  |  |
| N60 | ReportFormulaObject | AUDIT.RetTime4("forward") |  |  |
| O60 | ReportFormulaObject | AUDIT.RetTime5("forward") |  |  |
| K61 | ReportFormulaObject | chm.sig_value("average", AUDIT.RetTime1("forward")+Audit.TimeDiff_1, AUDIT.RetTime1("forward")+Audit.TimeDiff_2) | UV_VIS_1 |  |
| L61 | ReportFormulaObject | chm.sig_value("average", AUDIT.RetTime2("forward")+Audit.TimeDiff_1, AUDIT.RetTime2("forward")+Audit.TimeDiff_2) | UV_VIS_1 |  |
| M61 | ReportFormulaObject | chm.sig_value("average", AUDIT.RetTime3("forward")+Audit.TimeDiff_1, AUDIT.RetTime3("forward")+Audit.TimeDiff_2) | UV_VIS_1 |  |
| N61 | ReportFormulaObject | chm.sig_value("average", AUDIT.RetTime4("forward")+Audit.TimeDiff_1, AUDIT.RetTime4("forward")+Audit.TimeDiff_2) | UV_VIS_1 |  |
| O61 | ReportFormulaObject | chm.sig_value("average", AUDIT.RetTime5("forward")+Audit.TimeDiff_1, AUDIT.RetTime5("forward")+Audit.TimeDiff_2) | UV_VIS_1 |  |
| K66 | ReportFormulaObject | chm.noise(AUDIT.RetTime1("forward")+Audit.TimeDiff_1, AUDIT.RetTime1("forward")+Audit.TimeDiff_2)*1000 | UV_VIS_1 |  |
| L66 | ReportFormulaObject | chm.noise(AUDIT.RetTime2("forward")+Audit.TimeDiff_1, AUDIT.RetTime2("forward")+Audit.TimeDiff_2)*1000 | UV_VIS_1 |  |
| M66 | ReportFormulaObject | chm.noise(AUDIT.RetTime3("forward")+Audit.TimeDiff_1, AUDIT.RetTime3("forward")+Audit.TimeDiff_2)*1000 | UV_VIS_1 |  |
| N66 | ReportFormulaObject | chm.noise(AUDIT.RetTime4("forward")+Audit.TimeDiff_1, AUDIT.RetTime4("forward")+Audit.TimeDiff_2)*1000 | UV_VIS_1 |  |
| O66 | ReportFormulaObject | chm.noise(AUDIT.RetTime5("forward")+Audit.TimeDiff_1, AUDIT.RetTime5("forward")+Audit.TimeDiff_2)*1000 | UV_VIS_1 |  |
| J77:P82 | ReportTableObject | smp.name \| "Name " \| "" \| "" \| "" \| chm.sig_value("max",0,AUDIT.RetTime1("forward"))-chm.sig_value("min",0,AUDIT.RetTime1("forward")) \| "Difference Max. - Min. I" \| "%" \| "Compression_Blk1_Drv1" \| "" \| chm.sig_value("max",0,AUDIT.RetTime1("forward"))-chm.sig_value("min",0,AUDIT.RetTime1("forward")) \| "Difference Max. - Min. I" \| "%" \| "Compression_Blk1_Drv2" \| "" \| chm.sig_value("max",AUDIT.RetTime5("forward"),AUDIT.RetTime6("forward"))-chm.sig_value("min",AUDIT.RetTime5("forward"),AUDIT.RetTime6("forward")) \| "Difference Max. - Min. II" \| "%" \| "Compression_Blk1_Drv1" \| "" \| chm.sig_value("max",AUDIT.RetTime5("forward"),AUDIT.RetTime6("forward"))-chm.sig_value("min",AUDIT.RetTime5("forward"),AUDIT.RetTime6("forward")) \| "Difference Max. - Min. II" \| "%" \| "Compression_Blk1_Drv2" \| "" \| chm.sig_value("max",AUDIT.RetTime1("forward")+1,AUDIT.RetTime2("forward"))-chm.sig_value("min",AUDIT.RetTime1("forward")+1,AUDIT.RetTime2("forward")) \| "Difference Max. - Min." \| "%" \| "Compression_Blk2_Drv1" \| "" \| chm.sig_value("max",AUDIT.RetTime1("forward")+1,AUDIT.RetTime2("forward"))-chm.sig_value("min",AUDIT.RetTime1("forward")+1,AUDIT.RetTime2("forward")) \| "Difference Max. - Min." \| "%" \| injection.name \| "Compression_Blk2_Drv2" \| "" |  |  |
| J84:L89 | ReportTableObject | smp.name \| "Name " \| "" \| "" \| "" \| chm.sig_value("max",0,AUDIT.RetTime1("forward"))-chm.sig_value("min",0,AUDIT.RetTime1("forward")) \| "Difference Max. - Min." \| "%" \| injection.name \| "CompressionRight" \| "" \| chm.sig_value("max",0,AUDIT.RetTime2("forward"))-chm.sig_value("min",0,AUDIT.RetTime2("forward")) \| "Difference Max-Min" \| "%" \| "CompressionLeft" \| "" |  |  |
| M16 | ReportFormulaObject | AUDIT.PumpModule.Pump.%B.Value(AUDIT.RetTime1("forward")+Audit.TimeDiff_5,"backward") |  |  |
| M17 | ReportFormulaObject | AUDIT.PumpModule.Pump.%B.Value(AUDIT.RetTime2("forward")+Audit.TimeDiff_5,"backward") |  |  |
| M18 | ReportFormulaObject | AUDIT.PumpModule.Pump.%B.Value(AUDIT.RetTime3("forward")+Audit.TimeDiff_5,"backward") |  |  |
| M19 | ReportFormulaObject | AUDIT.PumpModule.Pump.%B.Value(AUDIT.RetTime4("forward")+Audit.TimeDiff_5,"backward") |  |  |
| M20 | ReportFormulaObject | AUDIT.PumpModule.Pump.%B.Value(AUDIT.RetTime5("forward")+Audit.TimeDiff_5,"backward") |  |  |
| N16 | ReportFormulaObject | AUDIT.PumpModule.PumpLeft.%B.Value(AUDIT.RetTime1("forward")+Audit.TimeDiff_5,"backward") |  |  |
| N17 | ReportFormulaObject | AUDIT.PumpModule.PumpLeft.%B.Value(AUDIT.RetTime2("forward")+Audit.TimeDiff_5,"backward") |  |  |
| N18 | ReportFormulaObject | AUDIT.PumpModule.PumpLeft.%B.Value(AUDIT.RetTime3("forward")+Audit.TimeDiff_5,"backward") |  |  |
| N19 | ReportFormulaObject | AUDIT.PumpModule.PumpLeft.%B.Value(AUDIT.RetTime4("forward")+Audit.TimeDiff_5,"backward") |  |  |
| N20 | ReportFormulaObject | AUDIT.PumpModule.PumpLeft.%B.Value(AUDIT.RetTime5("forward")+Audit.TimeDiff_5,"backward") |  |  |
| O16 | ReportFormulaObject | AUDIT.PumpModule.PumpRight.%B.Value(AUDIT.RetTime1("forward")+Audit.TimeDiff_5,"backward") |  |  |
| O17 | ReportFormulaObject | AUDIT.PumpModule.PumpRight.%B.Value(AUDIT.RetTime2("forward")+Audit.TimeDiff_5,"backward") |  |  |
| O18 | ReportFormulaObject | AUDIT.PumpModule.PumpRight.%B.Value(AUDIT.RetTime3("forward")+Audit.TimeDiff_5,"backward") |  |  |
| O19 | ReportFormulaObject | AUDIT.PumpModule.PumpRight.%B.Value(AUDIT.RetTime4("forward")+Audit.TimeDiff_5,"backward") |  |  |
| O20 | ReportFormulaObject | AUDIT.PumpModule.PumpRight.%B.Value(AUDIT.RetTime5("forward")+Audit.TimeDiff_5,"backward") |  |  |
| M9 | ReportFormulaObject | audit.PumpModule.Pump.Flow.Nominal |  |  |
| M10 | ReportFormulaObject | chm.sig_value("average", 1, 6) | Pump_Pressure |  |
| N9 | ReportFormulaObject | audit.PumpModule.PumpLeft.Flow.Nominal |  |  |
| N10 | ReportFormulaObject | chm.sig_value("average",1,6) | PumpLeft_Pressure |  |
| O9 | ReportFormulaObject | audit.PumpModule.PumpRight.Flow.Nominal |  |  |
| O10 | ReportFormulaObject | chm.sig_value("average",1,6) | PumpRight_Pressure |  |

## Sheet: Gradient CD

| Cell / Range | Object Type | Formula | Fixed Channel | Fixed Component |
|---|---|---|---|---|
| K7 | ReportFormulaObject | smp.program |  |  |
| K9 | ReportFormulaObject | audit.PumpModule.Pump.Flow.Nominal |  |  |
| K10 | ReportFormulaObject | chm.sig_value("average") | Pump_Pressure |  |
| K11 | ReportFormulaObject | AUDIT.RetTime1("forward") |  |  |
| K12 | ReportFormulaObject | AUDIT.RetTime2("forward") |  |  |
| K13 | ReportFormulaObject | AUDIT.RetTime3("forward") |  |  |
| K14 | ReportFormulaObject | AUDIT.RetTime4("forward") |  |  |
| K15 | ReportFormulaObject | AUDIT.RetTime5("forward") |  |  |
| K16 | ReportFormulaObject | audit.PumpModule.Pump.%B.Value(AUDIT.RetTime2("forward")+Audit.TimeDiff_5,"backward") |  |  |
| K17 | ReportFormulaObject | audit.PumpModule.Pump.%C.Value(AUDIT.RetTime3("forward")+Audit.TimeDiff_5,"backward") |  |  |
| K18 | ReportFormulaObject | audit.PumpModule.Pump.%D.Value(AUDIT.RetTime4("forward")+Audit.TimeDiff_5,"backward") |  |  |
| J45 | ReportFormulaObject | AUDIT.RetTime1("forward") |  |  |
| J46 | ReportFormulaObject | AUDIT.RetTime5("forward") |  |  |
| K45 | ReportFormulaObject | chm.sig_value("average", AUDIT.RetTime1("forward")+Audit.TimeDiff_1, AUDIT.RetTime1("forward")+Audit.TimeDiff_2) | UV_VIS_1 |  |
| K46 | ReportFormulaObject | chm.sig_value("average",AUDIT.RetTime5("forward")+Audit.TimeDiff_3,AUDIT.RetTime5("forward")+Audit.TimeDiff_4) | UV_VIS_1 |  |
| K60 | ReportFormulaObject | AUDIT.RetTime2("forward") |  |  |
| L60 | ReportFormulaObject | AUDIT.RetTime3("forward") |  |  |
| M60 | ReportFormulaObject | AUDIT.RetTime4("forward") |  |  |
| K61 | ReportFormulaObject | chm.sig_value("average",AUDIT.RetTime2("forward")+Audit.TimeDiff_1,AUDIT.RetTime2("forward")+Audit.TimeDiff_2) | UV_VIS_1 |  |
| L61 | ReportFormulaObject | chm.sig_value("average",AUDIT.RetTime3("forward")+Audit.TimeDiff_1,AUDIT.RetTime3("forward")+Audit.TimeDiff_2) | UV_VIS_1 |  |
| M61 | ReportFormulaObject | chm.sig_value("average",AUDIT.RetTime4("forward")+Audit.TimeDiff_1,AUDIT.RetTime4("forward")+Audit.TimeDiff_2) | UV_VIS_1 |  |

## Sheet: Gradient AC

| Cell / Range | Object Type | Formula | Fixed Channel | Fixed Component |
|---|---|---|---|---|
| K7 | ReportFormulaObject | smp.program |  |  |
| K11 | ReportFormulaObject | AUDIT.RetTime1("forward") |  |  |
| K12 | ReportFormulaObject | AUDIT.RetTime2("forward") |  |  |
| K13 | ReportFormulaObject | AUDIT.RetTime3("forward") |  |  |
| K14 | ReportFormulaObject | AUDIT.RetTime4("forward") |  |  |
| J45 | ReportFormulaObject | AUDIT.RetTime1("forward") |  |  |
| J46 | ReportFormulaObject | AUDIT.RetTime4("forward") |  |  |
| K45 | ReportFormulaObject | chm.sig_value("average", AUDIT.RetTime1("forward")+Audit.TimeDiff_1, AUDIT.RetTime1("forward")+Audit.TimeDiff_2) | UV_VIS_1 |  |
| K46 | ReportFormulaObject | chm.sig_value("average",AUDIT.RetTime4("forward")+Audit.TimeDiff_3,AUDIT.RetTime4("forward")+Audit.TimeDiff_4) | UV_VIS_1 |  |
| K60 | ReportFormulaObject | AUDIT.RetTime2("forward") |  |  |
| L60 | ReportFormulaObject | AUDIT.RetTime3("backward") |  |  |
| K61 | ReportFormulaObject | chm.sig_value("average",AUDIT.RetTime2("forward")+Audit.TimeDiff_1,AUDIT.RetTime2("forward")+Audit.TimeDiff_2) | UV_VIS_1 |  |
| L61 | ReportFormulaObject | chm.sig_value("average",AUDIT.RetTime3("backward")+Audit.TimeDiff_1,AUDIT.RetTime3("backward")+Audit.TimeDiff_2) | UV_VIS_1 |  |
| N17 | ReportFormulaObject | AUDIT.PumpModule.PumpLeft.%C.Value(AUDIT.RetTime3("forward")+Audit.TimeDiff_5,"backward") |  |  |
| O16 | ReportFormulaObject | AUDIT.PumpModule.PumpRight.%B.Value(AUDIT.RetTime2("forward")+Audit.TimeDiff_5,"backward") |  |  |
| O17 | ReportFormulaObject | AUDIT.PumpModule.PumpRight.%C.Value(AUDIT.RetTime3("forward")+Audit.TimeDiff_5,"backward") |  |  |
| N9 | ReportFormulaObject | audit.PumpModule.PumpLeft.Flow.Nominal |  |  |
| N10 | ReportFormulaObject | chm.sig_value("average",1,6) | PumpLeft_Pressure |  |
| O9 | ReportFormulaObject | audit.PumpModule.PumpRight.Flow.Nominal |  |  |
| O10 | ReportFormulaObject | chm.sig_value("average",1,6) | PumpRight_Pressure |  |
| N16 | ReportFormulaObject | AUDIT.PumpModule.PumpLeft.%B.Value(AUDIT.RetTime2("forward")+Audit.TimeDiff_5,"backward") |  |  |

## Sheet: Solvent Selector

| Cell / Range | Object Type | Formula | Fixed Channel | Fixed Component |
|---|---|---|---|---|
| K7 | ReportFormulaObject | smp.program |  |  |
| K9 | ReportFormulaObject | audit.PumpModule.Pump.Flow.Nominal |  |  |
| K10 | ReportFormulaObject | chm.sig_value("min", 0.00, 3.00) | Pump_Pressure |  |
| K11 | ReportFormulaObject | AUDIT.RetTime1("forward") |  |  |
| K12 | ReportFormulaObject | AUDIT.RetTime2("forward") |  |  |
| K13 | ReportFormulaObject | AUDIT.RetTime3("forward") |  |  |
| K14 | ReportFormulaObject | AUDIT.RetTime4("forward") |  |  |
| K15 | ReportFormulaObject | AUDIT.RetTime5("forward") |  |  |
| J45 | ReportFormulaObject | AUDIT.RetTime1("forward") |  |  |
| J46 | ReportFormulaObject | AUDIT.RetTime_End |  |  |
| K45 | ReportFormulaObject | chm.sig_value("average", AUDIT.RetTime1("forward")+Audit.TimeDiff_1, AUDIT.RetTime1("forward")+Audit.TimeDiff_2) | UV_VIS_1 |  |
| K46 | ReportFormulaObject | chm.sig_value("average", AUDIT.RetTime_End("forward")+Audit.TimeDiff_3, AUDIT.RetTime_End("forward")+Audit.TimeDiff_4) | UV_VIS_1 |  |
| K61 | ReportFormulaObject | AUDIT.RetTime2("forward") |  |  |
| L61 | ReportFormulaObject | AUDIT.RetTime3("forward") |  |  |
| M61 | ReportFormulaObject | AUDIT.RetTime4("forward") |  |  |
| N61 | ReportFormulaObject | AUDIT.RetTime5("forward") |  |  |
| K62 | ReportFormulaObject | chm.sig_value("average", AUDIT.RetTime2("forward")+Audit.TimeDiff_1, AUDIT.RetTime2("forward")+Audit.TimeDiff_2) | UV_VIS_1 |  |
| L62 | ReportFormulaObject | chm.sig_value("average", AUDIT.RetTime3("forward")+Audit.TimeDiff_1, AUDIT.RetTime3("forward")+Audit.TimeDiff_2) | UV_VIS_1 |  |
| M62 | ReportFormulaObject | chm.sig_value("average", AUDIT.RetTime4("forward")+Audit.TimeDiff_1, AUDIT.RetTime4("forward")+Audit.TimeDiff_2) | UV_VIS_1 |  |
| N62 | ReportFormulaObject | chm.sig_value("average", AUDIT.RetTime5("forward")+Audit.TimeDiff_1, AUDIT.RetTime5("forward")+Audit.TimeDiff_2) | UV_VIS_1 |  |
| K67 | ReportFormulaObject | chm.noise(AUDIT.RetTime2("forward")+Audit.TimeDiff_1, AUDIT.RetTime2("forward")+Audit.TimeDiff_2)*1000 | UV_VIS_1 |  |
| L67 | ReportFormulaObject | chm.noise(AUDIT.RetTime3("forward")+Audit.TimeDiff_1, AUDIT.RetTime3("forward")+Audit.TimeDiff_2)*1000 | UV_VIS_1 |  |
| M67 | ReportFormulaObject | chm.noise(AUDIT.RetTime4("forward")+Audit.TimeDiff_1, AUDIT.RetTime4("forward")+Audit.TimeDiff_2)*1000 | UV_VIS_1 |  |
| N67 | ReportFormulaObject | chm.noise(AUDIT.RetTime5("forward")+Audit.TimeDiff_1, AUDIT.RetTime5("forward")+Audit.TimeDiff_2)*1000 | UV_VIS_1 |  |

## Sheet: Digital IO

| Cell / Range | Object Type | Formula | Fixed Channel | Fixed Component |
|---|---|---|---|---|
| J7 | ReportFormulaObject | smp.program |  |  |
| K43 | ReportFormulaObject | AUDIT.Pump_Input_1.State(0.150) |  |  |
| K44 | ReportFormulaObject | AUDIT.Pump_Input_1.State(0.350) |  |  |
| K45 | ReportFormulaObject | AUDIT.Pump_Input_1.State(0.550) |  |  |
| K46 | ReportFormulaObject | AUDIT.Pump_Input_1.State(0.750) |  |  |
| N43 | ReportFormulaObject | AUDIT.Pump_Input_2.State(0.150) |  |  |
| N44 | ReportFormulaObject | AUDIT.Pump_Input_2.State(0.350) |  |  |
| N45 | ReportFormulaObject | AUDIT.Pump_Input_2.State(0.550) |  |  |
| N46 | ReportFormulaObject | AUDIT.Pump_Input_2.State(0.750) |  |  |

## Sheet: Definitions

| Cell / Range | Object Type | Formula | Fixed Channel | Fixed Component |
|---|---|---|---|---|
| C7 | ReportFormulaObject | seq.timebase |  |  |
| C8 | ReportFormulaObject | precond.System.Version |  |  |
| C9 | ReportFormulaObject | precond.System.SerialNo |  |  |
| C10 | ReportFormulaObject | seq.name |  |  |
| C11 | ReportFormulaObject | seq.update_time |  |  |
| C12 | ReportFormulaObject | gen.loggedOnUser.userName |  |  |
| E16 | ReportFormulaObject | precond.PumpModule.SerialNo |  |  |
| C17 | ReportFormulaObject | precond.UV.ModelNo |  |  |
| E17 | ReportFormulaObject | precond.UV.SerialNo |  |  |
| G16 | ReportFormulaObject | precond.PumpModule.HeadType |  |  |
| J3 | ReportFormulaObject | seq.timebase |  |  |
| H16 | ReportFormulaObject | precond.PumpModule.FirmwareVersion |  |  |
| D22 | ReportFormulaObject | precond.%B1_Equate |  |  |
| C22 | ReportFormulaObject | precond.%A1_Equate |  |  |
| C23 | ReportFormulaObject | precond.%A2_Equate |  |  |
| C24 | ReportFormulaObject | precond.%A3_Equate |  |  |
| D23 | ReportFormulaObject | precond.%B2_Equate |  |  |
| D24 | ReportFormulaObject | precond.%B3_Equate |  |  |
| F22 | ReportFormulaObject | precond.PumpModule.Pump.%A.Equate |  |  |
| F23 | ReportFormulaObject | precond.PumpModule.Pump.%B.Equate |  |  |
| F24 | ReportFormulaObject | precond.PumpModule.Pump.%C.Equate |  |  |
| F25 | ReportFormulaObject | precond.PumpModule.Pump.%D.Equate |  |  |
| I22 | ReportFormulaObject | precond.PumpRight.%A.Equate |  |  |
| H22 | ReportFormulaObject | precond.PumpLeft.%A.Equate |  |  |
| I23 | ReportFormulaObject | precond.PumpRight.%B.Equate |  |  |
| I24 | ReportFormulaObject | precond.PumpRight.%C.Equate |  |  |
| H23 | ReportFormulaObject | precond.PumpLeft.%B.Equate |  |  |
| H24 | ReportFormulaObject | precond.PumpLeft.%C.Equate |  |  |
| K22 | ReportFormulaObject | precond.PumpModule.Pump.%A.Equate |  |  |
| C13 | ReportFormulaObject | precond.System.Injection.URL |  |  |
| C16 | ReportFormulaObject | precond.PumpModule.ModelNo |  |  |
| D16 | ReportFormulaObject | precond.PumpModule.ModelVariant |  |  |

## Sheet: Pump Data

| Cell / Range | Object Type | Formula | Fixed Channel | Fixed Component |
|---|---|---|---|---|
| I48:L53 | ReportTableObject | smp.number \| "No. " \| "" \| "" \| "" \| smp.name \| "Name " \| "" \| "" \| "" \| AUDIT.LeakFlow_Evaluated(10,"backward") \| "Leak Flow_Evaluated" \| "nL/min" \| "" \| "" \| "" \| injection.name \| "" \| "" |  |  |
| I60:K65 | ReportTableObject | smp.number \| "No. " \| "" \| "" \| "" \| smp.name \| "Name " \| "" \| "" \| "" \| 1000*AUDIT.GenericDouble8(0,"backward") \| "Generic Double8 (measured scale drift)" \| "mg/min" \| "" \| "" |  |  |
| I71:K76 | ReportTableObject | smp.number \| "No. " \| "" \| "" \| "" \| smp.name \| "Name " \| "" \| "" \| "" \| 1000*AUDIT.GenericDouble8(0,"backward") \| "Generic Double8 (measured scale drift)" \| "mg/min" \| "" \| "" |  |  |
| J89 | ReportFormulaObject | precond.Pump_Wellness_LeftBlock.PressCalib_Drv1_B0 |  |  |
| L89 | ReportFormulaObject | precond.Pump_Wellness_RightBlock.PressCalib_Drv1_B0 |  |  |
| M89 | ReportFormulaObject | precond.Pump_Wellness_RightBlock.PressCalib_Drv2_B0 |  |  |
| K89 | ReportFormulaObject | precond.Pump_Wellness_LeftBlock.PressCalib_Drv2_B0 |  |  |
| J87 | ReportFormulaObject | precond.Pump_Wellness_LeftBlock.PressCalib_Drv1_B1 |  |  |
| L87 | ReportFormulaObject | precond.Pump_Wellness_RightBlock.PressCalib_Drv1_B1 |  |  |
| M87 | ReportFormulaObject | precond.Pump_Wellness_RightBlock.PressCalib_Drv2_B1 |  |  |
| K87 | ReportFormulaObject | precond.Pump_Wellness_LeftBlock.PressCalib_Drv2_B1 |  |  |
| J85 | ReportFormulaObject | precond.Pump_Wellness_LeftBlock.PressCalib_Drv1_B2 |  |  |
| L85 | ReportFormulaObject | precond.Pump_Wellness_RightBlock.PressCalib_Drv1_B2 |  |  |
| M85 | ReportFormulaObject | precond.Pump_Wellness_RightBlock.PressCalib_Drv2_B2 |  |  |
| K85 | ReportFormulaObject | precond.Pump_Wellness_LeftBlock.PressCalib_Drv2_B2 |  |  |
| I97:P102 | ReportTableObject | smp.number \| "No. " \| "" \| "" \| "" \| smp.name \| "Name " \| "" \| "" \| "" \| precond.PumpModule.Pump.Pump_Pressure.PressureFactor \| "Pressure Factor" \| "" \| injection.name \| "" \| "" \| precond.PumpModule.Pump.Pump_Pressure.PressureOffset \| "Pressure Offset " \| "" \| injection.name \| "" \| "" \| precond.PumpModule.PumpLeft.PumpLeft_Pressure.PressureFactor \| "Pressure Factor" \| "Left" \| injection.name \| "" \| "" \| precond.PumpModule.PumpLeft.PumpLeft_Pressure.PressureOffset \| "Pressure Offset" \| "Left" \| injection.name \| "" \| "" \| precond.PumpModule.PumpRight.PumpRight_Pressure.PressureFactor \| "Pressure Factor" \| "Right" \| "" \| "" \| precond.PumpModule.PumpRight.PumpRight_Pressure.PressureOffset \| "Pressure Offset" \| "Right" \| "" \| "" |  |  |
| C25 | ReportFormulaObject | AUDIT.Degasser |  |  |
| J108 | ReportFormulaObject | precond.Pump_Service_LeftBlock.FlowAsymmetry |  |  |
| J109 | ReportFormulaObject | precond.Pump_Service_RightBlock.FlowAsymmetry |  |  |
| N116 | ReportFormulaObject | seq.submitTime |  |  |
| O116 | ReportFormulaObject | seq.submitOperator |  |  |
| L116 | ReportFormulaObject | seq.creation_operator |  |  |
| K116 | ReportFormulaObject | seq.creation_time |  |  |
| J116 | ReportFormulaObject | seq.instrument |  |  |
| I116 | ReportFormulaObject | seq.name |  |  |
| M116 | ReportFormulaObject | seq.signStatus |  |  |
| I122:K144 | ReportTableObject | injection.number \| "No. " \| "" \| injection.name \| "" \| "" \| injection.name \| "Injection Name" \| "" \| injection.name \| "" \| "" \| injection.time \| "Inject Time " \| "" \| injection.name \| "" \| "" |  |  |
| C26 | ReportFormulaObject | precond.PumpModule.DegasserPressure |  |  |
| C27 | ReportFormulaObject | AUDIT.DegasserType |  |  |
| M108 | ReportFormulaObject | precond.UV.UVLampOperationTime.Value |  |  |
| P108 | ReportFormulaObject | chm.signalStatistic("max") | RecentDrops |  |
| I152:O166 | ReportTableObject | injection.number \| "No." \| "" \| injection.name \| "" \| "" \| injection.name \| "Injection Name" \| "" \| injection.name \| "" \| "" \| audit.RearSealLeakCounter \| "Rear Seal Leak Counter" \| "drops/h" \| injection.name \| "" \| "" \| chm.signalStatistic("max",chm.end_time-0.4,chm.end_time-0.1) \| "Wash Pump Active" \| "1 = on, 0 = off" \| injection.name \| "RearSealPumpStatus" \| "" \| chm.signalStatistic("max",chm.end_time-0.4,chm.end_time-0.1) \| "Current Drop Count (max)" \| "drops" \| injection.name \| "RecentDrops" \| "" \| chm.signalStatistic("min",chm.end_time-0.4,chm.end_time-0.1) \| "Current Drop Count (min)" \| "drops" \| injection.name \| "RecentDrops" \| "" \| "Result (evaluated)" \| "drops" \| injection.name \| "" \| "" |  |  |
| I172:L177 | ReportTableObject | injection.number \| "No." \| "" \| injection.name \| "" \| "" \| injection.name \| "Injection Name" \| "" \| injection.name \| "" \| "" \| audit.Variables.GenericLong9(15,"backward") \| "Flow Calibration" \| "ppm" \| injection.name \| "" \| "" \| audit.Variables.GenericBool3(15,"backward") \| "FlowCalib Warning" \| "" \| injection.name \| "" \| "" |  |  |
| C24 | ReportFormulaObject | Precond.PumpModule.ModuleHardwareRevision |  |  |
| Q23 | ReportFormulaObject | precond.Pump_Service_LeftBlock.FlowCalibration |  |  |
| R23 | ReportFormulaObject | precond.PumpLeft_Service_LeftBlock.FlowCalibration |  |  |
| S23 | ReportFormulaObject | precond.PumpRight_Service_RightBlock.FlowCalibration |  |  |
| Q24 | ReportFormulaObject | precond.Pump_Wellness_LeftBlock.WorkLoad |  |  |
| R24 | ReportFormulaObject | precond.PumpLeft_Wellness_LeftBlock.WorkLoad |  |  |
| S24 | ReportFormulaObject | precond.PumpRight_Wellness_RightBlock.WorkLoad |  |  |
| P26 | ReportFormulaObject | AUDIT.Pump_Pressure.PressureOffset |  |  |
| P25 | ReportFormulaObject | AUDIT.Pump_Pressure.PressureFactor |  |  |
| R26 | ReportFormulaObject | AUDIT.PumpLeft_Pressure.PressureOffset |  |  |
| R25 | ReportFormulaObject | AUDIT.PumpLeft_Pressure.PressureFactor |  |  |
| S26 | ReportFormulaObject | AUDIT.PumpRight_Pressure.PressureOffset |  |  |
| S25 | ReportFormulaObject | AUDIT.PumpRight_Pressure.PressureFactor |  |  |
| P27 | ReportFormulaObject | audit.PumpModule.Pump.StaticMixer(5,"backward") |  |  |
| R27 | ReportFormulaObject | audit.PumpModule.PumpLeft.StaticMixer(5,"backward") |  |  |
| S27 | ReportFormulaObject | audit.PumpModule.PumpRight.StaticMixer(5,"backward") |  |  |
| P28 | ReportFormulaObject | precond.PumpModule.Pump.Pump_Service_RightBlock.XValue |  |  |
| R28 | ReportFormulaObject | precond.PumpModule.PumpLeft.PumpLeft_Service_LeftBlock.XValue |  |  |
| S28 | ReportFormulaObject | precond.PumpModule.PumpRight.PumpRight_Service_RightBlock.XValue |  |  |
| P29 | ReportFormulaObject | precond.Pump_Service_RightBlock.CamZero |  |  |
| Q29 | ReportFormulaObject | precond.Pump_Service_LeftBlock.CamZero |  |  |
| R29 | ReportFormulaObject | precond.PumpLeft_Service_LeftBlock.CamZero |  |  |
| S29 | ReportFormulaObject | precond.PumpRight_Service_RightBlock.CamZero |  |  |
| P23 | ReportFormulaObject | precond.Pump_Service_RightBlock.FlowCalibration |  |  |
| P24 | ReportFormulaObject | precond.Pump_Wellness_RightBlock.WorkLoad |  |  |
| I184:U189 | ReportTableObject | smp.number \| "No. " \| "" \| "" \| "" \| smp.name \| "Name " \| "" \| "" \| "" \| AUDIT.GenericDouble20(10,"backward") \| "Leak Piston 11 - High Pressure " \| "nL/min" \| injection.name \| "" \| "" \| AUDIT.GenericDouble21(10,"backward") \| "Leak Piston 12 - High Pressure " \| "nL/min" \| injection.name \| "" \| "" \| AUDIT.GenericDouble22(10,"backward") \| "Leak Piston 21 - High Pressure " \| "nL/min" \| injection.name \| "" \| "" \| AUDIT.GenericDouble23(10,"backward") \| "Leak Piston 22- High Pressure " \| "nL/min" \| injection.name \| "" \| "" \| AUDIT.GenericInt20(10,"backward") \| "System Leak- High Pressure " \| "nL/min" \| injection.name \| "" \| "" \| AUDIT.GenericDouble25(10,"backward") \| "Leak Piston11 - Low Pressure " \| "nL/min" \| injection.name \| "" \| "" \| AUDIT.GenericDouble26(10,"backward") \| "Leak Piston12 - Low Pressure " \| "nL/min" \| injection.name \| "" \| "" \| AUDIT.GenericDouble27(10,"backward") \| "Leak Piston21 - Low Pressure " \| "nL/min" \| injection.name \| "" \| "" \| AUDIT.GenericDouble28(10,"backward") \| "Leak Piston22 - Low Pressure " \| "nL/min" \| injection.name \| "" \| "" \| AUDIT.GenericInt21(10,"backward") \| "System Leak- Low Pressure " \| "nL/min" \| injection.name \| "" \| "" \| AUDIT.Pump_Diagnostics.GenericString4(15,"backward")+AUDIT.Pump_Diagnostics.GenericString5(15,"backward")+AUDIT.Pump_Diagnostics.GenericString0(15,"backward")+AUDIT.Pump_Diagnostics.GenericString1(15,"backward")+AUDIT.Pump_Diagnostics.GenericString2(15,"backward")+AUDIT.Pump_Diagnostics.GenericString3(15,"backward") \| "Results " \| "" \| injection.name \| "" \| "" |  |  |
| I200:N205 | ReportTableObject | injection.number \| "No. " \| "" \| "" \| "" \| injection.name \| "Injection Name" \| "" \| "" \| "" \| precond.PumpModule.Pump.Pump_Service_RightBlock.FlowCalibration \| "Flow Calibration (Pump Module.Pump.Pump_Service_Right Block)" \| "ppm" \| injection.name \| "" \| "" \| precond.PumpModule.Pump.Pump_Service_LeftBlock.FlowCalibration \| "Flow Calibration (Pump Module.Pump.Pump_Service_Left Block)" \| "ppm" \| injection.name \| "" \| "" \| precond.PumpModule.PumpRight.PumpRight_Service_RightBlock.FlowCalibration \| "Flow Calibration (Pump Module.Pump Right.Pump Right_Service_Right Block)" \| "ppm" \| injection.name \| "" \| "" \| precond.PumpModule.PumpLeft.PumpLeft_Service_LeftBlock.FlowCalibration \| "Flow Calibration (Pump Module.Pump Left.Pump Left_Service_Left Block)" \| "ppm" \| injection.name \| "" \| "" |  |  |
