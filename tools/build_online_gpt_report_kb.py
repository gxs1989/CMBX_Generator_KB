from __future__ import annotations

import argparse
import shutil
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
APP_ROOT = REPO_ROOT / "cmbx_data_explorer"
DOCS_ROOT = APP_ROOT / "docs"
STAGING_ROOT = APP_ROOT / "online_kb_staging" / "Report"
DEFAULT_OUTPUT_ROOT = Path(r"C:\ProgramData\CMBX Data Explorer Workspace\KB\KB_Online_GPT")

SPEC_SOURCE = DOCS_ROOT / "CM_REPORT_TEMPLATE_MD_TO_CMBX_SPEC.md"
LANGUAGE_SOURCE = DOCS_ROOT / "CM_REPORT_FORMULA_LANGUAGE_REFERENCE.md"
HELP_SOURCE = DOCS_ROOT / "CM_REPORT_FORMULA_HELP_CATALOG.md"
DYNAMIC_TABLE_SOURCE = DOCS_ROOT / "CM_REPORT_DYNAMIC_TABLE_KNOWLEDGE_BASE.md"

TCC_ORIGINAL_SOURCE = STAGING_ROOT / "02_REPORT_ORIGINAL_TEMPLATES.md"
TCC_SUMMARY_SOURCE = STAGING_ROOT / "03_REPORT_SUMMARIES.md"

PROBE_ROOT = APP_ROOT / "outputs" / "report_template_probe"
CONTROL_ROOT = APP_ROOT / "outputs" / "formulaone_control_pair"
PROGRAM_REPORT_ROOT = Path(
    r"C:\ProgramData\CMBX Data Explorer Workspace\KB\Method Script Generator\TCC\report_template_cmbx"
)

REPORT_MODULES = {
    "TCC": {
        "status": "PARTIAL - VTCC and PressureEvaluation evidence available; VATCC canonical inventory missing",
        "originals": (
            ("VTCC_FULL", CONTROL_ROOT / "Report_VTCC_V2_12_full_formula_inventory.md"),
            ("VTCC_FORMULAONE", DOCS_ROOT / "REPORT_VTCC_V2_12_FORMULAONE_INVENTORY.md"),
            ("PRESSURE_EVALUATION", PROGRAM_REPORT_ROOT / "PressureEvaluation_FORMULA_INVENTORY.md"),
        ),
        "summaries": (
            ("TCC_METHOD_REPORT_KB", DOCS_ROOT / "TCC_FOQ_METHOD_REPORT_KNOWLEDGE_BASE.md"),
            ("TCC_ALIGNMENT", DOCS_ROOT / "TCC_METHOD_REPORT_ALIGNMENT.md"),
            ("VALVE_PRESSURE_CONTRACT", DOCS_ROOT / "VALVE_SHIFT_SYNCHRON_PRESSURE_EVALUATION_REPORT_CONTRACT.md"),
        ),
    },
    "VAS": {
        "status": "ORIGINAL AVAILABLE - semantic report summary not complete",
        "originals": (("VAS_3_45", PROBE_ROOT / "VAS_DVAS_V_3_45_FORMULA_INVENTORY.md"),),
        "summaries": (),
    },
    "VVWD": {
        "status": "ORIGINAL AVAILABLE - semantic report summary not complete",
        "originals": (("VVWD_2_31", PROBE_ROOT / "FOQ_REPORT_VVWD_V2_31_FORMULA_INVENTORY.md"),),
        "summaries": (),
    },
    "Pump": {
        "status": "ORIGINAL AVAILABLE - semantic report summary not complete",
        "originals": (("VA_PUMP_1_01_02", PROBE_ROOT / "Report_VAPump_FOQ_V1_01_02_FORMULA_INVENTORY.md"),),
        "summaries": (),
    },
}

