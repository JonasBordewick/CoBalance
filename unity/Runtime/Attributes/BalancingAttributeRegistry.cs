using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using BalancingFramework.Logger;
using UnityEngine;

namespace BalancingFramework
{
    public class BalancingAttributeRegistry
    {
        
        public static BalancingAttributeRegistry Instance { get; } = new BalancingAttributeRegistry();
        private BalancingAttributeRegistry()
        {
        }
        
        private readonly Dictionary<string, List<ParameterDescriptor>> _byKey = new();
        private readonly Dictionary<string, EntityDescriptor> _allEntities = new();
        
        public IReadOnlyList<EntityDescriptor> AllEntities => _allEntities.Values.ToList();
        
        public IReadOnlyDictionary<string, ParameterDescriptor> ByKeySingle => _byKey.ToDictionary(kv => kv.Key, kv => kv.Value.First());
        public IReadOnlyDictionary<string, List<ParameterDescriptor>> ByKeyList => _byKey;
        
        public void ClearRegistry()
        {
            _byKey.Clear();
            _allEntities.Clear();
        }

        private void BuildFromActiveScene(bool includeInactive = true)
        {
            var gameObjects = UnityEngine.Object.FindObjectsByType(
                type: typeof(GameObject),
                includeInactive ? FindObjectsInactive.Include : FindObjectsInactive.Exclude,
                FindObjectsSortMode.None
            ).Cast<GameObject>();
            
            
            foreach (var gameObject in gameObjects)
            {
                var entityComponent = gameObject.GetComponent<IBalanceableObject>();
                if (entityComponent == null)
                    continue;
                var entityDescriptor = entityComponent.Descriptor;
                
                if (string.IsNullOrWhiteSpace(entityDescriptor.ID))
                {
                    BalancingFrameworkLogger.LogWarning($"GameObject '{gameObject.name}' has an entity descriptor with null ID. Skipping.");
                    continue;
                }

                if (!_allEntities.TryAdd(entityDescriptor.ID, entityDescriptor))
                {
                    // BalancingFrameworkLogger.LogInfo("Entity with ID '" + entityDescriptor.ID + "' is already registered. Skipping prefab: " + gameObject.name);
                    // continue;
                }

                foreach (var mb in gameObject.GetComponents<MonoBehaviour>())
                {
                    if (mb is EntityDescriptorComponent)
                        continue;
                    CollectParametersFromObject(mb, entityDescriptor.ID);
                }
            }
        }

        public void RegisterAllEntities()
        {
#if UNITY_EDITOR
            var balancingPrefabs = GetAllBalancingPrefabs();
            foreach (var prefab in balancingPrefabs)
            {
                var entityComponent = prefab.GetComponent<IBalanceableObject>();
                var entityDescriptor = entityComponent.Descriptor;

                if (string.IsNullOrWhiteSpace(entityDescriptor.ID))
                {
                    BalancingFrameworkLogger.LogWarning($"Prefab '{prefab.name}' has an entity descriptor with null ID. Skipping.");
                    continue;
                }

                if (!_allEntities.TryAdd(entityDescriptor.ID, entityDescriptor))
                {
                    continue;
                }

                foreach (var mb in prefab.GetComponents<MonoBehaviour>())
                {
                    CollectParametersFromObject(mb, entityDescriptor.ID);
                }
            }

            var scriptableObjects = GetAllBalancingScriptableObjects();
            foreach (var scriptableObject in scriptableObjects)
            {
                var entityDescriptor = (scriptableObject as IBalanceableObject).Descriptor;
                if (string.IsNullOrWhiteSpace(entityDescriptor.ID))
                {
                    BalancingFrameworkLogger.LogWarning($"Scriptable Object '{scriptableObject.name}' has an entity descriptor with null ID. Skipping.");
                    continue;
                }
                if (!_allEntities.TryAdd(entityDescriptor.ID, entityDescriptor))
                {
                    continue;
                }

                CollectParametersFromObject(scriptableObject, entityDescriptor.ID);
            }
#endif
            BuildFromActiveScene();
        }

#if UNITY_EDITOR
        public List<GameObject> GetAllBalancingPrefabs()
        {
            List<GameObject> prefabs = new List<GameObject>();
            foreach (var guid in UnityEditor.AssetDatabase.FindAssets("t:Prefab"))
            {
                var prefabRoot = UnityEditor.AssetDatabase.LoadAssetAtPath<GameObject>(UnityEditor.AssetDatabase.GUIDToAssetPath(guid));
                if (prefabRoot == null) continue;

                var entityComponent = prefabRoot.GetComponent<IBalanceableObject>();
                if (entityComponent != null)
                {
                    prefabs.Add(prefabRoot);
                }
            }

            return prefabs;
        }

        public List<ScriptableObject> GetAllBalancingScriptableObjects()
        {
            var result = new List<ScriptableObject>();

            foreach (var guid in UnityEditor.AssetDatabase.FindAssets("t:ScriptableObject"))
            {
                var path = UnityEditor.AssetDatabase.GUIDToAssetPath(guid);

                var so = UnityEditor.AssetDatabase.LoadAssetAtPath<ScriptableObject>(path);
                if (so == null) continue;

                if (so is IBalanceableObject)
                    result.Add(so);
            }

            return result;
        }
#endif
        
