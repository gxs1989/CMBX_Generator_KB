# Online GPT KB Maintenance Rules

KB_Version: 1.2  
Updated: 2026-07-23  
Maintainer: Codex with user review

## Delivery Profiles

Every Method or Report KB family has two delivery profiles:

| Profile | Location | Use |
|---|---|---|
| Full context | `02_Full_Context/<Module>/<Family>` | Models that accept the complete three-file evidence package |
| Small context | `03_Small_Context/<Module>/<Family>` | Models with smaller per-file or context limits, including Doubao |

Each Method profile uses exactly three module-local upload files. Each Report
profile uses one shared `Report/01_REPORT_SPEC.md` plus the selected module's
ORIGINAL and SUMMARY files. The small-context profile is not an independent
source of truth. It is a selected derivative of the full-context package.

## Build Layers

| Layer | Responsibility |
|---|---|
| `00_Maintenance` | Rules, source status, model-validation findings and release policy |
| `01_Build_Sources` | Aliased source evidence plus build/profile manifests; never upload |
| `02_Full_Context` | Complete three-file delivery packages |
| `03_Small_Context` | Size-limited three-file delivery packages and optional ZIP files |

## Small-Context Rules

1. A small-context family contains exactly three upload MD files.
2. The default per-file hard limit is `< 200,000 bytes`.
3. SPEC remains complete; ORIGINAL and SUMMARY are selected by stable IDs.
4. The first section of ORIGINAL and SUMMARY must contain a self-index.
5. Scope omissions must be stated explicitly; omitted evidence must never be
   silently reconstructed by the model.
6. The builder writes a manifest under the matching
   `01_Build_Sources/<Module>/<Family>` tree with byte counts and scope.
7. Rebuild the small profile after every full-profile change.

## Validation Finding: Bare Time Rows

Web-model testing showed that a model may emit a numeric time in the first TSV
column and leave the remaining columns empty. Such a row is not an executable
time anchor and is classified as a Comment. The Method SPEC therefore requires
every numeric time row to contain a valid stage, Trigger, command, or property
on the same row.

## Readiness

Full and small profiles are validated separately. A successful small-context
trial proves that selected evidence remains usable after compaction; it does
not prove that tests omitted from that profile are supported.

## Module Separation

Delivery and build paths must always include the module before the artifact
family. Current module codes are `TCC` and `VAS`; future modules include
`VDAD_VMWD`, `VVWD`, and `Pump` only after their source evidence is ready.

```text
01_Build_Sources/<Module>/Method/
02_Full_Context/<Module>/Method/
03_Small_Context/<Module>/Method/
```

TCC and VAS may share the generic Method SPEC, but they must not share original
script or summary collections. VAS originals are rebuilt from `9318349.cmbx`;
the supplied per-method KB files are interpretation evidence and retain their
`not_cm_validated` status.

## Report SPEC Unification

Report authoring uses one module-neutral SPEC because direct CM report
formulas, FormulaOne formulas, workbook formatting, dynamic-table semantics,
carrier cloning and CMBX packaging are common language/compiler concerns.

```text
01_Build_Sources/Report/Common/01_Spec/
02_Full_Context/Report/01_REPORT_SPEC.md
02_Full_Context/Report/<Module>/02_REPORT_ORIGINAL_TEMPLATES.md
02_Full_Context/Report/<Module>/03_REPORT_SUMMARIES.md
03_Small_Context/Report/01_REPORT_SPEC.md
03_Small_Context/Report/<Module>/02_REPORT_ORIGINAL_TEMPLATES.md
03_Small_Context/Report/<Module>/03_REPORT_SUMMARIES.md
```

The universal SPEC embeds the HPLC-relevant official Help catalog and must not
refer to a local Help path as an external dependency. Module applicability,
available carriers, exact cells, audit paths, channels, RetTimes and processing
requirements remain module evidence and must not be promoted into the SPEC.
