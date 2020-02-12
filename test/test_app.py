#!/usr/bin/python
# coding=utf-8
""" Tests for Gym Booker application
:usage:
    Run with every commit.
:authors
    JP at 20/02/20
"""


def test_index(client):
    """Check the index page loads."""
    response = client.get('/')
    assert response.status_code == 200
