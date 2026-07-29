from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
import hashlib
import json
import os
import re
import shutil
from pathlib import Path

from method_md_linter import lint_method_rows
from report_template_md_compiler import (
    ReportTemplateMdSpec,
    compile_report_template_md_to_cmbx,
    parse_report_template_md,
    prepare_report_template_md,
)
from tools.compile_method_md_to_standalone_cmbx import compile_method_md_to_cmbx
from tools.render_cm_method_md import parse_md_to_rows


DEFAULT_WORKSPACE = Path(
    os.environ.get("CMBX_DATA_EXPLORER_WORKSPACE", "")
    or Path(os.environ.get("PROGRAMDATA", r"C:\ProgramData")) / "CMBX Data Explorer Workspace"
)
DEFAULT_PROJECT_ROOT = DEFAULT_WORKSPACE / "generation_projects"
DEFAULT_METHOD_CARRIERS = (
    DEFAULT_WORKSPACE / "KB" / "FOQ Template" / "TEMPERATURE_CALIBRATION_720.cmbx",
    DEFAULT_WORKSPACE / "KB" / "FOQ Template" / "TEMP_HEAT_UP_DOWN_20_50_20.cmbx",
)
DEFAULT_REPORT_SEARCH_ROOTS = (
    DEFAULT_WORKSPACE / "KB" / "Method Script Generator" / "TCC" / "report_template_cmbx",
    DEFAULT_WORKSPACE / "KB" / "FOQ Template",
)


@dataclass(frozen=True)
class ContractFinding:
    level: str
    item: str
    detail: str


@dataclass
class GenerationPreflight:
    method_path: Path | None = None
    report_path: Path | None = None
    method_sha256: str = ""
    report_sha256: str = ""
    method_rows: list[dict[str, str]] = field(default_factory=list)
    method_issues: list[object] = field(default_factory=list)
    report_spec: ReportTemplateMdSpec | None = None
    report_errors: list[str] = field(default_factory=list)
    report_warnings: list[str] = field(default_factory=list)
    findings: list[ContractFinding] = field(default_factory=list)

    @property
    def method_ready(self) -> bool:
        return bool(self.method_rows) and not any(getattr(item, "severity", "") == "error" for item in self.method_issues)

    @property
    def report_ready(self) -> bool:
        return self.report_spec is not None and not self.report_errors

    @property
    def contract_ready(self) -> bool:
        return not any(item.level == "blocked" for item in self.findings)

    @property
    def ready(self) -> bool:
        return self.method_ready and self.report_ready and self.contract_ready


@dataclass(frozen=True)
class GenerationRequest:
    project_name: str
    family: str
    device: str
    intent: str
    target_cm_version: str
    method_md: Path
    report_md: Path
    output_root: Path = DEFAULT_PROJECT_ROOT


@dataclass(frozen=True)
class GenerationResult:
    project_dir: Path
    method_cmbx: Path
    report_cmbx: Path
    manifest: Path


@dataclass
class AssetPreflight:
    asset_type: str
    source_path: Path
    source_sha256: str = ""
    method_rows: list[dict[str, str]] = field(default_factory=list)
    method_issues: list[object] = field(default_factory=list)
    report_spec: ReportTemplateMdSpec | None = None
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ready(self) -> bool:
        if self.asset_type == "method":
            return bool(self.method_rows) and not self.errors and not any(
                getattr(item, "severity", "") == "error" for item in self.method_issues
            )
        return self.report_spec is not None and not self.errors


@dataclass(frozen=True)
class AssetGenerationRequest:
    asset_type: str
    asset_name: str
    family: str
    intent: str
    target_cm_version: str
    source_md: Path
    output_root: Path = DEFAULT_PROJECT_ROOT
    basis_method_md: Path | None = None


@dataclass(frozen=True)
class AssetGenerationResult:
    project_dir: Path
    output_cmbx: Path
    manifest: Path


def method_carrier_for_version(target_cm_version: str) -> Path:
    if target_cm_version.startswith("7.2") and DEFAULT_METHOD_CARRIERS[0].exists():
        return DEFAULT_METHOD_CARRIERS[0]
    return next((path for path in DEFAULT_METHOD_CARRIERS if path.exists()), DEFAULT_METHOD_CARRIERS[-1])


