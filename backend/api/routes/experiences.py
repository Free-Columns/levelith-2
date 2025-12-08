"""
Experience Management API Endpoints

Provides REST API for experience CRUD operations.
Refactored to use service layer following clean architecture principles.
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.dependencies import get_experience_service, get_user_service, get_xp_service
from backend.services.experience_service import ExperienceService
from backend.services.user_service import UserService
from backend.services.xp_service import XPService
from backend.models.db_models import ExperienceDB
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
    user_service: UserService = Depends(get_user_service),
    experience_service: ExperienceService = Depends(get_experience_service),
    xp_service: XPService = Depends(get_xp_service)
):
    """
    Create a new experience for a user.

    Args:
        experience_data: Experience creation data
        user_id: ID of the user who owns this experience
        user_service: User service (injected)
        experience_service: Experience service (injected)

    Returns:
        Created experience information

    Raises:
        HTTPException: If user not found or invalid experience type
    """
    # Verify user exists
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Prepare common parameters
    common_params = {
        "user_id": user_id,
        "title": experience_data.title,
        "description": experience_data.description or "",
        "naics_code": experience_data.naics_code,
        "start_date": experience_data.start_date,
        "end_date": experience_data.end_date,
        "organization": experience_data.organization,
        "location": experience_data.location,
        "skills_gained": experience_data.tags or [],
        "metadata": experience_data.metadata or {}
    }

    # Route to appropriate service method based on experience type
    exp_type = experience_data.experience_type
    type_data = experience_data.type_specific_data or {}

    try:
        if exp_type == ExperienceType.CERTIFICATE:
            experience = experience_service.create_certificate(**common_params, **type_data)
        elif exp_type == ExperienceType.DEGREE:
            experience = experience_service.create_degree(**common_params, **type_data)
        elif exp_type == ExperienceType.COURSE:
            experience = experience_service.create_course(**common_params, **type_data)
        elif exp_type == ExperienceType.GIG:
            experience = experience_service.create_gig(**common_params, **type_data)
        elif exp_type == ExperienceType.PART_TIME:
            experience = experience_service.create_part_time(**common_params, **type_data)
        elif exp_type == ExperienceType.FULL_TIME:
            experience = experience_service.create_full_time(**common_params, **type_data)
        elif exp_type == ExperienceType.SOFT_SKILL:
            experience = experience_service.create_soft_skill(**common_params, **type_data)
        elif exp_type == ExperienceType.HARD_SKILL:
            experience = experience_service.create_hard_skill(**common_params, **type_data)
        elif exp_type == ExperienceType.NATIVE_SKILL:
            experience = experience_service.create_native_skill(**common_params, **type_data)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid experience type: {exp_type}"
            )

        # Recalculate XP for the user after creating experience
        xp_service.calculate_user_xp(user_id)

        return ExperienceResponse.model_validate(experience)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create experience: {str(e)}"
        )


@router.get("/{experience_id}", response_model=ExperienceResponse)
async def get_experience(
    experience_id: str,
    experience_service: ExperienceService = Depends(get_experience_service)
):
    """
    Get experience by ID.

    Args:
        experience_id: Experience ID
        experience_service: Experience service (injected)

    Returns:
        Experience information

    Raises:
        HTTPException: If experience not found
    """
    experience = experience_service.get_experience_by_id(experience_id)
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
    page_size: int = Query(50, ge=1, le=200, description="Items per page (default: 50, max: 200)"),
    experience_service: ExperienceService = Depends(get_experience_service),
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
        experience_service: Experience service (injected)
        db: Database session (used for non-user-specific queries)

    Returns:
        Paginated list of experiences
    """
    # Calculate pagination offset
    offset = (page - 1) * page_size

    if user_id:
        # Use service layer for user-specific queries
        experiences = experience_service.get_user_experiences(
            user_id=user_id,
            category=category,
            experience_type=experience_type,
            limit=page_size,
            offset=offset
        )

        # Get total count for pagination (need to query without limit)
        all_user_experiences = experience_service.get_user_experiences(
            user_id=user_id,
            category=category,
            experience_type=experience_type
        )
        total = len(all_user_experiences)
    else:
        # TODO: Add service layer method for listing all experiences
        # For now, use direct DB access when user_id is not specified
        query = db.query(ExperienceDB)

        if category:
            query = query.filter(ExperienceDB.category == category)
        if experience_type:
            query = query.filter(ExperienceDB.experience_type == experience_type)

        total = query.count()
        db_experiences = query.offset(offset).limit(page_size).all()

        # Convert DB models to domain models (ExperienceResponse expects domain models)
        experiences = db_experiences

    # Check if there are more pages
    has_more = (offset + len(experiences)) < total

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
    experience_service: ExperienceService = Depends(get_experience_service),
    xp_service: XPService = Depends(get_xp_service),
    db: Session = Depends(get_db)
):
    """
    Update experience information.

    Args:
        experience_id: Experience ID
        experience_data: Updated experience data
        experience_service: Experience service (injected)

    Returns:
        Updated experience information

    Raises:
        HTTPException: If experience not found
    """
    try:
        # Get the experience first to find the user_id
        existing_experience = db.query(ExperienceDB).filter(ExperienceDB.id == experience_id).first()
        if not existing_experience:
            raise ValueError(f"Experience {experience_id} not found")

        user_id = existing_experience.user_id

        # Convert update data to dictionary (exclude unset fields)
        update_data = experience_data.model_dump(exclude_unset=True)

        # Update experience via service
        experience = experience_service.update_experience(experience_id, **update_data)

        # Recalculate XP for the user after updating experience
        xp_service.calculate_user_xp(user_id)

        return ExperienceResponse.model_validate(experience)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.delete("/{experience_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_experience(
    experience_id: str,
    experience_service: ExperienceService = Depends(get_experience_service),
    xp_service: XPService = Depends(get_xp_service),
    db: Session = Depends(get_db)
):
    """
    Delete an experience.

    Args:
        experience_id: Experience ID
        experience_service: Experience service (injected)
        xp_service: XP service (injected)
        db: Database session (injected)

    Raises:
        HTTPException: If experience not found
    """
    # Get the experience first to find the user_id
    existing_experience = db.query(ExperienceDB).filter(ExperienceDB.id == experience_id).first()
    if not existing_experience:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experience not found"
        )

    user_id = existing_experience.user_id

    # Delete the experience
    success = experience_service.delete_experience(experience_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experience not found"
        )

    # Recalculate XP for the user after deleting experience
    xp_service.calculate_user_xp(user_id)


@router.get("/user/{user_id}/summary")
async def get_user_experience_summary(
    user_id: str,
    user_service: UserService = Depends(get_user_service),
    experience_service: ExperienceService = Depends(get_experience_service)
):
    """
    Get summary statistics of user's experiences.

    Args:
        user_id: User ID
        user_service: User service (injected)
        experience_service: Experience service (injected)

    Returns:
        Summary statistics by category and type

    Raises:
        HTTPException: If user not found
    """
    # Verify user exists
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Get all user experiences
    experiences = experience_service.get_user_experiences(user_id)

    # Calculate summary statistics
    summary = {
        "total": len(experiences),
        "by_category": {},
        "by_type": {},
        "current_count": sum(1 for exp in experiences if exp.is_current())
    }

    for exp in experiences:
        # Count by category
        cat = exp.category.value
        summary["by_category"][cat] = summary["by_category"].get(cat, 0) + 1

        # Count by type
        exp_type = exp.experience_type.value
        summary["by_type"][exp_type] = summary["by_type"].get(exp_type, 0) + 1

    return summary
