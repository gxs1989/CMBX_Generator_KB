# FormulaOne Report Export

## Purpose

This feature exports a real Chromeleon Report Designer workbook from a CMBX package.

The CMBX report definition contains:

- report XML
- sheet setup rules
- report formula objects
- `SpreadSheetData`, which is the real FormulaOne workbook binary

The exporter uses the FormulaOne workbook as the layout source. It can either export the blank template or write calculated values into the cells that Chromeleon would normally fill from raw data.

## Current Flow

```text
CMBX report definition
-> decode report XML
-> extract SpreadSheetData
-> load with Chromeleon FormulaOne runtime
-> expand all Report Designer sheets
-> evaluate direct report formulas and known workbook-derived rules
-> write values into the FormulaOne workbook
-> export selected sheets to .xls
```

For blank template export, the same runtime path is used without cell writes and without sheet filtering.

## Runtime Dependency

The current implementation uses the local 32-bit Chromeleon runtime:

```text
C:\Program Files (x86)\Thermo\Chromeleon\bin\Dionex.Controls.dll
C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe
```

The important APIs are:

```text
FormulaOneWorkbook.ReadFromBlob(byte[])
FormulaOneWorkbook.WriteToXml()
FormulaOneWorkbook.ReadFromXml(XmlNode)
AxF1Book.set_NumberSRC(sheet, row, column, value)
AxF1Book.set_TextSRC(sheet, row, column, value)
FormulaOneWorkbook.Export(path, Excel5, sheets)
```

The `ReadFromBlob -> WriteToXml -> ReadFromXml` round trip is required because direct blob loading initially exposes only one sheet, while the round trip expands the full workbook sheet list.

## Verified Behavior

Verified with `6545327.cmbx` and the CM-exported reference report `Temperature Accuracy_H.xls`.

The generated sheet set is:

```text
Definitions
Title
Test Procedures
Temp Accuracy
Temp Precision
COC
FOQ VTCC History
```

Key cells such as `Temp Accuracy!D26`, `E26`, `L66`, `M66`, and `N66` match the CM export within floating-point tail differences.

Sequence-level export was verified with `6545327.cmbx`; it writes one workbook containing the corresponding report sheets for the full sequence.

## Boundaries

- Sheet selection currently uses FOQ-specific heuristics.
- Helper sheets may remain blank if the selected injection does not contain the raw channel required by that sheet's formulas.
- A portable FormulaOne dependency bundle is not implemented yet.
- A full FormulaOne formula parser is not implemented; known CM formulas and workbook-derived rules are evaluated by the Python calculation layer.
