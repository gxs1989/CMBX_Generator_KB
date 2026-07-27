from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
from typing import Iterable


DEFAULT_PROJECT_KB_INDEX = Path(__file__).resolve().parent / "docs" / "KB_INDEX.md"
DEFAULT_WORKSPACE_ROOT = Path(
    os.environ.get("CMBX_DATA_EXPLORER_WORKSPACE", "")
    or Path(os.environ.get("PROGRAMDATA", r"C:\ProgramData")) / "CMBX Data Explorer Workspace"
)
DEFAULT_WORKSPACE_KB_INDEX = DEFAULT_WORKSPACE_ROOT / "KB" / "KB_INDEX.md"
PROJECT_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class KbIndexEntry:
    kb_name: str
    version: str
    update_date: str
    coverage: str
    status: str
    local_files: tuple[str, ...]


@dataclass(frozen=True)
class KbIndexResolvedFile:
    label: str
    path: Path | None
    exists: bool
    is_pattern: bool = False
    note: str = ""


KB_CATEGORY_ORDER = {
    "FOQ 测试知识 / TCC": 10,
    "FOQ 测试知识 / Detector": 20,
    "FOQ 测试知识 / Pump": 30,
    "FOQ 测试知识 / Autosampler": 40,
    "方法脚本知识 / CM命令": 50,
    "方法脚本知识 / Method Role": 55,
    "方法脚本知识 / MD格式与渲染": 60,
    "CMBX读取 / 解析与提取": 70,
    "CMBX读取 / 方法与报告证据": 75,
    "CMBX生成 / 生成策略": 80,
    "CMBX生成 / 打包与导出": 85,
    "报告与公式 / Report Template": 90,
    "报告与公式 / Formula与DB": 95,
    "Skills / 工作流": 100,
    "未分类 / General": 999,
}

KB_GROUP_ORDER = {
    "FOQ测试知识": 10,
    "方法脚本知识": 20,
    "CMBX读取": 30,
    "CMBX生成": 40,
    "报告与公式": 50,
    "Skills": 60,
    "未分类": 999,
}


def resolve_kb_index_path(preferred: str | Path | None = None) -> Path:
    candidates: list[Path] = []
    if preferred:
        candidates.append(Path(preferred))
    candidates.extend((DEFAULT_WORKSPACE_KB_INDEX, DEFAULT_PROJECT_KB_INDEX))
    for candidate in candidates:
        if candidate.exists() and candidate.is_file():
            return candidate
    return DEFAULT_PROJECT_KB_INDEX


def read_kb_index_text(preferred: str | Path | None = None) -> str:
    path = resolve_kb_index_path(preferred)
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def parse_kb_index_entries(markdown: str) -> tuple[KbIndexEntry, ...]:
    entries: list[KbIndexEntry] = []
    in_versions_table = False
    header_seen = False

    for raw_line in markdown.splitlines():
        line = raw_line.strip()
        if line.startswith("| KB Name |"):
            in_versions_table = True
            header_seen = True
            continue
        if not in_versions_table:
            continue
        if not line.startswith("|"):
            if header_seen:
                break
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if not cells or all(set(cell) <= {"-", ":"} for cell in cells):
            continue
        if len(cells) < 6:
            continue
        kb_name, version, update_date, coverage, status, local_files = cells[:6]
        entries.append(
            KbIndexEntry(
                kb_name=_clean_markdown_cell(kb_name),
                version=_clean_markdown_cell(version),
                update_date=_clean_markdown_cell(update_date),
                coverage=_clean_markdown_cell(coverage),
                status=_clean_markdown_cell(status),
                local_files=tuple(_split_local_files(local_files)),
            )
        )

    return tuple(entries)


