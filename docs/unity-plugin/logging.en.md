# Logging

The `BalanceLog` attribute marks values that should be captured during runtime and later analyzed in the external balancing tool.

Logging is especially useful when you want to not only adjust balance parameters but also analyze actual gameplay data.

## Using BalanceLog

To log a value, add the `BalanceLog` attribute to a field.

```csharp
[SerializeField, BalanceLog]
private int currentHealth;
```

The framework automatically recognizes this field and includes it in runtime logging.
A custom key can optionally be specified:

```csharp
[SerializeField, BalanceLog("player_health")]
private int currentHealth;
```

If no custom key is provided, the framework uses the field name by default.

## Automatic Detection on Scene Start

When a scene starts, the framework scans all existing MonoBehaviour instances for fields marked with `BalanceLog`.

This means:

- Objects that already exist at scene start are automatically detected
- their logged fields are automatically registered

In many simple cases, no further configuration is needed.

## Dynamically Created Objects

If GameObjects or components are created during runtime, their log fields cannot be automatically detected during the initial scene scan.

For such cases, the `BalanceLogSource` component must be added to the corresponding object.

```csharp
public sealed class BalanceLogSource : MonoBehaviour
```

This component ensures that the object is registered with the logger as soon as it is activated.

### When `BalanceLogSource` Is Needed

`BalanceLogSource` is needed when:

- an object is instantiated at runtime
- an object with `BalanceLog` is not present at scene start

`BalanceLogSource` is generally not needed if the object already exists in the scene from the beginning.

### Example

```csharp
public class Enemy : MonoBehaviour
{
    [SerializeField, BalanceLog]
    private int currentHealth;
}
```

If this object already exists at scene start, `currentHealth` is automatically detected.

If the object is created at runtime instead, the GameObject should additionally use `BalanceLogSource` as a component.

---

## Manual Logging via GameStatLogger

In addition to automatic attribute-based logging, the `GameStatLogger` provides three public methods to write values to the log explicitly.

The logger is implemented as a singleton and is accessible via `GameStatLogger.Instance`.

---

### `LogGameStats()`

Writes a snapshot of **all** registered `[BalanceLog]` fields to the log at once — using the current `Time.fixedTime` as a timestamp.

Useful when time-based logging is disabled and the snapshot should instead be triggered at a specific game event (e.g., at the end of a round).

```csharp
// Log all registered values once at the end of a fight
GameStatLogger.Instance.LogGameStats();
```

---

### `LogGameStat(string key, object value)`

Writes a single value with the specified key to the log. `Time.fixedTime` is used automatically as the timestamp.

```csharp
// Manually log current score
GameStatLogger.Instance.LogGameStat("score", currentScore);

// Any numeric values are allowed
GameStatLogger.Instance.LogGameStat("enemies_defeated", enemyCount);
```

---

### `LogGameStat(float t, string key, object value)`

Like the method above, but with a **manually specified timestamp** `t`. Useful when the exact time of the event is known and should be recorded precisely.

```csharp
// Log hit time with a custom timestamp
float hitTime = Time.fixedTime;
GameStatLogger.Instance.LogGameStat(hitTime, "hit_damage", damage);
```

---

## Notes

- `BalanceLog` can be used on fields that should be observed at runtime
- `BalanceLogSource` is required for dynamically created objects
- Duplicate log keys on the same object should be avoided
- `LogGameStat` and `LogGameStats` write regardless of whether time-based logging is enabled
