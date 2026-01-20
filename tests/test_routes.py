import unittest
from src.app import create_app # Assuming you used the App Factory pattern (Bonus point!)

class TestRoutes(unittest.TestCase):

    def setUp(self):
        """Set up a temporary test client before each test"""
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()

    def test_home_page_status_code(self):
        """
        Test that the home page loads successfully (HTTP 200).
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_login_route_post(self):
        """
        Test that the login route accepts data.
        """
        response = self.client.post('/login', data={
            'username': 'testuser', 
            'password': 'password123'
        })
        # Check if it redirects (302) or returns success depending on your logic
        self.assertEqual(response.status_code, 200)