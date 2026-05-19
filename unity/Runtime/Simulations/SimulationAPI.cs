namespace CoBalance.Simulations
{
    public static class SimulationAPI
    {
        public static void FinishScenario(string reason = null)
        {
            SimulationRunTerminator.FinishRun(reason);
        }
    }
}