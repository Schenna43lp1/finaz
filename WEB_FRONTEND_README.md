# Web Frontend für Finanzverwaltungstool

## Überblick

Das Finanzverwaltungstool verfügt jetzt über ein modernes, benutzerfreundliches Web-Frontend, das mit Flask entwickelt wurde. Das Web-Interface bietet dieselben Funktionen wie die CLI-Version, jedoch mit einer intuitiven grafischen Benutzeroberfläche.

## Features

### 📊 Dashboard
- Übersicht über alle Konten und deren Salden
- Monatliche Zusammenfassung (Einnahmen, Ausgaben, Saldo)
- Anzeige der letzten Transaktionen
- Schnellzugriff auf wichtige Funktionen

### 🏦 Kontenverwaltung
- Alle Konten anzeigen
- Neue Konten erstellen (Girokonto, Sparkonto, Kreditkarte, Bargeld, etc.)
- Konten löschen
- Kontostand in Echtzeit

### 💳 Transaktionsverwaltung
- Alle Transaktionen anzeigen
- Nach Konto filtern
- Neue Transaktionen hinzufügen (Einnahmen/Ausgaben)
- Automatische Kategoriezuordnung
- Datumsauswahl

### 🏷️ Kategorien
- Übersicht aller Einnahme-Kategorien
- Übersicht aller Ausgabe-Kategorien
- Vordefinierte Kategorien verfügbar

### 💰 Budgetverwaltung
- Aktive Budgets anzeigen
- Neue Budgets erstellen
- Zeitraumbasierte Budget-Planung

### 📈 Berichte
- Monatliche Finanzberichte
- Zeitraumauswahl (Jahr/Monat)
- Detaillierte Transaktionslisten
- Einnahmen/Ausgaben-Zusammenfassung

## Installation & Start

### Voraussetzungen
- Python 3.7 oder höher
- MariaDB Server (installiert und konfiguriert)
- Alle Python-Abhängigkeiten installiert

### Schritt 1: Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

Die `requirements.txt` enthält jetzt auch Flask:
- Flask==3.0.0
- mysql-connector-python>=9.1.0
- tabulate==0.9.0
- python-dotenv==1.0.0

### Schritt 2: Datenbank einrichten

Stellen Sie sicher, dass die MariaDB-Datenbank eingerichtet ist und die `.env` Datei korrekt konfiguriert ist:

```bash
# .env Datei erstellen
cp .env.example .env

# .env bearbeiten und Datenbankverbindung konfigurieren
nano .env
```

### Schritt 3: Web-Server starten

```bash
python app.py
```

Die Anwendung ist dann unter `http://localhost:5000` erreichbar.

#### Alternative: Mit eigener Host/Port-Konfiguration

Sie können den Server auch mit benutzerdefinierten Einstellungen starten:

```python
# In app.py am Ende ändern:
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
```

## Produktions-Deployment

Für den Produktionseinsatz sollten Sie einen WSGI-Server wie Gunicorn verwenden:

### Mit Gunicorn

```bash
# Gunicorn installieren
pip install gunicorn

# Server starten
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Mit uWSGI

```bash
# uWSGI installieren
pip install uwsgi

