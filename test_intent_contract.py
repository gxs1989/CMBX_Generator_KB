from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from method_contract import MethodContract


__test__ = False


@dataclass(frozen=True)
class TestIntentContractCoverage:
    device_model: str
    test_intent: str
    injection_name: str
    instrument_method: str
    processing_method: str
    expected_ret_times: tuple[str, ...]
    emitted_ret_times: tuple[str, ...]
    missing_ret_times: tuple[str, ...]
    expected_channels: tuple[str, ...]
    acquired_channels: tuple[str, ...]
    missing_channels: tuple[str, ...]
    expected_audit_properties: tuple[str, ...]
    logged_properties: tuple[str, ...]
    missing_audit_properties: tuple[str, ...]

    @property
    def passed(self) -> bool:
        return not (self.missing_ret_times or self.missing_channels or self.missing_audit_properties)


def build_test_intent_contract_coverages(
    catalog: dict[str, Any],
    device_model: str,
    method_contracts: Iterable[MethodContract],
) -> tuple[TestIntentContractCoverage, ...]:
    contract_by_method = {_normalize_name(contract.method_name): contract for contract in method_contracts}
    coverages: list[TestIntentContractCoverage] = []
    for test_intent, definition in catalog.get("test_intents", {}).items():
        binding = definition.get("device_bindings", {}).get(device_model)
        if not binding:
            continue
        instrument_method = definition.get("instrument_method")
        if instrument_method is None:
            instrument_method = definition.get("instrument_method_by_device", {}).get(device_model, "")
        processing_method = binding.get("processing_method", "")
        contract = contract_by_method.get(_normalize_name(str(instrument_method)))
        expected_ret_times = tuple(str(value) for value in definition.get("ret_times", ()))
        expected_channels = tuple(str(value) for value in definition.get("channels", ()))
        expected_audit_properties = _audit_dependencies(definition.get("report_dependencies", ()))
        emitted_ret_times = contract.ret_time_emissions if contract else ()
        acquired_channels = contract.acquisition_on if contract else ()
        logged_properties = contract.logged_properties if contract else ()
        coverages.append(
            TestIntentContractCoverage(
                device_model=device_model,
                test_intent=test_intent,
                injection_name=str(binding.get("injection_name", "")),
                instrument_method=str(instrument_method),
                processing_method=str(processing_method),
                expected_ret_times=expected_ret_times,
                emitted_ret_times=emitted_ret_times,
                missing_ret_times=_missing_ret_times(expected_ret_times, emitted_ret_times),
                expected_channels=expected_channels,
                acquired_channels=acquired_channels,
                missing_channels=_missing_channels(expected_channels, acquired_channels),
                expected_audit_properties=expected_audit_properties,
                logged_properties=logged_properties,
                missing_audit_properties=_missing_audit_properties(expected_audit_properties, logged_properties),
            )
        )
    return tuple(coverages)


def contract_coverages_tsv(coverages: Iterable[TestIntentContractCoverage]) -> str:
    lines = [
        "\t".join(
            [
                "Passed",
                "Device",
                "TestIntent",
                "Injection",
                "InstrumentMethod",
                "ProcessingMethod",
                "MissingRetTimes",
                "MissingChannels",
                "MissingAuditProperties",
                "ExpectedRetTimes",
                "EmittedRetTimes",
                "ExpectedChannels",
                "AcquiredChannels",
                "ExpectedAuditProperties",
                "LoggedProperties",
            ]
        )
    ]
    for coverage in coverages:
        lines.append(
            "\t".join(
                [
                    str(coverage.passed),
                    coverage.device_model,
                    coverage.test_intent,
                    coverage.injection_name,
                    coverage.instrument_method,
                    coverage.processing_method,
                    ", ".join(coverage.missing_ret_times),
                    ", ".join(coverage.missing_channels),
                    ", ".join(coverage.missing_audit_properties),
                    ", ".join(coverage.expected_ret_times),
                    ", ".join(coverage.emitted_ret_times),
                    ", ".join(coverage.expected_channels),
                    ", ".join(coverage.acquired_channels),
                    ", ".join(coverage.expected_audit_properties),
                    ", ".join(coverage.logged_properties),
                ]
            )
        )
    return "\n".join(lines)


test_intent_contract_coverages_tsv = contract_coverages_tsv
test_intent_contract_coverages_tsv.__test__ = False


def _missing_ret_times(expected: Iterable[str], emitted: Iterable[str]) -> tuple[str, ...]:
    emitted_normalized = {_normalize_ret_time(value) for value in emitted}
    return tuple(value for value in expected if _normalize_ret_time(value) not in emitted_normalized)


def _missing_channels(expected: Iterable[str], acquired: Iterable[str]) -> tuple[str, ...]:
    acquired_normalized = {_normalize_channel(value) for value in acquired}
    return tuple(value for value in expected if _normalize_channel(value) not in acquired_normalized)


def _missing_audit_properties(expected: Iterable[str], logged: Iterable[str]) -> tuple[str, ...]:
    logged_normalized = {_normalize_audit_property(value) for value in logged}
    return tuple(value for value in expected if _normalize_audit_property(value) not in logged_normalized)


def _audit_dependencies(dependencies: Iterable[str]) -> tuple[str, ...]:
    result: list[str] = []
    for dependency in dependencies:
        value = str(dependency)
        if not value.startswith("AUDIT."):
            continue
        path = value.removeprefix("AUDIT.")
        if "(" in path:
            path = path.split("(", 1)[0]
        result.append(path)
    return tuple(result)


def _normalize_ret_time(value: str) -> str:
    value = value.strip()
    if value.startswith("RetTimes."):
        value = value.removeprefix("RetTimes.")
    return value.lower()


def _normalize_channel(value: str) -> str:
    return _normalize_name(value.removeprefix("Thermometer1."))


def _normalize_audit_property(value: str) -> str:
    return _normalize_name(value)


def _normalize_name(value: str) -> str:
    return "".join(char.lower() for char in value if char.isalnum())
