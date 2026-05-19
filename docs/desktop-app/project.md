# Projekt

Ein CoBalance-Projekt ist eine `.cb`-Datei, die im Unity-Projekt automatisch beim ersten Start angelegt wird. Sie enthält Pfad- und Konfigurationsinformationen, die die Desktop App benötigt, um mit dem Unity-Projekt zu arbeiten.

---

## Projekt öffnen

Über **Project → Open** (`Ctrl+O`) öffnet sich ein Dateidialog, in dem eine `.cb`-Datei ausgewählt werden kann. Die App merkt sich das zuletzt geöffnete Projekt und springt beim nächsten Öffnen automatisch in das richtige Verzeichnis.

Nach dem Öffnen eines Projekts werden automatisch erkannt:

- alle **Balance-Snapshots** im `CoBalance/Balances/`-Verzeichnis
- alle **Unity-Szenen** des Projekts
- alle **Log-Dateien** im `CoBalance/Logs/`-Verzeichnis

---

## Balance-Snapshot wechseln

In der Statusleiste am unteren Rand zeigt ein Dropdown-Menü den aktuell aktiven Balance-Snapshot. Darüber kann zwischen allen verfügbaren Snapshots gewechselt werden — die Parameteransicht aktualisiert sich automatisch.

---

## Speichern

**Project → Save** (`Ctrl+S`) speichert den aktuellen Balance-Snapshot sowie etwaige Änderungen an Log-Gruppen.

**Project → Save Balance As** (`Ctrl+Shift+S`) speichert die aktuell geladene Balance unter einem neuen Dateinamen als `.json`-Datei.

Ist **Auto Save** in den Einstellungen aktiviert, werden alle Änderungen sofort automatisch gespeichert und der manuelle Save-Button ist deaktiviert.

Beim Schließen der App mit ungespeicherten Änderungen erscheint ein Bestätigungsdialog.

---

## Externe Änderungen

Wird die aktuell geöffnete Balance-Datei von außen verändert (z. B. durch eine abgeschlossene Simulation), erkennt die App das automatisch. Ein Dialog fragt, ob die Datei neu geladen werden soll.
