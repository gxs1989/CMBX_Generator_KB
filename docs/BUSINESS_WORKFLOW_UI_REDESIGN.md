# CMBX Data Explorer 业务流程与 UI 重构说明

> 文档状态：已确认业务基线 0.3  
> 建立日期：2026-07-27  
> 代码基线：V1.4 / `fee6634`  
> 实施状态：五中心信息架构已接入；业务中心 1 原生流程 V1、业务中心 2 Read & Analyze 原生 V1 已实现，其余中心按本文件逐步迁移

## 1. 文档目的

本文件是后续 UI 和内部功能重排的唯一业务依据。讨论阶段先确定用户实际如何完成工作，再将流程映射到界面和模块；文档确认前不实施大规模 UI 改造。

更新规则：

1. 已由用户确认的内容进入“已确认流程”。
2. 尚未确定的方案进入“待讨论事项”，不得提前固化到代码。
3. 每项 UI 功能必须能追溯到一个业务步骤。
4. 每项内部计算必须说明输入、输出、证据来源和失败状态。
5. 文档形成可验收版本后，再拆分为代码任务。

## 2. 产品角色边界

| 参与者 | 主要职责 | 不承担的职责 |
|---|---|---|
| 用户 | 提出测试意图、选择业务对象、审核方法和报告 | 不需要理解 CMBX 二进制结构 |
| Web AI | 根据 SPEC、方法 KB 和报告 KB 生成 Method MD / Report MD | 不直接写 CMBX 二进制 |
| CMBX Data Explorer | 读取 CMBX、确定性编译 MD、预检、预览、计算、导出和上传 | 不在本地重新实现通用自然语言 Agent |
| Chromeleon | 执行 instrument method，产生真实 injection、raw channel 和 audit 数据 | 不作为唯一的报告计算路径 |
| External Report Engine | 在 CM 外读取一个或多个 CMBX，并按统一 Report MD 计算和预览结果 | 第一阶段不替代完整色谱积分工作站 |
| KB / SPEC | 保存已验证的命令、公式、格式、配置和生成约束 | 不把未验证推测声明为可运行事实 |

## 3. 当前已具备的基础能力

| 能力 | 当前状态 |
|---|---|
| CMBX 结构、sequence、injection、channel、audit 读取 | 可用 |
| Instrument Method 解码与 CM 风格渲染 | 可用 |
| Method MD 预检、预览及 standalone method CMBX 编译 | 可用 |
| CM 7.2 standalone method 兼容输出 | 已验证 |
| Report Template、Direct CM Formula、FormulaOne cell-to-cell 读取 | 可用 |
| Report MD 到 report-template CMBX | 已建立第一版 |
| FOQ DB mapping、计算、导出和 SQL 上传 | 可用 |
| External Report Engine | 第一版可用，仍需围绕真实业务完善 |
| Processing Method / 高级积分 | 尚未完全解开 |
| 完整 HPLC 峰积分、手动积分、组分定量 | 后续阶段 |

## 4. 已确认的端到端业务主线

### 4.1 方法设计与执行

```text
测试需求
-> Web AI 读取 Method SPEC + 原始方法脚本 KB + 方法理解 KB
-> 生成结构化 Method MD
-> 本地 Method Script Generator 预检
-> CM 风格预览和问题定位
-> 编译为目标 CM 版本的 method CMBX
-> 导入 Chromeleon
-> 配置检查并运行
-> 得到含 raw channel、audit、RetTime 和 injection 的运行 CMBX
```

本地程序的关键职责是确定性转换和验证，不擅自猜测测试逻辑。

### 4.2 报告设计的两条路径

**路径 A：Chromeleon 原生 Report Template**

```text
Method MD + Report SPEC + Report KB
-> Web AI 生成 Report MD
-> 本地预检和布局预览
-> 编译为 report-template CMBX
-> 导入 Chromeleon 使用
```

**路径 B：External Report Engine**

```text
统一 Report MD
-> 加载一个或多个运行 CMBX
-> compatibility / preflight
-> 计算 CM formula、cell-to-cell 公式和外部扩展表
-> 预览
-> 导出报告或结构化结果
```

统一 Report SPEC 描述业务报告；不同执行后端负责检查自身能否实现，不要求用户维护两种报告语言。

### 4.3 FOQ 数据库流程

```text
选择 sequence
-> 从 AUDIT.ColumnComp.ModelNo 确认设备
-> 选择正确 report template / DB mapping
-> 计算 DB fields
-> 预览字段、精度、类型和来源 trace
-> 每个 sequence 输出一份 DB 数据
-> 批量上传 SQL Server
```

DB 是报告计算的消费端，不反向主导 method command 和 report formula 的设计。

### 4.4 知识维护流程

```text
FOQ TD / CM Help / 真实 CMBX / 人工验证
-> 构建或更新 KB
-> 更新 KB Index
-> 更新 Online GPT 最小文件包
-> 用真实 MD/CMBX 回归验证
```

## 5. UI 重构原则

1. UI 按业务任务组织，不按解析器或代码模块组织。
2. 用户进入一个工作区后，只看到完成当前任务所需的输入、步骤、状态和输出。
3. 大型工具可从主界面按钮打开独立窗口，避免所有能力挤在同一组标签页。
4. 每个长任务必须显示当前阶段、进度、日志和失败原因。
5. “预览”和“生成/上传”必须分开；生成前必须可审核。
6. 设备、sequence、injection、method、report 的上下文只在确有业务依赖时共享。
7. 不再保留没有明确业务入口、重复或仅供开发调试的 UI。

### 5.1 视觉与交互基调：现代、安静、非工业软件

新 UI 不延续传统工业软件“菜单 + 密集标签页 + 大表格 + 常驻日志”的视觉结构。底层能力可以复杂，但默认界面必须简单、清晰并具有明确的阅读顺序。

核心约束：

- 首页只展示三条用户路径：`设计与适配`、`读取与分析`、`验证与质量`。
- 每个页面只保留一个主要操作，主按钮在视觉上唯一突出。
- 使用步骤导航、任务卡片、摘要和渐进式展开，不在首屏平铺全部功能。
- 默认展示结论和下一步；formula、XML、DB field、audit 明细和日志进入 Evidence/Advanced 区域。
- 大表格仅用于确实需要批量比较的场景；普通选择使用搜索、筛选、分组列表或主从详情布局。
- 状态使用文字和克制的颜色共同表达，不依赖大片红绿背景。
- 避免多层工具栏、连续按钮带、嵌套卡片、过多边框和高密度表单。
- 保持稳定的页面骨架：页面标题、简短说明、步骤/状态、主要内容、底部操作。
- 长任务在页面内显示轻量状态和可展开日志，不弹出 CMD，不阻塞整个程序。
- Advanced Tools 与开发诊断默认隐藏，不影响普通业务流程。

推荐的信息层级：

```text
第一层：我现在要完成什么
第二层：需要提供什么、当前进行到哪里
第三层：结果、问题和下一步
第四层：证据、公式、日志和调试信息（按需展开）
```

视觉上应更接近现代数据工作台和引导式桌面应用，而不是 Chromeleon、数据库管理器或传统仪器控制软件的复制品。

### 5.2 UI 交付策略：功能先通，但不做一次性旧界面

UI 分两阶段交付，但两阶段使用同一套信息架构和页面骨架：

| 阶段 | 优先目标 | 必须具备的设计质量 |
|---|---|---|
| Phase A：Functional Shell | 打通导航、输入、预检、执行、预览和历史 | 统一间距/字体/颜色、清楚的主次操作、合理空状态、非阻塞任务反馈、没有旧式标签页堆叠 |
| Phase B：Visual Refinement | 优化细节、密度、响应式布局和数据可视化 | 统一图标、组件状态、动效、可访问性、图表主题、完整视觉验收 |

第一阶段禁止使用“先把所有按钮和表格堆出来，以后再整理”的方式。功能开发必须落入预先定义的页面组件：

- App Shell：左侧精简导航或首页任务入口。
- Workflow Header：标题、说明、当前步骤和状态。
- Input Panel：只显示本步必要输入。
- Result Workspace：摘要优先，详情按需展开。
- Action Bar：Back、Continue/Run、Save/Export，位置固定。
- Task Status：页面内进度、取消、失败原因和可展开日志。

当前程序使用 Tkinter/ttk。短期可以继续复用业务逻辑，但新 UI 必须使用集中式 theme、design tokens 和可复用组件，禁止在各页面单独硬编码颜色、字体和控件尺寸。正式视觉重构前制作一个代表性页面原型，同时评估：

1. 继续使用 themed ttk 是否能达到目标布局和数据交互质量。
2. 若无法满足现代导航、复杂主从布局、图表交互和高 DPI 要求，再将新 App Shell 迁移到 PySide6/Qt；CMBX 解析、公式求值和数据库服务保持不变。

框架选择以原型验证为准，不为了“现代感”提前重写全部后端，也不因保留 Tkinter 而接受古老的交互结构。

### 5.3 迁移策略：新旧 UI 双轨运行

业务 UI 使用独立启动器，经典 Explorer 继续保留：

