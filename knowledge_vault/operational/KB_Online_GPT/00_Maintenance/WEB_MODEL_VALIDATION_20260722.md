# Online Method KB Web-Model Validation

Validation_Date: 2026-07-22  
Profile: Small context, three files below 200 KB each  
Intent: Hold CC at 20 C for one hour; after minute 1 switch upper/lower valves every 6 seconds for 30 minutes

## Result

The small-context evidence profile remains usable. Doubao expert mode routed
the intent to the correct temperature and periodic-Trigger mechanisms and
produced a mostly correct script. Its defect was local and diagnosable: bare
`1.000` and `31.000` rows were emitted without a stage or executable command,
so they were classified as comments.

| Model | Structural result | Semantic result | Main finding |
|---|---|---|---|
| Doubao expert | Mostly valid | Mostly correct | Bare numeric time rows are not executable anchors |
| GPT-5.5 Instant | Invalid TSV serialization | Strong mechanism reasoning | Space-aligned text was used instead of real tabs |
| GPT-5.6 Medium | Valid | Correct for the requested same-position synchronous switching interpretation | Best directly usable output in this trial |
| DeepSeek | Structurally readable | Incorrect timeline | Interpreted switching as starting after the one-hour hold |

## Maintenance Implication

1. Keep the small-context package as a first-class delivery profile.
2. Keep a complete SPEC in that profile; compact ORIGINAL and SUMMARY only.
3. Explicitly prohibit a numeric `Time` value without a stage/Trigger/command
   on the same TSV row.
4. Local preview and preflight remain mandatory. A model producing no red rows
   is not sufficient evidence that test semantics are correct.
