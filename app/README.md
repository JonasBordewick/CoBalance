# Balancing Tool UI

A desktop application for game balance management. It lets you inspect and edit balance parameter files, run Unity simulations in batch mode, and use a genetic algorithm to automatically find optimised balance configurations.

## Features

| Feature | Description |
|---|---|
| **Parameter Overview** | Browse, search, and edit all parameters of the loaded balance file. |
| **Entity Comparison** | Compare parameter values across multiple entities with a normalised bar or radar chart. |
| **Log Explorer** | Explore simulation log files, group them, and plot results as line charts or boxplots. |
| **Simulation Runner** | Launch Unity in headless batch mode and run a configurable number of simulation iterations. |
| **Auto Suggestion** | Run a genetic algorithm over selected parameters to find balance configurations that maximise a fitness score returned by the Unity simulation. |

## Requirements

- Python 3.11+
- A Unity project with the `CoBalance` editor extension installed
- The compiled Unity application (headless executable)

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd balancing-tool-ui

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Running

```bash
python main.py
```

## Getting Started

1. **Open a project** via *Project → Open* and select a `.cb` file.
2. The **Parameter Overview** tab shows all balance values. Select rows to mark parameters for Auto Suggestion.
3. Open the **Simulation** panel (right navbar) to run a single simulation batch and inspect log output in the **Logs** tab.
4. Open the **Auto Suggestion** panel (right navbar) to configure and start the genetic algorithm. Results are written as new balance files to the project's `Balances/` directory.

## Project Structure

```
balancing-tool-ui/
├── main.py                         # Entry point, wires up ViewModels and launches the window
├── requirements.txt
├── styles/
│   └── default.qss                 # Application stylesheet
└── app/
    ├── domain/
    │   ├── auto_suggestion/        # GA settings and candidate models
    │   ├── logs/                   # Log analysis service (line charts, boxplots)
    │   └── simulation/             # Simulation job models and factory
    ├── enums/                      # Shared enums (chart types, value modes, …)
    ├── io/
    │   ├── group/                  # Group persistence (groups.json)
    │   ├── process/                # Unity subprocess runner
    │   ├── repositories/           # Balance, job, and project settings file I/O
    │   └── watchers/               # Filesystem watcher service
    ├── models/                     # Qt table models, data transfer objects
    ├── ui/
    │   ├── views/                  # Parameter, comparison, and log views
    │   ├── widgets/                # Reusable custom widgets
    │   ├── main_window.py
    │   ├── simulation_window.py
    │   └── auto_suggestion_window.py
    ├── utilities/                  # String helpers, log file parser
    └── viewmodels/                 # MVVM ViewModels — one per domain area
```

## Architecture

The application follows the **MVVM** pattern:

- **Models** — pure data classes and Qt table models (`app/models/`).
- **ViewModels** — hold application state, expose Qt signals, and contain all business logic (`app/viewmodels/`). Views never touch the data layer directly.
- **Views** — PyQt6 widgets that bind to ViewModels via signals and slots (`app/ui/`).
- **Workers** — `QObject` subclasses moved onto `QThread` for blocking I/O (Unity simulation, genetic algorithm). The `JobViewModel` manages their lifecycle.

## Auto Suggestion — How It Works

The genetic algorithm runs entirely in a background thread via `GeneticAlgorithmWorker`:

1. An initial population of random parameter combinations is created.
2. Each generation is evaluated in a single batched Unity simulation run.
3. Candidates are ranked by their average fitness score returned by Unity.
4. The next generation is bred via tournament selection, blend crossover, and random mutation.
5. Elite individuals are carried over unchanged so the best result is never lost.
6. After all generations, the top-k individuals are saved as separate balance files.
