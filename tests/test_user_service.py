"""
Tests for User Service

This module tests the User service business logic layer.

Test coverage includes:
- User registration and authentication
- Profile management
- Password operations
- User lifecycle (activate, deactivate, verify)
- Experience management for users
- User search and listing
"""

import pytest
from unittest.mock import Mock, MagicMock
from datetime import datetime

from backend.services.user_service import UserService
from backend.repositories.user_repository import UserRepository
from backend.models.user import User, create_user, hash_password


@pytest.fixture
def mock_repo():
    """Create a mock user repository."""
    return Mock(spec=UserRepository)


@pytest.fixture
def user_service(mock_repo):
    """Create a user service with mock repository."""
    return UserService(user_repo=mock_repo)


@pytest.fixture
def sample_user():
    """Create a sample user for testing."""
    return create_user(
        username="johndoe",
        email="john@example.com",
        password="SecurePassword123!",
        display_name="John Doe",
        bio="Software engineer"
    )


@pytest.fixture
def sample_user_2():
    """Create a second sample user for testing."""
    return create_user(
        username="janedoe",
        email="jane@example.com",
        password="AnotherSecure456!",
        display_name="Jane Doe",
        bio="Product manager"
    )


class TestUserServiceInitialization:
    """Test UserService initialization."""

    def test_service_initializes(self, mock_repo):
        """Test service initializes with repository."""
        service = UserService(user_repo=mock_repo)
        assert service is not None
        assert service.user_repo == mock_repo


class TestUserRegistration:
    """Test user registration operations."""

    def test_register_user_success(self, user_service, mock_repo):
        """Test successful user registration."""
        # Arrange
        mock_repo.exists_by_username.return_value = False
        mock_repo.exists_by_email.return_value = False
        mock_repo.save.return_value = create_user(
            username="newuser",
            email="new@example.com",
            password="Password123!"
        )

        # Act
        user = user_service.register_user(
            username="newuser",
            email="new@example.com",
            password="Password123!",
            display_name="New User"
        )

        # Assert
        assert user is not None
        assert user.username == "newuser"
        mock_repo.exists_by_username.assert_called_once_with("newuser")
        mock_repo.exists_by_email.assert_called_once_with("new@example.com")
        mock_repo.save.assert_called_once()

    def test_register_user_duplicate_username(self, user_service, mock_repo):
        """Test registration fails with duplicate username."""
        # Arrange
        mock_repo.exists_by_username.return_value = True

        # Act & Assert
        with pytest.raises(ValueError, match="Username 'existinguser' is already taken"):
            user_service.register_user(
                username="existinguser",
                email="new@example.com",
                password="Password123!"
            )

        mock_repo.exists_by_username.assert_called_once_with("existinguser")
        mock_repo.save.assert_not_called()

    def test_register_user_duplicate_email(self, user_service, mock_repo):
        """Test registration fails with duplicate email."""
        # Arrange
        mock_repo.exists_by_username.return_value = False
        mock_repo.exists_by_email.return_value = True

        # Act & Assert
        with pytest.raises(ValueError, match="Email 'existing@example.com' is already registered"):
            user_service.register_user(
                username="newuser",
                email="existing@example.com",
                password="Password123!"
            )

        mock_repo.exists_by_email.assert_called_once_with("existing@example.com")
        mock_repo.save.assert_not_called()

    def test_register_user_with_profile_data(self, user_service, mock_repo):
        """Test registration with additional profile data."""
        # Arrange
        mock_repo.exists_by_username.return_value = False
        mock_repo.exists_by_email.return_value = False

        def save_side_effect(user):
            return user
        mock_repo.save.side_effect = save_side_effect

        # Act
        user = user_service.register_user(
            username="profileuser",
            email="profile@example.com",
            password="Password123!",
            display_name="Profile User",
            bio="Test bio",
            location="San Francisco, CA"
        )

        # Assert
        assert user is not None
        assert user.username == "profileuser"
        mock_repo.save.assert_called_once()


