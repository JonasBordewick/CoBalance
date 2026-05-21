# Simulation

The simulation window starts simulation runs with a specific balance configuration. The results are saved as log files in the project and can then be analyzed in the [Logs view](logs-view.md).

The window is opened via the right navigation bar.

---

## Settings

### Context Settings

| Field | Description |
|---|---|
| **Simulation Identifier** | Freely chosen name for this simulation run. Determines the file name of the generated log files and is used to group runs together. Should be unique per set of runs. |
| **Balancing Snapshot** | Balance configuration used for the simulation. |
| **Unity Scene** | Unity scene in which the simulation is executed. |

### Execution Settings

| Field | Description |
|---|---|
| **Number of Runs** | How many times the simulation is repeated with the chosen balance. Multiple runs average out random variation. |
| **Speed Multiplier** | Acceleration factor for the simulation (1× to 20×). Higher values reduce runtime but may affect accuracy. |
| **Max Simulation Time [s]** | Maximum duration of a single simulation run in seconds. The run is automatically ended when this value is exceeded. This parameter serves as a fallback to prevent endless simulations. |

---

## Starting a Simulation

Clicking **Start Simulations** validates the inputs and starts the simulation. Progress is shown in the status bar of the main window.

If required fields (Identifier, Balance, Scene) are not filled in, a notification dialog appears.
