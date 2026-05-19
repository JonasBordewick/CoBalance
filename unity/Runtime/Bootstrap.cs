using System.IO;
using CoBalance.DTO;
using CoBalance.Logger;
using CoBalance.Simulations;
using UnityEngine;

namespace CoBalance
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
            
            var go = new GameObject("[CoBalance] Simulation");
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
            CoBalanceLogger.LogInfo("Initializing Balancing Framework...");
            var go = new GameObject("[CoBalance] Logger");
            go.AddComponent<GameStatLogger>();
        }

        
    }
}