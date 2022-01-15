import pytest
from run import app

@pytest.fixture
def server():
    return app
