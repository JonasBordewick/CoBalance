# Erste Schritte

Dieser Guide führt durch den kompletten CoBalance-Workflow — von der ersten Entität bis zur fertigen Simulation und automatischen Optimierung.

> **Voraussetzungen:** Unity-Plugin und Desktop App sind bereits installiert.  
> Falls nicht, folge zuerst den Schritten unter [Installation](index.md#installation).

---

## Schritt 1: Entität definieren

CoBalance arbeitet mit **Entitäten** — Objekten im Spiel, die balancerelevante Parameter besitzen. Je nach Objekttyp unterscheidet sich die Definition.

**ScriptableObject** — implementiert `IBalanceableObject`:

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

**GameObject / Prefab** — `EntityDescriptorComponent` am Root-Objekt hinzufügen. Keine Code-Änderungen nötig.

Mehr dazu unter [Entitäten](unity-plugin/entities.md).

---

## Schritt 2: Balance-Parameter markieren

Felder, die CoBalance optimieren soll, werden mit `[BalanceParameter]` annotiert. Unterstützte Typen sind `int` und `float`.

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

## Schritt 3: Projekt in der Desktop App öffnen

Starte das Unity-Projekt einmal im Editor. CoBalance legt dabei automatisch einen `CoBalance/`-Ordner im Projektverzeichnis an, der u.a. die Projektdatei `project.cb` enthält.

Öffne die Desktop App und gehe auf **Project → Open** (`Ctrl+O`). Wähle die `project.cb`-Datei aus dem `CoBalance/`-Ordner deines Unity-Projekts.

Nach dem Öffnen sollten in der **Parameter**-Ansicht alle mit `[BalanceParameter]` markierten Felder sichtbar sein — aufgeteilt nach Entität und Kategorie. Das ist eine gute Möglichkeit zu prüfen, ob die Annotationen korrekt erkannt wurden, bevor es weitergeht.

---

## Schritt 4: Simulation vorbereiten

CoBalance führt das Spiel im Headless Batch Mode aus. Der Spielcode muss das Ende jedes Simulationslaufs mit `SimulationAPI.FinishScenario()` signalisieren:

```csharp
using CoBalance.Simulations;
using UnityEngine;

public class GameManager : MonoBehaviour
{
    private void OnGameOver()
    {
        SimulationAPI.FinishScenario("gameOver");
    }

    private void OnPlayerWon()
    {
        SimulationAPI.FinishScenario("playerWon");
    }
}
```

Außerdem muss in den **Einstellungen der Desktop App** (`Project → Settings`) der Pfad zur Unity-Executable eingetragen sein.

Mehr dazu unter [Simulation](unity-plugin/simulation.md).

---

## Schritt 5: Simulation starten

Öffne in der Desktop App das Simulationsfenster über die **rechte Navigationsleiste**. Konfiguriere:

- **Simulation Identifier** — eindeutiger Name für diesen Lauf (bestimmt den Log-Dateinamen)
- **Balancing Snapshot** — welche Balance-Konfiguration verwendet werden soll
- **Unity Scene** — die Szene, in der die Simulation läuft
- **Number of Runs** — wie oft der Lauf wiederholt wird

Ein Klick auf **Start Simulations** startet Unity im Hintergrund. Der Status wird in der Statusleiste angezeigt.

Mehr dazu unter [Simulation (Desktop App)](desktop-app/simulation.md).

---

## Schritt 6: Logs auswerten (optional)

Felder, die während der Simulation beobachtet werden sollen, können mit `[BalanceLog]` markiert werden:

```csharp
public class Enemy : MonoBehaviour
{
    [SerializeField, BalanceLog("current_health")]
    private int currentHealth;
}
```

Nach abgeschlossener Simulation erscheinen die erzeugten Log-Dateien automatisch in der **Logs**-Ansicht der Desktop App. Dort können Werte als Linien- oder Boxplot-Diagramm dargestellt und mehrere Läufe miteinander verglichen werden.

Mehr dazu unter [Logging](unity-plugin/logging.md) und [Logs (Desktop App)](desktop-app/logs-view.md).

---

## Schritt 7: Auto Suggestion einrichten (optional)

Der genetische Algorithmus optimiert Parameter automatisch — er braucht dafür einen Fitnesswert pro Simulationslauf. Eine Szenenkomponente implementiert dafür `IGeneticAlgorithmFitnessEvaluator`:

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

Anschließend in der Desktop App:

1. In der **Parameter**-Ansicht die zu optimierenden Parameter auswählen
2. Das **Auto-Suggestion**-Fenster über die rechte Navigationsleiste öffnen
3. Snapshot-Identifier, Basis-Balance, Szene und Algorithmus-Einstellungen konfigurieren
4. Für jeden Parameter **Min/Max**-Grenzen festlegen
5. **Start Auto-Suggestion** klicken

Die besten Konfigurationen werden am Ende automatisch als neue Balance-Snapshots gespeichert.

Mehr dazu unter [Auto Suggestion (Unity)](unity-plugin/auto-suggestion.md) und [Auto Suggestion (Desktop App)](desktop-app/auto-suggestion.md).
