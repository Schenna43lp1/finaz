"""
Models module for Finanzverwaltungstool
Contains classes for accounts, transactions, categories, and budgets
"""

from typing import Optional, List, Dict, Any
from datetime import date, datetime
from database import Database


class Account:
    """Account model for managing financial accounts"""
    
    def __init__(self, db: Database):
        self.db = db
    
    def create(self, name: str, account_type: str, balance: float = 0.0, 
               currency: str = 'EUR', description: str = '') -> Optional[int]:
        """
        Create a new account
        
        Args:
            name: Account name
            account_type: Type of account (Girokonto, Sparkonto, etc.)
            balance: Initial balance
            currency: Currency code
            description: Account description
            
        Returns:
            Account ID if successful, None otherwise
        """
        query = """
            INSERT INTO accounts (name, account_type, balance, currency, description)
            VALUES (%s, %s, %s, %s, %s)
        """
        if self.db.execute_query(query, (name, account_type, balance, currency, description)):
            return self.db.get_last_insert_id()
        return None
    
    def get_all(self) -> List[Dict[str, Any]]:
        """
        Get all accounts
        
        Returns:
            List of account dictionaries
        """
        query = "SELECT id, name, account_type, balance, currency, description FROM accounts"
        results = self.db.fetch_query(query)
        if results:
            return [
                {
                    'id': row[0],
                    'name': row[1],
                    'account_type': row[2],
                    'balance': float(row[3]),
                    'currency': row[4],
                    'description': row[5]
                }
                for row in results
            ]
        return []
    
    def get_by_id(self, account_id: int) -> Optional[Dict[str, Any]]:
        """Get account by ID"""
        query = "SELECT id, name, account_type, balance, currency, description FROM accounts WHERE id = %s"
        result = self.db.fetch_one(query, (account_id,))
        if result:
            return {
                'id': result[0],
                'name': result[1],
                'account_type': result[2],
                'balance': float(result[3]),
                'currency': result[4],
                'description': result[5]
            }
        return None
    
    def update_balance(self, account_id: int, new_balance: float) -> bool:
        """Update account balance"""
        query = "UPDATE accounts SET balance = %s WHERE id = %s"
        return self.db.execute_query(query, (new_balance, account_id))
    
    def delete(self, account_id: int) -> bool:
        """Delete an account"""
        query = "DELETE FROM accounts WHERE id = %s"
        return self.db.execute_query(query, (account_id,))


class Category:
    """Category model for transaction categorization"""
    
    def __init__(self, db: Database):
        self.db = db
    
    def create(self, name: str, category_type: str, description: str = '', 
               parent_id: Optional[int] = None) -> Optional[int]:
        """Create a new category"""
        query = """
            INSERT INTO categories (name, category_type, description, parent_id)
            VALUES (%s, %s, %s, %s)
        """
        if self.db.execute_query(query, (name, category_type, description, parent_id)):
            return self.db.get_last_insert_id()
        return None
    
    def get_all(self) -> List[Dict[str, Any]]:
        """Get all categories"""
        query = "SELECT id, name, category_type, description FROM categories ORDER BY category_type, name"
        results = self.db.fetch_query(query)
        if results:
            return [
                {
                    'id': row[0],
                    'name': row[1],
                    'category_type': row[2],
                    'description': row[3]
                }
                for row in results
            ]
        return []
    
    def get_by_type(self, category_type: str) -> List[Dict[str, Any]]:
        """Get categories by type"""
        query = "SELECT id, name, category_type, description FROM categories WHERE category_type = %s ORDER BY name"
        results = self.db.fetch_query(query, (category_type,))
        if results:
            return [
                {
                    'id': row[0],
                    'name': row[1],
                    'category_type': row[2],
                    'description': row[3]
                }
                for row in results
            ]
        return []


