from __future__ import annotations

import re
from typing import Any, Iterable

from read_analyze_service import ChannelRecord, SignalPoint


def parse_leak_metadata(*labels: str) -> tuple[str, str]:
    text = " ".join(labels)
    upper = text.upper()
    liquid = "IPA" if "IPA" in upper else "MeOH" if "MEOH" in upper else "Water" if "WATER" in upper else ""
    match = re.search(r"(?<!\d)(\d{2})\s*°?\s*C(?![A-Za-z])", text, re.IGNORECASE)
    # Accept plain ``25C`` plus degree/word variants; this supersedes legacy mojibake input.
    normalized_match = re.search(
        r"(?<!\d)(\d{2})\s*(?:\N{DEGREE SIGN}|deg(?:ree)?s?)?\s*C(?![A-Za-z])",
        text,
        re.IGNORECASE,
    )
    condition_match = re.search(
        r"(?:water|meoh|ipa)[_\-\s]+(\d{2})(?:\s*(?:\N{DEGREE SIGN}|deg(?:ree)?s?)?\s*C)?(?:\b|_)",
        text,
        re.IGNORECASE,
    )
    temperature = (
        condition_match.group(1)
        if condition_match
        else normalized_match.group(1)
        if normalized_match
        else match.group(1)
        if match
        else ""
    )
    # IPA and MeOH leak tests are room-temperature conditions. Numeric
    # temperatures embedded in legacy names are labels, not separate groups.
    if liquid in {"IPA", "MeOH"}:
        temperature = "RT"
    return liquid, temperature


def leak_group_key(liquid: str, temperature: str) -> str:
    condition = temperature if temperature == "RT" else f"{temperature}C" if temperature else "-"
    return f"{liquid or '-'} | {condition}"


def is_leak_diff_channel(record: ChannelRecord) -> bool:
    normalized = re.sub(r"[^a-z0-9]", "", record.channel.name.casefold())
    return "leakdiff" in normalized


def leak_channel_candidates(records: Iterable[ChannelRecord]) -> tuple[list[ChannelRecord], str]:
    leak_diff = [record for record in records if is_leak_diff_channel(record)]
    focused = [
        record for record in leak_diff
        if "leak" in record.injection.name.casefold() or "liquid" in record.injection.name.casefold()
    ]
    if focused:
        return focused, "Liquid-leak injections"
    return leak_diff, "All LeakDiff channels (no liquid-leak injection name was found)"


def serialize_leak_candidate(record: ChannelRecord) -> dict[str, Any]:
    liquid, temp = parse_leak_metadata(
        record.injection.name, record.sequence.name, record.package.path.stem, record.channel.name,
    )
    return {
        "key": record.key,
        "package": record.package.path.name,
        "sequence": record.sequence.name,
        "injection": record.injection.name,
        "channel": record.channel.name,
        "label": record.label,
        "liquid": liquid,
        "temperature_c": temp,
    }


def compute_leak_metrics(record: ChannelRecord, points: list[SignalPoint]) -> dict[str, Any]:
    """Run the V1.1 Leak Sensor Analyzer algorithm on an in-memory CMBX signal."""
    if len(points) < 2:
        raise ValueError("Not enough numeric points")
    t_values = [float(point.time_min) for point in points]
    v_values = [float(point.value) for point in points]

    stable_count = 0
    sum_base = 0.0
    baseline = v_values[0]
    for index in range(1, len(v_values)):
        if abs(v_values[index] - v_values[index - 1]) < 0.5:
            sum_base += v_values[index]
            stable_count += 1
            if stable_count >= 10:
                break
        else:
            stable_count = 0
            sum_base = 0.0
    if stable_count:
        baseline = sum_base / stable_count

    maximum = max(v_values)
    minimum = min(v_values)
    diff_peak = maximum if abs(maximum - baseline) >= abs(minimum - baseline) else minimum
    peak_index = v_values.index(diff_peak)
    t_peak = t_values[peak_index]
    delta_diff = diff_peak - baseline
    direction = 1 if delta_diff >= 0 else -1
    t0 = _find_initial_response_t0(t_values, v_values, baseline, delta_diff)
    if not t0:
        t0 = _find_peak_direction_t0(t_values, v_values, baseline, direction)
    target50 = baseline + 0.5 * delta_diff
    target90 = baseline + 0.9 * delta_diff
    t50 = _first_directional_crossing(t_values, v_values, target50, t0, direction)
    t90 = _first_directional_crossing(t_values, v_values, target90, t0, direction)
    response_t90 = t90 - t0 if t90 and t0 else 0.0
    response_peak = t_peak - t0 if t_peak and t0 else 0.0
    rise_start_time, rise_start_value, rise_slope = _compute_rise_slope(
        t_values, v_values, peak_index, diff_peak,
    )
    liquid, temp = parse_leak_metadata(
        record.injection.name, record.sequence.name, record.package.path.stem, record.channel.name,
    )
    return {
        "key": record.key,
        "file": record.package.path.stem,
        "package": record.package.path.name,
        "sequence": record.sequence.name,
        "injection": record.injection.name,
        "channel": record.channel.name,
        "liquid": liquid,
        "temp": temp,
        "group_key": leak_group_key(liquid, temp),
        "diff_start": baseline,
        "diff_peak": diff_peak,
        "delta_diff": delta_diff,
        "t0": t0,
        "t50": t50,
        "t90": t90,
        "t_peak": t_peak,
        "response_t90": response_t90,
        "response_peak": response_peak,
        "t_rise_start": rise_start_time,
        "rise_start_value": rise_start_value,
        "rise_slope": rise_slope,
        "result": response_peak,
        "performance": abs(delta_diff) / response_t90 / 60 if response_t90 else 0.0,
        "is_benchmark": False,
        "benchmark_ref": "",
        "evaluation": "",
    }


