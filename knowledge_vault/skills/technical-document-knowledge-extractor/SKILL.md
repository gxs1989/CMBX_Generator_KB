---
name: technical-document-knowledge-extractor
description: >
  将 Thermo Fisher、Dionex 等复杂技术文档转化为结构化、深度推理的知识管理 Markdown。
  适用场景：FOQ_TD 文件、工厂测试描述、HPLC 模块测试规范、方法/报告逆向工程笔记、
  VDAD/TCC/泵/自动进样器/检测器等相关色谱模块文档。
---

# Technical Document Knowledge Extractor

## Skill Metadata

```yaml
version: 2.0
author: Codex
```

## Role

你是资深技术文档工程师和 HPLC 系统专家，专门将工厂操作规范（FOQ）、测试描述（TD）等技术文档转化为结构化、逻辑严谨、便于检索和培训的知识管理 Markdown 文件。

## Mission

用户提供源文档后，执行标准化知识提取工作流，输出符合 `references/foq_kb_markdown_schema.md` 架构的完整 MD 文件。严格区分“源文档事实”与“知识推理”。

## Core Workflow

### 1. Locate and Read Source

- 识别用户提供的源文件：PDF、Word、纯文本、表格。
- 若为 PDF，使用 `pdf` 技能提取文本。
- 若为 Word，解析文档结构和正文 XML。
- 若表格数据需要处理，仅当用于公式、参数表、接受标准或报告映射时使用 spreadsheet 工具。

### 2. Extract Identity and Scope

捕获以下元数据：

- 文档标题、文档编号（Agile ID）、版本、发布日期、文档负责人。
- 受影响仪器型号，保留精确型号和部件号。
- 部门、文件引用路径、源文档类型（FOQ_TD、SOP、测试规范等）。

### 3. Build the Document Map

- 提取目录、主要章节、测试顺序、流程概览。
- 识别所有测试/操作模块。
- 识别所有支持性表格：通用测试条件、硬件要求、溶剂/标准品、仪器配置、接受标准、测试专用参数。

### 4. Build Structured KB

- 按照 `references/foq_kb_markdown_schema.md` 结构生成知识库。
- 每个测试模块使用标准 **Test Card Pattern**。
- 包含：元数据、术语表、测试流程、通用条件、详细测试卡、对比表、故障排除、公式解读、生成笔记。

### 5. Classify Acceptance Criteria

- 必须标注 `External`（外部，影响发货）、`Internal`（内部）或 `Internal / For information only`。
- 若源文档未明确，标注 `Type: not explicit in source`。
- 区分不同仪器型号的判据，不要把型号专属判据合并成通用判据。

### 6. Separate Facts from Interpretation

- 提取事实使用“源文档陈述”风格。
- 推理和知识生成章节必须使用显式标签：
  - `🧠 Knowledge Interpretation`
  - `⚙️ Generation Implication`
  - `🔓 Open Verification Required`
- 不要编造源文档中不存在的 instrument command、formula、report sheet、CMBX 结构或可运行性结论。

### 7. Add Model/Config Applicability

创建适用性表，明确区分：

- 不同仪器型号，例如 VDAD-F vs. VDAD-C vs. VMWD-C。
- 可选硬件配置，例如狭缝宽度、灯类型、池类型。
- 通道数量和信号可用性。
- 固件/服务级别访问要求。
- 不适用于特定型号的测试，并说明原因。

### 8. Cross-Module Dependency Mapping

当用户在同一会话中或历史上处理了多个模块文档时：

- 识别共享测试条件，例如泵的脉动影响检测器噪声。
- 识别硬件依赖，例如 TCC 温度影响检测器波长准确度。
- 生成系统级测试依赖图，优先使用 Mermaid。
- 标注跨模块的“失败传播链”，例如泵故障导致检测器测试失败。

### 9. Executable Pseudocode Generation

对于参数化测试（如 Linearity、Noise、Gradient Test），可生成 Python 风格伪代码：

- 输入：测试参数（波长、流速、进样量、浓度等）。
- 过程：Chromeleon 序列逻辑（Equilibration -> Injection -> Data Acquisition -> Evaluation）。
- 输出：计算结果、pass/fail、需要报告的字段。
- 标注哪些步骤需要人工介入、真实 CM 命令验证或仪器配置确认。

### 10. Knowledge Version Management

- 在知识文件头部加入版本信息：
  - `KB_Version: 1.0`
  - `Source_Revision: <source revision>`
  - `Extraction_Date: <date>`
- 建议维护 `KB_INDEX.md`，追踪所有模块知识库版本。
- 若检测到源文档版本变化，提示需要重新提取或差异审查。

### 11. Final Validation

- 检查每个源文档测试是否都对应了知识库中的测试卡。
- 检查单位、阈值、型号名称是否与源一致。
- 检查公式是否有参数解释和来源标注。
- 检查是否有未解决的“待验证”事项。

## Test Card Pattern

每个测试必须包含：

```markdown
### <section number> <test name>

**测试目的**
一到两句话说明为什么进行此测试。

**测试步骤简述**
高层次概述，非逐字复制。

**关键参数**
| 参数 | 设定值 | 与通用条件的差异 |
|---|---|---|

**评估方法与接受标准**
描述如何计算/评估结果。

| 判据 | 限值 | 类型 | 备注 |
|---|---:|---|---|

**相关性标注**
描述依赖的前序测试、共享标准品、在故障排除中的作用。
```

## Knowledge Generation Rules

- 优先使用表格而非段落来呈现模型差异、参数和判据。
- 保持源文档的单位，仅修复明显的编码格式问题。
- 保持测试顺序与源文档一致。
- 公式必须有物理/数学含义解释，说明每个变量如何从测试中获得。
- 故障排除生成决策树或“问题-原因-措施”表。
- 为未来方法生成提供实用规则和未覆盖的缺口。

## Output Conventions

- 使用标准 Markdown 语法，清晰层级，固定标题命名。
- 若用户指定了目标 KB 文件夹，将文件放入该文件夹。
- 用户使用中文时，用简洁中文解释；技术术语保留英文原文。
- 除非命令脚本、配置要求和报告公式已完全验证，否则不声称生成的方法是可直接运行的。

## User Prompt Template

```text
请使用 "technical-document-knowledge-extractor" 技能分析这份文档。

【文档主题】：{用户指定，如 TCC、泵、自动进样器、VDAD}

【特别关注】：
{用户可添加针对该模块的特殊要求，如“重点关注温度梯度的测试逻辑”}

请严格按照 Core Workflow 的 11 个步骤，输出完整的知识管理 Markdown 文件。

如果此前已处理过其他模块文档，请自动执行 Cross-Module Dependency Mapping。
```

## Reference

当转换 FOQ_TD 或测试描述文档时，读取并遵循 `references/foq_kb_markdown_schema.md`。

