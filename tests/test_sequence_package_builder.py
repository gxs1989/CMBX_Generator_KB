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
NATIVE_TEN_ROW_CARRIER = ROOT / "assets" / "sequence_carrier_native_test2.cmbx"


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


@pytest.mark.skipif(
    not all(path.exists() for path in (NATIVE_TEN_ROW_CARRIER, METHOD, REPORT)),
    reason="Native ten-row Sequence carrier or component regression assets are unavailable.",
)
def test_native_ten_row_carrier_supports_more_than_two_injections(tmp_path: Path) -> None:
    output = tmp_path / "native_three_injection_sequence.cmbx"
    validation = build_multi_sequence_package(
        MultiSequencePackageRequest(
            carrier_cmbx=NATIVE_TEN_ROW_CARRIER,
            report_cmbx=REPORT,
            output_cmbx=output,
            sequence_name="Native Three Injection Sequence",
            report_name="SHARED_REPORT",
            injections=tuple(
                SequenceInjectionRequest(f"Injection {index}", METHOD, "ONE_SHARED_METHOD")
                for index in range(1, 4)
            ),
            include_processing_methods=False,
        )
    )

    assert validation.passed
    package = load_cmbx_package(output)
    assert len(package.injections) == 3
    assert len([item for item in package.methods_and_reports if item.kind == "instrument_method"]) == 1


@pytest.mark.skipif(
    not all(path.exists() for path in (NATIVE_TEN_ROW_CARRIER, METHOD, REPORT)),
    reason="Native ten-row Sequence carrier or component regression assets are unavailable.",
)
def test_native_ten_row_carrier_uses_full_eight_plus_two_capacity(tmp_path: Path) -> None:
    output = tmp_path / "native_ten_injection_sequence.cmbx"
    rows = [
        SequenceInjectionRequest(f"Method A Injection {index}", METHOD, "METHOD_A")
        for index in range(1, 9)
    ] + [
        SequenceInjectionRequest(f"Method B Injection {index}", METHOD, "METHOD_B")
        for index in range(1, 3)
    ]
    validation = build_multi_sequence_package(
        MultiSequencePackageRequest(
            carrier_cmbx=NATIVE_TEN_ROW_CARRIER,
            report_cmbx=REPORT,
            output_cmbx=output,
            sequence_name="Native Ten Injection Sequence",
            report_name="SHARED_REPORT",
            injections=tuple(rows),
            include_processing_methods=False,
        )
    )

    assert validation.passed
    assert len(validation.injection_names) == 10
    assert validation.instrument_methods == ("METHOD_A", "METHOD_B")


@pytest.mark.skipif(
    not all(path.exists() for path in (NATIVE_TEN_ROW_CARRIER, METHOD, REPORT)),
    reason="Native ten-row Sequence carrier or component regression assets are unavailable.",
)
@pytest.mark.parametrize("split", [(10, 0), (9, 1), (5, 5), (1, 9)])
def test_native_ten_row_carrier_rebinds_arbitrary_two_method_distribution(
    tmp_path: Path,
    split: tuple[int, int],
) -> None:
    first_count, second_count = split
    rows = [
        SequenceInjectionRequest(f"Method A Injection {index}", METHOD, "METHOD_A")
        for index in range(1, first_count + 1)
    ] + [
        SequenceInjectionRequest(f"Method B Injection {index}", METHOD, "METHOD_B")
        for index in range(1, second_count + 1)
    ]
    output = tmp_path / f"native_distribution_{first_count}_{second_count}.cmbx"
    validation = build_multi_sequence_package(
        MultiSequencePackageRequest(
            carrier_cmbx=NATIVE_TEN_ROW_CARRIER,
            report_cmbx=REPORT,
            output_cmbx=output,
            sequence_name=f"Native Distribution {first_count} {second_count}",
            report_name="SHARED_REPORT",
            injections=tuple(rows),
            include_processing_methods=False,
        )
    )

    assert validation.passed
    assert len(validation.injection_names) == 10
    assert len(validation.instrument_methods) == (1 if second_count == 0 else 2)


@pytest.mark.skipif(
    not all(path.exists() for path in (NATIVE_TEN_ROW_CARRIER, METHOD, REPORT)),
    reason="Native ten-row Sequence carrier or component regression assets are unavailable.",
)
def test_native_ten_row_carrier_clones_ten_distinct_method_slots(tmp_path: Path) -> None:
    output = tmp_path / "native_ten_distinct_methods.cmbx"
    validation = build_multi_sequence_package(
        MultiSequencePackageRequest(
            carrier_cmbx=NATIVE_TEN_ROW_CARRIER,
            report_cmbx=REPORT,
            output_cmbx=output,
            sequence_name="Ten Distinct Method Sequence",
            report_name="SHARED_REPORT",
            injections=tuple(
                SequenceInjectionRequest(
                    f"Injection {index}",
                    METHOD,
                    f"DISTINCT_METHOD_{index:02d}",
                )
                for index in range(1, 11)
            ),
            include_processing_methods=False,
        )
    )

    assert validation.passed
    assert validation.instrument_methods == tuple(
        f"DISTINCT_METHOD_{index:02d}" for index in range(1, 11)
    )
    package = load_cmbx_package(output)
    assert len(package.injections) == 10
    assert len([item for item in package.methods_and_reports if item.kind == "instrument_method"]) == 10
