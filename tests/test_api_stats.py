"""
Unit tests for statistics API endpoints

Tests the statistics endpoint that provides aggregated data for the admin dashboard.
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime


@pytest.fixture
def client():
    """Create test client for FastAPI app."""
    from backend.main import app
    return TestClient(app)


class TestStatsEndpoint:
    """Test suite for statistics endpoint."""

    def test_get_stats_success(self, client):
        """Test statistics endpoint returns valid data structure."""
        response = client.get("/api/v1/stats")
        assert response.status_code == 200

        data = response.json()

        # Check main structure
        assert "users" in data
        assert "experiences" in data
        assert "skills" in data
        assert "geography" in data

    def test_stats_user_data_structure(self, client):
        """Test user statistics data structure."""
        response = client.get("/api/v1/stats")
        assert response.status_code == 200

        users = response.json()["users"]

        # Check user stats fields
        assert "total" in users
        assert "active" in users
        assert "verified" in users
        assert "inactive" in users
        assert "growth" in users
        assert "activity" in users

        # Validate data types
        assert isinstance(users["total"], int)
        assert isinstance(users["active"], int)
        assert isinstance(users["verified"], int)
        assert isinstance(users["inactive"], int)
        assert isinstance(users["growth"], list)
        assert isinstance(users["activity"], list)

        # Validate growth data structure
        if len(users["growth"]) > 0:
            growth_entry = users["growth"][0]
            assert "month" in growth_entry
            assert "users" in growth_entry

        # Validate activity data structure
        if len(users["activity"]) > 0:
            activity_entry = users["activity"][0]
            assert "date" in activity_entry
            assert "logins" in activity_entry

    def test_stats_experience_data_structure(self, client):
        """Test experience statistics data structure."""
        response = client.get("/api/v1/stats")
        assert response.status_code == 200

        experiences = response.json()["experiences"]

        # Check experience stats fields
        assert "total" in experiences
        assert "byType" in experiences
        assert "byCategory" in experiences
        assert "byIndustry" in experiences

        # Validate data types
        assert isinstance(experiences["total"], int)
        assert isinstance(experiences["byType"], dict)
        assert isinstance(experiences["byCategory"], dict)
        assert isinstance(experiences["byIndustry"], dict)

    def test_stats_skills_data_structure(self, client):
        """Test skills statistics data structure."""
        response = client.get("/api/v1/stats")
        assert response.status_code == 200

        skills = response.json()["skills"]

        # Check skills stats fields
        assert "top" in skills
        assert "total" in skills

        # Validate data types
        assert isinstance(skills["top"], list)
        assert isinstance(skills["total"], int)

        # Validate top skills structure if present
        if len(skills["top"]) > 0:
            skill_entry = skills["top"][0]
            assert "skill" in skill_entry
            assert "count" in skill_entry

    def test_stats_geography_data_structure(self, client):
        """Test geography statistics data structure."""
        response = client.get("/api/v1/stats")
        assert response.status_code == 200

        geography = response.json()["geography"]

        # Check geography stats fields
        assert "locations" in geography

        # Validate data types
        assert isinstance(geography["locations"], list)

        # Validate locations structure if present
        if len(geography["locations"]) > 0:
            location_entry = geography["locations"][0]
            assert "location" in location_entry
            assert "count" in location_entry
            assert isinstance(location_entry["count"], int)

    def test_stats_user_math_consistency(self, client):
        """Test that user counts are mathematically consistent."""
        response = client.get("/api/v1/stats")
        assert response.status_code == 200

        users = response.json()["users"]

        # Total should equal active + inactive
        assert users["total"] == users["active"] + users["inactive"]

        # Active and verified should not be negative
        assert users["active"] >= 0
        assert users["verified"] >= 0
        assert users["inactive"] >= 0

    def test_stats_growth_has_12_months(self, client):
        """Test that growth data includes 12 months of data."""
        response = client.get("/api/v1/stats")
        assert response.status_code == 200

        growth = response.json()["users"]["growth"]

        # Should have 12 months of data
        assert len(growth) == 12

    def test_stats_activity_has_30_days(self, client):
        """Test that activity data includes 30 days of data."""
        response = client.get("/api/v1/stats")
        assert response.status_code == 200

        activity = response.json()["users"]["activity"]

        # Should have 30 days of data
        assert len(activity) == 30

    def test_stats_responds_quickly(self, client):
        """Ensure stats endpoint responds within acceptable time."""
        import time

        start = time.time()
        response = client.get("/api/v1/stats")
        duration = time.time() - start

        assert response.status_code == 200
        assert duration < 5.0  # Should respond in less than 5 seconds


class TestStatsIntegration:
    """Integration tests for statistics."""

    def test_stats_with_empty_database(self, client):
        """Test stats endpoint works even with empty database."""
        response = client.get("/api/v1/stats")
        assert response.status_code == 200

        data = response.json()

        # Should still return valid structure even if empty
        assert "users" in data
        assert "experiences" in data
        assert isinstance(data["users"]["total"], int)
        assert isinstance(data["experiences"]["total"], int)

    def test_multiple_stats_calls(self, client):
        """Test multiple consecutive stats calls."""
        for _ in range(3):
            response = client.get("/api/v1/stats")
            assert response.status_code == 200

            data = response.json()
            assert "users" in data
            assert "experiences" in data
