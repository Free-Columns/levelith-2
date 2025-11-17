"""
Tests for ExperienceRepository

This module contains comprehensive tests for the ExperienceRepository class,
ensuring all data access operations work correctly for all 9 experience types.

Test Coverage:
- Experience creation and storage (all 9 types)
- Experience retrieval (by ID, user, category, type, NAICS)
- Experience updates
- Experience deletion
- Index management (user, NAICS, category, type)
- Search functionality
- Edge cases and error handling
"""

import pytest
from datetime import datetime
from backend.repositories.experience_repository import ExperienceRepository
from backend.models.experience import (
    Experience,
    ExperienceCategory,
    ExperienceType,
    Certificate,
    Degree,
    Course,
    Gig,
    PartTime,
    FullTime,
    SoftSkill,
    HardSkill,
    NativeSkill,
)


class TestExperienceRepository:
    """Test suite for ExperienceRepository"""

    def setup_method(self):
        """Set up test fixtures before each test"""
        self.repo = ExperienceRepository()
        self.test_certificate = Certificate(
            id="exp_cert1",
            user_id="user123",
            title="AWS Certified Solutions Architect",
            description="Cloud architecture certification",
            naics_code="541511",
            start_date=datetime(2024, 1, 15),
        )

    def teardown_method(self):
        """Clean up after each test"""
        self.repo.clear()

    # ============================================================================
    # SAVE TESTS
    # ============================================================================

    def test_save_new_experience(self):
        """Test saving a new experience"""
        saved = self.repo.save(self.test_certificate)

        assert saved.id == "exp_cert1"
        assert saved.title == "AWS Certified Solutions Architect"
        assert self.repo.count() == 1

    def test_save_updates_existing_experience(self):
        """Test that save updates an existing experience"""
        self.repo.save(self.test_certificate)
        assert self.repo.count() == 1

        # Update and save again
        self.test_certificate.title = "Updated Title"
        updated = self.repo.save(self.test_certificate)

        assert updated.title == "Updated Title"
        assert self.repo.count() == 1  # Still only one experience

    def test_save_updates_all_indexes(self):
        """Test that save updates all indexes correctly"""
        saved = self.repo.save(self.test_certificate)

        # Verify in user index
        user_exps = self.repo.find_by_user("user123")
        assert len(user_exps) == 1

        # Verify in NAICS index
        naics_exps = self.repo.find_by_naics_code("541511")
        assert len(naics_exps) == 1

        # Verify in category index
        cat_exps = self.repo.find_by_category(ExperienceCategory.EDUCATION)
        assert len(cat_exps) == 1

        # Verify in type index
        type_exps = self.repo.find_by_type(ExperienceType.CERTIFICATE)
        assert len(type_exps) == 1

    def test_save_updates_timestamp(self):
        """Test that save updates the updated_at timestamp"""
        original_time = self.test_certificate.updated_at
        self.repo.save(self.test_certificate)

        # Save again
        import time
        time.sleep(0.01)
        updated = self.repo.save(self.test_certificate)

        assert updated.updated_at > original_time

    # ============================================================================
    # FIND BY ID TESTS
    # ============================================================================

    def test_find_by_id_existing_experience(self):
        """Test finding an existing experience by ID"""
        self.repo.save(self.test_certificate)

        found = self.repo.find_by_id("exp_cert1")
        assert found is not None
        assert found.id == "exp_cert1"
        assert found.title == "AWS Certified Solutions Architect"

    def test_find_by_id_nonexistent_experience(self):
        """Test finding a nonexistent experience returns None"""
        found = self.repo.find_by_id("nonexistent_id")
        assert found is None

    # ============================================================================
    # FIND BY USER TESTS
    # ============================================================================

    def test_find_by_user_single_experience(self):
        """Test finding experiences for a user with one experience"""
        self.repo.save(self.test_certificate)

        experiences = self.repo.find_by_user("user123")
        assert len(experiences) == 1
        assert experiences[0].id == "exp_cert1"

    def test_find_by_user_multiple_experiences(self):
        """Test finding multiple experiences for a user"""
        cert = self.test_certificate
        degree = Degree(
            id="exp_degree1",
            user_id="user123",
            title="BS Computer Science",
            description="Bachelor's degree",
            naics_code="611310",
            start_date=datetime(2020, 9, 1),
        )

        self.repo.save(cert)
        self.repo.save(degree)

        experiences = self.repo.find_by_user("user123")
        assert len(experiences) == 2

    def test_find_by_user_no_experiences(self):
        """Test finding experiences for user with no experiences"""
        experiences = self.repo.find_by_user("nonexistent_user")
        assert experiences == []

    def test_find_by_user_with_limit(self):
        """Test finding user experiences with limit"""
        for i in range(5):
            exp = Certificate(
                id=f"exp_{i}",
                user_id="user123",
                title=f"Cert {i}",
                description="Description",
                naics_code="541511",
                start_date=datetime.now(),
            )
            self.repo.save(exp)

        experiences = self.repo.find_by_user("user123", limit=3)
        assert len(experiences) == 3

    def test_find_by_user_with_offset(self):
        """Test finding user experiences with offset"""
        for i in range(5):
            exp = Certificate(
                id=f"exp_{i}",
                user_id="user123",
                title=f"Cert {i}",
                description="Description",
                naics_code="541511",
                start_date=datetime.now(),
            )
            self.repo.save(exp)

        experiences = self.repo.find_by_user("user123", offset=2)
        assert len(experiences) == 3  # 5 total - 2 skipped

    # ============================================================================
    # FIND BY NAICS TESTS
    # ============================================================================

    def test_find_by_naics_code(self):
        """Test finding experiences by NAICS code"""
        cert1 = self.test_certificate  # 541511
        cert2 = Certificate(
            id="exp_cert2",
            user_id="user456",
            title="Another AWS Cert",
            description="Description",
            naics_code="541511",  # Same NAICS
            start_date=datetime.now(),
        )

        self.repo.save(cert1)
        self.repo.save(cert2)

        experiences = self.repo.find_by_naics_code("541511")
        assert len(experiences) == 2

    def test_find_by_naics_code_no_matches(self):
        """Test finding experiences by NAICS with no matches"""
        self.repo.save(self.test_certificate)

        experiences = self.repo.find_by_naics_code("999999")
        assert experiences == []

    # ============================================================================
    # FIND BY CATEGORY TESTS
    # ============================================================================

    def test_find_by_category_education(self):
        """Test finding education experiences"""
        cert = self.test_certificate
        degree = Degree(
            id="exp_degree1",
            user_id="user123",
            title="BS CS",
            description="Degree",
            naics_code="611310",
            start_date=datetime.now(),
        )
        gig = Gig(
            id="exp_gig1",
            user_id="user123",
            title="Freelance Work",
            description="Gig",
            naics_code="541511",
            start_date=datetime.now(),
        )

        self.repo.save(cert)
        self.repo.save(degree)
        self.repo.save(gig)

        education = self.repo.find_by_category(ExperienceCategory.EDUCATION)
        assert len(education) == 2
        assert all(e.category == ExperienceCategory.EDUCATION for e in education)

    def test_find_by_category_workplace(self):
        """Test finding workplace experiences"""
        gig = Gig(
            id="exp_gig1",
            user_id="user123",
            title="Freelance",
            description="Gig work",
            naics_code="541511",
            start_date=datetime.now(),
        )
        fulltime = FullTime(
            id="exp_ft1",
            user_id="user123",
            title="Software Engineer",
            description="Full-time job",
            naics_code="541511",
            start_date=datetime.now(),
        )

        self.repo.save(gig)
        self.repo.save(fulltime)

        workplace = self.repo.find_by_category(ExperienceCategory.WORKPLACE)
        assert len(workplace) == 2
        assert all(e.category == ExperienceCategory.WORKPLACE for e in workplace)

    def test_find_by_category_skills(self):
        """Test finding skills experiences"""
        soft = SoftSkill(
            id="exp_soft1",
            user_id="user123",
            title="Leadership",
            description="Soft skill",
            naics_code="123456",
            start_date=datetime.now(),
        )
        hard = HardSkill(
            id="exp_hard1",
            user_id="user123",
            title="Python",
            description="Hard skill",
            naics_code="541511",
            start_date=datetime.now(),
        )

        self.repo.save(soft)
        self.repo.save(hard)

        skills = self.repo.find_by_category(ExperienceCategory.SKILLS)
        assert len(skills) == 2
        assert all(e.category == ExperienceCategory.SKILLS for e in skills)

    def test_find_by_category_with_pagination(self):
        """Test finding experiences by category with pagination"""
        for i in range(10):
            cert = Certificate(
                id=f"exp_{i}",
                user_id="user123",
                title=f"Cert {i}",
                description="Description",
                naics_code="541511",
                start_date=datetime.now(),
            )
            self.repo.save(cert)

        education = self.repo.find_by_category(ExperienceCategory.EDUCATION, limit=5, offset=3)
        assert len(education) == 5

    # ============================================================================
    # FIND BY TYPE TESTS
    # ============================================================================

    def test_find_by_type_certificate(self):
        """Test finding certificate experiences"""
        cert1 = self.test_certificate
        cert2 = Certificate(
            id="exp_cert2",
            user_id="user456",
            title="Another Cert",
            description="Description",
            naics_code="541511",
            start_date=datetime.now(),
        )
        degree = Degree(
            id="exp_degree1",
            user_id="user123",
            title="BS CS",
            description="Degree",
            naics_code="611310",
            start_date=datetime.now(),
        )

        self.repo.save(cert1)
        self.repo.save(cert2)
        self.repo.save(degree)

        certificates = self.repo.find_by_type(ExperienceType.CERTIFICATE)
        assert len(certificates) == 2
        assert all(e.experience_type == ExperienceType.CERTIFICATE for e in certificates)

    def test_find_by_type_full_time(self):
        """Test finding full-time experiences"""
        ft1 = FullTime(
            id="exp_ft1",
            user_id="user123",
            title="Software Engineer",
            description="Full-time job",
            naics_code="541511",
            start_date=datetime.now(),
        )
        ft2 = FullTime(
            id="exp_ft2",
            user_id="user456",
            title="Data Scientist",
            description="Full-time job",
            naics_code="541511",
            start_date=datetime.now(),
        )

        self.repo.save(ft1)
        self.repo.save(ft2)

        fulltime = self.repo.find_by_type(ExperienceType.FULL_TIME)
        assert len(fulltime) == 2
        assert all(e.experience_type == ExperienceType.FULL_TIME for e in fulltime)

    # ============================================================================
    # COMBINED FILTER TESTS
    # ============================================================================

    def test_find_by_user_and_category(self):
        """Test finding experiences by user and category"""
        cert = self.test_certificate
        degree = Degree(
            id="exp_degree1",
            user_id="user123",
            title="BS CS",
            description="Degree",
            naics_code="611310",
            start_date=datetime.now(),
        )
        gig = Gig(
            id="exp_gig1",
            user_id="user123",
            title="Freelance",
            description="Gig",
            naics_code="541511",
            start_date=datetime.now(),
        )

        self.repo.save(cert)
        self.repo.save(degree)
        self.repo.save(gig)

        education = self.repo.find_by_user_and_category("user123", ExperienceCategory.EDUCATION)
        assert len(education) == 2
        assert all(e.category == ExperienceCategory.EDUCATION for e in education)
        assert all(e.user_id == "user123" for e in education)

    def test_find_by_user_and_type(self):
        """Test finding experiences by user and type"""
        cert1 = self.test_certificate
        cert2 = Certificate(
            id="exp_cert2",
            user_id="user123",
            title="Another Cert",
            description="Description",
            naics_code="541511",
            start_date=datetime.now(),
        )
        degree = Degree(
            id="exp_degree1",
            user_id="user123",
            title="BS CS",
            description="Degree",
            naics_code="611310",
            start_date=datetime.now(),
        )

        self.repo.save(cert1)
        self.repo.save(cert2)
        self.repo.save(degree)

        certificates = self.repo.find_by_user_and_type("user123", ExperienceType.CERTIFICATE)
        assert len(certificates) == 2
        assert all(e.experience_type == ExperienceType.CERTIFICATE for e in certificates)

    # ============================================================================
    # ACTIVE EXPERIENCE TESTS
    # ============================================================================

    def test_find_active_all_users(self):
        """Test finding all active experiences"""
        active = Certificate(
            id="exp_active",
            user_id="user123",
            title="Active Cert",
            description="Description",
            naics_code="541511",
            start_date=datetime.now(),
            end_date=None,  # Active
        )
        completed = Certificate(
            id="exp_completed",
            user_id="user123",
            title="Completed Cert",
            description="Description",
            naics_code="541511",
            start_date=datetime(2020, 1, 1),
            end_date=datetime(2020, 12, 31),  # Completed
        )

        self.repo.save(active)
        self.repo.save(completed)

        active_exps = self.repo.find_active()
        assert len(active_exps) == 1
        assert active_exps[0].is_active() is True

    def test_find_active_for_user(self):
        """Test finding active experiences for specific user"""
        active1 = Certificate(
            id="exp_active1",
            user_id="user123",
            title="Active Cert",
            description="Description",
            naics_code="541511",
            start_date=datetime.now(),
            end_date=None,
        )
        active2 = Certificate(
            id="exp_active2",
            user_id="user456",
            title="Another Active",
            description="Description",
            naics_code="541511",
            start_date=datetime.now(),
            end_date=None,
        )

        self.repo.save(active1)
        self.repo.save(active2)

        user_active = self.repo.find_active(user_id="user123")
        assert len(user_active) == 1
        assert user_active[0].user_id == "user123"

    # ============================================================================
    # DELETE TESTS
    # ============================================================================

    def test_delete_existing_experience(self):
        """Test deleting an existing experience"""
        self.repo.save(self.test_certificate)
        assert self.repo.count() == 1

        success = self.repo.delete("exp_cert1")
        assert success is True
        assert self.repo.count() == 0

    def test_delete_removes_from_indexes(self):
        """Test that delete removes experience from all indexes"""
        self.repo.save(self.test_certificate)

        # Verify in indexes
        assert len(self.repo.find_by_user("user123")) == 1
        assert len(self.repo.find_by_naics_code("541511")) == 1
        assert len(self.repo.find_by_category(ExperienceCategory.EDUCATION)) == 1
        assert len(self.repo.find_by_type(ExperienceType.CERTIFICATE)) == 1

        # Delete
        self.repo.delete("exp_cert1")

        # Verify removed from all indexes
        assert len(self.repo.find_by_user("user123")) == 0
        assert len(self.repo.find_by_naics_code("541511")) == 0
        assert len(self.repo.find_by_category(ExperienceCategory.EDUCATION)) == 0
        assert len(self.repo.find_by_type(ExperienceType.CERTIFICATE)) == 0

    def test_delete_nonexistent_experience(self):
        """Test deleting a nonexistent experience returns False"""
        success = self.repo.delete("nonexistent_id")
        assert success is False

    # ============================================================================
    # COUNT TESTS
    # ============================================================================

    def test_count_empty_repo(self):
        """Test count on empty repository"""
        assert self.repo.count() == 0

    def test_count_all_experiences(self):
        """Test count of all experiences"""
        for i in range(5):
            cert = Certificate(
                id=f"exp_{i}",
                user_id="user123",
                title=f"Cert {i}",
                description="Description",
                naics_code="541511",
                start_date=datetime.now(),
            )
            self.repo.save(cert)

        assert self.repo.count() == 5

    def test_count_by_user(self):
        """Test count experiences for specific user"""
        cert1 = Certificate(
            id="exp_1",
            user_id="user123",
            title="Cert 1",
            description="Description",
            naics_code="541511",
            start_date=datetime.now(),
        )
        cert2 = Certificate(
            id="exp_2",
            user_id="user456",
            title="Cert 2",
            description="Description",
            naics_code="541511",
            start_date=datetime.now(),
        )

        self.repo.save(cert1)
        self.repo.save(cert2)

        assert self.repo.count(user_id="user123") == 1
        assert self.repo.count(user_id="user456") == 1

    def test_count_by_category(self):
        """Test count experiences by category"""
        cert = self.test_certificate
        gig = Gig(
            id="exp_gig1",
            user_id="user123",
            title="Gig",
            description="Description",
            naics_code="541511",
            start_date=datetime.now(),
        )

        self.repo.save(cert)
        self.repo.save(gig)

        assert self.repo.count_by_category(ExperienceCategory.EDUCATION) == 1
        assert self.repo.count_by_category(ExperienceCategory.WORKPLACE) == 1

    def test_count_by_type(self):
        """Test count experiences by type"""
        cert = self.test_certificate
        degree = Degree(
            id="exp_degree1",
            user_id="user123",
            title="Degree",
            description="Description",
            naics_code="611310",
            start_date=datetime.now(),
        )

        self.repo.save(cert)
        self.repo.save(degree)

        assert self.repo.count_by_type(ExperienceType.CERTIFICATE) == 1
        assert self.repo.count_by_type(ExperienceType.DEGREE) == 1

    # ============================================================================
    # SEARCH TESTS
    # ============================================================================

    def test_search_by_title(self):
        """Test searching experiences by title"""
        cert1 = Certificate(
            id="exp_1",
            user_id="user123",
            title="AWS Certified Developer",
            description="Description",
            naics_code="541511",
            start_date=datetime.now(),
        )
        cert2 = Certificate(
            id="exp_2",
            user_id="user123",
            title="Python Programming Course",
            description="Description",
            naics_code="541511",
            start_date=datetime.now(),
        )

        self.repo.save(cert1)
        self.repo.save(cert2)

        results = self.repo.search_by_title("AWS")
        assert len(results) == 1
        assert "AWS" in results[0].title

    def test_search_by_title_case_insensitive(self):
        """Test that title search is case-insensitive"""
        self.repo.save(self.test_certificate)

        results_lower = self.repo.search_by_title("aws")
        results_upper = self.repo.search_by_title("AWS")

        assert len(results_lower) == 1
        assert len(results_upper) == 1

    def test_search_by_title_for_user(self):
        """Test searching experiences by title for specific user"""
        cert1 = Certificate(
            id="exp_1",
            user_id="user123",
            title="AWS Certification",
            description="Description",
            naics_code="541511",
            start_date=datetime.now(),
        )
        cert2 = Certificate(
            id="exp_2",
            user_id="user456",
            title="AWS Training",
            description="Description",
            naics_code="541511",
            start_date=datetime.now(),
        )

        self.repo.save(cert1)
        self.repo.save(cert2)

        results = self.repo.search_by_title("AWS", user_id="user123")
        assert len(results) == 1
        assert results[0].user_id == "user123"

    def test_search_by_skill(self):
        """Test searching experiences by skill"""
        cert1 = Certificate(
            id="exp_1",
            user_id="user123",
            title="Web Development",
            description="Description",
            naics_code="541511",
            start_date=datetime.now(),
            skills_gained=["Python", "Django", "JavaScript"],
        )
        cert2 = Certificate(
            id="exp_2",
            user_id="user123",
            title="Data Science",
            description="Description",
            naics_code="541511",
            start_date=datetime.now(),
            skills_gained=["Python", "NumPy", "Pandas"],
        )

        self.repo.save(cert1)
        self.repo.save(cert2)

        results = self.repo.search_by_skill("Python")
        assert len(results) == 2

        results = self.repo.search_by_skill("Django")
        assert len(results) == 1

    def test_search_by_skill_case_insensitive(self):
        """Test that skill search is case-insensitive"""
        cert = Certificate(
            id="exp_1",
            user_id="user123",
            title="Programming",
            description="Description",
            naics_code="541511",
            start_date=datetime.now(),
            skills_gained=["Python", "JavaScript"],
        )
        self.repo.save(cert)

        results_lower = self.repo.search_by_skill("python")
        results_upper = self.repo.search_by_skill("PYTHON")

        assert len(results_lower) == 1
        assert len(results_upper) == 1

    # ============================================================================
    # CLEAR TESTS
    # ============================================================================

    def test_clear_empty_repo(self):
        """Test clearing an empty repository"""
        self.repo.clear()
        assert self.repo.count() == 0

    def test_clear_with_experiences(self):
        """Test clearing repository with experiences"""
        for i in range(5):
            cert = Certificate(
                id=f"exp_{i}",
                user_id="user123",
                title=f"Cert {i}",
                description="Description",
                naics_code="541511",
                start_date=datetime.now(),
            )
            self.repo.save(cert)

        assert self.repo.count() == 5

        self.repo.clear()
        assert self.repo.count() == 0
        assert self.repo.find_all() == []

    def test_clear_removes_all_indexes(self):
        """Test that clear removes all indexes"""
        self.repo.save(self.test_certificate)

        assert len(self.repo.find_by_user("user123")) == 1
        assert len(self.repo.find_by_naics_code("541511")) == 1

        self.repo.clear()

        assert len(self.repo.find_by_user("user123")) == 0
        assert len(self.repo.find_by_naics_code("541511")) == 0
