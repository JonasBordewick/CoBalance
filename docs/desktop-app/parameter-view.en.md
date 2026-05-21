# Parameters

The parameter view displays all balance parameters of the currently loaded configuration in a table. Values can be edited directly here.

---

## Structure

The table contains four columns:

| Column | Content |
|---|---|
| **Parameter** | Display name of the parameter |
| **Value** | Current value — directly editable |
| **Entity** | Entity the parameter belongs to |
| **Category** | Category of the entity |

The table supports sorting by all columns. Multiple rows can be selected simultaneously.

---

## Search

The search bar at the top can be used to filter the table. The search covers all columns simultaneously and filters in real time.

---

## Editing Values

Double-clicking a cell in the Value column opens the input field. After entering the value, it is directly updated in the loaded balance snapshot.

If **Auto Save** is enabled, the change is saved immediately. Otherwise, the file is marked as modified (`*` in the window title) and must be saved manually.

---

## Selection for Auto Suggestion

By selecting multiple rows in the table, the corresponding parameters are queued for the Auto Suggestion window. There, a value range (Min/Max) can be defined for each selected parameter within which the genetic algorithm searches.

More details under [Auto Suggestion](auto-suggestion.md).
