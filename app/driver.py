#!/usr/bin/python
# coding=utf-8
from selenium import webdriver
import chromedriver_binary  # noqa: F401
import logging
from app import read_secrets


class NoCreds(Exception):
    """GYM_CREDS not set"""


class GymDriver:
    def __init__(self, headless=True):
        """Gym navigation object to hold driver, credentials"""
        self.headless = headless
        self.chrome_options = None
        self.driver = None
        self.email = None
        self.password = None
        self.base_url = None

    def setup(self, secret_id):
        """Call setup and creds"""
        self._get_creds(secret_id)
        self._get_driver()
        logging.info('got driver and credentials')

    def _get_creds(self, secret_id):
        """Read secrets"""
        creds = read_secrets.get_creds(secret_id)

        self.email = creds['email']
        self.password = creds['password']
        self.base_url = creds['base_url']

    def _get_driver(self, ):
        """Setup Chrome Driver"""
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--window-size=1420,1080')
        if self.headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.chrome_options = chrome_options
        self.driver = webdriver.Chrome(options=chrome_options)

    def save_test_screenshot(self):
        self.driver.save_screenshot('./screenshots/screenshot_test.png')
