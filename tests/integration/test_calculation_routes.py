from fastapi.testclient import TestClient
from app import database
from app.models import User, Calculation
from main import app
import pytest

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_database():
    database.Base.metadata.create_all(bind=database.engine)
    # Create a test user
    client.post(
        "/users/register",
        json={"username": "calcuser", "email": "calc@example.com", "password": "password123"},
    )
    yield
    database.Base.metadata.drop_all(bind=database.engine)

def test_create_calculation(setup_database):
    # Get user id
    login_res = client.post(
        "/users/login",
        json={"username": "calcuser", "email": "calc@example.com", "password": "password123"},
    )
    user_id = login_res.json()["user_id"]

    response = client.post(
        "/calculations",
        params={"user_id": user_id},
        json={"a": 10, "b": 5, "type": "Add"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == 15
    assert data["type"] == "Add"

def test_read_calculations(setup_database):
    response = client.get("/calculations")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_read_calculation_by_id(setup_database):
    # Get user id
    login_res = client.post(
        "/users/login",
        json={"username": "calcuser", "email": "calc@example.com", "password": "password123"},
    )
    user_id = login_res.json()["user_id"]
    
    # Create a calculation first
    create_res = client.post(
        "/calculations",
        params={"user_id": user_id},
        json={"a": 20, "b": 4, "type": "Divide"},
    )
    calc_id = create_res.json()["id"]

    response = client.get(f"/calculations/{calc_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == calc_id
    assert data["result"] == 5

def test_update_calculation(setup_database):
    # Get user id
    login_res = client.post(
        "/users/login",
        json={"username": "calcuser", "email": "calc@example.com", "password": "password123"},
    )
    user_id = login_res.json()["user_id"]
    
    # Create a calculation first
    create_res = client.post(
        "/calculations",
        params={"user_id": user_id},
        json={"a": 10, "b": 5, "type": "Multiply"},
    )
    calc_id = create_res.json()["id"]

    # Update it
    response = client.put(
        f"/calculations/{calc_id}",
        json={"a": 10, "b": 2, "type": "Divide"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == 5
    assert data["type"] == "Divide"

def test_delete_calculation(setup_database):
    # Get user id
    login_res = client.post(
        "/users/login",
        json={"username": "calcuser", "email": "calc@example.com", "password": "password123"},
    )
    user_id = login_res.json()["user_id"]
    
    # Create a calculation first
    create_res = client.post(
        "/calculations",
        params={"user_id": user_id},
        json={"a": 50, "b": 10, "type": "Subtract"},
    )
    calc_id = create_res.json()["id"]

    # Delete it
    response = client.delete(f"/calculations/{calc_id}")
    assert response.status_code == 200
    
    # Verify it's gone
    get_res = client.get(f"/calculations/{calc_id}")
    assert get_res.status_code == 404