class TestUserAuthentication:
    """Test user authentication operations."""

    def test_authenticate_user_success(self, user_service, mock_repo, sample_user):
        """Test successful authentication."""
        # Arrange
        sample_user.is_active = True
        mock_repo.find_by_email.return_value = sample_user
        mock_repo.save.return_value = sample_user

        # Act
        authenticated_user = user_service.authenticate_user(
            "john@example.com",
            "SecurePassword123!"
        )

        # Assert
        assert authenticated_user is not None
        assert authenticated_user.email == "john@example.com"
        mock_repo.find_by_email.assert_called_once_with("john@example.com")
        mock_repo.save.assert_called_once()  # For updating last_login

    def test_authenticate_user_wrong_password(self, user_service, mock_repo, sample_user):
        """Test authentication fails with wrong password."""
        # Arrange
        sample_user.is_active = True
        mock_repo.find_by_email.return_value = sample_user

        # Act
        authenticated_user = user_service.authenticate_user(
            "john@example.com",
            "WrongPassword123!"
        )

        # Assert
        assert authenticated_user is None
        mock_repo.find_by_email.assert_called_once_with("john@example.com")
        mock_repo.save.assert_not_called()

    def test_authenticate_user_not_found(self, user_service, mock_repo):
        """Test authentication fails when user not found."""
        # Arrange
        mock_repo.find_by_email.return_value = None

        # Act
        authenticated_user = user_service.authenticate_user(
            "nonexistent@example.com",
            "Password123!"
        )

        # Assert
        assert authenticated_user is None
        mock_repo.find_by_email.assert_called_once_with("nonexistent@example.com")

    def test_authenticate_inactive_user(self, user_service, mock_repo, sample_user):
        """Test authentication fails for inactive user."""
        # Arrange
        sample_user.is_active = False
        mock_repo.find_by_email.return_value = sample_user

        # Act
        authenticated_user = user_service.authenticate_user(
            "john@example.com",
            "SecurePassword123!"
        )

        # Assert
        assert authenticated_user is None
        mock_repo.find_by_email.assert_called_once_with("john@example.com")
        mock_repo.save.assert_not_called()


class TestUserRetrieval:
    """Test user retrieval operations."""

    def test_get_user_by_id_found(self, user_service, mock_repo, sample_user):
        """Test retrieving user by ID when found."""
        # Arrange
        mock_repo.find_by_id.return_value = sample_user

        # Act
        user = user_service.get_user_by_id("user123")

        # Assert
        assert user is not None
        assert user.username == "johndoe"
        mock_repo.find_by_id.assert_called_once_with("user123")

    def test_get_user_by_id_not_found(self, user_service, mock_repo):
        """Test retrieving user by ID when not found."""
        # Arrange
        mock_repo.find_by_id.return_value = None

        # Act
        user = user_service.get_user_by_id("nonexistent")

        # Assert
        assert user is None
        mock_repo.find_by_id.assert_called_once_with("nonexistent")

    def test_get_user_by_email_found(self, user_service, mock_repo, sample_user):
        """Test retrieving user by email when found."""
        # Arrange
        mock_repo.find_by_email.return_value = sample_user

        # Act
        user = user_service.get_user_by_email("john@example.com")

        # Assert
        assert user is not None
        assert user.email == "john@example.com"
        mock_repo.find_by_email.assert_called_once_with("john@example.com")

    def test_get_user_by_email_not_found(self, user_service, mock_repo):
        """Test retrieving user by email when not found."""
        # Arrange
        mock_repo.find_by_email.return_value = None

        # Act
        user = user_service.get_user_by_email("nonexistent@example.com")

        # Assert
        assert user is None
        mock_repo.find_by_email.assert_called_once_with("nonexistent@example.com")

    def test_get_user_by_username_found(self, user_service, mock_repo, sample_user):
        """Test retrieving user by username when found."""
        # Arrange
        mock_repo.find_by_username.return_value = sample_user

        # Act
        user = user_service.get_user_by_username("johndoe")

        # Assert
        assert user is not None
        assert user.username == "johndoe"
        mock_repo.find_by_username.assert_called_once_with("johndoe")

    def test_get_user_by_username_not_found(self, user_service, mock_repo):
        """Test retrieving user by username when not found."""
        # Arrange
        mock_repo.find_by_username.return_value = None

        # Act
        user = user_service.get_user_by_username("nonexistent")

        # Assert
        assert user is None
        mock_repo.find_by_username.assert_called_once_with("nonexistent")


