# KB Index Tab

The `KB Index` tab exposes `KB_INDEX.md` inside the application. It prefers the
workspace KB index:

```text
C:\ProgramData\CMBX Data Explorer Workspace\KB\KB_INDEX.md
```

and falls back to the project copy:

```text
cmbx_data_explorer/docs/KB_INDEX.md
```

Purpose:

- Show the current knowledge-base version table in the UI.
- Classify KB entries by functional area, such as `FOQ / TCC`,
  `FOQ / Detector`, `CMBX / Methods`, `CMBX / Reports`, `CMBX / Formulas`,
  and `Generation`.
- Show a left-side grouped category navigator with `All`, knowledge-layer
  parents (`FOQ`, `CM`, `CMBX`, `Generation`, `General`), and child
  categories such as `FOQ / TCC` and `CMBX / Reports`.
- Each group/category row includes a KB count. Selecting a parent group renders
  all KB content inside that group; selecting a child category renders that
  category only.
- Show the KB entries for the active category in the right-side table.
- Filter entries by category and index text.
- Keep the raw Markdown index visible for review.
- Show an `Index Overview` panel with the full category inventory and status
  counts.
- Provide a quick selected-entry detail panel for KB name, version, coverage,
  status, and local file references.
- Render the full content of the selected KB row's local Markdown/text files in
  the lower panel.
- Render every KB file in a selected group or category when the left navigator
  row is selected; selecting `All` renders the full indexed KB set.
- Explicitly render the active category or the entire index with the
  `Render Category` and `Render All` buttons, so full-content reading does not
  depend on remembering the category-row click behavior.
- Auto-discover additional Markdown files under the workspace KB root that are
  not explicitly listed in the version table, such as the CM instrument command
  KB.
- Open either the selected KB source file or the rendered Markdown review
  window from the toolbar.

Scope:

- This tab is an index and navigation aid.
- It is now also a light KB reader for the files referenced by the index.
- It does not calculate FOQ results or perform TD-to-CMBX alignment.
- The `FOQ Knowledge Alignment` tab consumes the parsed KB/CMBX evidence for
  detailed test-level alignment.

Detail panels:

- `Rendered Markdown`: concatenated full content of resolved local files for a
  selected KB entry, or every resolved file in the selected group/category.
  Wildcard references are expanded with a small safety cap.
- `Selected KB`: normalized metadata and listed local files for a specific KB,
  or a compact entry list for the active category.
- `Index Overview`: generated category/status summary from the parsed and
  auto-discovered KB entries.
- `Index Markdown`: raw KB index file.

Toolbar actions:

- `Open Source`: opens the preferred resolved source file for a selected KB
  entry. Category rows do not open a single source file.
- `Open Full Render`: opens the same full rendered Markdown shown in the lower
  panel in a larger review window.
- `Render Category`: clears any selected KB row and renders the current
  navigator scope in the lower `Rendered Markdown` panel.
- `Render All`: clears search/category filters and renders every indexed or
  auto-discovered KB entry in the lower `Rendered Markdown` panel.
