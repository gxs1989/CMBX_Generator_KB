收到。这是针对 **温度校准 (Temperature Calibration)** 仪器方法的详细分析。该方法严格对应 FOQ TD 文档的 **第 5.2 节（Instrument Calibration）**。

---

# Vanquish 柱温箱 (VH-C10-A / VC-C10-A) 温度校准仪器方法 (Instrument Method) 详细分析

> 本文档基于提供的 Chromeleon 仪器方法脚本（用于 FOQ 温度校准测试）进行逐行分析。  
> 该方法用于在 Burn-In 之后、温度准确性测试之前，对柱温箱上下两个区域的内部温度传感器进行多点校准。  
> 适用设备：VH‑C10‑A（带后冷却）和 VC‑C10‑A（无后冷却）。

---

## 1. 文档与测试意图

| 项目 | 内容 |
|------|------|
| **方法名称** | 注释为 `IM to calibrate temperature of the VH-C10-A and VC-C10-A` |
| **对应 FOQ 文档** | 第 5.2 节 – **Instrument Calibration** (仪器校准) |
| **核心目的** | 在 8 个不同温度设定点下，使用外部校准温度传感器测量实际温度，计算与内部传感器读数的偏差（校准偏移量），并将这些校准参数写入柱温箱硬件（非易失性存储），以修正后续测试中的温度控制精度。 |
| **执行顺序** | 该方法在 **Burn-In (5.1.1)** 之后执行，是后续所有温度相关测试（准确性、精度等）的前提条件。 |

---

## 2. 全局参数设置与关键差异

与之前的“温度准确性测试”相比，本方法的全局设置针对“快速触发”和“长时稳定”做了特殊优化。

### 2.1 温度就绪参数（严格且快速）

```text
ColumnComp.CC.ReadyTempDelta   0.3 [°C]
ColumnComp.CC.EquilibrationTime   0.1 [min]
```

- **`ReadyTempDelta` = 0.3°C**：比准确性测试（1.0°C）更严格，确保只有在温度非常接近设定点时，`CC.TempReady` 才为真。
- **`EquilibrationTime` = 0.1 分钟（6 秒）**：时间极短，作用是让 `CC.TempReady` 在温度进入 ±0.3°C 窗口后**几乎立即**变为真。这是为了**精准触发后续的 Trigger**，而不会因过长的平衡时间导致稳定计时（`TrueTime`）产生额外偏差。

### 2.2 温控及后冷却单元（PCC）

```text
ColumnComp.CC.TempCtrl   On
If      ColumnComp.ModelNo="VH-C10-A"
    ColumnComp.CmdString  Cmd="PCC.TempCtrl=0"   // 关闭后冷却温控
Else
End If
ColumnComp.CC.Mode   StillAir
```

- 逻辑与准确性测试完全一致：强制开启柱温箱温控，关闭 VH 型号的后冷却单元（避免干扰），使用 **StillAir** 模式。

### 2.3 泄漏传感器与数据采集

```text
ColumnComp.LiquidLeakSensor   Off
...（所有通道 Data_Collection_Rate = 20）
```

- 泄漏传感器全程关闭（防止冷凝水误报）。
- 所有内部温度、PWM、风扇、泄漏板信号采样间隔统一设为 20 秒。

---

## 3. 校准变量重置与型号识别

### 3.1 禁用所有现有校准点

脚本首先通过将 `ColumnComp.CC.TempCalibrationPointUpper/Lower1~10` 全部设为 `Off`，清除仪器中可能存在的旧校准参数。这确保本次校准是完全全新的。

### 3.2 临时变量清零

所有 `CCCalib.CalPointU/L01~08`（记录内部温度）和 `CCCalib.CalDevU/L01~08`（记录偏差值）均被重置为 0。这些变量将在触发器触发时被赋值，最后统一写入硬件。

### 3.3 按型号设定 8 个校准温度点

| 型号 | 预置温度 (`GenericDouble0`) | 温度点 1~8 (`GenericDouble1` ~ `8`) |
| :--- | :--- | :--- |
| **VH-C10-A** | 115°C | 120, 100, 80, 60, 40, 20, 10, 5 (°C) |
| **VC-C10-A** | 80°C | 85, 70, 55, 40, 30, 20, 10, 5 (°C) |

