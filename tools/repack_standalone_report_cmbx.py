from __future__ import annotations

"""Repack a standalone Chromeleon report-template CMBX from decoded report XML.

The report layout is carried in FormulaOne ``SpreadSheetData`` inside the XML.
This tool deliberately preserves it unless the caller has edited it with a
compatible writer.  It only owns the CMBX/CpXm container boundary.
"""

import argparse
import re
import sys
import tempfile
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

TOOL_ROOT = Path(__file__).resolve().parents[1]
if str(TOOL_ROOT) not in sys.path:
    sys.path.insert(0, str(TOOL_ROOT))

from chromeleon_method_encoder import encode_method_xml_cpxm
from cmbx_container import extract_cmbx_entry, load_cmbx_package
from tools.repack_standalone_instmeth_cmbx import _field_bytes, _parse_fields


def repack_standalone_report_cmbx(
    source_cmbx: Path,
    edited_xml: Path,
    output_cmbx: Path,
    report_name: str | None = None,
) -> None:
    """Create a standalone report CMBX, using one exported report as a carrier."""
    package = load_cmbx_package(source_cmbx)
    reports = [element for element in package.methods_and_reports if element.kind == "report_template"]
    if len(reports) != 1:
        raise ValueError(f"Expected exactly one standalone report template, found {len(reports)}.")
    report = reports[0]
    entry_name = report.package_entry_name
    if not entry_name:
        raise ValueError("Report template element does not reference a package entry.")

    with tempfile.TemporaryDirectory(prefix="cmbx_report_repack_") as tmp:
        cpxm_path = Path(tmp) / "edited.report.cpxm"
        result = encode_method_xml_cpxm(edited_xml, cpxm_path)
        if not result.ok:
            raise RuntimeError(result.message)
        new_cpxm = cpxm_path.read_bytes()

    original_cmd = extract_cmbx_entry(source_cmbx, entry_name)
    new_cmd = _replace_report_cpxm_payload(
        original_cmd,
        new_cpxm,
        old_report_name=report.name,
        new_report_name=report_name,
    )
    header = extract_cmbx_entry(source_cmbx, "header.xml")
    output_entry_name = entry_name
    if report_name:
        output_entry_name = f"{_safe_entry_stem(report_name)}.report_1.cmd"
        header = _rename_standalone_report_header(header, report_name, output_entry_name, len(new_cmd))

    output_cmbx.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output_cmbx, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(output_entry_name, new_cmd)
        archive.writestr("header.xml", header)


def _replace_report_cpxm_payload(
    cmd_payload: bytes,
    new_cpxm: bytes,
    old_report_name: str | None = None,
    new_report_name: str | None = None,
) -> bytes:
    rebuilt = bytearray()
    replaced = False
    for field in _parse_fields(cmd_payload):
        if field.number != 19 or field.wire_type != 2:
            rebuilt.extend(field.raw)
            continue
        nested_data = cmd_payload[field.value_start : field.value_end]
        nested_rebuilt = bytearray()
        for nested in _parse_fields(nested_data):
            value = nested_data[nested.value_start : nested.value_end]
            if (
                nested.number == 28
                and nested.wire_type == 2
                and old_report_name
                and new_report_name
                and value == old_report_name.encode("utf-8")
            ):
                nested_rebuilt.extend(_field_bytes(28, 2, new_report_name.encode("utf-8")))
            elif nested.number == 15 and nested.wire_type == 2:
                # Field 15 contains a small protobuf wrapper whose field 1 is CpXm.
                nested_rebuilt.extend(_field_bytes(15, 2, _field_bytes(1, 2, new_cpxm)))
                replaced = True
            else:
                nested_rebuilt.extend(nested.raw)
        rebuilt.extend(_field_bytes(19, 2, bytes(nested_rebuilt)))
    if not replaced:
        raise ValueError("Could not replace standalone report CpXm payload (field 19/15/1).")
    return bytes(rebuilt)


def _rename_standalone_report_header(header: bytes, report_name: str, entry_name: str, payload_size: int) -> bytes:
    root = ET.fromstring(header.decode("utf-8-sig", errors="replace"))
    elements = [node for node in root if node.tag.endswith("ChromeleonElement")]
    if len(elements) != 1:
        raise ValueError(f"Expected exactly one ChromeleonElement in standalone report header, found {len(elements)}.")
    element = elements[0]
    display_name = report_name.strip()
    element.set("Name", display_name)
    element.set("Filename", entry_name)
    element.set("Size", str(payload_size))
    url = element.attrib.get("Url", "")
    if url:
        prefix = url.rsplit("/", 1)[0] if "/" in url else ""
        suffix = f"{_safe_entry_stem(display_name)}.report"
        element.set("Url", f"{prefix}/{suffix}" if prefix else suffix)
    return b'<?xml version="1.0" encoding="UTF-8"?>' + ET.tostring(root, encoding="utf-8")


def _safe_entry_stem(name: str) -> str:
    cleaned = "".join(ch if ch.isalnum() or ch in {"_", "-"} else "_" for ch in name.strip())
    cleaned = re.sub(r"_+", "_", cleaned).strip("_")
    return cleaned or "generated_report"


def main() -> None:
    parser = argparse.ArgumentParser(description="Repack a standalone Chromeleon report-template CMBX from decoded XML.")
    parser.add_argument("source_cmbx", type=Path)
    parser.add_argument("edited_xml", type=Path)
    parser.add_argument("output_cmbx", type=Path)
    parser.add_argument("--report-name", default=None)
    args = parser.parse_args()
    repack_standalone_report_cmbx(args.source_cmbx, args.edited_xml, args.output_cmbx, report_name=args.report_name)
    print(args.output_cmbx)


if __name__ == "__main__":
    main()
