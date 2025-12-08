# Complete Database Guide

---
title: "Complete Database Guide"
description: "Comprehensive reference for the Levelith database including data models, usage patterns, testing strategies, and best practices."
category: "guides"
tags: ["database", "orm", "sqlalchemy", "testing", "usage", "reference"]
author: "Semour Media Group"
date: "2025-11-20"
lastUpdated: "2025-11-20"
difficulty: "beginner-to-advanced"
readingTime: 40
version: "1.0"
---

> **TL;DR:** Complete database reference covering ORM models (UserDB, ExperienceDB with 9 subtypes, NAICSCodeDB), CRUD operations, relationships, testing patterns with pytest fixtures, and best practices. Use `Depends(get_db)` in FastAPI, maintain 80% test coverage, leverage SQLAlchemy relationships, always use parameterized queries.

---

## Table of Contents

- [Part 1: Database Models](#part-1-database-models)
  - [UserDB Model](#userdb-model)
  - [ExperienceDB Model](#experiencedb-model)
  - [Experience Subtypes](#experience-subtypes)
  - [NAICSCodeDB Model](#naicscodedb-model)
  - [Model Relationships](#model-relationships)
  - [Enums Reference](#enums-reference)
- [Part 2: Database Usage](#part-2-database-usage)
  - [Quick Start](#quick-start)
  - [CRUD Operations](#crud-operations)
  - [Working with Relationships](#working-with-relationships)
  - [Common Patterns](#common-patterns)
  - [Best Practices](#best-practices)
  - [Error Handling](#error-handling)
  - [Performance Tips](#performance-tips)
- [Part 3: Database Testing](#part-3-database-testing)
  - [Test Database Setup](#test-database-setup)
  - [Test Fixtures](#test-fixtures)
  - [Test Patterns](#test-patterns)
  - [Test Data Factories](#test-data-factories)
  - [Mocking Strategies](#mocking-strategies)
  - [Coverage Requirements](#coverage-requirements)

---

# Part 1: Database Models

## UserDB Model

### Definition

```python
class UserDB(Base):
    """User ORM model for database persistence."""
    
    __tablename__ = "users"
    
    # Identity
    id = Column(String(32), primary_key=True, 
                default=lambda: secrets.token_hex(16))
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    
    # Profile
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    profile_data = Column(JSON, default=dict, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, 
                       onupdate=datetime.utcnow, nullable=False)
    last_login = Column(DateTime, nullable=True)
    
    # Relationships
    experiences = relationship("ExperienceDB", back_populates="user", 
                             cascade="all, delete-orphan")
```

### Usage

```python
# Create
user = UserDB(
    username="john_doe",
    email="john@example.com",
    password_hash=hash_password("password123"),
    profile_data={
        "bio": "Software engineer",
        "location": "San Francisco"
    }
)
db.add(user)
db.commit()

# Read
user = db.query(UserDB).filter(UserDB.email == "john@example.com").first()

# Update
user.username = "johndoe"
user.last_login = datetime.utcnow()
db.commit()

# Delete (cascades to experiences)
db.delete(user)
db.commit()
```

---

## ExperienceDB Model

### Base Model

```python
class ExperienceDB(Base):
    """Polymorphic base model for all experience types."""
    
    __tablename__ = "experiences"
    
    # Identity
    id = Column(String(32), primary_key=True,
               default=lambda: secrets.token_hex(16))
    user_id = Column(String(32), ForeignKey("users.id"), 
                    nullable=False, index=True)
    
    # Core
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    naics_code = Column(String(6), nullable=False, default="123456")
    
    # Classification
    category = Column(SQLEnum(ExperienceCategory), nullable=False)
    experience_type = Column(SQLEnum(ExperienceType), nullable=False)
    
    # Dates
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    is_current = Column(Boolean, default=False)
    
    # Organization
    organization = Column(String(255), nullable=True)
    location = Column(String(255), nullable=True)
    
    # Flexible data
    type_specific_data = Column(JSON, default=dict, nullable=False)
    tags = Column(JSON, default=list, nullable=False)
    experience_metadata = Column(JSON, default=dict, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow,
                       onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("UserDB", back_populates="experiences")
```

---

## Experience Subtypes

### Education Experiences

#### CertificateDB

```python
class CertificateDB(ExperienceDB):
    """Professional certification."""
    __mapper_args__ = {'polymorphic_identity': ExperienceType.CERTIFICATE}

# Example type_specific_data:
{
    "certification_number": "AWS-123456",
    "certifying_body": "Amazon Web Services",
    "expiration_date": "2025-12-31",
    "is_renewable": true
}
```

#### DegreeDB

```python
class DegreeDB(ExperienceDB):
    """Academic degree."""
    __mapper_args__ = {'polymorphic_identity': ExperienceType.DEGREE}

# Example type_specific_data:
{
    "degree_level": "Bachelor",
    "major": "Computer Science",
    "minor": "Mathematics",
    "gpa": 3.8,
    "honors": ["Cum Laude", "Dean's List"]
}
```

#### CourseDB

```python
class CourseDB(ExperienceDB):
    """Individual course or training."""
    __mapper_args__ = {'polymorphic_identity': ExperienceType.COURSE}

# Example type_specific_data:
{
    "course_code": "CS101",
    "credits": 3,
    "grade": "A",
    "instructor": "Dr. Smith"
}
```

### Workplace Experiences

#### GigDB

```python
class GigDB(ExperienceDB):
    """Short-term contract work."""
    __mapper_args__ = {'polymorphic_identity': ExperienceType.GIG}

# Example type_specific_data:
{
    "contract_type": "1099",
    "hourly_rate": 150,
    "total_hours": 120,
    "client_name": "Acme Corp"
}
```

#### PartTimeDB

```python
class PartTimeDB(ExperienceDB):
    """Part-time employment."""
    __mapper_args__ = {'polymorphic_identity': ExperienceType.PART_TIME}

# Example type_specific_data:
{
    "hours_per_week": 20,
    "employment_type": "w2",
    "department": "Engineering"
}
```

#### FullTimeDB

```python
class FullTimeDB(ExperienceDB):
    """Full-time employment."""
    __mapper_args__ = {'polymorphic_identity': ExperienceType.FULL_TIME}

# Example type_specific_data:
{
    "job_title": "Senior Software Engineer",
    "department": "Engineering",
    "employment_type": "permanent",
    "team_size": 8
}
```

### Skills Experiences

#### SoftSkillDB

```python
class SoftSkillDB(ExperienceDB):
    """Soft/interpersonal skill."""
    __mapper_args__ = {'polymorphic_identity': ExperienceType.SOFT_SKILL}

# Example type_specific_data:
{
    "skill_level": "advanced",
    "contexts": ["team leadership", "public speaking"],
    "certifications": []
}
```

#### HardSkillDB

```python
class HardSkillDB(ExperienceDB):
    """Technical/measurable skill."""
    __mapper_args__ = {'polymorphic_identity': ExperienceType.HARD_SKILL}

# Example type_specific_data:
{
    "proficiency_level": "expert",
    "years_experience": 5,
    "tools": ["Python", "Django", "FastAPI"],
    "certifications": ["AWS Certified Developer"]
}
```

#### NativeSkillDB

```python
class NativeSkillDB(ExperienceDB):
    """Innate ability or language."""
    __mapper_args__ = {'polymorphic_identity': ExperienceType.NATIVE_SKILL}

# Example type_specific_data:
{
    "skill_type": "language",
    "language": "Spanish",
    "proficiency": "native",
    "dialects": ["Mexican", "Castilian"]
}
```

---

## NAICSCodeDB Model

```python
class NAICSCodeDB(Base):
    """NAICS 2022 industry classification."""
    
    __tablename__ = "naics_codes"
    
    # Primary key
    code = Column(String(6), primary_key=True)
    
    # Core
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    
    # Hierarchy
    level = Column(Integer, nullable=False, index=True)
    parent_code = Column(String(6), nullable=True, index=True)
    sector = Column(String(2), nullable=True, index=True)
    subsector = Column(String(3), nullable=True, index=True)
    industry_group = Column(String(4), nullable=True, index=True)
    industry_detail = Column(String(6), nullable=True)
    
    # Categorization
    category = Column(SQLEnum(NAICSCategory), nullable=False, index=True)
    
    # SBA
    sba_size_standard = Column(String(255), nullable=True)
    sba_source = Column(String(255), nullable=True)
    
    # Search
    keywords = Column(JSON, default=list, nullable=False)
    aliases = Column(JSON, default=list, nullable=False)
    examples = Column(Text, nullable=True)
    
    # Metadata
    is_active = Column(Boolean, default=True, nullable=False)
    year = Column(Integer, default=2022, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow,
                       onupdate=datetime.utcnow, nullable=False)
```

---

## Model Relationships

### One-to-Many: User → Experiences

```python
# User side
user = db.query(UserDB).first()
experiences = user.experiences  # List[ExperienceDB]

# Experience side
experience = db.query(ExperienceDB).first()
user = experience.user  # UserDB
```

### Self-Referential: NAICS → Parent NAICS

```python
naics = db.query(NAICSCodeDB).filter(NAICSCodeDB.code == "541511").first()
parent = db.query(NAICSCodeDB).filter(
    NAICSCodeDB.code == naics.parent_code
).first()
```

---

## Enums Reference

### ExperienceCategory

```python
class ExperienceCategory(str, Enum):
    EDUCATION = "education"
    WORKPLACE = "workplace"
    SKILLS = "skills"
```

### ExperienceType

```python
class ExperienceType(str, Enum):
    # Education
    CERTIFICATE = "certificate"
    DEGREE = "degree"
    COURSE = "course"
    
    # Workplace
    GIG = "gig"
    PART_TIME = "part_time"
    FULL_TIME = "full_time"
    
    # Skills
    SOFT_SKILL = "soft_skill"
    HARD_SKILL = "hard_skill"
    NATIVE_SKILL = "native_skill"
```

### NAICSCategory

```python
class NAICSCategory(str, Enum):
    AGRICULTURE_FORESTRY_FISHING = "agriculture_forestry_fishing"
    MINING_QUARRYING = "mining_quarrying"
    UTILITIES = "utilities"
    CONSTRUCTION = "construction"
    MANUFACTURING = "manufacturing"
    WHOLESALE_TRADE = "wholesale_trade"
    RETAIL_TRADE = "retail_trade"
    TRANSPORTATION_WAREHOUSING = "transportation_warehousing"
    INFORMATION = "information"
    FINANCE_INSURANCE = "finance_insurance"
    REAL_ESTATE = "real_estate"
    PROFESSIONAL_TECHNICAL_SERVICES = "professional_technical_services"
    EDUCATIONAL_SERVICES = "educational_services"
    HEALTHCARE = "healthcare"
```

---

# Part 2: Database Usage

## Quick Start

### Setup Database Connection

```python
from backend.database import init_db

# Initialize tables (run once at startup)
init_db()
```

### Get Database Session (FastAPI)

```python
from backend.database import get_db
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/users")
def list_users(db: Session = Depends(get_db)):
    users = db.query(UserDB).all()
    return users
```

### Get Database Session (Scripts)

```python
from backend.database import get_db_context

with get_db_context() as db:
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    print(user.username)
```

---

## CRUD Operations

### Create

```python
from backend.models.db_models import UserDB
import secrets

# Create new user
user = UserDB(
    id=secrets.token_hex(16),
    username="john_doe",
    email="john@example.com",
    password_hash="hashed_password_here"
)
db.add(user)
db.commit()
db.refresh(user)  # Get updated data (timestamps, defaults)
```

### Read

```python
# Get by ID
user = db.query(UserDB).filter(UserDB.id == user_id).first()

# Get by email
user = db.query(UserDB).filter(UserDB.email == email).first()

# Get all active users
users = db.query(UserDB).filter(UserDB.is_active == True).all()

# Get with limit/offset
users = db.query(UserDB).limit(10).offset(20).all()
```

### Update

```python
# Get user
user = db.query(UserDB).filter(UserDB.id == user_id).first()

# Update fields
user.username = "new_username"
user.profile_data = {"bio": "Updated bio"}

# Commit changes
db.commit()
db.refresh(user)
```

### Delete

```python
# Get user
user = db.query(UserDB).filter(UserDB.id == user_id).first()

# Delete
db.delete(user)
db.commit()

# Note: Cascade delete will remove all user's experiences
```

---

## Working with Relationships

### Load User with Experiences

```python
from sqlalchemy.orm import joinedload

# Eager load (single query with JOIN)
user = db.query(UserDB).options(
    joinedload(UserDB.experiences)
).filter(UserDB.id == user_id).first()

# Access experiences (already loaded)
for exp in user.experiences:
    print(exp.title)
```

### Access Related Data

```python
# User → Experiences (one-to-many)
user = db.query(UserDB).filter(UserDB.id == user_id).first()
experiences = user.experiences  # List[ExperienceDB]

# Experience → User (many-to-one)
experience = db.query(ExperienceDB).filter(ExperienceDB.id == exp_id).first()
user = experience.user  # UserDB
```

---

## Common Patterns

### Pagination

```python
def get_users_paginated(db: Session, page: int = 1, page_size: int = 50):
    offset = (page - 1) * page_size
    users = db.query(UserDB).offset(offset).limit(page_size).all()
    total = db.query(UserDB).count()
    
    return {
        "items": users,
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": (total + page_size - 1) // page_size
    }
```

### Search

```python
def search_users(db: Session, query: str):
    # Case-insensitive search
    users = db.query(UserDB).filter(
        UserDB.username.ilike(f"%{query}%") |
        UserDB.email.ilike(f"%{query}%")
    ).all()
    return users
```

### Filtering

```python
# Multiple filters
experiences = db.query(ExperienceDB).filter(
    ExperienceDB.user_id == user_id,
    ExperienceDB.category == "education",
    ExperienceDB.is_current == True
).all()

# OR conditions
from sqlalchemy import or_

experiences = db.query(ExperienceDB).filter(
    or_(
        ExperienceDB.experience_type == "degree",
        ExperienceDB.experience_type == "certificate"
    )
).all()
```

---

## Best Practices

### ✅ DO

1. **Use Dependency Injection**
```python
@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(UserDB).all()
```

2. **Use Parameterized Queries**
```python
# ✅ SAFE
user = db.query(UserDB).filter(UserDB.email == email).first()

# ❌ DANGEROUS
user = db.execute(f"SELECT * FROM users WHERE email = '{email}'")
```

3. **Close Sessions Automatically**
```python
# FastAPI handles this
def route(db: Session = Depends(get_db)):
    # db is automatically closed after request

# For scripts, use context manager
with get_db_context() as db:
    # db is automatically closed when leaving context
```

4. **Use Transactions**
```python
try:
    user = UserDB(...)
    db.add(user)
    
    experience = ExperienceDB(user_id=user.id, ...)
    db.add(experience)
    
    db.commit()  # Commit all or nothing
except Exception:
    db.rollback()  # Rollback on error
    raise
```

### ❌ DON'T

1. **Don't Create Engine/Session Manually**
```python
# ❌ WRONG
engine = create_engine("postgresql://...")
session = Session(engine)

# ✅ CORRECT
from backend.database import get_db
```

2. **Don't Keep Sessions Open**
```python
# ❌ WRONG
db = SessionLocal()
# ... long operation ...
db.close()

# ✅ CORRECT
with get_db_context() as db:
    # ... operation ...
```

3. **Don't Use String Interpolation**
```python
# ❌ SQL INJECTION RISK
query = f"SELECT * FROM users WHERE id = '{user_id}'"

# ✅ SAFE
user = db.query(UserDB).filter(UserDB.id == user_id).first()
```

---

## Error Handling

```python
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

try:
    user = UserDB(username="duplicate", email="existing@example.com")
    db.add(user)
    db.commit()
except IntegrityError as e:
    db.rollback()
    if "unique constraint" in str(e).lower():
        raise ValueError("Username or email already exists")
    raise
except SQLAlchemyError as e:
    db.rollback()
    logger.error(f"Database error: {e}")
    raise
```

---

## Performance Tips

### Use Eager Loading

```python
# ❌ N+1 Query Problem
users = db.query(UserDB).all()
for user in users:
    experiences = user.experiences  # Triggers query per user!

# ✅ Single Query
users = db.query(UserDB).options(joinedload(UserDB.experiences)).all()
for user in users:
    experiences = user.experiences  # Already loaded
```

### Use Batch Operations

```python
# Create multiple records
users = [
    UserDB(username=f"user{i}", email=f"user{i}@example.com")
    for i in range(100)
]
db.bulk_save_objects(users)
db.commit()
```

### Use Indexes

```python
# Filter on indexed fields (fast)
users = db.query(UserDB).filter(UserDB.email == email).all()

# Filter on non-indexed JSON (slow)
users = db.query(UserDB).filter(
    UserDB.profile_data['location'].astext == 'San Francisco'
).all()
```

---

# Part 3: Database Testing

## Test Database Setup

### Basic Test Database

```python
# conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database import Base
from backend.models.db_models import UserDB, ExperienceDB

@pytest.fixture(scope="function")
def test_db():
    """Create test database for each test."""
    # Use in-memory SQLite for speed
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    yield db
    
    db.close()
    Base.metadata.drop_all(engine)
```

### Basic Test Example

```python
def test_create_user(test_db):
    """Test user creation."""
    user = UserDB(
        username="testuser",
        email="test@example.com",
        password_hash="hashed_password"
    )
    test_db.add(user)
    test_db.commit()
    
    # Verify
    saved_user = test_db.query(UserDB).filter(
        UserDB.username == "testuser"
    ).first()
    
    assert saved_user is not None
    assert saved_user.email == "test@example.com"
```

---

## Test Fixtures

### Database Fixtures

```python
@pytest.fixture(scope="session")
def test_engine():
    """Create test engine (session scope)."""
    engine = create_engine("sqlite:///:memory:")
    yield engine
    engine.dispose()

@pytest.fixture(scope="function")
def test_db(test_engine):
    """Create test database session (function scope)."""
    Base.metadata.create_all(test_engine)
    SessionLocal = sessionmaker(bind=test_engine)
    db = SessionLocal()
    
    yield db
    
    db.rollback()  # Rollback any uncommitted changes
    db.close()
    Base.metadata.drop_all(test_engine)
```

### Factory Fixtures

```python
@pytest.fixture
def create_user(test_db):
    """Factory for creating test users."""
    def _create_user(**kwargs):
        defaults = {
            "username": f"testuser_{secrets.token_hex(4)}",
            "email": f"test_{secrets.token_hex(4)}@example.com",
            "password_hash": "hashed_password",
            "is_active": True,
            "is_verified": False
        }
        defaults.update(kwargs)
        
        user = UserDB(**defaults)
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)
        return user
    
    return _create_user

# Usage
def test_user_creation(create_user):
    user = create_user(username="john_doe")
    assert user.username == "john_doe"
```

---

## Test Patterns

### Testing CRUD Operations

```python
class TestUserCRUD:
    def test_create(self, test_db):
        user = UserDB(username="test", email="test@example.com", 
                     password_hash="hash")
        test_db.add(user)
        test_db.commit()
        assert user.id is not None
    
    def test_read(self, test_db, create_user):
        user = create_user()
        found = test_db.query(UserDB).filter(UserDB.id == user.id).first()
        assert found.username == user.username
    
    def test_update(self, test_db, create_user):
        user = create_user()
        user.username = "updated"
        test_db.commit()
        
        updated = test_db.query(UserDB).filter(UserDB.id == user.id).first()
        assert updated.username == "updated"
    
    def test_delete(self, test_db, create_user):
        user = create_user()
        user_id = user.id
        
        test_db.delete(user)
        test_db.commit()
        
        deleted = test_db.query(UserDB).filter(UserDB.id == user_id).first()
        assert deleted is None
```

### Testing Relationships

```python
def test_user_experiences_relationship(test_db, create_user):
    user = create_user()
    
    # Create experiences
    exp1 = ExperienceDB(user_id=user.id, title="Experience 1", 
                       category="education", experience_type="degree")
    exp2 = ExperienceDB(user_id=user.id, title="Experience 2",
                       category="workplace", experience_type="full_time")
    
    test_db.add_all([exp1, exp2])
    test_db.commit()
    
    # Test relationship
    test_db.refresh(user)
    assert len(user.experiences) == 2
    assert user.experiences[0].title in ["Experience 1", "Experience 2"]
```

### Testing Cascade Delete

```python
def test_cascade_delete(test_db, create_user):
    user = create_user()
    
    # Create experience
    exp = ExperienceDB(user_id=user.id, title="Test", 
                      category="education", experience_type="degree")
    test_db.add(exp)
    test_db.commit()
    
    exp_id = exp.id
    
    # Delete user (should cascade to experiences)
    test_db.delete(user)
    test_db.commit()
    
    # Verify experience deleted
    deleted_exp = test_db.query(ExperienceDB).filter(
        ExperienceDB.id == exp_id
    ).first()
    assert deleted_exp is None
```

---

## Test Data Factories

```python
import secrets
from datetime import datetime, timedelta

class UserFactory:
    @staticmethod
    def create(db, **kwargs):
        defaults = {
            "username": f"user_{secrets.token_hex(4)}",
            "email": f"{secrets.token_hex(4)}@example.com",
            "password_hash": "hashed_password",
            "is_active": True,
            "is_verified": False,
            "profile_data": {}
        }
        defaults.update(kwargs)
        
        user = UserDB(**defaults)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

class ExperienceFactory:
    @staticmethod
    def create_degree(db, user_id, **kwargs):
        defaults = {
            "user_id": user_id,
            "title": "Bachelor of Science",
            "category": "education",
            "experience_type": "degree",
            "naics_code": "611310",
            "organization": "University",
            "start_date": datetime(2020, 1, 1),
            "end_date": datetime(2024, 5, 1),
            "type_specific_data": {
                "degree_level": "Bachelor",
                "major": "Computer Science",
                "gpa": 3.8
            }
        }
        defaults.update(kwargs)
        
        exp = ExperienceDB(**defaults)
        db.add(exp)
        db.commit()
        db.refresh(exp)
        return exp
```

---

## Mocking Strategies

### Mock Database Session

```python
from unittest.mock import Mock

def test_with_mock_db():
    mock_db = Mock()
    mock_user = UserDB(username="test", email="test@example.com")
    mock_db.query().filter().first.return_value = mock_user
    
    # Use mock_db in test
    result = mock_db.query(UserDB).filter(UserDB.id == "123").first()
    assert result.username == "test"
```

### Mock External Dependencies

```python
from unittest.mock import patch

@patch('backend.services.user_service.hash_password')
def test_user_registration(mock_hash, test_db):
    mock_hash.return_value = "mocked_hash"
    
    # Test registration logic
    user = UserDB(username="test", email="test@example.com",
                 password_hash=mock_hash("password"))
    test_db.add(user)
    test_db.commit()
    
    assert user.password_hash == "mocked_hash"
    mock_hash.assert_called_once_with("password")
```

---

## Testing Best Practices

### ✅ DO

1. **Use In-Memory SQLite for Speed**
```python
engine = create_engine("sqlite:///:memory:")
```

2. **Isolate Tests**
```python
@pytest.fixture(scope="function")  # New DB per test
def test_db(test_engine):
    # ... creates fresh DB for each test
```

3. **Use Factories for Test Data**
```python
user = UserFactory.create(test_db, username="specific_user")
```

4. **Test Edge Cases**
```python
def test_unique_constraint_violation(test_db, create_user):
    create_user(username="duplicate")
    
    with pytest.raises(IntegrityError):
        create_user(username="duplicate")
```

5. **Maintain 80% Coverage**
```bash
pytest --cov=backend --cov-report=html
```

### ❌ DON'T

1. **Don't Use Production Database**
```python
# ❌ WRONG
engine = create_engine(settings.database_url)

# ✅ CORRECT  
engine = create_engine("sqlite:///:memory:")
```

2. **Don't Share State Between Tests**
```python
# ❌ WRONG - Session scope causes shared state
@pytest.fixture(scope="session")
def test_db():
    # Tests can interfere with each other

# ✅ CORRECT - Function scope isolates tests
@pytest.fixture(scope="function")
def test_db():
    # Each test gets fresh database
```

3. **Don't Skip Cleanup**
```python
# ✅ ALWAYS cleanup after tests
@pytest.fixture
def test_db():
    db = setup_db()
    yield db
    db.close()  # Cleanup
```

---

## Coverage Requirements

Per Golden Rules, maintain ≥80% test coverage:

```bash
# Run with coverage
pytest --cov=backend --cov-report=term-missing

# Generate HTML report
pytest --cov=backend --cov-report=html
open htmlcov/index.html
```

---

## Complete Example: Full Test Suite

```python
# tests/test_database.py
import pytest
import secrets
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database import Base
from backend.models.db_models import UserDB, ExperienceDB

@pytest.fixture(scope="function")
def test_db():
    """Create test database."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(engine)

@pytest.fixture
def create_user(test_db):
    """Factory for creating users."""
    def _create(**kwargs):
        defaults = {
            "username": f"user_{secrets.token_hex(4)}",
            "email": f"{secrets.token_hex(4)}@example.com",
            "password_hash": "hash"
        }
        defaults.update(kwargs)
        user = UserDB(**defaults)
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)
        return user
    return _create

class TestUserOperations:
    def test_create_user(self, test_db):
        user = UserDB(username="test", email="test@example.com", 
                     password_hash="hash")
        test_db.add(user)
        test_db.commit()
        assert user.id is not None
    
    def test_read_user(self, test_db, create_user):
        user = create_user(username="john")
        found = test_db.query(UserDB).filter(
            UserDB.username == "john"
        ).first()
        assert found.id == user.id
    
    def test_update_user(self, test_db, create_user):
        user = create_user()
        user.username = "updated"
        test_db.commit()
        
        updated = test_db.query(UserDB).filter(
            UserDB.id == user.id
        ).first()
        assert updated.username == "updated"
    
    def test_delete_user(self, test_db, create_user):
        user = create_user()
        user_id = user.id
        test_db.delete(user)
        test_db.commit()
        
        deleted = test_db.query(UserDB).filter(
            UserDB.id == user_id
        ).first()
        assert deleted is None

class TestExperienceOperations:
    def test_create_experience(self, test_db, create_user):
        user = create_user()
        exp = ExperienceDB(
            user_id=user.id,
            title="Test Experience",
            category="education",
            experience_type="degree"
        )
        test_db.add(exp)
        test_db.commit()
        assert exp.id is not None
    
    def test_user_experience_relationship(self, test_db, create_user):
        user = create_user()
        exp = ExperienceDB(
            user_id=user.id,
            title="Test",
            category="education",
            experience_type="degree"
        )
        test_db.add(exp)
        test_db.commit()
        
        test_db.refresh(user)
        assert len(user.experiences) == 1
        assert user.experiences[0].title == "Test"
    
    def test_cascade_delete(self, test_db, create_user):
        user = create_user()
        exp = ExperienceDB(
            user_id=user.id,
            title="Test",
            category="education",
            experience_type="degree"
        )
        test_db.add(exp)
        test_db.commit()
        exp_id = exp.id
        
        test_db.delete(user)
        test_db.commit()
        
        deleted_exp = test_db.query(ExperienceDB).filter(
            ExperienceDB.id == exp_id
        ).first()
        assert deleted_exp is None
```

---

## Summary

This complete guide covers:

1. **Database Models**: UserDB, ExperienceDB (9 polymorphic subtypes), NAICSCodeDB with full field definitions and relationships
2. **Usage Patterns**: CRUD operations, relationship management, pagination, search, filtering with best practices
3. **Testing Strategies**: pytest fixtures, factory patterns, mocking, coverage requirements, and complete test examples

**Key Takeaways:**
- Use `Depends(get_db)` for automatic session management
- Always use parameterized queries (never string interpolation)
- Leverage SQLAlchemy relationships and eager loading
- Test with in-memory SQLite and function-scoped fixtures
- Maintain ≥80% test coverage per Golden Rules
- Use factory patterns for test data generation
- Close sessions automatically via context managers

---

**Last Updated:** November 20, 2025 | **Version:** 1.0 | **Difficulty:** 🟢🟡🔴 Beginner to Advanced
