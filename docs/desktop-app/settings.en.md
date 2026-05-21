# Settings

The settings window is opened via **Project → Settings**. It is divided into two sections: app-wide settings and project-specific settings.

---

## App Settings

These settings apply regardless of the open project and are stored platform-specifically.

| Setting | Description |
|---|---|
| **Theme** | Switches between light and dark appearance of the app. |
| **Enable Auto Save** | Automatically saves changes to balance files and log groups on every change. Disables the manual save button. |
| **Default Number of Runs** | Pre-filled value for the number of simulation runs in the simulation window. |
| **Default Speed Multiplier** | Pre-filled acceleration factor in the simulation and auto suggestion window. |
| **Default Max Simulation Time [s]** | Pre-filled maximum simulation duration in the simulation and auto suggestion window. |

---

## Project Settings

These settings relate to the currently open project and are saved together with the `.cb` file. They are disabled when no project is open.

| Setting | Description |
|---|---|
| **Enable Time-Based Logging** | Enables or disables time-based logging in the Unity plugin. When disabled, `[BalanceLog]` fields are only written manually via `GameStatLogger`. |
| **Logging Interval [s]** | How often (in seconds) the Unity plugin writes a data point to the log file. Smaller values provide more detail but generate larger files. |
| **Unity Executable** | Path to the Unity application used for simulation runs. The file can be located in the file system via **Browse...**. |

---

## Saving

Settings are saved automatically when the window is closed.
