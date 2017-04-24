from django.test import TestCase

import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


class LoginPageTestCase(TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome('./client/chromedriver_linux64')

    def test_login(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/login")

        login = driver.find_element_by_id("username")
        login.send_keys("abc")

        password = driver.find_element_by_id("password")
        password.send_keys("abc")

        driver.find_element_by_xpath("//button[@type='submit' and @value='Submit']").click()

    def tearDown(self):
        self.driver.close()