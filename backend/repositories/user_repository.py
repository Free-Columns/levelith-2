"""
User Repository

This module implements the Repository pattern for User data access.
The repository abstracts data storage operations and provides a clean
interface for CRUD operations on User entities.

According to MANIFEST.md:
- Repository Pattern: Separates data access from business logic
- Dependency Injection: Repositories are injected into services
- Type Safety: All methods use type hints for clarity

Architecture:
    Controllers/API → Services → Repositories → Data Store

The repository layer handles:
- Data persistence (create, read, update, delete)
- Query construction and execution
- Data mapping between storage and domain models
- Transaction management
"""

from typing import Optional, List, Dict
from datetime import datetime
from backend.models.user import User


class UserRepository:
    """
    Repository for User entity data access operations.

    This class provides an abstraction layer between the domain models
    and the data storage mechanism. Currently implements in-memory storage,
    but designed to be easily swapped with database implementations.

    Design Pattern: Repository Pattern
    - Centralizes data access logic
    - Provides consistent interface for data operations
    - Enables easy testing with mock repositories
    - Allows switching storage backends without changing business logic

    Attributes:
        _users: In-memory storage dictionary mapping user IDs to User objects
        _email_index: Index for fast email lookups
        _username_index: Index for fast username lookups

    Examples:
        >>> repo = UserRepository()
        >>> user = User(id="123", username="johndoe", ...)
        >>> repo.save(user)
        >>> found = repo.find_by_id("123")
        >>> print(found.username)
        'johndoe'

    Note:
        In production, this will be replaced with database implementations
        (PostgreSQL via SQLAlchemy, for example).
    """

    def __init__(self):
        """
        Initialize the UserRepository with in-memory storage.

        In production, this would accept database connection/session
        as a dependency injection parameter.

        Example:
            # Current (in-memory)
            repo = UserRepository()

            # Future (database)
            repo = UserRepository(db_session=session)
        """
        self._users: Dict[str, User] = {}
        self._email_index: Dict[str, str] = {}  # email -> user_id
        self._username_index: Dict[str, str] = {}  # username -> user_id

    def save(self, user: User) -> User:
        """
        Save or update a user in the repository.

        This method handles both creation (if user doesn't exist) and
        updates (if user exists). It maintains indexes for efficient lookups.

        Args:
            user: User object to save

        Returns:
            User: The saved user object

        Raises:
            ValueError: If email or username already exists (for different user)

        Examples:
            >>> repo = UserRepository()
            >>> user = User(id="123", username="johndoe", email="john@example.com", ...)
            >>> saved_user = repo.save(user)
            >>> print(saved_user.id)
            '123'

            # Update existing user
            >>> user.username = "john_doe_updated"
            >>> updated = repo.save(user)
            >>> print(updated.username)
            'john_doe_updated'
        """
        # Check for duplicate email (different user)
        existing_email_id = self._email_index.get(user.email)
        if existing_email_id and existing_email_id != user.id:
            raise ValueError(f"Email {user.email} is already in use")

        # Check for duplicate username (different user)
        existing_username_id = self._username_index.get(user.username)
        if existing_username_id and existing_username_id != user.id:
            raise ValueError(f"Username {user.username} is already in use")

        # Update timestamp
        user.updated_at = datetime.now()

        # Save user
        self._users[user.id] = user

        # Update indexes
        self._email_index[user.email] = user.id
        self._username_index[user.username] = user.id

        return user

    def find_by_id(self, user_id: str) -> Optional[User]:
        """
        Find a user by their unique ID.

        Args:
            user_id: Unique identifier for the user

        Returns:
            Optional[User]: User object if found, None otherwise

        Examples:
            >>> repo = UserRepository()
            >>> user = repo.find_by_id("123")
            >>> if user:
            ...     print(user.username)
            ... else:
            ...     print("User not found")
        """
        return self._users.get(user_id)

    def find_by_email(self, email: str) -> Optional[User]:
        """
        Find a user by their email address.

        Uses email index for O(1) lookup performance.

        Args:
            email: Email address to search for

        Returns:
            Optional[User]: User object if found, None otherwise

        Examples:
            >>> repo = UserRepository()
            >>> user = repo.find_by_email("john@example.com")
            >>> if user:
            ...     print(f"Found user: {user.username}")
        """
        user_id = self._email_index.get(email)
        if user_id:
            return self._users.get(user_id)
        return None

    def find_by_username(self, username: str) -> Optional[User]:
        """
        Find a user by their username.

        Uses username index for O(1) lookup performance.

        Args:
            username: Username to search for

        Returns:
            Optional[User]: User object if found, None otherwise

        Examples:
            >>> repo = UserRepository()
            >>> user = repo.find_by_username("johndoe")
            >>> if user:
            ...     print(f"User email: {user.email}")
        """
        user_id = self._username_index.get(username)
        if user_id:
            return self._users.get(user_id)
        return None

    def find_all(
        self, limit: Optional[int] = None, offset: Optional[int] = 0
    ) -> List[User]:
        """
        Find all users with optional pagination.

        Args:
            limit: Maximum number of users to return (None = all)
            offset: Number of users to skip (for pagination)

        Returns:
            List[User]: List of user objects

        Examples:
            >>> repo = UserRepository()
            >>> all_users = repo.find_all()
            >>> print(f"Total users: {len(all_users)}")

            # Pagination (10 users per page, page 2)
            >>> page_2 = repo.find_all(limit=10, offset=10)
        """
        users = list(self._users.values())

        # Apply pagination
        if offset:
            users = users[offset:]
        if limit:
            users = users[:limit]

        return users

    def find_by_experience(self, experience_id: str) -> List[User]:
        """
        Find all users who have a specific experience.

        Args:
            experience_id: ID of the experience to search for

        Returns:
            List[User]: List of users with this experience

        Examples:
            >>> repo = UserRepository()
            >>> users = repo.find_by_experience("exp_123")
            >>> print(f"Found {len(users)} users with this experience")
        """
        return [
            user
            for user in self._users.values()
            if experience_id in user.experiences
        ]

    def delete(self, user_id: str) -> bool:
        """
        Delete a user from the repository.

        Removes the user and cleans up all indexes.

        Args:
            user_id: ID of the user to delete

        Returns:
            bool: True if user was deleted, False if not found

        Examples:
            >>> repo = UserRepository()
            >>> success = repo.delete("123")
            >>> if success:
            ...     print("User deleted successfully")
        """
        user = self._users.get(user_id)
        if not user:
            return False

        # Remove from indexes
        if user.email in self._email_index:
            del self._email_index[user.email]
        if user.username in self._username_index:
            del self._username_index[user.username]

        # Remove user
        del self._users[user_id]
        return True

    def exists_by_email(self, email: str) -> bool:
        """
        Check if a user exists with the given email.

        Args:
            email: Email address to check

        Returns:
            bool: True if user exists, False otherwise

        Examples:
            >>> repo = UserRepository()
            >>> if repo.exists_by_email("john@example.com"):
            ...     print("Email already taken")
        """
        return email in self._email_index

    def exists_by_username(self, username: str) -> bool:
        """
        Check if a user exists with the given username.

        Args:
            username: Username to check

        Returns:
            bool: True if user exists, False otherwise

        Examples:
            >>> repo = UserRepository()
            >>> if repo.exists_by_username("johndoe"):
            ...     print("Username already taken")
        """
        return username in self._username_index

    def count(self) -> int:
        """
        Get the total count of users in the repository.

        Returns:
            int: Total number of users

        Examples:
            >>> repo = UserRepository()
            >>> total = repo.count()
            >>> print(f"Total users: {total}")
        """
        return len(self._users)

    def find_active_users(self, limit: Optional[int] = None) -> List[User]:
        """
        Find all active users (is_active = True).

        Args:
            limit: Maximum number of users to return (None = all)

        Returns:
            List[User]: List of active users

        Examples:
            >>> repo = UserRepository()
            >>> active = repo.find_active_users()
            >>> print(f"Active users: {len(active)}")
        """
        active_users = [user for user in self._users.values() if user.is_active]

        if limit:
            active_users = active_users[:limit]

        return active_users

    def find_verified_users(self, limit: Optional[int] = None) -> List[User]:
        """
        Find all verified users (is_verified = True).

        Args:
            limit: Maximum number of users to return (None = all)

        Returns:
            List[User]: List of verified users

        Examples:
            >>> repo = UserRepository()
            >>> verified = repo.find_verified_users()
            >>> print(f"Verified users: {len(verified)}")
        """
        verified_users = [
            user for user in self._users.values() if user.is_verified
        ]

        if limit:
            verified_users = verified_users[:limit]

        return verified_users

    def search_by_username_pattern(self, pattern: str) -> List[User]:
        """
        Search for users whose username contains the given pattern.

        Case-insensitive substring search.

        Args:
            pattern: Pattern to search for in usernames

        Returns:
            List[User]: List of matching users

        Examples:
            >>> repo = UserRepository()
            >>> results = repo.search_by_username_pattern("john")
            >>> for user in results:
            ...     print(user.username)
        """
        pattern_lower = pattern.lower()
        return [
            user
            for user in self._users.values()
            if pattern_lower in user.username.lower()
        ]

    def clear(self):
        """
        Clear all users from the repository.

        WARNING: This is destructive and should only be used for testing.

        Examples:
            >>> repo = UserRepository()
            >>> repo.clear()
            >>> print(repo.count())
            0
        """
        self._users.clear()
        self._email_index.clear()
        self._username_index.clear()
