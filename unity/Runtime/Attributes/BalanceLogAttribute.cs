using System;

namespace BalancingFramework
{
    [AttributeUsage(AttributeTargets.Field, Inherited = true, AllowMultiple = false)]
    public class BalanceLogAttribute : Attribute
    {
        public string Key { get; }
        
        public BalanceLogAttribute(string key = null)
        {
            Key = key;
        }
    }
    
    public sealed class LogDescriptor
    {
        public string Key { get; }
        public Func<object> Getter { get; }
        
        public LogDescriptor(string key, Func<object> getter)
        {
            Key = key;
            Getter = getter;
        }
    }
}