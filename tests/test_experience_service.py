"""
Tests for Experience Service

This module tests the Experience service business logic layer.

Test coverage includes:
- Creation of all 9 experience types (Certificate, Degree, Course, Gig, PartTime,
  FullTime, SoftSkill, HardSkill, NativeSkill)
- Experience retrieval and querying
- NAICS code validation and fallback
- Experience updates and deletion
- Search and filtering operations
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime, timedelta

from backend.services.experience_service import ExperienceService
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


@pytest.fixture
def mock_repo():
    """Create a mock experience repository."""
    return Mock(spec=ExperienceRepository)


@pytest.fixture
def experience_service(mock_repo):
    """Create an experience service with mock repository."""
    return ExperienceService(experience_repo=mock_repo)


@pytest.fixture
def sample_certificate():
    """Create a sample certificate experience."""
    return Certificate(
        id="exp_cert123",
        user_id="user123",
        title="AWS Certified Solutions Architect",
        description="Professional cloud architecture certification",
        naics_code="541511",
        start_date=datetime(2023, 1, 1),
        end_date=datetime(2023, 3, 1),
        organization="Amazon Web Services",
        location=None,
        skills_gained=["Cloud Architecture", "AWS Services"],
        achievements=["Passed with 850/1000"],
        metadata={"certification_number": "AWS-12345"}
    )


@pytest.fixture
def sample_degree():
    """Create a sample degree experience."""
    return Degree(
        id="exp_deg123",
        user_id="user123",
        title="Bachelor of Science in Computer Science",
        description="Four-year undergraduate degree program",
        naics_code="611310",
        start_date=datetime(2018, 9, 1),
        end_date=datetime(2022, 6, 1),
        organization="Tech University",
        location="San Francisco, CA",
        skills_gained=["Programming", "Algorithms", "Data Structures"],
        achievements=["Graduated with Honors", "GPA: 3.8"],
        metadata={"degree_level": "Bachelor's", "major": "Computer Science"}
    )


@pytest.fixture
def sample_fulltime():
    """Create a sample full-time job experience."""
    return FullTime(
        id="exp_ft123",
        user_id="user123",
        title="Senior Software Engineer",
        description="Led development of microservices architecture",
        naics_code="541511",
        start_date=datetime(2022, 7, 1),
        end_date=None,  # Current job
        organization="Tech Corp",
        location="San Francisco, CA",
        skills_gained=["Python", "FastAPI", "PostgreSQL", "Docker"],
        achievements=["Led team of 5 engineers", "Reduced API latency by 40%"],
        metadata={"salary_range": "$150k-$200k", "team_size": 5}
    )


class TestExperienceServiceInitialization:
    """Test ExperienceService initialization."""

    def test_service_initializes(self, mock_repo):
        """Test service initializes with repository."""
        service = ExperienceService(experience_repo=mock_repo)
        assert service is not None
        assert service.experience_repo == mock_repo


class TestExperienceIDGeneration:
    """Test experience ID generation."""

    def test_generate_experience_id_format(self, experience_service):
        """Test that generated IDs have correct format."""
        exp_id = experience_service._generate_experience_id()
        assert exp_id.startswith("exp_")
        assert len(exp_id) == 28  # "exp_" (4) + 24 hex chars

    def test_generate_unique_ids(self, experience_service):
        """Test that generated IDs are unique."""
        id1 = experience_service._generate_experience_id()
        id2 = experience_service._generate_experience_id()
        id3 = experience_service._generate_experience_id()

        assert id1 != id2
        assert id2 != id3
        assert id1 != id3


class TestEducationExperienceCreation:
    """Test creation of education-type experiences."""

    def test_create_certificate_success(self, experience_service, mock_repo):
        """Test successful certificate creation."""
        # Arrange
        def save_side_effect(exp):
            return exp
        mock_repo.save.side_effect = save_side_effect

        # Act
        cert = experience_service.create_certificate(
            user_id="user123",
            title="Google Cloud Professional",
            description="Cloud certification",
            naics_code="541511",
            start_date=datetime(2023, 1, 1),
            end_date=datetime(2023, 3, 1),
            organization="Google",
            issuing_organization="Google Cloud",
            credential_id="GCP-123",
            credential_url="https://google.com/cert/123"
        )

        # Assert
        assert cert is not None
        assert cert.title == "Google Cloud Professional"
        assert cert.experience_type == ExperienceType.CERTIFICATE
        assert cert.category == ExperienceCategory.EDUCATION
        assert cert.naics_code == "541511"
        mock_repo.save.assert_called_once()

    def test_create_degree_success(self, experience_service, mock_repo):
        """Test successful degree creation."""
        # Arrange
        def save_side_effect(exp):
            return exp
        mock_repo.save.side_effect = save_side_effect

        # Act
        degree = experience_service.create_degree(
            user_id="user123",
            title="Master of Science",
            description="Graduate degree in CS",
            naics_code="611310",
            start_date=datetime(2020, 9, 1),
            end_date=datetime(2022, 6, 1),
            organization="Tech University",
            location="Boston, MA",
            institution="MIT",
            degree_level="Master's",
            field_of_study="Computer Science"
        )

        # Assert
        assert degree is not None
        assert degree.experience_type == ExperienceType.DEGREE
        assert degree.category == ExperienceCategory.EDUCATION
        mock_repo.save.assert_called_once()

    def test_create_course_success(self, experience_service, mock_repo):
        """Test successful course creation."""
        # Arrange
        def save_side_effect(exp):
            return exp
        mock_repo.save.side_effect = save_side_effect

        # Act
        course = experience_service.create_course(
            user_id="user123",
            title="Advanced React",
            description="Learn advanced React patterns",
            naics_code="611420",
            start_date=datetime(2023, 1, 1),
            end_date=datetime(2023, 2, 1),
            organization="Online Academy",
            provider="Udemy",
            course_code="REACT-301",
            completion_status="Completed"
        )

        # Assert
        assert course is not None
        assert course.experience_type == ExperienceType.COURSE
        assert course.category == ExperienceCategory.EDUCATION
        mock_repo.save.assert_called_once()


class TestWorkplaceExperienceCreation:
    """Test creation of workplace-type experiences."""

    def test_create_gig_success(self, experience_service, mock_repo):
        """Test successful gig creation."""
        # Arrange
        def save_side_effect(exp):
            return exp
        mock_repo.save.side_effect = save_side_effect

        # Act
        gig = experience_service.create_gig(
            user_id="user123",
            title="Freelance Web Developer",
            description="Built e-commerce website",
            naics_code="541511",
            start_date=datetime(2023, 1, 1),
            end_date=datetime(2023, 3, 1),
            organization="Client Corp",
            location="Remote",
            contract_type="Freelance",
            hourly_rate=150.00,
            total_hours=120
        )

        # Assert
        assert gig is not None
        assert gig.experience_type == ExperienceType.GIG
        assert gig.category == ExperienceCategory.WORKPLACE
        mock_repo.save.assert_called_once()

    def test_create_part_time_success(self, experience_service, mock_repo):
        """Test successful part-time job creation."""
        # Arrange
        def save_side_effect(exp):
            return exp
        mock_repo.save.side_effect = save_side_effect

        # Act
        part_time = experience_service.create_part_time(
            user_id="user123",
            title="Part-Time Developer",
            description="Mobile app development",
            naics_code="541511",
            start_date=datetime(2023, 1, 1),
            organization="Startup Inc",
            location="San Francisco, CA",
            hours_per_week=20,
            employment_type="Part-time",
            job_title="Junior Developer"
        )

        # Assert
        assert part_time is not None
        assert part_time.experience_type == ExperienceType.PART_TIME
        assert part_time.category == ExperienceCategory.WORKPLACE
        mock_repo.save.assert_called_once()

    def test_create_full_time_success(self, experience_service, mock_repo):
        """Test successful full-time job creation."""
        # Arrange
        def save_side_effect(exp):
            return exp
        mock_repo.save.side_effect = save_side_effect

        # Act
        full_time = experience_service.create_full_time(
            user_id="user123",
            title="Senior Software Engineer",
            description="Backend development",
            naics_code="541511",
            start_date=datetime(2022, 1, 1),
            organization="Big Tech Corp",
            location="Seattle, WA",
            employment_type="Full-time",
            job_level="Senior",
            department="Engineering"
        )

        # Assert
        assert full_time is not None
        assert full_time.experience_type == ExperienceType.FULL_TIME
        assert full_time.category == ExperienceCategory.WORKPLACE
        assert full_time.end_date is None  # Ongoing by default
        mock_repo.save.assert_called_once()


class TestSkillsExperienceCreation:
    """Test creation of skills-type experiences."""

    def test_create_soft_skill_success(self, experience_service, mock_repo):
        """Test successful soft skill creation."""
        # Arrange
        def save_side_effect(exp):
            return exp
        mock_repo.save.side_effect = save_side_effect

        # Act
        soft_skill = experience_service.create_soft_skill(
            user_id="user123",
            title="Leadership",
            description="Team leadership and management",
            naics_code="123456",  # GENERAL fallback
            start_date=datetime(2020, 1, 1),
            skill_name="Leadership",
            proficiency_level="Advanced",
            years_of_experience=5
        )

        # Assert
        assert soft_skill is not None
        assert soft_skill.experience_type == ExperienceType.SOFT_SKILL
        assert soft_skill.category == ExperienceCategory.SKILLS
        mock_repo.save.assert_called_once()

    def test_create_hard_skill_success(self, experience_service, mock_repo):
        """Test successful hard skill creation."""
        # Arrange
        def save_side_effect(exp):
            return exp
        mock_repo.save.side_effect = save_side_effect

        # Act
        hard_skill = experience_service.create_hard_skill(
            user_id="user123",
            title="Python Programming",
            description="Advanced Python development",
            naics_code="541511",
            start_date=datetime(2018, 1, 1),
            skill_name="Python",
            proficiency_level="Expert",
            certifications=["Python Institute PCEP", "PCAP"]
        )

        # Assert
        assert hard_skill is not None
        assert hard_skill.experience_type == ExperienceType.HARD_SKILL
        assert hard_skill.category == ExperienceCategory.SKILLS
        mock_repo.save.assert_called_once()

    def test_create_native_skill_success(self, experience_service, mock_repo):
        """Test successful native skill creation."""
        # Arrange
        def save_side_effect(exp):
            return exp
        mock_repo.save.side_effect = save_side_effect

        # Act
        native_skill = experience_service.create_native_skill(
            user_id="user123",
            title="Spanish Language",
            description="Native fluency in Spanish",
            naics_code="123456",
            start_date=datetime(1990, 1, 1),  # Birth year
            skill_name="Spanish",
            proficiency_level="Native",
            is_mother_tongue=True
        )

        # Assert
        assert native_skill is not None
        assert native_skill.experience_type == ExperienceType.NATIVE_SKILL
        assert native_skill.category == ExperienceCategory.SKILLS
        mock_repo.save.assert_called_once()


class TestNAICSValidation:
    """Test NAICS code validation and fallback logic."""

    @patch('backend.services.experience_service.validate_naics_code')
    def test_create_with_invalid_naics_uses_fallback(
        self, mock_validate, experience_service, mock_repo
    ):
        """Test that invalid NAICS codes use fallback."""
        # Arrange
        mock_validate.return_value = False
        def save_side_effect(exp):
            return exp
        mock_repo.save.side_effect = save_side_effect

        # Act
        cert = experience_service.create_certificate(
            user_id="user123",
            title="Test Cert",
            description="Test",
            naics_code="999999",  # Invalid code
            start_date=datetime.now()
        )

        # Assert
        assert cert.naics_code == "123456"  # Fallback code
        mock_repo.save.assert_called_once()


class TestExperienceRetrieval:
    """Test experience retrieval operations."""

    def test_get_experience_by_id_found(
        self, experience_service, mock_repo, sample_certificate
    ):
        """Test retrieving experience by ID when found."""
        # Arrange
        mock_repo.find_by_id.return_value = sample_certificate

        # Act
        exp = experience_service.get_experience_by_id("exp_cert123")

        # Assert
        assert exp is not None
        assert exp.id == "exp_cert123"
        assert exp.title == "AWS Certified Solutions Architect"
        mock_repo.find_by_id.assert_called_once_with("exp_cert123")

    def test_get_experience_by_id_not_found(self, experience_service, mock_repo):
        """Test retrieving experience by ID when not found."""
        # Arrange
        mock_repo.find_by_id.return_value = None

        # Act
        exp = experience_service.get_experience_by_id("nonexistent")

        # Assert
        assert exp is None
        mock_repo.find_by_id.assert_called_once_with("nonexistent")

    def test_get_user_experiences_all(
        self, experience_service, mock_repo, sample_certificate, sample_degree
    ):
        """Test retrieving all experiences for a user."""
        # Arrange
        mock_repo.find_by_user_id.return_value = [sample_certificate, sample_degree]

        # Act
        experiences = experience_service.get_user_experiences("user123")

        # Assert
        assert len(experiences) == 2
        assert experiences[0].id == "exp_cert123"
        assert experiences[1].id == "exp_deg123"
        mock_repo.find_by_user_id.assert_called_once_with("user123")

    def test_get_user_experiences_by_category(
        self, experience_service, mock_repo, sample_certificate, sample_degree
    ):
        """Test retrieving experiences filtered by category."""
        # Arrange
        education_experiences = [sample_certificate, sample_degree]
        mock_repo.find_by_user_id_and_category.return_value = education_experiences

        # Act
        experiences = experience_service.get_user_experiences(
            "user123",
            category=ExperienceCategory.EDUCATION
        )

        # Assert
        assert len(experiences) == 2
        mock_repo.find_by_user_id_and_category.assert_called_once_with(
            "user123",
            ExperienceCategory.EDUCATION
        )

    def test_get_user_experiences_by_type(
        self, experience_service, mock_repo, sample_certificate
    ):
        """Test retrieving experiences filtered by type."""
        # Arrange
        mock_repo.find_by_user_id_and_type.return_value = [sample_certificate]

        # Act
        experiences = experience_service.get_user_experiences(
            "user123",
            experience_type=ExperienceType.CERTIFICATE
        )

        # Assert
        assert len(experiences) == 1
        assert experiences[0].experience_type == ExperienceType.CERTIFICATE
        mock_repo.find_by_user_id_and_type.assert_called_once_with(
            "user123",
            ExperienceType.CERTIFICATE
        )

    def test_get_experiences_by_naics(
        self, experience_service, mock_repo, sample_certificate
    ):
        """Test retrieving experiences by NAICS code."""
        # Arrange
        mock_repo.find_by_naics_code.return_value = [sample_certificate]

        # Act
        experiences = experience_service.get_experiences_by_naics("541511")

        # Assert
        assert len(experiences) == 1
        assert experiences[0].naics_code == "541511"
        mock_repo.find_by_naics_code.assert_called_once_with("541511")


class TestExperienceSearch:
    """Test experience search operations."""

    def test_search_experiences_by_title(
        self, experience_service, mock_repo, sample_certificate
    ):
        """Test searching experiences by title."""
        # Arrange
        mock_repo.search.return_value = [sample_certificate]

        # Act
        results = experience_service.search_experiences("AWS Certified")

        # Assert
        assert len(results) == 1
        assert "AWS Certified" in results[0].title
        mock_repo.search.assert_called_once_with("AWS Certified")

    def test_search_experiences_empty_query(self, experience_service, mock_repo):
        """Test searching with empty query returns empty list."""
        # Arrange
        mock_repo.search.return_value = []

        # Act
        results = experience_service.search_experiences("")

        # Assert
        assert len(results) == 0


class TestExperienceUpdate:
    """Test experience update operations."""

    def test_update_experience_success(
        self, experience_service, mock_repo, sample_certificate
    ):
        """Test successful experience update."""
        # Arrange
        mock_repo.find_by_id.return_value = sample_certificate
        mock_repo.save.return_value = sample_certificate

        update_data = {
            "title": "AWS Certified Solutions Architect - Updated",
            "description": "Updated description",
            "organization": "Amazon Web Services"
        }

        # Act
        updated_exp = experience_service.update_experience("exp_cert123", update_data)

        # Assert
        assert updated_exp is not None
        mock_repo.find_by_id.assert_called_once_with("exp_cert123")
        mock_repo.save.assert_called_once()

    def test_update_experience_not_found(self, experience_service, mock_repo):
        """Test update fails when experience not found."""
        # Arrange
        mock_repo.find_by_id.return_value = None

        # Act & Assert
        with pytest.raises(ValueError, match="Experience with ID 'nonexistent' not found"):
            experience_service.update_experience("nonexistent", {"title": "New Title"})

        mock_repo.find_by_id.assert_called_once_with("nonexistent")
        mock_repo.save.assert_not_called()


class TestExperienceDeletion:
    """Test experience deletion operations."""

    def test_delete_experience_success(self, experience_service, mock_repo):
        """Test successful experience deletion."""
        # Arrange
        mock_repo.delete.return_value = True

        # Act
        result = experience_service.delete_experience("exp_cert123")

        # Assert
        assert result is True
        mock_repo.delete.assert_called_once_with("exp_cert123")

    def test_delete_experience_not_found(self, experience_service, mock_repo):
        """Test deletion returns False when not found."""
        # Arrange
        mock_repo.delete.return_value = False

        # Act
        result = experience_service.delete_experience("nonexistent")

        # Assert
        assert result is False
        mock_repo.delete.assert_called_once_with("nonexistent")


class TestExperienceCount:
    """Test experience counting operations."""

    def test_get_experience_count(self, experience_service, mock_repo):
        """Test getting total experience count."""
        # Arrange
        mock_repo.count.return_value = 150

        # Act
        count = experience_service.get_experience_count()

        # Assert
        assert count == 150
        mock_repo.count.assert_called_once()

    def test_get_experience_count_by_user(self, experience_service, mock_repo):
        """Test getting experience count for specific user."""
        # Arrange
        mock_repo.count_by_user.return_value = 12

        # Act
        count = experience_service.get_experience_count(user_id="user123")

        # Assert
        assert count == 12
        mock_repo.count_by_user.assert_called_once_with("user123")

    def test_get_experience_count_by_category(self, experience_service, mock_repo):
        """Test getting experience count by category."""
        # Arrange
        mock_repo.count_by_category.return_value = 50

        # Act
        count = experience_service.get_experience_count(
            category=ExperienceCategory.EDUCATION
        )

        # Assert
        assert count == 50
        mock_repo.count_by_category.assert_called_once_with(
            ExperienceCategory.EDUCATION
        )
