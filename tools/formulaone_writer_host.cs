// x86 STA host for FormulaOne workbook writes used by Chromeleon reports.
using System;
using System.Collections;
using System.Collections.Generic;
using System.Drawing;
using System.IO;
using System.Reflection;
using System.Text;
using System.Web.Script.Serialization;
using System.Windows.Forms;
using System.Xml;

internal static class FormulaOneWriterHost
{
    [STAThread]
    private static int Main(string[] args)
    {
        if (args.Length != 2)
        {
            Console.Error.WriteLine("Usage: formulaone_writer_host.exe <instructions.json> <output-base64.txt>");
            return 2;
        }

        Form host = null;
        object activationScope = null;
        try
        {
            var instructions = ReadInstructions(args[0]);
            var chromeleonBin = GetString(instructions, "chromeleonBin");
            if (String.IsNullOrEmpty(chromeleonBin) || !File.Exists(Path.Combine(chromeleonBin, "Dionex.Controls.dll")))
                throw new InvalidOperationException("Dionex.Controls.dll was not found in chromeleonBin.");

            Environment.SetEnvironmentVariable("PATH", chromeleonBin + ";" + Environment.GetEnvironmentVariable("PATH"));
            AppDomain.CurrentDomain.AssemblyResolve += delegate(object sender, ResolveEventArgs eventArgs)
            {
                var candidate = Path.Combine(chromeleonBin, new AssemblyName(eventArgs.Name).Name + ".dll");
                return File.Exists(candidate) ? Assembly.LoadFrom(candidate) : null;
            };

            var controls = Assembly.LoadFrom(Path.Combine(chromeleonBin, "Dionex.Controls.dll"));
            activationScope = Activator.CreateInstance(controls.GetType(
                "Dionex.Common.Controls.SpreadsheetControl.FormulaOneSideBySideActivationContextScope", true));
            var spreadsheetType = controls.GetType("Dionex.Common.Controls.FormulaOneSpreadsheet", true);

            host = new Form
            {
                ShowInTaskbar = false,
                StartPosition = FormStartPosition.Manual,
                Left = -32000,
                Top = -32000,
                Width = 1,
                Height = 1,
                Opacity = 0,
            };
            host.CreateControl();

            object source = CreateHostedSpreadsheet(spreadsheetType, host);
            object sourceWorkbook = GetProperty(source, "Workbook");
            Invoke(sourceWorkbook, "ReadFromBlob", Convert.FromBase64String(GetString(instructions, "blob")));
            XmlNode xml = (XmlNode)Invoke(sourceWorkbook, "WriteToXml");

            object spreadsheet = CreateHostedSpreadsheet(spreadsheetType, host);
            object workbook = GetProperty(spreadsheet, "Workbook");
            Invoke(workbook, "ReadFromXml", xml);
            Application.DoEvents();

            object f1 = GetProperty(workbook, "F1Book");
            if (String.Equals(GetString(instructions, "mode"), "runtime_api", StringComparison.OrdinalIgnoreCase))
            {
                File.WriteAllText(args[1], RuntimeApi(f1), new UTF8Encoding(false));
                return 0;
            }
            if (String.Equals(GetString(instructions, "mode"), "inventory", StringComparison.OrdinalIgnoreCase))
            {
                var serializer = new JavaScriptSerializer { MaxJsonLength = Int32.MaxValue };
                File.WriteAllText(args[1], serializer.Serialize(ReadFormulaInventory(f1, workbook)), new UTF8Encoding(false));
                Console.WriteLine("FormulaOne formula inventory written.");
                return 0;
            }
            if (String.Equals(GetString(instructions, "mode"), "read_cells", StringComparison.OrdinalIgnoreCase))
            {
                var serializer = new JavaScriptSerializer { MaxJsonLength = Int32.MaxValue };
                File.WriteAllText(args[1], serializer.Serialize(ReadCells(f1, workbook, instructions)), new UTF8Encoding(false));
                Console.WriteLine("FormulaOne cells read.");
                return 0;
            }
            if (String.Equals(GetString(instructions, "mode"), "create_workbook", StringComparison.OrdinalIgnoreCase))
            {
                CreateWorkbook(workbook, instructions);
                Application.DoEvents();
                byte[] createdBlob = (byte[])Invoke(workbook, "WriteToBlob");
                XmlNode createdXml = (XmlNode)Invoke(workbook, "WriteToXml");
                var serializer = new JavaScriptSerializer { MaxJsonLength = Int32.MaxValue };
                File.WriteAllText(
                    args[1],
                    serializer.Serialize(new Dictionary<string, object>
                    {
                        { "blob", Convert.ToBase64String(createdBlob) },
                        { "xml", createdXml.OuterXml },
                    }),
                    new UTF8Encoding(false));
                Console.WriteLine("FormulaOne workbook created: " + createdBlob.Length + " bytes.");
                return 0;
            }
            var sheetIndexes = BuildSheetIndex(workbook);
            foreach (Dictionary<string, object> patch in GetPatches(instructions))
                ApplyPatch(f1, sheetIndexes, patch);
            Application.DoEvents();

            // Deliberately do not call RecalculateExcelFormulas here. It blocks
            // in a noninteractive process; CM recalculates the workbook on open.
            byte[] blob = (byte[])Invoke(workbook, "WriteToBlob");
            File.WriteAllText(args[1], Convert.ToBase64String(blob), Encoding.ASCII);
            Console.WriteLine("FormulaOne blob written: " + blob.Length + " bytes.");
            return 0;
        }
        catch (Exception ex)
        {
            Console.Error.WriteLine(ex.ToString());
            return 1;
        }
        finally
        {
            var disposable = activationScope as IDisposable;
            if (disposable != null) disposable.Dispose();
            if (host != null) host.Dispose();
        }
    }

