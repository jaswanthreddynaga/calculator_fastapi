from app.security import hash_password, verify_password


def test_hash_password_changes_value():
    password = "mysecretpassword"
    hashed = hash_password(password)
    assert hashed != password
    assert isinstance(hashed, str)


def test_verify_password_success_and_failure():
    password = "anothersecret"
    hashed = hash_password(password)
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpassword", hashed) is False
