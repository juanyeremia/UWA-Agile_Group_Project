import unittest
import multiprocessing
import os
import tempfile


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from app import create_app, db
from app.models import User
from config import TestConfig



LOCAL_HOST = "http://127.0.0.1:5000"


class SeleniumTestConfig(TestConfig):
    SQLALCHEMY_DATABASE_URI = None


def run_test_server(database_path):
    # The Flask app in the child process must point at the same temp DB file.
    SeleniumTestConfig.SQLALCHEMY_DATABASE_URI = f"sqlite:///{database_path}"
    app = create_app(SeleniumTestConfig)
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)


class TestAuthentication(unittest.TestCase):
    def setUp(self):
        # Use a file-backed test DB so both the test process and Flask process can share it.
        file_descriptor, self.database_path = tempfile.mkstemp(suffix=".db")
        os.close(file_descriptor)

        SeleniumTestConfig.SQLALCHEMY_DATABASE_URI = f"sqlite:///{self.database_path}"
        self.testApp = create_app(SeleniumTestConfig)
        self.app_context = self.testApp.app_context()
        self.app_context.push()
        db.create_all()
        # Create a test user to use for login tests.
        self.test_user = User(
            username='testuser',
            email='test@example.com',
            role='user'
        )
        self.test_user.set_password('Qwerpassword!1')
        db.session.add(self.test_user)
        db.session.commit()

        # Selenium needs a live HTTP server, so the app runs in a separate process.
        self.server_process = multiprocessing.Process(
            target=run_test_server,
            args=(self.database_path,)
        )
        self.server_process.start()

        # Set up Chrome options for headless testing
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1400,1200")

        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.get(LOCAL_HOST)


    def tearDown(self):
        self.driver.quit()
        self.server_process.terminate()
        self.server_process.join() 

        # Clean up the shared temp DB after each test run.
        db.session.remove()
        db.drop_all()
        db.engine.dispose()
        self.app_context.pop()

        if os.path.exists(self.database_path):
            os.remove(self.database_path)

    def user_log_in(self):
        test_password = 'Qwerpassword!1'
        self.driver.get(f"{LOCAL_HOST}/login")

        # Fill and submit the same form a browser user would use.
        self.wait.until(EC.visibility_of_element_located((By.ID, "email"))).send_keys(self.test_user.email)
        self.driver.find_element(By.ID, "password").send_keys(test_password)
        self.driver.find_element(By.CSS_SELECTOR, "#loginForm input[type='submit']").click()

    def test_edit_profile(self):
        self.user_log_in()
        new_username = "updateduser"
        new_email = "updated@example.com"
        new_bio = "new_bio"
        
        # Navigate to the profile page
        self.wait.until(EC.presence_of_element_located((By.LINK_TEXT, "My Profile"))).click()

        # Click the edit profile button
        self.wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Edit Profile"))).click()

        # Fill in the edit profile form with new values
        self.driver.find_element(By.NAME, "username").clear()
        self.driver.find_element(By.NAME, "email").clear()
        self.driver.find_element(By.NAME, "bio").clear()
        self.driver.find_element(By.NAME, "username").send_keys(new_username)
        self.driver.find_element(By.NAME, "email").send_keys(new_email)
        self.driver.find_element(By.NAME, "bio").send_keys(new_bio)
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # Complete the profile update and the changes
        self.wait.until(EC.url_contains("/profile"))
        self.assertIn("Profile", self.driver.title)
        self.assertIn("/profile", self.driver.current_url)
        self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
        displayed_username = self.driver.find_element(By.NAME, "username").get_attribute("value")
        displayed_email = self.driver.find_element(By.NAME, "email").get_attribute("value")
        displayed_bio = self.driver.find_element(By.NAME, "bio").get_attribute("value")
        self.assertEqual(displayed_username, new_username)
        self.assertEqual(displayed_email, new_email)
        self.assertEqual(displayed_bio, new_bio)


if __name__ == "__main__":
    unittest.main()