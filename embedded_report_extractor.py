from __future__ import annotations

import tempfile
from dataclasses import dataclass
from pathlib import Path
import xml.etree.ElementTree as ET

from chromeleon_method_decoder import decode_cpxm_method_xml
from cmbx_container import CmbxElement, CmbxPackage, extract_cmbx_entry


REPORT_HEADER_MARKER = b"\xca\x01"


@dataclass(frozen=True)
class EmbeddedReportTemplate:
    element_name: str
    sequence_name: str
    sequence_entry: str
    start: int
    end: int
    data: bytes
    cpxm_payload: bytes
    cpxm_start: int
    cpxm_end: int

    def metadata_text(self) -> str:
        return "\n".join(
            [
                f"Name: {self.element_name}",
                "Kind: embedded_report_template",
                f"Sequence: {self.sequence_name}",
                f"Sequence Entry: {self.sequence_entry}",
                f"Byte Range: {self.start}..{self.end}",
                f"Size: {len(self.data)} bytes",
                f"CpXm Payload Range: {self.cpxm_start}..{self.cpxm_end}",
                f"CpXm Payload Size: {len(self.cpxm_payload)} bytes",
                "",
                "Note",
                "----",
                "This report template block was extracted from the CMBX sequence command object.",
                "The CpXm payload can be decoded to Chromeleon report XML when Chromeleon runtime DLLs are available.",
            ]
        )


@dataclass(frozen=True)
class ReportSheet:
    report_name: str
    sheet_name: str
    sheet_id: str
    is_active: str
    each_injection: str
    query_enabled: str
    injection_variable: str
    comparison: str
    query_values: str
    applies_to_injection: str
    reason: str
    object_count: int = 0
    formula_count: int = 0


@dataclass(frozen=True)
class ReportSheetObject:
    report_name: str
    sheet_name: str
    object_id: str
    object_type: str
    left: str
    top: str
    right: str
    bottom: str
    excel_range: str
    formula: str
    fixed_channel: str
    fixed_component: str
    plot_type: str
    table_type: str


def extract_embedded_report_template(package: CmbxPackage, element: CmbxElement) -> EmbeddedReportTemplate | None:
    if element.kind != "report_template":
        return None
    sequence = _sequence_for_report_element(package, element)
    # A report exported directly from Chromeleon has no sequence parent: the
    # report command itself is the package entry.  Treat it as a first-class
    # report source so the Report Templates view can inspect its XML too.
    if not sequence and element.filename:
        data = extract_cmbx_entry(package.path, element.filename)
        # CpXm is a length-delimited protobuf value. It is not necessarily the
        # final value in a standalone .report command: generated reports can
        # carry object name and version metadata after it. Slicing to EOF would
        # silently append that metadata to the compressed report payload.
        cpxm = _find_cpxm_wire_value(data, 0, len(data))
        if not cpxm:
            return None
        cpxm_start, cpxm_end, cpxm_payload = cpxm
        return EmbeddedReportTemplate(
            element_name=element.name,
            sequence_name="(standalone report template)",
            sequence_entry=element.filename,
            start=0,
            end=len(data),
            data=data,
            cpxm_payload=cpxm_payload,
            cpxm_start=cpxm_start,
            cpxm_end=cpxm_end,
        )
    if not sequence or not sequence.filename:
        return None
    data = extract_cmbx_entry(package.path, sequence.filename)
    cpxm = _report_template_cpxm(data, element)
    if not cpxm:
        return None
    start, cpxm_start, cpxm_end, cpxm_payload = cpxm
    return EmbeddedReportTemplate(
        element_name=element.name,
        sequence_name=sequence.name,
        sequence_entry=sequence.filename,
        start=start,
        end=cpxm_end,
        data=data[start:cpxm_end],
        cpxm_payload=cpxm_payload,
        cpxm_start=cpxm_start,
        cpxm_end=cpxm_end,
    )


def _sequence_for_report_element(package: CmbxPackage, element: CmbxElement) -> CmbxElement | None:
    if element.parent_id:
        parent = package.elements_by_id.get(element.parent_id)
        if parent and parent.kind == "sequence":
            return parent
    for sequence in package.sequences:
        if any(child.id == element.id for child in sequence.children):
            return sequence
    # A folder-level or root report is a standalone payload even when the
    # package also contains sequences. Falling back to the first sequence
    # decodes unrelated method/report bytes from that sequence command.
    return None


