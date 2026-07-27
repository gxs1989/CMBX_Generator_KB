from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from datetime import date
import hashlib
from pathlib import Path
import re
import shutil


DEFAULT_KB_ROOT = Path(r"C:\ProgramData\CMBX Data Explorer Workspace\KB")


@dataclass(frozen=True)
class ScriptSource:
    path: Path
    method: str
    device: str
    sequence: str
    digest: str
    rows: tuple[dict[str, str], ...]


METHOD_ID = {
    "BURNIN": "BURNIN",
    "CHECKERRORLOG": "ERRORLOG",
    "ColumnID": "COLUMN-ID",
    "FACTORYDEFAULT": "FACTORY",
    "LIQUID LEAK": "LEAK",
    "PREHEATER": "PREHEATER",
    "QUALIFICATION_SERVICE_DONE": "SERVICE",
    "TEMP_HEAT_UP_DOWN_20_50_20": "HEAT-COOL",
    "TEMPERATURE_ACCURACY": "ACCURACY",
    "TEMPERATURE_CALIBRATION": "CALIBRATION",
    "TEMPERATURE_PRECISION": "PRECISION",
    "TEMPERATURE_PRECISION_AND_FAN": "PRECISION-FAN",
    "TEMPERATURE_STABILITY_70_C": "STABILITY",
    "TEMPERATURE_STABILITY_AND_PCC_70_H": "STABILITY-PCC",
    "VALVES": "VALVES",
}


SUMMARY_SOURCES = [
    ("K001", "FOQ test logic", Path("FOQ/TCC/FOQ_TD_TEST_LOGIC_KNOWLEDGE_BASE.md"), "tcc-test-logic"),
    ("K002", "Method role contracts", Path("FOQ/TCC/TCC_METHOD_ROLE_CONTRACTS.md"), "tcc-method-roles"),
    ("K003", "Test relationship model", Path("FOQ/TCC/TCC_TEST_RELATIONSHIP_MODEL.md"), "tcc-relationships"),
    ("K004", "TCC stress Trigger method contract", Path("Method Script Generator/TCC/TCC_STRESS_TRIGGER_METHOD_CONTRACT.md"), "tcc-stress-trigger-contract"),
    ("B001", "Column ID black box", Path("FOQ/TCC/TCC_COLUMN_ID_BLACK_BOX_DECOMPOSITION.md"), "tcc-column-id"),
    ("B002", "Preheater black box", Path("FOQ/TCC/TCC_PREHEATER_BLACK_BOX_DECOMPOSITION.md"), "tcc-preheater"),
    ("B003", "Valve/keypad black box", Path("FOQ/TCC/TCC_VALVE_KEYPAD_BLACK_BOX_DECOMPOSITION.md"), "tcc-valves"),
    ("B004", "Burn-in black box", Path("FOQ/TCC/TCC_BURNIN_BLACK_BOX_DECOMPOSITION.md"), "tcc-burnin"),
    ("B005", "Calibration black box", Path("FOQ/TCC/TCC_CALIBRATION_BLACK_BOX_DECOMPOSITION.md"), "tcc-calibration"),
    ("B006", "Accuracy black box", Path("FOQ/TCC/TCC_ACCURACY_BLACK_BOX_DECOMPOSITION.md"), "tcc-accuracy"),
    ("B007", "Precision/fan black box", Path("FOQ/TCC/TCC_PRECISION_FAN_BLACK_BOX_DECOMPOSITION.md"), "tcc-precision"),
    ("B008", "Stability/PCC black box", Path("FOQ/TCC/TCC_STABILITY_BLACK_BOX_DECOMPOSITION.md"), "tcc-stability"),
    ("B009", "Heat-up/cool-down black box", Path("FOQ/TCC/TCC_HEATUP_COOLDOWN_BLACK_BOX_DECOMPOSITION.md"), "tcc-heat-cool"),
    ("B010", "Liquid leak black box", Path("FOQ/TCC/TCC_LIQUID_LEAK_BLACK_BOX_DECOMPOSITION.md"), "tcc-leak"),
    ("B011", "Qualification service black box", Path("FOQ/TCC/TCC_QUALIFICATION_SERVICE_BLACK_BOX_DECOMPOSITION.md"), "tcc-service"),
    ("B012", "Factory default black box", Path("FOQ/TCC/TCC_FACTORY_DEFAULT_BLACK_BOX_DECOMPOSITION.md"), "tcc-factory"),
    ("B013", "Error log black box", Path("FOQ/TCC/TCC_ERROR_LOG_BLACK_BOX_DECOMPOSITION.md"), "tcc-error-log"),
]


