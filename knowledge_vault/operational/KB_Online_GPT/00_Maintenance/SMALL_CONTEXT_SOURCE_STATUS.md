# Online GPT KB Source Status

Status_Date: 2026-07-22

## Method Packages

| Profile | Status | Evidence |
|---|---|---|
| Full context | Candidate for controlled web-model validation | Complete current TCC Method SPEC, original-script collection and summaries |
| Small context | Validated as usable for selected TCC temperature and valve/stress intents | Three files below 200 KB were accepted by Doubao expert mode and produced a mostly correct periodic-valve method |

Small-context validation found one authoring defect: bare `1.000` and `31.000`
time rows were classified as comments. The SPEC now contains an explicit
prohibition and corrected same-row command examples.

## Rebuild Requirement

Rebuild both profiles whenever the Method SPEC, source scripts, stress Trigger
contract, role summaries, renderer, or compiler rules change.
