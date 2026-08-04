# Single Verification

Single Verification contains focused development analyses. It is a category, not
one universal calculation. Every child feature owns its algorithm and evidence
contract.

## Leak Sensor Analysis

- Input: decoded `LEDBoard_LeakDiff` raw channels from owned CMBX files.
- Grouping: Water remains temperature-specific; MeOH and IPA normalize to RT.
- Baseline: stable signal region before leakage.
- `T0`: first directional departure from baseline.
- `t90`: interpolated 90% response crossing.
- Displayed `T90`: `t90 - T0`, two decimals.
- Displayed `Delta Diff`: integer; internal calculations retain precision.
- Charts: Aptos (Body), configurable 8-16 pt and aspect ratio, 50% Web preview,
  full-resolution clipboard output.

See [[../05_Web_Workspace/_INDEX|Web Workspace]] for the current implementation
status and access-control contract.
