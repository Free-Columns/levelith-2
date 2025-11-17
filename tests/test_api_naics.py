"""
Tests for NAICS API Endpoints

This module tests the NAICS REST API endpoints.

Test coverage includes:
- GET /api/v1/naics/{code} - Get NAICS code details
- GET /api/v1/naics/validate/{code} - Validate NAICS code
- GET /api/v1/naics/search - Search NAICS codes
- GET /api/v1/naics/autocomplete - Autocomplete suggestions
- GET /api/v1/naics/suggest/experience/{type} - Experience suggestions
- GET /api/v1/naics/category/{category} - Get codes by category
- GET /api/v1/naics/level/{level} - Get codes by level
- GET /api/v1/naics/{code}/hierarchy - Get code hierarchy
- GET /api/v1/naics/{code}/children - Get child codes
- GET /api/v1/naics/{code}/parent - Get parent code
- GET /api/v1/naics/categories/summary - Get category summary
- GET /api/v1/naics/categories/list - List all categories
"""

import pytest
from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


class TestGetNAICSCode:
    """Test GET /api/v1/naics/{code} endpoint."""

    def test_get_naics_code_success(self):
        """Test getting existing NAICS code."""
        response = client.get("/api/v1/naics/541511")

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == "541511"
        assert "title" in data
        assert "description" in data
        assert "category" in data
        assert "hierarchy" in data

    def test_get_naics_code_sector(self):
        """Test getting sector-level code."""
        response = client.get("/api/v1/naics/54")

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == "54"
        assert data["level"] == "SECTOR"
        assert data["level_value"] == 2

    def test_get_naics_code_not_found(self):
        """Test getting non-existent code returns 404."""
        response = client.get("/api/v1/naics/999999")

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_get_naics_fallback_code(self):
        """Test getting fallback code."""
        response = client.get("/api/v1/naics/123456")

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == "123456"


class TestValidateNAICSCode:
    """Test GET /api/v1/naics/validate/{code} endpoint."""

    def test_validate_valid_code(self):
        """Test validating valid NAICS code."""
        response = client.get("/api/v1/naics/validate/541511")

        assert response.status_code == 200
        data = response.json()
        assert data["is_valid"] is True
        assert data["code"] == "541511"
        assert data["message"] == "Valid NAICS code"
        assert data["naics"] is not None
        assert data["naics"]["code"] == "541511"

    def test_validate_invalid_code(self):
        """Test validating invalid NAICS code."""
        response = client.get("/api/v1/naics/validate/999999")

        assert response.status_code == 200
        data = response.json()
        assert data["is_valid"] is False
        assert data["code"] == "123456"  # Fallback code
        assert "fallback" in data["message"].lower()
        assert data["naics"] is None

    def test_validate_malformed_code(self):
        """Test validating malformed code."""
        response = client.get("/api/v1/naics/validate/invalid")

        assert response.status_code == 200
        data = response.json()
        assert data["is_valid"] is False
        assert data["code"] == "123456"


class TestSearchNAICSCodes:
    """Test GET /api/v1/naics/search endpoint."""

    def test_search_with_results(self):
        """Test searching with matching results."""
        response = client.get("/api/v1/naics/search?q=computer")

        assert response.status_code == 200
        data = response.json()
        assert "query" in data
        assert data["query"] == "computer"
        assert "results" in data
        assert "count" in data
        assert data["count"] >= 0

    def test_search_with_limit(self):
        """Test search respects limit parameter."""
        response = client.get("/api/v1/naics/search?q=services&limit=5")

        assert response.status_code == 200
        data = response.json()
        assert len(data["results"]) <= 5

    def test_search_case_insensitive(self):
        """Test search is case-insensitive."""
        response1 = client.get("/api/v1/naics/search?q=computer")
        response2 = client.get("/api/v1/naics/search?q=COMPUTER")

        assert response1.status_code == 200
        assert response2.status_code == 200

    def test_search_missing_query(self):
        """Test search without query parameter returns 422."""
        response = client.get("/api/v1/naics/search")

        assert response.status_code == 422  # Validation error


class TestAutocompleteNAICS:
    """Test GET /api/v1/naics/autocomplete endpoint."""

    def test_autocomplete_success(self):
        """Test autocomplete returns suggestions."""
        response = client.get("/api/v1/naics/autocomplete?q=comp")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

        if len(data) > 0:
            assert "code" in data[0]
            assert "title" in data[0]
            assert "description" in data[0]
            assert "category" in data[0]

    def test_autocomplete_with_limit(self):
        """Test autocomplete respects limit."""
        response = client.get("/api/v1/naics/autocomplete?q=services&limit=3")

        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 3

    def test_autocomplete_missing_query(self):
        """Test autocomplete without query returns 422."""
        response = client.get("/api/v1/naics/autocomplete")

        assert response.status_code == 422