def _report_template_cpxm(data: bytes, element: CmbxElement) -> tuple[int, int, int, bytes] | None:
    report_definition = "reportdefinition" in element.item_type.lower()
    name_offsets = _find_exact_name_offsets(data, element.name) if report_definition else _find_name_offsets(data, element.name)
    marker_offsets = _marker_offsets(data)
    if not name_offsets or not marker_offsets:
        return None
    candidates = _cpxm_candidates(data, marker_offsets)
    if not candidates:
        return None
    for name_offset in name_offsets:
        marker = _nearest_marker_before(marker_offsets, name_offset)
        if marker is None:
            continue
        if report_definition:
            previous = _nearest_cpxm_ending_at_or_before(candidates, marker)
            if previous:
                return previous
        current = next((candidate for candidate in candidates if candidate[0] == marker), None)
        if current:
            return current
    return None


def _find_name_offsets(data: bytes, name: str) -> list[int]:
    needle = name.encode("utf-8", errors="ignore")
    if not needle:
        return []
    offsets: list[int] = []
    pos = 0
    while True:
        pos = data.find(needle, pos)
        if pos < 0:
            return offsets
        offsets.append(pos)
        pos += 1


def _find_exact_name_offsets(data: bytes, name: str) -> list[int]:
    needle = name.encode("utf-8", errors="ignore")
    if not needle:
        return []
    offsets: list[int] = []
    pos = 0
    while True:
        pos = data.find(needle, pos)
        if pos < 0:
            break
        end = pos + len(needle)
        if _name_boundary(data, pos - 1) and _name_boundary(data, end):
            offsets.append(pos)
        pos += 1
    return offsets


def _name_boundary(data: bytes, offset: int) -> bool:
    if offset < 0 or offset >= len(data):
        return True
    byte = data[offset]
    return not (48 <= byte <= 57 or 65 <= byte <= 90 or 97 <= byte <= 122 or byte in (45, 95))


def _marker_offsets(data: bytes) -> list[int]:
    offsets: list[int] = []
    pos = 0
    while True:
        pos = data.find(REPORT_HEADER_MARKER, pos)
        if pos < 0:
            return offsets
        offsets.append(pos)
        pos += 1


def _cpxm_candidates(data: bytes, marker_offsets: list[int]) -> list[tuple[int, int, int, bytes]]:
    candidates: list[tuple[int, int, int, bytes]] = []
    seen: set[tuple[int, int]] = set()
    for marker in marker_offsets:
        cpxm = _extract_first_cpxm_from_record(data, marker)
        if not cpxm:
            continue
        cpxm_start, cpxm_end, cpxm_payload = cpxm
        key = (cpxm_start, cpxm_end)
        if key in seen:
            continue
        seen.add(key)
        candidates.append((marker, cpxm_start, cpxm_end, cpxm_payload))
    return candidates


def _nearest_marker_before(marker_offsets: list[int], offset: int) -> int | None:
    previous = None
    for marker in marker_offsets:
        if marker > offset:
            break
        previous = marker
    return previous


def _nearest_cpxm_ending_at_or_before(candidates: list[tuple[int, int, int, bytes]], marker: int) -> tuple[int, int, int, bytes] | None:
    previous = [candidate for candidate in candidates if candidate[2] <= marker]
    if not previous:
        return None
    return max(previous, key=lambda candidate: candidate[2])


def decode_report_template_xml(package: CmbxPackage, element: CmbxElement) -> tuple[EmbeddedReportTemplate, str]:
    embedded = extract_embedded_report_template(package, element)
    if not embedded:
        raise ValueError(f"Embedded report template payload was not found: {element.name}")
    tmp = Path(tempfile.gettempdir()) / "CmbxDataExplorer" / "report_templates"
    tmp.mkdir(parents=True, exist_ok=True)
    cpxm_path = tmp / f"{_safe_temp_name(element.name)}.cpxm.bin"
    xml_path = tmp / f"{_safe_temp_name(element.name)}.xml"
    cpxm_path.write_bytes(embedded.cpxm_payload)
    result = decode_cpxm_method_xml(cpxm_path, xml_path)
    if not result.ok or not xml_path.exists():
        raise ValueError(result.message)
    return embedded, xml_path.read_text(encoding="utf-8")


def parse_report_sheets(xml_text: str, report_name: str, injection_name: str = "") -> list[ReportSheet]:
    root = ET.fromstring(xml_text)
    sheet_ids = _sheet_ids(root)
    setups = _sheet_setups(root)
    object_counts = _sheet_object_counts(root)
    rows: list[ReportSheet] = []
    for sheet_name, sheet_id in sheet_ids.items():
        setup = setups.get(sheet_name, {})
        applies, reason = _applies_to_injection(setup, injection_name)
        object_count, formula_count = object_counts.get(sheet_name, (0, 0))
        rows.append(
            ReportSheet(
                report_name=report_name,
                sheet_name=sheet_name,
                sheet_id=sheet_id,
                is_active=setup.get("is_active", ""),
                each_injection=setup.get("each_injection", ""),
                query_enabled=setup.get("query_enabled", ""),
                injection_variable=setup.get("variable", ""),
                comparison=setup.get("comparison", ""),
                query_values=", ".join(setup.get("values", [])),
                applies_to_injection=applies,
                reason=reason,
                object_count=object_count,
                formula_count=formula_count,
            )
        )
    return rows


