"""Pytest configuration and fixtures for testing."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app import models

# Create a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_bank_branches.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with test database."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def sample_banks(db_session):
    """Create sample banks for testing."""
    banks = [
        models.Bank(id=1, name="STATE BANK OF INDIA"),
        models.Bank(id=2, name="HDFC BANK"),
        models.Bank(id=3, name="ICICI BANK")
    ]
    for bank in banks:
        db_session.add(bank)
    db_session.commit()
    return banks


@pytest.fixture(scope="function")
def sample_branches(db_session, sample_banks):
    """Create sample branches for testing."""
    branches = [
        models.Branch(
            ifsc="SBIN0000001",
            bank_id=1,
            branch="MUMBAI MAIN",
            address="MUMBAI SAMACHAR MARG, MUMBAI",
            city="MUMBAI",
            district="MUMBAI",
            state="MAHARASHTRA"
        ),
        models.Branch(
            ifsc="HDFC0000001",
            bank_id=2,
            branch="RTGS-HO",
            address="KAMALA MILLS COMPOUND, MUMBAI",
            city="MUMBAI",
            district="MUMBAI",
            state="MAHARASHTRA"
        ),
        models.Branch(
            ifsc="ICIC0000001",
            bank_id=3,
            branch="MUMBAI NARIMAN POINT",
            address="MITTAL TOWER, MUMBAI",
            city="MUMBAI",
            district="MUMBAI",
            state="MAHARASHTRA"
        ),
        models.Branch(
            ifsc="SBIN0000002",
            bank_id=1,
            branch="DELHI MAIN",
            address="11 SANSAD MARG, NEW DELHI",
            city="NEW DELHI",
            district="NEW DELHI",
            state="DELHI"
        )
    ]
    for branch in branches:
        db_session.add(branch)
    db_session.commit()
    return branches
