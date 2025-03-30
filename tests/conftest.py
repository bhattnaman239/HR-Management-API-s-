import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.dependencies import get_db
from app.database.database import Base
from app.models import User
from app.utils.security import get_password_hash

TEST_DATABASE_URL = "sqlite:///./test_db.sqlite3"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    """Yield a test DB session instead of the production DB."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session", autouse=True)
def seed_roles():
    """
    Ensure that exactly three user records exist in the database:
    1) admin_test (role=admin)
    2) test_user  (role=user)
    3) test_reader (role=reader)
    """
    db = TestingSessionLocal()
    try:
        # Check for admin
        existing_admin = db.query(User).filter_by(role="admin").first()
        if not existing_admin:
            admin = User(
                name="Admin",
                username="admin_test",
                password=get_password_hash("Test@1234"),
                role="admin"
            )
            db.add(admin)
            db.commit()

        # Check for user
        existing_user = db.query(User).filter_by(role="user").first()
        if not existing_user:
            user = User(
                name="User",
                username="test_user",
                password=get_password_hash("Test@1234"),
                role="user"
            )
            db.add(user)
            db.commit()

        # Check for reader
        existing_reader = db.query(User).filter_by(role="reader").first()
        if not existing_reader:
            reader = User(
                name="Reader",
                username="test_reader",
                password=get_password_hash("Test@1234"),
                role="reader"
            )
            db.add(reader)
            db.commit()
    finally:
        db.close()

@pytest.fixture(scope="session")
def client():
    """Provide a TestClient for making HTTP requests in tests."""
    with TestClient(app) as c:
        yield c