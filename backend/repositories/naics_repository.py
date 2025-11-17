"""
NAICS Repository

This module implements the Repository pattern for NAICS code data access.
The repository provides efficient lookups, search, and filtering of NAICS codes.

Architecture:
    Controllers/API → Services → Repositories → Data Store

The NAICS repository handles:
- NAICS code storage and retrieval
- Search and autocomplete functionality
- Hierarchical code lookups (parent/child relationships)
- Category-based filtering
- Code validation against official NAICS database
"""

from typing import Optional, List, Dict
import json
import os
from pathlib import Path

from backend.models.naics import (
    NAICSCode,
    NAICSCategory,
    NAICSLevel,
    create_naics_code,
    FALLBACK_NAICS,
    normalize_naics_code,
)


class NAICSRepository:
    """
    Repository for NAICS code data access operations.

    This class provides an abstraction layer for accessing NAICS code data.
    It loads the official 2022 NAICS codes from a JSON file and provides
    efficient indexing and search capabilities.

    Design Pattern: Repository Pattern
    - Centralizes NAICS code data access logic
    - Provides consistent interface for NAICS operations
    - Enables fast lookups via multiple indexes
    - Supports hierarchical code relationships

    Attributes:
        _naics_codes: Dictionary mapping code -> NAICSCode object
        _category_index: Index for fast category lookups
        _level_index: Index for fast level lookups
        _title_index: Index for searching by title keywords

    Examples:
        >>> repo = NAICSRepository()
        >>> code = repo.find_by_code("541511")
        >>> print(code.title)
        'Custom Computer Programming Services'

        >>> tech_codes = repo.find_by_category(NAICSCategory.TECHNOLOGY)
        >>> print(len(tech_codes))
        10
    """

    def __init__(self, data_file_path: Optional[str] = None):
        """
        Initialize the NAICSRepository and load NAICS codes.

        Args:
            data_file_path: Path to NAICS codes JSON file. If None, uses default.
        """
        self._naics_codes: Dict[str, NAICSCode] = {}
        self._category_index: Dict[str, List[str]] = {}  # category -> [codes]
        self._level_index: Dict[int, List[str]] = {}  # level -> [codes]
        self._title_index: Dict[str, List[str]] = {}  # keyword -> [codes]

        # Load NAICS codes from data file
        if data_file_path is None:
            # Default path: backend/data/naics_codes_2022.json
            current_file = Path(__file__)
            backend_dir = current_file.parent.parent
            data_file_path = backend_dir / "data" / "naics_codes_2022.json"

        self._load_naics_codes(str(data_file_path))

    def _load_naics_codes(self, file_path: str) -> None:
        """
        Load NAICS codes from JSON file and build indexes.

        Args:
            file_path: Path to NAICS codes JSON file
        """
        if not os.path.exists(file_path):
            # If file doesn't exist, at least add the fallback code
            self._add_to_indexes(FALLBACK_NAICS)
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                naics_data = json.load(f)

            for item in naics_data:
                # Create NAICSCode instance
                try:
                    category = NAICSCategory(item.get("category", "general"))
                except ValueError:
                    category = NAICSCategory.GENERAL

                naics_code = create_naics_code(
                    code=item["code"],
                    title=item["title"],
                    description=item.get("description", ""),
                    category=category,
                    is_active=item.get("is_active", True),
                )

                # Add to main storage and indexes
                self._add_to_indexes(naics_code)

        except (json.JSONDecodeError, FileNotFoundError, KeyError) as e:
            # If loading fails, at least add the fallback code
            print(f"Warning: Failed to load NAICS codes from {file_path}: {e}")
            self._add_to_indexes(FALLBACK_NAICS)

    def _add_to_indexes(self, naics_code: NAICSCode) -> None:
        """
        Add a NAICS code to all indexes for efficient lookups.

        Args:
            naics_code: NAICSCode instance to index
        """
        code = naics_code.code

        # Main storage
        self._naics_codes[code] = naics_code

        # Category index
        category_key = naics_code.category.value
        if category_key not in self._category_index:
            self._category_index[category_key] = []
        if code not in self._category_index[category_key]:
            self._category_index[category_key].append(code)

        # Level index
        level_key = naics_code.level.value
        if level_key not in self._level_index:
            self._level_index[level_key] = []
        if code not in self._level_index[level_key]:
            self._level_index[level_key].append(code)

        # Title keyword index
        # Tokenize title into words for search
        title_words = naics_code.title.lower().split()
        for word in title_words:
            # Only index words >= 3 characters
            if len(word) >= 3:
                if word not in self._title_index:
                    self._title_index[word] = []
                if code not in self._title_index[word]:
                    self._title_index[word].append(code)

    def find_by_code(self, code: str) -> Optional[NAICSCode]:
        """
        Find a NAICS code by its code string.

        Args:
            code: NAICS code to find (e.g., "541511")

        Returns:
            NAICSCode if found, None otherwise

        Examples:
            >>> repo = NAICSRepository()
            >>> code = repo.find_by_code("541511")
            >>> code.title
            'Custom Computer Programming Services'
        """
        normalized = normalize_naics_code(code)
        return self._naics_codes.get(normalized)

    def find_by_category(self, category: NAICSCategory) -> List[NAICSCode]:
        """
        Find all NAICS codes in a specific category.

        Args:
            category: NAICSCategory to filter by

        Returns:
            List of NAICSCode objects in the category

        Examples:
            >>> repo = NAICSRepository()
            >>> tech_codes = repo.find_by_category(NAICSCategory.TECHNOLOGY)
            >>> len(tech_codes) > 0
            True
        """
        code_list = self._category_index.get(category.value, [])
        return [self._naics_codes[code] for code in code_list]

    def find_by_level(self, level: NAICSLevel) -> List[NAICSCode]:
        """
        Find all NAICS codes at a specific hierarchical level.

        Args:
            level: NAICSLevel to filter by (SECTOR, SUBSECTOR, etc.)

        Returns:
            List of NAICSCode objects at the specified level

        Examples:
            >>> repo = NAICSRepository()
            >>> sectors = repo.find_by_level(NAICSLevel.SECTOR)
            >>> all(len(code.code) == 2 for code in sectors)
            True
        """
        code_list = self._level_index.get(level.value, [])
        return [self._naics_codes[code] for code in code_list]

    def search_by_title(self, query: str, limit: int = 20) -> List[NAICSCode]:
        """
        Search NAICS codes by title keywords.

        Args:
            query: Search query string
            limit: Maximum number of results to return

        Returns:
            List of matching NAICSCode objects

        Examples:
            >>> repo = NAICSRepository()
            >>> results = repo.search_by_title("computer")
            >>> any("computer" in code.title.lower() for code in results)
            True
        """
        if not query:
            return []

        query_lower = query.lower()
        matching_codes = set()

        # Search in title index
        for word in query_lower.split():
            if len(word) >= 3 and word in self._title_index:
                matching_codes.update(self._title_index[word])

        # Also check for partial matches in titles
        for code, naics in self._naics_codes.items():
            if query_lower in naics.title.lower():
                matching_codes.add(code)

        # Convert to NAICSCode objects and limit results
        results = [self._naics_codes[code] for code in matching_codes]
        return results[:limit]

    def get_children(self, parent_code: str) -> List[NAICSCode]:
        """
        Get all child codes of a parent NAICS code.

        Args:
            parent_code: Parent NAICS code

        Returns:
            List of child NAICSCode objects

        Examples:
            >>> repo = NAICSRepository()
            >>> parent = repo.find_by_code("54")
            >>> children = repo.get_children("54")
            >>> all(child.code.startswith("54") for child in children)
            True
        """
        normalized = normalize_naics_code(parent_code)
        if not normalized:
            return []

        children = []
        for code, naics in self._naics_codes.items():
            if naics.is_child_of(normalized):
                children.append(naics)

        return children

    def get_parent(self, code: str) -> Optional[NAICSCode]:
        """
        Get the parent NAICS code of a given code.

        Args:
            code: NAICS code to find parent for

        Returns:
            Parent NAICSCode if found, None otherwise

        Examples:
            >>> repo = NAICSRepository()
            >>> child = repo.find_by_code("541511")
            >>> parent = repo.get_parent("541511")
            >>> parent.code
            '5415'
        """
        naics = self.find_by_code(code)
        if not naics or not naics.parent_code:
            return None

        return self.find_by_code(naics.parent_code)

    def get_hierarchy(self, code: str) -> List[NAICSCode]:
        """
        Get the full hierarchical path for a NAICS code.

        Returns all parent codes from sector to the given code.

        Args:
            code: NAICS code to get hierarchy for

        Returns:
            List of NAICSCode objects from sector to code

        Examples:
            >>> repo = NAICSRepository()
            >>> hierarchy = repo.get_hierarchy("541511")
            >>> [c.code for c in hierarchy]
            ['54', '541', '5415', '541511']
        """
        naics = self.find_by_code(code)
        if not naics:
            return []

        hierarchy_codes = naics.get_hierarchy()
        hierarchy = []

        for code_str in hierarchy_codes:
            naics_code = self.find_by_code(code_str)
            if naics_code:
                hierarchy.append(naics_code)

        return hierarchy

    def is_valid_code(self, code: str) -> bool:
        """
        Check if a NAICS code exists in the official database.

        Args:
            code: NAICS code to validate

        Returns:
            True if code exists, False otherwise

        Examples:
            >>> repo = NAICSRepository()
            >>> repo.is_valid_code("541511")
            True

            >>> repo.is_valid_code("999999")
            False
        """
        normalized = normalize_naics_code(code)
        return normalized in self._naics_codes

    def get_all_codes(self, active_only: bool = True) -> List[NAICSCode]:
        """
        Get all NAICS codes in the repository.

        Args:
            active_only: If True, return only active codes

        Returns:
            List of all NAICSCode objects

        Examples:
            >>> repo = NAICSRepository()
            >>> all_codes = repo.get_all_codes()
            >>> len(all_codes) > 0
            True
        """
        if active_only:
            return [
                naics for naics in self._naics_codes.values()
                if naics.is_active
            ]
        return list(self._naics_codes.values())

    def count(self) -> int:
        """
        Get the total count of NAICS codes in the repository.

        Returns:
            Number of NAICS codes

        Examples:
            >>> repo = NAICSRepository()
            >>> repo.count() > 0
            True
        """
        return len(self._naics_codes)

    def get_categories_summary(self) -> Dict[str, int]:
        """
        Get a summary of NAICS codes by category.

        Returns:
            Dictionary mapping category names to code counts

        Examples:
            >>> repo = NAICSRepository()
            >>> summary = repo.get_categories_summary()
            >>> 'technology' in summary
            True
        """
        summary = {}
        for category, codes in self._category_index.items():
            summary[category] = len(codes)
        return summary
