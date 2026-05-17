# Überblick

Das **Balancing Framework** ist ein Unity-Plugin zur Vorbereitung und Unterstützung des Game Balancings.

Es ist Teil eines Gesamtsystems, das aus zwei Komponenten besteht:

- dem **Unity-Plugin**
- dem **externen Balancing Tool**

Das Unity-Plugin wird verwendet, um balancerelevante Daten innerhalb eines Unity-Projekts zu kennzeichnen und zu erfassen.  
Dazu gehören insbesondere Parameter, die angepasst werden sollen, sowie Werte, die während des Spiels geloggt und später ausgewertet werden können.

## Grundidee

Damit das Framework mit Spielinhalten arbeiten kann, müssen relevante Objekte und Parameter im Projekt entsprechend markiert werden.

Hierfür stehen aktuell zwei zentrale Attribute zur Verfügung:

- `BalanceParameter`  
  Markiert Werte, die vom Framework als Balancing-Parameter erkannt und verwaltet werden sollen.

- `BalanceLog`  
  Markiert Werte, die während der Laufzeit geloggt werden, damit sie später im externen Tool ausgewertet werden können.

## Balancierbare Entitäten

Damit das Framework Parameter erkennen kann, müssen Objekte im Projekt als **balancierbare Entitäten** definiert werden.

Je nach Objekttyp erfolgt dies auf unterschiedliche Weise.

### GameObjects und Prefabs

Für GameObjects und Prefabs wird das Component `EntityDescriptorComponent` verwendet.

Dieses Component enthält grundlegende Informationen über die Entität:

- eine eindeutige **ID**
- einen **Display Name**
- eine **Kategorie**

Das Component muss dem Root-Objekt eines Prefabs oder GameObjects hinzugefügt werden.

### ScriptableObjects

ScriptableObjects können ebenfalls als balancierbare Entitäten verwendet werden.

Dafür muss das ScriptableObject das Interface `IBalanceableObject` implementieren.

## Parametererkennung

Das Framework durchsucht die markierten Objekte nach Feldern, die mit `BalanceParameter` versehen wurden.  
Aktuell werden dabei vor allem Parameter vom Typ `int` und `float` unterstützt.

Zusätzlich ist eine Erweiterung über eigene Parametertypen möglich.  
Diese Funktion ist für fortgeschrittene Anwendungsfälle gedacht und wird separat beschrieben.

## Logging

Über das Attribut `BalanceLog` können Werte für das Laufzeit-Logging markiert werden.  
Diese Daten können später im externen Balancing Tool analysiert werden.