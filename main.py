#!/usr/bin/python
# coding=utf-8
import datetime
import logging
import sys
from flask import Flask
from flask_restx import Api, Resource

from app import driver, booker, gym_class_parser

app = Flask(__name__)
api = Api(app, version='1.0', title='Gym Booker API',
          description='An API to log on to the gym website and book classes',
          )

# Setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
logger.addHandler(handler)


@api.route('/book')
class GymBooker(Resource):
    def get(self):
        setup = driver.GymDriver(headless=True)
        setup.setup(secret_id='jp')  # nosec

        draft = False

        if not draft:
            nav = booker.GymBooker(setup)
            nav.login()

            target_class = gym_class_parser.TargetClass(target_class_name='HOT HATHA YOGA',
                                                        target_class_datetime=datetime.datetime(2020, 2, 10, 12, 00))

            nav.find_class(target_class)
            booking_message = nav.book_class()
        else:
            booking_message = 'Draft mode'

        logging.info(booking_message)

        return booking_message


if __name__ == '__main__':
    app.run()
