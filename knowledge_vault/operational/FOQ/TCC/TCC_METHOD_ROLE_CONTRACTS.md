# TCC Method Role Contracts

Version: 0.2
Date: 2026-07-13
Scope: TCC method-script role understanding for `VH-C10-A`, `VC-C10-A`, and `VA-C10-A`

This document is the reusable bridge between a user test intent and a concrete
Chromeleon instrument method script edit. It is not a raw extractor output. It
records the semantic roles that were learned from TCC FOQ TD knowledge,
black-box decompositions, decoded CMBX method scripts, and report formula
contracts.

The goal is to make Test Plan changes evidence-based:

```text
user intent
-> reference CMBX method script
-> method role map
-> editable natural-language change contract
-> reviewed modified method script
-> report/formula impact notes
```

## 1. Source Evidence

| Evidence layer | Source |
|---|---|
| FOQ test meaning | `FOQ_TCC_VX_C10_A_TD_KNOWLEDGE_MANAGEMENT.md`, `FOQ_TD_TEST_LOGIC_KNOWLEDGE_BASE.md` |
| Test node model | `TCC_TEST_KNOWLEDGE_NODE_MODEL.md` |
| Method command extraction | `TCC_METHOD_COMMAND_CONTRACTS.md` |
| Dependency model | `TCC_CM_METHOD_SCRIPT_DEPENDENCY_MODEL.md` |
| Black-box contracts | All `TCC_*_BLACK_BOX_DECOMPOSITION.md` files for Temperature Calibration, Accuracy, Precision/Fan, Stability/PCC, HeatUp/CoolDown, BurnIn, Preheater, Column ID, Valve/Keypad, Liquid Leak, Qualification Service, Factory Default, and Error Log Check |
| Report and DB bridge | `TCC_METHOD_REPORT_ALIGNMENT.md`, `CM_FORMULA_REVERSE_ENGINEERING.md` |

## 2. Role Contract Principle

A CM method script row must not be edited as an isolated text row. Most rows
belong to a role group. A safe edit changes the role group and then propagates
the consequences to RetTimes, report formulas, DB fields, and configuration
requirements.

Core rule:

```text
Do not edit visible setpoint text until the owning role is identified.
```

Example:

```text
ColumnComp.CC.Temperature.Nominal = 20.0
```

can mean very different things:

| Method context | Role | Editable meaning |
|---|---|---|
| `TEMPERATURE_ACCURACY`, near method end | Final reset / cleanup | Locked by default. Not a measurement point. |
| `TEMPERATURE_ACCURACY`, after a RetTime emission | Advance to next accuracy target | Editable only with ladder and RetTime/report remap. |
| `TEMP_HEAT_UP_DOWN_20_50_20`, start phase | Baseline conditioning | Editable with heat/cool trigger and report-name impact. |
| `TEMP_HEAT_UP_DOWN_20_50_20`, cool-down phase | Return target | Editable with RetTime4/5 and cool-down formula impact. |

## 3. Shared Method Role Taxonomy

### 3.1 Model Branch

Typical evidence:

```text
IF ColumnComp.ModelNo = "VH-C10-A"
ELSE IF ColumnComp.ModelNo = "VC-C10-A"
ELSE
  System.AbortQueue
END IF
```

Role:

```text
Select model-specific constants, report page count, optional PCC branch, and
sometimes sequence/IRC branch flags.
```

Edit rule:

```text
Do not remove or merge model branches unless all downstream report templates,
DB fields, and optional hardware symbols are also revalidated.
```

### 3.2 Method State Variables

| Symbol group | Common role | Edit rule |
|---|---|---|
| `Variables.GenericDouble*` | Temperature setpoints, thresholds, or model constants | Editable only after mapping each variable to its role in the selected method. |
| `Variables.GenericLong*` | Page count, phase counter, trigger gate, run-state flag | Usually locked. Changing these can break report pages or trigger flow. |
| `Variables.GenericBool*` | Branch flag, skip flag, model variant flag, IRC helper | Usually locked unless the flag role is explicitly known. |
| `TempVars.*` | Ambient temperature and temperature helper variables | Locked unless target logic explicitly requires an ambient rule change. |
| `StabVars.*` | External thermometer stability-state machine | Locked for normal setpoint edits. |
| `CCCalib.*` | Calibration values and calibration comparison state | Locked outside Calibration. |
| `RetTimes.RetTime*` | Report-visible event anchors | Editable only by preserving physical meaning and report formulas. |

### 3.3 Setup and Readiness Roles

