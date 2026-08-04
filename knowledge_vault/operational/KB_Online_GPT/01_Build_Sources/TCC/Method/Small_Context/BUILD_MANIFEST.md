# Small-Context Method KB Build Manifest

Build_Date: 2026-07-23  
Per_File_Byte_Limit: 199999  
Upload_File_Count: 3

## Delivery Files

| File | Bytes | Status |
|---|---:|---|
| `01_METHOD_SPEC.md` | 44,231 | OK |
| `02_METHOD_ORIGINAL_SCRIPTS.md` | 168,443 | OK |
| `03_METHOD_SUMMARIES.md` | 178,626 | OK |

## Selected Stable IDs

- ORIGINAL: `M-TCC-ASYNCHRON8, M-TCC-PREHEATER, M-TCC-STRESS-TEST-5S, M-TCC-STRESS-TEST-5S-REALPREHEATER-PCC-OFF-10MIN-EQUIBRATION, M-TCC-SYNCHRON8, M-TCC-HEAT-COOL-VA, M-TCC-HEAT-COOL-VCVH, M-TCC-ACCURACY-VA, M-TCC-ACCURACY-VCVH, M-TCC-CALIBRATION-VA, M-TCC-CALIBRATION-VCVH, M-TCC-PRECISION, M-TCC-PRECISION-FAN, M-TCC-STABILITY-VA, M-TCC-STABILITY-VCVH, M-TCC-STABILITY-PCC-VA, M-TCC-STABILITY-PCC-VCVH, M-TCC-VALVES-VA, M-TCC-VALVES-VCVH`
- SUMMARY: `K001, K002, K003, K004, B005, B006, B007, B008, B009`

## Scope

Included: TCC temperature methods, Preheater, standard Valves, and representative periodic Stress Trigger methods.
Omitted: unrelated service, error-log, factory-default, liquid-leak, burn-in and non-selected stress variants.

The small-context package is a selected derivative of the full Method KB. Rebuild it whenever the full SPEC, ORIGINAL, or SUMMARY changes.
Only the three delivery files are uploaded to the web model. This manifest remains in `01_Build_Sources/TCC/Method/Small_Context`.