HPLC_HELP_SECTIONS = (
    "FormulaOne Function Topics",
    "Peak",
    "DetectionParameter",
    "Component",
    "ProcessingMethod",
    "Sequence",
    "Chromatogram",
    "Injection",
    "DataAuditTrail",
    "SSTDefinition",
    "GlobalFunctions",
    "Fraction",
    "General",
    "InstrumentMethod",
    "ReportTemplate",
    "ReportValueList",
    "SSTResults",
    "Table",
    "UvSettings",
    "AuditTrailEvent",
    "TimeFunctions",
    "AuditTrail",
    "AuditTrailEvents",
    "CellFormula",
    "CustomFormulas",
    "CustomVar",
    "Evaluate",
    "IntegrationTable",
    "Precondition",
    "repvar",
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig").strip()


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def _heading_sections(text: str) -> dict[str, str]:
    lines = text.splitlines()
    headings: list[tuple[int, int, str]] = []
    for index, line in enumerate(lines):
        stripped = line.lstrip()
        if not stripped.startswith("#"):
            continue
        level = len(stripped) - len(stripped.lstrip("#"))
        if level not in (2, 3):
            continue
        title = stripped[level:].strip()
        headings.append((index, level, title))

    sections: dict[str, str] = {}
    for position, (start, level, title) in enumerate(headings):
        end = len(lines)
        for next_start, next_level, _ in headings[position + 1 :]:
            if next_level <= level:
                end = next_start
                break
        sections[title] = "\n".join(lines[start:end]).strip()
    return sections


def _without_title(text: str) -> str:
    lines = text.splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    return "\n".join(lines).strip()


def build_universal_report_spec() -> str:
    base = _without_title(_read(SPEC_SOURCE))
    language = _without_title(_read(LANGUAGE_SOURCE))
    base = base.replace(
        "**Formula language reference:** Read `CM_REPORT_FORMULA_LANGUAGE_REFERENCE.md` before authoring any direct CM formula. This specification controls the Markdown-to-CMBX conversion contract; it does not duplicate the complete Chromeleon report-variable language.",
        "**Formula language reference:** The complete HPLC authoring reference is embedded in Part B of this file. Use it before authoring any direct CM formula.",
    ).replace(
        "**Complete Help index:** Use `CM_REPORT_FORMULA_HELP_CATALOG.md` for the local CM7 Help topic catalog. For TCC workbook formulas, also use `REPORT_VTCC_V2_12_FORMULAONE_INVENTORY.md` as observed-function evidence.",
        "**Help index:** The HPLC-relevant CM7 Help catalog is embedded in Part C. Carrier-specific observed-function evidence belongs in the selected module ORIGINAL file.",
    )
    language = language.replace(
        "**Companion sources:** `CM_REPORT_FORMULA_HELP_CATALOG.md` is the complete local CM7 Help index (128 FormulaOne function topics and 994 report-variable topics). `REPORT_VTCC_V2_12_FORMULAONE_INVENTORY.md` remains observed FormulaOne evidence for TCC.",
        "**Embedded lookup:** Part C contains the HPLC-relevant CM7 Help index. Carrier-level FormulaOne evidence and verification matrices are supplied by the selected module ORIGINAL file.",
    )
    help_text = _read(HELP_SOURCE)
    help_sections = _heading_sections(help_text)
    selected = [help_sections[name] for name in HPLC_HELP_SECTIONS if name in help_sections]

    preface = """# Universal HPLC Report Template MD Specification

KB_Profile: Online Web Model  
Scope: Chromeleon report-template Markdown authoring and MD-to-CMBX static/native dynamic-table report creation  
Module_Scope: Shared by TCC, VAS, detector, pump and future HPLC modules  
Source_Policy: Self-contained; no access to local Chromeleon Help is required

## Upload and Routing Rule

Use this one SPEC for every HPLC module. It is sufficient for syntax and
compiler structure. Pair it with up to two module-specific evidence files
when the report must follow an existing method/test contract:

1. `02_REPORT_ORIGINAL_TEMPLATES.md` - decoded carrier objects, formulas and workbook evidence;
2. `03_REPORT_SUMMARIES.md` - semantic roles, method/report dependencies and safe-change guidance.

The universal SPEC defines the language and compiler contract. Module files
decide which channel, audit path, RetTime and processing result are actually
available. The model may create new sheets/cells, a new static layout, and the
native dynamic table types explicitly enabled by Part A. It must not invent
unavailable run data merely because the formula or table syntax exists.

## Embedded Source Index

| Part | Embedded content | Authority |
|---|---|---|
| A | MD-to-CMBX report-template contract, including supported native dynamic tables | Current compiler/write boundary |
| B | CM report formula language reference | HPLC authoring semantics and observed templates |
| C | HPLC-relevant official Help catalog | FormulaOne functions and report-variable lookup |

"""
    parts = [
        preface,
        "# Part A - Report Template Generation Contract\n\n" + base,
        "# Part B - CM Report Formula Language\n\n" + language,
        "# Part C - Embedded HPLC Formula Help Catalog\n\n"
        "The following entries are embedded from the local CM7 Help extraction. "
        "They are lookup evidence, not proof that every variable is available in every configuration.\n\n"
        + "\n\n".join(selected),
    ]
    return "\n\n".join(parts)


def _copy_build_sources(output_root: Path) -> None:
    common = output_root / "01_Build_Sources" / "Report" / "Common" / "01_Spec"
    for alias, source in (
        ("S001_REPORT_TEMPLATE_CONTRACT.md", SPEC_SOURCE),
        ("S002_REPORT_FORMULA_LANGUAGE.md", LANGUAGE_SOURCE),
        ("S003_REPORT_HELP_CATALOG.md", HELP_SOURCE),
        ("S004_REPORT_DYNAMIC_TABLE_KB.md", DYNAMIC_TABLE_SOURCE),
    ):
        common.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, common / alias)

    for module, definition in REPORT_MODULES.items():
        module_root = output_root / "01_Build_Sources" / "Report" / module
        for source_id, source in (*definition["originals"], *definition["summaries"]):
            if source.exists():
                target_family = "02_Original" if (source_id, source) in definition["originals"] else "03_Summary"
                target = module_root / target_family / f"{source_id}.md"
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)


