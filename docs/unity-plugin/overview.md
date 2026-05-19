# Überblick

Das **CoBalance Unity-Plugin** kennzeichnet balancerelevante Daten im Unity-Projekt und stellt die Schnittstelle zur CoBalance Desktop App bereit.

## Attribute

Zwei Attribute stehen zur Verfügung, um Felder für CoBalance zu markieren:

- `[BalanceParameter]` — kennzeichnet Felder als Balance-Parameter, die von der Desktop App gelesen und optimiert werden.
- `[BalanceLog]` — kennzeichnet Felder, deren Werte während der Laufzeit in Log-Dateien geschrieben werden.

## Entitäten

Parameter müssen sich in einer **balancierbaren Entität** befinden, damit CoBalance sie erkennt. Je nach Objekttyp:

- **GameObject / Prefab** — `EntityDescriptorComponent` am Root-Objekt hinzufügen
- **ScriptableObject** — `IBalanceableObject` implementieren

Details unter [Entitäten](entities.md).

## Simulation

CoBalance startet Unity im Headless Batch Mode. Der Spielcode signalisiert das Simulationsende mit `SimulationAPI.FinishScenario()`. Für den genetischen Algorithmus wird zusätzlich `IGeneticAlgorithmFitnessEvaluator` implementiert.

Details unter [Simulation](simulation.md) und [Auto Suggestion](auto-suggestion.md).