#!/usr/bin/env python3
"""
Tests for the authentication system
"""

import sys
import unittest
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))


class TestAuthenticationStructure(unittest.TestCase):
    """Test authentication system structure"""
    
    def test_user_model_import(self):
        """Test that User model can be imported"""
        try:
            from models import User
            self.assertIsNotNone(User)
        except ImportError as e:
            self.fail(f"Cannot import User model: {e}")
    
    def test_werkzeug_security_import(self):
        """Test that werkzeug.security is available"""
        try:
            from werkzeug.security import generate_password_hash, check_password_hash
            self.assertIsNotNone(generate_password_hash)
            self.assertIsNotNone(check_password_hash)
        except ImportError as e:
            self.fail(f"Cannot import werkzeug.security: {e}")
    
    def test_password_hashing(self):
        """Test password hashing functionality"""
        from werkzeug.security import generate_password_hash, check_password_hash
        
        password = "test_password_123"
        hashed = generate_password_hash(password)
        
        # Hash should be different from original password
        self.assertNotEqual(password, hashed)
        
        # Verification should work with correct password
        self.assertTrue(check_password_hash(hashed, password))
        
        # Verification should fail with wrong password
        self.assertFalse(check_password_hash(hashed, "wrong_password"))
    
    def test_auth_templates_exist(self):
        """Test that authentication templates exist"""
        from pathlib import Path
        
        templates_dir = Path(__file__).parent / 'templates'
        
        # Check login template
        login_template = templates_dir / 'login.html'
        self.assertTrue(login_template.exists(), "login.html template not found")
        
        # Check register template
        register_template = templates_dir / 'register.html'
        self.assertTrue(register_template.exists(), "register.html template not found")
    
    def test_auth_routes_defined(self):
        """Test that authentication routes are defined in app"""
        try:
            import app as flask_app
            
            # Check for required route functions
            self.assertTrue(hasattr(flask_app, 'login'), "login route not defined")
            self.assertTrue(hasattr(flask_app, 'register'), "register route not defined")
            self.assertTrue(hasattr(flask_app, 'logout'), "logout route not defined")
            self.assertTrue(hasattr(flask_app, 'login_required'), "login_required decorator not defined")
        except Exception as e:
            self.fail(f"Error checking authentication routes: {e}")


class TestUserModel(unittest.TestCase):
    """Test User model functionality (without database)"""
    
    def test_user_model_structure(self):
        """Test User model has required methods"""
        from models import User
        from database import Database
        
        db = Database()
        user_model = User(db)
        
        # Check for required methods
        self.assertTrue(hasattr(user_model, 'create'), "User.create method not found")
        self.assertTrue(hasattr(user_model, 'get_by_username'), "User.get_by_username method not found")
        self.assertTrue(hasattr(user_model, 'verify_password'), "User.verify_password method not found")
        self.assertTrue(hasattr(user_model, 'get_by_id'), "User.get_by_id method not found")


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)
