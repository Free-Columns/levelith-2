"""
Tests for NAICS Database Repository

Tests the NAICSDBRepository class and its database operations.
"""

import pytest
from backend.repositories.naics_db_repository import NAICSDBRepository
from backend.models.naics import NAICSCategory, NAICSLevel, create_naics_code
from backend.models.db_models import NAICSCodeDB
from backend.database import Base, engine, get_db_context


class TestNAICSDBRepository:
    """Test suite for NAICSDBRepository."""

    @pytest.fixture(autouse=True)
    def setup_database(self):
        """
        Create test database tables before each test.
        Seed with sample data.
        Drop tables after each test.
        """
        Base.metadata.create_all(bind=engine)

        # Seed sample data
        with get_db_context() as db:
            sample_codes = [
                NAICSCodeDB(code="54", title="Professional, Scientific, and Technical Services", level=2,
                           category=NAICSCategory.PROFESSIONAL_SERVICES, is_active=True),
                NAICSCodeDB(code="541", title="Professional, Scientific, and Technical Services", level=3,
                           category=NAICSCategory.PROFESSIONAL_SERVICES, parent_code="54", is_active=True),
                NAICSCodeDB(code="5415", title="Computer Systems Design and Related Services", level=4,
                           category=NAICSCategory.TECHNOLOGY, parent_code="541", is_active=True),
                NAICSCodeDB(code="541511", title="Custom Computer Programming Services", level=6,
                           category=NAICSCategory.TECHNOLOGY, parent_code="5415", is_active=True,
                           description="Software development services"),
                NAICSCodeDB(code="541512", title="Computer Systems Design Services", level=6,
                           category=NAICSCategory.TECHNOLOGY, parent_code="5415", is_active=True),
                NAICSCodeDB(code="11", title="Agriculture, Forestry, Fishing and Hunting", level=2,
                           category=NAICSCategory.AGRICULTURE, is_active=True),
                NAICSCodeDB(code="611", title="Educational Services", level=3,
                           category=NAICSCategory.EDUCATION, parent_code="61", is_active=True),
                NAICSCodeDB(code="123456", title="General/Unclassified", level=6,
                           category=NAICSCategory.GENERAL, is_active=True),
            ]
            db.add_all(sample_codes)
            db.commit()

        yield
        Base.metadata.drop_all(bind=engine)

    def test_find_by_code_success(self):
        """Test finding a NAICS code that exists."""
        repo = NAICSDBRepository()
        code = repo.find_by_code("541511")

        assert code is not None
        assert code.code == "541511"
        assert code.title == "Custom Computer Programming Services"
        assert code.category == NAICSCategory.TECHNOLOGY
        assert code.level == NAICSLevel.NATIONAL_INDUSTRY

    def test_find_by_code_not_found(self):
        """Test finding a NAICS code that doesn't exist."""
        repo = NAICSDBRepository()
        code = repo.find_by_code("999999")

        assert code is None

    def test_find_by_code_normalization(self):
        """Test that code is normalized before lookup."""
        repo = NAICSDBRepository()

        # Should normalize to "541511"
        code = repo.find_by_code("  541511  ")
        assert code is not None
        assert code.code == "541511"

    def test_find_by_category(self):
        """Test finding NAICS codes by category."""
        repo = NAICSDBRepository()
        tech_codes = repo.find_by_category(NAICSCategory.TECHNOLOGY)

        assert len(tech_codes) >= 3  # 5415, 541511, 541512
        assert all(code.category == NAICSCategory.TECHNOLOGY for code in tech_codes)

    def test_find_by_level(self):
        """Test finding NAICS codes by hierarchical level."""
        repo = NAICSDBRepository()

        # Find sectors (2-digit)
        sectors = repo.find_by_level(NAICSLevel.SECTOR)
        assert len(sectors) >= 2  # 54, 11
        assert all(code.level == NAICSLevel.SECTOR for code in sectors)

        # Find national industries (6-digit)
        industries = repo.find_by_level(NAICSLevel.NATIONAL_INDUSTRY)
        assert len(industries) >= 3  # 541511, 541512, 123456
        assert all(code.level == NAICSLevel.NATIONAL_INDUSTRY for code in industries)

    def test_search_by_title(self):
        """Test searching NAICS codes by title."""
        repo = NAICSDBRepository()

        # Search for "computer"
        results = repo.search_by_title("computer")
        assert len(results) >= 2  # Should find computer-related codes
        assert all("computer" in code.title.lower() for code in results)

        # Search for "programming"
        results = repo.search_by_title("programming")
        assert len(results) >= 1
        assert any("programming" in code.title.lower() for code in results)

    def test_search_by_title_limit(self):
        """Test search limit parameter."""
        repo = NAICSDBRepository()

        results = repo.search_by_title("services", limit=2)
        assert len(results) <= 2

    def test_search_by_title_case_insensitive(self):
        """Test that search is case-insensitive."""
        repo = NAICSDBRepository()

        results_lower = repo.search_by_title("computer")
        results_upper = repo.search_by_title("COMPUTER")
        results_mixed = repo.search_by_title("CoMpUtEr")

        assert len(results_lower) == len(results_upper)
        assert len(results_lower) == len(results_mixed)

    def test_get_children(self):
        """Test getting child codes."""
        repo = NAICSDBRepository()

        # Get children of "54"
        children = repo.get_children("54")
        assert len(children) >= 1
        assert any(child.code == "541" for child in children)

        # Get children of "541"
        children = repo.get_children("541")
        assert len(children) >= 1
        assert any(child.code == "5415" for child in children)

    def test_get_parent(self):
        """Test getting parent code."""
        repo = NAICSDBRepository()

        # Get parent of "541511"
        parent = repo.get_parent("541511")
        assert parent is not None
        assert parent.code == "5415"

        # Get parent of "541"
        parent = repo.get_parent("541")
        assert parent is not None
        assert parent.code == "54"

    def test_get_parent_no_parent(self):
        """Test getting parent of top-level code."""
        repo = NAICSDBRepository()

        # Sector has no parent
        parent = repo.get_parent("54")
        assert parent is None

    def test_get_hierarchy(self):
        """Test getting full hierarchy."""
        repo = NAICSDBRepository()

        hierarchy = repo.get_hierarchy("541511")

        # Should have 4 levels: 54, 541, 5415, 541511
        assert len(hierarchy) == 4
        assert hierarchy[0].code == "54"
        assert hierarchy[1].code == "541"
        assert hierarchy[2].code == "5415"
        assert hierarchy[3].code == "541511"

    def test_is_valid_code(self):
        """Test code validation."""
        repo = NAICSDBRepository()

        assert repo.is_valid_code("541511") is True
        assert repo.is_valid_code("54") is True
        assert repo.is_valid_code("999999") is False
        assert repo.is_valid_code("invalid") is False

    def test_get_all_codes(self):
        """Test getting all codes."""
        repo = NAICSDBRepository()

        all_codes = repo.get_all_codes(active_only=True)
        assert len(all_codes) >= 8  # Our sample data

        # All should be active
        assert all(code.is_active for code in all_codes)

    def test_get_all_codes_include_inactive(self):
        """Test getting all codes including inactive."""
        # Add an inactive code
        with get_db_context() as db:
            inactive = NAICSCodeDB(
                code="999999",
                title="Inactive Industry",
                level=6,
                category=NAICSCategory.GENERAL,
                is_active=False
            )
            db.add(inactive)
            db.commit()

        repo = NAICSDBRepository()

        all_codes = repo.get_all_codes(active_only=False)
        active_codes = repo.get_all_codes(active_only=True)

        assert len(all_codes) > len(active_codes)

    def test_count(self):
        """Test counting NAICS codes."""
        repo = NAICSDBRepository()

        count = repo.count()
        assert count >= 8  # Our sample data

    def test_get_categories_summary(self):
        """Test getting category summary."""
        repo = NAICSDBRepository()

        summary = repo.get_categories_summary()

        assert isinstance(summary, dict)
        assert "technology" in summary
        assert "agriculture" in summary
        assert summary["technology"] >= 3  # 5415, 541511, 541512

    def test_get_levels_summary(self):
        """Test getting level summary."""
        repo = NAICSDBRepository()

        summary = repo.get_levels_summary()

        assert isinstance(summary, dict)
        assert 2 in summary  # Sectors
        assert 6 in summary  # National industries
        assert summary[2] >= 2  # 54, 11

    def test_bulk_insert(self):
        """Test bulk inserting NAICS codes."""
        repo = NAICSDBRepository()

        new_codes = [
            create_naics_code("99", "Test Industry 1", category=NAICSCategory.GENERAL),
            create_naics_code("991", "Test Industry 2", category=NAICSCategory.GENERAL),
            create_naics_code("9911", "Test Industry 3", category=NAICSCategory.GENERAL),
        ]

        inserted = repo.bulk_insert(new_codes)
        assert inserted == 3

        # Verify they were inserted
        code = repo.find_by_code("99")
        assert code is not None
        assert code.title == "Test Industry 1"

    def test_bulk_insert_skip_duplicates(self):
        """Test bulk insert skips existing codes."""
        repo = NAICSDBRepository()

        # Try to insert code that already exists
        codes = [
            create_naics_code("541511", "Duplicate Code", category=NAICSCategory.TECHNOLOGY),
            create_naics_code("999998", "New Code", category=NAICSCategory.GENERAL),
        ]

        inserted = repo.bulk_insert(codes)
        assert inserted == 1  # Only the new code

        # Original code should be unchanged
        original = repo.find_by_code("541511")
        assert original.title == "Custom Computer Programming Services"  # Not changed

    def test_db_to_domain_conversion(self):
        """Test conversion from database model to domain model."""
        repo = NAICSDBRepository()

        code = repo.find_by_code("541511")

        # Verify it's a domain model (NAICSCode), not db model
        from backend.models.naics import NAICSCode
        assert isinstance(code, NAICSCode)
        assert code.code == "541511"
        assert code.category == NAICSCategory.TECHNOLOGY

    def test_empty_search(self):
        """Test search with empty query."""
        repo = NAICSDBRepository()

        results = repo.search_by_title("")
        assert results == []

    def test_search_no_results(self):
        """Test search that returns no results."""
        repo = NAICSDBRepository()

        results = repo.search_by_title("nonexistentindustry123456789")
        assert len(results) == 0
