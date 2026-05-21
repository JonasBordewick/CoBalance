# CoBalance — Game Balancing Framework

CoBalance is a two-part toolchain for data-driven game balancing in Unity, developed as part of a master's thesis. It combines a Unity plugin with a desktop application to help game developers find optimal balance configurations through automated simulations and genetic algorithms.

## How It Works

```text
Unity (Headless Batch Mode)
  └─ runs simulation, returns fitness value
        ↑ starts process          ↓ reads value
Desktop App
  └─ genetic algorithm breeds parameter candidates over generations
  └─ best configurations are saved as .json files
```

You annotate your Unity MonoBehaviours or ScriptableObjects with CoBalance attributes to expose their fields as balance parameters. The desktop app reads these parameters, runs headless Unity simulations to evaluate them, and uses a genetic algorithm to automatically find optimized configurations.

---

## Components

### Unity Plugin

The Unity package provides the runtime and editor tools within your game project:

- Expose fields as balance parameters via attributes
- Define entities and their parameter groups
- Built-in logging system for simulation runs
- Headless simulation bootstrap for batch mode operation
- Editor window to view and manage balance files

### Desktop App

The desktop application is the control center for the balancing workflow:

- Load and browse `.cb` files and balance configurations
- View and edit parameters in a structured overview
- Start batch simulations and analyze the generated logs
- Run the genetic algorithm to automatically suggest optimized parameter sets
- Available as a pre-built executable for Windows, macOS, and Linux

---

## Installation

### Install the Unity Plugin

The Unity plugin is installed via the **Unity Package Manager** using a Git URL. No manual file copying is required.

1. Open the Package Manager in Unity via **Window → Package Manager**
2. Click the **+** button in the top-left corner
3. Select **Add package from git URL...**
4. Enter the following URL and confirm:

```text
https://github.com/JonasBordewick/CoBalance.git?path=unity
```

After successful installation, a new **CoBalance** menu entry appears in the Unity menu bar.

> **Requirements:** Unity 6000.0 or newer

### Install the Desktop App

Download the latest version for your operating system from the [Releases page](https://github.com/JonasBordewick/CoBalance/releases). The download is a single executable — no installation required, just run it.

| Platform | File                    |
|----------|-------------------------|
| Windows  | `CoBalance-windows.exe` |
| macOS    | `CoBalance-macos`       |
| Linux    | `CoBalance-linux`       |

---

## Getting Started

Once both components are installed, follow the [Getting Started guide](getting-started.md) to set up your first balancing project.
