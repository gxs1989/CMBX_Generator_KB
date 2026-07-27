# Online Web-Model Knowledge Base

This directory publishes self-contained KB packages for web AI products.

## Directory Layout

```text
00_Maintenance/                    Rules, status and validation findings
01_Build_Sources/<Module>/Method/  Module-specific Method build evidence; never upload
01_Build_Sources/Report/           Shared Report language sources plus module evidence
02_Full_Context/<Module>/Method/   Complete three-file Method package
02_Full_Context/Report/            One universal Report SPEC plus module evidence folders
03_Small_Context/<Module>/Method/  Size-limited three-file Method package
03_Small_Context/Report/           Same universal Report SPEC plus compact module evidence
```

Current modules:

| Module | Method package | Report package |
|---|---|---|
| TCC | Full + small context | VTCC/Pressure original evidence and summaries built; VATCC inventory remains missing |
| VAS | Full + small context | Original report inventory built; semantic summary still open |
| VDAD_VMWD | Not built; representative method CMBX missing | Not built |
| VVWD | Method evidence incomplete | Original report inventory built; semantic summary still open |
| Pump | Method evidence incomplete | Original report inventory built; semantic summary still open |

## Upload Contract

For Method, upload exactly three files from one module:

1. `01_*_SPEC.md`
2. `02_*_ORIGINAL_*.md`
3. `03_*_SUMMARIES.md`

For Report, upload:

1. `Report/01_REPORT_SPEC.md` (shared by every HPLC module)
2. `Report/<Module>/02_REPORT_ORIGINAL_TEMPLATES.md`
3. `Report/<Module>/03_REPORT_SUMMARIES.md`

Do not upload `00_Maintenance` or `01_Build_Sources`. Do not mix an ORIGINAL
collection from one module with a SUMMARY from another. There is only one
Report SPEC; module differences belong exclusively in ORIGINAL and SUMMARY.

Use `02_Full_Context` when the model accepts the complete evidence package.
Use `03_Small_Context` when per-file or context limits are smaller. Every small
file must remain below 200,000 bytes and must include a self-index and scope.

## Evidence Policy

- Decoded CMBX method rows are executable evidence.
- Derived method summaries explain intent and reusable roles, but do not
  override decoded command spelling, timing, branches, or service strings.
- Generated output still requires local preflight, CMBX compilation,
  Chromeleon import/open, and CM Method Check.
- Report generation is carrier-based. Existing report objects and existing
  FormulaOne cells can be patched; structural workbook creation is outside the
  current verified boundary.
