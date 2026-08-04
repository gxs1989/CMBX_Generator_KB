收到。这是针对 **温度稳定性与后冷却单元测试 (Temperature Stability and PCC Test)** 仪器方法的详细分析。该方法严格对应 FOQ TD 文档的 **第 7.3 节（温度稳定性）** 和 **第 7.4 节（后冷却单元，仅 VH‑C10‑A）**。

---

# Vanquish 柱温箱 (VH‑C10‑A) 温度稳定性与后冷却单元测试仪器方法详细分析

> 本文档基于提供的 Chromeleon 仪器方法脚本进行分析。  
> 该方法在 **温度精度与风扇测试（第 7.2 节）** 之后执行，用于验证柱温箱在恒温 70°C 时的温度稳定性，并同时测试后冷却单元（PCC）的加热、冷却、漂移及准确性等关键性能指标。  
> **适用设备**：仅 **VH‑C10‑A**（带后冷却单元）。VC‑C10‑A 使用单独的“温度稳定性_C”脚本（无 PCC 测试）。

---

## 1. 文档与测试意图

| 项目 | 内容 |
| :--- | :--- |
| **方法名称** | 注释为 `IM to measure the temperature stability of the Vanquish VH-C10-A` |
| **对应 FOQ 文档** | **第 7.3 节** – Temperature Stability and Signal Noise（柱温箱稳定性）<br>**第 7.4 节** – Post‑Column Cooler Unit（后冷却单元，仅 VH） |
| **核心目的** | ① **柱温箱温度稳定性**：将柱温箱恒温于 70°C，使用外部温度传感器连续监测 15 分钟，评估温度波动范围。<br>② **后冷却单元性能**：在 PCC 上进行 40°C → 80°C → 40°C 的温变循环，测试其加热/冷却时间、温度漂移、准确性及信号噪声，验证 PCC 电子及控制逻辑是否正常。 |
| **执行顺序** | 该方法由 **温度精度测试（第 7.2 节）** 末尾通过 IRC（智能运行控制）自动插入执行，插入依据为 `GenericBool0` 变量的值（VH=1 插入本方法，VC=0 插入另一方法）。 |

---

## 2. 全局参数设置

### 2.1 系统识别与页数设置

```text
If      ColumnComp.ModelNo="VH-C10-A"
    Variables.GenericLong9  12
Else If     ColumnComp.ModelNo="VC-C10-A"
    Variables.GenericLong9  10
Else
    Message "Column compartment model unknown, please reinspect in production!"
    System.AbortQueue
End If
```

- **`GenericLong9`**：设定报告页数（VH=12，VC=10），与之前脚本一致。
- 虽然该脚本仅用于 VH，但保留了 VC 分支以确保兼容性（若误用于 VC 至少能生成正确页数的报告）。

### 2.2 温度就绪参数（极致严格）

```text
ColumnComp.CC.ReadyTempDelta   0.05 [°C]
ColumnComp.CC.EquilibrationTime   0.5 [min]
```

- **`ReadyTempDelta` = 0.05°C**：这是整个 FOQ 流程中最严格的内部温度容差。因为稳定性测试要求外部温度在 ±0.05°C 内波动（文档 7.3.2），内部传感器也必须达到同等稳定水平，否则无法作为可靠参照。
- **`EquilibrationTime` = 0.5 分钟**：要求连续 30 秒满足 0.05°C 窗口，`CC.TempReady` 才为真。

### 2.3 温控及后冷却单元（PCC）明确开启

```text
ColumnComp.CC.TempCtrl   On
ColumnComp.PCC.TempCtrl  On            // 显式开启后冷却温控
ColumnComp.CC.Mode       StillAir      // 柱温箱静态空气模式
```

- **关键差异**：此处明确开启 `PCC.TempCtrl`（之前脚本均关闭），因为本测试需要主动控制 PCC 温度。
- **初始 PCC 设定**：`ColumnComp.PCC.Temperature.Nominal  40.00`（在 Run 段之前设定）。

