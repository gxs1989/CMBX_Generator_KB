using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Reflection;
using Dionex.Chromeleon.Data.Common;
using Dionex.InstrumentServerInterfaces;

class ChromeleonAuditExporter
{
    static int Main(string[] args)
    {
        if (args.Length < 2)
        {
            Console.Error.WriteLine("usage: ChromeleonAuditExporter raw-audit-file output-tsv");
            return 2;
        }

        string rawPath = args[0];
        string outputPath = args[1];
        var culture = CultureInfo.InvariantCulture;
        var messages = new List<AuditTrailMessage>();

        using (var stream = File.OpenRead(rawPath))
        {
            AuditTrailCompression.UncompressAndDeserialize(stream, messages);
        }

        using (var writer = new StreamWriter(outputPath, false))
        {
            writer.WriteLine("Index\tRetentionTime(min)\tDevice\tMessage\tTriggerName\tPropertyName\tPropertyValue\tDayTime");
            for (int i = 0; i < messages.Count; i++)
            {
                var msg = messages[i];
                string retention = msg.RetentionTime.HasValue
                    ? msg.RetentionTime.Value.ToString("0.############", culture)
                    : "";
                writer.Write(i.ToString(culture));
                writer.Write("\t");
                writer.Write(Sanitize(retention));
                writer.Write("\t");
                writer.Write(Sanitize(msg.Device));
                writer.Write("\t");
                writer.Write(Sanitize(msg.Message));
                writer.Write("\t");
                writer.Write(Sanitize(msg.TriggerName));
                writer.Write("\t");
                writer.Write(Sanitize(msg.PropertyName));
                writer.Write("\t");
                writer.Write(Sanitize(msg.PropertyValue));
                writer.Write("\t");
                writer.WriteLine(Sanitize(DayTime(msg)));
            }
        }

        return 0;
    }

    static string Sanitize(string value)
    {
        if (value == null)
        {
            return "";
        }
        return value.Replace("\t", " ").Replace("\r", " ").Replace("\n", " ").Trim();
    }

    static string DayTime(AuditTrailMessage msg)
    {
        string[] preferredNames = new string[]
        {
            "DayTime",
            "DateTime",
            "TimeStamp",
            "Timestamp",
            "Time",
            "CreationTime",
            "Created",
            "AuditTime",
            "SystemTime"
        };

        Type type = msg.GetType();
        foreach (string name in preferredNames)
        {
            PropertyInfo prop = type.GetProperty(name);
            string formatted = FormatDayTime(prop == null ? null : prop.GetValue(msg, null));
            if (!String.IsNullOrEmpty(formatted))
            {
                return formatted;
            }
        }

        foreach (PropertyInfo prop in type.GetProperties())
        {
            string name = prop.Name.ToLowerInvariant();
            if (name == "retentiontime")
            {
                continue;
            }
            if (name.Contains("time") || name.Contains("date"))
            {
                string formatted = FormatDayTime(prop.GetValue(msg, null));
                if (!String.IsNullOrEmpty(formatted))
                {
                    return formatted;
                }
            }
        }
        return "";
    }

    static string FormatDayTime(object value)
    {
        if (value == null)
        {
            return "";
        }
        if (value is DateTime)
        {
            DateTime dt = (DateTime)value;
            return dt.ToString("yyyy-MM-dd HH:mm:ss", CultureInfo.InvariantCulture);
        }
        if (value is DateTimeOffset)
        {
            DateTimeOffset dto = (DateTimeOffset)value;
            return dto.ToString("yyyy-MM-dd HH:mm:ss", CultureInfo.InvariantCulture);
        }
        string text = Convert.ToString(value, CultureInfo.InvariantCulture);
        return text == null ? "" : text;
    }
}
