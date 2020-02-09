#!/usr/bin/python
# coding=utf-8
from urllib import parse
import logging
import datetime
from app import website_utils, gym_class_parser


class BookingError(Exception):
    """Base booking exception"""


class LoginError(BookingError):
    """Errors logging in"""


class TimetableError(BookingError):
    """Errors finding classes"""


class TimingError(BookingError):
    """Too early or late to book"""


class GymBooker:
    def __init__(self, driver):
        self.driver = driver.driver
        self.email = driver.email
        self.password = driver.password
        self.base_url = driver.base_url
        self.target_class = None

    def login(self):
        """Login to website"""
        login_url = self._get_url('login')
        target_url = self._get_url('members')
        self.driver.get(login_url)
        self.driver.find_element_by_name('email').send_keys(self.email)
        self.driver.find_element_by_name('password').send_keys(self.password)
        self.driver.find_element_by_css_selector('input[type="submit"]').click()

        website_utils.sleep()

        if not website_utils.compare_url_paths(self.driver.current_url, target_url):
            logging.error(f'{self.driver.current_url} when expecting {target_url}')
            raise LoginError

        logging.info('successfully logged in')

    def find_class(self, target_class: gym_class_parser.TargetClass):
        self.target_class = target_class

        # Get timetable page and wait for load
        class_url = self._get_url('timetable')
        self.driver.get(class_url)
        website_utils.sleep()

        # Get whole timetable and specific class
        gym_timetable = self.driver.find_element_by_xpath('/html/body/main/div[5]/div/div[2]/div[1]/*')

        gym_class_parser.get_gym_class(gym_timetable, target_class) \
            .click()
        website_utils.sleep(1)

    def book_class(self) -> list:
        """Book the selected class and return the message"""
        try:
            book_div = self.driver.find_element_by_css_selector('div[class="fkl-modal-inner"] input[value="Book"]')
        except Exception as e:
            logging.warning(f'Book option not found so looking for Join Waiting List - error {e}')
            book_div = self.driver.find_element_by_css_selector(
                'div[class="fkl-modal-inner"] input[value = "Join Waiting List"]')

        website_utils.sleep(1)
        book_div.click()

        booking_message_div = self.driver.find_element_by_css_selector('div[class="fkl-modal-inner"]')
        return booking_message_div.text.splitlines()

    def _get_url(self, url):
        return parse.urljoin(self.base_url, url, '/')


def get_booking_column(class_datetime: datetime.datetime) -> int:
    """Get the column on the timetable page"""
    booking_datetime = class_datetime - datetime.timedelta(days=2)
    now_datetime = datetime.datetime.now()

    if now_datetime <= booking_datetime:
        booking_datetime = datetime.datetime.now()

    if now_datetime >= class_datetime:
        logging.error(f'booking_datetime {booking_datetime} after current datetime, class passed')
        raise TimingError
    elif now_datetime >= booking_datetime:
        booking_column = 1 + (class_datetime.day - now_datetime.day)
    else:
        booking_column = 3 + (booking_datetime.day - now_datetime.day)

    logging.info(f'booking column is {booking_column}')

    return booking_column
