from __future__ import annotations

import os
from pathlib import Path


TOOL_ROOT = Path(__file__).resolve().parent
LOCAL_DEPENDENCY_ROOT = TOOL_ROOT / "dependencies" / "chromeleon"
CSC_PATH = Path(r"C:\Windows\Microsoft.NET\Framework\v4.0.30319\csc.exe")
REQUIRED_RUNTIME_DLLS = (
    "Dionex.DataCommon.dll",
    "Dionex.RawData.dll",
    "Dionex.RawDataInterfaces.dll",
    "Dionex.Chromeleon.Common.dll",
)


def chromeleon_bin() -> Path | None:
    for candidate in chromeleon_bin_candidates():
        if _looks_like_chromeleon_bin(candidate):
            return candidate
    return None


def chromeleon_bin_candidates() -> list[Path]:
    candidates: list[Path] = []
    env_path = os.environ.get("CMBX_CHROMELEON_BIN") or os.environ.get("CHROMELEON_BIN")
    if env_path:
        candidates.extend(_runtime_variants(Path(env_path)))
    candidates.extend(_runtime_variants(LOCAL_DEPENDENCY_ROOT))
    for root_name in ("ProgramFiles(x86)", "ProgramFiles"):
        root = os.environ.get(root_name)
        if root:
            candidates.append(Path(root) / "Thermo" / "Chromeleon" / "bin")
    candidates.append(Path(r"C:\Program Files (x86)\Thermo\Chromeleon\bin"))
    candidates.append(Path(r"C:\Program Files\Thermo\Chromeleon\bin"))
    return _dedupe(candidates)


def chromeleon_dll(name: str) -> Path | None:
    runtime = chromeleon_bin()
    if not runtime:
        return None
    path = runtime / name
    return path if path.exists() else None


def runtime_status_text() -> str:
    runtime = chromeleon_bin()
    lines = [
        "Chromeleon Runtime Resolution",
        "-----------------------------",
        f"Environment variable CMBX_CHROMELEON_BIN: {os.environ.get('CMBX_CHROMELEON_BIN') or ''}",
        f"Local dependency folder: {LOCAL_DEPENDENCY_ROOT}",
        f"Resolved runtime folder: {runtime or 'Not found'}",
        f".NET C# compiler: {CSC_PATH if CSC_PATH.exists() else 'Not found'}",
        "",
        "Required DLL check",
        "------------------",
    ]
    if runtime:
        for dll in REQUIRED_RUNTIME_DLLS:
            lines.append(f"{dll}: {'OK' if (runtime / dll).exists() else 'Missing'}")
    else:
        lines.extend(f"{dll}: Missing" for dll in REQUIRED_RUNTIME_DLLS)
    return "\n".join(lines)


def _runtime_variants(path: Path) -> list[Path]:
    return [path, path / "bin"] if path.name.lower() != "bin" else [path]


def _looks_like_chromeleon_bin(path: Path) -> bool:
    return path.exists() and (path / "Dionex.DataCommon.dll").exists()


def _dedupe(paths: list[Path]) -> list[Path]:
    seen: set[str] = set()
    result: list[Path] = []
    for path in paths:
        key = str(path).lower()
        if key in seen:
            continue
        seen.add(key)
        result.append(path)
    return result
