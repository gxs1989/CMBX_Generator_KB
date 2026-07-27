from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os
import re
from typing import Iterable


DEFAULT_CODEX_HOME = Path(os.environ.get("CODEX_HOME", "") or Path.home() / ".codex")


@dataclass(frozen=True)
class SkillCatalogEntry:
    name: str
    description: str
    source: str
    path: Path
    skill_file: Path
    reference_files: tuple[Path, ...]
    kb_references: tuple[str, ...]


def discover_skill_catalog_entries(codex_home: Path = DEFAULT_CODEX_HOME) -> tuple[SkillCatalogEntry, ...]:
    entries: list[SkillCatalogEntry] = []
    seen: set[Path] = set()
    for skill_file, source in _iter_skill_files(codex_home):
        resolved = skill_file.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        text = _read_text(skill_file)
        metadata = _frontmatter(text)
        name = metadata.get("name") or skill_file.parent.name
        description = metadata.get("description") or ""
        reference_files = tuple(sorted((skill_file.parent / "references").glob("**/*"), key=lambda p: str(p).lower())) if (skill_file.parent / "references").exists() else ()
        reference_files = tuple(path for path in reference_files if path.is_file())
        kb_references = _extract_kb_references(text, reference_files)
        entries.append(
            SkillCatalogEntry(
                name=name,
                description=description,
                source=source,
                path=skill_file.parent,
                skill_file=skill_file,
                reference_files=reference_files,
                kb_references=kb_references,
            )
        )
    return tuple(sorted(entries, key=lambda item: (item.source, item.name.lower())))


def skill_catalog_overview_markdown(entries: Iterable[SkillCatalogEntry]) -> str:
    rows = list(entries)
    lines = [
        "# Skills Catalog",
        "",
        f"Total skills: {len(rows)}",
        "",
        "| Source | Skill | References | KB references |",
        "|---|---|---:|---:|",
    ]
    for entry in rows:
        lines.append(f"| {entry.source} | {entry.name} | {len(entry.reference_files)} | {len(entry.kb_references)} |")
    return "\n".join(lines)


def skill_catalog_entry_markdown(entry: SkillCatalogEntry) -> str:
    lines = [
        f"# {entry.name}",
        "",
        f"Source: `{entry.source}`",
        f"Path: `{entry.path}`",
        "",
        "## Description",
        "",
        entry.description or "-",
        "",
        "## Reference Files",
        "",
    ]
    if entry.reference_files:
        lines.extend(f"- `{path}`" for path in entry.reference_files)
    else:
        lines.append("- None")
    lines.extend(["", "## KB / Evidence References", ""])
    if entry.kb_references:
        lines.extend(f"- `{ref}`" for ref in entry.kb_references)
    else:
        lines.append("- No explicit KB reference paths found in skill text.")
    return "\n".join(lines)


def _iter_skill_files(codex_home: Path) -> Iterable[tuple[Path, str]]:
    personal_root = codex_home / "skills"
    if personal_root.exists():
        for path in personal_root.glob("*/SKILL.md"):
            source = "system" if path.parent.parent.name == ".system" or path.parent.parent == personal_root / ".system" else "personal"
            if ".system" in path.parts:
                source = "system"
            yield path, source
        system_root = personal_root / ".system"
        if system_root.exists():
            for path in system_root.glob("*/SKILL.md"):
                yield path, "system"
    plugin_cache = codex_home / "plugins" / "cache"
    if plugin_cache.exists():
        for path in plugin_cache.rglob("SKILL.md"):
            yield path, "plugin"


def _frontmatter(text: str) -> dict[str, str]:
    clean = text.lstrip("\ufeff")
    if not clean.startswith("---"):
        return {}
    parts = clean.split("---", 2)
    if len(parts) < 3:
        return {}
    metadata: dict[str, str] = {}
    current_key = ""
    current_value: list[str] = []
    for raw_line in parts[1].splitlines():
        if not raw_line.strip():
            continue
        if not raw_line.startswith((" ", "\t")) and ":" in raw_line:
            if current_key:
                metadata[current_key] = " ".join(current_value).strip().strip('"')
            key, value = raw_line.split(":", 1)
            current_key = key.strip()
            current_value = [value.strip().strip("> ").strip()]
        elif current_key:
            current_value.append(raw_line.strip())
    if current_key:
        metadata[current_key] = " ".join(current_value).strip().strip('"')
    return metadata


def _extract_kb_references(skill_text: str, reference_files: tuple[Path, ...]) -> tuple[str, ...]:
    texts = [skill_text]
    for path in reference_files:
        if path.suffix.lower() in {".md", ".txt", ".yaml", ".yml"}:
            texts.append(_read_text(path))
    joined = "\n".join(texts)
    refs: set[str] = set()
    patterns = [
        r"`([^`]*(?:KB|FOQ|CMBX|CM_|TCC_|VDAD|method|report|formula)[^`]*)`",
        r"([A-Za-z]:\\[^\n\r|`]+)",
        r"(cmbx_data_explorer/[^\s`|]+)",
        r"(cmbx_data_explorer\\[^\s`|]+)",
        r"((?:FOQ|CM|knowledge_base|references)[/\\][^\s`|]+)",
    ]
    for pattern in patterns:
        for match in re.finditer(pattern, joined, flags=re.IGNORECASE):
            value = match.group(1).strip().strip(".,;)")
            if not value or len(value) < 4:
                continue
            if any(token in value.lower() for token in ("todo", "example")):
                continue
            refs.add(value)
    return tuple(sorted(refs, key=str.lower))


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
