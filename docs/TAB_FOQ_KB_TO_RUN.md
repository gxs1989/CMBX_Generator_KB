# FOQ Knowledge Alignment Tab

V1.2+ update: the former `FOQ KB to Run` tab is now the `FOQ Knowledge Alignment`
workbench.

Its purpose is to connect three evidence layers before any method/report/CMBX
generation is attempted:

```text
FOQ TD / KB meaning
-> loaded CMBX runtime evidence
-> method, report, DB, and configuration contract coverage
```

This tab is a verification and knowledge-alignment surface. It is not a direct
generator and should not claim that a new method is runnable unless the command
script, configuration requirements, and report formulas are verified.

Initial catalog families:

```text
TCC
VDAD
```

The central row is now `FoqAlignmentRecord`, implemented in
`foq_alignment_catalog.py`. The UI exposes family filtering, device multi-select,
TestIntent/TD text filtering, CMBX scope selection, an alignment table, and
review/design evidence panels:

- `TKN Node`
- `TD Meaning`
- `Method Evidence`
- `Report Evidence`
- `DB Evidence`
- `Design Actions`
- `Milestone Status`
- `Next Action Queue`
- `BlackBox Audit`
- `Open Verification Topics`
- `Dependency Impact`
- `Relationship Audit`
- `Resolution Choices`
- `Intent Preview`
- `Intent Conflict`
- `Open Verification`
- `Generation Readiness`

The alignment table includes `Modifiability` and `Intent Gate` columns. These
are derived design labels, not source facts. `Modifiability` summarizes whether
a row is currently:

```text
editable contract
editable after review
verify before editing
locked foundation
preserve audit/state step
not applicable
```

`Intent Gate` reflects the currently selected intent and parameter. It separates
review-only packet availability from runnable generation:

```text
review packet available
specialized draft available
blocked for runnable generation
```

The gate now also promotes hard relationship rules into blockers. For example,
an Accuracy single-point crop inherits `DEP_01` (Calibration -> Accuracy) and
shared-resource rules such as external thermometer requirements. These rules
must be resolved as explicit design decisions before any generated package can
be treated as runnable.

The detail panels are intended to move the tab from static knowledge display to
a design workbench:

- `Design Actions` lists known editable, review-required, and locked points.
- `Milestone Status` shows M1-M5 progress for the overall TCC knowledge
  engineering goal. It highlights the current test's milestone, documents the
  evidence behind each milestone, and carries forward the remaining open work
  such as unresolved black-box topics.
- `Next Action Queue` shows the global evidence queue across M2/M3. It groups
  open black-box closure tasks by milestone, priority, and evidence group, then
  ranks what should be decoded next. In the current TCC model, this keeps
  Processing Method decode / CM UI and Report workbook/formula extraction ahead
  of lower-priority review work because those black boxes block runnable
  generation for crop/merge intents.
- `BlackBox Audit` shows the selected TCC test's decomposition document,
  six-contract coverage, evidence-source section status, model-branch mentions,
  Mermaid/flow evidence, Open Verification count, parsed Open Verification
  topics, and document size. This lets the UI explain why an intent is still
  review-only instead of only saying that a gap exists.
  The Alignment workbook also includes `TCC Open Verification Topics`, a
  closure queue that classifies each topic as Method Command, Processing
  Method, Report Formula, DB Contract, Config Requirement, or general Open
  Verification, with likely evidence sources and closure actions.
- `Open Verification Topics` renders the selected row's closure queue as a
  dedicated detail panel, so the user can see the exact black-box task, likely
  evidence source, and closure action without scrolling through the full
  black-box audit text.
- `Dependency Impact` shows a compact dependency/impact graph for the selected
  test.
- `Relationship Audit` expands the structured relationship rows that apply to
  the selected test, grouped by execution order, dependency, shared resource,
  and intent rule. This is the review basis for deciding whether a crop, merge,
  or compare request changes upstream tests or shared CM resources.
- `Resolution Choices` turns hard relationship blockers into concrete design
  decisions. For example, a cropped Accuracy method must decide whether to
  reuse Temperature Calibration evidence, rerun Calibration, or explicitly mark
  Calibration out of scope for a non-FOQ exploratory run.
- `Intent Preview` renders a non-mutating preview for the selected intent tool:
  search/recommend, crop/modify, merge, or compare.
