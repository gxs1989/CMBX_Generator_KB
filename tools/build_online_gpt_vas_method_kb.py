from __future__ import annotations

import argparse
import csv
from datetime import date
import hashlib
import io
from pathlib import Path
import re
import shutil
import sys
import tempfile
import zipfile


MODULE_DIR = Path(__file__).resolve().parents[1]
if str(MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(MODULE_DIR))

from chromeleon_method_decoder import decode_cpxm_method_xml
from cmbx_container import load_cmbx_package, safe_filename
from embedded_method_extractor import extract_embedded_instrument_method
from method_xml_flow import build_method_flow_tsv
from tools.build_online_gpt_method_kb import build_spec, render_strict_method_rows


DEFAULT_KB_ROOT = Path(r"C:\ProgramData\CMBX Data Explorer Workspace\KB")
BYTE_LIMIT = 200_000
DELIVERY_NAMES = (
    "01_METHOD_SPEC.md",
    "02_METHOD_ORIGINAL_SCRIPTS.md",
    "03_METHOD_SUMMARIES.md",
)


def _repair(text: str) -> str:
    for broken, repaired in {
        "Ã‚Â°C": "°C",
        "Â°C": "°C",
        "[Â°C]": "[°C]",
        "Âµ": "µ",
        "Ã‚Âµ": "µ",
        "ml/minÂ²": "ml/min²",
        "Ã¢â€°Â¤": "<=",
        "Ã¢â€°Â¥": ">=",
    }.items():
        text = text.replace(broken, repaired)
    return text


def _slug(value: str) -> str:
    return re.sub(r"[^A-Z0-9]+", "-", value.upper()).strip("-")


def _decode_methods(cmbx_path: Path) -> list[tuple[str, tuple[dict[str, str], ...], str]]:
    package = load_cmbx_package(cmbx_path)
    decoded: list[tuple[str, tuple[dict[str, str], ...], str]] = []
    for method in package.methods_and_reports:
        if method.kind != "instrument_method":
            continue
        embedded = extract_embedded_instrument_method(package, method)
        if not embedded:
            raise RuntimeError(f"No embedded instrument method payload: {method.name}")
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            cpxm_path = temp / "method.cpxm.bin"
            xml_path = temp / "method.xml"
            cpxm_path.write_bytes(embedded.cpxm_payload)
            result = decode_cpxm_method_xml(cpxm_path, xml_path)
            if not result.ok or not xml_path.exists():
                raise RuntimeError(f"Failed to decode instrument method: {method.name}: {result.message}")
            xml_text = xml_path.read_text(encoding="utf-8")
        flow = build_method_flow_tsv(xml_text, method.name)
        rows = tuple(csv.DictReader(io.StringIO(flow), delimiter="\t"))
        digest = hashlib.sha256(flow.encode("utf-8")).hexdigest()
        decoded.append((method.name, rows, digest))
    if len(decoded) != 19:
        raise RuntimeError(f"Expected 19 VAS instrument methods in {cmbx_path.name}, found {len(decoded)}")
    return decoded


def _build_originals(methods: list[tuple[str, tuple[dict[str, str], ...], str]], cmbx_path: Path) -> str:
    index: list[str] = []
    sections: list[str] = []
    for method, rows, digest in methods:
        stable_id = f"M-VAS-{_slug(method)}"
        anchor = stable_id.casefold()
        index.append(f"| `{stable_id}` | `{method}` | {len(rows)} | `{digest[:12]}` | [Open](#{anchor}) |")
        sections.extend([
            "",
            f'<a id="{anchor}"></a>',
            f"## {stable_id}: {method}",
            "",
            f"Source CMBX: `{cmbx_path.name}`  ",
            f"Decoded flow SHA-256: `{digest}`  ",
            f"Decoded rows: `{len(rows)}`",
            "",
            "```tsv",
            "Time\tCommand\tValue\tComment",
            *(_repair(row) for row in render_strict_method_rows(rows)),
            "```",
        ])
    header = [
        "# Online Original VAS Method Script Collection",
        "",
        "Online_KB_Status: DECODED_FROM_GOLDEN_CMBX  ",
        f"Build_Date: {date.today().isoformat()}  ",
        f"Source_CMBX: {cmbx_path.name}  ",
        f"Instrument_Method_Count: {len(methods)}",
        "",
        "This file is regenerated from embedded instrument-method payloads in the VAS CMBX. It is executable evidence, not interpretation. Preserve command spelling, stage timing, branch structure, service-command strings, and acquisition symmetry unless a reviewed change contract explicitly permits modification.",
        "",
        "## Self Index",
        "",
        "| Stable ID | CM method | Rows | Hash | Section |",
        "|---|---|---:|---|---|",
        *index,
    ]
    return "\n".join(header + sections).rstrip() + "\n"


