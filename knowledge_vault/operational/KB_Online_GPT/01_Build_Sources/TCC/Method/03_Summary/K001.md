# FOQ TD Test Logic Knowledge Base

This document records the working understanding of the supplied FOQ Test
Description and the corresponding CMBX method/report evidence. It is designed
as a reusable pattern for future FOQ TDs from other modules.

中文目的：不是只提取 FOQ TD 的文字，而是把“TD 要证明什么、CM 方法怎么运行、
报告公式怎么计算、生成时哪些不能猜”整理成知识库。

## Source

Primary TD:

```text
C:\ProgramData\CMBX Data Explorer Workspace\KB\FOQ TD\FOQ_Testdescription_VX-C10-A.docm
```

Extracted text:

```text
knowledge_base/tcc_td_vx_c10_a_text.txt
```

TD metadata from extracted text:

```text
FOQ Test Description (FOQ_TD)
Affected instruments: VH-C10-A, VC-C10-A, VA-C10-A
File reference: FOQ_Testdescription_VX-C10-A.docm
Agile Document ID: DOC0000266
Revision: 1.00
Revision date: 14-Oct-2023
Document owner: Lei Shi
```

Important naming rule:

```text
VX-C10-A is the generic TCC family in the TD.
VH-C10-A, VC-C10-A, and VA-C10-A are affected module variants.
```

So the knowledge base name should be TD/family based, not a single example
device name.

## Core TD Meaning

The TD states that FOQ verifies whether the VX-C10-A family meets the acceptance
criteria in the specification master sheet. The order of tests matters because
earlier tests and thermal history can influence later results.

中文理解：

```text
FOQ 不是一组独立按钮。
它是一个有顺序的生产/出厂验证流程：
  先检查通信/附件/接口类错误，
  再 burn-in 和 calibration，
  再做 accuracy/precision/stability/heat-up 等性能测试，
  最后恢复默认状态并检查日志。
```

TD also notes that `Temperature Accuracy` and `Temperature Stability`
injections are inserted by Intelligent Run Control (IRC) depending on device
type. This explains why processing methods matter even if report formulas do
the final numeric calculation.

## FOQ Test Matrix

Extracted TD matrix:

| Test | VH-C10-A | VC-C10-A | VA-C10-A | 中文理解 |
| --- | --- | --- | --- | --- |
| ColumnIDs | yes | yes | no/variant-dependent | Column ID 端口/芯片识别，早期发现电子通信错误 |
| Preheater Connection Test | yes | yes | yes | 左右 preheater 连接、memory state、热响应和噪声 |
| Valve | yes | yes | yes | 上下阀切换和 keypad 功能 |
| VATCC_BurnIn | yes | yes | yes | 温度循环预处理，减少后续测试受首次高温影响 |
| Temperature Calibration | yes | yes | yes | 用外部温度计校准内部 CC 上下传感器 |
| Temperature Accuracy | yes | yes | yes | 外部测得温度和 nominal setpoint 的偏差 |
| Temperature Precision_and_Fan | yes | yes | yes | 重复性/precision，以及 fan/mode 功能 |
| Temperature Stability_and_PCC | yes | no | no | VH 专属，70 C 稳定性 + PCC 测试 |
| Temperature Stability | no | yes | yes | VC/VA 的 70 C 稳定性 |
| HeatUp and CoolDownTime | yes | yes | yes | 20->50 C 和 50->20 C 的升降温时间 |
| Liquid Leak Test | yes | yes | yes | 漏液传感器和 alarm/mute 流程 |
| Qualification_Service_Done | yes | yes | yes | qualification/service 完成记录 |
| Factory Default | yes | yes | yes | 恢复默认/清理状态/记录身份 |

## Global Hardware and Configuration Requirements

The TD requires calibrated external thermometer hardware for tests that use
external temperature measurement.

From extracted TD:

```text
Temperature accuracy of thermometer: +/- 0.03 C
Thermometer controlled by CM7
P755 series thermometer with two PT100 sensors
Thermometer serial number is set by a custom sequence variable
Sensors are fixed in the column compartment using clips
```

Current CMBX/report channel names:

```text
Thermometer1.ExtTemp_UpperCC
Thermometer1.ExtTemp_LowerCC
Thermometer.Environment_Temperature
```

