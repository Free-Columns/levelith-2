"""
Tests for NAICS Service

This module tests the NAICS service business logic layer.

Test coverage includes:
- Code lookup and validation
- Search and autocomplete
- Experience-based suggestions
- Category and level filtering
- Hierarchical operations
"""

import pytest
from unittest.mock import Mock, patch

from backend.services.naics_service import NAICSService
from backend.repositories.naics_repository import NAICSRepository
from backend.models.naics import (
    NAICSCode,
    NAICSCategory,
    NAICSLevel,
    create_naics_code,
    FALLBACK_NAICS,
)


@pytest.fixture
def mock_repo():
    """Create a mock NAICS repository."""
    return Mock(spec=NAICSRepository)


@pytest.fixture
def naics_service(mock_repo):
    """Create a NAICS service with mock repository."""
    return NAICSService(naics_repo=mock_repo)


@pytest.fixture
def sample_naics_code():
    """Create a sample NAICS code for testing."""
    return create_naics_code(
        code="541511",
        title="Custom Computer Programming Services",
        description="Software development",
        category=NAICSCategory.TECHNOLOGY
    )


class TestNAICSServiceInitialization:
    """Test NAICS service initialization."""

    def test_service_initializes(self, mock_repo):
        """Test service initializes with repository."""
        service = NAICSService(naics_repo=mock_repo)
        assert service is not None
        assert service.naics_repo == mock_repo

    def test_service_builds_category_mapping(self, mock_repo):
        """Test service builds experience to category mapping."""
        service = NAICSService(naics_repo=mock_repo)
        assert service._experience_category_mapping is not None
        assert isinstance(service._experience_category_mapping, dict)


class TestCodeLookup:
    """Test NAICS code lookup operations."""

    def test_lookup_code_found(self, naics_service, mock_repo, sample_naics_code):
        """Test looking up existing code."""
        mock_repo.find_by_code.return_value = sample_naics_code

        result = naics_service.lookup_code("541511")

        assert result is not None
        assert result.code == "541511"
        mock_repo.find_by_code.assert_called_once_with("541511")

    def test_lookup_code_not_found(self, naics_service, mock_repo):
        """Test looking up non-existent code."""
        mock_repo.find_by_code.return_value = None

        result = naics_service.lookup_code("999999")

        assert result is None
        mock_repo.find_by_code.assert_called_once_with("999999")


class TestCodeValidation:
    """Test NAICS code validation."""

    def test_validate_code_valid(self, naics_service, mock_repo):
        """Test validating valid code."""
        mock_repo.is_valid_code.return_value = True

        is_valid, normalized = naics_service.validate_code("541511")

        assert is_valid is True
        assert normalized == "541511"

    def test_validate_code_invalid(self, naics_service, mock_repo):
        """Test validating invalid code."""
        mock_repo.is_valid_code.return_value = False

        is_valid, normalized = naics_service.validate_code("invalid")

        assert is_valid is False
        assert normalized == FALLBACK_NAICS.code

    def test_validate_with_metadata_valid(self, naics_service, mock_repo, sample_naics_code):
        """Test validation with metadata for valid code."""
        mock_repo.is_valid_code.return_value = True
        mock_repo.find_by_code.return_value = sample_naics_code

        is_valid, naics = naics_service.validate_with_metadata("541511")

        assert is_valid is True
        assert naics.code == "541511"
        assert naics.title == "Custom Computer Programming Services"

    def test_validate_with_metadata_invalid(self, naics_service, mock_repo):
        """Test validation with metadata for invalid code."""
        mock_repo.is_valid_code.return_value = False

        is_valid, naics = naics_service.validate_with_metadata("invalid")

        assert is_valid is False
        assert naics.code == FALLBACK_NAICS.code