def _front_matter_value(text: str, key: str) -> str:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*(.+?)\s*$", text)
    return match.group(1).strip() if match else ""


def _summary_files(summary_root: Path) -> list[Path]:
    files = sorted(summary_root.glob("[0-9][0-9]_*_KB.md"))
    if len(files) != 19:
        raise RuntimeError(f"Expected 19 VAS summary files in {summary_root}, found {len(files)}")
    return files


def _compact_summary(text: str) -> str:
    chunks: list[str] = []
    preamble = text.split("## 1.", 1)[0].strip()
    if preamble:
        chunks.append(preamble)
    for section in (1, 2, 5, 6, 9, 10, 11, 12):
        match = re.search(rf"(?ms)^## {section}\..*?(?=^## \d+\.|\Z)", text)
        if match:
            chunks.append(match.group(0).strip())
    return "\n\n".join(chunks)


def _build_summaries(summary_root: Path, kb_root: Path, compact: bool) -> str:
    index_rows: list[str] = []
    sections: list[str] = []
    for path in _summary_files(summary_root):
        text = _repair(path.read_text(encoding="utf-8"))
        source = _front_matter_value(text, "source_method_file") or path.stem
        family = _front_matter_value(text, "method_family") or "unknown"
        status = _front_matter_value(text, "status") or "not explicit"
        source_method = Path(source).stem
        stable_id = f"S-VAS-{_slug(source_method)}"
        anchor = stable_id.casefold()
        index_rows.append(f"| `{stable_id}` | `{source_method}` | `{family}` | `{status}` | [Open](#{anchor}) |")
        body = _compact_summary(text) if compact else text
        sections.extend(["", f'<a id="{anchor}"></a>', f"## {stable_id}: {source_method}", "", body.strip()])

    method_index_path = summary_root / "00_METHOD_KB_INDEX.md"
    if not method_index_path.exists():
        raise RuntimeError(f"Missing VAS method index: {method_index_path}")
    method_index_text = _repair(method_index_path.read_text(encoding="utf-8"))

    support_sources = [
        ("K-VAS-TD", kb_root / "FOQ/Autosampler/FOQ_VAS_TD_KNOWLEDGE_MANAGEMENT.md"),
        ("K-VAS-LOGIC", kb_root / "FOQ/Autosampler/FOQ_TD_TEST_LOGIC_KNOWLEDGE_BASE.md"),
        ("K-VAS-REPORT", kb_root / "Method Script Generator/TCC/report_template_cmbx/VAS_DVAS_V_3_45_FORMULA_INVENTORY.md"),
    ]
    support_index: list[str] = []
    support_sections: list[str] = []
    for source_id, path in support_sources:
        if not path.exists():
            support_index.append(f"| `{source_id}` | Missing | `{path.name}` |")
            continue
        support_index.append(f"| `{source_id}` | Available | `{path.name}` |")
        if not compact:
            support_sections.extend(["", f'<a id="{source_id.casefold()}"></a>', f"## {source_id}: {path.stem}", "", _repair(path.read_text(encoding="utf-8")).strip()])

    header = [
        "# Online VAS Method Understanding and Summary Collection" + (" (<200 KB)" if compact else ""),
        "",
        "Online_KB_Status: DERIVED_KNOWLEDGE_REQUIRES_CM_REVIEW  ",
        f"Build_Date: {date.today().isoformat()}  ",
        "Scope: VAS method roles, reusable execution patterns, configuration dependencies, and report-facing evidence",
        "",
        "The original-script collection is the command source of truth. These summaries are derived interpretations. They may route an intent and explain a method, but they must not override decoded CMBX rows. Any generated method still requires local preflight, CMBX compilation, CM import/open, and CM Method Check.",
        "",
        "## Self Index",
        "",
        "| Summary ID | Source method | Family | Evidence status | Section |",
        "|---|---|---|---|---|",
        *index_rows,
        "",
        "## Supporting Knowledge",
        "",
        "| ID | Status | Source |",
        "|---|---|---|",
        *support_index,
    ]
    routing_section = [
        "",
        '<a id="k-vas-method-index"></a>',
        "## K-VAS-METHOD-INDEX: Cross-Method Routing Index",
        "",
        method_index_text.strip(),
    ]
    return "\n".join(header + routing_section + sections + support_sections).rstrip() + "\n"


