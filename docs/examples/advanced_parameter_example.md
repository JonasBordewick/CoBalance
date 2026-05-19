# Advanced Parameter Example

!!! note
    Erweiterte Parameter sind ein optionales Feature des Balancing Frameworks.
    Für die meisten Anwendungsfälle reichen einfache Parameter vom Typ `int` oder `float`.

Neben einfachen Parametern von Typ `int` oder `float` unterstützt das Balancing Framework auch komplexere Parameterstrukturen.
Dafür kann ein Datentyp das Interface `IBalanceParameter` implementieren. Dies erlaubt es, eigene Parameterlogik in das Balancing-System zu integrieren.

Typische Anwendungsfälle sind zum Beispiel:

- Werte mit mehreren Upgrade-Stufen
- Parameter mit interner Logik
- Parametergruppen

## `IBalanceParameter` Interface
Das Interface `IBalanceParameter` definiert, wie ein Parameter vom Balancing Framework gelesen und verändert werden kann.

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
Dieses Interface erlaubt es dem Framework sowohl einfache Parameter als auch komplexe Strukturen mit mehreren werten zu verarbeiten.

## Beispiel: Upgradebarer Parameter
Ein typischer Anwendungsfall für eiinen erweiterten Parameter sind **upgradebare Werte**, wie sie häufig in Spielen vorkommen.
Ein Parameter besitzt dabei:

- einen Basiswert
- mehrere Upgrade-Stufen

### Implementierung

```csharp
// Interface für upgradable Values
public interface IUpgradeableValue
{
    int UpgradeCount { get; }

    void Register(AbilityManager abilityManager);
    void RegisterInUse();
    void Upgrade();
    string GetUpgradeDescription();
}

// Abstrakte generische Klasse 
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

    // IBalanceParameter Implementationen
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

#### Verwendung im Spielcode

Ein solcher Parameter kann anschließend ganz normal mit `BalanceParameter` verwendet werden.
Beispiel:

```csharp
[SerializeField, BalanceParameter]
private UpgradeableFloat attackDamage;
```

Das Balancing Framework erkennt automatisch:

- den Basiswert
- alle Upgrade-Stufen
- Diese können anschließend im Balancing Tool analysiert oder angepasst werden.