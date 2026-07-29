from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from cmbx_container import CmbxPackage
from sequence_cmd_parser import build_injection_method_links, get_injection_method_link


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TCC_CATALOG_PATH = PROJECT_ROOT / "knowledge_base" / "tcc_semantic_test_catalog.json"
DEFAULT_TCC_SYMBOL_MANIFEST_PATH = PROJECT_ROOT / "knowledge_base" / "tcc_required_symbol_manifest.json"


@dataclass(frozen=True)
class InjectionBlueprint:
    test_intent: str
    injection_name: str
    instrument_method: str
    processing_method: str
    capability_groups: tuple[str, ...]
    report_sheets: tuple[str, ...]
    ret_times: tuple[str, ...]
    channels: tuple[str, ...]


@dataclass(frozen=True)
class SequenceBlueprint:
    family: str
    device_model: str
    report_template: str
    db_device_source_formula: str
    injections: tuple[InjectionBlueprint, ...]

    @property
    def required_capability_groups(self) -> tuple[str, ...]:
        groups: set[str] = set()
        for injection in self.injections:
            groups.update(injection.capability_groups)
        return tuple(sorted(groups))


@dataclass(frozen=True)
class CapabilityValidation:
    required_groups: tuple[str, ...]
    available_groups: tuple[str, ...]
    missing_groups: tuple[str, ...]

    @property
    def passed(self) -> bool:
        return not self.missing_groups


@dataclass(frozen=True)
class PackageCompatibility:
    device_model: str
    report_template: str
    missing_injections: tuple[str, ...]
    missing_instrument_methods: tuple[str, ...]
    missing_processing_methods: tuple[str, ...]
    missing_report_templates: tuple[str, ...]
    mismatched_links: tuple[str, ...]

    @property
    def passed(self) -> bool:
        return not (
            self.missing_injections
            or self.missing_instrument_methods
            or self.missing_processing_methods
            or self.missing_report_templates
            or self.mismatched_links
        )


@dataclass(frozen=True)
class ExecutionPackageCompatibility:
    device_model: str
    missing_injections: tuple[str, ...]
    missing_instrument_methods: tuple[str, ...]
    missing_processing_methods: tuple[str, ...]
    mismatched_links: tuple[str, ...]

    @property
    def passed(self) -> bool:
        return not (
            self.missing_injections
            or self.missing_instrument_methods
            or self.missing_processing_methods
            or self.mismatched_links
        )


@dataclass(frozen=True)
class CloneSelectPlan:
    source_package: str
    family: str
    device_model: str
    report_template: str
    injections: tuple[str, ...]
    instrument_methods: tuple[str, ...]
    processing_methods: tuple[str, ...]
    required_capability_groups: tuple[str, ...]


@dataclass(frozen=True)
class ExecutionSequenceRow:
    row_order: int
    injection_name: str
    instrument_method: str
    processing_method: str
    test_intent: str


@dataclass(frozen=True)
class ExecutionSequencePlan:
    family: str
    device_model: str
    rows: tuple[ExecutionSequenceRow, ...]

    @property
    def instrument_methods(self) -> tuple[str, ...]:
        return _unique_in_order(row.instrument_method for row in self.rows)

    @property
    def processing_methods(self) -> tuple[str, ...]:
        return _unique_in_order(row.processing_method for row in self.rows)


def load_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_tcc_semantic_catalog(path: str | Path | None = None) -> dict[str, Any]:
    return load_json(path or DEFAULT_TCC_CATALOG_PATH)


def load_tcc_symbol_manifest(path: str | Path | None = None) -> dict[str, Any]:
    return load_json(path or DEFAULT_TCC_SYMBOL_MANIFEST_PATH)


def available_capability_groups(symbol_manifest: dict[str, Any]) -> tuple[str, ...]:
    return tuple(sorted(symbol_manifest.get("capability_groups", {})))


def build_sequence_blueprint(
    catalog: dict[str, Any],
    device_model: str,
    test_intents: Iterable[str] | None = None,
) -> SequenceBlueprint:
    device_models = catalog.get("device_models", {})
    if device_model not in device_models:
        raise KeyError(f"Unknown device model: {device_model}")

    selected = list(test_intents) if test_intents is not None else list(catalog.get("test_intents", {}))
    injections: list[InjectionBlueprint] = []
    tests = catalog.get("test_intents", {})

    for test_intent in selected:
        test = tests.get(test_intent)
        if test is None:
            raise KeyError(f"Unknown test intent: {test_intent}")
        binding = test.get("device_bindings", {}).get(device_model)
        if binding is None:
            continue
        instrument_method = test.get("instrument_method")
        if instrument_method is None:
            instrument_method = test.get("instrument_method_by_device", {}).get(device_model)
        if not instrument_method:
            raise KeyError(f"Missing instrument method for {test_intent} on {device_model}")
        injections.append(
            InjectionBlueprint(
                test_intent=test_intent,
                injection_name=str(binding["injection_name"]),
                instrument_method=str(instrument_method),
                processing_method=str(binding["processing_method"]),
                capability_groups=tuple(test.get("capability_groups", ())),
                report_sheets=tuple(test.get("report_sheets", ())),
                ret_times=tuple(test.get("ret_times", ())),
                channels=tuple(test.get("channels", ())),
            )
        )

    device = device_models[device_model]
    return SequenceBlueprint(
        family=str(catalog.get("family", "")),
        device_model=device_model,
        report_template=str(device["report_template"]),
        db_device_source_formula=str(device["db_device_source_formula"]),
        injections=tuple(injections),
    )


