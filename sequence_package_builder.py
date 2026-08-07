from __future__ import annotations

import zipfile
import xml.etree.ElementTree as ET
import uuid
from copy import deepcopy
from dataclasses import dataclass, field
from pathlib import Path

from cmbx_container import (
    CmbxElement,
    extract_cmbx_entry,
    load_cmbx_package,
    read_cmbx_header_xml,
)
from embedded_method_extractor import _extract_method_payload, extract_embedded_instrument_method
from embedded_report_extractor import extract_embedded_report_template
from sequence_cmd_parser import build_injection_method_links, get_injection_method_link
from tools.repack_standalone_instmeth_cmbx import (
    _field_bytes,
    _parse_fields,
    _replace_method_payload_cpxm,
)


@dataclass(frozen=True)
class SequencePackageRequest:
    carrier_cmbx: Path
    method_cmbx: Path
    report_cmbx: Path
    output_cmbx: Path
    sequence_name: str
    injection_name: str
    method_name: str = ""
    report_name: str = ""


@dataclass(frozen=True)
class SequencePackageValidation:
    path: Path
    sequence_name: str
    injection_name: str
    instrument_method: str
    processing_method: str
    report_template: str
    method_payload_matches: bool
    report_payload_matches: bool
    hidden_object_names: tuple[str, ...] = ()
    errors: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()

    @property
    def passed(self) -> bool:
        return not self.errors and self.method_payload_matches and self.report_payload_matches


@dataclass(frozen=True)
class SequenceInjectionRequest:
    injection_name: str
    method_cmbx: Path
    method_name: str = ""


@dataclass(frozen=True)
class MultiSequencePackageRequest:
    carrier_cmbx: Path
    report_cmbx: Path
    output_cmbx: Path
    sequence_name: str
    injections: tuple[SequenceInjectionRequest, ...]
    report_name: str = ""
    include_processing_methods: bool = False


@dataclass(frozen=True)
class MultiSequencePackageValidation:
    path: Path
    sequence_name: str
    injection_names: tuple[str, ...]
    instrument_methods: tuple[str, ...]
    report_template: str
    processing_methods: tuple[str, ...]
    method_payload_matches: tuple[bool, ...]
    report_payload_matches: bool
    hidden_object_names: tuple[str, ...] = ()
    errors: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()

    @property
    def passed(self) -> bool:
        return not self.errors and all(self.method_payload_matches) and self.report_payload_matches


@dataclass
class _BuildContext:
    carrier_sequence: CmbxElement
    carrier_injection: CmbxElement
    carrier_method: CmbxElement
    carrier_report: CmbxElement
    processing_methods: list[CmbxElement] = field(default_factory=list)


def build_sequence_package(request: SequencePackageRequest) -> SequencePackageValidation:
    """Build a one-injection sequence by replacing assets in a CM-exported carrier.

    The carrier owns the Chromeleon DataContract graph and injection bindings. The
    standalone Method/Report CMBX files only supply their verified CpXm bodies.
    """
    carrier = load_cmbx_package(request.carrier_cmbx)
    context = _validate_carrier(carrier)
    method_package = load_cmbx_package(request.method_cmbx)
    report_package = load_cmbx_package(request.report_cmbx)
    source_method, method_cpxm = _standalone_method_cpxm(method_package)
    source_report, report_cpxm = _standalone_report_cpxm(report_package)

    method_name = _clean_name(request.method_name or source_method.name, "Generated Method")
    report_name = _clean_name(request.report_name or source_report.name, "Generated Report")
    sequence_name = _clean_name(request.sequence_name, "Generated Sequence")
    injection_name = _clean_name(request.injection_name, "Injection 1")

    command = extract_cmbx_entry(carrier.path, context.carrier_sequence.filename)
    command = _replace_asset_cpxm(
        command,
        context.carrier_method.name,
        method_cpxm,
        asset_kind="method",
    )
    command = _replace_asset_cpxm(
        command,
        context.carrier_report.name,
        report_cpxm,
        asset_kind="report",
    )
    command = _rename_object(command, context.carrier_method.name, method_name)
    command = _rename_object(command, context.carrier_report.name, report_name)
    command = _rename_object(command, context.carrier_injection.name, injection_name)
    command = _rename_sequence_object(command, sequence_name)

    header = _build_header(
        carrier.path,
        context,
        sequence_name=sequence_name,
        injection_name=injection_name,
        method_name=method_name,
        report_name=report_name,
        command_size=len(command),
    )
    output = request.output_cmbx
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("header.xml", header)
        archive.writestr(context.carrier_sequence.filename, command)

    return validate_sequence_package(output, method_cpxm, report_cpxm)


