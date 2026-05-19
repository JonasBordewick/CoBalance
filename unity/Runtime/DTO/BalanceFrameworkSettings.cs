using System;
using UnityEditor;
using UnityEngine;

namespace CoBalance.DTO
{
    [Serializable]
    public class BalanceFrameworkSettings : IExportableDTO
    {
        public string version;
        public bool enableTimeBasedLogging;
        public int defaultLogTickRate;
        public string defaultBalanceFile;
        public string unityApplicationPath;
        public string projectPath;

        public bool IsValidForExport()
        {
            return true;
        }
        
        public static BalanceFrameworkSettings CreateDefault()
        {

            var assetPath = Application.dataPath;
            // get Parent dir of asset Path
            
            var projectPath = System.IO.Directory.GetParent(assetPath)?.FullName ?? assetPath;

            var applicationPath = System.IO.Path.GetFullPath(EditorApplication.applicationPath);
            
            
            return new BalanceFrameworkSettings
            {
                version = "1.0",
                enableTimeBasedLogging = true,
                defaultLogTickRate = 50,
                defaultBalanceFile = "default_balance.json",
                unityApplicationPath = applicationPath,
                projectPath = projectPath
            };
        }

        public static BalanceFrameworkSettings Load()
        {
            var filePath = System.IO.Path.Combine(
                Utilities.GetFrameworkFolderPath(),
                "project.cb"
            );
            
            if (System.IO.File.Exists(filePath))
            {
                return JsonSerializer.ReadJson<BalanceFrameworkSettings>(filePath);
            }
            var defaultSettings = CreateDefault();
            JsonSerializer.WriteJson(filePath, defaultSettings);
            return defaultSettings;
        }
    }
}