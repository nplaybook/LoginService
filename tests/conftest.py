import pytest
from run import app

@pytest.fixture
def server():
    app.config["TESTING"] = True
    with app.app_context():
        with app.test_client() as server:
            yield server
