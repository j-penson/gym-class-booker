#!/usr/bin/python
# coding=utf-8
from collections import namedtuple
import datetime
from selenium.webdriver.remote import webelement
import logging
from app import booker

GymClass = namedtuple('GymClass', 'class_name start_time_str start_time instructor')


class ClassNotFound(Exception):
    """Class not found in timetable"""


class TargetClass:
    def __init__(self, target_class_name: str, target_class_datetime: datetime.datetime):
        self.target_class_name = target_class_name
        self.target_class_datetime = target_class_datetime
        self.target_booking_column = booker.get_booking_column(self.target_class_datetime)
        self.target_booking_start_time = self.target_class_datetime.time()


def get_gym_class(gym_timetable: webelement.WebElement, target_class: TargetClass):
    """For each gym class in the timetable, parse and check if it matched the """
    booking_column = 1
    previous_time = datetime.datetime.strptime('00:00', '%H:%M').time()

    classes = gym_timetable.find_elements_by_css_selector('div[class="fkl-cal-td fkl-class"]')
    logging.info(f'got {len(classes)} classes')

    for class_div in classes:
        gym_class = class_div.text.splitlines()
        if len(gym_class) == 4:
            gym_class_tuple = parse_class(gym_class)

            # The timetable is in a big list rather than columns. When the start time is less than the previous time
            # we've moved to a new column so increase the count
            if gym_class_tuple.start_time < previous_time:
                booking_column += 1

            previous_time = gym_class_tuple.start_time

            logging.debug(f'Parsed: {gym_class_tuple.class_name} at {gym_class_tuple.start_time} in {booking_column}')
            logging.debug(f'Target: {target_class.target_class_name} at {target_class.target_booking_start_time} in '
                          f'{target_class.target_booking_column}')

            # Check for a match on start time, class name and booking column
            if gym_class_tuple.class_name == target_class.target_class_name and \
                    gym_class_tuple.start_time == target_class.target_booking_start_time and \
                    booking_column == target_class.target_booking_column:
                return class_div

    # If we go through everything and don't find a match raise an exception
    raise ClassNotFound


def parse_class(gym_class):
    """Parse the text from the divs in a timetable"""
    # Parse times
    start_time_str, end_time_str = gym_class[1].split(' – ')
    start_time = datetime.datetime.strptime(start_time_str, '%H:%M').time()

    # Put into a namedtuple for easy access
    return GymClass(gym_class[0], start_time_str, start_time, gym_class[2])
