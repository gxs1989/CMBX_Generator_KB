from __future__ import annotations

import sys
from pathlib import Path


MODULE_ROOT = Path(__file__).resolve().parents[1]
if str(MODULE_ROOT) not in sys.path:
    sys.path.insert(0, str(MODULE_ROOT))

from generation_project import (
    cross_contract_findings,
    preflight_asset,
    preflight_generation,
    recommended_online_kb_files_for_modules,
)
from report_template_md_compiler import ReportFormulaPatch, ReportTemplateMdSpec


def _report_spec(formula: str, fixed_channel: str = "") -> ReportTemplateMdSpec:
    return ReportTemplateMdSpec(
        path=Path("report.md"), template_name="Test", reference_cmbx="", reference_template_name="",
        generation_mode="create_from_blank", workbook_policy="new",
        patches=(ReportFormulaPatch("Result", "B2", "ReportFormulaObject", "create", formula, fixed_channel, ""),),
    )


def test_cross_contract_detects_missing_rettime() -> None:
    rows = [{"Time": "0.000", "Command": "Thermometer.ExtTemp.AcqOn", "Value": "", "Comment": ""}]
    findings = cross_contract_findings(rows, _report_spec('chm.signalValue(AUDIT.RetTime2(1,"forward"))', "ExtTemp"))
    assert next(item for item in findings if item.item == "RetTime anchors").level == "blocked"


def test_cross_contract_accepts_rettime_and_channel_evidence() -> None:
    rows = [
        {"Time": "0.000", "Command": "Thermometer.ExtTemp.AcqOn", "Value": "", "Comment": ""},
        {"Time": "1.000", "Command": "RetTimes.RetTime2", "Value": "System.Retention", "Comment": ""},
    ]
    findings = cross_contract_findings(rows, _report_spec('chm.signalValue(AUDIT.RetTime2(1,"forward"))', "ExtTemp"))
    assert not any(item.level == "blocked" for item in findings)


def test_paired_preflight_reports_missing_files(tmp_path: Path) -> None:
    result = preflight_generation(tmp_path / "missing_method.md", tmp_path / "missing_report.md")
    assert not result.ready
    assert result.report_errors


def test_single_asset_preflight_reports_missing_method(tmp_path: Path) -> None:
    result = preflight_asset("method", tmp_path / "missing.md")
    assert not result.ready
    assert result.errors == ["Method MD was not found."]


def test_single_asset_preflight_rejects_unknown_branch(tmp_path: Path) -> None:
    try:
        preflight_asset("processing", tmp_path / "anything.md")
    except ValueError as exc:
        assert "Unsupported asset type" in str(exc)
    else:
        raise AssertionError("Unknown asset branch should fail")


def test_recommended_files_support_multiple_modules_and_deduplicate_common_report_spec(monkeypatch, tmp_path: Path) -> None:
    import generation_project

    root = tmp_path / "KB" / "KB_Online_GPT" / "02_Full_Context"
    (root / "Report" / "TCC").mkdir(parents=True)
    (root / "Report" / "VAS").mkdir(parents=True)
    (root / "Report" / "01_REPORT_SPEC.md").write_text("spec", encoding="utf-8")
    (root / "Report" / "TCC" / "02_REPORT_ORIGINAL_TEMPLATES.md").write_text("tcc", encoding="utf-8")
    (root / "Report" / "VAS" / "02_REPORT_ORIGINAL_TEMPLATES.md").write_text("vas", encoding="utf-8")
    monkeypatch.setattr(generation_project, "DEFAULT_WORKSPACE", tmp_path)

    files = recommended_online_kb_files_for_modules("report", ("TCC", "VAS"))

    assert files[0].name == "01_REPORT_SPEC.md"
    assert len(files) == 3
    assert {path.parent.name for path in files[1:]} == {"TCC", "VAS"}