- 对照 FOQ 文档 **表 6**，完全一致。
- **`GenericBool0`**：VH 设为 1，VC 设为 0。此变量虽在本方法中未直接使用，但会在后续的 **温度准确性测试** 中通过 IRC（智能运行控制）被读取，用于动态插入正确的准确性测试序列（参见文档第 9.2 节）。

---

## 4. 关键设计：初始温度偏移与触发器级联机制

### 4.1 初始温度偏移（强制升温触发）

```text
ColumnComp.CC.Temperature.Nominal  Variables.GenericDouble0
Wait  CC.TempReady
0.000  Start Run
```

- 在 Run 段开始前，仪器被设定到 `GenericDouble0`（VH: 115°C，VC: 80°C），即**比第一个校准温度点（VH:120°C / VC:85°C）低 5°C**，并等待内部就绪。
- **目的**：确保当 Run 段启动并设定第一个校准温度时，仪器必须执行**升温**操作。这保证了触发器的启动条件（`CC.TempReady`）在开始时为“假”，当温度爬升至设定点时变为“真”，从而精准触发第一个 Trigger。若直接设定目标温度，可能因过冲或起始就绪状态不确定导致触发器时序混乱。

### 4.2 触发器级联逻辑（自动步进）

脚本中定义了 8 个触发器（`T120/85`, `T100/70` ... `T05`）。**每个触发器在被触发并完成数据记录与偏差检查后，会立即设定下一个温度点的目标值**。

**以第一个触发器 `T120/85` 为例：**

```text
Trigger     "T120/85",
(CC.TempReady) AND (CC.Temperature.Nominal=Variables.GenericDouble1),
TrueTime=850.00,
Limit=1,
Hysteresis=0.0,
AllowImmediateExecution=No
    CCCalib.CalPointU01  CC.TempActual_Upper
    CCCalib.CalDevU01  ExtTemp_UpperCC.Signal - CC.TempActual_Upper
    ...（记录Lower、检查偏差）
    ColumnComp.CC.Temperature.Nominal  Variables.GenericDouble2   // 关键：设定下一温度
End Trigger
```

- **触发条件**：内部就绪 (`CC.TempReady`) 且当前设定温度等于第一个温度点。
- **`TrueTime=850.00`**：**稳定保持时间**。条件必须持续满足 850 秒（约 14.2 分钟），触发器才会执行内部命令。这对应了文档第 5.2 节中要求的 **“内部温度信号稳定 850 秒”**。
- **`Limit=1`**：触发器仅执行一次。
- **执行动作**：
  1. 记录当前内部传感器温度（上/下）到 `CalPointU/L01`。
  2. 计算偏差（外部温度 - 内部温度）存到 `CalDevU/L01`。
  3. 检查偏差是否在 **±4°C** 范围内（超出则中止）。
  4. **设定 `GenericDouble2`（第二温度点）**，触发下一个触发器。

这种“链式反应”使得整个 8 点校准过程完全自动化，无需在 Run 段中编写复杂的条件分支或循环。

---

## 5. 稳定保持时间（TrueTime）的差异

| 温度点编号 | 触发器名称 | 设定温度 (VH / VC) | TrueTime (秒) | 对应 FOQ 文档说明 |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `T120/85` | 120 / 85 | **850** | 高温点稳定时间 |
| 2 | `T100/70` | 100 / 70 | **850** | 高温点稳定时间 |
| 3 | `T80/55` | 80 / 55 | **850** | 高温点稳定时间 |
| 4 | `T60/40` | 60 / 40 | **850** | 高温点稳定时间 |
| 5 | **`T40/30`** | 40 / 30 | **1150** | **特殊温度点**（文档规定稳定 1150 秒） |
| 6 | `T20` | 20 | **850** | - |
| 7 | `T10` | 10 | **850** | - |
| 8 | `T05` | 5 | **850** | - |

