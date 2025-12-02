from fastapi.testclient import TestClient
from app import database
from main import app
import pytest

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_database():
    database.Base.metadata.create_all(bind=database.engine)
    yield
    database.Base.metadata.drop_all(bind=database.engine)

def test_register_user(setup_database):
    response = client.post(
        "/users/register",
        json={"username": "testuser", "email": "test@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_register_existing_user(setup_database):
    response = client.post(
        "/users/register",
        json={"username": "testuser", "email": "test@example.com", "password": "password123"},
    )
    assert response.status_code == 400

def test_login_user(setup_database):
    response = client.post(
        "/users/login",
        json={"username": "testuser", "email": "test@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Login successful"
    assert "user_id" in data

def test_login_invalid_credentials(setup_database):
    response = client.post(
        "/users/login",
        json={"username": "testuser", "email": "test@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401
