#!/usr/bin/env python3
"""
Finanzverwaltungstool - Web Application
Flask-based web frontend for financial management
"""

import os
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from datetime import date, datetime, timedelta
from database import Database
from models import Account, Category, Transaction, Budget, User

app = Flask(__name__)
# Use environment variable for secret key in production, fallback for development
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Initialize database and models
db = Database()
account_model = None
category_model = None
transaction_model = None
budget_model = None
user_model = None


def init_models():
    """Initialize database models"""
    global account_model, category_model, transaction_model, budget_model, user_model
    if db.connect():
        account_model = Account(db)
        category_model = Category(db)
        transaction_model = Transaction(db)
        budget_model = Budget(db)
        user_model = User(db)
        return True
    return False


def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Bitte melden Sie sich an, um auf diese Seite zuzugreifen', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Decorator to require admin privileges for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Bitte melden Sie sich an, um auf diese Seite zuzugreifen', 'error')
            return redirect(url_for('login'))
        if not session.get('is_admin', False):
            flash('Zugriff verweigert. Administratorrechte erforderlich.', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        if not init_models():
            flash('Fehler bei der Datenbankverbindung', 'error')
            return redirect(url_for('login'))
        
        username = request.form.get('username')
        password = request.form.get('password')
        
        if user_model.verify_password(username, password):
            user = user_model.get_by_username(username)
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['is_admin'] = user.get('is_admin', False)
            flash(f'Willkommen zurück, {username}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Ungültiger Benutzername oder Passwort', 'error')
    
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
@admin_required
def register():
    """Admin-only user registration page"""
    if request.method == 'POST':
        if not init_models():
            flash('Fehler bei der Datenbankverbindung', 'error')
            return redirect(url_for('users'))
        
        username = request.form.get('username')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        email = request.form.get('email', '')
        is_admin = request.form.get('is_admin') == 'on'
        
        # Validate input
        if not username or not password:
            flash('Benutzername und Passwort sind erforderlich', 'error')
            return redirect(url_for('register'))
        
        if password != password_confirm:
            flash('Passwörter stimmen nicht überein', 'error')
            return redirect(url_for('register'))
        
        if len(password) < 6:
            flash('Passwort muss mindestens 6 Zeichen lang sein', 'error')
            return redirect(url_for('register'))
        
        # Check if username already exists
        if user_model.get_by_username(username):
            flash('Benutzername existiert bereits', 'error')
            return redirect(url_for('register'))
        
        # Create user
        user_id = user_model.create(username, password, email, is_admin)
        if user_id:
            flash(f'Benutzer "{username}" erfolgreich erstellt', 'success')
            return redirect(url_for('users'))
        else:
            flash('Fehler beim Erstellen des Benutzers', 'error')
    
    return render_template('register.html')


@app.route('/logout')
def logout():
    """Logout user"""
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('is_admin', None)
    flash('Sie wurden erfolgreich abgemeldet', 'success')
    return redirect(url_for('login'))


@app.route('/')
@login_required
def index():
    """Dashboard/Overview page"""
    if not init_models():
        flash('Fehler bei der Datenbankverbindung', 'error')
        return render_template('error.html', message='Datenbankverbindung fehlgeschlagen')
    
    # Get accounts summary
    accounts = account_model.get_all()
    total_balance = sum(acc['balance'] for acc in accounts) if accounts else 0
    
    # Get current month summary
    today = date.today()
    start_of_month = date(today.year, today.month, 1)
    summary = transaction_model.get_summary_by_period(start_of_month, today)
    
    # Get recent transactions
    recent_transactions = transaction_model.get_all()[:10] if transaction_model else []
    
    return render_template('index.html',
                         accounts=accounts,
                         total_balance=total_balance,
                         summary=summary,
                         recent_transactions=recent_transactions,
                         current_month=today.strftime('%B %Y'))


@app.route('/accounts')
@login_required
def accounts():
    """Account management page"""
    if not init_models():
        flash('Fehler bei der Datenbankverbindung', 'error')
        return redirect(url_for('index'))
    
    accounts = account_model.get_all()
    return render_template('accounts.html', accounts=accounts)


@app.route('/accounts/create', methods=['GET', 'POST'])
@login_required
def create_account():
    """Create new account"""
    if request.method == 'POST':
        if not init_models():
            flash('Fehler bei der Datenbankverbindung', 'error')
            return redirect(url_for('accounts'))
        
        name = request.form.get('name')
        account_type = request.form.get('account_type')
        balance = float(request.form.get('balance', 0))
        currency = request.form.get('currency', 'EUR')
        description = request.form.get('description', '')
        
        account_id = account_model.create(name, account_type, balance, currency, description)
        if account_id:
            flash(f'Konto "{name}" erfolgreich erstellt', 'success')
        else:
            flash('Fehler beim Erstellen des Kontos', 'error')
        
        return redirect(url_for('accounts'))
    
    return render_template('create_account.html')


@app.route('/accounts/delete/<int:account_id>', methods=['POST'])
@login_required
def delete_account(account_id):
    """Delete an account"""
    if not init_models():
        flash('Fehler bei der Datenbankverbindung', 'error')
        return redirect(url_for('accounts'))
    
    if account_model.delete(account_id):
        flash('Konto erfolgreich gelöscht', 'success')
    else:
        flash('Fehler beim Löschen des Kontos', 'error')
    
    return redirect(url_for('accounts'))


@app.route('/transactions')
@login_required
def transactions():
    """Transaction list page"""
    if not init_models():
        flash('Fehler bei der Datenbankverbindung', 'error')
        return redirect(url_for('index'))
    
    account_id = request.args.get('account_id', type=int)
    
    if account_id:
        transactions = transaction_model.get_by_account(account_id)
    else:
        transactions = transaction_model.get_all()
    
    accounts = account_model.get_all()
    
    return render_template('transactions.html', 
                         transactions=transactions,
                         accounts=accounts,
                         selected_account=account_id)


@app.route('/transactions/create', methods=['GET', 'POST'])
@login_required
def create_transaction():
    """Create new transaction"""
    if not init_models():
        flash('Fehler bei der Datenbankverbindung', 'error')
        return redirect(url_for('transactions'))
    
    if request.method == 'POST':
        account_id = int(request.form.get('account_id'))
        category_id = int(request.form.get('category_id'))
        transaction_type = request.form.get('transaction_type')
        amount = float(request.form.get('amount'))
        description = request.form.get('description', '')
        transaction_date_str = request.form.get('transaction_date')
        
        if transaction_date_str:
            transaction_date = datetime.strptime(transaction_date_str, '%Y-%m-%d').date()
        else:
            transaction_date = date.today()
        
        transaction_id = transaction_model.create(
            account_id, category_id, transaction_type, amount, description, transaction_date
        )
        
        if transaction_id:
            flash('Transaktion erfolgreich hinzugefügt', 'success')
        else:
            flash('Fehler beim Hinzufügen der Transaktion', 'error')
        
        return redirect(url_for('transactions'))
    
    # GET request - show form
    accounts = account_model.get_all()
    categories = category_model.get_all()
    
    return render_template('create_transaction.html',
                         accounts=accounts,
                         categories=categories,
                         today=date.today().strftime('%Y-%m-%d'))


@app.route('/categories')
@login_required
def categories():
    """Categories page"""
    if not init_models():
        flash('Fehler bei der Datenbankverbindung', 'error')
        return redirect(url_for('index'))
    
    all_categories = category_model.get_all()
    
    # Group by type
    income_categories = [c for c in all_categories if c['category_type'] == 'Einnahme']
    expense_categories = [c for c in all_categories if c['category_type'] == 'Ausgabe']
    
    return render_template('categories.html',
                         income_categories=income_categories,
                         expense_categories=expense_categories)


@app.route('/budgets')
@login_required
def budgets():
    """Budget management page"""
    if not init_models():
        flash('Fehler bei der Datenbankverbindung', 'error')
        return redirect(url_for('index'))
    
    active_budgets = budget_model.get_active_budgets()
    
    return render_template('budgets.html', budgets=active_budgets)


@app.route('/budgets/create', methods=['GET', 'POST'])
@login_required
def create_budget():
    """Create new budget"""
    if not init_models():
        flash('Fehler bei der Datenbankverbindung', 'error')
        return redirect(url_for('budgets'))
    
    if request.method == 'POST':
        category_id = int(request.form.get('category_id'))
        amount = float(request.form.get('amount'))
        period_start = datetime.strptime(request.form.get('period_start'), '%Y-%m-%d').date()
        period_end = datetime.strptime(request.form.get('period_end'), '%Y-%m-%d').date()
        
        budget_id = budget_model.create(category_id, amount, period_start, period_end)
        
        if budget_id:
            flash('Budget erfolgreich erstellt', 'success')
        else:
            flash('Fehler beim Erstellen des Budgets', 'error')
        
        return redirect(url_for('budgets'))
    
    # GET request - show form
    expense_categories = category_model.get_by_type('Ausgabe')
    
    return render_template('create_budget.html',
                         categories=expense_categories,
                         today=date.today().strftime('%Y-%m-%d'))


@app.route('/reports')
@login_required
def reports():
    """Monthly reports page"""
    if not init_models():
        flash('Fehler bei der Datenbankverbindung', 'error')
        return redirect(url_for('index'))
    
    # Get current month by default
    today = date.today()
    year = request.args.get('year', today.year, type=int)
    month = request.args.get('month', today.month, type=int)
    
    start_date = date(year, month, 1)
    # Calculate last day of month
    if month == 12:
        end_date = date(year, 12, 31)
    else:
        end_date = date(year, month + 1, 1) - timedelta(days=1)
    
    summary = transaction_model.get_summary_by_period(start_date, end_date)
    transactions = transaction_model.get_all()
    
    # Filter transactions for the selected period
    period_transactions = [
        t for t in transactions 
        if start_date <= datetime.strptime(str(t['transaction_date']), '%Y-%m-%d').date() <= end_date
    ]
    
    return render_template('reports.html',
                         summary=summary,
                         transactions=period_transactions,
                         year=year,
                         month=month,
                         start_date=start_date,
                         end_date=end_date)


@app.route('/api/categories/<transaction_type>')
@login_required
def api_categories(transaction_type):
    """API endpoint to get categories by type"""
    if not init_models():
        return jsonify({'error': 'Database connection failed'}), 500
    
    categories = category_model.get_by_type(transaction_type)
    return jsonify(categories)


@app.route('/users')
@admin_required
def users():
    """User management page (admin only)"""
    if not init_models():
        flash('Fehler bei der Datenbankverbindung', 'error')
        return redirect(url_for('index'))
    
    all_users = user_model.get_all()
    return render_template('users.html', users=all_users)


if __name__ == '__main__':
    # Debug mode should only be enabled for development
    # For production, use a WSGI server like gunicorn or uwsgi
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1', 'yes')
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
