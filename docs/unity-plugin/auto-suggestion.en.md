# Auto Suggestion

The Auto Suggestion feature of the Desktop App uses a genetic algorithm to automatically find optimized parameter combinations. It does this by running multiple simulation runs and evaluating each combination based on a **fitness value**.

For CoBalance to retrieve this fitness value, the Unity project must provide a component that implements the `IGeneticAlgorithmFitnessEvaluator` interface.

---

## IGeneticAlgorithmFitnessEvaluator

```csharp
public interface IGeneticAlgorithmFitnessEvaluator
{
    float CalculateFitness();
}
```

When `SimulationAPI.FinishScenario()` is called, CoBalance automatically searches for a component with this interface in the current scene and calls `CalculateFitness()`.

**A higher return value means a better parameter combination.** The genetic algorithm maximizes this value over generations.

If no such component is present in the scene, this step is silently skipped — simulations without Auto Suggestion therefore work without any changes.

---

## Example

```csharp
using CoBalance;
using UnityEngine;

public class SimulationFitnessEvaluator : MonoBehaviour, IGeneticAlgorithmFitnessEvaluator
{
    [SerializeField] private GameManager gameManager;

    public float CalculateFitness()
    {
        // Higher score = better balance
        return gameManager.FinalScore;
    }
}
```

`SimulationFitnessEvaluator` is its own component in the scene. The `GameManager` calls `SimulationAPI.FinishScenario()` — CoBalance finds the evaluator automatically and retrieves the fitness value.

---

## Notes

- `CalculateFitness()` is called synchronously, immediately before the simulation run ends
- The fitness value should be calculated based on the entire simulation run, not just the final state
- Negative fitness values are allowed, but the genetic algorithm always optimizes toward higher values
