# Online GPT KB Source Status

Status_Date: 2026-07-23

## Method Packages

| Module / profile | Status | Evidence |
|---|---|---|
| TCC / Full context | Candidate for controlled web-model validation | Complete current TCC Method SPEC, original-script collection and summaries |
| TCC / Small context | Validated as usable for selected TCC temperature and valve/stress intents | Three files below 200 KB were accepted by Doubao expert mode and produced a mostly correct periodic-valve method |
| VAS / Full context | Built; requires controlled web-model and CM validation | 19 methods decoded directly from `9318349.cmbx`; 19 supplied derived method summaries; VAS TD/test logic and report inventory included as supporting knowledge |
| VAS / Small context | Built; not yet web-model validated | SPEC 44 KB, all 19 decoded originals 105 KB, compact role summaries plus cross-method routing index 138 KB |

Small-context validation found one authoring defect: bare `1.000` and `31.000`
time rows were classified as comments. The SPEC now contains an explicit
prohibition and corrected same-row command examples.

## Rebuild Requirement

Rebuild both profiles for the affected module whenever the Method SPEC, source
CMBX/scripts, role summaries, renderer, or compiler rules change. TCC and VAS
must remain separate upload packages.

## Report Package

| Component | Status | Evidence |
|---|---|---|
| Universal HPLC Report SPEC | Built | MD-to-CMBX contract, formula-language reference and curated HPLC Help catalog merged into one self-contained file below 200 KB |
| TCC Report originals | Draft / incomplete | VTCC evidence is strong; VATCC canonical inventory still missing |
| TCC Report summaries | Draft / incomplete | Formula and audit-table rules exist; consolidated semantic summary remains incomplete |
| VAS Report originals | Built | `VAS_DVAS_V_3_45` formula inventory included |
| VVWD Report originals | Built | `FOQ_REPORT_VVWD_V2_31` formula inventory included |
| Pump Report originals | Built | `Report_VAPump_FOQ_V1_01_02` formula inventory included |
| VAS/VVWD/Pump summaries | Open verification | Original inventories are not substitutes for interpretation, dependency and safe-change summaries |

Report delivery now uses one shared SPEC. A module becomes upload-ready only
when both its ORIGINAL and SUMMARY files are complete; the shared SPEC alone
does not make a module report package runnable.
