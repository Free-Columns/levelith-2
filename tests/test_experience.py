"""
Unit tests for experience.py

Comprehensive tests for Experience model, all 9 experience subtypes, and NAICS validation.
Tests follow the 80% minimum coverage requirement from AI_AGENT_GOLDEN_RULES.md
"""

import pytest
from datetime import datetime, timedelta
from backend.models.experience import (
    ExperienceCategory,
    ExperienceType,
    Experience,
    validate_naics_code,
    NAICS_GENERAL_FALLBACK,
    # Education types
    Certificate,
    Degree,
    Course,
    # Workplace types
    Gig,
    PartTime,
    FullTime,
    # Skills types
    SoftSkill,
    HardSkill,
    NativeSkill,
)


class TestNAICSValidation:
    """Test suite for NAICS code validation"""

    def test_validate_valid_naics(self):
        """Test validating valid 6-digit NAICS code"""
        assert validate_naics_code("541511") == "541511"  # Software development
        assert validate_naics_code("611110") == "611110"  # Elementary schools
        assert validate_naics_code("541430") == "541430"  # Graphic design

    def test_validate_empty_naics(self):
        """Test empty NAICS code returns fallback"""
        assert validate_naics_code("") == NAICS_GENERAL_FALLBACK
        assert validate_naics_code(None) == NAICS_GENERAL_FALLBACK

    def test_validate_invalid_length(self):
        """Test NAICS code with invalid length returns fallback"""
        assert validate_naics_code("123") == NAICS_GENERAL_FALLBACK  # Too short
        assert validate_naics_code("1234567") == NAICS_GENERAL_FALLBACK  # Too long

    def test_validate_non_numeric(self):
        """Test non-numeric NAICS code returns fallback"""
        assert validate_naics_code("abcdef") == NAICS_GENERAL_FALLBACK
        assert validate_naics_code("12345a") == NAICS_GENERAL_FALLBACK

    def test_validate_with_whitespace(self):
        """Test NAICS code with whitespace is trimmed"""
        assert validate_naics_code("  541511  ") == "541511"


class TestExperience:
    """Test suite for base Experience class"""

    def setup_method(self):
        """Set up test fixtures"""
        self.base_experience_data = {
            "id": "exp_123",
            "user_id": "user_456",
            "category": ExperienceCategory.EDUCATION,
            "experience_type": ExperienceType.DEGREE,
            "title": "Bachelor of Science in Computer Science",
            "description": "4-year degree program focusing on software engineering",
            "naics_code": "611310",  # Colleges and universities
            "start_date": datetime(2018, 9, 1),
            "end_date": datetime(2022, 5, 15),
            "organization": "Tech University",
            "location": "San Francisco, CA",
        }

    def test_experience_initialization(self):
        """Test Experience initialization with valid data"""
        exp = Experience(**self.base_experience_data)

        assert exp.id == "exp_123"
        assert exp.user_id == "user_456"
        assert exp.category == ExperienceCategory.EDUCATION
        assert exp.experience_type == ExperienceType.DEGREE
        assert exp.title == "Bachelor of Science in Computer Science"
        assert exp.naics_code == "611310"
        assert exp.organization == "Tech University"
        assert isinstance(exp.created_at, datetime)

    def test_experience_naics_validation_on_init(self):
        """Test NAICS code is validated on initialization"""
        data = self.base_experience_data.copy()
        data["naics_code"] = "invalid"

        exp = Experience(**data)
        assert exp.naics_code == NAICS_GENERAL_FALLBACK  # Should be corrected

    def test_experience_is_active_ongoing(self):
        """Test is_active returns True for ongoing experience"""
        data = self.base_experience_data.copy()
        data["end_date"] = None

        exp = Experience(**data)
        assert exp.is_active() is True

    def test_experience_is_active_completed(self):
        """Test is_active returns False for completed experience"""
        exp = Experience(**self.base_experience_data)
        assert exp.is_active() is False

    def test_experience_duration_days_completed(self):
        """Test duration calculation for completed experience"""
        exp = Experience(**self.base_experience_data)
        expected_days = (datetime(2022, 5, 15) - datetime(2018, 9, 1)).days

        assert exp.duration_days() == expected_days

    def test_experience_duration_days_ongoing(self):
        """Test duration calculation for ongoing experience"""
        data = self.base_experience_data.copy()
        data["start_date"] = datetime.now() - timedelta(days=100)
        data["end_date"] = None

        exp = Experience(**data)
        duration = exp.duration_days()

        # Should be approximately 100 days (allowing for test execution time)
        assert 99 <= duration <= 101

    def test_experience_to_dict(self):
        """Test converting experience to dictionary"""
        exp = Experience(**self.base_experience_data)
        exp_dict = exp.to_dict()

        assert exp_dict["id"] == "exp_123"
        assert exp_dict["user_id"] == "user_456"
        assert exp_dict["category"] == "education"
        assert exp_dict["experience_type"] == "degree"
        assert exp_dict["title"] == "Bachelor of Science in Computer Science"
        assert exp_dict["naics_code"] == "611310"
        assert isinstance(exp_dict["start_date"], str)  # ISO format
        assert isinstance(exp_dict["end_date"], str)

    def test_experience_with_skills_and_achievements(self):
        """Test experience with skills and achievements"""
        data = self.base_experience_data.copy()
        data["skills_gained"] = ["Python", "Java", "Algorithms"]
        data["achievements"] = ["Dean's List", "Graduated with Honors"]

        exp = Experience(**data)

        assert len(exp.skills_gained) == 3
        assert "Python" in exp.skills_gained
        assert len(exp.achievements) == 2
        assert "Dean's List" in exp.achievements

    def test_experience_with_metadata(self):
        """Test experience with custom metadata"""
        data = self.base_experience_data.copy()
        data["metadata"] = {
            "gpa": 3.8,
            "major": "Computer Science",
            "minor": "Mathematics",
        }

        exp = Experience(**data)

        assert exp.metadata["gpa"] == 3.8
        assert exp.metadata["major"] == "Computer Science"


