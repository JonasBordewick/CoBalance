using System;
using System.IO;
using CoBalance.Simulations;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;

namespace CoBalance.Editor
{
    [Serializable]
    public struct IterationProgress
    {
        public int currentIteration;
    }
    
    [InitializeOnLoad]
    public static class SimulationBatchEntry
    {
        private const string SessionKeyIsRunning = "SimulationBatchEntry.IsRunning";
        private const string SessionKeyConfigPath = "SimulationBatchEntry.ConfigPath";
        private const string SessionKeyIgnoreLog = "SimulationBatchEntry.IgnoreLog";
        private const string SessionKeyCurrentIteration = "SimulationBatchEntry.CurrentIteration";

        static SimulationBatchEntry()
        {
            EditorApplication.playModeStateChanged -= OnPlayModeChanged;
            EditorApplication.playModeStateChanged += OnPlayModeChanged;
        }

        public static void Run()
        {
            var configPath = Utilities.GetArg("-jobConfig");
            if (string.IsNullOrEmpty(configPath) || !File.Exists(configPath))
            {
                StopBatch();
                return;
            }

            SessionState.SetBool(SessionKeyIsRunning, true);
            SessionState.SetString(SessionKeyConfigPath, configPath);
            SessionState.SetBool(SessionKeyIgnoreLog, Utilities.HasArg("-ignoreLog"));
            SessionState.SetInt(SessionKeyCurrentIteration, 0);
            
            var iteration = SessionState.GetInt(SessionKeyCurrentIteration, 0);
            var ignoreLog = SessionState.GetBool(SessionKeyIgnoreLog, false);

            if (string.IsNullOrEmpty(configPath) || !File.Exists(configPath))
            {
                StopBatch();
                return;
            }
            
            JobContext.SetJob(configPath, ignoreLog: ignoreLog);
            
            EditorSceneManager.OpenScene(JobContext.CurrentJobSettings.input.scenePath);
            
            
            RunNextIteration();
        }

        private static void OnPlayModeChanged(PlayModeStateChange state)
        {
            if (!SessionState.GetBool(SessionKeyIsRunning, false))
                return;

            if (state == PlayModeStateChange.EnteredEditMode)
            {
                RunNextIteration();
            }
        }

        private static void RunNextIteration()
        {
            if (!SessionState.GetBool(SessionKeyIsRunning, false))
                return;

            int iteration = SessionState.GetInt(SessionKeyCurrentIteration, 0);
            string configPath = SessionState.GetString(SessionKeyConfigPath, "");
            bool ignoreLog = SessionState.GetBool(SessionKeyIgnoreLog, false);

            if (string.IsNullOrEmpty(configPath) || !File.Exists(configPath))
            {
                StopBatch();
                return;
            }

            // Job laden, damit TotalIterations / RunPlan verfügbar sind
            JobContext.SetJob(configPath, ignoreLog: ignoreLog);

            if (iteration >= JobContext.TotalIterations)
            {
                GeneticAlgorithmFitnessResultFinalizer.FinalizeResults();
                StopBatch();
                EditorApplication.Exit(0);
                return;
            }

            var run = JobContext.GetRunAt(iteration);
            if (run == null)
            {
                Debug.LogError($"No run definition found for iteration index {iteration}.");
                StopBatch();
                EditorApplication.Exit(1);
                return;
            }
            
            // TODO: PUSH THE NEW ITERATION PROGRESS TO FILE SO THAT THE GUI CAN SEE THE PROGRESS
            // var progress = new IterationProgress();
            // progress.currentIteration = iteration;
            // var json = JsonUtility.ToJson(progress);
            // File.WriteAllText(JobContext.CurrentJobSettings.input.progressFilePath, json);
            
            //Debug.Log(
            //    $"Starting run {iteration + 1}/{JobContext.TotalIterations} | " +
            //    $"jobType={JobContext.CurrentJobType} | " +
            //    $"balanceFile={run.BalanceFilePath}");

            RunSingleIteration(configPath, run, ignoreLog);

            SessionState.SetInt(SessionKeyCurrentIteration, iteration + 1);
        }

        public static void RunSingleIteration(string configPath, JobContext.JobRunDefinition run, bool ignoreLog = false)
        {
            JobContext.SetJob(configPath, run.BalanceFilePath, run.Counter, ignoreLog);

            // EditorSceneManager.OpenScene(JobContext.CurrentJobSettings.input.scenePath);
            EditorApplication.EnterPlaymode();
        }

        private static void StopBatch()
        {
            SessionState.EraseBool(SessionKeyIsRunning);
            SessionState.EraseString(SessionKeyConfigPath);
            SessionState.EraseBool(SessionKeyIgnoreLog);
            SessionState.EraseInt(SessionKeyCurrentIteration);

            JobContext.Clear();
        }
    }
}