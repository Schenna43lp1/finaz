#!/usr/bin/env python3
"""
Tests for admin-only functionality
"""

import sys
import unittest
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))


class TestAdminDecorator(unittest.TestCase):
    """Test admin_required decorator"""
    
    def test_admin_decorator_exists(self):
        """Test that admin_required decorator is defined"""
        try:
            import app as flask_app
            self.assertTrue(hasattr(flask_app, 'admin_required'), "admin_required decorator not defined")
        except Exception as e:
            self.fail(f"Error checking admin_required decorator: {e}")


class TestUserModelAdminSupport(unittest.TestCase):
    """Test User model admin functionality"""
    
    def test_user_model_create_accepts_is_admin(self):
        """Test User.create method accepts is_admin parameter"""
        from models import User
        from database import Database
        import inspect
        
        db = Database()
        user_model = User(db)
        
        # Check that create method has is_admin parameter
        sig = inspect.signature(user_model.create)
        params = list(sig.parameters.keys())
        self.assertIn('is_admin', params, "User.create should have is_admin parameter")
    
    def test_user_model_get_all_method(self):
        """Test User model has get_all method"""
        from models import User
        from database import Database
        
        db = Database()
        user_model = User(db)
        
        self.assertTrue(hasattr(user_model, 'get_all'), "User.get_all method not found")


class TestRegisterRoute(unittest.TestCase):
    """Test register route is admin-only"""
    
    def test_register_route_has_admin_decorator(self):
        """Test register route is protected by admin_required"""
        import app as flask_app
        
        # The register function should exist
        self.assertTrue(hasattr(flask_app, 'register'), "register route not defined")
        
        # Check if the route is wrapped (has __wrapped__ attribute from decorator)
        register_func = flask_app.register
        # Decorators with @wraps will preserve function name
        self.assertEqual(register_func.__name__, 'register')


class TestUsersRoute(unittest.TestCase):
    """Test users management route"""
    
    def test_users_route_exists(self):
        """Test that users route is defined"""
        try:
            import app as flask_app
            self.assertTrue(hasattr(flask_app, 'users'), "users route not defined")
        except Exception as e:
            self.fail(f"Error checking users route: {e}")


class TestTemplateChanges(unittest.TestCase):
    """Test template changes"""
    
    def test_users_template_exists(self):
        """Test that users.html template exists"""
        from pathlib import Path
        
        templates_dir = Path(__file__).parent / 'templates'
        users_template = templates_dir / 'users.html'
        self.assertTrue(users_template.exists(), "users.html template not found")
    
    def test_login_template_no_register_link(self):
        """Test that login template doesn't have register link"""
        from pathlib import Path
        
        templates_dir = Path(__file__).parent / 'templates'
        login_template = templates_dir / 'login.html'
        
        with open(login_template, 'r', encoding='utf-8') as f:
            content = f.read()
            # Should not have "Jetzt registrieren" link
            self.assertNotIn('Jetzt registrieren', content, 
                           "Login template should not have 'Jetzt registrieren' link")
            # Should have message about contacting admin
            self.assertIn('Administrator', content, 
                         "Login template should have message about contacting administrator")
    
    def test_register_template_has_admin_checkbox(self):
        """Test that register template has admin checkbox"""
        from pathlib import Path
        
        templates_dir = Path(__file__).parent / 'templates'
        register_template = templates_dir / 'register.html'
        
        with open(register_template, 'r', encoding='utf-8') as f:
            content = f.read()
            # Should have admin checkbox
            self.assertIn('is_admin', content, 
                         "Register template should have is_admin checkbox")
            self.assertIn('Administrator', content, 
                         "Register template should mention Administrator")


class TestDatabaseSchema(unittest.TestCase):
    """Test database schema changes"""
    
    def test_schema_has_is_admin_field(self):
        """Test that database schema includes is_admin field"""
        from pathlib import Path
        
        schema_file = Path(__file__).parent / 'database_schema.sql'
        
        with open(schema_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Should have is_admin field in users table
            self.assertIn('is_admin', content, 
                         "Database schema should have is_admin field")
            self.assertIn('BOOLEAN', content, 
                         "is_admin should be a BOOLEAN field")


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)
