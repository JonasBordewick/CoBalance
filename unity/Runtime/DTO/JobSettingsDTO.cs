using System;
using System.Collections.Generic;

namespace BalancingFramework.DTO
{
    public static class JobTypes
    {
        public const string Simulation = "simulation";
        public const string GeneticAlgorithm = "geneticAlgorithm";
    }

    [Serializable]
    public class JobSettingsDTO : IExportableDTO
    {
        public string version;
        public string jobId;
        public string jobType;
        public JobInputDTO input;
        public JobExecution execution;

        public bool IsValidForExport()
        {
            if (string.IsNullOrWhiteSpace(jobId))
                return false;

            if (input == null)
                return false;

            if (string.IsNullOrWhiteSpace(input.scenePath))
                return false;

            switch (jobType)
            {
                case JobTypes.Simulation:
                    return !string.IsNullOrWhiteSpace(input.balanceFilePath)
                           && input.iterations > 0;

                case JobTypes.GeneticAlgorithm:
                    return input.balanceFilePaths != null
                           && input.balanceFilePaths.Count > 0
                           && input.iterationsPerBalanceFile > 0;

                default:
                    return false;
            }
        }
    }

    [Serializable]
    public class JobInputDTO
    {
        public string scenePath;

        public string balanceFilePath;
        public int iterations;

        public List<string> balanceFilePaths;
        public int iterationsPerBalanceFile;
        public string resultFilePath;
        public string progressFilePath;
    }

    [Serializable]
    public class JobExecution
    {
        public float timeScale;
        public float fixedDeltaTime;
        public float maxSimulationTime;
    }
}