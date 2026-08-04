收到。这是针对 **阀性能与键盘功能测试（第一部分）** 仪器方法的详细分析。该方法严格对应 FOQ TD 文档的 **第 6.3 节**。

---

# Vanquish 柱温箱 (VX‑C10‑A) 阀性能与键盘功能测试（第一部分）仪器方法详细分析

> 本文档基于提供的 Chromeleon 仪器方法脚本进行分析。  
> 该方法在 **预加热器连接端口测试（第 6.2 节）** 之后、**Burn‑In（第 5.1.1 节）** 之前执行，属于 FOQ 流程早期阶段。  
> 适用设备：VH‑C10‑A 和 VC‑C10‑A（均配备上下两个柱切换阀）。

---

## 1. 文档与测试意图

| 项目 | 内容 |
| :--- | :--- |
| **方法名称** | 注释为 `IM to measure the valve performance of the Vanquish TCC` |
| **对应 FOQ 文档** | **第 6.3 节** – Valve Test and Keypad Functionality Test (Part 1) |
| **核心目的** | ① **阀切换精度**：验证上/下柱切换阀（CSV）在 6_1 ↔ 1_2 位置之间的切换精度（偏差 ≤ ±100 索引）。<br>② **键盘功能（部分）**：在断开与 Chromeleon 的连接后，测试前面板“Fast Cool”、“Upper Valve”、“Lower Valve”三个按键的硬件功能及 LED 指示灯是否正常响应。<br>③ **早期故障排查**：在 Burn‑In 之前尽早发现电子通信或阀驱动问题，避免浪费后续测试时间。 |
| **执行顺序** | 在 Burn‑In 和温度校准之前执行（文档表 2 中标记为 (A) 类测试）。 |

---

## 2. 全局参数设置

### 2.1 温度控制（仅维持基础状态）

```text
ColumnComp.CC.ReadyTempDelta   1.0 [°C]
ColumnComp.CC.EquilibrationTime   0.5
ColumnComp.CC.TempCtrl   On
ColumnComp.CC.Mode       StillAir
```

- 温度容差设定为 1.0°C，但本测试不涉及温度变化，仅需维持温控开启和静风模式。
- `EquilibrationTime` 定义为 0.5 分钟，但并未使用 `Wait CC.TempReady`，因此实际上不等待温度就绪。

### 2.2 初始阀位置设定（预定位）

```text
-0.100  ColumnComp.UpperValve.CurrentPosition  6_1
        Delay  0.2
        ColumnComp.LowerValve.CurrentPosition  6_1
        Delay  0.1
-0.020  Log  UpperValve.Precision
        Log  LowerValve.Precision
```

- 在 Run 段开始前，将上下阀初始位置统一设为 **6_1**（对应文档中的“从位置 6_1 切换到 1_2”）。
- 每次阀位置切换后添加短暂延迟（0.1~0.2 分钟），确保硬件动作完成。
- 在 -0.020 分钟（Run 开始前 0.02 分钟）记录初始位置的精度值。此时阀尚未切换，精度值应反映上次操作的偏差（但作为初始基线）。

### 2.3 数据采集

```text
0.000  Run  Duration = 1.000 [min]
       ColumnComp.CC_Temp.AcqOn
```

- Run 段仅持续 1 分钟，非常短。仅开启 `CC_Temp` 通道（可能为了满足 Chromeleon 对活动通道的需求），其他通道均未开启。

---

## 3. 阀切换精度测试（顺序执行）

### 3.1 第一次切换：6_1 → 1_2

```text
0.050  ColumnComp.UpperValve.CurrentPosition  1_2
       ColumnComp.LowerValve.CurrentPosition  1_2
       Delay  0.1
0.100  Log  UpperValve.Precision
       Log  LowerValve.Precision
```

- 在 0.050 分钟同时将上下阀切换到 **1_2** 位置。
- 延迟 0.1 分钟（6 秒）后，在 0.100 分钟记录此时的精度值。
- **精度定义**：`UpperValve.Precision` 和 `LowerValve.Precision` 是驱动程序提供的属性，表示最近一次阀驱动位置与目标位置的偏差（单位：索引）。文档第 6.3 节要求偏差 ≤ ±100 索引。

### 3.2 第二次切换：1_2 → 6_1

