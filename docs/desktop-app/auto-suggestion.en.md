# Auto Suggestion

The Auto Suggestion window runs the genetic algorithm to automatically find optimized balance parameter combinations. The result is a set of balance snapshots representing the best configurations found.

The window is opened via the right navigation bar.

> **Requirement:** The Unity project must implement `IGeneticAlgorithmFitnessEvaluator` so the algorithm can evaluate candidates. More details under [Auto Suggestion (Unity Plugin)](../unity-plugin/auto-suggestion.md).

---

## Pre-selecting Parameters

Before opening the window, the parameters to be optimized should be selected in the [Parameters view](parameter-view.md). The window only shows these parameters and allows setting a value range (Min/Max) for each one, within which the algorithm searches.

---

## Settings

### Context Settings

| Field | Description |
|---|---|
| **Snapshot Identifier** | Name for this optimization run. The best configurations will be saved under this name as balance files. |
| **Base Balance Snapshot** | Starting configuration from which the algorithm begins. |
| **Unity Scene** | Unity scene in which the simulations are executed. |

### Execution Settings

| Field | Description |
|---|---|
| **Method** | Optimization algorithm. Currently only the genetic algorithm is supported. |
| **Population Size** | Number of candidates per generation. Larger populations explore the search space more broadly but increase runtime. |
| **Number of Generations** | How many generations the algorithm runs. More generations allow deeper optimization at the cost of longer total runtime. |
| **Iterations per Individual** | How many times each candidate is simulated. Multiple iterations average out random variation and lead to more reliable fitness values. |
| **Choose Top** | How many of the best candidates are saved as separate balance files at the end. |
| **Speed Multiplier** | Acceleration factor per simulation run (1× to 20×). |
| **Max Simulation Time [s]** | Maximum duration per simulation run in seconds. See [Simulation](./simulation.md). |

### Parameter Settings

A **minimum** and **maximum** can be defined for each pre-selected parameter. The genetic algorithm only generates values within these bounds.

---

## Starting the Optimization

Clicking **Start Auto-Suggestion** validates all inputs and starts the process. Progress is shown in the status bar of the main window (`Auto Suggestion: Generation X / Y`).

At the end, the best configurations are automatically saved as balance snapshots in the project and appear in the snapshot selector in the status bar.