def discover_kb_index_entries(
    index_path: str | Path | None = None,
    existing_entries: Iterable[KbIndexEntry] = (),
) -> tuple[KbIndexEntry, ...]:
    path = resolve_kb_index_path(index_path)
    kb_root = path.parent if path.exists() and path.is_file() else DEFAULT_WORKSPACE_KB_INDEX.parent
    if not kb_root.exists() or not kb_root.is_dir():
        return ()

    referenced_names: set[str] = set()
    referenced_relatives: set[str] = set()
    for entry in existing_entries:
        for resolved in resolve_kb_entry_files(entry, index_path=path):
            if not resolved.path:
                continue
            referenced_names.add(resolved.path.name.lower())
            try:
                referenced_relatives.add(resolved.path.relative_to(kb_root).as_posix().lower())
            except ValueError:
                referenced_relatives.add(resolved.path.name.lower())

    discovered: list[KbIndexEntry] = []
    for md_path in sorted(kb_root.rglob("*.md")):
        if md_path.name.lower() == "kb_index.md":
            continue
        rel = md_path.relative_to(kb_root).as_posix()
        if rel.lower() in referenced_relatives or md_path.name.lower() in referenced_names:
            continue
        category = _category_from_path(rel)
        display_name = _display_name_from_path(rel)
        discovered.append(
            KbIndexEntry(
                kb_name=display_name,
                version="-",
                update_date="-",
                coverage=category,
                status="Discovered",
                local_files=(rel,),
            )
        )
    return tuple(discovered)


def kb_index_entry_detail(entry: KbIndexEntry) -> str:
    lines = [
        f"KB Name: {entry.kb_name}",
        f"Category: {kb_index_entry_category(entry)}",
        f"Version: {entry.version}",
        f"Update Date: {entry.update_date}",
        f"Coverage: {entry.coverage}",
        f"Status: {entry.status}",
        "",
        "Local File(s):",
    ]
    if entry.local_files:
        lines.extend(f"- {path}" for path in entry.local_files)
    else:
        lines.append("- not listed")
    return "\n".join(lines)


def kb_index_entry_category(entry: KbIndexEntry) -> str:
    name = entry.kb_name.lower()
    if entry.coverage in KB_CATEGORY_ORDER:
        return entry.coverage
    text = " ".join((entry.kb_name, entry.coverage, " ".join(entry.local_files))).lower()
    if "skill" in name or ".codex\\skills" in text or ".codex/skills" in text:
        return "Skills / 工作流"
    if any(token in text for token in ("standalone method cmbx packaging", "method cmbx packaging", "package review spec", "cmbx method package")):
        return "CMBX生成 / 打包与导出"
    if any(token in text for token in ("method script md", "compiler rules", "method script generator", "method authoring", "method script", "md compiler")):
        return "方法脚本知识 / MD格式与渲染"
    if "rendering contract" in text or "method rendering" in text:
        return "方法脚本知识 / MD格式与渲染"
    if any(token in text for token in ("method role", "role-level", "script description", "script analysis", "method command contract")):
        return "方法脚本知识 / Method Role"
    if "parsing" in text or "cmbx_parsing" in text:
        return "CMBX读取 / 解析与提取"
    if name.startswith("tcc_") or name.startswith("foq_tcc"):
        return "FOQ 测试知识 / TCC"
    if "formula" in name:
        return "报告与公式 / Formula与DB"
    if "report" in name:
        return "报告与公式 / Report Template"
    if "generation" in name or "strategy" in name:
        return "CMBX生成 / 生成策略"
    if "method" in name:
        return "CMBX读取 / 方法与报告证据"
    if "tcc" in text or "vtcc" in text or "c10" in text:
        return "FOQ 测试知识 / TCC"
    if any(token in text for token in ("vdad", "vmwd", "vvwd", "detector", "dad", "vwd")):
        return "FOQ 测试知识 / Detector"
    if "pump" in text or "vpump" in text:
        return "FOQ 测试知识 / Pump"
    if "autosampler" in text or "vas" in text:
        return "FOQ 测试知识 / Autosampler"
    if "command" in text or "instrument command" in text:
        return "方法脚本知识 / CM命令"
    if "formula" in text or "db mapping" in text or "db contract" in text:
        return "报告与公式 / Formula与DB"
    if "report" in text:
        return "报告与公式 / Report Template"
    if "generation" in text or "strategy" in text:
        return "CMBX生成 / 生成策略"
    if "package" in text or "export" in text:
        return "CMBX生成 / 打包与导出"
    if "parsing" in text or "decode" in text or "extract" in text:
        return "CMBX读取 / 解析与提取"
    if "method" in text:
        return "CMBX读取 / 方法与报告证据"
    return "未分类 / General"


