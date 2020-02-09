#!/usr/bin/python
# coding=utf-8
from flask import Flask
from flask_restx import Api, fields
from app import log_setup

app = Flask(__name__)
api = Api(app,
          version='1.0',
          title='Gym Booker API',
          description='An API to log on to the gym website and book classes',
          )

ns = api.namespace('api', description='Gym Class Booking')

gym_class = api.model('gym_class', {
    'draft': fields.Boolean(default=False, description='Draft mode - search only if true, search and book if false'),
    'headless': fields.Boolean(default=False, description='Run Chrome in headless mode'),
    'user': fields.String(required=True, description='Run Chrome in headless mode'),
    'class_name': fields.String(required=True, description='Target gym class to book'),
    'class_datetime': fields.DateTime(required=True, description='Target gym class date and time'),
})


def create_app():
    """Create the Flask application."""
    log_setup.setup()
    return app