class TestSearch:
    """Test NAICS code search functionality."""

    def test_search_returns_results(self, naics_service, mock_repo, sample_naics_code):
        """Test search returns matching codes."""
        mock_repo.search_by_title.return_value = [sample_naics_code]

        results = naics_service.search("computer programming")

        assert len(results) == 1
        assert results[0].code == "541511"
        mock_repo.search_by_title.assert_called_once_with("computer programming", limit=20)

    def test_search_with_custom_limit(self, naics_service, mock_repo):
        """Test search respects custom limit."""
        mock_repo.search_by_title.return_value = []

        naics_service.search("test", limit=5)

        mock_repo.search_by_title.assert_called_once_with("test", limit=5)

    def test_search_empty_query(self, naics_service, mock_repo):
        """Test search with empty query returns empty list."""
        results = naics_service.search("")

        assert results == []
        mock_repo.search_by_title.assert_not_called()


class TestAutocomplete:
    """Test autocomplete suggestions."""

    def test_autocomplete_returns_suggestions(self, naics_service, mock_repo, sample_naics_code):
        """Test autocomplete returns formatted suggestions."""
        mock_repo.search_by_title.return_value = [sample_naics_code]

        results = naics_service.autocomplete("comp")

        assert len(results) == 1
        assert isinstance(results[0], dict)
        assert results[0]["code"] == "541511"
        assert results[0]["title"] == "Custom Computer Programming Services"
        assert results[0]["category"] == "technology"

    def test_autocomplete_with_limit(self, naics_service, mock_repo):
        """Test autocomplete respects limit."""
        mock_repo.search_by_title.return_value = []

        naics_service.autocomplete("test", limit=5)

        mock_repo.search_by_title.assert_called_once_with("test", limit=5)


class TestExperienceSuggestions:
    """Test NAICS suggestions for experience types."""

    def test_suggest_for_full_time_with_title(self, naics_service, mock_repo, sample_naics_code):
        """Test suggesting for full-time experience with title."""
        mock_repo.search_by_title.return_value = [sample_naics_code]

        results = naics_service.suggest_for_experience(
            experience_type="full_time",
            title="Software Engineer"
        )

        assert len(results) > 0
        mock_repo.search_by_title.assert_called()

    def test_suggest_for_degree_no_title(self, naics_service, mock_repo):
        """Test suggesting for degree without title uses categories."""
        education_code = create_naics_code(
            code="611310",
            title="Colleges and Universities",
            category=NAICSCategory.EDUCATION
        )
        mock_repo.find_by_category.return_value = [education_code]

        results = naics_service.suggest_for_experience(
            experience_type="degree",
            title=None
        )

        assert len(results) > 0
        mock_repo.find_by_category.assert_called()

    def test_suggest_for_soft_skill(self, naics_service, mock_repo):
        """Test suggesting for soft skill uses general category."""
        mock_repo.find_by_category.return_value = [FALLBACK_NAICS]

        results = naics_service.suggest_for_experience(
            experience_type="soft_skill"
        )

        # Should use general category for skills
        assert len(results) > 0


class TestCategoryOperations:
    """Test category-based operations."""

    def test_get_by_category(self, naics_service, mock_repo, sample_naics_code):
        """Test getting codes by category."""
        mock_repo.find_by_category.return_value = [sample_naics_code]

        results = naics_service.get_by_category("technology")

        assert len(results) == 1
        assert results[0].category == NAICSCategory.TECHNOLOGY
        mock_repo.find_by_category.assert_called_once()

    def test_get_by_category_invalid(self, naics_service, mock_repo):
        """Test getting codes by invalid category."""
        results = naics_service.get_by_category("invalid_category")

        assert results == []
        mock_repo.find_by_category.assert_not_called()

    def test_get_all_categories(self, naics_service):
        """Test getting all available categories."""
        categories = naics_service.get_all_categories()

        assert isinstance(categories, list)
        assert "technology" in categories
        assert "education" in categories
        assert "healthcare" in categories

    def test_get_categories_summary(self, naics_service, mock_repo):
        """Test getting category summary."""
        mock_repo.get_categories_summary.return_value = {
            "technology": 10,
            "education": 5
        }

        summary = naics_service.get_categories_summary()

        assert summary["technology"] == 10
        assert summary["education"] == 5
        mock_repo.get_categories_summary.assert_called_once()