    private static string RuntimeApi(object value)
    {
        string[] tokens = { "font", "color", "format", "align", "border", "merge", "pattern", "colwidth", "rowheight", "selection" };
        var lines = new List<string>();
        foreach (MemberInfo member in value.GetType().GetMembers(BindingFlags.Public | BindingFlags.Instance))
        {
            bool match = false;
            foreach (string token in tokens)
                if (member.Name.IndexOf(token, StringComparison.OrdinalIgnoreCase) >= 0) { match = true; break; }
            if (!match) continue;
            MethodInfo method = member as MethodInfo;
            if (method != null)
            {
                var parameters = new List<string>();
                foreach (ParameterInfo parameter in method.GetParameters()) parameters.Add(parameter.ParameterType.Name + " " + parameter.Name);
                lines.Add("METHOD " + method.ReturnType.Name + " " + method.Name + "(" + String.Join(", ", parameters.ToArray()) + ")");
            }
            PropertyInfo property = member as PropertyInfo;
            if (property != null) lines.Add("PROPERTY " + property.PropertyType.Name + " " + property.Name);
        }
        lines.Sort(StringComparer.Ordinal);
        return String.Join(Environment.NewLine, lines.ToArray());
    }

    private static List<Dictionary<string, object>> ReadCells(object f1, object workbook, Dictionary<string, object> instructions)
    {
        var result = new List<Dictionary<string, object>>();
        var sheetIndexes = BuildSheetIndex(workbook);
        var probes = instructions.ContainsKey("probes") ? instructions["probes"] as ArrayList : null;
        if (probes == null) return result;
        foreach (object raw in probes)
        {
            var probe = (Dictionary<string, object>)raw;
            string sheet = GetString(probe, "sheet");
            int row = Convert.ToInt32(probe["row"]);
            int column = Convert.ToInt32(probe["column"]);
            if (!sheetIndexes.ContainsKey(sheet)) throw new InvalidOperationException("Workbook sheet was not found: " + sheet);
            int sheetIndex = sheetIndexes[sheet];
            result.Add(new Dictionary<string, object>
            {
                { "sheet", sheet },
                { "row", row },
                { "column", column },
                { "formula", Convert.ToString(Invoke(f1, "get_FormulaSRC", sheetIndex, row, column)) },
                { "text", Convert.ToString(Invoke(f1, "get_TextSRC", sheetIndex, row, column)) },
            });
        }
        return result;
    }