- **关键点**：第 5 个温度点（VH 为 40°C，VC 为 30°C）使用了 **1150 秒**（约 19.2 分钟）的稳定时间，与 FOQ 文档第 5.2 节中的特殊要求严格对应。
- 第 5 个触发器的触发条件中额外增加了 `(CC.TempActual_Lower>=(Variables.GenericDouble5-0.3))`，这可能是为了确保下腔体温度同样进入窗口，增加了可靠性。

---

## 6. 偏差检查与异常中止（±4°C 规则）

每个触发器在记录完数据后，都会立即执行以下检查：

```text
If  (CCCalib.CalDevU01>4) Or (CCCalib.CalDevU01<-4) OR (CCCalib.CalDevL01>4) OR (CCCalib.CalDevL01<-4)
    ColumnComp.CC.Temperature.Nominal  25.0
    ColumnComp.CC.TempCtrl  Off
    ColumnComp.CmdString  Cmd="LedBar.ForceColor=1"
    Message "Temperature calibration error! One calibration deviation is greater than 4°C."
    System.AbortQueue
End If
```

- **偏差计算**：`偏差 = 外部温度 - 内部温度`。
- **判定标准**：若上或下任一传感器的偏差绝对值 > 4°C，则判定校准失败。这与文档第 5.2 节描述一致（“若标称温度与测量温度相差超过 4°C，则中止运行”）。
- **异常处理**：
  - 将柱温箱设定至安全温度 25°C。
  - 关闭温控。
  - 强制 LED 亮红色。
  - 弹出错误消息并**立即中止整个队列**。
  - 操作员需检查测试设置（如外部传感器连接、安装位置）后重新运行校准。

---

## 7. 智能后备逻辑（处理 5°C 和 10°C 无法达到的情况）

根据 FOQ 文档第 5.2 节，如果环境温度过高，仪器可能无法实际达到 5°C 或 10°C 的低温度点。此时，脚本提供了**优雅的后备处理**，而不是直接失败。

### 7.1 确保至少 20°C 及以上温度校准成功

```text
If  (CCCalib.CalPointU06<>0) AND (CCCalib.CalPointL06<>0)
    // 将记录点 1~6 的校准值写入硬件
Else
    // 如果 20°C (第六点) 未触发，则中止整个校准
    Message "Temperature calibration error! ... at 20°C or higher."
    System.AbortQueue
End If
```

- 脚本首先检查 `CalPointU06` 和 `CalPointL06`（对应 20°C 设定点）是否不为 0（即该触发器已被执行）。
- 如果 20°C 校准点缺失，则判定为严重故障，**中止校准**。因为 20°C 是常温校准的基础，不可跳过。

### 7.2 后备赋值：将 20°C 的偏差值复制给 10°C 和 5°C

```text
If  CCCalib.CalPointU07<>0   // 如果 10°C 触发器执行了
    直接写入记录的值
Else
    // 否则，将 10°C 的标称点设为 10，但偏差直接复用 20°C 的偏差值 (CalDevU06)
    ColumnComp.CC.TempCalibrationPointUpper7  10
    ColumnComp.CC.TempCalibrationDeviationUpper7  CCCalib.CalDevU06
End If

// 5°C 同理，复用 20°C 的偏差值
```

- **设计意图**：当环境温度过高（例如 > 28.49°C）导致无法稳定达到 10°C 或 5°C 时，程序**不报错**，而是采用 20°C 时测得的偏差值作为低温度点的修正值。
- 这符合 FOQ 文档的说明：“若 10°C 和 5°C 校准点无法直接测量…则使用 20°C 温度设定点的校准参数（由于非线性关系，无法外推）。” 这是一种务实且经过工程验证的妥协策略。

---

## 8. 最终参数写入硬件

在所有 8 个温度点处理完毕后（无论是否使用了后备值），脚本执行**批量写入**操作：

```text
ColumnComp.CC.TempCalibrationPointUpper1  CCCalib.CalPointU01
ColumnComp.CC.TempCalibrationDeviationUpper1  CCCalib.CalDevU01
...（共 8 组，每组包含 Upper/Lower 的 Point 和 Deviation）
```

