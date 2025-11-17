"""
Tests for NAICS Domain Model

This module tests the NAICS code domain model, validation functions,
and hierarchical operations.

Test coverage includes:
- NAICS code creation and validation
- Hierarchical relationships (parent/child)
- Code normalization
- Level detection
- Factory functions
"""

import pytest
from datetime import datetime

from backend.models.naics import (
    NAICSCode,
    NAICSLevel,
    NAICSCategory,
    create_naics_code,
    normalize_naics_code,
    get_naics_level,
    extract_parent_codes,
    FALLBACK_NAICS,
    NAICS_FALLBACK_CODE,
)


class TestNAICSCodeNormalization:
    """Test NAICS code normalization and validation."""

    def test_normalize_valid_6_digit_code(self):
        """Test normalization of valid 6-digit NAICS code."""
        assert normalize_naics_code("541511") == "541511"

    def test_normalize_valid_2_digit_code(self):
        """Test normalization of valid 2-digit sector code."""
        assert normalize_naics_code("54") == "54"

    def test_normalize_valid_3_digit_code(self):
        """Test normalization of valid 3-digit subsector code."""
        assert normalize_naics_code("541") == "541"

    def test_normalize_valid_4_digit_code(self):
        """Test normalization of valid 4-digit industry group code."""
        assert normalize_naics_code("5415") == "5415"

    def test_normalize_with_whitespace(self):
        """Test normalization removes whitespace."""
        assert normalize_naics_code("  541511  ") == "541511"

    def test_normalize_empty_string(self):
        """Test normalization of empty string returns fallback."""
        assert normalize_naics_code("") == NAICS_FALLBACK_CODE

    def test_normalize_none(self):
        """Test normalization of None returns fallback."""
        assert normalize_naics_code(None) == NAICS_FALLBACK_CODE

    def test_normalize_invalid_length(self):
        """Test normalization of invalid length returns fallback."""
        assert normalize_naics_code("1") == NAICS_FALLBACK_CODE
        assert normalize_naics_code("12345") == NAICS_FALLBACK_CODE
        assert normalize_naics_code("1234567") == NAICS_FALLBACK_CODE

    def test_normalize_non_numeric(self):
        """Test normalization of non-numeric code returns fallback."""
        assert normalize_naics_code("abcdef") == NAICS_FALLBACK_CODE
        assert normalize_naics_code("54151a") == NAICS_FALLBACK_CODE


class TestNAICSLevelDetection:
    """Test NAICS hierarchical level detection."""

    def test_get_level_sector(self):
        """Test level detection for 2-digit sector."""
        assert get_naics_level("54") == NAICSLevel.SECTOR

    def test_get_level_subsector(self):
        """Test level detection for 3-digit subsector."""
        assert get_naics_level("541") == NAICSLevel.SUBSECTOR

    def test_get_level_industry_group(self):
        """Test level detection for 4-digit industry group."""
        assert get_naics_level("5415") == NAICSLevel.INDUSTRY_GROUP

    def test_get_level_national_industry(self):
        """Test level detection for 6-digit national industry."""
        assert get_naics_level("541511") == NAICSLevel.NATIONAL_INDUSTRY

    def test_get_level_invalid(self):
        """Test level detection for invalid code returns None."""
        assert get_naics_level("1") is None
        assert get_naics_level("12345") is None
        assert get_naics_level("") is None
        assert get_naics_level(None) is None


class TestParentCodeExtraction:
    """Test parent code extraction from NAICS codes."""

    def test_extract_parents_6_digit(self):
        """Test extracting parents from 6-digit code."""
        parents = extract_parent_codes("541511")
        assert parents == ["54", "541", "5415", "541511"]

    def test_extract_parents_4_digit(self):
        """Test extracting parents from 4-digit code."""
        parents = extract_parent_codes("5415")
        assert parents == ["54", "541", "5415"]

    def test_extract_parents_3_digit(self):
        """Test extracting parents from 3-digit code."""
        parents = extract_parent_codes("541")
        assert parents == ["54", "541"]

    def test_extract_parents_2_digit(self):
        """Test extracting parents from 2-digit code."""
        parents = extract_parent_codes("54")
        assert parents == ["54"]

    def test_extract_parents_invalid(self):
        """Test extracting parents from invalid code returns empty."""
        assert extract_parent_codes("") == []
        assert extract_parent_codes("1") == []


