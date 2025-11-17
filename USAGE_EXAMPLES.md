# Finanzverwaltungstool - Verwendungsbeispiele

## Schnellstart

Nach der Installation können Sie das Tool mit folgendem Befehl starten:

```bash
python finaz.py
```

## Beispiel-Szenario: Monatliche Finanzverwaltung

### 1. Erstes Konto erstellen

```
Hauptmenü → 1 (Konten verwalten) → 2 (Neues Konto erstellen)

Kontoname: Girokonto Hauptkonto
Kontotyp: 1 (Girokonto)
Anfangssaldo: 2500.00
Beschreibung: Mein Hauptkonto für alltägliche Ausgaben
```

### 2. Zweites Konto hinzufügen

```
Kontenverwaltung → 2 (Neues Konto erstellen)

Kontoname: Sparkonto
Kontotyp: 2 (Sparkonto)
Anfangssaldo: 10000.00
Beschreibung: Langfristige Rücklagen
```

### 3. Einnahme hinzufügen (Gehalt)

```
Hauptmenü → 2 (Neue Transaktion hinzufügen)

Konto-ID: 1 (Girokonto Hauptkonto)
Transaktionstyp: 1 (Einnahme)
Kategorie-ID: 1 (Gehalt)
Betrag: 3500.00
Beschreibung: Monatsgehalt November
Datum: [Enter für heute]
```

Ergebnis: Das Konto wird automatisch auf 6000.00 EUR aktualisiert (2500 + 3500)

### 4. Ausgaben erfassen

```
Hauptmenü → 2 (Neue Transaktion hinzufügen)

# Miete
Konto-ID: 1
Transaktionstyp: 2 (Ausgabe)
Kategorie-ID: 5 (Miete)
Betrag: 950.00
Beschreibung: Monatsmiete November

# Lebensmittel
Konto-ID: 1
Transaktionstyp: 2 (Ausgabe)
Kategorie-ID: 4 (Lebensmittel)
Betrag: 350.00
Beschreibung: Wocheneinkauf

# Transport
Konto-ID: 1
Transaktionstyp: 2 (Ausgabe)
Kategorie-ID: 6 (Transport)
Betrag: 89.00
Beschreibung: Monatsticket ÖPNV
```

### 5. Budget erstellen

```
Hauptmenü → 5 (Budget verwalten) → 2 (Neues Budget erstellen)

Kategorie-ID: 4 (Lebensmittel)
Budget-Betrag: 400.00
Startdatum: 2024-11-01
Enddatum: 2024-11-30
```

### 6. Finanzübersicht anzeigen

```
Hauptmenü → 6 (Finanzübersicht)

Ausgabe:
============================================================
                   FINANZÜBERSICHT
============================================================

KONTENSTAND:
  Girokonto Hauptkonto: 4611.00 EUR
  Sparkonto: 10000.00 EUR

  GESAMT: 14611.00 EUR

AKTUELLER MONAT (November 2024):
  Einnahmen:  +3500.00 EUR
  Ausgaben:   -1389.00 EUR
  Saldo:       2111.00 EUR
```

### 7. Transaktionshistorie anzeigen

```
Hauptmenü → 3 (Transaktionen anzeigen) → 1 (Alle Transaktionen)

Ausgabe:
+----+------------+---------------------+---------------+----------+----------+-----------------+
| ID | Datum      | Konto               | Kategorie     | Typ      | Betrag   | Beschreibung    |
+====+============+=====================+===============+==========+==========+=================+
| 4  | 2024-11-17 | Girokonto Hauptko.. | Transport     | Ausgabe  | 89.00    | Monatsticket... |
| 3  | 2024-11-17 | Girokonto Hauptko.. | Lebensmittel  | Ausgabe  | 350.00   | Wocheneinkauf   |
| 2  | 2024-11-17 | Girokonto Hauptko.. | Miete         | Ausgabe  | 950.00   | Monatsmiete...  |
| 1  | 2024-11-17 | Girokonto Hauptko.. | Gehalt        | Einnahme | 3500.00  | Monatsgehalt... |
+----+------------+---------------------+---------------+----------+----------+-----------------+
```

### 8. Monatsreport erstellen

```
Hauptmenü → 7 (Monatsreport)

Jahr (YYYY): 2024
Monat (1-12): 11

Ausgabe:
============================================================
           MONATSREPORT 11/2024
============================================================
Zeitraum: 2024-11-01 bis 2024-11-30

Einnahmen:  +3500.00 EUR
Ausgaben:   -1389.00 EUR
============================================================
Saldo:       2111.00 EUR
============================================================
```

## Erweiterte Verwendung

### Kategorien anzeigen

```
Hauptmenü → 4 (Kategorien verwalten)
```

Zeigt alle verfügbaren Kategorien für Einnahmen und Ausgaben an.

### Budget-Überwachung

```
Hauptmenü → 5 (Budget verwalten) → 1 (Aktuelle Budgets anzeigen)
```

Zeigt alle aktiven Budgets und deren Zeiträume an.

### Kontospezifische Transaktionen

```
Hauptmenü → 3 (Transaktionen anzeigen) → 2 (Transaktionen nach Konto)
Konto-ID: 1
```

Zeigt nur Transaktionen für das ausgewählte Konto an.

## Tipps für die tägliche Nutzung

1. **Regelmäßige Eingabe**: Erfassen Sie Transaktionen täglich oder wöchentlich für bessere Übersicht
2. **Kategorisierung**: Nutzen Sie konsistente Kategorien für bessere Auswertungen
3. **Budgets**: Setzen Sie realistische monatliche Budgets für Hauptausgabenkategorien
4. **Monatsreports**: Erstellen Sie am Monatsende einen Report zur Finanzplanung
5. **Mehrere Konten**: Verwalten Sie verschiedene Konten (Girokonto, Sparkonto, etc.) parallel

## Datenintegrität

Das Tool kümmert sich automatisch um:

- ✓ Aktualisierung der Kontostände bei Transaktionen
- ✓ Verhinderung von Duplikaten bei Kontonamen
- ✓ Konsistente Datumsspeicherung
- ✓ Transaktionshistorie mit Zeitstempeln
- ✓ Währungsunterstützung

## Datensicherung

Wichtig: Sichern Sie regelmäßig Ihre MariaDB-Datenbank:

```bash
# Backup erstellen
mysqldump -u finaz_user -p finaz_db > finaz_backup_$(date +%Y%m%d).sql

# Backup wiederherstellen
mysql -u finaz_user -p finaz_db < finaz_backup_20241117.sql
```

## Nächste Schritte

- Passen Sie die vordefinierten Kategorien an Ihre Bedürfnisse an
- Erstellen Sie Budgets für Ihre wichtigsten Ausgabenkategorien
- Erfassen Sie regelmäßig Ihre Transaktionen
- Nutzen Sie die Berichte zur Finanzplanung
