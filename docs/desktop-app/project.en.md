# Project

A CoBalance project is a `.cb` file that is automatically created in the Unity project on first launch. It contains path and configuration information that the Desktop App needs to work with the Unity project.

---

## Opening a Project

**Project → Open** (`Ctrl+O`) opens a file dialog where a `.cb` file can be selected. The app remembers the last opened project and automatically navigates to the correct directory on the next launch.

After opening a project, the following are automatically detected:

- all **balance snapshots** in the `CoBalance/Balances/` directory
- all **Unity scenes** in the project
- all **log files** in the `CoBalance/Logs/` directory

---

## Switching Balance Snapshots

A dropdown menu in the status bar at the bottom shows the currently active balance snapshot. It allows switching between all available snapshots — the parameter view updates automatically.

---

## Saving

**Project → Save** (`Ctrl+S`) saves the current balance snapshot and any changes to log groups.

**Project → Save Balance As** (`Ctrl+Shift+S`) saves the currently loaded balance under a new file name as a `.json` file.

If **Auto Save** is enabled in the settings, all changes are saved automatically immediately, and the manual save button is disabled.

When closing the app with unsaved changes, a confirmation dialog appears.

---

## External Changes

If the currently open balance file is modified externally (e.g., by a completed simulation), the app detects this automatically. A dialog asks whether the file should be reloaded.
