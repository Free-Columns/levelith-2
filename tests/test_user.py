"""
Unit tests for user.py

Comprehensive tests for User model and authentication functions.
Tests follow the 80% minimum coverage requirement from AI_AGENT_GOLDEN_RULES.md
"""

import pytest
from datetime import datetime
from backend.models.user import User, hash_password, verify_password, create_user


class TestUser:
    """Test suite for user module"""

    def setup_method(self):
        """Set up test fixtures"""
        self.test_user_data = {
            "id": "test123",
            "username": "johndoe",
            "password_hash": "hashed_password_123",
            "email": "john@example.com",
        }

    def teardown_method(self):
        """Clean up after tests"""
        pass

    def test_user_initialization(self):
        """Test User initialization with valid data"""
        user = User(**self.test_user_data)

        assert user.id == "test123"
        assert user.username == "johndoe"
        assert user.email == "john@example.com"
        assert user.password_hash == "hashed_password_123"
        assert user.experiences == []
        assert user.is_active is True
        assert user.is_verified is False
        assert user.last_login is None
        assert isinstance(user.created_at, datetime)
        assert isinstance(user.updated_at, datetime)

    def test_user_username_validation_too_short(self):
        """Test username validation rejects short usernames"""
        with pytest.raises(ValueError, match="must be at least 3 characters"):
            User(
                id="test", username="ab", password_hash="hash", email="test@example.com"
            )

    def test_user_username_validation_too_long(self):
        """Test username validation rejects long usernames"""
        with pytest.raises(ValueError, match="must be at most 50 characters"):
            User(
                id="test",
                username="a" * 51,
                password_hash="hash",
                email="test@example.com",
            )

    def test_user_username_validation_invalid_characters(self):
        """Test username validation rejects invalid characters"""
        with pytest.raises(
            ValueError, match="must contain only alphanumeric characters"
        ):
            User(
                id="test",
                username="user@name",
                password_hash="hash",
                email="test@example.com",
            )

    def test_user_email_validation_missing_at(self):
        """Test email validation rejects email without @"""
        with pytest.raises(ValueError, match="Invalid email format"):
            User(
                id="test",
                username="testuser",
                password_hash="hash",
                email="invalidemail.com",
            )

    def test_user_email_validation_missing_domain(self):
        """Test email validation rejects email without domain"""
        with pytest.raises(ValueError, match="Invalid email format"):
            User(id="test", username="testuser", password_hash="hash", email="test@")

    def test_add_experience(self):
        """Test adding experience to user"""
        user = User(**self.test_user_data)
        user.add_experience("exp_123")

        assert "exp_123" in user.experiences
        assert len(user.experiences) == 1

    def test_add_duplicate_experience(self):
        """Test adding duplicate experience raises error"""
        user = User(**self.test_user_data)
        user.add_experience("exp_123")

        with pytest.raises(ValueError, match="Experience already exists"):
            user.add_experience("exp_123")

    def test_add_empty_experience(self):
        """Test adding empty experience ID raises error"""
        user = User(**self.test_user_data)

        with pytest.raises(ValueError, match="Experience ID is required"):
            user.add_experience("")

    def test_remove_experience(self):
        """Test removing experience from user"""
        user = User(**self.test_user_data)
        user.add_experience("exp_123")
        user.remove_experience("exp_123")

        assert "exp_123" not in user.experiences
        assert len(user.experiences) == 0

    def test_remove_nonexistent_experience(self):
        """Test removing nonexistent experience raises error"""
        user = User(**self.test_user_data)

        with pytest.raises(ValueError, match="Experience not found"):
            user.remove_experience("nonexistent")

    def test_update_last_login(self):
        """Test updating last login timestamp"""
        user = User(**self.test_user_data)
        assert user.last_login is None

        user.update_last_login()
        assert isinstance(user.last_login, datetime)
        assert user.last_login is not None

    def test_activate_user(self):
        """Test activating user account"""
        user = User(**self.test_user_data)
        user.deactivate()
        assert user.is_active is False

        user.activate()
        assert user.is_active is True

    def test_deactivate_user(self):
        """Test deactivating user account"""
        user = User(**self.test_user_data)
        assert user.is_active is True

        user.deactivate()
        assert user.is_active is False

    def test_verify_email(self):
        """Test verifying user email"""
        user = User(**self.test_user_data)
        assert user.is_verified is False

        user.verify_email()
        assert user.is_verified is True

    def test_update_profile(self):
        """Test updating user profile data"""
        user = User(**self.test_user_data)
        profile_data = {
            "display_name": "John Doe",
            "bio": "Software engineer",
            "avatar_url": "https://example.com/avatar.jpg",
        }

        user.update_profile(profile_data)

        assert user.profile_data["display_name"] == "John Doe"
        assert user.profile_data["bio"] == "Software engineer"
        assert user.profile_data["avatar_url"] == "https://example.com/avatar.jpg"

    def test_to_dict_without_sensitive(self):
        """Test converting user to dict excludes password by default"""
        user = User(**self.test_user_data)
        user_dict = user.to_dict()

        assert "password_hash" not in user_dict
        assert user_dict["id"] == "test123"
        assert user_dict["username"] == "johndoe"
        assert user_dict["email"] == "john@example.com"

    def test_to_dict_with_sensitive(self):
        """Test converting user to dict includes password when requested"""
        user = User(**self.test_user_data)
        user_dict = user.to_dict(include_sensitive=True)

        assert user_dict["password_hash"] == "hashed_password_123"

    def test_generate_id(self):
        """Test generating unique user ID"""
        id1 = User.generate_id()
        id2 = User.generate_id()

        assert isinstance(id1, str)
        assert isinstance(id2, str)
        assert len(id1) == 32  # 16 bytes = 32 hex characters
        assert id1 != id2  # Should be unique


