# KB Migration and Runtime-Path Manifest

## Current Migration Mode

`navigation-only`

The `00_Business_View` tree adds Web-workflow navigation without moving existing
knowledge files. This is deliberate: the application currently resolves legacy
paths directly.

## Runtime-Critical Legacy Paths

| Path | Current consumers |
|---|---|
| `FOQ Template` | Method CMBX carrier selection, 7.2/7.3 packaging, compiler examples |
| `Method Script Generator/Generator Spec` | Method authoring packages and preflight rules |
| `Method Script Generator/TCC/report_template_cmbx` | Report carriers, formula catalog, report compiler, help-catalog builder |
| `KB_Online_GPT` | Desktop/Web Method and Report context packaging and automatic generation |
| `FOQ/<module>` | FOQ alignment, test knowledge, method/report contracts |
| `CMBX Method Scripts` | decoded method-script lookup where available |

## Required Checks Before Physical Migration

1. Replace direct path constants with a central KB path registry.
2. Preserve compatibility fallbacks for one release.
3. Rebuild full and small Online GPT packages.
4. Run Method MD preflight and CMBX generation for CM 7.2 and 7.3.
5. Run Report MD preflight and report-template CMBX generation.
6. Verify Formula Finder and Direct CM formula catalog.
7. Verify FOQ Quick Check knowledge/mapping lookup.
8. Verify Obsidian links and update the root `KB_INDEX.md`.

Until all checks pass, business-view notes are navigation links only.
