import pytest
from fastapi.testclient import TestClient

from main import app
from app.database import Base, engine, SessionLocal
from app.models import User


@pytest.fixture(scope="module")
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)


def _clear_users_table():
    db = SessionLocal()
    try:
        db.query(User).delete()
        db.commit()
    finally:
        db.close()


def test_create_user_success(client):
    _clear_users_table()
    response = client.post(
        "/users",
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
    first = client.post("/users", json=payload)
    assert first.status_code == 200

    second = client.post(
        "/users",
        json={
            "username": "dupuser",  # same username
            "email": "dup2@example.com",
            "password": "password123",
        },
    )
    assert second.status_code == 400
    assert "already exists" in second.json()["detail"]


def test_create_user_invalid_email_returns_422(client):
    _clear_users_table()
    response = client.post(
        "/users",
        json={
            "username": "bademail",
            "email": "not-an-email",
            "password": "password123",
        },
    )
    assert response.status_code == 422