- `启动CMBX工作台.bat`：进入新的业务首页和指引式流程。
- `启动CMBX数据浏览器.bat`：进入现有完整 Explorer，作为已验证功能和高级工具入口。
- 新工作台第一阶段通过独立进程打开 Classic Explorer、External Report Engine 等大型工具，避免一个窗口故障影响其他任务。
- 只有当某条业务流程完成输入、执行、预览、错误恢复和回归验收后，才从经典界面迁入新工作区。
- 迁移期间不删除经典功能；完成迁移后再决定保留为 Advanced Tools 还是移除。

## 6. 顶层业务分类提案

### Decision 001: 五个业务中心

- 状态：Confirmed / implementation in progress
- 用户目标：面对持续增长的功能，用户不需要记住标签页位置，而是从实际需求出发，由程序分步骤引导完成工作。

建议将程序划分为五个业务中心：

| 业务中心 | 用户要解决的问题 | 主要输入 | 主要输出 |
|---|---|---|---|
| 1. 方法与报告建立 | 我要设计或修改一个测试，并得到可导入 CM 的方法/报告 | 测试需求、Method MD、Report MD、SPEC/KB | method CMBX、report-template CMBX、配置检查清单 |
| 2. CMBX 浏览与诊断 | 我要打开一个 CMBX，确认其中有什么、运行了什么、采集了什么 | CMBX 文件或文件夹 | sequence/injection/channel/audit/method/report 证据、原始数据导出 |
| 3. FOQ 快速检查 | 我要快速判断一份 FOQ 测试是否完整、匹配且可用于后续结果计算 | FOQ CMBX、设备、测试知识和 mapping | 测试覆盖、设备匹配、缺失项、公式/报告契约检查 |
| 4. 质量数据与数据库 | 我要计算、比较、跟踪和上传已经运行的数据 | 一个或多个 CMBX、Report MD、FOQ DB mapping | 外部报告、DB 数据、批量上传结果、后续质量趋势 |
| 5. HPLC 应用与工作流 | 我要查找、导入、理解、适配并运行一个完整的 HPLC 应用 | AppsLab eWorkflow、应用文档、本地配置和样品计划 | 本地应用项目、兼容性报告、派生 sequence/eWorkflow、运行与结果记录 |

边界说明：

- “Report Builder”属于业务中心 1，因为它创建报告定义。
- “External Report Engine”属于业务中心 4，因为它使用报告定义处理已经运行的数据。
- FOQ DB field 的完整性检查属于业务中心 3；正式计算、导出和上传属于业务中心 4。
- CMBX 浏览器既是业务中心 2，也可作为其他流程中的统一文件/sequence/injection 选择器。
- HPLC 应用与工作流管理的是完整应用生命周期；其中的 CMBX 检查复用业务中心 2，方法/报告派生复用业务中心 1，运行结果分析复用业务中心 2 和 4。
- Processing Method、report formula、instrument command 等逆向证据默认不作为顶层入口，而在相关业务步骤中按需展开。

### 全局支撑层

以下能力不作为独立业务中心，而作为所有流程共享的工具：

| 支撑能力 | 使用位置 |
|---|---|
| KB / SPEC / Skills | 各流程中的证据、规则和生成依据 |
| Workspace | 默认路径、最近文件、扫描范围和输出位置 |
| Settings | AI、数据库、Chromeleon runtime 和版本兼容设置 |
| Help / Guided Tour | 当前步骤说明、示例和失败恢复建议 |
| Advanced Tools | 逆向分析、调试导出和尚未产品化的实验功能 |

### 指引式交互骨架

主界面不直接展示全部标签页，而先询问“今天要完成什么”：

```text
选择业务中心
-> 选择具体任务
-> 程序列出所需输入
-> 完成输入并执行预检
-> 显示当前步骤、证据和问题
-> 用户预览与确认
-> 生成、导出或上传
-> 保存任务记录和下一步建议
```

每个流程统一显示：

- 当前处于第几步。
- 本步为什么需要。
- 已获得哪些输入。
- 还缺什么，以及从哪里获得。
- 当前是否可以继续。
- 最终会产生什么输出。

### 仍需确认

- 五个业务中心的正式中文名称。
- 每个业务中心首页包含哪些具体任务。
- “FOQ 快速检查”和“质量数据与数据库”之间的交接点。
- External Report Engine 第一版放入质量数据中心的哪个具体流程。
- 哪些现有标签页迁移为步骤，哪些进入 Advanced Tools，哪些彻底删除。

## 7. 业务中心 1：方法与报告建立

### Decision 002: Web AI 设计、本地确定性编译

- 状态：Confirmed / native V1 implemented
- 用户目标：用户知道想做什么测试，但无法独立编写完整 CM method script 和 report template。用户用自然语言与网页模型完成设计，再用本地程序生成可导入 Chromeleon 的 CMBX 文件。

### 7.1 业务边界

```text
自然语言测试需求
-> 网页 AI 读取 Method/Report SPEC 与对应模块 KB
-> 用户决定本次创建 Instrument Method 或 Report Template
-> 网页 AI 生成所选分支的 Method MD 或 Report MD
-> 用户将生成的 MD 导入本地程序
-> 本地程序自动预检并显示对应预览
-> 选择目标 CM 版本
-> 生成 method CMBX 或 report-template CMBX
-> 保存完整生成历史
```

明确约束：

- 本地程序不负责通用自然语言理解，也不重新设计测试逻辑。
- MD 是网页 AI 与本地编译器之间的正式契约。
- Method 与 Report 可以来自同一个测试设计，但本地生成界面按单资产分支处理；用户不需要为了生成 Method 而同时准备 Report，反之亦然。
- 原始自然语言意图应保存在 MD 元数据或项目记录中，用于审计，但本地编译不依赖重新解释该文本。

### 7.2 已确认的四步指引流程

| 步骤 | 用户动作 | 程序职责 | 输出/状态 |
|---|---|---|---|
| 0. 选择资产 | 点击 Instrument Method 或 Report Template | 建立独立生成支线并立即进入下一步，不显示额外 Continue | Method / Report 分支 |
| 1. 准备网页 AI | 多选相关 module；可输入自然语言需求并选择是否优化 | 列出相关 SPEC/KB；提供显式 `Optimize prompt` 操作。优化结果必须回写到可见编辑框，允许人工修改和再次优化；打包时使用屏幕上已审核的文本，不允许隐藏地再次调用 AI；支持每个 MD 小于 200 KB 的小文件包 | 可审核的 `00_PROMPT.md` + SPEC/KB ZIP |
| 2. 导入与预览 | 导入网页模型生成的单个 MD | 自动预检；Method 使用 CM 的 Stage/Branch/Comment/Invalid 配色并支持双向滚动；Report 显示 sheet/cell/formula/table。错误明确要求重新生成或联系维护人 | ready / warning / blocked |
| 3. 生成 CMBX | 确认名称、输出位置；Method 额外确认目标 CM 版本 | 生成单个 standalone CMBX，计算 hash，并自动保存输入快照和 `project.json` | method CMBX 或 report-template CMBX |

设计约束：

- 页面一次只显示当前步骤，不在左侧列步骤、右侧同时暴露完整表单。
- 每步只有一个主要 Continue/Generate 操作；预检在导入后自动执行。
- 长任务必须写入页面底部 Progress log，不能让用户通过窗口无响应猜测状态。
- 新业务页面启用 Windows DPI awareness，并使用圆角任务卡和圆角操作按钮；窗口缩小时输入区保持稳定高度，数据预览通过滚动条承载宽内容。
- Method/Report 的 0-1-2-3 步骤编号使用与 Read & Analyze 一致的方形状态块：当前步骤蓝色、已完成绿色、未来步骤中性；当前页面外围和步骤提示同步高亮。
- 模块和小文件选项使用主题无关的蓝底白色勾选，不接受因 Windows/Tk 主题差异显示为叉号。
- 公共圆角按钮必须根据可用宽度自动收缩字号；受限状态标签和路径标签必须换行或提供滚动，不得把文字绘制到控件边界之外。
- Method 与 Report 的交叉契约检查保留为后续“关联两个已生成资产”的独立审核能力，不阻塞单资产生成流程。

### 7.3 后续关联审核：方法与报告的交叉契约

本节不属于当前四步单资产生成向导。它用于用户以后选择一个已生成 Method 和一个已生成 Report 时执行关联审核。

程序至少检查：

| 检查项 | 示例 | 失败级别 |
|---|---|---|
| 设备与型号 | Report 使用的设备属性是否由 Method 目标配置提供 | warning / blocked |
| Raw channel | Report 的 `FixedChannel` 是否由 Method `AcqOn` | blocked |
| Audit property | Report 的 `AUDIT.*` 是否会在运行中存在 | warning / blocked |
| RetTime | Report 使用的 `RetTimeN` 是否由 Method 赋值 | blocked |
| 自定义变量 | Report/Method 引用的变量是否已定义或导入 | blocked |
| 时间窗口 | Report 计算窗口是否落在 method 运行和采集区间内 | blocked |
| 单位和数据类型 | 温度、压力、时间、布尔值等是否一致 | warning / blocked |
| 能力边界 | 动态表、积分或未支持 FormulaOne 功能能否由当前编译器实现 | open verification / blocked |

### 7.4 生成项目与历史记录

历史记录的基本单位是一次 Method 或 Report 资产生成记录；关联审核可再把两个记录绑定为同一个测试项目。建议保存：