- `Intent Conflict` renders the current selected-row conflict matrix in the UI.
  It uses the same rows as `intent_conflict_matrix.tsv`, so merge/crop/compare
  review sees one consistent status model for method, processing, report, DB,
  configuration, RetTime, channel, audit, relationship, and open-verification
  evidence.
- `Open Verification` renders open gaps as a closure checklist. Closing an item
  should update the source KB or black-box decomposition document, then refresh
  the catalog.

## Intent Preview Controls

The workbench now exposes a first intent-tool layer above the alignment table.
This is still review-only; it does not write method files, report templates, or
CMBX packages.

| Control | Purpose |
|---|---|
| `Intent` | Selects `Search / Recommend`, `Crop / Modify`, `Merge`, or `Compare`. |
| `Parameter` | Optional free text such as `40 C`, `20->50->20`, `valve cycle`, or `noise`. |
| `Preview Intent` | Renders the impact preview into the `Intent Preview` detail tab. |
| `Export Intent MD` | Writes the selected intent preview and contract context as a Markdown review packet. |
| `Export Action Plan` | Writes a layered Method / Processing / Report / DB / Config / Validation task plan, including the current intent conflict matrix, conflict-driven required actions, and a categorized Open Verification closure queue. |
| `Export Draft Packet` | Writes reviewable draft method/report/config assets for supported intents. |

Intent behavior:

| Intent | What it answers | Generation boundary |
|---|---|---|
| Search / Recommend | Which known alignment rows match this query or current filter? | Retrieval only. |
| Crop / Modify | What RetTimes, channels, report cells, DB fields, and config must survive if this test is changed? | Does not rewrite method/report. |
| Merge | What shared resources and conflicts appear when two or more selected rows are merged? | Requires manual contract closure before generation. |
| Compare | What changes across selected tests or across device branches for one test? | Comparison only. |

Example: selecting `Temperature Accuracy` with intent `Crop / Modify` and
parameter `40 C` will explicitly flag that a single-point 40 C method still
needs an approach/baseline rule, report row/cell remapping, DB field subset
selection, RetTime/channel preservation, and open-verification closure before a
runnable CMBX can be claimed.

For TCC `Temperature Accuracy`, the same preview now also builds a structured
parameter impact model. A parameter such as `40 C` is parsed as an Accuracy
setpoint, checked against the selected VH/VC/VA device branches, and expanded
into:

- affected device models;
- retained setpoint(s);
- selected DB fields, for example `TempAcc40` plus `RES_TempAccuracy`;
- removed or unused `TempAcc*` fields that must be removed, hidden, or marked
  not applicable in the report/DB contract;
- notes about workbook-rule narrowing, such as keeping `RES_TempAccuracy`
  meaningful only after the pass/fail rule is narrowed to the retained point.

This structured impact appears both in the `Intent Preview` tab and in exported
`Intent Action Plan` Markdown.

The exported `Intent Action Plan` also includes an `Open Verification Closure
Queue`. Each unresolved black-box topic is normalized into a row with:

- Test ID
- category, such as Method Command, Processing Method, Report Formula, DB
  Contract, or Config Requirement
- topic
- likely evidence source
- closure action

The same action plan also expands the current Intent Gate blockers and next
actions, including hard relationship rules from the relationship model. A
`Relationship Resolution Choices` section records the available design options
and the evidence that must be captured for each hard rule. Draft packets and
the exported workbook additionally include a fillable decision register with
`Selected Option`, `Decision Status`, `Evidence Path`, `Owner`, and `Notes`
columns so a reviewer can close those decisions explicitly instead of leaving
them as prose.

Intent review packets are written to:

```text
<Output Folder>/foq_knowledge_alignment/intent_reviews/*.md
```

Intent action plans are written to:

```text
<Output Folder>/foq_knowledge_alignment/intent_action_plans/*.md
```

Draft asset packets are written to:

```text
<Output Folder>/foq_knowledge_alignment/draft_asset_packets/<device>_<family>_<test_intent>_<intent>_<parameter>/
```

Each packet contains:

- selected intent and parameter
- selected alignment rows
- anchor Test Knowledge Node summary
- required RetTime/channel/audit/config contracts
- rendered intent preview
- open verification and next review actions

