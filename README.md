# CoBalance — Game Balancing Framework

A two-part toolchain for data-driven game balancing in Unity, built as part of a master's thesis.

- **Unity Package** (`unity/`) — runtime & editor extension that exposes balance parameters, runs headless simulations, and reports fitness scores.
- **Desktop App** (`app/`) — PyQt6 GUI that loads balance files, triggers Unity batch simulations, and runs a genetic algorithm to find optimised parameter configurations automatically.

📖 **Full documentation:** [cobalance.bordewick.dev](https://cobalance.bordewick.dev)

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

## Installation

### Unity Plugin

The plugin is installed via the **Unity Package Manager** using a Git URL. No manual file copying required.

1. Open **Window → Package Manager** in Unity
2. Click **+** → **Add package from git URL...**
3. Enter the following URL and confirm:

```
https://github.com/JonasBordewick/CoBalance.git?path=unity
```

After a successful installation a **CoBalance** menu entry will appear in the Unity menu bar.

> **Requires Unity 6000.0 or newer.**

### Desktop App

#### Option A — Pre-built Binaries

Download the latest release for your operating system from the [Releases page](https://github.com/JonasBordewick/CoBalance/releases). The download is a single executable — no installation required, just run it.

| Platform | File                    |
|----------|-------------------------|
| Windows  | [CoBalance.exe](https://github.com/USER/REPO/releases/latest/download/CoBalance.exe) |
| macOS    | [CoBalance.dmg](https://github.com/USER/REPO/releases/latest/download/CoBalance.dmg)       |
| Linux    | [CoBalance-x86_64.AppImage](https://github.com/USER/REPO/releases/latest/download/CoBalance-x86_64.AppImage)      |

#### Option B — Build from Source

Requires **Python 3.11+**.

```bash
git clone https://github.com/JonasBordewick/CoBalance.git
cd CoBalance/app
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

---

## How the toolchain works together

```
Unity (headless batch mode)
  └─ runs simulation, returns fitness score
        ↑ spawns process          ↓ reads score
Desktop App
  └─ GA worker breeds parameter candidates across generations
  └─ best configurations saved as .json balance files
```

The genetic algorithm evaluates each candidate by launching Unity in batch mode, collecting the fitness score returned by `IGeneticAlgorithmFitnessEvaluator`, and breeding the next generation via tournament selection, blend crossover, and elitism.

---

## Documentation

Full documentation is available at [cobalance.bordewick.dev](https://cobalance.bordewick.dev).

To build and preview locally:

```bash
pip install mkdocs mkdocs-material
mkdocs serve        # live preview at http://localhost:8000
mkdocs build        # output → site/
```

---

## Requirements

| Component     | Requirement           |
|---------------|-----------------------|
| Unity Plugin  | Unity 6000.0+         |
| Desktop App   | Python 3.11+, PyQt6   |
| Documentation | MkDocs + mkdocs-material |
