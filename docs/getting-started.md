# Erste Schritte

Dieser Guide führt dich durch die Einrichtung deines Unity-Projekts für CoBalance — von der ersten Entität bis zur lauffähigen Simulation.

> **Voraussetzungen:** Unity-Plugin und Desktop App sind bereits installiert.  
> Falls nicht, folge zuerst den Schritten unter [Installation](index.md#installation).

---

## Schritt 1: Entität definieren

CoBalance arbeitet mit **Entitäten** — Spielobjekten, die balancerelevante Parameter besitzen. Je nach Objekttyp unterscheidet sich die Definition.

### ScriptableObject

Das ScriptableObject implementiert `IBalanceableObject` und stellt über die `Descriptor`-Property seine Metadaten bereit:

```csharp
using UnityEngine;
using CoBalance;

[CreateAssetMenu(menuName = "Game/Enemy Stats")]
public class EnemyStats : ScriptableObject, IBalanceableObject
{
    [SerializeField] private string entityID;
    [SerializeField] private string displayName;
    [SerializeField] private string category;

    public EntityDescriptor Descriptor => new EntityDescriptor(entityID, displayName, category);
}
```

### GameObject / Prefab

Für GameObjects wird stattdessen die Komponente `EntityDescriptorComponent` dem Root-Objekt hinzugefügt. Sie enthält dieselben Metadaten (ID, Display Name, Category) und erfordert keine Code-Änderungen.

Mehr dazu unter [Entitäten](unity-plugin/entities.md).

---

## Schritt 2: Balance-Parameter markieren

Felder, die CoBalance erkennen und optimieren soll, werden mit `[BalanceParameter]` annotiert. Unterstützte Typen sind `int` und `float`.

```csharp
[SerializeField, BalanceParameter]
private int health;

[SerializeField, BalanceParameter]
private float speed;
```

Optional kann ein eigener Anzeigename vergeben werden:

```csharp
[SerializeField, BalanceParameter(DisplayName = "Move Speed")]
private float speed;
```

Vollständiges Beispiel mit Entität und Parametern:

```csharp
using UnityEngine;
using CoBalance;

[CreateAssetMenu(menuName = "Game/Enemy Stats")]
public class EnemyStats : ScriptableObject, IBalanceableObject
{
    [SerializeField] private string entityID;
    [SerializeField] private string displayName;
    [SerializeField] private string category;

    [SerializeField, BalanceParameter(DisplayName = "Health")]
    private int health;

    [SerializeField, BalanceParameter(DisplayName = "Move Speed")]
    private float speed;

    [SerializeField, BalanceParameter(DisplayName = "Damage")]
    private float damage;

    public EntityDescriptor Descriptor => new EntityDescriptor(entityID, displayName, category);
}
```

Mehr dazu unter [Parameter](unity-plugin/parameters.md).

---

## Schritt 3: Laufzeitdaten loggen (optional)

Mit `[BalanceLog]` können Felder für das Laufzeit-Logging markiert werden. Diese Werte werden während der Simulation automatisch aufgezeichnet und sind später in der Desktop App auswertbar.

```csharp
using UnityEngine;
using CoBalance;

public class Enemy : MonoBehaviour
{
    [SerializeField, BalanceLog("current_health")]
    private int currentHealth;
}
```

Objekte, die bereits beim Szenenstart existieren, werden automatisch erkannt. Für dynamisch erzeugte Objekte (z. B. per `Instantiate`) muss zusätzlich die Komponente `BalanceLogSource` am Root-GameObject hinzugefügt werden.

Mehr dazu unter [Logging](unity-plugin/logging.md).

---

## Schritt 4: Simulation beenden

CoBalance führt das Spiel im Headless Batch Mode aus. Damit es weiß, wann ein Simulationslauf abgeschlossen ist, muss `SimulationAPI.FinishScenario()` am natürlichen Endpunkt aufgerufen werden:

```csharp
using CoBalance.Simulations;
using UnityEngine;

public class GameManager : MonoBehaviour
{
    private void OnGameOver()
    {
        SimulationAPI.FinishScenario("gameOver");
    }
}
```

Mehr dazu unter [Simulation](unity-plugin/simulation.md).

---

## Schritt 5: Fitnesswert liefern (nur für Auto Suggestion)

Wird die Auto-Suggestion-Funktion der Desktop App genutzt, benötigt CoBalance zusätzlich einen Fitnesswert pro Simulationslauf. Dazu implementiert eine Szenenkomponente `IGeneticAlgorithmFitnessEvaluator`:

```csharp
using CoBalance;
using UnityEngine;

public class FitnessEvaluator : MonoBehaviour, IGeneticAlgorithmFitnessEvaluator
{
    [SerializeField] private GameManager gameManager;

    public float CalculateFitness()
    {
        return gameManager.FinalScore;
    }
}
```

Ein höherer Rückgabewert bedeutet eine bessere Balance. Wird die Komponente nicht gefunden, überspringt CoBalance diesen Schritt stillschweigend.

Mehr dazu unter [Auto Suggestion](unity-plugin/auto-suggestion.md).

---

## Nächste Schritte

Das Unity-Projekt ist jetzt eingerichtet. Im nächsten Abschnitt wird erklärt, wie das Projekt in der Desktop App geöffnet, Simulationen gestartet und die Auto-Suggestion-Funktion genutzt wird.

> Dieser Teil der Dokumentation wird in Kürze ergänzt.
