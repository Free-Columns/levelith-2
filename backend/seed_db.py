#!/usr/bin/env python3
"""
Database Seeding Script

Populates the PostgreSQL database with realistic mock data for testing.
Generates users and experiences matching the admin dashboard mock data structure.

Usage:
    python backend/seed_db.py              # Seed with default data (25 users)
    python backend/seed_db.py --users 50   # Seed with 50 users
    python backend/seed_db.py --clear      # Clear all data first
    python backend/seed_db.py --verbose    # Show detailed logging
"""

import sys
import random
import argparse
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Add backend directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.config import settings
from backend.database import get_db_context, init_db, DatabaseHealthCheck
from backend.models.db_models import UserDB, ExperienceDB
from backend.models.experience import ExperienceCategory, ExperienceType
from passlib.context import CryptContext

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# MOCK DATA GENERATORS (matching admin dashboard mockData.js)
# ============================================================================

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
    "Product manager with a track record of successful launches",
    "DevOps engineer automating infrastructure at scale",
    "Mobile developer building iOS and Android applications",
    "Technical writer creating clear documentation",
    "Quality assurance engineer ensuring software reliability",
    "Database administrator optimizing performance"
]

# Experience data
CERT_TITLES = [
    "AWS Certified Solutions Architect",
    "Google Cloud Professional",
    "Certified Scrum Master",
    "PMP Certification",
    "Certified Kubernetes Administrator"
]

DEGREE_TITLES = [
    "Bachelor of Science in Computer Science",
    "Master of Business Administration",
    "Bachelor of Arts in Design",
    "Master of Science in Data Science",
    "Bachelor of Engineering"
]

COURSE_TITLES = [
    "Advanced React Development",
    "Machine Learning Fundamentals",
    "Product Management Essentials",
    "UI/UX Design Bootcamp",
    "Cloud Architecture Workshop"
]

JOB_TITLES = [
    "Senior Software Engineer",
    "Product Manager",
    "UX Designer",
    "Data Scientist",
    "DevOps Engineer",
    "Frontend Developer",
    "Backend Developer",
    "Mobile Developer",
    "QA Engineer",
    "Technical Writer"
]

COMPANIES = [
    "Tech Corp", "Innovation Labs", "Digital Solutions Inc", "Cloud Systems",
    "Data Dynamics", "WebDev Pro", "Mobile First", "AI Ventures",
    "Startup Hub", "Enterprise Systems"
]

SKILLS = [
    "Python", "JavaScript", "React", "Node.js", "AWS", "Docker",
    "Kubernetes", "SQL", "MongoDB", "Git", "CI/CD", "Agile",
    "Scrum", "Leadership", "Communication", "Problem Solving"
]

# NAICS codes (subset from admin dashboard)
NAICS_CODES = [
    "123456",  # GENERAL
    "541511",  # Custom Computer Programming Services
    "541512",  # Computer Systems Design Services
    "611310",  # Colleges, Universities, and Professional Schools
    "611420",  # Computer Training
    "522110",  # Commercial Banking
    "445110",  # Supermarkets and Other Grocery Stores
    "722511",  # Full-Service Restaurants
]


def generate_mock_user(index: int) -> Dict[str, Any]:
    """Generate a single mock user."""
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    username = f"{first_name.lower()}{last_name.lower()}{index}"
    email = f"{first_name.lower()}.{last_name.lower()}{index}@example.com"

    # Random dates
    created_days_ago = random.randint(1, 365)
    created_at = datetime.utcnow() - timedelta(days=created_days_ago)
    updated_at = datetime.utcnow() - timedelta(days=random.randint(1, 30))
    last_login = datetime.utcnow() - timedelta(days=random.randint(0, 7)) if random.random() > 0.2 else None

    return {
        "username": username,
        "email": email,
        "password": "TestPassword123!",  # Will be hashed
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


def generate_mock_experience(user_id: str, exp_type: ExperienceType) -> Dict[str, Any]:
    """Generate a single mock experience for a user."""

    # Determine category from type
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
    else:  # Skills
        skill_name = random.choice(SKILLS)
        title = skill_name
        description = f"Proficiency in {skill_name}"
        organization = None

    # Generate dates
    start_date = datetime.utcnow() - timedelta(days=random.randint(30, 1095))
    is_current = random.random() > 0.6
    end_date = None if is_current else start_date + timedelta(days=random.randint(30, 730))

    # Type-specific data
    type_specific_data = {}
    if exp_type == ExperienceType.CERTIFICATE:
        type_specific_data["credential_id"] = f"CERT-{random.randint(10000, 99999)}"
    elif exp_type == ExperienceType.DEGREE:
        type_specific_data["major"] = "Computer Science"
        type_specific_data["level"] = random.choice(["Bachelor", "Master", "Doctorate"])
    elif exp_type == ExperienceType.HARD_SKILL:
        type_specific_data["proficiency_level"] = random.choice(["Beginner", "Intermediate", "Advanced", "Expert"])
        type_specific_data["years_experience"] = random.randint(1, 10)

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
        "type_specific_data": type_specific_data,
        "tags": random.sample(SKILLS, k=random.randint(2, 5)),
        "experience_metadata": {},
    }


