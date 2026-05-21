# Overview

The CoBalance Desktop App is the control center for the entire balancing workflow. It reads balance configurations from the Unity project, starts simulations, and helps find optimized parameter combinations.

---

## Interface

The main window consists of three areas:

```
┌────┬────────────────────────────┬────┐
│    │                            │    │
│ L  │       Content Area         │ R  │
│    │                            │    │
├────┴────────────────────────────┴────┤
│              Status Bar              │
└──────────────────────────────────────┘
```

**Left navigation bar** — switches between the three main views:

- **Parameters** — view and edit all balance parameters of the loaded configuration
- **Comparison** — compare parameter values of multiple entities side by side
- **Logs** — browse and analyze simulation logs

**Right navigation bar** — opens the action panels:

- **Simulation** — start simulation runs with the current balance
- **Auto Suggestion** — run the genetic algorithm to find optimized parameters

**Status bar** — shows the current status of running jobs and the active balance snapshot.

---

## Menu Bar

| Menu | Entries |
|---|---|
| **Project** | Open (`Ctrl+O`), Save (`Ctrl+S`), Save Balance As (`Ctrl+Shift+S`), Settings, Exit (`Ctrl+Q`) |
| **Selection** | Create Group From Selection (`Ctrl+G`), Remove Selected Logs From Group |
| **Help** | About, Documentation |

---

## Requirement: Open a Project

Most of the app's features are only available after a project has been opened. How this works is described under [Project](project.md).