| 字段 | 说明 |
|---|---|
| Project ID / Name | 用户可读名称和内部唯一标识 |
| Original Intent | 用户交给网页 AI 的原始测试需求 |
| Family / Device | 模块和目标设备/配置 |
| Asset Type | Method 或 Report |
| Source MD | 本次输入文件快照，而不只是原路径 |
| SPEC / KB Version | 网页生成所依据的知识版本 |
| Target CM Version | 例如 CM 7.2 或 CM 7.3 |
| Preflight Result | 当前 MD 的结构和编译能力检查结果 |
| Cross-contract Result | 仅在以后执行关联审核时保存 |
| Configuration Checklist | 运行所需设备、channel、变量和导入项 |
| Generated Assets | 输出 CMBX 文件、hash 和路径 |
| Runtime Evidence | 实际运行 CMBX、关联 sequence/injection 和验证结果 |
| Generation Log | 编译时间、警告、错误和工具版本 |
| Validation Status | 未验证 / 可导入 / CM 已打开 / 已实际运行 |
| Notes | 用户审核意见和后续修改原因 |

历史必须支持：

- 重新打开项目。
- 查看当时实际使用的 MD，而不受源文件后来修改影响。
- 基于旧项目创建新版本。
- 比较同类资产两个版本的 MD 和生成结果。
- 从失败步骤继续，而不必重新执行全部流程。

### 7.5 当前缺口

- 需要定义以后关联 Method 与 Report 生成记录时使用的共同项目元数据字段。
- 需要确定历史记录保存目录、保留策略和迁移方式。
- 需要定义 native report CMBX 无法实现某项 Report MD 时，是阻止生成还是允许生成带警告的部分结果。
- 需要确认配置清单是否作为独立 MD/PDF 输出，还是只保存在项目历史中。
- 需要确认关联审核后是否额外提供包含两个独立 CMBX 的项目文件夹/压缩包。

### 7.6 原生 V1 实施记录（2026-07-27）

- 新业务工作台按照三条用户路径组织五个业务中心；路径不再替代业务中心。
- “方法与报告建立”使用独立原生窗口，不加载 Classic Explorer。
- 已实现 Method/Report 单资产分支、模块 KB 文件推荐、自动预检、对应预览、standalone CMBX 编译和 `project.json` 历史清单。
- Classic Explorer 仅作为明确标注的 Legacy fallback，不再据此把业务中心标为 Available。
- 运行后 CMBX 回证、项目重新打开/版本比较以及完整 report layout 像素级预览仍为后续迭代。

### 7.7 当前验收基线（2026-07-28）

Design & Adapt 的第一版业务流程暂时收口，后续开发不再改变其主路径，除非实际使用暴露阻断问题。

当前已确认：

- Step 0 点击 `Instrument Method` 或 `Report Template` 后立即进入对应分支。
- Step 1 支持多选 module，展示相关 SPEC/KB，并生成网页模型使用的 ZIP；可选小于 200 KB 的拆分包。
- 本地 Intent 仅用于可选的 AI 提示词优化，不作为 CMBX 编译依据。
- Step 2 自动预检并使用与 Classic Explorer 一致的 CM 语义配色预览；Method 支持横向和纵向滚动。
- blocked/invalid 行必须明确提示重新生成 MD，或联系 `xiaoshu.guan@thermofisher.com`。
- Step 3 生成独立 Method 或 Report Template CMBX，并保存输入快照、hash、日志和项目记录。
- 新窗口统一采用高 DPI 字体、圆角任务卡/按钮、稳定的顶部输入区和底部进度日志。

本阶段明确延后：Method/Report 配对契约审核、运行后证据回链、历史项目版本比较和 report 像素级版式复刻。

## 8. 业务中心 2：CMBX 浏览与诊断

### Decision 003: 多 CMBX 通用读取与分析工作区

- 状态：Confirmed；原生 V1 已实现
- 用户目标：自由、快速地读取和比较 CMBX 中的数据与结构，不要求数据属于 FOQ，也不默认套用 FOQ mapping、接受标准或数据库规则。

#### 8.0.1 原生 V1 验收基线（2026-07-28）

Read & Analyze 使用独立窗口和共享多 CMBX workset，不进入 Classic Explorer，也不为三个任务重复扫描 package。当前原生 V1 固定为三个引导流程：

| 流程 | 当前实现 | 失败可见性 |
|---|---|---|
| Batch raw data export | package、sequence、injection、channel 四级筛选可同时生效；支持层级多选与从 channel 名反向匹配；一个 channel 输出一个原始精度 TSV，并生成 manifest | raw payload 缺失、CM runtime 错误和单 channel 导出失败进入 manifest/log |
| Compare channel traces | 使用同一套四级组合筛选；支持多个 CMBX/injection/channel 任意多选、overlay、separate tracks、鼠标缩放、拖动平移和 reset；信号线使用增强宽度 | 无数据、channel 不兼容或 raw bridge 失败明确显示，不改变原始 CMBX |
| External integration | 对当前加载的全部 trace 使用一套共享参数：Baseline Noise Range、smoothing width、noise multiplier、minimum height/area/width 和 negative peak；可按全部 trace 的采样间隔自动适配 smoothing/minimum width；列表输出 start/apex/end、baseline endpoints、height、area、width 和 polarity；图中用红色 baseline 连接积分起止并显示端点 | 积分在线性复杂度后台任务中执行；参数命名参考 CM Help 的 Cobra Detection Parameters，但算法明确标记为 Cobra-inspired external integration，不宣称逐字节复现 CM Processing Method；原始 CMBX 保持只读 |
| Evaluate Direct CM formulas | 为缩短多 CMBX 启动时间，本业务页只扫描 report XML 中的 Direct CM `ReportFormulaObject`，不启动 FormulaOne runtime；inventory 显示公式自动解释，context 支持 package/sequence/injection/channel 四级组合筛选并位于公式表下方；支持多公式 × 多 injection batch preview | FormulaOne inventory 能力仍保留在 Report/KB 专用工具中，不进入本页；unsupported、missing-channel、missing-data 和 evaluator error 分开显示 |

V1 的 raw、plot 和 external integration 均使用原始采样时间轴；仅显示时允许降采样，导出、积分和公式计算继续使用全部原始点。当前积分是只读外部实现；读取 CM Processing Method 参数、手工调整 baseline/边界以及与 CM Cobra 的定量等价验证仍属于后续范围。

RID 已接入工作台：`OQ 2026-07-28.cmbx` 可识别 4 个 sequence、10 个 injection、6 个 Instrument Method、4 个 Processing Method 和 1 个共享 Report Template；由于其为未采集的 OQ sequence template，Read & Analyze 正确显示 0 acquired channel，而不是解析失败。RID 同时进入 Method & Report Creation 的 module/网页 KB 选择。

Direct CM inventory performance contract:

- Default to an instant `Useful formula library` built from concrete Direct CM formulas in verified report inventories and implemented by the local evaluator.
- Keep `Used by loaded reports` as an optional evidence source that preserves package/report/sheet/cell provenance.
- A library formula is "locally evaluable", not automatically compatible with every injection. `chm.*` requires one resolved channel; audit, RetTime and precondition formulas report missing/unsupported evidence during batch preview.
- Start a background inventory prefetch immediately after the shared CMBX workset is indexed.
- Show completed/total reports, percentage, formulas found, current report, and estimated remaining time on the task card and formula page.
- Reuse the in-memory inventory when the formula workflow opens; never launch a duplicate scan.
- Deduplicate Direct CM report sources by report identity without hashing payloads. FormulaOne remains outside this workflow.

Guided-step interaction contract (2026-07-29):

- A workflow stepper is an active navigation aid, not a static illustration. Its current step must follow real user actions and background-task completion.
- The current step is blue, completed steps are green, and future steps remain neutral.
- Each step binds to one concrete operation region below the heading. The active region receives a blue outline and a concise action instruction; the highlight moves when the workflow advances.
- Step changes may move keyboard focus to the newly active region, but must not start work automatically or claim completion before the underlying operation succeeds.
- `Batch raw data export` advances from scope filters -> hierarchy review/selection -> export action.
- `Chromatograms & Integration` advances from channel discovery -> load selected traces -> view/integrate results.
- `Evaluate Direct CM formulas` advances from formula discovery/selection -> injection context selection -> batch-preview results.
- The same guided-step behavior is the default for future native business workflows. A numbered row that never changes state or highlights its corresponding operation is not considered an implemented guided workflow.

Chromatogram interaction contract (2026-07-29):

- Normal left-button drag draws a visible rectangle and zooms to that range on release.
- Holding Space changes the pointer to a hand; Space + left-button drag pans the complete chromatogram view.
- Right-click restores the previous zoom/pan view. Toolbar zoom and reset operations also enter the bounded view history.
- Pointer-driven panning is redraw-throttled so high-frequency mouse events do not trigger an unbounded sequence of complete trace redraws.
- In separate-track mode, rectangle zoom changes the time range while preserving the shared vertical display contract for individual tracks.

### 8.1 业务边界

该中心负责回答：

- CMBX 中包含哪些 package、sequence、injection、channel、method、audit 和 report。
- 一个或多个 channel 的原始数据是什么样。
- 多个 CMBX 的信号、方法、audit 或 formula 结果有什么差异。
- 用户选择的 raw data、方法、audit 或报告证据如何导出。
- 原始信号如何在程序外进行非破坏性积分分析。

该中心不负责：

- FOQ 测试覆盖、设备与 DB mapping 匹配。
- FOQ 接受标准判断。
- SQL 数据库上传。
- 修改原始 CMBX 内的数据或覆盖 Chromeleon 原始结果。

### 8.2 统一的多 CMBX 工作集

所有任务首先建立一个共享工作集：

```text
添加 CMBX / 添加文件夹
-> 后台建立轻量索引
-> 显示 package -> sequence -> injection 层级
-> 用户选择当前分析范围
-> 进入具体任务
```

工作集必须支持：

| 能力 | 说明 |
|---|---|
| 多文件添加 | 一次加入多个 CMBX 或整个文件夹 |
| 范围控制 | package、sequence、injection、channel 多选 |
| 快速索引 | 首先读取 header/metadata，不立即展开所有 raw data |
| 去重和状态 | 标记重复、无法读取、缺少 raw/audit、CM 版本差异 |
| 搜索与筛选 | 按名称、日期、设备、method、channel、状态筛选 |
| 后台加载 | 读取 raw data 或大型 report 时不阻塞 UI |
| 会话保存 | 保存文件路径、选择范围、图表、积分参数和导出记录 |

#### 8.2.1 Package 类型与资产作用域

Read & Analyze 不能假设每个 CMBX 都是一个已经运行完成、只含一个 sequence 的数据包。轻量索引阶段必须区分：

| Package 类型 | 识别特征 | UI 含义 |
|---|---|---|
| Runtime data | 存在 acquired channels 和/或 audit | 可进入 raw plot、audit、公式计算和数据导出 |
| Sequence template | 有 sequence/injection/method/report，但没有 acquired channel/audit | 显示为“模板，尚无采集数据”，不是解析错误 |
| Standalone asset | 主要包含单独 Method 或 Report Template | 进入资产检查，不显示空的数据分析任务 |
| Mixed package | 同时包含多个 sequence、共享资产和运行数据 | 按资产作用域建立关系，不强制归属第一个 sequence |

资产作用域规则：

1. Injection 的 Instrument Method / Processing Method 绑定必须在其所属 sequence 的 `.cmd` 中解析；不能只读取第一个 sequence。
2. Report Template 可直接属于 sequence，也可位于 sequence 的父文件夹或 package root。父文件夹级 report 对同一文件夹内的 sequence 可见。
3. 同名且 payload hash 相同的 folder/root report 视为一个逻辑资产；保留全部物理来源用于审计，但 UI 默认只显示一次。
4. Folder/root report 必须从自己的 report payload 解码；不得用第一个 sequence payload 代替。
5. 资产继承或去重存在歧义时显示 `Review Required`，而不是静默选择。

真实回归样本 `OQ 2026-07-28.cmbx` 已验证：4 个 sequence、10 个 injection、6 个 Instrument Method、4 个 Processing Method 和 1 个逻辑共享 Report Template 均可识别；该包无 acquired channel/audit，分类为 Sequence Template。

### 8.3 六个核心任务

#### 任务 A：Raw Data 导出

```text
选择 CMBX 范围
-> 选择 injection/channel
-> 预览点数、时间范围、单位和文件大小
-> 选择导出格式
-> 批量导出
```

建议支持：TSV/CSV、原始精度、时间单位、一个 channel 一个文件或合并长表，并附带 package/sequence/injection/channel 元数据。

#### 任务 B：Channel 预览与叠加

核心交互：

- 从任意 CMBX/injection 添加多个 channel。
- 多选显示、隐藏、移除和重新排序。
- overlay、分面显示和按单位分 Y 轴。
- zoom、pan、reset、区域选择、十字光标和数值提示。
- RetTime、audit event 和用户标记可叠加到时间轴。
- 不同采样率使用原始时间轴，不因显示而修改原始数据。
- 大数据采用显示降采样，但导出和计算仍使用原始点。
- 支持图像与当前可视范围数据导出。

跨 CMBX 叠加时需要明确对齐模式：

| 对齐模式 | 用途 |
|---|---|
| Absolute retention time | 比较相同运行时间位置 |
| Injection start = 0 | 默认运行时间对齐 |
| Selected RetTime = 0 | 比较某个事件前后信号 |
| Manual offset | 用户手工校正不同运行的起点 |

#### 任务 C：信号积分

第一阶段建议定位为“外部、非破坏性积分”：

- 原始 CMBX 保持只读。
- 用户选择 channel 和时间区间。
- 支持 baseline、peak start/end、threshold、smoothing、minimum width 等参数。
- 显示峰面积、峰高、保留时间、baseline 和积分边界。
- 支持自动积分后手工调整边界/baseline。
- 保存积分方法和手工修改记录，可应用到多个 injection。
- 积分结果可导出，并可供 External Report Engine 使用。

需要明确区分：

- “读取 CM Processing Method 的积分参数”。
- “程序自己的外部积分参数”。
- “将积分结果写回 CM/CMBX”。后者当前不在第一阶段范围内。

当前第一版已实现第二项的自动积分基线：所有选中 trace 共用一套外部参数并输出峰结果列表。尚未实现手工 baseline/边界编辑，也未将 CM Processing Method 参数自动翻译为外部参数。

#### 任务 D：检查方法

建议覆盖：

- 查看 injection 实际绑定的 Instrument Method 和 Processing Method。
- CM 风格渲染 Instrument Method。
- 查看 stage、time、command、value、comment、trigger 和 required symbols。
- 多 CMBX/method 并排比较和差异高亮。
- 导出为 MD、TSV/XLSX、decoded XML 或原始对象。
- Processing Method 在未完全解码的部分明确显示能力边界。

#### 任务 E：检查 Audit

建议覆盖：

- 多 injection audit 浏览、搜索、筛选和导出。
- 按时间、device、property、command/message、RetTime 分类。
- precondition、run-time event 和错误/警告分组。
- 点击 audit 行时定位到 channel plot 的对应时间。
- 对多个 CMBX 的相同 property/event 进行并排比较。

#### 任务 F：选择并读取 Report Formula

```text
选择 CMBX/report template/sheet
-> 浏览可读 formula objects 和 FormulaOne cells
-> 选择一个或多个公式
-> 选择 injection/channel context
-> 显示依赖链和兼容性
-> 对工作集批量计算
-> 比较和导出结果
```

需要显示：

- Report template、sheet、cell/range、formula、FixedChannel、FixedComponent。
- Direct CM formula 与 FormulaOne cell-to-cell 公式的区别。
- formula -> audit/raw/RetTime/cell 的依赖 trace。
- 每个 CMBX/injection 的 evaluated value、状态和失败原因。
- 公式可以来自当前 CMBX，也可以从 Formula Finder 选择后应用到兼容 CMBX。

### 8.4 任务间联动

| 起点 | 联动动作 |
|---|---|
| Channel Plot | 将当前范围发送到 Raw Export 或 Integration |
| Audit | 将事件时间标记到 Plot |
| Method | 将 RetTime、trigger、AcqOn/Off 标记到 Plot |
| Report Formula | 打开其 FixedChannel 和计算时间窗口 |
| Integration | 将结果发送到 External Report Engine |
| 任意任务 | 将当前 package/sequence/injection 范围传给其他任务 |

### 8.5 分析历史与复现

建议保存一个轻量 Analysis Session：

- CMBX 文件路径和文件 hash。
- 当前 package/sequence/injection/channel 选择。
- plot 布局、颜色、轴和对齐方式。
- integration 参数及手工修改。
- 选中的 report formulas。
- 导出记录和错误日志。

如果源 CMBX 被移动或 hash 改变，重新打开会话时必须提示，而不是静默使用不同数据。

### 8.6 当前缺口

- 需要继续验证 external Cobra-inspired integration 与 CM Cobra 在不同信号类型上的差异，并定义手工 baseline/边界编辑能力。
- 当前 Formula Finder 默认优先显示工作集中 CMBX 自带公式；全局 KB 公式后续作为明确的第二来源接入，不能与包内证据混淆。
- 需要确定多 CMBX 的默认时间对齐方式。
- 需要确定 Analysis Session 的保存格式和默认位置。
- 需要定义超过多少数据点时启用显示降采样。
- 需要确认 Processing Method 第一阶段只读到什么深度。

## 9. 业务中心 3：FOQ 快速检查

### Decision 004: 以测试结果和通过判定为中心

- 状态：Proposed
- 用户目标：批量读取 FOQ CMBX，快速得到每个测试的必要 report cell 数据、通过/失败状态、缺失项和证据链，并对关键 channel 信号进行跨 sequence 对比。

### 9.0 核心业务痛点

Chromeleon 可以查看单个 CMBX/report，但当用户完成一批 FOQ 测试后，通常仍需要：

- 逐个打开 CMBX。
- 逐个找到 report 中的关键数值。
- 逐个确认对应 Definitions/spec。
- 逐个判断 pass/fail。
- 手工将数据抄到其他工具后才能横向比较。

FOQ 快速检查必须消除上述重复工作。目标状态是：

```text
选择一批 CMBX
-> 自动生成全部 sequence 的关键数据和 pass/fail 矩阵
-> 自动突出 fail / incomplete / outlier / spec changed
-> 用户只审核异常项
```

正常、可识别且数据完整的 CMBX 不应要求用户逐个打开或逐个确认。

### 9.1 业务边界

该中心优先回答：

