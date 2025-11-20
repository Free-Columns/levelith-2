"""
User Management API Endpoints

Provides REST API for user CRUD operations and authentication.
"""

import random
from typing import List
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.db_models import UserDB, ExperienceDB
from backend.models.user import hash_password, verify_password
from backend.models.experience import ExperienceCategory, ExperienceType
from backend.schemas.user import UserCreate, UserResponse, UserUpdate, UserLogin, UserWithExperiences

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.

    Args:
        user_data: User creation data
        db: Database session

    Returns:
        Created user information

    Raises:
        HTTPException: If username or email already exists
    """
    # Check if username already exists
    existing_user = db.query(UserDB).filter(UserDB.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )

    # Check if email already exists
    existing_email = db.query(UserDB).filter(UserDB.email == user_data.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )

    # Hash password
    password_hash = hash_password(user_data.password)

    # Create user
    db_user = UserDB(
        username=user_data.username,
        email=user_data.email,
        password_hash=password_hash,
        profile_data=user_data.profile_data or {}
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Convert to response schema
    return UserResponse(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        is_active=db_user.is_active,
        is_verified=db_user.is_verified,
        profile_data=db_user.profile_data,
        created_at=db_user.created_at,
        updated_at=db_user.updated_at,
        last_login=db_user.last_login,
        experience_count=len(db_user.experiences)
    )


@router.get("/{user_id}", response_model=UserWithExperiences)
async def get_user(user_id: str, db: Session = Depends(get_db)):
    """
    Get user by ID.

    Args:
        user_id: User ID
        db: Database session

    Returns:
        User information with experiences

    Raises:
        HTTPException: If user not found
    """
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return UserWithExperiences(
        id=user.id,
        username=user.username,
        email=user.email,
        is_active=user.is_active,
        is_verified=user.is_verified,
        profile_data=user.profile_data,
        created_at=user.created_at,
        updated_at=user.updated_at,
        last_login=user.last_login,
        experience_count=len(user.experiences),
        experiences=[exp.id for exp in user.experiences]
    )


@router.get("/", response_model=List[UserResponse])
async def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    List all users with pagination.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session

    Returns:
        List of users
    """
    users = db.query(UserDB).offset(skip).limit(limit).all()

    return [
        UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            is_verified=user.is_verified,
            profile_data=user.profile_data,
            created_at=user.created_at,
            updated_at=user.updated_at,
            last_login=user.last_login,
            experience_count=len(user.experiences)
        )
        for user in users
    ]


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, user_data: UserUpdate, db: Session = Depends(get_db)):
    """
    Update user information.

    Args:
        user_id: User ID
        user_data: Updated user data
        db: Database session

    Returns:
        Updated user information

    Raises:
        HTTPException: If user not found
    """
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Update fields
    if user_data.email is not None:
        # Check if email is already taken
        existing = db.query(UserDB).filter(
            UserDB.email == user_data.email,
            UserDB.id != user_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists"
            )
        user.email = user_data.email

    if user_data.profile_data is not None:
        user.profile_data.update(user_data.profile_data)

    if user_data.is_active is not None:
        user.is_active = user_data.is_active

    db.commit()
    db.refresh(user)

    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        is_active=user.is_active,
        is_verified=user.is_verified,
        profile_data=user.profile_data,
        created_at=user.created_at,
        updated_at=user.updated_at,
        last_login=user.last_login,
        experience_count=len(user.experiences)
    )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str, db: Session = Depends(get_db)):
    """
    Delete a user.

    Args:
        user_id: User ID
        db: Database session

    Raises:
        HTTPException: If user not found
    """
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    db.delete(user)
    db.commit()


