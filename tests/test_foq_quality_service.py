from __future__ import annotations

import sys
import tkinter as tk
from pathlib import Path
from types import SimpleNamespace


MODULE_ROOT = Path(__file__).resolve().parents[1]
if str(MODULE_ROOT) not in sys.path:
    sys.path.insert(0, str(MODULE_ROOT))

from cmbx_container import CmbxElement, CmbxPackage
import foq_quality_service
import foq_quality_window
from db_upload_service import DatabaseUploadConfig, _connection_string
from foq_quality_service import (
    FoqSequenceCandidate,
    FoqMetricResult,
    attach_history,
    classify_result_value,
    expand_metric_dependencies,
    filter_database_rows,
    filter_history_for_device,
    metric_catalog_for_devices,
    summarize_history,
)
from windows_credentials import protect_secret, unprotect_secret


def metric(value=10.0) -> FoqMetricResult:
    return FoqMetricResult(
        package="sample.cmbx",
        sequence="Sequence 1",
        device="VH-C10-A",
        db_field="TempStability",
        description="Temperature stability",
        value=value,
        unit="K",
        calculation_status="ok",
        spec_status="pass",
        spec_evidence="RES_TempStability",
        report_sheet="Temp Stability_Noise",
        report_cell="D26",
        injection="Temperature Stability_H",
        detail="derived result",
    )


def test_classify_report_result_values() -> None:
    assert classify_result_value("Test passed") == "pass"
    assert classify_result_value("FAILED") == "fail"
    assert classify_result_value("") == "not-evaluated"
    assert classify_result_value("Manual review") == "review"


def test_history_summary_uses_three_sigma_limits() -> None:
    summary = summarize_history([8.0, 10.0, 12.0])
    assert summary.count == 3
    assert summary.mean == 10.0
    assert summary.stdev == 2.0
    assert summary.ucl == 16.0
    assert summary.lcl == 4.0


def test_attach_history_matches_database_columns_case_insensitively() -> None:
    rows = attach_history([metric(17.0)], [{"tempstability": 8.0}, {"TempStability": 10.0}, {"TEMPSTABILITY": 12.0}])
    assert rows[0].history.count == 3
    assert rows[0].history.mean == 10.0
    assert rows[0].history_delta == 7.0
    assert rows[0].history_status == "outside-3sigma"


def test_history_baseline_is_filtered_to_the_current_device_model() -> None:
    rows, scope = filter_history_for_device(
        [{"ModelNo": "VH-C10-A", "TempStability": 1}, {"ModelNo": "VC-C10-A", "TempStability": 99}],
        "VH-C10-A",
    )
    assert rows == [{"ModelNo": "VH-C10-A", "TempStability": 1}]
    assert scope == "ModelNo = VH-C10-A"


def test_candidate_discovery_skips_additional_injection_support_sequence(tmp_path, monkeypatch) -> None:
    support = CmbxElement("support", "AdditionalInjections", "Sequence")
    support.children.append(CmbxElement("inj1", "Accuracy_H", "Injection"))
    completed = CmbxElement("main", "Completed FOQ", "Sequence")
    completed.children.extend(
        [CmbxElement("inj2", "Accuracy_H", "Injection"), CmbxElement("report", "Report_VTCC", "ReportDefinition")]
    )
    package = CmbxPackage(tmp_path / "mixed.cmbx", [], [support, completed], {})
    monkeypatch.setattr(foq_quality_service, "load_cmbx_package", lambda _path: package)
    monkeypatch.setattr(
        foq_quality_service,
        "detect_sequence_device",
        lambda _package, sequence, _lookup: ("VH-C10-A", "audit") if sequence is completed else ("unresolved", "missing"),
    )
    monkeypatch.setattr(foq_quality_service, "_device_lookup", lambda _path: {})

    candidates, errors = foq_quality_service.discover_foq_candidates([package.path], tmp_path / "mapping.xls")

    assert not errors
    assert [candidate.sequence.name for candidate in candidates] == ["Completed FOQ"]
    assert candidates[0].report_template == "Report_VTCC"