```text
0.120  ColumnComp.UpperValve.CurrentPosition  6_1
       Delay  0.2
       ColumnComp.LowerValve.CurrentPosition  6_1
       Delay  0.1
0.200  Log  UpperValve.Precision
       Log  LowerValve.Precision
```

- 在 0.120 分钟设定上阀回 6_1，延迟 0.2 分钟（12 秒）后才设定下阀回 6_1（上下阀切换有时间差，可能为了错开电流冲击或观察独立动作）。
- 分别在 0.200 分钟记录第二次精度值。

**评估逻辑**：报告脚本将检查两次记录的 `Precision` 值是否均在 ±100 范围内。若超出，则判定阀测试失败。

---

## 4. 键盘功能测试（用户交互与断开连接）

### 4.1 断开连接前的准备

```text
0.200  Message  "By pressing 'OK', the device will be disconnected automatically in order to check the keypad functionality. Please click 'OK' and press each button for 'FAST COOL' and 'Upper/Lower Valve' once within 30 seconds! Check that the LEDs work as expected!"
0.210  ColumnComp.CC_Temp.AcqOff
0.300  ColumnComp.Disconnect
```

- 在 0.200 分钟弹出消息框，指导操作员即将断开设备连接，并要求在断开后 **30 秒内** 依次按下三个按键：`FAST COOL`、`Upper Valve`、`Lower Valve`，并观察 LED 是否按预期亮起。
- 0.210 分钟关闭温度数据采集（可能为了释放资源）。
- 0.300 分钟执行 `ColumnComp.Disconnect`，断开与 Chromeleon 的通信。此时设备处于“离线”状态，前面板按键将直接控制硬件（而不会通过软件）。

### 4.2 重新连接与状态恢复

```text
0.800  ColumnComp.Connect
       Wait  ColumnComp.Connected=Connected
0.900  ColumnComp.FastCoolActive  Off
       Delay  1
1.000  Stop Run
```

- 在 0.800 分钟重新连接设备，并等待连接成功（`Connected=Connected`）。
- 在 0.900 分钟，将 `FastCoolActive` 属性设置为 `Off`。此操作可能用于清除因按键可能引发的快速冷却状态，但更重要的是 **触发驱动程序记录按键事件**。实际上，当设备离线时按下的按键，其动作状态会在重新连接后被读取并存储到相应的属性中（例如 `FastCoolActive` 会反映最后一次按键状态）。这里将其强制置 `Off` 可能是为了后续评估能检测到按键是否被正确按下（若按键正常，则属性在按键后会有变化，而置 Off 可能是为了统一报告逻辑）。详细评估由报告脚本完成。
- 延迟 1 秒后结束 Run。

**键盘按键验证原理**：
- 当设备与 CM 断开连接时，前面板按键被按下后，硬件的状态寄存器会记录该事件（例如 `FastCoolActive` 变为 `On`，`UpperValve` 或 `LowerValve` 的位置会切换）。
- 重新连接后，驱动程序会同步硬件状态到软件属性。报告脚本可以检查这些属性是否发生了预期的变化（如 `FastCoolActive` 曾被置为 `On` 并又回到 `Off`，或阀位置被切换过），从而确认按键硬件工作正常。

---

## 5. 关键变量与状态总结

| 变量/属性 | 用途 |
| :--- | :--- |
| `UpperValve.CurrentPosition` / `LowerValve.CurrentPosition` | 设置阀的目标位置（6_1 或 1_2） |
| `UpperValve.Precision` / `LowerValve.Precision` | 记录阀实际到达位置与目标位置的偏差（索引值），由报告评估 |
| `ColumnComp.Disconnect` | 断开与 Chromeleon 的通信，使前面板按键可以独立操作 |
| `ColumnComp.Connect` | 重新建立通信，同步硬件状态 |
| `ColumnComp.Connected` | 连接状态属性，用于等待连接完成 |
| `ColumnComp.FastCoolActive` | 快速冷却功能的激活状态，在断开期间按键会改变它，重新连接后可由报告读取 |
| `ColumnComp.CC_Temp.AcqOn/Off` | 本测试仅象征性开启温度通道，满足 CM 基本要求 |

---

## 6. 与 FOQ 测试文档的对应关系