class TestLevelOperations:
    """Test level-based operations."""

    def test_get_by_level_sector(self, naics_service, mock_repo):
        """Test getting sector-level codes."""
        sector = create_naics_code(code="54", title="Professional Services")
        mock_repo.find_by_level.return_value = [sector]

        results = naics_service.get_by_level(2)

        assert len(results) == 1
        assert results[0].level == NAICSLevel.SECTOR
        mock_repo.find_by_level.assert_called_once()

    def test_get_by_level_national_industry(self, naics_service, mock_repo, sample_naics_code):
        """Test getting national industry-level codes."""
        mock_repo.find_by_level.return_value = [sample_naics_code]

        results = naics_service.get_by_level(6)

        assert len(results) == 1
        assert results[0].level == NAICSLevel.NATIONAL_INDUSTRY

    def test_get_by_level_invalid(self, naics_service, mock_repo):
        """Test getting codes by invalid level."""
        results = naics_service.get_by_level(99)

        assert results == []
        mock_repo.find_by_level.assert_not_called()


class TestHierarchicalOperations:
    """Test hierarchical operations."""

    def test_get_hierarchy(self, naics_service, mock_repo):
        """Test getting code hierarchy."""
        hierarchy = [
            create_naics_code(code="54", title="Sector"),
            create_naics_code(code="541", title="Subsector"),
            create_naics_code(code="5415", title="Industry Group"),
            create_naics_code(code="541511", title="National Industry"),
        ]
        mock_repo.get_hierarchy.return_value = hierarchy

        results = naics_service.get_hierarchy("541511")

        assert len(results) == 4
        assert results[0].code == "54"
        assert results[-1].code == "541511"
        mock_repo.get_hierarchy.assert_called_once_with("541511")

    def test_get_children(self, naics_service, mock_repo, sample_naics_code):
        """Test getting child codes."""
        mock_repo.get_children.return_value = [sample_naics_code]

        results = naics_service.get_children("5415")

        assert len(results) == 1
        assert results[0].code == "541511"
        mock_repo.get_children.assert_called_once_with("5415")

    def test_get_parent(self, naics_service, mock_repo):
        """Test getting parent code."""
        parent = create_naics_code(code="5415", title="Computer Services")
        mock_repo.get_parent.return_value = parent

        result = naics_service.get_parent("541511")

        assert result is not None
        assert result.code == "5415"
        mock_repo.get_parent.assert_called_once_with("541511")

    def test_get_parent_not_found(self, naics_service, mock_repo):
        """Test getting parent when none exists."""
        mock_repo.get_parent.return_value = None

        result = naics_service.get_parent("54")

        assert result is None


class TestExperienceCategoryMapping:
    """Test experience type to NAICS category mapping."""

    def test_mapping_includes_all_experience_types(self, naics_service):
        """Test mapping includes all experience types."""
        mapping = naics_service._experience_category_mapping

        # Education types
        assert "certificate" in mapping
        assert "degree" in mapping
        assert "course" in mapping

        # Workplace types
        assert "gig" in mapping
        assert "part_time" in mapping
        assert "full_time" in mapping

        # Skills types
        assert "soft_skill" in mapping
        assert "hard_skill" in mapping
        assert "native_skill" in mapping

    def test_education_types_map_to_education(self, naics_service):
        """Test education experience types map to education category."""
        mapping = naics_service._experience_category_mapping

        assert NAICSCategory.EDUCATION in mapping["degree"]
        assert NAICSCategory.EDUCATION in mapping["certificate"]

    def test_full_time_maps_to_professional_categories(self, naics_service):
        """Test full-time maps to professional categories."""
        mapping = naics_service._experience_category_mapping

        categories = mapping["full_time"]
        assert NAICSCategory.TECHNOLOGY in categories
        assert NAICSCategory.PROFESSIONAL_SERVICES in categories

    def test_skills_map_to_general(self, naics_service):
        """Test skill types map to general category."""
        mapping = naics_service._experience_category_mapping

        assert NAICSCategory.GENERAL in mapping["soft_skill"]
        assert NAICSCategory.GENERAL in mapping["hard_skill"]
        assert NAICSCategory.GENERAL in mapping["native_skill"]
