# Simulation

Eine Simulation in CoBalance ist eine vollständige Ausführung des Spiels — von Start bis zu einem definierten Endpunkt. CoBalance startet diese Simulationen automatisch im Headless Batch Mode, um Parameterkombinationen zu testen.

Die einzige Anforderung an den Spielcode ist: **das Ende der Simulation muss signalisiert werden.**

---

## Simulation beenden

Sobald die Simulation ihren natürlichen Endpunkt erreicht hat — z. B. ein Timer abgelaufen ist, ein Spieler gewonnen hat oder eine bestimmte Bedingung erfüllt wurde — wird `SimulationAPI.FinishScenario()` aufgerufen:

```csharp
using CoBalance.Simulations;

SimulationAPI.FinishScenario();
```

CoBalance beendet daraufhin den laufenden Simulationslauf und startet den nächsten, falls noch weitere ausstehen.

Der optionale `reason`-Parameter ist ein freier Label für den Endgrund und dient nur der Diagnose:

```csharp
SimulationAPI.FinishScenario("timeout");
SimulationAPI.FinishScenario("playerWon");
```

!!! warning
    `FinishScenario` darf pro Simulationslauf **genau einmal** aufgerufen werden.
    Mehrfache Aufrufe werden intern ignoriert.

---

## Beispiel

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

Das war's — mehr ist für eine Simulation nicht notwendig.

Soll die Simulation zusammen mit dem **genetischen Algorithmus** der Desktop App verwendet werden, ist zusätzlich ein Fitnesswert erforderlich. Mehr dazu unter [Auto Suggestion](auto-suggestion.md).
