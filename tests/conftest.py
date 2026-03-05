import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.models.address import Base  # Corrected import path

# from app.db.session import get_db # Import the dependency
from app.api.dependencies import (
    get_db as override_get_db_dependency,
)  # Alias for clarity

# Database for testing
TEST_DATABASE_URL = "sqlite:///:memory:"

# Create a test engine and session
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ---- Fixtures for Tests ----


@pytest.fixture(scope="session")
def db_engine():
    """
    Provides a SQLAlchemy engine for the test database.
    """
    # Create all tables in the test database
    Base.metadata.create_all(bind=engine)
    yield engine
    # Drop all tables after tests are finished
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(db_engine):
    """
    Provides a transactional database session for each test function.
    Each test function will run in its own transaction, which is then rolled back.
    """
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    # Override the app's get_db dependency to use our test session
    app.dependency_overrides[override_get_db_dependency] = lambda: session

    yield session

    session.close()
    transaction.rollback()  # Rollback changes after each test
    connection.close()


@pytest.fixture(scope="function")
def client(db_session):
    """
    Provides a FastAPI test client that uses our test database session.
    """
    # The `db_session` fixture already overrides get_db for us,
    # so we just need to yield the client.
    with TestClient(app) as test_client:
        yield test_client
