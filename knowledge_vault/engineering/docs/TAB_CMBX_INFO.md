# CMBX Info Tab

## Purpose

The CMBX Info tab shows metadata and diagnostic text for the current package, sequence, injection, or method/report object.

It is intentionally read-only and does not export files directly.

## User Actions

- Select package tree nodes to update the info text.
- Use `CMBX Notes` in the header for the global parsing and dependency explanation.

## Implementation Boundary

UI behavior lives in `app.py` methods:

- `_build_info_tab`
- `_show_package_summary`
- `_show_element_info`
- `_set_info`

Detailed reverse engineering notes are maintained in `CM_FORMULA_REVERSE_ENGINEERING.md`.
# V1.2 Status

- CMBX Info reflects faster package load and cached package summary counts.
- Use this tab to confirm loaded package counts before FOQ DB preview/export/upload.