1. 这是什么设备和 FOQ 测试。
2. 应使用哪个 report template、test contract 和 acceptance criteria。
3. 计算结果是什么。
4. 是否通过。
5. 如果不能判定，缺少什么。
6. 结果来自哪个 report cell、formula、RetTime、audit 或 raw channel 区间。

该中心不以 SQL 上传为目标。完成检查后，可将“已验证结果集”交给业务中心 4 进行数据库输出和质量跟踪。

### 9.2 指引式业务流程

```text
添加 FOQ CMBX / 文件夹
-> 快速识别 sequence、device、model 和测试内容
-> 为每个 sequence 确认 report template / FOQ contract
-> 完整性预检
-> 选择要检查的设备、测试或结果字段
-> 依赖驱动地批量计算必要 report cells
-> 计算 acceptance result
-> 查看结果矩阵、异常和 channel 对比
-> 人工审核
-> 导出 FOQ 检查报告或移交质量数据中心
```

批量处理规则：

- 文件夹可以直接作为检查批次加入。
- `deleted` 文件夹默认排除。
- 一个 CMBX 内的多个 sequence 分别形成结果记录。
- report template、device 和 contract 按 sequence 解析，而不是按整个文件统一假设。
- 自动识别成功的记录直接计算；只有 ambiguity、missing 或 conflict 进入人工确认队列。
- 用户确认某条规则后，可选择仅应用当前 sequence、当前批次或保存为可复用规则。

### 9.3 设备、模板和契约识别

| 项目 | 规则 |
|---|---|
| Device source of truth | 优先使用 CMBX 内 `AUDIT.ColumnComp.ModelNo` 等已验证设备属性，不根据文件名猜测 |
| Sequence identity | 保留 CMBX、sequence、injection 的原始名称和路径 |
| Report template | 按 sequence 单独识别和确认；一个 CMBX 中可能存在多个模板 |
| FOQ contract | 绑定 KB/TD 版本、report template 版本和 mapping 版本 |
| Definitions sheet | 读取模板内的 spec/limit、单位、比较方向和可能的型号分支，作为复现 CM 报告判定的重要输入 |
| Ambiguity | 自动识别不唯一时要求用户确认，不静默选择 |
| Model applicability | 不适用项显示 `Not Applicable`，不能显示为缺失或失败 |

### 9.3.1 完整 CMBX 与三层 FOQ 契约

该业务中心的输入是已经测试完成的完整 CMBX。原则上，以下运行证据都从 CMBX 自动读取：

- sequence 和 injection。
- raw channels 和采样时间轴。
- audit、precondition 和 RetTimes。
- Instrument Method / Processing Method 绑定。
- embedded report templates、sheets、Direct CM formulas 和 FormulaOne workbook。
- Definitions sheet 和模板内 lookup/spec 数据。

用户不应为了正常批量检查再次手工导出这些数据。

一键 FOQ 检查依赖三层外部/嵌入契约：

| 契约层 | 主要来源 | 回答的问题 | 不负责的内容 |
|---|---|---|---|
| Result Location Contract | `FOQResultLocations*.xls` 等 FOQ Location 文件 | 哪些 DB field / 关键结果位于哪个 report sheet/cell | 不定义底层 raw formula 如何计算 |
| Calculation Contract | CMBX 内实际绑定的 Report Template | 目标 cell 如何由 Direct CM formula、FormulaOne 和 workbook-derived rule 得到 | 不替代正式 FOQ 规范版本管理 |
| Acceptance Contract | Report Definitions sheet + FOQ TD/SPEC/KB | spec 是什么、比较符是什么、适用型号是什么、是否 pass | 不决定结果 cell 的位置 |

完整计算链应显示为：

```text
FOQ Location field
-> report sheet/cell
-> FormulaOne dependency / workbook-derived rule
-> Direct CM formula
-> CMBX RetTime / audit / precondition / raw channel
-> observed value
-> Definitions / FOQ SPEC criterion
-> Pass / Fail / other status
```

每次批量检查必须锁定并记录：

- FOQ Location 文件路径、版本和 hash。
- 每个 sequence 实际使用的 report template 名称、版本和 hash。
- Definitions sheet 的来源 cells。
- FOQ SPEC/KB 的文档编号和版本。
- evaluator 版本和当前已验证/未验证的公式能力。

如果完整 CMBX 中存在多份 report template，程序先根据 sequence/injection 绑定和覆盖度推荐候选；不能唯一确定时才要求用户确认。

### 9.4 完整性预检

开始计算前检查：

- 必要 injection 是否存在。
- 绑定的 Instrument Method / Processing Method 是否存在。
- 必要 raw channel 是否实际采集。
- 必要 audit / precondition property 是否存在。
- report formula 使用的 RetTime 是否已记录。
- report template 和目标 sheet/cell 是否匹配。
- acceptance criteria 是否有明确来源和版本。
- 运行时长是否覆盖公式窗口。
- 数据单位和类型是否满足计算要求。

预检不会把“缺失”自动判为“失败”，而是进入独立状态。

### 9.5 依赖驱动的 Report Cell 批量计算

不需要为每个 sequence 重建整份报告。程序从用户选择的结果项和 pass/fail cells 反向建立依赖图，只读取必要数据：

```text
Selected FOQ Result / Pass Cell
-> FormulaOne dependency
-> Direct CM formula / workbook-derived rule
-> RetTime / audit / precondition / raw channel window
-> cached CMBX data
```

计算要求：

- 同一个 sequence 的 raw/audit/method/report evidence 只解析一次并缓存。
- 同一公式依赖被多个 DB field 或结果引用时只计算一次。
- 多 CMBX 后台并行处理，但 UI 保持可响应。
- 显示 package、sequence、test 级别的真实进度、日志和取消操作。
- 保留 raw value、display value、number format 和 pass/fail comparison value 的区别。

“一键检查”默认计算 FOQ Location 文件中适用于当前 device 的全部关键字段及其 pass/fail 依赖，而不是要求用户逐个选择字段。用户可在高级筛选中缩小范围。

### 9.6 结果状态模型

| 状态 | 含义 |
|---|---|
| Pass | 数据完整，计算成功并满足适用 acceptance criteria |
| Fail | 数据完整，计算成功但不满足 acceptance criteria |
| Incomplete | 缺 injection、channel、audit、RetTime 或必要 cell |
| Not Applicable | 该测试/字段不适用于当前型号或配置 |
| Unverified | 有结果，但 acceptance criteria、公式或模板尚未验证 |
| Error | 文件损坏、解析异常或计算执行失败 |
| Review Required | 数据可计算，但存在模板冲突、边界值或人工复核要求 |

External、Internal 和 For information only 判据必须分别显示。Internal/For information only 不应被错误提升为外部放行结论。

### 9.7 FOQ 结果总览

建议使用“sequence 为行、测试项为列”的结果矩阵：

| Sequence | Device | Overall | Calibration | Accuracy | Stability | Precision | Heat/Cool | Open Issues |
|---|---|---|---|---|---|---|---|---|---|

交互要求：

- 点击测试状态，打开该测试的结果卡片。
- 结果卡片显示 observed value、limit、判定类型和 pass/fail。
- 可展开 report cell、formula、source channel、RetTime/window 和原始点统计。
- 可只查看 Fail、Incomplete、Unverified 或 Review Required。
- 支持跨不同 device 选择共同测试项；字段列表取适用交集，同时保留型号差异提示。

结果总览必须提供两种并列模式：

| 模式 | 主要问题 | 显示重点 |
|---|---|---|
| Status View | 哪些测试通过、失败或缺失 | Pass/Fail/Incomplete/N/A 和异常数量 |
| Data Comparison View | 不同 CMBX 的关键数值有什么差异 | observed、spec、margin、raw/display value 和跨文件比较 |

### 9.7.1 关键数据跨 CMBX 对比

关键数据不依赖是否进入数据库。它可来自：

- Report summary/result cells。
- FOQ contract 标记的关键测量 cells。
- Definitions sheet 对应的 spec/limit cells。
- 用户临时选择的可计算 report cells。

建议使用 sequence 为行、关键指标为列的数据矩阵：

| Sequence | Device | Test Date | TempAcc40 | Spec | Margin | TempStability | Spec | Margin |
|---|---|---|---:|---:|---:|---:|---:|---:|

每个数值保留：

- raw calculated value。
- report display value 和 number format。
- spec/limit value。
- comparison operator，例如 `<=`、`>=` 或 range。
- margin to limit。
- report template / Definitions sheet 来源。
- cell/formula/raw evidence trace。

跨 CMBX 比较支持：

- 按 device model、report template/version 和测试类型分组。
- 排序、筛选、固定关键列和导出当前比较表。
- 对选中指标显示 min/max/mean/range 和差值。
- 选择一个 CMBX 作为 reference，显示 absolute delta 和 relative delta。
- 将选中指标绘制为点图、箱图或按测试日期排列的短期趋势图。
- 点击异常值打开对应 channel、formula window 和 audit evidence。

如果不同 CMBX 使用不同 report template 或 Definitions spec，界面必须同时显示各自 spec，并突出“spec changed”；不得先统一限值再比较。

### 9.7.2 异常优先审核

批量计算结束后，默认首先显示需要用户处理的记录：

1. Fail。
2. Incomplete / Error。
3. Review Required / Unverified。
4. Spec changed。
5. 与批次分布明显不同的关键数值。

