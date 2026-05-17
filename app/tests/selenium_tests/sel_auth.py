import unittest
import multiprocessing
import os
import tempfile
import time
import uuid

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
        # Create a test user to use for sign-up tests.
        self.test_user = User(
            username='testuser',
            email='test@example.com',
            role='user'
        )
        
        db.session.commit()

        # Selenium needs a live HTTP server, so the app runs in a separate process.
        self.server_process = multiprocessing.Process(
            target=run_test_server,
            args=(self.database_path,)
        )
        self.server_process.start()


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

    def test_user_can_sign_up(self):

        test_password = 'Qwerpassword!1'
        self.driver.get(f"{LOCAL_HOST}/sign_up")

        # Fill and submit the same form a browser user would use.
        self.wait.until(EC.visibility_of_element_located((By.ID, "username"))).send_keys(self.test_user.username)
        self.driver.find_element(By.ID, "email").send_keys(self.test_user.email)
        self.driver.find_element(By.ID, "password").send_keys(test_password)
        self.driver.find_element(By.ID, "confirm_password").send_keys(test_password)
        self.driver.find_element(By.CSS_SELECTOR, "#signUpForm input[type='submit']").click()
        self.wait.until(EC.url_contains("/login"))

        # Refresh the parent-process session before reading data written by the app process.
        db.session.remove()
        created_user = User.query.filter_by(email=self.test_user.email).first()

        # Verify the user was created in the database and has the expected attributes.
        self.assertIsNotNone(created_user)
        self.assertEqual(created_user.username, self.test_user.username)
        self.assertTrue(created_user.check_password(test_password))
        self.assertIn("Log In", self.driver.title)
        self.assertIn("/login", self.driver.current_url)


if __name__ == "__main__":
    unittest.main()