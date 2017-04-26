import unittest
from unittest import TestCase
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os
cwd = os.getcwd()
print(cwd)

class AuthenticationTestCase(TestCase):
    def setUp(self):
	display = Display(visible=0, size=(800, 800))  
	display.start()
        driver = webdriver.Chrome('/root/marketplace/web/client/chromedriver')

    def test_login(self):
        driver = self.driver
        driver.get("http://107.170.77.19:8000/login")
	print('getting test log')
        username = driver.find_element_by_id("username")
        username.send_keys("abc")

        password = driver.find_element_by_id("password")
        password.send_keys("abc")

        driver.find_element_by_xpath("//button[@type='submit' and @value='Submit']").click()

    def test_logout(self):
        driver = self.driver
        driver.get("http://107.170.77.19:8000/login")
	print('test logout')
        username = driver.find_element_by_id("username")
        username.send_keys("abc")

        password = driver.find_element_by_id("password")
        password.send_keys("abc")

        driver.find_element_by_xpath("//button[@type='submit' and @value='Submit']").click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "container-fluid")))

        driver.find_element_by_xpath("//a[@href='/logout']").click()

    def tearDown(self):
      	driver.close()
	display.stop()

if __name__ == '__main__':
	unittest.main()