class TestNAICSCodeCreation:
    """Test NAICS code creation and initialization."""

    def test_create_basic_naics_code(self):
        """Test creating basic NAICS code."""
        naics = NAICSCode(
            code="541511",
            title="Custom Computer Programming Services"
        )
        assert naics.code == "541511"
        assert naics.title == "Custom Computer Programming Services"
        assert naics.level == NAICSLevel.NATIONAL_INDUSTRY

    def test_create_naics_with_description(self):
        """Test creating NAICS code with description."""
        naics = NAICSCode(
            code="541511",
            title="Custom Computer Programming Services",
            description="Establishments primarily engaged in writing software."
        )
        assert naics.description == "Establishments primarily engaged in writing software."

    def test_create_naics_with_category(self):
        """Test creating NAICS code with category."""
        naics = NAICSCode(
            code="541511",
            title="Custom Computer Programming Services",
            category=NAICSCategory.TECHNOLOGY
        )
        assert naics.category == NAICSCategory.TECHNOLOGY

    def test_auto_detect_level(self):
        """Test automatic level detection on creation."""
        sector = NAICSCode(code="54", title="Professional Services")
        subsector = NAICSCode(code="541", title="Professional Services")
        industry_group = NAICSCode(code="5415", title="Computer Services")
        national = NAICSCode(code="541511", title="Custom Programming")

        assert sector.level == NAICSLevel.SECTOR
        assert subsector.level == NAICSLevel.SUBSECTOR
        assert industry_group.level == NAICSLevel.INDUSTRY_GROUP
        assert national.level == NAICSLevel.NATIONAL_INDUSTRY

    def test_auto_set_parent_code(self):
        """Test automatic parent code detection."""
        naics = NAICSCode(code="541511", title="Custom Programming")
        assert naics.parent_code == "5415"

        naics_4 = NAICSCode(code="5415", title="Computer Services")
        assert naics_4.parent_code == "541"

        naics_3 = NAICSCode(code="541", title="Professional Services")
        assert naics_3.parent_code == "54"

        naics_2 = NAICSCode(code="54", title="Sector")
        assert naics_2.parent_code is None

    def test_normalize_code_on_init(self):
        """Test code normalization during initialization."""
        naics = NAICSCode(code="  541511  ", title="Test")
        assert naics.code == "541511"


class TestNAICSCodeFactory:
    """Test NAICS code factory function."""

    def test_factory_creates_code(self):
        """Test factory function creates NAICS code."""
        naics = create_naics_code(
            code="541511",
            title="Custom Computer Programming Services",
            category=NAICSCategory.TECHNOLOGY
        )
        assert isinstance(naics, NAICSCode)
        assert naics.code == "541511"
        assert naics.title == "Custom Computer Programming Services"
        assert naics.category == NAICSCategory.TECHNOLOGY

    def test_factory_auto_detects_level(self):
        """Test factory auto-detects level."""
        naics = create_naics_code(code="54", title="Sector")
        assert naics.level == NAICSLevel.SECTOR

    def test_factory_auto_sets_parent(self):
        """Test factory auto-sets parent code."""
        naics = create_naics_code(code="541511", title="Programming")
        assert naics.parent_code == "5415"

    def test_factory_normalizes_code(self):
        """Test factory normalizes code."""
        naics = create_naics_code(code="  541  ", title="Test")
        assert naics.code == "541"


class TestNAICSCodeHierarchy:
    """Test NAICS code hierarchical operations."""

    def test_get_hierarchy(self):
        """Test getting full hierarchy for a code."""
        naics = NAICSCode(code="541511", title="Programming")
        hierarchy = naics.get_hierarchy()
        assert hierarchy == ["54", "541", "5415", "541511"]

    def test_is_parent_of(self):
        """Test parent relationship checking."""
        sector = NAICSCode(code="54", title="Professional Services")
        assert sector.is_parent_of("541")
        assert sector.is_parent_of("5415")
        assert sector.is_parent_of("541511")
        assert not sector.is_parent_of("54")  # Not parent of itself
        assert not sector.is_parent_of("62")  # Not parent of different sector

    def test_is_child_of(self):
        """Test child relationship checking."""
        naics = NAICSCode(code="541511", title="Programming")
        assert naics.is_child_of("54")
        assert naics.is_child_of("541")
        assert naics.is_child_of("5415")
        assert not naics.is_child_of("541511")  # Not child of itself
        assert not naics.is_child_of("62")  # Not child of different sector


class TestNAICSCodeSerialization:
    """Test NAICS code serialization to dictionary."""

    def test_to_dict(self):
        """Test converting NAICS code to dictionary."""
        naics = create_naics_code(
            code="541511",
            title="Custom Computer Programming Services",
            description="Software development",
            category=NAICSCategory.TECHNOLOGY
        )
        data = naics.to_dict()

        assert data["code"] == "541511"
        assert data["title"] == "Custom Computer Programming Services"
        assert data["description"] == "Software development"
        assert data["level"] == "NATIONAL_INDUSTRY"
        assert data["level_value"] == 6
        assert data["category"] == "technology"
        assert data["parent_code"] == "5415"
        assert data["is_active"] is True
        assert data["year"] == 2022
        assert data["hierarchy"] == ["54", "541", "5415", "541511"]

    def test_to_dict_includes_timestamps(self):
        """Test dictionary includes timestamp fields."""
        naics = create_naics_code(code="54", title="Sector")
        data = naics.to_dict()

        assert "created_at" in data
        assert "updated_at" in data


class TestFallbackNAICS:
    """Test fallback NAICS code constant."""

    def test_fallback_code_exists(self):
        """Test fallback NAICS code is defined."""
        assert FALLBACK_NAICS is not None
        assert isinstance(FALLBACK_NAICS, NAICSCode)

    def test_fallback_code_value(self):
        """Test fallback code has correct value."""
        assert FALLBACK_NAICS.code == "123456"

    def test_fallback_code_title(self):
        """Test fallback code has title."""
        assert "General" in FALLBACK_NAICS.title or "Unclassified" in FALLBACK_NAICS.title

    def test_fallback_code_category(self):
        """Test fallback code has general category."""
        assert FALLBACK_NAICS.category == NAICSCategory.GENERAL