def test_local_dsn_uses_filedsn_connection_string() -> None:
    config = DatabaseUploadConfig("", "QCLab", "QCUser", "secret", dsn=r"C:\Data\QCLab.dsn")
    connection = _connection_string(config)
    assert connection.startswith(r"FILEDSN=C:\Data\QCLab.dsn;")
    assert "UID=QCUser;" in connection


def test_database_password_can_be_saved_for_current_windows_user() -> None:
    protected = protect_secret("temporary-test-password")
    assert protected
    assert "temporary-test-password" not in protected
    assert unprotect_secret(protected) == "temporary-test-password"


def test_metric_catalog_uses_union_for_multiple_devices(monkeypatch) -> None:
    by_device = {
        "VH-C10-A": [
            SimpleNamespace(db_field="TempStability", unit="K", report_sheet="Stability"),
            SimpleNamespace(db_field="Performance_PCC", unit="min", report_sheet="Stability"),
            SimpleNamespace(db_field="RES_Stability", unit="NO SEARCH RESULT", report_sheet="Stability"),
        ],
        "VC-C10-A": [
            SimpleNamespace(db_field="TempStability", unit="K", report_sheet="Stability"),
            SimpleNamespace(db_field="TempAcc40", unit="K", report_sheet="Accuracy"),
        ],
    }
    monkeypatch.setattr(foq_quality_service, "locations_for_device_type", lambda _path, device: ("sheet", by_device[device]))
    assert metric_catalog_for_devices("mapping.xls", ["VH-C10-A", "VC-C10-A"]) == [
        "Performance_PCC", "TempAcc40", "TempStability",
    ]


def test_metric_dependency_adds_result_from_same_report_sheet(monkeypatch) -> None:
    locations = [
        SimpleNamespace(db_field="TempAcc40", unit="K", report_sheet="Temp Accuracy"),
        SimpleNamespace(db_field="RES_TempAccuracy", unit="NO SEARCH RESULT", report_sheet="Temp Accuracy"),
        SimpleNamespace(db_field="RES_Stability", unit="NO SEARCH RESULT", report_sheet="Temp Stability"),
    ]
    monkeypatch.setattr(foq_quality_service, "locations_for_device_type", lambda _path, _device: ("sheet", locations))
    assert expand_metric_dependencies("mapping.xls", "VH-C10-A", ["TempAcc40"]) == ["RES_TempAccuracy", "TempAcc40"]


def test_database_rows_can_be_filtered_by_model_timebase_and_date() -> None:
    rows = [
        {"ModelNo": "VH-C10-A", "ModelVariant": "03", "TimeBase": "Line 1", "TestDate": "2025-06-01"},
        {"ModelNo": "VH-C10-A", "ModelVariant": "03", "TimeBase": "Line 2", "TestDate": "2025-08-01"},
        {"ModelNo": "VC-C10-A", "ModelVariant": "03", "TimeBase": "Line 1", "TestDate": "2025-06-01"},
    ]
    filtered = filter_database_rows(rows, {"model": "VH-C10-A", "timebase": "Line 1", "date_from": "2025-01-01", "date_to": "2025-07-01"})
    assert filtered == [rows[0]]


def test_selected_injection_ids_are_forwarded_to_contract_evaluation(tmp_path, monkeypatch) -> None:
    sequence = CmbxElement("sequence", "FOQ", "Sequence")
    package = CmbxPackage(tmp_path / "sample.cmbx", [], [sequence], {})
    candidate = FoqSequenceCandidate(package, sequence, "VH-C10-A", "audit", "Report_VTCC")
    captured = {}

    def fake_evaluate(*_args, **kwargs):
        captured.update(kwargs)
        return "VTCC", []

    monkeypatch.setattr(foq_quality_service, "evaluate_foq_contract_values", fake_evaluate)
    rows = foq_quality_service.evaluate_candidate(candidate, tmp_path / "mapping.xls", selected_injection_ids=["inj-2"])

    assert rows == []
    assert captured["selected_injection_ids"] == ["inj-2"]


