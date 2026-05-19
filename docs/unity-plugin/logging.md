# Logging

Mit dem Attribut `BalanceLog` können Werte markiert werden, die während der Laufzeit erfasst und später im externen Balancing Tool ausgewertet werden sollen.

Das Logging ist vor allem dann nützlich, wenn nicht nur Balancing-Parameter angepasst, sondern auch tatsächliche Spieldaten analysiert werden sollen.

## BalanceLog verwenden

Um einen Wert zu loggen, wird das Attribut `BalanceLog` auf ein Feld gesetzt.

```csharp
[SerializeField, BalanceLog]
private int currentHealth;
```

Das Framework erkennt dieses Feld automatisch und nimmt es in das Laufzeit-Logging auf.
Optional kann ein eigener Schlüssel angegeben werden:

```csharp
[SerializeField, BalanceLog("player_health")]
private int currentHealth;
```

Wird kein eigener Schlüssel angegeben, verwendet das Framework standardmäßig den Feldnamen.

## Automatische Erkennung beim Szenenstart

Beim Start einer Szene durchsucht das Framework alle vorhandenen MonoBehaviour-Instanzen nach Feldern, die mit BalanceLog markiert wurden.

Das bedeutet:

- Objekte, die bereits beim Start der Szene existieren, werden automatisch erkannt
- ihre geloggten Felder werden automatisch registriert

In vielen einfachen Fällen ist daher keine weitere Konfiguration notwendig.

## Dynamisch erzeugte Objekte

Werden GameObjects oder Komponenten erst während der Laufzeit erzeugt, können ihre Log-Felder nicht automatisch beim initialen Szenenscan erkannt werden.

Für solche Fälle muss dem entsprechenden Objekt zusätzlich die Komponente `BalanceLogSource` hinzugefügt werden.

```csharp
public sealed class BalanceLogSource : MonoBehaviour
```

Diese Komponente sorgt dafür, dass das Objekt beim Logger registriert wird, sobald es aktiviert wird.

### Wann `BalanceLogSource` benötigt wird

`BalanceLogSource` wird benötigt, wenn:

- ein Objekt zur Laufzeit instanziiert wird
- ein Objekt mit `BalanceLog` nicht bereits beim Szenenstart vorhanden ist

`BalanceLogSource` ist in der Regel nicht notwendig, wenn das Objekt bereits von Anfang an in der Szene existiert.

### Beispiel

```csharp
public class Enemy : MonoBehaviour
{
    [SerializeField, BalanceLog]
    private int currentHealth;
}
```

Wenn dieses Objekt bereits beim Start der Szene vorhanden ist, wird `currentHealth` automatisch erkannt.

Wird das Objekt dagegen erst später zur Laufzeit erzeugt, sollte das GameObjekt zusätzlich `BalanceLogSource` als Komponente verweden.

---

## Manuelles Logging über GameStatLogger

Neben dem automatischen Attribut-Logging bietet der `GameStatLogger` drei öffentliche Methoden, um Werte gezielt und manuell ins Log zu schreiben.

Der Logger ist als Singleton implementiert und über `GameStatLogger.Instance` erreichbar.

---

### `LogGameStats()`

Schreibt einen Schnappschuss **aller** registrierten `[BalanceLog]`-Felder auf einmal ins Log — mit dem aktuellen `Time.fixedTime` als Zeitstempel.

Nützlich, wenn das zeitgesteuerte Logging deaktiviert ist und der Snapshot stattdessen an einem bestimmten Spielereignis ausgelöst werden soll (z. B. am Ende einer Runde).

```csharp
// Am Ende eines Kampfes alle registrierten Werte einmalig loggen
GameStatLogger.Instance.LogGameStats();
```

---

### `LogGameStat(string key, object value)`

Schreibt einen einzelnen Wert mit dem angegebenen Schlüssel ins Log. Als Zeitstempel wird automatisch `Time.fixedTime` verwendet.

```csharp
// Aktuellen Punktestand manuell loggen
GameStatLogger.Instance.LogGameStat("score", currentScore);

// Beliebige numerische Werte sind erlaubt
GameStatLogger.Instance.LogGameStat("enemies_defeated", enemyCount);
```

---

### `LogGameStat(float t, string key, object value)`

Wie die obige Methode, aber mit einem **manuell angegebenen Zeitstempel** `t`. Sinnvoll, wenn der Zeitpunkt des Ereignisses bekannt ist und exakt ins Log übernommen werden soll.

```csharp
// Zeitpunkt des Treffers mit einem eigenen Timestamp loggen
float hitTime = Time.fixedTime;
GameStatLogger.Instance.LogGameStat(hitTime, "hit_damage", damage);
```

---

## Hinweise

- `BalanceLog` kann auf Feldern verwendet werden, die zur Laufzeit beobachtet werden sollen
- Für dynamisch erzeugte Objekte ist `BalanceLogSource` erforderlich
- Doppelte Log-Schlüssel auf demselben Objekt sollten vermieden werden
- `LogGameStat` und `LogGameStats` schreiben unabhängig davon, ob zeitgesteuertes Logging aktiviert ist