from __future__ import annotations

"""Create a compact, source-backed Markdown index from CM7 report Formula Help.

The output is intended for a web authoring project: it collects every official
``ReportVariables_CSH/RepVar_*.htm`` and ``FormulaFunctions/IDH_*.htm`` topic
without requiring that project to access the local Help installation.
"""

import argparse
from collections import defaultdict
from html import unescape
from pathlib import Path
import re


DEFAULT_HELP_ROOT = Path(
    r"C:\ProgramData\CMBX Data Explorer Workspace\KB\Method Script Generator\TCC\report_template_cmbx\CM7Help_EN"
)


def build_catalog(help_root: Path) -> str:
    formula_dir = help_root / "FormulaFunctions"
    variable_dir = help_root / "ReportVariables_CSH"
    formula_topics = [_topic(path, help_root) for path in sorted(formula_dir.glob("IDH_*.htm"))]
    variable_topics = [_topic(path, help_root) for path in sorted(variable_dir.glob("RepVar_*.htm"))]
    grouped: dict[str, list[Topic]] = defaultdict(list)
    for topic in variable_topics:
        grouped[_report_variable_group(Path(topic.path).name)].append(topic)

    lines = [
        "# CM Report Formula Help Catalog",
        "",
        "**Source:** Chromeleon 7 Help, `FormulaFunctions` and `ReportVariables_CSH`  ",
        f"**Help root used:** `{help_root}`  ",
        f"**Coverage:** {len(formula_topics)} FormulaOne function topics; {len(variable_topics)} report-variable topics.",
        "",
        "## Purpose and Boundary",
        "",
        "This catalog is an official-Help index for web authoring. It is not evidence that every topic is available in every instrument configuration or that CMBX Data Explorer evaluates every formula locally. Use an observed carrier formula and configuration evidence before declaring a generated CM report formula runnable.",
        "",
        "FormulaOne functions are workbook-layer functions. CM report variables are direct `ReportFormulaObject` / report-table sources; do not mix the two engines.",
        "",
        "## FormulaOne Function Topics",
        "",
        "These function names come from the FormulaOne Help collection. The V1 report compiler can persist a formula in a newly declared cell, but only functions marked verified by a control matrix have end-to-end evidence in this project.",
        "",
        "| Function | Help summary | Help topic |",
        "|---|---|---|",
    ]
    for topic in formula_topics:
        lines.append(f"| `{topic.title}` | {topic.summary} | `{topic.path}` |")

    lines.extend(["", "## Direct CM Report Variable Topics", ""])
    for group in sorted(grouped, key=lambda item: (-len(grouped[item]), item.lower())):
        topics = grouped[group]
        lines.extend([f"### {group}", "", f"**Official Help topics:** {len(topics)}", "", "| Variable / topic | Help summary | Help topic |", "|---|---|---|"])
        for topic in topics:
            lines.append(f"| {topic.title} | {topic.summary} | `{topic.path}` |")
        lines.append("")

    lines.extend(
        [
            "## Authoring Rule",
            "",
            "1. Select the formula engine first: direct CM report formula or FormulaOne workbook formula.",
            "2. For direct CM formulas, select an observed device path/channel/component from the carrier or configuration KB.",
            "3. For FormulaOne, use a documented function in a declared workbook cell; V1 can create the containing sheet and static grid.",
            "4. If the carrier/configuration does not prove the variable path or function behaviour, mark `OPEN VERIFICATION REQUIRED`.",
            "",
        ]
    )
    return "\n".join(lines)


class Topic:
    def __init__(self, title: str, summary: str, path: str) -> None:
        self.title = _escape_cell(title)
        self.summary = _escape_cell(summary)
        self.path = path.replace("\\", "/")


def _topic(path: Path, root: Path) -> Topic:
    text = path.read_text(encoding="cp1252", errors="replace")
    title_match = re.search(r"<title>(.*?)</title>", text, re.I | re.S)
    h1_match = re.search(r"<h1[^>]*>(.*?)</h1>", text, re.I | re.S)
    title = _clean_html(h1_match.group(1) if h1_match else title_match.group(1) if title_match else path.stem)
    paragraphs = [_clean_html(value) for value in re.findall(r"<p[^>]*>(.*?)</p>", text, re.I | re.S)]
    summary = next((value for value in paragraphs if len(value) > 25 and "access this" not in value.lower()), "Official Help topic.")
    return Topic(title, summary[:360], str(path.relative_to(root)))


def _report_variable_group(filename: str) -> str:
    stem = Path(filename).stem.removeprefix("RepVar_")
    return stem.split("_", 1)[0].replace("MS", "MS ")


def _clean_html(value: str) -> str:
    value = re.sub(r"<script.*?</script>|<style.*?</style>", " ", value, flags=re.I | re.S)
    value = re.sub(r"<[^>]+>", " ", value)
    value = unescape(value).replace("\xa0", " ")
    return re.sub(r"\s+", " ", value).strip()


def _escape_cell(value: str) -> str:
    return value.replace("|", "\\|")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a Markdown catalog from CM7 report formula Help.")
    parser.add_argument("--help-root", type=Path, default=DEFAULT_HELP_ROOT)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not args.help_root.is_dir():
        raise SystemExit(f"Help root was not found: {args.help_root}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(build_catalog(args.help_root), encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