        private void CollectParametersFromObject(UnityEngine.Object obj, string ownerName)
        {
            var type = obj.GetType();
            var flags = BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic;

            foreach (var field in type.GetFields(flags))
            {
                var parameterAttribute = field.GetCustomAttribute<BalanceParameterAttribute>(inherit: true);
                if (parameterAttribute == null)
                    continue;
                
                var keyPart = !string.IsNullOrWhiteSpace(parameterAttribute.Key) ? parameterAttribute.Key : field.Name;
                var baseKey = $"{NormalizeIdPart(ownerName)}.{NormalizeIdPart(keyPart)}";
                
                var displayName = !string.IsNullOrWhiteSpace(parameterAttribute.DisplayName)
                    ? parameterAttribute.DisplayName
                    : Utilities.Nicify(field.Name);
                
                object fieldValue = null;
                try { fieldValue = field.GetValue(obj); }
                catch { /* ignore, will warn below */ }
                
                if (TryGetValueType(field.FieldType, out var valueType))
                {
                    var baseId = $"{baseKey}.base";
                    
                    var descriptor = new ParameterDescriptor(
                        id: baseId,
                        displayName: displayName,
                        owner: ownerName,
                        valueType: valueType,
                        objectInstance: obj,
                        fieldInfo: field,
                        groupKey: baseKey,
                        parameterType: BalanceParameterType.Scalar,
                        nestedLevel: -1
                    );
                    
                    AddDescriptor(descriptor);
                    continue;
                }

                if (fieldValue is IBalanceParameter balanceParameter)
                {
                    
                    var vt = ConvertValueType(balanceParameter.ValueType);
                    
                    // base leaf
                    {
                        var baseId = $"{baseKey}.base";
                        var finalId = EnsureUniqueId(baseId, type, field);

                        var descriptor = new ParameterDescriptor(
                            id: finalId,
                            displayName: displayName,
                            owner: ownerName,
                            valueType: vt,
                            objectInstance: obj,
                            fieldInfo: field,
                            groupKey: baseKey,
                            parameterType: balanceParameter.ParameterType,
                            nestedLevel: -1,
                            getter: () => balanceParameter.GetBaseValue(),
                            setter: v => balanceParameter.SetBaseValue(v)
                        );
                        AddDescriptor(descriptor);
                    }

                    if (balanceParameter.ParameterType == BalanceParameterType.Nested)
                    {
                        var n = balanceParameter.GetNestedValueCount();
                        for (int i = 0; i < n; i++)
                        {
                            var stepID = $"{baseKey}.{balanceParameter.KeyOfNestedValues}{i + 1}";
                            var finalId = EnsureUniqueId(stepID, type, field);

                            var idx = i;

                            var d = new ParameterDescriptor(
                                id: finalId,
                                displayName: $"{displayName} - {balanceParameter.DisplayNameOfNestedValues} {idx + 1}",
                                owner: ownerName,
                                valueType: vt,
                                objectInstance: obj,
                                fieldInfo: field,
                                groupKey: baseKey,
                                parameterType: BalanceParameterType.Nested,
                                nestedLevel: idx,
                                getter: () => balanceParameter.GetNestedValue(idx),
                                setter: v => balanceParameter.SetNestedValue(idx, v)
                            );
                            
                            AddDescriptor(d);
                        }
                    }
                    continue; 
                }
                BalancingFrameworkLogger.LogWarning($"Unsupported parameter type '{field.FieldType}' in field '{field.Name}' of component '{type.Name}'. Supported types are float and int.");
            }
            
        }

        private void AddDescriptor(ParameterDescriptor descriptor)
        {
            if(!_byKey.TryGetValue(descriptor.Key, out var list))
            {
                list = new List<ParameterDescriptor>();
                _byKey[descriptor.Key] = list;
            }
            list.Add(descriptor);
        }
        
        private string EnsureUniqueId(string baseId, Type componentType, FieldInfo field)
        {
            if (!_byKey.ContainsKey(baseId))
                return baseId;

            int dotIdx = baseId.IndexOf('.');
            string withComponent = dotIdx >= 0
                ? baseId.Insert(dotIdx + 1, $"{NormalizeIdPart(componentType.Name)}.")
                : $"{baseId}.{NormalizeIdPart(componentType.Name)}";

            if (!_byKey.ContainsKey(withComponent))
                return withComponent;


            var i = 2;
            while (true)
            {
                var candidate = $"{withComponent}#{i}";
                if (!_byKey.ContainsKey(candidate))
                    return candidate;
                i++;
            }
        }

        private static ParameterValueType ConvertValueType(BalanceValueType balanceValueType)
        {
            if (balanceValueType == BalanceValueType.Float)
                return ParameterValueType.Float;
            if (balanceValueType == BalanceValueType.Int)
                return ParameterValueType.Int;
            throw new ArgumentException($"Unsupported BalanceValueType: {balanceValueType}");
        }
        
        private static bool TryGetValueType(Type t, out ParameterValueType valueType)
        {
            if (t == typeof(float))
            {
                valueType = ParameterValueType.Float;
                return true;
            }
            if (t == typeof(int))
            {
                valueType = ParameterValueType.Int;
                return true;
            }
            
            valueType = default;
            return false;
        }
        
        private static string NormalizeIdPart(string s)
        {
            if (string.IsNullOrWhiteSpace(s))
                return "unknown";
            
            s = s.Trim().Replace(" ", "_");
            
            return s;
        }
    }
}