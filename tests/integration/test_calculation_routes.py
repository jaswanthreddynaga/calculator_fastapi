from fastapi.testclient import TestClient
from app import database
from app.models import User, Calculation
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

def test_create_calculation(setup_database):
    token = get_auth_token("calcuser_create", "calc_create@example.com", "password123")
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post(
        "/calculations",
        headers=headers,
        json={"a": 10, "b": 5, "type": "Add"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == 15
    assert data["type"] == "Add"

def test_read_calculations(setup_database):
    token = get_auth_token("calcuser_read_all", "calc_read_all@example.com", "password123")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create a calculation
    client.post(
        "/calculations",
        headers=headers,
        json={"a": 10, "b": 5, "type": "Add"},
    )

    response = client.get("/calculations", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_read_calculation_by_id(setup_database):
    token = get_auth_token("calcuser_read", "calc_read@example.com", "password123")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create a calculation first
    create_res = client.post(
        "/calculations",
        headers=headers,
        json={"a": 20, "b": 4, "type": "Divide"},
    )
    calc_id = create_res.json()["id"]

    response = client.get(f"/calculations/{calc_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == calc_id
    assert data["result"] == 5

def test_update_calculation(setup_database):
    token = get_auth_token("calcuser_update", "calc_update@example.com", "password123")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create a calculation first
    create_res = client.post(
        "/calculations",
        headers=headers,
        json={"a": 10, "b": 5, "type": "Multiply"},
    )
    calc_id = create_res.json()["id"]

    # Update it
    response = client.put(
        f"/calculations/{calc_id}",
        headers=headers,
        json={"a": 10, "b": 2, "type": "Divide"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == 5
    assert data["type"] == "Divide"

def test_delete_calculation(setup_database):
    token = get_auth_token("calcuser_delete", "calc_delete@example.com", "password123")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create a calculation first
    create_res = client.post(
        "/calculations",
        headers=headers,
        json={"a": 50, "b": 10, "type": "Subtract"},
    )
    calc_id = create_res.json()["id"]

    # Delete it
    response = client.delete(f"/calculations/{calc_id}", headers=headers)
    assert response.status_code == 200
    
    # Verify it's gone
    get_res = client.get(f"/calculations/{calc_id}", headers=headers)
    assert get_res.status_code == 404

def test_user_isolation(setup_database):
    # User 1
    token1 = get_auth_token("user1", "user1@example.com", "password123")
    headers1 = {"Authorization": f"Bearer {token1}"}
    create_res1 = client.post(
        "/calculations",
        headers=headers1,
        json={"a": 1, "b": 1, "type": "Add"},
    )
    calc_id1 = create_res1.json()["id"]

    # User 2
    token2 = get_auth_token("user2", "user2@example.com", "password123")
    headers2 = {"Authorization": f"Bearer {token2}"}
    
    # User 2 tries to read User 1's calculation
    response = client.get(f"/calculations/{calc_id1}", headers=headers2)
    assert response.status_code == 404

    # User 2 tries to update User 1's calculation
    response = client.put(
        f"/calculations/{calc_id1}",
        headers=headers2,
        json={"a": 2, "b": 2, "type": "Add"},
    )
    assert response.status_code == 404

    # User 2 tries to delete User 1's calculation
    response = client.delete(f"/calculations/{calc_id1}", headers=headers2)
    assert response.status_code == 404