The packet is intended to become the handoff artifact between "I want this
change" and "we can now safely edit/generate method/report/CMBX assets."

The action plan is the next artifact after the review packet. It converts the
same intent into explicit modification tasks by layer:

```text
Method command
Processing method / IRC
Report template / FormulaOne
DB mapping and type/precision
Configuration symbols and channels
Validation in Chromeleon
```

For example, a `Temperature Accuracy` `Crop / Modify` plan with parameter
`40 C` will include tasks to define the 40 C approach/baseline rule, preserve
RetTime/channel contracts, review IRC/pass-action behavior, remove or mark
unused TempAcc report rows, choose the meaningful DB field subset, and validate
the modified package in Chromeleon.

## Draft Asset Packet Boundary

A generic draft packet is available for every alignment row after exactly one
device model is selected. It is conservative and review-only. It writes:

- `sequence_template.tsv`
- `method_report_binding.md`
- `config_contract.md`
- `report_db_contract.tsv`
- `intent_conflict_matrix.tsv`
- `generation_boundary.md`
- intent review and action plan Markdown
- a `draft_asset_packet_manifest.md`

The generic packet does not edit method/report payloads. It packages the current
FOQ -> injection -> method -> processing -> report -> DB evidence so the next
black-box review step has a stable handoff folder.
Both `generation_boundary.md` and `draft_asset_packet_manifest.md` include
relationship resolution choices, so the packet carries not only blockers but
also the allowed decisions and evidence that must be recorded.

For `Merge` and `Compare`, the generic packet preserves all selected alignment
rows in `sequence_template.tsv`, `method_report_binding.md`,
`config_contract.md`, `report_db_contract.tsv`,
`intent_conflict_matrix.tsv`, and `generation_boundary.md`.
This keeps multi-test intent reviews from collapsing back to the anchor row.
If more than one alignment row is selected, export uses the generic packet even
when the anchor row also has a specialized generator.

`intent_conflict_matrix.tsv` is the review table for multi-test design work. It
labels method, processing, report, DB, configuration, RetTime, channel, audit,
relationship, and open-verification evidence as `single value`,
`multiple values - review`, `union required`, `single-row review`, or
`open verification`.

The first specialized draft packet is deliberately narrow:

```text
Family: TCC
TestIntent: Temperature Accuracy
Intent: Crop / Modify
Parameter: numeric single setpoint, for example 40 C
Device: exactly one selected TCC model
```

The packet reuses the semantic single-point accuracy generator and includes:

- `project_spec.json`
- `sequence_template.tsv`
- `processing_method_binding.md`
- `instrument_method_draft.txt`
- `method_script_<setpoint>.txt`
- `required_configuration.md`
- `report_calculation_spec.md`
- `report_formula_map_<setpoint>.tsv`
- intent review and action plan Markdown
- `relationship_decision_register.tsv`
- method/report Excel workbooks
- a `draft_asset_packet_manifest.md`

It is still **not** a runnable CMBX. It is the first concrete bridge from
knowledge alignment into reviewable method/report assets. The added
`sequence_template.tsv` and `processing_method_binding.md` make the draft
packet look like a small method package review folder: one sequence row, one
instrument method draft, one preserved processing binding, one report
calculation contract, and explicit configuration requirements.
The manifest also includes the same relationship resolution choices as the
action plan, for example whether Accuracy reuses Calibration evidence, reruns
Calibration, or remains blocked until that dependency is waived.
`relationship_decision_register.tsv` is the fillable companion file for those
choices. Its default status is `Open`; after review, the chosen option and
evidence path should be recorded there or in the equivalent workbook sheet.

Coverage values are:

```text
complete
partial
open verification
missing
not applicable
```

`not applicable` is important for VDAD/VMWD distinctions. For example, VMWD-C
does not support DAD 3D Field behavior, so that row must not be presented as a
missing failure for VMWD-C.

The export button writes:

```text
<Output Folder>/foq_knowledge_alignment/FOQ_Knowledge_Alignment.xlsx
```

The workbook includes multiple review sheets:

- `FOQ Knowledge Alignment`: review-oriented evidence rows, including
  `Modifiability`, current `Intent Gate`, generic/specialized packet flags, and
  runnable-generation status.
- `Intent Gate Matrix`: one row per filtered alignment record showing the
  current intent's gate status, blockers, next actions, and matching
  relationship-model rules. Black-box open-verification topics are summarized
  by category in blockers, and the first closure actions are promoted into next
  actions.
