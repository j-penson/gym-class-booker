#!/usr/bin/python
# coding=utf-8
from selenium import webdriver
import chromedriver_binary  # noqa: F401
import json
import logging


class GymDriver:
    def __init__(self, headless=True):
        """Gym navigation object to hold driver, credentials"""
        self.headless = headless
        self.chrome_options = None
        self.driver = None
        self.email = None
        self.password = None
        self.base_url = None

    def setup(self):
        """Call setup and creds"""
        self._get_creds()
        self._get_driver()
        logging.info('got driver and credentials')

    def _get_creds(self):
        """Read secrets"""
        with open('./secrets/credentials.json', 'r') as f:
            secrets = json.load(f)
        self.email = secrets['email']
        self.password = secrets['password']
        self.base_url = secrets['base_url']

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
