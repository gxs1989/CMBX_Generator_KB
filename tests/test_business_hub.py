from __future__ import annotations

import sys
from pathlib import Path


MODULE_ROOT = Path(__file__).resolve().parents[1]
if str(MODULE_ROOT) not in sys.path:
    sys.path.insert(0, str(MODULE_ROOT))

from business_hub import BusinessHubApp, BusinessMindMap, CENTER_LIMITATIONS, CENTERS, JOURNEYS, child_command, center_by_id, task_by_id, workflow_by_id


def test_business_hub_exposes_three_journeys_and_eight_direct_tasks() -> None:
    assert [workflow.id for workflow in JOURNEYS] == ["design", "analyze", "quality"]
    assert [center.id for center in CENTERS] == [
        "method-generation",
        "report-generation",
        "hplc-applications",
        "raw-export",
        "chromatograms",
        "direct-formulas",
        "foq-check",
        "quality-data",
    ]
    assert workflow_by_id("design").title == "Design & Generate"
    assert workflow_by_id("analyze").title == "Chromatograms & Results"
    assert workflow_by_id("quality").title == "Quality Control & Database"
    assert workflow_by_id("design").center_ids == ("method-generation", "report-generation", "hplc-applications")
    assert workflow_by_id("analyze").center_ids == ("raw-export", "chromatograms", "direct-formulas")


def test_migrated_centers_are_marked_as_native() -> None:
    assert center_by_id("method-generation").action == "method_creation"
    assert center_by_id("report-generation").action == "report_creation"
    assert task_by_id("chromatograms").action == "chromatograms"
    assert task_by_id("direct-formulas").status == "native"
    assert task_by_id("foq-check").action == "foq_check"
    assert task_by_id("foq-check").status == "native"
    assert task_by_id("quality-data").action == "quality_data"
    assert task_by_id("quality-data").status == "native"


def test_home_map_supports_preview_before_direct_action() -> None:
    assert hasattr(BusinessHubApp, "open_center")
    assert not hasattr(BusinessHubApp, "show_center")
    assert hasattr(BusinessMindMap, "_select_preview")
    assert hasattr(BusinessMindMap, "_animate_focus")
    assert set(CENTER_LIMITATIONS) == {center.id for center in CENTERS}

    opened: list[str] = []
    previewed: list[tuple[str, str]] = []
    mind_map = object.__new__(BusinessMindMap)
    mind_map.on_preview = lambda kind, item_id: previewed.append((kind, item_id))
    mind_map.on_center = opened.append
    mind_map.on_journey = opened.append
    mind_map.focus_kind = ""
    mind_map.focus_id = ""
    mind_map.animation_progress = 1.0
    mind_map._animate_focus = lambda: None

    mind_map._select_preview("center", "quality-data")
    assert previewed == [("center", "quality-data")]
    assert opened == []

    mind_map.animation_progress = 1.0
    mind_map._select_preview("center", "quality-data")
    assert opened == ["quality-data"]


def test_child_command_uses_existing_script_and_no_shell(tmp_path: Path, monkeypatch) -> None:
    script = MODULE_ROOT / "run_app.py"
    command = child_command(script.name, executable=tmp_path / "python.exe")

    assert command[1] == "-B"
    assert Path(command[2]) == script
    assert command[0].endswith("python.exe")


def test_child_command_appends_workflow_route_arguments(tmp_path: Path) -> None:
    command = child_command("run_read_analyze.py", tmp_path / "python.exe", "--task", "formula")
    assert command[-2:] == ["--task", "formula"]
