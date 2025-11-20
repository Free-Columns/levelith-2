"""
NAICS Code Domain Models

This module defines the NAICS (North American Industry Classification System)
domain model with metadata support.

NAICS codes are hierarchical:
- 2-digit: Sector (e.g., "54" = Professional, Scientific, and Technical Services)
- 3-digit: Subsector (e.g., "541" = Professional, Scientific, and Technical Services)
- 4-digit: Industry Group (e.g., "5415" = Computer Systems Design and Related Services)
- 6-digit: National Industry (e.g., "541511" = Custom Computer Programming Services)

Based on the 2022 NAICS codes from the U.S. Census Bureau.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from enum import Enum


class NAICSLevel(Enum):
    """
    NAICS code hierarchy levels.

    NAICS codes have 4 hierarchical levels based on digit count:
    - SECTOR: 2 digits (e.g., "54")
    - SUBSECTOR: 3 digits (e.g., "541")
    - INDUSTRY_GROUP: 4 digits (e.g., "5415")
    - NATIONAL_INDUSTRY: 6 digits (e.g., "541511")
    """
    SECTOR = 2
    SUBSECTOR = 3
    INDUSTRY_GROUP = 4
    NATIONAL_INDUSTRY = 6


class NAICSCategory(Enum):
    """
    High-level industry categories for classification.

    These map NAICS sectors to broad categories for easier filtering
    and user experience improvements.
    """
    TECHNOLOGY = "technology"
    EDUCATION = "education"
    HEALTHCARE = "healthcare"
    FINANCE = "finance"
    MANUFACTURING = "manufacturing"
    RETAIL = "retail"
    HOSPITALITY = "hospitality"
    CONSTRUCTION = "construction"
    AGRICULTURE = "agriculture"
    TRANSPORTATION = "transportation"
    PROFESSIONAL_SERVICES = "professional_services"
    ARTS_ENTERTAINMENT = "arts_entertainment"
    PUBLIC_ADMINISTRATION = "public_administration"
    GENERAL = "general"  # Fallback category


# NAICS validation constants
NAICS_FALLBACK_CODE = "123456"
NAICS_FALLBACK_TITLE = "General/Unclassified"
NAICS_FALLBACK_CATEGORY = NAICSCategory.GENERAL

# Valid NAICS code lengths (2, 3, 4, or 6 digits)
VALID_NAICS_LENGTHS = [2, 3, 4, 6]


def get_naics_level(code: str) -> Optional[NAICSLevel]:
    """
    Determine the hierarchical level of a NAICS code based on length.

    Args:
        code: NAICS code string

    Returns:
        NAICSLevel if valid length, None otherwise

    Examples:
        >>> get_naics_level("54")
        NAICSLevel.SECTOR

        >>> get_naics_level("541")
        NAICSLevel.SUBSECTOR

        >>> get_naics_level("541511")
        NAICSLevel.NATIONAL_INDUSTRY
    """
    if not code or not isinstance(code, str):
        return None

    code_length = len(code.strip())

    if code_length == 2:
        return NAICSLevel.SECTOR
    elif code_length == 3:
        return NAICSLevel.SUBSECTOR
    elif code_length == 4:
        return NAICSLevel.INDUSTRY_GROUP
    elif code_length == 6:
        return NAICSLevel.NATIONAL_INDUSTRY

    return None


def normalize_naics_code(code: str) -> str:
    """
    Normalize NAICS code by trimming whitespace and validating format.

    Args:
        code: NAICS code to normalize

    Returns:
        Normalized NAICS code or fallback code if invalid

    Examples:
        >>> normalize_naics_code("  541511  ")
        '541511'

        >>> normalize_naics_code("invalid")
        '123456'
    """
    if not code:
        return NAICS_FALLBACK_CODE

    # Remove whitespace and convert to string
    code = str(code).strip()

    # Must be numeric
    if not code.isdigit():
        return NAICS_FALLBACK_CODE

    # Must be valid length (2, 3, 4, or 6)
    if len(code) not in VALID_NAICS_LENGTHS:
        return NAICS_FALLBACK_CODE

    return code


def extract_parent_codes(code: str) -> List[str]:
    """
    Extract all parent codes from a NAICS code.

    For a 6-digit code like "541511", returns the hierarchy:
    ["54", "541", "5415", "541511"]

    Args:
        code: Full NAICS code

    Returns:
        List of parent codes from sector to national industry

    Examples:
        >>> extract_parent_codes("541511")
        ['54', '541', '5415', '541511']

        >>> extract_parent_codes("541")
        ['54', '541']
    """
    if not code or len(code) < 2:
        return []

    parents = []

    # Add 2-digit sector
    if len(code) >= 2:
        parents.append(code[:2])

    # Add 3-digit subsector
    if len(code) >= 3:
        parents.append(code[:3])

    # Add 4-digit industry group
    if len(code) >= 4:
        parents.append(code[:4])

    # Add 6-digit national industry
    if len(code) == 6:
        parents.append(code)

    return parents


@dataclass
class NAICSCode:
    """
    NAICS Code domain model with complete metadata and enhanced search support.

    Attributes:
        code: The NAICS code (2, 3, 4, or 6 digits)
        title: Official NAICS title
        description: Detailed description of what this code represents
        level: Hierarchical level (sector, subsector, industry group, national industry)
        category: High-level category for filtering (technology, education, etc.)
        parent_code: Parent code in the hierarchy (None for 2-digit sectors)
        
        # Denormalized hierarchy for fast queries
        sector: 2-digit sector code
        subsector: 3-digit subsector code
        industry_group: 4-digit industry group code
        industry_detail: 6-digit national industry code
        
        # SBA integration
        sba_size_standard: Small Business Administration size standard
        sba_source: Source reference for SBA data
        
        # Enhanced search and discovery
        keywords: List of searchable keywords
        aliases: List of alternative names/synonyms for better matching
        examples: Text examples of businesses in this classification
        
        # Documentation
        cross_references: List of related NAICS codes
        notes: Additional notes about this classification
        data_source: Source of the NAICS data
        
        # Admin fields
        tags: Custom tags for admin organization and filtering
        custom_category: Admin-defined category for internal classification
        admin_notes: Internal notes and comments for admin use only
        
        # Metadata
        is_active: Whether this code is currently active in NAICS 2022
        year: NAICS version year (default: 2022)
        created_at: When this code record was created
        updated_at: When this code record was last updated
    """

    code: str
    title: str
    description: str = ""
    level: NAICSLevel = NAICSLevel.NATIONAL_INDUSTRY
    category: NAICSCategory = NAICSCategory.GENERAL
    parent_code: Optional[str] = None
    
    # Denormalized hierarchy
    sector: Optional[str] = None
    subsector: Optional[str] = None
    industry_group: Optional[str] = None
    industry_detail: Optional[str] = None
    
    # SBA integration
    sba_size_standard: Optional[str] = None
    sba_source: Optional[str] = None
    
    # Enhanced search
    keywords: List[str] = field(default_factory=list)
    aliases: List[str] = field(default_factory=list)
    examples: Optional[str] = None
    
    # Documentation
    cross_references: List[str] = field(default_factory=list)
    notes: Optional[str] = None
    data_source: Optional[str] = None
    
    # Admin fields
    is_active: bool = True
    year: int = 2022
    tags: List[str] = field(default_factory=list)
    custom_category: Optional[str] = None
    admin_notes: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Validate and auto-populate fields after initialization."""
        from backend.models.naics import normalize_naics_code, get_naics_level, extract_parent_codes
        
        # Normalize the code
        self.code = normalize_naics_code(self.code)

        # Auto-detect level if not set correctly
        detected_level = get_naics_level(self.code)
        if detected_level:
            self.level = detected_level

        # Auto-populate denormalized hierarchy fields
        if len(self.code) >= 2:
            self.sector = self.code[:2]
        if len(self.code) >= 3:
            self.subsector = self.code[:3]
        if len(self.code) >= 4:
            self.industry_group = self.code[:4]
        if len(self.code) == 6:
            self.industry_detail = self.code

        # Auto-set parent code based on hierarchy
        if not self.parent_code and len(self.code) > 2:
            parents = extract_parent_codes(self.code)
            if len(parents) > 1:
                self.parent_code = parents[-2]

    def get_hierarchy(self) -> List[str]:
        """Get the full hierarchical path for this NAICS code."""
        from backend.models.naics import extract_parent_codes
        return extract_parent_codes(self.code)

    def get_all_search_terms(self) -> List[str]:
        """
        Get all searchable terms for this NAICS code.
        
        Combines title words, keywords, and aliases for comprehensive searching.
        
        Returns:
            List of unique search terms (lowercased)
        """
        terms = set()
        
        # Add title words
        terms.update(self.title.lower().split())
        
        # Add keywords
        terms.update(k.lower() for k in self.keywords)
        
        # Add aliases
        terms.update(a.lower() for a in self.aliases)
        
        # Add code itself
        terms.add(self.code)
        
        return sorted(list(terms))

    def matches_search_term(self, term: str) -> bool:
        """
        Check if this NAICS code matches a search term.
        
        Searches in: code, title, keywords, aliases, description
        
        Args:
            term: Search term (case-insensitive)
            
        Returns:
            True if term matches any searchable field
        """
        term_lower = term.lower()
        
        # Check code
        if term_lower in self.code.lower():
            return True
        
        # Check title
        if term_lower in self.title.lower():
            return True
        
        # Check keywords
        if any(term_lower in k.lower() for k in self.keywords):
            return True
        
        # Check aliases
        if any(term_lower in a.lower() for a in self.aliases):
            return True
        
        # Check description
        if self.description and term_lower in self.description.lower():
            return True
        
        return False

    def to_dict(self) -> dict:
        """Convert NAICS code to dictionary representation."""
        return {
            "code": self.code,
            "title": self.title,
            "description": self.description,
            "level": self.level.name,
            "level_value": self.level.value,
            "category": self.category.value,
            "parent_code": self.parent_code,
            
            # Hierarchy
            "sector": self.sector,
            "subsector": self.subsector,
            "industry_group": self.industry_group,
            "industry_detail": self.industry_detail,
            "hierarchy": self.get_hierarchy(),
            
            # SBA
            "sba_size_standard": self.sba_size_standard,
            "sba_source": self.sba_source,
            
            # Search
            "keywords": self.keywords,
            "aliases": self.aliases,
            "examples": self.examples,
            
            # Documentation
            "cross_references": self.cross_references,
            "notes": self.notes,
            "data_source": self.data_source,
            
            # Admin
            "tags": self.tags,
            "custom_category": self.custom_category,
            "admin_notes": self.admin_notes,
            
            # Metadata
            "is_active": self.is_active,
            "year": self.year,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }




