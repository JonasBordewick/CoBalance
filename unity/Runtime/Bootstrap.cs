using System.IO;
using BalancingFramework.DTO;
using BalancingFramework.Logger;
using BalancingFramework.Simulations;
using UnityEngine;

namespace BalancingFramework
{
    public static class Bootstrap
    {
        [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.BeforeSceneLoad)]
        private static void Initialize()
        {
            InitializeSimulationBootstrap();
            InitializeBalance();
            InitializeGameStatLogger();
        }
        private static void InitializeSimulationBootstrap()
        {
            if (!JobContext.IsJobMode)
            {
                Debug.Log("Not in Simulation Mode");
                return;
            }
            
            var go = new GameObject("[BalancingFramework] Simulation");
            go.AddComponent<SimulationBootstrap>();
        }

        private static void InitializeBalance()
        {
            var settings = BalanceFrameworkSettings.Load();
            var balancePath = Utilities.GetBalanceFilePath(settings.defaultBalanceFile);
            
            if (JobContext.IsJobMode)
            {
                balancePath = JobContext.CurrentBalancePath;
            }
            
            BalanceRepository.ImportNewFromFile(balancePath);
        }
        
        private static void InitializeGameStatLogger()
        {
            if (JobContext.IgnoreLog) return;
            BalancingFrameworkLogger.LogInfo("Initializing Balancing Framework...");
            var go = new GameObject("[BalancingFramework] Logger");
            go.AddComponent<GameStatLogger>();
        }

        
    }
}