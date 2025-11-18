#!/usr/bin/env python3
"""
Script to create an admin user for Finanzverwaltungstool
This should be used after database setup to create the first admin user.
"""

import sys
import getpass
from database import Database
from models import User


def create_admin_user():
    """Create an admin user interactively"""
    print("=" * 60)
    print("   Finanzverwaltungstool - Admin-Benutzer erstellen")
    print("=" * 60)
    print()
    
    # Connect to database
    db = Database()
    if not db.connect():
        print("✗ Fehler: Datenbankverbindung fehlgeschlagen")
        print("Bitte überprüfen Sie Ihre .env Datei und stellen Sie sicher,")
        print("dass die Datenbank läuft und das Schema importiert wurde.")
        return False
    
    user_model = User(db)
    
    # Get username
    while True:
        username = input("Benutzername: ").strip()
        if not username:
            print("✗ Benutzername darf nicht leer sein")
            continue
        
        # Check if username already exists
        if user_model.get_by_username(username):
            print(f"✗ Benutzer '{username}' existiert bereits")
            retry = input("Anderen Benutzernamen versuchen? (j/n): ").lower()
            if retry != 'j':
                return False
            continue
        
        break
    
    # Get email (optional)
    email = input("E-Mail (optional): ").strip()
    
    # Get password
    while True:
        password = getpass.getpass("Passwort (mindestens 6 Zeichen): ")
        if len(password) < 6:
            print("✗ Passwort muss mindestens 6 Zeichen lang sein")
            continue
        
        password_confirm = getpass.getpass("Passwort bestätigen: ")
        if password != password_confirm:
            print("✗ Passwörter stimmen nicht überein")
            continue
        
        break
    
    # Create admin user
    print()
    print("Erstelle Admin-Benutzer...")
    user_id = user_model.create(username, password, email, is_admin=True)
    
    if user_id:
        print(f"✓ Admin-Benutzer '{username}' erfolgreich erstellt (ID: {user_id})")
        print()
        print("Sie können sich jetzt mit diesem Benutzer anmelden und")
        print("weitere Benutzer über die Web-Oberfläche erstellen.")
        return True
    else:
        print("✗ Fehler beim Erstellen des Admin-Benutzers")
        return False


def main():
    """Main function"""
    try:
        success = create_admin_user()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print()
        print("Abgebrochen")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Fehler: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