def _module_collection(module: str, family: str) -> str:
    definition = REPORT_MODULES[module]
    items = definition[family]
    label = "Original Report Template Evidence" if family == "originals" else "Report Understanding Summaries"
    filename = "02_REPORT_ORIGINAL_TEMPLATES.md" if family == "originals" else "03_REPORT_SUMMARIES.md"
    lines = [
        f"# {module} {label}",
        "",
        f"Module: {module}  ",
        f"Status: {definition['status']}  ",
        f"Delivery_File: {filename}",
        "",
        "## Self Index",
        "",
        "| ID | Source | Included |",
        "|---|---|---|",
    ]
    available: list[tuple[str, Path]] = []
    for source_id, source in items:
        included = source.exists()
        lines.append(f"| `{source_id}` | `{source.name}` | {'Yes' if included else 'No - source missing'} |")
        if included:
            available.append((source_id, source))

    if not available:
        lines.extend(
            [
                "",
                "## Open Verification Required",
                "",
                "No consolidated semantic summary is currently available for this module. "
                "Do not ask a web model to generate a runnable report from the original inventory alone.",
            ]
        )
        return "\n".join(lines)

    for source_id, source in available:
        lines.extend(
            [
                "",
                "---",
                "",
                f"## Evidence: {source_id}",
                "",
                f"Source file: `{source.name}`",
                "",
                _without_title(_read(source)),
            ]
        )
    return "\n".join(lines)


def build(output_root: Path) -> None:
    universal_spec = build_universal_report_spec()
    spec_bytes = len(universal_spec.encode("utf-8"))
    if spec_bytes >= 200_000:
        raise RuntimeError(f"Universal Report SPEC must remain below 200,000 bytes; got {spec_bytes}")

    for owned in (
        output_root / "01_Build_Sources" / "Report",
        output_root / "02_Full_Context" / "Report",
        output_root / "03_Small_Context" / "Report",
    ):
        if owned.exists():
            shutil.rmtree(owned)

    _copy_build_sources(output_root)

    module_payloads = {
        module: {
            "originals": _module_collection(module, "originals"),
            "summaries": _module_collection(module, "summaries"),
        }
        for module in REPORT_MODULES
    }

    for profile in ("02_Full_Context", "03_Small_Context"):
        report_root = output_root / profile / "Report"
        _write(report_root / "01_REPORT_SPEC.md", universal_spec)
        for module, payload in module_payloads.items():
            _write(report_root / module / "02_REPORT_ORIGINAL_TEMPLATES.md", payload["originals"])
            _write(report_root / module / "03_REPORT_SUMMARIES.md", payload["summaries"])

    manifest = f"""# Universal Report KB Build Manifest

SPEC_bytes: {spec_bytes}  
SPEC_source_count: 4  
Delivery_rule: one universal SPEC plus two module-specific evidence files  
Modules: TCC, VAS, VVWD, Pump  
TCC_evidence_status: PARTIAL  
VAS_VVWD_Pump_status: ORIGINAL_ONLY

The same universal SPEC is published in Full and Small profiles because its
curated HPLC Help subset remains below the 200,000-byte per-file limit.
The delivery SPEC includes the supported Audit Trail, Peak Summary, and Integration dynamic-table contracts.
"""
    _write(output_root / "01_Build_Sources" / "Report" / "BUILD_MANIFEST.md", manifest)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the module-neutral Online GPT Report KB hierarchy.")
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    args = parser.parse_args()
    build(args.output_root.resolve())


if __name__ == "__main__":
    main()
