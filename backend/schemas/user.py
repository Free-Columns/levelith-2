"""
User API Schemas

Pydantic models for user-related API requests and responses.
"""

from datetime import datetime
from typing import Optional, Dict, List

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserBase(BaseModel):
    """Base user schema with common fields."""

    username: str = Field(..., min_length=3, max_length=50, description="Unique username")
    email: EmailStr = Field(..., description="User email address")

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        """Validate username format."""
        if not all(c.isalnum() or c in ("_", "-") for c in v):
            raise ValueError("Username must contain only alphanumeric characters, underscores, and hyphens")
        return v


class UserCreate(UserBase):
    """Schema for creating a new user."""

    password: str = Field(..., min_length=8, description="User password (min 8 characters)")
    profile_data: Optional[Dict] = Field(default_factory=dict, description="Additional profile data")


class UserUpdate(BaseModel):
    """Schema for updating user information."""

    email: Optional[EmailStr] = None
    profile_data: Optional[Dict] = None
    is_active: Optional[bool] = None


class UserLogin(BaseModel):
    """Schema for user login."""

    username: str = Field(..., description="Username or email")
    password: str = Field(..., description="User password")


class UserResponse(UserBase):
    """Schema for user response (without sensitive data)."""

    id: str
    is_active: bool
    is_verified: bool
    profile_data: Dict

    # XP and Leveling
    professional_xp: float = Field(default=0.0, description="Professional experience XP")
    education_xp: float = Field(default=0.0, description="Education XP")
    skills_xp: float = Field(default=0.0, description="Skills XP")
    vocational_xp: float = Field(default=0.0, description="Vocational XP")
    total_xp: float = Field(default=0.0, description="Total XP (sum of all categories)")
    level: int = Field(default=0, description="User level")

    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None
    experience_count: int = Field(default=0, description="Number of experiences")

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Schema for authentication token response."""

    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    expires_in: int = Field(..., description="Token expiration time in seconds")


class UserWithExperiences(UserResponse):
    """Schema for user with their experiences."""

    experiences: List[str] = Field(default_factory=list, description="List of experience IDs")