    private static void CreateWorkbook(object workbook, Dictionary<string, object> instructions)
    {
        var requested = instructions.ContainsKey("sheets") ? instructions["sheets"] as ArrayList : null;
        if (requested == null || requested.Count == 0)
            throw new InvalidOperationException("create_workbook requires at least one sheet.");

        int originalCount = Convert.ToInt32(GetProperty(workbook, "NumberOfSheets"));
        foreach (object raw in requested)
        {
            var sheetSpec = (Dictionary<string, object>)raw;
            int insertAt = Convert.ToInt32(GetProperty(workbook, "NumberOfSheets"));
            object sheet = Invoke(workbook, "InsertSheet", insertAt);
            SetProperty(sheet, "Name", GetString(sheetSpec, "name"));
        }
        for (int index = originalCount - 1; index >= 0; index--)
            Invoke(workbook, "DeleteSheet", index);

        object f1 = GetProperty(workbook, "F1Book");
        var sheetIndexes = BuildSheetIndex(workbook);
        foreach (object raw in requested)
        {
            var sheetSpec = (Dictionary<string, object>)raw;
            string name = GetString(sheetSpec, "name");
            if (!sheetIndexes.ContainsKey(name))
                throw new InvalidOperationException("Created workbook sheet was not found: " + name);
            int sheetIndex = sheetIndexes[name];
            var cells = sheetSpec.ContainsKey("cells") ? sheetSpec["cells"] as ArrayList : null;
            if (cells != null)
                foreach (object cellRaw in cells)
                {
                    var cell = (Dictionary<string, object>)cellRaw;
                    var patch = new Dictionary<string, object>(cell);
                    patch["sheet"] = name;
                    ApplyPatch(f1, sheetIndexes, patch);
                    ApplyCellStyle(f1, sheetIndex, patch);
                }
            ApplyDimensions(workbook, name, sheetSpec);
        }
    }

    private static void ApplyCellStyle(object f1, int sheetIndex, Dictionary<string, object> cell)
    {
        string style = GetString(cell, "style").Trim().ToLowerInvariant();
        string numberFormat = GetString(cell, "number_format").Trim();
        if (style.Length == 0 && numberFormat.Length == 0) return;
        int row = Convert.ToInt32(cell["row"]);
        int column = Convert.ToInt32(cell["column"]);
        Invoke(f1, "set_Sheet", sheetIndex);
        Invoke(f1, "SetSelection", row, column, row, column);
        if (numberFormat.Length > 0) SetProperty(f1, "NumberFormat", numberFormat);
        if (style.Length == 0) return;

        bool bold = style == "title" || style == "header" || style == "result" || style == "warning";
        short size = (short)(style == "title" ? 14 : 10);
        Color fontColor = style == "warning" ? Color.DarkRed : Color.Black;
        uint oleFontColor = unchecked((uint)ColorTranslator.ToOle(fontColor));
        Invoke(f1, "SetFont", "Arial", size, bold, false, false, false, oleFontColor, false, false);
        SetProperty(f1, "FontBold", bold);
        Color fill = Color.White;
        if (style == "header") fill = Color.FromArgb(217, 225, 242);
        else if (style == "result") fill = Color.FromArgb(226, 239, 218);
        else if (style == "warning") fill = Color.FromArgb(255, 199, 206);
        if (fill != Color.White) SetProperty(f1, "BackColor", fill);
    }

    private static void ApplyDimensions(object workbook, string sheetName, Dictionary<string, object> sheetSpec)
    {
        object sheet = Invoke(workbook, "GetSheetByName", sheetName);
        var columns = sheetSpec.ContainsKey("column_widths") ? sheetSpec["column_widths"] as ArrayList : null;
        if (columns != null)
            foreach (object raw in columns)
            {
                var item = (Dictionary<string, object>)raw;
                int column = Convert.ToInt32(item["column"]);
                object range = CreateCellRange(workbook, column, 1, column, 1);
                double minimumWidth = Convert.ToDouble(item["width"]);
                Invoke(sheet, "AutoFitColumnWidth", range);
                double fittedWidth = Convert.ToDouble(Invoke(sheet, "GetColumnWidth", column));
                Invoke(sheet, "SetColumnWidth", range, Math.Max(minimumWidth, fittedWidth), false);
            }
        var rows = sheetSpec.ContainsKey("row_heights") ? sheetSpec["row_heights"] as ArrayList : null;
        if (rows != null)
            foreach (object raw in rows)
            {
                var item = (Dictionary<string, object>)raw;
                int row = Convert.ToInt32(item["row"]);
                object range = CreateCellRange(workbook, 1, row, 1, row);
                double minimumHeight = Convert.ToDouble(item["height"]);
                Invoke(sheet, "AutoFitRowHeight", range);
                double fittedHeight = Convert.ToDouble(Invoke(sheet, "GetRowHeight", row));
                Invoke(sheet, "SetRowHeight", range, Math.Max(minimumHeight, fittedHeight));
            }
    }

    private static object CreateCellRange(object workbook, int left, int top, int right, int bottom)
    {
        Assembly assembly = workbook.GetType().Assembly;
        Type rangeType = assembly.GetType("Dionex.Common.Controls.CellRange", true);
        return Activator.CreateInstance(rangeType, new object[] { left, top, right, bottom });
    }