每条异常必须给出：

- 哪个 CMBX / sequence / test 出现问题。
- 具体数值、spec 和 margin。
- 问题发生在哪一层：template、cell、formula、RetTime、audit、channel 或 raw data。
- 推荐下一步操作，例如确认模板、查看 channel、检查 method 或补充证据。

### 9.7.3 批次保存

一次批量检查保存为 FOQ Review Batch，包含：

- 输入 CMBX 路径和 hash。
- sequence/device/template/contract 绑定。
- 所有关键数值和状态。
- 用户确认、备注和 override。
- 计算器、KB、mapping 和 Definitions 版本。
- 最终检查报告与移交结果。

重新打开批次时，只重新计算新增、修改或上次失败的 CMBX。

### 9.8 FOQ Channel 对比

Channel 对比是独立任务，但使用 FOQ contract 提供上下文：

- 根据所选测试自动推荐相关 channels。
- 跨多个 sequence/injection 叠加相同 channel。
- 同时显示 upper/lower/internal/external 等成组 channels。
- 自动标记 method RetTimes、report formula 计算窗口和 acceptance 区间。
- 支持按 injection start、RetTime 或测试阶段对齐。
- 支持 zoom、pan、隐藏、分面、单位分轴和数值提示。
- 显示窗口内 average/min/max/range/noise/drift 等与 FOQ 公式一致的统计。
- 可选择一个已验证 sequence 作为 reference，显示差值或偏差，但 reference 不自动成为 acceptance criteria。
- 图表、当前窗口数据和比较摘要可导出。

与业务中心 2 的区别：

| 通用 CMBX Channel Plot | FOQ Channel 对比 |
|---|---|
| 用户自由选择任意 channel | 按 FOQ test contract 推荐 channel 组合 |
| 只显示信号和用户标记 | 自动显示 RetTime、formula window、nominal/limit |
| 不做测试判定 | 与测试结果卡片和 pass/fail evidence 联动 |

### 9.9 Acceptance Criteria 管理

每个判定必须保存来源：

- FOQ TD / KB 文档和版本。
- Report Definitions cell 或模板版本。
- 外部/内部判据类型。
- 单位、比较符和有效型号。

#### Definitions sheet 的处理原则

- 选定 report template 后，优先解析其 Definitions sheet、named cells、lookup table 和适用型号分支。
- 为复现该模板的 CM 报告结果，默认使用模板实际引用的 Definitions value。
- FOQ TD / KB 用于验证该值是否符合正式测试规范，而不是在后台静默覆盖模板值。
- Definitions sheet 没有明确标记 External/Internal 时，显示 `Type: not explicit in source`。
- 同一测试在不同模板版本中的 Definitions value 必须可比较和追踪。
- Definitions cell、FormulaOne 引用和最终 pass/fail cell 之间应建立 dependency trace。

当 FOQ TD、KB、report template 或 mapping 中的限值冲突时，状态必须为 `Review Required`，由用户选择有效来源并记录理由。

### 9.10 人工审核与结果移交

人工审核允许：

- 确认自动选择的 report template。
- 对 Unverified/Open Verification 项补充证据和备注。
- 标记数据已审核，但不能无痕改写计算值。
- 对判定进行 override 时必须记录原状态、理由、时间和操作者。

完成后产生“FOQ Verified Result Set”，包含：

- sequence/device/test 结果。
- 计算值、显示值、单位和判定。
- acceptance criteria 和版本。
- 完整依赖 trace。
- 人工审核和 override 记录。

该结果集可导出为检查报告，也可移交业务中心 4 生成数据库记录。

### 9.11 当前缺口

- 需要定义 Overall 状态如何由 External、Internal 和信息类测试汇总。
- 需要确定 FOQ contract 的版本锁定与升级策略。
- 需要确定用户确认 report template 后，确认结果保存到 sequence 级历史还是全局规则。
- 需要定义 reference sequence 的选择和 channel 差值统计。
- 需要确定人工 override 是否需要电子签名或只记录本地审计。
- 需要列出第一批完整支持的 module/test，未支持模块必须显示能力边界。
- 需要定义哪些 report cells 默认属于“关键数据”，以及用户如何补充自定义关键 cells。
- 需要确认短期比较图与第四部分长期质量趋势的交接格式。

### 9.12 最低业务验收场景

给定一个包含多份 TCC FOQ CMBX 的文件夹，用户应能：

1. 一次加入整个文件夹。
2. 无需逐个打开文件，即看到所有 sequence、device 和测试覆盖。
3. 一次计算全部已支持测试的关键 report values。
4. 在同一个矩阵中看到 observed、Definitions spec、margin 和 pass/fail。
5. 筛选所有 Fail、Incomplete 和 spec changed 项。
6. 点击任一数值追溯到 report cell、formula、RetTime、audit 和 raw channel。
7. 对多个 CMBX 的相同关键指标和相关 channels 进行对比。
8. 保存本次审核，并将已验证结果移交质量数据与数据库流程。

### 9.13 多 HPLC Module 扩展架构

FOQ 快速检查不得把 TCC、VDAD 或任何具体型号硬编码进页面和计算主流程。采用“公共检查内核 + Module Package”结构：

| 层 | 固定职责 | Module Package 提供的内容 |
|---|---|---|
| 公共检查内核 | CMBX 批量加载、依赖求值、状态模型、证据追踪、结果矩阵、批次保存 | 不包含具体测试名和字段名 |
| Module Catalog | module/family/model/test 的发现、筛选和显示 | module ID、型号别名、测试目录、适用性 |
| FOQ Contract Adapter | 统一 Result Location、Calculation、Acceptance 三层契约 | mapping 文件、report template 规则、Definitions/TD/SPEC 来源 |
| Formula/Evaluator Adapter | 将 report cell 依赖解析为 raw/audit/workbook 计算 | module 特有 workbook-derived rules 和尚未实现的公式声明 |
| Visualization Profile | 推荐关键指标和 channel 对比方式 | channel 组、默认窗口、单位、图表和关键结果列 |
| Export Adapter | 生成模块对应的检查报告和 Verified Result Set | DB/table/field mapping、显示精度、数据类型 |

UI 不为每个 module 新建标签页，而使用统一导航：

```text
FOQ Quick Check
-> Module Family
-> Device Model
-> Test / Metric
-> Batch Result Matrix
-> Evidence / Channel Comparison
```

新增 module 时，理想状态只增加一个版本化 Module Package，并通过 contract tests 验证，不修改公共页面。无法识别的 module 仍可由业务中心 2 通用浏览，但在 FOQ 中显示 `Unsupported Module Contract`，不得套用相似型号规则。

## 10. 业务中心 4：质量数据与数据库

### Decision 005: 历史生产数据、受控写入和双 QC 工作台

- 状态：Proposed
- 用户目标：读取全部历史生产质量数据，将新验证结果可靠写入目标数据库，并通过 Power BI 和程序内工作台进行统计分析、历史对比和失败率预测。

### 10.1 数据源与目标

| 连接 | 角色 | 默认权限 | 主要用途 |
|---|---|---|---|
| `deger-db04.emea.thermo.com.dsn` | 历史生产数据源 | Read | 读取所有历史生产/QC 数据，建立历史基线 |
| `deger-db04.emea.thermo.com` | 生产写入目标 | Controlled Write | 写入审核通过的新质量结果 |
| `QCLab.dsn` | 本地写入与验证目标 | Read/Write | 本地测试、开发、回归验证和离线分析 |

连接配置必须明确标记 `Historical Read`、`Production Write` 和 `Local/Test`，避免用户把测试数据误写入生产数据库。

### 10.2 端到端数据流程

```text
Historical DSN
-> schema discovery / legacy mapping
-> canonical QC data model
-> historical baseline and statistics
-> Power BI semantic layer + in-app QC preview

FOQ Verified Result Set
-> write preflight
-> staging / duplicate check / schema validation
-> user confirmation
-> transactional write to Local QCLab or Production DB
-> write audit and reconciliation
-> updated QC analysis
```

只有业务中心 3 生成的 `FOQ Verified Result Set` 或经过同等级验证的数据，才能进入正式写入流程。

### 10.3 统一 QC 数据模型

无论历史数据库当前采用多少张宽表，分析层都需要统一为可追溯的数据模型。建议核心实体包括：

| 实体 | 关键内容 |
|---|---|
| Device | Serial、ModelNo、ModelVariant、hardware/firmware、生产线 |
| Test Run | CMBX/sequence、test date、operator、location、source hash |
| Test Definition | test、metric、unit、model applicability、spec version |
| Measurement | observed raw/display value、unit、result cell、formula trace |
| Specification | lower/upper/target、operator、External/Internal、source/version |
| Result | Pass/Fail/other status、margin、review/override |
| Data Lineage | CMBX、Location file、Report Template、Definitions、KB/evaluator version |
| Write Audit | target、operation、time、operator、row count、success/error |

建议保留现有业务宽表用于兼容，同时建立适合 Power BI 和统计分析的长表/星型模型或数据库 views。

### 10.4 历史生产数据读取

首次接入 `deger-db04.emea.thermo.com.dsn` 时需要：

