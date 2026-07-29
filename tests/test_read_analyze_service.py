from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace


MODULE_ROOT = Path(__file__).resolve().parents[1]
if str(MODULE_ROOT) not in sys.path:
    sys.path.insert(0, str(MODULE_ROOT))

from cmbx_container import CmbxElement, CmbxPackage
from read_analyze_service import (
    IntegrationSettings,
    _rolling_minimum,
    adapt_integration_settings,
    channel_records,
    classify_package,
    discover_cmbx_paths,
    describe_cm_formula,
    filter_channel_records,
    formula_records,
    injection_records,
    integrate_signal,
    match_channel_records,
    unique_channel_names,
)
from report_formula_evaluator import SignalPoint


def _package(tmp_path: Path) -> CmbxPackage:
    channel_a = CmbxElement("c1", "UV_VIS_1", "Signal", raw_filename="c1.raw", parent_id="i1")
    channel_b = CmbxElement("c2", "Pressure", "Signal", raw_filename="c2.raw", parent_id="i2")
    injection_a = CmbxElement("i1", "Injection A", "Injection", parent_id="s1", children=[channel_a])
    injection_b = CmbxElement("i2", "Injection B", "Injection", parent_id="s1", children=[channel_b])
    sequence = CmbxElement("s1", "Sequence 1", "Sequence", children=[injection_a, injection_b])
    return CmbxPackage(
        path=tmp_path / "sample.cmbx",
        entries=[],
        root_elements=[sequence],
        elements_by_id={item.id: item for item in (sequence, injection_a, injection_b, channel_a, channel_b)},
    )


def test_index_preserves_package_sequence_injection_channel_context(tmp_path: Path) -> None:
    package = _package(tmp_path)

    channels = channel_records([package])
    injections = injection_records([package])

    assert [(row.sequence.name, row.injection.name, row.channel.name) for row in channels] == [
        ("Sequence 1", "Injection A", "UV_VIS_1"),
        ("Sequence 1", "Injection B", "Pressure"),
    ]
    assert [row.injection.name for row in injections] == ["Injection A", "Injection B"]
    assert classify_package(package) == "Runtime data"


def test_reverse_channel_match_is_case_insensitive_and_exact_by_default(tmp_path: Path) -> None:
    rows = channel_records([_package(tmp_path)])

    assert [row.injection.name for row in match_channel_records(rows, "uv_vis_1")] == ["Injection A"]
    assert [row.channel.name for row in match_channel_records(rows, "press", exact=False)] == ["Pressure"]
    assert unique_channel_names(rows) == ["Pressure", "UV_VIS_1"]


def test_folder_discovery_skips_deleted_subtrees(tmp_path: Path) -> None:
    keep = tmp_path / "active" / "keep.cmbx"
    skip = tmp_path / "deleted" / "skip.cmbx"
    keep.parent.mkdir(); skip.parent.mkdir()
    keep.write_bytes(b"x"); skip.write_bytes(b"x")

    assert discover_cmbx_paths([tmp_path]) == [keep.resolve()]


def test_combined_channel_filters_apply_to_every_context_level(tmp_path: Path) -> None:
    rows = channel_records([_package(tmp_path)])

    matched = filter_channel_records(
        rows, package="sample", sequence="sequence 1", injection="injection a", channel="uv_vis"
    )

    assert [row.channel.name for row in matched] == ["UV_VIS_1"]
    assert filter_channel_records(rows, sequence="missing") == []


def test_external_integration_uses_one_parameter_set_and_finds_peak() -> None:
    points = []
    for index in range(301):
        time_min = index / 60.0
        distance = (time_min - 2.5) / 0.10
        value = 10.0 * pow(2.718281828459045, -(distance * distance) / 2.0)
        points.append(SignalPoint(time_min, value))

    peaks = integrate_signal(
        "synthetic", points,
        IntegrationSettings(smoothing_width_s=1.0, noise_multiplier=3.0, minimum_height=1.0, minimum_width_s=1.0),
    )

    assert len(peaks) == 1
    assert abs(peaks[0].apex_min - 2.5) < 0.05
    assert peaks[0].height > 8.0
    assert peaks[0].area > 0.0
    assert peaks[0].baseline_start <= 1.0
    assert peaks[0].baseline_end <= 1.0


def test_fast_rolling_minimum_matches_centered_window_definition() -> None:
    values = [5.0, 4.0, 6.0, 2.0, 8.0, 3.0, 7.0]
    width = 5
    half = width // 2
    expected = [min(values[max(0, i - half):min(len(values), i + half + 1)]) for i in range(len(values))]

    assert _rolling_minimum(values, width) == expected


def test_auto_adapt_uses_one_sampling_dependent_setting_for_all_traces() -> None:
    fast = [SignalPoint(index / 600.0, float(index)) for index in range(20)]
    slow = [SignalPoint(index / 60.0, float(index)) for index in range(20)]

    adapted = adapt_integration_settings([fast, slow], IntegrationSettings(smoothing_width_s=0.1))

    assert adapted.smoothing_width_s >= 1.65
    assert adapted.minimum_width_s == adapted.smoothing_width_s


def test_direct_cm_formula_meaning_uses_namespace_and_fixed_channel() -> None:
    assert "ExtTemp_UpperCC" in describe_cm_formula(
        'chm.sig_value("average", 1, 2)', "ExtTemp_UpperCC"
    )
    assert "RetTime2" in describe_cm_formula('AUDIT.RetTime2(1,"forward")')
    assert "precondition" in describe_cm_formula("precond.ColumnComp.ModelNo")


def test_direct_cm_inventory_reports_incremental_progress(tmp_path: Path, monkeypatch) -> None:
    import read_analyze_service

    reports = [
        CmbxElement("r1", "Report A", "Dionex.Chromeleon.Report.ReportDefinition", raw_filename="r1.bin"),
        CmbxElement("r2", "Report B", "Dionex.Chromeleon.Report.ReportDefinition", raw_filename="r2.bin"),
    ]
    package = CmbxPackage(
        path=tmp_path / "reports.cmbx", entries=[], root_elements=reports,
        elements_by_id={report.id: report for report in reports},
    )
    monkeypatch.setattr(read_analyze_service, "decode_report_template_xml", lambda _package, report: (b"", report.name))
    monkeypatch.setattr(
        read_analyze_service,
        "parse_report_sheet_objects",
        lambda _xml, report_name: [SimpleNamespace(
            formula=f'AUDIT.{report_name.replace(" ", "")}', sheet_name="Sheet1", excel_range="A1",
            object_type="ReportFormulaObject", fixed_channel="", fixed_component="",
        )],
    )
    updates = []

    records, errors = formula_records([package], progress=updates.append)

    assert errors == []
    assert len(records) == 2
    assert (updates[0].completed, updates[0].total, updates[0].formulas_found) == (0, 2, 0)
    assert (updates[-1].completed, updates[-1].total, updates[-1].formulas_found) == (2, 2, 2)
    assert updates[-1].eta_s == 0.0