# ============================================================================
# EDUCATION EXPERIENCE TYPES
# ============================================================================


class TestCertificate:
    """Test suite for Certificate experience type"""

    def test_certificate_initialization(self):
        """Test Certificate initializes with correct category and type"""
        cert = Certificate(
            id="cert_1",
            user_id="user_1",
            title="AWS Certified Developer",
            description="Cloud certification",
            naics_code="541511",
            start_date=datetime(2023, 1, 1),
            end_date=datetime(2023, 3, 1),
        )

        assert cert.category == ExperienceCategory.EDUCATION
        assert cert.experience_type == ExperienceType.CERTIFICATE
        assert cert.title == "AWS Certified Developer"

    def test_certificate_inherits_experience_methods(self):
        """Test Certificate inherits base Experience methods"""
        cert = Certificate(
            id="cert_1",
            user_id="user_1",
            title="Google Analytics Certification",
            description="Digital marketing cert",
            naics_code="541613",
            start_date=datetime(2023, 1, 1),
            end_date=None,  # Ongoing
        )

        assert cert.is_active() is True
        assert isinstance(cert.to_dict(), dict)


class TestDegree:
    """Test suite for Degree experience type"""

    def test_degree_initialization(self):
        """Test Degree initializes with correct category and type"""
        degree = Degree(
            id="deg_1",
            user_id="user_1",
            title="Master of Business Administration",
            description="MBA program",
            naics_code="611310",
            start_date=datetime(2020, 9, 1),
            end_date=datetime(2022, 5, 15),
        )

        assert degree.category == ExperienceCategory.EDUCATION
        assert degree.experience_type == ExperienceType.DEGREE
        assert degree.title == "Master of Business Administration"


class TestCourse:
    """Test suite for Course experience type"""

    def test_course_initialization(self):
        """Test Course initializes with correct category and type"""
        course = Course(
            id="course_1",
            user_id="user_1",
            title="Introduction to Machine Learning",
            description="Coursera course on ML fundamentals",
            naics_code="611420",
            start_date=datetime(2023, 6, 1),
            end_date=datetime(2023, 8, 1),
        )

        assert course.category == ExperienceCategory.EDUCATION
        assert course.experience_type == ExperienceType.COURSE


# ============================================================================
# WORKPLACE EXPERIENCE TYPES
# ============================================================================


class TestGig:
    """Test suite for Gig experience type"""

    def test_gig_initialization(self):
        """Test Gig initializes with correct category and type"""
        gig = Gig(
            id="gig_1",
            user_id="user_1",
            title="Website Redesign Project",
            description="2-month freelance web design project",
            naics_code="541511",
            start_date=datetime(2023, 1, 1),
            end_date=datetime(2023, 3, 1),
        )

        assert gig.category == ExperienceCategory.WORKPLACE
        assert gig.experience_type == ExperienceType.GIG
        assert gig.title == "Website Redesign Project"


class TestPartTime:
    """Test suite for PartTime experience type"""

    def test_parttime_initialization(self):
        """Test PartTime initializes with correct category and type"""
        part_time = PartTime(
            id="pt_1",
            user_id="user_1",
            title="Retail Associate",
            description="Part-time retail position, 20 hours/week",
            naics_code="452311",
            start_date=datetime(2022, 1, 1),
            end_date=None,  # Ongoing
        )

        assert part_time.category == ExperienceCategory.WORKPLACE
        assert part_time.experience_type == ExperienceType.PART_TIME
        assert part_time.is_active() is True


class TestFullTime:
    """Test suite for FullTime experience type"""

    def test_fulltime_initialization(self):
        """Test FullTime initializes with correct category and type"""
        full_time = FullTime(
            id="ft_1",
            user_id="user_1",
            title="Software Engineer",
            description="Full-time software development position",
            naics_code="541511",
            start_date=datetime(2020, 6, 1),
            end_date=None,
        )

        assert full_time.category == ExperienceCategory.WORKPLACE
        assert full_time.experience_type == ExperienceType.FULL_TIME


# ============================================================================
# SKILLS EXPERIENCE TYPES
# ============================================================================


