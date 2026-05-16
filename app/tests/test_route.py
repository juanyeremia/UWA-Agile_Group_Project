import unittest
from app import create_app, db
from config import TestConfig
from app.models import User, Review

# This test case focuses on testing the route functionality of the application.
class RouteTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        user = User(username='testuser', email='test@example.com', role='user')
        user.set_password('initialpassword')
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # Test that the login page laods successfully and returns a 200 status code
    def test_login_page_loads(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)

    # Test that the profile page redirects to the login page when the user is not logged in
    def test_profile_redirects_when_not_logged_in(self):
        response = self.client.get('/profile')
        self.assertEqual(response.status_code, 302)  # Should redirect to login page
    
    # Test that the recent reviews endpoint returns an empty list when there are no reviews in the database
    def test_recent_reviews_empty(self):
        response = self.client.get('/api/reviews/recent')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])  # Should return an empty list when there are no reviews