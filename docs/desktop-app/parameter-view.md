# Parameter

Die Parameteransicht zeigt alle Balance-Parameter der aktuell geladenen Konfiguration in einer Tabelle. Werte können hier direkt bearbeitet werden.

---

## Aufbau

Die Tabelle enthält vier Spalten:

| Spalte | Inhalt |
|---|---|
| **Parameter** | Anzeigename des Parameters |
| **Value** | Aktueller Wert — direkt editierbar |
| **Entity** | Entität, zu der der Parameter gehört |
| **Category** | Kategorie der Entität |

Die Tabelle unterstützt Sortierung über alle Spalten. Mehrere Zeilen können gleichzeitig ausgewählt werden.

---

## Suche

Über die Suchleiste oben kann die Tabelle gefiltert werden. Die Suche greift auf alle Spalten gleichzeitig zu und filtert in Echtzeit.

---

## Werte bearbeiten

Ein Doppelklick auf eine Zelle in der Value-Spalte öffnet das Eingabefeld. Nach der Eingabe wird der Wert direkt im geladenen Balance-Snapshot aktualisiert.

Ist **Auto Save** aktiviert, wird die Änderung sofort gespeichert. Andernfalls wird die Datei als geändert markiert (`*` im Fenstertitel) und muss manuell gespeichert werden.

---

## Auswahl für Auto Suggestion

Durch Auswahl mehrerer Zeilen in der Tabelle werden die entsprechenden Parameter für das Auto-Suggestion-Fenster vorgemerkt. Dort kann für jeden ausgewählten Parameter ein Wertebereich (Min/Max) definiert werden, innerhalb dessen der genetische Algorithmus sucht.

Mehr dazu unter [Auto Suggestion](auto-suggestion.md).
