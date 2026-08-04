from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import subprocess
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MANAGED_ROOT = REPO_ROOT / "knowledge_vault"
DEFAULT_KB_ROOT = Path(r"C:\ProgramData\CMBX Data Explorer Workspace\KB")
SKILL_ROOTS = (
    Path.home() / ".codex" / "skills" / "cm-method-script-author",
    Path.home() / ".codex" / "skills" / "technical-document-knowledge-extractor",
    Path.home() / ".codex" / "skills" / "cmbx-method-script-generator",
)
OPERATIONAL_MIRROR_EXCLUDES = {"Engineering", "Skills"}
SAFE_PATH_LENGTH = 235


@dataclass
class Entry:
    layer: str
    managed_path: str
    source_path: str
    sha256: str
    size: int
    duplicate_group: str = ""


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def copy_markdown(source: Path, destination: Path) -> Entry:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    return Entry(
        layer="",
        managed_path=destination.relative_to(MANAGED_ROOT).as_posix(),
        source_path="",
        sha256=digest(destination),
        size=destination.stat().st_size,
    )


def managed_destination(layer: str, relative: Path) -> Path:
    destination = MANAGED_ROOT / layer / relative
    if len(str(destination)) <= SAFE_PATH_LENGTH:
        return destination
    path_hash = hashlib.sha256(relative.as_posix().encode("utf-8")).hexdigest()[:16]
    suffix = relative.suffix or ".md"
    stem = "".join(character if character.isalnum() else "_" for character in relative.stem)
    filename = f"{stem[:48]}_{path_hash}{suffix}"
    return MANAGED_ROOT / layer / "_long_paths" / filename


def tracked_markdown() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "*.md"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    paths = []
    for relative in result.stdout.splitlines():
        if not relative or relative.startswith("knowledge_vault/"):
            continue
        path = REPO_ROOT / relative
        if path.is_file():
            paths.append(path)
    return paths


def collect(kb_root: Path) -> list[Entry]:
    entries: list[Entry] = []

    for source in sorted(kb_root.rglob("*.md")):
        relative = source.relative_to(kb_root)
        if relative.parts and relative.parts[0] in OPERATIONAL_MIRROR_EXCLUDES:
            continue
        item = copy_markdown(source, managed_destination("operational", relative))
        item.layer = "operational"
        item.source_path = f"{{programdata_kb}}/{relative.as_posix()}"
        entries.append(item)

    for source in tracked_markdown():
        relative = source.relative_to(REPO_ROOT)
        item = copy_markdown(source, managed_destination("engineering", relative))
        item.layer = "engineering"
        item.source_path = f"{{repo}}/{relative.as_posix()}"
        entries.append(item)

    for skill_root in SKILL_ROOTS:
        if not skill_root.is_dir():
            continue
        for source in sorted(skill_root.rglob("*.md")):
            relative = source.relative_to(skill_root)
            skill_relative = Path(skill_root.name) / relative
            item = copy_markdown(source, managed_destination("skills", skill_relative))
            item.layer = "skill"
            item.source_path = f"{{codex_skills}}/{skill_root.name}/{relative.as_posix()}"
            entries.append(item)

    groups: dict[str, list[Entry]] = defaultdict(list)
    for item in entries:
        groups[item.sha256].append(item)
    duplicate_number = 0
    for items in groups.values():
        if len(items) < 2:
            continue
        duplicate_number += 1
        group_id = f"DUP-{duplicate_number:03d}"
        for item in items:
            item.duplicate_group = group_id

    write_manifest(entries, kb_root)
    write_readme(entries, kb_root)
    return entries


