# Einstellungen

Das Einstellungsfenster wird über **Project → Settings** geöffnet. Es ist in zwei Bereiche unterteilt: App-weite Einstellungen und projektspezifische Einstellungen.

---

## App Settings

Diese Einstellungen gelten unabhängig vom geöffneten Projekt und werden plattformspezifisch gespeichert.

| Einstellung | Beschreibung |
|---|---|
| **Theme** | Wechselt zwischen hellem und dunklem Erscheinungsbild der App. |
| **Enable Auto Save** | Speichert Änderungen an Balance-Dateien und Log-Gruppen automatisch bei jeder Änderung. Deaktiviert den manuellen Save-Button. |
| **Default Number of Runs** | Vorausgefüllter Wert für die Anzahl der Simulationsläufe im Simulationsfenster. |
| **Default Speed Multiplier** | Vorausgefüllter Beschleunigungsfaktor im Simulations- und Auto-Suggestion-Fenster. |
| **Default Max Simulation Time [s]** | Vorausgefüllte maximale Simulationsdauer im Simulations- und Auto-Suggestion-Fenster. |

---

## Project Settings

Diese Einstellungen beziehen sich auf das aktuell geöffnete Projekt und werden zusammen mit der `.cb`-Datei gespeichert. Sie sind deaktiviert, wenn kein Projekt geöffnet ist.

| Einstellung | Beschreibung |
|---|---|
| **Enable Time-Based Logging** | Aktiviert oder deaktiviert das zeitgesteuerte Logging im Unity-Plugin. Wenn deaktiviert, werden `[BalanceLog]`-Felder nur noch manuell über `GameStatLogger` beschrieben. |
| **Logging Interval [s]** | Wie oft (in Sekunden) das Unity-Plugin einen Datenpunkt in die Log-Datei schreibt. Kleinere Werte liefern mehr Detail, erzeugen aber größere Dateien. |
| **Unity Executable** | Pfad zur Unity-Anwendung, die für Simulationsläufe gestartet wird. Über **Browse...** kann die Datei im Dateisystem gesucht werden. |

---

## Speichern

Die Einstellungen werden automatisch gespeichert, wenn das Fenster geschlossen wird.