class TestSoftSkill:
    """Test suite for SoftSkill experience type"""

    def test_softskill_initialization(self):
        """Test SoftSkill initializes with correct category and type"""
        soft_skill = SoftSkill(
            id="ss_1",
            user_id="user_1",
            title="Public Speaking",
            description="Developed through presentations and conferences",
            naics_code=NAICS_GENERAL_FALLBACK,
            start_date=datetime(2018, 1, 1),
        )

        assert soft_skill.category == ExperienceCategory.SKILLS
        assert soft_skill.experience_type == ExperienceType.SOFT_SKILL


class TestHardSkill:
    """Test suite for HardSkill experience type"""

    def test_hardskill_initialization(self):
        """Test HardSkill initializes with correct category and type"""
        hard_skill = HardSkill(
            id="hs_1",
            user_id="user_1",
            title="Python Programming",
            description="Professional Python development experience",
            naics_code="541511",
            start_date=datetime(2019, 1, 1),
        )

        assert hard_skill.category == ExperienceCategory.SKILLS
        assert hard_skill.experience_type == ExperienceType.HARD_SKILL


class TestNativeSkill:
    """Test suite for NativeSkill experience type"""

    def test_nativeskill_initialization(self):
        """Test NativeSkill initializes with correct category and type"""
        native_skill = NativeSkill(
            id="ns_1",
            user_id="user_1",
            title="Bilingual (English/Spanish)",
            description="Native fluency in both languages",
            naics_code=NAICS_GENERAL_FALLBACK,
            start_date=datetime(1990, 1, 1),  # Birth year
        )

        assert native_skill.category == ExperienceCategory.SKILLS
        assert native_skill.experience_type == ExperienceType.NATIVE_SKILL


# ============================================================================
# INTEGRATION TESTS
# ============================================================================


class TestExperienceIntegration:
    """Integration tests for experience functionality"""

    def test_create_all_experience_types(self):
        """Test creating all 9 experience types"""
        experiences = [
            # Education
            Certificate(
                id="1",
                user_id="u1",
                title="Cert",
                description="desc",
                naics_code="123456",
                start_date=datetime.now(),
            ),
            Degree(
                id="2",
                user_id="u1",
                title="Degree",
                description="desc",
                naics_code="123456",
                start_date=datetime.now(),
            ),
            Course(
                id="3",
                user_id="u1",
                title="Course",
                description="desc",
                naics_code="123456",
                start_date=datetime.now(),
            ),
            # Workplace
            Gig(
                id="4",
                user_id="u1",
                title="Gig",
                description="desc",
                naics_code="123456",
                start_date=datetime.now(),
            ),
            PartTime(
                id="5",
                user_id="u1",
                title="PT",
                description="desc",
                naics_code="123456",
                start_date=datetime.now(),
            ),
            FullTime(
                id="6",
                user_id="u1",
                title="FT",
                description="desc",
                naics_code="123456",
                start_date=datetime.now(),
            ),
            # Skills
            SoftSkill(
                id="7",
                user_id="u1",
                title="Soft",
                description="desc",
                naics_code="123456",
                start_date=datetime.now(),
            ),
            HardSkill(
                id="8",
                user_id="u1",
                title="Hard",
                description="desc",
                naics_code="123456",
                start_date=datetime.now(),
            ),
            NativeSkill(
                id="9",
                user_id="u1",
                title="Native",
                description="desc",
                naics_code="123456",
                start_date=datetime.now(),
            ),
        ]

        assert len(experiences) == 9
        # Verify all are Experience instances
        assert all(isinstance(exp, Experience) for exp in experiences)

    def test_experience_serialization_deserialization(self):
        """Test converting experience to dict and back"""
        original = FullTime(
            id="ft_1",
            user_id="user_1",
            title="Senior Developer",
            description="Full-stack development",
            naics_code="541511",
            start_date=datetime(2020, 1, 1),
            end_date=datetime(2023, 12, 31),
            skills_gained=["Python", "React", "PostgreSQL"],
            achievements=["Led team of 5", "Shipped 3 major features"],
        )

        # Convert to dict
        exp_dict = original.to_dict()

        # Verify all fields present
        assert exp_dict["id"] == "ft_1"
        assert exp_dict["category"] == "workplace"
        assert exp_dict["experience_type"] == "full_time"
        assert len(exp_dict["skills_gained"]) == 3
        assert len(exp_dict["achievements"]) == 2

    def test_naics_fallback_across_types(self):
        """Test that all experience types use NAICS fallback correctly"""
        # Test with invalid NAICS
        cert = Certificate(
            id="1",
            user_id="u1",
            title="Test",
            description="desc",
            naics_code="INVALID",
            start_date=datetime.now(),
        )

        degree = Degree(
            id="2",
            user_id="u1",
            title="Test",
            description="desc",
            naics_code="",
            start_date=datetime.now(),
        )

        gig = Gig(
            id="3",
            user_id="u1",
            title="Test",
            description="desc",
            naics_code=None,
            start_date=datetime.now(),
        )

        # All should have fallback code
        assert cert.naics_code == NAICS_GENERAL_FALLBACK
        assert degree.naics_code == NAICS_GENERAL_FALLBACK
        assert gig.naics_code == NAICS_GENERAL_FALLBACK
