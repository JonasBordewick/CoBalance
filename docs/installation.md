# Installation

**Ziel:** Die CoBalance-Toolchain auf deinem Rechner einrichten, bevor du mit den eigentlichen Übungen beginnst. Am Ende hast du das Unity-Beispielprojekt geöffnet, das Balancing Tool gestartet und bestätigt, dass beide Dateien austauschen können.

---

## Schritt 1 – Unity-Projekt vorbereiten

- Erstelle ein neues Projekt: **New Project → 2D (Built-in Render Pipeline)**, Unity 6.
- Lade [TODO: Paketname]() von der Release-Seite oder Digicampus herunter.
- In Unity: **Assets → Import Package → Custom Package...**, wähle das heruntergeladene `.unitypackage`.
- Lass im Import-Dialog alles ausgewählt und klicke auf **Import**.

---

## Schritt 2 – CoBalance-Plugin installieren

Das Plugin wird über den Unity Package Manager per Git-URL installiert – kein manuelles Kopieren von Dateien nötig.

1. Öffne **Window → Package Manager**
2. Klicke auf den **+**-Button oben links
3. Wähle **Add package from git URL...**
4. Gib diese URL ein und bestätige:

```text
https://github.com/JonasBordewick/CoBalance.git?path=unity
```

> ✅ **Prüfpunkt:** Ein neuer **CoBalance**-Eintrag erscheint in der Unity-Menüleiste.

---

## Schritt 3 – CoBalance Tool einrichten

Das Tool wird als eigenständige Anwendung ausgeliefert – keine Python-Installation notwendig.

!!! warning
        Die App ist **nicht code-signiert**, weshalb das Betriebssystem beim ersten Öffnen eine Warnung anzeigt. Das ist erwartet. Folge den Schritten für dein System:

### Windows

1. Lade [Windows](https://github.com/USER/REPO/releases/latest/download/CoBalance.exe) herunter
2. Doppelklicke auf die `.exe`. Falls "_Windows protected your PC_" erscheint, klicke auf **More Info → Run anyway**.

### macOS

1. Lade [macOS](https://github.com/USER/REPO/releases/latest/download/CoBalance.dmg) herunter
2. Per Doppelklick öffnen wird wahrscheinlich mit der Meldung abgelehnt, dass der Entwickler nicht verifiziert werden kann. Stattdessen:
    1. **Rechtsklick** auf die App → **Öffnen** → im Dialog erneut **Öffnen** klicken.
    2. Alternativ: **Systemeinstellungen → Datenschutz & Sicherheit**, nach unten scrollen zur Meldung über die blockierte App → **Trotzdem öffnen**.

### Linux

1. Lade [Linux (AppImage)](https://github.com/USER/REPO/releases/latest/download/CoBalance-x86_64.AppImage) herunter
2. Mache die Datei ausführbar (Dateimanager → Eigenschaften → Berechtigungen → "Ausführen erlauben", oder im Terminal):

```sh
chmod +x CoBalance-x86_64.AppImage
```

3. Starte die Anwendung.


---

## Schritt 4 – Überprüfen, ob alles funktioniert

Dies ist der eigentliche Checkpoint: Unity erkennt das Plugin **und** das Tool kann die Projektdatei öffnen.

1. **In Unity:** Prüfe, ob ein **CoBalance**-Eintrag in der Unity-Menüleiste vorhanden ist.
2. Suche die Datei **`project.cb`** im Ordner **`CoBalance/`** deines Projekts (sie wurde beim Installieren des Plugins automatisch angelegt).
3. **Im Balancing Tool:** Öffne die Datei über **Project → Open** (`Strg+O`).

> ✅ **Einrichtung abgeschlossen:** Die `project.cb`-Datei öffnet sich im Balancing Tool und zeigt die Parameter-Ansicht. Wenn du hier angelangt bist, ist deine Toolchain bereit — weiter geht es mit [Erste Schritte](getting-started.md).
