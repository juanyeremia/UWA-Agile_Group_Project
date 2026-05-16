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

    # Test that the recent reviews endpoint returns the correct data when there are reviews in the database
    def test_recent_reviews_returns_data(self):
        # add a review to the database
        review = Review(movie_id=550, body='Great film', rating=5, user_id=1)
        db.session.add(review) 
        db.session.commit() 

        # test that the recent reviews endpoint returns the review we just added
        response = self.client.get('/api/reviews/recent')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]['movie_id'], 550)
        self.assertEqual(response.json[0]['body'], 'Great film')
    
    # Test that the highest rated movies endpoint returns an empty list when there are no movies in the database
    def test_highest_rated_empty(self):
        response = self.client.get('/api/movies/highest_rated')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    # Test that the highest rated movies endpoint returns the correct data when there are movies in the database
    def test_highest_rated_returns_data(self):
        # add a review to the database
        review = Review(movie_id=550, body='Great', rating=5, user_id=1)
        db.session.add(review)
        db.session.commit()

        # test that the highest rated movies endpoint returns the movie we just added
        response = self.client.get('/api/movies/highest_rated')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['movie_id'], 550)
        self.assertEqual(response.json[0]['avg_rating'], 5.0)