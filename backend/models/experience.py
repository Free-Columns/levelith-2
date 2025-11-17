"""
Experience Domain Models

This module defines the core Experience model and all its subtypes.
According to MANIFEST.md, there are 9 experience subtypes across 3 categories:

1. Education: Certificate, Degree, Course
2. Workplace: Gig, PartTime, FullTime
3. Skills: SoftSkill, HardSkill, NativeSkill

Every Experience MUST have a NAICS code. Fallback code: 123456 (GENERAL)
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from enum import Enum


class ExperienceCategory(Enum):
    """
    Main categories of experiences.

    Each category has 3 subtypes as defined in MANIFEST.md.
    """

    EDUCATION = "education"
    WORKPLACE = "workplace"
    SKILLS = "skills"


class ExperienceType(Enum):
    """
    Specific types of experiences.

    9 types total as defined in MANIFEST.md:
    - Education: Certificate, Degree, Course
    - Workplace: Gig, PartTime, FullTime
    - Skills: SoftSkill, HardSkill, NativeSkill
    """

    # Education types
    CERTIFICATE = "certificate"
    DEGREE = "degree"
    COURSE = "course"

    # Workplace types
    GIG = "gig"
    PART_TIME = "part_time"
    FULL_TIME = "full_time"

    # Skills types
    SOFT_SKILL = "soft_skill"
    HARD_SKILL = "hard_skill"
    NATIVE_SKILL = "native_skill"


# NAICS code constants
NAICS_GENERAL_FALLBACK = "123456"  # Fallback code for GENERAL classification
NAICS_VALID_LENGTH = 6  # NAICS codes are 6 digits


def validate_naics_code(code: str) -> str:
    """
    Validate and normalize NAICS code.

    CRITICAL REQUIREMENT: Every Experience MUST have a valid NAICS code.
    If the provided code is invalid, returns the fallback code 123456.

    Args:
        code: NAICS code to validate (should be 6 digits)

    Returns:
        str: Validated NAICS code or fallback code 123456

    Examples:
        >>> validate_naics_code("541511")  # Software development
        '541511'

        >>> validate_naics_code("invalid")  # Invalid code
        '123456'

        >>> validate_naics_code("")  # Empty code
        '123456'

        >>> validate_naics_code(None)  # None
        '123456'
    """
    if not code:
        return NAICS_GENERAL_FALLBACK

    # Remove whitespace
    code = str(code).strip()

    # Check if it's 6 digits
    if len(code) != NAICS_VALID_LENGTH or not code.isdigit():
        return NAICS_GENERAL_FALLBACK

    return code


@dataclass
class Experience:
    """
    Base Experience model.

    Every user has an array of Experience elements. This is the core data model
    representing any trackable professional/educational activity.

    CRITICAL REQUIREMENTS from MANIFEST.md:
    - Every Experience MUST include a NAICS code
    - NAICS fallback code is 123456 for GENERAL classification
    - Experiences come in 9 subtypes across 3 categories

    Attributes:
        id: Unique identifier for this experience
        user_id: ID of the user who owns this experience
        category: Main category (Education, Workplace, Skills)
        experience_type: Specific type within the category
        title: Title or name of the experience
        description: Detailed description of the experience
        naics_code: REQUIRED - North American Industry Classification System code
        start_date: When the experience started
        end_date: When the experience ended (None if ongoing)
        organization: Organization/institution associated with this experience
        location: Geographic location of the experience
        skills_gained: List of skills acquired through this experience
        achievements: Notable achievements or milestones
        metadata: Additional type-specific data
        created_at: When this experience record was created
        updated_at: When this experience record was last updated
    """

    id: str
    user_id: str
    category: ExperienceCategory
    experience_type: ExperienceType
    title: str
    description: str
    naics_code: str  # REQUIRED field
    start_date: datetime
    end_date: Optional[datetime] = None
    organization: Optional[str] = None
    location: Optional[str] = None
    skills_gained: List[str] = field(default_factory=list)
    achievements: List[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Validate NAICS code after initialization."""
        self.naics_code = validate_naics_code(self.naics_code)

    def is_active(self) -> bool:
        """
        Check if experience is currently active (ongoing).

        Returns:
            bool: True if end_date is None, False otherwise
        """
        return self.end_date is None

    def duration_days(self) -> Optional[int]:
        """
        Calculate duration of experience in days.

        Returns:
            Optional[int]: Number of days, or None if still ongoing
        """
        if self.is_active():
            # For ongoing experiences, calculate from start to now
            return (datetime.now() - self.start_date).days

        return (self.end_date - self.start_date).days

    def to_dict(self) -> dict:
        """
        Convert experience to dictionary representation.

        Returns:
            dict: Dictionary representation of the experience
        """
        return {
            "id": self.id,
            "user_id": self.user_id,
            "category": self.category.value,
            "experience_type": self.experience_type.value,
            "title": self.title,
            "description": self.description,
            "naics_code": self.naics_code,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "organization": self.organization,
            "location": self.location,
            "skills_gained": self.skills_gained,
            "achievements": self.achievements,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


# ============================================================================
# EDUCATION EXPERIENCES
# ============================================================================


@dataclass
class Certificate(Experience):
    """
    Certificate Experience Type.

    Represents short-term certifications, professional credentials, and
    industry-specific training.

    Examples:
        - AWS Certified Developer
        - Google Analytics Certification
        - PMP Certification
        - CompTIA Security+
    """

    def __init__(self, **kwargs):
        """Initialize Certificate experience."""
        kwargs["category"] = ExperienceCategory.EDUCATION
        kwargs["experience_type"] = ExperienceType.CERTIFICATE
        super().__init__(**kwargs)


@dataclass
class Degree(Experience):
    """
    Degree Experience Type.

    Represents formal academic degrees from universities and colleges.

    Examples:
        - Bachelor of Science in Computer Science
        - Master of Business Administration (MBA)
        - Doctor of Philosophy (PhD)
        - Associate degree in Nursing
    """

    def __init__(self, **kwargs):
        """Initialize Degree experience."""
        kwargs["category"] = ExperienceCategory.EDUCATION
        kwargs["experience_type"] = ExperienceType.DEGREE
        super().__init__(**kwargs)


@dataclass
class Course(Experience):
    """
    Course Experience Type.

    Represents individual courses, workshops, or skill-specific training programs.

    Examples:
        - Introduction to Machine Learning (Coursera)
        - Advanced SQL Workshop
        - Public Speaking Bootcamp
        - Web Development Fundamentals
    """

    def __init__(self, **kwargs):
        """Initialize Course experience."""
        kwargs["category"] = ExperienceCategory.EDUCATION
        kwargs["experience_type"] = ExperienceType.COURSE
        super().__init__(**kwargs)


# ============================================================================
# WORKPLACE EXPERIENCES
# ============================================================================


@dataclass
class Gig(Experience):
    """
    Gig Experience Type.

    Represents short-term contract work, freelance projects, and one-off engagements.

    Examples:
        - Website redesign project (2 months)
        - Freelance graphic design work
        - Consulting engagement
        - One-time photography session
    """

    def __init__(self, **kwargs):
        """Initialize Gig experience."""
        kwargs["category"] = ExperienceCategory.WORKPLACE
        kwargs["experience_type"] = ExperienceType.GIG
        super().__init__(**kwargs)


@dataclass
class PartTime(Experience):
    """
    PartTime Experience Type.

    Represents regular part-time employment with flexible schedules and
    secondary employment positions.

    Examples:
        - Retail associate (20 hrs/week)
        - Teaching assistant
        - Weekend barista
        - Part-time customer support
    """

    def __init__(self, **kwargs):
        """Initialize PartTime experience."""
        kwargs["category"] = ExperienceCategory.WORKPLACE
        kwargs["experience_type"] = ExperienceType.PART_TIME
        super().__init__(**kwargs)


@dataclass
class FullTime(Experience):
    """
    FullTime Experience Type.

    Represents primary career positions, standard employment, and long-term roles.

    Examples:
        - Software Engineer at Tech Corp
        - Marketing Manager at Startup
        - Senior Data Analyst
        - Product Designer
    """

    def __init__(self, **kwargs):
        """Initialize FullTime experience."""
        kwargs["category"] = ExperienceCategory.WORKPLACE
        kwargs["experience_type"] = ExperienceType.FULL_TIME
        super().__init__(**kwargs)


# ============================================================================
# SKILLS EXPERIENCES
# ============================================================================


@dataclass
class SoftSkill(Experience):
    """
    SoftSkill Experience Type.

    Represents interpersonal abilities, communication skills, and leadership qualities.

    Examples:
        - Public speaking
        - Team collaboration
        - Conflict resolution
        - Leadership
        - Emotional intelligence
    """

    def __init__(self, **kwargs):
        """Initialize SoftSkill experience."""
        kwargs["category"] = ExperienceCategory.SKILLS
        kwargs["experience_type"] = ExperienceType.SOFT_SKILL
        super().__init__(**kwargs)


@dataclass
class HardSkill(Experience):
    """
    HardSkill Experience Type.

    Represents technical abilities, measurable competencies, and
    industry-specific knowledge.

    Examples:
        - Python programming
        - Data analysis
        - Graphic design
        - SQL databases
        - Financial modeling
    """

    def __init__(self, **kwargs):
        """Initialize HardSkill experience."""
        kwargs["category"] = ExperienceCategory.SKILLS
        kwargs["experience_type"] = ExperienceType.HARD_SKILL
        super().__init__(**kwargs)


@dataclass
class NativeSkill(Experience):
    """
    NativeSkill Experience Type.

    Represents natural talents, innate abilities, cultural knowledge, and
    language fluencies.

    Examples:
        - Bilingual (English/Spanish)
        - Artistic ability
        - Musical talent
        - Cultural knowledge
        - Natural athleticism
    """

    def __init__(self, **kwargs):
        """Initialize NativeSkill experience."""
        kwargs["category"] = ExperienceCategory.SKILLS
        kwargs["experience_type"] = ExperienceType.NATIVE_SKILL
        super().__init__(**kwargs)