def kb_index_entry_group(entry_or_category: KbIndexEntry | str) -> str:
    category = kb_index_entry_category(entry_or_category) if isinstance(entry_or_category, KbIndexEntry) else entry_or_category
    if category.startswith("FOQ 测试知识"):
        return "FOQ测试知识"
    if category.startswith("方法脚本知识"):
        return "方法脚本知识"
    if category.startswith("CMBX读取"):
        return "CMBX读取"
    if category.startswith("CMBX生成"):
        return "CMBX生成"
    if category.startswith("报告与公式"):
        return "报告与公式"
    if category.startswith("Skills"):
        return "Skills"
    return "未分类"


def kb_index_group_options(entries: Iterable[KbIndexEntry]) -> tuple[str, ...]:
    return tuple(
        sorted(
            {kb_index_entry_group(entry) for entry in entries},
            key=lambda group: (KB_GROUP_ORDER.get(group, 999), group),
        )
    )


def kb_index_category_options(entries: Iterable[KbIndexEntry]) -> tuple[str, ...]:
    return tuple(
        sorted(
            {kb_index_entry_category(entry) for entry in entries},
            key=lambda category: (KB_CATEGORY_ORDER.get(category, 999), category),
        )
    )


def filter_kb_index_entries(
    entries: Iterable[KbIndexEntry],
    category: str = "All",
    search_text: str = "",
) -> tuple[KbIndexEntry, ...]:
    category = (category or "All").strip()
    search = search_text.strip().lower()
    result: list[KbIndexEntry] = []
    for entry in entries:
        if category != "All" and kb_index_entry_category(entry) != category:
            continue
        haystack = " ".join(
            (
                entry.kb_name,
                entry.version,
                entry.update_date,
                entry.coverage,
                entry.status,
                " ".join(entry.local_files),
            )
        ).lower()
        if search and search not in haystack:
            continue
        result.append(entry)
    return tuple(result)


def kb_index_entries_for_scope(entries: Iterable[KbIndexEntry], scope: str = "All") -> tuple[KbIndexEntry, ...]:
    scope = (scope or "All").strip()
    all_entries = tuple(entries)
    if scope == "All":
        return all_entries
    if scope.startswith("group:"):
        group = scope.partition(":")[2]
        return tuple(entry for entry in all_entries if kb_index_entry_group(entry) == group)
    if scope.startswith("category:"):
        category = scope.partition(":")[2]
        return tuple(entry for entry in all_entries if kb_index_entry_category(entry) == category)
    return tuple(entry for entry in all_entries if kb_index_entry_category(entry) == scope)


def kb_index_scope_label(scope: str) -> str:
    scope = (scope or "All").strip()
    if scope == "All":
        return "All Knowledge Bases"
    if scope.startswith("group:"):
        return f"{scope.partition(':')[2]} Knowledge Bases"
    if scope.startswith("category:"):
        return scope.partition(":")[2]
    return scope


def resolve_kb_entry_files(entry: KbIndexEntry, index_path: str | Path | None = None) -> tuple[KbIndexResolvedFile, ...]:
    base_paths = _kb_resolution_base_paths(index_path)
    resolved: list[KbIndexResolvedFile] = []
    for local_file in entry.local_files:
        label = local_file.strip()
        if not label:
            continue
        if any(marker in label for marker in ("*", "?")):
            matches = _resolve_pattern(label, base_paths)
            if matches:
                resolved.extend(
                    KbIndexResolvedFile(label=f"{label} -> {match}", path=match, exists=True, is_pattern=True)
                    for match in matches
                )
            else:
                resolved.append(KbIndexResolvedFile(label=label, path=None, exists=False, is_pattern=True, note="pattern did not match any local file"))
            continue
        path = _resolve_one_file(label, base_paths)
        resolved.append(KbIndexResolvedFile(label=label, path=path, exists=path is not None))
    return tuple(resolved)