# Server starten
uwsgi --http 0.0.0.0:5000 --wsgi-file app.py --callable app --processes 4
```

### Wichtige Sicherheitshinweise für Produktion

1. **Secret Key ändern**: Setzen Sie einen sicheren Secret Key als Umgebungsvariable:
   ```python
   import os
   app.secret_key = os.environ.get('SECRET_KEY', 'fallback-secret-key')
   ```

2. **Debug-Modus deaktivieren**:
   ```python
   app.run(debug=False)
   ```

3. **HTTPS verwenden**: Nutzen Sie einen Reverse Proxy (nginx/Apache) mit SSL/TLS

4. **Datenbankverbindung sichern**: Verwenden Sie sichere Passwörter und beschränken Sie Datenbankzugriffe

## Projektstruktur

```
finaz/
├── app.py                      # Flask-Anwendung (Hauptdatei)
├── finaz.py                    # CLI-Anwendung (weiterhin verfügbar)
├── database.py                 # Datenbankverbindung
├── models.py                   # Datenmodelle
├── templates/                  # HTML-Templates
│   ├── base.html              # Basis-Template mit Navigation
│   ├── index.html             # Dashboard
│   ├── accounts.html          # Kontenübersicht
│   ├── create_account.html    # Konto erstellen
│   ├── transactions.html      # Transaktionsübersicht
│   ├── create_transaction.html# Transaktion erstellen
│   ├── categories.html        # Kategorienübersicht
│   ├── budgets.html          # Budgetübersicht
│   ├── create_budget.html    # Budget erstellen
│   ├── reports.html          # Monatsberichte
│   └── error.html            # Fehlerseite
├── static/                    # Statische Dateien
│   └── css/
│       └── style.css         # Stylesheet
├── requirements.txt          # Python-Abhängigkeiten
└── .env                      # Konfiguration (nicht im Git)
```

## Design & Benutzeroberfläche

### Farbschema
- **Primärfarbe**: Violett-Blau Gradient (#667eea - #764ba2)
- **Erfolg**: Grün (#28a745)
- **Fehler**: Rot (#dc3545)
- **Neutral**: Grau (#6c757d)

### Responsive Design
Das Web-Frontend ist vollständig responsive und funktioniert auf:
- Desktop-Computern
- Tablets
- Smartphones

### Navigation
Einfache Navigation durch eine persistente Navigationsleiste:
- Dashboard
- Konten
- Transaktionen
- Kategorien
- Budgets
- Berichte

## API-Endpunkte

### Hauptrouten
- `GET /` - Dashboard
- `GET /accounts` - Kontenübersicht
- `GET /accounts/create` - Formular für neues Konto
- `POST /accounts/create` - Konto erstellen
- `POST /accounts/delete/<id>` - Konto löschen
- `GET /transactions` - Transaktionsübersicht
- `GET /transactions?account_id=<id>` - Gefilterte Transaktionen
- `GET /transactions/create` - Formular für neue Transaktion
- `POST /transactions/create` - Transaktion erstellen
- `GET /categories` - Kategorienübersicht
- `GET /budgets` - Budgetübersicht
- `GET /budgets/create` - Formular für neues Budget
- `POST /budgets/create` - Budget erstellen
- `GET /reports` - Monatsberichte
- `GET /reports?year=<year>&month=<month>` - Bericht für bestimmten Monat

### API-Endpunkte (JSON)
- `GET /api/categories/<type>` - Kategorien nach Typ (Einnahme/Ausgabe)

## Tests

Tests für das Web-Frontend ausführen:

```bash
python test_web_frontend.py
```

Die Tests prüfen:
- Flask-Installation
- App-Import und Konfiguration
- Existenz aller Routen
- Vorhandensein aller Templates
- Statische Dateien
- HTTP-Responses

## Fehlerbehebung

### Problem: "Fehler bei der Datenbankverbindung"
**Lösung**: 
- Überprüfen Sie, ob MariaDB läuft: `sudo systemctl status mariadb`
- Prüfen Sie die `.env` Datei auf korrekte Zugangsdaten
- Testen Sie die Verbindung: `mysql -u finaz_user -p`

### Problem: "Port bereits in Verwendung"
**Lösung**: 
- Ändern Sie den Port in `app.py`: `app.run(port=8080)`
- Oder beenden Sie die Anwendung auf Port 5000

### Problem: "Template not found"
**Lösung**: 
- Stellen Sie sicher, dass der `templates/` Ordner existiert
- Überprüfen Sie die Dateinamen (Groß-/Kleinschreibung beachten)

### Problem: "Static files not loading"
**Lösung**: 
- Prüfen Sie, ob der `static/css/` Ordner existiert
- Leeren Sie den Browser-Cache
- Überprüfen Sie die URL-Pfade in den Templates

## Vorteile gegenüber CLI

1. **Benutzerfreundlichkeit**: Intuitive grafische Oberfläche
2. **Echtzeit-Updates**: Sofortige Anzeige von Änderungen
3. **Mehrbenutzerfähigkeit**: Kann von mehreren Benutzern gleichzeitig genutzt werden
4. **Plattformunabhängig**: Funktioniert in jedem modernen Browser
5. **Visuelle Darstellung**: Bessere Übersicht durch Cards und Tabellen
6. **Responsive**: Funktioniert auf Desktop und Mobilgeräten

## CLI weiterhin verfügbar

Die ursprüngliche CLI-Anwendung (`finaz.py`) ist weiterhin verfügbar und kann parallel zum Web-Frontend verwendet werden:

```bash
python finaz.py
```

## Weiterentwicklung

Mögliche zukünftige Erweiterungen:
- Grafische Charts und Diagramme (Chart.js)
- Export-Funktionen (PDF, CSV, Excel)
- Benutzerverwaltung und Authentifizierung
- Mehrsprachigkeit (i18n)
- Dark Mode
- Benachrichtigungen bei Budget-Überschreitungen
- Recurring Transactions (wiederkehrende Transaktionen)
- Dashboard-Widgets anpassbar machen
- Mobile App (React Native / Flutter)

## Support

Bei Fragen oder Problemen:
1. Überprüfen Sie die Dokumentation
2. Führen Sie die Tests aus
3. Prüfen Sie die Logs
4. Erstellen Sie ein Issue auf GitHub

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz.

---

**Entwickelt mit ❤️ für eine bessere Finanzverwaltung**
