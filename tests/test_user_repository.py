"""
Tests for UserRepository

This module contains comprehensive tests for the UserRepository class,
ensuring all data access operations work correctly.

Test Coverage:
- User creation and storage
- User retrieval (by ID, email, username)
- User updates
- User deletion
- Index management (email, username)
- Duplicate detection
- Search functionality
- Edge cases and error handling
"""

import pytest
from datetime import datetime
from backend.repositories.user_repository import UserRepository
from backend.models.user import User, create_user


class TestUserRepository:
    """Test suite for UserRepository"""

    def setup_method(self):
        """Set up test fixtures before each test"""
        self.repo = UserRepository()
        self.test_user = create_user(
            username="testuser",
            email="test@example.com",
            password="TestPassword123!",
            display_name="Test User",
            bio="Test bio",
        )

    def teardown_method(self):
        """Clean up after each test"""
        self.repo.clear()

    # ============================================================================
    # SAVE TESTS
    # ============================================================================

    def test_save_new_user(self):
        """Test saving a new user"""
        saved_user = self.repo.save(self.test_user)

        assert saved_user.id == self.test_user.id
        assert saved_user.username == "testuser"
        assert saved_user.email == "test@example.com"
        assert self.repo.count() == 1

    def test_save_updates_existing_user(self):
        """Test that save updates an existing user"""
        # Save user first time
        self.repo.save(self.test_user)
        assert self.repo.count() == 1

        # Update and save again
        self.test_user.username = "updateduser"
        updated_user = self.repo.save(self.test_user)

        assert updated_user.username == "updateduser"
        assert self.repo.count() == 1  # Still only one user

    def test_save_updates_email_index(self):
        """Test that email index is updated correctly"""
        self.repo.save(self.test_user)

        # Find by email should work
        found = self.repo.find_by_email("test@example.com")
        assert found is not None
        assert found.id == self.test_user.id

    def test_save_updates_username_index(self):
        """Test that username index is updated correctly"""
        self.repo.save(self.test_user)

        # Find by username should work
        found = self.repo.find_by_username("testuser")
        assert found is not None
        assert found.id == self.test_user.id

    def test_save_duplicate_email_different_user_raises_error(self):
        """Test that duplicate email for different user raises error"""
        self.repo.save(self.test_user)

        # Create different user with same email
        duplicate_user = create_user(
            username="differentuser",
            email="test@example.com",  # Same email
            password="Password123!",
        )

        with pytest.raises(ValueError, match="Email .* is already in use"):
            self.repo.save(duplicate_user)

    def test_save_duplicate_username_different_user_raises_error(self):
        """Test that duplicate username for different user raises error"""
        self.repo.save(self.test_user)

        # Create different user with same username
        duplicate_user = create_user(
            username="testuser",  # Same username
            email="different@example.com",
            password="Password123!",
        )

        with pytest.raises(ValueError, match="Username .* is already in use"):
            self.repo.save(duplicate_user)

    def test_save_updates_timestamp(self):
        """Test that save updates the updated_at timestamp"""
        original_time = self.test_user.updated_at
        self.repo.save(self.test_user)

        # Wait a tiny bit and save again
        import time

        time.sleep(0.01)
        updated_user = self.repo.save(self.test_user)

        assert updated_user.updated_at > original_time

    # ============================================================================
    # FIND TESTS
    # ============================================================================

    def test_find_by_id_existing_user(self):
        """Test finding an existing user by ID"""
        self.repo.save(self.test_user)

        found = self.repo.find_by_id(self.test_user.id)
        assert found is not None
        assert found.id == self.test_user.id
        assert found.username == "testuser"

    def test_find_by_id_nonexistent_user(self):
        """Test finding a nonexistent user returns None"""
        found = self.repo.find_by_id("nonexistent_id")
        assert found is None

    def test_find_by_email_existing_user(self):
        """Test finding an existing user by email"""
        self.repo.save(self.test_user)

        found = self.repo.find_by_email("test@example.com")
        assert found is not None
        assert found.email == "test@example.com"
        assert found.username == "testuser"

    def test_find_by_email_nonexistent_user(self):
        """Test finding a nonexistent email returns None"""
        found = self.repo.find_by_email("nonexistent@example.com")
        assert found is None

    def test_find_by_username_existing_user(self):
        """Test finding an existing user by username"""
        self.repo.save(self.test_user)

        found = self.repo.find_by_username("testuser")
        assert found is not None
        assert found.username == "testuser"
        assert found.email == "test@example.com"

    def test_find_by_username_nonexistent_user(self):
        """Test finding a nonexistent username returns None"""
        found = self.repo.find_by_username("nonexistent")
        assert found is None

    def test_find_all_empty_repo(self):
        """Test find_all on empty repository"""
        users = self.repo.find_all()
        assert users == []
        assert len(users) == 0

    def test_find_all_multiple_users(self):
        """Test find_all with multiple users"""
        user1 = self.test_user
        user2 = create_user(username="user2", email="user2@example.com", password="Pass123!")
        user3 = create_user(username="user3", email="user3@example.com", password="Pass123!")

        self.repo.save(user1)
        self.repo.save(user2)
        self.repo.save(user3)

        users = self.repo.find_all()
        assert len(users) == 3

    def test_find_all_with_limit(self):
        """Test find_all with limit parameter"""
        for i in range(5):
            user = create_user(
                username=f"user{i}", email=f"user{i}@example.com", password="Pass123!"
            )
            self.repo.save(user)

        users = self.repo.find_all(limit=3)
        assert len(users) == 3

    def test_find_all_with_offset(self):
        """Test find_all with offset parameter"""
        for i in range(5):
            user = create_user(
                username=f"user{i}", email=f"user{i}@example.com", password="Pass123!"
            )
            self.repo.save(user)

        users = self.repo.find_all(offset=2)
        assert len(users) == 3  # 5 total - 2 skipped = 3

    def test_find_all_with_limit_and_offset(self):
        """Test find_all with both limit and offset"""
        for i in range(10):
            user = create_user(
                username=f"user{i}", email=f"user{i}@example.com", password="Pass123!"
            )
            self.repo.save(user)

        users = self.repo.find_all(limit=3, offset=5)
        assert len(users) == 3  # Get 3 users starting from index 5

    def test_find_by_experience(self):
        """Test finding users by experience ID"""
        user1 = self.test_user
        user2 = create_user(username="user2", email="user2@example.com", password="Pass123!")

        # Add same experience to both users
        user1.add_experience("exp_123")
        user2.add_experience("exp_123")

        self.repo.save(user1)
        self.repo.save(user2)

        users = self.repo.find_by_experience("exp_123")
        assert len(users) == 2
        assert all("exp_123" in u.experiences for u in users)

    def test_find_by_experience_no_matches(self):
        """Test finding users by experience that doesn't exist"""
        self.repo.save(self.test_user)

        users = self.repo.find_by_experience("nonexistent_exp")
        assert users == []

    # ============================================================================
    # DELETE TESTS
    # ============================================================================

    def test_delete_existing_user(self):
        """Test deleting an existing user"""
        self.repo.save(self.test_user)
        assert self.repo.count() == 1

        success = self.repo.delete(self.test_user.id)
        assert success is True
        assert self.repo.count() == 0

    def test_delete_removes_from_indexes(self):
        """Test that delete removes user from all indexes"""
        self.repo.save(self.test_user)

        # Verify user is in indexes
        assert self.repo.find_by_email("test@example.com") is not None
        assert self.repo.find_by_username("testuser") is not None

        # Delete user
        self.repo.delete(self.test_user.id)

        # Verify user is removed from indexes
        assert self.repo.find_by_email("test@example.com") is None
        assert self.repo.find_by_username("testuser") is None

    def test_delete_nonexistent_user(self):
        """Test deleting a nonexistent user returns False"""
        success = self.repo.delete("nonexistent_id")
        assert success is False

    # ============================================================================
    # EXISTS TESTS
    # ============================================================================

    def test_exists_by_email_true(self):
        """Test exists_by_email returns True for existing email"""
        self.repo.save(self.test_user)
        assert self.repo.exists_by_email("test@example.com") is True

    def test_exists_by_email_false(self):
        """Test exists_by_email returns False for nonexistent email"""
        assert self.repo.exists_by_email("nonexistent@example.com") is False

    def test_exists_by_username_true(self):
        """Test exists_by_username returns True for existing username"""
        self.repo.save(self.test_user)
        assert self.repo.exists_by_username("testuser") is True

    def test_exists_by_username_false(self):
        """Test exists_by_username returns False for nonexistent username"""
        assert self.repo.exists_by_username("nonexistent") is False

    # ============================================================================
    # COUNT TESTS
    # ============================================================================

    def test_count_empty_repo(self):
        """Test count on empty repository"""
        assert self.repo.count() == 0

    def test_count_single_user(self):
        """Test count with one user"""
        self.repo.save(self.test_user)
        assert self.repo.count() == 1

    def test_count_multiple_users(self):
        """Test count with multiple users"""
        for i in range(5):
            user = create_user(
                username=f"user{i}", email=f"user{i}@example.com", password="Pass123!"
            )
            self.repo.save(user)

        assert self.repo.count() == 5

    # ============================================================================
    # FILTER TESTS
    # ============================================================================

    def test_find_active_users(self):
        """Test finding only active users"""
        user1 = self.test_user  # Active by default
        user2 = create_user(username="user2", email="user2@example.com", password="Pass123!")
        user2.deactivate()

        self.repo.save(user1)
        self.repo.save(user2)

        active_users = self.repo.find_active_users()
        assert len(active_users) == 1
        assert active_users[0].is_active is True

    def test_find_active_users_with_limit(self):
        """Test finding active users with limit"""
        for i in range(5):
            user = create_user(
                username=f"user{i}", email=f"user{i}@example.com", password="Pass123!"
            )
            self.repo.save(user)

        active_users = self.repo.find_active_users(limit=3)
        assert len(active_users) == 3

    def test_find_verified_users(self):
        """Test finding only verified users"""
        user1 = self.test_user
        user1.verify_email()
        user2 = create_user(username="user2", email="user2@example.com", password="Pass123!")
        # user2 is unverified

        self.repo.save(user1)
        self.repo.save(user2)

        verified_users = self.repo.find_verified_users()
        assert len(verified_users) == 1
        assert verified_users[0].is_verified is True

    def test_find_verified_users_with_limit(self):
        """Test finding verified users with limit"""
        for i in range(5):
            user = create_user(
                username=f"user{i}", email=f"user{i}@example.com", password="Pass123!"
            )
            user.verify_email()
            self.repo.save(user)

        verified_users = self.repo.find_verified_users(limit=3)
        assert len(verified_users) == 3

    # ============================================================================
    # SEARCH TESTS
    # ============================================================================

    def test_search_by_username_pattern(self):
        """Test searching users by username pattern"""
        user1 = create_user(username="johndoe", email="john@example.com", password="Pass123!")
        user2 = create_user(username="janedoe", email="jane@example.com", password="Pass123!")
        user3 = create_user(username="bobsmith", email="bob@example.com", password="Pass123!")

        self.repo.save(user1)
        self.repo.save(user2)
        self.repo.save(user3)

        # Search for "doe"
        results = self.repo.search_by_username_pattern("doe")
        assert len(results) == 2
        assert all("doe" in u.username.lower() for u in results)

    def test_search_by_username_pattern_case_insensitive(self):
        """Test that search is case-insensitive"""
        user = create_user(username="JohnDoe", email="john@example.com", password="Pass123!")
        self.repo.save(user)

        # Search with lowercase
        results = self.repo.search_by_username_pattern("john")
        assert len(results) == 1

        # Search with uppercase
        results = self.repo.search_by_username_pattern("JOHN")
        assert len(results) == 1

    def test_search_by_username_pattern_no_matches(self):
        """Test search with no matches"""
        self.repo.save(self.test_user)

        results = self.repo.search_by_username_pattern("nonexistent")
        assert results == []

    # ============================================================================
    # CLEAR TESTS
    # ============================================================================

    def test_clear_empty_repo(self):
        """Test clearing an empty repository"""
        self.repo.clear()
        assert self.repo.count() == 0

    def test_clear_with_users(self):
        """Test clearing repository with users"""
        for i in range(5):
            user = create_user(
                username=f"user{i}", email=f"user{i}@example.com", password="Pass123!"
            )
            self.repo.save(user)

        assert self.repo.count() == 5

        self.repo.clear()
        assert self.repo.count() == 0
        assert self.repo.find_all() == []

    def test_clear_removes_indexes(self):
        """Test that clear removes all indexes"""
        self.repo.save(self.test_user)

        assert self.repo.exists_by_email("test@example.com") is True
        assert self.repo.exists_by_username("testuser") is True

        self.repo.clear()

        assert self.repo.exists_by_email("test@example.com") is False
        assert self.repo.exists_by_username("testuser") is False
