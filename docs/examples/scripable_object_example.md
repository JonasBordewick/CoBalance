# Basic Scriptable Object Example

```csharp
[CreateAssetMenu(fileName = "Enemy Stats", menuName = "Blueprints/Enemy Stats")]
public class Enemy Stats : ScriptableObject, IBalanceableObject
{
    [Header("Entity Descriptor Data")]
    [SerializeField] private string entityID;
    [SerializeField] private string displayName;
    [SerializeField] private string category;

    [Header("Enemy Stats")]
    [SerializeField, BalanceParameter] private int health;
    [SerializeField, BalanceParameter] private float speed;
    [SerializeField, BalanceParameter] private float damage;

    public EntityDescriptor Descriptor => new EntityDescriptor(
        entityID, displayName, category
    );
}
```
## Erklärung

- Das ScriptableObject implementiert `IBalanceableObject`
- Über die `Descriptor` Property werden die Entity Metadaten definiert
- Die Felder `health`, `speed`, `damage` sind als `BalanceParamater` markiert und werden vom Plugin automatisch erkannt  
