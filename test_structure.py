#!/usr/bin/env python3
"""
Test script to verify the structure of the Finanzverwaltungstool
without requiring a database connection
"""

import sys
import importlib.util

def test_module_imports():
    """Test if all modules can be imported"""
    print("Testing module imports...")
    
    modules = {
        'database': 'database.py',
        'models': 'models.py',
        'finaz': 'finaz.py'
    }
    
    for module_name, file_path in modules.items():
        try:
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            print(f"✓ {module_name} module imported successfully")
        except Exception as e:
            print(f"✗ Failed to import {module_name}: {e}")
            return False
    
    return True

def test_class_existence():
    """Test if all required classes exist"""
    print("\nTesting class existence...")
    
    from database import Database
    from models import Account, Category, Transaction, Budget
    from finaz import FinanzTool
    
    classes = [
        ('Database', Database),
        ('Account', Account),
        ('Category', Category),
        ('Transaction', Transaction),
        ('Budget', Budget),
        ('FinanzTool', FinanzTool)
    ]
    
    for class_name, class_obj in classes:
        if class_obj:
            print(f"✓ {class_name} class exists")
        else:
            print(f"✗ {class_name} class not found")
            return False
    
    return True

def test_database_class():
    """Test Database class structure"""
    print("\nTesting Database class methods...")
    
    from database import Database
    
    required_methods = [
        'connect',
        'disconnect',
        'execute_query',
        'fetch_query',
        'fetch_one',
        'get_last_insert_id'
    ]
    
    db = Database()
    
    for method_name in required_methods:
        if hasattr(db, method_name):
            print(f"✓ Database.{method_name} exists")
        else:
            print(f"✗ Database.{method_name} not found")
            return False
    
    return True

def test_model_classes():
    """Test model classes structure"""
    print("\nTesting model class methods...")
    
    from database import Database
    from models import Account, Category, Transaction, Budget
    
    db = Database()
    
    models_methods = {
        'Account': ['create', 'get_all', 'get_by_id', 'update_balance', 'delete'],
        'Category': ['create', 'get_all', 'get_by_type'],
        'Transaction': ['create', 'get_all', 'get_by_account', 'get_summary_by_period', 'delete'],
        'Budget': ['create', 'get_all', 'get_active_budgets']
    }
    
    for model_name, methods in models_methods.items():
        model_class = {
            'Account': Account,
            'Category': Category,
            'Transaction': Transaction,
            'Budget': Budget
        }[model_name]
        
        model_instance = model_class(db)
        
        for method_name in methods:
            if hasattr(model_instance, method_name):
                print(f"✓ {model_name}.{method_name} exists")
            else:
                print(f"✗ {model_name}.{method_name} not found")
                return False
    
    return True

def test_finanz_tool():
    """Test FinanzTool class structure"""
    print("\nTesting FinanzTool class methods...")
    
    from finaz import FinanzTool
    
    required_methods = [
        'connect',
        'disconnect',
        'print_menu',
        'manage_accounts',
        'show_accounts',
        'create_account',
        'add_transaction',
        'show_transactions',
        'manage_categories',
        'manage_budgets',
        'show_overview',
        'show_monthly_report',
        'run'
    ]
    
    app = FinanzTool()
    
    for method_name in required_methods:
        if hasattr(app, method_name):
            print(f"✓ FinanzTool.{method_name} exists")
        else:
            print(f"✗ FinanzTool.{method_name} not found")
            return False
    
    return True

def test_dependencies():
    """Test if required dependencies are available"""
    print("\nTesting dependencies...")
    
    dependencies = [
        'mysql.connector',
        'tabulate',
        'dotenv'
    ]
    
    for dep in dependencies:
        try:
            if dep == 'dotenv':
                __import__('dotenv')
            else:
                __import__(dep)
            print(f"✓ {dep} is available")
        except ImportError:
            print(f"✗ {dep} is not installed")
            print(f"  Install with: pip install {dep if dep != 'dotenv' else 'python-dotenv'}")
            return False
    
    return True

def main():
    """Run all tests"""
    print("="*60)
    print("  Finanzverwaltungstool - Structure Test")
    print("="*60)
    print()
    
    tests = [
        ("Dependencies", test_dependencies),
        ("Module Imports", test_module_imports),
        ("Class Existence", test_class_existence),
        ("Database Class", test_database_class),
        ("Model Classes", test_model_classes),
        ("FinanzTool Class", test_finanz_tool)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ Error during {test_name} test: {e}")
            results.append((test_name, False))
    
    print("\n" + "="*60)
    print("  Test Results Summary")
    print("="*60)
    
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    all_passed = all(result for _, result in results)
    
    print("\n" + "="*60)
    if all_passed:
        print("✓ All tests passed! The application structure is correct.")
        print("\nNext steps:")
        print("1. Configure your .env file with database credentials")
        print("2. Run setup_database.sh to initialize the database")
        print("3. Start the application with: python finaz.py")
    else:
        print("✗ Some tests failed. Please check the errors above.")
    print("="*60)
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())
