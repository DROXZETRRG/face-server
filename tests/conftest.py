"""Test configuration and fixtures."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

# Test database URL (use a separate test database)
SQLALCHEMY_DATABASE_URL = "postgresql://faceserver:faceserver123@localhost:5432/faceserver_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture
def client():
    """Create test client."""
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Override dependency
    app.dependency_overrides[get_db] = override_get_db
    
    # Create test client
    with TestClient(app) as c:
        yield c
    
    # Drop tables
    Base.metadata.drop_all(bind=engine)
