from __future__ import annotations

import base64
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path

from chromeleon_runtime import chromeleon_dll


@dataclass(frozen=True)
class MethodDecodeResult:
    ok: bool
    message: str


def decode_cpxm_method_xml(cpxm_path: Path, xml_path: Path) -> MethodDecodeResult:
    dll_path = _chromeleon_data_common_dll()
    if not dll_path:
        return MethodDecodeResult(False, "Chromeleon DataCommon DLL was not found; readable method XML was not generated.")
    powershell = _powershell_executable()
    if not powershell:
        return MethodDecodeResult(False, "PowerShell was not found; readable method XML was not generated.")

    script = _decode_script(dll_path, cpxm_path, xml_path)
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
        return MethodDecodeResult(False, f"Embedded method XML decode could not run: {exc}")
    if completed.returncode != 0:
        message = (completed.stderr or completed.stdout or "Unknown Chromeleon method decode error.").strip()
        return MethodDecodeResult(False, message)
    message = (completed.stdout or "Embedded method XML decoded.").strip()
    return MethodDecodeResult(xml_path.exists(), message)


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


def _decode_script(dll_path: Path, cpxm_path: Path, xml_path: Path) -> str:
    return f"""
$ErrorActionPreference = 'Stop'
$asm = [Reflection.Assembly]::LoadFrom({_ps_literal(dll_path)})
$type = $asm.GetTypes() | Where-Object {{ $_.FullName -eq 'Dionex.Chromeleon.Data.Utilities.XmlCompressor' }} | Select-Object -First 1
if ($null -eq $type) {{ throw 'XmlCompressor type was not found in Dionex.DataCommon.dll.' }}
$method = $type.GetMethods([Reflection.BindingFlags]'Public,NonPublic,Static') | Where-Object {{
    $_.Name -eq 'Uncompress' -and
    $_.GetParameters().Count -eq 1 -and
    $_.GetParameters()[0].ParameterType.FullName -eq 'System.Byte[]'
}} | Select-Object -First 1
if ($null -eq $method) {{ throw 'XmlCompressor.Uncompress(byte[]) was not found.' }}
$data = [byte[]][IO.File]::ReadAllBytes({_ps_literal(cpxm_path)})
$args = [object[]]::new(1)
$args[0] = $data
$xml = [string]$method.Invoke($null, $args)
[IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName({_ps_literal(xml_path)})) | Out-Null
[IO.File]::WriteAllText({_ps_literal(xml_path)}, $xml, [Text.UTF8Encoding]::new($false))
Write-Output "Embedded method XML decoded: $($xml.Length) characters."
""".strip()
