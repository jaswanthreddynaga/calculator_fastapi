import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Calculation, User
from app.calculation_factory import CalculationFactory

# Setup test database
# Use SQLite by default for local testing if DATABASE_URL is not set or is the default production one
# But in CI, DATABASE_URL will be set to the postgres service.
# We'll check if we are in CI or just use a separate env var, or just try to use DATABASE_URL.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///:memory:")

connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def db():
    # Create tables
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def test_user(db):
    user = User(username="testuser", email="test@example.com", password_hash="hashedsecret")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def test_create_calculation_record(db, test_user):
    # Use factory to get result
    op_type = "Add"
    a, b = 10, 5
    operation = CalculationFactory.create_operation(op_type)
    result = operation.execute(a, b)

    # Create calculation record
    calc = Calculation(a=a, b=b, type=op_type, result=result, user_id=test_user.id)
    db.add(calc)
    db.commit()
    db.refresh(calc)

    assert calc.id is not None
    assert calc.a == 10
    assert calc.b == 5
    assert calc.type == "Add"
    assert calc.result == 15
    assert calc.user_id == test_user.id
    assert calc.user.username == "testuser"

def test_calculation_retrieval(db, test_user):
    # Retrieve calculations for user
    calcs = db.query(Calculation).filter(Calculation.user_id == test_user.id).all()
    assert len(calcs) >= 1
    assert calcs[0].type == "Add"

def test_invalid_calculation_type(db, test_user):
    # This tests database constraint if we had one, but we only have schema validation.
    # However, we can test that we can save other types.
    calc = Calculation(a=10, b=2, type="Divide", result=5, user_id=test_user.id)
    db.add(calc)
    db.commit()
    
    saved_calc = db.query(Calculation).filter(Calculation.type == "Divide").first()
    assert saved_calc is not None
    assert saved_calc.result == 5
