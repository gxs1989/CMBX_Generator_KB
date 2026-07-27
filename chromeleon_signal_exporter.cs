using System;
using System.Globalization;
using System.IO;
using Dionex.Chromeleon.RawData;

class ChromeleonSignalExporter
{
    static int Main(string[] args)
    {
        if (args.Length < 3)
        {
            Console.Error.WriteLine("usage: ChromeleonSignalExporter raw-file output-tsv channel-name");
            return 2;
        }

        string rawPath = args[0];
        string outputPath = args[1];
        string channelName = args[2];
        var culture = CultureInfo.InvariantCulture;

        using (var stream = File.OpenRead(rawPath))
        {
            var metadata = new SignalMetadata();
            var reader = NativeSignalReader.Create(stream, metadata, false);
            using (var writer = new StreamWriter(outputPath, false))
            {
                writer.WriteLine("Channel\t" + channelName);
                writer.WriteLine("Time (min)\tStep (s)\tValue");
                for (int i = 0; i < reader.Count; i++)
                {
                    var point = reader[i];
                    double stepSeconds = i == 0 ? 0.0 : (reader[i].X - reader[i - 1].X) * 60.0;
                    writer.Write(point.X.ToString("0.############", culture));
                    writer.Write("\t");
                    writer.Write(stepSeconds.ToString("0.############", culture));
                    writer.Write("\t");
                    writer.WriteLine(point.Y.ToString("0.############", culture));
                }
            }
        }

        return 0;
    }
}