@router.post("/login")
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate user and return access token.

    Args:
        credentials: Login credentials
        db: Database session

    Returns:
        Authentication token information

    Raises:
        HTTPException: If credentials are invalid
    """
    # Find user by username
    user = db.query(UserDB).filter(UserDB.username == credentials.username).first()

    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    # TODO: Implement JWT token generation
    # For now, return basic user info
    return {
        "message": "Login successful",
        "user_id": user.id,
        "username": user.username,
        "note": "JWT token generation to be implemented"
    }


# ============================================================================
# SEED DATABASE ENDPOINT
# ============================================================================

# Mock data constants (from seed_db.py)
FIRST_NAMES = [
    "John", "Jane", "Michael", "Sarah", "David", "Emily", "Robert", "Jessica",
    "William", "Ashley", "James", "Amanda", "Christopher", "Melissa", "Daniel",
    "Jennifer", "Matthew", "Stephanie", "Andrew", "Nicole"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Thomas", "Taylor", "Moore", "Jackson", "Martin"
]

LOCATIONS = [
    "New York, NY", "Los Angeles, CA", "Chicago, IL", "Houston, TX", "Phoenix, AZ",
    "Philadelphia, PA", "San Antonio, TX", "San Diego, CA", "Dallas, TX", "San Jose, CA",
    "Austin, TX", "Seattle, WA", "Denver, CO", "Boston, MA", "Miami, FL"
]

BIOS = [
    "Software engineer passionate about building scalable applications",
    "Full-stack developer with expertise in modern web technologies",
    "Data scientist specializing in machine learning and AI",
    "UX designer focused on creating intuitive user experiences",
    "Product manager with a track record of successful launches"
]

CERT_TITLES = ["AWS Certified Solutions Architect", "Google Cloud Professional", "Certified Scrum Master"]
DEGREE_TITLES = ["Bachelor of Science in Computer Science", "Master of Business Administration", "Master of Science in Data Science"]
COURSE_TITLES = ["Advanced React Development", "Machine Learning Fundamentals", "Product Management Essentials"]
JOB_TITLES = ["Senior Software Engineer", "Product Manager", "UX Designer", "Data Scientist", "DevOps Engineer"]
COMPANIES = ["Tech Corp", "Innovation Labs", "Digital Solutions Inc", "Cloud Systems", "Data Dynamics"]
SKILLS = ["Python", "JavaScript", "React", "Node.js", "AWS", "Docker", "Kubernetes", "SQL", "MongoDB", "Git"]
NAICS_CODES = ["123456", "541511", "541512", "611310", "611420", "522110"]


def _generate_mock_user(index: int) -> dict:
    """Generate a single mock user."""
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    username = f"{first_name.lower()}{last_name.lower()}{index}{random.randint(100, 999)}"
    email = f"{first_name.lower()}.{last_name.lower()}{index}@example.com"

    created_days_ago = random.randint(1, 365)
    created_at = datetime.utcnow() - timedelta(days=created_days_ago)
    updated_at = datetime.utcnow() - timedelta(days=random.randint(1, 30))
    last_login = datetime.utcnow() - timedelta(days=random.randint(0, 7)) if random.random() > 0.2 else None

    return {
        "username": username,
        "email": email,
        "password": "TestPassword123!",
        "is_active": random.random() > 0.1,
        "is_verified": random.random() > 0.3,
        "profile_data": {
            "display_name": f"{first_name} {last_name}",
            "bio": random.choice(BIOS),
            "location": random.choice(LOCATIONS),
            "website": f"https://{username}.dev" if random.random() > 0.5 else None,
        },
        "created_at": created_at,
        "updated_at": updated_at,
        "last_login": last_login,
    }


def _generate_mock_experience(user_id: str, exp_type: ExperienceType) -> dict:
    """Generate a single mock experience for a user."""
    if exp_type in [ExperienceType.CERTIFICATE, ExperienceType.DEGREE, ExperienceType.COURSE]:
        category = ExperienceCategory.EDUCATION
    elif exp_type in [ExperienceType.GIG, ExperienceType.PART_TIME, ExperienceType.FULL_TIME]:
        category = ExperienceCategory.WORKPLACE
    else:
        category = ExperienceCategory.SKILLS

    # Generate type-specific data
    if exp_type == ExperienceType.CERTIFICATE:
        title = random.choice(CERT_TITLES)
        description = "Professional certification in specialized field"
        organization = "Certification Authority"
    elif exp_type == ExperienceType.DEGREE:
        title = random.choice(DEGREE_TITLES)
        description = "Academic degree program"
        organization = "University of Technology"
    elif exp_type == ExperienceType.COURSE:
        title = random.choice(COURSE_TITLES)
        description = "Professional development course"
        organization = "Online Learning Platform"
    elif exp_type in [ExperienceType.GIG, ExperienceType.PART_TIME, ExperienceType.FULL_TIME]:
        title = random.choice(JOB_TITLES)
        description = f"{exp_type.value.replace('_', '-')} position in technology sector"
        organization = random.choice(COMPANIES)
    else:
        skill_name = random.choice(SKILLS)
        title = skill_name
        description = f"Proficiency in {skill_name}"
        organization = None

    start_date = datetime.utcnow() - timedelta(days=random.randint(30, 1095))
    is_current = random.random() > 0.6
    end_date = None if is_current else start_date + timedelta(days=random.randint(30, 730))

    return {
        "user_id": user_id,
        "category": category,
        "experience_type": exp_type,
        "title": title,
        "description": description,
        "naics_code": random.choice(NAICS_CODES),
        "start_date": start_date,
        "end_date": end_date,
        "is_current": is_current,
        "organization": organization,
        "location": random.choice(LOCATIONS) if category != ExperienceCategory.SKILLS else None,
        "type_specific_data": {},
        "tags": random.sample(SKILLS, k=random.randint(2, 5)),
        "experience_metadata": {},
    }


@router.post("/seed", status_code=status.HTTP_201_CREATED)
async def seed_users(user_count: int = 50, db: Session = Depends(get_db)):
    """
    Seed the database with mock users and experiences.

    This endpoint creates the specified number of users, each with 2-8 random experiences.
    Used for testing and demo purposes in the admin dashboard.

    Args:
        user_count: Number of users to create (default: 50)
        db: Database session

    Returns:
        Statistics about the seeded data

    Raises:
        HTTPException: If seeding fails
    """
    try:
        created_users = 0
        created_experiences = 0

        # Generate and insert users with experiences
        for i in range(user_count):
            # Create user
            user_data = _generate_mock_user(i)

            user = UserDB(
                username=user_data["username"],
                email=user_data["email"],
                password_hash=hash_password(user_data["password"]),
                is_active=user_data["is_active"],
                is_verified=user_data["is_verified"],
                profile_data=user_data["profile_data"],
                created_at=user_data["created_at"],
                updated_at=user_data["updated_at"],
                last_login=user_data["last_login"],
            )

            db.add(user)
            db.flush()  # Get user.id

            # Create 2-8 random experiences for this user
            exp_count = random.randint(2, 8)
            experience_types = random.choices(list(ExperienceType), k=exp_count)

            for exp_type in experience_types:
                exp_data = _generate_mock_experience(user.id, exp_type)
                experience = ExperienceDB(**exp_data)
                db.add(experience)
                created_experiences += 1

            created_users += 1

        # Commit all changes
        db.commit()

        return {
            "success": True,
            "message": f"Successfully seeded {created_users} users with {created_experiences} experiences",
            "statistics": {
                "users_created": created_users,
                "experiences_created": created_experiences,
                "average_experiences_per_user": round(created_experiences / created_users, 1) if created_users > 0 else 0
            }
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to seed database: {str(e)}"
        )
