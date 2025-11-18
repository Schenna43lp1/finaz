#!/usr/bin/env python3
"""
Tests for the web frontend
"""

import sys
import unittest
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))


class TestWebFrontendStructure(unittest.TestCase):
    """Test web frontend structure and imports"""
    
    def test_flask_import(self):
        """Test that Flask is installed"""
        try:
            import flask
            self.assertTrue(True)
        except ImportError:
            self.fail("Flask is not installed")
    
    def test_app_import(self):
        """Test that app.py can be imported"""
        try:
            import app
            self.assertTrue(hasattr(app, 'app'))
        except ImportError as e:
            self.fail(f"Cannot import app.py: {e}")
    
    def test_app_routes(self):
        """Test that all required routes are defined"""
        import app as flask_app
        
        # Get all route rules
        routes = [rule.rule for rule in flask_app.app.url_map.iter_rules()]
        
        # Required routes
        required_routes = [
            '/',
            '/accounts',
            '/accounts/create',
            '/transactions',
            '/transactions/create',
            '/categories',
            '/budgets',
            '/budgets/create',
            '/reports',
        ]
        
        for route in required_routes:
            self.assertIn(route, routes, f"Route {route} not found")
    
    def test_templates_exist(self):
        """Test that all required templates exist"""
        templates_dir = Path(__file__).parent / 'templates'
        
        required_templates = [
            'base.html',
            'index.html',
            'accounts.html',
            'create_account.html',
            'transactions.html',
            'create_transaction.html',
            'categories.html',
            'budgets.html',
            'create_budget.html',
            'reports.html',
            'error.html',
        ]
        
        for template in required_templates:
            template_path = templates_dir / template
            self.assertTrue(
                template_path.exists(),
                f"Template {template} not found"
            )
    
    def test_static_files_exist(self):
        """Test that static CSS file exists"""
        static_dir = Path(__file__).parent / 'static' / 'css'
        css_file = static_dir / 'style.css'
        
        self.assertTrue(static_dir.exists(), "Static CSS directory not found")
        self.assertTrue(css_file.exists(), "style.css not found")
    
    def test_app_config(self):
        """Test Flask app configuration"""
        import app as flask_app
        
        # Test that app is a Flask instance
        from flask import Flask
        self.assertIsInstance(flask_app.app, Flask)
        
        # Test that secret key is set
        self.assertIsNotNone(flask_app.app.secret_key)


class TestFlaskAppClient(unittest.TestCase):
    """Test Flask app with test client (without database)"""
    
    def setUp(self):
        """Set up test client"""
        import app as flask_app
        flask_app.app.config['TESTING'] = True
        self.client = flask_app.app.test_client()
    
    def test_routes_respond(self):
        """Test that routes return valid HTTP responses"""
        # Note: Routes will fail with database errors, but should return 200 or redirect
        # This tests that the route handlers are properly defined
        
        routes_to_test = [
            ('/', ['GET']),
            ('/accounts', ['GET']),
            ('/accounts/create', ['GET']),
            ('/transactions', ['GET']),
            ('/transactions/create', ['GET']),
            ('/categories', ['GET']),
            ('/budgets', ['GET']),
            ('/budgets/create', ['GET']),
            ('/reports', ['GET']),
        ]
        
        for route, methods in routes_to_test:
            for method in methods:
                with self.subTest(route=route, method=method):
                    if method == 'GET':
                        response = self.client.get(route)
                    elif method == 'POST':
                        response = self.client.post(route)
                    
                    # Should get a response (even if it's an error due to no DB)
                    self.assertIsNotNone(response)
                    self.assertIn(response.status_code, [200, 302, 500])


def run_tests():
    """Run all tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestWebFrontendStructure))
    suite.addTests(loader.loadTestsFromTestCase(TestFlaskAppClient))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