- `TCC Milestone Status`: M1-M5 goal-progress summary, including whether a
  milestone is documented, structured/exportable, or still review-only.
- `TCC BlackBox Coverage`: milestone-oriented audit of expected TCC
  black-box decomposition documents, six-contract headings, open verification
  count, evidence-source section presence, VH/VC/VA branch mentions,
  Mermaid/flow evidence, and approximate document size. This is the audit sheet
  that tells the workbench whether a test is merely named or actually backed by
  a usable black-box review document.
- `M2 Temperature Contract Matrix`: temperature-family planning matrix for
  Calibration, Precision/Fan, Stability/PCC, HeatUp/CoolDown, and BurnIn. It
  summarizes each six-contract status, open topic categories, closure actions,
  and whether the test is still review-only or can become a candidate template
  after CM validation.
- `M2 Contract Closure Tasks`: actionable evidence tasks derived from the M2
  black-box documents. Each row binds an open topic or missing heading to a
  specific contract layer, such as Method Command, Processing Method, Report
  Formula, DB Contract, or Config Requirement, and records the evidence source
  and closure action needed before generation can move beyond review-only. The
  queue is prioritized (`P1` for Method/Processing/Report black boxes, `P2` for
  DB/Config, `P3` for residual review items) and grouped by evidence workstream,
  such as processing-method decode, report workbook/formula extraction, DB audit,
  method-command decode, or configuration evidence.
- `M2 Evidence Workstreams`: grouped execution view of the closure-task queue.
  This is the recommended starting point for the next engineering pass: pick a
  `P1` workstream, such as `Processing method decode / CM UI` or
  `Report workbook/formula extraction`, then close all tasks in that group and
  update the source black-box documents.
- `M2 P1 Extraction Plan`: concrete extraction checklist for the highest-risk
  Method Command, Processing Method, and Report Formula black boxes. Each row is
  derived from a P1 closure task and expands it into evidence steps, validation
  outputs, and the source contract update needed to move a temperature test from
  review-only toward reusable generation-template status.
- `M2 Processing Targets`: processing-method-specific target list for the
  `Processing method decode / CM UI` workstream. It expands open IRC/corrective
  topics by device model and sequence binding, showing the injection,
  instrument method, processing method, expected behavior, extraction target,
  and readiness. This is the handoff point for a future processing-method row
  decoder or manual CM UI confirmation.
  For TCC corrective insertions, TD evidence now states that
  `Variables.GenericBool0` selects the VH pass branches
  (`Temperature Accuracy_H`, `Temperature Stability_and_PCC_H`) and the VC/VA
  fail branches (`Temperature Accuracy_C`, `Temperature Stability_C`) from
  `FOQ_VX-C10_V2_00_AdditionalInjections`. The UI therefore treats the intended
  behavior as TD-backed while still requiring serialized CM action-row
  confirmation before runnable generation.
  When loaded CMBX packages contain the referenced processing method, the
  Alignment detail `Method Evidence` now includes a processing-method inspector
  summary: embedded XML/root-control evidence, action-column labels such as
  `Pass Actions` / `Fail Actions`, relevant `SST/IRC` labels, token counts, and
  snippets. The inspector also reports grid/control summaries, including
  `SSTGrid` column names and row-candidate counts. If `Pass Actions` /
  `Fail Actions` columns are present but row candidates are `0`, the payload is
  treated as editor-layout evidence only. This is intentionally not treated as
  closed row semantics yet; the actual pass-action/inserted-injection row
  decoder remains the next black-box closure layer.
- `M2 Report Formula Targets`: concrete target list for the
  `Report workbook/formula extraction` workstream. It maps each report-formula
  closure topic to its report template, report sheet(s), DB field contract,
  formula ID, extraction target, source document, and readiness state. Rows are
  expanded by device model so `Report_VTCC_V2_12` and `Report_VATCC_V1_01`
  branches remain explicit.
- `M2 Report Extraction Plan`: execution checklist generated from the report
  targets. It records the exact report template/sheet to inspect, the
  extraction steps for `ReportFormulaObject`, `SpreadSheetData` / FormulaOne,
  number formats, DB-field traces, the expected validation outputs, and which
  black-box contract must be updated after evidence is captured. This is still
  a planned extraction layer; it does not claim the FormulaOne evidence has
  already been extracted.