def validate_blueprint_capabilities(
    blueprint: SequenceBlueprint,
    available_groups: Iterable[str],
) -> CapabilityValidation:
    available = set(available_groups)
    required = set(blueprint.required_capability_groups)
    missing = sorted(required - available)
    return CapabilityValidation(
        required_groups=tuple(sorted(required)),
        available_groups=tuple(sorted(available)),
        missing_groups=tuple(missing),
    )


def blueprint_to_dict(blueprint: SequenceBlueprint) -> dict[str, Any]:
    return {
        "family": blueprint.family,
        "device_model": blueprint.device_model,
        "report_template": blueprint.report_template,
        "db_device_source_formula": blueprint.db_device_source_formula,
        "required_capability_groups": list(blueprint.required_capability_groups),
        "injections": [
            {
                "test_intent": item.test_intent,
                "injection_name": item.injection_name,
                "instrument_method": item.instrument_method,
                "processing_method": item.processing_method,
                "capability_groups": list(item.capability_groups),
                "report_sheets": list(item.report_sheets),
                "ret_times": list(item.ret_times),
                "channels": list(item.channels),
            }
            for item in blueprint.injections
        ],
    }


def validate_blueprint_against_package(
    blueprint: SequenceBlueprint,
    package: CmbxPackage,
) -> PackageCompatibility:
    execution_compatibility = validate_execution_plan_against_package(
        build_execution_sequence_plan(blueprint),
        package,
    )
    package_reports = _normalized_name_map(
        element.name
        for element in package.methods_and_reports
        if element.kind == "report_template"
    )
    missing_report_templates = []
    if _normalize_name(blueprint.report_template) not in package_reports:
        missing_report_templates.append(blueprint.report_template)

    return PackageCompatibility(
        device_model=blueprint.device_model,
        report_template=blueprint.report_template,
        missing_injections=execution_compatibility.missing_injections,
        missing_instrument_methods=execution_compatibility.missing_instrument_methods,
        missing_processing_methods=execution_compatibility.missing_processing_methods,
        missing_report_templates=tuple(missing_report_templates),
        mismatched_links=execution_compatibility.mismatched_links,
    )


def validate_execution_plan_against_package(
    plan: ExecutionSequencePlan,
    package: CmbxPackage,
) -> ExecutionPackageCompatibility:
    package_injections = _normalized_name_map(injection.name for injection in package.injections)
    package_methods = _normalized_name_map(
        element.name
        for element in package.methods_and_reports
        if element.kind == "instrument_method"
    )
    package_processing_methods = _normalized_name_map(
        element.name
        for element in package.methods_and_reports
        if element.kind == "processing_method"
    )
    links = build_injection_method_links(package)

    missing_injections: list[str] = []
    missing_instrument_methods: list[str] = []
    missing_processing_methods: list[str] = []
    mismatched_links: list[str] = []

    for row in plan.rows:
        if _normalize_name(row.injection_name) not in package_injections:
            missing_injections.append(row.injection_name)
        if _normalize_name(row.instrument_method) not in package_methods:
            missing_instrument_methods.append(row.instrument_method)
        if _normalize_name(row.processing_method) not in package_processing_methods:
            missing_processing_methods.append(row.processing_method)

        actual_link = get_injection_method_link(links, row.injection_name)
        if actual_link is None:
            actual_link = _find_link_by_normalized_name(links, row.injection_name)
        if actual_link is None:
            continue
        if _normalize_name(actual_link.instrument_method) != _normalize_name(row.instrument_method):
            mismatched_links.append(
                f"{row.injection_name}: instrument {actual_link.instrument_method} != {row.instrument_method}"
            )
        if _normalize_name(actual_link.processing_method) != _normalize_name(row.processing_method):
            mismatched_links.append(
                f"{row.injection_name}: processing {actual_link.processing_method} != {row.processing_method}"
            )

    return ExecutionPackageCompatibility(
        device_model=plan.device_model,
        missing_injections=tuple(sorted(set(missing_injections))),
        missing_instrument_methods=tuple(sorted(set(missing_instrument_methods))),
        missing_processing_methods=tuple(sorted(set(missing_processing_methods))),
        mismatched_links=tuple(mismatched_links),
    )