| Role | Typical commands | Meaning | Default edit status |
|---|---|---|---|
| Ready tolerance setup | `ColumnComp.CC.ReadyTempDelta`, `EquilibrationTime` | Defines when `CC.TempReady` becomes meaningful. | Locked |
| Temperature controller setup | `ColumnComp.CC.TempCtrl = On`, `Mode = StillAir` | Enables stable oven control. | Locked |
| Leak sensor mode | `ColumnComp.LiquidLeakSensor = Off/On` | Avoids false alarms during large temp moves. | Locked unless test is Liquid Leak. |
| Acquisition setup | `*.Data_Collection_Rate`, `*.AcqOn`, `*.AcqOff` | Makes raw channels available for report formulas. | Locked unless report channels are remapped. |

### 3.4 Measurement Anchor Roles

| Role | Typical evidence | Report consequence |
|---|---|---|
| Stable-point RetTime | `RetTimes.RetTimeN = System.Retention` after `CC.TempReady` and stability gates | Report averages external thermometer channels around RetTimeN. |
| Transition start RetTime | RetTime emitted just before target change | Report computes heat/cool duration from start/end pair. |
| Transition end RetTime | RetTime emitted when target crossing/hold condition is satisfied | Report uses duration minus stable-hold constant. |
| Diagnostic RetTime | Internal endpoint or PCC event not exported to DB | Must be preserved if report layout or diagnostics use it. |

## 4. Per-Method Role Contracts

### 4.1 `TEMPERATURE_ACCURACY`

Purpose:

```text
Measure external thermometer deviation at a model-specific temperature ladder.
```

Primary injection binding:

| Model | Injection | Processing method | Report template | Sheet |
|---|---|---|---|---|
| `VH-C10-A` | `Temperature Accuracy_H` | `ACCURACY_IRC_STOP_H` | `Report_VTCC_V2_12` | `Temp Accuracy` |
| `VC-C10-A` | `Temperature Accuracy_C` | `ACCURACY_IRC_STOP_C` | `Report_VTCC_V2_12` | `Temp Accuracy` |
| `VA-C10-A` | `Temperature Accuracy_C` | `ACCURACY_IRC_STOP_C` | `Report_VATCC_V1_01` | `Temp Accuracy` |

Role map:

| Role | VH evidence | VC/VA evidence | Meaning |
|---|---|---|---|
| Temperature ladder | `GenericDouble1..5 = 10,20,40,80,120` | `GenericDouble1..5 = 10,20,40,60,85` | Source values for five measurement targets. |
| Ambient skip gate | `TempVars.Ambient_Temp > 28.49`, `GenericBool1` | Same | Allows 10 C point skip under high ambient. |
| Stable measurement anchors | `RetTime1..5` | `RetTime1..5` | Report-visible anchors for each ladder point. |
| External stability machine | `StabVars.TriggerStab*`, external thermometer bands, counter logic | Same | Prevents RetTime until external probes are stable. |
| Final reset | Direct `ColumnComp.CC.Temperature.Nominal = 20.0` near method end | Same | Cleanup target, not `TempAcc20`. |

Report coupling:

| RetTime | VH target | VC/VA target | Report raw window |
|---|---:|---:|---|
| `RetTime1` | 10 | 10 | `RetTime1 - 1.0` to `RetTime1 - 0.2` |
| `RetTime2` | 20 | 20 | `RetTime2 - 1.0` to `RetTime2 - 0.2` |
| `RetTime3` | 40 | 40 | `RetTime3 - 1.0` to `RetTime3 - 0.2` |
| `RetTime4` | 80 | 60 | `RetTime4 - 1.0` to `RetTime4 - 0.2` |
| `RetTime5` | 120 | 85 | `RetTime5 - 1.0` to `RetTime5 - 0.2` |

Editable surfaces:

| User intent | Safe role-level edit | Required follow-up |
|---|---|---|
| `accuracy only 40 C` | Keep method setup and stability gate; keep the 40 C measurement path; disable or skip non-target measurement anchors by a reviewed branch. | Report must use the RetTime mapped to 40 C and ignore missing omitted points. |
| `accuracy from 20 C stable to 40 C` | Treat 20 C as baseline conditioning and 40 C as measurement target, not as a request to edit the final 20 C reset. | Decide whether result is accuracy deviation at 40 C or stability/ramp behavior after a 20->40 transition. |
| Change full ladder | Change `GenericDouble1..5` plus RetTime-target mapping. | Update report cells, DB fields, and acceptance logic. |

Locked semantics:

| Role | Reason |
|---|---|
| External thermometer acquisition | Report formulas read `ExtTemp_LowerCC` and `ExtTemp_UpperCC`. |
| Stability state machine | It defines when a RetTime is valid. |
| Final 20 C reset | Cleanup, not a measurement target. |
| Ambient skip semantics | Affects validity of `RetTime1` and low-temperature DB field. |

Open verification:

| Item | Needed evidence |
|---|---|
| Exact IRC pass/fail action table for `ACCURACY_IRC_STOP_H/C` | Processing method action payload or CM UI export. |
| Runnable one-point accuracy report behavior | Modified report template and CM import trial. |

### 4.2 `TEMPERATURE_CALIBRATION`

Purpose:

```text
Capture TCC calibration state over model-specific temperature points. This is a
foundation for later temperature tests but has different RetTime semantics than
Accuracy.
```

Role map:

| Role | VH evidence | VC/VA evidence | Meaning |
|---|---|---|---|
| Calibration ladder | `120,100,80,60,40,20,10,5` | `85,70,55,40,30,20,10,5` | Calibration capture targets. |
| Pre-start setpoint | `GenericDouble0` | `GenericDouble0` | Conditioning point before capture sequence. |
| Calibration RetTimes | `RetTime1..8` | `RetTime1..8` | Capture/duration evidence, not accuracy averaging anchors. |
| Calibration variables | `CCCalib.*` | `CCCalib.*` | Internal calibration values and checks. |

Editable surfaces:

| User intent | Safe role-level edit | Required follow-up |
|---|---|---|
| Remove unrelated calibration points | High risk. Only possible if later report/formula no longer requires those points. | Calibration report and acceptance criteria must be rewritten. |
| Use calibration as precondition for a custom accuracy/stability test | Keep original calibration method as reference or pre-run, do not silently edit it into measurement method. | Define whether calibration result is required before custom method execution. |

Locked semantics:

```text
Calibration RetTimes are not interchangeable with Accuracy RetTimes.
```

### 4.3 `TEMPERATURE_STABILITY_70_C` and `TEMPERATURE_STABILITY_AND_PCC_70_H`

Purpose:

```text
Hold the TCC at a stability target and evaluate external thermometer range
over the report window. The VH method also carries PCC performance evidence.
```

Primary binding:

| Model | Injection | Method | Report sheet |
|---|---|---|---|
| `VH-C10-A` | `Temperature Stability...` | `TEMPERATURE_STABILITY_AND_PCC_70_H` | `Temp Stability and PCC` |
| `VC-C10-A` / `VA-C10-A` | `Temperature Stability_C` | `TEMPERATURE_STABILITY_70_C` | `Temp Stability` |

Role map:

| Role | Evidence | Meaning |
|---|---|---|
| Stability target | `ColumnComp.CC.Temperature.Nominal = 70.0` | Main hold target. |
| Long acquisition window | External thermometer channels acquired through report window | Supports range calculation. |
| Stability report window | 45 to 60 min report cells | Computes lower/upper sensor ranges. |
| VH PCC branch | PCC RetTimes and PCC temperature commands | VH-only PCC performance result. |

Report coupling:

```text
LowerRange = max(ExtTemp_LowerCC window) - min(ExtTemp_LowerCC window)
UpperRange = max(ExtTemp_UpperCC window) - min(ExtTemp_UpperCC window)
RawStability = max(LowerRange, UpperRange)
```

Editable surfaces:

| User intent | Safe role-level edit | Required follow-up |
|---|---|---|
| `stability at 40 C` | Change the stability target role from 70 C to 40 C while preserving acquisition duration and report window semantics. | Report label/criteria may still say 70 C unless updated. |
| `from 20 C stable to 40 C test stability` | Use 20 C as baseline conditioning, then 40 C as stability hold target. This resembles a custom stability method more than Temperature Accuracy. | Need explicit report window and pass/fail criterion for the 40 C hold. |
| VH without PCC | Possible only if PCC DB/report branch is removed or marked not applicable. | Report template and DB mapping must be branched. |

Locked semantics:

| Role | Reason |
|---|---|
| External channel acquisition | Required for stability calculation. |
| Window duration/report row logic | Defines comparable stability metric. |
| PCC branch in VH production method | Required by current VH FOQ report unless custom report removes it. |

### 4.4 `TEMPERATURE_PRECISION_AND_FAN`

Purpose:

```text
Evaluate repeatability/precision of external thermometer readings and fan or
mode-related behavior under controlled TCC conditions.
```

Role map:

| Role | Evidence | Meaning |
|---|---|---|
| Model page count | `GenericLong9` values by model | Controls report/page behavior. |
| Precision target/hold phases | Temperature nominal and stability/collection windows | Creates repeated measurement samples. |
| External precision windows | Report reads lower/upper thermometer series | Calculates worse sensor range. |
| Fan/mode setup | `ColumnComp.CC.Mode`, fan-related comments/commands | Preserves tested operating mode. |

Report coupling:

```text
LowerRange = max(lower precision cells) - min(lower precision cells)
UpperRange = max(upper precision cells) - min(upper precision cells)
RawPrecision = max(LowerRange, UpperRange)
```

Editable surfaces:

| User intent | Safe role-level edit | Required follow-up |
|---|---|---|
| Change precision target | Only after locating the target role and its report windows. | Update report labels, criteria context, and formula sources if windows move. |
| Remove fan subtest | Possible only after report/DB fields for fan are removed or marked not applicable. | Need report branch. |

Locked semantics:

```text
Do not merge Precision with Stability unless the report formulas distinguish
repeatability windows from long-hold stability windows.
```

### 4.5 `TEMP_HEAT_UP_DOWN_20_50_20`

Purpose:

```text
Measure heat-up and cool-down timing between a stable 20 C baseline, 50 C
target, and return to 20 C.
```

Role map:

| Role | Evidence | Meaning |
|---|---|---|
| Cold precondition | `17 C` then `20 C` readiness | Ensures comparable start before heat-up. |
| Heat-up start | `RetTime1` after internal and external 20 C conditions | Start anchor. |
| Heat-up external endpoint | `RetTime2` after external upper thermometer reaches/holds 50 C | DB/report heat-up endpoint. |
| Heat-up internal endpoint | `RetTime3` | Internal diagnostic endpoint. |
| Cool-down start | `RetTime4` at start of return from 50 C to 20 C | Cool-down start anchor. |
| Cool-down external endpoint | `RetTime5` after external upper thermometer reaches/holds 20 C | DB/report cool-down endpoint. |
| Cool-down internal endpoint | `RetTime6` | Internal diagnostic endpoint. |

Report coupling:

```text
HeatUp_Time_20to50 = RetTime2 - RetTime1 - 2.0 min
CoolDown_Time_50to20 = RetTime5 - RetTime4 - 2.0 min
```

Editable surfaces:

| User intent | Safe role-level edit | Required follow-up |
|---|---|---|
| `HeatUp 25->45->25` | Change baseline, high target, and return target together; update trigger thresholds and labels. | Rename/report formula labels and acceptance context. |
| `only heat-up` | Preserve RetTime1/2; remove or skip cool-down roles only with report/DB change. | Cool-down fields must become not applicable or be removed. |
| `from 20 stable to 40` | This method has the correct transition structure. It can provide design reference for baseline-to-target logic. | If metric is stability rather than timing, use Stability report logic, not HeatUp duration formula. |

Locked semantics:

```text
Do not use RetTime3 or RetTime6 as exported DB endpoints unless the report rule
is changed. Row 66 uses external endpoints RetTime2 and RetTime5.
```

### 4.6 `BURNIN`

Purpose:

```text
Condition and stress the TCC thermal system through high/low/high temperature
cycles before downstream temperature tests. This is a preconditioning method,
not a DB-result method.
```

Primary binding:

| Model | Injection | Method | Processing | Report role |
|---|---|---|---|---|
| `VH-C10-A` | `VTCC_BurnIn` | `BURNIN` | `NO_INTEGRATION` | no mapped result sheet |
| `VC-C10-A` | `VTCC_BurnIn` | `BURNIN` | `NO_INTEGRATION` | no mapped result sheet |
| `VA-C10-A` | `VTCC_BurnIn` | `BURNIN` | `NO_INTEGRATION` | no mapped result sheet |

Role map:

| Role | Evidence | Meaning |
|---|---|---|
| Model thermal range | VH min/max `5/120 C`; VC/VA min/max `5/85 C` | Selects stress-cycle limits. |
| Cycle state | `Variables.GenericFloat1`, triggers `T_Maximum`, `T_Minimum`, `HoldTemp` | Drives high/low/high cycling. |
| Long hold | `Delay 7200.0` | Final high-temperature conditioning period. |
| External thermometer guard | Abort if external signals do not track CC heating | Validates external thermometer configuration plausibility. |
| Leak sensor suppression | `ColumnComp.LiquidLeakSensor = Off` | Avoids false alarms during aggressive thermal cycling. |

Editable surfaces:

| User intent | Safe role-level edit | Required follow-up |
|---|---|---|
| Omit BurnIn from a single custom measurement | Usually allowed if the user accepts changed preconditioning assumptions. | Show warning that downstream tests were validated after BurnIn in FOQ context. |
| Change stress range or duration | High risk. Preserve cloned method unless TD/spec explicitly allows. | Revalidate trigger-cycle semantics and TD duration/cycle requirement. |
| Conditioning-only package | Reuse method as a clone first. | Live CM verification required before parameterized rewrite. |

Locked semantics:

```text
BurnIn has no mapped DB fields and no RetTimes. Do not convert it into an
accuracy/stability result method by editing its setpoints.
```

### 4.7 `PREHEATER`

Purpose:

```text
Verify left/right preheater connection, memory state, temperature response, and
heater-vs-external preheater temperature difference.
```

Primary binding:

| Model | Injection | Method | Report sheet | Applicability |
|---|---|---|---|---|
| `VH-C10-A` | `Preheater Connection Test` | `PREHEATER` | `Preheater Ports_Noise` | closed |
| `VC-C10-A` | `Preheater Connection Test` | `PREHEATER` | `Preheater Ports_Noise` | closed |
| `VA-C10-A` | open / payload exists | `PREHEATER` payload exists | open | do not generate automatically |

Role map:

| Role | Evidence | Meaning |
|---|---|---|
| Background CC state | `ColumnComp.CC.Temperature.Nominal = 15 C` | Keeps oven controlled while preheaters are tested. |
| Preheater baseline | left/right preheaters set to `40 C`, wait ready | Common starting point. |
| Crossing anchors | `RetTime1..4` | left/right 45 C and 55 C crossing anchors. |
| Port metadata | `ModulePresent`, `MemoryState` | Report pass requires module present and memory OK. |
| Temperature difference | heater actual average minus preheater temp average | Reported left/right difference. |

RetTime coupling:

| RetTime | Meaning |
|---|---|
| `RetTime1` | left preheater reaches 45 C |
| `RetTime2` | right preheater reaches 45 C |
| `RetTime3` | left preheater reaches 55 C |
| `RetTime4` | right preheater reaches 55 C |

Editable surfaces:

| User intent | Safe role-level edit | Required follow-up |
|---|---|---|
| Generate standalone preheater diagnostic | Partial. Reuse full method first. | Decide processing binding and report workbook route. |
| Change crossing temperatures | Locked unless report RetTime formulas and acceptance criteria are updated. | Update formulas using `RetTime1..4`. |
| Disable one side | Partial. | Report and DB fields for the removed side must become not applicable. |

Locked semantics:

```text
The four RetTimes are not interchangeable; they encode left/right and 45/55 C
crossing identity.
```

### 4.8 `ColumnID`

Purpose:

```text
Verify Column ID slot descriptions A/B/C/D through audit properties, not raw
temperature channels.
```

Primary binding:

| Model | Injection | Method | Report sheet | Applicability |
|---|---|---|---|---|
| `VH-C10-A` | `ColumnIDs` | `ColumnID` | `Column ID` | closed |
| `VC-C10-A` | `ColumnIDs` | `ColumnID` | `Column ID` | closed |
| `VA-C10-A` | not observed in current VA sequence | payload exists | open | do not add automatically |

Role map:

| Role | Evidence | Meaning |
|---|---|---|
| Model/page context | `Variables.GenericLong9` branch and log | Report/page helper, not physical result. |
| Minimal data carrier | `ColumnComp.CC_Temp.AcqOn/Off` | Allows audit/report evaluation context. |
| Operator setup | Message to plug column ID adapters | Manual precondition. |
| Card-state wait | `Column_A/B/C/D.CardState = OK` | Ensures all slots are visible. |
| Description audit | `Log Column_A/B/C/D.Description` | Source for report cells `L46:L49`. |
| Method-side abort | Abort if descriptions are not `A/B/C/D` | Hard guard before report pass/fail. |

Editable surfaces:

| User intent | Safe role-level edit | Required follow-up |
|---|---|---|
| Reuse full Column ID check | Ready for VC/VH after config validation. | Preserve production processing binding. |
| Change expected labels | Locked. | Report workbook and method abort guard must both change. |
| Add to VA | Locked until VA applicability is confirmed. | Need VA TD/current CMBX evidence. |

Locked semantics:

```text
Column ID has no RetTimes and no raw result channels. Do not invent RetTime
anchors for it.
```

### 4.9 `VALVES`

Purpose:

```text
Exercise valve switching precision and keypad/front-panel behavior through audit
properties and operator interaction.
```

Primary binding:

| Model | Injection | Method | Report sheet | Model difference |
|---|---|---|---|---|
| `VH-C10-A` | `Valve` | `VALVES` | `Valve_Keypad` | upper + lower valve |
| `VC-C10-A` | `Valve` | `VALVES` | `Valve_Keypad` | upper + lower valve |
| `VA-C10-A` | `Valve` | `VALVES` | `Valve_Keypad` | lower valve only |

Role map:

| Role | VC/VH evidence | VA evidence | Meaning |
|---|---|---|---|
| Initial position | upper/lower `6_1` | lower `6_1` | Home-position audit evidence. |
| Switch position | upper/lower `1_2` | lower `1_2` | Exercise alternate position. |
| Return position | upper/lower `6_1` | lower `6_1` | Exercise return to home. |
| Precision logs | upper/lower precision | lower precision | Report fixed-time audit evidence. |
| Keypad block | message, `AcqOff`, disconnect/connect, `FastCoolActive = Off` | same pattern | Operator-assisted keypad/FastCool evidence. |

Editable surfaces:

| User intent | Safe role-level edit | Required follow-up |
|---|---|---|
| Periodic upper/lower valve cycling | Reuse position commands and precision logs; omit keypad/disconnect block unless requested. | Report formulas with fixed-time audit reads must be rewritten or omitted. |
| Full FOQ Valve/Keypad | Reuse whole method. | Preserve keypad/disconnect behavior. |
| Add upper valve to VA | Locked. | Requires VA hardware/config and VATCC report formula confirmation. |

Locked semantics:

```text
Timing changes affect fixed-time report formulas such as -0.05, 0.095, 0.19,
and 0.9 min. Method timing and report formulas must move together.
```

### 4.10 `LIQUID LEAK`

Purpose:

```text
Exercise and report the TCC liquid leak sensor state. This is a hardware/sensor
function test, not a temperature performance calculation.
```

Role map:

| Role | Meaning | Edit status |
|---|---|---|
| Leak-sensor enable/disable | Places the leak sensor into the required test state. | Locked for full FOQ leak test. |
| Leak/audit evidence | Report reads leak-related audit/raw context depending template. | Preserve source symbols. |
| Operator/safe-state context | Leak tests can involve physical sensor state and safety prompts. | Do not auto-generate destructive variants. |

Editable surfaces:

| User intent | Safe role-level edit | Required follow-up |
|---|---|---|
| Include full Liquid Leak test | Reuse production method row. | Preserve processing binding by device. |
| Omit from custom temperature-only package | Usually allowed if DB/report does not require leak result. | Surface as a config/safety omission. |
| Parameterize leak behavior | Not ready. | Need live CM/sensor procedure evidence. |

Open verification:

```text
Use the Liquid Leak black-box decomposition for exact command details before
turning this into a parameterized method generator.
```

### 4.11 `Qualification_Service_Done`

Purpose:

```text
Mark or record qualification/service completion state through ColumnComp
wellness/service commands. This is a service-state side-effect method.
```

Primary binding:

| Model | Injection | Method | Role |
|---|---|---|---|
| `VH-C10-A` | `Qualification_Service_Done` | `Qualification_Service_Done` | service completion marker |
| `VC-C10-A` | `Qualification_Service_Done` | `Qualification_Service_Done` | same method, different processing binding |
| `VA-C10-A` | `Qualification_Service_Done` | `Qualification_Service_Done` | same method |

Role map:

| Role | Evidence | Meaning |
|---|---|---|
| Wellness command | `ColumnComp.ColumnComp_Wellness.QualificationDone` | Declares qualification done. |
| Service done command | service/wellness related method flow | Updates service-state metadata. |
| Metadata/report endpoint | report/internal-use cells | Supports final report metadata, not raw data. |

Editable surfaces:

| User intent | Safe role-level edit | Required follow-up |
|---|---|---|
| Full FOQ sequence | Preserve near end. | Confirm service-state policy. |
| Standalone measurement package | Exclude by default. | Include only if user asks for service-state mutation. |

Locked semantics:

```text
Do not include this method merely because a report field is desired. It changes
instrument wellness/service state.
```

### 4.12 `FACTORYDEFAULT`

Purpose:

```text
Return the TCC to factory/default service state and expose identity metadata for
the final FOQ report and DB upload.
```

Role map:

| Role | Evidence | Meaning |
|---|---|---|
| Service access | `GetServiceCode`, `ServiceCode = 87794` | Enables subsequent service/default actions. |
| Wellness reset | Qualification/service intervals and warning periods set to `None` | Clears reminder configuration. |
| Metadata logs | qualification/service last date/operator/hours/workload | Report/internal metadata source. |
| Log cleanup | `ExceptionLogClear`, `ErrorLog.Clear` | Prepares final error-log state. |
| Revision cleanup | `CC.ThermoUnitRevision=`, `ModuleRevision=` | Clears temporary revision strings. |
| Final TCC state | `Temperature.Nominal = 20 C`, `TempCtrl = Off`, `LiquidLeakSensor = On` | Final safe/default state. |
| Operator prompt | valve covers and thermometer serial/location confirmation | Manual final review. |

