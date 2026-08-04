# Database Upload Tab

## Purpose

The Database Upload tab uploads exported FOQ DB workbooks to SQL Server.

It supports manual upload of multiple DB workbooks and is also used by the FOQ DB tab's direct candidate upload workflow.

## Configuration

Default V1.2 configuration:

```text
Server: 10.68.178.52
Database: QCLab
User: QCUser
Schema: dbo
Table: AUTO
Driver: ODBC Driver 17 for SQL Server
```

The password is entered in the UI or supplied through `CMBX_DB_PASSWORD`. Saved configuration does not store the password.

## Upload Model

Each FOQ DB workbook represents one sequence DB row.

The uploader reads the `DB Data` sheet:

```text
row 1 -> SQL column names
row 2 -> values for one sequence
```

When table is `AUTO`, the uploader resolves the target table from `DeviceType` and `MappingSheet`.

## Table Creation

If the target table does not exist, V1.2 creates a FOQ-style table:

- `ID int identity primary key`
- `TestDate datetime2(0)`
- known metadata fields such as `Serial`, `TimeBase`, `ModelNo`, `ModelVariant`, and `Firmware` as `nvarchar(30)`
- numeric DB fields as `float`
- result fields as `nvarchar(30)`

If the table already exists, only existing matching columns are inserted.

## Logging

The tab log reports:

- connection test status
- target database/schema/table
- table creation
- skipped fields not present in an existing table
- string truncation required to fit existing column widths
- per-workbook upload result

## Implementation Boundary

SQL-specific behavior lives in `db_upload_service.py`. The UI only collects configuration and file selections.