def blueprint_report_text(
    blueprint: SequenceBlueprint,
    capability_validation: CapabilityValidation | None = None,
    package_compatibility: PackageCompatibility | None = None,
) -> str:
    lines = [
        f"Family: {blueprint.family}",
        f"Device Model: {blueprint.device_model}",
        f"Report Template: {blueprint.report_template}",
        f"Device Source Formula: {blueprint.db_device_source_formula}",
        f"Required Capability Groups: {', '.join(blueprint.required_capability_groups) or '(none)'}",
        "",
        "Injections",
        "----------",
        "Test Intent\tInjection\tInstrument Method\tProcessing Method\tCapability Groups\tReport Sheets",
    ]
    for item in blueprint.injections:
        lines.append(
            "\t".join(
                [
                    item.test_intent,
                    item.injection_name,
                    item.instrument_method,
                    item.processing_method,
                    ", ".join(item.capability_groups),
                    ", ".join(item.report_sheets),
                ]
            )
        )

    if capability_validation is not None:
        lines.extend(
            [
                "",
                "Capability Validation",
                "---------------------",
                f"Passed: {capability_validation.passed}",
                f"Missing Groups: {', '.join(capability_validation.missing_groups) or '(none)'}",
            ]
        )

    if package_compatibility is not None:
        lines.extend(
            [
                "",
                "Golden Package Compatibility",
                "----------------------------",
                f"Passed: {package_compatibility.passed}",
                f"Missing Injections: {', '.join(package_compatibility.missing_injections) or '(none)'}",
                f"Missing Instrument Methods: {', '.join(package_compatibility.missing_instrument_methods) or '(none)'}",
                f"Missing Processing Methods: {', '.join(package_compatibility.missing_processing_methods) or '(none)'}",
                f"Missing Report Templates: {', '.join(package_compatibility.missing_report_templates) or '(none)'}",
                f"Mismatched Links: {'; '.join(package_compatibility.mismatched_links) or '(none)'}",
            ]
        )
    return "\n".join(lines)


def build_clone_select_plan(
    blueprint: SequenceBlueprint,
    package: CmbxPackage,
    compatibility: PackageCompatibility | None = None,
) -> CloneSelectPlan:
    compatibility = compatibility or validate_blueprint_against_package(blueprint, package)
    if not compatibility.passed:
        raise ValueError(
            "Blueprint is not compatible with the selected golden package. "
            f"Missing injections={compatibility.missing_injections}, "
            f"missing instrument methods={compatibility.missing_instrument_methods}, "
            f"missing processing methods={compatibility.missing_processing_methods}, "
            f"missing reports={compatibility.missing_report_templates}, "
            f"mismatched links={compatibility.mismatched_links}"
        )
    return CloneSelectPlan(
        source_package=str(package.path),
        family=blueprint.family,
        device_model=blueprint.device_model,
        report_template=blueprint.report_template,
        injections=tuple(item.injection_name for item in blueprint.injections),
        instrument_methods=_unique_in_order(item.instrument_method for item in blueprint.injections),
        processing_methods=_unique_in_order(item.processing_method for item in blueprint.injections),
        required_capability_groups=blueprint.required_capability_groups,
    )


def build_execution_sequence_plan(blueprint: SequenceBlueprint) -> ExecutionSequencePlan:
    """Return the minimal sequence layer required to run the selected tests.

    Report templates, DB fields, workbook formulas, and print/page layout are intentionally
    excluded from this plan. Processing methods remain because IRC can change sequence
    behavior, such as inserting or stopping injections.
    """
    return ExecutionSequencePlan(
        family=blueprint.family,
        device_model=blueprint.device_model,
        rows=tuple(
            ExecutionSequenceRow(
                row_order=index,
                injection_name=item.injection_name,
                instrument_method=item.instrument_method,
                processing_method=item.processing_method,
                test_intent=item.test_intent,
            )
            for index, item in enumerate(blueprint.injections, 1)
        ),
    )


def execution_sequence_plan_to_dict(plan: ExecutionSequencePlan) -> dict[str, Any]:
    return {
        "family": plan.family,
        "device_model": plan.device_model,
        "instrument_methods": list(plan.instrument_methods),
        "processing_methods": list(plan.processing_methods),
        "rows": [
            {
                "row_order": row.row_order,
                "injection_name": row.injection_name,
                "instrument_method": row.instrument_method,
                "processing_method": row.processing_method,
                "test_intent": row.test_intent,
            }
            for row in plan.rows
        ],
    }


def clone_select_plan_to_dict(plan: CloneSelectPlan) -> dict[str, Any]:
    return {
        "source_package": plan.source_package,
        "family": plan.family,
        "device_model": plan.device_model,
        "report_template": plan.report_template,
        "injections": list(plan.injections),
        "instrument_methods": list(plan.instrument_methods),
        "processing_methods": list(plan.processing_methods),
        "required_capability_groups": list(plan.required_capability_groups),
    }


def _normalize_name(value: str) -> str:
    return "".join(char.lower() for char in value if char.isalnum())


def _normalized_name_map(values: Iterable[str]) -> dict[str, str]:
    return {_normalize_name(value): value for value in values}


def _find_link_by_normalized_name(links: dict[str, Any], injection_name: str) -> Any | None:
    expected = _normalize_name(injection_name)
    for name, link in links.items():
        if _normalize_name(name) == expected:
            return link
    return None


def _unique_in_order(values: Iterable[str]) -> tuple[str, ...]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        normalized = _normalize_name(value)
        if normalized in seen:
            continue
        seen.add(normalized)
        result.append(value)
    return tuple(result)
