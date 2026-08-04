from pathlib import Path
from types import SimpleNamespace

from leak_sensor_analysis import (
    compute_leak_metrics,
    evaluate_leak_groups,
    leak_channel_candidates,
    parse_leak_metadata,
)
from report_formula_evaluator import SignalPoint


def _record(name: str, injection: str = "LiquidLeaktest Water 25C"):
    package = SimpleNamespace(path=Path(name))
    sequence = SimpleNamespace(id="seq", name="Leak Sensor Sequence")
    injection_item = SimpleNamespace(id="inj", name=injection)
    channel = SimpleNamespace(id="channel", name="LEDBoard_LeakDiff")
    return SimpleNamespace(
        package=package,
        sequence=sequence,
        injection=injection_item,
        channel=channel,
        key=f"{name}|seq|inj|channel",
        label=f"{name} / Leak Sensor Sequence / {injection} / LEDBoard_LeakDiff",
    )


def _response_points(scale: float = 1.0) -> list[SignalPoint]:
    values = [0.0] * 12 + [1.0, 3.0, 5.0, 7.0, 9.0, 10.0, 10.0]
    return [SignalPoint(index * 0.01, value * scale) for index, value in enumerate(values)]


def test_leak_sensor_algorithm_runs_on_decoded_signal_points() -> None:
    row = compute_leak_metrics(_record("Water_25C.cmbx"), _response_points())

    assert row["liquid"] == "Water"
    assert row["temp"] == "25"
    assert row["diff_start"] == 0.0
    assert row["diff_peak"] == 10.0
    assert row["delta_diff"] == 10.0
    assert row["t0"] > 0
    assert row["t50"] > row["t0"]
    assert row["t90"] >= row["t50"]
    assert row["response_t90"] > 0
    assert row["rise_slope"] > 0


def test_t0_ignores_deviation_opposite_to_final_response() -> None:
    values = [0.0] * 12 + [-2.0, 0.0, 1.0, 4.0, 8.0, 10.0]
    points = [SignalPoint(index * 0.01, value) for index, value in enumerate(values)]
    row = compute_leak_metrics(_record("Water_25C.cmbx"), points)

    assert row["t0"] >= 0.13
    assert row["t90"] > row["t0"]
    assert row["response_t90"] == row["t90"] - row["t0"]


def test_benchmark_comparison_preserves_original_three_metric_rule() -> None:
    benchmark = compute_leak_metrics(_record("benchmark_Water_25C.cmbx"), _response_points())
    test_row = compute_leak_metrics(_record("test_Water_25C.cmbx"), _response_points(1.2))
    evaluated = evaluate_leak_groups([benchmark, test_row], [benchmark["key"]])

    assert evaluated[0]["evaluation"] == "Benchmark"
    assert evaluated[1]["benchmark_ref"] == benchmark["injection"]
    assert evaluated[1]["delta_eval"] == "BETTER"
    assert evaluated[1]["evaluation"] in {"BETTER", "MIXED"}


def test_leak_channel_catalog_prefers_liquid_leak_injections() -> None:
    focused = _record("focused.cmbx")
    unrelated = _record("other.cmbx", injection="Temperature Accuracy")
    records, scope = leak_channel_candidates([unrelated, focused])

    assert records == [focused]
    assert scope == "Liquid-leak injections"


def test_metadata_parser_accepts_compact_and_word_temperature_names() -> None:
    assert parse_leak_metadata("Water 25C") == ("Water", "25")
    assert parse_leak_metadata("MeOH 30 degrees C") == ("MeOH", "RT")
    assert parse_leak_metadata("IPA_40") == ("IPA", "RT")
    assert parse_leak_metadata("LiquidLeaktest_water_40") == ("Water", "40")


def test_room_temperature_solvents_share_one_benchmark_group() -> None:
    meoh_25 = compute_leak_metrics(
        _record("benchmark.cmbx", "LiquidLeaktest_MeOH_25"), _response_points(),
    )
    meoh_40 = compute_leak_metrics(
        _record("test.cmbx", "LiquidLeaktest_MeOH_40"), _response_points(1.1),
    )
    ipa_25 = compute_leak_metrics(
        _record("ipa.cmbx", "LiquidLeaktest_IPA_25"), _response_points(),
    )
    evaluated = evaluate_leak_groups([meoh_25, meoh_40, ipa_25], [meoh_25["key"]])

    assert meoh_25["group_key"] == "MeOH | RT"
    assert meoh_40["group_key"] == "MeOH | RT"
    assert ipa_25["group_key"] == "IPA | RT"
    assert evaluated[1]["benchmark_ref"] == meoh_25["injection"]
    assert evaluated[2]["benchmark_ref"] == "No matched benchmark"


def test_benchmark_never_crosses_liquid_or_temperature_condition() -> None:
    water_25 = compute_leak_metrics(
        _record("benchmark.cmbx", "LiquidLeaktest_water_25"), _response_points(),
    )
    water_40 = compute_leak_metrics(
        _record("test.cmbx", "LiquidLeaktest_water_40"), _response_points(1.1),
    )
    evaluated = evaluate_leak_groups([water_25, water_40], [water_25["key"]])

    assert water_25["group_key"] == "Water | 25C"
    assert water_40["group_key"] == "Water | 40C"
    assert evaluated[1]["benchmark_ref"] == "No matched benchmark"
    assert evaluated[1]["evaluation"] == ""
