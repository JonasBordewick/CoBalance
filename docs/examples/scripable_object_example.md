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
## Erklärung

- Das ScriptableObject implementiert `IBalanceableObject`
- Über die `Descriptor` Property werden die Entity Metadaten definiert
- Die Felder `health`, `speed`, `damage` sind als `BalanceParamater` markiert und werden vom Plugin automatisch erkannt  
