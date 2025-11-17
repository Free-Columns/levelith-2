"""
Levelith Domain Models

This module contains the core domain models for the Levelith application.
All models follow the architecture defined in MANIFEST.md.

Models:
    - User: User account and profile
    - Experience: Base class for all experience types
    - Education experiences: Certificate, Degree, Course
    - Workplace experiences: Gig, PartTime, FullTime
    - Skills experiences: SoftSkill, HardSkill, NativeSkill
"""

from backend.models.user import User
from backend.models.experience import (
    Experience,
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

__all__ = [
    "User",
    "Experience",
    "validate_naics_code",
    # Education
    "Certificate",
    "Degree",
    "Course",
    # Workplace
    "Gig",
    "PartTime",
    "FullTime",
    # Skills
    "SoftSkill",
    "HardSkill",
    "NativeSkill",
]