中文理解：

```text
温度类 FOQ 的外部温度计不是附属信息，而是计算结果的核心数据源。
如果 CM 配置里没有这些通道，method 即使能运行，也不能得到正确 report/DB。
```

## Test Logic By Injection

### 1. Column ID

TD intent:

```text
Before thermal tests, detect electronic communication or port assignment errors.
```

中文解释：

```text
插入 A/B/C/D 四个 column ID tag，确认每个端口读到正确 description。
```

Method evidence:

```text
Message operator to plug adapters.
Wait Column_A-D.CardState=OK.
Log Column_A-D.Description.
Abort if descriptions are not A/B/C/D.
Acquire CC_Temp only as audit/report carrier.
```

Report evidence:

```text
AUDIT.Column_A.Description(0,"forward")
AUDIT.Column_B.Description(0,"forward")
AUDIT.Column_C.Description(0,"forward")
AUDIT.Column_D.Description(0,"forward")
```

Generation note:

```text
This is audit/configuration validation, not raw temperature calculation.
```

### 2. Preheater Connection Test

TD intent:

```text
Test active preheater connection ports, left/right electronics, short-circuit
behavior, memory state and signal noise.
```

中文解释：

```text
用 preheater simulator/测试硬件让左右 preheater 先后升温。
检查左右端口是否存在、memory 是否 OK、升温是否响应、是否串扰、噪声是否正常。
```

Method evidence:

```text
Set left/right preheater nominal 40 C and wait ready.
Temporarily set PREH.L/R PID parameters by CmdString.
Heat left and right toward 60 C.
RetTime1: left reaches 45 C.
RetTime2: right reaches 45 C.
RetTime3: left reaches 55 C.
RetTime4: right reaches 55 C.
Abort if right side heats while right TempCtrl is off, indicating short circuit.
Restore/off controls at the end.
```

Report evidence:

```text
RetTime1..4 prove heat-up events.
precond.ColumnComp.PrehtLeft/Right.ModulePresent
precond.ColumnComp.PrehtLeft/Right.MemoryState
Preheater and heater raw channels provide average, max, and noise windows.
```

Generation note:

```text
Do not generate this test from report formulas alone. The method-side thermal
sequence and short-circuit guard are part of the TD logic.
```

### 3. Valve and Keypad

TD intent:

```text
Check valve electronics and front-panel/keypad behavior.
```

中文解释：

```text
方法驱动上/下阀切换位置，同时记录 precision；之后要求操作者按 keypad/fast cool
相关按钮，确认前面板行为。
```

Method evidence:

```text
UpperValve.CurrentPosition = 6_1
LowerValve.CurrentPosition = 6_1
Log UpperValve.Precision / LowerValve.Precision
UpperValve.CurrentPosition = 1_2
LowerValve.CurrentPosition = 1_2
Log precision again
Return to 6_1
Prompt operator for keypad test
Disconnect/reconnect ColumnComp
Wait ColumnComp.Connected = Connected
FastCoolActive = Off
```

Report evidence:

```text
AUDIT.UpperValve.CurrentPosition at fixed times
AUDIT.LowerValve.CurrentPosition at fixed times
AUDIT.UpperValve.Precision
AUDIT.LowerValve.Precision
AUDIT.ColumnComp.FastCoolState
```

Generation note:

```text
For an automatic periodic valve-cycle method, the core commands are the direct
CurrentPosition assignments. Keypad/disconnect steps should be included only
when the requirement is specifically the FOQ valve/keypad test.
```

### 4. Burn-In

TD intent:

```text
Expose the TCC to high/low/high thermal cycles before temperature-related FOQ
tests because first heating can change sensor behavior.
```

中文解释：

```text
Burn-in 是热历史预处理，不是单纯为了产出一个 DB 数值。
```

TD setpoint idea:

```text
VH: high around 120 C, low around 10 C.
VC/VA: high around 85 C, low around 10 C.
```

Method/report relation:

```text
Method creates conditioning evidence and stable thermal history.
Report formulas are not the main value of this row.
```

Generation note:

```text
Custom short test can omit burn-in only if TD/procedure explicitly allows it.
```

### 5. Temperature Calibration

TD intent:

```text
Calibrate internal upper/lower compartment temperature sensors against external
thermometers.
```

中文解释：

```text
这是写入/记录校准点和偏差的测试，不只是读取温度。
```

Setpoint ladder:

```text
VH: 120, 100, 80, 60, 40, 20, 10, 5 C
VC/VA: 85, 70, 55, 40, 30, 20, 10, 5 C
```

Method evidence:

```text
Initialize RetTime1..8.
At each setpoint, wait ready/stable.
Write RetTimeN.
Write CCCalib.CalPointU/L and CalDevU/L values.
Abort on excessive deviation.
```

Report evidence:

```text
CC_Temp signal values at RetTimes.
External thermometer drift windows.
Audit calibration point/deviation properties.
Environment temperature.
```

Generation note:

```text
To generate calibration, we need the exact point-by-point method script and
calibration write properties. Report formulas only verify the result.
```

### 6. Temperature Accuracy

TD intent:

```text
At each nominal setpoint, compare external measured upper/lower temperature to
the nominal compartment temperature. The largest absolute deviation is the
accuracy result.
```

中文解释：

```text
准确度测试的核心不是“设到某温度后读值”，而是：
  先让 CC 到目标温度，
  再确认外部上下温度计稳定，
  再写 RetTime，
  report 用 RetTime 前一段窗口平均外部温度。
```

Method evidence:

```text
VH setpoints:
  10, 20, 40, 80, 120 C
VC/VA setpoints:
  10, 20, 40, 60, 85 C

If ambient > 28.49 C, first 10 C point can be skipped and method starts at 20 C.
StabVars track external upper/lower stability within +/-0.05 C.
RetTimeN is written only after CC.TempReady and both external probes are stable.
```

Report evidence:

```text
AUDIT.RetTime1..5
AUDIT.ColumnComp.CC.Temperature.Nominal(RetTimeN - 0.1)
chm.sig_value("average", RetTimeN - 1.0, RetTimeN - 0.2)
  FixedChannel ExtTemp_LowerCC
  FixedChannel ExtTemp_UpperCC
Workbook chooses upper/lower value with larger absolute deviation.
```

Generation note:

```text
For a custom "40 C only" accuracy test, RetTime3 is the original 40 C report
anchor in the five-point ladder. If we create a one-point report, we can choose
a new RetTime; if we reuse the original report row, RetTime3 semantics must be
preserved.

The approach/baseline temperature must come from TD logic or user selection.
Do not guess whether a 120 C point starts from 80 C, 20 C, or another state.
```

### 7. Temperature Precision and Fan

TD intent:

```text
Reach the same temperature repeatedly and measure repeatability. Check fan/mode
behavior separately.
```

中文解释：

```text
Precision 不是上下温度计混在一起取最大最小，而是上探头自己比三次，
下探头自己比三次，然后取较差的那个 range。
```

Report rule:

```text
LowerRange = max(K65:K67) - min(K65:K67)
UpperRange = max(L65:L67) - min(L65:L67)
RawPrecision = max(LowerRange, UpperRange)
```

Generation note:

```text
If shortening method, must keep enough repeated measurement windows; otherwise
precision definition本身就不存在。
```

### 8. Temperature Stability and PCC

TD intent:

```text
Measure CC stability at 70 C. For VH only, also test PCC accuracy, drift, noise
and cool-down performance.
```

中文解释：

```text
VH 这条 injection 同时承载两个逻辑：CC 70 C 稳定性 + PCC 测试。
VC/VA 应走 Temperature Stability_C，不应带 PCC 依赖。
```

Report rule:

```text
CC stability:
  15 one-minute external temperature averages from 45..60 min.
  Stability = max(range(lower), range(upper)).

PCC:
  Accuracy windows: 0..5, 10..15, 19..24 min.
  Drift: linear/regression-like slope over 19..24 min.
  Cooldown: RetTime4 - RetTime3.
```

Generation note:

```text
For non-VH variants, remove PCC method commands and report dependencies.
```

### 9. Heat-Up and Cool-Down

TD intent:

```text
Measure 20->50 C heat-up time and 50->20 C cool-down time.
```

中文解释：

```text
method 写出的 RetTime 包含稳定保持过程，所以 report 最后会减去 2.0 min。
```

