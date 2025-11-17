"""
User Service

This module implements the Service layer for User business logic.
The service layer sits between the API/controllers and repositories,
handling business logic, validation, and orchestration.

According to MANIFEST.md:
- Service Layer: Contains business logic and orchestration
- Dependency Injection: Services receive repositories as dependencies
- Validation: Input validation and business rule enforcement
- Security: Password hashing, authentication logic

Architecture:
    Controllers/API → Services → Repositories → Data Store

The service layer handles:
- User registration and authentication
- Password management (hashing, verification)
- Profile management
- Business rule validation
- Experience management for users
- User lifecycle operations (activate, deactivate, verify)
"""

from typing import Optional, List, Dict
from datetime import datetime
from backend.models.user import User, create_user, verify_password
from backend.repositories.user_repository import UserRepository


class UserService:
    """
    Service for User business logic and operations.

    This class encapsulates all business logic related to user management,
    including registration, authentication, profile updates, and user lifecycle.

    Design Pattern: Service Layer Pattern
    - Encapsulates business logic separate from data access
    - Orchestrates operations across multiple repositories
    - Validates business rules before data persistence
    - Provides clean API for controllers to consume

    Attributes:
        user_repo: UserRepository instance for data access

    Examples:
        >>> from backend.repositories import UserRepository
        >>> repo = UserRepository()
        >>> service = UserService(user_repo=repo)
        >>> user = service.register_user(
        ...     username="johndoe",
        ...     email="john@example.com",
        ...     password="SecurePass123!"
        ... )
        >>> print(user.username)
        'johndoe'

    Note:
        This service implements business rules defined in MANIFEST.md:
        - Username/password authentication
        - Secure password hashing
        - Email verification workflow
        - User activation/deactivation
    """

    def __init__(self, user_repo: UserRepository):
        """
        Initialize UserService with required dependencies.

        Args:
            user_repo: UserRepository instance for data access

        Example:
            >>> repo = UserRepository()
            >>> service = UserService(user_repo=repo)
        """
        self.user_repo = user_repo

    def register_user(
        self,
        username: str,
        email: str,
        password: str,
        **profile_data,
    ) -> User:
        """
        Register a new user in the system.

        This method handles the complete user registration process:
        1. Validates uniqueness of username and email
        2. Creates user with hashed password
        3. Saves to repository
        4. Returns the created user

        Args:
            username: Desired username (must be unique)
            email: Email address (must be unique)
            password: Plain text password (will be hashed)
            **profile_data: Additional profile information

        Returns:
            User: Newly created user object

        Raises:
            ValueError: If username or email already exists
            ValueError: If password doesn't meet requirements

        Examples:
            >>> service = UserService(user_repo=UserRepository())
            >>> user = service.register_user(
            ...     username="johndoe",
            ...     email="john@example.com",
            ...     password="SecurePassword123!",
            ...     display_name="John Doe",
            ...     bio="Software engineer"
            ... )
            >>> print(user.id)
            '...'  # Generated user ID

        Business Rules:
            - Username must be unique across all users
            - Email must be unique across all users
            - Password must meet security requirements (handled by User model)
            - New users start as unverified and active
        """
        # Check if username already exists
        if self.user_repo.exists_by_username(username):
            raise ValueError(f"Username '{username}' is already taken")

        # Check if email already exists
        if self.user_repo.exists_by_email(email):
            raise ValueError(f"Email '{email}' is already registered")

        # Create user with hashed password
        user = create_user(
            username=username,
            email=email,
            password=password,
            **profile_data,
        )

        # Save to repository
        return self.user_repo.save(user)

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """
        Authenticate a user with email and password.

        This method verifies credentials and returns the user if valid.
        Updates last_login timestamp on successful authentication.

        Args:
            email: User's email address
            password: Plain text password to verify

        Returns:
            Optional[User]: User object if authentication succeeds, None otherwise

        Examples:
            >>> service = UserService(user_repo=UserRepository())
            >>> user = service.authenticate_user("john@example.com", "password123")
            >>> if user:
            ...     print(f"Welcome, {user.username}!")
            ... else:
            ...     print("Invalid credentials")

        Business Rules:
            - User must exist with the given email
            - User must be active (is_active = True)
            - Password must match stored hash
            - Last login timestamp is updated on success
        """
        # Find user by email
        user = self.user_repo.find_by_email(email)
        if not user:
            return None

        # Check if user is active
        if not user.is_active:
            return None

        # Verify password
        if not verify_password(password, user.password_hash):
            return None

        # Update last login
        user.update_last_login()
        self.user_repo.save(user)

        return user

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """
        Retrieve a user by their ID.

        Args:
            user_id: Unique identifier for the user

        Returns:
            Optional[User]: User object if found, None otherwise

        Examples:
            >>> service = UserService(user_repo=UserRepository())
            >>> user = service.get_user_by_id("123")
        """
        return self.user_repo.find_by_id(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve a user by their email address.

        Args:
            email: Email address to search for

        Returns:
            Optional[User]: User object if found, None otherwise

        Examples:
            >>> service = UserService(user_repo=UserRepository())
            >>> user = service.get_user_by_email("john@example.com")
        """
        return self.user_repo.find_by_email(email)

    def get_user_by_username(self, username: str) -> Optional[User]:
        """
        Retrieve a user by their username.

        Args:
            username: Username to search for

        Returns:
            Optional[User]: User object if found, None otherwise

        Examples:
            >>> service = UserService(user_repo=UserRepository())
            >>> user = service.get_user_by_username("johndoe")
        """
        return self.user_repo.find_by_username(username)

    def update_profile(self, user_id: str, profile_data: Dict) -> Optional[User]:
        """
        Update a user's profile information.

        Args:
            user_id: ID of the user to update
            profile_data: Dictionary of profile fields to update

        Returns:
            Optional[User]: Updated user object if found, None otherwise

        Raises:
            ValueError: If user not found

        Examples:
            >>> service = UserService(user_repo=UserRepository())
            >>> updated = service.update_profile("123", {
            ...     "display_name": "John Doe Updated",
            ...     "bio": "Senior software engineer",
            ...     "location": "San Francisco, CA"
            ... })

        Business Rules:
            - User must exist
            - Profile data is merged with existing data
            - Updated timestamp is automatically set
        """
        user = self.user_repo.find_by_id(user_id)
        if not user:
            raise ValueError(f"User with ID '{user_id}' not found")

        user.update_profile(profile_data)
        return self.user_repo.save(user)

    def change_password(
        self, user_id: str, old_password: str, new_password: str
    ) -> bool:
        """
        Change a user's password.

        Args:
            user_id: ID of the user
            old_password: Current password (for verification)
            new_password: New password to set

        Returns:
            bool: True if password changed successfully, False otherwise

        Raises:
            ValueError: If user not found
            ValueError: If old password is incorrect
            ValueError: If new password doesn't meet requirements

        Examples:
            >>> service = UserService(user_repo=UserRepository())
            >>> success = service.change_password(
            ...     "123",
            ...     "OldPassword123!",
            ...     "NewSecurePass456!"
            ... )

        Business Rules:
            - User must exist
            - Old password must be correct
            - New password must meet security requirements
            - Password hash is updated
        """
        from backend.models.user import hash_password

        user = self.user_repo.find_by_id(user_id)
        if not user:
            raise ValueError(f"User with ID '{user_id}' not found")

        # Verify old password
        if not verify_password(old_password, user.password_hash):
            raise ValueError("Current password is incorrect")

        # Hash new password
        user.password_hash = hash_password(new_password)
        user.updated_at = datetime.now()

        self.user_repo.save(user)
        return True

    def activate_user(self, user_id: str) -> Optional[User]:
        """
        Activate a user account.

        Args:
            user_id: ID of the user to activate

        Returns:
            Optional[User]: Updated user if found, None otherwise

        Raises:
            ValueError: If user not found

        Examples:
            >>> service = UserService(user_repo=UserRepository())
            >>> user = service.activate_user("123")
            >>> print(user.is_active)
            True
        """
        user = self.user_repo.find_by_id(user_id)
        if not user:
            raise ValueError(f"User with ID '{user_id}' not found")

        user.activate()
        return self.user_repo.save(user)

    def deactivate_user(self, user_id: str) -> Optional[User]:
        """
        Deactivate a user account.

        Args:
            user_id: ID of the user to deactivate

        Returns:
            Optional[User]: Updated user if found, None otherwise

        Raises:
            ValueError: If user not found

        Examples:
            >>> service = UserService(user_repo=UserRepository())
            >>> user = service.deactivate_user("123")
            >>> print(user.is_active)
            False
        """
        user = self.user_repo.find_by_id(user_id)
        if not user:
            raise ValueError(f"User with ID '{user_id}' not found")

        user.deactivate()
        return self.user_repo.save(user)

    def verify_user_email(self, user_id: str) -> Optional[User]:
        """
        Mark a user's email as verified.

        Args:
            user_id: ID of the user to verify

        Returns:
            Optional[User]: Updated user if found, None otherwise

        Raises:
            ValueError: If user not found

        Examples:
            >>> service = UserService(user_repo=UserRepository())
            >>> user = service.verify_user_email("123")
            >>> print(user.is_verified)
            True
        """
        user = self.user_repo.find_by_id(user_id)
        if not user:
            raise ValueError(f"User with ID '{user_id}' not found")

        user.verify_email()
        return self.user_repo.save(user)

    def delete_user(self, user_id: str) -> bool:
        """
        Delete a user account.

        WARNING: This permanently deletes the user and cannot be undone.

        Args:
            user_id: ID of the user to delete

        Returns:
            bool: True if deleted successfully, False if not found

        Examples:
            >>> service = UserService(user_repo=UserRepository())
            >>> success = service.delete_user("123")

        Business Rules:
            - Permanently deletes user data
            - Cannot be undone
            - Consider deactivation instead for soft deletes
        """
        return self.user_repo.delete(user_id)

    def list_users(
        self,
        active_only: bool = False,
        verified_only: bool = False,
        limit: Optional[int] = None,
        offset: Optional[int] = 0,
    ) -> List[User]:
        """
        List users with optional filtering and pagination.

        Args:
            active_only: If True, return only active users
            verified_only: If True, return only verified users
            limit: Maximum number of users to return
            offset: Number of users to skip (for pagination)

        Returns:
            List[User]: List of users matching criteria

        Examples:
            >>> service = UserService(user_repo=UserRepository())
            >>> all_users = service.list_users()
            >>> active_users = service.list_users(active_only=True)
            >>> page_2 = service.list_users(limit=10, offset=10)
        """
        if active_only:
            users = self.user_repo.find_active_users()
        elif verified_only:
            users = self.user_repo.find_verified_users()
        else:
            users = self.user_repo.find_all(limit=limit, offset=offset)

        # Apply additional filters if needed
        if active_only and verified_only:
            users = [u for u in users if u.is_active and u.is_verified]

        # Apply pagination if not already done
        if (active_only or verified_only) and (limit or offset):
            if offset:
                users = users[offset:]
            if limit:
                users = users[:limit]

        return users

    def search_users(self, query: str) -> List[User]:
        """
        Search for users by username pattern.

        Args:
            query: Search query (case-insensitive substring match)

        Returns:
            List[User]: List of matching users

        Examples:
            >>> service = UserService(user_repo=UserRepository())
            >>> results = service.search_users("john")
            >>> for user in results:
            ...     print(user.username)
        """
        return self.user_repo.search_by_username_pattern(query)

    def get_user_count(self) -> int:
        """
        Get the total number of users.

        Returns:
            int: Total user count

        Examples:
            >>> service = UserService(user_repo=UserRepository())
            >>> total = service.get_user_count()
            >>> print(f"Total users: {total}")
        """
        return self.user_repo.count()

    def add_experience_to_user(self, user_id: str, experience_id: str) -> Optional[User]:
        """
        Add an experience to a user's experience array.

        Args:
            user_id: ID of the user
            experience_id: ID of the experience to add

        Returns:
            Optional[User]: Updated user if successful, None otherwise

        Raises:
            ValueError: If user not found
            ValueError: If experience_id is empty or already exists

        Examples:
            >>> service = UserService(user_repo=UserRepository())
            >>> user = service.add_experience_to_user("user123", "exp456")
            >>> print(len(user.experiences))
        """
        user = self.user_repo.find_by_id(user_id)
        if not user:
            raise ValueError(f"User with ID '{user_id}' not found")

        user.add_experience(experience_id)
        return self.user_repo.save(user)

    def remove_experience_from_user(
        self, user_id: str, experience_id: str
    ) -> Optional[User]:
        """
        Remove an experience from a user's experience array.

        Args:
            user_id: ID of the user
            experience_id: ID of the experience to remove

        Returns:
            Optional[User]: Updated user if successful, None otherwise

        Raises:
            ValueError: If user not found
            ValueError: If experience doesn't exist for user

        Examples:
            >>> service = UserService(user_repo=UserRepository())
            >>> user = service.remove_experience_from_user("user123", "exp456")
        """
        user = self.user_repo.find_by_id(user_id)
        if not user:
            raise ValueError(f"User with ID '{user_id}' not found")

        user.remove_experience(experience_id)
        return self.user_repo.save(user)

    def get_user_experiences(self, user_id: str) -> List[str]:
        """
        Get the list of experience IDs for a user.

        Args:
            user_id: ID of the user

        Returns:
            List[str]: List of experience IDs

        Raises:
            ValueError: If user not found

        Examples:
            >>> service = UserService(user_repo=UserRepository())
            >>> exp_ids = service.get_user_experiences("user123")
            >>> print(f"User has {len(exp_ids)} experiences")
        """
        user = self.user_repo.find_by_id(user_id)
        if not user:
            raise ValueError(f"User with ID '{user_id}' not found")

        return user.experiences
