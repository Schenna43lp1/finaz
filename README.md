# Finanzverwaltungstool mit MariaDB Backend

Ein umfassendes Finanzverwaltungstool (Financial Management Tool) mit MariaDB als Backend-Datenbank. Dieses Tool ermöglicht die Verwaltung von Konten, Transaktionen, Kategorien und Budgets über eine benutzerfreundliche **Web-Oberfläche** oder **Kommandozeilenschnittstelle**.

## Funktionen

- ✓ **Web-Frontend**: Moderne, responsive Web-Oberfläche mit Flask
- ✓ **CLI-Interface**: Traditionelle Kommandozeilenschnittstelle (weiterhin verfügbar)
- ✓ **Kontenverwaltung**: Erstellen und verwalten Sie verschiedene Konten (Girokonto, Sparkonto, Kreditkarte, Bargeld)
- ✓ **Transaktionsverwaltung**: Erfassen Sie Einnahmen und Ausgaben mit automatischer Saldo-Aktualisierung
- ✓ **Kategorisierung**: Organisieren Sie Transaktionen in vordefinierte oder benutzerdefinierte Kategorien
- ✓ **Budget-Tracking**: Erstellen und überwachen Sie Budgets für verschiedene Ausgabenkategorien
- ✓ **Finanzberichte**: Zeigen Sie monatliche Reports und Finanzübersichten an
- ✓ **Multi-Currency Support**: Unterstützung für verschiedene Währungen (Standard: EUR)
- ✓ **Dashboard**: Übersichtliche Darstellung aller wichtigen Finanzdaten

## Technologie-Stack

- **Backend-Datenbank**: MariaDB
- **Programmiersprache**: Python 3
- **Web-Framework**: Flask 3.0
- **Datenbank-Connector**: mysql-connector-python
- **CLI-Interface**: tabulate für formatierte Ausgaben
- **Frontend**: HTML5, CSS3, JavaScript

## Voraussetzungen

- Python 3.7 oder höher
- MariaDB Server 10.3 oder höher
- pip (Python Package Manager)

**ODER für Docker:**
- Docker Engine (Version 20.10 oder höher)
- Docker Compose (Version 2.0 oder höher)

## Installation

### Option A: Mit Docker (Empfohlen für schnellen Start)

Mit Docker können Sie die Anwendung inklusive Datenbank mit wenigen Befehlen starten:

```bash
# 1. Umgebungsvariablen konfigurieren
cp .env.example .env

# 2. Container starten
docker compose up -d

# 3. Anwendung öffnen
# Öffnen Sie http://localhost:5000 im Browser
```

Fertig! Die Anwendung läuft nun mit einer vollständig konfigurierten MariaDB-Datenbank.

> **Hinweis**: Für detaillierte Docker-Anweisungen siehe [DOCKER_README.md](DOCKER_README.md)

### Option B: Manuelle Installation

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

### Option 1: Web-Frontend (empfohlen)

Starten Sie den Web-Server:

```bash
python app.py
```

Öffnen Sie dann Ihren Browser und navigieren Sie zu: **http://localhost:5000**

Das Web-Frontend bietet:
- 📊 **Dashboard** mit Übersicht aller Konten und aktuellen Monatsdaten
- 🏦 **Kontenverwaltung** - Konten erstellen, anzeigen und löschen
- 💳 **Transaktionen** - Einnahmen und Ausgaben erfassen und filtern
- 🏷️ **Kategorien** - Übersicht aller Kategorien
- 💰 **Budgets** - Budget erstellen und verwalten
- 📈 **Berichte** - Monatliche Finanzberichte mit Filterung

> **Hinweis**: Für detaillierte Informationen zum Web-Frontend siehe [WEB_FRONTEND_README.md](WEB_FRONTEND_README.md)

### Option 2: CLI (Kommandozeile)

Starten Sie die CLI-Version:

```bash
python finaz.py
```

### CLI-Hauptmenü

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

### Beispiel-Workflow (CLI)

1. **Konto erstellen**: Wählen Sie Option 1 → 2, um ein neues Konto zu erstellen
2. **Transaktion hinzufügen**: Wählen Sie Option 2, um Einnahmen oder Ausgaben zu erfassen
3. **Übersicht anzeigen**: Wählen Sie Option 6, um Ihre aktuelle Finanzsituation zu sehen
4. **Monatsreport**: Wählen Sie Option 7, um einen detaillierten Monatsbericht zu erstellen

### Beispiel-Workflow (Web)

1. Öffnen Sie **Dashboard** für eine Übersicht
2. Klicken Sie auf **"+ Neues Konto"** um ein Konto zu erstellen
3. Nutzen Sie **"+ Neue Transaktion"** um Einnahmen/Ausgaben zu erfassen
4. Besuchen Sie **Berichte** für monatliche Finanzauswertungen

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
├── app.py                      # Web-Anwendung (Flask)
├── finaz.py                    # CLI-Anwendung
├── database.py                 # Datenbankverbindung und -operationen
├── models.py                   # Datenmodelle (Account, Transaction, Category, Budget)
├── database_schema.sql         # SQL-Schema für MariaDB
├── templates/                  # HTML-Templates für Web-Frontend
│   ├── base.html              # Basis-Template
│   ├── index.html             # Dashboard
│   ├── accounts.html          # Kontenübersicht
│   ├── transactions.html      # Transaktionsübersicht
│   ├── categories.html        # Kategorienübersicht
│   ├── budgets.html          # Budgetübersicht
│   ├── reports.html          # Berichte
│   └── ...                    # Weitere Templates
├── static/                    # Statische Dateien (CSS, JS)
│   └── css/
│       └── style.css         # Stylesheet
├── requirements.txt          # Python-Abhängigkeiten
├── .env.example             # Beispiel-Konfigurationsdatei
├── .gitignore               # Git-Ignore-Regeln
├── README.md                # Diese Datei
└── WEB_FRONTEND_README.md   # Detaillierte Web-Frontend-Dokumentation
```

## Sicherheitshinweise

- ⚠️ Speichern Sie niemals Passwörter im Quellcode
- ⚠️ Verwenden Sie starke Passwörter für den Datenbankbenutzer
- ⚠️ Die `.env` Datei ist in `.gitignore` enthalten und wird nicht versioniert
- ⚠️ Für Produktionsumgebungen sollten zusätzliche Sicherheitsmaßnahmen implementiert werden

## Weiterentwicklung

Mögliche zukünftige Erweiterungen:

- ✅ ~~Web-Interface mit Flask~~ (Implementiert!)
- Grafische Darstellung von Finanzberichten (Charts/Diagramme)
- Import/Export von Transaktionen (CSV, Excel)
- Multi-User-Unterstützung mit Authentifizierung
- Automatische Backup-Funktionen
- Mobile App-Integration
- Dark Mode für Web-Frontend
- Benachrichtigungen und Alerts

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
