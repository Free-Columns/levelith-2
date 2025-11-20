# Complete Database Model Guide

---
title: "Complete Database Model Guide"
description: "Comprehensive reference for all Levilith database models: User, Experience (9 polymorphic types), and NAICS industry classification with hierarchical structure."
category: "reference"
tags: ["database", "models", "sqlalchemy", "orm", "user", "experience", "naics"]
author: "Semour Media Group"
date: "2025-11-20"
lastUpdated: "2025-11-20"
difficulty: "intermediate"
readingTime: 30
relatedPages:
  - "/docs/backend/database/DATA_MODELS.md"
  - "/docs/backend/database/SCHEMA_REFERENCE.md"
  - "/docs/backend/naics/NAICS_EXPANSION_SUMMARY.md"
searchKeywords:
  - "database models"
  - "user model"
  - "experience model"
  - "naics model"
  - "polymorphism"
  - "sqlalchemy"
showTOC: true
showBreadcrumbs: true
showLastUpdated: true
version: "1.0"
---

# Complete Database Model Guide

> **TL;DR:** Complete reference for Levilith's three core database models: UserDB (authentication & profiles), ExperienceDB (9 polymorphic experience types), and NAICSCodeDB (NAICS 2022 industry classification with 4-level hierarchy).

**Difficulty:** 🟡 Intermediate | **Time:** ⏱️ 30 minutes | **Last Updated:** November 20, 2025

---

## Table of Contents

