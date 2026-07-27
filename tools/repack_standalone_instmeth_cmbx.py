from __future__ import annotations

import argparse
import re
import sys
import tempfile
import zipfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path

TOOL_ROOT = Path(__file__).resolve().parents[1]
if str(TOOL_ROOT) not in sys.path:
    sys.path.insert(0, str(TOOL_ROOT))

from chromeleon_method_encoder import encode_method_xml_cpxm
from cmbx_container import extract_cmbx_entry, load_cmbx_package
from embedded_method_extractor import _extract_method_payload


@dataclass(frozen=True)
class Field:
    number: int
    wire_type: int
    tag_start: int
    value_start: int
    value_end: int
    field_end: int
    raw: bytes


def repack_standalone_method_cmbx(source_cmbx: Path, edited_xml: Path, output_cmbx: Path, method_name: str | None = None) -> None:
    package = load_cmbx_package(source_cmbx)
    methods = [element for element in package.methods_and_reports if element.kind == "instrument_method"]
    if len(methods) != 1:
        raise ValueError(f"Expected exactly one standalone instrument method, found {len(methods)}.")
    method = methods[0]
    entry_name = method.package_entry_name
    if not entry_name:
        raise ValueError("Instrument method element does not reference a package entry.")

    with tempfile.TemporaryDirectory(prefix="cmbx_repack_") as tmp:
        cpxm_path = Path(tmp) / "edited.cpxm"
        encode_result = encode_method_xml_cpxm(edited_xml, cpxm_path)
        if not encode_result.ok:
            raise RuntimeError(encode_result.message)
        new_cpxm = cpxm_path.read_bytes()

    original_cmd = extract_cmbx_entry(source_cmbx, entry_name)
    payload = _extract_method_payload(original_cmd, 0)
    if payload is None:
        raise ValueError(f"Could not locate method payload inside {entry_name}.")
    new_cmd = _replace_cpxm_payload(original_cmd, new_cpxm, old_method_name=method.name, new_method_name=method_name)

    header = extract_cmbx_entry(source_cmbx, "header.xml")
    output_entry_name = entry_name
    if method_name:
        output_entry_name = f"{_safe_entry_stem(method_name)}.instmeth_1.cmd"
        header = _rename_standalone_method_header(header, method_name, output_entry_name, len(new_cmd))
    output_cmbx.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output_cmbx, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(output_entry_name, new_cmd)
        archive.writestr("header.xml", header)


def _rename_standalone_method_header(header: bytes, method_name: str, entry_name: str, payload_size: int) -> bytes:
    root = ET.fromstring(header.decode("utf-8-sig", errors="replace"))
    elements = [node for node in root if node.tag.endswith("ChromeleonElement")]
    if len(elements) != 1:
        raise ValueError(f"Expected exactly one ChromeleonElement in standalone method header, found {len(elements)}.")
    element = elements[0]
    display_name = method_name.strip()
    element.set("Name", display_name)
    element.set("Filename", entry_name)
    element.set("Size", str(payload_size))
    url = element.attrib.get("Url", "")
    if url:
        prefix = url.rsplit("/", 1)[0] if "/" in url else ""
        suffix = f"{_safe_entry_stem(display_name)}.instmeth"
        element.set("Url", f"{prefix}/{suffix}" if prefix else suffix)
    return b'<?xml version="1.0" encoding="UTF-8"?>' + ET.tostring(root, encoding="utf-8")


def _safe_entry_stem(method_name: str) -> str:
    cleaned = "".join(ch if ch.isalnum() or ch in {"_", "-"} else "_" for ch in method_name.strip())
    cleaned = re.sub(r"_+", "_", cleaned).strip("_")
    return cleaned or "generated_method"