def seed_database(user_count: int = 25, clear_first: bool = False, verbose: bool = False):
    """
    Seed the database with mock data.

    Args:
        user_count: Number of users to create
        clear_first: If True, clear all existing data first
        verbose: If True, show detailed logging
    """
    if verbose:
        logger.setLevel(logging.DEBUG)

    logger.info("=" * 70)
    logger.info("DATABASE SEEDING SCRIPT")
    logger.info("=" * 70)

    # Check database connection
    logger.info("Checking database connection...")
    if not DatabaseHealthCheck.check():
        logger.error("❌ Database connection failed!")
        logger.error("Please check your DATABASE_URL and ensure database is running.")
        sys.exit(1)

    logger.info("✅ Database connection successful")

    # Initialize database (create tables if needed)
    logger.info("Initializing database tables...")
    init_db()
    logger.info("✅ Database tables ready")

    with get_db_context() as db:
        # Clear existing data if requested
        if clear_first:
            logger.warning("⚠️  Clearing existing data...")
            db.query(ExperienceDB).delete()
            db.query(UserDB).delete()
            db.commit()
            logger.info("✅ Existing data cleared")

        # Check if data already exists
        existing_users = db.query(UserDB).count()
        if existing_users > 0 and not clear_first:
            logger.warning(f"⚠️  Database already contains {existing_users} users")
            response = input("Continue and add more users? (y/n): ")
            if response.lower() != 'y':
                logger.info("Seeding cancelled")
                return

        logger.info(f"Creating {user_count} users with experiences...")

        created_users = 0
        created_experiences = 0

        # Generate and insert users with experiences
        for i in range(user_count):
            try:
                # Create user
                user_data = generate_mock_user(i)

                user = UserDB(
                    username=user_data["username"],
                    email=user_data["email"],
                    password_hash=pwd_context.hash(user_data["password"]),
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
                    exp_data = generate_mock_experience(user.id, exp_type)

                    experience = ExperienceDB(**exp_data)
                    db.add(experience)
                    created_experiences += 1

                created_users += 1

                if verbose or (i + 1) % 5 == 0:
                    logger.info(f"  Created user {i+1}/{user_count}: {user.username}")

            except Exception as e:
                logger.error(f"Failed to create user {i}: {e}")
                db.rollback()
                continue

        # Commit all changes
        try:
            db.commit()
            logger.info("=" * 70)
            logger.info("✅ DATABASE SEEDING COMPLETE!")
            logger.info("=" * 70)
            logger.info(f"📊 Statistics:")
            logger.info(f"   Users created: {created_users}")
            logger.info(f"   Experiences created: {created_experiences}")
            logger.info(f"   Average experiences per user: {created_experiences / created_users:.1f}")
            logger.info("=" * 70)
            logger.info("🎉 You can now use the admin panel to view and manage this data!")
            logger.info("   Admin Panel: dev/dev-frontend/levelith_admin_dashboard")
            logger.info("   Backend API: http://localhost:8000/docs")
            logger.info("=" * 70)

        except Exception as e:
            logger.error(f"❌ Failed to commit data: {e}")
            db.rollback()
            sys.exit(1)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Seed Levelith database with mock data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                      # Seed with 25 users (default)
  %(prog)s --users 50           # Seed with 50 users
  %(prog)s --clear --users 10   # Clear database and seed with 10 users
  %(prog)s --verbose            # Show detailed logging
        """
    )

    parser.add_argument(
        '--users', '-u',
        type=int,
        default=25,
        help='Number of users to create (default: 25)'
    )

    parser.add_argument(
        '--clear', '-c',
        action='store_true',
        help='Clear existing data before seeding'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )

    args = parser.parse_args()

    # Confirm if clearing data
    if args.clear:
        logger.warning("⚠️  WARNING: This will DELETE ALL existing data!")
        response = input("Are you sure you want to continue? (yes/no): ")
        if response.lower() != 'yes':
            logger.info("Seeding cancelled")
            return

    # Run seeding
    seed_database(
        user_count=args.users,
        clear_first=args.clear,
        verbose=args.verbose
    )


if __name__ == "__main__":
    main()