### 2.4 变量初始化与泄漏传感器

```text
Variables.GenericBool1  0
Variables.GenericBool2  0
RetTimes.RetTime1  0  ... (RetTime2~4 设为 0)
ColumnComp.LiquidLeakSensor  （未设置，默认保持之前状态，但在本测试中未开启）
```

- `GenericBool1/2` 用作触发器之间的**连锁标志**，确保降温触发器按顺序触发。
- `RetTimes.RetTime1~4` 用于记录关键温度点的时间（仅使用 2,3,4，RetTime1 未使用）。
- 泄漏传感器在本方法中未操作，保持关闭状态（由前一步骤开启并校准后，本测试中不再干预）。

### 2.5 数据采集通道（新增 PCC 通道）

与之前脚本相比，本方法新增了 PCC 相关的采集通道：
- `ColumnComp.PCC_Temp.AcqOn`
- `ColumnComp.PWM_PCC_A.AcqOn`
- `ColumnComp.PWM_PCC_B.AcqOn`

所有通道采样间隔统一为 20 秒。

---

## 3. 运行前准备（Pre-Run）

```text
-0.700  Equilibration  Duration = 0.700 [min]
        ColumnComp.CC.Temperature.Nominal  70.0
0.000   Inject Preparation
        Wait  CC.TempReady AND PCC.TempReady
0.000   Start Run
```

- 在 Equilibration 阶段将柱温箱设定为 70°C，并给予 0.7 分钟（42 秒）的平衡时间（由于已在上一步骤中预热，此处时间较短）。
- **关键等待**：`Wait CC.TempReady AND PCC.TempReady` – 必须等到**柱温箱和后冷却单元双双达到就绪状态**才启动 Run 段，确保测试开始时两者都处于稳定状态。
- PCC 初始温度在之前已设定为 40°C，此时 PCC 也应已稳定在 40°C。

---

## 4. 主运行流程（Run 段 0 ~ 60 分钟）

### 4.1 柱温箱恒温（温度稳定性测试）

- 柱温箱在 70°C 保持整个 Run 段（60 分钟）。
- **外部温度传感器**（`ExtTemp_UpperCC` / `LowerCC`）连续采集数据，用于后续报告中的稳定性评估（15 分钟区间内的最大温差）。
- **内部 CC_Temp 信号**同时采集，用于信号噪声评估（文档 7.3.2 b））。

### 4.2 后冷却单元（PCC）温度循环与触发器

PCC 温度控制与触发器设计如下表所示：

| 时间点 | 动作 | 对应评估项 |
| :--- | :--- | :--- |
| 0.000 | PCC 初始设定 40°C（已在 Run 前就绪） | – |
| 5.000 | `ColumnComp.PCC.Temperature.Nominal  80.0` | **开始加热**，测试加热速率 |
| 触发器 `T60UP` (条件触发) | 当 `PCC.Temperature.Value >= 60.0` 时触发 | 记录 `RetTime2`，设置 `GenericBool1=1`，标记已升温至 60°C（可用于计算加热时间） |
| 14.500 | 触发器 `T50Down` (条件: ≤50°C 且 GenericBool1=1) | 记录 `RetTime3`，设置 `GenericBool2=1`，标记降温至 50°C（用于冷却时间计算） |
| 触发器 `T40Down` (条件: ≤40°C 且 GenericBool2=1) | 记录 `RetTime4`，记录 PCC 温度值 | 标记降温至 40°C（用于冷却时间计算） |
| 15.000 | `ColumnComp.PCC.Temperature.Nominal  40.0` | **开始冷却**，测试冷却速率 |
| 25.000 | `ColumnComp.PCC.TempCtrl  Off` | **关闭 PCC 温控**，用于后续温度漂移评估（无控温时温度自然变化） |
| 60.000 | Run 结束 | – |

**触发器逻辑详解**：

