import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app
from app.rate_limit import reset_rate_limits

# These imports make sure SQLAlchemy knows about all database tables during tests.
from app.models.user import User
from app.models.note import Note
from app.models.audit_log import AuditLog


TEST_DATABASE_URL = "sqlite:///./test_secure_notes.db"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)


@pytest.fixture()
def db_session():
    reset_rate_limits()
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture()
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture()
def registered_user(client):
    user_data = {
        "email": "dana@example.com",
        "password": "Password123!"
    }

    response = client.post("/auth/register", json=user_data)

    assert response.status_code == 201

    return user_data


@pytest.fixture()
def auth_headers(client, registered_user):
    response = client.post("/auth/login", json=registered_user)

    assert response.status_code == 200

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }
