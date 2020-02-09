#!/usr/bin/python
# coding=utf-8
from flask_restx import Resource
import logging
from app import driver, booker, gym_class_parser, api, log_setup


@api.ns.route('/book')
class GymBooker(Resource):

    @api.ns.doc('gym_class')
    @api.ns.expect(api.gym_class)
    @api.ns.marshal_with(api.gym_class, code=201)
    def post(self):

        headless = self.api.payload['headless']
        user = self.api.payload['user']
        draft = self.api.payload['draft']

        setup = driver.GymDriver(headless=headless)
        setup.setup(secret_id=user)

        if draft:
            booking_message = 'Draft mode'

        else:
            nav = booker.GymBooker(setup)
            nav.login()

            target_class = gym_class_parser.TargetClass(target_class_name=self.api.payload['class_name'],
                                                        target_class_datetime=self.api.payload['class_datetime'])

            nav.find_class(target_class)
            booking_message = nav.book_class()

        logging.info(booking_message)

        return booking_message


log_setup.setup()
app = api.app
app.run()
