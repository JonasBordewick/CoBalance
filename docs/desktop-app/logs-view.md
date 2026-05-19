# Logs

Die Logs-Ansicht erlaubt es, Simulationslogs zu durchsuchen, zu gruppieren und grafisch auszuwerten.

---

## Aufbau

Die Ansicht ist zweigeteilt:

- **Oben links** — Tabelle aller verfügbaren Log-Dateien
- **Oben rechts** — Parameter-Panel mit Diagrammeinstellungen
- **Unten** — Diagrammbereich

---

## Log-Tabelle

Die Tabelle listet alle Log-Dateien im `CoBalance/Logs/`-Verzeichnis. Mehrere Logs können gleichzeitig ausgewählt werden.

| Spalte | Inhalt |
|---|---|
| **Name** | Dateiname des Logs |
| **Timestamp** | Erstellungszeitpunkt |
| **Group** | Zugehörige Gruppe (falls vorhanden) |

Die Tabelle ist standardmäßig nach Timestamp absteigend sortiert (neueste zuerst).

---

## Gruppen

Logs können zu Gruppen zusammengefasst werden, um mehrere Läufe gemeinsam auszuwerten.

**Gruppe erstellen:** Logs auswählen → Rechtsklick → *Create Group From Selection*, oder **Selection → Create Group From Selection** (`Ctrl+G`).

**Gruppe umbenennen / löschen:** Rechtsklick auf einen Log in der Gruppe.

**Log aus Gruppe entfernen:** Rechtsklick → *Remove From Group*, oder **Selection → Remove Selected Logs From Group**.

---

## Parameter-Panel

Nach Auswahl eines oder mehrerer Logs erscheinen im Panel rechts alle Log-Schlüssel, die in den ausgewählten Dateien vorkommen. Über Mehrfachauswahl können mehrere Schlüssel gleichzeitig geplottet werden.

---

## Diagrammeinstellungen

| Einstellung | Optionen | Beschreibung |
|---|---|---|
| **Value Mode** | Raw Values / Value per Second | Raw: absolute Werte. Per Second: normalisiert auf die Simulationsdauer — nützlich beim Vergleich unterschiedlich langer Läufe. |
| **Chart Type** | Line Chart / Boxplot | Line: Verlauf über die Zeit. Boxplot: Verteilung über alle ausgewählten Läufe. |
| **Compare Mode** | Individual / Grouped | Individual: jeder Log als eigene Linie. Grouped: Logs einer Gruppe werden zu einer Linie aggregiert. |
| **Group Aggregation Mode** | Mean / Median / Min / Max / Sum | Wie Werte innerhalb einer Gruppe zusammengefasst werden. Nur aktiv im Grouped-Modus. |