SCRIPT_DESCRIPTION_NAMES = [
    "Heat-Up and Cool-Down Time Test.md",
    "Liquid Leak Sensor Test.md",
    "Temperature Calibration.MD",
    "Temperature Precision and Fan Functionality Test.md",
    "Temperature Stability and PCC Test.md",
    "valve and keyboard.md",
    "Vanquish_TCC_Temperature_Accuracy_Method_Analysis.md",
]


def read_sources(raw_root: Path) -> list[ScriptSource]:
    sources: list[ScriptSource] = []
    for path in sorted(raw_root.rglob("*_embedded_method_flow.tsv")):
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = tuple(csv.DictReader(handle, delimiter="\t"))
        if not rows:
            continue
        method = rows[0].get("Method", "") or path.name.removesuffix("_embedded_method_flow.tsv")
        if "stress_probe" in path.parts:
            device = "VH-STRESS"
        else:
            device = next((part for part in path.parts if part in {"VA", "VC", "VH"}), "Unknown")
        sequence = path.parent.name
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        sources.append(ScriptSource(path, method, device, sequence, digest, rows))
    return sources


def script_groups(sources: list[ScriptSource]) -> list[list[ScriptSource]]:
    groups: dict[tuple[str, str], list[ScriptSource]] = {}
    for source in sources:
        groups.setdefault((source.method, source.digest), []).append(source)
    return sorted(groups.values(), key=lambda group: (group[0].method.casefold(), sorted(item.device for item in group)))


def build_spec(kb_root: Path) -> str:
    sources = [
        ("SPEC", "CM Method Script MD Generation SPEC", kb_root / "Method Script Generator/Generator Spec/CM_METHOD_SCRIPT_MD_FORMAT_SPEC.md"),
        ("COMMAND", "CM Instrument Command Knowledge Base", kb_root / "CM/Instrument Commands/CM_INSTRUMENT_COMMAND_KNOWLEDGE_BASE_V2.md"),
        ("PREFLIGHT", "CM Compiler Rules", kb_root / "Method Script Generator/Generator Spec/CM Compiler Rules.MD"),
    ]
    lines = [
        "# Online Method Script Generation SPEC",
        "",
        "Online_KB_Status: CANDIDATE_FOR_WEB_VALIDATION  ",
        "Upload_Allowed: Validation only  ",
        f"Build_Date: {date.today().isoformat()}  ",
        "Scope: CM instrument-method Markdown authoring for later local preview and CMBX compilation",
        "",
        "## Self Index",
        "",
        "| Priority | Section | Purpose | Anchor |",
        "|---:|---|---|---|",
        "| 1 | Method MD generation contract | Required output syntax and authoring workflow | `#source-spec` |",
        "| 2 | CM command language | Meaning of executable commands and device symbols | `#source-command` |",
        "| 3 | Compiler/preflight rules | Local structural rejection rules | `#source-preflight` |",
        "",
        "## Precedence",
        "",
        "When sections overlap, the current Method MD generation contract controls the output format; compiler rules control whether the output can be packaged; command evidence controls semantic meaning. Never invent a command absent from source evidence.",
    ]
    for source_id, title, path in sources:
        lines.extend([
            "",
            f'<a id="source-{source_id.lower()}"></a>',
            f"## Source {source_id}: {title}",
            "",
            f"Build source name: `{path.name}`",
            "",
            _web_safe(path.read_text(encoding="utf-8")),
        ])
    return "\n".join(lines).rstrip() + "\n"


