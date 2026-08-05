from __future__ import annotations

"""FormulaOne workbook writer for Chromeleon report templates.

The Chromeleon FormulaOne runtime needs an x86 STA WinForms host to persist a
workbook blob. Existing-cell patching remains available for legacy contracts;
the structural path creates business-level blank workbooks with named sheets.
"""

import base64
import json
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

from chromeleon_runtime import chromeleon_bin as resolve_chromeleon_bin

CHROMELEON_BIN = resolve_chromeleon_bin() or Path(r"C:\Program Files (x86)\Thermo\Chromeleon\bin")
_TOOLS_DIR = Path(__file__).resolve().parent / "tools"
_HOST_SOURCE = _TOOLS_DIR / "formulaone_writer_host.cs"


@dataclass(frozen=True)
class FormulaOneWorkbookPatch:
    sheet_name: str
    row: int
    column: int
    kind: str  # number | text | formula
    value: object
    style: str = ""
    number_format: str = ""


@dataclass(frozen=True)
class FormulaOneSheetSpec:
    name: str
    cells: tuple[FormulaOneWorkbookPatch, ...] = ()
    column_widths: tuple[tuple[int, float], ...] = ()
    row_heights: tuple[tuple[int, float], ...] = ()


@dataclass(frozen=True)
class FormulaOneWorkbookBuild:
    blob: bytes
    xml_text: str


