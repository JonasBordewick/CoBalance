using UnityEngine;

namespace BalancingFramework
{
    /// <summary>
    /// Interface <c>IGeneticAlgorithmFitnessEvaluator</c> defines all methods
    /// which will be executed, if the plugin is started with job type genetic algortihm
    public interface IGeneticAlgorithmFitnessEvaluator
    {
        /// <summary>
        /// Method <c>CalculateFitness</c> will be executed at the end of a run.
        /// in here the fitness of the current run should be calculated and returend
        /// as a float
        public float CalculateFitness();
    }
}