def test_metric_sets_can_be_saved_and_loaded(tmp_path, monkeypatch) -> None:
    preset_path = tmp_path / "metric_sets.json"
    monkeypatch.setattr(foq_quality_window, "DEFAULT_METRIC_PRESETS", preset_path)
    expected = {"Temperature essentials": ["TempStability", "TempAcc40"]}

    foq_quality_window.FoqQualityWindow._save_metric_presets(expected)

    assert foq_quality_window.FoqQualityWindow._load_metric_presets() == expected


def _history_scope_window(master: tk.Tcl):
    window = object.__new__(foq_quality_window.FoqQualityWindow)
    window.history_use_var = tk.BooleanVar(master=master, value=True)
    window.history_table_var = tk.StringVar(master=master, value="dbo.VTCC")
    window.history_limit_var = tk.StringVar(master=master, value="5000")
    window.history_model_var = tk.StringVar(master=master)
    window.history_variant_var = tk.StringVar(master=master)
    window.history_timebase_var = tk.StringVar(master=master)
    window.history_date_from_var = tk.StringVar(master=master)
    window.history_date_to_var = tk.StringVar(master=master)
    window.history_selected_models = set()
    window.history_selected_variants = set()
    window.history_selected_timebases = set()
    window.history_cached_choices = {"model": [], "variant": [], "timebase": []}
    window.database_tables = []
    window.history_scope_confirmed = False
    return window


def test_history_filter_settings_are_persisted_without_loading_database(tmp_path, monkeypatch) -> None:
    path = tmp_path / "history_scope.json"
    monkeypatch.setattr(foq_quality_window, "DEFAULT_HISTORY_SCOPE", path)
    master = tk.Tcl()
    saved = _history_scope_window(master)
    saved.history_selected_models = {"VH-C10-A"}
    saved.history_selected_timebases = {"Line 1"}
    saved.history_date_from_var.set("2025-01-01")
    saved.history_date_to_var.set("2025-12-31")
    saved.history_cached_choices = {"model": ["VH-C10-A", "VC-C10-A"], "variant": ["03"], "timebase": ["Line 1"]}
    saved.database_tables = [("dbo", "VTCC")]
    saved._save_history_scope_defaults()

    loaded = _history_scope_window(master)
    loaded._load_history_scope_defaults()

    assert loaded.history_scope_confirmed
    assert loaded.history_selected_models == {"VH-C10-A"}
    assert loaded.history_selected_timebases == {"Line 1"}
    assert loaded.history_date_from_var.get() == "2025-01-01"
    assert loaded.history_date_to_var.get() == "2025-12-31"
    assert loaded.history_cached_choices["model"] == ["VH-C10-A", "VC-C10-A"]
    assert loaded.database_tables == [("dbo", "VTCC")]


def test_new_cmbx_inventory_keeps_confirmed_metric_and_history_scope(tmp_path) -> None:
    window = object.__new__(foq_quality_window.FoqQualityWindow)
    window.metric_scope_confirmed = True
    window.history_scope_confirmed = True
    window.selected_metric_fields = {"TempStability"}
    window.history_selected_models = {"VH-C10-A"}
    window.selected_sequence_ids = set()
    window.selected_injection_ids = {}
    window.metrics = [metric()]
    window._metric_catalog = lambda: ["TempStability", "TempAcc40"]
    window._log = lambda _message: None
    window.show_task = lambda: None
    sequence = CmbxElement("seq-1", "FOQ", "Sequence")
    package = CmbxPackage(tmp_path / "sample.cmbx", [], [sequence], {})
    item = SimpleNamespace(eligible=True, device="VH-C10-A", sequence=sequence, package=package)

    window._finish_source_inventory([item], [])

    assert window.metric_scope_confirmed
    assert window.history_scope_confirmed
    assert window.selected_metric_fields == {"TempStability"}
    assert window.history_selected_models == {"VH-C10-A"}
