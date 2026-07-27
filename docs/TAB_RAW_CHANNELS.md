# Raw Filter Export Tab

## Purpose

The `Raw Filter Export` tab is an advanced raw-channel filter and batch export workspace.

Direct one-off exports are handled from the `Sequence Data` tree:

- Right-click a signal channel to export that channel.
- Right-click an injection to export all raw channels in that injection.
- Right-click a sequence to export all raw channels in that sequence.

Plot preview is handled by the separate `Raw Plot` tab.

## Filter Model

The filter can match across all loaded CMBX packages:

```text
Sequence contains / Injection contains / Channel contains
```

Example:

```text
Injection = accuracy
Channel   = CC_TEMP
```

This finds matching channels across different loaded sequences/packages without manually expanding every CMBX in the tree.

## User Actions

- Click `Apply Filter` to list matched raw channels.
- Click `Export Filtered` to export all matched raw channels.
- Select rows in the result table and double-click to export/open only selected rows.

## Output

Raw channel exports are written below:

```text
<output folder>/<sequence name>/<injection name>/<channel name>.tsv
```

The internal raw extraction cache is also kept below the sequence folder so one CMBX package stays grouped together.

## Implementation Boundary

UI behavior lives in `app.py` methods:

- `_build_channels_tab`
- `apply_raw_channel_filter`
- `export_filtered_channels`
- `open_selected_channels`
- `_filtered_raw_channel_items`

Export logic is delegated to `export_service.export_elements`.
# V1.2 Status

- Raw channel browsing benefits from faster package scanning and cached package element lists.
- Non-CMBX files are hidden from the Sequence Data package view.
- Raw channel export remains separate from Raw Plot so batch export and visual inspection stay independent.
