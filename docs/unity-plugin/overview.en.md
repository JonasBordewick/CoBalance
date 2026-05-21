# Overview

The **CoBalance Unity Plugin** marks balance-relevant data in the Unity project and provides the interface to the CoBalance Desktop App.

## Attributes

Two attributes are available to mark fields for CoBalance:

- `[BalanceParameter]` — marks fields as balance parameters that are read and optimized by the Desktop App.
- `[BalanceLog]` — marks fields whose values are written to log files during runtime.

## Entities

Parameters must be inside a **balanceable entity** for CoBalance to recognize them. Depending on the object type:

- **GameObject / Prefab** — add `EntityDescriptorComponent` to the root object
- **ScriptableObject** — implement `IBalanceableObject`

Details under [Entities](entities.md).

## Simulation

CoBalance starts Unity in Headless Batch Mode. The game code signals the end of the simulation using `SimulationAPI.FinishScenario()`. For the genetic algorithm, `IGeneticAlgorithmFitnessEvaluator` must also be implemented.

Details under [Simulation](simulation.md) and [Auto Suggestion](auto-suggestion.md).