Editable surfaces:

| User intent | Safe role-level edit | Required follow-up |
|---|---|---|
| Full FOQ package with DB upload | Include near end. | Preserve metadata/report contract. |
| Single custom functional test | Exclude by default. | Add separate metadata strategy if DB upload still needed. |
| Metadata-only package | Partial. | Workbook-derived `ModelVariant` and serial check remain open. |

Locked semantics:

```text
This method mutates service/default state. Do not use it as a generic cleanup
snippet unless the user explicitly wants factory/default finalization.
```

### 4.13 `CHECKERRORLOG`

Purpose:

```text
Provide final safe-state cleanup and report-table endpoint for the final
audit/error log after Factory Default.
```

Primary binding:

| Model | Injection | Method | Report sheet | DB role |
|---|---|---|---|---|
| `VH-C10-A` | `Error Log Check` | `CHECKERRORLOG` | `Error Log` | no mapped DB fields |
| `VC-C10-A` | `Error Log Check` | `CHECKERRORLOG` | `Error Log` | no mapped DB fields |
| `VA-C10-A` | `Error Log Check` | `CHECKERRORLOG` | `Error Log` | no mapped DB fields |

Role map:

| Role | VH/VC evidence | VA evidence | Meaning |
|---|---|---|---|
| Preheater off | `PrehtRight.TempCtrl = Off` | not present in decoded VA flow | VH/VC safe preheater state. |
| Temperature control off | `ColumnComp.CC.TempCtrl = Off` | same | Final safe CC state. |
| Column temp target | `20 C` in VH/VC flow | not fully mirrored in VA flow | Final stable/safe temperature context. |
| Connection cycle | disconnect/connect/wait ready in VH/VC | smaller VA flow | Refreshes final audit/error-log report state. |
| Report table | `Error Log` `ReportTableObject` `B11:D14`, source `audittrail` | same report family | Renders audit/error log, not scalar formula. |

Editable surfaces:

| User intent | Safe role-level edit | Required follow-up |
|---|---|---|
| Full FOQ package | Keep as last injection. | Preserve report table endpoint. |
| Single custom diagnostic | Replace with equivalent StopRun cleanup only if no Error Log sheet is needed. | Document omission. |
| Change final safe state | Locked unless configuration policy changes. | CM validation required. |

Locked semantics:

```text
Error Log Check has no RetTimes, no raw channel output, and no mapped DB fields.
Its value is final safe state and report-table visibility.
```

## 5. All TCC Method Coverage Matrix

| Method | Primary role | RetTimes | Raw channels | Report / DB role | Test Plan readiness |
|---|---|---|---|---|---|
| `ColumnID` | Column ID audit-property verification | no | carrier only | `Column ID`, DB fields for VC/VH | reusable for VC/VH, VA open |
| `PREHEATER` | preheater left/right response and metadata | `RetTime1..4` | preheater/heater/temp channels | `Preheater Ports_Noise`, DB leaves VC/VH | reusable for VC/VH, VA open |
| `VALVES` | valve position/precision + keypad evidence | no | carrier only | `Valve_Keypad`, report-only | reusable with timing/report caution |
| `BURNIN` | thermal preconditioning / stress history | no | diagnostic channels | no mapped DB | optional for custom single tests |
| `TEMPERATURE_CALIBRATION` | calibration capture and transfer | `RetTime1..8` | internal/external temp channels | calibration report/DB fields | reusable, parameterized edits high risk |
| `TEMPERATURE_ACCURACY` | multi-point external accuracy | `RetTime1..5` | external temp channels | `Temp Accuracy`, DB fields | reusable; one-point edits require report update |
| `TEMPERATURE_PRECISION_AND_FAN` | repeatability/fan mode evidence | method-dependent | external temp/debug channels | precision/fan report | reusable, report windows locked |
| `TEMPERATURE_STABILITY_70_C` | VC/VA long-hold stability/noise | no decoded RetTime dependency for exported stability | external temp + `CC_Temp` | stability/noise report | reusable; shortened methods need report redesign |
| `TEMPERATURE_STABILITY_AND_PCC_70_H` | VH stability + PCC performance | PCC `RetTime2..4` | external temp + `CC_Temp` + `PCC_Temp` | stability/PCC DB fields | reusable for VH only |
| `TEMP_HEAT_UP_DOWN_20_50_20` | heat-up/cool-down timing | `RetTime1..6` | external/internal temp channels | heat/cool DB fields | reusable; target edits require trigger/report update |
| `LIQUID LEAK` | liquid leak sensor function | method-specific / not primary | leak/sensor context | leak report/DB if mapped | reuse production row; parameterized generation open |
| `Qualification_Service_Done` | service/qualification completion side effect | no | no primary raw data | metadata/report endpoint | include only for full FOQ/service-state intent |
| `FACTORYDEFAULT` | final factory/default state + metadata | no | no | metadata DB fields | full FOQ only by default |
| `CHECKERRORLOG` | final safe state + error-log report table | no | no | `Error Log` table, no DB fields | full FOQ final row or explicit audit intent |