- `Test Knowledge Nodes`: stable TKN model rows for downstream generation,
  indexing, and method/report design.
- `Cross-KB Mapping`: explicit `FOQ -> method -> report -> formula` bridge rows.
- `Generation Strategy`: method/report/config generation guardrails from
  `CMBX_GENERATION_STRATEGY_KB.md`.
- `TCC Relationship Model`: structured execution-order, dependency,
  shared-resource, and intent-rule rows from `TCC_TEST_RELATIONSHIP_MODEL.md`.
- `Selected Relationship Audit`: per-export/per-filter relationship rows mapped
  back to each selected alignment record and current intent, so a review packet
  can show why a specific test is or is not independently editable.
- `Relationship Resolution Choices`: hard relationship rules converted into
  decision options, evidence-to-capture notes, and default recommendations.
- `Selected Resolution Choices`: the subset of those decisions that applies to
  the currently exported/filtered alignment rows and intent.
- `Resolution Decision Register`: fillable rows for the same selected decisions,
  with empty `Selected Option`, `Evidence Path`, and reviewer-owner fields plus
  an initial `Decision Status` of `Open`.

## Test Knowledge Node Model

`TestKnowledgeNode` is the normalized knowledge object derived from an
alignment row. It is intentionally smaller and more stable than
`FoqAlignmentRecord`.

| Field | Meaning | Primary source |
|---|---|---|
| `test_id` | Stable ID, for example `TCC_ACC_01` | Generated from family + TestIntent |
| `test_name` | Test name | FOQ KB / alignment row |
| `foq_section` | FOQ section or sequence-row reference | FOQ KB / current normalized map |
| `purpose` | Why the test exists | FOQ KB |
| `acceptance_criteria` | Criteria with type when known | FOQ KB + report/DB contract |
| `instrument_method` | Bound CM instrument method | CMBX method evidence |
| `report_template` | Bound report template | CMBX/report evidence |
| `formula_id` | Stable formula contract ID | Formula KB / alignment rule |
| `model_applicability` | Applicable module models | FOQ KB |
| `dependencies` | Required hardware, RetTimes, channels, audit/config paths | FOQ KB + CMBX config/method evidence |
| `irc_injected` | Whether IRC/corrective processing is involved | Processing method binding |

Acceptance criteria are only normalized where we have source-backed knowledge.
Rows that still need FOQ/report extraction say `Not normalized from FOQ KB yet`
instead of guessing.

## Cross-KB Mapping

The second-stage bridge table connects the knowledge node to the four KB layers
that must agree before generation can be trusted:

```text
FOQ test item -> CMBX method binding -> CMBX report binding -> formula contract
```

Example normalized TCC rows:

| FOQ test | CMBX method | CMBX report/template | Formula ID |
|---|---|---|---|
| Temperature Accuracy | `TEMPERATURE_ACCURACY` | `Report_VTCC_V2_12` / `Temp Accuracy` | `FORMULA_TCC_TEMP_ACCURACY_MAX_DEVIATION` |
| Temperature Stability and PCC | `TEMPERATURE_STABILITY_AND_PCC_70_H` | `Report_VTCC_V2_12` / `Temp Stability_Noise`, `PCC` | `FORMULA_TCC_TEMP_STABILITY_AND_PCC_COOLDOWN` |
| HeatUp and CoolDown | `TEMP_HEAT_UP_DOWN_20_50_20` | `Report_VTCC_V2_12` / `HeatUp&CoolDown` | `FORMULA_TCC_HEATUP_COOLDOWN_RETTIME_DELTA_MINUS_HOLD` |

VDAD rows are currently alignment placeholders until reference VDAD/VMWD CMBX
method and report evidence are decoded. Their `mapping_status` should remain
`open verification` instead of being treated as runnable generation input.

## CMBX Generation Strategy KB

The strategy KB is maintained in:

```text
cmbx_data_explorer/docs/CMBX_GENERATION_STRATEGY_KB.md
```

It contains four practical rule families:

- Method generation rules.
- Report formula and template-selection rules.
- Cross-module dependency rules.
- Configuration validation rules.

