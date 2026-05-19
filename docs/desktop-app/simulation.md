# Simulation

Das Simulationsfenster startet Simulationsläufe mit einer bestimmten Balance-Konfiguration. Die Ergebnisse landen als Log-Dateien im Projekt und können anschließend in der [Logs-Ansicht](logs-view.md) ausgewertet werden.

Das Fenster wird über die rechte Navigationsleiste geöffnet.

---

## Einstellungen

### Context Settings

| Feld | Beschreibung |
|---|---|
| **Simulation Identifier** | Frei wählbarer Name für diesen Simulationslauf. Bestimmt den Dateinamen der erzeugten Log-Dateien und wird genutzt, um Läufe zusammenzufassen. Sollte pro Läufe-Set eindeutig sein. |
| **Balancing Snapshot** | Balance-Konfiguration, die für die Simulation verwendet wird. |
| **Unity Scene** | Unity-Szene, in der die Simulation ausgeführt wird. |

### Execution Settings

| Feld | Beschreibung |
|---|---|
| **Number of Runs** | Wie oft die Simulation mit der gewählten Balance wiederholt wird. Mehrere Läufe mitteln zufällige Schwankungen heraus. |
| **Speed Multiplier** | Beschleunigungsfaktor für die Simulation (1× bis 20×). Höhere Werte reduzieren die Laufzeit, können aber die Genauigkeit beeinflussen. |
| **Max Simulation Time [s]** | Maximale Dauer eines einzelnen Simulationslaufs in Sekunden. Der Lauf wird automatisch beendet, wenn dieser Wert überschritten wird. |

---

## Simulation starten

Ein Klick auf **Start Simulations** validiert die Eingaben und startet die Simulation. Der Fortschritt wird in der Statusleiste des Hauptfensters angezeigt.

Sind Pflichtfelder (Identifier, Balance, Szene) nicht ausgefüllt, erscheint ein Hinweisdialog.
