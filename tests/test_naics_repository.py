"""
Tests for NAICS Repository

This module tests the NAICS repository data access layer.

Test coverage includes:
- NAICS code lookup and retrieval
- Search and filtering operations
- Category and level indexing
- Hierarchical operations
- Data loading from JSON
"""

import pytest
import json
import tempfile
from pathlib import Path

from backend.repositories.naics_repository import NAICSRepository
from backend.models.naics import NAICSCode, NAICSCategory, NAICSLevel


@pytest.fixture
def sample_naics_data():
    """Create sample NAICS data for testing."""
    return [
        {
            "code": "123456",
            "title": "General/Unclassified",
            "description": "Fallback code",
            "category": "general",
            "is_active": True
        },
        {
            "code": "54",
            "title": "Professional, Scientific, and Technical Services",
            "description": "Professional services sector",
            "category": "professional_services",
            "is_active": True
        },
        {
            "code": "541",
            "title": "Professional, Scientific, and Technical Services",
            "description": "Professional services subsector",
            "category": "professional_services",
            "is_active": True
        },
        {
            "code": "5415",
            "title": "Computer Systems Design and Related Services",
            "description": "Computer services industry group",
            "category": "technology",
            "is_active": True
        },
        {
            "code": "541511",
            "title": "Custom Computer Programming Services",
            "description": "Software development services",
            "category": "technology",
            "is_active": True
        },
        {
            "code": "541512",
            "title": "Computer Systems Design Services",
            "description": "Systems design services",
            "category": "technology",
            "is_active": True
        },
        {
            "code": "61",
            "title": "Educational Services",
            "description": "Education sector",
            "category": "education",
            "is_active": True
        },
        {
            "code": "611310",
            "title": "Colleges, Universities, and Professional Schools",
            "description": "Higher education",
            "category": "education",
            "is_active": True
        },
    ]