1. 枚举 schema、tables、views、columns、types、keys 和 row count。
2. 建立 legacy table/column 到统一 QC metric 的 mapping。
3. 识别单位差异、空值、重复记录、历史字段改名和型号分支。
4. 识别不同 report/spec 版本导致的数据含义变化。
5. 建立增量同步水位，例如 TestDate + ID，而不是每次全量读取。
6. 在本地保存只读缓存和最后同步状态，支持快速预览。

历史数据不得因为 mapping 不明确而静默合并。无法统一的字段保留原值并标记 `Unmapped`。

### 10.5 受控写入

写入流程必须提供：

- 目标环境醒目标识：Production / Local。
- schema 和 data type 预检。
- 字段级 preview：将写入哪张表、哪些 columns、哪些 values。
- unique key / duplicate 检查。
- dry run。
- staging 后再 commit。
- transaction：整批成功或明确回滚。
- idempotency：同一 Verified Result Set 重试不会重复写入。
- 写入后的 row count 和关键值回读核对。
- 完整 write audit 和错误记录。
- 用户权限和最小权限原则。

Production 写入不得使用保存在源代码或明文项目文件中的密码；优先使用 ODBC DSN、Windows authentication 或操作系统凭据存储。

### 10.6 统一 QC Analysis SPEC

Power BI 与程序内工作台应读取同一套统计定义，避免两个界面算出不同结果。QC Analysis SPEC 至少定义：

- metric ID、名称、单位和来源字段。
- device/model/test applicability。
- aggregation level：measurement、sequence、device、batch、period。
- cohort/filter 定义。
- spec limit 与 control limit 的来源。
- mean、median、standard deviation、percentile 等统计方法。
- outlier 规则和 minimum sample size。
- failure rate 分母/分子定义。
- 时间粒度和 rolling window。
- prediction target、特征、训练区间和评估指标。
- Power BI visual 与程序内 quick view 的推荐展示。

### 10.7 两套 QC 工作台

#### A. Power BI 工作台

适合长期、共享和管理层分析：

- 生产量、Pass/Fail 和 failure rate 趋势。
- 按 model、variant、line、period、test 和 metric 下钻。
- 关键指标分布、箱图、控制图和 spec margin。
- Top failure tests 和 Pareto。
- 历史版本/spec 变化影响。
- 预测失败率、置信区间和模型状态。
- 定时刷新、权限控制和共享。

程序负责提供稳定的数据模型、views/data mart 和 refresh contract，不在代码中硬编码 Power BI 页面布局。

#### B. 程序内 QC 快速预览

适合工程师即时分析：

- 快速选择 device/model/test/metric/date cohort。
- 当前批次与历史均值、标准差、percentile 和 control limit 比较。
- trend、distribution、box plot、scatter 和 control chart。
- 点击统计点回到具体 Test Run、CMBX 和 FOQ evidence。
- 查看新写入数据是否落在预期分布中。
- 保存筛选条件和导出当前分析。

### 10.8 统计分析范围

基础统计建议包括：

- count、missing count。
- mean、median、standard deviation、variance。
- min、max、range、quartiles、percentiles、IQR。
- failure count/rate 和置信区间。
- spec margin 分布。
- moving average / rolling failure rate。
- process control chart，例如 I-MR；有合理分组时再使用 Xbar-R/S。
- Cp/Cpk/Pp/Ppk，但只有在 spec、分布假设和样本量满足时才显示。

Spec limits 与 statistical control limits 必须视觉和语义分离：前者决定规范通过，后者反映过程是否稳定。

### 10.9 失败率预测

预测功能分阶段建立：

| 阶段 | 输出 | 要求 |
|---|---|---|
| 1. 描述 | 当前/滚动 failure rate + confidence interval | 明确分母、cohort 和时间窗口 |
| 2. 统计预测 | 下一时间窗口的 failure rate forecast | 足够历史样本、时间验证和预测区间 |
| 3. 风险模型 | 按 model/batch/test 给出风险概率 | 防止数据泄漏、处理类别不平衡、解释关键因素 |

每个预测必须显示：

- 使用的数据范围和样本量。
- target 定义。
- model/version 和训练日期。
- validation method 和指标。
- confidence/prediction interval。
- data drift、spec change 和适用范围警告。

样本量或数据质量不足时显示 `Insufficient Data`，不得输出看似精确的失败概率。

### 10.10 向 FOQ 快速检查提供历史基线

业务中心 3 可以调用质量数据中心的只读 Historical Baseline Service：

```text
Current FOQ key value
-> select historical cohort
-> historical mean/std/percentile/control limit
-> delta, z-score, percentile rank, anomaly flag
```

历史 cohort 至少可按以下条件选择：

- Device Model / ModelVariant。
- Test / Metric。
- Report/SPEC version。
- Firmware/Hardware version。
- Production line/location。
- Date range。

FOQ 结果必须并列显示：

| Formal SPEC Result | Historical Comparison |
|---|---|
| 基于 Definitions/FOQ SPEC 的 Pass/Fail | 与指定历史 cohort 的均值、分布和控制限比较 |

Historical anomaly 不得自动改写正式 Pass/Fail；它只产生 `Historical Review` 提示。

### 10.11 当前缺口

- 需要读取并记录 `deger-db04.emea.thermo.com.dsn` 的实际 schema 和权限边界。
- 需要确认生产写入目标的数据库名、schema、table contract 和审批流程。
- 需要确认现有宽表是否允许新增 views/analysis tables。
- 需要定义第一版统一 QC metric dictionary。
- 需要确认 Power BI 的部署位置、refresh gateway 和访问权限。
- 需要确定预测目标是总体 failure rate、test-level rate、device risk，还是分阶段全部支持。
- 需要定义第三与第四业务中心之间 `FOQ Verified Result Set` 和 Historical Baseline API/文件格式。

### 10.12 最低业务验收场景

1. 通过只读 DSN 查看指定历史 table 的数据量、字段和时间范围。
2. 将历史字段映射为统一的 device/test/metric/value/spec/status 结构。
3. 将一个 FOQ Verified Result Set dry-run 写入本地 `QCLab.dsn`。
4. 预览目标表和 values，确认后事务写入并回读验证。
5. 在程序内查看当前批次与历史 cohort 的均值、分布、failure rate 和趋势。
6. Power BI 使用同一数据模型得到一致统计结果。
7. FOQ 快速检查能选择一个历史 cohort，并并列显示正式 SPEC 结果与历史对比。
8. 失败率预测在数据不足时明确拒绝，在数据充分时显示预测区间和验证指标。

### 10.13 多 HPLC Module 扩展架构

质量中心必须以 metric 为核心，而不是以某个 module 的宽表为核心。TCC、VDAD、Pump、Autosampler 等模块共享同一套 canonical QC entities，并通过版本化 Metric Dictionary 扩展：

| 维度 | 示例 |
|---|---|
| Module / Device | TCC、VDAD、Pump；VH-C10-A、VF-D11-A |
| Test | Temperature Accuracy、Noise、Flow Accuracy |
| Metric | TempAcc40、ASTM Noise、Flow Deviation |
| Value Contract | data type、unit、display precision、aggregation |
| Specification | limits、operator、External/Internal、适用型号、版本 |
| Source Mapping | legacy DB table/column、FOQ field、report cell/formula trace |
| Analysis Profile | cohort、control chart、minimum sample size、预测适用性 |

程序内 QC UI 使用动态筛选与指标面板：`Module -> Model -> Test -> Metric -> Cohort`。模块专用图表由 Analysis Profile 声明；没有 profile 时仍显示通用 trend/distribution/control chart，不为每个 module 复制页面。

Power BI 读取同一 canonical model 和 Metric Dictionary。新增 module 时，先完成 source mapping 和数据质量验证，再开放正式写入、统计和预测；“已有数据但未完成 metric mapping”的状态必须显示为 `Unmapped`。

## 11. 业务中心 5：HPLC 应用与工作流

### Decision 006: AppsLab 发现、本地应用库与受控派生

- 状态：Proposed
- 用户目标：从 Thermo Scientific AppsLab 或本地资料找到可用 HPLC 应用，将完整 eWorkflow 导入本地、理解其配置和方法，适配到实际仪器与样品计划，并保留来源、变更和运行结果。

### 11.1 业务对象与边界

AppsLab 的 eWorkflow 是完整应用过程，不只是一个 CMBX 文件。官方资料显示其可包含 sequence 结构、instrument method、processing method、report template、view setting、custom variables 和附加文档。因此本中心的核心对象定义为 `Application Project`：

| 内容 | 说明 |
|---|---|
| Provenance | AppsLab application ID、source URL、下载时间、文件 hash、作者/版本 |
| Application Metadata | analytes、matrix、market、keywords、仪器与色谱柱信息 |
| Sequence Blueprint | injection list、bracketing、sample/calibration 结构和默认值 |
| Execution Assets | instrument/processing methods、custom variables、view settings |
| Result Assets | report templates、计算与校准约束 |
| Requirements | instrument modules、configuration、columns、consumables、solvents/standards |
| Documents | AppsLab guide、application note、用户补充说明 |
| Local Derivative | 本地适配后的变更、责任人、验证状态和派生版本 |
| Run History | 创建的 sequence、运行 CMBX、结果、偏差和复用记录 |

第一版不批量抓取或镜像 AppsLab。用户在官方 AppsLab 搜索并下载 eWorkflow，程序负责导入本地应用库。后续只有在确认官方 API、认证、许可和下载边界后，才考虑站内搜索或受控下载集成。

