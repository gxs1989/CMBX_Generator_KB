# TCC Stress Trigger Method Contract

Status: Source-grounded execution contract  
Evidence: `Stress_VH_DVT013_20260529.cmbx`, especially `stress test_5s`

## Purpose

This contract explains the reusable CM mechanism used by the TCC stress
methods for periodic synchronous upper/lower valve switching. It is execution
evidence, not an FOQ acceptance criterion.

## Verified Module Roles

| Role | Source pattern | Meaning |
|---|---|---|
| Initial valve state | `UpperValve.CurrentPosition`, `LowerValve.CurrentPosition` | Establish a known complementary valve state before the run |
| Alternating gates | `Variables.GenericBool1`, `Variables.GenericBool2` | Exactly one Ping/Pong trigger is armed at a time |
| Next-switch time | `Variables.GenericFloat1` | Absolute next switch time in `System.Retention` minutes |
| Ping/Pong triggers | `System.Trigger` in `Start Run` | Alternately change both valves and hand control to the opposite trigger |
| Arm cycle | `Variables.GenericBool1 = 1` in `Run` | Starts periodic switching only after the run timeline begins |
| Stop cycle | Both Boolean gates reset to `0` | Prevents further trigger execution during cleanup |

## Period Encoding

`System.Retention` is expressed in minutes. The source method schedules the
next trigger edge by adding a minute fraction:

| Requested period | Source-grounded assignment |
|---:|---|
| 6 seconds | `Variables.GenericFloat1 = System.Retention+0.1` |
| 3 seconds | `Variables.GenericFloat1 = System.Retention+0.05` |

The period is **not** encoded as ordinary `Delay 0.1`. Trigger `TrueTime` and
trigger `Delay` are seconds and serve trigger qualification/execution timing;
they do not replace the absolute next-edge schedule.

## Source-Grounded 6-Second Skeleton

```text
Instrument Setup:
  GenericBool1 = 0
  GenericBool2 = 0
  GenericFloat1 = 0

Start Run:
  Trigger Ping when Bool1=1 and Retention>GenericFloat1 and inside window
    GenericFloat1 = System.Retention+0.1
    preserve source Delay/valve-set/Delay sequence
    Bool1 = 0
    Bool2 = 1

  Trigger Pong when Bool2=1 and Retention>GenericFloat1 and inside window
    GenericFloat1 = System.Retention+0.1
    preserve source Delay/valve-set/Delay sequence
    Bool1 = 1
    Bool2 = 0

Run:
  GenericBool1 = 1

Stop Run:
  GenericBool1 = 0
  GenericBool2 = 0
```

## Composition Guardrails

1. Copy the complete verified Ping/Pong module, including state handoff and
   the Delay rows around valve actuation. Do not retain only the valve-set rows.
2. Change the active time window and the `System.Retention` increment together.
3. Keep trigger names unique.
4. Keep upper/lower valve assignments paired as proven by the chosen source
   method and target plumbing configuration.
5. Log valve positions only with the exact configured symbols.
6. Preserve final Boolean reset and acquisition cleanup.
7. A script that uses `Delay 0.1` as "6 seconds" but does not update the
   absolute next-switch time does not implement the verified cycle mechanism.

## Open Verification Required

- Confirm target valve position labels against the actual CM instrument
  configuration.
- Confirm whether the requested physical test needs complementary positions or
  identical positions for upper/lower valves.
- Run Chromeleon Method Check before claiming runnable status.
