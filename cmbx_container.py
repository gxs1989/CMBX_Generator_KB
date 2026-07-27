from __future__ import annotations

import re
import os
import struct
import tempfile
import zlib
import zipfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path


LOCAL_FILE_HEADER = b"PK\x03\x04"


@dataclass(frozen=True)
class CmbxEntry:
    name: str
    compression_method: int
    compressed_size: int
    uncompressed_size: int
    data_offset: int


@dataclass
class CmbxElement:
    id: str
    name: str
    item_type: str
    url: str = ""
    raw_filename: str = ""
    filename: str = ""
    size: int | None = None
    raw_data_file_id: str = ""
    parent_id: str | None = None
    children: list["CmbxElement"] = field(default_factory=list)

    @property
    def kind(self) -> str:
        lowered = self.item_type.lower()
        if "subfolder" in lowered or lowered.endswith(".folder") or "data.folder" in lowered:
            return "folder"
        if "sequencefolder" in lowered or "sequence.folder" in lowered:
            return "folder"
        if "sequence" in lowered:
            return "sequence"
        if "injection" in lowered:
            return "injection"
        if "signal" in lowered:
            return "signal"
        if "audittrail" in lowered:
            return "audit"
        if "instrumentmethod" in lowered:
            return "instrument_method"
        if "processingmethod" in lowered:
            return "processing_method"
        if "reportdefinition" in lowered or "datapresentationlayout" in lowered:
            return "report_template"
        return "other"

    @property
    def package_entry_name(self) -> str:
        return self.raw_filename or self.filename


@dataclass
class CmbxPackage:
    path: Path
    entries: list[CmbxEntry]
    root_elements: list[CmbxElement]
    elements_by_id: dict[str, CmbxElement]
    header_attributes: dict[str, str] = field(default_factory=dict)
    _sequences_cache: list[CmbxElement] | None = field(default=None, init=False, repr=False)
    _injections_cache: list[CmbxElement] | None = field(default=None, init=False, repr=False)
    _channels_cache: list[CmbxElement] | None = field(default=None, init=False, repr=False)
    _audits_cache: list[CmbxElement] | None = field(default=None, init=False, repr=False)
    _methods_reports_cache: list[CmbxElement] | None = field(default=None, init=False, repr=False)

    @property
    def sequences(self) -> list[CmbxElement]:
        if self._sequences_cache is not None:
            return self._sequences_cache
        sequences: list[CmbxElement] = []

        def walk(elements: list[CmbxElement]) -> None:
            for element in elements:
                if element.kind == "sequence":
                    sequences.append(element)
                walk(element.children)

        walk(self.root_elements)
        self._sequences_cache = sequences
        return sequences

    @property
    def injections(self) -> list[CmbxElement]:
        if self._injections_cache is None:
            self._injections_cache = [element for element in self.elements_by_id.values() if element.kind == "injection"]
        return self._injections_cache

    @property
    def channels(self) -> list[CmbxElement]:
        if self._channels_cache is None:
            self._channels_cache = [element for element in self.elements_by_id.values() if element.kind == "signal"]
        return self._channels_cache

    @property
    def audits(self) -> list[CmbxElement]:
        if self._audits_cache is None:
            self._audits_cache = [element for element in self.elements_by_id.values() if element.kind == "audit"]
        return self._audits_cache

    @property
    def methods_and_reports(self) -> list[CmbxElement]:
        if self._methods_reports_cache is None:
            self._methods_reports_cache = [
                element
                for element in self.elements_by_id.values()
                if element.kind in {"instrument_method", "processing_method", "report_template"}
            ]
        return self._methods_reports_cache


def iter_cmbx_entries(path: str | Path) -> list[CmbxEntry]:
    data = Path(path).read_bytes()
    return _iter_cmbx_entries_from_bytes(data)


def _iter_cmbx_entries_from_bytes(data: bytes) -> list[CmbxEntry]:
    entries: list[CmbxEntry] = []
    pos = 0
    while True:
        sig = data.find(LOCAL_FILE_HEADER, pos)
        if sig < 0 or sig + 30 > len(data):
            break
        (
            _signature,
            _version,
            _flags,
            compression_method,
            _modified_time,
            _modified_date,
            _crc,
            compressed_size,
            uncompressed_size,
            name_length,
            extra_length,
        ) = struct.unpack_from("<IHHHHHIIIHH", data, sig)
        name_start = sig + 30
        data_offset = name_start + name_length + extra_length
        if data_offset > len(data):
            break
        name = data[name_start : name_start + name_length].decode("utf-8", errors="replace")
        entries.append(
            CmbxEntry(
                name=name,
                compression_method=compression_method,
                compressed_size=compressed_size,
                uncompressed_size=uncompressed_size,
                data_offset=data_offset,
            )
        )
        pos = data_offset + compressed_size if compressed_size else data_offset + 1
    return entries


