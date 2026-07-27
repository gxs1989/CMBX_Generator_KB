from __future__ import annotations

import base64
import json
import os
import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path

from cmbx_container import safe_filename
from foq_contract_report import ReportCellValue


CHROMELEON_BIN = Path(r"C:\Program Files (x86)\Thermo\Chromeleon\bin")
POWERSHELL_32 = Path(r"C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe")


@dataclass(frozen=True)
class FormulaOneCellWrite:
    sheet: str
    row: int
    column: int
    value: object


def export_formulaone_report_template(
    output_path: str | Path,
    report_xml: str,
    sheet_names: list[str] | None = None,
    cell_values: dict[tuple[str, str], ReportCellValue] | None = None,
    chromeleon_bin: Path = CHROMELEON_BIN,
    powershell_32: Path = POWERSHELL_32,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    blob = extract_formulaone_spreadsheet_data(report_xml)
    writes = _cell_writes(cell_values or {})
    instructions = {
        "blob": base64.b64encode(blob).decode("ascii"),
        "outputPath": str(output),
        "sheetNames": sheet_names or [],
        "cells": [
            {"sheet": item.sheet, "row": item.row, "column": item.column, "value": item.value}
            for item in writes
        ],
        "chromeleonBin": str(chromeleon_bin),
    }
    with tempfile.TemporaryDirectory(prefix="cmbx_formulaone_") as tmp:
        json_path = Path(tmp) / "formulaone_export.json"
        json_path.write_text(json.dumps(instructions, ensure_ascii=False), encoding="utf-8")
        script = _formulaone_export_script(json_path)
        encoded = base64.b64encode(script.encode("utf-16le")).decode("ascii")
        result = subprocess.run(
            [str(powershell_32), "-NoProfile", "-EncodedCommand", encoded],
            cwd=str(Path.cwd()),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=120,
            **_hidden_subprocess_kwargs(),
        )
    if result.returncode != 0:
        message = (result.stderr or result.stdout or "FormulaOne export failed.").strip()
        raise RuntimeError(message)
    if not output.exists():
        raise RuntimeError(f"FormulaOne export did not create the expected file: {output}")
    return output


def extract_formulaone_spreadsheet_data(report_xml: str) -> bytes:
    root = ET.fromstring(report_xml)
    for node in root.iter():
        if node.tag == "SpreadSheetData":
            value = node.attrib.get("value", "")
            if value:
                return base64.b64decode(value)
    raise ValueError("No FormulaOne SpreadSheetData payload was found in the report template.")


def report_export_sheet_names(injection_name: str, available_sheet_names: list[str]) -> list[str]:
    available = {name.lower(): name for name in available_sheet_names}
    selected: list[str] = []

    def add(name: str) -> None:
        actual = available.get(name.lower())
        if actual and actual not in selected:
            selected.append(actual)

    for common in ("Definitions", "Title", "Test Procedures"):
        add(common)

    compact = _compact(injection_name)
    if "temperatureaccuracy" in compact:
        add("Temp Accuracy")
        add("Temp Precision")
    elif "temperatureprecision" in compact:
        add("Temp Precision")
        add("Fan")
    elif "temperaturestability" in compact:
        add("Temp Stability_Noise")
        add("PCC")
    elif "heatupandcooldowntime" in compact:
        add("HeatUp&CoolDown")
    elif "preheaterconnectiontest" in compact:
        add("Preheater Ports_Noise")
    elif "columnids" in compact:
        add("Temp Precision")
        add("Column ID")
    elif "valve" in compact:
        add("Valve_Keypad")
    elif "liquidleaktest" in compact:
        add("Liquid Leak Test")
    elif "temperaturecalibration" in compact:
        add("Temp_Calib_Internal")
    elif "factorydefault" in compact:
        add("Internal Use")
        add("Audit Trail")
    elif "errorlogcheck" in compact:
        add("Error Log")

    for common in ("COC", "FOQ VTCC History"):
        add(common)
    return selected or available_sheet_names


def formulaone_report_filename(injection_name: str) -> str:
    return f"{safe_filename(injection_name, 'report')}.xls"


def _cell_writes(values: dict[tuple[str, str], ReportCellValue]) -> list[FormulaOneCellWrite]:
    writes: list[FormulaOneCellWrite] = []
    for value in values.values():
        if value.status != "ok" or value.value is None:
            continue
        parsed = _cell_to_row_col(value.cell)
        if not parsed:
            continue
        row, column = parsed
        writes.append(FormulaOneCellWrite(value.sheet_name, row, column, value.value))
    return writes


def _cell_to_row_col(cell: str) -> tuple[int, int] | None:
    match = re.fullmatch(r"([A-Z]+)([0-9]+)", cell.strip().upper())
    if not match:
        return None
    column = 0
    for char in match.group(1):
        column = column * 26 + ord(char) - 64
    return int(match.group(2)), column


def _compact(value: str) -> str:
    return "".join(ch.lower() for ch in value if ch.isalnum())


def _hidden_subprocess_kwargs() -> dict[str, int]:
    if os.name == "nt" and hasattr(subprocess, "CREATE_NO_WINDOW"):
        return {"creationflags": subprocess.CREATE_NO_WINDOW}
    return {}


def _formulaone_export_script(json_path: Path) -> str:
    return rf'''
$ErrorActionPreference = "Stop"
$instructions = Get-Content -LiteralPath "{json_path}" -Raw | ConvertFrom-Json
$chrom = [string]$instructions.chromeleonBin
$asm = [System.Reflection.Assembly]::LoadFrom((Join-Path $chrom "Dionex.Controls.dll"))
$scopeType = $asm.GetType("Dionex.Common.Controls.SpreadsheetControl.FormulaOneSideBySideActivationContextScope")
$scope = [Activator]::CreateInstance($scopeType)
try {{
  $spreadsheetType = $asm.GetType("Dionex.Common.Controls.FormulaOneSpreadsheet")
  $source = [Activator]::CreateInstance($spreadsheetType)
  $blob = [Convert]::FromBase64String([string]$instructions.blob)
  $source.Workbook.ReadFromBlob($blob)
  $xmlNode = $source.Workbook.WriteToXml()

  $spreadsheet = [Activator]::CreateInstance($spreadsheetType)
  $spreadsheet.Workbook.ReadFromXml($xmlNode)
  $f1 = $spreadsheet.Workbook.F1Book

  $sheetIndexByName = @{{}}
  $index = 1
  foreach ($sheet in $spreadsheet.Workbook.Sheets) {{
    $sheetIndexByName[[string]$sheet.Name] = $index
    $index += 1
  }}

  foreach ($cell in $instructions.cells) {{
    $sheetName = [string]$cell.sheet
    if (-not $sheetIndexByName.ContainsKey($sheetName)) {{ continue }}
    $sheetIndex = [int]$sheetIndexByName[$sheetName]
    $row = [int]$cell.row
    $column = [int]$cell.column
    $rawValue = $cell.value
    if ($rawValue -is [System.ValueType] -and -not ($rawValue -is [bool])) {{
      $f1.set_NumberSRC($sheetIndex, $row, $column, [double]$rawValue)
    }} else {{
      $f1.set_TextSRC($sheetIndex, $row, $column, [string]$rawValue)
    }}
  }}

  $sheetInterface = $asm.GetType("Dionex.Common.Controls.ISheet")
  $listType = ([System.Collections.Generic.List``1]).MakeGenericType($sheetInterface)
  $selected = [Activator]::CreateInstance($listType)
  if ($instructions.sheetNames.Count -gt 0) {{
    foreach ($name in $instructions.sheetNames) {{
      $sheet = $spreadsheet.Workbook.GetSheetByName([string]$name)
      if ($sheet -ne $null) {{ $selected.Add($sheet) }}
    }}
  }}
  if ($selected.Count -eq 0) {{
    foreach ($sheet in $spreadsheet.Workbook.Sheets) {{ $selected.Add($sheet) }}
  }}

  $fmtType = $asm.GetType("Dionex.Common.Controls.WorkbookFileFormat")
  $fmt = [Enum]::Parse($fmtType, "Excel5")
  $spreadsheet.Workbook.Export([string]$instructions.outputPath, $fmt, $selected)
}} finally {{
}}
'''

