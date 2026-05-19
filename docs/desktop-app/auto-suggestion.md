# Auto Suggestion

Das Auto-Suggestion-Fenster startet den genetischen Algorithmus, um automatisch optimierte Balance-Parameterkombinationen zu finden. Als Ergebnis entstehen mehrere Balance-Snapshots, die die besten gefundenen Konfigurationen repräsentieren.

Das Fenster wird über die rechte Navigationsleiste geöffnet.

> **Voraussetzung:** Das Unity-Projekt muss `IGeneticAlgorithmFitnessEvaluator` implementieren, damit der Algorithmus Kandidaten bewerten kann. Mehr dazu unter [Auto Suggestion (Unity Plugin)](../unity-plugin/auto-suggestion.md).

---

## Parameter vorauswählen

Bevor das Fenster geöffnet wird, sollten in der [Parameteransicht](parameter-view.md) die Parameter ausgewählt werden, die optimiert werden sollen. Das Fenster zeigt nur diese Parameter und erlaubt es, für jeden einen Wertebereich (Min/Max) festzulegen, innerhalb dessen der Algorithmus sucht.

---

## Einstellungen

### Context Settings

| Feld | Beschreibung |
|---|---|
| **Snapshot Identifier** | Name für diesen Optimierungslauf. Die besten Konfigurationen werden unter diesem Namen als Balance-Dateien gespeichert. |
| **Base Balance Snapshot** | Ausgangskonfiguration, auf deren Basis der Algorithmus startet. |
| **Unity Scene** | Unity-Szene, in der die Simulationen ausgeführt werden. |

### Execution Settings

| Feld | Beschreibung |
|---|---|
| **Method** | Optimierungsalgorithmus. Aktuell wird nur der genetische Algorithmus unterstützt. |
| **Population Size** | Anzahl der Kandidaten pro Generation. Größere Populationen erkunden den Suchraum breiter, erhöhen aber die Laufzeit. |
| **Number of Generations** | Wie viele Generationen der Algorithmus durchläuft. Mehr Generationen ermöglichen tiefere Optimierung bei längerer Gesamtlaufzeit. |
| **Iterations per Individual** | Wie oft jeder Kandidat simuliert wird. Mehrere Iterationen mitteln zufällige Schwankungen heraus und führen zu verlässlicheren Fitnesswerten. |
| **Choose Top** | Wie viele der besten Kandidaten am Ende als separate Balance-Dateien gespeichert werden. |
| **Speed Multiplier** | Beschleunigungsfaktor pro Simulationslauf (1× bis 20×). |
| **Max Simulation Time [s]** | Maximale Dauer pro Simulationslauf in Sekunden. |

### Parameter Settings

Für jeden vorausgewählten Parameter kann ein **Minimum** und ein **Maximum** definiert werden. Der genetische Algorithmus erzeugt nur Werte innerhalb dieser Grenzen.

---

## Optimierung starten

Ein Klick auf **Start Auto-Suggestion** validiert alle Eingaben und startet den Prozess. Der Fortschritt wird in der Statusleiste des Hauptfensters angezeigt (`Auto Suggestion: Generation X / Y`).

Am Ende werden die besten Konfigurationen automatisch als Balance-Snapshots im Projekt gespeichert und erscheinen in der Snapshot-Auswahl der Statusleiste.
