# Advanced Parameter Example

!!! note
    Advanced parameters are an optional feature of the balancing framework.
    For most use cases, simple parameters of type `int` or `float` are sufficient.

In addition to simple `int` or `float` parameters, the balancing framework also supports more complex parameter structures.
For this, a data type can implement the `IBalanceParameter` interface. This allows custom parameter logic to be integrated into the balancing system.

Typical use cases include:

- Values with multiple upgrade tiers
- Parameters with internal logic
- Parameter groups

## `IBalanceParameter` Interface
The `IBalanceParameter` interface defines how a parameter can be read and modified by the balancing framework.

```csharp
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
```
This interface allows the framework to process both simple parameters and complex structures with multiple values.

## Example: Upgradeable Parameter
A typical use case for an advanced parameter is **upgradeable values**, as commonly found in games.
Such a parameter has:

- a base value
- multiple upgrade tiers

### Implementation

```csharp
// Interface for upgradeable values
public interface IUpgradeableValue
{
    int UpgradeCount { get; }

    void Register(AbilityManager abilityManager);
    void RegisterInUse();
    void Upgrade();
    string GetUpgradeDescription();
}

// Abstract generic class 
public abstract class UpgradeableValue<T> : IUpgradeableValue, IBalanceParameter
{
    [SerializeField] protected T value;
    [SerializeField] protected T[] upgrades;
    protected AbilityManager abilityManager;
    protected int level = 0;

    protected virtual string UpgradeName { get; set; }
    public virtual T Value { get => value; set => this.value = value; }
    public int UpgradeCount { get => upgrades.Length; }
    public UnityEvent OnChanged { get; } = new UnityEvent();

    public void Register(AbilityManager abilityManager) { this.abilityManager = abilityManager; }
    public abstract void RegisterInUse();
    public virtual void Upgrade()
    {
        if (level < upgrades.Length)
            Upgrade(upgrades[level++]); 
    }
    public abstract void Upgrade(T upgrade);
    public abstract string GetUpgradeDescription();

    // IBalanceParameter implementations
    public BalanceParameterType ParameterType => BalanceParameterType.Nested;
    public abstract BalanceValueType ValueType { get; }

    public object GetBaseValue()
    {
        return value;
    }

    public bool SetBaseValue(object value)
    {
        try
        {
            this.value = (T)Convert.ChangeType(value, typeof(T));
            return true;
        }
        catch
        {
            return false;
        }
    }

    public int GetNestedValueCount()
    {
        return upgrades.Length;
    }

    public object GetNestedValue(int index)
    {
        return index < upgrades.Length ? upgrades[index] : null;
    }

    public bool SetNestedValue(int index, object value)
    {
        if (index >= upgrades.Length) return false;
        try
        {
            upgrades[index] = (T)Convert.ChangeType(value, typeof(T));
            return true;
        }
        catch
        {
            return false;
        }
    }

    public string DisplayNameOfNestedValues => "Upgrade";
    public string KeyOfNestedValues => "upgrade";
}

public abstract class UpgradeableFloat : UpgradeableValue<float>
{
    public override void Upgrade(float upgrade)
    {
        value *= (1+upgrade);
        OnChanged.Invoke();
    }

    public override string GetUpgradeDescription()
    {
        if (level >= upgrades.Length || upgrades[level] == 0) return "";
        return DescriptionUtils.GetUpgradeDescription(UpgradeName, upgrades[level]);
    }


    public override BalanceValueType ValueType => BalanceValueType.Float;
}
```

#### Usage in Game Code

Such a parameter can then be used normally with `BalanceParameter`.
Example:

```csharp
[SerializeField, BalanceParameter]
private UpgradeableFloat attackDamage;
```

The balancing framework automatically recognizes:

- the base value
- all upgrade tiers
- These can then be analyzed or adjusted in the balancing tool.
