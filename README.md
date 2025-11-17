# Finanzverwaltungstool mit MariaDB Backend

Ein umfassendes Finanzverwaltungstool (Financial Management Tool) mit MariaDB als Backend-Datenbank. Dieses Tool ermöglicht die Verwaltung von Konten, Transaktionen, Kategorien und Budgets über eine benutzerfreundliche Kommandozeilenschnittstelle.

## Funktionen

- ✓ **Kontenverwaltung**: Erstellen und verwalten Sie verschiedene Konten (Girokonto, Sparkonto, Kreditkarte, Bargeld)
- ✓ **Transaktionsverwaltung**: Erfassen Sie Einnahmen und Ausgaben mit automatischer Saldo-Aktualisierung
- ✓ **Kategorisierung**: Organisieren Sie Transaktionen in vordefinierte oder benutzerdefinierte Kategorien
- ✓ **Budget-Tracking**: Erstellen und überwachen Sie Budgets für verschiedene Ausgabenkategorien
- ✓ **Finanzberichte**: Zeigen Sie monatliche Reports und Finanzübersichten an
- ✓ **Multi-Currency Support**: Unterstützung für verschiedene Währungen (Standard: EUR)

## Technologie-Stack

- **Backend-Datenbank**: MariaDB
- **Programmiersprache**: Python 3
- **Datenbank-Connector**: mysql-connector-python
- **CLI-Interface**: tabulate für formatierte Ausgaben

## Voraussetzungen

- Python 3.7 oder höher
- MariaDB Server 10.3 oder höher
- pip (Python Package Manager)

## Installation

### 1. MariaDB Server installieren

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install mariadb-server
sudo systemctl start mariadb
sudo systemctl enable mariadb
```

**macOS (mit Homebrew):**
```bash
brew install mariadb
brew services start mariadb
```

**Windows:**
Laden Sie den MariaDB Installer von [mariadb.org](https://mariadb.org/download/) herunter.

### 2. Datenbank und Benutzer einrichten

```bash
sudo mysql
```

Führen Sie in der MySQL/MariaDB Console aus:
```sql
CREATE DATABASE finaz_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'finaz_user'@'localhost' IDENTIFIED BY 'ihr_sicheres_passwort';
GRANT ALL PRIVILEGES ON finaz_db.* TO 'finaz_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 3. Datenbank-Schema importieren

```bash
mysql -u finaz_user -p finaz_db < database_schema.sql
```

### 4. Python-Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

### 5. Umgebungsvariablen konfigurieren

Kopieren Sie die Beispiel-Konfiguration:
```bash
cp .env.example .env
```

Bearbeiten Sie die `.env` Datei und passen Sie die Datenbankverbindung an:
```
DB_HOST=localhost
DB_PORT=3306
DB_USER=finaz_user
DB_PASSWORD=ihr_sicheres_passwort
DB_NAME=finaz_db
```

## Verwendung

Starten Sie das Finanzverwaltungstool:

```bash
python finaz.py
```

### Hauptmenü

Nach dem Start sehen Sie das Hauptmenü:

```
============================================================
        FINANZVERWALTUNGSTOOL - HAUPTMENÜ
============================================================
1.  Konten verwalten
2.  Neue Transaktion hinzufügen
3.  Transaktionen anzeigen
4.  Kategorien verwalten
5.  Budget verwalten
6.  Finanzübersicht
7.  Monatsreport
0.  Beenden
============================================================
```

### Beispiel-Workflow

1. **Konto erstellen**: Wählen Sie Option 1 → 2, um ein neues Konto zu erstellen
2. **Transaktion hinzufügen**: Wählen Sie Option 2, um Einnahmen oder Ausgaben zu erfassen
3. **Übersicht anzeigen**: Wählen Sie Option 6, um Ihre aktuelle Finanzsituation zu sehen
4. **Monatsreport**: Wählen Sie Option 7, um einen detaillierten Monatsbericht zu erstellen

## Datenbank-Schema

### Tabellen

- **accounts**: Speichert Kontoinformationen (Name, Typ, Saldo, Währung)
- **categories**: Definiert Kategorien für Einnahmen und Ausgaben
- **transactions**: Erfasst alle finanziellen Transaktionen
- **budgets**: Verwaltet Budgets für verschiedene Kategorien

### Vordefinierte Kategorien

**Einnahmen:**
- Gehalt
- Bonus
- Investitionen

**Ausgaben:**
- Lebensmittel
- Miete
- Transport
- Unterhaltung
- Gesundheit
- Versicherungen
- Sonstiges

## Projektstruktur

```
finaz/
├── finaz.py              # Hauptanwendung (CLI)
├── database.py           # Datenbankverbindung und -operationen
├── models.py             # Datenmodelle (Account, Transaction, Category, Budget)
├── database_schema.sql   # SQL-Schema für MariaDB
├── requirements.txt      # Python-Abhängigkeiten
├── .env.example         # Beispiel-Konfigurationsdatei
├── .gitignore           # Git-Ignore-Regeln
└── README.md            # Diese Datei
```

## Sicherheitshinweise

- ⚠️ Speichern Sie niemals Passwörter im Quellcode
- ⚠️ Verwenden Sie starke Passwörter für den Datenbankbenutzer
- ⚠️ Die `.env` Datei ist in `.gitignore` enthalten und wird nicht versioniert
- ⚠️ Für Produktionsumgebungen sollten zusätzliche Sicherheitsmaßnahmen implementiert werden

## Weiterentwicklung

Mögliche zukünftige Erweiterungen:

- Web-Interface mit Flask oder Django
- Grafische Darstellung von Finanzberichten
- Import/Export von Transaktionen (CSV, Excel)
- Multi-User-Unterstützung
- Automatische Backup-Funktionen
- Mobile App-Integration

## Fehlerbehebung

### Problem: "Fehler bei der Datenbankverbindung"
- Überprüfen Sie, ob MariaDB läuft: `sudo systemctl status mariadb`
- Prüfen Sie die Verbindungsdaten in der `.env` Datei
- Testen Sie die Verbindung: `mysql -u finaz_user -p`

### Problem: "Module not found"
- Installieren Sie die Abhängigkeiten neu: `pip install -r requirements.txt`
- Verwenden Sie ggf. ein virtuelles Environment: `python -m venv venv && source venv/bin/activate`

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz.

## Autor

Erstellt als Finanzverwaltungstool mit MariaDB Backend.