def preflight_asset(asset_type: str, source_md: Path) -> AssetPreflight:
    kind = asset_type.strip().lower()
    if kind not in {"method", "report"}:
        raise ValueError(f"Unsupported asset type: {asset_type}")
    result = AssetPreflight(kind, source_md)
    if not source_md.is_file():
        result.errors.append(f"{kind.title()} MD was not found.")
        return result
    result.source_sha256 = _sha256(source_md)
    try:
        if kind == "method":
            result.method_rows = parse_md_to_rows(source_md)
            result.method_issues = list(lint_method_rows(result.method_rows))
            result.errors.extend(
                getattr(item, "display", lambda: str(item))()
                for item in result.method_issues
                if getattr(item, "severity", "") == "error"
            )
            result.warnings.extend(
                getattr(item, "display", lambda: str(item))()
                for item in result.method_issues
                if getattr(item, "severity", "") != "error"
            )
        else:
            result.report_spec = parse_report_template_md(source_md)
            result.errors.extend(result.report_spec.errors)
            if not result.errors:
                prepared = prepare_report_template_md(
                    result.report_spec,
                    tuple(dict.fromkeys((source_md.parent, *DEFAULT_REPORT_SEARCH_ROOTS))),
                )
                result.errors.extend(prepared.errors)
                result.warnings.extend(prepared.warnings)
    except Exception as exc:
        result.errors.append(str(exc))
    return result


