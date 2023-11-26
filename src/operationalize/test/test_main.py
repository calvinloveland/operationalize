import pytest


@pytest.fixture
def client():
    from operationalize.main import app

    with app.test_client() as client:
        yield client


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