def build_originals(sources: list[ScriptSource]) -> tuple[str, list[tuple[str, list[ScriptSource]]]]:
    groups = script_groups(sources)
    identified: list[tuple[str, list[ScriptSource]]] = []
    method_counts: dict[str, int] = {}
    for group in groups:
        method_counts[group[0].method] = method_counts.get(group[0].method, 0) + 1

    index_lines: list[str] = []
    sections: list[str] = []
    seen_variant: dict[str, int] = {}
    for group in groups:
        method = group[0].method
        seen_variant[method] = seen_variant.get(method, 0) + 1
        devices = sorted({item.device for item in group})
        device_code = "".join(devices)
        short = METHOD_ID.get(method, _slug(method).upper())
        suffix = f"-{device_code}" if method_counts[method] > 1 else ""
        stable_id = f"M-TCC-{short}{suffix}"
        anchor = stable_id.lower()
        identified.append((stable_id, group))
        sequences = ", ".join(f"{item.device}:{item.sequence}" for item in sorted(group, key=lambda item: item.device))
        rows_count = len(group[0].rows)
        index_lines.append(
            f"| `{stable_id}` | `{method}` | {'/'.join(devices)} | {sequences} | {rows_count} | `{group[0].digest[:12]}` | [Open](#{anchor}) |"
        )
        sections.extend([
            "",
            f'<a id="{anchor}"></a>',
            f"## {stable_id}: {method}",
            "",
            f"Applicable device evidence: **{' / '.join(devices)}**  ",
            f"Source sequence(s): `{sequences}`  ",
            f"Source SHA-256: `{group[0].digest}`  ",
            f"Decoded flow rows: `{rows_count}`",
            "",
            "```tsv",
            "Time\tCommand\tValue\tComment",
            *render_strict_method_rows(group[0].rows),
            "```",
        ])

    header = [
        "# Online Original TCC Method Script Collection",
        "",
        "Online_KB_Status: CANDIDATE_FOR_WEB_VALIDATION  ",
        "Upload_Allowed: Validation only  ",
        f"Build_Date: {date.today().isoformat()}  ",
        f"Decoded sources: {len(sources)} device/method files  ",
        f"Core FOQ sources: {sum(1 for item in sources if item.device != 'VH-STRESS')}  ",
        f"Stress-extension sources: {sum(1 for item in sources if item.device == 'VH-STRESS')}  ",
        f"Unique script bodies: {len(groups)}",
        "",
        "## Evidence Rules",
        "",
        "These sections are regenerated from the golden VA/VC/VH TCC CMBX packages and the VH stress-test package using the current embedded-method decoder. Identical device variants are stored once and list all applicable devices. Sections marked `VH-STRESS` are experimental execution evidence, not an FOQ acceptance contract. This file is source evidence; interpretation belongs in `03_METHOD_SUMMARIES.md`.",
        "",
        "## Self Index",
        "",
        "| Stable ID | CM method | Device evidence | Sequence source | Rows | Hash | Section |",
        "|---|---|---|---|---:|---|---|",
        *index_lines,
    ]
    return "\n".join(header + sections).rstrip() + "\n", identified


