# TCC Column ID Black Box Decomposition

Extraction date: 2026-07-10

Scope: TCC FOQ Column ID test for `VH-C10-A`, `VC-C10-A`, and the open
`VA-C10-A` method-library branch.

---
Test name: Column ID
Models: VH-C10-A / VC-C10-A / VA-C10-A
Status: method/report/DB contract closed for VC/VH; VA production-sequence
applicability remains open verification
---

This document decomposes the Column ID test as a generation contract. It is not
a raw-signal temperature test. The method verifies that the four column-ID
positions report descriptions `A`, `B`, `C`, and `D`, and the report reads the
same audit properties.

```text
Method guard:
  Column_A.Description == "A"
  Column_B.Description == "B"
  Column_C.Description == "C"
  Column_D.Description == "D"

Report leaves:
  L46 = AUDIT.Column_A.Description(0,"forward")
  L47 = AUDIT.Column_B.Description(0,"forward")
  L48 = AUDIT.Column_C.Description(0,"forward")
  L49 = AUDIT.Column_D.Description(0,"forward")
```

## Evidence Sources

| Evidence | Source |
|---|---|
| Test intent node | `cmbx_data_explorer/docs/TCC_TEST_KNOWLEDGE_NODE_MODEL.md` |
| Injection workbench notes | `cmbx_data_explorer/docs/TCC_INJECTION_BY_INJECTION_REVERSE_WORKBENCH.md` |
| Method/report alignment | `cmbx_data_explorer/docs/TCC_METHOD_REPORT_ALIGNMENT.md` |
| Required symbols | `cmbx_data_explorer/docs/TCC_REQUIRED_SYMBOL_MANIFEST.md` |
| Method flow, VH | `knowledge_base/tcc_reverse_probe/VH/6000001/ColumnID_embedded_method_flow.txt` |
| Method flow, VC | `knowledge_base/tcc_reverse_probe/VC/3000004/ColumnID_embedded_method_flow.txt` |
| Method flow, VA payload | `knowledge_base/tcc_reverse_probe/VA/0000003/ColumnID_embedded_method_flow.txt` |
| Report formula objects | `knowledge_base/tcc_report_formula_objects_vh_6000001_all_sheets.tsv` |
| DB mapping | `foq/FOQResultLocations_V2.83.xls` |

## Executive Answer

1. The instrument method is `ColumnID`.
2. The method is audit/configuration based: it waits for all four card states to
   be OK, logs descriptions A-D, and aborts if any description is wrong.
3. The method intentionally acquires `ColumnComp.CC_Temp` even though the result
   is not temperature based; the method comments state CM needs data from at
   least one channel to evaluate the audit trail in the report.
4. There are no RetTimes and no raw report statistics for this test.
5. The report sheet is `Column ID`; DB fields `RES_ColumnID_A..D` resolve from
   cells `L46:L49`.
6. VC/VH DB mapping is closed. VA has a `ColumnID` method payload, but the
   observed VA production sequence omits the `ColumnIDs` injection; do not add
   the row to a VA generated sequence without confirmation.

## Contract 1: Method Command

### 1.1 Device Branch Binding

| Device | Injection | Instrument Method | Processing Method | Report Template | Report Sheets | Status |
|---|---|---|---|---|---|---|
| VH-C10-A | `ColumnIDs` | `ColumnID` | `CORRECT_STABILITY_INJ_INSERTION` | `Report_VTCC_V2_12` | `Column ID` | sequence evidence closed |
| VC-C10-A | `ColumnIDs` | `ColumnID` | `CORRECT_ACCURACY_INJ_INSERTION` | `Report_VTCC_V2_12` | `Column ID` | sequence evidence closed |
| VA-C10-A | open | `ColumnID` payload exists | open | `Report_VATCC_V1_01` open | open | Open Verification Required |

### 1.2 Method Contract Summary

Decoded method evidence:

```yaml
method: ColumnID
stages:
  - InstrumentSetup
  - StartRun
  - Run
  - StopRun
  - PostRun
initialization:
  model_branch:
    if ColumnComp.ModelNo == VH-C10-A:
      Variables.GenericLong9: 12
      Log: GenericLong9
    else supported non-VH branch:
      Variables.GenericLong9: 10
      Log: GenericLong9
    else:
      Message: column compartment model unknown
      action: System.AbortQueue
  column_compartment:
    ColumnComp.CC.TempCtrl: On
    ColumnComp.CC.Temperature.Nominal: 15 C
    ColumnComp.CC.Mode: StillAir
  end_gate:
    Variables.GenericBool1: 0
    System.Trigger END_RUN: Variables.GenericBool1 = 1
acquisition:
  - ColumnComp.CC_Temp.AcqOn
  - ColumnComp.CC_Temp.AcqOff
```

### 1.3 Command Flow

```yaml
ColumnID_Command_Flow:
  - order: 1
    stage: InstrumentSetup
    command: IF
    condition: ColumnComp.ModelNo = "VH-C10-A"
    result: Variables.GenericLong9 = 12; Log GenericLong9
    note: VH report/page-count branch evidence.
  - order: 2
    stage: InstrumentSetup
    command: ELSE
    condition: supported non-VH branch
    result: Variables.GenericLong9 = 10; Log GenericLong9
    note: VC/non-PCC report/page-count branch evidence.
  - order: 3
    stage: InstrumentSetup
    command: ABORT
    condition: unknown ColumnComp.ModelNo
    result: System.AbortQueue
    note: Stops if the device branch cannot be identified.
  - order: 4
    stage: InstrumentSetup
    command: SET
    target: ColumnComp.CC.TempCtrl / Temperature.Nominal / Mode
    value: On / 15 C / StillAir
    note: Minimal column compartment context.
  - order: 5
    stage: InstrumentSetup
    command: TRIGGER
    target: END_RUN
    condition: Variables.GenericBool1 = 1
    note: Normal completion gate.
  - order: 6
    stage: StartRun
    command: ACQ_ON
    target: ColumnComp.CC_Temp
    note: Provides a data channel so audit report evaluation can run.
  - order: 7
    stage: Run
    command: MESSAGE
    target: operator
    note: Prompts operator to plug column ID adapters in correct positions.
  - order: 8
    stage: Run
    command: WAIT
    condition: Column_A/B/C/D.CardState = OK
    timeout: 2.00 min
    note: Confirms all four slots can see cards.
  - order: 9
    stage: Run
    command: LOG
    target: Column_A.Description, Column_B.Description, Column_C.Description, Column_D.Description
    note: Creates audit properties used by the report.
  - order: 10
    stage: Run
    command: IF_ABORT
    condition: Column_A.Description <> "A" OR Column_B.Description <> "B" OR Column_C.Description <> "C" OR Column_D.Description <> "D"
    result: message + System.AbortQueue
    note: Method-side hard guard; report is not the only pass/fail layer.
  - order: 11
    stage: Run
    command: SET
    target: Variables.GenericBool1
    value: 1
    note: Allows END_RUN trigger to finish sample normally.
  - order: 12
    stage: StopRun
    command: ACQ_OFF
    target: ColumnComp.CC_Temp
    note: Clean acquisition close.
```

### 1.4 RetTime and Channel Semantics

| Item | Status | Reason |
|---|---|---|
| RetTimes | not used | Column ID is an audit-property test. |
| Raw signal result channels | not used | Report pass/fail comes from `AUDIT.Column_A-D.Description`. |
| `ColumnComp.CC_Temp` | acquired but not a result channel | Required as a minimal CM data channel for report/audit evaluation. |
| `Variables.GenericLong9` | branch evidence/helper | Logged value appears tied to device/page-count context, not the physical Column ID result. |

## Contract 2: Processing Method

Known sequence bindings:

| Device | Processing Method | IRC / corrective role | Status |
|---|---|---|---|
| VH-C10-A | `CORRECT_STABILITY_INJ_INSERTION` | corrective processing binding preserved in VH sequence | verified from sequence binding |
| VC-C10-A | `CORRECT_ACCURACY_INJ_INSERTION` | corrective processing binding preserved in VC sequence | verified from TKN/package map |
| VA-C10-A | open | production sequence does not currently include `ColumnIDs` | Open Verification Required |

Processing interpretation:

- The method itself enforces the A/B/C/D check and aborts on mismatch.
- The processing method binding is therefore a sequence-level corrective/IRC
  context, not the primary Column ID result calculation.
- For full-sequence generation, preserve the production binding by device.
- For a standalone Column ID diagnostic package, whether `No_Integration` is
  acceptable remains Open Verification Required.

## Contract 3: Report Formula

### 3.1 `Column ID` Formula Objects

| Cell | Formula | Meaning |
|---|---|---|
| `L46` | `AUDIT.Column_A.Description(0,"forward")` | Description reported by Column ID slot A |
| `L47` | `AUDIT.Column_B.Description(0,"forward")` | Description reported by Column ID slot B |
| `L48` | `AUDIT.Column_C.Description(0,"forward")` | Description reported by Column ID slot C |
| `L49` | `AUDIT.Column_D.Description(0,"forward")` | Description reported by Column ID slot D |

### 3.2 Workbook-Derived Rules

Known evaluator/report rules:

```text
RES_ColumnID_A passes if L46 == "A"
RES_ColumnID_B passes if L47 == "B"
RES_ColumnID_C passes if L48 == "C"
RES_ColumnID_D passes if L49 == "D"
```

Formula flow:

```mermaid
flowchart LR
    Method["ColumnID method"] --> Log["Log Column_A-D.Description"]
    Log --> Audit["Audit trail"]
    Audit --> Sheet["Column ID L46:L49"]
    Sheet --> Result["RES_ColumnID_A..D"]
    Result --> DB["FOQ DB result fields"]
```

## Contract 4: DB Contract

### 4.1 DB Leaves

| Device | DB Field | Report file | Sheet | Cell | Rule |
|---|---|---|---|---|---|
| VH-C10-A | `RES_ColumnID_A` | `ColumnIDs.XLS` | `Column ID` | result from `L46` | passes when `L46 = A` |
| VH-C10-A | `RES_ColumnID_B` | `ColumnIDs.XLS` | `Column ID` | result from `L47` | passes when `L47 = B` |
| VH-C10-A | `RES_ColumnID_C` | `ColumnIDs.XLS` | `Column ID` | result from `L48` | passes when `L48 = C` |
| VH-C10-A | `RES_ColumnID_D` | `ColumnIDs.XLS` | `Column ID` | result from `L49` | passes when `L49 = D` |
| VC-C10-A | `RES_ColumnID_A` | `ColumnIDs.XLS` | `Column ID` | result from `L46` | same as VH |
| VC-C10-A | `RES_ColumnID_B` | `ColumnIDs.XLS` | `Column ID` | result from `L47` | same as VH |
| VC-C10-A | `RES_ColumnID_C` | `ColumnIDs.XLS` | `Column ID` | result from `L48` | same as VH |
| VC-C10-A | `RES_ColumnID_D` | `ColumnIDs.XLS` | `Column ID` | result from `L49` | same as VH |
| VA-C10-A | open | open | open | open | no current VA Column ID DB leaves confirmed |

### 4.2 DB Is a Leaf

```text
ColumnID command flow
-> audit log Column_A-D.Description
-> Column ID report cells L46:L49
-> RES_ColumnID_A..D DB fields
```

The DB contract validates the audit path. It does not define the method command
logic.

## Contract 5: Config Requirement