This file is the bridge from knowledge alignment toward generation. It should
be updated whenever a new FOQ KB, decoded CMBX method, decoded report formula,
or live CM configuration check turns an `open verification` rule into verified
evidence.

## Historical Design Note

The `FOQ KB to Run` tab is a knowledge alignment workspace. It starts from FOQ
TD test items and aligns each one to:

```text
TD intent
-> sequence injection
-> instrument method script contract
-> processing method binding
-> report sheet/formula contract
-> design questions that still need human confirmation
```

This tab intentionally does not pretend that a full runnable Chromeleon method
can be generated from a short user sentence. Its purpose is to make the reverse
path reviewable before generation.

## Current Scope

Current high-confidence alignment:

```text
Family: TCC
FOQ TD: FOQ Test Description (FOQ_TD) - VX-C10-A
TD source file: FOQ_Testdescription_VX-C10-A.docm
TD metadata: subject VX-C10-A; manager lists VH-C10-A and VC-C10-A
Reference CMBX: 6000001.cmbx
Rows: 13 FOQ injections from Column ID through Error Log Check
```

The tab therefore should not be read as a `VH-C10-A`-only design surface. It is
a common TCC FOQ TD alignment table. Concrete device variants still need their
own method/report evidence before generation.

The tab lists the TD item, injection name, instrument method, processing method,
and report sheet(s). Selecting a row shows:

- TD intent.
- Chinese TD/test explanation for easier review.
- Method script contract.
- Chinese method-script implementation relationship.
- Report calculation contract.
- Chinese report-calculation relationship.
- Design questions / human decisions.

Examples of design questions:

- For a custom temperature accuracy point, what baseline/approach temperature
  should be used?
- Which manual operator prompts are required by TD and which are optional?
- Which processing method must be preserved because IRC can modify report data?
- Which report template/sheet is the source of truth for this device variant?

## Export

`Export Alignment Excel` writes:

```text
<Output Folder>/foq_kb_to_run/FOQ_TD_VX-C10-A_FOQ_KB_to_Run.xlsx
```

The workbook is a review artifact, not a runnable CMBX. It is intended to be
the shared checklist before designing or generating method/report assets.

The workbook includes both English and Chinese columns. The Chinese columns are
not a translation-only layer; they are meant to state the practical meaning:
what the test proves, what the instrument method must emit, and how the report
consumes that evidence.

## Method Script Meaning

For method generation, the important unit is not a copied script fragment. The
important unit is this contract:

```text
TD test logic
-> required instrument configuration and CM symbols
-> method stages and commands
-> generated evidence: RetTimes, audit properties, raw channel data
-> report formulas and workbook-derived pass/fail cells
```

For example, `Temperature Accuracy` is not simply "set 40 C and read a value."
The TD/method/report contract is:

```text
Approach the target from a confirmed baseline or previous state.
Wait until CC and external upper/lower thermometers are stable.
Write the RetTime that marks the stable measurement window.
Report averages external thermometer channels over RetTimeN-1.0..RetTimeN-0.2.
Report chooses the larger upper/lower deviation and compares it to the TD limit.
```

This is why custom requests such as "accuracy at 40 C" still need one design
decision: the baseline/approach path must come from TD evidence or user
confirmation. If that rule is not encoded, the tool should show it as an open
question instead of guessing.

## Updating With New FOQ TDs

When a new module FOQ TD is available, update this alignment at the same level:

```text
TD title and metadata
TD test item
Chromeleon sequence injection
instrument method script name
processing method binding if IRC is involved
report template/sheet/formula evidence
Chinese explanation of the test logic
open design questions
```

This lets VA, VC, VH, and future module FOQs be added without treating one
reference device name as the knowledge-base name.

## Relationship To Generation

The intended workflow is:

```text
1. Pick a FOQ TD item.
2. Confirm injection/method/report alignment.
3. Resolve the listed design questions.
4. Generate or draft method/report assets only after that alignment is clear.
```

For example, `Temperature Accuracy` is aligned to:

```text
Injection: Temperature Accuracy_H
Instrument method: TEMPERATURE_ACCURACY
Processing method: ACCURACY_IRC_STOP_H
Report sheet: Temp Accuracy
```

But a custom single-point test still needs a confirmed approach/baseline
temperature. The tool should not infer whether a 120 C test approaches from
80 C, 20 C, or another state unless that rule is encoded from TD/method evidence.
