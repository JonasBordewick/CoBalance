# CoBalance — Game-Balancing-Framework

CoBalance ist ein zweiteiliges Toolchain für datengetriebenes Game-Balancing in Unity, das im Rahmen einer Masterarbeit entwickelt wurde. Es kombiniert ein Unity-Plugin mit einer Desktop-Anwendung, um Spieleentwicklern dabei zu helfen, optimale Balance-Konfigurationen durch automatisierte Simulationen und genetische Algorithmen zu finden.

## Funktionsweise

```text
Unity (Headless Batch Mode)
  └─ führt Simulation aus, gibt Fitnesswert zurück
        ↑ startet Prozess          ↓ liest Wert
Desktop App
  └─ genetischer Algorithmus züchtet Parameterkandidaten über Generationen
  └─ beste Konfigurationen werden als .json-Dateien gespeichert
```

Du annotierst deine Unity-MonoBehaviours oder ScriptableObjects mit CoBalance-Attributen, um ihre Felder als Balance-Parameter freizugeben. Die Desktop-App liest diese Parameter, führt Headless-Unity-Simulationen zur Auswertung durch und nutzt einen genetischen Algorithmus, um automatisch optimierte Konfigurationen zu finden.

---

## Komponenten

### Unity-Plugin

Das Unity-Paket stellt die Laufzeit- und Editor-Werkzeuge innerhalb deines Spielprojekts bereit:

- Felder als Balance-Parameter per Attribut freigeben
- Entitäten und ihre Parametergruppen definieren
- Integriertes Logging-System für Simulationsdurchläufe
- Headless-Simulations-Bootstrap für den Batch-Mode-Betrieb
- Editor-Fenster zum Einsehen und Verwalten von Balance-Dateien

### Desktop App

Die Desktop-Anwendung ist die Steuerzentrale für den Balancing-Workflow:

- `.cb`-Dateien und Balance-Konfigurationen laden und durchsuchen
- Parameter in einer strukturierten Übersicht einsehen und bearbeiten
- Batch-Simulationen starten und die erzeugten Logs auswerten
- Genetischen Algorithmus starten, um automatisch optimierte Parametersätze vorzuschlagen
- Als vorgefertigte ausführbare Datei für Windows, macOS und Linux verfügbar

---

## Installation

### Unity-Plugin installieren

Das Unity-Plugin wird über den **Unity Package Manager** per Git-URL installiert. Es ist kein manuelles Kopieren von Dateien erforderlich.

1. Öffne den Package Manager in Unity über **Window → Package Manager**
2. Klicke auf den **+**-Button in der oberen linken Ecke
3. Wähle **Add package from git URL...**
4. Gib die folgende URL ein und bestätige:

```text
https://github.com/JonasBordewick/CoBalance.git?path=unity
```

Nach erfolgreicher Installation erscheint ein neuer **CoBalance**-Menüeintrag in der Unity-Menüleiste.

> **Voraussetzungen:** Unity 6000.0 oder neuer

### Desktop App installieren

Lade die neueste Version für dein Betriebssystem von der [Releases-Seite](https://github.com/JonasBordewick/CoBalance/releases) herunter. Der Download ist eine einzelne ausführbare Datei — keine Installation erforderlich, einfach starten.

| Plattform | Datei                   |
|-----------|-------------------------|
| Windows   | `CoBalance-windows.exe` |
| macOS     | `CoBalance-macos`       |
| Linux     | `CoBalance-linux`       |

---

## Erste Schritte

Sobald beide Komponenten installiert sind, folge dem [Erste-Schritte-Leitfaden](getting-started.md), um dein erstes Balancing-Projekt einzurichten.
