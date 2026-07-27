from __future__ import annotations

import shutil
import os
import subprocess
import tempfile
from pathlib import Path

from chromeleon_runtime import CSC_PATH, chromeleon_bin

SIGNAL_EXPORTER_SOURCE = Path(__file__).resolve().parent / "chromeleon_signal_exporter.cs"
AUDIT_EXPORTER_SOURCE = Path(__file__).resolve().parent / "chromeleon_audit_exporter.cs"


class ChromeleonExportError(RuntimeError):
    pass


def chromeleon_export_available() -> bool:
    return chromeleon_bin() is not None and CSC_PATH.exists()


def export_signal_raw(raw_path: str | Path, output_tsv: str | Path, channel_name: str) -> Path:
    exporter = _ensure_signal_exporter()
    return _run_exporter(exporter, [raw_path, output_tsv, channel_name], "Chromeleon signal export failed")


def export_audit_raw(raw_path: str | Path, output_tsv: str | Path) -> Path:
    exporter = _ensure_audit_exporter()
    return _run_exporter(exporter, [raw_path, output_tsv], "Chromeleon audit export failed")


def _run_exporter(exporter: Path, args: list[str | Path], failure_message: str) -> Path:
    output_path = Path(args[1]).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    runtime = chromeleon_bin()
    env = None
    if runtime:
        env = dict(**os.environ)
        env["PATH"] = str(runtime) + os.pathsep + env.get("PATH", "")
    result = subprocess.run(
        [str(exporter), *[str(Path(arg).resolve()) if index < 2 else str(arg) for index, arg in enumerate(args)]],
        cwd=str(exporter.parent),
        env=env,
        capture_output=True,
        text=True,
        check=False,
        **_hidden_subprocess_kwargs(),
    )
    if result.returncode != 0:
        message = (result.stderr or result.stdout or failure_message).strip()
        raise ChromeleonExportError(message)
    return output_path


def _ensure_signal_exporter() -> Path:
    runtime = _resolved_runtime_or_error()
    cache_dir = _cache_dir()
    exporter = cache_dir / "ChromeleonSignalExporter.exe"
    if not exporter.exists() or exporter.stat().st_mtime < SIGNAL_EXPORTER_SOURCE.stat().st_mtime:
        _compile(
            SIGNAL_EXPORTER_SOURCE,
            exporter,
            [
                runtime / "Dionex.RawData.dll",
                runtime / "Dionex.RawDataInterfaces.dll",
                runtime / "Dionex.Chromeleon.Common.dll",
            ],
        )
    _copy_runtime_dependencies(cache_dir, runtime)
    return exporter


def _ensure_audit_exporter() -> Path:
    runtime = _resolved_runtime_or_error()
    cache_dir = _cache_dir()
    exporter = cache_dir / "ChromeleonAuditExporter.exe"
    if not exporter.exists() or exporter.stat().st_mtime < AUDIT_EXPORTER_SOURCE.stat().st_mtime:
        _compile(
            AUDIT_EXPORTER_SOURCE,
            exporter,
            [
                runtime / "Dionex.DataCommon.dll",
                runtime / "Dionex.InstrumentServerInterfaces.dll",
                runtime / "Dionex.Serialization.dll",
            ],
        )
    _copy_runtime_dependencies(cache_dir, runtime)
    return exporter


def _cache_dir() -> Path:
    path = Path(tempfile.gettempdir()) / "CmbxDataExplorer" / "chromeleon_exporter"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _compile(source: Path, target: Path, references: list[Path]) -> None:
    command = [
        str(CSC_PATH),
        "/nologo",
        "/platform:x86",
        "/target:exe",
        f"/out:{target}",
        *[f"/reference:{path}" for path in references],
        str(source),
    ]
    result = subprocess.run(command, capture_output=True, text=True, check=False, **_hidden_subprocess_kwargs())
    if result.returncode != 0:
        message = (result.stderr or result.stdout or "C# compiler failed").strip()
        raise ChromeleonExportError(message)


def _resolved_runtime_or_error() -> Path:
    runtime = chromeleon_bin()
    if not runtime or not CSC_PATH.exists():
        raise ChromeleonExportError(
            "Chromeleon runtime DLLs or .NET Framework csc.exe were not found. "
            "Install Chromeleon, set CMBX_CHROMELEON_BIN, or place approved runtime DLLs under cmbx_data_explorer\\dependencies\\chromeleon."
        )
    return runtime


def _copy_runtime_dependencies(cache_dir: Path, runtime: Path) -> None:
    prefixes = ("Dionex", "Thermo", "Wintellect", "protobuf", "log4net", "Newtonsoft", "Microsoft", "System.")
    for source in runtime.glob("*.dll"):
        if source.name.startswith(prefixes):
            target = cache_dir / source.name
            if not target.exists() or target.stat().st_mtime < source.stat().st_mtime:
                shutil.copy2(source, target)


def _hidden_subprocess_kwargs() -> dict[str, int]:
    if os.name == "nt" and hasattr(subprocess, "CREATE_NO_WINDOW"):
        return {"creationflags": subprocess.CREATE_NO_WINDOW}
    return {}