规划依据：

- [Thermo Scientific AppsLab Library](https://appslab.thermofisher.com/)
- [AppsLab Getting Started](https://appslab.thermofisher.com/GettingStarted)
- [Chromeleon eWorkflow 官方指南](https://appslab.thermofisher.com/Content/GettingStarted/AppsLab%20Library%20-%20eWorkflow%20-%20English.pdf)

### 11.2 指引式业务流程

```text
Discover on AppsLab
-> Download official eWorkflow and documents
-> Import into Local Application Library
-> Extract application manifest and assets
-> Compare requirements with local instrument/configuration
-> Review compatibility and unresolved gaps
-> Create an immutable source snapshot
-> Create a local derivative project
-> Adjust sequence/sample plan and permitted parameters
-> Preflight methods, processing, reports and configuration together
-> Export/launch in Chromeleon
-> Attach completed CMBX and analyze results
-> Save run history and lessons back to the local application project
```

### 11.3 UI 结构

HPLC Applications 首页提供五个任务入口：

| 入口 | 主要操作 |
|---|---|
| Discover | 打开 AppsLab、保存 application URL/ID、登记待下载项目 |
| Local Library | 导入 eWorkflow/CMBX/文档，按 analyte、matrix、instrument、column 搜索 |
| Inspect | 查看 sequence blueprint、methods、processing、reports、custom variables 和 requirements |
| Adapt & Launch | 选择本地仪器，执行兼容性检查，创建派生项目并调整样品计划 |
| Run History | 关联运行后的 CMBX、结果、偏差、版本和复用经验 |

主界面显示应用卡片与状态，而不是暴露所有底层文件。进入项目后采用步骤导航，并可按需跳转到业务中心 1 的方法/报告编辑、业务中心 2 的 CMBX 诊断和业务中心 4 的结果分析。

### 11.4 兼容性与变更控制

兼容性检查至少覆盖：

- Chromeleon/eWorkflow archive version。
- 本地 instrument module、型号和 driver 能力。
- method symbols、channels、valves、lamps、cells 和 custom variables。
- column、flow path、solvents、standards 和 consumables。
- sequence injection 类型、校准结构和 sample position 要求。
- processing/integration/calibration 依赖。
- report formula、component 和 result contract。

原始 AppsLab 包保持只读和 hash 锁定。任何修改都生成 Local Derivative，并记录差异、修改原因、验证人和运行证据。通过语义生成或自动适配得到的资产在完成配置预检和实机验证前不得标记为 runnable/validated。

### 11.5 与现有业务中心的协作

| 需要 | 复用业务中心 |
|---|---|
| 修改/生成 instrument method 和 report | 1. 方法与报告建立 |
| 检查下载包和运行后 CMBX | 2. CMBX 浏览与诊断 |
| 对应用做工厂 FOQ 验证 | 3. FOQ 快速检查，仅在确属 FOQ 时使用 |
| 外部报告、统计、数据库和长期趋势 | 4. 质量数据与数据库 |

HPLC 应用与 FOQ 必须保持语义分离：FOQ 验证设备是否满足工厂规范；HPLC application 解决特定 analyte/matrix 的采集、处理、定量与报告工作流。

### 11.6 分阶段实施

| 阶段 | 范围 | 不包含 |
|---|---|---|
| 1. Local Application Library | 手工下载后导入、manifest 提取、资产浏览、来源追踪、兼容性预检 | 自动抓取 AppsLab、自动运行 |
| 2. Guided Adaptation | 本地派生项目、sequence/sample plan 调整、配置差异与交叉预检 | 未验证的全自动 method transfer |
| 3. Application Lifecycle | Chromeleon 启动交接、运行 CMBX 回收、结果分析、版本与经验复用 | 无审批的生产部署 |

### 11.7 当前缺口

- 需要获得一个或多个真实 AppsLab eWorkflow 样本，确认其 archive、metadata 和附带文档结构。
- 需要确认 AppsLab 的下载认证、许可、再分发和自动化访问边界。
- 需要定义 `Application Project Manifest` 和 Local Derivative diff 格式。
- 需要梳理 Chromeleon 创建 sequence 时可安全修改的 eWorkflow 参数。
- 需要扩展 Processing Method、integration、calibration 和 component/quantitation 的解析能力；这些对常规 HPLC 应用比 FOQ 更关键。
- 需要定义应用结果如何进入 External Report Engine、QC metric model 或独立 application result model。

### 11.8 最低业务验收场景

1. 用户从 AppsLab 下载一个 eWorkflow 并导入本地应用库。
2. 程序展示 application metadata、sequence blueprint 和全部关联资产。
3. 程序将应用要求与一个本地 instrument configuration 比较并列出兼容、缺失和待确认项。
4. 原始包保持不变，用户创建一个有完整 provenance 的 Local Derivative。
5. 用户调整样品数量/位置等允许参数，并完成交叉预检。
6. 用户在 Chromeleon 中创建/运行 sequence 后，将结果 CMBX 关联回项目。
7. 用户可从 Run History 跳转到 raw data、method/audit/report 和统计结果。

## 12. 后续讨论记录模板

每次确认一项业务流程时追加：

```markdown
### Decision <编号>: <主题>

- 状态：Proposed / Confirmed / Superseded
- 用户目标：
- 起点：
- 必要输入：
- 操作步骤：
- 输出：
- 失败与恢复：
- UI 映射：
- 内部模块：
- 验收标准：
```

## 13. 实施门槛

只有满足以下条件才开始代码重构：

- 顶层业务入口已确认。
- 每个入口的输入、步骤、输出已确认。
- 旧功能的保留、迁移、隐藏或删除清单已确认。
- 长任务和错误处理方式已确认。
- 至少形成一条从输入到结果的完整验收场景。

## 14. Business Hub 首页导航更新（2026-07-29）

- 状态：Implemented
- 首页标题改为 `Choose a task`，标题后显示轻量的变色龙视觉提示。
- 三个顶层业务分支调整为：
  - `Design & Generate`
  - `Chromatograms & Results`
  - `Quality Control & Database`
- `Home` 与功能导航视觉分离，并使用 Thermo Fisher 红色。
- 首页原三列 journey 卡片改为响应式思维导图：
  `CMBX Workspace -> 业务分支 -> 具体任务`。
- 具体任务节点直接启动真实工作流，不再经过包含
  `Input / Output / Migration / Start guided workflow` 的冗余说明页。
- 从侧栏选择业务分支时，显示居中的单分支任务图，叶节点仍直接启动任务。

## 15. 任务分支与生成链路更新（2026-07-29）

- 状态：Implemented
- `Design & Generate` 不再把方法和报告合并成一个入口，而是显示三个同级任务：
  - `Instrument Method Generation`
  - `Report Template Generation`
  - `HPLC Applications & Workflows`
- 方法与报告入口直接打开各自分支的 Step 1，不再要求用户重复选择资产类型。
- Report 分支支持选择本地 Method MD，也支持从 generation history 选择最近生成的方法。
  该 Method MD 会进入网页 AI ZIP，作为 report 的 channels、variables、audit events、RetTimes、
  timing windows 与 configuration 的执行契约；生成 Report CMBX 时，Method basis 也会写入项目快照和 manifest。
- Prompt optimization 的职责是把用户零散输入重写成一条有顺序、可独立发送给网页模型的完整生成请求，
  而不是只增加标题或标注。最终提示词必须要求网页模型按照附件 SPEC/KB 返回完整 Markdown。
- Import & Preview 顶部文件区增加稳定高度，按钮统一缩短为 `Choose MD`，避免窄窗口下标题、路径和按钮互相挤压。
- `Chromatograms & Results` 拆成三个同级任务：
  - `Batch Raw Data Export`
  - `Chromatograms & Integration`
  - `Direct CM Formula Results`
- 三条分析流程均遵循：`Choose task -> Choose CMBX workspace -> Review result`。
  从首页任务节点进入时，任务已确定，窗口首先要求选择 CMBX；独立启动分析窗口时，先显示任务选择页。

## 16. V1.4 工作流构建验收（2026-07-29）

- 状态：Implemented and verified
- Business Hub 已按业务对象提供八个直接任务节点，不再将已迁移功能包装成旧 Explorer 的跳转说明页。
- Method/Report Creation 支持模块多选、网页 AI 材料打包、可编辑提示词优化、MD 预检、彩色预览、CMBX 生成和历史 manifest。
- Report Generation 可以绑定本地或最近生成的 Method MD；Method basis 同时进入网页 AI 上下文、生成项目输入快照和项目 manifest。
- Chromatograms & Results 已完成 task-first 导航，Raw Export、Chromatograms & Integration、Direct CM Formula Results 各自独立进入 CMBX workspace。
- Import & Preview 在最小窗口尺寸下保留稳定的文件标题、路径和 `Choose MD` 操作区，并提供横向/纵向预览滚动与底部进度日志。
- Prompt optimization 会把零散需求重写成可直接发送给网页模型的完整、有顺序生成请求，并强制要求按 SPEC/KB 返回完整 Markdown。
- RID OQ 多 sequence 解析、Direct CM formula catalog、method/report generation 及相关构建文档纳入同一版本提交。
- 自动验证：`190 passed`；关键 GUI 路由完成 Tk smoke test；Python 模块完成 `py_compile`。
