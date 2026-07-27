# Feature: CMBX Package Browser

## Purpose

Provide a Chromeleon-independent first look into a CMBX package: sequences, injections, channels, audit trails, methods, processing methods, and reports.

## User Workflow

1. Use the app workspace as the fixed working area:

```text
C:\ProgramData\CMBX Data Explorer Workspace
  packages
  cache
  exports
  db
  reports
  logs
```

2. Put source CMBX packages under `packages`, or choose another package folder.
3. Click `Scan CMBX`. The scanner recursively finds `.cmbx` files in that folder and nested folders. Individual `.cmbx` files can still be added as a convenience.
4. Inspect the package summary.
5. Select a CMBX, sequence, injection, or channel from the `Sequence Data` tree.
6. Review available channels, audit trails, report context, and method/report associations.

## Main Modules

```text
app.py
cmbx_container.py
export_service.py
```

## Inputs

- A CMBX export folder scanned recursively for `.cmbx` files, or one or more individual CMBX files.
- `header.xml` inside the CMBX package.

## App Workspace

The app deliberately does not mirror Chromeleon's imported DataVault tree. Chromeleon has already unpacked/imported data into a logical DataVault. This tool reads exported `.cmbx` packages directly, so it uses its own fixed working folder:

```text
C:\ProgramData\CMBX Data Explorer Workspace
```

The machine-wide default can be overridden with `CMBX_DATA_EXPLORER_WORKSPACE` when a lab or CI machine needs a different fixed drive.

Planned layout:

| Folder | Purpose |
| --- | --- |
| `packages` | Source `.cmbx` files copied/exported from CM or other locations. |
| `cache` | Parsed headers, raw-channel decode cache, workbook preview cache, and future formula/runtime caches. |
| `exports` | User-facing exports: raw TSV/XLSX, audit workbooks, report sheets, method workbooks. |
| `db` | FOQ DB workbooks and future SQL import-ready files. |
| `reports` | Optional generated report-template/report-sheet artifacts when separated from general exports. |
| `logs` | Future app run logs and diagnostics. |

Resolution order for package scanning:

```text
CMBX_RAW_DATA_FOLDER environment variable
-> CMBX_DATA_EXPLORER_WORKSPACE\packages
-> C:\ProgramData\CMBX Data Explorer Workspace\packages
```

## Outputs

- UI tree and detail panels.
- Optional raw package-entry exports through `Export Selected`.

## Current Behavior

- Reads CMBX entries without needing Chromeleon.
- Loads each CMBX package with a single full-file read for header/entry discovery.
- Caches common package element lists such as sequences, injections, channels, audits, methods, and reports.
- Scans multiple CMBX packages in parallel from the UI worker.
- Shows scanned CMBX packages as top-level roots in the `Sequence Data` tree.
- Parses `header.xml` into a parent/child element tree.
- Classifies common Chromeleon item types.
- Keeps method/report objects separate from injection child channels, while showing per-injection context in the detail panel.

## Known Limits

- The CMBX container is ZIP-like, but not treated as a normal complete ZIP archive.
- Some useful metadata lives in binary sequence command payloads and needs additional parsers.
- Package inspection does not itself decode raw signal or audit payloads.

## Verification

- Unit tests cover header parsing, package summaries, and element classification.
- Validated manually with `6545327.cmbx` and `20260701_New` CMBX data.
