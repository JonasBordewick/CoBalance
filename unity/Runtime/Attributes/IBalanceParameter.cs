namespace BalancingFramework
{
    public enum BalanceValueType
    {
        Float,
        Int
    }
    
    public enum BalanceParameterType
    {
        Scalar,
        Nested
    }
    
    
    public interface IBalanceParameter
    {
        BalanceParameterType ParameterType { get; }
        BalanceValueType ValueType { get; }
        
        object GetBaseValue();
        bool SetBaseValue(object value);
        
        int GetNestedValueCount();
        object GetNestedValue(int index);
        bool SetNestedValue(int index, object value);

        public string DisplayNameOfNestedValues { get; }
        public string KeyOfNestedValues { get; }
    }

    public interface ITestInterface
    {
        
    }
}