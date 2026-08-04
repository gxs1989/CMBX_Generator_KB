收到。这是针对 **液体泄漏传感器测试 (Liquid Leak Sensor Test)** 仪器方法的详细分析。该方法严格对应 FOQ TD 文档的 **第 7.6 节**（以及第 5.3.1 节关于泄漏传感器状态的部分）。

---

# Vanquish 柱温箱 (VH-C10-A / VC-C10-A) 液体泄漏传感器测试仪器方法详细分析

> 本文档基于提供的 Chromeleon 仪器方法脚本进行分析。
> 该方法在 **升温/降温时间测试（第 7.5 节）** 之后执行，用于验证液体泄漏传感器的检测功能及前面板“Mute Alarm”按键的操作是否正常。
> 适用设备：VH‑C10‑A 和 VC‑C10‑A。

---

## 1. 文档与测试意图

| 项目 | 内容 |
| :--- | :--- |
| **方法名称** | 注释为 `IM to measure the performance of the Vanquish VH-C10-A or VC-C10-A Liquid Leak Sensor` |
| **对应 FOQ 文档** | **第 7.6 节** – Liquid Leak Test and Keypad Functionality Test (Part 2)<br>同时关联 **第 5.3.1 节** – Leak Sensor States（泄漏传感器在温度精度测试结束后已开启并校准） |
| **核心目的** | ① 验证液体泄漏传感器能够正确检测到人为注入的液体（水），触发泄漏报警。<br>② 验证前面板“Mute Alarm”按键能够正常关闭声光报警。<br>③ 验证泄漏传感器的校准值（`LiquidLeakCalibration-Value`）是否在允许范围内（±700，警告 ±500）。<br>④ 通过用户交互，确保操作员正确执行注水、清洁等步骤。 |
| **执行顺序** | 该方法在 **温度精度测试（第 7.2 节）** 中已开启并校准泄漏传感器，本测试直接使用已校准的传感器进行功能验证。 |

---

## 2. 全局参数设置

### 2.1 温度控制（确保恒温环境）

```text
ColumnComp.CC.Temperature.Nominal  20.0 [°C]
ColumnComp.CC.TempCtrl  On
ColumnComp.CC.Mode      StillAir
ColumnComp.CC.ReadyTempDelta   None
ColumnComp.CC.EquilibrationTime  0.5
```

- **设定 20°C**：使柱温箱保持在常温，避免温度变化引起冷凝水干扰泄漏传感器的判断。
- **`ReadyTempDelta = None`**：表示不启用温度就绪检查（本测试不关心温度是否精确稳定，只需大致恒温即可）。
- **`EquilibrationTime = 0.5`**：虽然定义了但实际无效（因 `ReadyTempDelta=None`），保留仅为语法兼容。

### 2.2 泄漏传感器状态

```text
ColumnComp.LiquidLeakSensor   On
```

- 在 Instrument Setup 阶段即**开启**泄漏传感器。此前在温度精度测试中已执行过 `LiquidLeakSensorCalibrate`，因此传感器已有正确的基准值。

### 2.3 数据采集通道

与之前脚本类似，采集柱温箱内部温度、PWM、风扇转速以及泄漏板相关信号（`LEDBoard_LeakDiff`, `A13`, `A14` 等），采样间隔 20 秒。这些数据主要用于报告中的 `LiquidLeakCalibration-Value` 评估。

---

## 3. 测试流程（用户交互驱动）

本测试高度依赖操作员的手动操作，脚本通过 `Message` 对话框和 `Wait` 条件引导操作员完成一系列动作。

### 3.1 初始状态检查

```text
0.000  Start Run
Wait  ColumnComp.CC.TempReady
If  Door=Closed AND LiquidLeak=NoLeak
    ColumnComp.CmdString  Cmd="LedBar.ForceColor=1"
    Message "Press OK, open compartment door and then inject 5 mL water to bottom of compartment."
    ColumnComp.CmdString  Cmd="LedBar.ForceColor=0"
Else
    System.AbortQueue
End If
```

- **等待 `CC.TempReady`**：确保温度已达到 20°C 附近（尽管 `ReadyTempDelta=None`，但 `CC.TempReady` 可能仍由其他机制定义，此处以实际为准）。
- **前置条件检查**：门必须关闭且当前无泄漏（`LiquidLeak=NoLeak`）。如果条件不满足，直接中止队列，防止在异常状态下继续测试。
- **LED 指示灯**：强制 LED 亮红色以引起操作员注意，弹出消息框指示操作员**开门并注入 5 mL 去离子水**到腔体底部（对应文档第 4.1.5 节要求）。
- 操作员点击“OK”后，LED 恢复默认颜色。

