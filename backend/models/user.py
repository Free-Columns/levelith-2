"""
User Domain Model

This module defines the User model for the Levelith application.
Users have username/password authentication and maintain an array of experiences.

According to MANIFEST.md:
- Authentication: Username + password (traditional authentication)
- JWT tokens for session management
- Secure password hashing (bcrypt)
- Each user has an array of Experience objects
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict
import secrets
from passlib.context import CryptContext

# Password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@dataclass
class User:
    """
    User object representing a Levelith user account.

    This is the core user model as defined in MANIFEST.md.

    Attributes:
        id: Unique user identifier (UUID or similar)
        username: User's chosen username (must be unique)
        password_hash: Hashed password (NEVER store plain text)
        email: User's email address (must be unique)
        experiences: Array of Experience objects (the core feature)
        created_at: Account creation timestamp
        updated_at: Last update timestamp
        profile_data: Additional profile information (flexible dict)
        is_active: Whether the account is active
        is_verified: Whether email has been verified
        last_login: Timestamp of last login
    """

    id: str
    username: str
    password_hash: str
    email: str
    experiences: List[str] = field(
        default_factory=list
    )  # List of experience IDs (not full objects to avoid circular deps)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    profile_data: Dict = field(default_factory=dict)
    is_active: bool = True
    is_verified: bool = False
    last_login: Optional[datetime] = None

    def __post_init__(self):
        """Validate user data after initialization."""
        self._validate_username()
        self._validate_email()

    def _validate_username(self):
        """
        Validate username meets requirements.

        Requirements:
        - Must be at least 3 characters
        - Must be at most 50 characters
        - Must contain only alphanumeric characters, underscores, and hyphens

        Raises:
            ValueError: If username is invalid
        """
        if not self.username:
            raise ValueError("Username is required")

        if len(self.username) < 3:
            raise ValueError("Username must be at least 3 characters")

        if len(self.username) > 50:
            raise ValueError("Username must be at most 50 characters")

        if not all(c.isalnum() or c in ("_", "-") for c in self.username):
            raise ValueError(
                "Username must contain only alphanumeric characters, underscores, and hyphens"
            )

    def _validate_email(self):
        """
        Validate email format.

        Basic validation - checks for @ symbol and domain.
        More robust validation should be done at the service layer.

        Raises:
            ValueError: If email is invalid
        """
        if not self.email:
            raise ValueError("Email is required")

        if "@" not in self.email or "." not in self.email.split("@")[1]:
            raise ValueError("Invalid email format")

    def add_experience(self, experience_id: str):
        """
        Add an experience to the user's experience array.

        Args:
            experience_id: ID of the experience to add

        Raises:
            ValueError: If experience_id is empty or already exists
        """
        if not experience_id:
            raise ValueError("Experience ID is required")

        if experience_id in self.experiences:
            raise ValueError("Experience already exists for this user")

        self.experiences.append(experience_id)
        self.updated_at = datetime.now()

    def remove_experience(self, experience_id: str):
        """
        Remove an experience from the user's experience array.

        Args:
            experience_id: ID of the experience to remove

        Raises:
            ValueError: If experience_id doesn't exist
        """
        if experience_id not in self.experiences:
            raise ValueError("Experience not found for this user")

        self.experiences.remove(experience_id)
        self.updated_at = datetime.now()

    def update_last_login(self):
        """Update the last login timestamp to now."""
        self.last_login = datetime.now()
        self.updated_at = datetime.now()

    def activate(self):
        """Activate the user account."""
        self.is_active = True
        self.updated_at = datetime.now()

    def deactivate(self):
        """Deactivate the user account."""
        self.is_active = False
        self.updated_at = datetime.now()

    def verify_email(self):
        """Mark the user's email as verified."""
        self.is_verified = True
        self.updated_at = datetime.now()

    def update_profile(self, profile_data: Dict):
        """
        Update user profile data.

        Args:
            profile_data: Dictionary of profile information to update

        Example:
            user.update_profile({
                "display_name": "John Doe",
                "bio": "Software engineer and educator",
                "avatar_url": "https://example.com/avatar.jpg",
                "location": "San Francisco, CA",
                "website": "https://johndoe.com"
            })
        """
        self.profile_data.update(profile_data)
        self.updated_at = datetime.now()

    def to_dict(self, include_sensitive: bool = False) -> Dict:
        """
        Convert user to dictionary representation.

        Args:
            include_sensitive: Whether to include sensitive data (password_hash)

        Returns:
            dict: Dictionary representation of the user

        Note:
            By default, password_hash is NOT included for security.
            Only include it when explicitly needed (e.g., database operations).
        """
        user_dict = {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "experiences": self.experiences,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "profile_data": self.profile_data,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "last_login": self.last_login.isoformat() if self.last_login else None,
        }

        if include_sensitive:
            user_dict["password_hash"] = self.password_hash

        return user_dict

    @staticmethod
    def generate_id() -> str:
        """
        Generate a unique user ID.

        Returns:
            str: Unique identifier (32 character hex string)

        Note:
            In production, this should use UUIDs or database-generated IDs.
            This is a simple implementation for in-memory storage.
        """
        return secrets.token_hex(16)  # 32 character hex string


def hash_password(password: str) -> str:
    """
    Hash a password securely using bcrypt.

    Args:
        password: Plain text password

    Returns:
        str: Bcrypt hashed password

    Raises:
        ValueError: If password is too weak

    Example:
        >>> hash_password("MySecurePassword123!")
        '$2b$12$...'
    """
    if not password:
        raise ValueError("Password is required")

    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters")

    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """
    Verify a password against its bcrypt hash.

    Args:
        password: Plain text password to verify
        password_hash: Stored bcrypt hash to compare against

    Returns:
        bool: True if password matches, False otherwise

    Example:
        >>> hashed = hash_password("MyPassword123!")
        >>> verify_password("MyPassword123!", hashed)
        True
        >>> verify_password("WrongPassword", hashed)
        False
    """
    if not password or not password_hash:
        return False

    try:
        return pwd_context.verify(password, password_hash)
    except Exception:
        return False


def create_user(username: str, email: str, password: str, **profile_data) -> User:
    """
    Factory function to create a new user with hashed password.

    Args:
        username: User's chosen username
        email: User's email address
        password: Plain text password (will be hashed)
        **profile_data: Additional profile information

    Returns:
        User: New user instance with hashed password

    Raises:
        ValueError: If username, email, or password is invalid

    Example:
        >>> user = create_user(
        ...     username="johndoe",
        ...     email="john@example.com",
        ...     password="SecurePassword123!",
        ...     display_name="John Doe",
        ...     bio="Software engineer"
        ... )
    """
    user_id = User.generate_id()
    password_hash = hash_password(password)

    return User(
        id=user_id,
        username=username,
        password_hash=password_hash,
        email=email,
        profile_data=profile_data or {},
    )
