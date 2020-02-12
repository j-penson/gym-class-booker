#!/usr/bin/python
# coding=utf-8
""" Tests for Gym Booker application
:usage:
    Run with every commit.
:authors
    JP at 20/02/20
"""
import pytest
import datetime
from app import booker


def test_compare_url_paths():
    pass


@pytest.mark.parametrize("class_date", [3, -1])
@pytest.mark.xfail(raises=booker.TimingError)
def test_get_booking_column_invalid(class_date):
    """Check bookings outside the valid range return an error"""
    class_date = datetime.datetime.now() + datetime.timedelta(days=class_date)
    booker.get_booking_column(class_date)


@pytest.mark.parametrize("class_date, expected", [(2, 3),
                                                  (1, 2),
                                                  (0.001, 1)])
def test_get_booking_column_valid(class_date, expected):
    """Checking bookings in the valid range return the column number"""
    class_date = datetime.datetime.now() + datetime.timedelta(days=class_date)
    actual = booker.get_booking_column(class_date)
    assert actual == expected, f'Got {actual} when expecting {expected}'
