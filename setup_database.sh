#!/bin/bash
# Setup script for Finanzverwaltungstool database

set -e

echo "============================================================"
echo "   Finanzverwaltungstool - Datenbank Setup"
echo "============================================================"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env Datei nicht gefunden!"
    echo "Erstelle .env aus .env.example..."
    cp .env.example .env
    echo "✓ .env Datei erstellt"
    echo ""
    echo "Bitte bearbeiten Sie die .env Datei mit Ihren Datenbankzugangsdaten"
    echo "und führen Sie dieses Script erneut aus."
    exit 1
fi

# Source .env file
export $(cat .env | grep -v '^#' | xargs)

echo "Datenbankverbindung:"
echo "  Host: ${DB_HOST}"
echo "  Port: ${DB_PORT}"
echo "  Datenbank: ${DB_NAME}"
echo "  Benutzer: ${DB_USER}"
echo ""

# Check if MariaDB is installed
if ! command -v mysql &> /dev/null; then
    echo "✗ MariaDB/MySQL ist nicht installiert!"
    echo ""
    echo "Installation (Ubuntu/Debian):"
    echo "  sudo apt update"
    echo "  sudo apt install mariadb-server"
    echo ""
    exit 1
fi

# Check if MariaDB is running
if ! systemctl is-active --quiet mariadb 2>/dev/null && ! systemctl is-active --quiet mysql 2>/dev/null; then
    echo "⚠️  MariaDB/MySQL läuft nicht!"
    echo "Versuche MariaDB zu starten..."
    sudo systemctl start mariadb || sudo systemctl start mysql || {
        echo "✗ Konnte MariaDB nicht starten"
        exit 1
    }
    echo "✓ MariaDB gestartet"
fi

echo "Hinweis: Sie werden möglicherweise nach dem MySQL root-Passwort gefragt."
echo ""

# Create database and user (if they don't exist)
read -p "Möchten Sie die Datenbank und den Benutzer erstellen? (j/n): " create_db

if [ "$create_db" = "j" ] || [ "$create_db" = "J" ]; then
    echo ""
    echo "Erstelle Datenbank und Benutzer..."
    
    mysql -u root -p <<EOF
CREATE DATABASE IF NOT EXISTS ${DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS '${DB_USER}'@'localhost' IDENTIFIED BY '${DB_PASSWORD}';
GRANT ALL PRIVILEGES ON ${DB_NAME}.* TO '${DB_USER}'@'localhost';
FLUSH PRIVILEGES;
EOF
    
    if [ $? -eq 0 ]; then
        echo "✓ Datenbank und Benutzer erfolgreich erstellt"
    else
        echo "✗ Fehler beim Erstellen der Datenbank"
        exit 1
    fi
fi

echo ""
echo "Importiere Datenbank-Schema..."

mysql -u "${DB_USER}" -p"${DB_PASSWORD}" "${DB_NAME}" < database_schema.sql

if [ $? -eq 0 ]; then
    echo "✓ Schema erfolgreich importiert"
else
    echo "✗ Fehler beim Importieren des Schemas"
    exit 1
fi

echo ""
echo "============================================================"
echo "✓ Setup abgeschlossen!"
echo "============================================================"
echo ""
echo "Sie können jetzt das Finanzverwaltungstool starten:"
echo "  python finaz.py"
echo ""
