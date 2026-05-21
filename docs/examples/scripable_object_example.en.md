# Basic Scriptable Object Example

```csharp
[CreateAssetMenu(fileName = "Enemy Stats", menuName = "Blueprints/Enemy Stats")]
public class EnemyStats : ScriptableObject, IBalanceableObject
{
    private string enemyName;
    [Header("Enemy Stats")]
    [SerializeField, BalanceParameter] private int health;
    [SerializeField, BalanceParameter] private float speed;
    [SerializeField, BalanceParameter] private float damage;

    public EntityDescriptor Descriptor => new EntityDescriptor(
        $"enemy_{enemyName.ToLower()}", enemyName, "Enemy"
    );
}
```
## Explanation

- The ScriptableObject implements `IBalanceableObject`
- The entity metadata is defined via the `Descriptor` property
- The fields `health`, `speed`, `damage` are marked as `BalanceParameter` and are automatically recognized by the plugin
