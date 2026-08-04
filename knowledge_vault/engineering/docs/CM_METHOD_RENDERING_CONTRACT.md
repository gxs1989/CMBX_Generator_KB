# CM Method Script Rendering Contract

This document defines how decoded Chromeleon method flow rows are rendered into the CMBX Data Explorer method preview table.

## Column Contract

| Kind | Time | Command | Value | Comment |
|---|---|---|---|---|
| Stage | Source stage time. Only `Instrument Setup` may default to `{Initial Time}` when source time is blank. | Stage display name | Stage duration or stage value metadata, when present | Stage comment |
| Comment | Blank unless source row has an explicit time marker | Comment text | Blank | Blank |
| Branch | `If`, `Else If`, `Else`, or `End If` with indentation | Blank | Branch condition | Blank |
| Command | Source command time only when it changes from previous visible time | CM command or property path | CM value | Source comment |
| End | Blank unless explicit source end time exists | `End` | Blank | Blank |

## Guardrails

- Do not display `{Initial Time}` on every stage. If a non-initial stage has no source time in the decoded TSV, leave `Time` blank rather than inventing a value.
- Branch keywords belong in the `Time` column; branch conditions belong in `Value`.
- Green CM rows are comments only when `Kind=Comment`; do not treat them as executable commands.
- Stage duration belongs in `Value`, not `Comment`, so it aligns with the CM table layout.

## Known Source Limitation

Some existing `*_embedded_method_flow.tsv` files were generated before stage time and duration extraction was complete. For those files, the renderer cannot recover a missing stage time such as `-30.000` from the TSV alone. The correct fix is to refresh the Method Script KB from the original embedded method XML after improving XML stage-time extraction.

## KB Refresh Procedure

Use the checked-in refresh helper after changing embedded method XML extraction:

```powershell
python cmbx_data_explorer\tools\refresh_tcc_method_script_kb.py --source all
```

This rebuilds the TCC Method Script KB from the source CMBX packages under `C:\ProgramData\CMBX Data Explorer Workspace\packages`, including the VA/VC/VH reverse-probe methods and the VH stress-test methods. The refreshed TSV rows preserve stage start time and stage duration from the decoded embedded method XML.
