import pytest
from fastapi.testclient import TestClient
from app import database
from main import app
from app.models import User

@pytest.fixture(scope="module")
def client():
    database.Base.metadata.create_all(bind=database.engine)
    with TestClient(app) as c:
        yield c
    database.Base.metadata.drop_all(bind=database.engine)


def _clear_users_table():
    db = database.SessionLocal()
    try:
        db.query(User).delete()
        db.commit()
    finally:
        db.close()


def test_create_user_success(client):
    _clear_users_table()
    response = client.post(
        "/users/register",
        json={
            "username": "apiuser",
            "email": "apiuser@example.com",
            "password": "password123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "apiuser"
    assert data["email"] == "apiuser@example.com"
    assert "id" in data
    assert "created_at" in data


def test_create_user_duplicate_username_returns_400(client):
    _clear_users_table()
    payload = {
        "username": "dupuser",
        "email": "dup1@example.com",
        "password": "password123",
    }
    first = client.post("/users/register", json=payload)
    assert first.status_code == 200

    second = client.post(
        "/users/register",
        json={
            "username": "dupuser",  # same username
            "email": "dup2@example.com",
            "password": "password123",
        },
    )
    assert second.status_code == 400
    body = second.json()
    assert "error" in body # Custom exception handler returns "error"
    assert "already exists" in body["error"]


def test_create_user_invalid_email_returns_400(client): # Custom handler returns 400
    _clear_users_table()
    response = client.post(
        "/users/register",
        json={
            "username": "bademail",
            "email": "not-an-email",
            "password": "password123",
        },
    )
    assert response.status_code == 400 # RequestValidationError handled as 400

