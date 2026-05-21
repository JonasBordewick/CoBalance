# Logs

The logs view allows browsing, grouping, and graphically analyzing simulation logs.

---

## Structure

The view is split into two sections:

- **Top left** — table of all available log files
- **Top right** — parameter panel with chart settings
- **Bottom** — chart area

---

## Log Table

The table lists all log files in the `CoBalance/Logs/` directory. Multiple logs can be selected simultaneously.

| Column | Content |
|---|---|
| **Name** | File name of the log |
| **Timestamp** | Creation time |
| **Group** | Associated group (if any) |

The table is sorted by timestamp descending by default (newest first).

---

## Groups

Logs can be combined into groups to analyze multiple runs together.

**Create group:** Select logs → Right-click → *Create Group From Selection*, or **Selection → Create Group From Selection** (`Ctrl+G`).

**Rename / delete group:** Right-click a log in the group.

**Remove log from group:** Right-click → *Remove From Group*, or **Selection → Remove Selected Logs From Group**.

---

## Parameter Panel

After selecting one or more logs, all log keys present in the selected files appear in the panel on the right. Multiple keys can be selected simultaneously to plot several values at once.

---

## Chart Settings

| Setting | Options | Description |
|---|---|---|
| **Value Mode** | Raw Values / Value per Second | Raw: absolute values. Per Second: normalized to simulation duration — useful when comparing runs of different lengths. |
| **Chart Type** | Line Chart / Boxplot | Line: progression over time. Boxplot: distribution across all selected runs. |
| **Compare Mode** | Individual / Grouped | Individual: each log as its own line. Grouped: logs in a group are aggregated into one line. |
| **Group Aggregation Mode** | Mean / Median / Min / Max / Sum | How values within a group are combined. Only active in Grouped mode. |