1. [User Model](#user-model)
2. [Experience Model](#experience-model)
3. [NAICS Model](#naics-model)
4. [Model Relationships](#model-relationships)
5. [Usage Patterns](#usage-patterns)

---

# User Model

## Model Definition

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

## User Fields Reference

### Identity Fields

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | String(32) | PRIMARY KEY | Unique hex identifier (16 bytes) |
| `username` | String(50) | UNIQUE, NOT NULL, INDEXED | User's unique username (3-50 chars) |
| `email` | String(255) | UNIQUE, NOT NULL, INDEXED | User's email address |
| `password_hash` | String(255) | NOT NULL | Hashed password (never plain text) |

### Profile Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `is_active` | Boolean | TRUE | Account active status |
| `is_verified` | Boolean | FALSE | Email verification status |
| `profile_data` | JSON | `{}` | Flexible profile metadata |

### Timestamp Fields

| Field | Type | Auto-Updated | Description |
|-------|------|--------------|-------------|
| `created_at` | DateTime | No | Account creation timestamp |
| `updated_at` | DateTime | Yes | Last modification timestamp |
| `last_login` | DateTime | No | Last login timestamp (nullable) |

## Profile Data Schema

The `profile_data` JSON field stores flexible user metadata:

```json
{
  "bio": "Software engineer passionate about clean code",
  "location": "San Francisco, CA",
  "avatar_url": "https://example.com/avatar.jpg",
  "website": "https://example.com",
  "social": {
    "github": "username",
    "linkedin": "profile-url",
    "twitter": "@handle"
  },
  "preferences": {
    "theme": "dark",
    "notifications": true,
    "language": "en"
  },
  "metadata": {
    "onboarding_completed": true,
    "tutorial_step": 5
  }
}
```

## User Usage Examples

### Create User

```python
from backend.models.db_models import UserDB
import secrets

user = UserDB(
    username="john_doe",
    email="john@example.com",
    password_hash=hash_password("secure_password"),
    profile_data={
        "bio": "Software engineer",
        "location": "San Francisco"
    }
)
db.add(user)
db.commit()
db.refresh(user)
```

### Find User

```python
# By ID
user = db.query(UserDB).filter(UserDB.id == user_id).first()

# By email
user = db.query(UserDB).filter(UserDB.email == "john@example.com").first()

# By username
user = db.query(UserDB).filter(UserDB.username == "john_doe").first()
```

### Update User

```python
user = db.query(UserDB).filter(UserDB.id == user_id).first()
user.username = "johndoe"
user.profile_data["bio"] = "Updated bio"
user.last_login = datetime.utcnow()
db.commit()
```

### Delete User

```python
user = db.query(UserDB).filter(UserDB.id == user_id).first()
db.delete(user)  # Cascades to experiences
db.commit()
```

## User Validation Rules

- `username`: 3-50 characters, alphanumeric + underscore
- `email`: Valid email format
- `password_hash`: Must be hashed (PBKDF2/bcrypt/argon2)
- `profile_data`: Valid JSON object

## User Indexes

| Index | Columns | Type | Purpose |
|-------|---------|------|---------|
| PRIMARY | id | BTREE | Fast lookups by ID |
| idx_users_username | username | BTREE UNIQUE | Fast username lookups, enforce uniqueness |
| idx_users_email | email | BTREE UNIQUE | Fast email lookups, enforce uniqueness |

## Security Considerations

1. **Password Storage:** Never store plain text passwords
   - Use bcrypt, argon2, or PBKDF2
   - Minimum 10 rounds for bcrypt

2. **Email Verification:** Use `is_verified` flag
   - Send verification email on signup
   - Require verification for sensitive operations

3. **Account Status:** Use `is_active` flag
   - Deactivate instead of delete for audit trails
   - Check `is_active` in authentication

---

# Experience Model

## Base Model Definition

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

## Experience Types (9 Total)

### Education Category

#### CertificateDB - Professional certifications

```python
class CertificateDB(ExperienceDB):
    __mapper_args__ = {'polymorphic_identity': ExperienceType.CERTIFICATE}

# type_specific_data example:
{
    "certification_number": "AWS-123456",
    "certifying_body": "Amazon Web Services",
    "expiration_date": "2025-12-31",
    "is_renewable": true
}
```

#### DegreeDB - Academic degrees

```python
class DegreeDB(ExperienceDB):
    __mapper_args__ = {'polymorphic_identity': ExperienceType.DEGREE}

# type_specific_data example:
{
    "degree_level": "Bachelor",
    "major": "Computer Science",
    "minor": "Mathematics",
    "gpa": 3.8,
    "honors": ["Cum Laude"]
}
```

#### CourseDB - Individual courses

```python
class CourseDB(ExperienceDB):
    __mapper_args__ = {'polymorphic_identity': ExperienceType.COURSE}

# type_specific_data example:
{
    "course_code": "CS101",
    "credits": 3,
    "grade": "A",
    "instructor": "Dr. Smith"
}
```

### Workplace Category

#### GigDB - Short-term contracts

```python
class GigDB(ExperienceDB):
    __mapper_args__ = {'polymorphic_identity': ExperienceType.GIG}

# type_specific_data example:
{
    "contract_type": "1099",
    "hourly_rate": 150,
    "total_hours": 120
}
```

#### PartTimeDB - Part-time employment

```python
class PartTimeDB(ExperienceDB):
    __mapper_args__ = {'polymorphic_identity': ExperienceType.PART_TIME}

# type_specific_data example:
{
    "hours_per_week": 20,
    "employment_type": "w2",
    "department": "Engineering"
}
```

#### FullTimeDB - Full-time employment

```python
class FullTimeDB(ExperienceDB):
    __mapper_args__ = {'polymorphic_identity': ExperienceType.FULL_TIME}

# type_specific_data example:
{
    "job_title": "Senior Software Engineer",
    "department": "Engineering",
    "team_size": 8
}
```

### Skills Category

#### SoftSkillDB - Interpersonal skills

```python
class SoftSkillDB(ExperienceDB):
    __mapper_args__ = {'polymorphic_identity': ExperienceType.SOFT_SKILL}

# type_specific_data example:
{
    "skill_level": "advanced",
    "contexts": ["team leadership", "public speaking"]
}
```

#### HardSkillDB - Technical skills

```python
class HardSkillDB(ExperienceDB):
    __mapper_args__ = {'polymorphic_identity': ExperienceType.HARD_SKILL}

# type_specific_data example:
{
    "proficiency_level": "expert",
    "years_experience": 5,
    "tools": ["Python", "FastAPI"]
}
```

#### NativeSkillDB - Innate abilities/languages

```python
class NativeSkillDB(ExperienceDB):
    __mapper_args__ = {'polymorphic_identity': ExperienceType.NATIVE_SKILL}

# type_specific_data example:
{
    "skill_type": "language",
    "language": "Spanish",
    "proficiency": "native"
}
```

## Experience Field Reference

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `id` | String(32) | Yes | auto | Unique identifier |
| `user_id` | String(32) | Yes | - | Foreign key to users |
| `title` | String(255) | Yes | - | Experience title |
| `description` | Text | No | NULL | Detailed description |
| `naics_code` | String(6) | Yes | "123456" | NAICS industry code |
| `category` | Enum | Yes | - | education/workplace/skills |
| `experience_type` | Enum | Yes | - | Specific type (9 options) |
| `start_date` | DateTime | No | NULL | Start date |
| `end_date` | DateTime | No | NULL | End date |
| `is_current` | Boolean | Yes | FALSE | Currently active |
| `organization` | String(255) | No | NULL | Organization name |
| `location` | String(255) | No | NULL | Location |
| `type_specific_data` | JSON | Yes | `{}` | Type-specific fields |
| `tags` | JSON | Yes | `[]` | Searchable tags |
| `experience_metadata` | JSON | Yes | `{}` | Additional metadata |

## Experience Usage Examples

### Create Experience

```python
from backend.models.db_models import DegreeDB

degree = DegreeDB(
    user_id=user.id,
    title="Bachelor of Science in Computer Science",
    description="Comprehensive CS program...",
    naics_code="611310",  # Colleges & Universities
    category="education",
    experience_type="degree",
    organization="Stanford University",
    location="Stanford, CA",
    start_date=datetime(2020, 9, 1),
    end_date=datetime(2024, 6, 1),
    type_specific_data={
        "degree_level": "Bachelor",
        "major": "Computer Science",
        "gpa": 3.8
    },
    tags=["computer science", "engineering", "bachelor"]
)
db.add(degree)
db.commit()
```

### Query Experiences

```python
# Get all user experiences
experiences = db.query(ExperienceDB).filter(
    ExperienceDB.user_id == user_id
).all()

# Get specific type
degrees = db.query(DegreeDB).filter(
    DegreeDB.user_id == user_id
).all()

# Filter by category
education = db.query(ExperienceDB).filter(
    ExperienceDB.user_id == user_id,
    ExperienceDB.category == "education"
).all()
```

## Polymorphic Queries

```python
# Query returns correct subtype
experiences = db.query(ExperienceDB).all()
for exp in experiences:
    print(type(exp))  # DegreeDB, CertificateDB, etc.

# Access type-specific data
if isinstance(exp, DegreeDB):
    gpa = exp.type_specific_data.get("gpa")
```

---

# NAICS Model

## Model Definition

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
    cross_references = Column(JSON, default=list, nullable=False)
    notes = Column(Text, nullable=True)

    # Admin
    tags = Column(JSON, default=list, nullable=False)
    custom_category = Column(String(100), nullable=True)
    admin_notes = Column(Text, nullable=True)

    # Metadata
    is_active = Column(Boolean, default=True, nullable=False)
    year = Column(Integer, default=2022, nullable=False)
    data_source = Column(String(255), nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow,
                       onupdate=datetime.utcnow, nullable=False)
```

## Hierarchy Structure

### Levels

| Level | Digits | Example | Description |
|-------|--------|---------|-------------|
| 2 | XX | 54 | Sector |
| 3 | XXX | 541 | Subsector |
| 4 | XXXX | 5415 | Industry Group |
| 6 | XXXXXX | 541511 | National Industry |

### Denormalized Fields

```
code: "541511" (6 digits)
├── level: 6
├── parent_code: "5415"
├── sector: "54"
├── subsector: "541"
├── industry_group: "5415"
└── industry_detail: "541511"
```

**Benefits:**
- Fast queries: `WHERE level = 2` (get all sectors)
- No string parsing needed
- Indexed for performance

## NAICS Field Reference

### Core Fields

| Field | Type | Description |
|-------|------|-------------|
| `code` | String(6) | NAICS code (PRIMARY KEY) |
| `title` | String(500) | Industry title |
| `description` | Text | Detailed description |

### Hierarchy Fields

| Field | Type | Indexed | Description |
|-------|------|---------|-------------|
| `level` | Integer | Yes | Hierarchy level (2/3/4/6) |
| `parent_code` | String(6) | Yes | Parent NAICS code |
| `sector` | String(2) | Yes | 2-digit sector |
| `subsector` | String(3) | Yes | 3-digit subsector |
| `industry_group` | String(4) | Yes | 4-digit industry group |
| `industry_detail` | String(6) | No | 6-digit detail (same as code) |

### Search Fields

| Field | Type | Description |
|-------|------|-------------|
| `keywords` | JSON Array | Searchable keywords |
| `aliases` | JSON Array | Alternative names/synonyms |
| `examples` | Text | Example businesses |
| `cross_references` | JSON Array | Related NAICS codes |

## NAICS Categories

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

## NAICS Usage Examples

### Get NAICS Code

```python
# By code
naics = db.query(NAICSCodeDB).filter(
    NAICSCodeDB.code == "541511"
).first()

print(naics.title)  # "Custom Computer Programming Services"
```

### Get All Sectors

```python
sectors = db.query(NAICSCodeDB).filter(
    NAICSCodeDB.level == 2
).order_by(NAICSCodeDB.code).all()

for sector in sectors:
    print(f"{sector.code}: {sector.title}")
```

### Get Children

```python
# Get subsectors of sector 54
subsectors = db.query(NAICSCodeDB).filter(
    NAICSCodeDB.parent_code == "54"
).all()
```

### Hierarchical Query

```python
# Get full hierarchy for a code
code = "541511"
hierarchy = []

current = db.query(NAICSCodeDB).filter(NAICSCodeDB.code == code).first()
while current:
    hierarchy.insert(0, current)
    if current.parent_code:
        current = db.query(NAICSCodeDB).filter(
            NAICSCodeDB.code == current.parent_code
        ).first()
    else:
        break

# hierarchy = [Sector(54), Subsector(541), IndustryGroup(5415), Industry(541511)]
```

### Search by Keyword

```python
# Search in title or keywords
search_term = "software"
results = db.query(NAICSCodeDB).filter(
    NAICSCodeDB.title.ilike(f"%{search_term}%")
).all()
```

## Example NAICS Entry

```python
naics = NAICSCodeDB(
    code="541511",
    title="Custom Computer Programming Services",
    description="This industry comprises establishments...",
    level=6,
    parent_code="5415",
    sector="54",
    subsector="541",
    industry_group="5415",
    industry_detail="541511",
    category=NAICSCategory.PROFESSIONAL_TECHNICAL_SERVICES,
    keywords=["software", "programming", "development", "coding"],
    aliases=["Software Development", "Custom Software"],
    examples="Custom programming, software consulting, mobile app development",
    sba_size_standard="$30 million",
    sba_source="SBA Size Standards Table",
    is_active=True,
    year=2022
)
```

## NAICS Indexes

| Index | Purpose |
|-------|---------|
| PRIMARY (code) | Fast code lookups |
| idx_naics_level | Fast level filtering (get all sectors) |
| idx_naics_sector | Fast sector queries |
| idx_naics_subsector | Fast subsector queries |
| idx_naics_category | Fast category filtering |
| idx_naics_parent | Fast parent lookups |

## Performance Optimization

### Fast Hierarchy Queries

```python
# Get all codes in Professional Services sector
# Uses indexed sector field - FAST
codes = db.query(NAICSCodeDB).filter(
    NAICSCodeDB.sector == "54"
).all()

# vs parsing code string - SLOW
codes = db.query(NAICSCodeDB).filter(
    NAICSCodeDB.code.startswith("54")
).all()
```

### Cached Lookups

```python
# Cache frequently accessed codes
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_naics_cached(code: str):
    return db.query(NAICSCodeDB).filter(
        NAICSCodeDB.code == code
    ).first()
```

---

# Model Relationships

## Entity Relationship Diagram

```
┌─────────────┐
│   UserDB    │
│             │
│ id (PK)     │
│ username    │
│ email       │
│ ...         │
└──────┬──────┘
       │
       │ 1:N (cascade delete)
       │
       ▼
┌─────────────────┐         ┌──────────────┐
│  ExperienceDB   │────────▶│ NAICSCodeDB  │
│                 │ N:1     │              │
│ id (PK)         │         │ code (PK)    │
│ user_id (FK)    │         │ title        │
│ naics_code (FK) │         │ hierarchy    │
│ category        │         │ ...          │
│ experience_type │         └──────────────┘
│ ...             │
└─────────────────┘
```

## Relationship Patterns

### User → Experiences (One-to-Many)

```python
# Access from user
user = db.query(UserDB).first()
all_experiences = user.experiences

# Filter experiences
education = [e for e in user.experiences if e.category == "education"]
current_jobs = [e for e in user.experiences 
                if e.category == "workplace" and e.is_current]
```

### Experience → User (Many-to-One)

```python
# Access from experience
experience = db.query(ExperienceDB).first()
owner = experience.user
print(f"Experience belongs to: {owner.username}")
```

### Experience → NAICS (Many-to-One)

```python
# Get NAICS info for experience
experience = db.query(ExperienceDB).first()
naics = db.query(NAICSCodeDB).filter(
    NAICSCodeDB.code == experience.naics_code
).first()
print(f"Industry: {naics.title}")
```

---

# Usage Patterns

## Complete User Profile Creation

```python
# Create user
user = UserDB(
    username="john_doe",
    email="john@example.com",
    password_hash=hash_password("secure_password"),
    profile_data={
        "bio": "Full-stack developer",
        "location": "San Francisco, CA"
    }
)
db.add(user)
db.commit()
db.refresh(user)

# Add education
degree = DegreeDB(
    user_id=user.id,
    title="BS Computer Science",
    naics_code="611310",
    category="education",
    experience_type="degree",
    organization="Stanford University",
    start_date=datetime(2016, 9, 1),
    end_date=datetime(2020, 6, 1),
    type_specific_data={
        "degree_level": "Bachelor",
        "major": "Computer Science",
        "gpa": 3.8
    }
)
db.add(degree)

# Add work experience
job = FullTimeDB(
    user_id=user.id,
    title="Senior Software Engineer",
    naics_code="541511",
    category="workplace",
    experience_type="full_time",
    organization="Tech Corp",
    location="San Francisco, CA",
    start_date=datetime(2020, 7, 1),
    is_current=True,
    type_specific_data={
        "job_title": "Senior Software Engineer",
        "department": "Engineering",
        "team_size": 8
    }
)
db.add(job)

# Add skills
skill = HardSkillDB(
    user_id=user.id,
    title="Python Development",
    naics_code="541511",
    category="skills",
    experience_type="hard_skill",
    type_specific_data={
        "proficiency_level": "expert",
        "years_experience": 5,
        "tools": ["Python", "FastAPI", "SQLAlchemy"]
    }
)
db.add(skill)

db.commit()
```

## Complex Queries

### Get User's Complete Profile

```python
def get_complete_profile(user_id: str):
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    
    profile = {
        "user": {
            "username": user.username,
            "email": user.email,
            "profile": user.profile_data,
            "created_at": user.created_at
        },
        "education": [],
        "work": [],
        "skills": []
    }
    
    for exp in user.experiences:
        naics = db.query(NAICSCodeDB).filter(
            NAICSCodeDB.code == exp.naics_code
        ).first()
        
        exp_data = {
            "title": exp.title,
            "organization": exp.organization,
            "dates": {
                "start": exp.start_date,
                "end": exp.end_date,
                "is_current": exp.is_current
            },
            "industry": naics.title if naics else None,
            "details": exp.type_specific_data
        }
        
        if exp.category == "education":
            profile["education"].append(exp_data)
        elif exp.category == "workplace":
            profile["work"].append(exp_data)
        elif exp.category == "skills":
            profile["skills"].append(exp_data)
    
    return profile
```

### Search Experiences by Industry

```python
def find_experiences_by_industry(sector_code: str):
    """Find all experiences in a given sector."""
    # Get all NAICS codes in sector
    sector_codes = db.query(NAICSCodeDB.code).filter(
        NAICSCodeDB.sector == sector_code
    ).all()
    code_list = [code[0] for code in sector_codes]
    
    # Find experiences
    experiences = db.query(ExperienceDB).filter(
        ExperienceDB.naics_code.in_(code_list)
    ).all()
    
    return experiences
```

### Get Industry Statistics

```python
def get_industry_stats():
    """Get count of experiences per industry sector."""
    from sqlalchemy import func
    
    stats = db.query(
        NAICSCodeDB.sector,
        NAICSCodeDB.title,
        func.count(ExperienceDB.id).label('experience_count')
    ).join(
        ExperienceDB,
        ExperienceDB.naics_code == NAICSCodeDB.code
    ).filter(
        NAICSCodeDB.level == 2
    ).group_by(
        NAICSCodeDB.sector,
        NAICSCodeDB.title
    ).order_by(
        func.count(ExperienceDB.id).desc()
    ).all()
    
    return stats
```

## Batch Operations

### Import Multiple Experiences

```python
def import_user_resume(user_id: str, resume_data: dict):
    """Import complete resume data."""
    experiences = []
    
    # Process education
    for edu in resume_data.get("education", []):
        exp = DegreeDB(
            user_id=user_id,
            title=edu["degree"],
            organization=edu["school"],
            naics_code="611310",
            category="education",
            experience_type="degree",
            start_date=edu["start_date"],
            end_date=edu["end_date"],
            type_specific_data=edu.get("details", {})
        )
        experiences.append(exp)
    
    # Process work
    for job in resume_data.get("work", []):
        exp = FullTimeDB(
            user_id=user_id,
            title=job["position"],
            organization=job["company"],
            naics_code=job.get("naics_code", "999999"),
            category="workplace",
            experience_type="full_time",
            start_date=job["start_date"],
            end_date=job.get("end_date"),
            is_current=job.get("is_current", False),
            type_specific_data=job.get("details", {})
        )
        experiences.append(exp)
    
    # Batch insert
    db.bulk_save_objects(experiences)
    db.commit()
    
    return len(experiences)
```

## Migration Patterns

### Update All Experiences with NAICS

```python
def backfill_naics_codes():
    """Update experiences with inferred NAICS codes."""
    experiences = db.query(ExperienceDB).filter(
        ExperienceDB.naics_code == "123456"  # Default placeholder
    ).all()
    
    for exp in experiences:
        # Infer NAICS from organization or title
        if "university" in exp.organization.lower():
            exp.naics_code = "611310"
        elif "software" in exp.title.lower():
            exp.naics_code = "541511"
        # Add more inference logic...
    
    db.commit()
```

---

## Database Indexes Summary

### UserDB Indexes
- PRIMARY KEY: `id`
- UNIQUE INDEX: `username`
- UNIQUE INDEX: `email`

### ExperienceDB Indexes
- PRIMARY KEY: `id`
- INDEX: `user_id` (for FK joins)
- INDEX: `category` (for filtering)
- INDEX: `experience_type` (for polymorphic queries)

### NAICSCodeDB Indexes
- PRIMARY KEY: `code`
- INDEX: `level`
- INDEX: `parent_code`
- INDEX: `sector`
- INDEX: `subsector`
- INDEX: `industry_group`
- INDEX: `category`

---

## Best Practices

### 1. Always Use Relationships

```python
# ✅ Good - Use relationship
user = db.query(UserDB).first()
experiences = user.experiences

# ❌ Bad - Manual join
experiences = db.query(ExperienceDB).filter(
    ExperienceDB.user_id == user.id
).all()
```

### 2. Leverage Polymorphism

```python
# ✅ Good - Query returns correct type
exp = db.query(ExperienceDB).first()
if isinstance(exp, DegreeDB):
    gpa = exp.type_specific_data.get("gpa")

# ❌ Bad - Check type field manually
if exp.experience_type == "degree":
    # Still need to parse type_specific_data
```

### 3. Use Indexed Fields

```python
# ✅ Good - Uses indexed sector field
codes = db.query(NAICSCodeDB).filter(
    NAICSCodeDB.sector == "54"
).all()

# ❌ Bad - String operation, no index
codes = db.query(NAICSCodeDB).filter(
    NAICSCodeDB.code.startswith("54")
).all()
```

### 4. Validate NAICS Codes

```python
# ✅ Good - Validate before creating experience
naics = db.query(NAICSCodeDB).filter(
    NAICSCodeDB.code == naics_code
).first()
if not naics:
    raise ValueError(f"Invalid NAICS code: {naics_code}")

experience = DegreeDB(naics_code=naics_code, ...)
```

### 5. Use Cascade Deletes

```python
# ✅ Good - Cascade handles cleanup
user = db.query(UserDB).first()
db.delete(user)  # Automatically deletes all experiences
db.commit()

# ❌ Bad - Manual cleanup
experiences = db.query(ExperienceDB).filter(
    ExperienceDB.user_id == user.id
).all()
for exp in experiences:
    db.delete(exp)
db.delete(user)
db.commit()
```

---

## Related Documentation

- [Data Models Reference](/docs/backend/database/DATA_MODELS.md)
- [Schema Reference](/docs/backend/database/SCHEMA_REFERENCE.md)
- [NAICS Expansion Summary](/docs/backend/naics/NAICS_EXPANSION_SUMMARY.md)
- [NAICS Import Guide](/docs/backend/naics/NAICS_IMPORT_GUIDE.md)
- [API Endpoints](/docs/backend/api/ENDPOINTS.md)

---

**Last Updated:** November 20, 2025 | **Version:** 1.0
