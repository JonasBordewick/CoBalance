# Simulation

A simulation in CoBalance is a complete run of the game — from start to a defined endpoint. CoBalance starts these simulations automatically in Headless Batch Mode to test parameter combinations.

The only requirement on the game code is: **the end of the simulation must be signaled.**

---

## Ending the Simulation

Once the simulation has reached its natural endpoint — e.g., a timer has expired, a player has won, or a certain condition has been met — `SimulationAPI.FinishScenario()` is called:

```csharp
using CoBalance.Simulations;

SimulationAPI.FinishScenario();
```

CoBalance then ends the current simulation run and starts the next one if more are pending.

The optional `reason` parameter is a free label for the end reason and is used only for diagnostics:

```csharp
SimulationAPI.FinishScenario("timeout");
SimulationAPI.FinishScenario("playerWon");
```

!!! warning
    `FinishScenario` must be called **exactly once** per simulation run.
    Multiple calls are ignored internally.

---

## Example

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

That's it — nothing more is needed for a simulation.

If the simulation is to be used together with the **genetic algorithm** of the Desktop App, a fitness value is also required. More details under [Auto Suggestion](auto-suggestion.md).
