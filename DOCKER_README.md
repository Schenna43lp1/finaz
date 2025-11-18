# Docker Setup für Finaz

Diese Anleitung beschreibt, wie Sie die Finaz-Anwendung mit Docker und Docker Compose ausführen.

## Voraussetzungen

- Docker Engine (Version 20.10 oder höher)
- Docker Compose (Version 2.0 oder höher)

### Docker installieren

**Ubuntu/Debian:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

**macOS:**
Installieren Sie [Docker Desktop für Mac](https://www.docker.com/products/docker-desktop)

**Windows:**
Installieren Sie [Docker Desktop für Windows](https://www.docker.com/products/docker-desktop)

## Schnellstart

1. **Repository klonen:**
   ```bash
   git clone <repository-url>
   cd finaz
   ```

2. **Umgebungsvariablen konfigurieren:**
   ```bash
   cp .env.example .env
   ```
   
   Bearbeiten Sie die `.env` Datei und passen Sie die Werte an (optional):
   ```env
   DB_USER=finaz_user
   DB_PASSWORD=ihr_sicheres_passwort
   DB_NAME=finaz_db
   DB_ROOT_PASSWORD=root_passwort
   SECRET_KEY=ihr-geheimer-schluessel
   ```

3. **Container starten:**
   ```bash
   docker compose up -d
   ```
   
   > **Hinweis:** Bei älteren Docker-Versionen verwenden Sie `docker-compose` (mit Bindestrich) statt `docker compose`

4. **Anwendung öffnen:**
   
   Öffnen Sie Ihren Browser und navigieren Sie zu: **http://localhost:5000**

## Docker-Services

Die Docker-Compose-Konfiguration startet zwei Services:

### 1. MariaDB Datenbank (`db`)
- **Image:** mariadb:10.11
- **Port:** 3306
- **Volume:** Persistent storage für Datenbankdaten
- **Initialisierung:** Automatische Schema-Erstellung beim ersten Start

### 2. Flask Web-Anwendung (`web`)
- **Build:** Aus lokalem Dockerfile
- **Port:** 5000
- **Abhängigkeit:** Wartet auf Datenbank-Bereitschaft

## Nützliche Befehle

### Container starten
```bash
docker compose up -d
```

### Container stoppen
```bash
docker compose down
```

### Container stoppen und Daten löschen
```bash
docker compose down -v
```

### Logs anzeigen
```bash
# Alle Logs
docker compose logs

# Nur Web-Anwendung
docker compose logs web

# Nur Datenbank
docker compose logs db

# Logs in Echtzeit verfolgen
docker compose logs -f
```

### Container-Status prüfen
```bash
docker compose ps
```

### Container neu starten
```bash
docker compose restart
```

### In Container-Shell einsteigen
```bash
# Web-Anwendung
docker compose exec web /bin/bash

# Datenbank
docker compose exec db /bin/bash
```

### Datenbank-Zugriff
```bash
docker compose exec db mysql -u finaz_user -p finaz_db
```

### Container neu bauen (nach Code-Änderungen)
```bash
docker compose build
docker compose up -d
```

> **Hinweis:** Bei Docker-Versionen vor 2.0 verwenden Sie `docker-compose` (mit Bindestrich) anstelle von `docker compose`

## Datenpersistenz

Die Datenbankdaten werden in einem Docker-Volume namens `mariadb_data` gespeichert und bleiben auch nach dem Stoppen der Container erhalten. Um die Daten zu löschen:

```bash
docker compose down -v
```

## Troubleshooting

### Problem: "Port already in use"
Wenn Port 5000 oder 3306 bereits belegt ist, können Sie die Ports in der `docker-compose.yml` ändern:

```yaml
ports:
  - "8080:5000"  # Statt 5000:5000
```

### Problem: "Database connection failed"
1. Prüfen Sie, ob der Datenbank-Container läuft:
   ```bash
   docker compose ps
   ```

2. Prüfen Sie die Datenbank-Logs:
   ```bash
   docker compose logs db
   ```

3. Stellen Sie sicher, dass die Umgebungsvariablen in `.env` korrekt sind.

### Problem: Container starten nicht
1. Prüfen Sie die Logs:
   ```bash
   docker compose logs
   ```

2. Entfernen Sie alte Container und Volumes:
   ```bash
   docker compose down -v
   docker compose up -d
   ```

## Entwicklung mit Docker

Für die Entwicklung können Sie das `docker-compose.override.yml` verwenden, um lokale Volumes zu mounten:

```yaml
services:
  web:
    volumes:
      - .:/app
    environment:
      FLASK_DEBUG: "True"
```

Dies ermöglicht Live-Reloading bei Code-Änderungen.

## Produktion

Für den Produktionseinsatz sollten Sie:

1. **Sichere Passwörter** in `.env` setzen
2. **SECRET_KEY** mit einem starken, zufälligen Wert versehen
3. **FLASK_DEBUG** auf `False` setzen
4. Einen **Reverse Proxy** (nginx) vorschalten
5. **SSL/TLS** Zertifikate einrichten
6. Regelmäßige **Backups** der Datenbank-Volumes durchführen

### Backup erstellen
```bash
docker compose exec db mysqldump -u finaz_user -p finaz_db > backup.sql
```

### Backup wiederherstellen
```bash
docker compose exec -T db mysql -u finaz_user -p finaz_db < backup.sql
```

## Weitere Informationen

Für die Verwendung der Anwendung siehe:
- [README.md](README.md) - Hauptdokumentation
- [WEB_FRONTEND_README.md](WEB_FRONTEND_README.md) - Web-Frontend Details
