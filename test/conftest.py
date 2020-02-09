""" Fixtures for Gym Booker application
:usage:
    With pytest unit tests.
:authors
    JP at 20/02/20
"""

import pytest
from app import api


@pytest.fixture
def client():
    """Flask test client with Google Cloud logging client removed."""
    app = api.create_app()
    return app.test_client()
