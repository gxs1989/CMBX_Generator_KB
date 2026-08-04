# CM Report Dynamic Table Knowledge Base

**Status:** Native schema evidence established; Audit Trail, Peak Summary, and Integration creation implemented.  
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

It has native event columns rather than arbitrary `Table Column` formulas. For valve-cycle reporting, the method must log the valve property or emit an informative message. The table then expands to the complete set of audit entries admitted by the selected audit level and run/precondition options.

Chromeleon Help confirms that this table has no command-text, property-path, device-name or regular-expression row predicate. A logged valve event can be included, but it cannot be isolated from other accepted run entries by the native table.

### Generation implication

This is the preferred dynamic table for:

- complete run audit evidence that includes valve switches and logged positions;
- trigger/protocol messages;
- errors and warnings;
- device property changes recorded in the audit trail.

It does not require a Processing Method.

It is not the correct table for an exact business view containing only switch time and valve positions. For a finite known schedule, use fixed report rows and verified timed `AUDIT.UpperValve.CurrentPosition(...)` / `AUDIT.LowerValve.CurrentPosition(...)` formulas. For a runtime-variable number of exact rows, use a verified dynamic measurement source plus Processing Method results, or filter the audit externally.

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

Integration rows are peaks from the current injection. The PressureEvaluation reference proves that a virtual pressure channel can be integrated and displayed with custom columns, including `peak.*` and audit formulas. The report table does not create those peaks. The Processing Method must integrate the selected virtual channel first.

The implemented MD contract requires:

1. exact `processing_method` identity;
2. `requires_processing: true`;
3. a non-empty integrated `fixed_channel`;
4. identified/unidentified peak inclusion;
5. formula-defined columns whose count matches the table width.

For valve switching, the verified runtime contract is:

```text
VirtualChannel PumpPressureVirtual
-> PressureSpikeEval
-> integrated pressure-spike peak
-> peak.retention_time("detected")*60
-> audit.ColumnComp.UpperValve.CurrentPosition
-> audit.ColumnComp.LowerValve.CurrentPosition
```

This produces the requested business table without unrelated Audit Trail rows. Compile/reopen/reverse-decode is automated. CM runtime evaluation remains necessary because peak detection depends on the injection's assigned Processing Method and its integration settings.

## 6. Sheet Templates vs. Report Tables

**Insert Sheet > Thermo Scientific Template** copies a whole predefined sheet such as Overview, Integration or Calibration. This can include layout, plots and tables. It is a convenience template, not a new calculation engine.

**Insert > All Tables** inserts a single native report table. This is the better reverse-engineering boundary for independent MD-to-CMBX generation because table type, columns and properties can be modeled explicitly.

## 7. Implemented MD Contract

The canonical syntax is defined only in `CM_REPORT_TEMPLATE_MD_TO_CMBX_SPEC.md`:

- `### Dynamic Table: <range>` with `table_type: audittrail`;
- `### Dynamic Table: <range>` with `table_type: peak_summary`;
- `### Dynamic Table: <range>` with `table_type: integration` plus Processing Method and fixed-channel contract;
- repeated `#### Table Column: <name>` blocks for Peak Summary and Integration columns.

The compiler uses verified native XML skeletons only as serialization schema carriers. Business formulas, columns, options, sheet names and ranges come from the MD.

## 8. Open Verification

| Item | Why open | Required evidence |
|---|---|---|
| Integration runtime result | Peak detection depends on assigned Processing Method settings and raw virtual-channel data | CM import/evaluation test using `PressureSpikeEval` and `PumpPressureVirtual` |
| Peak Summary custom injection queries | Query tree has nested native objects | Controlled query examples and CM round trip |
| Fixed peak/multi-peak selection | Selection changes table width and headers | Native examples and CM round trip |
| Dynamic column number formats | Formatting is partly stored in FormulaOne/table attributes | Controlled before/after report pair |
| Other table families | Distinct runtime data models | One verified standalone reference per type |
| Plots | Separate `PlotObject` schemas and links | Controlled plot references and CM round trip |

## 9. Native Boundary and External Event Tables

Official CM Help describes Report Tables as typed runtime row sources. The complete list includes Integration, Peak Summary, Consolidated, Test Cases, processing-method tables, instrument-method tables, audit tables, Fraction and Tube tables. It does not include a normal chromatogram table that emits one row per raw point, nor a generic table whose rows are created by an arbitrary formula condition.

This creates a strict separation:

```text
report-column formula = calculate the current row
native report-table type = decide which rows exist
```

Without peak integration, CM can dynamically list Instrument Audit Trail entries. It cannot natively reduce that table to only valve-position changes because its report-table filter is limited to audit level, run/preconditions, and Day Time/Device display options. `Audit Trail Events` is a different sequence/data-audit event family and is not a generic replacement for instrument command/property events.

Raw channels remain fully useful without CM integration for scalar/window calculations and plots:

- `chm.signalValue(time)`;
- `chm.signalStatistic(...)` / `chm.sig_value(...)`;
- `chm.noise(start, end)`;
- `chm.drift(start, end)`;
- fixed time-grid rows designed in advance.

They do not create a runtime-variable row count. Arbitrary raw/audit event extraction therefore belongs in an external report engine unless the event is first mapped to a verified native CM row source.

Recommended external event-table contract:

1. choose `raw_channel` or `instrument_audit` as the source;
2. define a typed event predicate instead of a display formula;
3. define edge direction, debounce/hysteresis and minimum spacing for raw signals;
4. define event grouping for related audit changes such as upper/lower valve positions;
5. calculate table rows and summaries outside CM;
6. retain source traceability back to package, sequence, injection, channel/audit record and method command.

The external engine may reproduce verified CM formula semantics where parity is required, but it should use structured operations internally rather than evaluating arbitrary CM formula text.