def _replace_cpxm_payload(cmd_payload: bytes, new_cpxm: bytes, old_method_name: str | None = None, new_method_name: str | None = None) -> bytes:
    top_fields = _parse_fields(cmd_payload)
    rebuilt = bytearray()
    replaced = False
    for field in top_fields:
        if field.number != 19 or field.wire_type != 2:
            rebuilt.extend(field.raw)
            continue
        nested_buffer = cmd_payload[field.value_start : field.value_end]
        nested = _parse_fields(nested_buffer)
        nested_rebuilt = bytearray()
        for nested_field in nested:
            nested_value = nested_buffer[nested_field.value_start : nested_field.value_end]
            if (
                nested_field.number == 28
                and nested_field.wire_type == 2
                and old_method_name
                and new_method_name
                and nested_value == old_method_name.encode("utf-8")
            ):
                nested_rebuilt.extend(_field_bytes(28, 2, new_method_name.encode("utf-8")))
                continue
            if nested_field.number != 11 or nested_field.wire_type != 2:
                nested_rebuilt.extend(nested_field.raw)
                continue
            method_payload = nested_field.raw[nested_field.value_start - nested_field.tag_start : nested_field.value_end - nested_field.tag_start]
            new_method_payload = _replace_method_payload_cpxm(method_payload, new_cpxm)
            nested_rebuilt.extend(_field_bytes(11, 2, new_method_payload))
            replaced = True
        rebuilt.extend(_field_bytes(19, 2, bytes(nested_rebuilt)))
    if not replaced:
        raise ValueError("Could not replace nested CpXm payload.")
    return bytes(rebuilt)


def _replace_method_payload_cpxm(method_payload: bytes, new_cpxm: bytes) -> bytes:
    fields = _parse_fields(method_payload)
    rebuilt = bytearray()
    replaced = False
    for field in fields:
        if field.number == 3 and field.wire_type == 2:
            rebuilt.extend(_field_bytes(3, 2, new_cpxm))
            replaced = True
        else:
            rebuilt.extend(field.raw)
    if not replaced:
        raise ValueError("Method payload does not contain a length-delimited CpXm field 3.")
    return bytes(rebuilt)


def _parse_fields(data: bytes) -> list[Field]:
    fields: list[Field] = []
    pos = 0
    while pos < len(data):
        tag_start = pos
        tag, pos = _read_varint(data, pos)
        number = tag >> 3
        wire_type = tag & 7
        if wire_type == 0:
            value_start = pos
            _value, pos = _read_varint(data, pos)
            value_end = pos
        elif wire_type == 1:
            value_start = pos
            pos += 8
            value_end = pos
        elif wire_type == 2:
            length, pos = _read_varint(data, pos)
            value_start = pos
            value_end = pos + length
            pos = value_end
        elif wire_type == 5:
            value_start = pos
            pos += 4
            value_end = pos
        else:
            raise ValueError(f"Unsupported protobuf wire type {wire_type} at byte {tag_start}.")
        if value_end > len(data):
            raise ValueError(f"Field {number} extends beyond payload length.")
        fields.append(
            Field(
                number=number,
                wire_type=wire_type,
                tag_start=tag_start,
                value_start=value_start,
                value_end=value_end,
                field_end=pos,
                raw=data[tag_start:pos],
            )
        )
    return fields


def _field_bytes(number: int, wire_type: int, value: bytes) -> bytes:
    tag = (number << 3) | wire_type
    if wire_type != 2:
        raise ValueError("Only length-delimited fields are supported for synthetic writes.")
    return _encode_varint(tag) + _encode_varint(len(value)) + value


def _read_varint(data: bytes, offset: int) -> tuple[int, int]:
    value = 0
    shift = 0
    pos = offset
    while pos < len(data):
        byte = data[pos]
        pos += 1
        value |= (byte & 0x7F) << shift
        if not byte & 0x80:
            return value, pos
        shift += 7
        if shift > 63:
            break
    raise ValueError(f"Invalid varint at byte offset {offset}")


def _encode_varint(value: int) -> bytes:
    output = bytearray()
    while value > 0x7F:
        output.append((value & 0x7F) | 0x80)
        value >>= 7
    output.append(value)
    return bytes(output)


def main() -> None:
    parser = argparse.ArgumentParser(description="Repack a standalone exported Chromeleon instrument method CMBX from edited decoded XML.")
    parser.add_argument("source_cmbx", type=Path)
    parser.add_argument("edited_xml", type=Path)
    parser.add_argument("output_cmbx", type=Path)
    parser.add_argument("--method-name", default=None, help="Display/import name for the generated standalone method.")
    args = parser.parse_args()
    repack_standalone_method_cmbx(args.source_cmbx, args.edited_xml, args.output_cmbx, method_name=args.method_name)
    print(args.output_cmbx)


if __name__ == "__main__":
    main()
