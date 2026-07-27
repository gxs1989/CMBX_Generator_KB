using System;
using System.IO;
using System.Linq;
using System.Reflection;

internal static class FormulaOneApiProbe
{
    private static int Main(string[] args)
    {
        if (args.Length != 1)
        {
            Console.Error.WriteLine("Usage: formulaone_api_probe.exe <Chromeleon bin>");
            return 2;
        }
        string bin = args[0];
        Environment.SetEnvironmentVariable("PATH", bin + ";" + Environment.GetEnvironmentVariable("PATH"));
        AppDomain.CurrentDomain.AssemblyResolve += delegate(object sender, ResolveEventArgs eventArgs)
        {
            string candidate = Path.Combine(bin, new AssemblyName(eventArgs.Name).Name + ".dll");
            return File.Exists(candidate) ? Assembly.LoadFrom(candidate) : null;
        };
        try
        {
            Assembly controls = Assembly.LoadFrom(Path.Combine(bin, "Dionex.Controls.dll"));
            Type spreadsheet = controls.GetType("Dionex.Common.Controls.FormulaOneSpreadsheet", true);
            PrintType("FormulaOneSpreadsheet", spreadsheet);
            foreach (PropertyInfo property in spreadsheet.GetProperties(BindingFlags.Public | BindingFlags.Instance))
            {
                if (property.Name != "Workbook") continue;
                Type workbookType = property.PropertyType;
                PrintType("Workbook", workbookType);
                PrintRelatedTypes(workbookType);
            }
            return 0;
        }
        catch (Exception ex)
        {
            Console.Error.WriteLine(ex.ToString());
            return 1;
        }
    }

    private static void PrintRelatedTypes(Type workbookType)
    {
        var seen = new System.Collections.Generic.HashSet<Type>();
        var pending = new System.Collections.Generic.Queue<Type>();
        pending.Enqueue(workbookType);
        while (pending.Count > 0)
        {
            Type current = pending.Dequeue();
            if (!seen.Add(current)) continue;
            foreach (MemberInfo member in current.GetMembers(BindingFlags.Public | BindingFlags.Instance))
            {
                PropertyInfo property = member as PropertyInfo;
                if (property != null) EnqueueRelatedType(pending, seen, property.PropertyType);
                MethodInfo method = member as MethodInfo;
                if (method == null) continue;
                EnqueueRelatedType(pending, seen, method.ReturnType);
                foreach (ParameterInfo parameter in method.GetParameters()) EnqueueRelatedType(pending, seen, parameter.ParameterType);
            }
        }
        foreach (Type type in seen.Where(t => t != workbookType && IsSpreadsheetType(t)).OrderBy(t => t.FullName))
            PrintType(type.Name, type);
    }

    private static void EnqueueRelatedType(System.Collections.Generic.Queue<Type> pending, System.Collections.Generic.ISet<Type> seen, Type type)
    {
        var types = new System.Collections.Generic.HashSet<Type>();
        AddRelatedType(types, type);
        foreach (Type item in types)
            if (IsSpreadsheetType(item) && !seen.Contains(item)) pending.Enqueue(item);
    }

    private static void AddRelatedType(System.Collections.Generic.ISet<Type> types, Type type)
    {
        if (type == null || type == typeof(void)) return;
        if (type.IsArray) type = type.GetElementType();
        if (type.IsGenericType)
            foreach (Type argument in type.GetGenericArguments()) AddRelatedType(types, argument);
        types.Add(type);
    }

    private static bool IsSpreadsheetType(Type type)
    {
        if (type == null || type.FullName == null) return false;
        string name = type.FullName;
        return name.StartsWith("Dionex.Common.Controls", StringComparison.Ordinal)
            || name.IndexOf("SpreadSheet", StringComparison.OrdinalIgnoreCase) >= 0
            || name.IndexOf("FormulaOne", StringComparison.OrdinalIgnoreCase) >= 0;
    }

    private static void PrintType(string label, Type type)
    {
        Console.WriteLine("## " + label + " :: " + type.FullName);
        string[] tokens = { "sheet", "insert", "delete", "name", "formula", "text", "number", "row", "col", "cell", "range", "merge", "format", "style", "font", "color", "border", "align", "width", "height", "blob", "xml", "print", "page", "visible" };
        var members = type.GetMembers(BindingFlags.Public | BindingFlags.Instance)
            .Where(member => tokens.Any(token => member.Name.IndexOf(token, StringComparison.OrdinalIgnoreCase) >= 0))
            .OrderBy(member => member.MemberType).ThenBy(member => member.Name);
        foreach (MemberInfo member in members)
        {
            ConstructorInfo constructor = member as ConstructorInfo;
            if (constructor != null)
            {
                string constructorParameters = String.Join(", ", constructor.GetParameters().Select(p => p.ParameterType.Name + " " + p.Name));
                Console.WriteLine("CTOR " + type.Name + "(" + constructorParameters + ")");
                continue;
            }
            MethodInfo method = member as MethodInfo;
            if (method != null)
            {
                string parameters = String.Join(", ", method.GetParameters().Select(p => p.ParameterType.Name + " " + p.Name));
                Console.WriteLine("METHOD " + method.ReturnType.Name + " " + method.Name + "(" + parameters + ")");
                continue;
            }
            PropertyInfo property = member as PropertyInfo;
            if (property != null)
                Console.WriteLine("PROPERTY " + property.PropertyType.Name + " " + property.Name + " get=" + property.CanRead + " set=" + property.CanWrite);
        }
        foreach (ConstructorInfo constructor in type.GetConstructors(BindingFlags.Public | BindingFlags.Instance))
        {
            string parameters = String.Join(", ", constructor.GetParameters().Select(p => p.ParameterType.Name + " " + p.Name));
            Console.WriteLine("CTOR " + type.Name + "(" + parameters + ")");
        }
    }
}
