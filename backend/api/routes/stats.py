"""
Statistics API Endpoints

Provides aggregated statistics for the admin dashboard.
"""

from typing import Dict, List
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.database import get_db
from backend.models.db_models import UserDB, ExperienceDB

router = APIRouter()


@router.get("/stats")
async def get_stats(db: Session = Depends(get_db)) -> Dict:
    """
    Get comprehensive statistics for admin dashboard.

    Args:
        db: Database session

    Returns:
        Dictionary containing user, experience, skills, and geographic statistics

    Example:
        >>> GET /api/v1/stats
        {
            "users": {
                "total": 100,
                "active": 85,
                "verified": 60,
                "inactive": 15,
                "growth": [...],
                "activity": [...]
            },
            "experiences": {
                "total": 450,
                "byType": {...},
                "byCategory": {...},
                "byIndustry": {...}
            },
            "skills": {
                "top": [...],
                "total": 120
            },
            "geography": {
                "locations": [...]
            }
        }
    """
    # User statistics
    total_users = db.query(UserDB).count()
    active_users = db.query(UserDB).filter(UserDB.is_active == True).count()
    verified_users = db.query(UserDB).filter(UserDB.is_verified == True).count()
    inactive_users = total_users - active_users

    # User growth over last 12 months
    now = datetime.utcnow()
    user_growth = []
    for i in range(11, -1, -1):
        month_start = datetime(now.year, now.month, 1) - timedelta(days=30 * i)
        month_name = month_start.strftime("%b")

        # Count users created up to this month
        count = db.query(UserDB).filter(UserDB.created_at <= month_start).count()
        user_growth.append({
            "month": month_name,
            "users": max(1, count)
        })

    # User activity (last 30 days)
    user_activity = []
    for i in range(29, -1, -1):
        activity_date = now - timedelta(days=i)
        date_str = activity_date.strftime("%b %d")

        # Count users who logged in on this day
        # For now, we'll use a simple estimate based on active users
        # TODO: Implement proper login tracking
        logins = active_users // 30 if active_users > 0 else 0
        user_activity.append({
            "date": date_str,
            "logins": logins
        })

    # Experience statistics
    total_experiences = db.query(ExperienceDB).count()

    # Experiences by type
    exp_by_type = db.query(
        ExperienceDB.experience_type,
        func.count(ExperienceDB.id)
    ).group_by(ExperienceDB.experience_type).all()

    experiences_by_type = {
        exp_type: count for exp_type, count in exp_by_type
    }

    # Experiences by category
    exp_by_category = db.query(
        ExperienceDB.category,
        func.count(ExperienceDB.id)
    ).group_by(ExperienceDB.category).all()

    experiences_by_category = {
        category: count for category, count in exp_by_category
    }

    # Experiences by industry (based on NAICS codes)
    # Map NAICS codes to industries
    naics_to_industry = {
        "123456": "general",
        "541511": "technology",
        "541512": "technology",
        "541513": "technology",
        "541519": "technology",
        "541611": "services",
        "541618": "services",
        "611310": "education",
        "611420": "education",
        "611430": "education",
        "611710": "education",
        "621111": "healthcare",
        "621511": "healthcare",
        "522110": "finance",
        "522210": "finance",
        "445110": "retail",
        "722511": "retail",
        "311811": "manufacturing",
        "336411": "manufacturing",
    }

    exp_by_naics = db.query(
        ExperienceDB.naics_code,
        func.count(ExperienceDB.id)
    ).group_by(ExperienceDB.naics_code).all()

    experiences_by_industry = {}
    for naics_code, count in exp_by_naics:
        industry = naics_to_industry.get(naics_code, "general")
        experiences_by_industry[industry] = experiences_by_industry.get(industry, 0) + count

    # Top skills
    # TODO: Implement proper skills tracking from experiences
    # For now, return empty list
    top_skills = []
    total_skills = 0

    # Geographic distribution
    # Extract locations from user profile data
    users_with_locations = db.query(UserDB).filter(
        UserDB.profile_data.isnot(None)
    ).all()

    location_counts = {}
    for user in users_with_locations:
        if user.profile_data and isinstance(user.profile_data, dict):
            location = user.profile_data.get("location")
            if location:
                location_counts[location] = location_counts.get(location, 0) + 1

    # Sort and get top 8 locations
    top_locations = sorted(
        location_counts.items(),
        key=lambda x: x[1],
        reverse=True
    )[:8]

    locations_list = [
        {"location": loc, "count": count}
        for loc, count in top_locations
    ]

    return {
        "users": {
            "total": total_users,
            "active": active_users,
            "verified": verified_users,
            "inactive": inactive_users,
            "growth": user_growth,
            "activity": user_activity,
        },
        "experiences": {
            "total": total_experiences,
            "byType": experiences_by_type,
            "byCategory": experiences_by_category,
            "byIndustry": experiences_by_industry,
        },
        "skills": {
            "top": top_skills,
            "total": total_skills,
        },
        "geography": {
            "locations": locations_list,
        },
    }