    private static Dictionary<string, object> ReadInstructions(string path)
    {
        // Base64-encoded FormulaOne workbooks routinely exceed the default
        // JavaScriptSerializer input limit for cross-module OQ reports.
        var serializer = new JavaScriptSerializer { MaxJsonLength = Int32.MaxValue };
        return serializer.Deserialize<Dictionary<string, object>>(File.ReadAllText(path, Encoding.UTF8));
    }

    private static object CreateHostedSpreadsheet(Type spreadsheetType, Form host)
    {
        object spreadsheet = Activator.CreateInstance(spreadsheetType);
        var control = spreadsheet as Control;
        if (control != null)
        {
            control.Width = 1;
            control.Height = 1;
            host.Controls.Add(control);
            control.CreateControl();
        }
        Application.DoEvents();
        return spreadsheet;
    }

    private static Dictionary<string, int> BuildSheetIndex(object workbook)
    {
        var indexes = new Dictionary<string, int>(StringComparer.Ordinal);
        var sheets = (IEnumerable)GetProperty(workbook, "Sheets");
        int index = 1;
        foreach (object sheet in sheets)
        {
            indexes[(string)GetProperty(sheet, "Name")] = index++;
        }
        return indexes;
    }

    private static IEnumerable<Dictionary<string, object>> GetPatches(Dictionary<string, object> instructions)
    {
        var values = instructions.ContainsKey("patches") ? instructions["patches"] as ArrayList : null;
        if (values == null) yield break;
        foreach (object value in values)
            yield return (Dictionary<string, object>)value;
    }

    private static void ApplyPatch(object f1, Dictionary<string, int> sheetIndexes, Dictionary<string, object> patch)
    {
        string sheet = GetString(patch, "sheet");
        int row = Convert.ToInt32(patch["row"]);
        int column = Convert.ToInt32(patch["column"]);
        string kind = GetString(patch, "kind");
        if (!sheetIndexes.ContainsKey(sheet)) throw new InvalidOperationException("Workbook sheet was not found: " + sheet);
        int sheetIndex = sheetIndexes[sheet];
        object value = patch.ContainsKey("value") ? patch["value"] : "";
        if (kind == "formula")
        {
            string formula = Convert.ToString(value).Trim();
            if (formula.StartsWith("=")) formula = formula.Substring(1);
            if (formula.Length == 0) throw new InvalidOperationException("Formula patch is empty.");
            Invoke(f1, "set_FormulaSRC", sheetIndex, row, column, formula);
        }
        else if (kind == "number") Invoke(f1, "set_NumberSRC", sheetIndex, row, column, Convert.ToDouble(value));
        else if (kind == "text") Invoke(f1, "set_TextSRC", sheetIndex, row, column, Convert.ToString(value));
        else throw new InvalidOperationException("Unsupported patch kind: " + kind);
    }

    private static List<Dictionary<string, object>> ReadFormulaInventory(object f1, object workbook)
    {
        var rows = new List<Dictionary<string, object>>();
        var sheetIndexes = BuildSheetIndex(workbook);
        foreach (var item in sheetIndexes)
        {
            string name = item.Key;
            int sheet = item.Value;
            Invoke(f1, "set_Sheet", sheet);
            int lastRow = Convert.ToInt32(GetProperty(f1, "LastRow"));
            int lastColumn = Convert.ToInt32(GetProperty(f1, "LastCol"));
            for (int row = 1; row <= lastRow; row++)
            {
                for (int column = 1; column <= lastColumn; column++)
                {
                    string formula = Convert.ToString(Invoke(f1, "get_FormulaSRC", sheet, row, column));
                    if (String.IsNullOrWhiteSpace(formula)) continue;
                    rows.Add(new Dictionary<string, object>
                    {
                        { "sheet", name },
                        { "row", row },
                        { "column", column },
                        { "formula", formula },
                    });
                }
            }
        }
        return rows;
    }

    private static object GetProperty(object value, string name)
    {
        return value.GetType().InvokeMember(name, BindingFlags.GetProperty, null, value, null);
    }

    private static void SetProperty(object value, string name, object propertyValue)
    {
        value.GetType().InvokeMember(name, BindingFlags.SetProperty, null, value, new object[] { propertyValue });
    }

    private static object Invoke(object value, string name, params object[] args)
    {
        return value.GetType().InvokeMember(name, BindingFlags.InvokeMethod, null, value, args);
    }

    private static string GetString(Dictionary<string, object> values, string key)
    {
        return values.ContainsKey(key) && values[key] != null ? Convert.ToString(values[key]) : "";
    }
}
