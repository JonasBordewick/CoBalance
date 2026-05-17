#if UNITY_EDITOR
using System;
using System.Collections.Generic;
using System.IO;
using BalancingFramework.DTO;
using UnityEditor;
using UnityEngine;

namespace BalancingFramework.Simulations
{
    public static class JobContext
    {
        private const string KeyIsJobMode = "BalancingFramework.JobContext.IsJobMode";
        private const string KeyConfigPath = "BalancingFramework.JobContext.ConfigPath";
        private const string KeyCounter = "BalancingFramework.JobContext.Counter";
        private const string KeyIgnoreLog = "BalancingFramework.JobContext.IgnoreLog";
        private const string KeyCurrentBalancePath = "BalancingFramework.JobContext.CurrentBalancePath";

        private static JobSettingsDTO _cachedJobSettings;
        private static List<JobRunDefinition> _cachedRunPlan;

        public class JobRunDefinition
        {
            public int GlobalIndex;
            public int TotalRuns;
            public string Counter;
            public string BalanceFilePath;
            public int LocalIteration;
        }

        public static bool IsJobMode
        {
            get => SessionState.GetBool(KeyIsJobMode, false);
            private set => SessionState.SetBool(KeyIsJobMode, value);
        }

        public static string ConfigPath
        {
            get => SessionState.GetString(KeyConfigPath, null);
            private set => SessionState.SetString(KeyConfigPath, value ?? string.Empty);
        }

        public static string Counter
        {
            get
            {
                var value = SessionState.GetString(KeyCounter, string.Empty);
                return string.IsNullOrEmpty(value) ? null : value;
            }
            private set => SessionState.SetString(KeyCounter, value ?? string.Empty);
        }

        public static bool IgnoreLog
        {
            get => SessionState.GetBool(KeyIgnoreLog, false);
            private set => SessionState.SetBool(KeyIgnoreLog, value);
        }

        public static string CurrentBalancePath
        {
            get
            {
                var overridePath = SessionState.GetString(KeyCurrentBalancePath, string.Empty);
                if (!string.IsNullOrEmpty(overridePath))
                    return overridePath;

                return CurrentJobSettings?.input?.balanceFilePath;
            }
            private set => SessionState.SetString(KeyCurrentBalancePath, value ?? string.Empty);
        }

        public static JobSettingsDTO CurrentJobSettings
        {
            get
            {
                if (!IsJobMode)
                    return null;

                if (_cachedJobSettings != null)
                    return _cachedJobSettings;

                var configPath = ConfigPath;
                if (string.IsNullOrEmpty(configPath) || !File.Exists(configPath))
                {
                    Debug.LogError("JobContext: ConfigPath is missing or file does not exist.");
                    return null;
                }

                _cachedJobSettings = JsonSerializer.ReadJson<JobSettingsDTO>(configPath);
                return _cachedJobSettings;
            }
        }

        public static string CurrentJobType => CurrentJobSettings?.jobType;

        public static int TotalIterations => GetRunPlan().Count;
        
        public static string CurrentCandidateId => ExtractCandidateId(CurrentBalancePath);

        public static string ExtractCandidateId(string balancePath)
        {
            if (string.IsNullOrWhiteSpace(balancePath))
                return null;

            var fileName = Path.GetFileNameWithoutExtension(balancePath);
            const string suffix = "_balance";

            if (fileName.EndsWith(suffix, StringComparison.OrdinalIgnoreCase))
                return fileName.Substring(0, fileName.Length - suffix.Length);

            return fileName;
        }

        public static void SetJob(string configPath, string balanceFilePath = null, string counter = null, bool ignoreLog = false)
        {
            IsJobMode = true;
            ConfigPath = configPath;
            Counter = counter;
            IgnoreLog = ignoreLog;
            CurrentBalancePath = balanceFilePath;

            _cachedJobSettings = null;
            _cachedRunPlan = null;

            _cachedJobSettings = JsonSerializer.ReadJson<JobSettingsDTO>(configPath);

            if (counter != null)
                Debug.Log("Job mode enabled with counter: " + counter);
        }
        
        public static void SetSimulation(string configPath, string counter = null, bool ignoreLog = false)
        {
            SetJob(configPath, null, counter, ignoreLog);
        }

        public static JobRunDefinition GetRunAt(int index)
        {
            var runPlan = GetRunPlan();
            if (index < 0 || index >= runPlan.Count)
                return null;

            return runPlan[index];
        }

        public static List<JobRunDefinition> GetRunPlan()
        {
            if (_cachedRunPlan != null)
                return _cachedRunPlan;

            _cachedRunPlan = BuildRunPlan(CurrentJobSettings);
            return _cachedRunPlan;
        }

        private static List<JobRunDefinition> BuildRunPlan(JobSettingsDTO settings)
        {
            var result = new List<JobRunDefinition>();

            if (settings?.input == null)
                return result;

            switch (settings.jobType)
            {
                case JobTypes.Simulation:
                {
                    var total = settings.input.iterations;
                    for (int i = 0; i < total; i++)
                    {
                        result.Add(new JobRunDefinition
                        {
                            GlobalIndex = i,
                            TotalRuns = total,
                            BalanceFilePath = settings.input.balanceFilePath,
                            LocalIteration = i
                        });
                    }
                    break;
                }

                case JobTypes.GeneticAlgorithm:
                {
                    var balanceFiles = settings.input.balanceFilePaths ?? new List<string>();
                    int perFileRuns = settings.input.iterationsPerBalanceFile;
                    int globalIndex = 0;
                    int total = balanceFiles.Count * perFileRuns;

                    foreach (var balanceFile in balanceFiles)
                    {
                        for (int i = 0; i < perFileRuns; i++)
                        {
                            result.Add(new JobRunDefinition
                            {
                                GlobalIndex = globalIndex++,
                                TotalRuns = total,
                                BalanceFilePath = balanceFile,
                                LocalIteration = i
                            });
                        }
                    }
                    break;
                }

                default:
                    Debug.LogError($"Unsupported jobType: {settings?.jobType}");
                    break;
            }

            int width = Math.Max(1, result.Count.ToString().Length);
            foreach (var run in result)
            {
                run.Counter = run.GlobalIndex.ToString($"D{width}");
            }

            return result;
        }

        public static void Clear()
        {
            IsJobMode = false;
            ConfigPath = null;
            Counter = null;
            IgnoreLog = false;
            CurrentBalancePath = null;

            _cachedJobSettings = null;
            _cachedRunPlan = null;

            SessionState.EraseBool(KeyIsJobMode);
            SessionState.EraseString(KeyConfigPath);
            SessionState.EraseString(KeyCounter);
            SessionState.EraseBool(KeyIgnoreLog);
            SessionState.EraseString(KeyCurrentBalancePath);
        }

        public static string DebugString()
        {
            if (!IsJobMode)
                return "JobContext: Not in job mode.";

            var settings = CurrentJobSettings;
            if (settings == null)
                return $"JobContext: Job mode enabled, but settings could not be loaded. ConfigPath: {ConfigPath}";

            return $"JobContext: Job mode enabled. ConfigPath: {ConfigPath}, JobId: {settings.jobId}, JobType: {settings.jobType}";
        }
    }
}
#endif