class TestProfileManagement:
    """Test profile management operations."""

    def test_update_profile_success(self, user_service, mock_repo, sample_user):
        """Test successful profile update."""
        # Arrange
        mock_repo.find_by_id.return_value = sample_user
        mock_repo.save.return_value = sample_user

        profile_data = {
            "display_name": "John Doe Updated",
            "bio": "Senior software engineer",
            "location": "San Francisco, CA"
        }

        # Act
        updated_user = user_service.update_profile("user123", profile_data)

        # Assert
        assert updated_user is not None
        mock_repo.find_by_id.assert_called_once_with("user123")
        mock_repo.save.assert_called_once()

    def test_update_profile_user_not_found(self, user_service, mock_repo):
        """Test profile update fails when user not found."""
        # Arrange
        mock_repo.find_by_id.return_value = None

        # Act & Assert
        with pytest.raises(ValueError, match="User with ID 'nonexistent' not found"):
            user_service.update_profile("nonexistent", {"bio": "New bio"})

        mock_repo.find_by_id.assert_called_once_with("nonexistent")
        mock_repo.save.assert_not_called()


class TestPasswordManagement:
    """Test password management operations."""

    def test_change_password_success(self, user_service, mock_repo, sample_user):
        """Test successful password change."""
        # Arrange
        mock_repo.find_by_id.return_value = sample_user
        mock_repo.save.return_value = sample_user

        # Act
        result = user_service.change_password(
            "user123",
            "SecurePassword123!",
            "NewSecurePass456!"
        )

        # Assert
        assert result is True
        mock_repo.find_by_id.assert_called_once_with("user123")
        mock_repo.save.assert_called_once()

    def test_change_password_wrong_old_password(self, user_service, mock_repo, sample_user):
        """Test password change fails with wrong old password."""
        # Arrange
        mock_repo.find_by_id.return_value = sample_user

        # Act & Assert
        with pytest.raises(ValueError, match="Current password is incorrect"):
            user_service.change_password(
                "user123",
                "WrongOldPassword!",
                "NewSecurePass456!"
            )

        mock_repo.find_by_id.assert_called_once_with("user123")
        mock_repo.save.assert_not_called()

    def test_change_password_user_not_found(self, user_service, mock_repo):
        """Test password change fails when user not found."""
        # Arrange
        mock_repo.find_by_id.return_value = None

        # Act & Assert
        with pytest.raises(ValueError, match="User with ID 'nonexistent' not found"):
            user_service.change_password(
                "nonexistent",
                "OldPassword123!",
                "NewPassword456!"
            )

        mock_repo.find_by_id.assert_called_once_with("nonexistent")
        mock_repo.save.assert_not_called()


