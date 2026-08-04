# CM Instrument Command Knowledge Base

This document is the working knowledge base for Chromeleon instrument-method
commands. It focuses on the method-script side, not report formulas.

中文目的：把 CM instrument method 里可执行的命令、设备树、变量、触发器和
报告证据之间的关系整理出来，作为以后生成 instrument method 的基础。

## Source Status

Current evidence sources:

```text
User screenshot:
  Instrument Setup tree:
    ColumnOven
    PumpModule
    SamplerModule
    Thermometer
    UV
    Variables
    System
    End

Local Chromeleon installation:
  C:\Program Files (x86)\Thermo\Chromeleon\bin\CM7Help_EN.CHM
  C:\Program Files (x86)\Thermo\Chromeleon\bin\InstrumentConfiguration_EN.chm
  C:\Program Files (x86)\Thermo\Chromeleon\bin\ControlList.xml
  C:\Program Files (x86)\Thermo\Chromeleon\bin\FOQVTCC.GEN
  C:\Program Files (x86)\Thermo\Chromeleon\bin\TCC100.CDD
  C:\Program Files (x86)\Thermo\Chromeleon\bin\UM3_TCC.CDD

Decoded CMBX methods:
  knowledge_base/tcc_reverse_probe/VH/6000001/*_embedded_method_flow.txt
  knowledge_base/tcc_reverse_probe/VC/3000004/*_embedded_method_flow.txt
  knowledge_base/tcc_reverse_probe/VA/0000003/*_embedded_method_flow.txt

Existing project notes:
  cmbx_data_explorer/docs/CM_METHOD_COMMAND_KNOWLEDGE_BASE.md
  cmbx_data_explorer/docs/CM_INSTRUMENT_CONFIGURATION_KNOWLEDGE_BASE.md
  cmbx_data_explorer/docs/TCC_CM_METHOD_SCRIPT_DEPENDENCY_MODEL.md
```

Boundary:

```text
已确认：
  可以从 CMBX 中解出 CM-like method flow。
  可以识别 set/wait/trigger/log/acq/abort/message 等命令族。
  可以建立 method command -> audit/raw data -> report formula 的合同。

未确认：
  CHM help 还没有完整文本化。
  还不能保证生成二进制 .instmeth payload 后可被 CM 原生导入。
  每个设备树节点下的完整命令清单仍需要继续从 CM help / driver definition / 实测 CMBX 补齐。
```

## Mental Model

CM instrument method commands are not one flat language. They are selected from
an instrument setup tree. The visible script line depends on both:

```text
configured instrument tree
-> selected device node
-> command/property/channel under that node
-> method stage and timing
-> report/audit evidence expected later
```

截图里的框架应理解为：

| Instrument Setup Node | 中文解释 | TCC FOQ 当前映射 | 作用 |
| --- | --- | --- | --- |
| `ColumnOven` | 柱温箱/温控模块 | `ColumnComp` | TCC 主设备，包含 CC/PCC/preheater/valve/leak 等子设备 |
| `PumpModule` | 泵模块 | not used in standalone TCC FOQ | 以后扩展 HPLC 系统 FOQ 时需要 |
| `SamplerModule` | 自动进样器 | not used in standalone TCC FOQ | 以后扩展 HPLC 系统 FOQ 时需要 |
| `Thermometer` | 外部温度计 | `Thermometer`, `Thermometer1` | 外部温度传感器和环境温度通道 |
| `UV` | UV 检测器 | not used in TCC FOQ | 以后扩展 detector FOQ 时需要 |
| `Variables` | 方法变量 | `Variables.*`, `RetTimes.*`, `StabVars.*`, `TempVars.*` | 脚本状态、阈值、RetTime、触发器状态 |
| `System` | CM 系统命令 | `System.Trigger`, `System.Retention`, `System.AbortQueue` | 触发器、当前保留时间、停止队列 |
| `End` | 方法终止 | `End`, stage end | 方法阶段结束 |

## Method Stages

Decoded methods show these stage names:

```text
InstrumentSetup
Equilibration
InjectPreparation
StartRun
Run
StopRun
```

中文理解：

- `InstrumentSetup`: 方法说明和全局设置入口。
- `Equilibration`: 进样前设备状态准备，如温控、模式、变量、采集率。
- `InjectPreparation`: 真正 run 前的等待和 RetTime/trigger 初始化。
- `StartRun`: 打开采集通道，开始记录 raw data。
- `Run`: 执行测试动作、等待、触发器、记录 audit/RetTime。
- `StopRun`: 关闭采集、关闭温控、恢复安全状态。

生成方法时不能只复制 `Run` 部分。很多 `Run` 命令依赖前面阶段设置好的
变量、ReadyTempDelta、EquilibrationTime、AcqOn 通道和 trigger gate。

## Command Families

### Property Assignment

Pattern:

```text
SET <device/property> = <value>
```

Examples:

```text
SET ColumnComp.CC.TempCtrl = On
SET ColumnComp.CC.Mode = StillAir
SET ColumnComp.CC.Temperature.Nominal = Variables.GenericDouble3
SET ColumnComp.PrehtLeft.TempCtrl = On
SET ColumnComp.UpperValve.CurrentPosition = 6_1
```

中文解释：这是最常见的设备控制方式。它要求 CM 配置里确实存在该设备/属性。

Generation rule:

```text
Before emitting a SET line, validate the target symbol exists for the selected device profile.
```

### Delay

Pattern:

```text
RUN Delay <minutes>
```

Examples:

```text
RUN Delay 0.1
RUN Delay 1
RUN Delay 5
RUN Delay 60
```

中文解释：延时本身不产生测试证据，但它决定 audit 时间、raw data window 和
operator prompt 的相对位置。

### Wait

Pattern:

```text
RUN Wait <condition>
```

Examples:

```text
RUN Wait CC.TempReady
RUN Wait PrehtLeft.TempReady AND PrehtRight.TempReady
RUN Wait ColumnComp.Connected = Connected
RUN Wait Column_A.CardState=OK AND Column_B.CardState=OK AND Column_C.CardState=OK AND Column_D.CardState=OK
```

中文解释：Wait 不是普通暂停，它定义“下一步测试证据有效”的条件。

### System.Trigger

Pattern:

```text
RUN System.Trigger "<name>", <condition>, TrueTime=<seconds>, Limit=<n>, Hysteresis=<x>, AllowImmediateExecution=<Yes/No>
  commands executed when trigger fires
```

Observed roles:

| Role | 中文解释 | Example |
| --- | --- | --- |
| stability loop | 周期性检查外部温度计是否稳定 | `Gradient_1`, `Gradient_2` |
| boundary crossing | 到达温度边界时写 RetTime | preheater 45/55 C, PCC 50/40 C |
| run-end gate | 满足结束条件后结束 run | `END_RUN` |
| abort guard | 超时或异常时中止队列 | `Abort` |

Important rule:

```text
If a trigger writes a RetTime, the trigger condition is part of the report calculation contract.
```

### RetTime Logging

Pattern:

```text
SET RetTimes.RetTimeN = 0
SET RetTimes.RetTimeN = System.Retention
```

中文解释：RetTime 是 method 和 report 之间最重要的桥。报告公式里
`AUDIT.RetTimeN(...)` 读的就是这里写出的时间锚点。

Examples:

```text
TEMPERATURE_ACCURACY:
  RetTime1 -> first stable setpoint
  RetTime2 -> second stable setpoint
  RetTime3 -> 40 C stable point in VH/VC/VA accuracy ladder

PREHEATER:
  RetTime1 -> left reaches 45 C
  RetTime2 -> right reaches 45 C
  RetTime3 -> left reaches 55 C
  RetTime4 -> right reaches 55 C

TEMP_HEAT_UP_DOWN_20_50_20:
  RetTime1/3 -> heat-up start/end
  RetTime4/6 -> cool-down start/end
```

Generation rule:

```text
If reusing an existing report template, keep RetTime numbering and meaning unchanged.
If changing RetTime numbering, rewrite report formulas and DB mapping together.
```

### Acquisition On/Off

Pattern:

```text
RUN <channel>.AcqOn
RUN <channel>.AcqOff
```

Examples:

```text
RUN ColumnComp.CC_Temp.AcqOn
RUN Thermometer1.ExtTemp_UpperCC.AcqOn
RUN Thermometer1.ExtTemp_LowerCC.AcqOn
RUN ColumnComp.PCC_Temp.AcqOn
RUN ColumnComp.PrehtLeft_Temp.AcqOn
```

中文解释：报告里的 `chm.*` raw signal formula 只能读取已经采集的通道。

Generation rule:

```text
Every report FixedChannel must be covered by an AcqOn window that spans the formula time range.
```

### Log

Pattern:

```text
RUN Log <audit/property>
```

Examples:

```text
RUN Log Column_A.Description
RUN Log UpperValve.Precision
RUN Log LowerValve.Precision
RUN Log PrehtLeft.Temperature.Value
```

中文解释：Log 产生 audit evidence。Column ID、Valve、Liquid Leak 这类测试
很多结果不是 raw signal 算出来的，而是 audit property 被记录后由报告读取。

### Message and Protocol

Examples:

```text
RUN Message "Please plug the column ID adapters..."
RUN Message "QUEUE WAS ABORTED! Please check your test setup..."
RUN Protocol "***Temperature increase observed on right pre-heater...***"
```

中文解释：这些不是装饰文字。对手动测试项，Message/Protocol 是测试流程的一部分，
提示操作者插卡、加水、按 keypad 或处理异常。

### System.AbortQueue

Pattern:

```text
RUN System.AbortQueue
```

Observed use:

- unsupported device model
- column ID mismatch
- timeout / stability not reached
- preheater short-circuit condition

中文解释：很多 FOQ method 自己就有 pass/fail guard，并不是只靠 report 判断。

### CmdString

Pattern:

```text
RUN ColumnComp.CmdString Cmd="<driver command>"
```

Examples:

```text
RUN ColumnComp.CmdString Cmd="PCC.TempCtrl=0"
RUN ColumnComp.CmdString Cmd="PREH.L.PID.Kp=10000"
RUN ColumnComp.CmdString Cmd="PREH.L.PID.Ki=1200"
RUN ColumnComp.CmdString Cmd="LedBar.ForceColor=1"
```

中文解释：`CmdString` 是 driver-level escape hatch。它常用于没有直接方法符号
或需要兼容不同 TCC 型号的底层命令。生成时要谨慎，因为它比普通 SET 更依赖
driver 内部命令名。

## TCC Command Groups

### ColumnComp / ColumnOven

Core paths:

```text
ColumnComp.CC.TempCtrl
ColumnComp.CC.Temperature.Nominal
ColumnComp.CC.TempReady
ColumnComp.CC.ReadyTempDelta
ColumnComp.CC.EquilibrationTime
ColumnComp.CC.Mode
ColumnComp.CC_Temp
ColumnComp.LiquidLeakSensor
```

中文解释：TCC FOQ 里的 `ColumnOven` 在 CMBX/method 中主要表现为
`ColumnComp`。`CC` 是 column compartment controller。

### Preheater

Required paths:

```text
ColumnComp.PrehtLeft.TempCtrl
ColumnComp.PrehtRight.TempCtrl
ColumnComp.PrehtLeft.Temperature.Nominal
ColumnComp.PrehtRight.Temperature.Nominal
ColumnComp.PrehtLeft.TempReady
ColumnComp.PrehtRight.TempReady
ColumnComp.PrehtLeft_Temp
ColumnComp.PrehtRight_Temp
ColumnComp.PREH_L_HeaterTemp_Actual
ColumnComp.PREH_R_HeaterTemp_Actual
```

Key command idea:

```text
set both preheaters to 40 C
wait ready
heat left/right toward 60 C
write RetTimes at 45 C and 55 C
restore/turn off controls
```

### Valve

Confirmed direct write paths:

```text
SET ColumnComp.UpperValve.CurrentPosition = 6_1
SET ColumnComp.LowerValve.CurrentPosition = 6_1
SET ColumnComp.UpperValve.CurrentPosition = 1_2
SET ColumnComp.LowerValve.CurrentPosition = 1_2
RUN Log UpperValve.Precision
RUN Log LowerValve.Precision
```

中文解释：周期性转阀方法应优先用 `CurrentPosition` 直接属性，而不是猜
`CmdString`。但位置字符串必须来自实际阀类型/端口配置。

### Thermometer

Current TCC FOQ factory-test channels:

```text
Thermometer1.ExtTemp_UpperCC
Thermometer1.ExtTemp_LowerCC
Thermometer.Environment_Temperature
```

中文解释：这些不是默认每台 CM 都一定有的通道，通常依赖外部温度计和虚拟通道配置。

### Variables

Observed groups:

```text
Variables.GenericDouble*  -> setpoints / thresholds
Variables.GenericLong*    -> counters / page count / branch context
Variables.GenericBool*    -> trigger gates / state flags
TempVars.*                -> ambient and temporary temperature values
StabVars.*                -> external thermometer stability logic
CCCalib.*                 -> calibration point and deviation values
RetTimes.*                -> report-visible time anchors
```

中文解释：变量名不能随便改。它们连接 IF 条件、Trigger、RetTime、report 和
processing/IRC 行为。

### System

Important paths:

```text
System.Retention
System.Trigger
System.AbortQueue
```

中文解释：

- `System.Retention`: 当前 run 时间，用来写 RetTime。
- `System.Trigger`: 异步事件/边界检测/稳定性循环。
- `System.AbortQueue`: 中止当前队列。

## Generation Checklist

Before generating or editing a CM instrument method:

1. Identify the target Instrument Setup node: `ColumnOven`, `Thermometer`, `Variables`, `System`, etc.
2. Validate required symbols against the target device configuration.
3. Preserve stage context: setup, acquisition, run, cleanup.
4. Preserve RetTime semantics if reusing report formulas.
5. Preserve AcqOn windows for every report raw channel.
6. Preserve Log commands for audit-based report formulas.
7. Treat `CmdString` as driver-specific and verify before reuse.
8. Keep operator `Message` steps when TD requires manual action.
9. Add a safe cleanup path: `AcqOff`, `TempCtrl Off`, reset flags where required.

## Open Work

1. Extract searchable text from `CM7Help_EN.CHM` and `InstrumentConfiguration_EN.chm`.
2. Build a per-node command catalog for the screenshot tree:
   - `ColumnOven`
   - `PumpModule`
   - `SamplerModule`
   - `Thermometer`
   - `UV`
   - `Variables`
   - `System`
3. Link every command catalog entry to:
   - source CM help or driver evidence,
   - observed CMBX method usage,
   - required configuration symbols,
   - report/audit evidence created.
4. Convert the current method-flow knowledge into a schema that can emit:
   - CM-like method script Excel/text,
   - required configuration checklist,
   - report formula contract.
