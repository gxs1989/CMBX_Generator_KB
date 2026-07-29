from __future__ import annotations

import csv
import hashlib
import math
import re
import statistics
import tempfile
import time
from collections import deque
from dataclasses import dataclass
from dataclasses import replace
from pathlib import Path
from typing import Callable, Iterable

from cmbx_container import (
    CmbxElement,
    CmbxPackage,
    element_path,
    extract_cmbx_entry,
    load_cmbx_package,
    safe_filename,
)
from chromeleon_bridge import export_signal_raw
from embedded_report_extractor import decode_report_template_xml, parse_report_sheet_objects
from formulaone_report_exporter import extract_formulaone_spreadsheet_data
from formulaone_workbook_writer import read_formulaone_formula_inventory
from report_formula_evaluator import (
    SignalPoint,
    evaluate_external_report_formula,
    read_signal_tsv,
)


@dataclass(frozen=True)
class WorksetPackage:
    package: CmbxPackage
    package_type: str


@dataclass(frozen=True)
class InjectionRecord:
    package: CmbxPackage
    sequence: CmbxElement
    injection: CmbxElement

    @property
    def key(self) -> str:
        return f"{self.package.path}|{self.sequence.id}|{self.injection.id}"


@dataclass(frozen=True)
class ChannelRecord:
    package: CmbxPackage
    sequence: CmbxElement
    injection: CmbxElement
    channel: CmbxElement

    @property
    def key(self) -> str:
        return f"{self.package.path}|{self.sequence.id}|{self.injection.id}|{self.channel.id}"

    @property
    def label(self) -> str:
        return f"{self.package.path.stem} / {self.sequence.name} / {self.injection.name} / {self.channel.name}"


@dataclass(frozen=True)
class FormulaResult:
    package: str
    sequence: str
    injection: str
    formula: str
    fixed_channel: str
    value: str
    status: str
    detail: str


@dataclass(frozen=True)
class FormulaRecord:
    package: CmbxPackage
    report_name: str
    sheet_name: str
    excel_range: str
    object_type: str
    formula: str
    fixed_channel: str
    fixed_component: str
    engine: str = "Direct CM"
    source_scope: str = ""
    support: str = ""

    @property
    def key(self) -> str:
        return "|".join((str(self.package.path), self.report_name, self.sheet_name, self.excel_range, self.formula, self.fixed_channel, self.engine))

    @property
    def meaning(self) -> str:
        return describe_cm_formula(self.formula, self.fixed_channel, self.fixed_component)

    @property
    def source_label(self) -> str:
        return self.source_scope or self.package.path.name


@dataclass(frozen=True)
class FormulaScanProgress:
    completed: int
    total: int
    package: str
    report: str
    formulas_found: int
    elapsed_s: float
    eta_s: float | None


@dataclass(frozen=True)
class IntegrationSettings:
    baseline_noise_start_min: float | None = None
    baseline_noise_end_min: float | None = None
    smoothing_width_s: float = 1.0
    noise_multiplier: float = 5.0
    minimum_height: float = 0.0
    minimum_area: float = 0.0
    minimum_width_s: float = 0.0
    detect_negative: bool = False


@dataclass(frozen=True)
class PeakResult:
    trace_key: str
    peak_index: int
    start_min: float
    apex_min: float
    end_min: float
    height: float
    area: float
    width_s: float
    polarity: str
    baseline_start: float
    baseline_end: float


def discover_cmbx_paths(sources: Iterable[str | Path]) -> list[Path]:
    paths: list[Path] = []
    for source in sources:
        path = Path(source).expanduser()
        if path.is_file() and path.suffix.lower() == ".cmbx":
            paths.append(path.resolve())
        elif path.is_dir():
            for candidate in path.rglob("*.cmbx"):
                relative_parts = candidate.relative_to(path).parts[:-1]
                if any(part.lower() == "deleted" for part in relative_parts):
                    continue
                paths.append(candidate.resolve())
    return sorted(dict.fromkeys(paths), key=lambda item: str(item).lower())


def load_workset(paths: Iterable[str | Path]) -> tuple[list[WorksetPackage], list[tuple[Path, str]]]:
    loaded: list[WorksetPackage] = []
    errors: list[tuple[Path, str]] = []
    for value in paths:
        path = Path(value)
        try:
            package = load_cmbx_package(path)
            loaded.append(WorksetPackage(package, classify_package(package)))
        except Exception as exc:
            errors.append((path, str(exc)))
    return loaded, errors


