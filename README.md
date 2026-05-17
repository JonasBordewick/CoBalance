# Cobalance — Game Balancing Framework

A two-part toolchain for data-driven game balancing in Unity, built as part of a master's thesis.

- **Unity Package** (`unity/`) — runtime & editor extension that exposes balance parameters, runs headless simulations, and reports fitness scores.
- **Desktop App** (`app/`) — PyQt6 GUI that loads balance files, triggers Unity batch simulations, and runs a genetic algorithm to find optimised parameter configurations automatically.

---

## Repository layout

```
cobalance/
├── app/               # Python desktop application (PyQt6, MVVM)
│   ├── main.py        # Entry point
│   ├── requirements.txt
│   ├── styles/        # QSS stylesheet
│   └── app/           # Source — domain, io, models, ui, viewmodels
├── unity/             # Unity UPM package
│   ├── Runtime/       # Components, logging, simulation bootstrap
│   └── Editor/        # Inspector windows, menu builder, GA finalizer
├── docs/              # MkDocs source
└── mkdocs.yml
```

---

## Quick start

### Unity Package

Add the package to your Unity project (Unity 6+) via the Package Manager using a local path or Git URL:

```
Packages/manifest.json  →  "dev.bordewick.balancingframework": "file:../../cobalance/unity"
```

Mark your MonoBehaviour fields or ScriptableObject properties with the provided attributes to expose them as balance parameters. See [docs/unity-plugin/](docs/unity-plugin/) for a full walkthrough.

### Desktop App

Requires **Python 3.11+** and a compiled headless Unity build of your project.

```bash
cd app
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

1. **File → Open Project** — select a `.bfproject` file.
2. Browse and edit parameters in the **Parameter Overview** tab.
3. Open the **Simulation** panel to run a batch and inspect logs.
4. Open the **Auto Suggestion** panel to start the genetic algorithm — results are saved as new balance files in the project's `Balances/` directory.

---

## How the toolchain works together

```
Unity (headless batch mode)
  └─ runs simulation, writes fitness score to stdout
        ↑ spawns process          ↓ reads score
Desktop App
  └─ GA worker breeds parameter candidates across generations
  └─ best configurations saved as .balance files
```

The genetic algorithm evaluates each candidate by launching Unity in batch mode, collecting the fitness score returned by `GeneticAlgorithmFitnessResultFinalizer`, and breeding the next generation via tournament selection, blend crossover, and elitism.

---

## Documentation

Full documentation is built with [MkDocs](https://www.mkdocs.org/):

```bash
pip install mkdocs mkdocs-material
mkdocs serve        # live preview at http://localhost:8000
mkdocs build        # output → site/
```

---

## Requirements

| Component     | Requirement                        |
|---------------|------------------------------------|
| Unity Package | Unity 6000.0+                      |
| Desktop App   | Python 3.11+, PyQt6                |
| Documentation | MkDocs + readthedocs theme         |
