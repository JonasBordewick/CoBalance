namespace CoBalance.Simulations
{
    public static class SimulationAPI
    {
        /// <summary>
        /// Marks the end of a simulation run. Triggers fitness calculation via
        /// <see cref="IGeneticAlgorithmFitnessEvaluator"/> and terminates the session.
        /// Must be called exactly once when the simulation reaches its natural end condition.
        /// </summary>
        /// <param name="reason">Optional label identifying the end condition (e.g. "timeout", "playerWon"). Used for diagnostics.</param>
        public static void FinishScenario(string reason = null)
        {
            SimulationRunTerminator.FinishRun(reason);
        }
    }
}