class TestUserLifecycle:
    """Test user lifecycle operations (activate, deactivate, verify)."""

    def test_activate_user_success(self, user_service, mock_repo, sample_user):
        """Test successful user activation."""
        # Arrange
        sample_user.is_active = False
        mock_repo.find_by_id.return_value = sample_user
        mock_repo.save.return_value = sample_user

        # Act
        activated_user = user_service.activate_user("user123")

        # Assert
        assert activated_user is not None
        mock_repo.find_by_id.assert_called_once_with("user123")
        mock_repo.save.assert_called_once()

    def test_activate_user_not_found(self, user_service, mock_repo):
        """Test activation fails when user not found."""
        # Arrange
        mock_repo.find_by_id.return_value = None

        # Act & Assert
        with pytest.raises(ValueError, match="User with ID 'nonexistent' not found"):
            user_service.activate_user("nonexistent")

        mock_repo.find_by_id.assert_called_once_with("nonexistent")
        mock_repo.save.assert_not_called()

    def test_deactivate_user_success(self, user_service, mock_repo, sample_user):
        """Test successful user deactivation."""
        # Arrange
        sample_user.is_active = True
        mock_repo.find_by_id.return_value = sample_user
        mock_repo.save.return_value = sample_user

        # Act
        deactivated_user = user_service.deactivate_user("user123")

        # Assert
        assert deactivated_user is not None
        mock_repo.find_by_id.assert_called_once_with("user123")
        mock_repo.save.assert_called_once()

    def test_deactivate_user_not_found(self, user_service, mock_repo):
        """Test deactivation fails when user not found."""
        # Arrange
        mock_repo.find_by_id.return_value = None

        # Act & Assert
        with pytest.raises(ValueError, match="User with ID 'nonexistent' not found"):
            user_service.deactivate_user("nonexistent")

        mock_repo.find_by_id.assert_called_once_with("nonexistent")
        mock_repo.save.assert_not_called()

    def test_verify_user_email_success(self, user_service, mock_repo, sample_user):
        """Test successful email verification."""
        # Arrange
        sample_user.is_verified = False
        mock_repo.find_by_id.return_value = sample_user
        mock_repo.save.return_value = sample_user

        # Act
        verified_user = user_service.verify_user_email("user123")

        # Assert
        assert verified_user is not None
        mock_repo.find_by_id.assert_called_once_with("user123")
        mock_repo.save.assert_called_once()

    def test_verify_user_email_not_found(self, user_service, mock_repo):
        """Test verification fails when user not found."""
        # Arrange
        mock_repo.find_by_id.return_value = None

        # Act & Assert
        with pytest.raises(ValueError, match="User with ID 'nonexistent' not found"):
            user_service.verify_user_email("nonexistent")

        mock_repo.find_by_id.assert_called_once_with("nonexistent")
        mock_repo.save.assert_not_called()


class TestUserDeletion:
    """Test user deletion operations."""

    def test_delete_user_success(self, user_service, mock_repo):
        """Test successful user deletion."""
        # Arrange
        mock_repo.delete.return_value = True

        # Act
        result = user_service.delete_user("user123")

        # Assert
        assert result is True
        mock_repo.delete.assert_called_once_with("user123")

    def test_delete_user_not_found(self, user_service, mock_repo):
        """Test deletion returns False when user not found."""
        # Arrange
        mock_repo.delete.return_value = False

        # Act
        result = user_service.delete_user("nonexistent")

        # Assert
        assert result is False
        mock_repo.delete.assert_called_once_with("nonexistent")


class TestUserListing:
    """Test user listing and search operations."""

    def test_list_all_users(self, user_service, mock_repo, sample_user, sample_user_2):
        """Test listing all users."""
        # Arrange
        mock_repo.find_all.return_value = [sample_user, sample_user_2]

        # Act
        users = user_service.list_users()

        # Assert
        assert len(users) == 2
        assert users[0].username == "johndoe"
        assert users[1].username == "janedoe"
        mock_repo.find_all.assert_called_once_with(limit=None, offset=0)

    def test_list_active_users_only(self, user_service, mock_repo, sample_user):
        """Test listing only active users."""
        # Arrange
        sample_user.is_active = True
        mock_repo.find_active_users.return_value = [sample_user]

        # Act
        users = user_service.list_users(active_only=True)

        # Assert
        assert len(users) == 1
        assert users[0].is_active is True
        mock_repo.find_active_users.assert_called_once()

    def test_list_verified_users_only(self, user_service, mock_repo, sample_user):
        """Test listing only verified users."""
        # Arrange
        sample_user.is_verified = True
        mock_repo.find_verified_users.return_value = [sample_user]

        # Act
        users = user_service.list_users(verified_only=True)

        # Assert
        assert len(users) == 1
        assert users[0].is_verified is True
        mock_repo.find_verified_users.assert_called_once()

    def test_list_users_with_pagination(self, user_service, mock_repo, sample_user):
        """Test listing users with pagination."""
        # Arrange
        mock_repo.find_all.return_value = [sample_user]

        # Act
        users = user_service.list_users(limit=10, offset=20)

        # Assert
        assert len(users) == 1
        mock_repo.find_all.assert_called_once_with(limit=10, offset=20)

    def test_search_users(self, user_service, mock_repo, sample_user):
        """Test searching users by username pattern."""
        # Arrange
        mock_repo.search_by_username_pattern.return_value = [sample_user]

        # Act
        users = user_service.search_users("john")

        # Assert
        assert len(users) == 1
        assert users[0].username == "johndoe"
        mock_repo.search_by_username_pattern.assert_called_once_with("john")

    def test_get_user_count(self, user_service, mock_repo):
        """Test getting total user count."""
        # Arrange
        mock_repo.count.return_value = 42

        # Act
        count = user_service.get_user_count()

        # Assert
        assert count == 42
        mock_repo.count.assert_called_once()