def render_strict_method_rows(rows: tuple[dict[str, str], ...]) -> list[str]:
    output: list[str] = []
    last_time = ""
    stage_duration = _derived_stage_durations(rows)
    for position, row in enumerate(rows):
        action = row.get("Action", "")
        level = _int(row.get("Level", ""))
        indent = "    " * level
        row_time = row.get("Time", "")
        target = row.get("Target", "")
        value = row.get("Value", "")
        comment = row.get("Comment", "")
        condition = row.get("Condition", "")
        cells: tuple[str, str, str, str] | None = None
        if action == "STAGE":
            stage_name = value or row.get("Stage", "")
            if stage_name == "InstrumentSetup":
                stage_name = "Instrument Setup"
            duration = comment or stage_duration.get(position, "")
            cells = (row_time, stage_name, duration, "")
            last_time = row_time
        elif action == "COMMENT":
            cells = ("", f"{indent}{comment}", "", "")
        elif action in {"IF", "ELSE IF"}:
            keyword = "If" if action == "IF" else "Else If"
            cells = (f"{indent}{keyword}", "", condition, comment)
        elif action == "ELSE":
            cells = (f"{indent}Else", "", "", comment)
        elif action == "END IF":
            cells = (f"{indent}End If", "", "", comment)
        elif action == "TRIGGER":
            trigger_name, parameters = _trigger_parts(value)
            display_time = row_time if row_time and row_time != last_time else ""
            if display_time:
                output.append(_tsv((display_time, "", "", "")))
                last_time = display_time
            cells = (f"{indent}Trigger", "", f"{trigger_name}," if trigger_name else "", comment)
            output.append(_tsv(cells))
            for key, parameter_value in parameters:
                output.append(_tsv(("", f"{indent}    {key}", parameter_value, "")))
            continue
        elif action == "END TRIGGER":
            cells = (f"{indent}End Trigger", "", "", "")
        elif action == "END":
            cells = ("", "End", "", comment)
        elif action in {"SET", "RUN"}:
            display_time = row_time if row_time and row_time != last_time else ""
            if display_time:
                last_time = display_time
            cells = (display_time, f"{indent}{target}", value, comment)
        if cells is not None:
            output.append(_tsv(cells))
    return output


def _derived_stage_durations(rows: tuple[dict[str, str], ...]) -> dict[int, str]:
    stages: list[tuple[int, float]] = []
    for index, row in enumerate(rows):
        if row.get("Action") != "STAGE":
            continue
        try:
            stages.append((index, float(row.get("Time", ""))))
        except ValueError:
            continue
    result: dict[int, str] = {}
    for (index, start), (_, end) in zip(stages, stages[1:]):
        duration = end - start
        if duration > 0:
            result[index] = f"Duration = {duration:.3f} [min]"
    return result


def _trigger_parts(value: str) -> tuple[str, list[tuple[str, str]]]:
    parts = _split_top_level_commas(value)
    if not parts:
        return "", []
    name = parts[0].strip().rstrip(",")
    if name and not (name.startswith('"') and name.endswith('"')):
        name = f'"{name.strip(chr(34))}"'
    parameters: list[tuple[str, str]] = []
    known = {"truetime": "TrueTime", "delay": "Delay", "limit": "Limit", "hysteresis": "Hysteresis", "allowimmediateexecution": "AllowImmediateExecution"}
    for index, part in enumerate(parts[1:]):
        stripped = part.strip()
        key_text, separator, val = stripped.partition("=")
        normalized = re.sub(r"[^a-z]", "", key_text.casefold())
        if separator and normalized in known:
            parameters.append((known[normalized], val.strip()))
        else:
            parameters.append(("Condition" if index == 0 else "Parameter", stripped))
    return name, parameters


def _split_top_level_commas(value: str) -> list[str]:
    parts: list[str] = []
    current: list[str] = []
    depth = 0
    quoted = False
    for char in str(value or ""):
        if char == '"':
            quoted = not quoted
        elif not quoted and char == "(":
            depth += 1
        elif not quoted and char == ")" and depth:
            depth -= 1
        if char == "," and not quoted and depth == 0:
            parts.append("".join(current).strip())
            current = []
        else:
            current.append(char)
    if current or value.endswith(","):
        parts.append("".join(current).strip())
    return [part for part in parts if part]