def write_manifest(entries: list[Entry], kb_root: Path) -> None:
    payload = {
        "schema_version": 1,
        "programdata_kb": "{programdata_kb}",
        "repo_root": "{repo}",
        "entry_count": len(entries),
        "layers": {
            layer: sum(1 for item in entries if item.layer == layer)
            for layer in ("operational", "engineering", "skill")
        },
        "entries": [asdict(item) for item in entries],
    }
    MANAGED_ROOT.mkdir(parents=True, exist_ok=True)
    (MANAGED_ROOT / "manifest.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    with (MANAGED_ROOT / "manifest.csv").open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=Entry.__dataclass_fields__.keys())
        writer.writeheader()
        writer.writerows(asdict(item) for item in entries)


def write_readme(entries: list[Entry], kb_root: Path) -> None:
    counts = {
        layer: sum(1 for item in entries if item.layer == layer)
        for layer in ("operational", "engineering", "skill")
    }
    duplicate_groups = len({item.duplicate_group for item in entries if item.duplicate_group})
    text = f"""# Managed CMBX Knowledge Vault

This directory brings the project's Markdown knowledge under one Git-managed
inventory while preserving the paths required by the running application.

## Layers

| Layer | Files | Editing contract |
|---|---:|---|
| `operational` | {counts['operational']} | Snapshot of `{kb_root}`. Obsidian edits are collected back into this layer. |
| `engineering` | {counts['engineering']} | Read-only mirror of Git-tracked project Markdown. Edit the original repository file. |
| `skills` | {counts['skill']} | Read-only mirror of relevant Codex skills. Edit the installed skill source. |

Exact-content duplicates are retained where runtime compatibility requires their
legacy paths. `manifest.json` and `manifest.csv` identify {duplicate_groups}
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
"""
    (MANAGED_ROOT / "README.md").write_text(text, encoding="utf-8")


def deploy(kb_root: Path) -> None:
    manifest = json.loads((MANAGED_ROOT / "manifest.json").read_text(encoding="utf-8"))
    for entry in manifest["entries"]:
        source = MANAGED_ROOT / entry["managed_path"]
        declared = str(entry["source_path"])
        if entry["layer"] == "operational":
            destination = source_from_entry(entry, kb_root)
        elif entry["layer"] == "engineering":
            destination = kb_root / "Engineering" / declared.removeprefix("{repo}/")
        elif entry["layer"] == "skill":
            destination = kb_root / "Skills" / declared.removeprefix("{codex_skills}/")
        else:
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def source_from_entry(entry: dict[str, object], kb_root: Path) -> Path:
    source = str(entry["source_path"])
    if source.startswith("{programdata_kb}/"):
        return kb_root / source.removeprefix("{programdata_kb}/")
    if source.startswith("{repo}/"):
        return REPO_ROOT / source.removeprefix("{repo}/")
    if source.startswith("{codex_skills}/"):
        relative = Path(source.removeprefix("{codex_skills}/"))
        if relative.parts:
            for skill_root in SKILL_ROOTS:
                if skill_root.name == relative.parts[0]:
                    return skill_root.joinpath(*relative.parts[1:])
        return Path.home() / ".codex" / "skills" / relative
    raise ValueError(f"Unsupported source path: {source}")


def verify(kb_root: Path) -> list[str]:
    manifest = json.loads((MANAGED_ROOT / "manifest.json").read_text(encoding="utf-8"))
    errors: list[str] = []
    for entry in manifest["entries"]:
        managed = MANAGED_ROOT / entry["managed_path"]
        source = source_from_entry(entry, kb_root)
        for label, path in (("managed", managed), ("source", source)):
            if not path.is_file():
                errors.append(f"Missing {label}: {path}")
        if managed.is_file() and digest(managed) != entry["sha256"]:
            errors.append(f"Managed hash changed: {managed}")
        if source.is_file() and digest(source) != entry["sha256"]:
            errors.append(f"Source differs from collected copy: {source}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect and deploy the managed CMBX Markdown vault.")
    parser.add_argument("command", choices=("collect", "deploy", "verify"))
    parser.add_argument("--kb-root", type=Path, default=DEFAULT_KB_ROOT)
    args = parser.parse_args()
    if args.command == "collect":
        entries = collect(args.kb_root)
        print(f"Collected {len(entries)} Markdown files into {MANAGED_ROOT}")
        return 0
    if args.command == "deploy":
        deploy(args.kb_root)
        print(f"Deployed managed Markdown to {args.kb_root}")
        return 0
    errors = verify(args.kb_root)
    if errors:
        print("\n".join(errors))
        return 1
    print("Managed Markdown vault verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