class TestExperienceManagement:
    """Test experience management for users."""

    def test_add_experience_to_user_success(self, user_service, mock_repo, sample_user):
        """Test adding experience to user."""
        # Arrange
        mock_repo.find_by_id.return_value = sample_user
        mock_repo.save.return_value = sample_user

        # Act
        updated_user = user_service.add_experience_to_user("user123", "exp456")

        # Assert
        assert updated_user is not None
        mock_repo.find_by_id.assert_called_once_with("user123")
        mock_repo.save.assert_called_once()

    def test_add_experience_user_not_found(self, user_service, mock_repo):
        """Test adding experience fails when user not found."""
        # Arrange
        mock_repo.find_by_id.return_value = None

        # Act & Assert
        with pytest.raises(ValueError, match="User with ID 'nonexistent' not found"):
            user_service.add_experience_to_user("nonexistent", "exp456")

        mock_repo.find_by_id.assert_called_once_with("nonexistent")
        mock_repo.save.assert_not_called()

    def test_remove_experience_from_user_success(self, user_service, mock_repo, sample_user):
        """Test removing experience from user."""
        # Arrange
        sample_user.experiences = ["exp123", "exp456"]
        mock_repo.find_by_id.return_value = sample_user
        mock_repo.save.return_value = sample_user

        # Act
        updated_user = user_service.remove_experience_from_user("user123", "exp456")

        # Assert
        assert updated_user is not None
        mock_repo.find_by_id.assert_called_once_with("user123")
        mock_repo.save.assert_called_once()

    def test_remove_experience_user_not_found(self, user_service, mock_repo):
        """Test removing experience fails when user not found."""
        # Arrange
        mock_repo.find_by_id.return_value = None

        # Act & Assert
        with pytest.raises(ValueError, match="User with ID 'nonexistent' not found"):
            user_service.remove_experience_from_user("nonexistent", "exp456")

        mock_repo.find_by_id.assert_called_once_with("nonexistent")
        mock_repo.save.assert_not_called()

    def test_get_user_experiences_success(self, user_service, mock_repo, sample_user):
        """Test getting user experiences."""
        # Arrange
        sample_user.experiences = ["exp123", "exp456", "exp789"]
        mock_repo.find_by_id.return_value = sample_user

        # Act
        experiences = user_service.get_user_experiences("user123")

        # Assert
        assert len(experiences) == 3
        assert "exp123" in experiences
        assert "exp456" in experiences
        assert "exp789" in experiences
        mock_repo.find_by_id.assert_called_once_with("user123")

    def test_get_user_experiences_user_not_found(self, user_service, mock_repo):
        """Test getting experiences fails when user not found."""
        # Arrange
        mock_repo.find_by_id.return_value = None

        # Act & Assert
        with pytest.raises(ValueError, match="User with ID 'nonexistent' not found"):
            user_service.get_user_experiences("nonexistent")

        mock_repo.find_by_id.assert_called_once_with("nonexistent")
