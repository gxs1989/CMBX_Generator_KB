# Processing Methods Tab

## Purpose

The Processing Methods tab separates processing method context from instrument methods.

- When a sequence is selected, sequence-level processing methods are shown.
- When an injection is selected, the linked processing method name from the sequence command object is shown.

Processing method formula behavior is not yet evaluated. The tab is currently focused on discovery and export.

Current TCC reverse-engineering status:

- Processing method objects are embedded in the parent sequence `.cmd`; they do not expose independent CMBX package entries.
- Exported `_embedded_N.xml` files are currently `ProcessingMethodRootControl` editor layout/configuration payloads.
- These XML files include SSTGrid and IRC-related column definitions such as `Injection Condition`, `Pass Actions`, and `Fail Actions`.
- The FOQ Knowledge Alignment processing inspector can summarize these XML
  payloads, including root type, SSTGrid/control column names, token counts,
  snippets, and row-candidate counts.
- The decoded SSTGrid nodes currently do not contain actual SST/IRC row data; row semantics are likely in a non-XML sequence-command payload or internal CM object serialization.
- For reverse generation, preserve known-good processing method payloads from a golden CMBX until the row serialization is decoded.

## User Actions

- Click `Export Selected Processing` to export selected processing method objects.
- Double-click a row to export and open the most readable exported file.

## Output

Processing method exports are written below:

```text
<output folder>/<sequence name>/<processing method export files>
```

## Implementation Boundary

UI behavior lives in `app.py` methods:

- `_build_processing_methods_tab`
- `_populate_processing_methods`
- `_populate_processing_methods_for_injection`
- `export_selected_processing`
- `open_selected_processing`

Export logic is delegated to `export_service.export_elements`.
# V1.2 Status

- Processing Methods are still extracted as embedded configuration payloads when present.
- Processing logic is not yet part of the FOQ DB calculation contract.