def _copy_build_sources(
    methods: list[tuple[str, tuple[dict[str, str], ...], str]],
    summary_root: Path,
    kb_root: Path,
    build_root: Path,
) -> None:
    decoded_root = build_root / "02_Original_Decoded"
    summary_out = build_root / "03_Summary"
    spec_out = build_root / "01_Spec"
    for directory in (decoded_root, summary_out, spec_out):
        directory.mkdir(parents=True, exist_ok=True)
    spec_sources = [
        kb_root / "Method Script Generator/Generator Spec/CM_METHOD_SCRIPT_MD_FORMAT_SPEC.md",
        kb_root / "CM/Instrument Commands/CM_INSTRUMENT_COMMAND_KNOWLEDGE_BASE_V2.md",
        kb_root / "Method Script Generator/Generator Spec/CM Compiler Rules.MD",
    ]
    for index, path in enumerate(spec_sources, 1):
        shutil.copy2(path, spec_out / f"S{index:03d}.md")
    source_map = ["# VAS Build Source Alias Map", "", "| Alias | Source |", "|---|---|"]
    for index, (method, rows, _digest) in enumerate(methods, 1):
        alias = f"R{index:03d}.tsv"
        path = decoded_root / alias
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=rows[0].keys(), delimiter="\t")
            writer.writeheader()
            writer.writerows(rows)
        source_map.append(f"| `{alias}` | `{method}` |")
    for index, path in enumerate(_summary_files(summary_root), 1):
        alias = f"B{index:03d}.md"
        shutil.copy2(path, summary_out / alias)
        source_map.append(f"| `{alias}` | `{path.name}` |")
    shutil.copy2(summary_root / "00_METHOD_KB_INDEX.md", summary_out / "B000.md")
    source_map.append("| `B000.md` | `00_METHOD_KB_INDEX.md` |")
    (build_root / "SOURCE_MANIFEST.md").write_text(
        "# VAS Online Method KB Build Manifest\n\n"
        f"Build_Date: {date.today().isoformat()}  \n"
        f"Decoded_Methods: {len(methods)}  \n"
        "Derived_Summaries: 19\n\n"
        "Decoded TSV files are regenerated from the golden VAS CMBX and are the execution source of truth. Summary files retain their supplied review status.\n",
        encoding="utf-8",
    )
    (build_root / "SOURCE_ALIAS_MAP.md").write_text("\n".join(source_map) + "\n", encoding="utf-8")


def _write(path: Path, text: str, byte_limit: int | None = None) -> None:
    payload = text.encode("utf-8")
    if byte_limit is not None and len(payload) >= byte_limit:
        raise RuntimeError(f"{path.name} is {len(payload):,} bytes; limit is {byte_limit - 1:,}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)


def build(kb_root: Path, cmbx_path: Path, summary_root: Path, output_root: Path) -> None:
    methods = _decode_methods(cmbx_path)
    full_root = output_root / "02_Full_Context" / "VAS" / "Method"
    small_root = output_root / "03_Small_Context" / "VAS" / "Method"
    build_root = output_root / "01_Build_Sources" / "VAS" / "Method"
    spec = build_spec(kb_root).replace("# Online Method Script Generation SPEC", "# Online VAS Method Script Generation SPEC", 1)
    originals = _build_originals(methods, cmbx_path)
    summaries = _build_summaries(summary_root, kb_root, compact=False)
    compact_summaries = _build_summaries(summary_root, kb_root, compact=True)
    _write(full_root / DELIVERY_NAMES[0], spec)
    _write(full_root / DELIVERY_NAMES[1], originals)
    _write(full_root / DELIVERY_NAMES[2], summaries)
    _write(small_root / DELIVERY_NAMES[0], spec, BYTE_LIMIT)
    _write(small_root / DELIVERY_NAMES[1], originals, BYTE_LIMIT)
    _write(small_root / DELIVERY_NAMES[2], compact_summaries, BYTE_LIMIT)
    _copy_build_sources(methods, summary_root, kb_root, build_root)
    zip_path = output_root / "03_Small_Context" / "VAS" / "Method_3Files_Under200K.zip"
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name in DELIVERY_NAMES:
            archive.write(small_root / name, arcname=name)
    manifest_lines = [
        "# VAS Small-Context Method KB Manifest",
        "",
        f"Build_Date: {date.today().isoformat()}",
        "",
        "| File | Bytes | Status |",
        "|---|---:|---|",
    ]
    for name in DELIVERY_NAMES:
        size = (small_root / name).stat().st_size
        manifest_lines.append(f"| `{name}` | {size:,} | {'OK' if size < BYTE_LIMIT else 'OVER LIMIT'} |")
    (build_root / "SMALL_CONTEXT_MANIFEST.md").write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")
    print(f"Decoded VAS methods: {len(methods)}")
    for root in (full_root, small_root):
        for name in DELIVERY_NAMES:
            print(f"{root}: {name} = {(root / name).stat().st_size:,} bytes")
    print(f"Small-context ZIP: {zip_path}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build module-scoped VAS online Method KB packages.")
    parser.add_argument("--kb-root", type=Path, default=DEFAULT_KB_ROOT)
    parser.add_argument("--cmbx", type=Path, required=True)
    parser.add_argument("--summary-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    args = parser.parse_args()
    build(args.kb_root, args.cmbx, args.summary_root, args.output_root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