def kb_index_entry_full_markdown(entry: KbIndexEntry, index_path: str | Path | None = None, max_pattern_files: int = 12) -> str:
    lines = [
        f"# {entry.kb_name}",
        "",
        kb_index_entry_detail(entry),
        "",
        "## Rendered Local File Content",
    ]
    resolved_files = resolve_kb_entry_files(entry, index_path=index_path)
    if not resolved_files:
        lines.append("No local files listed in KB index.")
        return "\n".join(lines)

    rendered_count = 0
    pattern_count = 0
    for resolved in resolved_files:
        if resolved.is_pattern:
            pattern_count += 1
            if pattern_count > max_pattern_files:
                continue
        lines.extend(("", f"---", "", f"## {resolved.label}"))
        if not resolved.exists or not resolved.path:
            lines.append(f"Missing local file. {resolved.note}".strip())
            continue
        if resolved.path.is_dir():
            lines.append(f"Directory: {resolved.path}")
            continue
        try:
            content = resolved.path.read_text(encoding="utf-8", errors="replace")
        except Exception as exc:
            lines.append(f"Failed to read file: {resolved.path}\n{exc}")
            continue
        rendered_count += 1
        lines.extend(("", f"Source: `{resolved.path}`", "", content))
    if pattern_count > max_pattern_files:
        lines.extend(("", f"Pattern expansion truncated after {max_pattern_files} files."))
    if rendered_count == 0:
        lines.extend(("", "No readable local Markdown/text files were resolved for this KB row."))
    return "\n".join(lines)


def kb_index_category_full_markdown(
    entries: Iterable[KbIndexEntry],
    category: str,
    index_path: str | Path | None = None,
    max_pattern_files_per_entry: int = 12,
) -> str:
    all_entries = tuple(entries)
    if category == "All":
        selected = all_entries
        title = "All Knowledge Bases"
    else:
        selected = tuple(entry for entry in all_entries if kb_index_entry_category(entry) == category)
        title = category
    lines = [
        f"# {title}",
        "",
        f"KB count: {len(selected)}",
    ]
    if not selected:
        lines.append("")
        lines.append("No KB entries are listed in this category.")
        return "\n".join(lines)

    lines.extend(
        (
            "",
            "## Entries",
            "",
            "| KB | Version | Update Date | Status | Coverage |",
            "|---|---:|---|---|---|",
        )
    )
    for entry in selected:
        lines.append(
            f"| {entry.kb_name} | {entry.version} | {entry.update_date} | {entry.status} | {entry.coverage} |"
        )
    for entry in selected:
        lines.extend(
            (
                "",
                "---",
                "",
                kb_index_entry_full_markdown(
                    entry,
                    index_path=index_path,
                    max_pattern_files=max_pattern_files_per_entry,
                ),
            )
        )
    return "\n".join(lines)


def kb_index_scope_full_markdown(
    entries: Iterable[KbIndexEntry],
    scope: str,
    index_path: str | Path | None = None,
    max_pattern_files_per_entry: int = 12,
) -> str:
    selected = kb_index_entries_for_scope(entries, scope)
    title = kb_index_scope_label(scope)
    lines = [
        f"# {title}",
        "",
        f"KB count: {len(selected)}",
    ]
    if not selected:
        lines.extend(("", "No KB entries are listed in this scope."))
        return "\n".join(lines)

    lines.extend(
        (
            "",
            "## Entries",
            "",
            "| Group | Category | KB | Version | Update Date | Status | Coverage |",
            "|---|---|---|---:|---|---|---|",
        )
    )
    for entry in selected:
        lines.append(
            f"| {kb_index_entry_group(entry)} | {kb_index_entry_category(entry)} | {entry.kb_name} | {entry.version} | {entry.update_date} | {entry.status} | {entry.coverage} |"
        )
    for entry in selected:
        lines.extend(
            (
                "",
                "---",
                "",
                kb_index_entry_full_markdown(
                    entry,
                    index_path=index_path,
                    max_pattern_files=max_pattern_files_per_entry,
                ),
            )
        )
    return "\n".join(lines)


