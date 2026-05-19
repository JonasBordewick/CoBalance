using System;
using System.IO;
using CoBalance.DTO;
using CoBalance.Logger;
using UnityEditor;
using UnityEngine;

namespace CoBalance.Editor
{
    public static class MenuBuilder
    {
        
        private static readonly string BalanceFilePath;
        private static BalanceFrameworkSettings _settings;
        
        
        static MenuBuilder()
        {
            _settings = BalanceFrameworkSettings.Load();
            BalanceFilePath = Utilities.GetBalanceFilePath(_settings.defaultBalanceFile);
        }
        
        [MenuItem("CoBalance/Open Workspace Folder")]
        public static void RevealEntitiesJson()
        {
            var path = Utilities.GetFrameworkFolderPath();
            EditorUtility.RevealInFinder(path);
        }
        
        [MenuItem("CoBalance/Reload")]
        public static void BuildBalancingConfiguration()
        {
            if (BalanceFilePath == null)
            {
                CoBalanceLogger.LogError("Failed to determine balance file path.");
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
                CoBalanceLogger.LogError($"Failed to export balancing configuration: {ex.Message}");
            }
        }
        
        [MenuItem("CoBalance/Bake Balancing Configuration")]
        public static void Bake()
        {
            if (BalanceFilePath == null || !File.Exists(BalanceFilePath))
            {
                CoBalanceLogger.LogError(
                    $"Balance file not found at: {BalanceFilePath}. Bake aborted.");
                return;
            }
 
            try
            {
                // 1. Rebuild the registry so we have fresh ObjectInstance references
                var registry = BalancingAttributeRegistry.Instance;
                registry.ClearRegistry();
                registry.RegisterAllEntities();
 
                // 2. Read the balance file
                var dto = JsonSerializer.ReadJson<BalanceDTO>(BalanceFilePath);
                if (dto == null || dto.values == null)
                {
                    CoBalanceLogger.LogError("Balance file is empty or invalid. Bake aborted.");
                    return;
                }
 
                var appliedCount = 0;
                var skippedCount = 0;
 
                // 3. Apply every value and mark the owning UnityEngine.Object dirty
                foreach (var valueDto in dto.values)
                {
                    if (valueDto == null || string.IsNullOrWhiteSpace(valueDto.id))
                        continue;
 
                    if (!registry.ByKeyList.TryGetValue(valueDto.id, out var descriptors) || descriptors == null)
                    {
                        skippedCount++;
                        continue;
                    }
 
                    foreach (var descriptor in descriptors)
                    {
                        bool ok = descriptor.ValueType switch
                        {
                            ParameterValueType.Float =>
                                descriptor.TrySetValueFromObject(valueDto.value),
                            ParameterValueType.Int =>
                                descriptor.TrySetValueFromObject(Convert.ToInt32(valueDto.value)),
                            _ => false
                        };
 
                        if (ok)
                        {
                            // Mark the asset dirty so Unity knows it needs to be saved
                            if (descriptor.ObjectInstance != null)
                                EditorUtility.SetDirty(descriptor.ObjectInstance);
 
                            appliedCount++;
                        }
                        else
                        {
                            skippedCount++;
                        }
                    }
                }
 
                // 4. Persist all dirty assets to disk
                AssetDatabase.SaveAssets();
                AssetDatabase.Refresh();
 
                CoBalanceLogger.LogInfo(
                    $"Bake completed. Applied: {appliedCount}, Skipped: {skippedCount}.");
 
                Debug.Log(
                    $"[CoBalance] Bake completed – {appliedCount} value(s) written to assets, " +
                    $"{skippedCount} skipped.");
            }
            catch (Exception ex)
            {
                CoBalanceLogger.LogError($"Bake failed: {ex.Message}\n{ex.StackTrace}");
            }
        }

    }
    
}