class Transaction:
    """Transaction model for financial transactions"""
    
    def __init__(self, db: Database):
        self.db = db
    
    def create(self, account_id: int, category_id: int, transaction_type: str,
               amount: float, description: str = '', transaction_date: date = None) -> Optional[int]:
        """
        Create a new transaction
        
        Args:
            account_id: ID of the account
            category_id: ID of the category
            transaction_type: Type (Einnahme, Ausgabe, Transfer)
            amount: Transaction amount
            description: Transaction description
            transaction_date: Date of transaction (defaults to today)
            
        Returns:
            Transaction ID if successful, None otherwise
        """
        if transaction_date is None:
            transaction_date = date.today()
        
        query = """
            INSERT INTO transactions (account_id, category_id, transaction_type, amount, description, transaction_date)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        if self.db.execute_query(query, (account_id, category_id, transaction_type, amount, description, transaction_date)):
            transaction_id = self.db.get_last_insert_id()
            
            # Update account balance
            account = Account(self.db)
            current_account = account.get_by_id(account_id)
            if current_account:
                if transaction_type == 'Einnahme':
                    new_balance = current_account['balance'] + amount
                else:  # Ausgabe
                    new_balance = current_account['balance'] - amount
                account.update_balance(account_id, new_balance)
            
            return transaction_id
        return None
    
    def get_all(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all transactions"""
        query = """
            SELECT t.id, t.account_id, a.name as account_name, t.category_id, c.name as category_name,
                   t.transaction_type, t.amount, t.description, t.transaction_date
            FROM transactions t
            JOIN accounts a ON t.account_id = a.id
            JOIN categories c ON t.category_id = c.id
            ORDER BY t.transaction_date DESC, t.id DESC
            LIMIT %s
        """
        results = self.db.fetch_query(query, (limit,))
        if results:
            return [
                {
                    'id': row[0],
                    'account_id': row[1],
                    'account_name': row[2],
                    'category_id': row[3],
                    'category_name': row[4],
                    'transaction_type': row[5],
                    'amount': float(row[6]),
                    'description': row[7],
                    'transaction_date': row[8]
                }
                for row in results
            ]
        return []
    
    def get_by_account(self, account_id: int, limit: int = 100) -> List[Dict[str, Any]]:
        """Get transactions for a specific account"""
        query = """
            SELECT t.id, t.account_id, a.name as account_name, t.category_id, c.name as category_name,
                   t.transaction_type, t.amount, t.description, t.transaction_date
            FROM transactions t
            JOIN accounts a ON t.account_id = a.id
            JOIN categories c ON t.category_id = c.id
            WHERE t.account_id = %s
            ORDER BY t.transaction_date DESC, t.id DESC
            LIMIT %s
        """
        results = self.db.fetch_query(query, (account_id, limit))
        if results:
            return [
                {
                    'id': row[0],
                    'account_id': row[1],
                    'account_name': row[2],
                    'category_id': row[3],
                    'category_name': row[4],
                    'transaction_type': row[5],
                    'amount': float(row[6]),
                    'description': row[7],
                    'transaction_date': row[8]
                }
                for row in results
            ]
        return []
    
    def get_summary_by_period(self, start_date: date, end_date: date) -> Dict[str, float]:
        """Get transaction summary for a period"""
        query = """
            SELECT transaction_type, SUM(amount) as total
            FROM transactions
            WHERE transaction_date BETWEEN %s AND %s
            GROUP BY transaction_type
        """
        results = self.db.fetch_query(query, (start_date, end_date))
        summary = {'Einnahme': 0.0, 'Ausgabe': 0.0}
        if results:
            for row in results:
                summary[row[0]] = float(row[1])
        summary['Saldo'] = summary['Einnahme'] - summary['Ausgabe']
        return summary
    
    def delete(self, transaction_id: int) -> bool:
        """Delete a transaction"""
        # First get the transaction details to reverse the balance update
        query = "SELECT account_id, transaction_type, amount FROM transactions WHERE id = %s"
        result = self.db.fetch_one(query, (transaction_id,))
        
        if result:
            account_id, transaction_type, amount = result[0], result[1], float(result[2])
            
            # Delete the transaction
            delete_query = "DELETE FROM transactions WHERE id = %s"
            if self.db.execute_query(delete_query, (transaction_id,)):
                # Update account balance
                account = Account(self.db)
                current_account = account.get_by_id(account_id)
                if current_account:
                    if transaction_type == 'Einnahme':
                        new_balance = current_account['balance'] - amount
                    else:  # Ausgabe
                        new_balance = current_account['balance'] + amount
                    account.update_balance(account_id, new_balance)
                return True
        return False


class Budget:
    """Budget model for financial planning"""
    
    def __init__(self, db: Database):
        self.db = db
    
    def create(self, category_id: int, amount: float, period_start: date, 
               period_end: date) -> Optional[int]:
        """Create a new budget"""
        query = """
            INSERT INTO budgets (category_id, amount, period_start, period_end)
            VALUES (%s, %s, %s, %s)
        """
        if self.db.execute_query(query, (category_id, amount, period_start, period_end)):
            return self.db.get_last_insert_id()
        return None
    
    def get_all(self) -> List[Dict[str, Any]]:
        """Get all budgets"""
        query = """
            SELECT b.id, b.category_id, c.name as category_name, b.amount, b.period_start, b.period_end
            FROM budgets b
            JOIN categories c ON b.category_id = c.id
            ORDER BY b.period_start DESC
        """
        results = self.db.fetch_query(query)
        if results:
            return [
                {
                    'id': row[0],
                    'category_id': row[1],
                    'category_name': row[2],
                    'amount': float(row[3]),
                    'period_start': row[4],
                    'period_end': row[5]
                }
                for row in results
            ]
        return []
    
    def get_active_budgets(self, current_date: date = None) -> List[Dict[str, Any]]:
        """Get budgets active on a specific date"""
        if current_date is None:
            current_date = date.today()
        
        query = """
            SELECT b.id, b.category_id, c.name as category_name, b.amount, b.period_start, b.period_end
            FROM budgets b
            JOIN categories c ON b.category_id = c.id
            WHERE %s BETWEEN b.period_start AND b.period_end
            ORDER BY c.name
        """
        results = self.db.fetch_query(query, (current_date,))
        if results:
            return [
                {
                    'id': row[0],
                    'category_id': row[1],
                    'category_name': row[2],
                    'amount': float(row[3]),
                    'period_start': row[4],
                    'period_end': row[5]
                }
                for row in results
            ]
        return []