def generate_asset(request: AssetGenerationRequest, preflight: AssetPreflight) -> AssetGenerationResult:
    if preflight.asset_type != request.asset_type or preflight.source_path != request.source_md:
        raise ValueError("The selected asset or source path changed after preview. Import the MD again.")
    if preflight.source_sha256 != _sha256(request.source_md):
        raise ValueError("The source MD changed after preview. Import the MD again.")
    if not preflight.ready:
        raise ValueError("Generation is blocked by MD preflight errors.")

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    project_dir = request.output_root / f"{stamp}_{_safe_name(request.asset_name)}"
    inputs = project_dir / "inputs"
    outputs = project_dir / "outputs"
    inputs.mkdir(parents=True, exist_ok=False)
    outputs.mkdir(parents=True)
    snapshot = inputs / request.source_md.name
    shutil.copy2(request.source_md, snapshot)
    method_basis_snapshot: Path | None = None
    if request.basis_method_md and request.basis_method_md.is_file():
        method_basis_snapshot = inputs / f"METHOD_BASIS_{request.basis_method_md.name}"
        shutil.copy2(request.basis_method_md, method_basis_snapshot)
    output = outputs / f"{_safe_name(request.asset_name)}_{request.asset_type}.cmbx"

    compiler_detail: dict[str, object]
    if request.asset_type == "method":
        compiler_detail = compile_method_md_to_cmbx(
            method_carrier_for_version(request.target_cm_version),
            snapshot,
            output,
            method_name=request.asset_name,
        )
    else:
        assert preflight.report_spec is not None
        compiled = compile_report_template_md_to_cmbx(
            preflight.report_spec,
            output,
            tuple(dict.fromkeys((request.source_md.parent, snapshot.parent, *DEFAULT_REPORT_SEARCH_ROOTS))),
        )
        if not compiled.ready:
            raise ValueError("Report CMBX generation failed: " + "; ".join(compiled.errors))
        compiler_detail = {
            "sheets": list(compiled.sheets),
            "cm_formulas": len(compiled.applied_patches),
            "workbook_cells": len(compiled.applied_workbook_patches),
            "dynamic_tables": len(compiled.applied_dynamic_tables),
        }

    manifest = project_dir / "project.json"
    manifest.write_text(
        json.dumps(
            {
                "schema": "cmbx-generation-asset/v1",
                "created_at": datetime.now().isoformat(timespec="seconds"),
                "asset_type": request.asset_type,
                "asset_name": request.asset_name,
                "family": request.family,
                "intent": request.intent,
                "target_cm_version": request.target_cm_version,
                "source_md": str(snapshot),
                "basis_method_md": str(method_basis_snapshot) if method_basis_snapshot else "",
                "source_sha256": _sha256(snapshot),
                "output_cmbx": str(output),
                "compiler_detail": compiler_detail,
                "warnings": preflight.warnings,
                "status": "generated",
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return AssetGenerationResult(project_dir, output, manifest)


def recommended_online_kb_files(asset_type: str, family: str) -> list[Path]:
    return recommended_online_kb_files_for_modules(asset_type, (family,), small_context=False)


def recommended_online_kb_files_for_modules(
    asset_type: str,
    modules: tuple[str, ...] | list[str],
    *,
    small_context: bool = False,
) -> list[Path]:
    context = "03_Small_Context" if small_context else "02_Full_Context"
    root = DEFAULT_WORKSPACE / "KB" / "KB_Online_GPT" / context
    module_names = tuple(dict.fromkeys(item.strip() for item in modules if item.strip()))
    files: list[Path] = []
    if asset_type == "method":
        for module_name in module_names:
            folder = root / module_name / "Method"
            names = ("01_METHOD_SPEC.md", "02_METHOD_ORIGINAL_SCRIPTS.md", "03_METHOD_SUMMARIES.md")
            files.extend(folder / name for name in names if (folder / name).is_file())
        return list(dict.fromkeys(files))
    common = root / "Report" / "01_REPORT_SPEC.md"
    if common.is_file():
        files.append(common)
    for module_name in module_names:
        folder = root / "Report" / module_name
        if folder.is_dir():
            files.extend(sorted(folder.glob("*.md")))
    return list(dict.fromkeys(files))


def preflight_generation(method_md: Path, report_md: Path) -> GenerationPreflight:
    result = GenerationPreflight(method_path=method_md, report_path=report_md)
    if not method_md.is_file():
        result.method_issues.append(_SimpleIssue("error", "METHOD_FILE", "Method MD was not found."))
    else:
        try:
            result.method_sha256 = _sha256(method_md)
            result.method_rows = parse_md_to_rows(method_md)
            result.method_issues = list(lint_method_rows(result.method_rows))
        except Exception as exc:
            result.method_issues.append(_SimpleIssue("error", "METHOD_PARSE", str(exc)))

    if not report_md.is_file():
        result.report_errors.append("Report MD was not found.")
    else:
        try:
            result.report_sha256 = _sha256(report_md)
            result.report_spec = parse_report_template_md(report_md)
            result.report_errors.extend(result.report_spec.errors)
            if not result.report_errors:
                prepared = prepare_report_template_md(
                    result.report_spec,
                    tuple(dict.fromkeys((report_md.parent, *DEFAULT_REPORT_SEARCH_ROOTS))),
                )
                result.report_errors.extend(prepared.errors)
                result.report_warnings.extend(prepared.warnings)
        except Exception as exc:
            result.report_errors.append(str(exc))

    result.findings = cross_contract_findings(result.method_rows, result.report_spec)
    return result


def cross_contract_findings(
    method_rows: list[dict[str, str]], report_spec: ReportTemplateMdSpec | None
) -> list[ContractFinding]:
    if not method_rows or report_spec is None:
        return [ContractFinding("blocked", "Paired design", "Both parsed Method MD and Report MD are required.")]

    method_text = "\n".join(
        " ".join(str(row.get(key, "")) for key in ("Time", "Command", "Value", "Comment"))
        for row in method_rows
    )
    ret_times = {int(value) for value in re.findall(r"RetTimes\.RetTime(\d+)", method_text, re.I)}
    acquisitions = {
        match.group(1).lower()
        for match in re.finditer(r"([A-Za-z0-9_.]+)\.AcqOn\b", method_text, re.I)
    }
    report_formulas = [patch.formula for patch in report_spec.patches]
    report_text = "\n".join(report_formulas)
    required_ret_times = {int(value) for value in re.findall(r"AUDIT\.RetTime(\d+)", report_text, re.I)}
    fixed_channels = {patch.fixed_channel.strip() for patch in report_spec.patches if patch.fixed_channel.strip()}

    findings: list[ContractFinding] = []
    findings.append(
        ContractFinding(
            "warning",
            "Project identity",
            "Current Method MD has no mandatory shared project ID. The user-selected generation project binds this MD pair.",
        )
    )
    missing_ret_times = sorted(required_ret_times - ret_times)
    findings.append(
        ContractFinding(
            "blocked" if missing_ret_times else "ok",
            "RetTime anchors",
            f"Missing method anchors: {', '.join('RetTime' + str(v) for v in missing_ret_times)}"
            if missing_ret_times
            else f"All {len(required_ret_times)} report RetTime anchor(s) are present.",
        )
    )

    missing_channels = sorted(
        channel for channel in fixed_channels if not _channel_has_acquisition(channel, acquisitions, method_text)
    )
    findings.append(
        ContractFinding(
            "warning" if missing_channels else "ok",
            "Fixed channels",
            f"No explicit AcqOn evidence for: {', '.join(missing_channels)}"
            if missing_channels
            else f"All {len(fixed_channels)} fixed channel(s) have acquisition evidence.",
        )
    )

    method_devices = sorted({value for value in re.findall(r"\b([A-Za-z][A-Za-z0-9_]*)\.", method_text) if value not in {"Variables", "StabVars", "TempVars", "RetTimes", "System"}})
    findings.append(ContractFinding("ok", "Configuration symbols", ", ".join(method_devices) or "No device prefix detected."))

    if report_spec.dynamic_tables:
        requiring_processing = [item for item in report_spec.dynamic_tables if item.requires_processing]
        findings.append(
            ContractFinding(
                "warning" if requiring_processing else "ok",
                "Dynamic tables",
                f"{len(requiring_processing)} table(s) require a Processing Method."
                if requiring_processing
                else f"{len(report_spec.dynamic_tables)} dynamic table(s); none declares a processing dependency.",
            )
        )
    return findings


def generate_project(request: GenerationRequest, preflight: GenerationPreflight | None = None) -> GenerationResult:
    check = preflight or preflight_generation(request.method_md, request.report_md)
    if check.method_path != request.method_md or check.report_path != request.report_md:
        raise ValueError("Input paths changed after preflight. Run preflight again.")
    if check.method_sha256 != _sha256(request.method_md) or check.report_sha256 != _sha256(request.report_md):
        raise ValueError("An input MD changed after preflight. Run preflight again.")
    if not check.ready:
        raise ValueError("Generation is blocked. Resolve Method MD, Report MD, and cross-contract preflight findings first.")
    assert check.report_spec is not None

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    project_dir = request.output_root / f"{stamp}_{_safe_name(request.project_name)}"
    inputs = project_dir / "inputs"
    outputs = project_dir / "outputs"
    inputs.mkdir(parents=True, exist_ok=False)
    outputs.mkdir(parents=True)
    method_snapshot = inputs / request.method_md.name
    report_snapshot = inputs / request.report_md.name
    shutil.copy2(request.method_md, method_snapshot)
    shutil.copy2(request.report_md, report_snapshot)

    method_output = outputs / f"{_safe_name(request.project_name)}_method.cmbx"
    report_output = outputs / f"{_safe_name(request.project_name)}_report.cmbx"
    method_stats = compile_method_md_to_cmbx(
        method_carrier_for_version(request.target_cm_version),
        method_snapshot,
        method_output,
        method_name=request.project_name,
    )
    report_result = compile_report_template_md_to_cmbx(
        check.report_spec,
        report_output,
        tuple(dict.fromkeys((request.report_md.parent, report_snapshot.parent, *DEFAULT_REPORT_SEARCH_ROOTS))),
    )
    if not report_result.ready:
        raise ValueError("Report CMBX generation failed: " + "; ".join(report_result.errors))

    manifest = project_dir / "project.json"
    payload = {
        "schema": "cmbx-generation-project/v1",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "project_name": request.project_name,
        "family": request.family,
        "device": request.device,
        "intent": request.intent,
        "target_cm_version": request.target_cm_version,
        "inputs": {
            "method_md": str(method_snapshot),
            "method_sha256": _sha256(method_snapshot),
            "report_md": str(report_snapshot),
            "report_sha256": _sha256(report_snapshot),
        },
        "outputs": {"method_cmbx": str(method_output), "report_cmbx": str(report_output)},
        "method_stats": method_stats,
        "contract_findings": [asdict(item) for item in check.findings],
        "status": "generated",
    }
    manifest.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return GenerationResult(project_dir, method_output, report_output, manifest)


def configuration_requirements(rows: list[dict[str, str]]) -> list[str]:
    text = "\n".join(" ".join(str(value) for value in row.values()) for row in rows)
    devices = sorted({value for value in re.findall(r"\b([A-Za-z][A-Za-z0-9_]*)\.", text) if value not in {"Variables", "StabVars", "TempVars", "RetTimes", "System"}})
    acquisitions = sorted(set(re.findall(r"([A-Za-z0-9_.]+)\.AcqOn\b", text, re.I)))
    variables = sorted(set(re.findall(r"\b(?:Variables|StabVars|TempVars)\.[A-Za-z0-9_]+", text)))
    return [
        "Device/config prefixes: " + (", ".join(devices) or "none detected"),
        "Acquired channels: " + (", ".join(acquisitions) or "none detected"),
        "Imported/custom variables: " + (", ".join(variables) or "none detected"),
    ]


@dataclass(frozen=True)
class _SimpleIssue:
    severity: str
    code: str
    message: str

    def display(self) -> str:
        return f"{self.severity.upper()} {self.code}: {self.message}"


def _channel_has_acquisition(channel: str, acquisitions: set[str], method_text: str) -> bool:
    normalized = channel.lower()
    return any(normalized == item or normalized in item or item.endswith("." + normalized) for item in acquisitions) or normalized in method_text.lower()


def _safe_name(value: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9._-]+", "_", value.strip()).strip("._")
    return safe or "generation_project"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()