### 3.2 等待泄漏检测（带超时）

```text
Wait  LiquidLeak=Leak,
Continue,
Timeout=2.00
Delay  1
Log  LiquidLeak
Delay  1
```

- **`Wait` 条件**：等待泄漏传感器状态变为 `Leak`（检测到液体）。
- **`Continue` 选项**：即使超时也不中止队列，而是继续执行后续指令。
- **`Timeout=2.00`**：**2 分钟超时**。如果 2 分钟内未检测到泄漏，脚本仍会继续（但可能因未检测到泄漏而导致后续评估失败）。操作员应在 2 分钟内完成注水操作。
- 记录当前泄漏状态（`Log LiquidLeak`）用于审计。

### 3.3 确认“Mute Alarm”按键操作

```text
ColumnComp.CmdString  Cmd="LedBar.ForceColor=1"
Message "Confirm the leak alarm by pressing 'MUTE ALARM' on the instruments keypad!"
ColumnComp.CmdString  Cmd="LedBar.ForceColor=0"
Wait  ColumnComp.Alarm=NoAlarm
If  ColumnComp.Alarm=NoAlarm
    ColumnComp.LiquidLeakSensor  Off
    Delay  1
Else
    System.AbortQueue
End If
```

- 当检测到泄漏后，仪器会发出声光报警。此时脚本弹出消息，要求操作员**按下前面板的“MUTE ALARM”按钮**。
- **`Wait ColumnComp.Alarm=NoAlarm`**：等待报警状态清除（即按键被按下且报警解除）。此等待**没有超时**，意味着如果操作员不按键，队列将永远等待。这确保了操作员必须执行此步骤。
- **条件判断**：如果成功清除报警（`Alarm=NoAlarm`），则关闭泄漏传感器（避免持续报警），并继续。如果仍然报警（理论上不可能，因为 Wait 会一直等待），则中止队列。

### 3.4 清洁与清理

```text
ColumnComp.CmdString  Cmd="LedBar.ForceColor=1"
Message "With a cloth or tissue, thoroughly absorb all liquid that has collected under the leak sensor and in compartment. Close door again."
Delay  5
Message "Please confirm that all liquid under the liquid leak sensor has been removed!"
ColumnComp.CmdString  Cmd="LedBar.ForceColor=0"
Delay  5
Variables.GenericBool1  1   // Enables Trigger "END_RUN"
Delay  1
```

- 弹出消息指导操作员**用布或纸巾彻底吸干泄漏托盘、传感器下方和腔体底部的水**，然后关闭门。
- 等待 5 秒后，弹出确认消息，要求操作员确认液体已清除。
- 点击确认后，**设置 `GenericBool1 = 1`**，此变量用于激活结束触发器。
- 最后延迟 1 秒，然后运行结束。

### 3.5 结束触发器 `END_RUN`

```text
Trigger     "END_RUN",
Variables.GenericBool1=1 AND System.Retention>0.01,
TrueTime=10,
Limit=1,
Hysteresis=0,
AllowImmediateExecution=No
    // 停止所有数据采集
    ColumnComp.CC_Temp.AcqOff  ...
End Trigger
```

- **触发条件**：`GenericBool1=1`（用户已确认清洁完成）且运行时间大于 0.01 分钟（确保 Run 已启动）。
- **`TrueTime=10`**：条件必须持续 10 秒才触发，防止误触发。
- **执行动作**：停止所有数据采集通道，结束 Run 段。

---

## 4. Run 段时长与超时设计

```text
0.000  Run  Duration = 120.000 [min]
```

- Run 段总时长为 120 分钟，但注释说明：*“运行时间 120 分钟是为了给确认消息框足够时间；触发器 END_RUN 应更早停止样品。”*
- 实际上，在用户完成所有操作后，`END_RUN` 触发器会在几分钟内触发并停止采集，因此 120 分钟只是上限，防止队列无限期运行。

**关键点**：`Wait LiquidLeak=Leak` 的超时仅有 2 分钟，如果操作员未及时注水，脚本会继续执行并弹出“Mute Alarm”消息，但此时并未发生报警，导致后续 `Wait Alarm=NoAlarm` 永远无法满足（因为报警从未触发），队列将卡死。因此，操作员必须在 **2 分钟内完成注水**，否则测试将陷入死锁，只能手动中止。

---

## 5. 与 FOQ 测试文档的对应关系

