using System;
using System.Collections.Generic;
using System.Reflection;
using BalancingFramework.Logger;
using UnityEngine;

namespace BalancingFramework
{
    [AttributeUsage(AttributeTargets.Field)]
    public class BalanceParameterAttribute : Attribute
    {
        public string Key { get; }
        
        public string DisplayName { get; private set; }

        
        public BalanceParameterAttribute(string displayName = null, string key = null)
        {
            DisplayName = displayName;
            Key = key;
        }
    }
    
    public enum ParameterValueType
    {
        Float,
        Int,
    }
    
    public sealed class ParameterDescriptor
    {
        public string Key { get; }
        public string DisplayName { get; }
        public string Owner { get; }
        
        public ParameterValueType ValueType { get; }
        
        public UnityEngine.Object ObjectInstance { get; }
        public FieldInfo FieldInfo { get; }
        
        public string GroupKey { get; } // for grouping parameters in the UI, e.g. molotov_ability.damage
        public BalanceParameterType ParameterType { get; }
        public int NestedLevel { get; } // -1 for base, otherwise 0...n-1
        
        private readonly Func<object> _getter;
        private readonly Action<object> _setter;
        
        
        public ParameterDescriptor(
            string id, string displayName, string owner,
            ParameterValueType valueType, UnityEngine.Object objectInstance,
            FieldInfo fieldInfo, string groupKey = "", BalanceParameterType parameterType = BalanceParameterType.Scalar,
            int nestedLevel = -1, Func<object> getter = null, Action<object> setter = null
        )
        {
            Key = id;
            DisplayName = displayName;
            Owner = owner;
            ValueType = valueType;
            ObjectInstance = objectInstance;
            FieldInfo = fieldInfo;
            GroupKey = groupKey;
            ParameterType = parameterType;
            NestedLevel = nestedLevel;
            _getter = getter ?? (() => FieldInfo.GetValue(ObjectInstance));
            _setter = setter ?? (v => FieldInfo.SetValue(ObjectInstance, v));
        }
        
        public object GetValue()
        {
            return _getter();
        }

        public bool TrySetValueFromObject(object value)
        {
            try
            {
                switch (ValueType)
                {
                    case ParameterValueType.Float:
                        _setter(Convert.ToSingle(value));
                        return true;
                    case ParameterValueType.Int:
                        _setter(Convert.ToInt32(value));
                        return true;
                    default:
                        BalancingFrameworkLogger.LogError($"Unsupported parameter value type: {ValueType}");
                        return false;
                }
            }
            catch (Exception exception)
            {
                BalancingFrameworkLogger.LogError($"Failed to set value for parameter '{Key}': {exception.Message}");
                return false;
            }
        }
    }
}
