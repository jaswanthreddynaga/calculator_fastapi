from sqlalchemy.exc import IntegrityError

from app.database import Base, SessionLocal, engine
from app.models import User


def setup_module(module):  # noqa: D401
    """Create all tables before tests in this module run."""
    Base.metadata.create_all(bind=engine)


def teardown_module(module):  # noqa: D401
    """Drop all tables after tests in this module run."""
    Base.metadata.drop_all(bind=engine)


def _clear_users_table():
    db = SessionLocal()
    try:
        db.query(User).delete()
        db.commit()
    finally:
        db.close()


def test_user_created_at_and_password_hash_persisted():
    _clear_users_table()
    db = SessionLocal()
    try:
        user = User(
            username="dbuser1",
            email="dbuser1@example.com",
            password_hash="hashed-password",
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        assert user.id is not None
        assert user.created_at is not None
        assert user.password_hash == "hashed-password"
    finally:
        db.close()


def test_user_username_and_email_uniqueness():
    _clear_users_table()
    db = SessionLocal()
    try:
        user1 = User(
            username="uniqueuser",
            email="unique@example.com",
            password_hash="hashed1",
        )
        db.add(user1)
        db.commit()

        user2 = User(
            username="uniqueuser",  # same username
            email="other@example.com",
            password_hash="hashed2",
        )
        db.add(user2)
        try:
            db.commit()
            assert False, "Expected IntegrityError for duplicate username"
        except IntegrityError:
            db.rollback()
    finally:
        db.close()
