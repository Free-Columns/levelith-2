"""
SQLAlchemy ORM Models

Database models for User and Experience using SQLAlchemy ORM.
These models map to PostgreSQL tables and handle persistence.
"""

import secrets
from datetime import datetime
from typing import List

from sqlalchemy import (
    Column, String, Boolean, DateTime, JSON, ForeignKey, Text, Enum as SQLEnum, Integer
)
from sqlalchemy.orm import relationship

from backend.database import Base
from backend.models.experience import ExperienceCategory, ExperienceType


class UserDB(Base):
    """
    User ORM model for database persistence.

    Maps to 'users' table in PostgreSQL.
    """

    __tablename__ = "users"

    id = Column(String(32), primary_key=True, default=lambda: secrets.token_hex(16))
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)

    # Profile fields
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    profile_data = Column(JSON, default=dict, nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login = Column(DateTime, nullable=True)

    # Relationships
    experiences = relationship("ExperienceDB", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username={self.username})>"


class ExperienceDB(Base):
    """
    Experience ORM model for database persistence.

    Maps to 'experiences' table in PostgreSQL.
    Handles all 9 experience subtypes with polymorphic identity.
    """

    __tablename__ = "experiences"

    id = Column(String(32), primary_key=True, default=lambda: secrets.token_hex(16))
    user_id = Column(String(32), ForeignKey("users.id"), nullable=False, index=True)

    # Core fields
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    naics_code = Column(String(6), nullable=False, default="123456")

    # Category and Type
    category = Column(SQLEnum(ExperienceCategory), nullable=False)
    experience_type = Column(SQLEnum(ExperienceType), nullable=False)

    # Dates
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    is_current = Column(Boolean, default=False)

    # Organization/Institution
    organization = Column(String(255), nullable=True)
    location = Column(String(255), nullable=True)

    # Type-specific data stored as JSON
    type_specific_data = Column(JSON, default=dict, nullable=False)

    # Metadata
    tags = Column(JSON, default=list, nullable=False)
    metadata = Column(JSON, default=dict, nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("UserDB", back_populates="experiences")

    def __repr__(self) -> str:
        return f"<Experience(id={self.id}, type={self.experience_type.value}, title={self.title})>"


class CertificateDB(ExperienceDB):
    """Certificate experience - extends ExperienceDB."""

    __mapper_args__ = {
        'polymorphic_identity': ExperienceType.CERTIFICATE,
    }


class DegreeDB(ExperienceDB):
    """Degree experience - extends ExperienceDB."""

    __mapper_args__ = {
        'polymorphic_identity': ExperienceType.DEGREE,
    }


class CourseDB(ExperienceDB):
    """Course experience - extends ExperienceDB."""

    __mapper_args__ = {
        'polymorphic_identity': ExperienceType.COURSE,
    }


class GigDB(ExperienceDB):
    """Gig experience - extends ExperienceDB."""

    __mapper_args__ = {
        'polymorphic_identity': ExperienceType.GIG,
    }


class PartTimeDB(ExperienceDB):
    """PartTime experience - extends ExperienceDB."""

    __mapper_args__ = {
        'polymorphic_identity': ExperienceType.PART_TIME,
    }


class FullTimeDB(ExperienceDB):
    """FullTime experience - extends ExperienceDB."""

    __mapper_args__ = {
        'polymorphic_identity': ExperienceType.FULL_TIME,
    }


class SoftSkillDB(ExperienceDB):
    """SoftSkill experience - extends ExperienceDB."""

    __mapper_args__ = {
        'polymorphic_identity': ExperienceType.SOFT_SKILL,
    }


class HardSkillDB(ExperienceDB):
    """HardSkill experience - extends ExperienceDB."""

    __mapper_args__ = {
        'polymorphic_identity': ExperienceType.HARD_SKILL,
    }


class NativeSkillDB(ExperienceDB):
    """NativeSkill experience - extends ExperienceDB."""

    __mapper_args__ = {
        'polymorphic_identity': ExperienceType.NATIVE_SKILL,
    }
