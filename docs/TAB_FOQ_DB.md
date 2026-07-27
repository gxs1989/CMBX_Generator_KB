# FOQ DB Tab

## Purpose

The FOQ DB tab builds one database-ready workbook per candidate sequence and can upload those candidate DB rows directly to SQL Server.

It is driven by `FOQResultLocations_V2.83.xls`, not by guessed field names.

## V1.2 Workflow

1. Load or scan the package workspace.
2. Select device and DB field filters from the mapping workbook.
3. Add sequence candidates from `Sequence Data` or from filter matches.
4. Confirm each candidate's report template in the candidate table.
5. Use `Preview` to compare selected DB fields before export.
6. Use `Export Candidate DB` to create one workbook per sequence.
7. Use `Upload Candidate DB` to export and upload those workbooks in one action.

## Candidate Table

The candidate table tracks:

```text
Device / Device Source / Report Template / CMBX / Sequence / Injections / Channels / Source
```

The report template cell is editable through a dropdown per sequence because different modules can carry multiple report templates in one CMBX.

## Preview

Preview uses a batched worker process:

- One worker is started per preview request.
- Jobs are grouped by CMBX package.
- Each package is loaded once.
- Progress and missing-field details are written to `Preview Log`.

## DB Precision

Values written to the DB workbook use report-display precision where verified:

- Temperature accuracy/calibration and PCC accuracy: 2 decimals.
- HeatUp/CoolDown and preheater temperature differences: 1 decimal.
- Noise, slope, and drift fields: 3 decimals.

The workbook keeps numeric cells numeric; the precision step removes binary float tails before SQL upload.

## Upload

`Upload Candidate DB` generates DB workbooks, resolves target SQL tables, and inserts one row per sequence.

With table set to `AUTO`, TCC C10 devices currently route to:

```text
VA-C10-A -> dbo.VTCC
VC-C10-A -> dbo.VTCC
VH-C10-A -> dbo.VTCC
VH-C10-A_GERMERING -> dbo.VTCC_Germering
```

## Implementation Boundary

UI behavior lives in `app.py`; calculation and upload logic are delegated to:

- `export_service.py`
- `foq_contract_report.py`
- `foq_preview_worker.py`
- `db_upload_service.py`