def build_summaries(kb_root: Path, original_ids: list[tuple[str, list[ScriptSource]]]) -> str:
    source_rows: list[str] = []
    sections: list[str] = []
    available = {item[0] for item in SUMMARY_SOURCES if (kb_root / item[2]).exists()}
    for alias, title, relative_path, anchor in SUMMARY_SOURCES:
        path = kb_root / relative_path
        status = "Available" if alias in available else "Missing"
        source_rows.append(f"| `{alias}` | {title} | {status} | [Open](#{anchor}) |")
        if not path.exists():
            continue
        sections.extend([
            "",
            f'<a id="{anchor}"></a>',
            f"## {alias}: {title}",
            "",
            f"Build source name: `{path.name}`",
            "",
            _web_safe(path.read_text(encoding="utf-8")),
        ])

    description_root = kb_root / "FOQ/TCC/Script Description"
    for index, name in enumerate(SCRIPT_DESCRIPTION_NAMES, 1):
        path = description_root / name
        alias = f"D{index:03d}"
        anchor = f"script-description-{index:03d}"
        source_rows.append(f"| `{alias}` | Deep script analysis: {name} | {'Available' if path.exists() else 'Missing'} | [Open](#{anchor}) |")
        if path.exists():
            sections.extend([
                "",
                f'<a id="{anchor}"></a>',
                f"## {alias}: Deep Script Analysis - {name}",
                "",
                _web_safe(path.read_text(encoding="utf-8")),
            ])

    method_index = [
        f"| `{stable_id}` | `{group[0].method}` | {'/'.join(sorted({item.device for item in group}))} | Original script evidence in `02_METHOD_ORIGINAL_SCRIPTS.md` |"
        for stable_id, group in original_ids
    ]
    header = [
        "# Online TCC Method Understanding and Summary Collection",
        "",
        "Online_KB_Status: CANDIDATE_FOR_WEB_VALIDATION  ",
        "Upload_Allowed: Validation only  ",
        f"Build_Date: {date.today().isoformat()}",
        "",
        "## Original Method Cross-Index",
        "",
        "| Original ID | CM method | Device evidence | Evidence location |",
        "|---|---|---|---|",
        *method_index,
        "",
        "## Summary Source Index",
        "",
        "| Source ID | Knowledge section | Status | Section |",
        "|---|---|---|---|",
        *source_rows,
        "",
        "## Interpretation Contract",
        "",
        "Use original scripts as executable evidence. Use the sections below to understand purpose, roles, dependencies and safe changes. If interpretation conflicts with an original command sequence, preserve the original and mark the conflict for review. Do not silently repair or invent commands.",
        "",
        "Stress-extension originals (`VH-STRESS`) currently have command evidence but no source-grounded TD/black-box interpretation. They may be used to learn verified Trigger and valve-switching syntax only; their test purpose and safe composition remain `Open Verification Required`.",
    ]
    return "\n".join(header + sections).rstrip() + "\n"