def build_multi_sequence_package(request: MultiSequencePackageRequest) -> MultiSequencePackageValidation:
    """Build a candidate multi-injection sequence from a controlled multi-slot carrier."""
    if not request.injections:
        raise ValueError("Add at least one Injection to the sequence.")
    carrier = load_cmbx_package(request.carrier_cmbx)
    prepared: list[tuple[int, SequenceInjectionRequest, str, str, bytes]] = []
    source_groups: dict[tuple[str, bytes], list[int]] = {}
    used_method_names: set[str] = set()
    group_method_names: dict[tuple[str, bytes], str] = {}
    for index, row in enumerate(request.injections):
        source_method, method_cpxm = _standalone_method_cpxm(load_cmbx_package(row.method_cmbx))
        base_method_name = _clean_name(row.method_name or source_method.name, f"Generated Method {index + 1}")
        source_key = (base_method_name.casefold(), method_cpxm)
        if source_key not in group_method_names:
            group_method_names[source_key] = _unique_name(base_method_name, used_method_names)
        method_name = group_method_names[source_key]
        injection_name = _clean_name(row.injection_name, f"Injection {index + 1}")
        prepared.append((index, row, injection_name, method_name, method_cpxm))
        source_groups.setdefault(source_key, []).append(index)

    required_group_sizes = tuple(len(items) for items in source_groups.values())
    sequence = _multi_carrier_sequence(
        carrier,
        required_injection_count=len(prepared),
    )
    reports = [item for item in sequence.children if item.kind == "report_template"]
    if not reports:
        raise ValueError("Sequence carrier does not expose a Report Template slot.")
    carrier_report = reports[0]
    source_report, report_cpxm = _standalone_report_cpxm(load_cmbx_package(request.report_cmbx))
    report_name = _clean_name(request.report_name or source_report.name, "Generated Report")
    sequence_name = _clean_name(request.sequence_name, "Generated Sequence")

    command = extract_cmbx_entry(carrier.path, sequence.filename)
    command, method_slots = _expand_multi_carrier_method_slots(
        command,
        sequence,
        required_method_count=len(source_groups),
    )
    allocated = _allocate_multi_carrier_bindings(
        carrier,
        sequence,
        required_group_sizes,
        method_slots,
    )

    selected_by_index: dict[
        int,
        tuple[CmbxElement, CmbxElement, CmbxElement, CmbxElement | None, str, str, bytes],
    ] = {}
    for (source_key, source_indexes), (carrier_method, carrier_rows) in zip(source_groups.items(), allocated):
        for source_index, (carrier_injection, source_carrier_method, carrier_processing) in zip(
            source_indexes, carrier_rows
        ):
            _index, _row, injection_name, method_name, method_cpxm = prepared[source_index]
            selected_by_index[source_index] = (
                carrier_injection,
                source_carrier_method,
                carrier_method,
                carrier_processing,
                injection_name,
                method_name,
                method_cpxm,
            )
    selected = [selected_by_index[index] for index in range(len(prepared))]

    native_injections = [item for item in sequence.children if item.kind == "injection"]
    selected_injection_ids = {item[0].id for item in selected}
    native_injection_names = [item.name for item in native_injections]
    needs_ordinal_selection = bool(native_injection_names) and all(
        not name for name in native_injection_names
    )
    command = _prune_multi_carrier_command(
        command,
        injection_names={item[0].name for item in selected},
        injection_ordinals=(
            {
                index for index, injection in enumerate(native_injections)
                if injection.id in selected_injection_ids
            }
            if needs_ordinal_selection
            else None
        ),
        method_names={item[2].name for item in selected},
        processing_names={item[3].name for item in selected if item[3] is not None} if request.include_processing_methods else set(),
        report_name=carrier_report.name,
    )
    for (
        carrier_injection,
        source_carrier_method,
        carrier_method,
        carrier_processing,
        injection_name,
        method_name,
        method_cpxm,
    ) in selected:
        command = _rewrite_injection_object(
            command,
            carrier_injection_name=carrier_injection.name,
            carrier_method_name=source_carrier_method.name,
            target_carrier_method_name=carrier_method.name,
            injection_name=injection_name,
            remove_processing_name=(
                carrier_processing.name
                if not request.include_processing_methods and carrier_processing is not None
                else ""
            ),
        )

    replaced_methods: set[str] = set()
    for (
        _carrier_injection,
        _source_carrier_method,
        carrier_method,
        _carrier_processing,
        _injection_name,
        method_name,
        method_cpxm,
    ) in selected:
        if carrier_method.id not in replaced_methods:
            command = _replace_asset_cpxm(command, carrier_method.name, method_cpxm, asset_kind="method")
            command = _rename_object(command, carrier_method.name, method_name)
            replaced_methods.add(carrier_method.id)

    command = _replace_asset_cpxm(command, carrier_report.name, report_cpxm, asset_kind="report")
    command = _rename_object(command, carrier_report.name, report_name)
    command = _rename_sequence_object(command, sequence_name)
    header = _build_multi_header(
        carrier.path,
        sequence,
        selected,
        carrier_report,
        sequence_name=sequence_name,
        report_name=report_name,
        command_size=len(command),
        include_processing_methods=request.include_processing_methods,
    )
    request.output_cmbx.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(request.output_cmbx, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("header.xml", header)
        archive.writestr(sequence.filename, command)
    return validate_multi_sequence_package(
        request.output_cmbx,
        len(selected),
        tuple(item[6] for index, item in enumerate(selected) if item[2].id not in {prior[2].id for prior in selected[:index]}),
        report_cpxm,
        expect_processing=request.include_processing_methods,
    )


def validate_multi_sequence_package(
    path: str | Path,
    expected_injection_count: int,
    expected_method_cpxm: tuple[bytes, ...],
    expected_report_cpxm: bytes,
    *,
    expect_processing: bool,
) -> MultiSequencePackageValidation:
    package = load_cmbx_package(path)
    errors: list[str] = []
    warnings: list[str] = []
    methods = [item for item in package.methods_and_reports if item.kind == "instrument_method"]
    reports = [item for item in package.methods_and_reports if item.kind == "report_template"]
    processing = [item for item in package.methods_and_reports if item.kind == "processing_method"]
    if len(package.sequences) != 1:
        errors.append(f"Expected one sequence, found {len(package.sequences)}.")
    if len(package.injections) != expected_injection_count:
        errors.append(f"Expected {expected_injection_count} injections, found {len(package.injections)}.")
    if len(methods) != len(expected_method_cpxm):
        errors.append(f"Expected {len(expected_method_cpxm)} instrument methods, found {len(methods)}.")
    if len(reports) != 1:
        errors.append(f"Expected one report template, found {len(reports)}.")
    if not expect_processing and processing:
        errors.append("Processing Method objects remain visible although blank bindings were requested.")

    if package.sequences and package.sequences[0].filename:
        command = extract_cmbx_entry(package.path, package.sequences[0].filename)
        try:
            inventory = _contract_object_inventory(command)
        except ValueError as exc:
            inventory = ()
            errors.append(str(exc))
        expected_counts = {
            "sequence": 1,
            "injection": expected_injection_count,
            "instrument_method": len(expected_method_cpxm),
            "processing_method": len(processing) if expect_processing else 0,
            "report_template": 1,
            "signal": 0,
            "chromatogram": 0,
            "audit": 0,
        }
        for kind, expected_count in expected_counts.items():
            actual_count = sum(item_kind == kind for item_kind, _name in inventory)
            if actual_count != expected_count:
                errors.append(
                    f"Sequence DataContract contains {actual_count} {kind} object(s); expected {expected_count}."
                )

    actual_method_payloads: list[bytes] = []
    for method in methods:
        embedded = extract_embedded_instrument_method(package, method)
        actual_method_payloads.append(embedded.cpxm_payload if embedded else b"")
    method_matches = tuple(
        index < len(actual_method_payloads) and actual_method_payloads[index] == expected
        for index, expected in enumerate(expected_method_cpxm)
    )
    report_payload = b""
    if reports:
        embedded_report = extract_embedded_report_template(package, reports[0])
        report_payload = embedded_report.cpxm_payload if embedded_report else b""
    report_match = report_payload == expected_report_cpxm
    if not all(method_matches):
        errors.append("One or more Instrument Method CpXm payloads differ from their standalone sources.")
    if not report_match:
        errors.append("Report Template CpXm differs from its standalone source.")

    links = build_injection_method_links(package)
    method_names = {item.name for item in methods}
    for injection in package.injections:
        link = get_injection_method_link(links, injection)
        if link is None or link.instrument_method not in method_names:
            errors.append(f"Injection '{injection.name}' does not resolve to a packaged Instrument Method.")

    hidden_names = _hidden_object_names(package)
    visible = {
        *(item.name for item in package.sequences),
        *(item.name for item in package.injections),
        *(item.name for item in package.methods_and_reports),
    }
    hidden = tuple(name for name in hidden_names if name and name not in visible)
    if hidden:
        warnings.append(f"Carrier command retains {len(hidden)} hidden object name(s).")
    if not expect_processing:
        warnings.append("Processing Method bindings are intentionally blank; no IRC or integration action is packaged.")
    return MultiSequencePackageValidation(
        path=Path(path),
        sequence_name=package.sequences[0].name if package.sequences else "",
        injection_names=tuple(item.name for item in package.injections),
        instrument_methods=tuple(item.name for item in methods),
        report_template=reports[0].name if reports else "",
        processing_methods=tuple(item.name for item in processing),
        method_payload_matches=method_matches,
        report_payload_matches=report_match,
        hidden_object_names=hidden,
        errors=tuple(errors),
        warnings=tuple(warnings),
    )


def validate_sequence_package(
    path: str | Path,
    expected_method_cpxm: bytes | None = None,
    expected_report_cpxm: bytes | None = None,
) -> SequencePackageValidation:
    output = Path(path)
    package = load_cmbx_package(output)
    errors: list[str] = []
    warnings: list[str] = []
    if len(package.sequences) != 1:
        errors.append(f"Expected one sequence, found {len(package.sequences)}.")
    if len(package.injections) != 1:
        errors.append(f"Expected one injection, found {len(package.injections)}.")
    methods = [item for item in package.methods_and_reports if item.kind == "instrument_method"]
    reports = [item for item in package.methods_and_reports if item.kind == "report_template"]
    processing = [item for item in package.methods_and_reports if item.kind == "processing_method"]
    if len(methods) != 1:
        errors.append(f"Expected one instrument method, found {len(methods)}.")
    if len(reports) != 1:
        errors.append(f"Expected one report template, found {len(reports)}.")

    method_cpxm = b""
    if methods:
        embedded = extract_embedded_instrument_method(package, methods[0])
        if embedded is None:
            errors.append("Generated instrument method payload could not be decoded from the sequence.")
        else:
            method_cpxm = embedded.cpxm_payload
    report_cpxm = b""
    if reports:
        embedded_report = extract_embedded_report_template(package, reports[0])
        if embedded_report is None:
            errors.append("Generated report payload could not be decoded from the sequence.")
        else:
            report_cpxm = embedded_report.cpxm_payload

    instrument_method = methods[0].name if methods else ""
    processing_method = processing[0].name if processing else ""
    injection_name = package.injections[0].name if package.injections else ""
    if package.injections:
        link = get_injection_method_link(build_injection_method_links(package), package.injections[0])
        if link is None:
            errors.append("Injection method binding could not be read from the generated sequence.")
        else:
            processing_method = link.processing_method
            if instrument_method and link.instrument_method != instrument_method:
                errors.append(
                    f"Injection links to '{link.instrument_method}', but the packaged method is '{instrument_method}'."
                )

    hidden_names = _hidden_object_names(package)
    visible = {
        *(item.name for item in package.sequences),
        *(item.name for item in package.injections),
        *(item.name for item in package.methods_and_reports),
    }
    hidden = tuple(name for name in hidden_names if name and name not in visible)
    if hidden:
        warnings.append(
            f"Carrier command retains {len(hidden)} hidden object name(s). Use a CM-exported minimal carrier before runtime approval."
        )
    if processing_method:
        warnings.append(
            f"Processing Method '{processing_method}' is preserved from the sequence carrier; "
            "its IRC/integration behavior has not been synthesized from the standalone assets."
        )

    method_match = expected_method_cpxm is None or method_cpxm == expected_method_cpxm
    report_match = expected_report_cpxm is None or report_cpxm == expected_report_cpxm
    if not method_match:
        errors.append("Instrument Method CpXm differs from the standalone source.")
    if not report_match:
        errors.append("Report Template CpXm differs from the standalone source.")
    return SequencePackageValidation(
        path=output,
        sequence_name=package.sequences[0].name if package.sequences else "",
        injection_name=injection_name,
        instrument_method=instrument_method,
        processing_method=processing_method,
        report_template=reports[0].name if reports else "",
        method_payload_matches=method_match,
        report_payload_matches=report_match,
        hidden_object_names=hidden,
        errors=tuple(errors),
        warnings=tuple(warnings),
    )


def sequence_package_validation_text(validation: SequencePackageValidation) -> str:
    return "\n".join(
        [
            f"Passed: {validation.passed}",
            f"Path: {validation.path}",
            f"Sequence: {validation.sequence_name}",
            f"Injection: {validation.injection_name}",
            f"Instrument Method: {validation.instrument_method}",
            f"Processing Method: {validation.processing_method or '(none)'}",
            f"Report Template: {validation.report_template}",
            f"Method Payload Match: {validation.method_payload_matches}",
            f"Report Payload Match: {validation.report_payload_matches}",
            f"Hidden Carrier Objects: {len(validation.hidden_object_names)}",
            *(f"WARNING: {item}" for item in validation.warnings),
            *(f"ERROR: {item}" for item in validation.errors),
        ]
    )


def _validate_carrier(package) -> _BuildContext:
    if len(package.sequences) != 1:
        raise ValueError(f"Sequence carrier must expose exactly one sequence; found {len(package.sequences)}.")
    sequence = package.sequences[0]
    injections = [item for item in sequence.children if item.kind == "injection"]
    methods = [item for item in sequence.children if item.kind == "instrument_method"]
    reports = [item for item in sequence.children if item.kind == "report_template"]
    processing = [item for item in sequence.children if item.kind == "processing_method"]
    if len(injections) != 1:
        raise ValueError(f"Sequence carrier must expose exactly one injection; found {len(injections)}.")
    if len(methods) != 1:
        raise ValueError(f"Sequence carrier must expose exactly one instrument method; found {len(methods)}.")
    if len(reports) != 1:
        raise ValueError(f"Sequence carrier must expose exactly one report template; found {len(reports)}.")
    if not sequence.filename:
        raise ValueError("Sequence carrier does not reference a sequence command entry.")
    return _BuildContext(sequence, injections[0], methods[0], reports[0], processing)


def _multi_carrier_sequence(
    package,
    *,
    required_injection_count: int,
) -> CmbxElement:
    candidates = []
    for sequence in package.sequences:
        groups = _multi_carrier_binding_groups(package, sequence)
        reports = [item for item in sequence.children if item.kind == "report_template"]
        if (
            groups
            and sum(len(rows) for _method, rows in groups) >= required_injection_count
            and reports
            and sequence.filename
        ):
            candidates.append((sum(len(rows) for _method, rows in groups), sequence))
    if not candidates:
        raise ValueError(
            "No sequence in the carrier exposes at least "
            f"{required_injection_count} Injection row(s), one Instrument Method template, "
            "and one Report Template."
        )
    return min(candidates, key=lambda item: item[0])[1]


def _multi_carrier_slots(package, sequence: CmbxElement) -> list[tuple[CmbxElement, CmbxElement, CmbxElement | None]]:
    methods = {item.name: item for item in sequence.children if item.kind == "instrument_method"}
    processing = {item.name: item for item in sequence.children if item.kind == "processing_method"}
    links = build_injection_method_links(package)
    result: list[tuple[CmbxElement, CmbxElement, CmbxElement | None]] = []
    used_methods: set[str] = set()
    for injection in (item for item in sequence.children if item.kind == "injection"):
        link = get_injection_method_link(links, injection)
        if link is None or link.instrument_method not in methods or link.instrument_method in used_methods:
            continue
        used_methods.add(link.instrument_method)
        result.append((injection, methods[link.instrument_method], processing.get(link.processing_method)))
    return result


def _multi_carrier_binding_groups(
    package,
    sequence: CmbxElement,
) -> list[tuple[CmbxElement, list[tuple[CmbxElement, CmbxElement | None]]]]:
    """Return each Method object with every native Injection row that references it."""
    methods = {item.name: item for item in sequence.children if item.kind == "instrument_method"}
    processing = {item.name: item for item in sequence.children if item.kind == "processing_method"}
    links = build_injection_method_links(package)
    grouped: dict[str, list[tuple[CmbxElement, CmbxElement | None]]] = {}
    for injection in (item for item in sequence.children if item.kind == "injection"):
        link = get_injection_method_link(links, injection)
        if link is None or link.instrument_method not in methods:
            continue
        grouped.setdefault(link.instrument_method, []).append(
            (injection, processing.get(link.processing_method))
        )
    if grouped:
        return [(methods[name], rows) for name, rows in grouped.items()]

    # Clean CM templates may legitimately have blank Injection names. The legacy
    # link parser searches by name and cannot resolve those rows, so align the
    # native Injection object order with header.xml and read RelativeUrl bindings
    # directly from each object payload.
    command = extract_cmbx_entry(package.path, sequence.filename)
    fields = _parse_fields(command)
    type_fields = [item for item in fields if item.number == 18 and item.wire_type == 2]
    object_fields = [item for item in fields if item.number == 19 and item.wire_type == 2]
    injection_payloads = [
        command[object_field.value_start : object_field.value_end]
        for type_field, object_field in zip(type_fields, object_fields)
        if _contract_object_type(command[type_field.value_start : type_field.value_end]) == "injection"
    ]
    injection_elements = [item for item in sequence.children if item.kind == "injection"]
    for injection, payload in zip(injection_elements, injection_payloads):
        method_name = next(
            (name for name in sorted(methods, key=len, reverse=True) if _relative_url_target(payload, name)),
            "",
        )
        if not method_name:
            continue
        processing_name = next(
            (name for name in sorted(processing, key=len, reverse=True) if _relative_url_target(payload, name)),
            "",
        )
        grouped.setdefault(method_name, []).append((injection, processing.get(processing_name)))
    return [(methods[name], rows) for name, rows in grouped.items()]


def _relative_url_target(payload: bytes, name: str) -> bool:
    encoded = name.encode("utf-8")
    return encoded in payload and b"RelativeUrl" in payload


def _expand_multi_carrier_method_slots(
    command: bytes,
    sequence: CmbxElement,
    *,
    required_method_count: int,
) -> tuple[bytes, list[CmbxElement]]:
    """Clone complete Instrument Method contract triplets when more slots are needed.

    Chromeleon stores each business object in three parallel DataContract arrays:
    type descriptor (field 18), object body (field 19), and metadata (field 20).
    A usable Method slot therefore cannot be created by copying only CpXm or a
    header node. Each clone receives fresh object/type identities and a matching
    header entry; its CpXm and visible name are replaced later by the normal
    sequence build pipeline.
    """
    native_methods = [item for item in sequence.children if item.kind == "instrument_method"]
    if not native_methods:
        raise ValueError("Sequence carrier has no Instrument Method template to clone.")
    if required_method_count <= len(native_methods):
        return command, native_methods[:required_method_count]

    fields = _parse_fields(command)
    type_fields = [item for item in fields if item.number == 18 and item.wire_type == 2]
    object_fields = [item for item in fields if item.number == 19 and item.wire_type == 2]
    metadata_fields = [item for item in fields if item.number == 20 and item.wire_type == 2]
    if not (len(type_fields) == len(object_fields) == len(metadata_fields)):
        raise ValueError(
            "Sequence carrier DataContract arrays are not parallel while expanding Method slots."
        )

    method_triplets: list[tuple[bytes, bytes, bytes, CmbxElement]] = []
    methods_by_name = {item.name: item for item in native_methods}
    for type_field, object_field, metadata_field in zip(type_fields, object_fields, metadata_fields):
        type_payload = command[type_field.value_start : type_field.value_end]
        if _contract_object_type(type_payload) != "instrument_method":
            continue
        object_payload = command[object_field.value_start : object_field.value_end]
        name = _field_text(object_payload, _parse_fields(object_payload), 28)
        method = methods_by_name.get(name)
        if method is None:
            continue
        metadata_payload = command[metadata_field.value_start : metadata_field.value_end]
        method_triplets.append((type_payload, object_payload, metadata_payload, method))
    if not method_triplets:
        raise ValueError("Sequence carrier Instrument Method contract triplet was not found.")

    numeric_ids = [int(item.id) for item in sequence.children if str(item.id).isdigit()]
    next_header_id = max(numeric_ids, default=0) + 1
    clone_types: list[bytes] = []
    clone_objects: list[bytes] = []
    clone_metadata: list[bytes] = []
    slots = list(native_methods)
    for slot_index in range(len(native_methods), required_method_count):
        type_payload, object_payload, metadata_payload, template = method_triplets[
            (slot_index - len(native_methods)) % len(method_triplets)
        ]
        slot_name = f"__CMBX_METHOD_SLOT_{slot_index + 1:02d}__"
        own_identity = _new_contract_identity()
        type_payload = _replace_contract_length_fields(
            type_payload,
            {
                5: own_identity,
                7: _new_contract_identity(),
                10: _new_contract_identity(),
            },
        )
        object_payload = _replace_contract_length_fields(
            object_payload,
            {
                25: own_identity,
                28: slot_name.encode("utf-8"),
                29: _new_contract_identity(),
            },
        )
        clone_types.append(type_payload)
        clone_objects.append(object_payload)
        clone_metadata.append(metadata_payload)
        slots.append(
            CmbxElement(
                id=str(next_header_id),
                name=slot_name,
                item_type=template.item_type,
                url=template.url,
                raw_data_file_id=template.id,
                parent_id=sequence.id,
            )
        )
        next_header_id += 1

    return (
        _append_contract_triplets(command, clone_types, clone_objects, clone_metadata),
        slots,
    )


def _new_contract_identity() -> bytes:
    raw = uuid.uuid4().bytes_le
    return b"\x09" + raw[:8] + b"\x11" + raw[8:]


def _replace_contract_length_fields(data: bytes, replacements: dict[int, bytes]) -> bytes:
    rebuilt = bytearray()
    replaced: set[int] = set()
    for field in _parse_fields(data):
        value = replacements.get(field.number)
        if field.wire_type == 2 and value is not None and field.number not in replaced:
            rebuilt.extend(_field_bytes(field.number, 2, value))
            replaced.add(field.number)
        else:
            rebuilt.extend(field.raw)
    missing = set(replacements) - replaced
    if missing:
        raise ValueError(f"Method contract clone is missing field(s): {sorted(missing)}.")
    return bytes(rebuilt)


def _append_contract_triplets(
    command: bytes,
    type_payloads: list[bytes],
    object_payloads: list[bytes],
    metadata_payloads: list[bytes],
) -> bytes:
    if not (len(type_payloads) == len(object_payloads) == len(metadata_payloads)):
        raise ValueError("Cloned Method contract arrays are not parallel.")
    fields = _parse_fields(command)
    last = {
        number: max(
            index
            for index, item in enumerate(fields)
            if item.number == number and item.wire_type == 2
        )
        for number in (18, 19, 20)
    }
    payloads = {18: type_payloads, 19: object_payloads, 20: metadata_payloads}
    rebuilt = bytearray()
    for index, field in enumerate(fields):
        rebuilt.extend(field.raw)
        if index == last.get(field.number):
            for payload in payloads[field.number]:
                rebuilt.extend(_field_bytes(field.number, 2, payload))
    return bytes(rebuilt)


def _allocate_multi_carrier_bindings(
    package,
    sequence: CmbxElement,
    required_group_sizes: tuple[int, ...],
    method_slots: list[CmbxElement],
) -> list[
    tuple[CmbxElement, list[tuple[CmbxElement, CmbxElement, CmbxElement | None]]]
]:
    """Allocate native rows independently from their original Method bindings."""
    available = _multi_carrier_binding_groups(package, sequence)
    if len(method_slots) < len(required_group_sizes):
        raise ValueError(
            f"Sequence carrier exposes {len(method_slots)} expandable Method slot(s); "
            f"{len(required_group_sizes)} distinct Method payload(s) were requested."
        )
    binding_by_injection_id = {
        injection.id: (method, processing)
        for method, rows in available
        for injection, processing in rows
    }
    ordered_rows = [
        (injection, *binding_by_injection_id[injection.id])
        for injection in sequence.children
        if injection.kind == "injection" and injection.id in binding_by_injection_id
    ]
    if len(ordered_rows) < sum(required_group_sizes):
        raise ValueError(
            f"Sequence carrier exposes {len(ordered_rows)} Injection row(s); "
            f"{sum(required_group_sizes)} were requested."
        )
    allocated: list[
        tuple[CmbxElement, list[tuple[CmbxElement, CmbxElement, CmbxElement | None]]]
    ] = []
    cursor = 0
    for target_method, required in zip(method_slots, required_group_sizes):
        allocated.append((target_method, ordered_rows[cursor : cursor + required]))
        cursor += required
    return allocated


def _build_multi_header(
    carrier_path: Path,
    sequence: CmbxElement,
    selected: list[
        tuple[
            CmbxElement,
            CmbxElement,
            CmbxElement,
            CmbxElement | None,
            str,
            str,
            bytes,
        ]
    ],
    report: CmbxElement,
    *,
    sequence_name: str,
    report_name: str,
    command_size: int,
    include_processing_methods: bool,
) -> bytes:
    source_root = ET.fromstring(read_cmbx_header_xml(carrier_path))
    source_nodes = {node.attrib.get("Id", ""): node for node in source_root.iter("ChromeleonElement")}
    sequence_node = deepcopy(source_nodes[sequence.id])
    keep_ids = {report.id}
    names: dict[str, str] = {report.id: report_name}
    for injection, _source_method, method, processing, injection_name, method_name, _payload in selected:
        keep_ids.update((injection.id, method.id))
        names[injection.id] = injection_name
        names[method.id] = method_name
        if include_processing_methods and processing is not None:
            keep_ids.add(processing.id)
    for child in list(sequence_node):
        child_id = child.attrib.get("Id", "")
        kind = _kind_from_item_type(child.attrib.get("ItemType", ""))
        if kind in {"injection", "instrument_method", "processing_method", "report_template"} and child_id not in keep_ids:
            sequence_node.remove(child)
            continue
        if child_id in names:
            new_name = names[child_id]
            child.set("Name", new_name)
            if kind == "instrument_method":
                _rename_header_node(child, new_name, ".instmeth")
            elif kind == "report_template":
                _rename_header_node(child, new_name, ".report")
        if kind == "injection" and child_id in keep_ids:
            for grandchild in list(child):
                grandchild_kind = _kind_from_item_type(grandchild.attrib.get("ItemType", ""))
                if grandchild_kind in {"signal", "audit"}:
                    child.remove(grandchild)
    appended_method_ids: set[str] = set()
    for _injection, _source_method, method, _processing, _injection_name, method_name, _payload in selected:
        if method.id in source_nodes or method.id in appended_method_ids:
            continue
        template_id = method.raw_data_file_id
        template_node = source_nodes.get(template_id)
        if template_node is None:
            raise ValueError(
                f"Cloned Instrument Method slot '{method.id}' has no header template '{template_id}'."
            )
        clone_node = deepcopy(template_node)
        clone_node.set("Id", method.id)
        _rename_header_node(clone_node, method_name, ".instmeth")
        sequence_node.append(clone_node)
        appended_method_ids.add(method.id)
    sequence_node.set("Name", sequence_name)
    sequence_node.set("Size", str(command_size))
    _rename_sequence_header_urls(sequence_node, sequence_name)
    root = ET.Element(source_root.tag, source_root.attrib)
    root.append(sequence_node)
    return b'<?xml version="1.0" encoding="UTF-8"?>' + ET.tostring(root, encoding="utf-8")


def _rewrite_injection_object(
    command: bytes,
    *,
    carrier_injection_name: str,
    carrier_method_name: str,
    target_carrier_method_name: str,
    injection_name: str,
    remove_processing_name: str,
) -> bytes:
    """Rewrite exactly one Injection object selected by its native Method binding.

    Injection names are not unique in real Chromeleon sequences. A global string
    replacement therefore corrupts repeated Injection rows. The Method binding is
    used as the discriminator, and repeated rows are consumed one at a time.
    """
    fields = _parse_fields(command)
    type_fields = [item for item in fields if item.number == 18 and item.wire_type == 2]
    object_fields = [item for item in fields if item.number == 19 and item.wire_type == 2]
    if len(type_fields) != len(object_fields):
        raise ValueError("Sequence DataContract type/object arrays are not parallel while rewriting Injection.")

    target_index = -1
    for index, (type_field, object_field) in enumerate(zip(type_fields, object_fields)):
        type_payload = command[type_field.value_start : type_field.value_end]
        if _contract_object_type(type_payload) != "injection":
            continue
        payload = command[object_field.value_start : object_field.value_end]
        try:
            name = _field_text(payload, _parse_fields(payload), 28)
        except ValueError:
            continue
        if name != carrier_injection_name or carrier_method_name.encode("utf-8") not in payload:
            continue
        target_index = index
        break
    if target_index < 0:
        raise ValueError(
            f"Could not resolve Injection '{carrier_injection_name}' bound to Method '{carrier_method_name}'."
        )

    target_payload = command[
        object_fields[target_index].value_start : object_fields[target_index].value_end
    ]
    if target_carrier_method_name != carrier_method_name:
        target_payload, rebound = _rewrite_exact_strings(
            target_payload,
            {
                carrier_method_name.encode("utf-8"): target_carrier_method_name.encode("utf-8")
            },
        )
        if rebound == 0:
            raise ValueError(
                f"Could not rebind Injection '{carrier_injection_name}' from Method "
                f"'{carrier_method_name}' to '{target_carrier_method_name}'."
            )
    if remove_processing_name:
        target_payload, removed = _strip_relative_url_reference(
            target_payload,
            remove_processing_name.encode("utf-8"),
        )
        if removed == 0:
            raise ValueError(
                f"Could not remove Processing Method reference '{remove_processing_name}' "
                f"from Injection '{carrier_injection_name}'."
            )
    nested_rebuilt = bytearray()
    renamed = False
    for item in _parse_fields(target_payload):
        if item.number == 28 and item.wire_type == 2 and not renamed:
            nested_rebuilt.extend(_field_bytes(28, 2, injection_name.encode("utf-8")))
            renamed = True
        else:
            nested_rebuilt.extend(item.raw)
    if not renamed:
        raise ValueError(f"Injection '{carrier_injection_name}' has no writable Name field.")

    rebuilt = bytearray()
    object_index = 0
    for item in fields:
        if item.number == 19 and item.wire_type == 2:
            if object_index == target_index:
                rebuilt.extend(_field_bytes(19, 2, bytes(nested_rebuilt)))
            else:
                rebuilt.extend(item.raw)
            object_index += 1
        else:
            rebuilt.extend(item.raw)
    return bytes(rebuilt)


def _remove_injection_reference(command: bytes, injection_name: str, reference_name: str) -> bytes:
    rebuilt = bytearray()
    changed = False
    for field in _parse_fields(command):
        if field.number != 19 or field.wire_type != 2:
            rebuilt.extend(field.raw)
            continue
        nested = command[field.value_start : field.value_end]
        try:
            name = _field_text(nested, _parse_fields(nested), 28)
        except ValueError:
            name = ""
        if name != injection_name:
            rebuilt.extend(field.raw)
            continue
        rewritten, count = _strip_relative_url_reference(nested, reference_name.encode("utf-8"))
        rebuilt.extend(_field_bytes(19, 2, rewritten))
        changed = changed or count > 0
    if not changed:
        raise ValueError(f"Could not remove Processing Method reference '{reference_name}' from Injection '{injection_name}'.")
    return bytes(rebuilt)


def _strip_relative_url_reference(data: bytes, target: bytes, *, depth: int = 0) -> tuple[bytes, int]:
    if depth > 12 or target not in data:
        return data, 0
    try:
        fields = _parse_fields(data)
    except ValueError:
        return data, 0
    rebuilt = bytearray()
    changes = 0
    for field in fields:
        if field.wire_type != 2:
            rebuilt.extend(field.raw)
            continue
        value = data[field.value_start : field.value_end]
        nested, nested_changes = _strip_relative_url_reference(value, target, depth=depth + 1)
        if nested_changes:
            rebuilt.extend(_field_bytes(field.number, 2, nested))
            changes += nested_changes
        elif target in value and b"RelativeUrl" in value:
            changes += 1
        else:
            rebuilt.extend(field.raw)
    return bytes(rebuilt), changes


def _prune_multi_carrier_command(
    command: bytes,
    *,
    injection_names: set[str],
    injection_ordinals: set[int] | None = None,
    method_names: set[str],
    processing_names: set[str],
    report_name: str,
) -> bytes:
    """Remove unused carrier business objects from both DataContract arrays.

    Chromeleon serializes the command as parallel field-18 type descriptors,
    field-19 object values, and field-20 object metadata. Removing an object only
    from header.xml, or pruning only part of this triplet, produces a package our
    lightweight parser can reopen but Chromeleon cannot import.
    """
    fields = _parse_fields(command)
    type_fields = [item for item in fields if item.number == 18 and item.wire_type == 2]
    object_fields = [item for item in fields if item.number == 19 and item.wire_type == 2]
    metadata_fields = [item for item in fields if item.number == 20 and item.wire_type == 2]
    if not (len(type_fields) == len(object_fields) == len(metadata_fields)):
        raise ValueError(
            "Sequence carrier DataContract type/object/metadata arrays are not parallel: "
            f"{len(type_fields)} type descriptors, {len(object_fields)} objects, "
            f"{len(metadata_fields)} metadata records."
        )

    keep: list[bool] = []
    injection_ordinal = 0
    for type_field, object_field in zip(type_fields, object_fields):
        type_payload = command[type_field.value_start : type_field.value_end]
        object_payload = command[object_field.value_start : object_field.value_end]
        object_type = _contract_object_type(type_payload)
        try:
            object_name = _field_text(object_payload, _parse_fields(object_payload), 28)
        except ValueError:
            object_name = ""
        if object_type == "injection":
            retain = (
                injection_ordinal in injection_ordinals
                if injection_ordinals is not None
                else object_name in injection_names
            )
            injection_ordinal += 1
        elif object_type == "instrument_method":
            retain = object_name in method_names
        elif object_type == "processing_method":
            retain = object_name in processing_names
        elif object_type == "report_template":
            retain = object_name == report_name
        elif object_type in {"signal", "chromatogram", "audit"}:
            retain = False
        else:
            retain = True
        keep.append(retain)

    rebuilt = bytearray()
    type_index = 0
    object_index = 0
    metadata_index = 0
    for item in fields:
        if item.number == 18 and item.wire_type == 2:
            if keep[type_index]:
                rebuilt.extend(item.raw)
            type_index += 1
        elif item.number == 19 and item.wire_type == 2:
            if keep[object_index]:
                rebuilt.extend(item.raw)
            object_index += 1
        elif item.number == 20 and item.wire_type == 2:
            if keep[metadata_index]:
                rebuilt.extend(item.raw)
            metadata_index += 1
        else:
            rebuilt.extend(item.raw)
    return bytes(rebuilt)


def _contract_object_type(type_payload: bytes) -> str:
    markers = (
        (b"ProcessingMethod\"", "processing_method"),
        (b"InstrumentMethod\"", "instrument_method"),
        (b"ReportDefinition\"", "report_template"),
        (b"Injection\"", "injection"),
        (b"AuditTrail\"", "audit"),
        (b"Chromatogram\"", "chromatogram"),
        (b"Signal\"", "signal"),
        (b"Sequence\"", "sequence"),
    )
    for marker, kind in markers:
        if marker in type_payload:
            return kind
    return "other"


def _contract_object_inventory(command: bytes) -> tuple[tuple[str, str], ...]:
    fields = _parse_fields(command)
    type_fields = [item for item in fields if item.number == 18 and item.wire_type == 2]
    object_fields = [item for item in fields if item.number == 19 and item.wire_type == 2]
    metadata_fields = [item for item in fields if item.number == 20 and item.wire_type == 2]
    if not (len(type_fields) == len(object_fields) == len(metadata_fields)):
        raise ValueError(
            "Sequence DataContract type/object/metadata arrays are not parallel: "
            f"{len(type_fields)} type descriptors, {len(object_fields)} objects, "
            f"{len(metadata_fields)} metadata records."
        )
    result: list[tuple[str, str]] = []
    for type_field, object_field in zip(type_fields, object_fields):
        type_payload = command[type_field.value_start : type_field.value_end]
        object_payload = command[object_field.value_start : object_field.value_end]
        try:
            name = _field_text(object_payload, _parse_fields(object_payload), 28)
        except ValueError:
            name = ""
        result.append((_contract_object_type(type_payload), name))
    return tuple(result)


def _unique_name(base: str, used: set[str]) -> str:
    candidate = base
    suffix = 2
    while candidate.casefold() in used:
        candidate = f"{base}_{suffix}"
        suffix += 1
    used.add(candidate.casefold())
    return candidate


def _kind_from_item_type(item_type: str) -> str:
    return CmbxElement("", "", item_type).kind


def _standalone_method_cpxm(package) -> tuple[CmbxElement, bytes]:
    methods = [item for item in package.methods_and_reports if item.kind == "instrument_method"]
    if len(methods) != 1:
        raise ValueError(f"Method CMBX must contain exactly one instrument method; found {len(methods)}.")
    method = methods[0]
    data = extract_cmbx_entry(package.path, method.package_entry_name)
    payload = _extract_method_payload(data, 0)
    if payload is None:
        raise ValueError("Standalone method CpXm payload was not found.")
    return method, payload.cpxm_payload


def _standalone_report_cpxm(package) -> tuple[CmbxElement, bytes]:
    reports = [item for item in package.methods_and_reports if item.kind == "report_template"]
    if len(reports) != 1:
        raise ValueError(f"Report CMBX must contain exactly one report template; found {len(reports)}.")
    report = reports[0]
    embedded = extract_embedded_report_template(package, report)
    if embedded is None:
        raise ValueError("Standalone report CpXm payload was not found.")
    return report, embedded.cpxm_payload


def _replace_asset_cpxm(command: bytes, target_name: str, cpxm: bytes, *, asset_kind: str) -> bytes:
    rebuilt = bytearray()
    replaced = False
    for field in _parse_fields(command):
        if field.number != 19 or field.wire_type != 2:
            rebuilt.extend(field.raw)
            continue
        nested = command[field.value_start : field.value_end]
        fields = _parse_fields(nested)
        name = _field_text(nested, fields, 28)
        if name != target_name:
            rebuilt.extend(field.raw)
            continue
        nested_rebuilt = bytearray()
        for item in fields:
            if asset_kind == "method" and item.number == 11 and item.wire_type == 2:
                value = nested[item.value_start : item.value_end]
                nested_rebuilt.extend(_field_bytes(11, 2, _replace_method_payload_cpxm(value, cpxm)))
                replaced = True
            elif asset_kind == "report" and item.number == 15 and item.wire_type == 2:
                nested_rebuilt.extend(_field_bytes(15, 2, _field_bytes(1, 2, cpxm)))
                replaced = True
            else:
                nested_rebuilt.extend(item.raw)
        rebuilt.extend(_field_bytes(19, 2, bytes(nested_rebuilt)))
    if not replaced:
        raise ValueError(f"Could not replace {asset_kind} payload for carrier object '{target_name}'.")
    return bytes(rebuilt)


def _rename_object(command: bytes, old_name: str, new_name: str) -> bytes:
    return _rewrite_exact_strings(command, {old_name.encode(): new_name.encode()})[0]


def _rename_sequence_object(command: bytes, new_name: str) -> bytes:
    rebuilt = bytearray()
    renamed = False
    for field in _parse_fields(command):
        if field.number != 19 or field.wire_type != 2 or renamed:
            rebuilt.extend(field.raw)
            continue
        nested = command[field.value_start : field.value_end]
        fields = _parse_fields(nested)
        if not any(item.number == 21 for item in fields):
            rebuilt.extend(field.raw)
            continue
        nested_rebuilt = bytearray()
        for item in fields:
            if item.number == 28 and item.wire_type == 2:
                nested_rebuilt.extend(_field_bytes(28, 2, new_name.encode("utf-8")))
                renamed = True
            else:
                nested_rebuilt.extend(item.raw)
        rebuilt.extend(_field_bytes(19, 2, bytes(nested_rebuilt)))
    return bytes(rebuilt)


def _rewrite_exact_strings(
    data: bytes,
    replacements: dict[bytes, bytes],
    *,
    depth: int = 0,
) -> tuple[bytes, int]:
    if depth > 12 or not any(old in data for old in replacements):
        return data, 0
    try:
        fields = _parse_fields(data)
    except ValueError:
        return data, 0
    rebuilt = bytearray()
    changes = 0
    for field in fields:
        if field.wire_type != 2:
            rebuilt.extend(field.raw)
            continue
        value = data[field.value_start : field.value_end]
        replacement = replacements.get(value)
        if replacement is not None:
            rebuilt.extend(_field_bytes(field.number, 2, replacement))
            changes += 1
            continue
        rewritten, nested_changes = _rewrite_exact_strings(value, replacements, depth=depth + 1)
        if nested_changes:
            rebuilt.extend(_field_bytes(field.number, 2, rewritten))
            changes += nested_changes
        else:
            rebuilt.extend(field.raw)
    return bytes(rebuilt), changes


def _build_header(
    carrier_path: Path,
    context: _BuildContext,
    *,
    sequence_name: str,
    injection_name: str,
    method_name: str,
    report_name: str,
    command_size: int,
) -> bytes:
    root = ET.fromstring(read_cmbx_header_xml(carrier_path))
    nodes = {node.attrib.get("Id", ""): node for node in root.iter("ChromeleonElement")}
    sequence = nodes[context.carrier_sequence.id]
    sequence.set("Name", sequence_name)
    sequence.set("Size", str(command_size))
    injection = nodes[context.carrier_injection.id]
    injection.set("Name", injection_name)
    _rename_header_node(nodes[context.carrier_method.id], method_name, ".instmeth")
    _rename_header_node(nodes[context.carrier_report.id], report_name, ".report")
    for child in list(injection):
        item_type = child.attrib.get("ItemType", "").lower()
        if "signal" in item_type or "audittrail" in item_type:
            injection.remove(child)
    _rename_sequence_header_urls(sequence, sequence_name)
    return b'<?xml version="1.0" encoding="UTF-8"?>' + ET.tostring(root, encoding="utf-8")


def _rename_header_node(node: ET.Element, new_name: str, suffix: str) -> None:
    node.set("Name", new_name)
    url = node.attrib.get("Url", "")
    if url:
        prefix = url.rsplit("/", 1)[0] if "/" in url else ""
        value = f"{new_name}{suffix}"
        node.set("Url", f"{prefix}/{value}" if prefix else value)


def _rename_sequence_header_urls(sequence_node: ET.Element, sequence_name: str) -> None:
    old_url = sequence_node.attrib.get("Url", "")
    if not old_url:
        return
    prefix = old_url.rsplit("/", 1)[0] if "/" in old_url else ""
    new_tail = f"{sequence_name}.seq"
    new_url = f"{prefix}/{new_tail}" if prefix else new_tail
    sequence_node.set("Url", new_url)
    old_prefix = old_url.rstrip("/") + "/"
    new_prefix = new_url.rstrip("/") + "/"
    for child in sequence_node.iter("ChromeleonElement"):
        if child is sequence_node:
            continue
        url = child.attrib.get("Url", "")
        if url.startswith(old_prefix):
            child.set("Url", new_prefix + url[len(old_prefix) :])


def _hidden_object_names(package) -> tuple[str, ...]:
    if not package.sequences or not package.sequences[0].filename:
        return ()
    data = extract_cmbx_entry(package.path, package.sequences[0].filename)
    names: list[str] = []
    for field in _parse_fields(data):
        if field.number != 19 or field.wire_type != 2:
            continue
        nested = data[field.value_start : field.value_end]
        try:
            name = _field_text(nested, _parse_fields(nested), 28)
        except ValueError:
            continue
        if name and name not in names:
            names.append(name)
    return tuple(names)


def _field_text(data: bytes, fields, number: int) -> str:
    for field in fields:
        if field.number == number and field.wire_type == 2:
            return data[field.value_start : field.value_end].decode("utf-8", errors="replace")
    return ""


def _clean_name(value: str, fallback: str) -> str:
    cleaned = " ".join(str(value or "").split()).strip()
    return cleaned or fallback
