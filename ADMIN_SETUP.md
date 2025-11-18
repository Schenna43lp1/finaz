# Administrator Setup

## Übersicht

Aus Sicherheitsgründen können sich Benutzer nicht selbst registrieren. Nur Administratoren können neue Benutzer erstellen.

## Erste Schritte

### 1. Datenbank aktualisieren

Wenn Sie eine bestehende Installation haben, müssen Sie die Datenbank migrieren:

```bash
mysql -u <db_user> -p <db_name> < migrate_add_admin.sql
```

### 2. Ersten Admin-Benutzer erstellen

Verwenden Sie das bereitgestellte Script, um den ersten Admin-Benutzer zu erstellen:

```bash
python create_admin.py
```

Das Script führt Sie interaktiv durch den Prozess:
- Benutzername eingeben
- E-Mail (optional) eingeben
- Passwort eingeben (mindestens 6 Zeichen)
- Passwort bestätigen

Der erstellte Benutzer erhält automatisch Administrator-Rechte.

### 3. Anmelden und weitere Benutzer erstellen

1. Starten Sie die Anwendung:
   ```bash
   python app.py
   ```

2. Melden Sie sich mit dem Admin-Benutzer an

3. Klicken Sie im Menü auf "Benutzer" (nur für Admins sichtbar)

4. Klicken Sie auf "➕ Neuer Benutzer", um weitere Benutzer zu erstellen

## Benutzerrollen

### Administrator
- Kann neue Benutzer erstellen
- Kann Benutzer mit oder ohne Admin-Rechte erstellen
- Hat Zugriff auf alle Funktionen der Anwendung
- Sieht den "Benutzer"-Menüpunkt

### Normaler Benutzer
- Kann sich anmelden
- Hat Zugriff auf alle Finanzfunktionen (Konten, Transaktionen, etc.)
- Kann keine neuen Benutzer erstellen
- Sieht den "Benutzer"-Menüpunkt nicht

## Sicherheitshinweise

1. **Schützen Sie Admin-Zugangsdaten**: Admin-Konten haben erweiterte Rechte
2. **Erstellen Sie nicht zu viele Admins**: Vergeben Sie Admin-Rechte nur an vertrauenswürdige Personen
3. **Verwenden Sie sichere Passwörter**: Mindestens 6 Zeichen (empfohlen: 12+ Zeichen mit Zahlen und Sonderzeichen)

## Problemlösung

### "Fehler bei der Datenbankverbindung"
- Stellen Sie sicher, dass die Datenbank läuft
- Überprüfen Sie die `.env` Datei mit den korrekten Zugangsdaten
- Stellen Sie sicher, dass das Schema importiert wurde

### "Benutzername existiert bereits"
- Wählen Sie einen anderen Benutzernamen
- Wenn Sie einen bestehenden Benutzer zu einem Admin machen möchten:
  ```sql
  UPDATE users SET is_admin = TRUE WHERE username = 'benutzername';
  ```

### Kein Admin-Benutzer vorhanden
Wenn Sie versehentlich alle Admin-Benutzer gelöscht haben oder keiner Admin-Rechte hat:

```sql
-- Setzen Sie einen bestehenden Benutzer als Admin
UPDATE users SET is_admin = TRUE WHERE id = 1;
```

Oder verwenden Sie das `create_admin.py` Script, um einen neuen Admin zu erstellen.
