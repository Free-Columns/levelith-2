"""
NAICS Service

This module implements the Service layer for NAICS code business logic.
The service layer provides high-level operations for NAICS code lookups,
validation, search, and suggestions.

Architecture:
    Controllers/API → Services → Repositories → Data Store

The service layer handles:
- NAICS code validation and lookup
- Search and autocomplete functionality
- Suggestions based on experience types
- Category mapping and analytics
- Hierarchical code operations
"""

from typing import Optional, List, Dict
from backend.models.naics import (
    NAICSCode,
    NAICSCategory,
    NAICSLevel,
    normalize_naics_code,
    FALLBACK_NAICS,
    NAICS_FALLBACK_CODE,
)
from backend.models.experience import ExperienceType, ExperienceCategory
from backend.repositories.naics_repository import NAICSRepository


class NAICSService:
    """
    Service for NAICS code business logic and operations.

    This class encapsulates all business logic related to NAICS code
    management, including validation, search, suggestions, and analytics.

    Design Pattern: Service Layer Pattern
    - Encapsulates business logic separate from data access
    - Provides intelligent NAICS code suggestions
    - Validates codes against official NAICS database
    - Offers search and autocomplete capabilities

    Attributes:
        naics_repo: NAICSRepository instance for data access

    Examples:
        >>> from backend.repositories import NAICSRepository
        >>> repo = NAICSRepository()
        >>> service = NAICSService(naics_repo=repo)
        >>> code = service.lookup_code("541511")
        >>> print(code.title)
        'Custom Computer Programming Services'
    """

    def __init__(self, naics_repo: NAICSRepository):
        """
        Initialize NAICSService with required dependencies.

        Args:
            naics_repo: NAICSRepository instance for data access

        Example:
            >>> repo = NAICSRepository()
            >>> service = NAICSService(naics_repo=repo)
        """
        self.naics_repo = naics_repo

        # Build experience type to NAICS category mapping
        self._experience_category_mapping = self._build_category_mapping()

    def _build_category_mapping(self) -> Dict[str, List[NAICSCategory]]:
        """
        Build mapping from experience types to relevant NAICS categories.

        This helps suggest appropriate NAICS codes based on experience type.

        Returns:
            Dictionary mapping experience type to NAICS categories
        """
        return {
            # Education experience types
            "certificate": [
                NAICSCategory.EDUCATION,
                NAICSCategory.PROFESSIONAL_SERVICES,
            ],
            "degree": [NAICSCategory.EDUCATION],
            "course": [
                NAICSCategory.EDUCATION,
                NAICSCategory.TECHNOLOGY,
            ],
            # Workplace experience types
            "gig": [
                NAICSCategory.TECHNOLOGY,
                NAICSCategory.PROFESSIONAL_SERVICES,
                NAICSCategory.ARTS_ENTERTAINMENT,
            ],
            "part_time": [
                NAICSCategory.RETAIL,
                NAICSCategory.HOSPITALITY,
                NAICSCategory.TECHNOLOGY,
            ],
            "full_time": [
                NAICSCategory.TECHNOLOGY,
                NAICSCategory.FINANCE,
                NAICSCategory.HEALTHCARE,
                NAICSCategory.PROFESSIONAL_SERVICES,
                NAICSCategory.MANUFACTURING,
            ],
            # Skills experience types (use general fallback)
            "soft_skill": [NAICSCategory.GENERAL],
            "hard_skill": [NAICSCategory.GENERAL],
            "native_skill": [NAICSCategory.GENERAL],
        }

    def lookup_code(self, code: str) -> Optional[NAICSCode]:
        """
        Look up a NAICS code and return its metadata.

        Args:
            code: NAICS code to look up

        Returns:
            NAICSCode if found, None otherwise

        Examples:
            >>> service = NAICSService(NAICSRepository())
            >>> code = service.lookup_code("541511")
            >>> code.title
            'Custom Computer Programming Services'
        """
        return self.naics_repo.find_by_code(code)

    def validate_code(self, code: str) -> tuple[bool, str]:
        """
        Validate a NAICS code and return validation result.

        Args:
            code: NAICS code to validate

        Returns:
            Tuple of (is_valid, normalized_code_or_fallback)

        Examples:
            >>> service = NAICSService(NAICSRepository())
            >>> is_valid, normalized = service.validate_code("541511")
            >>> is_valid
            True

            >>> is_valid, normalized = service.validate_code("invalid")
            >>> is_valid
            False
            >>> normalized
            '123456'
        """
        original_code = code.strip() if code else ""
        normalized = normalize_naics_code(code)

        # If normalization resulted in fallback code and it's different from original,
        # the original code was invalid
        if normalized == NAICS_FALLBACK_CODE and original_code.upper() != NAICS_FALLBACK_CODE:
            return (False, FALLBACK_NAICS.code)

        # Check if it's in the official database
        is_valid = self.naics_repo.is_valid_code(normalized)

        # If invalid, return fallback
        if not is_valid:
            return (False, FALLBACK_NAICS.code)

        return (True, normalized)

    def validate_with_metadata(self, code: str) -> tuple[bool, NAICSCode]:
        """
        Validate a NAICS code and return validation result with metadata.

        Args:
            code: NAICS code to validate

        Returns:
            Tuple of (is_valid, NAICSCode object)

        Examples:
            >>> service = NAICSService(NAICSRepository())
            >>> is_valid, naics = service.validate_with_metadata("541511")
            >>> is_valid
            True
            >>> naics.title
            'Custom Computer Programming Services'
        """
        is_valid, normalized = self.validate_code(code)

        if is_valid:
            naics = self.naics_repo.find_by_code(normalized)
            return (True, naics)
        else:
            return (False, FALLBACK_NAICS)

    def search(self, query: str, limit: int = 20) -> List[NAICSCode]:
        """
        Search for NAICS codes by title or description.

        Args:
            query: Search query string
            limit: Maximum number of results

        Returns:
            List of matching NAICSCode objects

        Examples:
            >>> service = NAICSService(NAICSRepository())
            >>> results = service.search("computer programming")
            >>> len(results) > 0
            True
        """
        if not query:
            return []

        return self.naics_repo.search_by_title(query, limit=limit)

    def autocomplete(self, partial: str, limit: int = 10) -> List[Dict[str, str]]:
        """
        Provide autocomplete suggestions for NAICS codes.

        Args:
            partial: Partial search string
            limit: Maximum number of suggestions

        Returns:
            List of dictionaries with code and title

        Examples:
            >>> service = NAICSService(NAICSRepository())
            >>> suggestions = service.autocomplete("comp")
            >>> len(suggestions) > 0
            True
        """
        results = self.search(partial, limit=limit)

        return [
            {
                "code": naics.code,
                "title": naics.title,
                "description": naics.description,
                "category": naics.category.value,
            }
            for naics in results
        ]

    def suggest_for_experience(
        self,
        experience_type: str,
        title: Optional[str] = None,
        limit: int = 10
    ) -> List[NAICSCode]:
        """
        Suggest relevant NAICS codes for a given experience type.

        If title is provided, uses intelligent search. Otherwise, returns
        codes from categories typically associated with the experience type.

        Args:
            experience_type: Type of experience (e.g., "full_time", "degree")
            title: Optional experience title for intelligent matching
            limit: Maximum number of suggestions

        Returns:
            List of suggested NAICSCode objects

        Examples:
            >>> service = NAICSService(NAICSRepository())
            >>> suggestions = service.suggest_for_experience(
            ...     "full_time",
            ...     title="Software Engineer"
            ... )
            >>> len(suggestions) > 0
            True
        """
        suggestions = []

        # If title provided, use search
        if title:
            suggestions = self.search(title, limit=limit)

        # If no title or insufficient results, use category mapping
        if len(suggestions) < limit:
            categories = self._experience_category_mapping.get(
                experience_type,
                [NAICSCategory.GENERAL]
            )

            for category in categories:
                category_codes = self.naics_repo.find_by_category(category)
                suggestions.extend(category_codes)

                if len(suggestions) >= limit:
                    break

        return suggestions[:limit]

    def get_by_category(self, category: str) -> List[NAICSCode]:
        """
        Get all NAICS codes in a specific category.

        Args:
            category: Category name (e.g., "technology", "education")

        Returns:
            List of NAICSCode objects in the category

        Examples:
            >>> service = NAICSService(NAICSRepository())
            >>> tech_codes = service.get_by_category("technology")
            >>> len(tech_codes) > 0
            True
        """
        try:
            naics_category = NAICSCategory(category)
            return self.naics_repo.find_by_category(naics_category)
        except ValueError:
            return []

    def get_by_level(self, level: int) -> List[NAICSCode]:
        """
        Get all NAICS codes at a specific hierarchical level.

        Args:
            level: Level value (2, 3, 4, or 6)

        Returns:
            List of NAICSCode objects at the level

        Examples:
            >>> service = NAICSService(NAICSRepository())
            >>> sectors = service.get_by_level(2)
            >>> all(len(code.code) == 2 for code in sectors)
            True
        """
        try:
            naics_level = NAICSLevel(level)
            return self.naics_repo.find_by_level(naics_level)
        except ValueError:
            return []

    def get_hierarchy(self, code: str) -> List[NAICSCode]:
        """
        Get the full hierarchical path for a NAICS code.

        Returns all parent codes from sector to the given code.

        Args:
            code: NAICS code

        Returns:
            List of NAICSCode objects from sector to code

        Examples:
            >>> service = NAICSService(NAICSRepository())
            >>> hierarchy = service.get_hierarchy("541511")
            >>> [c.code for c in hierarchy]
            ['54', '541', '5415', '541511']
        """
        return self.naics_repo.get_hierarchy(code)

    def get_children(self, parent_code: str) -> List[NAICSCode]:
        """
        Get all child codes of a parent NAICS code.

        Args:
            parent_code: Parent NAICS code

        Returns:
            List of child NAICSCode objects

        Examples:
            >>> service = NAICSService(NAICSRepository())
            >>> children = service.get_children("54")
            >>> len(children) > 0
            True
        """
        return self.naics_repo.get_children(parent_code)

    def get_parent(self, code: str) -> Optional[NAICSCode]:
        """
        Get the parent NAICS code of a given code.

        Args:
            code: NAICS code

        Returns:
            Parent NAICSCode if found, None otherwise

        Examples:
            >>> service = NAICSService(NAICSRepository())
            >>> parent = service.get_parent("541511")
            >>> parent.code
            '5415'
        """
        return self.naics_repo.get_parent(code)

    def get_categories_summary(self) -> Dict[str, int]:
        """
        Get a summary of NAICS codes by category.

        Returns:
            Dictionary mapping category names to code counts

        Examples:
            >>> service = NAICSService(NAICSRepository())
            >>> summary = service.get_categories_summary()
            >>> 'technology' in summary
            True
        """
        return self.naics_repo.get_categories_summary()

    def get_all_categories(self) -> List[str]:
        """
        Get all available NAICS categories.

        Returns:
            List of category names

        Examples:
            >>> service = NAICSService(NAICSRepository())
            >>> categories = service.get_all_categories()
            >>> 'technology' in categories
            True
        """
        return [category.value for category in NAICSCategory]

    def update_code(self, code: str, updates: Dict) -> Optional[NAICSCode]:
        """
        Update admin-specific fields for a NAICS code.

        Only updates admin fields (tags, custom_category, admin_notes).
        Official NAICS data cannot be modified.

        Args:
            code: NAICS code to update
            updates: Dictionary with fields to update

        Returns:
            Updated NAICSCode if successful, None if code not found

        Examples:
            >>> service = NAICSService(NAICSDBRepository())
            >>> updated = service.update_code("541511", {
            ...     "tags": ["software", "programming"],
            ...     "custom_category": "Tech Services",
            ...     "admin_notes": "High demand sector"
            ... })
            >>> updated.tags
            ['software', 'programming']
        """
        # Validate code exists
        if not self.naics_repo.is_valid_code(code):
            return None

        # Only allow updating admin fields
        allowed_fields = {"tags", "custom_category", "admin_notes"}
        filtered_updates = {
            k: v for k, v in updates.items()
            if k in allowed_fields
        }

        if not filtered_updates:
            return self.lookup_code(code)  # No valid updates, return existing

        return self.naics_repo.update_code(code, filtered_updates)

    def delete_code(self, code: str) -> bool:
        """
        Delete a NAICS code from the database.

        WARNING: This permanently removes the code. Use with extreme caution.
        This should only be used for:
        - Removing test/dummy codes
        - Cleaning up invalid imports
        - NOT for official NAICS codes

        Args:
            code: NAICS code to delete

        Returns:
            True if deleted, False if not found or deletion failed

        Examples:
            >>> service = NAICSService(NAICSDBRepository())
            >>> service.delete_code("999999")
            True
        """
        # Validate code exists
        if not self.naics_repo.is_valid_code(code):
            return False

        return self.naics_repo.delete_code(code)

    def search_with_pagination(
        self,
        query: str = "",
        category: Optional[str] = None,
        level: Optional[int] = None,
        page: int = 1,
        page_size: int = 50
    ) -> Dict:
        """
        Search NAICS codes with server-side pagination.

        Optimized for large datasets (1000s+ codes) with filtering and pagination.

        Args:
            query: Search term for code/title/description
            category: Optional category filter
            level: Optional level filter (2, 3, 4, or 6)
            page: Page number (1-indexed)
            page_size: Results per page (default: 50)

        Returns:
            Dictionary with:
                - items: List of NAICSCode objects
                - total: Total matching records
                - page: Current page number
                - page_size: Items per page
                - total_pages: Total number of pages

        Examples:
            >>> service = NAICSService(NAICSDBRepository())
            >>> results = service.search_with_pagination("computer", page=1, page_size=10)
            >>> results["page"]
            1
            >>> len(results["items"]) <= 10
            True
        """
        # Convert category string to enum
        category_enum = None
        if category:
            try:
                category_enum = NAICSCategory(category)
            except ValueError:
                pass  # Invalid category, ignore filter

        # Convert level int to enum
        level_enum = None
        if level:
            try:
                if level == 2:
                    level_enum = NAICSLevel.SECTOR
                elif level == 3:
                    level_enum = NAICSLevel.SUBSECTOR
                elif level == 4:
                    level_enum = NAICSLevel.INDUSTRY_GROUP
                elif level == 6:
                    level_enum = NAICSLevel.NATIONAL_INDUSTRY
            except ValueError:
                pass  # Invalid level, ignore filter

        return self.naics_repo.search_with_pagination(
            query=query,
            category=category_enum,
            level=level_enum,
            page=page,
            page_size=page_size
        )