Method/report contract:

```text
RetTime1 = heat-up start
RetTime3 = heat-up stable/end
RetTime4 = cool-down start
RetTime6 = cool-down stable/end

HeatUp = RetTime3 - RetTime1 - 2.0
CoolDown = RetTime6 - RetTime4 - 2.0
```

Generation note:

```text
如果改变脚本 hold/trigger 结构，report 里的 -2.0 min 也必须重新评估。
```

### 10. Liquid Leak

TD intent:

```text
Verify liquid leak sensor and alarm/mute workflow.
```

中文解释：

```text
这是人工交互测试。方法必须提示加水、等待 Leak、记录状态、提示 mute/清理。
```

Report evidence:

```text
AUDIT.LiquidLeak(100,"backward")
precond.LiquidLeakCalibrationValue
```

Generation note:

```text
不能把 Message/手动步骤删掉，否则只是生成了 audit 值，不再是 TD 定义的漏液测试。
```

### 11. Qualification Service

TD intent:

```text
Record completion evidence for qualification/service state.
```

中文解释：

```text
这是流程/状态记录，不是温度性能测试。
```

Generation note:

```text
应与功能测试分开处理，避免把 service-state 写入动作误当作普通 report calculation。
```

### 12. Factory Default

TD intent:

```text
Restore expected factory/default state and record device identity.
```

中文解释：

```text
这是会改变设备状态的清理步骤。包括 service interval、日志、revision 字段、
温控安全状态和最终人工检查。
```

Report evidence:

```text
AUDIT.ColumnComp.ModelNo
precond.ColumnComp.SerialNo
precond.ColumnComp.FirmwareVersion
precond.ColumnComp.HardwareVersion
precond.ColumnComp.ModuleHardwareRevision
sequence custom variables for thermometer serial/location
```

Generation note:

```text
不要默认把 Factory Default 加入任何单点诊断方法；只有完整 FOQ/生产流程需要时加入。
```

### 13. Error Log Check

TD intent:

```text
Check final error-log state and leave the instrument in a safe stopped state.
```

中文解释：

```text
结束前关闭 preheater/CC 温控，确认没有残留错误或危险运行状态。
```

Generation note:

```text
完整 FOQ-like sequence 应有安全 stop/end-state。单个自定义 injection 也应在
StopRun 里包含等价 cleanup。
```

## Acceptance Criteria Currently Captured

From TD/reverse notes:

```text
Temperature Accuracy: +/- 0.5 C
Temperature Precision: <= 0.1 C
Temperature Stability: +/- 0.05 C style, report as max difference <= 0.1 C
HeatUp/CoolDown: < 15 min each direction
PCC accuracy: +/- 2 C up to 80 C
PCC cooldown: < 2.0 min from 50 C to 40 C
PCC drift: +/- 0.2 C/min
PCC noise: <= 0.05 C
```

Open check:

```text
Criteria should be re-linked to exact TD tables and Definitions sheet cells for
each report template before automatic generation.
```

## Generation Pattern For Future FOQs

When another module FOQ TD is supplied, update this knowledge base using the
same shape:

```text
1. TD title, revision, affected instruments.
2. Test order and variant matrix.
3. Hardware/configuration prerequisites.
4. For each test:
   TD intent
   Chinese practical meaning
   sequence injection name
   instrument method name
   processing method/IRC role
   method command groups
   evidence emitted: RetTimes, audit properties, raw channels
   report formulas/workbook rules
   DB fields affected
   generation notes and non-guessable decisions
5. Acceptance criteria and source tables.
6. Open knowledge items.
```

## Why This Matters For Generation

A user request such as:

```text
Generate a VHTCC temperature accuracy test at 40 C.
```

must be expanded through TD knowledge:

```text
Device family: VX-C10-A, variant VH-C10-A
Relevant test: Temperature Accuracy
Required hardware: external upper/lower thermometer channels
Method logic: CC setpoint + external stability state machine
Evidence: RetTime for the stable 40 C point, raw external channels
Report logic: average external channels over RetTime window, choose max deviation
Open design decision: approach/baseline temperature if not reusing full ladder
```

This is the level of understanding needed before creating method script Excel,
report formula sheet, sequence rows, or a CMBX package.
