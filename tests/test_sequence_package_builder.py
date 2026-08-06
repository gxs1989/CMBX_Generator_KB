from pathlib import Path

import pytest

from cmbx_container import load_cmbx_package
from sequence_package_builder import (
    MultiSequencePackageRequest,
    SequenceInjectionRequest,
    SequencePackageRequest,
    build_multi_sequence_package,
    build_sequence_package,
)


ROOT = Path(__file__).resolve().parents[1]
CARRIER = (
    ROOT
    / "outputs"
    / "generated_cmbx"
    / "VH-C10-A_temperature_accuracy_40C"
    / "VH-C10-A_temperature_accuracy_reference_multipoint.cmbx"
)
METHOD = ROOT / "deployment" / "assets" / "TEMP_HEAT_UP_DOWN_20_50_20.cmbx"
REPORT = ROOT / "outputs" / "Simple_TCC_Report_verified.cmbx"
MULTI_CARRIER = ROOT / "assets" / "sequence_carrier_tcc_10_slots.cmbx"
NATIVE_MULTI_CARRIER = ROOT / "assets" / "sequence_carrier_native_test1.cmbx"


@pytest.mark.skipif(
    not all(path.exists() for path in (CARRIER, METHOD, REPORT)),
    reason="Local CM-exported sequence/method/report regression assets are unavailable.",
)
def test_build_sequence_package_replaces_assets_and_updates_binding(tmp_path: Path) -> None:
    output = tmp_path / "generated_sequence.cmbx"
    validation = build_sequence_package(
        SequencePackageRequest(
            carrier_cmbx=CARRIER,
            method_cmbx=METHOD,
            report_cmbx=REPORT,
            output_cmbx=output,
            sequence_name="Generated TCC Sequence",
            injection_name="HeatUp CoolDown Test",
            method_name="GENERATED_HEATUP_COOLDOWN",
            report_name="GENERATED_TCC_REPORT",
        )
    )

    assert validation.passed
    assert output.exists()
    assert validation.sequence_name == "Generated TCC Sequence"
    assert validation.injection_name == "HeatUp CoolDown Test"
    assert validation.instrument_method == "GENERATED_HEATUP_COOLDOWN"
    assert validation.report_template == "GENERATED_TCC_REPORT"
    assert validation.method_payload_matches
    assert validation.report_payload_matches
    assert any("Processing Method" in item for item in validation.warnings)


@pytest.mark.skipif(
    not all(path.exists() for path in (MULTI_CARRIER, METHOD, REPORT)),
    reason="Controlled multi-Injection carrier or component regression assets are unavailable.",
)
def test_build_multi_sequence_package_binds_two_methods_and_blank_processing(tmp_path: Path) -> None:
    output = tmp_path / "multi_sequence.cmbx"
    validation = build_multi_sequence_package(
        MultiSequencePackageRequest(
            carrier_cmbx=MULTI_CARRIER,
            report_cmbx=REPORT,
            output_cmbx=output,
            sequence_name="Generated Multi Test",
            report_name="SHARED_REPORT",
            injections=(
                SequenceInjectionRequest("Heat Test A", METHOD, "HEAT_METHOD_A"),
                SequenceInjectionRequest("Heat Test B", METHOD, "HEAT_METHOD_B"),
            ),
            include_processing_methods=False,
        )
    )

    assert validation.passed
    assert output.exists()
    assert validation.injection_names == ("Heat Test A", "Heat Test B")
    assert validation.instrument_methods == ("HEAT_METHOD_A", "HEAT_METHOD_B")
    assert validation.report_template == "SHARED_REPORT"
    assert validation.processing_methods == ()
    assert all(validation.method_payload_matches)
    assert validation.report_payload_matches
    package = load_cmbx_package(output)
    assert package.sequences[0].url.endswith("/Generated Multi Test.seq")
    assert all("/Generated Multi Test.seq/" in item.url for item in package.sequences[0].children)


@pytest.mark.skipif(
    not all(path.exists() for path in (MULTI_CARRIER, METHOD, REPORT)),
    reason="Controlled multi-Injection carrier or component regression assets are unavailable.",
)
def test_build_multi_sequence_package_reuses_one_method_for_repeated_injections(tmp_path: Path) -> None:
    output = tmp_path / "shared_method_sequence.cmbx"
    validation = build_multi_sequence_package(
        MultiSequencePackageRequest(
            carrier_cmbx=MULTI_CARRIER,
            report_cmbx=REPORT,
            output_cmbx=output,
            sequence_name="Repeated Method Test",
            report_name="SHARED_REPORT",
            injections=(
                SequenceInjectionRequest("Injection 1", METHOD, "ONE_SHARED_METHOD"),
                SequenceInjectionRequest("Injection 2", METHOD, "ONE_SHARED_METHOD"),
            ),
            include_processing_methods=False,
        )
    )

    assert validation.passed
    assert validation.injection_names == ("Injection 1", "Injection 2")
    assert validation.instrument_methods == ("ONE_SHARED_METHOD",)
    package = load_cmbx_package(output)
    assert len(package.injections) == 2
    assert len([item for item in package.methods_and_reports if item.kind == "instrument_method"]) == 1


@pytest.mark.skipif(
    not all(path.exists() for path in (NATIVE_MULTI_CARRIER, METHOD, REPORT)),
    reason="Native empty Sequence carrier or component regression assets are unavailable.",
)
def test_native_empty_carrier_keeps_cm_exported_object_shape(tmp_path: Path) -> None:
    output = tmp_path / "native_shared_method_sequence.cmbx"
    validation = build_multi_sequence_package(
        MultiSequencePackageRequest(
            carrier_cmbx=NATIVE_MULTI_CARRIER,
            report_cmbx=REPORT,
            output_cmbx=output,
            sequence_name="Native Sequence",
            report_name="SHARED_REPORT",
            injections=(
                SequenceInjectionRequest("Injection 1", METHOD, "ONE_SHARED_METHOD"),
                SequenceInjectionRequest("Injection 2", METHOD, "ONE_SHARED_METHOD"),
            ),
            include_processing_methods=False,
        )
    )

    assert validation.passed
    assert validation.hidden_object_names == ()
    assert validation.instrument_methods == ("ONE_SHARED_METHOD",)
