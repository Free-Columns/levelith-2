"""
Experience Service

This module implements the Service layer for Experience business logic.
The service layer handles business logic, validation, and orchestration
for all Experience types and their variants.

According to MANIFEST.md:
- Service Layer: Contains business logic and orchestration
- Supports all 9 experience types across 3 categories
- NAICS code validation and management
- Integration with User service for relationship management

Architecture:
    Controllers/API → Services → Repositories → Data Store

The service layer handles:
- Experience creation and validation
- NAICS code validation and fallback logic
- Category and type management
- User-experience relationship management
- Experience querying and filtering
- Business rule enforcement
"""

from typing import Optional, List, Dict
from datetime import datetime
import secrets
from backend.models.experience import (
    Experience,
    ExperienceCategory,
    ExperienceType,
    validate_naics_code,
    # Education types
    Certificate,
    Degree,
    Course,
    # Workplace types
    Gig,
    PartTime,
    FullTime,
    # Skills types
    SoftSkill,
    HardSkill,
    NativeSkill,
)
from backend.repositories.experience_repository import ExperienceRepository


class ExperienceService:
    """
    Service for Experience business logic and operations.

    This class encapsulates all business logic related to experience management,
    supporting all 9 experience types across 3 categories as defined in MANIFEST.md.

    Design Pattern: Service Layer Pattern
    - Encapsulates business logic for all experience types
    - Validates NAICS codes with fallback logic
    - Orchestrates experience-user relationships
    - Provides clean API for controllers

    Attributes:
        experience_repo: ExperienceRepository instance for data access

    Examples:
        >>> from backend.repositories import ExperienceRepository
        >>> repo = ExperienceRepository()
        >>> service = ExperienceService(experience_repo=repo)
        >>> exp = service.create_certificate(
        ...     user_id="user123",
        ...     title="AWS Certified Developer",
        ...     naics_code="541511",
        ...     start_date=datetime.now()
        ... )
        >>> print(exp.experience_type)
        ExperienceType.CERTIFICATE

    Note:
        This service implements business rules defined in MANIFEST.md:
        - Every experience MUST have a NAICS code
        - NAICS fallback code is 123456 for GENERAL
        - 9 experience types: Certificate, Degree, Course, Gig, PartTime,
          FullTime, SoftSkill, HardSkill, NativeSkill
    """

    def __init__(self, experience_repo: ExperienceRepository):
        """
        Initialize ExperienceService with required dependencies.

        Args:
            experience_repo: ExperienceRepository instance for data access

        Example:
            >>> repo = ExperienceRepository()
            >>> service = ExperienceService(experience_repo=repo)
        """
        self.experience_repo = experience_repo

    def _generate_experience_id(self) -> str:
        """
        Generate a unique experience ID.

        Returns:
            str: Unique identifier for an experience

        Note:
            In production, this should use UUIDs or database-generated IDs.
        """
        return f"exp_{secrets.token_hex(12)}"  # 24 character hex string

    def _create_experience(
        self,
        experience_class,
        user_id: str,
        title: str,
        description: str,
        naics_code: str,
        start_date: datetime,
        end_date: Optional[datetime] = None,
        organization: Optional[str] = None,
        location: Optional[str] = None,
        skills_gained: Optional[List[str]] = None,
        achievements: Optional[List[str]] = None,
        metadata: Optional[Dict] = None,
    ) -> Experience:
        """
        Internal method to create any experience type.

        This is a factory method used by all specific experience creation methods.

        Args:
            experience_class: Class to instantiate (Certificate, Degree, etc.)
            user_id: ID of the user who owns this experience
            title: Title of the experience
            description: Detailed description
            naics_code: NAICS code (will be validated)
            start_date: When the experience started
            end_date: When it ended (None if ongoing)
            organization: Associated organization
            location: Geographic location
            skills_gained: List of skills acquired
            achievements: List of achievements
            metadata: Additional metadata

        Returns:
            Experience: Created experience object

        Note:
            NAICS code is validated and falls back to 123456 if invalid.
        """
        experience_id = self._generate_experience_id()

        # Validate NAICS code (will fallback to 123456 if invalid)
        validated_naics = validate_naics_code(naics_code)

        experience = experience_class(
            id=experience_id,
            user_id=user_id,
            title=title,
            description=description,
            naics_code=validated_naics,
            start_date=start_date,
            end_date=end_date,
            organization=organization,
            location=location,
            skills_gained=skills_gained or [],
            achievements=achievements or [],
            metadata=metadata or {},
        )

        return self.experience_repo.save(experience)

    # ============================================================================
    # EDUCATION EXPERIENCE CREATION
    # ============================================================================

    def create_certificate(
        self,
        user_id: str,
        title: str,
        description: str,
        naics_code: str,
        start_date: datetime,
        end_date: Optional[datetime] = None,
        organization: Optional[str] = None,
        location: Optional[str] = None,
        skills_gained: Optional[List[str]] = None,
        achievements: Optional[List[str]] = None,
        metadata: Optional[Dict] = None,
    ) -> Certificate:
        """
        Create a Certificate experience.

        Certificates represent short-term certifications, professional credentials,
        and industry-specific training.

        Args:
            user_id: ID of the user
            title: Certificate title (e.g., "AWS Certified Developer")
            description: Description of the certification
            naics_code: NAICS code (e.g., "541511" for software)
            start_date: When the certification was obtained
            end_date: Expiration date (if applicable)
            organization: Issuing organization
            location: Location (if applicable)
            skills_gained: Skills acquired
            achievements: Notable achievements
            metadata: Additional data (exam score, credential ID, etc.)

        Returns:
            Certificate: Created certificate experience

        Examples:
            >>> service = ExperienceService(experience_repo=ExperienceRepository())
            >>> cert = service.create_certificate(
            ...     user_id="user123",
            ...     title="AWS Certified Solutions Architect",
            ...     description="Cloud architecture certification",
            ...     naics_code="541511",
            ...     start_date=datetime(2024, 1, 15),
            ...     organization="Amazon Web Services",
            ...     skills_gained=["AWS", "Cloud Architecture", "DevOps"]
            ... )
        """
        return self._create_experience(
            Certificate,
            user_id=user_id,
            title=title,
            description=description,
            naics_code=naics_code,
            start_date=start_date,
            end_date=end_date,
            organization=organization,
            location=location,
            skills_gained=skills_gained,
            achievements=achievements,
            metadata=metadata,
        )

    def create_degree(
        self,
        user_id: str,
        title: str,
        description: str,
        naics_code: str,
        start_date: datetime,
        end_date: Optional[datetime] = None,
        organization: Optional[str] = None,
        location: Optional[str] = None,
        skills_gained: Optional[List[str]] = None,
        achievements: Optional[List[str]] = None,
        metadata: Optional[Dict] = None,
    ) -> Degree:
        """
        Create a Degree experience.

        Degrees represent formal academic degrees from universities and colleges.

        Args:
            user_id: ID of the user
            title: Degree title (e.g., "Bachelor of Science in Computer Science")
            description: Description of the degree program
            naics_code: NAICS code
            start_date: When the program started
            end_date: Graduation date (None if in progress)
            organization: University/college name
            location: Location of institution
            skills_gained: Skills acquired
            achievements: Academic achievements (honors, GPA, etc.)
            metadata: Additional data (major, minor, concentration, GPA)

        Returns:
            Degree: Created degree experience

        Examples:
            >>> service = ExperienceService(experience_repo=ExperienceRepository())
            >>> degree = service.create_degree(
            ...     user_id="user123",
            ...     title="Bachelor of Science in Computer Science",
            ...     description="4-year undergraduate program",
            ...     naics_code="611310",
            ...     start_date=datetime(2020, 9, 1),
            ...     end_date=datetime(2024, 5, 15),
            ...     organization="MIT",
            ...     location="Cambridge, MA"
            ... )
        """
        return self._create_experience(
            Degree,
            user_id=user_id,
            title=title,
            description=description,
            naics_code=naics_code,
            start_date=start_date,
            end_date=end_date,
            organization=organization,
            location=location,
            skills_gained=skills_gained,
            achievements=achievements,
            metadata=metadata,
        )

    def create_course(
        self,
        user_id: str,
        title: str,
        description: str,
        naics_code: str,
        start_date: datetime,
        end_date: Optional[datetime] = None,
        organization: Optional[str] = None,
        location: Optional[str] = None,
        skills_gained: Optional[List[str]] = None,
        achievements: Optional[List[str]] = None,
        metadata: Optional[Dict] = None,
    ) -> Course:
        """
        Create a Course experience.

        Courses represent individual courses, workshops, or skill-specific training.

        Args:
            user_id: ID of the user
            title: Course title (e.g., "Introduction to Machine Learning")
            description: Description of the course
            naics_code: NAICS code
            start_date: When the course started
            end_date: When it ended (None if in progress)
            organization: Provider (Coursera, Udemy, etc.)
            location: Location or "Online"
            skills_gained: Skills acquired
            achievements: Course completion, grades, etc.
            metadata: Additional data (instructor, certificate, completion rate)

        Returns:
            Course: Created course experience

        Examples:
            >>> service = ExperienceService(experience_repo=ExperienceRepository())
            >>> course = service.create_course(
            ...     user_id="user123",
            ...     title="Machine Learning Specialization",
            ...     description="Andrew Ng's ML course",
            ...     naics_code="611420",
            ...     start_date=datetime(2024, 1, 1),
            ...     organization="Coursera",
            ...     location="Online"
            ... )
        """
        return self._create_experience(
            Course,
            user_id=user_id,
            title=title,
            description=description,
            naics_code=naics_code,
            start_date=start_date,
            end_date=end_date,
            organization=organization,
            location=location,
            skills_gained=skills_gained,
            achievements=achievements,
            metadata=metadata,
        )

    # ============================================================================
    # WORKPLACE EXPERIENCE CREATION
    # ============================================================================

    def create_gig(
        self,
        user_id: str,
        title: str,
        description: str,
        naics_code: str,
        start_date: datetime,
        end_date: Optional[datetime] = None,
        organization: Optional[str] = None,
        location: Optional[str] = None,
        skills_gained: Optional[List[str]] = None,
        achievements: Optional[List[str]] = None,
        metadata: Optional[Dict] = None,
    ) -> Gig:
        """
        Create a Gig experience.

        Gigs represent short-term contract work, freelance projects, and
        one-off engagements.

        Args:
            user_id: ID of the user
            title: Gig title (e.g., "Website Redesign Project")
            description: Description of the gig
            naics_code: NAICS code
            start_date: When the gig started
            end_date: When it ended (None if ongoing)
            organization: Client/company name
            location: Location or "Remote"
            skills_gained: Skills used/gained
            achievements: Project outcomes
            metadata: Additional data (contract value, platform, etc.)

        Returns:
            Gig: Created gig experience

        Examples:
            >>> service = ExperienceService(experience_repo=ExperienceRepository())
            >>> gig = service.create_gig(
            ...     user_id="user123",
            ...     title="E-commerce Website Development",
            ...     description="Built custom Shopify store",
            ...     naics_code="541511",
            ...     start_date=datetime(2024, 3, 1),
            ...     end_date=datetime(2024, 4, 15),
            ...     organization="XYZ Retail",
            ...     location="Remote"
            ... )
        """
        return self._create_experience(
            Gig,
            user_id=user_id,
            title=title,
            description=description,
            naics_code=naics_code,
            start_date=start_date,
            end_date=end_date,
            organization=organization,
            location=location,
            skills_gained=skills_gained,
            achievements=achievements,
            metadata=metadata,
        )

    def create_part_time(
        self,
        user_id: str,
        title: str,
        description: str,
        naics_code: str,
        start_date: datetime,
        end_date: Optional[datetime] = None,
        organization: Optional[str] = None,
        location: Optional[str] = None,
        skills_gained: Optional[List[str]] = None,
        achievements: Optional[List[str]] = None,
        metadata: Optional[Dict] = None,
    ) -> PartTime:
        """
        Create a PartTime experience.

        Part-time represents regular part-time employment with flexible schedules.

        Args:
            user_id: ID of the user
            title: Job title (e.g., "Part-Time Barista")
            description: Description of responsibilities
            naics_code: NAICS code
            start_date: Employment start date
            end_date: Employment end date (None if current)
            organization: Employer name
            location: Work location
            skills_gained: Skills developed
            achievements: Work achievements
            metadata: Additional data (hours per week, schedule, etc.)

        Returns:
            PartTime: Created part-time experience

        Examples:
            >>> service = ExperienceService(experience_repo=ExperienceRepository())
            >>> pt = service.create_part_time(
            ...     user_id="user123",
            ...     title="Customer Service Representative",
            ...     description="Part-time customer support",
            ...     naics_code="561422",
            ...     start_date=datetime(2023, 6, 1),
            ...     organization="Tech Support Co",
            ...     location="Remote"
            ... )
        """
        return self._create_experience(
            PartTime,
            user_id=user_id,
            title=title,
            description=description,
            naics_code=naics_code,
            start_date=start_date,
            end_date=end_date,
            organization=organization,
            location=location,
            skills_gained=skills_gained,
            achievements=achievements,
            metadata=metadata,
        )

    def create_full_time(
        self,
        user_id: str,
        title: str,
        description: str,
        naics_code: str,
        start_date: datetime,
        end_date: Optional[datetime] = None,
        organization: Optional[str] = None,
        location: Optional[str] = None,
        skills_gained: Optional[List[str]] = None,
        achievements: Optional[List[str]] = None,
        metadata: Optional[Dict] = None,
    ) -> FullTime:
        """
        Create a FullTime experience.

        Full-time represents primary career positions and standard employment.

        Args:
            user_id: ID of the user
            title: Job title (e.g., "Senior Software Engineer")
            description: Description of role and responsibilities
            naics_code: NAICS code
            start_date: Employment start date
            end_date: Employment end date (None if current)
            organization: Employer name
            location: Work location
            skills_gained: Skills developed
            achievements: Career achievements
            metadata: Additional data (department, manager, promotions, etc.)

        Returns:
            FullTime: Created full-time experience

        Examples:
            >>> service = ExperienceService(experience_repo=ExperienceRepository())
            >>> ft = service.create_full_time(
            ...     user_id="user123",
            ...     title="Senior Software Engineer",
            ...     description="Full-stack development lead",
            ...     naics_code="541511",
            ...     start_date=datetime(2022, 1, 1),
            ...     organization="Tech Corp",
            ...     location="San Francisco, CA"
            ... )
        """
        return self._create_experience(
            FullTime,
            user_id=user_id,
            title=title,
            description=description,
            naics_code=naics_code,
            start_date=start_date,
            end_date=end_date,
            organization=organization,
            location=location,
            skills_gained=skills_gained,
            achievements=achievements,
            metadata=metadata,
        )

    # ============================================================================
    # SKILLS EXPERIENCE CREATION
    # ============================================================================

    def create_soft_skill(
        self,
        user_id: str,
        title: str,
        description: str,
        naics_code: str,
        start_date: datetime,
        end_date: Optional[datetime] = None,
        organization: Optional[str] = None,
        location: Optional[str] = None,
        skills_gained: Optional[List[str]] = None,
        achievements: Optional[List[str]] = None,
        metadata: Optional[Dict] = None,
    ) -> SoftSkill:
        """
        Create a SoftSkill experience.

        Soft skills represent interpersonal abilities, communication, and leadership.

        Args:
            user_id: ID of the user
            title: Skill title (e.g., "Public Speaking")
            description: Description of the skill and how it was developed
            naics_code: NAICS code (use 123456 if no specific industry)
            start_date: When skill development began
            end_date: When formally recognized/completed (if applicable)
            organization: Where skill was developed
            location: Location
            skills_gained: Related skills
            achievements: Demonstrations of skill (presentations given, etc.)
            metadata: Additional data (proficiency level, certifications, etc.)

        Returns:
            SoftSkill: Created soft skill experience

        Examples:
            >>> service = ExperienceService(experience_repo=ExperienceRepository())
            >>> skill = service.create_soft_skill(
            ...     user_id="user123",
            ...     title="Team Leadership",
            ...     description="Led cross-functional teams",
            ...     naics_code="123456",
            ...     start_date=datetime(2020, 1, 1)
            ... )
        """
        return self._create_experience(
            SoftSkill,
            user_id=user_id,
            title=title,
            description=description,
            naics_code=naics_code,
            start_date=start_date,
            end_date=end_date,
            organization=organization,
            location=location,
            skills_gained=skills_gained,
            achievements=achievements,
            metadata=metadata,
        )

    def create_hard_skill(
        self,
        user_id: str,
        title: str,
        description: str,
        naics_code: str,
        start_date: datetime,
        end_date: Optional[datetime] = None,
        organization: Optional[str] = None,
        location: Optional[str] = None,
        skills_gained: Optional[List[str]] = None,
        achievements: Optional[List[str]] = None,
        metadata: Optional[Dict] = None,
    ) -> HardSkill:
        """
        Create a HardSkill experience.

        Hard skills represent technical abilities and measurable competencies.

        Args:
            user_id: ID of the user
            title: Skill title (e.g., "Python Programming")
            description: Description of proficiency and applications
            naics_code: NAICS code (e.g., "541511" for software)
            start_date: When skill learning began
            end_date: When proficiency was achieved (if applicable)
            organization: Where skill was learned
            location: Location
            skills_gained: Related skills
            achievements: Projects, certifications, etc.
            metadata: Additional data (proficiency level, years of experience)

        Returns:
            HardSkill: Created hard skill experience

        Examples:
            >>> service = ExperienceService(experience_repo=ExperienceRepository())
            >>> skill = service.create_hard_skill(
            ...     user_id="user123",
            ...     title="Python Programming",
            ...     description="5 years of professional Python development",
            ...     naics_code="541511",
            ...     start_date=datetime(2019, 1, 1)
            ... )
        """
        return self._create_experience(
            HardSkill,
            user_id=user_id,
            title=title,
            description=description,
            naics_code=naics_code,
            start_date=start_date,
            end_date=end_date,
            organization=organization,
            location=location,
            skills_gained=skills_gained,
            achievements=achievements,
            metadata=metadata,
        )

    def create_native_skill(
        self,
        user_id: str,
        title: str,
        description: str,
        naics_code: str,
        start_date: datetime,
        end_date: Optional[datetime] = None,
        organization: Optional[str] = None,
        location: Optional[str] = None,
        skills_gained: Optional[List[str]] = None,
        achievements: Optional[List[str]] = None,
        metadata: Optional[Dict] = None,
    ) -> NativeSkill:
        """
        Create a NativeSkill experience.

        Native skills represent natural talents, innate abilities, and language fluencies.

        Args:
            user_id: ID of the user
            title: Skill title (e.g., "Bilingual (English/Spanish)")
            description: Description of the native skill
            naics_code: NAICS code (use 123456 if no specific industry)
            start_date: Since when (birth, childhood, etc.)
            end_date: Usually None for native skills
            organization: Where developed/recognized
            location: Location
            skills_gained: Related skills
            achievements: Demonstrations of ability
            metadata: Additional data (fluency level, certifications, etc.)

        Returns:
            NativeSkill: Created native skill experience

        Examples:
            >>> service = ExperienceService(experience_repo=ExperienceRepository())
            >>> skill = service.create_native_skill(
            ...     user_id="user123",
            ...     title="Bilingual (English/Spanish)",
            ...     description="Native fluency in both languages",
            ...     naics_code="123456",
            ...     start_date=datetime(1990, 1, 1)
            ... )
        """
        return self._create_experience(
            NativeSkill,
            user_id=user_id,
            title=title,
            description=description,
            naics_code=naics_code,
            start_date=start_date,
            end_date=end_date,
            organization=organization,
            location=location,
            skills_gained=skills_gained,
            achievements=achievements,
            metadata=metadata,
        )

    # ============================================================================
    # QUERY AND RETRIEVAL METHODS
    # ============================================================================

    def get_experience_by_id(self, experience_id: str) -> Optional[Experience]:
        """
        Retrieve an experience by its ID.

        Args:
            experience_id: Unique identifier for the experience

        Returns:
            Optional[Experience]: Experience object if found, None otherwise

        Examples:
            >>> service = ExperienceService(experience_repo=ExperienceRepository())
            >>> exp = service.get_experience_by_id("exp123")
        """
        return self.experience_repo.find_by_id(experience_id)

    def get_user_experiences(
        self,
        user_id: str,
        category: Optional[ExperienceCategory] = None,
        experience_type: Optional[ExperienceType] = None,
        active_only: bool = False,
        limit: Optional[int] = None,
        offset: Optional[int] = 0,
    ) -> List[Experience]:
        """
        Get all experiences for a user with optional filtering.

        Args:
            user_id: ID of the user
            category: Optional category filter
            experience_type: Optional type filter
            active_only: If True, return only active experiences
            limit: Maximum number to return
            offset: Number to skip (pagination)

        Returns:
            List[Experience]: List of matching experiences

        Examples:
            >>> service = ExperienceService(experience_repo=ExperienceRepository())
            >>> all_exp = service.get_user_experiences("user123")
            >>> education = service.get_user_experiences(
            ...     "user123",
            ...     category=ExperienceCategory.EDUCATION
            ... )
            >>> active_certs = service.get_user_experiences(
            ...     "user123",
            ...     experience_type=ExperienceType.CERTIFICATE,
            ...     active_only=True
            ... )
        """
        if category:
            experiences = self.experience_repo.find_by_user_and_category(user_id, category)
        elif experience_type:
            experiences = self.experience_repo.find_by_user_and_type(user_id, experience_type)
        else:
            experiences = self.experience_repo.find_by_user(user_id, limit=limit, offset=offset)

        if active_only:
            experiences = [exp for exp in experiences if exp.is_active()]

        # Apply pagination if not already done
        if (category or experience_type) and (limit or offset):
            if offset:
                experiences = experiences[offset:]
            if limit:
                experiences = experiences[:limit]

        return experiences

    def get_experiences_by_naics(self, naics_code: str) -> List[Experience]:
        """
        Get all experiences with a specific NAICS code.

        Args:
            naics_code: NAICS code to filter by

        Returns:
            List[Experience]: List of experiences

        Examples:
            >>> service = ExperienceService(experience_repo=ExperienceRepository())
            >>> software_exp = service.get_experiences_by_naics("541511")
        """
        return self.experience_repo.find_by_naics_code(naics_code)

    def search_experiences(
        self,
        query: str,
        user_id: Optional[str] = None,
        search_skills: bool = False,
    ) -> List[Experience]:
        """
        Search experiences by title or skills.

        Args:
            query: Search query string
            user_id: Optional user ID to search only their experiences
            search_skills: If True, also search in skills_gained

        Returns:
            List[Experience]: List of matching experiences

        Examples:
            >>> service = ExperienceService(experience_repo=ExperienceRepository())
            >>> results = service.search_experiences("software", search_skills=True)
        """
        title_results = self.experience_repo.search_by_title(query, user_id)

        if search_skills:
            skill_results = self.experience_repo.search_by_skill(query, user_id)
            # Combine and deduplicate
            all_results = {exp.id: exp for exp in title_results}
            all_results.update({exp.id: exp for exp in skill_results})
            return list(all_results.values())

        return title_results

    def update_experience(
        self,
        experience_id: str,
        **updates,
    ) -> Optional[Experience]:
        """
        Update an existing experience.

        Args:
            experience_id: ID of the experience to update
            **updates: Fields to update (title, description, etc.)

        Returns:
            Optional[Experience]: Updated experience if found, None otherwise

        Raises:
            ValueError: If experience not found

        Examples:
            >>> service = ExperienceService(experience_repo=ExperienceRepository())
            >>> updated = service.update_experience(
            ...     "exp123",
            ...     title="Updated Title",
            ...     description="Updated description"
            ... )

        Note:
            Cannot update id, user_id, category, or experience_type
        """
        experience = self.experience_repo.find_by_id(experience_id)
        if not experience:
            raise ValueError(f"Experience with ID '{experience_id}' not found")

        # Update allowed fields
        allowed_fields = {
            "title",
            "description",
            "naics_code",
            "start_date",
            "end_date",
            "organization",
            "location",
            "skills_gained",
            "achievements",
            "metadata",
        }

        for key, value in updates.items():
            if key in allowed_fields:
                if key == "naics_code":
                    value = validate_naics_code(value)
                setattr(experience, key, value)

        experience.updated_at = datetime.now()
        return self.experience_repo.save(experience)

    def delete_experience(self, experience_id: str) -> bool:
        """
        Delete an experience.

        Args:
            experience_id: ID of the experience to delete

        Returns:
            bool: True if deleted, False if not found

        Examples:
            >>> service = ExperienceService(experience_repo=ExperienceRepository())
            >>> success = service.delete_experience("exp123")
        """
        return self.experience_repo.delete(experience_id)

    def get_experience_count(
        self,
        user_id: Optional[str] = None,
        category: Optional[ExperienceCategory] = None,
        experience_type: Optional[ExperienceType] = None,
    ) -> int:
        """
        Get count of experiences with optional filtering.

        Args:
            user_id: Optional user ID filter
            category: Optional category filter
            experience_type: Optional type filter

        Returns:
            int: Count of matching experiences

        Examples:
            >>> service = ExperienceService(experience_repo=ExperienceRepository())
            >>> total = service.get_experience_count()
            >>> user_total = service.get_experience_count(user_id="user123")
            >>> edu_count = service.get_experience_count(
            ...     category=ExperienceCategory.EDUCATION
            ... )
        """
        if experience_type:
            return self.experience_repo.count_by_type(experience_type)
        elif category:
            return self.experience_repo.count_by_category(category)
        else:
            return self.experience_repo.count(user_id=user_id)
