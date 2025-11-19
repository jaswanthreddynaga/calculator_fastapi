from datetime import datetime

import pytest
from pydantic import ValidationError

from app.schemas import UserCreate


def test_user_create_valid_email():
    data = {"username": "testuser", "email": "test@example.com", "password": "password123"}
    user = UserCreate(**data)
    assert user.email == data["email"]


def test_user_create_invalid_email():
    data = {"username": "testuser", "email": "not-an-email", "password": "password123"}
    with pytest.raises(ValidationError):
        UserCreate(**data)
