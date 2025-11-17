"""
Experience Repository

This module implements the Repository pattern for Experience data access.
The repository abstracts data storage operations and provides a clean
interface for CRUD operations on Experience entities and their subtypes.

According to MANIFEST.md:
- Repository Pattern: Separates data access from business logic
- Supports all 9 experience types (Certificate, Degree, Course, Gig, PartTime,
  FullTime, SoftSkill, HardSkill, NativeSkill)
- NAICS code filtering and search capabilities
- Type Safety: All methods use type hints

Architecture:
    Controllers/API → Services → Repositories → Data Store

The repository layer handles:
- Data persistence for all experience types
- Query construction with filtering capabilities
- NAICS-based categorization and search
- User-experience relationship management
"""

from typing import Optional, List, Dict
from datetime import datetime
from backend.models.experience import (
    Experience,
    ExperienceCategory,
    ExperienceType,
)


class ExperienceRepository:
    """
    Repository for Experience entity data access operations.

    This class provides an abstraction layer for all Experience types
    and their variants (Education, Workplace, Skills). Implements in-memory
    storage with indexing for efficient queries.

    Design Pattern: Repository Pattern
    - Centralizes data access logic for all experience types
    - Provides consistent interface for CRUD operations
    - Supports filtering by category, type, NAICS code, and user
    - Enables easy testing with mock repositories

    Attributes:
        _experiences: In-memory storage dictionary mapping experience IDs to Experience objects
        _user_index: Index mapping user IDs to lists of experience IDs
        _naics_index: Index mapping NAICS codes to lists of experience IDs
        _category_index: Index mapping categories to lists of experience IDs
        _type_index: Index mapping types to lists of experience IDs

    Examples:
        >>> repo = ExperienceRepository()
        >>> exp = Certificate(id="123", user_id="user1", title="AWS Cert", ...)
        >>> repo.save(exp)
        >>> found = repo.find_by_id("123")
        >>> print(found.title)
        'AWS Cert'

    Note:
        In production, this will be replaced with database implementations.
    """

    def __init__(self):
        """
        Initialize the ExperienceRepository with in-memory storage.

        Sets up primary storage and multiple indexes for efficient queries.

        Example:
            # Current (in-memory)
            repo = ExperienceRepository()

            # Future (database)
            repo = ExperienceRepository(db_session=session)
        """
        self._experiences: Dict[str, Experience] = {}
        self._user_index: Dict[str, List[str]] = {}  # user_id -> [experience_ids]
        self._naics_index: Dict[str, List[str]] = {}  # naics_code -> [experience_ids]
        self._category_index: Dict[
            str, List[str]
        ] = {}  # category -> [experience_ids]
        self._type_index: Dict[str, List[str]] = {}  # type -> [experience_ids]

    def save(self, experience: Experience) -> Experience:
        """
        Save or update an experience in the repository.

        This method handles both creation and updates, maintaining all
        indexes for efficient querying.

        Args:
            experience: Experience object to save (any subtype)

        Returns:
            Experience: The saved experience object

        Examples:
            >>> repo = ExperienceRepository()
            >>> cert = Certificate(
            ...     id="123",
            ...     user_id="user1",
            ...     title="AWS Certified Developer",
            ...     naics_code="541511",
            ...     ...
            ... )
            >>> saved = repo.save(cert)
            >>> print(saved.experience_type)
            ExperienceType.CERTIFICATE
        """
        # Update timestamp
        experience.updated_at = datetime.now()

        # Save experience
        self._experiences[experience.id] = experience

        # Update user index
        if experience.user_id not in self._user_index:
            self._user_index[experience.user_id] = []
        if experience.id not in self._user_index[experience.user_id]:
            self._user_index[experience.user_id].append(experience.id)

        # Update NAICS index
        naics_code = experience.naics_code
        if naics_code not in self._naics_index:
            self._naics_index[naics_code] = []
        if experience.id not in self._naics_index[naics_code]:
            self._naics_index[naics_code].append(experience.id)

        # Update category index
        category = experience.category.value
        if category not in self._category_index:
            self._category_index[category] = []
        if experience.id not in self._category_index[category]:
            self._category_index[category].append(experience.id)

        # Update type index
        exp_type = experience.experience_type.value
        if exp_type not in self._type_index:
            self._type_index[exp_type] = []
        if experience.id not in self._type_index[exp_type]:
            self._type_index[exp_type].append(experience.id)

        return experience

    def find_by_id(self, experience_id: str) -> Optional[Experience]:
        """
        Find an experience by its unique ID.

        Args:
            experience_id: Unique identifier for the experience

        Returns:
            Optional[Experience]: Experience object if found, None otherwise

        Examples:
            >>> repo = ExperienceRepository()
            >>> exp = repo.find_by_id("123")
            >>> if exp:
            ...     print(f"Found: {exp.title}")
        """
        return self._experiences.get(experience_id)

    def find_by_user(
        self, user_id: str, limit: Optional[int] = None, offset: Optional[int] = 0
    ) -> List[Experience]:
        """
        Find all experiences for a specific user.

        Args:
            user_id: ID of the user
            limit: Maximum number of experiences to return (None = all)
            offset: Number of experiences to skip (for pagination)

        Returns:
            List[Experience]: List of experiences for the user

        Examples:
            >>> repo = ExperienceRepository()
            >>> user_experiences = repo.find_by_user("user1")
            >>> print(f"User has {len(user_experiences)} experiences")

            # Pagination (10 per page, page 2)
            >>> page_2 = repo.find_by_user("user1", limit=10, offset=10)
        """
        experience_ids = self._user_index.get(user_id, [])
        experiences = [self._experiences[exp_id] for exp_id in experience_ids]

        # Apply pagination
        if offset:
            experiences = experiences[offset:]
        if limit:
            experiences = experiences[:limit]

        return experiences

    def find_by_naics_code(self, naics_code: str) -> List[Experience]:
        """
        Find all experiences with a specific NAICS code.

        Args:
            naics_code: NAICS code to filter by (e.g., "541511" for software)

        Returns:
            List[Experience]: List of experiences with this NAICS code

        Examples:
            >>> repo = ExperienceRepository()
            >>> software_experiences = repo.find_by_naics_code("541511")
            >>> print(f"Found {len(software_experiences)} software experiences")
        """
        experience_ids = self._naics_index.get(naics_code, [])
        return [self._experiences[exp_id] for exp_id in experience_ids]

    def find_by_category(
        self,
        category: ExperienceCategory,
        limit: Optional[int] = None,
        offset: Optional[int] = 0,
    ) -> List[Experience]:
        """
        Find all experiences in a specific category.

        Args:
            category: ExperienceCategory (EDUCATION, WORKPLACE, or SKILLS)
            limit: Maximum number of experiences to return
            offset: Number of experiences to skip

        Returns:
            List[Experience]: List of experiences in the category

        Examples:
            >>> repo = ExperienceRepository()
            >>> education = repo.find_by_category(ExperienceCategory.EDUCATION)
            >>> print(f"Found {len(education)} education experiences")
        """
        experience_ids = self._category_index.get(category.value, [])
        experiences = [self._experiences[exp_id] for exp_id in experience_ids]

        # Apply pagination
        if offset:
            experiences = experiences[offset:]
        if limit:
            experiences = experiences[:limit]

        return experiences

    def find_by_type(
        self,
        experience_type: ExperienceType,
        limit: Optional[int] = None,
        offset: Optional[int] = 0,
    ) -> List[Experience]:
        """
        Find all experiences of a specific type.

        Args:
            experience_type: ExperienceType (e.g., CERTIFICATE, FULL_TIME, etc.)
            limit: Maximum number of experiences to return
            offset: Number of experiences to skip

        Returns:
            List[Experience]: List of experiences of this type

        Examples:
            >>> repo = ExperienceRepository()
            >>> certificates = repo.find_by_type(ExperienceType.CERTIFICATE)
            >>> print(f"Found {len(certificates)} certificates")
        """
        experience_ids = self._type_index.get(experience_type.value, [])
        experiences = [self._experiences[exp_id] for exp_id in experience_ids]

        # Apply pagination
        if offset:
            experiences = experiences[offset:]
        if limit:
            experiences = experiences[:limit]

        return experiences

    def find_by_user_and_category(
        self, user_id: str, category: ExperienceCategory
    ) -> List[Experience]:
        """
        Find all experiences for a user in a specific category.

        Args:
            user_id: ID of the user
            category: ExperienceCategory to filter by

        Returns:
            List[Experience]: List of matching experiences

        Examples:
            >>> repo = ExperienceRepository()
            >>> user_education = repo.find_by_user_and_category(
            ...     "user1",
            ...     ExperienceCategory.EDUCATION
            ... )
            >>> print(f"User has {len(user_education)} education experiences")
        """
        user_experiences = self.find_by_user(user_id)
        return [exp for exp in user_experiences if exp.category == category]

    def find_by_user_and_type(
        self, user_id: str, experience_type: ExperienceType
    ) -> List[Experience]:
        """
        Find all experiences for a user of a specific type.

        Args:
            user_id: ID of the user
            experience_type: ExperienceType to filter by

        Returns:
            List[Experience]: List of matching experiences

        Examples:
            >>> repo = ExperienceRepository()
            >>> user_certs = repo.find_by_user_and_type(
            ...     "user1",
            ...     ExperienceType.CERTIFICATE
            ... )
        """
        user_experiences = self.find_by_user(user_id)
        return [exp for exp in user_experiences if exp.experience_type == experience_type]

    def find_active(self, user_id: Optional[str] = None) -> List[Experience]:
        """
        Find all active (ongoing) experiences.

        Args:
            user_id: Optional user ID to filter by specific user

        Returns:
            List[Experience]: List of active experiences

        Examples:
            >>> repo = ExperienceRepository()
            >>> active = repo.find_active()
            >>> print(f"Found {len(active)} active experiences")

            >>> user_active = repo.find_active(user_id="user1")
        """
        if user_id:
            experiences = self.find_by_user(user_id)
        else:
            experiences = list(self._experiences.values())

        return [exp for exp in experiences if exp.is_active()]

    def find_all(
        self, limit: Optional[int] = None, offset: Optional[int] = 0
    ) -> List[Experience]:
        """
        Find all experiences with optional pagination.

        Args:
            limit: Maximum number of experiences to return (None = all)
            offset: Number of experiences to skip

        Returns:
            List[Experience]: List of all experiences

        Examples:
            >>> repo = ExperienceRepository()
            >>> all_exp = repo.find_all()
            >>> print(f"Total experiences: {len(all_exp)}")
        """
        experiences = list(self._experiences.values())

        # Apply pagination
        if offset:
            experiences = experiences[offset:]
        if limit:
            experiences = experiences[:limit]

        return experiences

    def delete(self, experience_id: str) -> bool:
        """
        Delete an experience from the repository.

        Removes the experience and cleans up all indexes.

        Args:
            experience_id: ID of the experience to delete

        Returns:
            bool: True if experience was deleted, False if not found

        Examples:
            >>> repo = ExperienceRepository()
            >>> success = repo.delete("123")
            >>> if success:
            ...     print("Experience deleted successfully")
        """
        experience = self._experiences.get(experience_id)
        if not experience:
            return False

        # Remove from user index
        user_experiences = self._user_index.get(experience.user_id, [])
        if experience_id in user_experiences:
            user_experiences.remove(experience_id)

        # Remove from NAICS index
        naics_experiences = self._naics_index.get(experience.naics_code, [])
        if experience_id in naics_experiences:
            naics_experiences.remove(experience_id)

        # Remove from category index
        category_experiences = self._category_index.get(experience.category.value, [])
        if experience_id in category_experiences:
            category_experiences.remove(experience_id)

        # Remove from type index
        type_experiences = self._type_index.get(experience.experience_type.value, [])
        if experience_id in type_experiences:
            type_experiences.remove(experience_id)

        # Remove experience
        del self._experiences[experience_id]
        return True

    def count(self, user_id: Optional[str] = None) -> int:
        """
        Get the count of experiences.

        Args:
            user_id: Optional user ID to count only their experiences

        Returns:
            int: Total number of experiences

        Examples:
            >>> repo = ExperienceRepository()
            >>> total = repo.count()
            >>> user_total = repo.count(user_id="user1")
        """
        if user_id:
            return len(self._user_index.get(user_id, []))
        return len(self._experiences)

    def count_by_category(self, category: ExperienceCategory) -> int:
        """
        Get the count of experiences in a specific category.

        Args:
            category: ExperienceCategory to count

        Returns:
            int: Number of experiences in the category

        Examples:
            >>> repo = ExperienceRepository()
            >>> edu_count = repo.count_by_category(ExperienceCategory.EDUCATION)
        """
        return len(self._category_index.get(category.value, []))

    def count_by_type(self, experience_type: ExperienceType) -> int:
        """
        Get the count of experiences of a specific type.

        Args:
            experience_type: ExperienceType to count

        Returns:
            int: Number of experiences of this type

        Examples:
            >>> repo = ExperienceRepository()
            >>> cert_count = repo.count_by_type(ExperienceType.CERTIFICATE)
        """
        return len(self._type_index.get(experience_type.value, []))

    def search_by_title(self, query: str, user_id: Optional[str] = None) -> List[Experience]:
        """
        Search for experiences by title (case-insensitive substring match).

        Args:
            query: Search query string
            user_id: Optional user ID to search only their experiences

        Returns:
            List[Experience]: List of matching experiences

        Examples:
            >>> repo = ExperienceRepository()
            >>> results = repo.search_by_title("software")
            >>> for exp in results:
            ...     print(exp.title)
        """
        if user_id:
            experiences = self.find_by_user(user_id)
        else:
            experiences = list(self._experiences.values())

        query_lower = query.lower()
        return [exp for exp in experiences if query_lower in exp.title.lower()]

    def search_by_skill(self, skill: str, user_id: Optional[str] = None) -> List[Experience]:
        """
        Search for experiences that include a specific skill.

        Args:
            skill: Skill to search for
            user_id: Optional user ID to search only their experiences

        Returns:
            List[Experience]: List of experiences with this skill

        Examples:
            >>> repo = ExperienceRepository()
            >>> python_exp = repo.search_by_skill("Python")
        """
        if user_id:
            experiences = self.find_by_user(user_id)
        else:
            experiences = list(self._experiences.values())

        skill_lower = skill.lower()
        return [
            exp
            for exp in experiences
            if any(skill_lower in s.lower() for s in exp.skills_gained)
        ]

    def clear(self):
        """
        Clear all experiences from the repository.

        WARNING: This is destructive and should only be used for testing.

        Examples:
            >>> repo = ExperienceRepository()
            >>> repo.clear()
            >>> print(repo.count())
            0
        """
        self._experiences.clear()
        self._user_index.clear()
        self._naics_index.clear()
        self._category_index.clear()
        self._type_index.clear()
