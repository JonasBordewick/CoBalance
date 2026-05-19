# Basic GameObject Example

```csharp
public class Player : MonoBehaviour
{
    [SerializeField, BalanceParameter("Player Health", "player_health")] private int health = 100;
    [SerializeField, BalanceParameter] private float movementSpeed = 5f;
    [SerializeField, BalanceParameter] private float jumpHeight = 2f;
    [SerializeField, BalanceParameter] private float attackDamage = 20f;
    [SerializeField, BalanceParameter] private float attackRange = 1.5f;
    [SerializeField, BalanceParameter] private float attackCooldown = 1f;
}
```

Im Beispiel sieht man die einfache Verwendung des Attributs `BalanceParameter` in einem `MonoBehaviour`.
Damit das GameObject, welches dieses `MonoBehaviour` verwendet, vom Plugin erkannt wird, muss zusätzlich das Component `EntityDescriptorComponent` hinzugefügt werden.

![EntityDescriptor hinzufügen](../assets/gifs/add_entity_descriptor_component.gif)

Das `EntityDescriptorComponent` markiert ein GameObject als **balancierbare Entität**.
Dabei spielt es keine Rolle, ob es sich um ein GameObject handelt, das direkt in einer Szene verwendet wird, oder um ein Prefab.

Sobald ein Objekt das `EntityDescriptorComponent` besitzt, kann das Balancing Framework alle mit `BalanceParameter` markierten Felder erkennen.

!!! tip
    In vielen Projekten werden Entitäten als Prefabs umgesetzt.  
    Dadurch können mehrere Instanzen derselben Entität im Spiel verwendet werden.