| FOQ 文档章节 | 内容描述 | 本方法实现 |
| :--- | :--- | :--- |
| **6.3** | 阀测试和键盘功能测试（第一部分） | 脚本完整实现两部分测试 |
| 6.3 第一段 | 安装假阀（无流体测试） | 文档要求，脚本中未涉及安装操作（由操作员在运行前完成） |
| 6.3 第二段 | 通过 IM 切换 CSV 从 6_1 到 1_2 并返回 | 脚本执行了两次切换（6_1→1_2→6_1）并记录精度 |
| 6.3 | 评估 `Valve.Precision` 属性，目标偏差 ≤ ±100 | 记录 `UpperValve.Precision` 和 `LowerValve.Precision` |
| 6.3 | 断开 CM 连接，测试键盘按键 | `Disconnect` 和 `Connect` 实现 |
| 6.3 | 测试“Fast Cool”、“Upper Valve”、“Lower Valve”按键 | 消息中明确指示按下这三个按钮，重新连接后属性将反映按键操作 |
| 6.3 重要提示 | 每个按钮只能按一次，否则测试失败 | 消息中明确说明“once within 30 seconds” |

---

## 7. 注意事项与潜在陷阱

1. **操作员必须在 30 秒内完成按键**：脚本在断开连接后约 0.5 分钟（0.300 → 0.800）重新连接，但操作员必须在断开后的 30 秒内按下三个键。如果超过时间，重新连接后可能无法正确捕获按键事件，导致报告评估失败。消息中明确提示“within 30 seconds”。

2. **按键顺序和次数**：消息要求按 “FAST COOL” 和 “Upper/Lower Valve” **各一次**。若按多次，可能导致阀位置多次切换，报告中的预期状态不一致，最终判定失败（文档第 6.3 节明确说明“不得按超过一次，否则总结果将失败”）。

3. **阀切换的时间间隔**：上阀和下阀的切换在不同时间点执行（上阀在 0.120，下阀在 0.120+0.2=0.320？实际上脚本写的是 `Delay 0.2` 后设置下阀，但具体时间点在 0.120 秒后延迟 0.2 分钟（12 秒），即下阀在 0.320 分钟才切换回 6_1，而此时 Run 段已经过了 0.200 分钟记录精度。注意，脚本中在 0.200 分钟已经记录了精度，但下阀切换在 0.320 分钟才发生，因此 0.200 分钟的精度记录针对的是下阀处于 1_2 位置（因为下阀在 0.120+0.2=0.320 才切换），而上阀在 0.120 已切换回 6_1，所以第二次精度记录（0.200）上阀在 6_1，下阀仍在 1_2——这导致上下阀的切换不同步。实际测试中，第二次切换是否要求上下阀同时回 6_1？文档描述“通过 IM 将上下 CSV 从位置 6_1 切换到 1_2 并返回”，可能期望同时切换。但脚本有意错开，可能是为了分别验证每个阀的独立动作。无论如何，最终报告的精度值会分别记录上下阀各次切换后的偏差，只要每个阀的精度都合格即可。

4. **重新连接后的 FastCoolActive 置 Off**：此操作可能覆盖了按键动作，但报告脚本应检查按键事件的历史记录（如审计追踪或属性变化）。如果强行置 Off，可能使报告无法判断按键是否按过。因此，报告评估很可能不依赖于 `FastCoolActive` 的当前值，而是检查硬件是否记录了按键事件（例如通过阀位置是否被按键改变，或通过特定的状态标志）。具体实现需结合报告脚本分析。

5. **温度通道仅开启 `CC_Temp`**：本测试不关心温度，仅开此通道以满足 CM 对活跃数据通道的最低要求，防止报告生成错误。

---

## 8. 总结

该仪器方法是一个**简洁高效的早期功能验证测试**，聚焦于阀驱动精度和键盘硬件按键：

- **阀切换精度测试**：通过顺序切换上下阀并在每个位置记录精度属性，快速筛查阀驱动机械和电子问题。
- **键盘功能测试**：通过断开连接、人工按键、重新连接的方式，验证三个专用按键（Fast Cool、Upper/Lower Valve）的硬件功能和 LED 指示，不依赖于软件界面的模拟。
- **人工交互**：消息框引导操作员在严格的时间窗口内完成按键操作，确保测试的有效性。

此测试在 Burn‑In 之前进行，能够早期发现硬件缺陷，避免后续温度测试中因阀问题导致时间浪费，是 FOQ 流程中重要的“门控”环节。

---

*文档生成日期：2026-07-14*
*基于 Chromeleon 7 仪器方法脚本分析*