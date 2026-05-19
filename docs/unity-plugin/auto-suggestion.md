# Auto Suggestion

Die Auto-Suggestion-Funktion der Desktop App nutzt einen genetischen Algorithmus, um automatisch optimierte Parameterkombinationen zu finden. Dazu führt sie mehrere Simulationsläufe durch und bewertet jede Kombination anhand eines **Fitnesswerts**.

Damit CoBalance diesen Fitnesswert abrufen kann, muss das Unity-Projekt eine Komponente bereitstellen, die das Interface `IGeneticAlgorithmFitnessEvaluator` implementiert.

---

## IGeneticAlgorithmFitnessEvaluator

```csharp
public interface IGeneticAlgorithmFitnessEvaluator
{
    float CalculateFitness();
}
```

CoBalance sucht beim Aufruf von `SimulationAPI.FinishScenario()` automatisch nach einer Komponente mit diesem Interface in der aktuellen Szene und ruft `CalculateFitness()` ab.

**Ein höherer Rückgabewert bedeutet eine bessere Parameterkombination.** Der genetische Algorithmus maximiert diesen Wert über Generationen hinweg.

Ist keine solche Komponente in der Szene vorhanden, wird der Schritt stillschweigend übersprungen — Simulationen ohne Auto Suggestion funktionieren deshalb ohne Änderungen.

---

## Beispiel

```csharp
using CoBalance;
using UnityEngine;

public class SimulationFitnessEvaluator : MonoBehaviour, IGeneticAlgorithmFitnessEvaluator
{
    [SerializeField] private GameManager gameManager;

    public float CalculateFitness()
    {
        // Höherer Score = bessere Balance
        return gameManager.FinalScore;
    }
}
```

`SimulationFitnessEvaluator` ist eine eigene Komponente in der Szene. Der `GameManager` ruft `SimulationAPI.FinishScenario()` auf — CoBalance findet den Evaluator automatisch und holt den Fitnesswert ab.

---

## Hinweise

- `CalculateFitness()` wird synchron aufgerufen, direkt bevor der Simulationslauf beendet wird
- Der Fitnesswert sollte auf Basis des gesamten Simulationsverlaufs berechnet werden, nicht nur des letzten Zustands
- Negative Fitnesswerte sind erlaubt, aber der genetische Algorithmus optimiert immer in Richtung höherer Werte