def extract_cmbx_entry(path: str | Path, entry_name: str) -> bytes:
    cmbx_path = Path(path)
    data = cmbx_path.read_bytes()
    for entry in _iter_cmbx_entries_from_bytes(data):
        if entry.name != entry_name:
            continue
        payload = data[entry.data_offset : entry.data_offset + entry.compressed_size]
        if entry.compression_method == 0:
            return payload
        if entry.compression_method == 8:
            return zlib.decompress(payload, -15)
        raise ValueError(f"Unsupported CMBX compression method {entry.compression_method} for {entry.name}")
    raise KeyError(f"CMBX entry not found: {entry_name}")


def read_cmbx_header_xml(path: str | Path) -> str:
    return extract_cmbx_entry(path, "header.xml").decode("utf-8-sig", errors="replace")


def load_cmbx_package(path: str | Path) -> CmbxPackage:
    cmbx_path = Path(path)
    data = cmbx_path.read_bytes()
    entries = _iter_cmbx_entries_from_bytes(data)
    header = _extract_entry_from_bytes(data, entries, "header.xml").decode("utf-8-sig", errors="replace")
    root = ET.fromstring(header)
    elements_by_id: dict[str, CmbxElement] = {}

    def parse_element(node: ET.Element, parent_id: str | None) -> CmbxElement:
        element = CmbxElement(
            id=node.attrib.get("Id", ""),
            name=node.attrib.get("Name", ""),
            item_type=node.attrib.get("ItemType", ""),
            url=node.attrib.get("Url", ""),
            raw_filename=node.attrib.get("RawDataFilename", ""),
            filename=node.attrib.get("Filename", ""),
            size=_parse_int(node.attrib.get("Size")),
            raw_data_file_id=node.attrib.get("RawDataFileId", ""),
            parent_id=parent_id,
        )
        if element.id:
            elements_by_id[element.id] = element
        for child_node in node:
            if child_node.tag != "ChromeleonElement":
                continue
            element.children.append(parse_element(child_node, element.id or parent_id))
        return element

    root_elements = [
        parse_element(node, None)
        for node in root
        if node.tag == "ChromeleonElement"
    ]
    return CmbxPackage(
        path=cmbx_path,
        entries=entries,
        root_elements=root_elements,
        elements_by_id=elements_by_id,
        header_attributes=dict(root.attrib),
    )


def _extract_entry_from_bytes(data: bytes, entries: list[CmbxEntry], entry_name: str) -> bytes:
    for entry in entries:
        if entry.name != entry_name:
            continue
        payload = data[entry.data_offset : entry.data_offset + entry.compressed_size]
        if entry.compression_method == 0:
            return payload
        if entry.compression_method == 8:
            return zlib.decompress(payload, -15)
        raise ValueError(f"Unsupported CMBX compression method {entry.compression_method} for {entry.name}")
    raise KeyError(f"CMBX entry not found: {entry_name}")


def summarize_package(package: CmbxPackage) -> dict[str, int]:
    return {
        "sequences": len(package.sequences),
        "injections": len(package.injections),
        "channels": len(package.channels),
        "audits": len(package.audits),
        "instrument_methods": len([m for m in package.methods_and_reports if m.kind == "instrument_method"]),
        "processing_methods": len([m for m in package.methods_and_reports if m.kind == "processing_method"]),
        "report_templates": len([m for m in package.methods_and_reports if m.kind == "report_template"]),
        "entries": len(package.entries),
    }