class TestSuggestForExperience:
    """Test GET /api/v1/naics/suggest/experience/{type} endpoint."""

    def test_suggest_for_full_time(self):
        """Test suggesting codes for full-time experience."""
        response = client.get("/api/v1/naics/suggest/experience/full_time")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_suggest_with_title(self):
        """Test suggesting with experience title."""
        response = client.get(
            "/api/v1/naics/suggest/experience/full_time?title=Software%20Engineer"
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_suggest_for_degree(self):
        """Test suggesting codes for degree experience."""
        response = client.get("/api/v1/naics/suggest/experience/degree")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_suggest_with_limit(self):
        """Test suggest respects limit."""
        response = client.get(
            "/api/v1/naics/suggest/experience/full_time?limit=5"
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 5


class TestGetByCategory:
    """Test GET /api/v1/naics/category/{category} endpoint."""

    def test_get_by_category_technology(self):
        """Test getting technology category codes."""
        response = client.get("/api/v1/naics/category/technology")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        if len(data) > 0:
            assert all(code["category"] == "technology" for code in data)

    def test_get_by_category_education(self):
        """Test getting education category codes."""
        response = client.get("/api/v1/naics/category/education")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_get_by_category_not_found(self):
        """Test getting non-existent category returns 404."""
        response = client.get("/api/v1/naics/category/nonexistent")

        assert response.status_code == 404


class TestGetByLevel:
    """Test GET /api/v1/naics/level/{level} endpoint."""

    def test_get_by_level_sector(self):
        """Test getting sector-level codes."""
        response = client.get("/api/v1/naics/level/2")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        if len(data) > 0:
            assert all(len(code["code"]) == 2 for code in data)

    def test_get_by_level_national_industry(self):
        """Test getting national industry-level codes."""
        response = client.get("/api/v1/naics/level/6")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        if len(data) > 0:
            assert all(len(code["code"]) == 6 for code in data)

    def test_get_by_level_invalid(self):
        """Test getting codes by invalid level returns 400."""
        response = client.get("/api/v1/naics/level/5")

        assert response.status_code == 400
        assert "must be 2, 3, 4, or 6" in response.json()["detail"]


class TestGetHierarchy:
    """Test GET /api/v1/naics/{code}/hierarchy endpoint."""

    def test_get_hierarchy_success(self):
        """Test getting code hierarchy."""
        response = client.get("/api/v1/naics/541511/hierarchy")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

        # Verify hierarchy order
        codes = [item["code"] for item in data]
        assert codes[0].startswith(codes[0])  # First is shortest
        if len(codes) > 1:
            assert len(codes[-1]) >= len(codes[0])  # Last is longest or equal

    def test_get_hierarchy_sector(self):
        """Test getting hierarchy for sector returns single item."""
        response = client.get("/api/v1/naics/54/hierarchy")

        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert data[0]["code"] == "54"

    def test_get_hierarchy_not_found(self):
        """Test getting hierarchy for invalid code returns 404."""
        response = client.get("/api/v1/naics/999999/hierarchy")

        assert response.status_code == 404


class TestGetChildren:
    """Test GET /api/v1/naics/{code}/children endpoint."""

    def test_get_children_success(self):
        """Test getting child codes."""
        response = client.get("/api/v1/naics/54/children")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

        # All children should start with parent code
        if len(data) > 0:
            assert all(code["code"].startswith("54") for code in data)
            assert all(code["code"] != "54" for code in data)

    def test_get_children_industry_group(self):
        """Test getting children of industry group."""
        response = client.get("/api/v1/naics/5415/children")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_get_children_leaf_node(self):
        """Test getting children of leaf node returns empty."""
        response = client.get("/api/v1/naics/541511/children")

        assert response.status_code == 200
        data = response.json()
        assert data == []


class TestGetParent:
    """Test GET /api/v1/naics/{code}/parent endpoint."""

    def test_get_parent_success(self):
        """Test getting parent code."""
        response = client.get("/api/v1/naics/541511/parent")

        assert response.status_code == 200
        data = response.json()
        assert "code" in data
        assert data["code"] == "5415"

    def test_get_parent_subsector(self):
        """Test getting parent of subsector."""
        response = client.get("/api/v1/naics/541/parent")

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == "54"

    def test_get_parent_sector(self):
        """Test getting parent of sector returns 404."""
        response = client.get("/api/v1/naics/54/parent")

        assert response.status_code == 404


class TestCategoriesSummary:
    """Test GET /api/v1/naics/categories/summary endpoint."""

    def test_get_categories_summary(self):
        """Test getting category summary."""
        response = client.get("/api/v1/naics/categories/summary")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

        if len(data) > 0:
            assert "category" in data[0]
            assert "count" in data[0]
            assert isinstance(data[0]["count"], int)
            assert data[0]["count"] > 0


class TestListCategories:
    """Test GET /api/v1/naics/categories/list endpoint."""

    def test_list_categories(self):
        """Test listing all categories."""
        response = client.get("/api/v1/naics/categories/list")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert "technology" in data
        assert "education" in data
        assert "healthcare" in data
        assert "finance" in data


class TestAPIResponseFormat:
    """Test API response formats and structure."""

    def test_naics_code_response_structure(self):
        """Test NAICS code response has expected structure."""
        response = client.get("/api/v1/naics/541511")

        assert response.status_code == 200
        data = response.json()

        # Required fields
        assert "code" in data
        assert "title" in data
        assert "description" in data
        assert "level" in data
        assert "level_value" in data
        assert "category" in data
        assert "is_active" in data
        assert "year" in data
        assert "hierarchy" in data

        # Optional fields
        assert "parent_code" in data

    def test_validation_response_structure(self):
        """Test validation response has expected structure."""
        response = client.get("/api/v1/naics/validate/541511")

        assert response.status_code == 200
        data = response.json()

        assert "is_valid" in data
        assert "code" in data
        assert "message" in data
        assert "naics" in data

    def test_search_response_structure(self):
        """Test search response has expected structure."""
        response = client.get("/api/v1/naics/search?q=computer")

        assert response.status_code == 200
        data = response.json()

        assert "query" in data
        assert "results" in data
        assert "count" in data
        assert isinstance(data["results"], list)
        assert isinstance(data["count"], int)