def create_formulaone_workbook(
    carrier_blob: bytes,
    sheets: tuple[FormulaOneSheetSpec, ...],
    chromeleon_bin: Path = CHROMELEON_BIN,
) -> FormulaOneWorkbookBuild:
    """Create a new logical workbook inside a valid FormulaOne carrier blob."""
    if not sheets:
        raise ValueError("At least one FormulaOne sheet is required.")
    names = [sheet.name.strip() for sheet in sheets]
    if any(not name for name in names):
        raise ValueError("FormulaOne sheet names cannot be empty.")
    if len(set(names)) != len(names):
        raise ValueError("FormulaOne sheet names must be unique.")
    payload_sheets = []
    for sheet in sheets:
        cells = []
        for cell in sheet.cells:
            if cell.kind not in {"number", "text", "formula"}:
                raise ValueError(f"Unsupported FormulaOne cell type: {cell.kind}")
            cells.append(
                {
                    "row": cell.row,
                    "column": cell.column,
                    "kind": cell.kind,
                    "value": cell.value,
                    "style": cell.style,
                    "number_format": cell.number_format,
                }
            )
        payload_sheets.append(
            {
                "name": sheet.name,
                "cells": cells,
                "column_widths": [{"column": column, "width": width} for column, width in sheet.column_widths],
                "row_heights": [{"row": row, "height": height} for row, height in sheet.row_heights],
            }
        )
    if not chromeleon_bin.joinpath("Dionex.Controls.dll").is_file():
        raise RuntimeError(f"Chromeleon FormulaOne runtime was not found: {chromeleon_bin}")
    with tempfile.TemporaryDirectory(prefix="cmbx_formulaone_structural_") as tmp:
        temp = Path(tmp)
        host = _compile_host(temp)
        instructions = temp / "instructions.json"
        output = temp / "created_workbook.json"
        instructions.write_text(
            json.dumps(
                {
                    "mode": "create_workbook",
                    "chromeleonBin": str(chromeleon_bin),
                    "blob": base64.b64encode(carrier_blob).decode("ascii"),
                    "sheets": payload_sheets,
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        result = subprocess.run(
            [str(host), str(instructions), str(output)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=120,
            **_hidden_subprocess_kwargs(),
        )
        if result.returncode != 0 or not output.exists():
            detail = (result.stderr or result.stdout or "FormulaOne host did not create a workbook.").strip()
            raise RuntimeError(detail)
        payload = json.loads(output.read_text(encoding="utf-8"))
        return FormulaOneWorkbookBuild(base64.b64decode(payload["blob"]), str(payload["xml"]))


def write_formulaone_existing_cells(
    blob: bytes,
    patches: tuple[FormulaOneWorkbookPatch, ...],
    chromeleon_bin: Path = CHROMELEON_BIN,
) -> bytes:
    """Return a FormulaOne blob with verified existing-cell mutations applied."""
    if not patches:
        return blob
    if not chromeleon_bin.joinpath("Dionex.Controls.dll").is_file():
        raise RuntimeError(f"Chromeleon FormulaOne runtime was not found: {chromeleon_bin}")
    for patch in patches:
        if patch.kind not in {"number", "text", "formula"}:
            raise ValueError(f"Unsupported FormulaOne patch type: {patch.kind}")
        if patch.row < 1 or patch.column < 1:
            raise ValueError(f"FormulaOne address must be one-based: {patch.sheet_name}!R{patch.row}C{patch.column}")

    with tempfile.TemporaryDirectory(prefix="cmbx_formulaone_write_") as tmp:
        temp = Path(tmp)
        host = _compile_host(temp)
        instructions = temp / "instructions.json"
        output = temp / "written_blob.base64.txt"
        instructions.write_text(
            json.dumps(
                {
                    "chromeleonBin": str(chromeleon_bin),
                    "blob": base64.b64encode(blob).decode("ascii"),
                    "patches": [
                        {
                            "sheet": patch.sheet_name,
                            "row": patch.row,
                            "column": patch.column,
                            "kind": patch.kind,
                            "value": patch.value,
                        }
                        for patch in patches
                    ],
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        result = subprocess.run(
            [str(host), str(instructions), str(output)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=90,
            **_hidden_subprocess_kwargs(),
        )
        if result.returncode != 0 or not output.exists():
            detail = (result.stderr or result.stdout or "FormulaOne writer did not create an output blob.").strip()
            raise RuntimeError(detail)
        return base64.b64decode(output.read_text(encoding="ascii").strip())


def _run_blob_host(blob: bytes, payload: dict[str, object], chromeleon_bin: Path, timeout: int) -> bytes:
    if not chromeleon_bin.joinpath("Dionex.Controls.dll").is_file():
        raise RuntimeError(f"Chromeleon FormulaOne runtime was not found: {chromeleon_bin}")
    with tempfile.TemporaryDirectory(prefix="cmbx_formulaone_structural_") as tmp:
        temp = Path(tmp)
        host = _compile_host(temp)
        instructions = temp / "instructions.json"
        output = temp / "written_blob.base64.txt"
        body = {"chromeleonBin": str(chromeleon_bin), "blob": base64.b64encode(blob).decode("ascii")}
        body.update(payload)
        instructions.write_text(json.dumps(body, ensure_ascii=False), encoding="utf-8")
        result = subprocess.run(
            [str(host), str(instructions), str(output)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            **_hidden_subprocess_kwargs(),
        )
        if result.returncode != 0 or not output.exists():
            detail = (result.stderr or result.stdout or "FormulaOne host did not create an output blob.").strip()
            raise RuntimeError(detail)
        return base64.b64decode(output.read_text(encoding="ascii").strip())


def read_formulaone_formula_inventory(
    blob: bytes,
    chromeleon_bin: Path = CHROMELEON_BIN,
) -> list[dict[str, object]]:
    """Return every non-empty FormulaOne formula in a workbook blob.

    The runtime scans each existing sheet through its documented last row/column
    bounds. Values/text-only cells are intentionally excluded.
    """
    if not chromeleon_bin.joinpath("Dionex.Controls.dll").is_file():
        raise RuntimeError(f"Chromeleon FormulaOne runtime was not found: {chromeleon_bin}")
    with tempfile.TemporaryDirectory(prefix="cmbx_formulaone_inventory_") as tmp:
        temp = Path(tmp)
        host = _compile_host(temp)
        instructions = temp / "instructions.json"
        output = temp / "inventory.json"
        instructions.write_text(
            json.dumps(
                {
                    "mode": "inventory",
                    "chromeleonBin": str(chromeleon_bin),
                    "blob": base64.b64encode(blob).decode("ascii"),
                }
            ),
            encoding="utf-8",
        )
        result = subprocess.run(
            [str(host), str(instructions), str(output)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=120,
            **_hidden_subprocess_kwargs(),
        )
        if result.returncode != 0 or not output.exists():
            detail = (result.stderr or result.stdout or "FormulaOne inventory host did not create output.").strip()
            raise RuntimeError(detail)
        data = json.loads(output.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            raise RuntimeError("FormulaOne inventory host returned an invalid payload.")
        return [item for item in data if isinstance(item, dict)]


def read_formulaone_cells(
    blob: bytes,
    probes: tuple[tuple[str, int, int], ...],
    chromeleon_bin: Path = CHROMELEON_BIN,
) -> list[dict[str, object]]:
    """Read only explicitly requested cells from a FormulaOne workbook."""
    if not probes:
        return []
    if not chromeleon_bin.joinpath("Dionex.Controls.dll").is_file():
        raise RuntimeError(f"Chromeleon FormulaOne runtime was not found: {chromeleon_bin}")
    with tempfile.TemporaryDirectory(prefix="cmbx_formulaone_cells_") as tmp:
        temp = Path(tmp)
        host = _compile_host(temp)
        instructions = temp / "instructions.json"
        output = temp / "cells.json"
        instructions.write_text(
            json.dumps(
                {
                    "mode": "read_cells",
                    "chromeleonBin": str(chromeleon_bin),
                    "blob": base64.b64encode(blob).decode("ascii"),
                    "probes": [{"sheet": sheet, "row": row, "column": column} for sheet, row, column in probes],
                }
            ),
            encoding="utf-8",
        )
        result = subprocess.run(
            [str(host), str(instructions), str(output)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30,
            **_hidden_subprocess_kwargs(),
        )
        if result.returncode != 0 or not output.exists():
            detail = (result.stderr or result.stdout or "FormulaOne cell reader did not create output.").strip()
            raise RuntimeError(detail)
        data = json.loads(output.read_text(encoding="utf-8"))
        return [item for item in data if isinstance(item, dict)]


def _compile_host(destination: Path) -> Path:
    if not _HOST_SOURCE.is_file():
        raise RuntimeError(f"FormulaOne writer host source was not found: {_HOST_SOURCE}")
    csc = Path(r"C:\Windows\Microsoft.NET\Framework\v4.0.30319\csc.exe")
    if not csc.is_file():
        raise RuntimeError(f"The x86 .NET Framework compiler was not found: {csc}")
    source_stamp = f"{_HOST_SOURCE.stat().st_mtime_ns:x}_{_HOST_SOURCE.stat().st_size:x}"
    cache = Path(tempfile.gettempdir()) / "CmbxDataExplorer" / "tools"
    cache.mkdir(parents=True, exist_ok=True)
    output = cache / f"formulaone_writer_host_{source_stamp}.exe"
    if output.is_file():
        return output
    result = subprocess.run(
        [
            str(csc),
            "/nologo",
            "/target:exe",
            "/platform:x86",
            f"/out:{output}",
            "/r:System.Windows.Forms.dll",
            "/r:System.Drawing.dll",
            "/r:System.Web.Extensions.dll",
            str(_HOST_SOURCE),
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=30,
        **_hidden_subprocess_kwargs(),
    )
    if result.returncode != 0 or not output.exists():
        raise RuntimeError((result.stderr or result.stdout or "Could not compile FormulaOne writer host.").strip())
    return output


def _hidden_subprocess_kwargs() -> dict[str, int]:
    import os

    if os.name == "nt" and hasattr(subprocess, "CREATE_NO_WINDOW"):
        return {"creationflags": subprocess.CREATE_NO_WINDOW}
    return {}
