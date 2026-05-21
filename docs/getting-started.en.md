# Getting Started

This guide walks through the complete CoBalance workflow — from defining your first entity to running simulations and automatic optimization.

> **Prerequisites:** The Unity plugin and Desktop App are already installed.  
> If not, follow the steps under [Installation](index.md#installation) first.

---

## Step 1: Define an Entity

CoBalance works with **entities** — objects in the game that have balance-relevant parameters. The definition differs depending on the object type.

**ScriptableObject** — implements `IBalanceableObject`:

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

**GameObject / Prefab** — add `EntityDescriptorComponent` to the root object. No code changes required.

More details under [Entities](unity-plugin/entities.md).

---

## Step 2: Mark Balance Parameters

Fields that CoBalance should optimize are annotated with `[BalanceParameter]`. Supported types are `int` and `float`.

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

More details under [Parameters](unity-plugin/parameters.md).

---

## Step 3: Open the Project in the Desktop App

Start the Unity project once in the Editor. CoBalance automatically creates a `CoBalance/` folder in the project directory, which contains the project file `project.cb`.

Open the Desktop App and go to **Project → Open** (`Ctrl+O`). Select the `project.cb` file from the `CoBalance/` folder of your Unity project.

After opening, the **Parameters** view should show all fields annotated with `[BalanceParameter]`, organized by entity and category. This is a good way to verify that annotations were recognized correctly before proceeding.

---

## Step 4: Prepare the Simulation

CoBalance runs the game in Headless Batch Mode. The game code must signal the end of each simulation run using `SimulationAPI.FinishScenario()`:

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

Also, the path to the Unity executable must be set in the **Desktop App settings** (`Project → Settings`).

More details under [Simulation](unity-plugin/simulation.md).

---

## Step 5: Start the Simulation

Open the simulation window in the Desktop App via the **right navigation bar**. Configure:

- **Simulation Identifier** — a unique name for this run (determines the log file name)
- **Balancing Snapshot** — which balance configuration to use
- **Unity Scene** — the scene in which the simulation runs
- **Number of Runs** — how many times the run is repeated

Click **Start Simulations** to launch Unity in the background. The status is shown in the status bar.

More details under [Simulation (Desktop App)](desktop-app/simulation.md).

---

## Step 6: Analyze Logs (Optional)

Fields to be observed during the simulation can be annotated with `[BalanceLog]`:

```csharp
public class Enemy : MonoBehaviour
{
    [SerializeField, BalanceLog("current_health")]
    private int currentHealth;
}
```

After the simulation completes, the generated log files appear automatically in the **Logs** view of the Desktop App. Values can be displayed as line charts or boxplots, and multiple runs can be compared.

More details under [Logging](unity-plugin/logging.md) and [Logs (Desktop App)](desktop-app/logs-view.md).

---

## Step 7: Set Up Auto Suggestion (Optional)

The genetic algorithm optimizes parameters automatically — it needs a fitness value per simulation run. A scene component implements `IGeneticAlgorithmFitnessEvaluator` for this:

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

Then in the Desktop App:

1. Select the parameters to optimize in the **Parameters** view
2. Open the **Auto Suggestion** window via the right navigation bar
3. Configure the snapshot identifier, base balance, scene, and algorithm settings
4. Set **Min/Max** bounds for each parameter
5. Click **Start Auto-Suggestion**

The best configurations are automatically saved as new balance snapshots at the end.

More details under [Auto Suggestion (Unity)](unity-plugin/auto-suggestion.md) and [Auto Suggestion (Desktop App)](desktop-app/auto-suggestion.md).