def split_cmbx_sequences(package: CmbxPackage, sequences: list[CmbxElement], output_folder: str | Path | None = None) -> list[Path]:
    """Write selected sequence subtrees as standalone CMBX packages."""
    if not sequences:
        return []
    output_root = Path(output_folder) if output_folder else package.path.parent
    output_root.mkdir(parents=True, exist_ok=True)
    source_root = ET.fromstring(read_cmbx_header_xml(package.path))
    node_by_id = {
        node.attrib.get("Id", ""): node
        for node in source_root.iter("ChromeleonElement")
        if node.attrib.get("Id", "")
    }
    entry_names = {entry.name for entry in package.entries}
    written: list[Path] = []
    for sequence in sequences:
        source_node = node_by_id.get(sequence.id)
        if source_node is None:
            continue
        header_root = ET.Element(source_root.tag, source_root.attrib)
        header_root.append(ET.fromstring(ET.tostring(source_node, encoding="utf-8")))
        header_bytes = b'<?xml version="1.0" encoding="UTF-8"?>' + ET.tostring(header_root, encoding="utf-8")
        output_path = _unique_output_path(output_root / f"{safe_filename(sequence.name, 'sequence')}.cmbx")
        with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as archive:
            archive.writestr("header.xml", header_bytes)
            for entry_name in _entry_names_for_xml_node(source_node):
                if entry_name and entry_name in entry_names:
                    archive.writestr(entry_name, extract_cmbx_entry(package.path, entry_name))
        written.append(output_path)
    return written


def rename_cmbx_header_element(package: CmbxPackage, element: CmbxElement, new_name: str) -> None:
    """Rename an element in header.xml and rewrite the CMBX package in place."""
    if not element.id:
        raise ValueError("Cannot rename a CMBX element without an Id.")
    cleaned = str(new_name or "").strip()
    if not cleaned:
        raise ValueError("Name cannot be empty.")
    source_root = ET.fromstring(read_cmbx_header_xml(package.path))
    target = next((node for node in source_root.iter("ChromeleonElement") if node.attrib.get("Id", "") == element.id), None)
    if target is None:
        raise ValueError(f"CMBX element was not found in header.xml: {element.name}")
    target.set("Name", cleaned)
    header_bytes = b'<?xml version="1.0" encoding="UTF-8"?>' + ET.tostring(source_root, encoding="utf-8")
    fd, tmp_name = tempfile.mkstemp(prefix=f"{package.path.stem}_rename_", suffix=".cmbx", dir=str(package.path.parent))
    os.close(fd)
    Path(tmp_name).unlink(missing_ok=True)
    try:
        with zipfile.ZipFile(tmp_name, "w", zipfile.ZIP_DEFLATED) as archive:
            archive.writestr("header.xml", header_bytes)
            for entry in package.entries:
                if entry.name == "header.xml":
                    continue
                archive.writestr(entry.name, extract_cmbx_entry(package.path, entry.name))
        package.path.replace(package.path.with_suffix(package.path.suffix + ".bak"))
        Path(tmp_name).replace(package.path)
        package.path.with_suffix(package.path.suffix + ".bak").unlink(missing_ok=True)
    except Exception:
        tmp_path = Path(tmp_name)
        if tmp_path.exists():
            tmp_path.unlink(missing_ok=True)
        backup = package.path.with_suffix(package.path.suffix + ".bak")
        if backup.exists() and not package.path.exists():
            backup.replace(package.path)
        raise


def _entry_names_for_xml_node(node: ET.Element) -> list[str]:
    names: list[str] = []
    seen: set[str] = set()
    for child in node.iter("ChromeleonElement"):
        for attr_name in ("RawDataFilename", "Filename"):
            entry_name = child.attrib.get(attr_name, "")
            if entry_name and entry_name not in seen:
                seen.add(entry_name)
                names.append(entry_name)
    return names


def _unique_output_path(path: Path) -> Path:
    if not path.exists():
        return path
    stem = path.stem
    suffix = path.suffix
    for index in range(2, 10000):
        candidate = path.with_name(f"{stem}_{index}{suffix}")
        if not candidate.exists():
            return candidate
    raise FileExistsError(f"Could not find a unique output name for {path}")


def safe_filename(value: str, fallback: str = "item") -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_. -]+", "_", value).strip(" .")
    return cleaned or fallback


def element_path(package: CmbxPackage, element: CmbxElement) -> list[CmbxElement]:
    path = [element]
    current = element
    while current.parent_id and current.parent_id in package.elements_by_id:
        current = package.elements_by_id[current.parent_id]
        path.append(current)
    return list(reversed(path))


def injection_for_element(package: CmbxPackage, element: CmbxElement) -> CmbxElement | None:
    for candidate in reversed(element_path(package, element)):
        if candidate.kind == "injection":
            return candidate
    return None


def _parse_int(value: str | None) -> int | None:
    if value and value.isdigit():
        return int(value)
    return None