def report_sheets_tsv(sheets: list[ReportSheet]) -> str:
    header = [
        "Report",
        "Sheet",
        "SheetId",
        "IsActive",
        "EachInjection",
        "QueryEnabled",
        "InjectionVariable",
        "Comparison",
        "QueryValues",
        "AppliesToSelectedInjection",
        "Reason",
        "ObjectCount",
        "FormulaCount",
    ]
    lines = ["\t".join(header)]
    for sheet in sheets:
        lines.append(
            _tsv_row(
                [
                    sheet.report_name,
                    sheet.sheet_name,
                    sheet.sheet_id,
                    sheet.is_active,
                    sheet.each_injection,
                    sheet.query_enabled,
                    sheet.injection_variable,
                    sheet.comparison,
                    sheet.query_values,
                    sheet.applies_to_injection,
                    sheet.reason,
                    str(sheet.object_count),
                    str(sheet.formula_count),
                ]
            )
        )
    return "\n".join(lines)


def parse_report_sheet_objects(xml_text: str, report_name: str, sheet_name: str = "") -> list[ReportSheetObject]:
    root = ET.fromstring(xml_text)
    rows: list[ReportSheetObject] = []
    for description in root.findall(".//SheetDescription"):
        current_sheet = _child_value(description, "SheetName")
        if sheet_name and current_sheet != sheet_name:
            continue
        for obj in description.findall("SheetObject"):
            left = _child_value(obj, "Range/Left")
            top = _child_value(obj, "Range/Top")
            right = _child_value(obj, "Range/Right")
            bottom = _child_value(obj, "Range/Bottom")
            formulas = [node.attrib.get("value", "").strip() for node in obj.findall(".//Formula") if node.attrib.get("value", "").strip()]
            rows.append(
                ReportSheetObject(
                    report_name=report_name,
                    sheet_name=current_sheet,
                    object_id=_child_value(obj, "Id"),
                    object_type=obj.attrib.get("type", ""),
                    left=left,
                    top=top,
                    right=right,
                    bottom=bottom,
                    excel_range=_excel_range(left, top, right, bottom),
                    formula=" | ".join(formulas),
                    fixed_channel=_child_value(obj, "FixedChannel"),
                    fixed_component=_child_value(obj, "FixedComponentName"),
                    plot_type=_child_value(obj, "PlotType"),
                    table_type=_child_value(obj, "ReportTableType"),
                )
            )
    return rows


def report_sheet_objects_tsv(objects: list[ReportSheetObject]) -> str:
    header = [
        "Report",
        "Sheet",
        "ObjectId",
        "ObjectType",
        "Left",
        "Top",
        "Right",
        "Bottom",
        "ExcelRange",
        "Formula",
        "FixedChannel",
        "FixedComponent",
        "PlotType",
        "TableType",
    ]
    lines = ["\t".join(header)]
    for obj in objects:
        lines.append(
            _tsv_row(
                [
                    obj.report_name,
                    obj.sheet_name,
                    obj.object_id,
                    obj.object_type,
                    obj.left,
                    obj.top,
                    obj.right,
                    obj.bottom,
                    obj.excel_range,
                    obj.formula,
                    obj.fixed_channel,
                    obj.fixed_component,
                    obj.plot_type,
                    obj.table_type,
                ]
            )
        )
    return "\n".join(lines)


def _extract_first_cpxm_from_record(data: bytes, start: int) -> tuple[int, int, bytes] | None:
    pos = start
    while pos < len(data):
        try:
            tag, pos = _read_varint(data, pos)
        except ValueError:
            return None
        wire_type = tag & 7
        if wire_type == 0:
            try:
                _value, pos = _read_varint(data, pos)
            except ValueError:
                return None
        elif wire_type == 1:
            pos += 8
        elif wire_type == 2:
            try:
                length, pos = _read_varint(data, pos)
            except ValueError:
                return None
            value_start = pos
            value_end = value_start + length
            if value_end > len(data):
                return None
            cpxm = _find_cpxm_wire_value(data, value_start, value_end)
            if cpxm:
                return cpxm
            pos = value_end
        elif wire_type == 5:
            pos += 4
        else:
            return None
    return None


