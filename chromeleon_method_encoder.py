from __future__ import annotations

import base64
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path

from chromeleon_runtime import chromeleon_dll


@dataclass(frozen=True)
class MethodEncodeResult:
    ok: bool
    message: str


def encode_method_xml_cpxm(xml_path: Path, cpxm_path: Path) -> MethodEncodeResult:
    dll_path = _chromeleon_data_common_dll()
    if not dll_path:
        return MethodEncodeResult(False, "Chromeleon DataCommon DLL was not found; CpXm payload was not generated.")
    powershell = _powershell_executable()
    if not powershell:
        return MethodEncodeResult(False, "PowerShell was not found; CpXm payload was not generated.")

    script = _encode_script(dll_path, xml_path, cpxm_path)
    encoded = base64.b64encode(script.encode("utf-16le")).decode("ascii")
    env = dict(**os.environ)
    env["PATH"] = str(dll_path.parent) + os.pathsep + env.get("PATH", "")
    try:
        completed = subprocess.run(
            [powershell, "-NoProfile", "-ExecutionPolicy", "Bypass", "-EncodedCommand", encoded],
            capture_output=True,
            text=True,
            timeout=60,
            env=env,
            check=False,
            **_hidden_subprocess_kwargs(),
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        return MethodEncodeResult(False, f"Embedded method XML encode could not run: {exc}")
    if completed.returncode != 0:
        message = (completed.stderr or completed.stdout or "Unknown Chromeleon method encode error.").strip()
        return MethodEncodeResult(False, message)
    message = (completed.stdout or "Embedded method XML encoded.").strip()
    return MethodEncodeResult(cpxm_path.exists(), message)


def _chromeleon_data_common_dll() -> Path | None:
    return chromeleon_dll("Dionex.DataCommon.dll")


def _powershell_executable() -> str | None:
    windir = os.environ.get("WINDIR")
    if windir:
        path = Path(windir) / "System32" / "WindowsPowerShell" / "v1.0" / "powershell.exe"
        if path.exists():
            return str(path)
    return "powershell"


def _hidden_subprocess_kwargs() -> dict[str, int]:
    if os.name == "nt" and hasattr(subprocess, "CREATE_NO_WINDOW"):
        return {"creationflags": subprocess.CREATE_NO_WINDOW}
    return {}


def _ps_literal(path: Path) -> str:
    return "'" + str(path).replace("'", "''") + "'"


def _encode_script(dll_path: Path, xml_path: Path, cpxm_path: Path) -> str:
    return f"""
$ErrorActionPreference = 'Stop'
$asm = [Reflection.Assembly]::LoadFrom({_ps_literal(dll_path)})
$type = $asm.GetTypes() | Where-Object {{ $_.FullName -eq 'Dionex.Chromeleon.Data.Utilities.XmlCompressor' }} | Select-Object -First 1
if ($null -eq $type) {{ throw 'XmlCompressor type was not found in Dionex.DataCommon.dll.' }}
$method = $type.GetMethods([Reflection.BindingFlags]'Public,NonPublic,Static') | Where-Object {{
    $_.Name -eq 'Compress' -and
    $_.GetParameters().Count -eq 1 -and
    $_.GetParameters()[0].ParameterType.FullName -eq 'System.String'
}} | Select-Object -First 1
if ($null -eq $method) {{ throw 'XmlCompressor.Compress(string) was not found.' }}
$xml = [IO.File]::ReadAllText({_ps_literal(xml_path)}, [Text.UTF8Encoding]::new($false))
$args = [object[]]::new(1)
$args[0] = $xml
$bytes = [byte[]]$method.Invoke($null, $args)
[IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName({_ps_literal(cpxm_path)})) | Out-Null
[IO.File]::WriteAllBytes({_ps_literal(cpxm_path)}, $bytes)
Write-Output "Embedded method XML encoded: $($bytes.Length) bytes."
""".strip()
