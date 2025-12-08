"""
XP Calculation Service

Handles all XP calculation logic for the Levelith platform.

XP System Rules:
- 10 XP per hour of tenure
- 4 XP categories: Professional, Education, Skills, Vocational
- Exponential leveling: Level N requires 100 × N² total XP
- Total XP = sum of all category XP

Experience Type to XP Category Mapping:
- Professional XP ← FullTime, PartTime, Gig
- Education XP ← Certificate, Degree, Course
- Skills XP ← SoftSkill, HardSkill, NativeSkill
- Vocational XP ← (future: Volunteer, Projects, etc.)
"""

import math
from datetime import datetime
from typing import Dict, Tuple
from sqlalchemy.orm import Session

from backend.models.experience import ExperienceType
from backend.models.db_models import UserDB, ExperienceDB


# XP Constants
XP_PER_HOUR = 10.0
DEFAULT_FULLTIME_HOURS_PER_WEEK = 40.0
DEFAULT_PARTTIME_HOURS_PER_WEEK = 20.0


class XPCategory:
    """XP category identifiers."""
    PROFESSIONAL = "professional"
    EDUCATION = "education"
    SKILLS = "skills"
    VOCATIONAL = "vocational"


# Experience Type to XP Category Mapping
EXPERIENCE_TYPE_TO_XP_CATEGORY = {
    # Professional (Workplace)
    ExperienceType.FULL_TIME: XPCategory.PROFESSIONAL,
    ExperienceType.PART_TIME: XPCategory.PROFESSIONAL,
    ExperienceType.GIG: XPCategory.PROFESSIONAL,

    # Education
    ExperienceType.CERTIFICATE: XPCategory.EDUCATION,
    ExperienceType.DEGREE: XPCategory.EDUCATION,
    ExperienceType.COURSE: XPCategory.EDUCATION,

    # Skills
    ExperienceType.SOFT_SKILL: XPCategory.SKILLS,
    ExperienceType.HARD_SKILL: XPCategory.SKILLS,
    ExperienceType.NATIVE_SKILL: XPCategory.SKILLS,
}


def calculate_level_from_xp(total_xp: float) -> int:
    """
    Calculate level from total XP using exponential formula.

    Formula: Level N requires 100 × N² total XP
    - Level 0 = 0 XP
    - Level 1 = 100 XP
    - Level 2 = 400 XP
    - Level 3 = 900 XP
    - Level 4 = 1600 XP

    Inverse formula: Level = floor(sqrt(total_xp / 100))

    Args:
        total_xp: Total experience points

    Returns:
        int: Current level

    Examples:
        >>> calculate_level_from_xp(0)
        0
        >>> calculate_level_from_xp(100)
        1
        >>> calculate_level_from_xp(400)
        2
        >>> calculate_level_from_xp(500)
        2
        >>> calculate_level_from_xp(900)
        3
    """
    if total_xp <= 0:
        return 0

    level = math.floor(math.sqrt(total_xp / 100))
    return level


def calculate_xp_for_level(level: int) -> int:
    """
    Calculate total XP required to reach a specific level.

    Formula: XP = 100 × level²

    Args:
        level: Target level

    Returns:
        int: Total XP required

    Examples:
        >>> calculate_xp_for_level(1)
        100
        >>> calculate_xp_for_level(2)
        400
        >>> calculate_xp_for_level(3)
        900
    """
    return 100 * (level ** 2)


def calculate_experience_hours(experience: ExperienceDB) -> float:
    """
    Calculate total hours for an experience based on tenure.

    Calculation logic:
    - Uses start_date and end_date (or now if ongoing)
    - For FullTime: assume 40 hrs/week
    - For PartTime: check type_specific_data['hours_per_week'] or default 20 hrs/week
    - For Gig: check type_specific_data['total_hours'] or calculate from tenure
    - For Education: check type_specific_data['hours'] or estimate from duration
    - For Skills: check type_specific_data['practice_hours'] or 0

    Args:
        experience: Experience database model

    Returns:
        float: Total hours for this experience
    """
    if not experience.start_date:
        return 0.0

    # Determine end date (use current time if ongoing)
    end_date = experience.end_date if experience.end_date else datetime.utcnow()

    # Calculate tenure in days
    tenure_days = (end_date - experience.start_date).days
    if tenure_days < 0:
        tenure_days = 0

    # Convert days to weeks for easier calculation
    tenure_weeks = tenure_days / 7.0

    experience_type = experience.experience_type
    type_specific_data = experience.type_specific_data or {}

    # Calculate hours based on experience type
    if experience_type == ExperienceType.FULL_TIME:
        # FullTime: 40 hours/week standard
        hours_per_week = type_specific_data.get('hours_per_week', DEFAULT_FULLTIME_HOURS_PER_WEEK)
        return tenure_weeks * hours_per_week

    elif experience_type == ExperienceType.PART_TIME:
        # PartTime: check type_specific_data or default 20 hrs/week
        hours_per_week = type_specific_data.get('hours_per_week', DEFAULT_PARTTIME_HOURS_PER_WEEK)
        return tenure_weeks * hours_per_week

    elif experience_type == ExperienceType.GIG:
        # Gig: prefer explicit total_hours, else calculate from tenure
        if 'total_hours' in type_specific_data:
            return float(type_specific_data['total_hours'])
        # Default: assume 40 hrs/week for gig duration
        return tenure_weeks * 40.0

    elif experience_type in [ExperienceType.CERTIFICATE, ExperienceType.DEGREE, ExperienceType.COURSE]:
        # Education: check for explicit hours
        if 'hours' in type_specific_data:
            return float(type_specific_data['hours'])
        if 'credit_hours' in type_specific_data:
            # Convert credit hours to actual hours (1 credit ≈ 3 actual hours)
            return float(type_specific_data['credit_hours']) * 3.0
        # Default: estimate 10 hrs/week for education duration
        return tenure_weeks * 10.0

    elif experience_type in [ExperienceType.SOFT_SKILL, ExperienceType.HARD_SKILL, ExperienceType.NATIVE_SKILL]:
        # Skills: check practice_hours
        if 'practice_hours' in type_specific_data:
            return float(type_specific_data['practice_hours'])
        # Default: estimate from tenure (5 hrs/week practice)
        return tenure_weeks * 5.0

    # Fallback: estimate from tenure (10 hrs/week)
    return tenure_weeks * 10.0


