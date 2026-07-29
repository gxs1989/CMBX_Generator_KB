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
from cmbx_container import load_cmbx_package
from embedded_method_extractor import extract_embedded_instrument_method
from method_xml_flow import build_method_flow_tsv
from tools.build_online_gpt_method_kb import build_spec, render_strict_method_rows


DEFAULT_KB_ROOT = Path(r"C:\ProgramData\CMBX Data Explorer Workspace\KB")
DEFAULT_CMBX = Path(
    r"C:\Users\xiaoshu.guan\OneDrive - Thermo Fisher Scientific\Project\RID"
    r"\OQ sequence template\OQ 2026-07-28.cmbx"
)
EXPECTED_METHODS = {
    "WARM_UP",
    "RI_DET_LINEARITY",
    "EQUILIBRATION_RI_AND RF",
    "RI_DET_NOISE_AND_DRIFT",
    "STOP",
    "RESTORE",
}
BYTE_LIMIT = 200_000
DELIVERY_NAMES = (
    "01_METHOD_SPEC.md",
    "02_METHOD_ORIGINAL_SCRIPTS.md",
    "03_METHOD_SUMMARIES.md",
)


def _slug(value: str) -> str:
    return re.sub(r"[^A-Z0-9]+", "-", value.upper()).strip("-")


def _decode_methods(cmbx_path: Path) -> list[tuple[str, tuple[dict[str, str], ...], str]]:
    package = load_cmbx_package(cmbx_path)
    decoded: list[tuple[str, tuple[dict[str, str], ...], str]] = []
    for method in package.methods_and_reports:
        if method.kind != "instrument_method" or method.name not in EXPECTED_METHODS:
            continue
        embedded = extract_embedded_instrument_method(package, method)
        if not embedded:
            raise RuntimeError(f"No embedded instrument method payload: {method.name}")
        with tempfile.TemporaryDirectory(prefix="rid_method_decode_") as temp_dir:
            temp = Path(temp_dir)
            cpxm_path = temp / "method.cpxm.bin"
            xml_path = temp / "method.xml"
            cpxm_path.write_bytes(embedded.cpxm_payload)
            result = decode_cpxm_method_xml(cpxm_path, xml_path)
            if not result.ok or not xml_path.exists():
                raise RuntimeError(f"Failed to decode {method.name}: {result.message}")
            xml_text = xml_path.read_text(encoding="utf-8")
        flow = build_method_flow_tsv(xml_text, method.name)
        rows = tuple(csv.DictReader(io.StringIO(flow), delimiter="\t"))
        digest = hashlib.sha256(flow.encode("utf-8")).hexdigest()
        decoded.append((method.name, rows, digest))
    names = {item[0] for item in decoded}
    if names != EXPECTED_METHODS:
        missing = ", ".join(sorted(EXPECTED_METHODS - names)) or "none"
        raise RuntimeError(f"RID method set is incomplete; missing: {missing}")
    return sorted(decoded, key=lambda item: item[0].casefold())


def _build_originals(methods: list[tuple[str, tuple[dict[str, str], ...], str]], cmbx_path: Path) -> str:
    index: list[str] = []
    sections: list[str] = []
    for method, rows, digest in methods:
        stable_id = f"M-RID-{_slug(method)}"
        anchor = stable_id.casefold()
        index.append(f"| `{stable_id}` | `{method}` | {len(rows)} | `{digest[:12]}` | [Open](#{anchor}) |")
        sections.extend(
            [
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
                *(render_strict_method_rows(rows)),
                "```",
            ]
        )
    header = [
        "# Online Original RID OQ Method Script Collection",
        "",
        "Online_KB_Status: DECODED_FROM_OQ_CMBX  ",
        f"Build_Date: {date.today().isoformat()}  ",
        f"Source_CMBX: {cmbx_path.name}  ",
        f"Instrument_Method_Count: {len(methods)}",
        "",
        "This file contains the decoded executable method evidence from the RID OQ sequence template. Preserve command spelling, stage time, purge/autozero order, acquisition symmetry, and device macros. Interpretive summaries never override these rows.",
        "",
        "## Self Index",
        "",
        "| Stable ID | CM method | Rows | Hash | Section |",
        "|---|---|---:|---|---|",
        *index,
    ]
    return "\n".join(header + sections).rstrip() + "\n"