1. **`T60UP`**（在 3.5 分钟处定义，但触发时间取决于实际温度）：
   - 条件：PCC 温度 ≥ 60°C
   - 执行：记录 `RetTime2`，置 `GenericBool1=1`
   - 该触发器的**条件没有使用 `Limit=1`？** 实际上脚本中明确写了 `Limit=1`，所以触发一次后即失效。

2. **`T50Down`**（定义在 14.5 分钟处，但触发时间取决于实际降温进度）：
   - 条件：PCC 温度 ≤ 50°C **且** `GenericBool1=1`（确保已经先升温到 60°C 以上）
   - 执行：记录 `RetTime3`，置 `GenericBool2=1`
   - 此处用 `GenericBool1` 作为连锁条件，防止在升温过程中误触（因为升温时也会经过 50°C）。

3. **`T40Down`**（紧接着定义）：
   - 条件：PCC 温度 ≤ 40°C **且** `GenericBool2=1`
   - 执行：记录 `RetTime4`，并 `Log` 当前 PCC 温度值

**这样设计确保了冷却时间（50°C → 40°C）可以精确计算**（`RetTime4 - RetTime3`），而升温时间（40°C → 60°C）可以通过 `RetTime2` 与开始加热时刻（5.000）的差值获得，虽然文档未要求升温时间，但数据可用于内部诊断。

### 4.3 PCC 温度漂移评估（关闭温控后）

在 25.000 分钟关闭 `PCC.TempCtrl` 后，PCC 温度将自然漂移（受环境及散热影响）。报告脚本将分析 **19~24 分钟区间**（即在关闭温控之前）的温度漂移（线性斜率），以及 **25 分钟之后** 的漂移情况（根据文档 7.4.3 b），但文档指定的漂移评估区间是 19~24 分钟，即还在温控开启状态下的漂移，这似乎与关闭温控矛盾。重新阅读文档 7.4.3 b：*“温度漂移评估时间为 19 分钟至 24 分钟”*，这发生在 PCC 设定为 40°C 之后（15 分钟设定），且温控尚未关闭（25 分钟关闭）。因此，漂移评估是在 **温控开启但已稳定在 40°C** 的情况下进行的，用于检验 PCC 维持设定温度的能力。脚本在 25 分钟关闭温控可能用于其他内部检查，但文档未提及，可能为额外诊断。

### 4.4 温度准确性评估（三个区间）

文档 7.4.3 c 要求评估 PCC 温度准确性，取三个区间的平均值与设定值比较：
- 0~5 分钟（40°C 设定）
- 10~15 分钟（80°C 设定？但 10~15 分钟正处于加热过程中，未稳定，因此可能实际评估的是稳定后的区间）
- 19~24 分钟（40°C 设定，且已稳定）

本脚本提供了完整的温度数据，报告脚本将根据这些区间的 PCC 实际温度值计算偏差。

---

## 5. 关键变量与状态总结

| 变量名 | 类型 | 用途 |
| :--- | :--- | :--- |
| `GenericLong9` | Long | 报告页数（VH=12, VC=10） |
| `GenericBool1` | Boolean | 标记 PCC 是否已升温至 ≥60°C，用于连锁降温触发 |
| `GenericBool2` | Boolean | 标记 PCC 是否已降温至 ≤50°C，用于连锁触发降至 40°C |
| `RetTimes.RetTime2` | Double | PCC 升温至 60°C 时的运行时间 |
| `RetTimes.RetTime3` | Double | PCC 降温至 50°C 时的运行时间 |
| `RetTimes.RetTime4` | Double | PCC 降温至 40°C 时的运行时间 |
| `ColumnComp.PCC.Temperature.Nominal` | Double | PCC 当前设定温度 |
| `ColumnComp.PCC.TempCtrl` | On/Off | 后冷却温控开关 |

---

## 6. 与 FOQ 测试文档的完整对应关系

