# Managed CMBX Knowledge Vault

This directory brings the project's Markdown knowledge under one Git-managed
inventory while preserving the paths required by the running application.

## Layers

| Layer | Files | Editing contract |
|---|---:|---|
| `operational` | 219 | Snapshot of `C:\ProgramData\CMBX Data Explorer Workspace\KB`. Obsidian edits are collected back into this layer. |
| `engineering` | 108 | Read-only mirror of Git-tracked project Markdown. Edit the original repository file. |
| `skills` | 6 | Read-only mirror of relevant Codex skills. Edit the installed skill source. |

Exact-content duplicates are retained where runtime compatibility requires their
legacy paths. `manifest.json` and `manifest.csv` identify 77
duplicate groups by SHA-256 so they can be consolidated deliberately later.
Managed copies whose full Windows path would exceed the safe limit are stored under
`_long_paths` with a stable hash suffix; the manifest preserves and restores their
original source path.

## Commands

```powershell
python tools/sync_kb_vault.py collect
python tools/sync_kb_vault.py verify
python tools/sync_kb_vault.py deploy
```

- `collect` refreshes this Git-managed inventory from ProgramData, tracked project
  documents, and relevant Codex skills. Collection is non-destructive: the
  manifest defines the active inventory and no KB directory is deleted.
- `verify` checks every managed copy against its declared source.
- `deploy` refreshes the ProgramData Obsidian vault from the managed operational
  layer and adds read-only `Engineering` and `Skills` mirrors.

Runtime outputs, caches, user uploads, database credentials, API keys, and generated
job artifacts are excluded.