- 这些写入操作将校准参数实际存储到柱温箱的硬件存储器中（非易失性），在后续正常运行和所有温度测试中生效。
- 写入完成后，关闭所有数据采集通道，将柱温箱设定回 25°C 安全温度，Run 段结束（500 分钟为最大上限，实际通常提前完成）。

---

## 9. 与 FOQ 测试文档的完整对应关系

| FOQ 文档章节 | 内容描述 | 本方法实现 |
| :--- | :--- | :--- |
| **5.2** | 温度校准整体流程 | 脚本完整实现了 8 点校准逻辑 |
| 表 6 | VH: 120/100/80/60/40/20/10/5；VC: 85/70/55/40/30/20/10/5 | `GenericDouble1~8` 按型号精确匹配 |
| 5.2 | 稳定时间：高温点 850s，40°C/30°C 点 1150s | `T120`~`T60` 为 850s，`T40/30` 为 1150s |
| 5.2 | 偏差 > 4°C 时中止 | 每个触发器内嵌 ±4°C 检查与中止逻辑 |
| 5.2 | 低温度点不可达时借用 20°C 偏差值 | 最终赋值段的后备逻辑完美实现此规则 |
| 5.1.1 | Burn-In 之后执行 | 方法注释及执行顺序符合 |

---

## 10. 关键变量与状态总结（仅列核心校准变量）

| 变量名 | 类型 | 用途 |
| :--- | :--- | :--- |
| `GenericDouble0` ~ `8` | Double | 预置温度与 8 个校准温度点 |
| `GenericBool0` | Boolean | 标识型号 (1=VH, 0=VC)，供后续 IRC 使用 |
| `CCCalib.CalPointU/L01~08` | Double | 临时存储内部传感器实际温度 |
| `CCCalib.CalDevU/L01~08` | Double | 临时存储外部-内部偏差值 |
| `RetTimes.RetTime1~8` | Double | 记录每个温度点完成校准时的运行时间（可用于超时分析） |
| `ColumnComp.CC.TempCalibrationPoint/DeviationUpper/Lower1~8` | - | 写入硬件的最终校准参数 |

---

## 11. 潜在的注意事项与陷阱

1. **外部温度传感器必须稳定连接**：如果外部传感器未正确安装或接触不良，偏差值会异常并触发 ±4°C 中止。
2. **环境温度极端时依赖后备逻辑**：如果 10°C/5°C 被跳过，使用 20°C 的偏差值。操作员需确认环境温度确实过高，而非设备故障导致未达到低温。
3. **`TrueTime` 累加效应**：8 个点即使稳定很快，每个点仍需强制等待 850~1150 秒。因此整个校准过程耗时较长（约 2~3 小时），需预留充足时间。
4. **触发器`Limit=1`的重要性**：确保每个触发器只执行一次，防止在温度波动时重复写入或误设下一温度。
5. **初始温度差 5°C 的必要性**：操作员不应修改 `GenericDouble0`，否则可能导致第一触发器无法按预期触发。

---

## 12. 总结

该温度校准仪器方法是一个高度自动化的 8 点校准流程，其核心设计亮点在于：

- **触发器级联架构**：巧妙地利用触发器的内部动作来推进温度设定点，无需在 Run 主流程中编写复杂的循环或定时器。
- **差异化稳定时长**：严格遵循 FOQ 文档，区分 850 秒和 1150 秒的平衡时间。
- **鲁棒的异常处理**：既包含严格的 ±4°C 硬性中止条件，也包含针对高环境温度的优雅后备逻辑（借用 20°C 偏差值），确保设备在高环境温度下仍能完成校准，不影响生产进度。
- **完美的文档合规性**：所有温度点、稳定时间、偏差限值均与 FOQ 测试描述文档完全一致。

此校准方法是后续所有温度相关测试（准确性、精度、稳定性）的基础，其成功执行是仪器通过 FOQ 验收的关键前置条件。

---

*文档生成日期：2026-07-14*  
*基于 Chromeleon 7 仪器方法脚本分析*