"""
Experience Management API Endpoints

Provides REST API for experience CRUD operations.
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.db_models import ExperienceDB, UserDB
from backend.models.experience import ExperienceCategory, ExperienceType
from backend.schemas.experience import (
    ExperienceCreate,
    ExperienceResponse,
    ExperienceUpdate,
    ExperienceList
)

router = APIRouter()


@router.post("/", response_model=ExperienceResponse, status_code=status.HTTP_201_CREATED)
async def create_experience(
    experience_data: ExperienceCreate,
    user_id: str = Query(..., description="User ID who owns this experience"),
    db: Session = Depends(get_db)
):
    """
    Create a new experience for a user.

    Args:
        experience_data: Experience creation data
        user_id: ID of the user who owns this experience
        db: Database session

    Returns:
        Created experience information

    Raises:
        HTTPException: If user not found
    """
    # Verify user exists
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Create experience
    db_experience = ExperienceDB(
        user_id=user_id,
        title=experience_data.title,
        description=experience_data.description,
        naics_code=experience_data.naics_code,
        category=experience_data.category,
        experience_type=experience_data.experience_type,
        start_date=experience_data.start_date,
        end_date=experience_data.end_date,
        is_current=experience_data.is_current,
        organization=experience_data.organization,
        location=experience_data.location,
        type_specific_data=experience_data.type_specific_data,
        tags=experience_data.tags,
        experience_metadata=experience_data.metadata  # Map API 'metadata' to DB 'experience_metadata'
    )

    db.add(db_experience)
    db.commit()
    db.refresh(db_experience)

    return ExperienceResponse.model_validate(db_experience)


@router.get("/{experience_id}", response_model=ExperienceResponse)
async def get_experience(experience_id: str, db: Session = Depends(get_db)):
    """
    Get experience by ID.

    Args:
        experience_id: Experience ID
        db: Database session

    Returns:
        Experience information

    Raises:
        HTTPException: If experience not found
    """
    experience = db.query(ExperienceDB).filter(ExperienceDB.id == experience_id).first()
    if not experience:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experience not found"
        )

    return ExperienceResponse.model_validate(experience)


@router.get("/", response_model=ExperienceList)
async def list_experiences(
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    category: Optional[ExperienceCategory] = Query(None, description="Filter by category"),
    experience_type: Optional[ExperienceType] = Query(None, description="Filter by type"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """
    List experiences with filtering and pagination.

    Args:
        user_id: Filter by user ID
        category: Filter by experience category
        experience_type: Filter by specific experience type
        page: Page number (1-indexed)
        page_size: Number of items per page
        db: Database session

    Returns:
        Paginated list of experiences
    """
    # Build query
    query = db.query(ExperienceDB)

    # Apply filters
    if user_id:
        query = query.filter(ExperienceDB.user_id == user_id)
    if category:
        query = query.filter(ExperienceDB.category == category)
    if experience_type:
        query = query.filter(ExperienceDB.experience_type == experience_type)

    # Get total count
    total = query.count()

    # Apply pagination
    skip = (page - 1) * page_size
    experiences = query.offset(skip).limit(page_size).all()

    # Check if there are more pages
    has_more = (skip + len(experiences)) < total

    return ExperienceList(
        items=[ExperienceResponse.model_validate(exp) for exp in experiences],
        total=total,
        page=page,
        page_size=page_size,
        has_more=has_more
    )


@router.patch("/{experience_id}", response_model=ExperienceResponse)
async def update_experience(
    experience_id: str,
    experience_data: ExperienceUpdate,
    db: Session = Depends(get_db)
):
    """
    Update experience information.

    Args:
        experience_id: Experience ID
        experience_data: Updated experience data
        db: Database session

    Returns:
        Updated experience information

    Raises:
        HTTPException: If experience not found
    """
    experience = db.query(ExperienceDB).filter(ExperienceDB.id == experience_id).first()
    if not experience:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experience not found"
        )

    # Update fields
    update_data = experience_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        # Map 'metadata' from API to 'experience_metadata' in DB
        if field == 'metadata':
            setattr(experience, 'experience_metadata', value)
        else:
            setattr(experience, field, value)

    db.commit()
    db.refresh(experience)

    return ExperienceResponse.model_validate(experience)


@router.delete("/{experience_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_experience(experience_id: str, db: Session = Depends(get_db)):
    """
    Delete an experience.

    Args:
        experience_id: Experience ID
        db: Database session

    Raises:
        HTTPException: If experience not found
    """
    experience = db.query(ExperienceDB).filter(ExperienceDB.id == experience_id).first()
    if not experience:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experience not found"
        )

    db.delete(experience)
    db.commit()


@router.get("/user/{user_id}/summary")
async def get_user_experience_summary(user_id: str, db: Session = Depends(get_db)):
    """
    Get summary statistics of user's experiences.

    Args:
        user_id: User ID
        db: Database session

    Returns:
        Summary statistics by category and type

    Raises:
        HTTPException: If user not found
    """
    # Verify user exists
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    experiences = db.query(ExperienceDB).filter(ExperienceDB.user_id == user_id).all()

    # Calculate summary
    summary = {
        "total": len(experiences),
        "by_category": {},
        "by_type": {},
        "current_count": sum(1 for exp in experiences if exp.is_current)
    }

    for exp in experiences:
        # Count by category
        cat = exp.category.value
        summary["by_category"][cat] = summary["by_category"].get(cat, 0) + 1

        # Count by type
        exp_type = exp.experience_type.value
        summary["by_type"][exp_type] = summary["by_type"].get(exp_type, 0) + 1

    return summary
