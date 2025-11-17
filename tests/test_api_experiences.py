"""
Unit tests for experience API endpoints

Comprehensive tests for experience CRUD operations via REST API.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database import Base, get_db
from backend.main import app
from backend.models.experience import ExperienceCategory, ExperienceType


# Test database setup
TEST_DATABASE_URL = "sqlite:///./test_exp.db"
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
def test_user(client):
    """Create a test user and return user data."""
    user_data = {
        "username": "expuser",
        "email": "exp@example.com",
        "password": "TestPassword123!"
    }
    response = client.post("/api/v1/users/", json=user_data)
    return response.json()


@pytest.fixture
def sample_experience_data():
    """Sample experience data for testing."""
    return {
        "title": "Software Engineer",
        "description": "Full-stack development",
        "naics_code": "541511",
        "category": ExperienceCategory.WORKPLACE.value,
        "experience_type": ExperienceType.FULL_TIME.value,
        "organization": "Tech Corp",
        "location": "San Francisco, CA",
        "is_current": True,
        "type_specific_data": {"salary_range": "100k-150k"},
        "tags": ["python", "fastapi", "postgresql"],
        "metadata": {}
    }


class TestExperienceCreation:
    """Test suite for experience creation."""

    def test_create_experience_success(self, client, test_user, sample_experience_data):
        """Test successful experience creation."""
        response = client.post(
            f"/api/v1/experiences/?user_id={test_user['id']}",
            json=sample_experience_data
        )
        assert response.status_code == 201

        data = response.json()
        assert data["title"] == sample_experience_data["title"]
        assert data["user_id"] == test_user["id"]
        assert "id" in data

    def test_create_experience_invalid_user(self, client, sample_experience_data):
        """Test creating experience for non-existent user fails."""
        response = client.post(
            "/api/v1/experiences/?user_id=nonexistent",
            json=sample_experience_data
        )
        assert response.status_code == 404

    def test_create_experience_with_fallback_naics(self, client, test_user, sample_experience_data):
        """Test experience creation with invalid NAICS uses fallback."""
        data = sample_experience_data.copy()
        data["naics_code"] = "invalid"

        response = client.post(
            f"/api/v1/experiences/?user_id={test_user['id']}",
            json=data
        )
        assert response.status_code == 201
        assert response.json()["naics_code"] == "123456"  # Fallback code

    def test_create_all_experience_types(self, client, test_user):
        """Test creating all 9 experience types."""
        experience_types = [
            (ExperienceCategory.EDUCATION, ExperienceType.CERTIFICATE),
            (ExperienceCategory.EDUCATION, ExperienceType.DEGREE),
            (ExperienceCategory.EDUCATION, ExperienceType.COURSE),
            (ExperienceCategory.WORKPLACE, ExperienceType.GIG),
            (ExperienceCategory.WORKPLACE, ExperienceType.PART_TIME),
            (ExperienceCategory.WORKPLACE, ExperienceType.FULL_TIME),
            (ExperienceCategory.SKILLS, ExperienceType.SOFT_SKILL),
            (ExperienceCategory.SKILLS, ExperienceType.HARD_SKILL),
            (ExperienceCategory.SKILLS, ExperienceType.NATIVE_SKILL),
        ]

        for category, exp_type in experience_types:
            data = {
                "title": f"Test {exp_type.value}",
                "category": category.value,
                "experience_type": exp_type.value,
                "naics_code": "123456"
            }
            response = client.post(
                f"/api/v1/experiences/?user_id={test_user['id']}",
                json=data
            )
            assert response.status_code == 201


class TestExperienceRetrieval:
    """Test suite for retrieving experiences."""

    def test_get_experience_by_id(self, client, test_user, sample_experience_data):
        """Test retrieving experience by ID."""
        create_response = client.post(
            f"/api/v1/experiences/?user_id={test_user['id']}",
            json=sample_experience_data
        )
        exp_id = create_response.json()["id"]

        response = client.get(f"/api/v1/experiences/{exp_id}")
        assert response.status_code == 200
        assert response.json()["id"] == exp_id

    def test_get_nonexistent_experience(self, client):
        """Test retrieving non-existent experience returns 404."""
        response = client.get("/api/v1/experiences/nonexistent")
        assert response.status_code == 404

    def test_list_experiences(self, client, test_user, sample_experience_data):
        """Test listing experiences."""
        # Create multiple experiences
        for i in range(3):
            data = sample_experience_data.copy()
            data["title"] = f"Experience {i}"
            client.post(
                f"/api/v1/experiences/?user_id={test_user['id']}",
                json=data
            )

        response = client.get("/api/v1/experiences/")
        assert response.status_code == 200
        assert response.json()["total"] == 3

    def test_list_experiences_filter_by_user(self, client, test_user, sample_experience_data):
        """Test filtering experiences by user ID."""
        # Create experience for test user
        client.post(
            f"/api/v1/experiences/?user_id={test_user['id']}",
            json=sample_experience_data
        )

        response = client.get(f"/api/v1/experiences/?user_id={test_user['id']}")
        assert response.status_code == 200
        assert response.json()["total"] >= 1

    def test_list_experiences_filter_by_category(self, client, test_user, sample_experience_data):
        """Test filtering experiences by category."""
        client.post(
            f"/api/v1/experiences/?user_id={test_user['id']}",
            json=sample_experience_data
        )

        response = client.get(
            f"/api/v1/experiences/?category={ExperienceCategory.WORKPLACE.value}"
        )
        assert response.status_code == 200

    def test_list_experiences_pagination(self, client, test_user, sample_experience_data):
        """Test experience list pagination."""
        # Create 5 experiences
        for i in range(5):
            data = sample_experience_data.copy()
            data["title"] = f"Experience {i}"
            client.post(
                f"/api/v1/experiences/?user_id={test_user['id']}",
                json=data
            )

        response = client.get("/api/v1/experiences/?page=1&page_size=2")
        assert response.status_code == 200
        assert len(response.json()["items"]) == 2
        assert response.json()["has_more"] is True


class TestExperienceUpdate:
    """Test suite for updating experiences."""

    def test_update_experience_title(self, client, test_user, sample_experience_data):
        """Test updating experience title."""
        create_response = client.post(
            f"/api/v1/experiences/?user_id={test_user['id']}",
            json=sample_experience_data
        )
        exp_id = create_response.json()["id"]

        update_data = {"title": "Senior Software Engineer"}
        response = client.patch(f"/api/v1/experiences/{exp_id}", json=update_data)

        assert response.status_code == 200
        assert response.json()["title"] == "Senior Software Engineer"

    def test_update_nonexistent_experience(self, client):
        """Test updating non-existent experience returns 404."""
        update_data = {"title": "New Title"}
        response = client.patch("/api/v1/experiences/nonexistent", json=update_data)
        assert response.status_code == 404


class TestExperienceDeletion:
    """Test suite for deleting experiences."""

    def test_delete_experience(self, client, test_user, sample_experience_data):
        """Test deleting an experience."""
        create_response = client.post(
            f"/api/v1/experiences/?user_id={test_user['id']}",
            json=sample_experience_data
        )
        exp_id = create_response.json()["id"]

        response = client.delete(f"/api/v1/experiences/{exp_id}")
        assert response.status_code == 204

        # Verify deleted
        get_response = client.get(f"/api/v1/experiences/{exp_id}")
        assert get_response.status_code == 404

    def test_delete_nonexistent_experience(self, client):
        """Test deleting non-existent experience returns 404."""
        response = client.delete("/api/v1/experiences/nonexistent")
        assert response.status_code == 404


class TestExperienceSummary:
    """Test suite for experience summary endpoint."""

    def test_get_user_experience_summary(self, client, test_user):
        """Test getting user experience summary."""
        # Create experiences of different types
        experiences = [
            {"category": ExperienceCategory.EDUCATION, "type": ExperienceType.DEGREE},
            {"category": ExperienceCategory.EDUCATION, "type": ExperienceType.CERTIFICATE},
            {"category": ExperienceCategory.WORKPLACE, "type": ExperienceType.FULL_TIME},
            {"category": ExperienceCategory.SKILLS, "type": ExperienceType.HARD_SKILL},
        ]

        for exp in experiences:
            data = {
                "title": f"Test {exp['type'].value}",
                "category": exp["category"].value,
                "experience_type": exp["type"].value,
                "naics_code": "123456"
            }
            client.post(
                f"/api/v1/experiences/?user_id={test_user['id']}",
                json=data
            )

        response = client.get(f"/api/v1/experiences/user/{test_user['id']}/summary")
        assert response.status_code == 200

        data = response.json()
        assert data["total"] == 4
        assert "by_category" in data
        assert "by_type" in data

    def test_summary_nonexistent_user(self, client):
        """Test summary for non-existent user returns 404."""
        response = client.get("/api/v1/experiences/user/nonexistent/summary")
        assert response.status_code == 404
