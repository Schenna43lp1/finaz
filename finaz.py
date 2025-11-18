#!/usr/bin/env python3
"""
Finanzverwaltungstool - Financial Management Tool
Main CLI application with MariaDB backend
"""

import sys
from datetime import date, datetime, timedelta
from typing import Optional
from tabulate import tabulate
from database import Database
from models import Account, Category, Transaction, Budget


class FinanzTool:
    """Main application class for financial management"""
    
    def __init__(self):
        self.db = Database()
        self.account = None
        self.category = None
        self.transaction = None
        self.budget = None
    
    def connect(self) -> bool:
        """Connect to database and initialize models"""
        if self.db.connect():
            print("✓ Erfolgreich mit der Datenbank verbunden")
            self.account = Account(self.db)
            self.category = Category(self.db)
            self.transaction = Transaction(self.db)
            self.budget = Budget(self.db)
            return True
        else:
            print("✗ Fehler bei der Datenbankverbindung")
            print("Bitte überprüfen Sie Ihre .env Konfiguration")
            return False
    
    def disconnect(self):
        """Disconnect from database"""
        self.db.disconnect()
    
    def print_menu(self):
        """Display main menu"""
        print("\n" + "="*60)
        print("        FINANZVERWALTUNGSTOOL - HAUPTMENÜ")
        print("="*60)
        print("1.  Konten verwalten")
        print("2.  Neue Transaktion hinzufügen")
        print("3.  Transaktionen anzeigen")
        print("4.  Kategorien verwalten")
        print("5.  Budget verwalten")
        print("6.  Finanzübersicht")
        print("7.  Monatsreport")
        print("0.  Beenden")
        print("="*60)
    
    def manage_accounts(self):
        """Account management submenu"""
        while True:
            print("\n--- KONTENVERWALTUNG ---")
            print("1. Alle Konten anzeigen")
            print("2. Neues Konto erstellen")
            print("3. Konto löschen")
            print("0. Zurück")
            
            choice = input("\nAuswahl: ").strip()
            
            if choice == '1':
                self.show_accounts()
            elif choice == '2':
                self.create_account()
            elif choice == '3':
                self.delete_account()
            elif choice == '0':
                break
    
    def show_accounts(self):
        """Display all accounts"""
        accounts = self.account.get_all()
        if accounts:
            table_data = [
                [acc['id'], acc['name'], acc['account_type'], 
                 f"{acc['balance']:.2f} {acc['currency']}", acc['description']]
                for acc in accounts
            ]
            print("\n" + tabulate(table_data, 
                                 headers=['ID', 'Name', 'Typ', 'Saldo', 'Beschreibung'],
                                 tablefmt='grid'))
        else:
            print("\nKeine Konten vorhanden.")
    
    def create_account(self):
        """Create a new account"""
        print("\n--- NEUES KONTO ERSTELLEN ---")
        name = input("Kontoname: ").strip()
        
        print("\nKontotyp:")
        print("1. Girokonto")
        print("2. Sparkonto")
        print("3. Kreditkarte")
        print("4. Bargeld")
        print("5. Sonstiges")
        
        type_choice = input("Auswahl: ").strip()
        type_map = {
            '1': 'Girokonto',
            '2': 'Sparkonto',
            '3': 'Kreditkarte',
            '4': 'Bargeld',
            '5': 'Sonstiges'
        }
        account_type = type_map.get(type_choice, 'Sonstiges')
        
        balance_str = input("Anfangssaldo (Standard: 0.00): ").strip()
        balance = float(balance_str) if balance_str else 0.0
        
        description = input("Beschreibung (optional): ").strip()
        
        account_id = self.account.create(name, account_type, balance, 'EUR', description)
        if account_id:
            print(f"\n✓ Konto '{name}' erfolgreich erstellt (ID: {account_id})")
        else:
            print("\n✗ Fehler beim Erstellen des Kontos")
    
    def delete_account(self):
        """Delete an account"""
        self.show_accounts()
        account_id = input("\nKonto-ID zum Löschen (0 für Abbruch): ").strip()
        
        if account_id == '0':
            return
        
        try:
            account_id = int(account_id)
            confirm = input(f"Konto mit ID {account_id} wirklich löschen? (ja/nein): ").strip().lower()
            
            if confirm == 'ja':
                if self.account.delete(account_id):
                    print("\n✓ Konto erfolgreich gelöscht")
                else:
                    print("\n✗ Fehler beim Löschen des Kontos")
        except ValueError:
            print("\n✗ Ungültige Eingabe")
    
    def add_transaction(self):
        """Add a new transaction"""
        print("\n--- NEUE TRANSAKTION ---")
        
        # Show accounts
        accounts = self.account.get_all()
        if not accounts:
            print("Keine Konten vorhanden. Bitte erstellen Sie zuerst ein Konto.")
            return
        
        print("\nVerfügbare Konten:")
        for acc in accounts:
            print(f"{acc['id']}. {acc['name']} ({acc['account_type']}) - {acc['balance']:.2f} {acc['currency']}")
        
        account_id = int(input("\nKonto-ID: ").strip())
        
        print("\nTransaktionstyp:")
        print("1. Einnahme")
        print("2. Ausgabe")
        
        trans_type_choice = input("Auswahl: ").strip()
        transaction_type = 'Einnahme' if trans_type_choice == '1' else 'Ausgabe'
        
        # Show categories for selected type
        categories = self.category.get_by_type(transaction_type)
        if not categories:
            print(f"\nKeine Kategorien für {transaction_type} vorhanden.")
            return
        
        print(f"\nVerfügbare Kategorien ({transaction_type}):")
        for cat in categories:
            print(f"{cat['id']}. {cat['name']} - {cat['description']}")
        
        category_id = int(input("\nKategorie-ID: ").strip())
        
        amount = float(input("Betrag: ").strip())
        description = input("Beschreibung (optional): ").strip()
        
        date_str = input("Datum (YYYY-MM-DD, Enter für heute): ").strip()
        if date_str:
            trans_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        else:
            trans_date = date.today()
        
        transaction_id = self.transaction.create(
            account_id, category_id, transaction_type, amount, description, trans_date
        )
        
        if transaction_id:
            print(f"\n✓ Transaktion erfolgreich hinzugefügt (ID: {transaction_id})")
        else:
            print("\n✗ Fehler beim Hinzufügen der Transaktion")
    
    def show_transactions(self):
        """Display transactions"""
        print("\n--- TRANSAKTIONEN ---")
        print("1. Alle Transaktionen")
        print("2. Transaktionen nach Konto")
        print("0. Zurück")
        
        choice = input("\nAuswahl: ").strip()
        
        if choice == '1':
            transactions = self.transaction.get_all()
            self.display_transactions(transactions)
        elif choice == '2':
            self.show_accounts()
            account_id = int(input("\nKonto-ID: ").strip())
            transactions = self.transaction.get_by_account(account_id)
            self.display_transactions(transactions)
    
    def display_transactions(self, transactions):
        """Display list of transactions"""
        if transactions:
            table_data = [
                [t['id'], t['transaction_date'], t['account_name'], 
                 t['category_name'], t['transaction_type'], 
                 f"{t['amount']:.2f}", t['description']]
                for t in transactions
            ]
            print("\n" + tabulate(table_data,
                                 headers=['ID', 'Datum', 'Konto', 'Kategorie', 'Typ', 'Betrag', 'Beschreibung'],
                                 tablefmt='grid'))
        else:
            print("\nKeine Transaktionen vorhanden.")
    
    def manage_categories(self):
        """Category management"""
        print("\n--- KATEGORIEN ---")
        categories = self.category.get_all()
        
        if categories:
            # Group by type
            einnahme = [c for c in categories if c['category_type'] == 'Einnahme']
            ausgabe = [c for c in categories if c['category_type'] == 'Ausgabe']
            
            print("\nEINNAHME-KATEGORIEN:")
            for cat in einnahme:
                print(f"  {cat['id']}. {cat['name']} - {cat['description']}")
            
            print("\nAUSGABE-KATEGORIEN:")
            for cat in ausgabe:
                print(f"  {cat['id']}. {cat['name']} - {cat['description']}")
        else:
            print("\nKeine Kategorien vorhanden.")
    
    def manage_budgets(self):
        """Budget management"""
        while True:
            print("\n--- BUDGETVERWALTUNG ---")
            print("1. Aktuelle Budgets anzeigen")
            print("2. Neues Budget erstellen")
            print("0. Zurück")
            
            choice = input("\nAuswahl: ").strip()
            
            if choice == '1':
                self.show_budgets()
            elif choice == '2':
                self.create_budget()
            elif choice == '0':
                break
    
    def show_budgets(self):
        """Display active budgets"""
        budgets = self.budget.get_active_budgets()
        
        if budgets:
            table_data = [
                [b['id'], b['category_name'], f"{b['amount']:.2f} EUR",
                 b['period_start'], b['period_end']]
                for b in budgets
            ]
            print("\n" + tabulate(table_data,
                                 headers=['ID', 'Kategorie', 'Budget', 'Von', 'Bis'],
                                 tablefmt='grid'))
        else:
            print("\nKeine aktiven Budgets vorhanden.")
    
    def create_budget(self):
        """Create a new budget"""
        print("\n--- NEUES BUDGET ERSTELLEN ---")
        
        categories = self.category.get_by_type('Ausgabe')
        if not categories:
            print("Keine Ausgabe-Kategorien vorhanden.")
            return
        
        print("\nVerfügbare Kategorien:")
        for cat in categories:
            print(f"{cat['id']}. {cat['name']}")
        
        category_id = int(input("\nKategorie-ID: ").strip())
        amount = float(input("Budget-Betrag: ").strip())
        
        start_str = input("Startdatum (YYYY-MM-DD): ").strip()
        end_str = input("Enddatum (YYYY-MM-DD): ").strip()
        
        start_date = datetime.strptime(start_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_str, '%Y-%m-%d').date()
        
        budget_id = self.budget.create(category_id, amount, start_date, end_date)
        
        if budget_id:
            print(f"\n✓ Budget erfolgreich erstellt (ID: {budget_id})")
        else:
            print("\n✗ Fehler beim Erstellen des Budgets")
    
    def show_overview(self):
        """Display financial overview"""
        print("\n" + "="*60)
        print("                   FINANZÜBERSICHT")
        print("="*60)
        
        # Show accounts
        accounts = self.account.get_all()
        total_balance = sum(acc['balance'] for acc in accounts)
        
        print("\nKONTENSTAND:")
        for acc in accounts:
            print(f"  {acc['name']}: {acc['balance']:.2f} {acc['currency']}")
        print(f"\n  GESAMT: {total_balance:.2f} EUR")
        
        # Show current month summary
        today = date.today()
        start_of_month = date(today.year, today.month, 1)
        
        summary = self.transaction.get_summary_by_period(start_of_month, today)
        
        print(f"\nAKTUELLER MONAT ({today.strftime('%B %Y')}):")
        print(f"  Einnahmen:  +{summary['Einnahme']:.2f} EUR")
        print(f"  Ausgaben:   -{summary['Ausgabe']:.2f} EUR")
        print(f"  Saldo:       {summary['Saldo']:.2f} EUR")
    
    def show_monthly_report(self):
        """Display monthly report"""
        print("\n--- MONATSREPORT ---")
        
        year = int(input("Jahr (YYYY): ").strip())
        month = int(input("Monat (1-12): ").strip())
        
        start_date = date(year, month, 1)
        # Calculate last day of month
        if month == 12:
            end_date = date(year, 12, 31)
        else:
            end_date = date(year, month + 1, 1) - timedelta(days=1)
        
        summary = self.transaction.get_summary_by_period(start_date, end_date)
        
        print(f"\n{'='*60}")
        print(f"           MONATSREPORT {month}/{year}")
        print(f"{'='*60}")
        print(f"Zeitraum: {start_date} bis {end_date}")
        print(f"\nEinnahmen:  +{summary['Einnahme']:.2f} EUR")
        print(f"Ausgaben:   -{summary['Ausgabe']:.2f} EUR")
        print(f"{'='*60}")
        print(f"Saldo:       {summary['Saldo']:.2f} EUR")
        print(f"{'='*60}")
    
    def run(self):
        """Main application loop"""
        print("\n" + "="*60)
        print("       FINANZVERWALTUNGSTOOL mit MariaDB Backend")
        print("="*60)
        
        if not self.connect():
            return
        
        try:
            while True:
                self.print_menu()
                choice = input("\nAuswahl: ").strip()
                
                if choice == '1':
                    self.manage_accounts()
                elif choice == '2':
                    self.add_transaction()
                elif choice == '3':
                    self.show_transactions()
                elif choice == '4':
                    self.manage_categories()
                elif choice == '5':
                    self.manage_budgets()
                elif choice == '6':
                    self.show_overview()
                elif choice == '7':
                    self.show_monthly_report()
                elif choice == '0':
                    print("\nAuf Wiedersehen!")
                    break
                else:
                    print("\n✗ Ungültige Auswahl")
        
        except KeyboardInterrupt:
            print("\n\nProgramm abgebrochen.")
        except Exception as e:
            print(f"\n✗ Fehler: {e}")
        finally:
            self.disconnect()


if __name__ == '__main__':
    app = FinanzTool()
    app.run()
