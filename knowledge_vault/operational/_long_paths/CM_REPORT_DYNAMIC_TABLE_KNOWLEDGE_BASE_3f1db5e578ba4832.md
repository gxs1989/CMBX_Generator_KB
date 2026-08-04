# CM Report Dynamic Table Knowledge Base

**Status:** Native schema evidence established; Audit Trail and Peak Summary creation implemented.  
**Evidence:** 83 `ReportTableObject` instances decoded from TCC, VVWD, VAS, pump and valve/pressure report templates.  
**Schema inventory:** `outputs/report_table_schema_inventory.md` and `outputs/report_table_schema_inventory.json`.

## 1. Design Model

A Chromeleon report table is not a group of prefilled spreadsheet rows. It has two layers:

```text
ReportTableObject
├─ runtime row source
├─ table properties: filter, sort, channel/component/injection selection
├─ report columns: CM report formulas, headers, units and source selectors
└─ FormulaOne worksheet range: design-time location and formatting surface
```

The Report Designer's **Insert > All Tables** command creates a native table schema. The table body expands at evaluation time according to its row source. Editing a report column changes its CM report formula; it is not the same as writing a FormulaOne formula into a normal cell.

## 2. Observed Native Schemas

| `ReportTableType` | Native runtime type | Observed count | Row source | Processing dependency |
|---|---|---:|---|---|
| `audittrail` | `AuditTrailReportTable` | 9 | Instrument audit entries of the current injection | No peak integration dependency |
| `peak_summary` | `SummaryReportTable` | 69 | Injections selected by table filters; optional selected/fixed peaks | None for injection/audit formulas; required for `peak.*` results |
| `integration` | `IntegrationReportTable` | 5 | Integrated peaks of the current injection/channel | Yes |

The Help lists further table families, including Consolidated, Test Cases, Component, Peak Group, Detection Settings, Calibration History, SST/IRC, Instrument Method, Data Audit Trail, Audit Trail Events, Fraction and Tube tables. They require additional native schema evidence before creation is enabled.

## 3. Audit Trail Table

### Runtime meaning

The Audit Trail table reports commands, messages, warnings, errors and logged properties that occurred before or during the run. Native options select:

- audit level;
- run and/or precondition entries;
- Day Time display and format;
- device display.

It has native event columns rather than arbitrary `Table Column` formulas. For valve-cycle reporting, the method must log the valve property or emit an informative message. The table can then expand to one row per matching audit entry.

### Generation implication

This is the preferred dynamic table for:

- valve switch time and logged position;
- trigger/protocol messages;
- errors and warnings;
- device property changes recorded in the audit trail.

It does not require a Processing Method.

## 4. Peak Summary Table

### Runtime meaning

Peak Summary compares data across injections. Injections define rows. Every report column contains:

- CM report formula;
- header formula;
- unit/dimension formula;
- optional fixed channel/component selection;
- optional selected/fixed peak selection.

Chromeleon Help explicitly allows arithmetic combinations of report variables in a column, for example `peak.height / peak.amount`.

### Dependency split

| Column formula family | Required runtime evidence |
|---|---|
| `injection.*`, `seq.*`, verified `AUDIT.*` | Matching injection/sequence/audit data |
| `chm.*` | Matching acquired channel and time/data contract |
| `peak.*` | Processing Method integration and matching peak/channel/component selection |

A table may serialize correctly while showing `n.a.` if its runtime evidence is absent.

## 5. Integration Table

Integration rows are peaks from the current injection. The PressureEvaluation reference proves that a virtual pressure channel can be integrated and displayed with custom columns, including `peak.*` and audit formulas. However, the report table does not create those peaks. The Processing Method must integrate the selected virtual channel first.

Creation remains blocked until the MD contract can declare and validate:

1. Processing Method identity/integration availability;
2. table channel-selection mode and fixed channel;
3. include/exclude unknown and identified peaks;
4. peak/component selection;
5. column formulas and header formulas.

## 6. Sheet Templates vs. Report Tables

**Insert Sheet > Thermo Scientific Template** copies a whole predefined sheet such as Overview, Integration or Calibration. This can include layout, plots and tables. It is a convenience template, not a new calculation engine.

**Insert > All Tables** inserts a single native report table. This is the better reverse-engineering boundary for independent MD-to-CMBX generation because table type, columns and properties can be modeled explicitly.

## 7. Implemented MD Contract

The canonical syntax is defined only in `CM_REPORT_TEMPLATE_MD_TO_CMBX_SPEC.md`:

- `### Dynamic Table: <range>` with `table_type: audittrail`;
- `### Dynamic Table: <range>` with `table_type: peak_summary`;
- repeated `#### Table Column: <name>` blocks for Peak Summary columns.

The compiler uses verified native XML skeletons only as serialization schema carriers. Business formulas, columns, options, sheet names and ranges come from the MD.

## 8. Open Verification

| Item | Why open | Required evidence |
|---|---|---|
| Integration creation | Report depends on integrated peak rows | Processing Method contract plus CM import/evaluation test |
| Peak Summary custom injection queries | Query tree has nested native objects | Controlled query examples and CM round trip |
| Fixed peak/multi-peak selection | Selection changes table width and headers | Native examples and CM round trip |
| Dynamic column number formats | Formatting is partly stored in FormulaOne/table attributes | Controlled before/after report pair |
| Other table families | Distinct runtime data models | One verified standalone reference per type |
| Plots | Separate `PlotObject` schemas and links | Controlled plot references and CM round trip |