def copy_build_sources(kb_root: Path, raw_sources: list[ScriptSource], build_root: Path) -> None:
    spec_dir = build_root / "01_Spec"
    raw_dir = build_root / "02_Original"
    summary_dir = build_root / "03_Summary"
    for directory in (spec_dir, raw_dir, summary_dir):
        directory.mkdir(parents=True, exist_ok=True)

    spec_sources = [
        ("S001.md", kb_root / "Method Script Generator/Generator Spec/CM_METHOD_SCRIPT_MD_FORMAT_SPEC.md"),
        ("S002.md", kb_root / "CM/Instrument Commands/CM_INSTRUMENT_COMMAND_KNOWLEDGE_BASE_V2.md"),
        ("S003.md", kb_root / "Method Script Generator/Generator Spec/CM Compiler Rules.MD"),
    ]
    manifest = ["# Method Online KB Build Source Manifest", "", f"Build_Date: {date.today().isoformat()}", "", "## SPEC Sources", "", "| Alias | Original source |", "|---|---|"]
    for alias, path in spec_sources:
        shutil.copy2(path, spec_dir / alias)
        manifest.append(f"| `{alias}` | `{path}` |")

    manifest.extend(["", "## Original Script Sources", "", "| Alias | Method | Device | Sequence | SHA-256 | Original source |", "|---|---|---|---|---|---|"])
    for index, source in enumerate(sorted(raw_sources, key=lambda item: (item.method.casefold(), item.device)), 1):
        alias = f"R{index:03d}.tsv"
        shutil.copy2(source.path, raw_dir / alias)
        manifest.append(f"| `{alias}` | `{source.method}` | {source.device} | `{source.sequence}` | `{source.digest}` | `{source.path}` |")

    manifest.extend(["", "## Summary Sources", "", "| Alias | Purpose | Original source |", "|---|---|---|"])
    for alias, title, relative_path, _anchor in SUMMARY_SOURCES:
        path = kb_root / relative_path
        if path.exists():
            shutil.copy2(path, summary_dir / f"{alias}.md")
            manifest.append(f"| `{alias}.md` | {title} | `{path}` |")
    description_root = kb_root / "FOQ/TCC/Script Description"
    for index, name in enumerate(SCRIPT_DESCRIPTION_NAMES, 1):
        path = description_root / name
        if path.exists():
            alias = f"D{index:03d}.md"
            shutil.copy2(path, summary_dir / alias)
            manifest.append(f"| `{alias}` | Deep script analysis | `{path}` |")
    (build_root / "SOURCE_MANIFEST.md").write_text("\n".join(manifest) + "\n", encoding="utf-8")


def _web_safe(text: str) -> str:
    return re.sub(r"[A-Za-z]:\\[^\n`]+", "[local build source omitted]", text).strip()


def _tsv(cells: tuple[str, str, str, str]) -> str:
    return "\t".join(_cell(value) for value in cells)


def _cell(value: str) -> str:
    text = str(value or "")
    for broken, repaired in {
        "Â°C": "°C",
        "Â°": "°",
        "â‰¤": "<=",
        "â‰¥": ">=",
        "â€“": "-",
        "â€”": "-",
    }.items():
        text = text.replace(broken, repaired)
    return text.replace("\t", " ").replace("\r", " ").replace("\n", "\\n")


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", str(value).casefold()).strip("-")


def _int(value: str) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the three self-contained online Method KB files.")
    parser.add_argument("--kb-root", type=Path, default=DEFAULT_KB_ROOT)
    parser.add_argument("--raw-root", type=Path, required=True)
    parser.add_argument("--stress-root", type=Path)
    parser.add_argument("--output-root", type=Path, required=True)
    args = parser.parse_args()

    core_sources = read_sources(args.raw_root)
    if len(core_sources) != 42:
        raise SystemExit(f"Expected 42 refreshed core TCC method sources, found {len(core_sources)}")
    stress_sources = read_sources(args.stress_root) if args.stress_root else []
    if args.stress_root and len(stress_sources) != 22:
        raise SystemExit(f"Expected 22 refreshed TCC stress sources, found {len(stress_sources)}")
    sources = core_sources + stress_sources
    method_root = args.output_root / "02_Full_Context" / "TCC" / "Method"
    build_root = args.output_root / "01_Build_Sources" / "TCC" / "Method"
    method_root.mkdir(parents=True, exist_ok=True)
    spec = build_spec(args.kb_root)
    originals, original_ids = build_originals(sources)
    summaries = build_summaries(args.kb_root, original_ids)
    (method_root / "01_METHOD_SPEC.md").write_text(spec, encoding="utf-8")
    (method_root / "02_METHOD_ORIGINAL_SCRIPTS.md").write_text(originals, encoding="utf-8")
    (method_root / "03_METHOD_SUMMARIES.md").write_text(summaries, encoding="utf-8")
    copy_build_sources(args.kb_root, sources, build_root)
    print(f"Built Method SPEC: {len(spec):,} chars")
    print(f"Built Method ORIGINAL: {len(originals):,} chars")
    print(f"Built Method SUMMARY: {len(summaries):,} chars")
    print(f"Original source files: {len(sources)}; unique script bodies: {len(script_groups(sources))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
