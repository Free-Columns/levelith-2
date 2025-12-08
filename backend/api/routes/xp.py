"""
XP Management API Endpoints

Provides REST API for XP calculation, leveling, and leaderboard.
"""

from typing import Dict
from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel, Field

from backend.dependencies import get_xp_service
from backend.services.xp_service import XPService


router = APIRouter()


class XPResponse(BaseModel):
    """XP data response schema."""
    user_id: str
    professional_xp: float = Field(..., description="Professional XP (FullTime, PartTime, Gig)")
    education_xp: float = Field(..., description="Education XP (Certificate, Degree, Course)")
    skills_xp: float = Field(..., description="Skills XP (SoftSkill, HardSkill, NativeSkill)")
    vocational_xp: float = Field(..., description="Vocational XP (Volunteer, Projects - future)")
    total_xp: float = Field(..., description="Total XP (sum of all categories)")
    level: int = Field(..., description="Current level")


class LeaderboardEntry(BaseModel):
    """Leaderboard entry schema."""
    rank: int
    user_id: str
    username: str
    professional_xp: float
    education_xp: float
    skills_xp: float
    vocational_xp: float
    total_xp: float
    level: int


class LeaderboardResponse(BaseModel):
    """Leaderboard response schema."""
    entries: list[LeaderboardEntry]
    total_users: int


@router.get("/users/{user_id}/xp", response_model=XPResponse)
async def get_user_xp(
    user_id: str,
    xp_service: XPService = Depends(get_xp_service)
):
    """
    Get XP breakdown for a specific user.

    Returns current XP values across all categories and the user's level.

    Args:
        user_id: User ID
        xp_service: XP service (injected)

    Returns:
        XP breakdown and level

    Raises:
        HTTPException: If user not found
    """
    try:
        xp_data = xp_service.get_user_xp(user_id)
        return XPResponse(user_id=user_id, **xp_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/users/{user_id}/xp/recalculate", response_model=XPResponse)
async def recalculate_user_xp(
    user_id: str,
    xp_service: XPService = Depends(get_xp_service)
):
    """
    Manually trigger XP recalculation for a user.

    Useful for:
    - Fixing XP discrepancies
    - Updating XP after bulk experience changes
    - Admin operations

    Args:
        user_id: User ID
        xp_service: XP service (injected)

    Returns:
        Recalculated XP values

    Raises:
        HTTPException: If user not found
    """
    try:
        xp_data = xp_service.calculate_user_xp(user_id)
        return XPResponse(user_id=user_id, **xp_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/leaderboard", response_model=LeaderboardResponse)
async def get_leaderboard(
    limit: int = Query(10, ge=1, le=100, description="Number of top users to return"),
    xp_service: XPService = Depends(get_xp_service)
):
    """
    Get leaderboard of top users by total XP.

    Args:
        limit: Maximum number of users to return (1-100)
        xp_service: XP service (injected)

    Returns:
        Leaderboard with rankings
    """
    leaderboard_data = xp_service.get_leaderboard(limit=limit)

    # Add rankings
    entries = [
        LeaderboardEntry(rank=idx + 1, **entry)
        for idx, entry in enumerate(leaderboard_data)
    ]

    return LeaderboardResponse(
        entries=entries,
        total_users=len(entries)
    )


@router.post("/admin/recalculate-all", response_model=Dict[str, int])
async def recalculate_all_users_xp(
    xp_service: XPService = Depends(get_xp_service)
):
    """
    Recalculate XP for all users in the system.

    **Admin endpoint** - use with caution on large databases.

    Useful for:
    - After XP formula changes
    - Database migrations
    - Fixing system-wide XP issues

    Args:
        xp_service: XP service (injected)

    Returns:
        Number of users updated
    """
    count = xp_service.recalculate_all_users()

    return {
        "message": "XP recalculated for all users",
        "users_updated": count
    }
