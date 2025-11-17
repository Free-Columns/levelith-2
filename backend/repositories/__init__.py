"""
Levelith Repository Layer

This module contains the repository implementations for the Levelith application.
Repositories implement the Repository Pattern, providing an abstraction layer
between the domain models and data storage.

According to MANIFEST.md:
- Repository Pattern: Separates data access from business logic
- Dependency Injection: Repositories are injected into services
- Type Safety: All repositories use type hints
- Testability: Easy to mock for unit testing

Architecture:
    Controllers/API -> Services -> Repositories -> Data Store

Repositories:
    - UserRepository: CRUD operations for User entities
    - ExperienceRepository: CRUD operations for Experience entities (all 9 types)

Usage:
    >>> from backend.repositories import UserRepository, ExperienceRepository
    >>> user_repo = UserRepository()
    >>> exp_repo = ExperienceRepository()
"""

from backend.repositories.user_repository import UserRepository
from backend.repositories.experience_repository import ExperienceRepository

__all__ = [
    "UserRepository",
    "ExperienceRepository",
]
