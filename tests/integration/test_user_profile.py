from fastapi.testclient import TestClient
from app import database
from app.models import User
from main import app
from app.security import verify_password, hash_password
import pytest

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_database():
    database.Base.metadata.create_all(bind=database.engine)
    yield
    database.Base.metadata.drop_all(bind=database.engine)

def get_auth_token(username, email, password):
    # Register user
    client.post(
        "/users/register",
        json={"username": username, "email": email, "password": password},
    )
    # Login user
    response = client.post(
        "/users/login",
        json={"email": email, "password": password},
    )
    return response.json()["access_token"]

def test_update_user_profile(setup_database):
    token = get_auth_token("profile_user", "profile@example.com", "password123")
    headers = {"Authorization": f"Bearer {token}"}

    # Test updating username and email
    response = client.put(
        "/users/me",
        headers=headers,
        json={"username": "newusername", "email": "newemail@example.com"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "newusername"
    assert data["email"] == "newemail@example.com"

    # Verify database update (optional, but good)
    # Since we are using the same app/db instance, we can query directly if needed, 
    # but checking API response is usually sufficient for integration tests.
    # To be safe and simple, we can just check via API
    response = client.get(f"/users/{data['id']}", headers=headers) # Assuming we can read user by ID or similar
    # Actually, main.py has /users/{user_id}
    assert response.json()["username"] == "newusername"

def test_update_user_profile_duplicate_username(setup_database):
    # Create another user
    get_auth_token("other_user", "other@example.com", "password123")
    
    # Create current user
    token = get_auth_token("dup_user", "dup@example.com", "password123")
    headers = {"Authorization": f"Bearer {token}"}

    # Try to update to existing username
    response = client.put(
        "/users/me",
        headers=headers,
        json={"username": "other_user"}
    )
    assert response.status_code == 400
    assert response.json()["error"] == "Username already taken"

def test_change_password(setup_database):
    token = get_auth_token("pwd_user", "pwd@example.com", "password123")
    headers = {"Authorization": f"Bearer {token}"}

    # Test changing password
    response = client.post(
        "/users/me/password",
        headers=headers,
        json={"current_password": "password123", "new_password": "newpassword123"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Password updated successfully"

    # Verify new password works by logging in
    response = client.post(
        "/users/login",
        json={"email": "pwd@example.com", "password": "newpassword123"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_change_password_incorrect_current(setup_database):
    token = get_auth_token("wrong_pwd_user", "wrong_pwd@example.com", "password123")
    headers = {"Authorization": f"Bearer {token}"}

    # Test changing password with incorrect current password
    response = client.post(
        "/users/me/password",
        headers=headers,
        json={"current_password": "wrongpassword", "new_password": "newpassword123"}
    )
    assert response.status_code == 400
    assert response.json()["error"] == "Incorrect current password"
