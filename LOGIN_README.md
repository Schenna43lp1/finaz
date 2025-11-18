# Login System Documentation

## Overview

The Finaz application now includes a complete authentication system to secure access to financial data. Users must register and log in before accessing any financial management features.

## Features

- **User Registration**: Create new user accounts with username and password
- **Secure Login**: Authenticate with username and password
- **Session Management**: Keep users logged in across page requests
- **Password Security**: Passwords are hashed using Werkzeug's secure password hashing
- **Protected Routes**: All financial data pages require authentication
- **User-Friendly UI**: Clean, modern login and registration forms

## Database Schema

A new `users` table has been added to the database:

```sql
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

## Setup

### 1. Update Database Schema

If you have an existing database, apply the schema update:

```bash
mysql -u finaz_user -p finaz_db < database_schema.sql
```

Or manually create the users table using the SQL command above.

### 2. Restart the Application

```bash
python app.py
```

### 3. Register Your First User

1. Navigate to `http://localhost:5000`
2. You'll be redirected to the login page
3. Click "Jetzt registrieren" (Register now)
4. Fill in the registration form:
   - Username (required)
   - Email (optional)
   - Password (minimum 6 characters, required)
   - Confirm Password (required)
5. Click "Registrieren" to create your account
6. You'll be redirected to the login page

### 4. Log In

1. Enter your username and password
2. Click "Anmelden" (Login)
3. You'll be redirected to the dashboard

## Usage

### Accessing the Application

- **First Visit**: You'll be redirected to `/login`
- **After Login**: You can access all features (Dashboard, Accounts, Transactions, etc.)
- **Logout**: Click "Abmelden" in the navigation bar

### Protected Routes

All main application routes are now protected and require authentication:

- `/` - Dashboard
- `/accounts` - Account management
- `/transactions` - Transaction management
- `/categories` - Categories
- `/budgets` - Budget management
- `/reports` - Financial reports

### Public Routes

These routes are accessible without login:

- `/login` - Login page
- `/register` - Registration page

## Security Features

1. **Password Hashing**: Passwords are never stored in plain text. We use Werkzeug's `generate_password_hash()` with secure defaults.

2. **Session Management**: User sessions are managed by Flask's secure session system.

3. **Unique Usernames**: Database constraint ensures username uniqueness.

4. **Input Validation**: 
   - Username and password are required
   - Password must be at least 6 characters
   - Password confirmation must match
   - Existing usernames are rejected

## API Endpoints

### POST /register

Register a new user account.

**Parameters:**
- `username` (required): Unique username
- `password` (required): Password (min 6 characters)
- `password_confirm` (required): Password confirmation
- `email` (optional): Email address

**Response:**
- Success: Redirect to `/login` with success message
- Error: Redirect to `/register` with error message

### POST /login

Authenticate a user.

**Parameters:**
- `username` (required): Username
- `password` (required): Password

**Response:**
- Success: Redirect to `/` (dashboard) with user session created
- Error: Redirect to `/login` with error message

### GET /logout

Log out the current user and clear the session.

**Response:**
- Redirect to `/login` with logout message

## Testing

Run the authentication tests:

```bash
python test_authentication.py
```

The test suite includes:
- User model import tests
- Password hashing verification
- Template existence checks
- Route definition checks
- Model structure tests

## Troubleshooting

### Cannot access the application

**Problem**: Redirected to login page but can't log in

**Solution**: Make sure you've:
1. Updated the database schema with the `users` table
2. Registered a user account
3. Using the correct username and password

### Password hashing error

**Problem**: Error when trying to register or login

**Solution**: Ensure Werkzeug is installed:
```bash
pip install -r requirements.txt
```

### Session not persisting

**Problem**: Logged out after every page refresh

**Solution**: Check that Flask secret key is set in app.py or .env file

## Future Enhancements

Possible improvements for the authentication system:

- Password reset functionality
- Email verification
- Multi-factor authentication
- Remember me option
- Session timeout
- Password strength requirements
- User profile management
- Admin user roles
- Account deletion
- Password change feature