@pytest.fixture
def temp_naics_file(sample_naics_data):
    """Create a temporary NAICS data file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(sample_naics_data, f)
        temp_path = f.name

    yield temp_path

    # Cleanup
    Path(temp_path).unlink()


@pytest.fixture
def naics_repo(temp_naics_file):
    """Create a NAICS repository with test data."""
    return NAICSRepository(data_file_path=temp_naics_file)


class TestNAICSRepositoryInitialization:
    """Test NAICS repository initialization and data loading."""

    def test_repo_initializes(self, naics_repo):
        """Test repository initializes successfully."""
        assert naics_repo is not None
        assert naics_repo._naics_codes is not None

    def test_repo_loads_data(self, naics_repo):
        """Test repository loads NAICS data."""
        assert naics_repo.count() > 0

    def test_repo_builds_indexes(self, naics_repo):
        """Test repository builds all indexes."""
        assert len(naics_repo._category_index) > 0
        assert len(naics_repo._level_index) > 0
        assert len(naics_repo._title_index) > 0

    def test_repo_handles_missing_file(self):
        """Test repository handles missing data file gracefully."""
        repo = NAICSRepository(data_file_path="/nonexistent/file.json")
        # Should at least have the fallback code
        assert repo.count() > 0
        assert repo.find_by_code("123456") is not None


class TestNAICSCodeLookup:
    """Test NAICS code lookup operations."""

    def test_find_by_code_valid(self, naics_repo):
        """Test finding NAICS code by valid code."""
        naics = naics_repo.find_by_code("541511")
        assert naics is not None
        assert naics.code == "541511"
        assert "Computer Programming" in naics.title

    def test_find_by_code_sector(self, naics_repo):
        """Test finding sector code."""
        naics = naics_repo.find_by_code("54")
        assert naics is not None
        assert naics.code == "54"
        assert naics.level == NAICSLevel.SECTOR

    def test_find_by_code_not_found(self, naics_repo):
        """Test finding non-existent code returns None."""
        naics = naics_repo.find_by_code("999999")
        assert naics is None

    def test_find_by_code_normalizes(self, naics_repo):
        """Test finding code with whitespace."""
        naics = naics_repo.find_by_code("  541511  ")
        assert naics is not None
        assert naics.code == "541511"

    def test_find_by_code_fallback(self, naics_repo):
        """Test finding fallback code."""
        naics = naics_repo.find_by_code("123456")
        assert naics is not None
        assert naics.code == "123456"


class TestCategoryFiltering:
    """Test filtering NAICS codes by category."""

    def test_find_by_category_technology(self, naics_repo):
        """Test finding technology category codes."""
        codes = naics_repo.find_by_category(NAICSCategory.TECHNOLOGY)
        assert len(codes) > 0
        assert all(code.category == NAICSCategory.TECHNOLOGY for code in codes)

    def test_find_by_category_education(self, naics_repo):
        """Test finding education category codes."""
        codes = naics_repo.find_by_category(NAICSCategory.EDUCATION)
        assert len(codes) > 0
        assert all(code.category == NAICSCategory.EDUCATION for code in codes)

    def test_find_by_category_empty(self, naics_repo):
        """Test finding category with no codes returns empty list."""
        codes = naics_repo.find_by_category(NAICSCategory.HEALTHCARE)
        assert codes == []


class TestLevelFiltering:
    """Test filtering NAICS codes by hierarchical level."""

    def test_find_by_level_sector(self, naics_repo):
        """Test finding sector-level codes."""
        sectors = naics_repo.find_by_level(NAICSLevel.SECTOR)
        assert len(sectors) > 0
        assert all(len(code.code) == 2 for code in sectors)

    def test_find_by_level_subsector(self, naics_repo):
        """Test finding subsector-level codes."""
        subsectors = naics_repo.find_by_level(NAICSLevel.SUBSECTOR)
        assert len(subsectors) > 0
        assert all(len(code.code) == 3 for code in subsectors)

    def test_find_by_level_industry_group(self, naics_repo):
        """Test finding industry group-level codes."""
        groups = naics_repo.find_by_level(NAICSLevel.INDUSTRY_GROUP)
        assert len(groups) > 0
        assert all(len(code.code) == 4 for code in groups)

    def test_find_by_level_national_industry(self, naics_repo):
        """Test finding national industry-level codes."""
        industries = naics_repo.find_by_level(NAICSLevel.NATIONAL_INDUSTRY)
        assert len(industries) > 0
        assert all(len(code.code) == 6 for code in industries)


class TestNAICSSearch:
    """Test NAICS code search functionality."""

    def test_search_by_title_single_word(self, naics_repo):
        """Test searching by single keyword."""
        results = naics_repo.search_by_title("computer")
        assert len(results) > 0
        assert any("computer" in code.title.lower() for code in results)

    def test_search_by_title_multiple_words(self, naics_repo):
        """Test searching by multiple keywords."""
        results = naics_repo.search_by_title("computer programming")
        assert len(results) > 0

    def test_search_by_title_case_insensitive(self, naics_repo):
        """Test search is case-insensitive."""
        results_lower = naics_repo.search_by_title("computer")
        results_upper = naics_repo.search_by_title("COMPUTER")
        results_mixed = naics_repo.search_by_title("Computer")

        assert len(results_lower) > 0
        assert len(results_upper) > 0
        assert len(results_mixed) > 0

    def test_search_respects_limit(self, naics_repo):
        """Test search respects result limit."""
        results = naics_repo.search_by_title("services", limit=2)
        assert len(results) <= 2

    def test_search_empty_query(self, naics_repo):
        """Test searching with empty query returns empty list."""
        results = naics_repo.search_by_title("")
        assert results == []

    def test_search_no_results(self, naics_repo):
        """Test searching with no matches returns empty list."""
        results = naics_repo.search_by_title("nonexistent keyword xyz")
        assert results == []


class TestHierarchicalOperations:
    """Test hierarchical NAICS code operations."""

    def test_get_children(self, naics_repo):
        """Test getting child codes of a parent."""
        children = naics_repo.get_children("54")
        assert len(children) > 0
        assert all(code.code.startswith("54") for code in children)
        assert all(code.code != "54" for code in children)

    def test_get_children_industry_group(self, naics_repo):
        """Test getting children of industry group."""
        children = naics_repo.get_children("5415")
        assert len(children) > 0
        # Should include 541511 and 541512
        child_codes = [c.code for c in children]
        assert "541511" in child_codes
        assert "541512" in child_codes

    def test_get_children_leaf_node(self, naics_repo):
        """Test getting children of leaf node returns empty."""
        children = naics_repo.get_children("541511")
        assert children == []

    def test_get_parent(self, naics_repo):
        """Test getting parent code."""
        parent = naics_repo.get_parent("541511")
        assert parent is not None
        assert parent.code == "5415"

    def test_get_parent_subsector(self, naics_repo):
        """Test getting parent of subsector."""
        parent = naics_repo.get_parent("541")
        assert parent is not None
        assert parent.code == "54"

    def test_get_parent_sector(self, naics_repo):
        """Test getting parent of sector returns None."""
        parent = naics_repo.get_parent("54")
        assert parent is None

    def test_get_hierarchy(self, naics_repo):
        """Test getting full hierarchy for a code."""
        hierarchy = naics_repo.get_hierarchy("541511")
        assert len(hierarchy) == 4
        codes = [code.code for code in hierarchy]
        assert codes == ["54", "541", "5415", "541511"]

    def test_get_hierarchy_sector(self, naics_repo):
        """Test getting hierarchy for sector."""
        hierarchy = naics_repo.get_hierarchy("54")
        assert len(hierarchy) == 1
        assert hierarchy[0].code == "54"


class TestCodeValidation:
    """Test NAICS code validation operations."""

    def test_is_valid_code_existing(self, naics_repo):
        """Test validating existing code."""
        assert naics_repo.is_valid_code("541511") is True

    def test_is_valid_code_nonexistent(self, naics_repo):
        """Test validating non-existent code."""
        assert naics_repo.is_valid_code("999999") is False

    def test_is_valid_code_fallback(self, naics_repo):
        """Test validating fallback code."""
        assert naics_repo.is_valid_code("123456") is True

    def test_is_valid_code_normalizes(self, naics_repo):
        """Test validation normalizes code."""
        assert naics_repo.is_valid_code("  541511  ") is True


class TestRepositoryQueries:
    """Test repository query operations."""

    def test_get_all_codes(self, naics_repo):
        """Test getting all NAICS codes."""
        all_codes = naics_repo.get_all_codes()
        assert len(all_codes) > 0
        assert all(isinstance(code, NAICSCode) for code in all_codes)

    def test_get_all_codes_active_only(self, naics_repo):
        """Test getting only active codes."""
        all_codes = naics_repo.get_all_codes(active_only=True)
        assert all(code.is_active for code in all_codes)

    def test_count(self, naics_repo):
        """Test getting total code count."""
        count = naics_repo.count()
        assert count > 0
        assert isinstance(count, int)

    def test_get_categories_summary(self, naics_repo):
        """Test getting category summary."""
        summary = naics_repo.get_categories_summary()
        assert isinstance(summary, dict)
        assert "technology" in summary
        assert "education" in summary
        assert all(isinstance(count, int) for count in summary.values())
        assert all(count > 0 for count in summary.values())


class TestIndexConsistency:
    """Test that indexes remain consistent with data."""

    def test_category_index_complete(self, naics_repo):
        """Test category index contains all codes."""
        all_codes = naics_repo.get_all_codes()
        indexed_codes = []

        for codes in naics_repo._category_index.values():
            indexed_codes.extend(codes)

        assert len(indexed_codes) == len(all_codes)

    def test_level_index_complete(self, naics_repo):
        """Test level index contains all codes."""
        all_codes = naics_repo.get_all_codes()
        indexed_codes = []

        for codes in naics_repo._level_index.values():
            indexed_codes.extend(codes)

        assert len(indexed_codes) == len(all_codes)

    def test_title_index_searchable(self, naics_repo):
        """Test title index enables search."""
        # Search for known term
        results = naics_repo.search_by_title("computer")
        assert len(results) > 0

        # Verify results are in main storage
        for result in results:
            assert result.code in naics_repo._naics_codes
