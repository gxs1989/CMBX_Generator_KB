from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import Iterable, Sequence

from method_semantic_analyzer import cm_method_row_text


CmMethodRow = Sequence[object]
DEFAULT_ROLE_MAP_PATH = Path(__file__).resolve().parent / "docs" / "TCC_METHOD_ROLE_MAP.json"


@dataclass(frozen=True)
class MethodRoleMatch:
    row_index: int
    row_number: str
    role_id: str
    label: str
    edit_status: str
    reason: str


@dataclass(frozen=True)
class MethodRoleMapAudit:
    kb_path: Path
    kb_version: str
    method_name: str
    test_intent: str
    status: str
    summary: str
    matches: tuple[MethodRoleMatch, ...]
    missing_required_roles: tuple[str, ...]
    generation_mode: str

    def role_counts(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for match in self.matches:
            counts[match.role_id] = counts.get(match.role_id, 0) + 1
        return counts


def classify_method_role_map(
    rows: Iterable[CmMethodRow],
    *,
    family: str,
    method_name: str,
    test_intent: str,
    device_model: str = "",
    kb_path: Path = DEFAULT_ROLE_MAP_PATH,
) -> MethodRoleMapAudit:
    row_list = [tuple(row) for row in rows]
    data = _load_role_map(kb_path)
    family_data = data.get("families", {}).get(family, {})
    method_data = _resolve_method_contract(family_data, method_name=method_name, test_intent=test_intent)
    if not method_data:
        return MethodRoleMapAudit(
            kb_path=kb_path,
            kb_version=str(data.get("version", "")),
            method_name=method_name,
            test_intent=test_intent,
            status="missing",
            summary="No Method Role Map contract matched this method/test intent.",
            matches=(),
            missing_required_roles=(),
            generation_mode="blocked",
        )

    roles = method_data.get("roles", [])
    matches: list[MethodRoleMatch] = []
    for row_index, row in enumerate(row_list):
        for role in roles:
            if _row_matches_role(row_list, row_index, role, device_model=device_model):
                matches.append(
                    MethodRoleMatch(
                        row_index=row_index,
                        row_number=cm_method_row_text(row, 0),
                        role_id=str(role.get("id", "")),
                        label=str(role.get("label", role.get("id", ""))),
                        edit_status=str(role.get("edit_status", "review")),
                        reason=str(role.get("reason", "")),
                    )
                )
                break

    counts: dict[str, int] = {}
    for match in matches:
        counts[match.role_id] = counts.get(match.role_id, 0) + 1
    required = tuple(str(item) for item in method_data.get("required_roles_for_generation", ()))
    missing = tuple(role_id for role_id in required if counts.get(role_id, 0) == 0)
    if missing:
        status = "blocked"
        generation_mode = "blocked"
        summary = "Role Map incomplete: missing " + ", ".join(missing)
    else:
        status = "complete"
        generation_mode = str(method_data.get("generation_mode", "role_map_preview"))
        summary = _role_map_summary(counts)
    return MethodRoleMapAudit(
        kb_path=kb_path,
        kb_version=str(data.get("version", "")),
        method_name=str(method_data.get("method_name", method_name)),
        test_intent=test_intent,
        status=status,
        summary=summary,
        matches=tuple(matches),
        missing_required_roles=missing,
        generation_mode=generation_mode,
    )


def _load_role_map(path: Path) -> dict:
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {"version": "", "families": {}}


def _resolve_method_contract(family_data: dict, *, method_name: str, test_intent: str) -> dict | None:
    normalized_method = _norm(method_name)
    normalized_intent = _norm(test_intent)
    methods = family_data.get("methods", {})
    for contract in methods.values():
        if _norm(str(contract.get("method_name", ""))) == normalized_method:
            return contract
    for contract in methods.values():
        intents = {_norm(str(item)) for item in contract.get("test_intents", [])}
        if normalized_intent in intents:
            return contract
    return None


def _row_matches_role(rows: list[tuple[object, ...]], row_index: int, role: dict, *, device_model: str) -> bool:
    row = rows[row_index]
    kind = cm_method_row_text(row, 1)
    time = cm_method_row_text(row, 2)
    command = cm_method_row_text(row, 3)
    value = cm_method_row_text(row, 4)
    comment = cm_method_row_text(row, 5)
    text = " ".join((kind, time, command, value, comment))

    if role.get("special") == "final_reset":
        return _is_final_reset(rows, row_index)
    if role.get("special") == "device_branch":
        prefix = (device_model or "").split("-", 1)[0].upper()
        return kind == "Branch" and "ColumnComp.ModelNo" in value and (not prefix or prefix in value.upper())

    expected_kind = role.get("kind")
    if expected_kind and kind != expected_kind:
        return False
    for key, source in (("time_contains", time), ("command_contains", command), ("value_contains", value), ("comment_contains", comment), ("text_contains", text)):
        needle = role.get(key)
        if needle and str(needle).lower() not in source.lower():
            return False
    for key, source in (("time_regex", time), ("command_regex", command), ("value_regex", value), ("comment_regex", comment), ("text_regex", text)):
        pattern = role.get(key)
        if pattern and not re.search(str(pattern), source, flags=re.I):
            return False
    return True


def _is_final_reset(rows: list[tuple[object, ...]], row_index: int) -> bool:
    row = rows[row_index]
    command = cm_method_row_text(row, 3).lower()
    value = cm_method_row_text(row, 4).lower()
    if "columncomp.cc.temperature.nominal" not in command:
        return False
    if "variables." in value:
        return False
    last_ret_time = -1
    for index, candidate in enumerate(rows):
        candidate_command = cm_method_row_text(candidate, 3).lower()
        candidate_value = cm_method_row_text(candidate, 4).lower()
        if "rettimes.rettime" in candidate_command and "system.retention" in candidate_value:
            last_ret_time = index
    return row_index > last_ret_time >= 0


def _role_map_summary(counts: dict[str, int]) -> str:
    return "; ".join(f"{role_id}={count}" for role_id, count in sorted(counts.items())) or "No roles matched."


def _norm(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", str(value or "").lower()).strip("_")