def calculate_experience_xp(experience: ExperienceDB) -> Tuple[str, float]:
    """
    Calculate XP for a single experience.

    Returns both the XP category and the XP amount.

    Args:
        experience: Experience database model

    Returns:
        Tuple[str, float]: (xp_category, xp_amount)

    Examples:
        >>> exp = ExperienceDB(experience_type=ExperienceType.FULL_TIME, ...)
        >>> category, xp = calculate_experience_xp(exp)
        >>> category
        'professional'
    """
    # Calculate hours
    hours = calculate_experience_hours(experience)

    # Calculate XP (10 XP per hour)
    xp = hours * XP_PER_HOUR

    # Determine XP category
    xp_category = EXPERIENCE_TYPE_TO_XP_CATEGORY.get(
        experience.experience_type,
        XPCategory.VOCATIONAL  # Default for unknown types
    )

    return xp_category, xp


def recalculate_user_xp(user: UserDB, db: Session) -> Dict[str, float]:
    """
    Recalculate all XP for a user based on their experiences.

    This function:
    1. Fetches all user experiences
    2. Calculates XP for each experience
    3. Sums XP by category
    4. Calculates total XP and level
    5. Updates user XP fields in database

    Args:
        user: User database model
        db: Database session

    Returns:
        Dict containing all XP values:
        {
            'professional_xp': float,
            'education_xp': float,
            'skills_xp': float,
            'vocational_xp': float,
            'total_xp': float,
            'level': int
        }
    """
    # Initialize XP counters
    xp_totals = {
        XPCategory.PROFESSIONAL: 0.0,
        XPCategory.EDUCATION: 0.0,
        XPCategory.SKILLS: 0.0,
        XPCategory.VOCATIONAL: 0.0,
    }

    # Calculate XP for each experience
    for experience in user.experiences:
        category, xp = calculate_experience_xp(experience)
        xp_totals[category] += xp

    # Calculate total XP
    total_xp = sum(xp_totals.values())

    # Calculate level
    level = calculate_level_from_xp(total_xp)

    # Update user fields
    user.professional_xp = xp_totals[XPCategory.PROFESSIONAL]
    user.education_xp = xp_totals[XPCategory.EDUCATION]
    user.skills_xp = xp_totals[XPCategory.SKILLS]
    user.vocational_xp = xp_totals[XPCategory.VOCATIONAL]
    user.total_xp = total_xp
    user.level = level

    # Commit changes
    db.commit()
    db.refresh(user)

    return {
        'professional_xp': user.professional_xp,
        'education_xp': user.education_xp,
        'skills_xp': user.skills_xp,
        'vocational_xp': user.vocational_xp,
        'total_xp': user.total_xp,
        'level': user.level,
    }


class XPService:
    """Service class for XP-related operations."""

    def __init__(self, db: Session):
        """
        Initialize XP service.

        Args:
            db: Database session
        """
        self.db = db

    def calculate_user_xp(self, user_id: str) -> Dict[str, float]:
        """
        Calculate and update XP for a specific user.

        Args:
            user_id: User ID

        Returns:
            Dict containing all XP values

        Raises:
            ValueError: If user not found
        """
        user = self.db.query(UserDB).filter(UserDB.id == user_id).first()
        if not user:
            raise ValueError(f"User {user_id} not found")

        return recalculate_user_xp(user, self.db)

    def get_user_xp(self, user_id: str) -> Dict[str, float]:
        """
        Get current XP values for a user (without recalculating).

        Args:
            user_id: User ID

        Returns:
            Dict containing all XP values

        Raises:
            ValueError: If user not found
        """
        user = self.db.query(UserDB).filter(UserDB.id == user_id).first()
        if not user:
            raise ValueError(f"User {user_id} not found")

        return {
            'professional_xp': user.professional_xp,
            'education_xp': user.education_xp,
            'skills_xp': user.skills_xp,
            'vocational_xp': user.vocational_xp,
            'total_xp': user.total_xp,
            'level': user.level,
        }

    def get_leaderboard(self, limit: int = 10) -> list:
        """
        Get top users by total XP.

        Args:
            limit: Maximum number of users to return

        Returns:
            List of user dictionaries with XP data
        """
        users = (
            self.db.query(UserDB)
            .order_by(UserDB.total_xp.desc())
            .limit(limit)
            .all()
        )

        return [
            {
                'user_id': user.id,
                'username': user.username,
                'professional_xp': user.professional_xp,
                'education_xp': user.education_xp,
                'skills_xp': user.skills_xp,
                'vocational_xp': user.vocational_xp,
                'total_xp': user.total_xp,
                'level': user.level,
            }
            for user in users
        ]

    def recalculate_all_users(self) -> int:
        """
        Recalculate XP for all users in the system.

        Useful for maintenance or after XP formula changes.

        Returns:
            int: Number of users updated
        """
        users = self.db.query(UserDB).all()
        count = 0

        for user in users:
            recalculate_user_xp(user, self.db)
            count += 1

        return count
