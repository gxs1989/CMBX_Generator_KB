# Audit Trails Tab

## Purpose

The Audit Trails tab lists audit trail objects for the selected sequence or injection and previews the selected audit in a CM-like table.

- Selecting a sequence clears any previous injection-specific context and shows all audit trails in that sequence.
- Selecting an injection shows only the audit trail objects belonging to that injection.

## Internal CM-Like Preview

The lower `CM Audit Trail Preview` table follows the Chromeleon audit report shape:

```text
row number / Day Time / Ret. Time / Command/Message
```

It also adds the top metadata block:

- Injection Name
- Injection Type
- Instrument Method
- Processing Method
- Injection Time
- Run Time
- Channel

Day Time handling:

- The decoder exports `DayTime` when the Chromeleon audit message object exposes a timestamp-like property.
- If at least one row has both `DayTime` and `Ret. Time`, the preview infers injection start time as `DayTime - Ret. Time` and fills missing `DayTime` rows from that start time.
- If the raw audit object does not expose a timestamp, `DayTime` remains blank.

## User Actions

- Click `Export Selected Audits` to export selected audit trails as styled CM-like `.xlsx` preview workbooks.
- Double-click a row to export and open the styled audit workbook.
- Select a row to preview it internally.

## Output

Styled preview exports are written below:

```text
<output folder>/<sequence name>/_preview/audit_previews/<injection>_audit.xlsx
```

Raw audit TSV exports are still available through the lower-level export service and follow the sequence/injection folder layout:

```text
<output folder>/<sequence name>/<injection name>/<audit name>_audit.tsv
```

## Implementation Boundary

UI behavior lives in `app.py` methods:

- `_build_audit_tab`
- `preview_selected_audit`
- `export_selected_audits`
- `open_selected_audits`

Styled workbook export and internal preview use the same Chromeleon audit decoder through `chromeleon_bridge.export_audit_raw`.
# V1.2 Status

- Audit Trails continue to show injection or sequence audit records.
- Package scanning is faster because CMBX headers are parsed from a single file read and element lists are cached.
- Audit values remain an important source for FOQ device identification through `AUDIT.ColumnComp.ModelNo`.
