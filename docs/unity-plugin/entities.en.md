# Entities

In the balancing framework, game objects that have balance-relevant parameters are referred to as **entities**.

An entity serves as a container for balancing parameters and establishes the connection between game objects and the balancing system.

Each entity has a unique identity within the framework and can contain multiple parameters that can later be analyzed or adjusted in the external tool.

## Supported Object Types

The framework currently supports two types of Unity objects as entities:

- **GameObjects / Prefabs**
- **ScriptableObjects**

The entity definition differs depending on the object type.

---

## GameObjects and Prefabs

For GameObjects and Prefabs, the **`EntityDescriptorComponent`** component is used.

This component must be added to the root object of a GameObject or Prefab.

The `EntityDescriptorComponent` defines basic information about the entity:

- **ID**  
  A unique identifier for the entity.

- **Display Name**  
  A human-readable name shown in the balancing tool.

- **Category**  
  A category for grouping entities.

This information is used by the framework to uniquely identify entities in the external tool.

---

## ScriptableObjects

ScriptableObjects can also be used as entities in the balancing framework.

To do so, the ScriptableObject must implement the `IBalanceableObject` interface.

This interface ensures that the object provides a description of its entity.

```csharp
public interface IBalanceableObject
{
    EntityDescriptor Descriptor { get; }
}
```

The interface requires a Descriptor property that returns an EntityDescriptor object.

The EntityDescriptor contains basic information about the entity:

- **ID**  
  A unique identifier for the entity.

- **Display Name**  
  A human-readable name shown in the balancing tool.

- **Category**  
  A category for grouping entities.

This information is used by the framework to identify and display entities in the balancing tool.

### Example

The following example shows a simple ScriptableObject that can be used as an entity in the balancing framework.

```csharp
public class EnemyStats : ScriptableObject, IBalanceableObject
{
    [SerializeField] private string entityID;
    [SerializeField] private string displayName;
    [SerializeField] private string category;

    [SerializeField, BalanceParameter] private int health;
    [SerializeField, BalanceParameter] private int speed;
    [SerializeField, BalanceParameter] private int range;

    public EntityDescriptor Descriptor => new EntityDescriptor(
        entityID,
        displayName,
        category
    );
}
```

In this example:

The ScriptableObject implements `IBalanceableObject`

The `Descriptor` property defines the entity's metadata

The fields `health`, `speed`, and `range` are marked as `BalanceParameter`

!!! tip
    ScriptableObjects are particularly well-suited for balancing data,
    as they can be saved independently of scenes and are commonly
    used for configuration data.

---

## Relationship Between Entities and Parameters

An entity can have multiple **balancing parameters**.

These parameters are defined directly in code using the `BalanceParameter` attribute.

The next section explains how parameters can be marked for balancing.
