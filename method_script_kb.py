from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
import re
from typing import Iterable


DEFAULT_PROGRAMDATA_KB_ROOT = Path(r"C:\ProgramData\CMBX Data Explorer Workspace\KB")


CmPreviewRow = tuple[str, str, str, str, str, str, str]


@dataclass(frozen=True)
class MethodScriptKbEntry:
    method_name: str
    path: Path
    family: str
    device_hint: str
    source: str


def load_method_script_rows_from_kb(
    method_name: str,
    *,
    family: str = "TCC",
    device_model: str = "",
    kb_root: Path = DEFAULT_PROGRAMDATA_KB_ROOT,
    workspace_root: Path | None = None,
) -> list[CmPreviewRow]:
    entry = find_method_script_kb_entry(
        method_name,
        family=family,
        device_model=device_model,
        kb_root=kb_root,
        workspace_root=workspace_root,
    )
    if not entry:
        return []
    return flow_tsv_to_cm_preview_rows(entry.path)


def find_method_script_kb_entry(
    method_name: str,
    *,
    family: str = "TCC",
    device_model: str = "",
    kb_root: Path = DEFAULT_PROGRAMDATA_KB_ROOT,
    workspace_root: Path | None = None,
) -> MethodScriptKbEntry | None:
    wanted = _norm_method_name(method_name)
    if not wanted:
        return None
    candidates = list(_iter_method_script_entries(family=family, kb_root=kb_root, workspace_root=workspace_root))
    exact = [entry for entry in candidates if _norm_method_name(entry.method_name) == wanted]
    if exact:
        return _best_device_entry(exact, device_model)
    contains = [entry for entry in candidates if wanted in _norm_method_name(entry.method_name) or _norm_method_name(entry.method_name) in wanted]
    if contains:
        return _best_device_entry(contains, device_model)
    return None


def flow_tsv_to_cm_preview_rows(path: Path) -> list[CmPreviewRow]:
    rows: list[CmPreviewRow] = []
    last_time = ""
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        for index, row in enumerate(csv.DictReader(handle, delimiter="\t")):
            action = row.get("Action", "")
            row_time = row.get("Time", "")
            display_time = ""
            if action == "STAGE":
                stage_name = _stage_display_name(row.get("Value", "") or row.get("Stage", ""))
                display_time = row_time or ("{Initial Time}" if stage_name == "Instrument Setup" else "")
                last_time = display_time
            elif action not in {"IF", "ELSE IF", "ELSE", "END IF"} and row_time and row_time != last_time:
                display_time = row_time
                last_time = row_time
            preview_row = _flow_dict_to_cm_preview_row(index, row, display_time)
            if preview_row is not None:
                rows.append(preview_row)
    return rows


def _iter_method_script_entries(
    *,
    family: str,
    kb_root: Path,
    workspace_root: Path | None,
) -> Iterable[MethodScriptKbEntry]:
    roots: list[tuple[Path, str]] = []
    roots.append((Path(kb_root) / "CMBX Method Scripts" / family, "programdata_kb"))
    if workspace_root is not None:
        roots.append((Path(workspace_root) / "knowledge_base" / "tcc_reverse_probe", "legacy_workspace_probe"))
    for root, source in roots:
        if not root.exists():
            continue
        for path in root.rglob("*_embedded_method_flow.tsv"):
            yield MethodScriptKbEntry(
                method_name=_method_name_from_flow_path(path),
                path=path,
                family=family,
                device_hint=_device_hint_from_path(path),
                source=source,
            )


def _flow_dict_to_cm_preview_row(index: int, row: dict[str, str], display_time: str) -> CmPreviewRow | None:
    action = row.get("Action", "")
    level = _int_or_zero(row.get("Level", ""))
    indent = "    " * max(0, level)
    target = row.get("Target", "")
    value = row.get("Value", "")
    comment = row.get("Comment", "")
    condition = _clean_branch_condition(row.get("Condition", ""))
    if action == "STAGE":
        stage_name = _stage_display_name(value or row.get("Stage", ""))
        time_value = display_time or row.get("Time", "") or ("{Initial Time}" if stage_name == "Instrument Setup" else "")
        return (str(index), "Stage", time_value, stage_name, comment, "", "cm_initial")
    if action == "COMMENT":
        return (str(index), "Comment", display_time, f"{indent}{comment}", "", "", "cm_comment")
    if action == "IF":
        if not condition and row.get("NodeType") == "IfBlockNode":
            return None
        return (str(index), "Branch", f"{indent}If", "", condition, "", "cm_condition")
    if action == "ELSE IF":
        return (str(index), "Branch", f"{indent}Else If", "", condition, "", "cm_condition")
    if action == "ELSE":
        return (str(index), "Branch", f"{indent}Else", "", "", "cm_condition")
    if action == "END IF":
        return (str(index), "Branch", f"{indent}End If", "", "", "cm_condition")
    if action == "END":
        return (str(index), "End", display_time, "End", "", "", "")
    tag = _cm_method_tag(display_time, target, value, comment)
    return (str(index), "Command", display_time, f"{indent}{target}", value, comment, tag)


def _clean_branch_condition(condition: str) -> str:
    text = str(condition or "").strip()
    if not text:
        return ""
    model_match = re.search(r'ColumnComp\.ModelNo\s*=\s*"[^"]+"', text)
    if model_match:
        return model_match.group(0)
    starters = (
        "ColumnComp.",
        "Variables.",
        "System.",
        "TempVars.",
        "StabVars.",
        "RetTimes.",
        "Thermometer.",
    )
    positions = [text.rfind(starter) for starter in starters]
    start = max(positions)
    if start > 0:
        text = text[start:].strip()
    return text


def _cm_method_tag(time_text: str, command: str, value: str, comment: str) -> str:
    lower_time = (time_text or "").lower()
    lower_command = (command or "").lower()
    lower_value = (value or "").lower()
    if "{initial time}" in lower_time or lower_command == "equilibration":
        return "cm_initial"
    if lower_time in {"if", "else if", "else", "end if", "trigger", "end trigger"}:
        return "cm_condition"
    if command.startswith("=") or (command.startswith("-") and not value):
        return "cm_header"
    if comment and not command and not value:
        return "cm_comment"
    if "system.trigger" in lower_command or lower_value.startswith("columncomp.modelno"):
        return "cm_condition"
    return ""


def _method_name_from_flow_path(path: Path) -> str:
    name = path.name
    suffix = "_embedded_method_flow.tsv"
    return name[: -len(suffix)] if name.endswith(suffix) else path.stem


def _device_hint_from_path(path: Path) -> str:
    parts = [part.upper() for part in path.parts]
    for part in parts:
        if part in {"VH", "VC", "VA"}:
            return part
        if "VH" in part and "TCC" in part:
            return "VH"
        if "VC" in part and "TCC" in part:
            return "VC"
        if "VA" in part and "TCC" in part:
            return "VA"
    return ""


def _best_device_entry(entries: list[MethodScriptKbEntry], device_model: str) -> MethodScriptKbEntry:
    device = (device_model or "").upper()
    for prefix in ("VH", "VC", "VA"):
        if device.startswith(prefix):
            preferred = [entry for entry in entries if entry.device_hint == prefix]
            if preferred:
                return sorted(preferred, key=lambda item: len(str(item.path)))[0]
    return sorted(entries, key=lambda item: len(str(item.path)))[0]


def _stage_display_name(stage: str) -> str:
    text = str(stage or "")
    return "Instrument Setup" if text == "InstrumentSetup" else text


def _norm_method_name(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", str(value or "").lower()).strip("_")


def _int_or_zero(value: str) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0
