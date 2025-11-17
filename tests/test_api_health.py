"""
Unit tests for health check endpoints

Tests the health, readiness, and liveness endpoints.
Critical for Render deployment verification.
"""

import pytest
from fastapi.testclient import TestClient

# Import will be done in fixture


@pytest.fixture
def client():
    """Create test client for FastAPI app."""
    from backend.main import app
    return TestClient(app)


class TestHealthEndpoints:
    """Test suite for health check endpoints."""

    def test_health_check(self, client):
        """Test basic health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "service" in data
        assert "version" in data

    def test_readiness_check(self, client):
        """Test readiness check endpoint."""
        response = client.get("/health/ready")
        assert response.status_code in [200, 503]  # May fail if DB not available

        data = response.json()
        assert data["status"] in ["ready", "not_ready"]
        assert "checks" in data
        assert "database" in data["checks"]

    def test_liveness_check(self, client):
        """Test liveness check endpoint."""
        response = client.get("/health/live")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "alive"
        assert "timestamp" in data

    def test_health_details(self, client):
        """Test detailed health information endpoint."""
        response = client.get("/health/details")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "healthy"
        assert "service" in data
        assert "database" in data
        assert "configuration" in data


class TestRootEndpoint:
    """Test suite for root endpoint."""

    def test_root_endpoint(self, client):
        """Test root endpoint returns API information."""
        response = client.get("/")
        assert response.status_code == 200

        data = response.json()
        assert "name" in data
        assert "version" in data
        assert "environment" in data
        assert "status" in data
        assert data["status"] == "operational"


class TestHealthIntegration:
    """Integration tests for health monitoring."""

    def test_health_endpoints_respond_quickly(self, client):
        """Ensure health endpoints respond within acceptable time."""
        import time

        start = time.time()
        response = client.get("/health")
        duration = time.time() - start

        assert response.status_code == 200
        assert duration < 1.0  # Should respond in less than 1 second

    def test_multiple_health_checks(self, client):
        """Test multiple consecutive health checks."""
        for _ in range(5):
            response = client.get("/health")
            assert response.status_code == 200
            assert response.json()["status"] == "healthy"
