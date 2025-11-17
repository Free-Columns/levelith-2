"""
Unit tests for user API endpoints

Comprehensive tests for user CRUD operations via REST API.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database import Base, get_db
from backend.main import app


# Test database setup
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_database():
    """Create and drop database for each test."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "SecurePassword123!",
        "profile_data": {
            "display_name": "Test User",
            "bio": "Test bio"
        }
    }


class TestUserCreation:
    """Test suite for user creation."""

    def test_create_user_success(self, client, sample_user_data):
        """Test successful user creation."""
        response = client.post("/api/v1/users/", json=sample_user_data)
        assert response.status_code == 201

        data = response.json()
        assert data["username"] == sample_user_data["username"]
        assert data["email"] == sample_user_data["email"]
        assert "id" in data
        assert "password" not in data  # Password should not be in response

    def test_create_user_duplicate_username(self, client, sample_user_data):
        """Test creating user with duplicate username fails."""
        client.post("/api/v1/users/", json=sample_user_data)
        response = client.post("/api/v1/users/", json=sample_user_data)

        assert response.status_code == 409
        assert "username" in response.json()["detail"].lower()

    def test_create_user_duplicate_email(self, client, sample_user_data):
        """Test creating user with duplicate email fails."""
        client.post("/api/v1/users/", json=sample_user_data)

        different_username = sample_user_data.copy()
        different_username["username"] = "different"
        response = client.post("/api/v1/users/", json=different_username)

        assert response.status_code == 409
        assert "email" in response.json()["detail"].lower()

    def test_create_user_invalid_username(self, client, sample_user_data):
        """Test creating user with invalid username."""
        invalid_data = sample_user_data.copy()
        invalid_data["username"] = "ab"  # Too short

        response = client.post("/api/v1/users/", json=invalid_data)
        assert response.status_code == 422

    def test_create_user_invalid_email(self, client, sample_user_data):
        """Test creating user with invalid email."""
        invalid_data = sample_user_data.copy()
        invalid_data["email"] = "invalid-email"

        response = client.post("/api/v1/users/", json=invalid_data)
        assert response.status_code == 422

    def test_create_user_weak_password(self, client, sample_user_data):
        """Test creating user with weak password."""
        invalid_data = sample_user_data.copy()
        invalid_data["password"] = "weak"  # Too short

        response = client.post("/api/v1/users/", json=invalid_data)
        assert response.status_code == 422


class TestUserRetrieval:
    """Test suite for retrieving users."""

    def test_get_user_by_id(self, client, sample_user_data):
        """Test retrieving user by ID."""
        create_response = client.post("/api/v1/users/", json=sample_user_data)
        user_id = create_response.json()["id"]

        response = client.get(f"/api/v1/users/{user_id}")
        assert response.status_code == 200

        data = response.json()
        assert data["id"] == user_id
        assert data["username"] == sample_user_data["username"]

    def test_get_nonexistent_user(self, client):
        """Test retrieving non-existent user returns 404."""
        response = client.get("/api/v1/users/nonexistent-id")
        assert response.status_code == 404

    def test_list_users(self, client, sample_user_data):
        """Test listing users."""
        # Create multiple users
        for i in range(3):
            data = sample_user_data.copy()
            data["username"] = f"user{i}"
            data["email"] = f"user{i}@example.com"
            client.post("/api/v1/users/", json=data)

        response = client.get("/api/v1/users/")
        assert response.status_code == 200

        data = response.json()
        assert len(data) == 3

    def test_list_users_pagination(self, client, sample_user_data):
        """Test user list pagination."""
        # Create 5 users
        for i in range(5):
            data = sample_user_data.copy()
            data["username"] = f"user{i}"
            data["email"] = f"user{i}@example.com"
            client.post("/api/v1/users/", json=data)

        # Get first page
        response = client.get("/api/v1/users/?skip=0&limit=2")
        assert response.status_code == 200
        assert len(response.json()) == 2

        # Get second page
        response = client.get("/api/v1/users/?skip=2&limit=2")
        assert response.status_code == 200
        assert len(response.json()) == 2


class TestUserUpdate:
    """Test suite for updating users."""

    def test_update_user_email(self, client, sample_user_data):
        """Test updating user email."""
        create_response = client.post("/api/v1/users/", json=sample_user_data)
        user_id = create_response.json()["id"]

        update_data = {"email": "newemail@example.com"}
        response = client.patch(f"/api/v1/users/{user_id}", json=update_data)

        assert response.status_code == 200
        assert response.json()["email"] == "newemail@example.com"

    def test_update_user_profile_data(self, client, sample_user_data):
        """Test updating user profile data."""
        create_response = client.post("/api/v1/users/", json=sample_user_data)
        user_id = create_response.json()["id"]

        update_data = {
            "profile_data": {
                "new_field": "new_value"
            }
        }
        response = client.patch(f"/api/v1/users/{user_id}", json=update_data)

        assert response.status_code == 200
        assert "new_field" in response.json()["profile_data"]

    def test_update_nonexistent_user(self, client):
        """Test updating non-existent user returns 404."""
        update_data = {"email": "new@example.com"}
        response = client.patch("/api/v1/users/nonexistent-id", json=update_data)
        assert response.status_code == 404


class TestUserDeletion:
    """Test suite for deleting users."""

    def test_delete_user(self, client, sample_user_data):
        """Test deleting a user."""
        create_response = client.post("/api/v1/users/", json=sample_user_data)
        user_id = create_response.json()["id"]

        response = client.delete(f"/api/v1/users/{user_id}")
        assert response.status_code == 204

        # Verify user is deleted
        get_response = client.get(f"/api/v1/users/{user_id}")
        assert get_response.status_code == 404

    def test_delete_nonexistent_user(self, client):
        """Test deleting non-existent user returns 404."""
        response = client.delete("/api/v1/users/nonexistent-id")
        assert response.status_code == 404


class TestUserLogin:
    """Test suite for user authentication."""

    def test_login_success(self, client, sample_user_data):
        """Test successful login."""
        client.post("/api/v1/users/", json=sample_user_data)

        login_data = {
            "username": sample_user_data["username"],
            "password": sample_user_data["password"]
        }
        response = client.post("/api/v1/users/login", json=login_data)

        assert response.status_code == 200
        assert "user_id" in response.json()

    def test_login_invalid_credentials(self, client, sample_user_data):
        """Test login with invalid credentials."""
        client.post("/api/v1/users/", json=sample_user_data)

        login_data = {
            "username": sample_user_data["username"],
            "password": "wrong_password"
        }
        response = client.post("/api/v1/users/login", json=login_data)

        assert response.status_code == 401

    def test_login_nonexistent_user(self, client):
        """Test login with non-existent user."""
        login_data = {
            "username": "nonexistent",
            "password": "password123"
        }
        response = client.post("/api/v1/users/login", json=login_data)

        assert response.status_code == 401
