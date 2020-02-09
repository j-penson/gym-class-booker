import pytest
from app import api


@pytest.fixture(autouse=True)
def env_setup(monkeypatch):
    """Mock the credentials environment variable for when the Google logging client is initialised."""
    monkeypatch.setenv('GOOGLE_APPLICATION_CREDENTIALS',
                       './test/mock-secrets/sample-creds.json')


@pytest.fixture
def client():
    """Flask test client with Google Cloud logging client removed."""
    return api.app.test_client()
