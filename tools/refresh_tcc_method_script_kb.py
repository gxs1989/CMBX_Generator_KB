from __future__ import annotations

import argparse
from pathlib import Path
import sys
import tempfile


MODULE_DIR = Path(__file__).resolve().parents[1]
if str(MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(MODULE_DIR))

from chromeleon_method_decoder import decode_cpxm_method_xml
from cmbx_container import load_cmbx_package, safe_filename
from embedded_method_extractor import extract_embedded_instrument_method
from method_xml_flow import build_method_flow_tsv


DEFAULT_WORKSPACE = Path(r"C:\ProgramData\CMBX Data Explorer Workspace")


def _default_sources(workspace: Path) -> list[tuple[str, Path, Path]]:
    packages = workspace / "packages"
    return [
        (
            "main",
            packages / "TCC Cost Out" / "Zollner" / "Production" / "0000003.cmbx",
            Path("knowledge_base") / "tcc_reverse_probe" / "VA",
        ),
        (
            "main",
            packages / "TCC Cost Out" / "Zollner" / "Production" / "3000004.cmbx",
            Path("knowledge_base") / "tcc_reverse_probe" / "VC",
        ),
        (
            "main",
            packages / "TCC Cost Out" / "Zollner" / "Production" / "6000001.cmbx",
            Path("knowledge_base") / "tcc_reverse_probe" / "VH",
        ),
        (
            "stress",
            packages / "TCC Cost Out" / "Stress Test" / "Stress_VH_DVT013_20260529.cmbx",
            Path("cmbx_data_explorer") / "outputs" / "stress_probe",
        ),
    ]


def refresh_method_scripts(workspace: Path, kb_root: Path, source_filter: str = "all") -> list[Path]:
    refreshed: list[Path] = []
    for source_kind, cmbx_path, relative_output_root in _default_sources(workspace):
        if source_filter != "all" and source_kind != source_filter:
            continue
        if not cmbx_path.exists():
            print(f"SKIP missing source: {cmbx_path}")
            continue
        package = load_cmbx_package(cmbx_path)
        sequence_name = package.sequences[0].name if package.sequences else cmbx_path.stem
        output_dir = kb_root / relative_output_root / safe_filename(sequence_name, "sequence")
        output_dir.mkdir(parents=True, exist_ok=True)
        for method in package.methods_and_reports:
            if method.kind != "instrument_method":
                continue
            embedded = extract_embedded_instrument_method(package, method)
            if not embedded:
                print(f"SKIP no embedded method: {cmbx_path.name} / {method.name}")
                continue
            xml_text = _decode_embedded_method_xml(embedded.cpxm_payload)
            if not xml_text:
                print(f"SKIP decode failed: {cmbx_path.name} / {method.name}")
                continue
            path = output_dir / f"{safe_filename(method.name, 'instrument_method')}_embedded_method_flow.tsv"
            path.write_text(build_method_flow_tsv(xml_text, method.name), encoding="utf-8")
            refreshed.append(path)
            print(f"REFRESH {path}")
    return refreshed


def _decode_embedded_method_xml(cpxm_payload: bytes) -> str:
    with tempfile.TemporaryDirectory() as temp_dir:
        temp = Path(temp_dir)
        cpxm_path = temp / "method.cpxm.bin"
        xml_path = temp / "method.xml"
        cpxm_path.write_bytes(cpxm_payload)
        result = decode_cpxm_method_xml(cpxm_path, xml_path)
        if not result.ok or not xml_path.exists():
            return ""
        return xml_path.read_text(encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Refresh TCC embedded method flow TSV files from source CMBX packages.")
    parser.add_argument("--workspace", type=Path, default=DEFAULT_WORKSPACE)
    parser.add_argument(
        "--kb-root",
        type=Path,
        default=DEFAULT_WORKSPACE / "KB" / "CMBX Method Scripts" / "TCC",
    )
    parser.add_argument("--source", choices=["all", "main", "stress"], default="all")
    args = parser.parse_args()
    refreshed = refresh_method_scripts(args.workspace, args.kb_root, args.source)
    print(f"Refreshed {len(refreshed)} method flow TSV file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