| FOQ 文档章节 | 测试项 / 要求 | 本方法实现 |
| :--- | :--- | :--- |
| **7.3.1** | 设定柱温箱温度为 70°C | `CC.Temperature.Nominal = 70.0` |
| **7.3.2 a)** | 温度稳定性：15 个 1 分钟区间的最大温差 ≤ ±0.05°C | 外部传感器连续采集 15 分钟，由报告评估 |
| **7.3.2 b)** | 信号噪声：内部 CC_Temp 信号 1 分钟噪声 ≤ 0.05°C | 数据采集通道开启，报告脚本计算噪声 |
| **7.4.1** | 测试 PCC 电子功能 | PCC 温控开启，执行温度循环 |
| **7.4.2** | 测试描述：PCC 从 40°C → 80°C → 40°C | 5.000 min 升到 80°C，15.000 min 降回 40°C |
| **7.4.3 a)** | 冷却时间：50°C → 40°C | 触发器 `T50Down` 和 `T40Down` 记录时间 |
| **7.4.3 b)** | 温度漂移：19~24 分钟线性斜率 | 数据采集持续进行，报告脚本计算 |
| **7.4.3 c)** | 温度准确性：三个区间平均值与设定值比较 | 数据采集提供平均值计算基础 |
| **7.4.3 d)** | 信号噪声：内部 PCC_Temp 信号 1 分钟噪声 | 数据采集提供噪声计算基础 |

---

## 7. 注意事项与潜在陷阱

1. **该脚本仅适用于 VH‑C10‑A**：如误用于 VC 型号，PCC 相关命令将导致错误（因为 VC 无 PCC 硬件）。幸好 IRC 插入机制确保了这一点（VC 会插入不同的稳定性脚本）。
2. **触发器连锁条件**：`T50Down` 依赖 `GenericBool1=1`，而 `GenericBool1` 只在 `T60UP` 触发后才置 1。如果 PCC 加热异常（如无法达到 60°C），则 `T50Down` 永远不触发，后续 `T40Down` 也不触发，可能导致报告缺失关键数据，但脚本本身不会报错（因为触发条件未满足）。操作员需检查日志，确认所有触发器是否按时触发。
3. **`RetTime1` 未使用**：脚本中初始化了 `RetTime1` 但从未赋值，无影响。
4. **PCC 关闭温控后的行为**：25 分钟关闭温控后，PCC 温度会自然漂移，报告脚本可能会评估漂移，但文档未要求此时间段。若漂移过大，可能被误判为故障。实际评估应以 19~24 分钟（温控开启）为主。
5. **稳定等待**：`Wait CC.TempReady AND PCC.TempReady` 在 Run 开始前执行，确保了柱温箱 70°C 和 PCC 40°C 都已稳定，为测试提供了准确的初始条件。
6. **数据采集时长**：Run 段 60 分钟，为所有评估提供了充足的时间窗口（包括关闭温控后的观察）。

---

## 8. 总结

该仪器方法是一个**复合型测试脚本**，同时实现了柱温箱的温度稳定性验证和 PCC 功能验证，设计精巧：

- **柱温箱部分**：通过严格的 0.05°C 就绪阈值和连续 15 分钟的外部数据采集，精确评估腔体温度波动。
- **PCC 部分**：利用三个连锁触发器自动记录关键温度转折点的时间，实现了冷却时间的自动化计算，同时通过全程数据采集支持温度漂移、准确性和噪声的评估。
- **时序优化**：将温度循环与稳定性测试并行执行（柱温箱恒温 70°C 的同时，PCC 进行温度变化），节省了整体 FOQ 运行时间。
- **可靠性设计**：连锁条件防止触发器在错误方向触发，`Limit=1` 确保一次性记录。

该脚本的成功执行，为 VH‑C10‑A 型号的温度控制品质和 PCC 硬件可靠性提供了全面的证据，是其 FOQ 放行测试中不可或缺的一环。

---

*文档生成日期：2026-07-14*  
*基于 Chromeleon 7 仪器方法脚本分析*