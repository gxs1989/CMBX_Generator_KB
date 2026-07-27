# Raw Plot Tab

## Purpose

The Raw Plot tab compares raw signal channels from one or more loaded CMBX packages.

It is separated from the Raw Filter Export tab so batch export and visual comparison do not compete for the same space.

## Selection Model

Channels can be added from either place:

- `Sequence Data` tree signal nodes through the right-click menu.
- `Raw Filter Export` table rows through legacy plot actions.

Multiple signal nodes can be selected in `Sequence Data`, then added to the Raw Plot selection in one action.

## Selected Channels

The top table lists the channels currently used by the plot:

```text
Benchmark / CMBX / Sequence / Injection / Channel
```

This keeps comparison context visible without requiring the user to keep several CMBX trees expanded.

The table supports multi-select. The plot draws the currently selected rows in this table, so users can keep a larger channel pool and quickly compare different subsets.

Right-click actions on this table:

- `Plot Selected Channels`
- `Set Benchmark From Selection`
- `Remove Selected`
- `Clear Plot`

## Benchmark

`Set Benchmark` marks the first selected channel as the benchmark series.

The benchmark is drawn with a darker, thicker line and a `BENCHMARK` legend prefix. Other selected channels are drawn in comparison colors.

## Performance

Decoded raw points are cached per package, signal id, and raw filename:

```text
CMBX path + signal id + raw file
```

This avoids repeatedly extracting and decoding the same raw channel when switching previews or rebuilding comparison plots.

Large channels are sampled before drawing. Exported raw channel files still use the full decoded dataset.

## Implementation Boundary

UI behavior lives in `app.py` methods:

- `_build_raw_plot_tab`
- `plot_selected_raw_channels`
- `set_raw_plot_benchmark`
- `clear_raw_plot`
- `_set_raw_plot_selection_rows`
- `_selected_signal_items_for_plot`
- `_draw_raw_plot_series`

Raw decoding is shared with export/preview helpers through `_decode_signal_preview_points`.

## V1.2 Status

- Raw Plot remains the first functional tab.
- Channel data is cached after decoding so repeated visual comparisons do not reload the same signal.
- Multiple channels can be added from the Sequence Data tree context menu.
- `Plot Selected Channels` is now a Selected Channels table context-menu action.
- The plot is driven by the table's current multi-selection.
