import unittest
from app import create_app, db
from config import TestConfig
from app.models import User

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        user = User(
            username='testuser',
            email='test@example.com',
            role='user'
        )
        user.set_password('initialpassword')
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        user = db.session.get(User, 1)  # Get the test user
        user.set_password('testpassword')  # Set a password for the user
        self.assertFalse(user.check_password('wrongpassword'))  # Check that the wrong password does
        self.assertTrue(user.check_password('testpassword'))  # Check that the correct password works

    # Ensure that the password is not stored as plaintext in the database
    def test_password_not_stored_as_plaintext(self):
        user = db.session.get(User,1)  # Get the test user
        self.assertNotEqual(user.password_hash, 'initialpassword') # Ensure the password is not stored as plaintext

    # Ensure that the default role is 'user'
    def test_default_role_is_user(self):
        user = db.session.get(User,1)  # Get the test user
        self.assertEqual(user.role, 'user')  # Check that the default role is 'user'

