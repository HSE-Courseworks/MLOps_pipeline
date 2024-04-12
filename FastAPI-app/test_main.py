import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client

def test_post_request_with_name_ivan(client):
    response = client.post("/user", json={"name": "Иван"})
    assert response.status_code == 200
    assert response.json() == {"message": "Вас зовут Иван"}

def test_post_request_with_name_anna(client):
    response = client.post("/user", json={"name": "Анна"})
    assert response.status_code == 200
    assert response.json() == {"message": "Вас зовут Анна"}

def test_post_request_with_name_sergey(client):
    response = client.post("/user", json={"name": "Сергей"})
    assert response.status_code == 200
    assert response.json() == {"message": "Вас зовут Сергей"}

def test_post_request_without_user_input(client):
    response = client.post("/user", json={"name": ""})
    assert response.status_code == 200
    assert response.json() == {"message": "Вас зовут "}