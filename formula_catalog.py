from __future__ import annotations

import re
import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class FormulaCatalogEntry:
    name: str
    formula: str
    engine: str
    category: str
    summary: str
    support: str
    source: str

    @property
    def searchable_text(self) -> str:
        return " ".join((self.name, self.formula, self.engine, self.category, self.summary, self.support, self.source)).casefold()


_NAMESPACE_BY_CATEGORY = {
    "Peak": "peak",
    "Component": "component",
    "ProcessingMethod": "procMeth",
    "Sequence": "seq",
    "Chromatogram": "chm",
    "Injection": "injection",
    "General": "gen",
    "InstrumentMethod": "instMeth",
    "ReportTemplate": "rdf",
    "Table": "table",
    "SSTResults": "sstResult",
    "Fraction": "frac",
    "FractionTube": "tube",
    "Precondition": "precond",
    "AuditTrail": "audit",
    "AuditTrailEvent": "audit_event",
}
_EXTERNAL_PREFIXES = (
    "chm.sig_value(",
    "chm.signalstatistic(",
    "chm.signalvalue(",
    "chm.noise(",
    "chm.drift(",
)


def build_formula_catalog(docs_root: str | Path) -> tuple[FormulaCatalogEntry, ...]:
    root = Path(docs_root)
    help_path = root / "CM_REPORT_FORMULA_HELP_CATALOG.md"
    reference_path = root / "CM_REPORT_FORMULA_LANGUAGE_REFERENCE.md"
    entries: list[FormulaCatalogEntry] = []
    if help_path.exists():
        entries.extend(_help_entries(help_path))
    evidence_paths = list(root.rglob("*.md"))
    app_root = root.parent
    for evidence_root in (app_root / "outputs" / "report_template_probe", app_root / "outputs" / "formulaone_control_pair"):
        if evidence_root.exists():
            evidence_paths.extend(evidence_root.rglob("*.md"))
    workspace = Path(os.environ.get("CMBX_DATA_EXPLORER_WORKSPACE", "") or Path(os.environ.get("PROGRAMDATA", r"C:\ProgramData")) / "CMBX Data Explorer Workspace")
    program_evidence = (
        workspace / "KB" / "Method Script Generator" / "TCC" / "report_template_cmbx",
        workspace / "KB" / "KB_Online_GPT" / "02_Full_Context" / "Report",
    )
    for evidence_root in program_evidence:
        if evidence_root.exists():
            evidence_paths.extend(path for path in evidence_root.rglob("*.md") if "FORMULA" in path.name.upper() or path.name == "02_REPORT_ORIGINAL_TEMPLATES.md")
    for evidence_path in evidence_paths:
        entries.extend(_observed_entries(evidence_path))
    unique: dict[tuple[str, str, str], FormulaCatalogEntry] = {}
    for entry in entries:
        key = (entry.engine, entry.formula.casefold(), entry.name.casefold())
        existing = unique.get(key)
        if existing is None or _evidence_rank(entry) > _evidence_rank(existing):
            unique[key] = entry
    return tuple(sorted(unique.values(), key=lambda item: (item.engine, item.category, item.name.casefold())))


def filter_formula_catalog(
    entries: tuple[FormulaCatalogEntry, ...],
    query: str = "",
    engine: str = "All",
    external_only: bool = False,
) -> tuple[FormulaCatalogEntry, ...]:
    words = [word.casefold() for word in query.split() if word.strip()]
    return tuple(
        entry
        for entry in entries
        if (engine == "All" or entry.engine == engine)
        and (not external_only or entry.support == "External V1")
        and all(word in entry.searchable_text for word in words)
    )


def useful_direct_formula_catalog(
    entries: tuple[FormulaCatalogEntry, ...],
) -> tuple[FormulaCatalogEntry, ...]:
    """Return concrete, locally evaluable Direct CM formulas from observed evidence."""
    rejected_tokens = ("...", "RetTimeN", "(time", "<", ">", "REPLACE_WITH", "AUDIT.path")
    selected: dict[str, FormulaCatalogEntry] = {}
    for entry in entries:
        formula = entry.formula.strip()
        if (
            entry.engine != "CM Report"
            or entry.support != "External V1"
            or not formula
            or any(token.casefold() in formula.casefold() for token in rejected_tokens)
            or re.search(r"(?:^|\.)[A-Za-z0-9]*_$", formula.split("(", 1)[0])
            or re.search(r"(?:^|[,+(\-])\s*(?:start|end|time|path)\s*(?=[,)+\-])", formula, flags=re.I)
        ):
            continue
        selected.setdefault(formula.casefold(), entry)
    return tuple(sorted(selected.values(), key=lambda item: (item.category.casefold(), item.name.casefold(), item.formula.casefold())))


def _evidence_rank(entry: FormulaCatalogEntry) -> tuple[int, int]:
    source = entry.source.upper()
    if "FORMULA_INVENTORY" in source or "ORIGINAL_TEMPLATES" in source:
        source_rank = 3
    elif entry.support == "Help index":
        source_rank = 0
    else:
        source_rank = 2
    support_rank = {"External V1": 3, "Observed CM": 2, "Help index": 1}.get(entry.support, 0)
    return source_rank, support_rank


