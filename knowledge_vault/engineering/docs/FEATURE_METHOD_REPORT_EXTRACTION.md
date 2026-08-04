# Feature: Embedded Method and Report Extraction

## Purpose

Extract instrument methods and report templates directly from a CMBX package so users do not need to manually export those objects from Chromeleon.

## User Workflow

1. Load a CMBX file.
2. Select an instrument method or report template object.
3. Click `Export Selected`.
4. Review exported binary payloads, decoded XML, method flow tables, report sheet lists, and report object formula tables.

## Main Modules

```text
embedded_method_extractor.py
chromeleon_method_decoder.py
instrument_method_parser.py
method_xml_flow.py
sequence_cmd_parser.py
embedded_report_extractor.py
```

## Inputs

- Sequence command payload, for example `6545327.seq_1.cmd`.
- Embedded method/report binary blocks.
- Optional Chromeleon runtime DLLs for CpXm decoding.

## Outputs

Instrument method exports:

```text
*_embedded.instmeth.bin
*_embedded_payload.bin
*_embedded_payload.cpxm.bin
*_embedded_method.xml
*_embedded_method_flow.txt
*_embedded_method_flow.tsv
*_embedded_metadata.txt
```

Report template exports:

```text
*_embedded.report.bin
*_embedded_report.cpxm.bin
*_embedded_report.xml
*_report_sheets.tsv
*_report_sheet_objects.tsv
*_embedded_report_metadata.txt
```

## Current Behavior

- Finds embedded method/report payload slices in the parent sequence command data.
- Decodes readable XML when the local runtime supports it.
- Converts method XML into a more readable flow.
- Converts report template XML into sheet and sheet-object tables.

## Known Limits

- Some method exports from Chromeleon UI may be summaries; CMBX embedded method extraction is the more reliable source.
- Method flow is a readable reconstruction, not yet a full reverse-generated Chromeleon method.
- Processing method extraction is not the current priority.

## Verification

- Method and report template extraction has been validated against the method TXT reference and report sheets in `20260701_New`.
