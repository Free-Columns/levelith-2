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
from backend.models.naics import NAICSCategory


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

    # Metadata (renamed from 'metadata' to avoid SQLAlchemy reserved name)
    tags = Column(JSON, default=list, nullable=False)
    experience_metadata = Column(JSON, default=dict, nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("UserDB", back_populates="experiences")

    def __repr__(self) -> str:
        return f"<Experience(id={self.id}, type={self.experience_type.value}, title={self.title})>"


class NAICSCodeDB(Base):
    """
    NAICS Code ORM model for database persistence.

    Maps to 'naics_codes' table in PostgreSQL.
    Stores the complete NAICS 2022 classification system.

    Hierarchy Denormalization:
        sector: 2-digit sector code (denormalized for fast queries)
        subsector: 3-digit subsector code (denormalized)
        industry_group: 4-digit industry group code (denormalized)
        industry_detail: 6-digit national industry code (denormalized)

    SBA Integration:
        sba_size_standard: Small Business Administration size standard
        sba_source: Source reference for SBA data

    Enhanced Search/Discovery:
        keywords: JSON array of searchable keywords
        aliases: JSON array of alternative names/synonyms
        examples: Text examples of businesses in this classification

    Documentation:
        cross_references: JSON array of related NAICS codes
        notes: Additional notes about this classification
        data_source: Source of the NAICS data

    Admin Additional Fields:
        tags: JSON array of custom tags for filtering and organization
        custom_category: Admin-defined category for internal classification
        admin_notes: Internal notes and comments for admin use only
    """

    __tablename__ = "naics_codes"

    # ========================================================================
    # PRIMARY KEY
    # ========================================================================
    code = Column(String(6), primary_key=True)

    # ========================================================================
    # CORE FIELDS
    # ========================================================================
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)

    # ========================================================================
    # HIERARCHY
    # ========================================================================
    # Level indicator (2=sector, 3=subsector, 4=industry_group, 6=national_industry)
    level = Column(Integer, nullable=False, index=True)
    
    # Parent code for tree structure
    parent_code = Column(String(6), nullable=True, index=True)
    
    # Denormalized hierarchy fields for fast queries without string parsing
    sector = Column(String(2), nullable=True, index=True)  # First 2 digits
    subsector = Column(String(3), nullable=True, index=True)  # First 3 digits
    industry_group = Column(String(4), nullable=True, index=True)  # First 4 digits
    industry_detail = Column(String(6), nullable=True)  # Full 6 digits (same as code for detail level)

    # ========================================================================
    # CATEGORIZATION
    # ========================================================================
    category = Column(SQLEnum(NAICSCategory), nullable=False, index=True)

    # ========================================================================
    # SBA (SMALL BUSINESS ADMINISTRATION) INTEGRATION
    # ========================================================================
    sba_size_standard = Column(String(255), nullable=True)
    sba_source = Column(String(255), nullable=True)

    # ========================================================================
    # ENHANCED SEARCH AND DISCOVERY
    # ========================================================================
    keywords = Column(JSON, default=list, nullable=False)  # Searchable keywords
    aliases = Column(JSON, default=list, nullable=False)  # Alternative names/synonyms
    examples = Column(Text, nullable=True)  # Example businesses in this category

    # ========================================================================
    # DOCUMENTATION AND RELATIONSHIPS
    # ========================================================================
    cross_references = Column(JSON, default=list, nullable=False)  # Related NAICS codes
    notes = Column(Text, nullable=True)  # Additional notes
    data_source = Column(String(255), nullable=True)  # Source of data

    # ========================================================================
    # METADATA
    # ========================================================================
    is_active = Column(Boolean, default=True, nullable=False)
    year = Column(Integer, default=2022, nullable=False)

    # ========================================================================
    # ADMIN-SPECIFIC FIELDS
    # ========================================================================
    tags = Column(JSON, default=list, nullable=False)
    custom_category = Column(String(100), nullable=True)
    admin_notes = Column(Text, nullable=True)

    # ========================================================================
    # TIMESTAMPS
    # ========================================================================
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<NAICSCode(code={self.code}, title={self.title})>"


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