def unified_md_block(entry: FormulaCatalogEntry) -> str:
    if entry.engine == "FormulaOne":
        formula = entry.formula if entry.formula.startswith("=") else f"={entry.formula}"
        return (
            "\n### Workbook Formula: C2\n"
            "```yaml\noperation: create\nvalue_type: formula\n"
            f"formula: '{formula}'\nstyle: result\n```\n"
        )
    if not entry.formula:
        raise ValueError("This Help topic is conceptual and has no exact insertable formula syntax.")
    return (
        "\n### CM Formula: B2\n"
        "```yaml\noperation: create\nobject_type: ReportFormulaObject\n"
        f"formula: {entry.formula}\nfixed_channel: ''\nfixed_component: ''\nstyle: result\n```\n"
    )


def external_scalar_block(entry: FormulaCatalogEntry) -> str:
    if entry.support != "External V1":
        raise ValueError("The selected formula is not implemented by External Report Engine V1.")
    identifier = re.sub(r"[^A-Za-z0-9_]+", "", entry.name.title().replace(" ", "")) or "NewScalar"
    channel_line = "channel: REPLACE_WITH_CHANNEL\n" if entry.formula.casefold().startswith("chm.") else ""
    return (
        f"\n### Scalar: {identifier}\n"
        "```yaml\n"
        f"label: {entry.name}\n{channel_line}formula: {entry.formula}\nnumber_format: 0.000\n```\n"
    )


def _help_entries(path: Path) -> list[FormulaCatalogEntry]:
    text = path.read_text(encoding="utf-8-sig")
    entries: list[FormulaCatalogEntry] = []
    direct = False
    category = "FormulaOne"
    for line in text.splitlines():
        if line.startswith("## Direct CM Report Variable Topics"):
            direct = True
            continue
        if direct and line.startswith("### "):
            category = line[4:].strip()
            continue
        if not line.startswith("|") or line.startswith("|---"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 3 or cells[0] in {"Function", "Variable / topic"}:
            continue
        name = cells[0].strip("`")
        summary = cells[1]
        topic = cells[2].strip("`")
        if not direct:
            if not re.fullmatch(r"[A-Z][A-Z0-9.]*", name):
                continue
            entries.append(FormulaCatalogEntry(name, f"{name}(...)", "FormulaOne", "Workbook", summary, "Help index", topic))
            continue
        entries.append(FormulaCatalogEntry(name, "", "CM Report", category, summary, "Help index", topic))
    return entries


def _observed_entries(path: Path) -> list[FormulaCatalogEntry]:
    text = path.read_text(encoding="utf-8-sig")
    entries: list[FormulaCatalogEntry] = []
    for start, end, formula in _extract_cm_formulas(text):
        line_start = text.rfind("\n", 0, start) + 1
        line_end = text.find("\n", end)
        context = text[line_start : line_end if line_end >= 0 else len(text)].strip(" |-`")
        prefix = formula.split(".", 1)[0]
        support = "External V1" if _external_formula_supported(formula) else "Observed CM"
        entries.append(FormulaCatalogEntry(formula.split("(", 1)[0], formula, "CM Report", prefix, context, support, path.name))
    return entries


def _extract_cm_formulas(text: str) -> list[tuple[int, int, str]]:
    start_pattern = re.compile(
        r"(?<![A-Za-z0-9_])(?:AUDIT|audit|precond|chm|peak|component|procMeth|seq|injection|smp|gen|instMeth|rdf)\."
        r"[A-Za-z_][A-Za-z0-9_.]*"
    )
    formulas: list[tuple[int, int, str]] = []
    for match in start_pattern.finditer(text):
        end = match.end()
        if end >= len(text) or text[end] != "(":
            formula = match.group().rstrip(".")
            formulas.append((match.start(), match.start() + len(formula), formula))
            continue
        depth = 0
        quote = ""
        escaped = False
        index = end
        while index < len(text):
            char = text[index]
            if escaped:
                escaped = False
            elif char == "\\" and quote:
                escaped = True
            elif quote:
                if char == quote:
                    quote = ""
            elif char in {'"', "'"}:
                quote = char
            elif char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
                if depth == 0:
                    index += 1
                    break
            elif char in "\r\n`|" and depth > 0:
                break
            index += 1
        formula = text[match.start() : index].strip().rstrip(".,;:")
        if depth == 0 and formula.endswith(")"):
            formulas.append((match.start(), index, formula))
    return formulas


def _external_formula_supported(formula: str) -> bool:
    lowered = formula.casefold()
    if re.fullmatch(r"(?:precond|audit)\.[A-Za-z0-9_.]+", formula, flags=re.I):
        return True
    if re.fullmatch(r"(?:seq\.(?:name|update_time|timebase)|injection\.name|smp\.name)", formula, flags=re.I):
        return True
    if re.fullmatch(r"AUDIT\.RetTime\d+\((?:1(?:\.0+)?\s*,\s*)?[\"']forward[\"']\s*\)", formula, flags=re.I):
        return True
    if re.fullmatch(r"AUDIT\.[A-Za-z0-9_.]+\(.+\)", formula, flags=re.I) and "..." not in formula:
        return True
    if not (lowered.startswith(_EXTERNAL_PREFIXES) and formula.endswith(")") and "..." not in formula):
        return False
    if lowered.startswith(("chm.sig_value(", "chm.signalstatistic(")):
        match = re.match(r"chm\.(?:sig_value|signalstatistic)\(\s*[\"']([^\"']+)", formula, flags=re.I)
        return bool(match and match.group(1).casefold() in {"average", "avg", "min", "max", "drift", "stddev", "stdev"})
    return True