## 6. Intent Classification Rules for Test Plan

The local intent classifier should not collapse complex natural language into
one test too early. It should first identify all implicated method roles.

| User wording | Primary role | Reference roles | Notes |
|---|---|---|---|
| `accuracy only 40 C` | Accuracy stable-point measurement at 40 C | Accuracy ladder, RetTime3, external averaging window | Keep the 40 C target role; do not edit final reset. |
| `accuracy from 20 stable to 40` | Accuracy at 40 C with baseline conditioning | HeatUp baseline-transition role, Accuracy 40 C stable-point role | Needs explicit decision whether 20 C is a measured accuracy point. |
| `from 20 C stable to 40 C test stability` | Custom stability at 40 C after 20 C baseline | Stability hold role, HeatUp transition role | This is not plain Accuracy. Output should say multiple method scripts are implicated. |
| `HeatUp 20 to 50` | HeatUp timing role | HeatUp RetTime1/2 | Report computes duration, not accuracy. |
| `merge accuracy and stability` | Composite method | Accuracy RetTime windows and Stability long window | Requires new report design, not only method edit. |

## 7. Method Modification Workflow

### 7.1 Role Map Extraction

Given a reference CMBX method script:

1. Detect method name and model branch.
2. Detect role groups:
   - setup
   - model constants
   - setpoint ladder
   - readiness waits
   - triggers
   - RetTime emissions
   - acquisition windows
   - cleanup
3. Match role groups to this contract.
4. Render an editable natural-language change plan before generating script diff.

### 7.2 Natural-Language Change Plan Pattern

The plan shown to the user should be editable text, but each line should carry a
clear status marker:

```text
[CHANGE] Use 20 C as baseline conditioning before the target.
[CHANGE] Use 40 C as the only reported measurement target.
[LOCKED] Preserve external thermometer acquisition for lower and upper probes.
[LOCKED] Preserve stability gate before writing the reported RetTime.
[OPEN] Confirm whether the result should be Accuracy deviation or Stability range.
```

The UI should highlight:

| Marker | Meaning |
|---|---|
| `[CHANGE]` | Planned modification point. |
| `[LOCKED]` | Must not be changed unless user explicitly overrides and report impact is handled. |
| `[OPEN]` | Needs user or CM evidence before script generation can be trusted. |

### 7.3 Script Diff Generation Rule

Only after the user accepts or edits the change plan:

1. Generate the right-side full method script.
2. Highlight changed script rows.
3. Preserve row kind:
   - `Stage`
   - `Command`
   - `Branch`
   - `Comment`
4. Preserve CM copy/paste columns:
   - row number
   - time
   - command
   - value
   - comment
   - row kind metadata if available

## 8. Open Verification Required

| Gap | Why it matters | Possible evidence source |
|---|---|---|
| Full Chromeleon import behavior for generated one-point methods | Script diff may look correct but CM import can reject hidden dependencies. | CM import trial with exported method script. |
| Exact processing-method action table for IRC stop/pass actions | Processing can insert or stop injections independently of method script. | Processing method XML/action decode or CM UI screenshots. |
| Report template branch for custom reduced tests | Existing report templates expect full FOQ layouts. | Report template workbook/Formulas plus manual CM preview. |
| Configuration manifest per physical instrument | Some symbols depend on device options and imported channels. | Instrument configuration export or CM device tree evidence. |

## 9. Implementation Notes

The Test Plan UI should use this KB as a role dictionary. It should not send the
entire local KB or full method scripts to an AI model by default. For a single
analysis request, the minimal context is:

```text
family
reference CMBX path/name
selected method name
user intent
detected role map summary
relevant role contract section
```

This keeps token use small and prevents mechanical edits such as changing a
final reset line instead of the actual measurement target role.