def kb_index_overview_markdown(entries: Iterable[KbIndexEntry]) -> str:
    all_entries = tuple(entries)
    by_category: dict[str, list[KbIndexEntry]] = {}
    for entry in all_entries:
        by_category.setdefault(kb_index_entry_category(entry), []).append(entry)
    lines = [
        "# KB Index Overview",
        "",
        f"Total KB entries: {len(all_entries)}",
        "",
        "## Categories",
        "",
        "| Group | Category | KB Count | Published | In Development / Draft |",
        "|---|---|---:|---:|---:|",
    ]
    for category in kb_index_category_options(all_entries):
        rows = by_category.get(category, [])
        published = sum(1 for row in rows if "publish" in row.status.lower() or "已发布" in row.status)
        in_progress = len(rows) - published
        lines.append(f"| {kb_index_entry_group(category)} | {category} | {len(rows)} | {published} | {in_progress} |")
    return "\n".join(lines)


def _clean_markdown_cell(value: str) -> str:
    value = value.replace("**", "").strip()
    if value.startswith("`") and value.endswith("`") and len(value) >= 2:
        value = value[1:-1]
    return value.strip()


def _split_local_files(value: str) -> list[str]:
    files: list[str] = []
    for part in value.split(","):
        clean = _clean_markdown_cell(part.strip())
        if clean:
            files.append(clean)
    return files


def _kb_resolution_base_paths(index_path: str | Path | None) -> tuple[Path, ...]:
    bases: list[Path] = []
    if index_path:
        path = Path(index_path)
        if path.exists():
            bases.append(path.parent if path.is_file() else path)
    bases.extend(
        (
            DEFAULT_WORKSPACE_KB_INDEX.parent,
            PROJECT_ROOT,
            PROJECT_ROOT / "cmbx_data_explorer" / "docs",
        )
    )
    unique: list[Path] = []
    seen: set[str] = set()
    for base in bases:
        key = str(base)
        if key in seen:
            continue
        seen.add(key)
        unique.append(base)
    return tuple(unique)


def _resolve_one_file(label: str, base_paths: Iterable[Path]) -> Path | None:
    raw = Path(label)
    candidates = [raw] if raw.is_absolute() else []
    for base in base_paths:
        candidates.append(base / label)
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def _resolve_pattern(label: str, base_paths: Iterable[Path]) -> tuple[Path, ...]:
    matches: list[Path] = []
    raw = Path(label)
    if raw.is_absolute():
        parent = raw.parent
        if parent.exists():
            matches.extend(parent.glob(raw.name))
    else:
        for base in base_paths:
            matches.extend(base.glob(label))
    unique: list[Path] = []
    seen: set[str] = set()
    for match in matches:
        key = str(match)
        if key in seen:
            continue
        seen.add(key)
        unique.append(match)
    return tuple(unique)


def _category_from_path(relative_path: str) -> str:
    text = relative_path.replace("\\", "/").lower()
    if text.startswith("foq/tcc/"):
        return "FOQ 测试知识 / TCC"
    if text.startswith("foq/detector/"):
        return "FOQ 测试知识 / Detector"
    if text.startswith("foq/pump/"):
        return "FOQ 测试知识 / Pump"
    if text.startswith("foq/autosampler/"):
        return "FOQ 测试知识 / Autosampler"
    if text.startswith("cm/instrument commands/"):
        return "方法脚本知识 / CM命令"
    if text.startswith("foq template/") or "method script generator/" in text:
        return "方法脚本知识 / MD格式与渲染"
    if "standalone" in text or "packaging" in text or "package" in text:
        return "CMBX生成 / 打包与导出"
    if "parsing" in text or "decode" in text or "extract" in text:
        return "CMBX读取 / 解析与提取"
    if "role" in text or "script description" in text:
        return "方法脚本知识 / Method Role"
    if "method" in text:
        return "CMBX读取 / 方法与报告证据"
    if "report" in text:
        return "报告与公式 / Report Template"
    if "formula" in text:
        return "报告与公式 / Formula与DB"
    if "generation" in text or "strategy" in text:
        return "CMBX生成 / 生成策略"
    return "未分类 / General"


def _display_name_from_path(relative_path: str) -> str:
    path = Path(relative_path)
    stem = path.stem
    parts = [part for part in path.parts[:-1] if part.lower() not in {"foq", "cm"}]
    prefix = " / ".join(parts)
    return f"{prefix} / {stem}" if prefix else stem
