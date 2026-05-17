using System.Linq;
using UnityEngine;

namespace BalancingFramework.Simulations
{
    public static class SimulationRunTerminator
    {
        private static bool _isFinishing;

        public static void FinishRun(string reason = null)
        {
            if (_isFinishing)
                return;

            _isFinishing = true;

            try
            {
                WriteFitness();
            }
            finally
            {
#if UNITY_EDITOR
                UnityEditor.EditorApplication.ExitPlaymode();
                _isFinishing = false;
#else
                Debug.LogWarning("FinishRun called outside Unity Editor.");
#endif
            }
        }

        private static void WriteFitness()
        {
            var evaluator = Object
                .FindObjectsByType<MonoBehaviour>(FindObjectsInactive.Include, FindObjectsSortMode.None)
                .OfType<IGeneticAlgorithmFitnessEvaluator>()
                .FirstOrDefault();

            if (evaluator == null)
            {
                // Debug.LogError("No SimulationFitnessEvaluator found in scene.");
                return;
            }

            float fitness;
            try
            {
                fitness = evaluator.CalculateFitness();
            }
            catch (System.Exception ex)
            {
                Debug.LogError($"Fitness calculation failed: {ex}");
                return;
            }

            GeneticAlgorithmFitnessRecorder.AppendCurrentRun(fitness);
        }

        public static void ResetState()
        {
            _isFinishing = false;
        }
    }
}