using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Text;
using CoBalance.Simulations;
using UnityEngine;

namespace CoBalance.Editor
{
    public static class GeneticAlgorithmFitnessResultFinalizer
    {
        [Serializable]
        private class FitnessRunLine
        {
            public string candidateId;
            public float fitness;
        }

        public static void FinalizeResults()
        {
            var inputPath = GeneticAlgorithmFitnessRecorder.GetTempResultsPath();
            var outputPath = JobContext.CurrentJobSettings.input.resultFilePath;

            if (!File.Exists(inputPath))
            {
                Debug.LogWarning($"No fitness temp file found at: {inputPath}");
                return;
            }

            var map = new Dictionary<string, List<float>>();

            foreach (var line in File.ReadAllLines(inputPath))
            {
                if (string.IsNullOrWhiteSpace(line))
                    continue;

                FitnessRunLine entry;
                try
                {
                    entry = JsonUtility.FromJson<FitnessRunLine>(line);
                }
                catch (Exception ex)
                {
                    Debug.LogError($"Could not parse fitness line: {ex}");
                    continue;
                }

                if (entry == null || string.IsNullOrWhiteSpace(entry.candidateId))
                    continue;

                if (!map.TryGetValue(entry.candidateId, out var values))
                {
                    values = new List<float>();
                    map[entry.candidateId] = values;
                }

                values.Add(entry.fitness);
            }

            var dir = Path.GetDirectoryName(outputPath);
            if (!string.IsNullOrEmpty(dir))
                Directory.CreateDirectory(dir);

            File.WriteAllText(outputPath, BuildJson(map), Encoding.UTF8);
            Debug.Log($"Final fitness file written: {outputPath}");
            try
            {
                File.Delete(inputPath);
            }
            catch (Exception ex)
            {
                Debug.LogWarning($"Could not delete temp fitness file: {ex}");
            }
        }

        private static string BuildJson(Dictionary<string, List<float>> map)
        {
            var sb = new StringBuilder();
            var culture = CultureInfo.InvariantCulture;

            sb.AppendLine("{");

            int i = 0;
            foreach (var kvp in map)
            {
                sb.Append($"  \"{Escape(kvp.Key)}\": [");

                for (int j = 0; j < kvp.Value.Count; j++)
                {
                    if (j > 0)
                        sb.Append(", ");

                    sb.Append(kvp.Value[j].ToString(culture));
                }

                sb.Append("]");

                if (i < map.Count - 1)
                    sb.Append(",");

                sb.AppendLine();
                i++;
            }

            sb.AppendLine("}");
            return sb.ToString();
        }

        private static string Escape(string value)
        {
            return value.Replace("\\", "\\\\").Replace("\"", "\\\"");
        }
    }
}