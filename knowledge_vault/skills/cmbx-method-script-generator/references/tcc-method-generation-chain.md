# TCC Method Generation Chain

This reference connects the already-built TCC KB to method-script generation. Use it to avoid treating existing knowledge as missing.

## Existing KB To Connect

Read or search these local sources before generation:

| Layer | Preferred source |
|---|---|
| FOQ purpose and applicability | `C:\ProgramData\CMBX Data Explorer Workspace\KB\FOQ\TCC\FOQ_TCC_VX_C10_A_TD_KNOWLEDGE_MANAGEMENT.md` |
| Test logic | `C:\ProgramData\CMBX Data Explorer Workspace\KB\FOQ\TCC\FOQ_TD_TEST_LOGIC_KNOWLEDGE_BASE.md` |
| Test nodes / bindings | `cmbx_data_explorer/docs/TCC_TEST_KNOWLEDGE_NODE_MODEL.md` |
| Method roles | `cmbx_data_explorer/docs/TCC_METHOD_ROLE_CONTRACTS.md` |
| Method command rendering | `cmbx_data_explorer/docs/CM_METHOD_COMMAND_KNOWLEDGE_BASE.md` |
| Black-box contracts | `cmbx_data_explorer/docs/TCC_*_BLACK_BOX_DECOMPOSITION.md` |
| Full source method scripts | `C:\ProgramData\CMBX Data Explorer Workspace\KB\CMBX Method Scripts\TCC\**\*_embedded_method_flow.tsv` |

## Intent Interpretation Rules

| User phrase | Primary intent | Related knowledge |
|---|---|---|
| `accuracy at 40 C` | `temperature_accuracy` | Accuracy ladder, external thermometer report formulas |
| `from 20 C stable to 40 C test accuracy` | `temperature_accuracy` | Baseline/pre-equilibration + accuracy target |
| `from 20 C stable to 40 C test stability` | `temperature_stability` | Baseline/pre-equilibration + stability hold/report window |
| `stability at 80 C` | `temperature_stability` | Stability method target role; report window review |
| `precision plus stability at 50 C` | composite: `temperature_precision` + `temperature_stability` | Merge/cross-test plan; not a blind script splice |
| `valve every 5 s while holding 70 C` | composite: `temperature_stability` + `valve_stress` | Trigger commands and valve-position logging are required |

When the user uses both stability and accuracy words, classify by the measured result:

- If the requested result is accuracy, route to accuracy and treat earlier stable state as baseline.
- If the requested result is stability, route to stability and treat earlier temperature as baseline/pre-equilibration.

## TCC Method Role Map Essentials

### Accuracy

| Role | Row pattern | Notes |
|---|---|---|
| Model branch | `ColumnComp.ModelNo=...` | Selects VH/VC/VA ladder/page behavior. |
| Temperature ladder | `Variables.GenericDouble*` | Do not edit one observed setpoint without understanding ladder/report cells. |
| Measurement target | `ColumnComp.CC.Temperature.Nominal Variables.GenericDouble*` | Uses ladder variables, not literal values. |
| RetTime anchors | `RetTimes.RetTimeN = System.Retention` | Report formulas use these anchors. |
| External thermometer acquisition | `Thermometer*` channels | Accuracy report depends on external reference. |
| VH PCC command | `ColumnComp.CmdString Cmd="PCC.TempCtrl=0"` | Preserve unless designing a new VH PCC behavior. |

### Stability / PCC

| Role | Row pattern | Rule |
|---|---|---|
| CC stability target | `ColumnComp.CC.Temperature.Nominal = <target>` | Editable target role for custom stability. |
| Baseline/pre-equilibration | Insert before target setpoint when user says `from/before/after stable at X`. | Set CC nominal to baseline, wait ready, delay requested time. |
| Report window | Existing report uses fixed late stability window. | Shortened or shifted duration needs report redesign. |
| VH PCC branch | `ColumnComp.PCC.Temperature.Nominal`, PCC triggers, PCC RetTimes | Do not edit for CC stability target unless user explicitly requests PCC redesign. |
| External thermometer channels | `Thermometer1.ExtTemp_*` | Preserve for FOQ stability unless user explicitly changes sensor contract and report is redesigned. |

### HeatUp/CoolDown

| Role | Pattern | Rule |
|---|---|---|
| Transition endpoints | temperature nominal changes + RetTimes | Edit as transition role, not as accuracy/stability points. |
| Stable-hold subtraction | report uses hold-time adjustment | Method and report must change together. |

### Valve Stress

| Role | Pattern | Rule |
|---|---|---|
| Cyclic action | `System.Trigger` with rearm/interval conditions | Use trigger commands, not repeated manual rows, when periodic switching is requested. |
| Valve command | `ColumnComp.UpperValve.CurrentPosition`, `ColumnComp.LowerValve.CurrentPosition` | Preserve valid CM position values from KB examples. |
| Valve logging | `Log` or audit-visible position evidence | Add/verify logging when user asks to log valve position. |

## Script Generation Rules

1. Build a structured spec with `baseline_c` and `target_c` as separate fields.
2. Select a source method from KB by method role, not from current UI selection unless explicitly requested.
3. Render full source method script from embedded flow TSV.
4. Classify rows by role.
5. Apply changes only to matching editable roles.
6. Insert baseline/pre-equilibration blocks before target measurement when required.
7. Mark all inserted or modified rows.
8. Run report contract check:
   - RetTime anchors still exist?
   - required raw/audit channels still acquired?
   - report time window still covers requested measurement?
   - DB/display precision still valid?

## Required Review Language

Before showing the modified script, present a plain-language contract the user can edit:

```text
Use <source method> as the base.
Preserve <locked roles>.
Change <editable role> from <old> to <new>.
Insert <baseline block> before <target block>.
Report impact: <valid / requires redesign>.
Open verification: <items>.
```

Only after the user accepts this contract should the UI generate or export a full modified method script.
