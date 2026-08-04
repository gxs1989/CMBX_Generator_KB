# Online VAS Method Understanding and Summary Collection (<200 KB)

Online_KB_Status: DERIVED_KNOWLEDGE_REQUIRES_CM_REVIEW  
Build_Date: 2026-07-23  
Scope: VAS method roles, reusable execution patterns, configuration dependencies, and report-facing evidence

The original-script collection is the command source of truth. These summaries are derived interpretations. They may route an intent and explain a method, but they must not override decoded CMBX rows. Any generated method still requires local preflight, CMBX compilation, CM import/open, and CM Method Check.

## Self Index

| Summary ID | Source method | Family | Evidence status | Section |
|---|---|---|---|---|
| `S-VAS-BI-VASC-COOLED-STOPFLOW` | `BI_VASC_Cooled_STOPFLOW` | `burnin_stopflow_cleanup` | `derived_from_decoded_cmbx_preview_not_cm_validated` | [Open](#s-vas-bi-vasc-cooled-stopflow) |
| `S-VAS-FOQ-VASA-AUTO-LEAK-TEST` | `FOQ_VASA_Auto_Leak_Test` | `automatic_leak_test` | `derived_from_decoded_cmbx_preview_not_cm_validated` | [Open](#s-vas-foq-vasa-auto-leak-test) |
| `S-VAS-FOQ-VASA-COOLED-CO-END` | `FOQ_VASA_Cooled_CO_End` | `carryover_end_reset` | `derived_from_decoded_cmbx_preview_not_cm_validated` | [Open](#s-vas-foq-vasa-cooled-co-end) |
| `S-VAS-FOQ-VASA-COOLED-CO-RC` | `FOQ_VASA_Cooled_CO_RC` | `carryover_rc_long_sample` | `derived_from_decoded_cmbx_preview_not_cm_validated` | [Open](#s-vas-foq-vasa-cooled-co-rc) |
| `S-VAS-FOQ-VASA-COOLED-CO-RC-FILL-REF-VIALS` | `FOQ_VASA_Cooled_CO_RC_Fill_Ref_Vials` | `carryover_rc_fill_reference_vials` | `derived_from_decoded_cmbx_preview_not_cm_validated` | [Open](#s-vas-foq-vasa-cooled-co-rc-fill-ref-vials) |
| `S-VAS-FOQ-VASA-COOLED-CO-RC-SOLV-REF` | `FOQ_VASA_Cooled_CO_RC_Solv_Ref` | `carryover_rc_short_reference` | `derived_from_decoded_cmbx_preview_not_cm_validated` | [Open](#s-vas-foq-vasa-cooled-co-rc-solv-ref) |
| `S-VAS-FOQ-VASA-COOLED-EQUILIBRATION` | `FOQ_VASA_Cooled_equilibration` | `equilibration_flow_step` | `derived_from_decoded_cmbx_preview_not_cm_validated` | [Open](#s-vas-foq-vasa-cooled-equilibration) |
| `S-VAS-FOQ-VASA-COOLED-EXCEPTIONLOG-CLEAR` | `FOQ_VASA_Cooled_ExceptionLog_Clear` | `exceptionlog_clear_safe_transport` | `derived_from_decoded_cmbx_preview_not_cm_validated` | [Open](#s-vas-foq-vasa-cooled-exceptionlog-clear) |
| `S-VAS-FOQ-VASA-COOLED-FLOW-ADJUSTMENT-RESTRICTION-CAPILLARY` | `FOQ_VASA_Cooled_Flow_adjustment_restriction_capillary` | `flow_adjustment_restriction_capillary` | `derived_from_decoded_cmbx_preview_not_cm_validated` | [Open](#s-vas-foq-vasa-cooled-flow-adjustment-restriction-capillary) |
| `S-VAS-FOQ-VASA-COOLED-IN-RELAY-VWD` | `FOQ_VASA_Cooled_IN_RELAY_VWD` | `digital_io_relay_input` | `derived_from_decoded_cmbx_preview_not_cm_validated` | [Open](#s-vas-foq-vasa-cooled-in-relay-vwd) |
| `S-VAS-FOQ-VASA-COOLED-INIT` | `FOQ_VASA_Cooled_Init` | `sampler_initialization_drive_deviation` | `derived_from_decoded_cmbx_preview_not_cm_validated` | [Open](#s-vas-foq-vasa-cooled-init) |
| `S-VAS-FOQ-VASA-COOLED-LINEARITY-SETIDLEVOLUME` | `FOQ_VASA_Cooled_Linearity_SetIdleVolume` | `linearity_idle_volume_setting` | `derived_from_decoded_cmbx_preview_not_cm_validated` | [Open](#s-vas-foq-vasa-cooled-linearity-setidlevolume) |
| `S-VAS-FOQ-VASA-COOLED-MH-MAX-RANGE-IN-ONEINJ-NOUDP` | `FOQ_VASA_Cooled_MH_Max_Range_in_oneInj___NoUdp` | `mh_max_range_no_udp` | `derived_from_decoded_cmbx_preview_not_cm_validated` | [Open](#s-vas-foq-vasa-cooled-mh-max-range-in-oneinj-noudp) |
| `S-VAS-FOQ-VASA-COOLED-PRECISION-LINEARITY` | `FOQ_VASA_Cooled_Precision_Linearity` | `precision_linearity_analytical_injection` | `derived_from_decoded_cmbx_preview_not_cm_validated` | [Open](#s-vas-foq-vasa-cooled-precision-linearity) |
| `S-VAS-FOQ-VASA-COOLED-SETPARAMETERS` | `FOQ_VASA_Cooled_SetParameters` | `set_parameters_wellness_factory_defaults` | `derived_from_decoded_cmbx_preview_not_cm_validated` | [Open](#s-vas-foq-vasa-cooled-setparameters) |
| `S-VAS-FOQ-VASA-COOLED-STOP` | `FOQ_VASA_Cooled_STOP` | `stop_reset_factory_defaults` | `derived_from_decoded_cmbx_preview_not_cm_validated` | [Open](#s-vas-foq-vasa-cooled-stop) |
| `S-VAS-FOQ-VASA-COOLED-SYSTEM-FLUSH` | `FOQ_VASA_Cooled_System_Flush` | `system_flush_repeated_injections` | `derived_from_decoded_cmbx_preview_not_cm_validated` | [Open](#s-vas-foq-vasa-cooled-system-flush) |
| `S-VAS-FOQ-VASC-COOLED-MH-MAX-RANGE-IN-ONEINJ` | `FOQ_VASC_Cooled_MH_Max_Range_in_oneInj` | `mh_max_range_udp` | `derived_from_decoded_cmbx_preview_not_cm_validated` | [Open](#s-vas-foq-vasc-cooled-mh-max-range-in-oneinj) |
| `S-VAS-FOQ-VASC-COOLED-TEMP-COOLING-PERFORMANCE-BI` | `FOQ_VASC_Cooled_Temp_Cooling_Performance_BI` | `cooling_performance` | `derived_from_decoded_cmbx_preview_not_cm_validated` | [Open](#s-vas-foq-vasc-cooled-temp-cooling-performance-bi) |

## Supporting Knowledge

| ID | Status | Source |
|---|---|---|
| `K-VAS-TD` | Available | `FOQ_VAS_TD_KNOWLEDGE_MANAGEMENT.md` |
| `K-VAS-LOGIC` | Missing | `FOQ_TD_TEST_LOGIC_KNOWLEDGE_BASE.md` |
| `K-VAS-REPORT` | Available | `VAS_DVAS_V_3_45_FORMULA_INVENTORY.md` |

<a id="k-vas-method-index"></a>
## K-VAS-METHOD-INDEX: Cross-Method Routing Index

# Method Script Knowledge Base Index

This directory contains one derived Markdown knowledge artifact per uploaded Chromeleon method script. These files are not executable method scripts; they are high-granularity summaries for future script generation.

## Generated files

| # | Source method | Knowledge file | Family | Rows | Purpose |
|---:|---|---|---|---:|---|
| 1 | `BI_VASC_Cooled_STOPFLOW.md` | `01_BI_VASC_Cooled_STOPFLOW_KB.md` | `burnin_stopflow_cleanup` | 58 | Burn-in stop-flow/stop method. It initializes the sampler, performs an injection to avoid ready-check warnings, reconnects the sampler to log error queue behavior, switches valve to bypass, raises the needle, enters s... |
| 2 | `FOQ_VASA_Auto_Leak_Test.md` | `02_FOQ_VASA_Auto_Leak_Test_KB.md` | `automatic_leak_test` | 309 | Automatic high-pressure leak test. It prepares pump pistons for individual control, selects inject or bypass leak-test valve position according to sequence state, builds pressure with a selected pump drive, records pi... |
| 3 | `FOQ_VASA_Cooled_CO_End.md` | `03_FOQ_VASA_Cooled_CO_End_KB.md` | `carryover_end_reset` | 102 | Carry-over end/reset method. It resets chromatographic and sampler settings to general defaults, performs a final injection, records core diagnostic channels, handles table indexer abort, and turns acquisition off. |
| 4 | `FOQ_VASA_Cooled_CO_RC.md` | `04_FOQ_VASA_Cooled_CO_RC_KB.md` | `carryover_rc_long_sample` | 130 | Carry-over restriction-capillary high-concentration or long sample injection method. It is structurally similar to the solvent/reference method but extends the Stop Run to 7 min for the C2000 carry-over sample. |
| 5 | `FOQ_VASA_Cooled_CO_RC_Fill_Ref_Vials.md` | `05_FOQ_VASA_Cooled_CO_RC_Fill_Ref_Vials_KB.md` | `carryover_rc_fill_reference_vials` | 142 | Carry-over reference-vial fill method. It stops the pump to let backpressure drop, moves the needle to purge and reference-vial positions, uses high flow to purge/fill water into the solvent reference vial, stops the ... |
| 6 | `FOQ_VASA_Cooled_CO_RC_Solv_Ref.md` | `06_FOQ_VASA_Cooled_CO_RC_Solv_Ref_KB.md` | `carryover_rc_short_reference` | 130 | Carry-over restriction-capillary solvent/reference injection method. It uses the calculated restriction-capillary flow, AfterDraw wash, full diagnostic acquisition, and a short chromatographic run for solvent or low-l... |
| 7 | `FOQ_VASA_Cooled_equilibration.md` | `07_FOQ_VASA_Cooled_equilibration_KB.md` | `equilibration_flow_step` | 52 | Thermal/flow equilibration method. It waits for module readiness, then steps flow from 0.5 to 1.0 after a short delay, with a fallback Stop Run at 2 min. |
| 8 | `FOQ_VASA_Cooled_ExceptionLog_Clear.md` | `08_FOQ_VASA_Cooled_ExceptionLog_Clear_KB.md` | `exceptionlog_clear_safe_transport` | 32 | Short end/protection method. Despite the filename, the visible script reconnects the sampler, switches the valve to bypass, and moves the needle up to avoid transport damage; no explicit ExceptionLog.Clear row is pres... |
| 9 | `FOQ_VASA_Cooled_Flow_adjustment_restriction_capillary.md` | `09_FOQ_VASA_Cooled_Flow_adjustment_restriction_capillary_KB.md` | `flow_adjustment_restriction_capillary` | 122 | Restriction-capillary flow adjustment. It measures pump pressure at an initial flow, averages three pressure readings, calculates a new flow to hit target pressure, clamps to a permitted range, verifies pressure after... |
| 10 | `FOQ_VASA_Cooled_IN_RELAY_VWD.md` | `10_FOQ_VASA_Cooled_IN_RELAY_VWD_KB.md` | `digital_io_relay_input` | 47 | Digital I/O verification. It cycles relay 1 and relay 2 through all relevant ON/OFF combinations and logs input 1/input 2 states after each state change. |
| 11 | `FOQ_VASA_Cooled_Init.md` | `11_FOQ_VASA_Cooled_Init_KB.md` | `sampler_initialization_drive_deviation` | 135 | Sampler initialization and drive-deviation logging method. It performs a normal injection, initializes the sampler, waits until ready, then logs compression, metering, needle, and horizontal drive home deviations. |
| 12 | `FOQ_VASA_Cooled_Linearity_SetIdleVolume.md` | `12_FOQ_VASA_Cooled_Linearity_SetIdleVolume_KB.md` | `linearity_idle_volume_setting` | 58 | Extended linearity preparation method. It applies a sampler idle volume from the current injection custom variable and logs the resulting IdleVolume. |
| 13 | `FOQ_VASA_Cooled_MH_Max_Range_in_oneInj___NoUdp.md` | `13_FOQ_VASA_Cooled_MH_Max_Range_in_oneInj___NoUdp_KB.md` | `mh_max_range_no_udp` | 162 | Metering-head maximum range test in one injection, implemented as direct sequential sampler service commands instead of a UDP. It moves MD/CD over the high range, draws sample from SR:1, injects, then logs metering/co... |
| 14 | `FOQ_VASA_Cooled_Precision_Linearity.md` | `14_FOQ_VASA_Cooled_Precision_Linearity_KB.md` | `precision_linearity_analytical_injection` | 128 | Standard analytical injection method for precision and linearity with caffeine. It sets common chromatographic conditions, injects, records pump/temperature/UV diagnostic channels, watches TableIndexerMode, logs meter... |
| 15 | `FOQ_VASA_Cooled_SetParameters.md` | `15_FOQ_VASA_Cooled_SetParameters_KB.md` | `set_parameters_wellness_factory_defaults` | 112 | Factory/qualification/wellness parameter setup method. It rejects wrong model/template combinations, enters sampler service level, disables qualification/service intervals and wellness limits, applies factory defaults... |
| 16 | `FOQ_VASA_Cooled_STOP.md` | `16_FOQ_VASA_Cooled_STOP_KB.md` | `stop_reset_factory_defaults` | 121 | Final FOQ stop/factory-default reset method. It slows the pump to standby, validates table indexer status, enters sampler service level twice, performs an injection, applies factory defaults/internals, logs many sampl... |
| 17 | `FOQ_VASA_Cooled_System_Flush.md` | `17_FOQ_VASA_Cooled_System_Flush_KB.md` | `system_flush_repeated_injections` | 76 | System flush method with repeated water injections from R:A3. It uses two triggers and Boolean toggles to repeatedly inject until the custom variable Injectionnumber_Flush is reached, then holds for 90 s and ends. |
| 18 | `FOQ_VASC_Cooled_MH_Max_Range_in_oneInj.md` | `18_FOQ_VASC_Cooled_MH_Max_Range_in_oneInj_KB.md` | `mh_max_range_udp` | 149 | Metering-head maximum range test in one injection using a sampler UDP. The detailed MD/CD/valve/fan/GotoPosition sequence is assembled during Instrument Setup with UdpBegin/UdpWait/UdpEnd and executed during Run by Sa... |
| 19 | `FOQ_VASC_Cooled_Temp_Cooling_Performance_BI.md` | `19_FOQ_VASC_Cooled_Temp_Cooling_Performance_BI_KB.md` | `cooling_performance` | 86 | Cooling-performance measurement for thermostatted Vanquish autosamplers. It measures ambient temperature, sets the cabin to ambient, waits for stability, starts temperature/pressure acquisition, sets target to 4 C, an... |

## Cross-method reusable pattern map

| Pattern | Meaning | Source methods |
|---|---|---|
| Acquisition symmetry | Turns diagnostic acquisition channels on at Start Run or early Run and mirrors AcqOff at abort/Stop Run/Post Run. | `FOQ_VASA_Auto_Leak_Test.md`, `FOQ_VASA_Cooled_CO_End.md`, `FOQ_VASA_Cooled_CO_RC.md`, `FOQ_VASA_Cooled_CO_RC_Fill_Ref_Vials.md`, `FOQ_VASA_Cooled_CO_RC_Solv_Ref.md`, `FOQ_VASA_Cooled_Flow_adjustment_restriction_capillary.md`, `FOQ_VASA_Cooled_IN_RELAY_VWD.md`, `FOQ_VASA_Cooled_Init.md`, `FOQ_VASA_Cooled_MH_Max_Range_in_oneInj___NoUdp.md`, `FOQ_VASA_Cooled_Precision_Linearity.md`, `FOQ_VASA_Cooled_STOP.md`, `FOQ_VASA_Cooled_System_Flush.md`, `FOQ_VASC_Cooled_MH_Max_Range_in_oneInj.md`, `FOQ_VASC_Cooled_Temp_Cooling_Performance_BI.md` |
| Factory defaults | Uses Sampler.SetFactoryDefaults and often Sampler.SetFactoryInternals to restore factory/internal sampler settings. | `FOQ_VASA_Cooled_SetParameters.md`, `FOQ_VASA_Cooled_STOP.md` |
| Firmware/service command bridge | Uses SamplerModule_Service or PumpModule_Service _SendCommand for firmware-level operations not exposed as normal CM properties. Preserve exact strings and ordering. | `BI_VASC_Cooled_STOPFLOW.md`, `FOQ_VASA_Auto_Leak_Test.md`, `FOQ_VASA_Cooled_CO_RC.md`, `FOQ_VASA_Cooled_CO_RC_Fill_Ref_Vials.md`, `FOQ_VASA_Cooled_CO_RC_Solv_Ref.md`, `FOQ_VASA_Cooled_ExceptionLog_Clear.md`, `FOQ_VASA_Cooled_Linearity_SetIdleVolume.md`, `FOQ_VASA_Cooled_MH_Max_Range_in_oneInj___NoUdp.md`, `FOQ_VASA_Cooled_Precision_Linearity.md`, `FOQ_VASA_Cooled_SetParameters.md`, `FOQ_VASA_Cooled_STOP.md`, `FOQ_VASC_Cooled_MH_Max_Range_in_oneInj.md` |
| Injection custom variables | Uses current injection custom variables as runtime inputs; these must exist in the sequence/injection list. | `FOQ_VASA_Cooled_Linearity_SetIdleVolume.md`, `FOQ_VASA_Cooled_System_Flush.md` |
| Log clearing | Uses service _SendCommand ErrorLog.Clear and/or ExceptionLog.Clear; this should remain late in stop methods. | `BI_VASC_Cooled_STOPFLOW.md`, `FOQ_VASA_Cooled_STOP.md` |
| Selectable pump drive | Branches on System.Sequence.CustomVariables.chooseDrive to choose Blk1 Drv1 vs Drv2 for pressure/leak evaluation. | `FOQ_VASA_Auto_Leak_Test.md` |
| Service-level entry | Requests service level via GetServiceCode, writes ServiceCode 87794, delays, logs service status, and often retries once if not in Service. | `BI_VASC_Cooled_STOPFLOW.md`, `FOQ_VASA_Auto_Leak_Test.md`, `FOQ_VASA_Cooled_Flow_adjustment_restriction_capillary.md`, `FOQ_VASA_Cooled_MH_Max_Range_in_oneInj___NoUdp.md`, `FOQ_VASA_Cooled_SetParameters.md`, `FOQ_VASA_Cooled_STOP.md` |
| TableIndexerMode guard | Acquires TableIndexerMode and aborts the queue with a German protocol message if Signal > 0. Reuse as carousel/indexer motor protection. | `FOQ_VASA_Auto_Leak_Test.md`, `FOQ_VASA_Cooled_CO_End.md`, `FOQ_VASA_Cooled_CO_RC.md`, `FOQ_VASA_Cooled_CO_RC_Fill_Ref_Vials.md`, `FOQ_VASA_Cooled_CO_RC_Solv_Ref.md`, `FOQ_VASA_Cooled_Flow_adjustment_restriction_capillary.md`, `FOQ_VASA_Cooled_Init.md`, `FOQ_VASA_Cooled_MH_Max_Range_in_oneInj___NoUdp.md`, `FOQ_VASA_Cooled_Precision_Linearity.md`, `FOQ_VASA_Cooled_STOP.md`, `FOQ_VASA_Cooled_System_Flush.md`, `FOQ_VASC_Cooled_MH_Max_Range_in_oneInj.md`, `FOQ_VASC_Cooled_Temp_Cooling_Performance_BI.md` |
| Virtual channel calculation | Creates virtual channels for derived volumes or leak-rate diagnostics from raw signals. | `FOQ_VASA_Auto_Leak_Test.md` |

## Recommended future AI read order

1. Read `00_METHOD_KB_INDEX.md` to choose the closest method family.
2. Read the corresponding per-method KB file and inspect sections 10-12 before generating a new method.
3. If generating executable TSV, enforce the strict SPEC rules: real tab columns, no timed prose-only rows, numeric trigger limits, no invented custom variables, and Run/Stop timing consistency.
4. After packaging, validate by CMBX decode, rendered table comparison, CM import/open, and CM Method Check.

<a id="s-vas-bi-vasc-cooled-stopflow"></a>
## S-VAS-BI-VASC-COOLED-STOPFLOW: BI_VASC_Cooled_STOPFLOW

---
kb_type: chromeleon_method_summary
source_method_file: BI_VASC_Cooled_STOPFLOW.md
source_sha256_16: 517ae5eeeab9d9b1
method_family: burnin_stopflow_cleanup
row_count: 58
language: en
status: derived_from_decoded_cmbx_preview_not_cm_validated
---

# BI VASC Cooled STOPFLOW - Method Knowledge Summary

> This file is a derived knowledge artifact, not an executable method script. It is designed so a future AI/script generator can read the intent, command patterns, variables, safety guards, and reusable structures before authoring a new strict TSV method.

## 1. Method identity and role

- **Source file:** `BI_VASC_Cooled_STOPFLOW.md`
- **Primary purpose:** Burn-in stop-flow/stop method. It initializes the sampler, performs an injection to avoid ready-check warnings, reconnects the sampler to log error queue behavior, switches valve to bypass, raises the needle, enters service level, and clears ErrorLog.
- **Sequence role:** Burn-in end or stop-flow safe-state cleanup for cooled Core autosampler.
- **Method family tag:** `burnin_stopflow_cleanup`
- **When to reuse:** Use for BI cleanup methods that must leave the sampler in bypass with needle lifted and ErrorLog cleared.
- **Source visible title/comment cues:** `PumpDevice =  "Pump"`; `InjectWashMode = BeforeInject`; `InjectMode = Normal`
- **Detected modules/symbol roots:** `Pump`, `PumpModule`, `Sampler`, `SamplerModule`
- **Run duration declarations:** `1.6`
- **Stop Run times:** `2.0`

## 2. High-level execution story

This method configures or controls the pump, pressure limits, flow, or pump service commands; configures sampler mechanics, injection behavior, service commands, temperature, or table-indexer monitoring.

## 5. Variables, state, and custom inputs

No Variables.* or System.*CustomVariables.* symbols detected.

## 6. Branching, triggers, and asynchronous logic

### 6.2 Conditional branch rows

| Row | Branch keyword | Condition/value | Comment |
|---:|---|---|---|
| 46 | If | SamplerModule_Service.ServiceCode=Service |  |
| 47 | Else |  |  |
| 54 | End If |  |  |

No trigger blocks detected.

## 9. Waits, delays, logging, aborts, and report-facing outputs

### 9.1 Wait / Delay rows

| Row | Command | Value | Comment |
|---:|---|---|---|
| 21 | Delay | 3 |  |
| 22 | Wait | Sampler.Ready |  |
| 29 | Wait | Sampler.Ready |  |
| 33 | Delay | 1 |  |
| 41 | Delay | 5 |  |
| 43 | Delay | 1 |  |
| 45 | Delay | 1 |  |
| 49 | Delay | 5 |  |
| 51 | Delay | 1 |  |
| 53 | Delay | 1 |  |

### 9.2 Log / Protocol / Message / Abort rows

| Row | Command | Value | Comment | Role |
|---:|---|---|---|---|
| 44 | Log | SamplerModule_Service.ServiceCode |  | log |
| 52 | Log | SamplerModule_Service.ServiceCode |  | log |

## 10. Reusable design patterns extracted

- **Service-level entry:** Requests service level via GetServiceCode, writes ServiceCode 87794, delays, logs service status, and often retries once if not in Service.
- **Log clearing:** Uses service _SendCommand ErrorLog.Clear and/or ExceptionLog.Clear; this should remain late in stop methods.
- **Firmware/service command bridge:** Uses SamplerModule_Service or PumpModule_Service _SendCommand for firmware-level operations not exposed as normal CM properties. Preserve exact strings and ordering.

## 11. SPEC v2.2 compatibility and generation cautions

- Source display has Run Duration 1.600 min while Stop Run starts at 2.000 min. For new SPEC v2.2 output, make Run Duration equal the Stop Run time unless the compiler/source template explicitly supports the legacy display semantics.
- Contains timed prose/comment rows in the decoded source display. Convert these to executable anchors or move prose into the Comment column in newly authored strict TSV. Examples: row 25 @ 1.100: --------------------------------------------------------------------------------; row 37 @ 1.400: ==============================================================================
- Treat this decoded source as evidence of existing CM behavior, not as proof that a newly generated method with altered structure will open/run without CM Method Check.

## 12. Future-generation rules distilled from this method

- Reuse exact device/property symbols from this source only when the target CM configuration contains the same modules and channel names.
- Preserve acquisition start/stop symmetry, especially in every abort branch and Stop Run/Post Run cleanup.
- Preserve service-level command sequences, firmware command order, and protective delays unless validated on a decoded CMBX or in CM editor.
- Do not convert source comment rows into timed command rows; strict generated TSV must use real executable anchors.
- Any report-facing variable or log row should be retained if the downstream report likely reads it.

<a id="s-vas-foq-vasa-auto-leak-test"></a>
## S-VAS-FOQ-VASA-AUTO-LEAK-TEST: FOQ_VASA_Auto_Leak_Test

---
kb_type: chromeleon_method_summary
source_method_file: FOQ_VASA_Auto_Leak_Test.md
source_sha256_16: aad8f842cfab00f6
method_family: automatic_leak_test
row_count: 309
language: en
status: derived_from_decoded_cmbx_preview_not_cm_validated
---

# FOQ VASA Auto Leak Test - Method Knowledge Summary

> This file is a derived knowledge artifact, not an executable method script. It is designed so a future AI/script generator can read the intent, command patterns, variables, safety guards, and reusable structures before authoring a new strict TSV method.

## 1. Method identity and role

- **Source file:** `FOQ_VASA_Auto_Leak_Test.md`
- **Primary purpose:** Automatic high-pressure leak test. It prepares pump pistons for individual control, selects inject or bypass leak-test valve position according to sequence state, builds pressure with a selected pump drive, records piston movement, calculates leak rate, evaluates system/pump/inject-path leak results, logs all diagnostic variables, and aborts on fail.
- **Sequence role:** Internal automated leakage qualification, spanning system and bypass/pump test injections via persistent GenericFloat1 state.
- **Method family tag:** `automatic_leak_test`
- **When to reuse:** Use as the canonical pattern for pressure-hold leak calculations from pump linear encoder movement and time delta.
- **Source visible title/comment cues:** `Initializing variables`
- **Detected modules/symbol roots:** `ColumnComp`, `Pump`, `PumpModule`, `Sampler`, `SamplerModule`, `System`, `Variables`, `VirtualChannel`
- **Run duration declarations:** `12.0`
- **Stop Run times:** `13.0`

## 2. High-level execution story

This method configures or controls the pump, pressure limits, flow, or pump service commands; configures the column compartment temperature/valves and may use a restriction-capillary flow path; configures sampler mechanics, injection behavior, service commands, temperature, or table-indexer monitoring; uses generic variables as state, calculations, flags, limits, or report outputs; uses trigger blocks for asynchronous protection, live diagnostics, looping, or endpoint logging.

## 5. Variables, state, and custom inputs

### 5.1 Variable symbol inventory

| Variable/custom symbol | First observed role/context |
|---|---|
| `Variables.GenericBool1` | row 16: Variables.GenericBool1 = 0; Internal indicator. Set 1 when block-bypass position is additionally tested |
| `Variables.GenericBool4` | row 17: Variables.GenericBool4 = 0; Internal indicator. Set 1 when block-bypass position passes the test |
| `Variables.GenericBool5` | row 18: Variables.GenericBool5 = 0; Internal indicator. Set 1 when block-bypass position fails for high leakage |
| `Variables.GenericBool6` | row 19: Variables.GenericBool6 = 0; Internal indicator. Set 1 when block-bypass position fails for unknown reasons |
| `Variables.GenericBool9` | row 20: Variables.GenericBool9 = 0; Internal indicator. Set 1 when test fails for unknown reasons |
| `Variables.GenericDouble0` | row 21: Variables.GenericDouble0 = 0; Stores piston position for measurement (start) |
| `Variables.GenericDouble1` | row 22: Variables.GenericDouble1 = 0; Stores time for measurement (start) |
| `Variables.GenericDouble2` | row 23: Variables.GenericDouble2 = 0; Stores piston position for measurement (end) |
| `Variables.GenericDouble3` | row 24: Variables.GenericDouble3 = 0; Stores time for measurement (end) |
| `Variables.GenericDouble4` | row 25: Variables.GenericDouble4 = 0; Used for calculation. Difference in piston position (see above) |
| `Variables.GenericDouble5` | row 26: Variables.GenericDouble5 = 0; Used for calculation. Difference in time (see above) |
| `Variables.GenericDouble6` | row 27: Variables.GenericDouble6 = 0; leak rate of current test |
| `Variables.GenericDouble7` | row 28: Variables.GenericDouble7 = leak rate of system test = ;  |
| `Variables.GenericDouble8` | row 29: Variables.GenericDouble8 = 99999.99; leak rate of bypass |
| `Variables.GenericDouble9` | row 30: Variables.GenericDouble9 = 99999.99; leak rate of inject path |
| `Variables.GenericFloat0` | row 31: Variables.GenericFloat0 = 150; maximum leak rate of the VAS |
| `Variables.GenericFloat1` | row 32: Variables.GenericFloat1 decides whether or not to test VAS bypass (1 = system test passed; 2 = system test failed, pump test needs to be executed = ;  |
| `Variables.GenericFloat2` | row 33: Variables.GenericFloat2 = 600; maximum pump leak |
| `Variables.GenericFloat3` | row 34: Variables.GenericFloat3 = -50; maximum negative leak rate for all pump and autosampler |
| `Variables.GenericFloat8` | row 35: Variables.GenericFloat8 = 4; Used for beginning of live pressure test (+1 Minute) |
| `Variables.GenericFloat7` | row 36: Variables.GenericFloat7 = 0; Reset Live Leak Rate at beginning |
| `Variables.GenericFloat4` | row 37: Variables.GenericFloat4 = 0; Reset average leak rate at beginning |
| `Variables.GenericFloat6` | row 38: Variables.GenericFloat6 = 0; Used for estimation of live leak rate |
| `Variables.GenericFloat9` | row 39: Variables.GenericFloat9 = 0; Used for estimation of live leak rate |
| `Variables.GenericFloat5` | row 40: Variables.GenericFloat5 = 0; Used for estimation of live leak rate |
| `Variables.GenericString0` | row 45: Variables.GenericString0 = "49500,"; pressure for leak test. First three digits in bar |
| `Variables.GenericLong9` | row 46: Variables.GenericLong9 = 495; pressure of leak test in bar for display in the report |
| `Variables.GenericBool7` | row 48: Variables.GenericBool7 = 0;  |
| `Variables.GenericBool0` | row 63: Variables.GenericBool0 = 0;  |
| `Variables.GenericBool2` | row 64: Variables.GenericBool2 = 0;  |
| `Variables.GenericBool3` | row 65: Variables.GenericBool3 = 0;  |
| `System.Sequence.CustomVariables.chooseDrive` | row 76: System.Sequence.CustomVariables.chooseDrive="A1" = ;  |

### 5.2 Required sequence/injection custom variables

- `System.Sequence.CustomVariables.chooseDrive` must be defined outside the method; do not invent or rename it in generated methods.

## 6. Branching, triggers, and asynchronous logic

### 6.1 Model/location gates

| Row | Time | Command | Value | Comment |
|---:|---|---|---|---|
| 44 | If | SamplerModule.ModelNo="VA-A12-A" |  |  |
| 101 | If | (SamplerModule.ModelNo="VH-A40-A" or SamplerModule.ModelNo="VF-A40-A") and SamplerModule.Sampler.Location=Right |  |  |
| 108 | If | (SamplerModule.ModelNo="VH-A40-A" or SamplerModule.ModelNo="VF-A40-A") and SamplerModule.Sampler.Location=Right |  |  |

### 6.2 Conditional branch rows

| Row | Branch keyword | Condition/value | Comment |
|---:|---|---|---|
| 41 | If | System.Injection.Name="Injector pressure test (System)" |  |
| 43 | End If |  |  |
| 44 | If | SamplerModule.ModelNo="VA-A12-A" |  |
| 49 | Else |  |  |
| 54 | End If |  |  |
| 57 | If | Variables.GenericFloat1=1 |  |
| 60 | Else If | Variables.GenericFloat1=2 |  |
| 61 | Else |  |  |
| 66 | End If |  |  |
| 76 | If | System.Sequence.CustomVariables.chooseDrive="A1" |  |
| 79 | Else |  |  |
| 82 | End If |  |  |
| 99 | If | Variables.GenericFloat1=2 |  |
| 101 | If | (SamplerModule.ModelNo="VH-A40-A" or SamplerModule.ModelNo="VF-A40-A") and SamplerModule.Sampler.Location=Right |  |
| 103 | Else |  |  |
| 105 | End If |  |  |
| 106 | Else |  |  |
| 108 | If | (SamplerModule.ModelNo="VH-A40-A" or SamplerModule.ModelNo="VF-A40-A") and SamplerModule.Sampler.Location=Right |  |
| 110 | Else |  |  |
| 112 | End If |  |  |
| 113 | End If |  |  |
| 117 | If | System.Sequence.CustomVariables.chooseDrive="A1" |  |
| 119 | Else |  |  |
| 121 | End If |  |  |
| 124 | If | System.Retention<13 |  |
| 131 | If | Variables.GenericFloat1=0 |  |
| 137 | Else If | Variables.GenericFloat1=2 |  |
| 144 | End If |  |  |
| 145 | End If |  |  |
| 147 | If | SamplerModule.TableIndexerMode.Signal>0 |  |
| 162 | Else |  |  |
| 163 | End If |  |  |
| 170 | If | System.Retention>7.00 |  |
| 172 | End If |  |  |
| 178 | If | System.Sequence.CustomVariables.chooseDrive="A1" |  |
| 179 | If | PumpModule.Pump.Blk1_Drv1_Linenc.Signal>Variables.GenericDouble0 |  |
| 182 | End If |  |  |
| 184 | Else |  |  |
| 185 | If | PumpModule.Pump.Blk1_Drv2_Linenc.Signal>Variables.GenericDouble0 |  |
| 188 | End If |  |  |
| 190 | End If |  |  |
| 192 | If | System.Sequence.CustomVariables.chooseDrive="A1" |  |
| 193 | If | PumpModule.Pump.Blk1_Drv1_Linenc.Signal>Variables.GenericDouble2 |  |
| 196 | End If |  |  |
| 198 | Else |  |  |
| 199 | If | PumpModule.Pump.Blk1_Drv2_Linenc.Signal>Variables.GenericDouble2 |  |
| 202 | End If |  |  |
| 204 | End If |  |  |
| 238 | If | Variables.GenericFloat1=0 and Variables.GenericDouble6<Variables.GenericFloat0 and Variables.GenericDouble6>Variables.GenericFloat3 |  |
| 244 | Else If | Variables.GenericFloat1=0 and (Variables.GenericDouble6>Variables.GenericFloat0 or Variables.GenericDouble6<Variables.GenericFloat3) |  |
| 250 | Else If | Variables.GenericFloat1=2 and Variables.GenericDouble7-Variables.GenericDouble6<Variables.GenericFloat0 and Variables.GenericDouble6<Variables.GenericFloat2 and Variables.GenericDouble7-Variables.GenericDouble6>Variables.GenericFloat3 |  |
| 258 | Else |  |  |
| 259 | If | Variables.GenericFloat1=2 and (Variables.GenericDouble7-Variables.GenericDouble6>Variables.GenericFloat0 or Variables.GenericDouble7-Variables.GenericDouble6<Variables.GenericFloat3 or Variables.GenericDouble6>Variables.GenericFloat2) |  |
| 267 | Else |  |  |
| 270 | End If |  |  |
| 275 | End If |  |  |

### 6.3 Trigger blocks / trigger-like structures

#### Trigger 1: `CannotBuildUpPressure`

| Row | Time | Command | Value | Comment | Role |
|---:|---|---|---|---|---|
| 123 | Trigger | "CannotBuildUpPressure", PumpModule.Pump.Blk1_Drv1_Linenc>17000 or PumpModule.Pump.Blk1_Drv2_Linenc>17000, Limit=1 |  |  | trigger_start |
| 124 | If | System.Retention<13 |  |  | branch |
| 125 |  | PumpModule.Pump.Pump_Service.AbortModalCommand |  |  | command_or_property_without_value |
| 126 |  | PumpModule.Pump.Pump_Service.PurgeValve | Open |  | property_set |
| 127 |  | SamplerModule.Sampler.SwitchValve | Position=Bypass |  | property_set |
| 128 |  | Delay | 5 [s] |  | trigger_parameter |
| 129 |  | PumpModule.Pump.Pump_Service.PurgeValve | Closed |  | property_set |
| 130 |  | Delay | 5 [s] |  | trigger_parameter |
| 131 | If | Variables.GenericFloat1=0 |  |  | branch |
| 132 |  | Variables.GenericDouble7 | 99999.99 |  | variable_assignment |
| 133 |  | Variables.GenericFloat1 | 2 |  | variable_assignment |
| 134 |  | Variables.GenericBool0 | 1 |  | variable_assignment |
| 135 |  | Delay | 1 [s] |  | trigger_parameter |
| 136 |  | System.AbortInjection |  |  | abort_injection |
| 137 | Else If | Variables.GenericFloat1=2 |  |  | branch |
| 138 |  | Variables.GenericDouble8 | 99999.99 |  | variable_assignment |
| 139 |  | Variables.GenericBool1 | 1 |  | variable_assignment |
| 140 |  | Delay | 1 [s] |  | trigger_parameter |
| 141 |  | SamplerModule.SamplerModule_Service._SendCommand | "LedBar.ForceColor=1" | Led bar red | firmware_send_command |
| 142 |  | Delay | 1 [s] |  | trigger_parameter |
| 143 |  | System.AbortQueue |  |  | abort_queue |
| 144 | End If |  |  |  | branch |
| 145 | End If |  |  |  | branch |
| 146 | End Trigger |  |  |  | trigger_end |

#### Trigger 2: `LiveDrucktest`

| Row | Time | Command | Value | Comment | Role |
|---:|---|---|---|---|---|
| 164 | Trigger | "LiveDrucktest", System.Retention>Variables.GenericFloat8+1 AND System.Retention<12.900, AllowImmediateExecution=Yes |  | Execute trigger every minute (start at 5.0 min) | trigger_start |
| 165 |  | Variables.GenericFloat5 | Variables.GenericFloat8 | Shift retention time of last cycle | variable_assignment |
| 166 |  | Variables.GenericFloat6 | Variables.GenericFloat9 | Shift Volume of last cycle | variable_assignment |
| 167 |  | Variables.GenericFloat8 | System.Retention | Save current retention time | variable_assignment |
| 168 |  | Variables.GenericFloat9 | 3.141*1.5875*1.5875*PumpModule.Pump.Blk1_Drv1_Linenc.Signal | Save current volume | variable_assignment |
| 169 |  | Variables.GenericFloat7 | (Variables.GenericFloat9-Variables.GenericFloat6)/(Variables.GenericFloat8-Variables.GenericFloat5) | Calculate the difference to the last cycle | variable_assignment |
| 170 | If | System.Retention>7.00 |  |  | branch |
| 171 |  | Variables.GenericFloat4 | (Variables.GenericFloat9-(3.1415*1.5875*1.5875*Variables.GenericDouble0))/(Variables.GenericFloat8-Variables.GenericDouble1) | Calculation of the average leak rate (like in the report) | variable_assignment |
| 172 | End If |  |  |  | branch |
| 173 | End Trigger |  |  |  | trigger_end |

#### Trigger 3: `Abort Queue`

| Row | Time | Command | Value | Comment | Role |
|---:|---|---|---|---|---|
| 304 | Trigger | "Abort Queue", Variables.GenericBool9=1, Limit=1 |  |  | trigger_start |
| 305 |  | SamplerModule.SamplerModule_Service._SendCommand | "LedBar.ForceColor=1" |  | firmware_send_command |
| 306 |  | Delay | 1 [s] |  | trigger_parameter |
| 307 |  | System.AbortQueue |  |  | abort_queue |
| 308 | End Trigger |  |  |  | trigger_end |

## 9. Waits, delays, logging, aborts, and report-facing outputs

### 9.1 Wait / Delay rows

| Row | Command | Value | Comment |
|---:|---|---|---|
| 52 | Delay | 1 [s] |  |
| 72 | Delay | 1 [s] |  |
| 74 | Delay | 1 [s] |  |
| 78 | Delay | 5 [s] |  |
| 81 | Delay | 5 [s] |  |
| 114 | Delay | 1 [s] |  |
| 128 | Delay | 5 [s] |  |
| 130 | Delay | 5 [s] |  |
| 135 | Delay | 1 [s] |  |
| 140 | Delay | 1 [s] |  |
| 142 | Delay | 1 [s] |  |
| 159 | Delay | 1 |  |
| 183 | Delay | 0.1 [s] | Otherwise IF-block is executed every 100 ms |
| 189 | Delay | 0.1 [s] | Otherwise IF-block is executed every 100 ms |
| 197 | Delay | 0.1 [s] | Otherwise IF-block is executed every 100 ms |
| 203 | Delay | 0.1 [s] | Otherwise IF-block is executed every 100 ms |
| 222 | Delay | 1 [s] |  |
| 225 | Delay | 1 [s] |  |
| 228 | Delay | 1 [s] |  |
| 231 | Delay | 1 [s] |  |
| 236 | Delay | 1 [s] |  |
| 254 | Delay | 1 [s] |  |
| 263 | Delay | 1 [s] |  |
| 272 | Delay | 1 |  |
| 277 | Delay | 1 [s] |  |
| 306 | Delay | 1 [s] |  |

### 9.2 Log / Protocol / Message / Abort rows

| Row | Command | Value | Comment | Role |
|---:|---|---|---|---|
| 53 | System.AbortQueue |  |  | abort_queue |
| 136 | System.AbortInjection |  |  | abort_injection |
| 143 | System.AbortQueue |  |  | abort_queue |
| 160 | Protocol | "Indexer-Fehler. Bitte Motor des Drehtellers austauschen und den defekten Motor an R&D übergeben." |  | protocol |
| 161 | System.AbortQueue |  |  | abort_queue |
| 278 | Log | Variables.GenericBool0 |  | log |
| 279 | Log | Variables.GenericBool1 |  | log |
| 280 | Log | Variables.GenericBool2 |  | log |
| 281 | Log | Variables.GenericBool3 |  | log |
| 282 | Log | Variables.GenericBool4 |  | log |
| 283 | Log | Variables.GenericBool5 |  | log |
| 284 | Log | Variables.GenericBool6 |  | log |
| 285 | Log | Variables.GenericBool7 |  | log |
| 286 | Log | Variables.GenericBool9 |  | log |
| 287 | Log | Variables.GenericDouble0 |  | log |
| 288 | Log | Variables.GenericDouble1 |  | log |
| 289 | Log | Variables.GenericDouble2 |  | log |
| 290 | Log | Variables.GenericDouble3 |  | log |
| 291 | Log | Variables.GenericDouble4 |  | log |
| 292 | Log | Variables.GenericDouble5 |  | log |
| 293 | Log | Variables.GenericDouble6 |  | log |
| 294 | Log | Variables.GenericDouble7 |  | log |
| 295 | Log | Variables.GenericDouble8 |  | log |
| 296 | Log | Variables.GenericDouble9 |  | log |
| 297 | Log | Variables.GenericFloat0 |  | log |
| 298 | Log | Variables.GenericFloat1 |  | log |
| 299 | Log | Variables.GenericFloat2 |  | log |
| 300 | Log | Variables.GenericFloat3 |  | log |
| 307 | System.AbortQueue |  |  | abort_queue |

## 10. Reusable design patterns extracted

- **TableIndexerMode guard:** Acquires TableIndexerMode and aborts the queue with a German protocol message if Signal > 0. Reuse as carousel/indexer motor protection.
- **Service-level entry:** Requests service level via GetServiceCode, writes ServiceCode 87794, delays, logs service status, and often retries once if not in Service.
- **Acquisition symmetry:** Turns diagnostic acquisition channels on at Start Run or early Run and mirrors AcqOff at abort/Stop Run/Post Run.
- **Firmware/service command bridge:** Uses SamplerModule_Service or PumpModule_Service _SendCommand for firmware-level operations not exposed as normal CM properties. Preserve exact strings and ordering.
- **Virtual channel calculation:** Creates virtual channels for derived volumes or leak-rate diagnostics from raw signals.
- **Selectable pump drive:** Branches on System.Sequence.CustomVariables.chooseDrive to choose Blk1 Drv1 vs Drv2 for pressure/leak evaluation.

## 11. SPEC v2.2 compatibility and generation cautions

- Source display has Run Duration 12.000 min while Stop Run starts at 13.000 min. For new SPEC v2.2 output, make Run Duration equal the Stop Run time unless the compiler/source template explicitly supports the legacy display semantics.
- Contains timed prose/comment rows in the decoded source display. Convert these to executable anchors or move prose into the Comment column in newly authored strict TSV. Examples: row 122 @ 0.010: Trigger defined to terminate run, if measurement pressure is not reached or cann; row 176 @ 7.000: Leak rate measurement.; row 191 @ 12.000: Find the maximum piston position @ t ~ 12.5 min; row 303 @ 13.970: Queue is aborted if leak test fails.
- Contains legacy/CM-rendered single-row trigger syntax. For new SPEC v2.2 output, expand each trigger into Trigger + Condition/TrueTime/Delay/Limit/Hysteresis/AllowImmediateExecution parameter rows and keep actions before End Trigger.
- Uses custom variables that must be defined by the sequence/injection list: System.Sequence.CustomVariables.chooseDrive. Do not invent these in new methods.
- Treat this decoded source as evidence of existing CM behavior, not as proof that a newly generated method with altered structure will open/run without CM Method Check.

## 12. Future-generation rules distilled from this method

- Reuse exact device/property symbols from this source only when the target CM configuration contains the same modules and channel names.
- Preserve acquisition start/stop symmetry, especially in every abort branch and Stop Run/Post Run cleanup.
- Preserve service-level command sequences, firmware command order, and protective delays unless validated on a decoded CMBX or in CM editor.
- Do not convert source comment rows into timed command rows; strict generated TSV must use real executable anchors.
- Any report-facing variable or log row should be retained if the downstream report likely reads it.
- For calculation methods, keep all intermediate variables and logs; report templates and ePanels may depend on them even if they look redundant.

<a id="s-vas-foq-vasa-cooled-co-end"></a>
## S-VAS-FOQ-VASA-COOLED-CO-END: FOQ_VASA_Cooled_CO_End

---
kb_type: chromeleon_method_summary
source_method_file: FOQ_VASA_Cooled_CO_End.md
source_sha256_16: a1c631c23929337c
method_family: carryover_end_reset
row_count: 102
language: en
status: derived_from_decoded_cmbx_preview_not_cm_validated
---

# FOQ VASA Cooled CO End - Method Knowledge Summary

> This file is a derived knowledge artifact, not an executable method script. It is designed so a future AI/script generator can read the intent, command patterns, variables, safety guards, and reusable structures before authoring a new strict TSV method.

## 1. Method identity and role

- **Source file:** `FOQ_VASA_Cooled_CO_End.md`
- **Primary purpose:** Carry-over end/reset method. It resets chromatographic and sampler settings to general defaults, performs a final injection, records core diagnostic channels, handles table indexer abort, and turns acquisition off.
- **Sequence role:** Cleanup method at the end of the carry-over block.
- **Method family tag:** `carryover_end_reset`
- **When to reuse:** Use after carry-over injections to return method settings to normal FOQ conditions.
- **Source visible title/comment cues:** `End of carry-over test, set settings back to general settings (single injector)`; `Flow through restriction capillary`
- **Detected modules/symbol roots:** `ColumnComp`, `Pump`, `PumpModule`, `Sampler`, `SamplerModule`, `System`, `UV`
- **Run duration declarations:** `0.04`
- **Stop Run times:** `1.0`

## 2. High-level execution story

This method configures or controls the pump, pressure limits, flow, or pump service commands; configures the column compartment temperature/valves and may use a restriction-capillary flow path; configures sampler mechanics, injection behavior, service commands, temperature, or table-indexer monitoring; configures/records UV detector channels, typically at 272 nm for caffeine methods.

## 5. Variables, state, and custom inputs

No Variables.* or System.*CustomVariables.* symbols detected.

## 6. Branching, triggers, and asynchronous logic

### 6.1 Model/location gates

| Row | Time | Command | Value | Comment |
|---:|---|---|---|---|
| 12 | If | SamplerModule.ModelNo="VA-A12-A" |  |  |

### 6.2 Conditional branch rows

| Row | Branch keyword | Condition/value | Comment |
|---:|---|---|---|
| 12 | If | SamplerModule.ModelNo="VA-A12-A" |  |
| 18 | End If |  |  |
| 66 | If | SamplerModule.TableIndexerMode.Signal>0 |  |
| 84 | Else |  |  |
| 85 | End If |  |  |

No trigger blocks detected.

## 9. Waits, delays, logging, aborts, and report-facing outputs

### 9.1 Wait / Delay rows

| Row | Command | Value | Comment |
|---:|---|---|---|
| 25 | Delay | 1 |  |
| 47 | Wait | UV.Ready and Pump.Ready and ColumnComp.Ready and Sampler.Ready |  |
| 81 | Delay | 1 |  |

### 9.2 Log / Protocol / Message / Abort rows

| Row | Command | Value | Comment | Role |
|---:|---|---|---|---|
| 82 | Protocol | "Indexer-Fehler. Bitte Motor des Drehtellers austauschen und den defekten Motor an R&D übergeben." |  | protocol |
| 83 | System.AbortQueue |  |  | abort_queue |

## 10. Reusable design patterns extracted

- **TableIndexerMode guard:** Acquires TableIndexerMode and aborts the queue with a German protocol message if Signal > 0. Reuse as carousel/indexer motor protection.
- **Acquisition symmetry:** Turns diagnostic acquisition channels on at Start Run or early Run and mirrors AcqOff at abort/Stop Run/Post Run.

## 11. SPEC v2.2 compatibility and generation cautions

- Source display has Run Duration 0.040 min while Stop Run starts at 1.000 min. For new SPEC v2.2 output, make Run Duration equal the Stop Run time unless the compiler/source template explicitly supports the legacy display semantics.
- Treat this decoded source as evidence of existing CM behavior, not as proof that a newly generated method with altered structure will open/run without CM Method Check.

## 12. Future-generation rules distilled from this method

- Reuse exact device/property symbols from this source only when the target CM configuration contains the same modules and channel names.
- Preserve acquisition start/stop symmetry, especially in every abort branch and Stop Run/Post Run cleanup.
- Preserve service-level command sequences, firmware command order, and protective delays unless validated on a decoded CMBX or in CM editor.
- Do not convert source comment rows into timed command rows; strict generated TSV must use real executable anchors.
- Any report-facing variable or log row should be retained if the downstream report likely reads it.
- Carry-over methods depend on correct preceding flow adjustment and solvent/reference vial state; avoid reordering the carry-over block without report and sequence review.

<a id="s-vas-foq-vasa-cooled-co-rc"></a>
## S-VAS-FOQ-VASA-COOLED-CO-RC: FOQ_VASA_Cooled_CO_RC

---
kb_type: chromeleon_method_summary
source_method_file: FOQ_VASA_Cooled_CO_RC.md
source_sha256_16: 972ddccc4a8fbd9a
method_family: carryover_rc_long_sample
row_count: 130
language: en
status: derived_from_decoded_cmbx_preview_not_cm_validated
---

# FOQ VASA Cooled CO RC - Method Knowledge Summary

> This file is a derived knowledge artifact, not an executable method script. It is designed so a future AI/script generator can read the intent, command patterns, variables, safety guards, and reusable structures before authoring a new strict TSV method.

## 1. Method identity and role

- **Source file:** `FOQ_VASA_Cooled_CO_RC.md`
- **Primary purpose:** Carry-over restriction-capillary high-concentration or long sample injection method. It is structurally similar to the solvent/reference method but extends the Stop Run to 7 min for the C2000 carry-over sample.
- **Sequence role:** Carry-over block long/high-concentration sample injection.
- **Method family tag:** `carryover_rc_long_sample`
- **When to reuse:** Use for the long carry-over sample run where AfterDraw wash and diagnostic acquisition are needed but chromatography lasts 7 min.
- **Source visible title/comment cues:** `Carry over (restriction capillary) with caffeine (single injector)`; `Flow through restriction capillary`
- **Detected modules/symbol roots:** `ColumnComp`, `Pump`, `PumpModule`, `Sampler`, `SamplerModule`, `System`, `UV`, `Variables`
- **Run duration declarations:** `0.9`
- **Stop Run times:** `7.0`

## 2. High-level execution story

This method configures or controls the pump, pressure limits, flow, or pump service commands; configures the column compartment temperature/valves and may use a restriction-capillary flow path; configures sampler mechanics, injection behavior, service commands, temperature, or table-indexer monitoring; configures/records UV detector channels, typically at 272 nm for caffeine methods; uses generic variables as state, calculations, flags, limits, or report outputs.

## 5. Variables, state, and custom inputs

### 5.1 Variable symbol inventory

| Variable/custom symbol | First observed role/context |
|---|---|
| `Variables.GenericFloat1` | row 27: PumpModule.Pump.Flow.Nominal = Variables.GenericFloat1;  |

## 6. Branching, triggers, and asynchronous logic

### 6.1 Model/location gates

| Row | Time | Command | Value | Comment |
|---:|---|---|---|---|
| 12 | If | SamplerModule.ModelNo="VA-A12-A" |  |  |

### 6.2 Conditional branch rows

| Row | Branch keyword | Condition/value | Comment |
|---:|---|---|---|
| 12 | If | SamplerModule.ModelNo="VA-A12-A" |  |
| 18 | End If |  |  |
| 80 | If | SamplerModule.TableIndexerMode.Signal>0 |  |
| 103 | Else |  |  |
| 104 | End If |  |  |

No trigger blocks detected.

## 9. Waits, delays, logging, aborts, and report-facing outputs

### 9.1 Wait / Delay rows

| Row | Command | Value | Comment |
|---:|---|---|---|
| 56 | Wait | UV.Ready and Pump.Ready and ColumnComp.Ready and Sampler.Ready |  |
| 100 | Delay | 1 |  |

### 9.2 Log / Protocol / Message / Abort rows

| Row | Command | Value | Comment | Role |
|---:|---|---|---|---|
| 101 | Protocol | "Indexer-Fehler. Bitte Motor des Drehtellers austauschen und den defekten Motor an R&D übergeben." |  | protocol |
| 102 | System.AbortQueue |  |  | abort_queue |
| 105 | Log | Sampler_Service.MeteringPos |  | log |

## 10. Reusable design patterns extracted

- **TableIndexerMode guard:** Acquires TableIndexerMode and aborts the queue with a German protocol message if Signal > 0. Reuse as carousel/indexer motor protection.
- **Acquisition symmetry:** Turns diagnostic acquisition channels on at Start Run or early Run and mirrors AcqOff at abort/Stop Run/Post Run.
- **Firmware/service command bridge:** Uses SamplerModule_Service or PumpModule_Service _SendCommand for firmware-level operations not exposed as normal CM properties. Preserve exact strings and ordering.

## 11. SPEC v2.2 compatibility and generation cautions

- Source display has Run Duration 0.900 min while Stop Run starts at 7.000 min. For new SPEC v2.2 output, make Run Duration equal the Stop Run time unless the compiler/source template explicitly supports the legacy display semantics.
- Treat this decoded source as evidence of existing CM behavior, not as proof that a newly generated method with altered structure will open/run without CM Method Check.

## 12. Future-generation rules distilled from this method

- Reuse exact device/property symbols from this source only when the target CM configuration contains the same modules and channel names.
- Preserve acquisition start/stop symmetry, especially in every abort branch and Stop Run/Post Run cleanup.
- Preserve service-level command sequences, firmware command order, and protective delays unless validated on a decoded CMBX or in CM editor.
- Do not convert source comment rows into timed command rows; strict generated TSV must use real executable anchors.
- Any report-facing variable or log row should be retained if the downstream report likely reads it.
- Carry-over methods depend on correct preceding flow adjustment and solvent/reference vial state; avoid reordering the carry-over block without report and sequence review.

<a id="s-vas-foq-vasa-cooled-co-rc-fill-ref-vials"></a>
## S-VAS-FOQ-VASA-COOLED-CO-RC-FILL-REF-VIALS: FOQ_VASA_Cooled_CO_RC_Fill_Ref_Vials

---
kb_type: chromeleon_method_summary
source_method_file: FOQ_VASA_Cooled_CO_RC_Fill_Ref_Vials.md
source_sha256_16: 5edccf50dde06c42
method_family: carryover_rc_fill_reference_vials
row_count: 142
language: en
status: derived_from_decoded_cmbx_preview_not_cm_validated
---

# FOQ VASA Cooled CO RC Fill Ref Vials - Method Knowledge Summary

> This file is a derived knowledge artifact, not an executable method script. It is designed so a future AI/script generator can read the intent, command patterns, variables, safety guards, and reusable structures before authoring a new strict TSV method.

## 1. Method identity and role

- **Source file:** `FOQ_VASA_Cooled_CO_RC_Fill_Ref_Vials.md`
- **Primary purpose:** Carry-over reference-vial fill method. It stops the pump to let backpressure drop, moves the needle to purge and reference-vial positions, uses high flow to purge/fill water into the solvent reference vial, stops the pump again, performs a wash, logs sampler positions, and restores the calculated flow.
- **Sequence role:** Automated filling of empty solvent reference vials before carry-over measurement.
- **Method family tag:** `carryover_rc_fill_reference_vials`
- **When to reuse:** Use when the autosampler must fill a clean solvent vial/well from the pump flow path before injecting it as a blank.
- **Source visible title/comment cues:** `Carry over (restriction capillary) with caffeine (single injector)`; `Flow through restriction capillary`
- **Detected modules/symbol roots:** `ColumnComp`, `Pump`, `PumpModule`, `Sampler`, `SamplerModule`, `System`, `UV`, `Variables`
- **Run duration declarations:** `2.0`
- **Stop Run times:** `4.0`

## 2. High-level execution story

This method configures or controls the pump, pressure limits, flow, or pump service commands; configures the column compartment temperature/valves and may use a restriction-capillary flow path; configures sampler mechanics, injection behavior, service commands, temperature, or table-indexer monitoring; configures/records UV detector channels, typically at 272 nm for caffeine methods; uses generic variables as state, calculations, flags, limits, or report outputs.

## 5. Variables, state, and custom inputs

### 5.1 Variable symbol inventory

| Variable/custom symbol | First observed role/context |
|---|---|
| `Variables.GenericFloat1` | row 119: PumpModule.Pump.Flow.Nominal = Variables.GenericFloat1; Restore to calculated flow |

## 6. Branching, triggers, and asynchronous logic

### 6.1 Model/location gates

| Row | Time | Command | Value | Comment |
|---:|---|---|---|---|
| 12 | If | SamplerModule.ModelNo="VA-A12-A" |  |  |

### 6.2 Conditional branch rows

| Row | Branch keyword | Condition/value | Comment |
|---:|---|---|---|
| 12 | If | SamplerModule.ModelNo="VA-A12-A" |  |
| 18 | End If |  |  |
| 76 | If | SamplerModule.TableIndexerMode.Signal>0 |  |
| 99 | Else |  |  |
| 100 | End If |  |  |
| 118 | If | 1=1 |  |
| 120 | End If |  |  |

No trigger blocks detected.

## 9. Waits, delays, logging, aborts, and report-facing outputs

### 9.1 Wait / Delay rows

| Row | Command | Value | Comment |
|---:|---|---|---|
| 53 | Wait | UV.Ready and Pump.Ready and ColumnComp.Ready and Sampler.Ready |  |
| 96 | Delay | 1 |  |
| 102 | Delay | 6 |  |
| 104 | Delay | 10 | Purge the needle tip, push "old" solvent into waste |
| 106 | Delay | 2 | Wait until the pump is stopped |
| 108 | Delay | 6 | Wait until the needle is on position of the solvent reference vial/well |
| 110 | Delay | 30 | Wait until the vial or well is filled up to the desired level |

### 9.2 Log / Protocol / Message / Abort rows

| Row | Command | Value | Comment | Role |
|---:|---|---|---|---|
| 97 | Protocol | "Indexer-Fehler. Bitte Motor des Drehtellers austauschen und den defekten Motor an R&D übergeben." |  | protocol |
| 98 | System.AbortQueue |  |  | abort_queue |
| 113 | Log | Sampler_Service.MeteringPos |  | log |

## 10. Reusable design patterns extracted

- **TableIndexerMode guard:** Acquires TableIndexerMode and aborts the queue with a German protocol message if Signal > 0. Reuse as carousel/indexer motor protection.
- **Acquisition symmetry:** Turns diagnostic acquisition channels on at Start Run or early Run and mirrors AcqOff at abort/Stop Run/Post Run.
- **Firmware/service command bridge:** Uses SamplerModule_Service or PumpModule_Service _SendCommand for firmware-level operations not exposed as normal CM properties. Preserve exact strings and ordering.

## 11. SPEC v2.2 compatibility and generation cautions

- Source display has Run Duration 2.000 min while Stop Run starts at 4.000 min. For new SPEC v2.2 output, make Run Duration equal the Stop Run time unless the compiler/source template explicitly supports the legacy display semantics.
- Treat this decoded source as evidence of existing CM behavior, not as proof that a newly generated method with altered structure will open/run without CM Method Check.

## 12. Future-generation rules distilled from this method

- Reuse exact device/property symbols from this source only when the target CM configuration contains the same modules and channel names.
- Preserve acquisition start/stop symmetry, especially in every abort branch and Stop Run/Post Run cleanup.
- Preserve service-level command sequences, firmware command order, and protective delays unless validated on a decoded CMBX or in CM editor.
- Do not convert source comment rows into timed command rows; strict generated TSV must use real executable anchors.
- Any report-facing variable or log row should be retained if the downstream report likely reads it.
- Carry-over methods depend on correct preceding flow adjustment and solvent/reference vial state; avoid reordering the carry-over block without report and sequence review.

<a id="s-vas-foq-vasa-cooled-co-rc-solv-ref"></a>
## S-VAS-FOQ-VASA-COOLED-CO-RC-SOLV-REF: FOQ_VASA_Cooled_CO_RC_Solv_Ref

---
kb_type: chromeleon_method_summary
source_method_file: FOQ_VASA_Cooled_CO_RC_Solv_Ref.md
source_sha256_16: 2aca9f6f0c2253d9
method_family: carryover_rc_short_reference
row_count: 130
language: en
status: derived_from_decoded_cmbx_preview_not_cm_validated
---

# FOQ VASA Cooled CO RC Solv Ref - Method Knowledge Summary

> This file is a derived knowledge artifact, not an executable method script. It is designed so a future AI/script generator can read the intent, command patterns, variables, safety guards, and reusable structures before authoring a new strict TSV method.

## 1. Method identity and role

- **Source file:** `FOQ_VASA_Cooled_CO_RC_Solv_Ref.md`
- **Primary purpose:** Carry-over restriction-capillary solvent/reference injection method. It uses the calculated restriction-capillary flow, AfterDraw wash, full diagnostic acquisition, and a short chromatographic run for solvent or low-level reference samples.
- **Sequence role:** Carry-over block solvent reference / calibration reference injection.
- **Method family tag:** `carryover_rc_short_reference`
- **When to reuse:** Use for short carry-over reference injections where wash mode is AfterDraw and run time is about 1.5 min.
- **Source visible title/comment cues:** `Carry over (restriction capillary) with caffeine (single injector)`; `Flow through restriction capillary`
- **Detected modules/symbol roots:** `ColumnComp`, `Pump`, `PumpModule`, `Sampler`, `SamplerModule`, `System`, `UV`, `Variables`
- **Run duration declarations:** `0.9`
- **Stop Run times:** `1.5`

## 2. High-level execution story

This method configures or controls the pump, pressure limits, flow, or pump service commands; configures the column compartment temperature/valves and may use a restriction-capillary flow path; configures sampler mechanics, injection behavior, service commands, temperature, or table-indexer monitoring; configures/records UV detector channels, typically at 272 nm for caffeine methods; uses generic variables as state, calculations, flags, limits, or report outputs.

## 5. Variables, state, and custom inputs

### 5.1 Variable symbol inventory

| Variable/custom symbol | First observed role/context |
|---|---|
| `Variables.GenericFloat1` | row 27: PumpModule.Pump.Flow.Nominal = Variables.GenericFloat1;  |

## 6. Branching, triggers, and asynchronous logic

### 6.1 Model/location gates

| Row | Time | Command | Value | Comment |
|---:|---|---|---|---|
| 12 | If | SamplerModule.ModelNo="VA-A12-A" |  |  |

### 6.2 Conditional branch rows

| Row | Branch keyword | Condition/value | Comment |
|---:|---|---|---|
| 12 | If | SamplerModule.ModelNo="VA-A12-A" |  |
| 18 | End If |  |  |
| 80 | If | SamplerModule.TableIndexerMode.Signal>0 |  |
| 103 | Else |  |  |
| 104 | End If |  |  |

No trigger blocks detected.

## 9. Waits, delays, logging, aborts, and report-facing outputs

### 9.1 Wait / Delay rows

| Row | Command | Value | Comment |
|---:|---|---|---|
| 56 | Wait | UV.Ready and Pump.Ready and ColumnComp.Ready and Sampler.Ready |  |
| 100 | Delay | 1 |  |

### 9.2 Log / Protocol / Message / Abort rows

| Row | Command | Value | Comment | Role |
|---:|---|---|---|---|
| 101 | Protocol | "Indexer-Fehler. Bitte Motor des Drehtellers austauschen und den defekten Motor an R&D übergeben." |  | protocol |
| 102 | System.AbortQueue |  |  | abort_queue |
| 105 | Log | Sampler_Service.MeteringPos |  | log |

## 10. Reusable design patterns extracted

- **TableIndexerMode guard:** Acquires TableIndexerMode and aborts the queue with a German protocol message if Signal > 0. Reuse as carousel/indexer motor protection.
- **Acquisition symmetry:** Turns diagnostic acquisition channels on at Start Run or early Run and mirrors AcqOff at abort/Stop Run/Post Run.
- **Firmware/service command bridge:** Uses SamplerModule_Service or PumpModule_Service _SendCommand for firmware-level operations not exposed as normal CM properties. Preserve exact strings and ordering.

## 11. SPEC v2.2 compatibility and generation cautions

- Source display has Run Duration 0.900 min while Stop Run starts at 1.500 min. For new SPEC v2.2 output, make Run Duration equal the Stop Run time unless the compiler/source template explicitly supports the legacy display semantics.
- Treat this decoded source as evidence of existing CM behavior, not as proof that a newly generated method with altered structure will open/run without CM Method Check.

## 12. Future-generation rules distilled from this method

- Reuse exact device/property symbols from this source only when the target CM configuration contains the same modules and channel names.
- Preserve acquisition start/stop symmetry, especially in every abort branch and Stop Run/Post Run cleanup.
- Preserve service-level command sequences, firmware command order, and protective delays unless validated on a decoded CMBX or in CM editor.
- Do not convert source comment rows into timed command rows; strict generated TSV must use real executable anchors.
- Any report-facing variable or log row should be retained if the downstream report likely reads it.
- Carry-over methods depend on correct preceding flow adjustment and solvent/reference vial state; avoid reordering the carry-over block without report and sequence review.

<a id="s-vas-foq-vasa-cooled-equilibration"></a>
## S-VAS-FOQ-VASA-COOLED-EQUILIBRATION: FOQ_VASA_Cooled_equilibration

---
kb_type: chromeleon_method_summary
source_method_file: FOQ_VASA_Cooled_equilibration.md
source_sha256_16: feb676882c9f4782
method_family: equilibration_flow_step
row_count: 52
language: en
status: derived_from_decoded_cmbx_preview_not_cm_validated
---

# FOQ VASA Cooled equilibration - Method Knowledge Summary

> This file is a derived knowledge artifact, not an executable method script. It is designed so a future AI/script generator can read the intent, command patterns, variables, safety guards, and reusable structures before authoring a new strict TSV method.

## 1. Method identity and role

- **Source file:** `FOQ_VASA_Cooled_equilibration.md`
- **Primary purpose:** Thermal/flow equilibration method. It waits for module readiness, then steps flow from 0.5 to 1.0 after a short delay, with a fallback Stop Run at 2 min.
- **Sequence role:** Pre-analytical equilibration before higher-flow tests and system flushes.
- **Method family tag:** `equilibration_flow_step`
- **When to reuse:** Use when the system should stabilize TCC temperature before increasing flow and beginning analytical injections.
- **Source visible title/comment cues:** `Equilibration of Oven Temperatures`; `Flow through restriction capillary`
- **Detected modules/symbol roots:** `ColumnComp`, `Pump`, `PumpModule`, `Sampler`, `SamplerModule`, `UV`, `Variables`
- **Run duration declarations:** (none)
- **Stop Run times:** `2.0`

## 2. High-level execution story

This method configures or controls the pump, pressure limits, flow, or pump service commands; configures the column compartment temperature/valves and may use a restriction-capillary flow path; configures sampler mechanics, injection behavior, service commands, temperature, or table-indexer monitoring; configures/records UV detector channels, typically at 272 nm for caffeine methods; uses generic variables as state, calculations, flags, limits, or report outputs.

## 5. Variables, state, and custom inputs

### 5.1 Variable symbol inventory

| Variable/custom symbol | First observed role/context |
|---|---|
| `Variables.GenericBool9` | row 42: Variables.GenericBool9 = 0; important for insertion of additional linearity samples if linearity-standard is empty |

## 6. Branching, triggers, and asynchronous logic

### 6.1 Model/location gates

| Row | Time | Command | Value | Comment |
|---:|---|---|---|---|
| 12 | If | SamplerModule.ModelNo="VA-A12-A" |  |  |

### 6.2 Conditional branch rows

| Row | Branch keyword | Condition/value | Comment |
|---:|---|---|---|
| 12 | If | SamplerModule.ModelNo="VA-A12-A" |  |
| 18 | End If |  |  |

No trigger blocks detected.

## 9. Waits, delays, logging, aborts, and report-facing outputs

### 9.1 Wait / Delay rows

| Row | Command | Value | Comment |
|---:|---|---|---|
| 45 | Wait | UV.Ready and Pump.Ready and ColumnComp.Ready and Sampler.Ready |  |
| 47 | Delay | 0.5 |  |
| 49 | Delay | 0.5 |  |

## 10. Reusable design patterns extracted

- No reusable cross-method pattern detected beyond basic stage/command sequencing.

## 11. SPEC v2.2 compatibility and generation cautions

- No major SPEC v2.2 structural warning detected by the automatic extractor; still run CM Method Check after packaging.
- Treat this decoded source as evidence of existing CM behavior, not as proof that a newly generated method with altered structure will open/run without CM Method Check.

## 12. Future-generation rules distilled from this method

- Reuse exact device/property symbols from this source only when the target CM configuration contains the same modules and channel names.
- Preserve acquisition start/stop symmetry, especially in every abort branch and Stop Run/Post Run cleanup.
- Preserve service-level command sequences, firmware command order, and protective delays unless validated on a decoded CMBX or in CM editor.
- Do not convert source comment rows into timed command rows; strict generated TSV must use real executable anchors.
- Any report-facing variable or log row should be retained if the downstream report likely reads it.

<a id="s-vas-foq-vasa-cooled-exceptionlog-clear"></a>
## S-VAS-FOQ-VASA-COOLED-EXCEPTIONLOG-CLEAR: FOQ_VASA_Cooled_ExceptionLog_Clear

---
kb_type: chromeleon_method_summary
source_method_file: FOQ_VASA_Cooled_ExceptionLog_Clear.md
source_sha256_16: ad9d8f4380587b82
method_family: exceptionlog_clear_safe_transport
row_count: 32
language: en
status: derived_from_decoded_cmbx_preview_not_cm_validated
---

# FOQ VASA Cooled ExceptionLog Clear - Method Knowledge Summary

> This file is a derived knowledge artifact, not an executable method script. It is designed so a future AI/script generator can read the intent, command patterns, variables, safety guards, and reusable structures before authoring a new strict TSV method.

## 1. Method identity and role

- **Source file:** `FOQ_VASA_Cooled_ExceptionLog_Clear.md`
- **Primary purpose:** Short end/protection method. Despite the filename, the visible script reconnects the sampler, switches the valve to bypass, and moves the needle up to avoid transport damage; no explicit ExceptionLog.Clear row is present in the decoded script.
- **Sequence role:** End-of-sequence safe transport state and error-queue logging side effect through disconnect/connect.
- **Method family tag:** `exceptionlog_clear_safe_transport`
- **When to reuse:** Use the bypass + MoveNeedleUp pattern for making the sampler mechanically safe before transport or final shutdown.
- **Source visible title/comment cues:** `Slow down to standby conditions: 50 µl/min`
- **Detected modules/symbol roots:** `Pump`, `PumpModule`, `Sampler`, `SamplerModule`
- **Run duration declarations:** `0.3`
- **Stop Run times:** `0.5`

## 2. High-level execution story

This method configures or controls the pump, pressure limits, flow, or pump service commands; configures sampler mechanics, injection behavior, service commands, temperature, or table-indexer monitoring.

## 5. Variables, state, and custom inputs

No Variables.* or System.*CustomVariables.* symbols detected.

## 6. Branching, triggers, and asynchronous logic

### 6.1 Model/location gates

| Row | Time | Command | Value | Comment |
|---:|---|---|---|---|
| 18 | If | SamplerModule.ModelNo="VA-A12-A" |  |  |

### 6.2 Conditional branch rows

| Row | Branch keyword | Condition/value | Comment |
|---:|---|---|---|
| 18 | If | SamplerModule.ModelNo="VA-A12-A" |  |
| 20 | End If |  |  |

No trigger blocks detected.

## 9. Waits, delays, logging, aborts, and report-facing outputs

### 9.1 Wait / Delay rows

| Row | Command | Value | Comment |
|---:|---|---|---|
| 25 | Wait | Sampler.Ready |  |
| 29 | Delay | 1 |  |

## 10. Reusable design patterns extracted

- **Firmware/service command bridge:** Uses SamplerModule_Service or PumpModule_Service _SendCommand for firmware-level operations not exposed as normal CM properties. Preserve exact strings and ordering.

## 11. SPEC v2.2 compatibility and generation cautions

- Source display has Run Duration 0.300 min while Stop Run starts at 0.500 min. For new SPEC v2.2 output, make Run Duration equal the Stop Run time unless the compiler/source template explicitly supports the legacy display semantics.
- Contains timed prose/comment rows in the decoded source display. Convert these to executable anchors or move prose into the Comment column in newly authored strict TSV. Examples: row 22 @ 0.150: Commands to log the ErrorQueue
- Treat this decoded source as evidence of existing CM behavior, not as proof that a newly generated method with altered structure will open/run without CM Method Check.

## 12. Future-generation rules distilled from this method

- Reuse exact device/property symbols from this source only when the target CM configuration contains the same modules and channel names.
- Preserve acquisition start/stop symmetry, especially in every abort branch and Stop Run/Post Run cleanup.
- Preserve service-level command sequences, firmware command order, and protective delays unless validated on a decoded CMBX or in CM editor.
- Do not convert source comment rows into timed command rows; strict generated TSV must use real executable anchors.
- Any report-facing variable or log row should be retained if the downstream report likely reads it.

<a id="s-vas-foq-vasa-cooled-flow-adjustment-restriction-capillary"></a>
## S-VAS-FOQ-VASA-COOLED-FLOW-ADJUSTMENT-RESTRICTION-CAPILLARY: FOQ_VASA_Cooled_Flow_adjustment_restriction_capillary

---
kb_type: chromeleon_method_summary
source_method_file: FOQ_VASA_Cooled_Flow_adjustment_restriction_capillary.md
source_sha256_16: 0ba72f6cc3706662
method_family: flow_adjustment_restriction_capillary
row_count: 122
language: en
status: derived_from_decoded_cmbx_preview_not_cm_validated
---

# FOQ VASA Cooled Flow adjustment restriction capillary - Method Knowledge Summary

> This file is a derived knowledge artifact, not an executable method script. It is designed so a future AI/script generator can read the intent, command patterns, variables, safety guards, and reusable structures before authoring a new strict TSV method.

## 1. Method identity and role

- **Source file:** `FOQ_VASA_Cooled_Flow_adjustment_restriction_capillary.md`
- **Primary purpose:** Restriction-capillary flow adjustment. It measures pump pressure at an initial flow, averages three pressure readings, calculates a new flow to hit target pressure, clamps to a permitted range, verifies pressure after clamping, and aborts if pressure remains outside limits.
- **Sequence role:** Pressure-based dynamic flow calibration before precision/linearity/carryover blocks.
- **Method family tag:** `flow_adjustment_restriction_capillary`
- **When to reuse:** Use when capillary backpressure tolerances require sequence-time flow adaptation before analytical tests.
- **Source visible title/comment cues:** `Generic Variables`
- **Detected modules/symbol roots:** `ColumnComp`, `Pump`, `PumpModule`, `Sampler`, `SamplerModule`, `System`, `Variables`
- **Run duration declarations:** `0.04`
- **Stop Run times:** `4.0`

## 2. High-level execution story

This method configures or controls the pump, pressure limits, flow, or pump service commands; configures the column compartment temperature/valves and may use a restriction-capillary flow path; configures sampler mechanics, injection behavior, service commands, temperature, or table-indexer monitoring; uses generic variables as state, calculations, flags, limits, or report outputs.

## 5. Variables, state, and custom inputs

### 5.1 Variable symbol inventory

| Variable/custom symbol | First observed role/context |
|---|---|
| `Variables.GenericDouble0` | row 6: Variables.GenericDouble0 = 0; logged system pressure after 30 s for calculation of new flow |
| `Variables.GenericDouble1` | row 7: Variables.GenericDouble1 = 0; logged system pressure after 45 s for calculation of new flow |
| `Variables.GenericDouble2` | row 8: Variables.GenericDouble2 = 0; logged system pressure after 60 s for calculation of new flow |
| `Variables.GenericDouble3` | row 9: Variables.GenericDouble3 = 0; average of system pressure (GenericDouble0-2) for calculatiion of new flow |
| `Variables.GenericDouble4` | row 10: Variables.GenericDouble4 = 0; logged pressure if calculated flow is below 1 mL/min or above 1.4 mL/min |
| `Variables.GenericFloat0` | row 11: Variables.GenericFloat0 = 0.7; set flow in the beginning of the method for restriction capillary path ; VAccess |
| `Variables.GenericFloat1` | row 12: Variables.GenericFloat1 = 0; new calculated flow through restriction capillary (Repor/Lin) |
| `Variables.GenericFloat2` | row 13: Variables.GenericFloat2 = 0; set flow in the beginning of the method for column/restricition capillary waste path (CO) |
| `Variables.GenericFloat3` | row 14: Variables.GenericFloat3 = 0; new, calculated flow through column (CO) |
| `Variables.GenericFloat4` | row 15: Variables.GenericFloat4 = 0; new, calculated flow through restricition capillary to waste (CO high conc. sample) |
| `Variables.GenericLong0` | row 32: Variables.GenericLong0 = 450; wanted system pressure |
| `Variables.GenericLong1` | row 33: Variables.GenericLong1 = 410; minimum system pressure |
| `Variables.GenericLong2` | row 34: Variables.GenericLong2 = 480; maximum system pressure |

## 6. Branching, triggers, and asynchronous logic

### 6.1 Model/location gates

| Row | Time | Command | Value | Comment |
|---:|---|---|---|---|
| 29 | If | SamplerModule.ModelNo="VA-A12-A" |  |  |

### 6.2 Conditional branch rows

| Row | Branch keyword | Condition/value | Comment |
|---:|---|---|---|
| 29 | If | SamplerModule.ModelNo="VA-A12-A" |  |
| 39 | End If |  |  |
| 51 | If | SamplerModule_Service.ServiceCode=Service |  |
| 52 | Else |  |  |
| 59 | End If |  |  |
| 79 | If | GenericFloat1>=0.70 AND Variables.GenericFloat1<=1.10 |  |
| 82 | Else If | Variables.GenericFloat1>=1.10 |  |
| 88 | If | Variables.GenericDouble4>=Variables.GenericLong1 AND Variables.GenericDouble4<=Variables.GenericLong2 |  |
| 91 | Else |  |  |
| 95 | End If |  |  |
| 96 | Else If | Variables.GenericFloat1<=0.7 |  |
| 102 | If | Variables.GenericDouble4>=Variables.GenericLong1 AND Variables.GenericDouble4<=Variables.GenericLong2 |  |
| 105 | Else |  |  |
| 109 | End If |  |  |
| 110 | End If |  |  |
| 111 | If | SamplerModule.TableIndexerMode.Signal>0 |  |
| 117 | Else |  |  |
| 118 | End If |  |  |

No trigger blocks detected.

## 9. Waits, delays, logging, aborts, and report-facing outputs

### 9.1 Wait / Delay rows

| Row | Command | Value | Comment |
|---:|---|---|---|
| 20 | Delay | 1 |  |
| 35 | Delay | 0.5 |  |
| 46 | Delay | 5 |  |
| 48 | Delay | 1 |  |
| 50 | Delay | 1 |  |
| 54 | Delay | 5 |  |
| 56 | Delay | 1 |  |
| 58 | Delay | 1 |  |
| 61 | Wait | Pump.Ready and ColumnComp.Ready and Sampler.Ready |  |
| 65 | Delay | 30 |  |
| 67 | Delay | 15 |  |
| 69 | Delay | 15 |  |
| 71 | Delay | 1 |  |
| 73 | Delay | 1 |  |
| 75 | Delay | 1 |  |
| 77 | Delay | 1 |  |
| 84 | Delay | 30 |  |
| 86 | Delay | 1 |  |
| 98 | Delay | 30 |  |
| 100 | Delay | 1 |  |
| 114 | Delay | 1 |  |

### 9.2 Log / Protocol / Message / Abort rows

| Row | Command | Value | Comment | Role |
|---:|---|---|---|---|
| 49 | Log | SamplerModule_Service.ServiceCode |  | log |
| 57 | Log | SamplerModule_Service.ServiceCode |  | log |
| 74 | Log | Variables.GenericDouble3 | Averaged system pressure | log |
| 78 | Log | Variables.GenericFloat1 |  | log |
| 87 | Log | Variables.GenericDouble4 |  | log |
| 92 | Protocol | "System Pressure out of Limit - Pressure to low" |  | protocol |
| 94 | System.AbortQueue |  |  | abort_queue |
| 101 | Log | Variables.GenericDouble4 |  | log |
| 106 | Protocol | "System Pressure out of Limit - Pressure to high" |  | protocol |
| 108 | System.AbortQueue |  |  | abort_queue |
| 115 | Protocol | "Indexer-Fehler. Bitte Motor des Drehtellers austauschen und den defekten Motor an R&D übergeben." |  | protocol |
| 116 | System.AbortQueue |  |  | abort_queue |

## 10. Reusable design patterns extracted

- **TableIndexerMode guard:** Acquires TableIndexerMode and aborts the queue with a German protocol message if Signal > 0. Reuse as carousel/indexer motor protection.
- **Service-level entry:** Requests service level via GetServiceCode, writes ServiceCode 87794, delays, logs service status, and often retries once if not in Service.
- **Acquisition symmetry:** Turns diagnostic acquisition channels on at Start Run or early Run and mirrors AcqOff at abort/Stop Run/Post Run.

## 11. SPEC v2.2 compatibility and generation cautions

- Source display has Run Duration 0.040 min while Stop Run starts at 4.000 min. For new SPEC v2.2 output, make Run Duration equal the Stop Run time unless the compiler/source template explicitly supports the legacy display semantics.
- Treat this decoded source as evidence of existing CM behavior, not as proof that a newly generated method with altered structure will open/run without CM Method Check.

## 12. Future-generation rules distilled from this method

- Reuse exact device/property symbols from this source only when the target CM configuration contains the same modules and channel names.
- Preserve acquisition start/stop symmetry, especially in every abort branch and Stop Run/Post Run cleanup.
- Preserve service-level command sequences, firmware command order, and protective delays unless validated on a decoded CMBX or in CM editor.
- Do not convert source comment rows into timed command rows; strict generated TSV must use real executable anchors.
- Any report-facing variable or log row should be retained if the downstream report likely reads it.
- For calculation methods, keep all intermediate variables and logs; report templates and ePanels may depend on them even if they look redundant.

<a id="s-vas-foq-vasa-cooled-in-relay-vwd"></a>
## S-VAS-FOQ-VASA-COOLED-IN-RELAY-VWD: FOQ_VASA_Cooled_IN_RELAY_VWD

---
kb_type: chromeleon_method_summary
source_method_file: FOQ_VASA_Cooled_IN_RELAY_VWD.md
source_sha256_16: a9ec99b358e23208
method_family: digital_io_relay_input
row_count: 47
language: en
status: derived_from_decoded_cmbx_preview_not_cm_validated
---

# FOQ VASA Cooled IN RELAY VWD - Method Knowledge Summary

> This file is a derived knowledge artifact, not an executable method script. It is designed so a future AI/script generator can read the intent, command patterns, variables, safety guards, and reusable structures before authoring a new strict TSV method.

## 1. Method identity and role

- **Source file:** `FOQ_VASA_Cooled_IN_RELAY_VWD.md`
- **Primary purpose:** Digital I/O verification. It cycles relay 1 and relay 2 through all relevant ON/OFF combinations and logs input 1/input 2 states after each state change.
- **Sequence role:** Relay/input wiring and assembly check.
- **Method family tag:** `digital_io_relay_input`
- **When to reuse:** Use as the minimal pattern for relay-output to digital-input loopback tests with short-circuit plugs.
- **Source visible title/comment cues:** `Digital I/O for Vanquish autosamplers`
- **Detected modules/symbol roots:** `Pump`, `PumpModule`, `Sampler`, `SamplerModule`, `UV`
- **Run duration declarations:** `0.9`
- **Stop Run times:** `0.9`

## 2. High-level execution story

This method configures or controls the pump, pressure limits, flow, or pump service commands; configures sampler mechanics, injection behavior, service commands, temperature, or table-indexer monitoring; configures/records UV detector channels, typically at 272 nm for caffeine methods.

## 5. Variables, state, and custom inputs

No Variables.* or System.*CustomVariables.* symbols detected.

## 6. Branching, triggers, and asynchronous logic

### 6.1 Model/location gates

| Row | Time | Command | Value | Comment |
|---:|---|---|---|---|
| 14 | If | SamplerModule.ModelNo="VA-A12-A" |  |  |

### 6.2 Conditional branch rows

| Row | Branch keyword | Condition/value | Comment |
|---:|---|---|---|
| 14 | If | SamplerModule.ModelNo="VA-A12-A" |  |
| 16 | End If |  |  |

No trigger blocks detected.

## 9. Waits, delays, logging, aborts, and report-facing outputs

### 9.1 Wait / Delay rows

| Row | Command | Value | Comment |
|---:|---|---|---|
| 18 | Wait | Sampler.Ready |  |
| 21 | Delay | 1 |  |

### 9.2 Log / Protocol / Message / Abort rows

| Row | Command | Value | Comment | Role |
|---:|---|---|---|---|
| 20 | Log | SamplerModule.Sampler.Location |  | log |
| 28 | Log | Sampler_Input_1.State |  | log |
| 29 | Log | Sampler_Input_2.State |  | log |
| 32 | Log | Sampler_Input_1.State |  | log |
| 33 | Log | Sampler_Input_2.State |  | log |
| 36 | Log | Sampler_Input_1.State |  | log |
| 37 | Log | Sampler_Input_2.State |  | log |
| 40 | Log | Sampler_Input_1.State |  | log |
| 41 | Log | Sampler_Input_2.State |  | log |

## 10. Reusable design patterns extracted

- **Acquisition symmetry:** Turns diagnostic acquisition channels on at Start Run or early Run and mirrors AcqOff at abort/Stop Run/Post Run.

## 11. SPEC v2.2 compatibility and generation cautions

- No major SPEC v2.2 structural warning detected by the automatic extractor; still run CM Method Check after packaging.
- Treat this decoded source as evidence of existing CM behavior, not as proof that a newly generated method with altered structure will open/run without CM Method Check.

## 12. Future-generation rules distilled from this method

- Reuse exact device/property symbols from this source only when the target CM configuration contains the same modules and channel names.
- Preserve acquisition start/stop symmetry, especially in every abort branch and Stop Run/Post Run cleanup.
- Preserve service-level command sequences, firmware command order, and protective delays unless validated on a decoded CMBX or in CM editor.
- Do not convert source comment rows into timed command rows; strict generated TSV must use real executable anchors.
- Any report-facing variable or log row should be retained if the downstream report likely reads it.

<a id="s-vas-foq-vasa-cooled-init"></a>
## S-VAS-FOQ-VASA-COOLED-INIT: FOQ_VASA_Cooled_Init

---
kb_type: chromeleon_method_summary
source_method_file: FOQ_VASA_Cooled_Init.md
source_sha256_16: 726babccdca0115d
method_family: sampler_initialization_drive_deviation
row_count: 135
language: en
status: derived_from_decoded_cmbx_preview_not_cm_validated
---

# FOQ VASA Cooled Init - Method Knowledge Summary

> This file is a derived knowledge artifact, not an executable method script. It is designed so a future AI/script generator can read the intent, command patterns, variables, safety guards, and reusable structures before authoring a new strict TSV method.

## 1. Method identity and role

- **Source file:** `FOQ_VASA_Cooled_Init.md`
- **Primary purpose:** Sampler initialization and drive-deviation logging method. It performs a normal injection, initializes the sampler, waits until ready, then logs compression, metering, needle, and horizontal drive home deviations.
- **Sequence role:** Drive functionality verification after precision/linearity sets or other mechanical stress.
- **Method family tag:** `sampler_initialization_drive_deviation`
- **When to reuse:** Use after test blocks that should be followed by a drive home-deviation audit.
- **Source visible title/comment cues:** `Initialization instrument method for VAS and DVAS`; `==> DO NOT CHANGE THIS instrument method! <==`; `The following data regarding the drive movement deviations is`
- **Detected modules/symbol roots:** `ColumnComp`, `Pump`, `PumpModule`, `Sampler`, `SamplerModule`, `System`, `UV`, `Variables`
- **Run duration declarations:** `0.2`
- **Stop Run times:** `2.5`

## 2. High-level execution story

This method configures or controls the pump, pressure limits, flow, or pump service commands; configures the column compartment temperature/valves and may use a restriction-capillary flow path; configures sampler mechanics, injection behavior, service commands, temperature, or table-indexer monitoring; configures/records UV detector channels, typically at 272 nm for caffeine methods; uses generic variables as state, calculations, flags, limits, or report outputs.

## 5. Variables, state, and custom inputs

### 5.1 Variable symbol inventory

| Variable/custom symbol | First observed role/context |
|---|---|
| `Variables.GenericFloat1` | row 34: PumpModule.Pump.Flow.Nominal = Variables.GenericFloat1;  |

## 6. Branching, triggers, and asynchronous logic

### 6.1 Model/location gates

| Row | Time | Command | Value | Comment |
|---:|---|---|---|---|
| 20 | If | SamplerModule.ModelNo="VA-A12-A" |  |  |

### 6.2 Conditional branch rows

| Row | Branch keyword | Condition/value | Comment |
|---:|---|---|---|
| 20 | If | SamplerModule.ModelNo="VA-A12-A" |  |
| 26 | End If |  |  |
| 82 | If | SamplerModule.TableIndexerMode.Signal>0 |  |
| 105 | Else |  |  |
| 106 | End If |  |  |

No trigger blocks detected.

## 9. Waits, delays, logging, aborts, and report-facing outputs

### 9.1 Wait / Delay rows

| Row | Command | Value | Comment |
|---:|---|---|---|
| 58 | Wait | UV.Ready and Pump.Ready and ColumnComp.Ready and Sampler.Ready |  |
| 102 | Delay | 1 |  |
| 109 | Wait | Sampler.Ready |  |

### 9.2 Log / Protocol / Message / Abort rows

| Row | Command | Value | Comment | Role |
|---:|---|---|---|---|
| 103 | Protocol | "Indexer-Fehler. Bitte Motor des Drehtellers austauschen und den defekten Motor an R&D übergeben." |  | protocol |
| 104 | System.AbortQueue |  |  | abort_queue |
| 110 | Log | SamplerModule.Sampler.Sampler_Service.CompressionDrvHomeDeviation |  | log |
| 111 | Log | SamplerModule.Sampler.Sampler_Service.MeteringDrvHomeDeviation |  | log |
| 112 | Log | SamplerModule.Sampler.Sampler_Service.NeedleDrvHomeDeviation |  | log |
| 113 | Log | SamplerModule.Sampler.Sampler_Service.HorizontalDrvHomeDeviation |  | log |

## 10. Reusable design patterns extracted

- **TableIndexerMode guard:** Acquires TableIndexerMode and aborts the queue with a German protocol message if Signal > 0. Reuse as carousel/indexer motor protection.
- **Acquisition symmetry:** Turns diagnostic acquisition channels on at Start Run or early Run and mirrors AcqOff at abort/Stop Run/Post Run.

## 11. SPEC v2.2 compatibility and generation cautions

- Source display has Run Duration 0.200 min while Stop Run starts at 2.500 min. For new SPEC v2.2 output, make Run Duration equal the Stop Run time unless the compiler/source template explicitly supports the legacy display semantics.
- Contains timed prose/comment rows in the decoded source display. Convert these to executable anchors or move prose into the Comment column in newly authored strict TSV. Examples: row 107 @ 0.100: Sampler is initialized to check for drive movement step deviations
- Treat this decoded source as evidence of existing CM behavior, not as proof that a newly generated method with altered structure will open/run without CM Method Check.

## 12. Future-generation rules distilled from this method

- Reuse exact device/property symbols from this source only when the target CM configuration contains the same modules and channel names.
- Preserve acquisition start/stop symmetry, especially in every abort branch and Stop Run/Post Run cleanup.
- Preserve service-level command sequences, firmware command order, and protective delays unless validated on a decoded CMBX or in CM editor.
- Do not convert source comment rows into timed command rows; strict generated TSV must use real executable anchors.
- Any report-facing variable or log row should be retained if the downstream report likely reads it.

<a id="s-vas-foq-vasa-cooled-linearity-setidlevolume"></a>
## S-VAS-FOQ-VASA-COOLED-LINEARITY-SETIDLEVOLUME: FOQ_VASA_Cooled_Linearity_SetIdleVolume

---
kb_type: chromeleon_method_summary
source_method_file: FOQ_VASA_Cooled_Linearity_SetIdleVolume.md
source_sha256_16: 4fe4332e17f2eb6f
method_family: linearity_idle_volume_setting
row_count: 58
language: en
status: derived_from_decoded_cmbx_preview_not_cm_validated
---

# FOQ VASA Cooled Linearity SetIdleVolume - Method Knowledge Summary

> This file is a derived knowledge artifact, not an executable method script. It is designed so a future AI/script generator can read the intent, command patterns, variables, safety guards, and reusable structures before authoring a new strict TSV method.

## 1. Method identity and role

- **Source file:** `FOQ_VASA_Cooled_Linearity_SetIdleVolume.md`
- **Primary purpose:** Extended linearity preparation method. It applies a sampler idle volume from the current injection custom variable and logs the resulting IdleVolume.
- **Sequence role:** State-preparation injection before a linearity set at a specific idle-volume segment.
- **Method family tag:** `linearity_idle_volume_setting`
- **When to reuse:** Use when a sequence needs to change metering-head idle volume in a separate injection before analytical injections, especially for extended linearity.
- **Source visible title/comment cues:** `Linearity and reproducibility with caffeine (single injector)`; `Flow through restriction capillary`
- **Detected modules/symbol roots:** `ColumnComp`, `Pump`, `PumpModule`, `Sampler`, `SamplerModule`, `System`, `UV`, `Variables`
- **Run duration declarations:** (none)
- **Stop Run times:** `1.5`

## 2. High-level execution story

This method configures or controls the pump, pressure limits, flow, or pump service commands; configures the column compartment temperature/valves and may use a restriction-capillary flow path; configures sampler mechanics, injection behavior, service commands, temperature, or table-indexer monitoring; configures/records UV detector channels, typically at 272 nm for caffeine methods; uses generic variables as state, calculations, flags, limits, or report outputs.

## 5. Variables, state, and custom inputs

### 5.1 Variable symbol inventory

| Variable/custom symbol | First observed role/context |
|---|---|
| `Variables.GenericFloat1` | row 27: PumpModule.Pump.Flow.Nominal = Variables.GenericFloat1;  |
| `System.Injection.CustomVariables.IdleVolume` | row 55: SamplerModule.SamplerModule_Service._SendCommand = "Sampler.SetIdleVolume="+System.Injection.CustomVariables.IdleVolume;  |

### 5.2 Required sequence/injection custom variables

- `System.Injection.CustomVariables.IdleVolume` must be defined outside the method; do not invent or rename it in generated methods.

## 6. Branching, triggers, and asynchronous logic

### 6.1 Model/location gates

| Row | Time | Command | Value | Comment |
|---:|---|---|---|---|
| 12 | If | SamplerModule.ModelNo="VA-A12-A" |  |  |

### 6.2 Conditional branch rows

| Row | Branch keyword | Condition/value | Comment |
|---:|---|---|---|
| 12 | If | SamplerModule.ModelNo="VA-A12-A" |  |
| 18 | End If |  |  |

No trigger blocks detected.

## 9. Waits, delays, logging, aborts, and report-facing outputs

### 9.1 Wait / Delay rows

| Row | Command | Value | Comment |
|---:|---|---|---|
| 53 | Wait | Sampler.Ready |  |

### 9.2 Log / Protocol / Message / Abort rows

| Row | Command | Value | Comment | Role |
|---:|---|---|---|---|
| 57 | Log | SamplerModule.Sampler.IdleVolume |  | log |

## 10. Reusable design patterns extracted

- **Firmware/service command bridge:** Uses SamplerModule_Service or PumpModule_Service _SendCommand for firmware-level operations not exposed as normal CM properties. Preserve exact strings and ordering.
- **Injection custom variables:** Uses current injection custom variables as runtime inputs; these must exist in the sequence/injection list.

## 11. SPEC v2.2 compatibility and generation cautions

- Uses custom variables that must be defined by the sequence/injection list: System.Injection.CustomVariables.IdleVolume. Do not invent these in new methods.
- Treat this decoded source as evidence of existing CM behavior, not as proof that a newly generated method with altered structure will open/run without CM Method Check.

## 12. Future-generation rules distilled from this method

- Reuse exact device/property symbols from this source only when the target CM configuration contains the same modules and channel names.
- Preserve acquisition start/stop symmetry, especially in every abort branch and Stop Run/Post Run cleanup.
- Preserve service-level command sequences, firmware command order, and protective delays unless validated on a decoded CMBX or in CM editor.
- Do not convert source comment rows into timed command rows; strict generated TSV must use real executable anchors.
- Any report-facing variable or log row should be retained if the downstream report likely reads it.

<a id="s-vas-foq-vasa-cooled-mh-max-range-in-oneinj-noudp"></a>
## S-VAS-FOQ-VASA-COOLED-MH-MAX-RANGE-IN-ONEINJ-NOUDP: FOQ_VASA_Cooled_MH_Max_Range_in_oneInj___NoUdp

---
kb_type: chromeleon_method_summary
source_method_file: FOQ_VASA_Cooled_MH_Max_Range_in_oneInj___NoUdp.md
source_sha256_16: b3ecb2618d8407f7
method_family: mh_max_range_no_udp
row_count: 162
language: en
status: derived_from_decoded_cmbx_preview_not_cm_validated
---

# FOQ VASA Cooled MH Max Range in oneInj - NoUdp - Method Knowledge Summary

> This file is a derived knowledge artifact, not an executable method script. It is designed so a future AI/script generator can read the intent, command patterns, variables, safety guards, and reusable structures before authoring a new strict TSV method.

## 1. Method identity and role

- **Source file:** `FOQ_VASA_Cooled_MH_Max_Range_in_oneInj___NoUdp.md`
- **Primary purpose:** Metering-head maximum range test in one injection, implemented as direct sequential sampler service commands instead of a UDP. It moves MD/CD over the high range, draws sample from SR:1, injects, then logs metering/compression/decompression evidence.
- **Sequence role:** Core autosampler internal MD max-range check using explicit firmware command sequence.
- **Method family tag:** `mh_max_range_no_udp`
- **When to reuse:** Use when firmware command ordering and inter-command delays must be explicit in the Run stage rather than prepackaged in a UDP.
- **Source visible title/comment cues:** `MH Max Range Test in one Injection for Cooled Samplers VC-A12-A`; `Flow through restriction capillary`
- **Detected modules/symbol roots:** `ColumnComp`, `Pump`, `PumpModule`, `Sampler`, `SamplerModule`, `System`, `UV`
- **Run duration declarations:** `0.9`
- **Stop Run times:** `2.5`

## 2. High-level execution story

This method configures or controls the pump, pressure limits, flow, or pump service commands; configures the column compartment temperature/valves and may use a restriction-capillary flow path; configures sampler mechanics, injection behavior, service commands, temperature, or table-indexer monitoring; configures/records UV detector channels, typically at 272 nm for caffeine methods.

## 5. Variables, state, and custom inputs

No Variables.* or System.*CustomVariables.* symbols detected.

## 6. Branching, triggers, and asynchronous logic

### 6.1 Model/location gates

| Row | Time | Command | Value | Comment |
|---:|---|---|---|---|
| 12 | If | SamplerModule.ModelNo="VA-A12-A" |  |  |

### 6.2 Conditional branch rows

| Row | Branch keyword | Condition/value | Comment |
|---:|---|---|---|
| 12 | If | SamplerModule.ModelNo="VA-A12-A" |  |
| 18 | End If |  |  |
| 112 | If | SamplerModule.TableIndexerMode.Signal>0 |  |
| 135 | Else |  |  |
| 136 | End If |  |  |

No trigger blocks detected.

## 9. Waits, delays, logging, aborts, and report-facing outputs

### 9.1 Wait / Delay rows

| Row | Command | Value | Comment |
|---:|---|---|---|
| 56 | Wait | UV.Ready and Pump.Ready and ColumnComp.Ready and Sampler.Ready |  |
| 79 | Delay | 5 |  |
| 81 | Delay | 5 |  |
| 83 | Delay | 5 |  |
| 85 | Delay | 5 |  |
| 87 | Delay | 5 |  |
| 89 | Delay | 5 |  |
| 91 | Delay | 5 |  |
| 93 | Delay | 5 |  |
| 95 | Delay | 5 |  |
| 97 | Delay | 5 |  |
| 99 | Delay | 5 |  |
| 101 | Delay | 5 |  |
| 103 | Delay | 3 |  |
| 105 | Delay | 5 |  |
| 107 | Delay | 5 |  |
| 109 | Delay | 5 |  |
| 111 | Delay | 5 |  |
| 132 | Delay | 1 |  |

### 9.2 Log / Protocol / Message / Abort rows

| Row | Command | Value | Comment | Role |
|---:|---|---|---|---|
| 133 | Protocol | "Indexer-Fehler. Bitte Motor des Drehtellers austauschen und den defekten Motor an R&D übergeben." |  | protocol |
| 134 | System.AbortQueue |  |  | abort_queue |
| 137 | Log | Sampler_Service.MeteringPos |  | log |

## 10. Reusable design patterns extracted

- **TableIndexerMode guard:** Acquires TableIndexerMode and aborts the queue with a German protocol message if Signal > 0. Reuse as carousel/indexer motor protection.
- **Service-level entry:** Requests service level via GetServiceCode, writes ServiceCode 87794, delays, logs service status, and often retries once if not in Service.
- **Acquisition symmetry:** Turns diagnostic acquisition channels on at Start Run or early Run and mirrors AcqOff at abort/Stop Run/Post Run.
- **Firmware/service command bridge:** Uses SamplerModule_Service or PumpModule_Service _SendCommand for firmware-level operations not exposed as normal CM properties. Preserve exact strings and ordering.

## 11. SPEC v2.2 compatibility and generation cautions

- Source display has Run Duration 0.900 min while Stop Run starts at 2.500 min. For new SPEC v2.2 output, make Run Duration equal the Stop Run time unless the compiler/source template explicitly supports the legacy display semantics.
- Treat this decoded source as evidence of existing CM behavior, not as proof that a newly generated method with altered structure will open/run without CM Method Check.

## 12. Future-generation rules distilled from this method

- Reuse exact device/property symbols from this source only when the target CM configuration contains the same modules and channel names.
- Preserve acquisition start/stop symmetry, especially in every abort branch and Stop Run/Post Run cleanup.
- Preserve service-level command sequences, firmware command order, and protective delays unless validated on a decoded CMBX or in CM editor.
- Do not convert source comment rows into timed command rows; strict generated TSV must use real executable anchors.
- Any report-facing variable or log row should be retained if the downstream report likely reads it.
- MD/CD movement commands define a mechanical test path; do not alter positions, valve numbers, fan toggles, or delays without firmware/mechanical validation.

<a id="s-vas-foq-vasa-cooled-precision-linearity"></a>
## S-VAS-FOQ-VASA-COOLED-PRECISION-LINEARITY: FOQ_VASA_Cooled_Precision_Linearity

---
kb_type: chromeleon_method_summary
source_method_file: FOQ_VASA_Cooled_Precision_Linearity.md
source_sha256_16: e59d5271ee2bda2e
method_family: precision_linearity_analytical_injection
row_count: 128
language: en
status: derived_from_decoded_cmbx_preview_not_cm_validated
---

# FOQ VASA Cooled Precision Linearity - Method Knowledge Summary

> This file is a derived knowledge artifact, not an executable method script. It is designed so a future AI/script generator can read the intent, command patterns, variables, safety guards, and reusable structures before authoring a new strict TSV method.

## 1. Method identity and role

- **Source file:** `FOQ_VASA_Cooled_Precision_Linearity.md`
- **Primary purpose:** Standard analytical injection method for precision and linearity with caffeine. It sets common chromatographic conditions, injects, records pump/temperature/UV diagnostic channels, watches TableIndexerMode, logs metering position, and queries compression/decompression values.
- **Sequence role:** Reusable short analytical run for precision and linearity injections.
- **Method family tag:** `precision_linearity_analytical_injection`
- **When to reuse:** Use as the standard caffeine injection skeleton with full diagnostics and short 1.8 min run.
- **Source visible title/comment cues:** `Linearity and reproducibility with caffeine (single injector)`; `Flow through restriction capillary`
- **Detected modules/symbol roots:** `ColumnComp`, `Pump`, `PumpModule`, `Sampler`, `SamplerModule`, `System`, `UV`
- **Run duration declarations:** `0.9`
- **Stop Run times:** `1.8`

## 2. High-level execution story

This method configures or controls the pump, pressure limits, flow, or pump service commands; configures the column compartment temperature/valves and may use a restriction-capillary flow path; configures sampler mechanics, injection behavior, service commands, temperature, or table-indexer monitoring; configures/records UV detector channels, typically at 272 nm for caffeine methods.

## 5. Variables, state, and custom inputs

No Variables.* or System.*CustomVariables.* symbols detected.

## 6. Branching, triggers, and asynchronous logic

### 6.1 Model/location gates

| Row | Time | Command | Value | Comment |
|---:|---|---|---|---|
| 12 | If | SamplerModule.ModelNo="VA-A12-A" |  |  |

### 6.2 Conditional branch rows

| Row | Branch keyword | Condition/value | Comment |
|---:|---|---|---|
| 12 | If | SamplerModule.ModelNo="VA-A12-A" |  |
| 18 | End If |  |  |
| 78 | If | SamplerModule.TableIndexerMode.Signal>0 |  |
| 101 | Else |  |  |
| 102 | End If |  |  |

No trigger blocks detected.

## 9. Waits, delays, logging, aborts, and report-facing outputs

### 9.1 Wait / Delay rows

| Row | Command | Value | Comment |
|---:|---|---|---|
| 54 | Wait | UV.Ready and Pump.Ready and ColumnComp.Ready and Sampler.Ready |  |
| 98 | Delay | 1 |  |

### 9.2 Log / Protocol / Message / Abort rows

| Row | Command | Value | Comment | Role |
|---:|---|---|---|---|
| 99 | Protocol | "Indexer-Fehler. Bitte Motor des Drehtellers austauschen und den defekten Motor an R&D übergeben." |  | protocol |
| 100 | System.AbortQueue |  |  | abort_queue |
| 103 | Log | Sampler_Service.MeteringPos |  | log |

## 10. Reusable design patterns extracted

- **TableIndexerMode guard:** Acquires TableIndexerMode and aborts the queue with a German protocol message if Signal > 0. Reuse as carousel/indexer motor protection.
- **Acquisition symmetry:** Turns diagnostic acquisition channels on at Start Run or early Run and mirrors AcqOff at abort/Stop Run/Post Run.
- **Firmware/service command bridge:** Uses SamplerModule_Service or PumpModule_Service _SendCommand for firmware-level operations not exposed as normal CM properties. Preserve exact strings and ordering.

## 11. SPEC v2.2 compatibility and generation cautions

- Source display has Run Duration 0.900 min while Stop Run starts at 1.800 min. For new SPEC v2.2 output, make Run Duration equal the Stop Run time unless the compiler/source template explicitly supports the legacy display semantics.
- Treat this decoded source as evidence of existing CM behavior, not as proof that a newly generated method with altered structure will open/run without CM Method Check.

## 12. Future-generation rules distilled from this method

- Reuse exact device/property symbols from this source only when the target CM configuration contains the same modules and channel names.
- Preserve acquisition start/stop symmetry, especially in every abort branch and Stop Run/Post Run cleanup.
- Preserve service-level command sequences, firmware command order, and protective delays unless validated on a decoded CMBX or in CM editor.
- Do not convert source comment rows into timed command rows; strict generated TSV must use real executable anchors.
- Any report-facing variable or log row should be retained if the downstream report likely reads it.

<a id="s-vas-foq-vasa-cooled-setparameters"></a>
## S-VAS-FOQ-VASA-COOLED-SETPARAMETERS: FOQ_VASA_Cooled_SetParameters

---
kb_type: chromeleon_method_summary
source_method_file: FOQ_VASA_Cooled_SetParameters.md
source_sha256_16: d9ee04b75aee1bca
method_family: set_parameters_wellness_factory_defaults
row_count: 112
language: en
status: derived_from_decoded_cmbx_preview_not_cm_validated
---

# FOQ VASA Cooled SetParameters - Method Knowledge Summary

> This file is a derived knowledge artifact, not an executable method script. It is designed so a future AI/script generator can read the intent, command patterns, variables, safety guards, and reusable structures before authoring a new strict TSV method.

## 1. Method identity and role

- **Source file:** `FOQ_VASA_Cooled_SetParameters.md`
- **Primary purpose:** Factory/qualification/wellness parameter setup method. It rejects wrong model/template combinations, enters sampler service level, disables qualification/service intervals and wellness limits, applies factory defaults/internals, verifies InjectOptimizationMode=Firmware, sets loop and nominal loop volumes, reconnects the sampler, and logs loop volume.
- **Sequence role:** Post-burn-in parameter normalization and model/template validation before FOQ tests.
- **Method family tag:** `set_parameters_wellness_factory_defaults`
- **When to reuse:** Use when a method must normalize service/wellness counters and set loop-volume metadata for Core cooled autosamplers.
- **Source visible title/comment cues:** `Set of Service, Qualification and Wellness Parameters`; `Flow through restriction capillary`
- **Detected modules/symbol roots:** `ColumnComp`, `Pump`, `PumpModule`, `Sampler`, `SamplerModule`, `System`
- **Run duration declarations:** `1.3`
- **Stop Run times:** (none)

## 2. High-level execution story

This method configures or controls the pump, pressure limits, flow, or pump service commands; configures the column compartment temperature/valves and may use a restriction-capillary flow path; configures sampler mechanics, injection behavior, service commands, temperature, or table-indexer monitoring.

## 5. Variables, state, and custom inputs

No Variables.* or System.*CustomVariables.* symbols detected.

## 6. Branching, triggers, and asynchronous logic

### 6.1 Model/location gates

| Row | Time | Command | Value | Comment |
|---:|---|---|---|---|
| 8 | If | SamplerModule.ModelNo="VA-A12-A" |  |  |
| 14 | Else If | SamplerModule.ModelNo="VC-A13-A" |  |  |
| 22 | Else If | SamplerModule.ModelNo="VH-A10-A" or SamplerModule.ModelNo="VF-A10-A" or SamplerModule.ModelNo="VH-A40-A" or SamplerModule.ModelNo="VF-A40-A" |  |  |

### 6.2 Conditional branch rows

| Row | Branch keyword | Condition/value | Comment |
|---:|---|---|---|
| 8 | If | SamplerModule.ModelNo="VA-A12-A" |  |
| 14 | Else If | SamplerModule.ModelNo="VC-A13-A" |  |
| 22 | Else If | SamplerModule.ModelNo="VH-A10-A" or SamplerModule.ModelNo="VF-A10-A" or SamplerModule.ModelNo="VH-A40-A" or SamplerModule.ModelNo="VF-A40-A" |  |
| 30 | End If |  |  |
| 43 | If | SamplerModule_Service.ServiceCode=Service |  |
| 44 | Else |  |  |
| 51 | End If |  |  |
| 94 | If | SamplerModule.Sampler.Sampler_Service.InjectOptimizationMode=Firmware |  |
| 95 | Else |  |  |
| 100 | End If |  |  |

No trigger blocks detected.

## 9. Waits, delays, logging, aborts, and report-facing outputs

### 9.1 Wait / Delay rows

| Row | Command | Value | Comment |
|---:|---|---|---|
| 16 | Delay | 1 |  |
| 18 | Delay | 1 |  |
| 20 | Delay | 1 |  |
| 24 | Delay | 1 |  |
| 26 | Delay | 1 |  |
| 28 | Delay | 1 |  |
| 38 | Delay | 5 |  |
| 40 | Delay | 1 |  |
| 42 | Delay | 1 |  |
| 46 | Delay | 5 |  |
| 48 | Delay | 1 |  |
| 50 | Delay | 1 |  |
| 73 | Delay | 2 |  |
| 75 | Delay | 2 |  |

### 9.2 Log / Protocol / Message / Abort rows

| Row | Command | Value | Comment | Role |
|---:|---|---|---|---|
| 17 | Message | "Wrong FOQ template: Please use template for uncooled version of VAS-C. " |  | message |
| 21 | System.AbortQueue |  |  | abort_queue |
| 25 | Message | "Wrong FOQ template: Please use VAS or DVAS template." |  | message |
| 29 | System.AbortQueue |  |  | abort_queue |
| 41 | Log | SamplerModule_Service.ServiceCode |  | log |
| 49 | Log | SamplerModule_Service.ServiceCode |  | log |
| 76 | Log | SamplerModule_Wellness.PowerOnTime |  | log |
| 77 | Log | SamplerModule_Wellness.OperatingHours |  | log |
| 78 | Log | DrainPumpHours |  | log |
| 79 | Log | DrainPumpTubeHours.Value |  | log |
| 80 | Log | TrayDriveMovements |  | log |
| 81 | Log | BCR_ScanCounter |  | log |
| 82 | Log | SamplerModule_Wellness.HeatingWorkLoad |  | log |
| 83 | Log | SamplerModule_Wellness.CoolingWorkLoad |  | log |
| 84 | Log | NeedleSeatCounter.Value |  | log |
| 85 | Log | NeedleMovements.Value |  | log |
| 86 | Log | HorizontalDriveMovements |  | log |
| 87 | Log | NeedleDriveMovements |  | log |
| 88 | Log | MeteringDriveMovements |  | log |
| 89 | Log | InjectValveSwitches |  | log |
| 90 | Log | TotalInjections |  | log |
| 91 | Log | NeedleObstructions |  | log |
| 92 | Log | WashPumpHours |  | log |
| 93 | Log | InjectOptimizationMode |  | log |
| 97 | Message | "The Inject Optimization is turned off. Please repeat the Factory Defaults injection" |  | message |
| 99 | System.AbortQueue |  |  | abort_queue |
| 105 | Log | NeedleMovements.Value |  | log |
| 108 | Protocol | "Sampler is disconnected and reconnected to send the default sample loop volume to CM." |  | protocol |
| 111 | Log | Sampler.LoopVolume |  | log |

## 10. Reusable design patterns extracted

- **Service-level entry:** Requests service level via GetServiceCode, writes ServiceCode 87794, delays, logs service status, and often retries once if not in Service.
- **Factory defaults:** Uses Sampler.SetFactoryDefaults and often Sampler.SetFactoryInternals to restore factory/internal sampler settings.
- **Firmware/service command bridge:** Uses SamplerModule_Service or PumpModule_Service _SendCommand for firmware-level operations not exposed as normal CM properties. Preserve exact strings and ordering.

## 11. SPEC v2.2 compatibility and generation cautions

- Contains timed prose/comment rows in the decoded source display. Convert these to executable anchors or move prose into the Comment column in newly authored strict TSV. Examples: row 53 @ 0.100: --------------------------------------------------------------------------------
- Treat this decoded source as evidence of existing CM behavior, not as proof that a newly generated method with altered structure will open/run without CM Method Check.

## 12. Future-generation rules distilled from this method

- Reuse exact device/property symbols from this source only when the target CM configuration contains the same modules and channel names.
- Preserve acquisition start/stop symmetry, especially in every abort branch and Stop Run/Post Run cleanup.
- Preserve service-level command sequences, firmware command order, and protective delays unless validated on a decoded CMBX or in CM editor.
- Do not convert source comment rows into timed command rows; strict generated TSV must use real executable anchors.
- Any report-facing variable or log row should be retained if the downstream report likely reads it.

<a id="s-vas-foq-vasa-cooled-stop"></a>
## S-VAS-FOQ-VASA-COOLED-STOP: FOQ_VASA_Cooled_STOP

---
kb_type: chromeleon_method_summary
source_method_file: FOQ_VASA_Cooled_STOP.md
source_sha256_16: 09f7dd82d447ef99
method_family: stop_reset_factory_defaults
row_count: 121
language: en
status: derived_from_decoded_cmbx_preview_not_cm_validated
---

# FOQ VASA Cooled STOP - Method Knowledge Summary

> This file is a derived knowledge artifact, not an executable method script. It is designed so a future AI/script generator can read the intent, command patterns, variables, safety guards, and reusable structures before authoring a new strict TSV method.

## 1. Method identity and role

- **Source file:** `FOQ_VASA_Cooled_STOP.md`
- **Primary purpose:** Final FOQ stop/factory-default reset method. It slows the pump to standby, validates table indexer status, enters sampler service level twice, performs an injection, applies factory defaults/internals, logs many sampler settings, marks QualificationDone and ServiceDone, reconnects the sampler, and clears ErrorLog/ExceptionLog.
- **Sequence role:** End-of-sequence internal reset, audit/logging, and service/qualification date stamping.
- **Method family tag:** `stop_reset_factory_defaults`
- **When to reuse:** Use as the pattern for final methods that must restore factory/default sampler settings, log canonical parameters, and clear module logs at the end of a qualification sequence.
- **Source visible title/comment cues:** `Slow down to standby conditions: 50 µl/min`
- **Detected modules/symbol roots:** `Pump`, `PumpModule`, `Sampler`, `SamplerModule`, `System`
- **Run duration declarations:** `2.1`
- **Stop Run times:** (none)

## 2. High-level execution story

This method configures or controls the pump, pressure limits, flow, or pump service commands; configures sampler mechanics, injection behavior, service commands, temperature, or table-indexer monitoring.

## 5. Variables, state, and custom inputs

No Variables.* or System.*CustomVariables.* symbols detected.

## 6. Branching, triggers, and asynchronous logic

### 6.1 Model/location gates

| Row | Time | Command | Value | Comment |
|---:|---|---|---|---|
| 18 | If | SamplerModule.ModelNo="VA-A12-A" |  |  |

### 6.2 Conditional branch rows

| Row | Branch keyword | Condition/value | Comment |
|---:|---|---|---|
| 18 | If | SamplerModule.ModelNo="VA-A12-A" |  |
| 20 | End If |  |  |
| 25 | If | SamplerModule.TableIndexerMode.Signal>0 |  |
| 34 | Else |  |  |
| 35 | End If |  |  |
| 42 | If | SamplerModule_Service.ServiceCode=Service |  |
| 43 | Else |  |  |
| 50 | End If |  |  |
| 110 | If | SamplerModule_Service.ServiceCode=Service |  |
| 111 | Else |  |  |
| 118 | End If |  |  |

No trigger blocks detected.

## 9. Waits, delays, logging, aborts, and report-facing outputs

### 9.1 Wait / Delay rows

| Row | Command | Value | Comment |
|---:|---|---|---|
| 31 | Delay | 1 |  |
| 37 | Delay | 5 |  |
| 39 | Delay | 1 |  |
| 41 | Delay | 1 |  |
| 45 | Delay | 5 |  |
| 47 | Delay | 1 |  |
| 49 | Delay | 1 |  |
| 53 | Delay | 2 |  |
| 55 | Delay | 2 |  |
| 98 | Wait | Sampler.Ready |  |
| 105 | Delay | 5 |  |
| 107 | Delay | 1 |  |
| 109 | Delay | 1 |  |
| 113 | Delay | 5 |  |
| 115 | Delay | 1 |  |
| 117 | Delay | 1 |  |

### 9.2 Log / Protocol / Message / Abort rows

| Row | Command | Value | Comment | Role |
|---:|---|---|---|---|
| 32 | Protocol | "Indexer-Fehler. Bitte Motor des Drehtellers austauschen und den defekten Motor an R&D übergeben." |  | protocol |
| 33 | System.AbortQueue |  |  | abort_queue |
| 40 | Log | SamplerModule_Service.ServiceCode |  | log |
| 48 | Log | SamplerModule_Service.ServiceCode |  | log |
| 56 | Log | SamplerModule.Sampler.DrawSpeed |  | log |
| 57 | Log | SamplerModule.Sampler.WashTime |  | log |
| 58 | Log | SamplerModule.Sampler.InjectResponseMode |  | log |
| 59 | Log | SamplerModule.Sampler.DrawDelay |  | log |
| 60 | Log | SamplerModule.Sampler.DispenseSpeed |  | log |
| 61 | Log | SamplerModule.Sampler.WashSpeed |  | log |
| 62 | Log | SamplerModule.Sampler.InjectWashMode |  | log |
| 63 | Log | SamplerModule.Sampler.WashTime |  | log |
| 64 | Log | SamplerModule.Sampler.Sampler_Service.InjectOptimizationMode |  | log |
| 65 | Log | SamplerModule.Sampler.PunctureOffset |  | log |
| 66 | Log | SamplerModule.DrainPumpInterval |  | log |
| 67 | Log | SamplerModule.Sampler.Sampler_Service.WashAirGap |  | log |
| 68 | Log | SamplerModule.Sampler.Sampler_Service.WashDepth |  | log |
| 69 | Log | SamplerModule.SamplerModule_Service.SamplerConfig |  | log |
| 70 | Log | SamplerModule.ModuleHardwareRevision |  | log |
| 71 | Log | SamplerModule.Sampler.LoopVolume |  | log |
| 72 | Log | SamplerModule.Sampler.NominalLoopVolume |  | log |
| 73 | Log | SamplerModule.Light | Ensure, that cabin light is on after using it for carryover test | log |
| 74 | Log | SamplerModule.Temperature.Nominal |  | log |
| 75 | Log | SamplerModule.SamplerModule_Service.TempRegulationMode |  | log |
| 76 | Log | SamplerModule.Sampler.IdleVolume |  | log |
| 77 | Log | SamplerModule.NeedleHeight |  | log |
| 78 | Log | SamplerModule.Sampler.Sampler_Service.BacklashCompensation |  | log |
| 92 | Log | SamplerModule_Wellness.Service.LastDate |  | log |
| 93 | Log | SamplerModule_Wellness.Qualification.LastDate |  | log |
| 108 | Log | SamplerModule_Service.ServiceCode |  | log |
| 116 | Log | SamplerModule_Service.ServiceCode |  | log |

## 10. Reusable design patterns extracted

- **TableIndexerMode guard:** Acquires TableIndexerMode and aborts the queue with a German protocol message if Signal > 0. Reuse as carousel/indexer motor protection.
- **Service-level entry:** Requests service level via GetServiceCode, writes ServiceCode 87794, delays, logs service status, and often retries once if not in Service.
- **Factory defaults:** Uses Sampler.SetFactoryDefaults and often Sampler.SetFactoryInternals to restore factory/internal sampler settings.
- **Log clearing:** Uses service _SendCommand ErrorLog.Clear and/or ExceptionLog.Clear; this should remain late in stop methods.
- **Acquisition symmetry:** Turns diagnostic acquisition channels on at Start Run or early Run and mirrors AcqOff at abort/Stop Run/Post Run.
- **Firmware/service command bridge:** Uses SamplerModule_Service or PumpModule_Service _SendCommand for firmware-level operations not exposed as normal CM properties. Preserve exact strings and ordering.

## 11. SPEC v2.2 compatibility and generation cautions

- No major SPEC v2.2 structural warning detected by the automatic extractor; still run CM Method Check after packaging.
- Treat this decoded source as evidence of existing CM behavior, not as proof that a newly generated method with altered structure will open/run without CM Method Check.

## 12. Future-generation rules distilled from this method

- Reuse exact device/property symbols from this source only when the target CM configuration contains the same modules and channel names.
- Preserve acquisition start/stop symmetry, especially in every abort branch and Stop Run/Post Run cleanup.
- Preserve service-level command sequences, firmware command order, and protective delays unless validated on a decoded CMBX or in CM editor.
- Do not convert source comment rows into timed command rows; strict generated TSV must use real executable anchors.
- Any report-facing variable or log row should be retained if the downstream report likely reads it.

<a id="s-vas-foq-vasa-cooled-system-flush"></a>
## S-VAS-FOQ-VASA-COOLED-SYSTEM-FLUSH: FOQ_VASA_Cooled_System_Flush

---
kb_type: chromeleon_method_summary
source_method_file: FOQ_VASA_Cooled_System_Flush.md
source_sha256_16: 3a252566b47fc11a
method_family: system_flush_repeated_injections
row_count: 76
language: en
status: derived_from_decoded_cmbx_preview_not_cm_validated
---

# FOQ VASA Cooled System Flush - Method Knowledge Summary

> This file is a derived knowledge artifact, not an executable method script. It is designed so a future AI/script generator can read the intent, command patterns, variables, safety guards, and reusable structures before authoring a new strict TSV method.

## 1. Method identity and role

- **Source file:** `FOQ_VASA_Cooled_System_Flush.md`
- **Primary purpose:** System flush method with repeated water injections from R:A3. It uses two triggers and Boolean toggles to repeatedly inject until the custom variable Injectionnumber_Flush is reached, then holds for 90 s and ends.
- **Sequence role:** Automated repeated flushing after equilibration, linearity, or idle-volume changes.
- **Method family tag:** `system_flush_repeated_injections`
- **When to reuse:** Use when a variable number of sampler injections must be performed within one method through trigger-driven looping.
- **Source visible title/comment cues:** `System Flushing`; `Flow through restriction capillary`
- **Detected modules/symbol roots:** `ColumnComp`, `Pump`, `PumpModule`, `Sampler`, `SamplerModule`, `System`, `UV`, `Variables`
- **Run duration declarations:** (none)
- **Stop Run times:** `10.0`

## 2. High-level execution story

This method configures or controls the pump, pressure limits, flow, or pump service commands; configures the column compartment temperature/valves and may use a restriction-capillary flow path; configures sampler mechanics, injection behavior, service commands, temperature, or table-indexer monitoring; configures/records UV detector channels, typically at 272 nm for caffeine methods; uses generic variables as state, calculations, flags, limits, or report outputs; uses trigger blocks for asynchronous protection, live diagnostics, looping, or endpoint logging.

## 5. Variables, state, and custom inputs

### 5.1 Variable symbol inventory

| Variable/custom symbol | First observed role/context |
|---|---|
| `Variables.GenericBool0` | row 40: Variables.GenericBool0 = 1;  |
| `Variables.GenericBool1` | row 41: Variables.GenericBool1 = 0;  |
| `Variables.GenericLong1` | row 42: Variables.GenericLong1 = 0;  |
| `System.Injection.CustomVariables.Injectionnumber_Flush` | row 66: Variables.GenericLong1>=System.Injection.CustomVariables.Injectionnumber_Flush = ;  |

### 5.2 Required sequence/injection custom variables

- `System.Injection.CustomVariables.Injectionnumber_Flush` must be defined outside the method; do not invent or rename it in generated methods.

## 6. Branching, triggers, and asynchronous logic

### 6.1 Model/location gates

| Row | Time | Command | Value | Comment |
|---:|---|---|---|---|
| 12 | If | SamplerModule.ModelNo="VA-A12-A" |  |  |

### 6.2 Conditional branch rows

| Row | Branch keyword | Condition/value | Comment |
|---:|---|---|---|
| 12 | If | SamplerModule.ModelNo="VA-A12-A" |  |
| 18 | End If |  |  |
| 66 | If | Variables.GenericLong1>=System.Injection.CustomVariables.Injectionnumber_Flush |  |
| 71 | End If |  |  |

### 6.3 Trigger blocks / trigger-like structures

#### Trigger 1: `Injection`

| Row | Time | Command | Value | Comment | Role |
|---:|---|---|---|---|---|
| 52 | Trigger | "Injection", Variables.GenericBool0=1, TrueTime=0, Delay=0, Limit=Infinite, Hysteresis=0.0 [%], AllowImmediateExecution=Yes |  |  | trigger_start |
| 53 |  | Delay | 1 |  | trigger_parameter |
| 54 |  | SamplerModule.Sampler.Inject |  |  | sampler_operation |
| 55 |  | Wait | SamplerModule.Sampler.Ready |  | wait |
| 56 |  | Delay | 0.5 |  | trigger_parameter |
| 57 |  | Variables.GenericLong1 | Variables.GenericLong1+1 |  | variable_assignment |
| 58 |  | Variables.GenericBool0 | 0 |  | variable_assignment |
| 59 |  | Variables.GenericBool1 | 1 |  | variable_assignment |
| 60 | End Trigger |  |  |  | trigger_end |

#### Trigger 2: `Toggle`

| Row | Time | Command | Value | Comment | Role |
|---:|---|---|---|---|---|
| 62 | Trigger | "Toggle", Variables.GenericBool1=1, TrueTime=0, Delay=0, Limit=Infinite, Hysteresis=0, AllowImmediateExecution=No |  |  | trigger_start |
| 63 |  | Delay | 0.5 |  | trigger_parameter |
| 64 |  | Variables.GenericBool0 | 1 |  | variable_assignment |
| 65 |  | Variables.GenericBool1 | 0 |  | variable_assignment |
| 66 | If | Variables.GenericLong1>=System.Injection.CustomVariables.Injectionnumber_Flush |  |  | branch |
| 67 |  | Delay | 90 |  | trigger_parameter |
| 68 |  | PumpModule.Pump.Pump_Pressure.AcqOff |  |  | acquisition_off |
| 69 |  | SamplerModule.TableIndexerMode.AcqOff |  |  | acquisition_off |
| 70 |  | End |  |  | method_end |
| 71 | End If |  |  |  | branch |
| 72 | End Trigger |  |  |  | trigger_end |

## 9. Waits, delays, logging, aborts, and report-facing outputs

### 9.1 Wait / Delay rows

| Row | Command | Value | Comment |
|---:|---|---|---|
| 46 | Wait | UV.Ready and Pump.Ready and ColumnComp.Ready and Sampler.Ready |  |
| 53 | Delay | 1 |  |
| 55 | Wait | SamplerModule.Sampler.Ready |  |
| 56 | Delay | 0.5 |  |
| 63 | Delay | 0.5 |  |
| 67 | Delay | 90 |  |

## 10. Reusable design patterns extracted

- **TableIndexerMode guard:** Acquires TableIndexerMode and aborts the queue with a German protocol message if Signal > 0. Reuse as carousel/indexer motor protection.
- **Acquisition symmetry:** Turns diagnostic acquisition channels on at Start Run or early Run and mirrors AcqOff at abort/Stop Run/Post Run.
- **Injection custom variables:** Uses current injection custom variables as runtime inputs; these must exist in the sequence/injection list.

## 11. SPEC v2.2 compatibility and generation cautions

- Contains legacy/CM-rendered single-row trigger syntax. For new SPEC v2.2 output, expand each trigger into Trigger + Condition/TrueTime/Delay/Limit/Hysteresis/AllowImmediateExecution parameter rows and keep actions before End Trigger.
- Contains Infinite trigger limits in source/legacy display. New SPEC requires numeric Limit or omitted Limit; use a numeric high limit such as 1000 when needed.
- Uses custom variables that must be defined by the sequence/injection list: System.Injection.CustomVariables.Injectionnumber_Flush. Do not invent these in new methods.
- Treat this decoded source as evidence of existing CM behavior, not as proof that a newly generated method with altered structure will open/run without CM Method Check.

## 12. Future-generation rules distilled from this method

- Reuse exact device/property symbols from this source only when the target CM configuration contains the same modules and channel names.
- Preserve acquisition start/stop symmetry, especially in every abort branch and Stop Run/Post Run cleanup.
- Preserve service-level command sequences, firmware command order, and protective delays unless validated on a decoded CMBX or in CM editor.
- Do not convert source comment rows into timed command rows; strict generated TSV must use real executable anchors.
- Any report-facing variable or log row should be retained if the downstream report likely reads it.

<a id="s-vas-foq-vasc-cooled-mh-max-range-in-oneinj"></a>
## S-VAS-FOQ-VASC-COOLED-MH-MAX-RANGE-IN-ONEINJ: FOQ_VASC_Cooled_MH_Max_Range_in_oneInj

---
kb_type: chromeleon_method_summary
source_method_file: FOQ_VASC_Cooled_MH_Max_Range_in_oneInj.md
source_sha256_16: ed66cc88fab8e56b
method_family: mh_max_range_udp
row_count: 149
language: en
status: derived_from_decoded_cmbx_preview_not_cm_validated
---

# FOQ VASC Cooled MH Max Range in oneInj - Method Knowledge Summary

> This file is a derived knowledge artifact, not an executable method script. It is designed so a future AI/script generator can read the intent, command patterns, variables, safety guards, and reusable structures before authoring a new strict TSV method.

## 1. Method identity and role

- **Source file:** `FOQ_VASC_Cooled_MH_Max_Range_in_oneInj.md`
- **Primary purpose:** Metering-head maximum range test in one injection using a sampler UDP. The detailed MD/CD/valve/fan/GotoPosition sequence is assembled during Instrument Setup with UdpBegin/UdpWait/UdpEnd and executed during Run by Sampler.UdpExecute.
- **Sequence role:** Core autosampler internal MD max-range check using a firmware UDP payload.
- **Method family tag:** `mh_max_range_udp`
- **When to reuse:** Use when the complex sampler command sequence should be defined before the run and executed atomically/reproducibly during the run.
- **Source visible title/comment cues:** `MH Max Range Test in one Injection for Cooled Samplers VC-A12-A`; `Flow through restriction capillary`
- **Detected modules/symbol roots:** `ColumnComp`, `Pump`, `PumpModule`, `Sampler`, `SamplerModule`, `System`, `UV`, `Variables`
- **Run duration declarations:** `0.9`
- **Stop Run times:** `2.5`

## 2. High-level execution story

This method configures or controls the pump, pressure limits, flow, or pump service commands; configures the column compartment temperature/valves and may use a restriction-capillary flow path; configures sampler mechanics, injection behavior, service commands, temperature, or table-indexer monitoring; configures/records UV detector channels, typically at 272 nm for caffeine methods; uses generic variables as state, calculations, flags, limits, or report outputs.

## 5. Variables, state, and custom inputs

### 5.1 Variable symbol inventory

| Variable/custom symbol | First observed role/context |
|---|---|
| `Variables.GenericFloat1` | row 27: PumpModule.Pump.Flow.Nominal = Variables.GenericFloat1;  |

## 6. Branching, triggers, and asynchronous logic

### 6.1 Model/location gates

| Row | Time | Command | Value | Comment |
|---:|---|---|---|---|
| 12 | If | SamplerModule.ModelNo="VA-A12-A" |  |  |

### 6.2 Conditional branch rows

| Row | Branch keyword | Condition/value | Comment |
|---:|---|---|---|
| 12 | If | SamplerModule.ModelNo="VA-A12-A" |  |
| 18 | End If |  |  |
| 99 | If | SamplerModule.TableIndexerMode.Signal>0 |  |
| 122 | Else |  |  |
| 123 | End If |  |  |

No trigger blocks detected.

## 9. Waits, delays, logging, aborts, and report-facing outputs

### 9.1 Wait / Delay rows

| Row | Command | Value | Comment |
|---:|---|---|---|
| 76 | Wait | UV.Ready and Pump.Ready and ColumnComp.Ready and Sampler.Ready |  |
| 119 | Delay | 1 |  |

### 9.2 Log / Protocol / Message / Abort rows

| Row | Command | Value | Comment | Role |
|---:|---|---|---|---|
| 120 | Protocol | "Indexer-Fehler. Bitte Motor des Drehtellers austauschen und den defekten Motor an R&D übergeben." |  | protocol |
| 121 | System.AbortQueue |  |  | abort_queue |
| 124 | Log | Sampler_Service.MeteringPos |  | log |

## 10. Reusable design patterns extracted

- **TableIndexerMode guard:** Acquires TableIndexerMode and aborts the queue with a German protocol message if Signal > 0. Reuse as carousel/indexer motor protection.
- **Acquisition symmetry:** Turns diagnostic acquisition channels on at Start Run or early Run and mirrors AcqOff at abort/Stop Run/Post Run.
- **Firmware/service command bridge:** Uses SamplerModule_Service or PumpModule_Service _SendCommand for firmware-level operations not exposed as normal CM properties. Preserve exact strings and ordering.

## 11. SPEC v2.2 compatibility and generation cautions

- Source display has Run Duration 0.900 min while Stop Run starts at 2.500 min. For new SPEC v2.2 output, make Run Duration equal the Stop Run time unless the compiler/source template explicitly supports the legacy display semantics.
- Treat this decoded source as evidence of existing CM behavior, not as proof that a newly generated method with altered structure will open/run without CM Method Check.

## 12. Future-generation rules distilled from this method

- Reuse exact device/property symbols from this source only when the target CM configuration contains the same modules and channel names.
- Preserve acquisition start/stop symmetry, especially in every abort branch and Stop Run/Post Run cleanup.
- Preserve service-level command sequences, firmware command order, and protective delays unless validated on a decoded CMBX or in CM editor.
- Do not convert source comment rows into timed command rows; strict generated TSV must use real executable anchors.
- Any report-facing variable or log row should be retained if the downstream report likely reads it.
- MD/CD movement commands define a mechanical test path; do not alter positions, valve numbers, fan toggles, or delays without firmware/mechanical validation.

<a id="s-vas-foq-vasc-cooled-temp-cooling-performance-bi"></a>
## S-VAS-FOQ-VASC-COOLED-TEMP-COOLING-PERFORMANCE-BI: FOQ_VASC_Cooled_Temp_Cooling_Performance_BI

---
kb_type: chromeleon_method_summary
source_method_file: FOQ_VASC_Cooled_Temp_Cooling_Performance_BI.md
source_sha256_16: 8b5d4ad89c685b18
method_family: cooling_performance
row_count: 86
language: en
status: derived_from_decoded_cmbx_preview_not_cm_validated
---

# FOQ VASC Cooled Temp Cooling Performance BI - Method Knowledge Summary

> This file is a derived knowledge artifact, not an executable method script. It is designed so a future AI/script generator can read the intent, command patterns, variables, safety guards, and reusable structures before authoring a new strict TSV method.

## 1. Method identity and role

- **Source file:** `FOQ_VASC_Cooled_Temp_Cooling_Performance_BI.md`
- **Primary purpose:** Cooling-performance measurement for thermostatted Vanquish autosamplers. It measures ambient temperature, sets the cabin to ambient, waits for stability, starts temperature/pressure acquisition, sets target to 4 C, and uses a trigger to log the time when cabin air reaches ambient minus 10 C.
- **Sequence role:** Burn-in / FOQ cooling performance acquisition and report anchor generation.
- **Method family tag:** `cooling_performance`
- **When to reuse:** Use for temperature step-down methods where the key result is time from ambient equilibrium to a fixed temperature delta below ambient.
- **Source visible title/comment cues:** `Cooling performance for thermostatted Vanquish autosamplers`; `Test description`
- **Detected modules/symbol roots:** `Pump`, `PumpModule`, `Sampler`, `SamplerModule`, `System`, `Variables`
- **Run duration declarations:** `30.0`
- **Stop Run times:** `30.0`

## 2. High-level execution story

This method configures or controls the pump, pressure limits, flow, or pump service commands; configures sampler mechanics, injection behavior, service commands, temperature, or table-indexer monitoring; uses generic variables as state, calculations, flags, limits, or report outputs; uses trigger blocks for asynchronous protection, live diagnostics, looping, or endpoint logging.

## 5. Variables, state, and custom inputs

### 5.1 Variable symbol inventory

| Variable/custom symbol | First observed role/context |
|---|---|
| `Variables.GenericDouble0` | row 55: Variables.GenericDouble0 = SamplerModule.Temperature.Value;  |

## 6. Branching, triggers, and asynchronous logic

### 6.2 Conditional branch rows

| Row | Branch keyword | Condition/value | Comment |
|---:|---|---|---|
| 30 | If | SamplerModule.TableIndexerMode.Signal>0 |  |
| 41 | Else |  |  |
| 42 | End If |  |  |

### 6.3 Trigger blocks / trigger-like structures

#### Trigger 1: `T1`

| Row | Time | Command | Value | Comment | Role |
|---:|---|---|---|---|---|
| 58 | Trigger | "T1", (Temperature_Air.Signal<Variables.GenericDouble0-10), TrueTime=1.00, Delay=0.0, Limit=1, Hysteresis=0.0, AllowImmediateExecution=No |  |  | trigger_start |
| 59 |  | Log | system.retention |  | log |
| 60 |  | Log | SamplerModule.Temperature.Value |  | log |
| 61 |  | Delay | 30 | This ensures that the temperature signals are acquired for another 30 s after the desired temperature is reached | trigger_parameter |
| 62 |  | SamplerModule.Temperature_AmbientAir.AcqOff |  |  | acquisition_off |
| 63 |  | SamplerModule.Temperature_Air.AcqOff |  |  | acquisition_off |
| 64 |  | SamplerModule.Temperature_RightSink.AcqOff |  |  | acquisition_off |
| 65 |  | SamplerModule.Temperature_LeftSink.AcqOff |  |  | acquisition_off |
| 66 |  | SamplerModule.Temperature_AmbientSink.AcqOff |  |  | acquisition_off |
| 67 |  | SamplerModule.Temperature.Nominal | 20 |  | property_set |
| 68 |  | PumpModule.Pump.Pump_Pressure.AcqOff |  |  | acquisition_off |
| 69 |  | SamplerModule.TableIndexerMode.AcqOff |  |  | acquisition_off |
| 70 |  | PumpModule.Pump.Flow.Nominal | 0.600 [mL/min] |  | property_set |
| 71 |  | Delay | 1 |  | trigger_parameter |
| 72 |  | End |  |  | method_end |
| 73 | End Trigger |  |  |  | trigger_end |

## 9. Waits, delays, logging, aborts, and report-facing outputs

### 9.1 Wait / Delay rows

| Row | Command | Value | Comment |
|---:|---|---|---|
| 38 | Delay | 1 |  |
| 44 | Delay | 1 |  |
| 46 | Wait | (SamplerModule.Temperature.Value-SamplerModule.Temperature.Nominal)< 0.5 and (SamplerModule.Temperature.Nominal-SamplerModule.Temperature.Value)< 0.5 |  |
| 61 | Delay | 30 | This ensures that the temperature signals are acquired for another 30 s after the desired temperature is reached |
| 71 | Delay | 1 |  |
| 84 | Delay | 1 |  |

### 9.2 Log / Protocol / Message / Abort rows

| Row | Command | Value | Comment | Role |
|---:|---|---|---|---|
| 39 | Protocol | "Indexer-Fehler. Bitte Motor des Drehtellers austauschen und den defekten Motor an R&D übergeben." |  | protocol |
| 40 | System.AbortQueue |  |  | abort_queue |
| 43 | Log | SamplerModule.Temperature_Ambient |  | log |
| 54 | Log | SamplerModule.Temperature.Value |  | log |
| 57 | Log | system.retention |  | log |
| 59 | Log | system.retention |  | log |
| 60 | Log | SamplerModule.Temperature.Value |  | log |
| 74 | Log | system.retention |  | log |

## 10. Reusable design patterns extracted

- **TableIndexerMode guard:** Acquires TableIndexerMode and aborts the queue with a German protocol message if Signal > 0. Reuse as carousel/indexer motor protection.
- **Acquisition symmetry:** Turns diagnostic acquisition channels on at Start Run or early Run and mirrors AcqOff at abort/Stop Run/Post Run.

## 11. SPEC v2.2 compatibility and generation cautions

- Contains legacy/CM-rendered single-row trigger syntax. For new SPEC v2.2 output, expand each trigger into Trigger + Condition/TrueTime/Delay/Limit/Hysteresis/AllowImmediateExecution parameter rows and keep actions before End Trigger.
- Treat this decoded source as evidence of existing CM behavior, not as proof that a newly generated method with altered structure will open/run without CM Method Check.

## 12. Future-generation rules distilled from this method

- Reuse exact device/property symbols from this source only when the target CM configuration contains the same modules and channel names.
- Preserve acquisition start/stop symmetry, especially in every abort branch and Stop Run/Post Run cleanup.
- Preserve service-level command sequences, firmware command order, and protective delays unless validated on a decoded CMBX or in CM editor.
- Do not convert source comment rows into timed command rows; strict generated TSV must use real executable anchors.
- Any report-facing variable or log row should be retained if the downstream report likely reads it.
