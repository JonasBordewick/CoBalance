# Balance Parameters

Balance parameters are values in the game that can be recognized by the **balancing framework** and analyzed or adjusted in the external tool.

For a value to be treated as a balance parameter, the field must be marked with the `BalanceParameter` attribute.

## Overview

There are two types of balance parameters:

- **Simple Parameters**  
  Values of type `int` or `float`.
- **Advanced Parameters**  
  Custom data types that implement the `IBalanceParameter` interface.


## Example

```csharp
[SerializeField, BalanceParameter]
private int health;

[SerializeField, BalanceParameter]
private float speed;
```

All fields marked with `BalanceParameter` are automatically recognized by the framework.

## Supported Data Types

The framework currently supports the following data types:

- int
- float

Other data types are not automatically recognized.

!!! note
    If an unsupported type is used, the framework outputs a warning in the Unity Console log.

## Usage in Entities

Balance parameters must be inside an object defined as a balanceable entity.

Example:
```csharp
public class EnemyStats : ScriptableObject, IBalanceableObject
{
    [SerializeField] private string entityID;
    [SerializeField] private string displayName;
    [SerializeField] private string category;
    [SerializeField] private string description;

    [BalanceParameter]
    private int health;

    [BalanceParameter]
    private float speed;

    public EntityDescriptor Descriptor => new EntityDescriptor(
        entityID,
        displayName,
        category,
        description
    );
}
```
In this example, the parameters `health` and `speed` are recognized by the framework.

## Optional Attribute Settings

The `BalanceParameter` attribute can optionally be provided with additional information.

For example, a custom display name can be defined:

```csharp
[BalanceParameter(DisplayName = "Enemy Health")]
private int health;
```

This means the balancing tool will show `Enemy Health` instead of the field name `Health`.

Optionally, a custom key `(Key)` can also be specified:
```csharp
[BalanceParameter(Key = "enemy_health", DisplayName = "Enemy Health")]
private int health;
```
This is particularly useful when parameters should be uniquely named independently of the actual field name.

## Display in the Balancing Tool

Each recognized parameter is displayed as its own balancing value in the external tool.

Parameters are automatically assigned to their respective entity.


## Advanced Parameter Types

In addition to simple `int` and `float` parameters, the balancing framework also supports more complex parameter types.

For this, a data type can implement the `IBalanceParameter` interface.

This interface allows custom parameter structures to be integrated into the balancing system.

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
}
```

Such parameters can be used, for example, to represent values with multiple tiers or upgrades.

### Example

A typical use case is values with upgrade tiers, where a base value and multiple upgrade levels exist.
```csharp
[SerializeField, BalanceParameter]
private UpgradeableFloat damage;
```

The balancing framework automatically recognizes:

- the base value
- all upgrade values
