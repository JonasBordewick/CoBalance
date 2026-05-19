# Überblick

Die CoBalance Desktop App ist die Steuerzentrale für den gesamten Balancing-Workflow. Sie liest Balance-Konfigurationen aus dem Unity-Projekt, startet Simulationen und hilft dabei, optimierte Parameterkombinationen zu finden.

---

## Oberfläche

Das Hauptfenster besteht aus drei Bereichen:

```
┌────┬────────────────────────────┬────┐
│    │                            │    │
│ L  │       Inhaltsbereich       │ R  │
│    │                            │    │
├────┴────────────────────────────┴────┤
│            Statusleiste              │
└──────────────────────────────────────┘
```

**Linke Navigationsleiste** — wechselt zwischen den drei Hauptansichten:

- **Parameter** — alle Balance-Parameter der geladenen Konfiguration einsehen und bearbeiten
- **Vergleich** — Parameterwerte mehrerer Entitäten nebeneinander vergleichen
- **Logs** — Simulationslogs durchsuchen und auswerten

**Rechte Navigationsleiste** — öffnet die Aktionsfenster:

- **Simulation** — Simulationsläufe mit der aktuellen Balance starten
- **Auto Suggestion** — genetischen Algorithmus starten, um optimierte Parameter zu finden

**Statusleiste** — zeigt den aktuellen Status laufender Jobs sowie das aktive Balance-Snapshot an.

---

## Menüleiste

| Menü | Einträge |
|---|---|
| **Project** | Open (`Ctrl+O`), Save (`Ctrl+S`), Save Balance As (`Ctrl+Shift+S`), Settings, Exit (`Ctrl+Q`) |
| **Selection** | Create Group From Selection (`Ctrl+G`), Remove Selected Logs From Group |
| **Help** | About, Documentation |

---

## Voraussetzung: Projekt öffnen

Die meisten Funktionen der App sind erst verfügbar, nachdem ein Projekt geöffnet wurde. Wie das funktioniert, ist unter [Projekt](project.md) beschrieben.
