"""
Levelith Service Layer

This module contains the service implementations for the Levelith application.
Services implement the Service Layer Pattern, encapsulating business logic
and orchestrating operations across repositories.

According to MANIFEST.md:
- Service Layer: Contains business logic separate from data access
- Dependency Injection: Services receive repositories as dependencies
- Business Rules: Validates and enforces business rules
- Orchestration: Coordinates operations across multiple repositories

Architecture:
    Controllers/API -> Services -> Repositories -> Data Store

Services:
    - UserService: User management, authentication, profile operations
    - ExperienceService: Experience CRUD for all 9 types, NAICS validation

Usage:
    >>> from backend.repositories import UserRepository, ExperienceRepository
    >>> from backend.services import UserService, ExperienceService
    >>>
    >>> # Initialize repositories
    >>> user_repo = UserRepository()
    >>> exp_repo = ExperienceRepository()
    >>>
    >>> # Initialize services with dependency injection
    >>> user_service = UserService(user_repo=user_repo)
    >>> exp_service = ExperienceService(experience_repo=exp_repo)
    >>>
    >>> # Use services for business operations
    >>> user = user_service.register_user(
    ...     username="johndoe",
    ...     email="john@example.com",
    ...     password="SecurePass123!"
    ... )
"""

from backend.services.user_service import UserService
from backend.services.experience_service import ExperienceService

__all__ = [
    "UserService",
    "ExperienceService",
]
