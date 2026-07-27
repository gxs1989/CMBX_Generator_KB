# Instrument Methods Tab

## Purpose

The Instrument Methods tab shows method logic only. Processing methods and report templates stay in their own tabs.

- When a sequence is selected, all instrument methods in that sequence are listed.
- When an injection is selected, the linked instrument method resolved from the sequence command object is listed.
- External TXT exports placed beside the CMBX are shown only as reference material for comparison.

## Internal CM-Like Reader

The lower `CM Method Table Preview` table is an internal reader for method logic.

The preview intentionally follows the Chromeleon method editor layout as closely as possible:

```text
row number / Kind / Time / Command / Value / Comment
```

When a CM TXT method export exists beside the CMBX, the preview uses that TXT because it preserves the closest CM table structure. When no TXT reference exists, the embedded CMBX method is decoded from the method CpXm payload and converted into the same four-column table shape.

CM-like rendering details:

- The leftmost `#` column is the method row number and is used for screenshot/manual alignment.
- `Kind` is the structural row type. Green comment/header rows are `Kind=Comment`, not executable commands, even though the text appears in the visual `Command` column.
- Stage rows show the stage start time in `Time`, the stage name in `Command`, and stage duration in `Value` when the XML timetable provides enough points, for example `Duration = 30.000 [min]`.
- `If`, `Else If`, `Else`, and `End If` are rendered as control-flow rows. Conditions are shown in `Value`; child commands stay on their own rows.
- The final `End` command is appended to embedded-method previews to match the visible CM method-script boundary.
- Styled Excel previews use the same row-numbered table shape and include `Kind` so future copy/paste or generation logic can preserve comment vs command rows.

Visual cues:

- Orange rows: initial-time or equilibration/setup rows.
- Green rows: `If`, `Else If`, `Else`, `Trigger`, and block contents.
- Green text: comment/header-like rows.

The main reader is intentionally a view. The comparison window allows temporary cell editing for visual review, but it does not write edited method logic back into the CMBX or regenerate a method.

## Selected Methods

The upper comparison table records the two method sources currently selected for comparison. Methods are added by either:

- Selecting a method row and clicking `Add To Compare`.
- Dragging a method row from the method list into this comparison table.

```text
Benchmark / CMBX / Sequence / Method / Source
```

This keeps method comparison context visible without needing to keep multiple CMBX trees expanded.

## Method Comparison

The comparison supports two methods. When the second method is dropped into the comparison table, the side-by-side comparison opens automatically.

The comparison opens a side-by-side CM-like table:

```text
left method table   |   right method table
```

Rows that differ are highlighted. Double-clicking a cell opens an inline editor for that preview cell, which is useful for manual reconciliation and notes during reverse engineering.

## User Actions

- Select a method row to preview the decoded flow.
- Click `Add To Compare` or drag a method row into `Selected Methods For Compare`.
- Drag a second method row into the comparison table to compare side by side.
- Double-click a selected comparison row to remove it.
- Click `Export Selected Methods` to export embedded method payloads.
- Double-click a row to generate and open a styled CM-like `.xlsx` preview when possible.

Open priority after export:

```text
embedded method flow TSV
embedded method flow TXT
method XML
metadata TXT
binary payload
```

Double-click preview exports are written as styled Excel workbooks and use the same row tags as the internal preview.

## Output

Original method exports are written below:

```text
<output folder>/<sequence name>/<method export files>
```

Styled CM-like preview workbooks are written below:

```text
<output folder>/<sequence name>/_preview/instrument_method_previews/<method>.xlsx
```

If an exported method is linked through an injection, the method still belongs to the sequence-level method context.

## Implementation Boundary

UI behavior lives in `app.py` methods:

- `_build_method_context_tab`
- `_populate_method_context`
- `_populate_sequence_methods`
- `preview_selected_method`
- `compare_loaded_instrument_methods`
- `_add_method_to_compare`
- `_refresh_method_compare_selection_table`
- `export_selected_methods`
- `open_selected_methods`

Embedded method decoding is delegated to:

- `embedded_method_extractor.extract_embedded_instrument_method`
- `chromeleon_method_decoder.decode_cpxm_method_xml`
- `method_xml_flow.build_method_flow_rows`
# V1.2 Status

- Instrument Methods continue to decode and compare embedded method flow where Chromeleon runtime support is available.
- Future CM formula understanding will use this tab alongside report formula dependency traces to connect method RetTime generation with report calculations.
