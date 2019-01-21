import pytest
from stlfed_py.flask_app.app import create_app
import os

@pytest.fixture
def app():
    # Not 100% sure why, but both of these appear in the Flask docs. They might
    # be redundant.
    app = create_app({'TESTING': True})
    app.testing = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def teardown():
    """
    Dummy 'test' fixture for teardown functionality, like removing SQLite DB,
    etc.
    """
    os.remove('test.db')
