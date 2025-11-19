"""
NAICS Database Repository

Database-backed implementation of the NAICS Repository pattern.
Queries NAICS codes from PostgreSQL instead of JSON files.

This repository provides the same interface as NAICSRepository but uses
the database for persistent storage and querying.
"""

from typing import Optional, List, Dict
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.models.naics import (
    NAICSCode,
    NAICSCategory,
    NAICSLevel,
    create_naics_code,
    FALLBACK_NAICS,
    normalize_naics_code,
)
from backend.models.db_models import NAICSCodeDB
from backend.database import get_db_context


class NAICSDBRepository:
    """
    Database-backed repository for NAICS code data access operations.

    This class provides the same interface as NAICSRepository but queries
    the PostgreSQL database instead of loading from JSON files.

    Design Pattern: Repository Pattern
    - Centralizes NAICS code data access logic
    - Provides consistent interface for NAICS operations
    - Leverages database indexes for efficient queries
    - Supports hierarchical code relationships

    Examples:
        >>> repo = NAICSDBRepository()
        >>> code = repo.find_by_code("541511")
        >>> print(code.title)
        'Custom Computer Programming Services'

        >>> tech_codes = repo.find_by_category(NAICSCategory.TECHNOLOGY)
        >>> print(len(tech_codes))
        10
    """

    def __init__(self, db: Optional[Session] = None):
        """
        Initialize the NAICSDBRepository.

        Args:
            db: Optional database session. If None, creates new session per query.
        """
        self._db = db
        self._owns_session = db is None

    def _get_db(self) -> Session:
        """
        Get database session.

        Returns:
            Database session
        """
        if self._db:
            return self._db

        # Create new session (caller must manage lifecycle)
        from backend.database import SessionLocal
        return SessionLocal()

    def _db_to_domain(self, db_code: NAICSCodeDB) -> NAICSCode:
        """
        Convert database model to domain model.

        Args:
            db_code: NAICSCodeDB instance

        Returns:
            NAICSCode domain object
        """
        naics_code = create_naics_code(
            code=db_code.code,
            title=db_code.title,
            description=db_code.description or "",
            category=db_code.category,
            is_active=db_code.is_active,
        )
        # Add admin-specific fields
        naics_code.tags = db_code.tags if db_code.tags else []
        naics_code.custom_category = db_code.custom_category
        naics_code.admin_notes = db_code.admin_notes
        naics_code.year = db_code.year
        naics_code.created_at = db_code.created_at
        naics_code.updated_at = db_code.updated_at
        return naics_code

    def find_by_code(self, code: str) -> Optional[NAICSCode]:
        """
        Find a NAICS code by its code string.

        Args:
            code: NAICS code to find (e.g., "541511")

        Returns:
            NAICSCode if found, None otherwise

        Examples:
            >>> repo = NAICSDBRepository()
            >>> code = repo.find_by_code("541511")
            >>> code.title
            'Custom Computer Programming Services'
        """
        normalized = normalize_naics_code(code)
        if not normalized:
            return None

        with get_db_context() as db:
            db_code = db.query(NAICSCodeDB).filter_by(code=normalized).first()

            if not db_code:
                return None

            return self._db_to_domain(db_code)

    def find_by_category(self, category: NAICSCategory) -> List[NAICSCode]:
        """
        Find all NAICS codes in a specific category.

        Args:
            category: NAICSCategory to filter by

        Returns:
            List of NAICSCode objects in the category

        Examples:
            >>> repo = NAICSDBRepository()
            >>> tech_codes = repo.find_by_category(NAICSCategory.TECHNOLOGY)
            >>> len(tech_codes) > 0
            True
        """
        with get_db_context() as db:
            db_codes = db.query(NAICSCodeDB).filter_by(category=category).all()
            return [self._db_to_domain(db_code) for db_code in db_codes]

    def find_by_level(self, level: NAICSLevel) -> List[NAICSCode]:
        """
        Find all NAICS codes at a specific hierarchical level.

        Args:
            level: NAICSLevel to filter by (SECTOR, SUBSECTOR, etc.)

        Returns:
            List of NAICSCode objects at the specified level

        Examples:
            >>> repo = NAICSDBRepository()
            >>> sectors = repo.find_by_level(NAICSLevel.SECTOR)
            >>> all(len(code.code) == 2 for code in sectors)
            True
        """
        with get_db_context() as db:
            db_codes = db.query(NAICSCodeDB).filter_by(level=level.value).all()
            return [self._db_to_domain(db_code) for db_code in db_codes]

    def search_by_title(self, query: str, limit: int = 20) -> List[NAICSCode]:
        """
        Search NAICS codes by title keywords.

        Args:
            query: Search query string
            limit: Maximum number of results to return

        Returns:
            List of matching NAICSCode objects

        Examples:
            >>> repo = NAICSDBRepository()
            >>> results = repo.search_by_title("computer")
            >>> any("computer" in code.title.lower() for code in results)
            True
        """
        if not query:
            return []

        query_lower = query.lower()

        with get_db_context() as db:
            # Use ILIKE for case-insensitive search
            db_codes = (
                db.query(NAICSCodeDB)
                .filter(NAICSCodeDB.title.ilike(f"%{query_lower}%"))
                .limit(limit)
                .all()
            )

            return [self._db_to_domain(db_code) for db_code in db_codes]

    def get_children(self, parent_code: str) -> List[NAICSCode]:
        """
        Get all child codes of a parent NAICS code.

        Args:
            parent_code: Parent NAICS code

        Returns:
            List of child NAICSCode objects

        Examples:
            >>> repo = NAICSDBRepository()
            >>> parent = repo.find_by_code("54")
            >>> children = repo.get_children("54")
            >>> all(child.code.startswith("54") for child in children)
            True
        """
        normalized = normalize_naics_code(parent_code)
        if not normalized:
            return []

        with get_db_context() as db:
            # Find all codes that start with parent_code and are longer
            db_codes = (
                db.query(NAICSCodeDB)
                .filter(
                    NAICSCodeDB.code.like(f"{normalized}%"),
                    func.length(NAICSCodeDB.code) > len(normalized)
                )
                .all()
            )

            return [self._db_to_domain(db_code) for db_code in db_codes]

    def get_parent(self, code: str) -> Optional[NAICSCode]:
        """
        Get the parent NAICS code of a given code.

        Args:
            code: NAICS code to find parent for

        Returns:
            Parent NAICSCode if found, None otherwise

        Examples:
            >>> repo = NAICSDBRepository()
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
            >>> repo = NAICSDBRepository()
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
            >>> repo = NAICSDBRepository()
            >>> repo.is_valid_code("541511")
            True

            >>> repo.is_valid_code("999999")
            False
        """
        normalized = normalize_naics_code(code)
        if not normalized:
            return False

        with get_db_context() as db:
            exists = db.query(NAICSCodeDB).filter_by(code=normalized).first() is not None
            return exists

    def get_all_codes(self, active_only: bool = True) -> List[NAICSCode]:
        """
        Get all NAICS codes in the repository.

        Args:
            active_only: If True, return only active codes

        Returns:
            List of all NAICSCode objects

        Examples:
            >>> repo = NAICSDBRepository()
            >>> all_codes = repo.get_all_codes()
            >>> len(all_codes) > 0
            True
        """
        with get_db_context() as db:
            query = db.query(NAICSCodeDB)

            if active_only:
                query = query.filter_by(is_active=True)

            db_codes = query.all()
            return [self._db_to_domain(db_code) for db_code in db_codes]

    def count(self) -> int:
        """
        Get the total count of NAICS codes in the repository.

        Returns:
            Number of NAICS codes

        Examples:
            >>> repo = NAICSDBRepository()
            >>> repo.count() > 0
            True
        """
        with get_db_context() as db:
            return db.query(NAICSCodeDB).count()

    def get_categories_summary(self) -> Dict[str, int]:
        """
        Get a summary of NAICS codes by category.

        Returns:
            Dictionary mapping category names to code counts

        Examples:
            >>> repo = NAICSDBRepository()
            >>> summary = repo.get_categories_summary()
            >>> 'technology' in summary
            True
        """
        with get_db_context() as db:
            # Group by category and count
            results = (
                db.query(
                    NAICSCodeDB.category,
                    func.count(NAICSCodeDB.code)
                )
                .group_by(NAICSCodeDB.category)
                .all()
            )

            return {
                category.value: count
                for category, count in results
            }

    def get_levels_summary(self) -> Dict[int, int]:
        """
        Get a summary of NAICS codes by hierarchy level.

        Returns:
            Dictionary mapping level values to code counts

        Examples:
            >>> repo = NAICSDBRepository()
            >>> summary = repo.get_levels_summary()
            >>> 2 in summary  # Sector level
            True
        """
        with get_db_context() as db:
            # Group by level and count
            results = (
                db.query(
                    NAICSCodeDB.level,
                    func.count(NAICSCodeDB.code)
                )
                .group_by(NAICSCodeDB.level)
                .all()
            )

            return {level: count for level, count in results}

    def bulk_insert(self, naics_codes: List[NAICSCode]) -> int:
        """
        Bulk insert NAICS codes into database.

        Args:
            naics_codes: List of NAICSCode domain objects

        Returns:
            Number of codes inserted

        Examples:
            >>> repo = NAICSDBRepository()
            >>> codes = [create_naics_code("999999", "Test Code", category=NAICSCategory.GENERAL)]
            >>> count = repo.bulk_insert(codes)
            >>> count
            1
        """
        if not naics_codes:
            return 0

        with get_db_context() as db:
            inserted = 0

            for naics_code in naics_codes:
                # Check if exists
                existing = db.query(NAICSCodeDB).filter_by(code=naics_code.code).first()

                if not existing:
                    db_code = NAICSCodeDB(
                        code=naics_code.code,
                        title=naics_code.title,
                        description=naics_code.description,
                        level=naics_code.level.value,
                        category=naics_code.category,
                        parent_code=naics_code.parent_code,
                        is_active=naics_code.is_active,
                        year=naics_code.year,
                    )
                    db.add(db_code)
                    inserted += 1

            db.commit()
            return inserted

    def update_code(self, code: str, updates: Dict) -> Optional[NAICSCode]:
        """
        Update a NAICS code with admin-specific fields.

        Only updates admin fields: tags, custom_category, admin_notes.
        Official NAICS fields (title, description, category, etc.) are not updated.

        Args:
            code: NAICS code to update
            updates: Dictionary of fields to update

        Returns:
            Updated NAICSCode if found, None otherwise

        Examples:
            >>> repo = NAICSDBRepository()
            >>> updated = repo.update_code("541511", {
            ...     "tags": ["programming", "software"],
            ...     "custom_category": "Tech Services",
            ...     "admin_notes": "High demand industry"
            ... })
            >>> updated.tags
            ['programming', 'software']
        """
        normalized = normalize_naics_code(code)
        if not normalized:
            return None

        with get_db_context() as db:
            db_code = db.query(NAICSCodeDB).filter_by(code=normalized).first()

            if not db_code:
                return None

            # Only update admin-specific fields
            if "tags" in updates:
                db_code.tags = updates["tags"] if isinstance(updates["tags"], list) else []

            if "custom_category" in updates:
                db_code.custom_category = updates["custom_category"]

            if "admin_notes" in updates:
                db_code.admin_notes = updates["admin_notes"]

            # Update timestamp
            from datetime import datetime
            db_code.updated_at = datetime.utcnow()

            db.commit()
            db.refresh(db_code)

            return self._db_to_domain(db_code)

    def delete_code(self, code: str) -> bool:
        """
        Delete a NAICS code from the database.

        WARNING: This permanently removes the NAICS code. Use with caution.

        Args:
            code: NAICS code to delete

        Returns:
            True if deleted, False if not found

        Examples:
            >>> repo = NAICSDBRepository()
            >>> repo.delete_code("999999")
            True
        """
        normalized = normalize_naics_code(code)
        if not normalized:
            return False

        with get_db_context() as db:
            db_code = db.query(NAICSCodeDB).filter_by(code=normalized).first()

            if not db_code:
                return False

            db.delete(db_code)
            db.commit()
            return True

    def search_with_pagination(
        self,
        query: str = "",
        category: Optional[NAICSCategory] = None,
        level: Optional[NAICSLevel] = None,
        page: int = 1,
        page_size: int = 50
    ) -> Dict:
        """
        Search NAICS codes with pagination support.

        Args:
            query: Search query for title/description/code
            category: Optional category filter
            level: Optional level filter
            page: Page number (1-indexed)
            page_size: Number of results per page

        Returns:
            Dictionary with: items, total, page, page_size, total_pages

        Examples:
            >>> repo = NAICSDBRepository()
            >>> results = repo.search_with_pagination("computer", page=1, page_size=10)
            >>> results["total"] >= 0
            True
            >>> len(results["items"]) <= 10
            True
        """
        with get_db_context() as db:
            # Build query
            db_query = db.query(NAICSCodeDB)

            # Apply filters
            if query:
                query_lower = query.lower()
                db_query = db_query.filter(
                    (NAICSCodeDB.title.ilike(f"%{query_lower}%")) |
                    (NAICSCodeDB.description.ilike(f"%{query_lower}%")) |
                    (NAICSCodeDB.code.ilike(f"%{query_lower}%"))
                )

            if category:
                db_query = db_query.filter_by(category=category)

            if level:
                db_query = db_query.filter_by(level=level.value)

            # Get total count
            total = db_query.count()

            # Calculate pagination
            offset = (page - 1) * page_size
            total_pages = (total + page_size - 1) // page_size  # Ceiling division

            # Get paginated results
            db_codes = db_query.order_by(NAICSCodeDB.code).offset(offset).limit(page_size).all()

            return {
                "items": [self._db_to_domain(db_code) for db_code in db_codes],
                "total": total,
                "page": page,
                "page_size": page_size,
                "total_pages": total_pages
            }
