import unittest
import threading
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app import create_app, db
from app.models import User, Review
from config import TestConfig

BASE_URL = 'http://localhost:5001'

class SeleniumBase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)

        # Start server thread FIRST, with DB setup inside it
        def run_server():
            with self.app.app_context():
                db.create_all()

                user = User(username='testuser', email='test@test.com', role='user')
                user.set_password('testpass123')
                db.session.add(user)
                db.session.commit()

                self.app.run(port=5001, use_reloader=False, debug=False)

        self.server_thread = threading.Thread(target=run_server)
        self.server_thread.daemon = True
        self.server_thread.start()
        time.sleep(2)  # Wait for server + DB setup

        # Browser
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(5)

    def tearDown(self):
        self.driver.quit()
        if os.path.exists('test_selenium.db'):
            os.remove('test_selenium.db')

    def login(self):
        """Helper to log in via browser"""
        self.driver.get(f'{BASE_URL}/login')
        self.driver.find_element(By.ID, 'email').send_keys('test@test.com')
        self.driver.find_element(By.ID, 'password').send_keys('testpass123')
        self.driver.find_element(By.CLASS_NAME, 'outline-gold-btn').click()
        time.sleep(1)