def classify_package(package: CmbxPackage) -> str:
    if package.channels or package.audits:
        return "Runtime data"
    if package.sequences and package.injections:
        return "Sequence template"
    if package.methods_and_reports:
        return "Standalone asset"
    return "Structure only"


def injection_records(packages: Iterable[WorksetPackage | CmbxPackage]) -> list[InjectionRecord]:
    records: list[InjectionRecord] = []
    for item in packages:
        package = item.package if isinstance(item, WorksetPackage) else item
        for injection in package.injections:
            sequence = _ancestor_of_kind(package, injection, "sequence")
            if sequence is not None:
                records.append(InjectionRecord(package, sequence, injection))
    return records


def channel_records(packages: Iterable[WorksetPackage | CmbxPackage]) -> list[ChannelRecord]:
    records: list[ChannelRecord] = []
    for item in packages:
        package = item.package if isinstance(item, WorksetPackage) else item
        for channel in package.channels:
            injection = _ancestor_of_kind(package, channel, "injection")
            sequence = _ancestor_of_kind(package, channel, "sequence")
            if injection is not None and sequence is not None:
                records.append(ChannelRecord(package, sequence, injection, channel))
    return records


def unique_channel_names(records: Iterable[ChannelRecord]) -> list[str]:
    values = {record.channel.name for record in records if record.channel.name}
    return sorted(values, key=str.lower)


def match_channel_records(
    records: Iterable[ChannelRecord], channel_name: str, *, exact: bool = True
) -> list[ChannelRecord]:
    needle = channel_name.strip().casefold()
    if not needle:
        return list(records)
    if exact:
        return [record for record in records if record.channel.name.casefold() == needle]
    return [record for record in records if needle in record.channel.name.casefold()]


def filter_channel_records(
    records: Iterable[ChannelRecord], *, package: str = "", sequence: str = "",
    injection: str = "", channel: str = "",
) -> list[ChannelRecord]:
    filters = (package.casefold().strip(), sequence.casefold().strip(), injection.casefold().strip(), channel.casefold().strip())
    return [
        record for record in records
        if (not filters[0] or filters[0] in record.package.path.name.casefold())
        and (not filters[1] or filters[1] in record.sequence.name.casefold())
        and (not filters[2] or filters[2] in record.injection.name.casefold())
        and (not filters[3] or filters[3] in record.channel.name.casefold())
    ]


def formula_records(
    packages: Iterable[WorksetPackage | CmbxPackage], *, include_formulaone: bool = False,
    progress: Callable[[FormulaScanProgress], None] | None = None,
) -> tuple[list[FormulaRecord], list[tuple[str, str]]]:
    records: list[FormulaRecord] = []
    errors: list[tuple[str, str]] = []
    sources = _formula_report_sources(packages)
    total = len(sources)
    started = time.perf_counter()
    for completed, (package, report) in enumerate(sources, start=1):
        if progress is not None:
            elapsed = time.perf_counter() - started
            progress(FormulaScanProgress(
                completed - 1, total, package.path.name, report.name, len(records), elapsed, None,
            ))
        try:
            _embedded, xml_text = decode_report_template_xml(package, report)
            objects = parse_report_sheet_objects(xml_text, report.name)
        except Exception as exc:
            errors.append((f"{package.path.name} / {report.name}", str(exc)))
        else:
            for obj in objects:
                if not obj.formula.strip():
                    continue
                records.append(FormulaRecord(
                    package, report.name, obj.sheet_name, obj.excel_range, obj.object_type,
                    obj.formula.strip(), obj.fixed_channel, obj.fixed_component,
                ))
            if include_formulaone:
                try:
                    workbook_rows = read_formulaone_formula_inventory(extract_formulaone_spreadsheet_data(xml_text))
                except Exception as exc:
                    errors.append((f"{package.path.name} / {report.name} / FormulaOne", str(exc)))
                else:
                    for row in workbook_rows:
                        formula = str(row.get("formula", "")).strip()
                        if not formula:
                            continue
                        sheet_name = str(row.get("sheet", ""))
                        excel_range = _excel_address(int(row.get("row", 0)), int(row.get("column", 0)))
                        records.append(FormulaRecord(
                            package, report.name, sheet_name, excel_range, "FormulaOneCell",
                            formula, "", "", "FormulaOne",
                        ))
        if progress is not None:
            elapsed = time.perf_counter() - started
            eta = (elapsed / completed) * (total - completed) if completed and completed < total else 0.0
            progress(FormulaScanProgress(
                completed, total, package.path.name, report.name, len(records), elapsed, eta,
            ))
    unique = {record.key: record for record in records}
    return sorted(unique.values(), key=lambda row: (row.package.path.name.casefold(), row.report_name.casefold(), row.sheet_name.casefold(), row.excel_range)), errors


def _formula_report_sources(
    packages: Iterable[WorksetPackage | CmbxPackage],
) -> list[tuple[CmbxPackage, CmbxElement]]:
    """List logical report sources without hashing payloads that Direct CM does not need."""
    sources: list[tuple[CmbxPackage, CmbxElement]] = []
    for item in packages:
        package = item.package if isinstance(item, WorksetPackage) else item
        seen: set[tuple[str, str]] = set()
        reports = (element for element in package.elements_by_id.values() if element.kind == "report_template")
        for report in reports:
            source = report.package_entry_name.casefold() if report.package_entry_name else report.id
            key = (report.name.casefold(), source)
            if key in seen:
                continue
            seen.add(key)
            sources.append((package, report))
    return sources


def decode_channel_points(record: ChannelRecord) -> list[SignalPoint]:
    cache = _signal_cache(record)
    cache.mkdir(parents=True, exist_ok=True)
    raw_name = record.channel.raw_filename
    if not raw_name:
        raise ValueError(f"Channel has no raw payload: {record.label}")
    raw_path = cache / safe_filename(Path(raw_name).name, "signal.raw")
    if not raw_path.exists():
        raw_path.write_bytes(extract_cmbx_entry(record.package.path, raw_name))
    output = cache / f"{safe_filename(record.channel.name)}.tsv"
    if not output.exists() or output.stat().st_mtime < raw_path.stat().st_mtime:
        export_signal_raw(raw_path, output, record.channel.name)
    return read_signal_tsv(output)


def export_channel_records(
    records: Iterable[ChannelRecord], output_folder: str | Path
) -> tuple[list[Path], list[tuple[ChannelRecord, str]]]:
    output = Path(output_folder)
    output.mkdir(parents=True, exist_ok=True)
    exported: list[Path] = []
    errors: list[tuple[ChannelRecord, str]] = []
    manifest_rows: list[list[str]] = []
    for index, record in enumerate(records, start=1):
        name = safe_filename(
            f"{index:04d}_{record.package.path.stem}_{record.sequence.name}_{record.injection.name}_{record.channel.name}"
        )
        target = output / f"{name}.tsv"
        try:
            points = decode_channel_points(record)
            with target.open("w", encoding="utf-8-sig", newline="") as stream:
                writer = csv.writer(stream, delimiter="\t")
                writer.writerow(["Package", "Sequence", "Injection", "Channel", "Time_min", "Value"])
                for point in points:
                    writer.writerow([
                        str(record.package.path), record.sequence.name, record.injection.name,
                        record.channel.name, f"{point.time_min:.12g}", f"{point.value:.15g}",
                    ])
            exported.append(target)
            manifest_rows.append([
                target.name, str(record.package.path), record.sequence.name,
                record.injection.name, record.channel.name, str(len(points)), "ok", "",
            ])
        except Exception as exc:
            errors.append((record, str(exc)))
            manifest_rows.append([
                target.name, str(record.package.path), record.sequence.name,
                record.injection.name, record.channel.name, "0", "error", str(exc),
            ])
    manifest = output / "raw_data_manifest.csv"
    with manifest.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["File", "Package", "Sequence", "Injection", "Channel", "Points", "Status", "Detail"])
        writer.writerows(manifest_rows)
    return exported, errors


def evaluate_formula_records(
    records: Iterable[InjectionRecord], formula: str, fixed_channel: str = ""
) -> list[FormulaResult]:
    results: list[FormulaResult] = []
    for record in records:
        try:
            value, status, detail = evaluate_external_report_formula(
                record.package, record.injection, formula, fixed_channel,
            )
        except Exception as exc:
            value, status, detail = "", "error", str(exc)
        results.append(FormulaResult(
            record.package.path.name, record.sequence.name, record.injection.name,
            formula, fixed_channel, value, status, detail,
        ))
    return results


def evaluate_formula_batch(
    contexts: Iterable[InjectionRecord], formulas: Iterable[FormulaRecord]
) -> list[FormulaResult]:
    results: list[FormulaResult] = []
    for formula in formulas:
        for context in contexts:
            if formula.engine != "Direct CM":
                results.append(FormulaResult(
                    context.package.path.name, context.sequence.name, context.injection.name,
                    formula.formula, formula.fixed_channel, "", "workbook-context-required",
                    f"{formula.report_name} / {formula.sheet_name} / {formula.excel_range}: "
                    "FormulaOne cell formula was discovered, but batch recalculation needs a populated workbook context.",
                ))
                continue
            try:
                value, status, detail = evaluate_external_report_formula(
                    context.package, context.injection, formula.formula, formula.fixed_channel,
                )
            except Exception as exc:
                value, status, detail = "", "error", str(exc)
            results.append(FormulaResult(
                context.package.path.name, context.sequence.name, context.injection.name,
                formula.formula, formula.fixed_channel, value, status,
                f"{formula.report_name} / {formula.sheet_name} / {formula.excel_range}: {detail}",
            ))
    return results


