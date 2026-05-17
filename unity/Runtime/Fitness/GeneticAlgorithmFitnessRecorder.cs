#if UNITY_EDITOR
using System;
using System.IO;
using BalancingFramework.Simulations;
using UnityEngine;

namespace BalancingFramework
{
    public static class GeneticAlgorithmFitnessRecorder
    {
        [Serializable]
        private class GeneticAlgorithmFitnessRunLine
        {
            public string candidateId;
            public float fitness;
        }

        public static string GetTempResultsPath()
        {
            var jobId = JobContext.CurrentJobSettings?.jobId ?? "job";
            return Path.Combine(
                Utilities.GetFrameworkFolderPath(),
                $".{jobId}_fitness_runs.jsonl"
            );
        }

        public static string GetFinalResultsPath()
        {
            var jobId = JobContext.CurrentJobSettings?.jobId ?? "job";
            return Path.Combine(
                Utilities.GetFrameworkFolderPath(),
                $".{jobId}_fitness.json"
            );
        }

        public static void AppendCurrentRun(float fitness)
        {
            var candidateId = JobContext.CurrentCandidateId;
            if (string.IsNullOrWhiteSpace(candidateId))
            {
                Debug.LogError("FitnessResultRecorder: candidateId could not be determined.");
                return;
            }

            var path = GetTempResultsPath();
            var dir = Path.GetDirectoryName(path);
            if (!string.IsNullOrEmpty(dir))
                Directory.CreateDirectory(dir);

            var line = new GeneticAlgorithmFitnessRunLine()
            {
                candidateId = candidateId,
                fitness = fitness
            };

            var json = JsonUtility.ToJson(line);
            File.AppendAllText(path, json + Environment.NewLine);
        }
    }
}
#endif