| Requirement | VH-C10-A | VC-C10-A | VA-C10-A | Failure mode |
|---|---|---|---|---|
| `AUDIT.ColumnComp.ModelNo` source of truth | Required | Required | Required | Wrong branch/page context or method abort |
| Column ID option enabled | Required | Required | open | card state/description properties missing |
| `Column_A.CardState` / `Column_A.Description` | Required | Required | open | A slot cannot be verified |
| `Column_B.CardState` / `Column_B.Description` | Required | Required | open | B slot cannot be verified |
| `Column_C.CardState` / `Column_C.Description` | Required | Required | open | C slot cannot be verified |
| `Column_D.CardState` / `Column_D.Description` | Required | Required | open | D slot cannot be verified |
| Four chip cards with descriptions `A`, `B`, `C`, `D` | Required | Required | open | method aborts or report fails |
| `ColumnComp.CC_Temp` acquisition available | Required | Required | open | report/audit evaluation context may be missing |

Generation implication:

- Do not invent RetTimes for Column ID.
- Do not calculate Column ID from raw temperature data.
- Preserve the method-side abort guard unless intentionally generating a
  non-aborting diagnostic method.
- A generated full VC/VH FOQ sequence should preserve this test if the Column ID
  option is enabled.
- A generated VA sequence must not add `ColumnIDs` automatically until VA
  applicability is confirmed.

## Contract 6: Open Verification

Items below are marked Open Verification Required until the listed evidence is
captured.

| # | Open Verification Required | Why it matters | Needed evidence | Likely source |
|---:|---|---|---|---|
| 1 | VA-C10-A Column ID applicability | VA payload exists, but observed VA production sequence omits `ColumnIDs` and TD extraction is incomplete | VA TD table and a current VA production CMBX | VA TD, VA CMBX |
| 2 | Standalone processing method choice | Full sequence preserves corrective processing, but standalone diagnostic might use `No_Integration` | Processing method XML/pass-action behavior | VC/VH processing method payload |
| 3 | `Variables.GenericLong9` workbook role | It is logged as branch/page-count evidence; exact workbook dependency is not fully parsed | FormulaOne workbook formulas referencing GenericLong9 | report `SpreadSheetData` |
| 4 | Report result cell locations for `RES_ColumnID_A..D` | DB leaves are closed, but exact workbook result cells are derived from evaluator rules rather than fully parsed FormulaOne formulas | workbook parse of `Column ID` sheet | report template |

## VH / VC / VA Comparison

| Aspect | VH-C10-A | VC-C10-A | VA-C10-A |
|---|---|---|---|
| Production injection | `ColumnIDs` | `ColumnIDs` | not observed in current VA sequence |
| Instrument method payload | `ColumnID` | `ColumnID` | `ColumnID` payload exists |
| Processing method | `CORRECT_STABILITY_INJ_INSERTION` | `CORRECT_ACCURACY_INJ_INSERTION` | open |
| Report template | `Report_VTCC_V2_12` | `Report_VTCC_V2_12` | open / `Report_VATCC_V1_01` not verified for this row |
| DB fields | `RES_ColumnID_A..D` mapped | `RES_ColumnID_A..D` mapped | no mapped Column ID leaves confirmed |
| Generation status | reusable with config check | reusable with config check | Open Verification Required |

## Generation Readiness

| Generation action | Status | Notes |
|---|---|---|
| Reuse full VH Column ID row | ready after config validation | Preserve `CORRECT_STABILITY_INJ_INSERTION`, `ColumnID`, and `Column ID` report sheet. |
| Reuse full VC Column ID row | ready after config validation | Preserve `CORRECT_ACCURACY_INJ_INSERTION`. |
| Generate standalone Column ID diagnostic | partial | Need decide processing method and whether method-side abort should remain hard stop. |
| Add Column ID row to VA package | locked | Do not add until VA applicability is confirmed. |
| Modify expected descriptions | locked | A/B/C/D are part of the method abort guard and report contract. |