def integrate_signal(
    trace_key: str, points: list[SignalPoint], settings: IntegrationSettings
) -> list[PeakResult]:
    """External Cobra-inspired peak detection; it does not reproduce CM Processing Method byte-for-byte."""
    if len(points) < 5:
        return []
    times = [point.time_min for point in points]
    values = [point.value for point in points]
    intervals = [right - left for left, right in zip(times, times[1:]) if right > left]
    if not intervals:
        return []
    dt = statistics.median(intervals)
    width_points = max(1, int(round(max(settings.smoothing_width_s, 0.0) / 60.0 / dt)))
    smoothed = _moving_average(values, width_points)
    baseline_window = max(width_points * 30, 31)
    baseline = _rolling_minimum(smoothed, baseline_window)
    residual = [value - base for value, base in zip(smoothed, baseline)]
    signed = residual
    noise_residual = residual
    if (
        settings.baseline_noise_start_min is not None
        and settings.baseline_noise_end_min is not None
        and settings.baseline_noise_end_min > settings.baseline_noise_start_min
    ):
        noise_residual = [
            value for time, value in zip(times, residual)
            if settings.baseline_noise_start_min <= time <= settings.baseline_noise_end_min
        ]
    differences = [right - left for left, right in zip(noise_residual, noise_residual[1:])]
    median_difference = statistics.median(differences) if differences else 0.0
    mad = statistics.median(abs(value - median_difference) for value in differences) if differences else 0.0
    noise = mad / 0.67448975 / math.sqrt(2.0) if mad else statistics.pstdev(differences) / math.sqrt(2.0) if len(differences) > 1 else 0.0
    threshold = max(noise * max(settings.noise_multiplier, 0.0), settings.minimum_height, 1e-15)
    active = [abs(value) >= threshold if settings.detect_negative else value >= threshold for value in signed]
    support_threshold = threshold * 0.1
    support = [abs(value) >= support_threshold if settings.detect_negative else value >= support_threshold for value in signed]
    active_prefix = [0]
    for state in active:
        active_prefix.append(active_prefix[-1] + int(state))
    regions: list[tuple[int, int]] = []
    start = None
    for index, state in enumerate(support):
        if state and start is None:
            start = index
        elif not state and start is not None:
            end = index - 1
            if active_prefix[end + 1] - active_prefix[start]:
                regions.append((start, end))
            start = None
    if start is not None:
        end = len(active) - 1
        if active_prefix[end + 1] - active_prefix[start]:
            regions.append((start, end))
    peaks: list[PeakResult] = []
    for start, end in regions:
        width_s = max(0.0, (times[end] - times[start]) * 60.0)
        if width_s < settings.minimum_width_s:
            continue
        polarity = "negative" if min(residual[start:end + 1]) < -max(residual[start:end + 1]) else "positive"
        apex = min(range(start, end + 1), key=lambda i: smoothed[i]) if polarity == "negative" else max(range(start, end + 1), key=lambda i: smoothed[i])
        height = abs(residual[apex])
        area = 0.0
        for index in range(start, end):
            left = abs(residual[index]) if settings.detect_negative else max(residual[index], 0.0)
            right = abs(residual[index + 1]) if settings.detect_negative else max(residual[index + 1], 0.0)
            area += (left + right) * 0.5 * (times[index + 1] - times[index])
        if height < settings.minimum_height or area < settings.minimum_area:
            continue
        peaks.append(PeakResult(
            trace_key, len(peaks) + 1, times[start], times[apex], times[end],
            height, area, width_s, polarity, baseline[start], baseline[end],
        ))
    return peaks


