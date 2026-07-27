from __future__ import annotations

import sys
from pathlib import Path


MODULE_ROOT = Path(__file__).resolve().parents[1]
if str(MODULE_ROOT) not in sys.path:
    sys.path.insert(0, str(MODULE_ROOT))

from method_md_linter import lint_method_rows
from tools.render_cm_method_md import parse_md_to_rows


def test_compact_stage_aliases_are_normalized(tmp_path: Path) -> None:
    source = tmp_path / "compact_stages.md"
    source.write_text(
        """```tsv
Time\tCommand\tValue\tComment
{Initial Time}\tInstrument Setup\t\t
0.000\tInjectPreparation\t\t
0.000\tStartRun\t\t
0.000\tRun\tDuration = 30.000 [min]\t
30.000\tStopRun\t\t
\tEnd\t\t
```\n""",
        encoding="utf-8",
    )

    rows = parse_md_to_rows(source)
    stages = [(row["Time"], row["Command"]) for row in rows if row["Kind"] == "Stage"]

    assert stages == [
        ("{Initial Time}", "Instrument Setup"),
        ("0.000", "Inject Preparation"),
        ("0.000", "Start Run"),
        ("0.000", "Run"),
        ("30.000", "Stop Run"),
    ]
    assert lint_method_rows(rows) == []


def test_linter_accepts_trigger_command_on_numeric_time_row() -> None:
    rows = [
        {"#": "1", "Kind": "Stage", "Time": "0.000", "Command": "Run", "Value": "Duration = 10.000 [min]", "Comment": ""},
        {"#": "2", "Kind": "Command", "Time": "1.000", "Command": "Trigger", "Value": '\"TimedTrigger\",', "Comment": ""},
        {"#": "3", "Kind": "Command", "Time": "", "Command": "Condition", "Value": "System.Retention>=1", "Comment": ""},
        {"#": "4", "Kind": "Command", "Time": "", "Command": "TrueTime", "Value": "1", "Comment": ""},
        {"#": "5", "Kind": "Command", "Time": "", "Command": "Limit", "Value": "1", "Comment": ""},
        {"#": "6", "Kind": "Stage", "Time": "End Trigger", "Command": "", "Value": "", "Comment": ""},
        {"#": "7", "Kind": "Stage", "Time": "10.000", "Command": "Stop Run", "Value": "", "Comment": ""},
    ]

    assert lint_method_rows(rows) == []
