# Balance Parameters

Balancing-Parameter sind Werte im Spiel, die vom **Balancing Framework** erkannt und im externen Tool analysiert oder angepasst werden können.

Damit ein Wert als Balancing-Parameter behandelt wird, muss das Feld mit dem Attribut `BalanceParameter` markiert werden.

## Überblick

Es gibt zwei Arten von Balancing-Parametern:

- **Einfache Parameter**  
  Werte vom Typ `int` oder `float`.
- **Erweiterte Parameter**  
  Eigene Datentypen, die das Interface `IBalanceParameter` implementieren.


## Beispiel

```csharp
[SerializeField, BalanceParameter]
private int health;

[SerializeField, BalanceParameter]
private float speed;
```

Alle Felder, die mit `BalanceParameter` markiert sind, werden vom Framework automatisch erkannt.

## Unterstützte Datentypen

Aktuell unterstützt das Framework folgende Datentypen:

- int
- float

Andere Datentypen werden nicht automatisch erkannt.

!!! note
    Wenn ein nicht unterstützter Typ verwendet wird, gibt das Framework eine Warnung im Unity-Console-Log aus.

## Verwendung in Entitäten

Balancing-Parameter müssen sich in einem Objekt befinden, das als balancierbare Entität definiert ist.

Beispiel:
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
In diesem Beispiel werden die Parameter health und speed vom Framework erkannt.

## Optionale Attributeinstellungen

Das Attribut `BalanceParameter` kann optional mit zusätzlichen Informationen versehen werden.

Zum Beispiel kann ein eigener Anzeigename definiert werden:

```csharp
[BalanceParameter(displayName: "Enemy Health")]
private int health;
```

Dadurch wird im Balancing Tool nicht der Feldname `Health`, sondern der Anzeigename `Enemy Health` verwendet.

Optional kann außerdem ein eigener Schlüssel `(Key)` angegeben werden:
```csharp
[BalanceParameter(key: "enemy_health", displayName: "Enemy Health")]
private int health;
```
Das ist vor allem dann nützlich, wenn Parameter unabhängig vom tatsächlichen Feldnamen eindeutig benannt werden sollen.

## Anzeige im Balancing Tool

Jeder erkannte Parameter wird im externen Tool als eigener Balancing-Wert angezeigt.

Die Parameter werden dabei automatisch der jeweiligen Entität zugeordnet.


## Erweiterte Parametertypen

Neben einfachen Parametern vom Typ `int` und `float` unterstützt das Balancing Framework auch komplexere Parametertypen.

Hierfür kann ein Datentyp das Interface `IBalanceParameter` implementieren.

Dieses Interface erlaubt es, eigene Parameterstrukturen in das Balancing-System zu integrieren.

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

Solche Parameter können beispielsweise verwendet werden, um Werte mit mehreren Stufen oder Upgrades abzubilden.

### Beispiel

Ein typischer Anwendungsfall sind Werte mit Upgrade-Stufen, bei denen ein Basiswert und mehrere Upgrade-Level existieren.
```csharp
[SerializeField, BalanceParameter]
private UpgradeableFloat damage;
```

Das Balancing Framework erkennt automatisch:

- den Basiswert
- alle Upgrade-Werte