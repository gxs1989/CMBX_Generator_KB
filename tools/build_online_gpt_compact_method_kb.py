from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import re
import shutil
import zipfile


BYTE_LIMIT = 200_000
UPLOAD_FILES = (
    "01_METHOD_SPEC.md",
    "02_METHOD_ORIGINAL_SCRIPTS.md",
    "03_METHOD_SUMMARIES.md",
)

ORIGINAL_IDS = (
    "M-TCC-ASYNCHRON8",
    "M-TCC-PREHEATER",
    "M-TCC-STRESS-TEST-5S",
    "M-TCC-STRESS-TEST-5S-REALPREHEATER-PCC-OFF-10MIN-EQUIBRATION",
    "M-TCC-SYNCHRON8",
    "M-TCC-HEAT-COOL-VA",
    "M-TCC-HEAT-COOL-VCVH",
    "M-TCC-ACCURACY-VA",
    "M-TCC-ACCURACY-VCVH",
    "M-TCC-CALIBRATION-VA",
    "M-TCC-CALIBRATION-VCVH",
    "M-TCC-PRECISION",
    "M-TCC-PRECISION-FAN",
    "M-TCC-STABILITY-VA",
    "M-TCC-STABILITY-VCVH",
    "M-TCC-STABILITY-PCC-VA",
    "M-TCC-STABILITY-PCC-VCVH",
    "M-TCC-VALVES-VA",
    "M-TCC-VALVES-VCVH",
)

SUMMARY_IDS = (
    "K001",
    "K002",
    "K003",
    "K004",
    "B005",
    "B006",
    "B007",
    "B008",
    "B009",
)


def _section(text: str, heading_pattern: str, identifier: str) -> str:
    pattern = re.compile(
        rf"(?ms)(?:<a id=\"[^\"]+\"></a>\n)?## {re.escape(identifier)}:[^\n]*\n.*?(?=\n<a id=|\n## [A-Z][0-9]{{3}}:|\Z)"
    )
    match = pattern.search(text)
    if not match:
        raise ValueError(f"Missing section {identifier} using {heading_pattern}")
    return match.group(0).strip()


def _original_index_rows(text: str) -> dict[str, str]:
    rows: dict[str, str] = {}
    for line in text.splitlines():
        match = re.match(r"^\| `(M-TCC-[^`]+)` \|", line)
        if match:
            rows[match.group(1)] = line
    return rows


def _build_original(full_text: str) -> str:
    rows = _original_index_rows(full_text)
    sections = [_section(full_text, "original", identifier) for identifier in ORIGINAL_IDS]
    header = [
        "# Small-Context Online TCC Method Script Collection (<200 KB)",
        "",
        "Online_KB_Status: CANDIDATE_FOR_WEB_VALIDATION  ",
        "Upload_Profile: Small-context web models (including Doubao)  ",
        "Scope: TCC temperature tests, preheater, valves and representative stress Trigger methods",
        "",
        "This compact file contains exact selected sections from the full ORIGINAL collection. It intentionally omits unrelated service/error/factory methods. Use the full package when the requested intent is outside this scope.",
        "",
        "## Self Index",
        "",
        "| Stable ID | CM method | Device evidence | Sequence source | Rows | Hash | Section |",
        "|---|---|---|---|---:|---|---|",
        *(rows[identifier] for identifier in ORIGINAL_IDS),
        "",
    ]
    return "\n".join(header + sections) + "\n"


def _build_summary(full_text: str) -> str:
    sections = [_section(full_text, "summary", identifier) for identifier in SUMMARY_IDS]
    header = [
        "# Small-Context Online TCC Method Understanding Collection (<200 KB)",
        "",
        "Online_KB_Status: CANDIDATE_FOR_WEB_VALIDATION  ",
        "Upload_Profile: Small-context web models (including Doubao)  ",
        "Scope: TCC temperature intent plus valve/stress Trigger composition",
        "",
        "## Self Index",
        "",
        "| ID | Knowledge role |",
        "|---|---|",
        "| `K001` | FOQ test logic |",
        "| `K002` | Method role contracts |",
        "| `K003` | Test relationship model |",
        "| `K004` | Stress Trigger scheduling contract |",
        "| `B005` | Temperature Calibration black box |",
        "| `B006` | Temperature Accuracy black box |",
        "| `B007` | Temperature Precision/Fan black box |",
        "| `B008` | Temperature Stability/PCC black box |",
        "| `B009` | Heat-up/Cool-down black box |",
        "",
        "Use ORIGINAL scripts as executable evidence. Use this SUMMARY for roles and safe composition. Do not invent commands when evidence is absent.",
        "",
    ]
    return "\n".join(header + sections) + "\n"


