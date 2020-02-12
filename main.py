#!/usr/bin/python
# coding=utf-8
from flask_restx import Resource
import logging
from app import driver, booker, gym_class_parser, api


@api.ns.route('/book')
class GymBooker(Resource):

    @api.ns.doc('gym_class')
    @api.ns.expect(api.gym_class)
    @api.ns.marshal_with(api.gym_class, code=201)
    def post(self):

        logging.info(f'payload is {self.api.payload}')

        headless = self.api.payload['headless']
        user = self.api.payload['user']

        setup = driver.GymDriver(headless=headless)
        setup.setup(secret_id=user)

        nav = booker.GymBooker(setup)

        # Login to gym website with user credentials
        nav.login()

        # Get the class timetable for the week
        nav.get_classes()

        # Set the target class and book it
        target_class = gym_class_parser.TargetClass(target_class_name=self.api.payload['class_name'],
                                                    target_class_datetime=self.api.payload['class_datetime'])
        booking_message = nav.book_class(target_class)

        logging.info(booking_message)

        return booking_message


app = api.create_app()

if __name__ == "__main__":
    app.run()