def evaluate_leak_groups(rows: list[dict[str, Any]], benchmark_keys: Iterable[str]) -> list[dict[str, Any]]:
    selected = set(benchmark_keys)
    prepared = [{**row, "is_benchmark": row["key"] in selected} for row in rows]
    benchmarks = [row for row in prepared if row["is_benchmark"]]
    evaluated: list[dict[str, Any]] = []
    for row in prepared:
        result = {
            **row,
            "benchmark_ref": "No matched benchmark",
            "delta_eval": "",
            "response_eval": "",
            "performance_eval": "",
            "evaluation": "",
        }
        match = next((benchmark for benchmark in benchmarks if _same_group(row, benchmark)), None)
        if match:
            result["benchmark_ref"] = match["injection"]
            if row["is_benchmark"]:
                result["evaluation"] = "Benchmark"
            else:
                result["delta_eval"] = "BETTER" if abs(row["delta_diff"]) >= abs(match["delta_diff"]) else "WORSE"
                result["response_eval"] = "BETTER" if row["response_t90"] <= match["response_t90"] else "WORSE"
                ratio = row["performance"] / match["performance"] if match["performance"] else 0.0
                result["performance_eval"] = "BETTER" if ratio >= 1 else "WORSE"
                better = sum(
                    value == "BETTER"
                    for value in (result["delta_eval"], result["response_eval"], result["performance_eval"])
                )
                result["evaluation"] = "BETTER" if better == 3 else "WORSE" if better == 0 else "MIXED"
        evaluated.append(result)
    return evaluated


def marker_payload(row: dict[str, Any], start_time: float = 0.0) -> list[dict[str, Any]]:
    return [
        {"label": "baseline", "x": start_time, "y": row["diff_start"]},
        {"label": "t0", "x": row["t0"], "y": row["diff_start"]},
        {"label": "t50", "x": row["t50"], "y": row["diff_start"] + 0.5 * row["delta_diff"]},
        {"label": "t90", "x": row["t90"], "y": row["diff_start"] + 0.9 * row["delta_diff"]},
        {"label": "peak", "x": row["t_peak"], "y": row["diff_peak"]},
    ]


def _same_group(row: dict[str, Any], benchmark: dict[str, Any]) -> bool:
    row_liquid = str(row.get("liquid") or "").strip().casefold()
    benchmark_liquid = str(benchmark.get("liquid") or "").strip().casefold()
    row_temp = str(row.get("temp") or "").strip()
    benchmark_temp = str(benchmark.get("temp") or "").strip()
    return bool(row_liquid and row_temp) and row_liquid == benchmark_liquid and row_temp == benchmark_temp


def _interpolate_time(t1: float, v1: float, t2: float, v2: float, target: float) -> float:
    return t2 if v2 == v1 else t1 + (target - v1) * (t2 - t1) / (v2 - v1)


def _first_crossing(times: list[float], values: list[float], target: float) -> float:
    for index in range(1, len(values)):
        if (values[index - 1] - target) * (values[index] - target) <= 0:
            return _interpolate_time(times[index - 1], values[index - 1], times[index], values[index], target)
    return 0.0


def _first_directional_crossing(
    times: list[float], values: list[float], target: float, start_time: float, direction: int,
) -> float:
    for index in range(1, len(values)):
        if times[index] < start_time:
            continue
        before = (values[index - 1] - target) * direction
        after = (values[index] - target) * direction
        if before <= 0 <= after:
            return _interpolate_time(times[index - 1], values[index - 1], times[index], values[index], target)
    return 0.0


def _find_initial_response_t0(times: list[float], values: list[float], baseline: float, delta: float) -> float:
    threshold = max(0.5, abs(delta) * 0.05)
    final_direction = 1 if delta >= 0 else -1
    for index in range(1, len(values)):
        deviation = values[index] - baseline
        if deviation * final_direction < threshold:
            continue
        start = index
        while start > 0 and (values[start - 1] - baseline) * final_direction > 0:
            start -= 1
        if start > 0 and (values[start - 1] - baseline) * (values[start] - baseline) <= 0:
            return _interpolate_time(times[start - 1], values[start - 1], times[start], values[start], baseline)
        return times[start]
    return 0.0


def _find_peak_direction_t0(times: list[float], values: list[float], baseline: float, direction: int) -> float:
    for index in range(1, len(values)):
        if direction == 1 and values[index - 1] <= baseline < values[index]:
            return times[index]
        if direction == -1 and values[index - 1] >= baseline > values[index]:
            return times[index]
    return 0.0


def _compute_rise_slope(
    times: list[float], values: list[float], peak_index: int, peak: float,
) -> tuple[float, float, float]:
    if peak_index <= 0:
        return 0.0, 0.0, 0.0
    candidates = range(peak_index + 1)
    start = min(candidates, key=lambda index: values[index]) if peak >= values[0] else max(candidates, key=lambda index: values[index])
    duration = times[peak_index] - times[start]
    return times[start], values[start], (peak - values[start]) / duration if duration > 0 else 0.0