def _build_summaries(project_root: Path, compact: bool) -> str:
    main_path = project_root / "cmbx_data_explorer/docs/RID_OQ_TEST_KNOWLEDGE_BASE.md"
    evidence_path = project_root / "cmbx_data_explorer/docs/RID_OQ_METHOD_REPORT_EVIDENCE.md"
    main = main_path.read_text(encoding="utf-8")
    evidence = evidence_path.read_text(encoding="utf-8")
    routing = """## RID Method Routing Index

| User intent | Primary method | Supporting method | Required processing/report evidence |
|---|---|---|---|
| Warm up RID | `WARM_UP` | none | Precondition only; no dedicated RID result sheet |
| Five-point glycerine linearity | `RI_DET_LINEARITY` | `WARM_UP` | Processing Method `RI_DET_LINEARITY`; `RI_LINEARITY` report sheet |
| Prepare flowing noise/drift test | `EQUILIBRATION_RI_AND RF` | `WARM_UP` | Correct pump/mobile-phase state must exist before injection |
| Measure dynamic noise and drift | `RI_DET_NOISE_AND_DRIFT` | `EQUILIBRATION_RI_AND RF` | `NOINT`; `RI_NOISE_AND_DRIFT` report sheet |
| Stop into standby | `STOP` | none | Confirm actual pump standby command in configured system |
| Restore customer settings | `RESTORE` | none | Restore values are configuration-specific and not fully present in generic payload |

## Authoring Boundaries

- The OQ package uses generic `$RI`/`$RI_1` report macros and contains legacy detector comments. Confirm the configured device exposes compatible `RI` and `RI_1` symbols.
- Do not invent pump flow, sampler volume, integration events, calibration weighting, or customer restore values when they are absent from decoded evidence.
- `RI_DET_LINEARITY` requires five concentrations: 5, 10, 15, 25, and 35 mg/mL glycerine. The Processing Method remains partially decoded.
- Noise/drift relies on the exact purge schedule, -40 minute equilibration, -3 minute autozero, and 0–22 minute acquisition timeline.
- A generated method is a review candidate until local preflight, CMBX compilation, CM import/open, and CM Method Check pass.
"""
    if compact:
        selected = []
        for heading in ("## 4.", "## 5.", "## 6.", "## 7.", "## 8.", "## 9.", "## 13.", "## 14."):
            match = re.search(rf"(?ms)^{re.escape(heading)}.*?(?=^## \d+\.|\Z)", main)
            if match:
                selected.append(match.group(0).strip())
        main = "\n\n".join(selected)
        evidence = re.sub(r"(?ms)^## 7\..*\Z", "", evidence).strip()
    return (
        "# Online RID OQ Method Understanding and Summary Collection"
        + (" (<200 KB)" if compact else "")
        + "\n\n"
        + "Online_KB_Status: SOURCE_GROUNDED_WITH_OPEN_PROCESSING_GAPS  \n"
        + f"Build_Date: {date.today().isoformat()}  \n"
        + "Scope: RID OQ method roles, configuration, timing, report-facing RetTime/channel evidence, and safe authoring boundaries\n\n"
        + routing
        + "\n## RID OQ Test Knowledge\n\n"
        + main.strip()
        + "\n\n## Exact Method and Report Evidence\n\n"
        + evidence.strip()
        + "\n"
    )


def _write(path: Path, text: str, limit: int | None = None) -> None:
    payload = text.encode("utf-8")
    if limit is not None and len(payload) >= limit:
        raise RuntimeError(f"{path.name} is {len(payload):,} bytes; limit is {limit - 1:,}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)


def _zip_three(root: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name in DELIVERY_NAMES:
            archive.write(root / name, arcname=name)


def build(kb_root: Path, cmbx_path: Path, output_root: Path, project_root: Path) -> None:
    methods = _decode_methods(cmbx_path)
    full_root = output_root / "02_Full_Context/RID/Method"
    small_root = output_root / "03_Small_Context/RID/Method"
    build_root = output_root / "01_Build_Sources/RID/Method"
    spec = build_spec(kb_root).replace(
        "# Online Method Script Generation SPEC", "# Online RID Method Script Generation SPEC", 1
    )
    originals = _build_originals(methods, cmbx_path)
    summaries = _build_summaries(project_root, compact=False)
    compact_summaries = _build_summaries(project_root, compact=True)
    for root, summary, limit in (
        (full_root, summaries, None),
        (small_root, compact_summaries, BYTE_LIMIT),
    ):
        _write(root / DELIVERY_NAMES[0], spec, limit)
        _write(root / DELIVERY_NAMES[1], originals, limit)
        _write(root / DELIVERY_NAMES[2], summary, limit)
    _zip_three(small_root, output_root / "03_Small_Context/RID/Method_3Files_Under200K.zip")

    for folder in (build_root / "01_Spec", build_root / "02_Original_Decoded", build_root / "03_Summary"):
        folder.mkdir(parents=True, exist_ok=True)
    for index, path in enumerate(
        (
            kb_root / "Method Script Generator/Generator Spec/CM_METHOD_SCRIPT_MD_FORMAT_SPEC.md",
            kb_root / "CM/Instrument Commands/CM_INSTRUMENT_COMMAND_KNOWLEDGE_BASE_V2.md",
            kb_root / "Method Script Generator/Generator Spec/CM Compiler Rules.MD",
        ),
        1,
    ):
        shutil.copy2(path, build_root / "01_Spec" / f"S{index:03d}.md")
    for index, (method, rows, digest) in enumerate(methods, 1):
        with (build_root / "02_Original_Decoded" / f"R{index:03d}.tsv").open(
            "w", encoding="utf-8", newline=""
        ) as handle:
            writer = csv.DictWriter(handle, fieldnames=rows[0].keys(), delimiter="\t")
            writer.writeheader()
            writer.writerows(rows)
    shutil.copy2(
        project_root / "cmbx_data_explorer/docs/RID_OQ_TEST_KNOWLEDGE_BASE.md",
        build_root / "03_Summary/B001.md",
    )
    shutil.copy2(
        project_root / "cmbx_data_explorer/docs/RID_OQ_METHOD_REPORT_EVIDENCE.md",
        build_root / "03_Summary/B002.md",
    )
    (build_root / "SOURCE_MANIFEST.md").write_text(
        "# RID Online Method KB Build Manifest\n\n"
        f"Build_Date: {date.today().isoformat()}  \n"
        f"Source_CMBX: {cmbx_path}  \n"
        f"Decoded_Methods: {len(methods)}  \n\n"
        "R001..R006 are decoded execution evidence. B001/B002 are the reviewed RID OQ knowledge and method/report evidence layers.\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Build RID OQ online Method KB packages.")
    parser.add_argument("--kb-root", type=Path, default=DEFAULT_KB_ROOT)
    parser.add_argument("--cmbx", type=Path, default=DEFAULT_CMBX)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--project-root", type=Path, required=True)
    args = parser.parse_args()
    build(args.kb_root, args.cmbx, args.output_root, args.project_root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