def _write_checked(path: Path, text: str) -> None:
    payload = text.encode("utf-8")
    if len(payload) >= BYTE_LIMIT:
        raise ValueError(f"{path.name} is {len(payload)} bytes; limit is {BYTE_LIMIT - 1}")
    path.write_bytes(payload)


def _write_manifest(path: Path, output_root: Path) -> None:
    lines = [
        "# Small-Context Method KB Build Manifest",
        "",
        f"Build_Date: {date.today().isoformat()}  ",
        f"Per_File_Byte_Limit: {BYTE_LIMIT - 1}  ",
        "Upload_File_Count: 3",
        "",
        "## Delivery Files",
        "",
        "| File | Bytes | Status |",
        "|---|---:|---|",
    ]
    for name in UPLOAD_FILES:
        size = (output_root / name).stat().st_size
        lines.append(f"| `{name}` | {size:,} | {'OK' if size < BYTE_LIMIT else 'OVER LIMIT'} |")
    lines.extend([
        "",
        "## Selected Stable IDs",
        "",
        f"- ORIGINAL: `{', '.join(ORIGINAL_IDS)}`",
        f"- SUMMARY: `{', '.join(SUMMARY_IDS)}`",
        "",
        "## Scope",
        "",
        "Included: TCC temperature methods, Preheater, standard Valves, and representative periodic Stress Trigger methods.",
        "Omitted: unrelated service, error-log, factory-default, liquid-leak, burn-in and non-selected stress variants.",
        "",
        "The small-context package is a selected derivative of the full Method KB. Rebuild it whenever the full SPEC, ORIGINAL, or SUMMARY changes.",
        "Only the three delivery files are uploaded to the web model. This manifest remains in `01_Build_Sources/TCC/Method/Small_Context`.",
        "",
    ])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_zip(path: Path, output_root: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name in UPLOAD_FILES:
            archive.write(output_root / name, arcname=name)


def build(full_root: Path, output_root: Path, manifest: Path | None = None, zip_output: Path | None = None) -> None:
    source = full_root / "02_Full_Context" / "TCC" / "Method"
    output_root.mkdir(parents=True, exist_ok=True)
    spec_source = source / "01_METHOD_SPEC.md"
    original_source = source / "02_METHOD_ORIGINAL_SCRIPTS.md"
    summary_source = source / "03_METHOD_SUMMARIES.md"
    _write_checked(
        output_root / "01_METHOD_SPEC.md",
        spec_source.read_text(encoding="utf-8"),
    )
    _write_checked(
        output_root / "02_METHOD_ORIGINAL_SCRIPTS.md",
        _build_original(original_source.read_text(encoding="utf-8")),
    )
    _write_checked(
        output_root / "03_METHOD_SUMMARIES.md",
        _build_summary(summary_source.read_text(encoding="utf-8")),
    )
    for path in sorted(output_root.glob("*.md")):
        if path.stat().st_size >= BYTE_LIMIT:
            raise ValueError(f"{path.name} exceeds {BYTE_LIMIT - 1} bytes")
        print(f"{path.name}: {path.stat().st_size:,} bytes")
    delivery_names = tuple(path.name for path in sorted(output_root.glob("*.md")))
    if delivery_names != UPLOAD_FILES:
        raise ValueError(f"Expected exactly {UPLOAD_FILES}, found {delivery_names}")
    if manifest:
        _write_manifest(manifest, output_root)
        print(f"manifest={manifest}")
    if zip_output:
        _write_zip(zip_output, output_root)
        print(f"zip={zip_output}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a three-file Method KB profile below 200 KB per file.")
    parser.add_argument("--full-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--zip-output", type=Path)
    args = parser.parse_args()
    build(args.full_root, args.output_root, args.manifest, args.zip_output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
