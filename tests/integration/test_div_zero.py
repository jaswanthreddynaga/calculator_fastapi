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

def get_auth_token(username, email, password):
    client.post(
        "/users/register",
        json={"username": username, "email": email, "password": password},
    )
    response = client.post(
        "/users/login",
        json={"email": email, "password": password},
    )
    return response.json()["access_token"]

def test_create_calculation_divide_by_zero(setup_database):
    token = get_auth_token("calcuser_div0", "div0@example.com", "password123")
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post(
        "/calculations",
        headers=headers,
        json={"a": 10, "b": 0, "type": "Divide"},
    )
    assert response.status_code == 400
    data = response.json()
    # Check for 'error' key because of custom exception handler
    assert "Cannot divide by zero" in data["error"]