def create_naics_code(
    code: str,
    title: str,
    description: str = "",
    category: NAICSCategory = NAICSCategory.GENERAL,
    is_active: bool = True,
) -> NAICSCode:
    """
    Factory function to create a NAICSCode instance.

    This function handles normalization and validation automatically.

    Args:
        code: NAICS code (2, 3, 4, or 6 digits)
        title: Official NAICS title
        description: Detailed description (optional)
        category: Industry category for filtering
        is_active: Whether this code is currently active

    Returns:
        NAICSCode instance

    Examples:
        >>> naics = create_naics_code(
        ...     code="541511",
        ...     title="Custom Computer Programming Services",
        ...     category=NAICSCategory.TECHNOLOGY
        ... )
        >>> naics.code
        '541511'
    """
    # Normalize code first
    normalized_code = normalize_naics_code(code)

    # Auto-detect level
    level = get_naics_level(normalized_code) or NAICSLevel.NATIONAL_INDUSTRY

    # Auto-detect parent
    parent_code = None
    if len(normalized_code) > 2:
        hierarchy = extract_parent_codes(normalized_code)
        if len(hierarchy) > 1:
            parent_code = hierarchy[-2]

    return NAICSCode(
        code=normalized_code,
        title=title,
        description=description,
        level=level,
        category=category,
        parent_code=parent_code,
        is_active=is_active,
    )


# Fallback NAICS code instance
FALLBACK_NAICS = create_naics_code(
    code=NAICS_FALLBACK_CODE,
    title=NAICS_FALLBACK_TITLE,
    description="General or unclassified industry. Used as fallback when specific NAICS code is not provided.",
    category=NAICS_FALLBACK_CATEGORY,
    is_active=True,
)
