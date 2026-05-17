from app.tests.selenium_tests.selenium_test_base import SeleniumBase, BASE_URL
from selenium.webdriver.common.by import By

# This test class focuses on verifying that key pages of the application load correctly.
class TestPageLoad(SeleniumBase):
    # This test checks that the home page loads and contains the expected title.
    def test_home_page_loads(self):
            self.driver.get(f'{BASE_URL}/')
            self.assertIn('Home Page', self.driver.title)

    # This test checks that the login page loads and contains the expected form fields for email and password.
    def test_login_page_loads(self):
        self.driver.get(f'{BASE_URL}/login')
        self.assertIn('Log In', self.driver.title)
        self.assertTrue(self.driver.find_element(By.ID, 'email'))
        self.assertTrue(self.driver.find_element(By.ID, 'password'))

    # This test checks that the sign-up page loads and contains the expected form fields for username and email.
    def test_signup_page_loads(self):
        self.driver.get(f'{BASE_URL}/sign_up')
        self.assertIn('Sign Up', self.driver.title)
        self.assertTrue(self.driver.find_element(By.ID, 'username'))
        self.assertTrue(self.driver.find_element(By.ID, 'email'))

    # This test checks that the search page loads and contains the expected elements, even without a search query.
    def test_search_page_loads(self):
        self.driver.get(f'{BASE_URL}/search')   # no query
        self.assertIn('Search', self.driver.title)
        self.assertTrue(self.driver.find_element(By.ID, 'movie-results'))