def _find_cpxm_wire_value(data: bytes, start: int, end: int, depth: int = 0) -> tuple[int, int, bytes] | None:
    if depth > 8:
        return None
    pos = start
    while pos < end:
        try:
            tag, pos = _read_varint(data, pos)
        except ValueError:
            return None
        wire_type = tag & 7
        if wire_type == 0:
            try:
                _value, pos = _read_varint(data, pos)
            except ValueError:
                return None
        elif wire_type == 1:
            pos += 8
        elif wire_type == 2:
            try:
                length, pos = _read_varint(data, pos)
            except ValueError:
                return None
            value_start = pos
            value_end = value_start + length
            if value_end > end:
                return None
            if data[value_start : value_start + 4] == b"CpXm":
                return value_start, value_end, data[value_start:value_end]
            nested = _find_cpxm_wire_value(data, value_start, value_end, depth + 1)
            if nested:
                return nested
            pos = value_end
        elif wire_type == 5:
            pos += 4
        else:
            return None
    return None


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


def _sheet_ids(root: ET.Element) -> dict[str, str]:
    sheets: dict[str, str] = {}
    for sheet in root.findall(".//SheetList/Sheet"):
        name = _child_value(sheet, "Name")
        sheet_id = _child_value(sheet, "Data/Id")
        if name:
            sheets[name] = sheet_id
    return sheets


def _sheet_setups(root: ET.Element) -> dict[str, dict[str, object]]:
    setups: dict[str, dict[str, object]] = {}
    for item in root.findall(".//PrintSettings/PrintSheetSetups/Setups/Item"):
        name = _child_value(item, "Name")
        data = item.find("Data")
        if not name or data is None:
            continue
        query_rules = data.findall(".//InjectionQuery//Item")
        inj_rule = _first_injection_name_rule(query_rules)
        values = [node.attrib.get("value", "") for node in inj_rule.findall(".//ValueItem")] if inj_rule is not None else []
        setups[name] = {
            "is_active": _child_value(data, "IsActive"),
            "each_injection": _child_value(data, "SheetSetupCondition/EachInjection"),
            "query_enabled": _child_value(data, "SheetSetupCondition/InjectionQueryCondition/Enabled"),
            "variable": _child_value(inj_rule, "Variable") if inj_rule is not None else "",
            "comparison": _child_value(inj_rule, "Comparison") if inj_rule is not None else "",
            "values": [value for value in values if value],
        }
    return setups


def _sheet_object_counts(root: ET.Element) -> dict[str, tuple[int, int]]:
    counts: dict[str, tuple[int, int]] = {}
    for description in root.findall(".//SheetDescription"):
        sheet_name = _child_value(description, "SheetName")
        if not sheet_name:
            continue
        objects = description.findall("SheetObject")
        formula_count = sum(len(obj.findall(".//Formula")) for obj in objects)
        counts[sheet_name] = (len(objects), formula_count)
    return counts


def _first_injection_name_rule(rules: list[ET.Element]) -> ET.Element | None:
    for rule in rules:
        if _child_value(rule, "Variable") == "injname":
            return rule
    return None


def _applies_to_injection(setup: dict[str, object], injection_name: str) -> tuple[str, str]:
    if setup.get("is_active") == "N":
        return "No", "Sheet setup is inactive"
    if not injection_name:
        return "", "No injection selected"
    if setup.get("each_injection") == "Y":
        return "Yes", "EachInjection=Y"
    values = [str(value) for value in setup.get("values", [])]
    comparison = str(setup.get("comparison", ""))
    if not values:
        return "", "No injection-name query rule"
    if comparison == "Contains":
        matched = any(value.lower() in injection_name.lower() for value in values)
        return ("Yes" if matched else "No"), f"Injection name contains one of: {', '.join(values)}"
    if comparison == "Equal":
        matched = any(value.lower() == injection_name.lower() for value in values)
        return ("Yes" if matched else "No"), f"Injection name equals one of: {', '.join(values)}"
    return "", f"Unsupported comparison: {comparison}"


def _child_value(node: ET.Element | None, path: str) -> str:
    if node is None:
        return ""
    child = node.find(path)
    if child is None:
        return ""
    return child.attrib.get("value", "").strip()


def _tsv_row(values: list[str]) -> str:
    return "\t".join(str(value).replace("\t", " ").replace("\r", " ").replace("\n", " ").strip() for value in values)


def _excel_range(left: str, top: str, right: str, bottom: str) -> str:
    if not all([left, top, right, bottom]):
        return ""
    try:
        left_i = int(left)
        top_i = int(top)
        right_i = int(right)
        bottom_i = int(bottom)
    except ValueError:
        return ""
    start = f"{_excel_column(left_i + 1)}{top_i + 1}"
    end = f"{_excel_column(right_i + 1)}{bottom_i + 1}"
    return start if start == end else f"{start}:{end}"


def _excel_column(index: int) -> str:
    letters = []
    while index > 0:
        index, remainder = divmod(index - 1, 26)
        letters.append(chr(65 + remainder))
    return "".join(reversed(letters))


def _safe_temp_name(value: str) -> str:
    return "".join(ch if ch.isalnum() or ch in "._-" else "_" for ch in value).strip("._") or "report"