class TestPasswordFunctions:
    """Test suite for password hashing and verification"""

    def test_hash_password(self):
        """Test hashing a password"""
        password = "MySecurePassword123!"
        hashed = hash_password(password)

        assert isinstance(hashed, str)
        assert "$" in hashed  # Contains salt separator
        assert len(hashed) > 50  # Reasonable hash length

    def test_hash_password_different_hashes(self):
        """Test same password produces different hashes (due to salt)"""
        password = "SamePassword123"
        hash1 = hash_password(password)
        hash2 = hash_password(password)

        assert hash1 != hash2  # Different salts

    def test_hash_password_empty(self):
        """Test hashing empty password raises error"""
        with pytest.raises(ValueError, match="Password is required"):
            hash_password("")

    def test_hash_password_too_short(self):
        """Test hashing short password raises error"""
        with pytest.raises(ValueError, match="must be at least 8 characters"):
            hash_password("short")

    def test_verify_password_correct(self):
        """Test verifying correct password"""
        password = "MySecurePassword123!"
        hashed = hash_password(password)

        assert verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        """Test verifying incorrect password"""
        password = "MySecurePassword123!"
        hashed = hash_password(password)

        assert verify_password("WrongPassword", hashed) is False

    def test_verify_password_empty_password(self):
        """Test verifying with empty password"""
        hashed = hash_password("ValidPassword123")

        assert verify_password("", hashed) is False

    def test_verify_password_empty_hash(self):
        """Test verifying with empty hash"""
        assert verify_password("password", "") is False

    def test_verify_password_invalid_hash_format(self):
        """Test verifying with invalid hash format"""
        assert verify_password("password", "invalid_hash") is False


class TestCreateUser:
    """Test suite for create_user factory function"""

    def test_create_user(self):
        """Test creating a user with factory function"""
        user = create_user(
            username="johndoe",
            email="john@example.com",
            password="SecurePassword123!",
        )

        assert isinstance(user, User)
        assert user.username == "johndoe"
        assert user.email == "john@example.com"
        assert user.password_hash != "SecurePassword123!"  # Should be hashed
        assert len(user.id) == 32  # Generated ID

    def test_create_user_with_profile_data(self):
        """Test creating user with profile data"""
        user = create_user(
            username="johndoe",
            email="john@example.com",
            password="SecurePassword123!",
            display_name="John Doe",
            bio="Software engineer",
        )

        assert user.profile_data["display_name"] == "John Doe"
        assert user.profile_data["bio"] == "Software engineer"

    def test_create_user_password_is_hashed(self):
        """Test that created user has hashed password"""
        password = "MyPassword123!"
        user = create_user(
            username="testuser", email="test@example.com", password=password
        )

        # Password should be hashed
        assert user.password_hash != password
        # But should verify correctly
        assert verify_password(password, user.password_hash) is True

    def test_create_user_invalid_username(self):
        """Test creating user with invalid username"""
        with pytest.raises(ValueError):
            create_user(
                username="ab", email="test@example.com", password="Password123!"
            )

    def test_create_user_invalid_email(self):
        """Test creating user with invalid email"""
        with pytest.raises(ValueError):
            create_user(username="testuser", email="invalid", password="Password123!")

    def test_create_user_weak_password(self):
        """Test creating user with weak password"""
        with pytest.raises(ValueError, match="must be at least 8 characters"):
            create_user(username="testuser", email="test@example.com", password="weak")


class TestUserEdgeCases:
    """Test edge cases and error scenarios"""

    def test_user_with_many_experiences(self):
        """Test user with many experiences"""
        user = create_user(
            username="testuser", email="test@example.com", password="Password123!"
        )

        # Add many experiences
        for i in range(100):
            user.add_experience(f"exp_{i}")

        assert len(user.experiences) == 100

    def test_user_profile_data_update_merge(self):
        """Test profile data updates merge with existing data"""
        user = create_user(
            username="testuser",
            email="test@example.com",
            password="Password123!",
            initial_field="value1",
        )

        user.update_profile({"new_field": "value2"})

        assert user.profile_data["initial_field"] == "value1"
        assert user.profile_data["new_field"] == "value2"

    def test_user_timestamps_update(self):
        """Test that updated_at changes when user is modified"""
        user = create_user(
            username="testuser", email="test@example.com", password="Password123!"
        )

        initial_updated_at = user.updated_at

        # Perform some updates
        user.add_experience("exp_1")
        assert user.updated_at > initial_updated_at
