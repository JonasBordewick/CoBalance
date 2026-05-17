#if UNITY_EDITOR
using System.IO;
using UnityEditor;
using UnityEditor.Compilation;
using UnityEngine;
using BalancingFramework;
using BalancingFramework.DTO;
using BalancingFramework.Logger;

namespace BalancingFramework.Editor
{
    [InitializeOnLoad]
    public static class AutoExporter
    {
        private static readonly string BalanceFilePath;
        private static BalanceFrameworkSettings _settings;

        private static bool _pending;
        private static double _nextExportTime;
        
        static AutoExporter()
        {
            _settings = BalanceFrameworkSettings.Load();
            BalanceFilePath = Utilities.GetBalanceFilePath(_settings.defaultBalanceFile);
            
            
            AssemblyReloadEvents.afterAssemblyReload += () =>
            {
                EditorApplication.delayCall += Reload;
            };
            
            EditorApplication.hierarchyChanged += OnHierarchyChanged;
            EditorApplication.update += () =>
            {
                if (!_pending) return;
                if (EditorApplication.timeSinceStartup < _nextExportTime) return;
                _pending = false;
                BalancingFrameworkLogger.LogInfo("Hierarchy changed. Scheduled balance export performing now...");
                Reload();
            };
        }

        private static void Reload()
        {
            if (Utilities.GetBalanceFilePath(BalanceFilePath) == null)
            {
                BalancingFrameworkLogger.LogError($"Failed to determine balance file path.");
                return;
            }
            
            try
            {
                var registry = BalancingAttributeRegistry.Instance;
                registry.ClearRegistry();
                registry.RegisterAllEntities();
                
                BalanceRepository.ExportBalanceToFile(BalanceFilePath, registry);
            }
            catch (System.Exception ex)
            {
                BalancingFrameworkLogger.LogError($"Failed to export balancing configuration: {ex.Message}");
            }
        }

        private static void OnHierarchyChanged()
        {
            // When in play mode, we don't want to trigger exports on hierarchy changes
            if (Application.isPlaying)
                return;
            _pending = true;
            _nextExportTime = EditorApplication.timeSinceStartup + 5.0; // Delay export by 5 seconds to batch changes
            BalancingFrameworkLogger.LogInfo("Hierarchy changed. Scheduling balance export...");
        }
    }
}
#endif