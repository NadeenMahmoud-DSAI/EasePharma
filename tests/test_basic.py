import unittest
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))  
base_dir = os.path.dirname(current_dir)                
src_path = os.path.join(base_dir, 'src')                

sys.path.insert(0, src_path)

from app import create_app

class BasicTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app({'TESTING': True})
        self.client = self.app.test_client()

    def test_home_page_loads(self):
        """Test 1: Check if the Home Page works (Status 200)"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'EasePharma', response.data)

    def test_admin_redirect(self):
        """Test 2: Check if Admin page is protected (Redirects guest)"""
        response = self.client.get('/admin/products')
        self.assertEqual(response.status_code, 302) 

if __name__ == '__main__':
    print("Running Unit Tests")
    unittest.main()