| FOQ 文档章节 | 内容描述 | 本方法实现 |
| :--- | :--- | :--- |
| **7.6** | 液体泄漏测试与键盘功能测试（第 2 部分） | 完整实现了泄漏检测和“Mute Alarm”按键验证 |
| **4.1.5** | 使用去离子水（>18 MΩ·cm，TOC <3 ppb）和纸巾 | 消息中明确指示注入 5 mL 水，并用布/纸巾吸收 |
| **7.6 a)** | 泄漏测试通过条件：检测到泄漏且校准值在允许范围内 | 报告页评估 `LiquidLeakCalibration-Value` 是否满足 ±700（警告 ±500） |
| **7.6 b)** | 键盘功能：“Mute Alarm”按键正常工作 | `Wait Alarm=NoAlarm` 验证按键可清除报警 |
| **5.3.1** | 泄漏传感器在温度精度测试结束后已开启 | 本测试开始前传感器已处于 `On` 状态（由前序步骤保证） |
| 表 4 | 泄漏传感器验收标准：校准值 ±700（警告 ±500） | 报告脚本将评估此值，本方法仅提供数据 |

---

## 6. 关键变量与状态总结

| 变量名 | 类型 | 用途 |
| :--- | :--- | :--- |
| `GenericBool1` | Boolean | 用户确认清洁完成后置 1，触发 `END_RUN` 触发器 |
| `ColumnComp.LiquidLeakSensor` | On/Off | 测试开始时开启，检测到泄漏且按键清除后关闭 |
| `ColumnComp.Alarm` | Enum | 报警状态（`NoAlarm` / `Alarm`），用于验证按键功能 |
| `LiquidLeak` | Enum | 泄漏传感器状态（`NoLeak` / `Leak`），用于检测注水是否成功 |
| `LEDBoard_LeakDiff` 等 | Double | 泄漏板原始信号，用于计算校准值 |

---

## 7. 注意事项与潜在陷阱

1. **超时风险**：`Wait LiquidLeak=Leak` 仅有 **2 分钟超时**。操作员必须在 2 分钟内完成开门、注水、关门（或至少让水接触传感器）。否则脚本会继续执行，但后续 `Wait Alarm=NoAlarm` 将永远等待（因报警未触发），导致队列卡死。因此操作员应提前准备好水和工具，确保快速操作。

2. **“Mute Alarm”按键必须按下**：`Wait Alarm=NoAlarm` 没有超时，强制操作员必须按键才能继续。这确保了按键功能被实际验证。

3. **清洁确认的可靠性**：脚本依赖操作员主观确认“液体已清除”，但没有再次检测泄漏状态来验证清洁是否彻底。这可能导致残留液体影响后续测试或造成腐蚀，但文档未要求自动验证，仅要求操作员执行清洁（文档 7.6 最后提到“吸收所有液体”）。

4. **门状态检查**：初始检查要求 `Door=Closed`，但注入水时必须开门，因此操作员需在消息出现后手动开门。脚本未在注水后检查门是否关闭，但清洁后消息要求“关门”。若门未关，不影响泄漏检测（因为传感器在腔体底部），但可能影响后续温控，不过本测试不关心温度。

5. **数据采集停止时机**：`END_RUN` 触发器在清洁确认后 10 秒触发，此时泄漏传感器已被关闭（在按键清除后执行了 `Off`）。如果操作员在清洁后重新关门，但泄漏传感器仍处于关闭状态，不会影响已记录的数据（校准值已在报警时刻采集）。

6. **强制 LED 颜色**：脚本多次使用 `LedBar.ForceColor=1`（红色）吸引操作员注意，并在消息显示后恢复默认。这有助于在嘈杂环境中引导操作员。

---

## 8. 总结

该仪器方法是一个**高度依赖用户交互的验证测试**，通过消息框引导操作员执行一系列手动步骤，同时自动记录泄漏传感器状态和报警清除操作：

- **泄漏检测**：通过注入 5 mL 水触发传感器，验证其灵敏度。
- **按键验证**：通过等待报警清除，确认“Mute Alarm”按钮功能正常。
- **清理指导**：确保操作员完成清洁，为后续测试（或设备出厂）做好准备。
- **超时与容错**：注水步骤有 2 分钟超时（但后续无超时等待可能卡死），需操作员快速响应。

该测试是 FOQ 流程中唯一需要大量手动干预的环节，也是验证仪器安全功能（泄漏报警）的关键步骤。成功执行后，报告中的 `LiquidLeakCalibration-Value` 将最终决定该子测试是否通过。

---

*文档生成日期：2026-07-14*
*基于 Chromeleon 7 仪器方法脚本分析*