# Entitäten

Im Balancing Framework werden Spielobjekte, die balancerelevante Parameter besitzen, als **Entitäten** bezeichnet.

Eine Entität dient als Container für Balancing-Parameter und stellt die Verbindung zwischen Spielobjekten und dem Balancing-System her.

Jede Entität besitzt eine eindeutige Identität innerhalb des Frameworks und kann mehrere Parameter enthalten, die später im externen Tool analysiert oder angepasst werden können.

## Unterstützte Objekttypen

Aktuell unterstützt das Framework zwei Arten von Unity-Objekten als Entitäten:

- **GameObjects / Prefabs**
- **ScriptableObjects**

Je nach Objekttyp erfolgt die Definition der Entität auf unterschiedliche Weise.

---

## GameObjects und Prefabs

Für GameObjects und Prefabs wird das Component **`EntityDescriptorComponent`** verwendet.

Dieses Component muss dem Root-Objekt eines GameObjects oder Prefabs hinzugefügt werden.

Der `EntityDescriptorComponent` definiert grundlegende Informationen über die Entität:

- **ID** _string_  
  Eine eindeutige Kennung für die Entität.

- **Display Name** _string_  
  Ein lesbarer Name, der im Balancing Tool angezeigt wird.

- **Category**  _string_
  Eine Kategorie zur Gruppierung von Entitäten.

Diese Informationen werden vom Framework verwendet, um Entitäten im externen Tool eindeutig zu identifizieren.

---

## ScriptableObjects

ScriptableObjects können ebenfalls als Entitäten im Balancing Framework verwendet werden.

Dafür muss das ScriptableObject das Interface `IBalanceableObject` implementieren.

Dieses Interface stellt sicher, dass das Objekt eine Beschreibung seiner Entität bereitstellt.

```csharp
public interface IBalanceableObject
{
    EntityDescriptor Descriptor { get; }
}
```

Das Interface verlangt eine Descriptor-Property, die ein EntityDescriptor-Objekt zurückgibt.

Der EntityDescriptor enthält grundlegende Informationen über die Entität:

- **ID**  
  Eine eindeutige Kennung für die Entität.

- **Display Name**  
  Ein lesbarer Name, der im Balancing Tool angezeigt wird.

- **Category**  
  Eine Kategorie zur Gruppierung von Entitäten.

Diese Informationen werden vom Framework verwendet, um Entitäten im Balancing Tool zu identifizieren und darzustellen.

### Beispiel

Das folgende Beispiel zeigt ein einfaches ScriptableObject, das als Entität im Balancing Framework verwendet werden kann.

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

In diesem Beispiel:

Das ScriptableObject implementiert `IBalanceableObject`

Die `Descriptor`-Property definiert die Metadaten der Entität

Die Felder `health`, `speed` und `range` sind als `BalanceParameter` markiert

!!! tip
    ScriptableObjects eignen sich besonders gut für Balancing-Daten,
    da sie unabhängig von Szenen gespeichert werden können und häufig
    für Konfigurationsdaten verwendet werden.

---

## Beziehung zwischen Entitäten und Parametern

Eine Entität kann mehrere **Balancing-Parameter** besitzen.

Diese Parameter werden über das Attribut `BalanceParameter` direkt im Code definiert.

Im nächsten Abschnitt wird erklärt, wie Parameter für das Balancing markiert werden können.