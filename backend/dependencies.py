"""
Dependency Injection for FastAPI

Provides service instances and other dependencies to API routes.
Follows FastAPI's dependency injection pattern using Depends().
"""

from fastapi import Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.services.user_service import UserService
from backend.services.experience_service import ExperienceService
from backend.services.naics_service import NAICSService
from backend.services.xp_service import XPService
from backend.repositories.user_repository import UserRepository
from backend.repositories.experience_repository import ExperienceRepository
from backend.repositories.naics_repository import NAICSRepository


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    """
    Provide a UserRepository instance.

    Args:
        db: Database session (injected)

    Returns:
        UserRepository: Repository for user data access

    Example:
        @router.get("/users")
        async def list_users(
            user_repo: UserRepository = Depends(get_user_repository)
        ):
            return user_repo.find_all()
    """
    return UserRepository(db)


def get_experience_repository(db: Session = Depends(get_db)) -> ExperienceRepository:
    """
    Provide an ExperienceRepository instance.

    Args:
        db: Database session (injected)

    Returns:
        ExperienceRepository: Repository for experience data access
    """
    return ExperienceRepository(db)


def get_naics_repository(db: Session = Depends(get_db)) -> NAICSRepository:
    """
    Provide a NAICSRepository instance.

    Args:
        db: Database session (injected)

    Returns:
        NAICSRepository: Repository for NAICS data access
    """
    return NAICSRepository(db)


def get_user_service(
    user_repo: UserRepository = Depends(get_user_repository)
) -> UserService:
    """
    Provide a UserService instance.

    This is the primary dependency for user-related business logic.
    Use this instead of direct database access in API routes.

    Args:
        user_repo: UserRepository (injected)

    Returns:
        UserService: Service for user business logic

    Example:
        @router.post("/users")
        async def create_user(
            user_data: UserCreate,
            user_service: UserService = Depends(get_user_service)
        ):
            return user_service.register_user(
                username=user_data.username,
                email=user_data.email,
                password=user_data.password
            )
    """
    return UserService(user_repo=user_repo)


def get_experience_service(
    experience_repo: ExperienceRepository = Depends(get_experience_repository)
) -> ExperienceService:
    """
    Provide an ExperienceService instance.

    This is the primary dependency for experience-related business logic.
    Use this instead of direct database access in API routes.

    Args:
        experience_repo: ExperienceRepository (injected)

    Returns:
        ExperienceService: Service for experience business logic

    Example:
        @router.post("/experiences")
        async def create_experience(
            exp_data: ExperienceCreate,
            exp_service: ExperienceService = Depends(get_experience_service)
        ):
            return exp_service.create_certificate(
                user_id=exp_data.user_id,
                title=exp_data.title,
                ...
            )
    """
    return ExperienceService(experience_repo=experience_repo)


def get_naics_service(
    naics_repo: NAICSRepository = Depends(get_naics_repository)
) -> NAICSService:
    """
    Provide a NAICSService instance.

    Args:
        naics_repo: NAICSRepository (injected)

    Returns:
        NAICSService: Service for NAICS business logic
    """
    return NAICSService(naics_repo=naics_repo)


def get_xp_service(db: Session = Depends(get_db)) -> XPService:
    """
    Provide an XPService instance.

    Args:
        db: Database session (injected)

    Returns:
        XPService: Service for XP calculation and management
    """
    return XPService(db=db)