def describe_cm_formula(formula: str, fixed_channel: str = "", fixed_component: str = "") -> str:
    expression = formula.strip()
    lowered = expression.casefold()
    source = f"通道 {fixed_channel}" if fixed_channel else "当前/报告绑定通道"
    component = f"；component: {fixed_component}" if fixed_component else ""
    statistic = re.search(r'chm\.sig_value\(\s*["\']([^"\']+)', expression, re.IGNORECASE)
    if statistic:
        operation = statistic.group(1)
        return f"在公式指定的时间窗口内，对{source}计算 {operation} 信号统计值{component}。"
    if lowered.startswith("chm.signalstatistic"):
        return f"在指定时间窗口内读取{source}的信号统计量{component}。"
    if lowered.startswith("chm.signalvalue"):
        return f"读取{source}在指定保留时间处的信号值{component}。"
    if lowered.startswith("chm.noise"):
        return f"计算{source}在指定时间窗口内的基线噪声。"
    if lowered.startswith("chm.drift"):
        return f"计算{source}在指定时间窗口内的线性漂移斜率。"
    if lowered.startswith("chm.channel"):
        return f"返回或标识报告当前使用的 channel（{source}）。"
    if lowered.startswith("audit.rettime"):
        match = re.match(r"audit\.(rettime\d+)", expression, re.IGNORECASE)
        return f"从 injection audit trail 读取 {match.group(1) if match else 'RetTime'} 时间锚点。"
    if lowered.startswith("audit."):
        path = expression.split("(", 1)[0][6:]
        return f"从 injection audit trail 按时间方向读取属性 {path}。"
    if lowered.startswith("precond."):
        return f"读取 injection 开始时的设备 precondition 属性 {expression[8:].split('(', 1)[0]}。"
    for namespace, label in (("seq.", "sequence"), ("smp.", "sample"), ("injection.", "injection"), ("gen.", "general/report")):
        if lowered.startswith(namespace):
            return f"读取 {label} metadata：{expression.split('(', 1)[0]}。"
    if lowered.startswith("peak.") or lowered.startswith("comp."):
        return f"读取 Processing Method 产生的 peak/component 结果{component}。"
    namespace = expression.split(".", 1)[0] if "." in expression else "CM"
    return f"Direct CM {namespace} 公式；具体返回值由公式表达式和当前 injection context 决定{component}。"


def adapt_integration_settings(
    point_sets: Iterable[list[SignalPoint]], settings: IntegrationSettings
) -> IntegrationSettings:
    """Adapt sampling-dependent parameters once for a group of traces."""
    interval_seconds: list[float] = []
    for points in point_sets:
        if len(points) < 2:
            continue
        stride = max(1, (len(points) - 1) // 5000)
        for index in range(0, len(points) - stride, stride):
            interval = (points[index + stride].time_min - points[index].time_min) * 60.0 / stride
            if interval > 0:
                interval_seconds.append(interval)
    if not interval_seconds:
        return settings
    sampling_interval = statistics.median(interval_seconds)
    return replace(
        settings,
        smoothing_width_s=max(settings.smoothing_width_s, sampling_interval * 3.0),
        minimum_width_s=max(settings.minimum_width_s, sampling_interval * 3.0),
    )


def _moving_average(values: list[float], width: int) -> list[float]:
    if width <= 1:
        return list(values)
    half = width // 2
    prefix = [0.0]
    for value in values:
        prefix.append(prefix[-1] + value)
    result = []
    for index in range(len(values)):
        left = max(0, index - half); right = min(len(values), index + half + 1)
        result.append((prefix[right] - prefix[left]) / (right - left))
    return result


def _rolling_minimum(values: list[float], width: int) -> list[float]:
    half = max(1, width // 2)
    candidates: deque[int] = deque()
    result: list[float] = []
    right = -1
    for index in range(len(values)):
        target_right = min(len(values) - 1, index + half)
        while right < target_right:
            right += 1
            while candidates and values[candidates[-1]] >= values[right]:
                candidates.pop()
            candidates.append(right)
        left = max(0, index - half)
        while candidates and candidates[0] < left:
            candidates.popleft()
        result.append(values[candidates[0]])
    return result


def _excel_address(row: int, column: int) -> str:
    if row < 1 or column < 1:
        return ""
    letters = ""
    while column:
        column, remainder = divmod(column - 1, 26)
        letters = chr(65 + remainder) + letters
    return f"{letters}{row}"


def _ancestor_of_kind(
    package: CmbxPackage, element: CmbxElement, kind: str
) -> CmbxElement | None:
    return next((candidate for candidate in reversed(element_path(package, element)) if candidate.kind == kind), None)


def _signal_cache(record: ChannelRecord) -> Path:
    digest = hashlib.sha1(str(record.package.path.resolve()).encode("utf-8")).hexdigest()[:12]
    return (
        Path(tempfile.gettempdir()) / "CmbxDataExplorer" / "read_analyze" / digest
        / safe_filename(record.sequence.name) / safe_filename(record.injection.name)
    )
