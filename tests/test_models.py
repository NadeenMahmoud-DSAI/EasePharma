import unittest
from src.models.user_model import User  # Adjust import based on your actual structure

class TestUserModel(unittest.TestCase):

    def test_new_user_creation(self):
        """
        Test that a user model is created correctly.
        Functional Requirement: User Signup
        """
        user = User(username="testuser", email="test@example.com", password="password123")
        
        # Assertions
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertNotEqual(user.password, "password123") # Assuming you hash passwords for Security NFR!