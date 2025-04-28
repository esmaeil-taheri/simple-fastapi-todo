from fastapi.testclient import TestClient
from src.main import app
from fastapi import status

client = TestClient(app)


def test_app_is_running():
    response = client.get('/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'status': 'Running'}
    