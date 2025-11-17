"""
Experience API Schemas

Pydantic models for experience-related API requests and responses.
"""

from datetime import datetime
from typing import Optional, Dict, List

from pydantic import BaseModel, Field, field_validator

from backend.models.experience import ExperienceCategory, ExperienceType, validate_naics_code


class ExperienceBase(BaseModel):
    """Base experience schema with common fields."""

    title: str = Field(..., min_length=1, max_length=255, description="Experience title")
    description: Optional[str] = Field(None, description="Detailed description")
    naics_code: str = Field(default="123456", description="NAICS industry code (6 digits)")

    category: ExperienceCategory = Field(..., description="Experience category")
    experience_type: ExperienceType = Field(..., description="Specific experience type")

    start_date: Optional[datetime] = Field(None, description="Start date")
    end_date: Optional[datetime] = Field(None, description="End date")
    is_current: bool = Field(default=False, description="Whether this experience is current")

    organization: Optional[str] = Field(None, max_length=255, description="Organization or institution name")
    location: Optional[str] = Field(None, max_length=255, description="Location")

    type_specific_data: Dict = Field(default_factory=dict, description="Type-specific additional data")
    tags: List[str] = Field(default_factory=list, description="Tags for categorization")
    metadata: Dict = Field(default_factory=dict, description="Additional metadata")

    @field_validator("naics_code")
    @classmethod
    def validate_naics(cls, v: str) -> str:
        """Validate and normalize NAICS code."""
        return validate_naics_code(v)

    @field_validator("end_date")
    @classmethod
    def validate_dates(cls, v: Optional[datetime], info) -> Optional[datetime]:
        """Validate that end_date is after start_date."""
        if v and info.data.get("start_date") and v < info.data["start_date"]:
            raise ValueError("End date must be after start date")
        return v


class ExperienceCreate(ExperienceBase):
    """Schema for creating a new experience."""

    pass


class ExperienceUpdate(BaseModel):
    """Schema for updating an experience."""

    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    naics_code: Optional[str] = None

    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_current: Optional[bool] = None

    organization: Optional[str] = Field(None, max_length=255)
    location: Optional[str] = Field(None, max_length=255)

    type_specific_data: Optional[Dict] = None
    tags: Optional[List[str]] = None
    metadata: Optional[Dict] = None


class ExperienceResponse(ExperienceBase):
    """Schema for experience response."""

    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ExperienceList(BaseModel):
    """Schema for paginated list of experiences."""

    items: List[ExperienceResponse]
    total: int
    page: int = 1
    page_size: int = 20
    has_more: bool = False
