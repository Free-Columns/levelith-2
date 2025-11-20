# Experience Database Model

---
title: "Experience Database Model"
description: "Complete reference for the ExperienceDB polymorphic SQLAlchemy model including all 9 subtypes, fields, and relationships."
category: "reference"
tags: ["database", "experience-model", "polymorphism", "sqlalchemy"]
author: "Semour Media Group"
date: "2025-11-20"
lastUpdated: "2025-11-20"
difficulty: "intermediate"
readingTime: 10
relatedPages:
  - "/docs/backend/database/models/user.md"
  - "/docs/backend/database/models/naics.md"
  - "/docs/backend/database/DATA_MODELS.md"
nextPage: "/docs/backend/database/models/naics.md"
prevPage: "/docs/backend/database/models/user.md"
searchKeywords:
  - "experience model"
  - "experiencedb"
  - "polymorphism"
  - "experience types"
showTOC: true
showBreadcrumbs: true
showLastUpdated: true
version: "1.0"
---

# Experience Database Model

> **TL;DR:** ExperienceDB uses single-table inheritance for 9 polymorphic experience types (3 education, 3 workplace, 3 skills). Stores type-specific data in JSON field, linked to User via foreign key, requires NAICS code.

**Difficulty:** 🟡 Intermediate | **Time:** ⏱️ 10 minutes | **Last Updated:** November 20, 2025

---

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

---

## Experience Types (9 Total)

### Education Category

**CertificateDB** - Professional certifications
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

**DegreeDB** - Academic degrees
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

**CourseDB** - Individual courses
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

**GigDB** - Short-term contracts
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

**PartTimeDB** - Part-time employment
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

**FullTimeDB** - Full-time employment
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

**SoftSkillDB** - Interpersonal skills
```python
class SoftSkillDB(ExperienceDB):
    __mapper_args__ = {'polymorphic_identity': ExperienceType.SOFT_SKILL}

# type_specific_data example:
{
    "skill_level": "advanced",
    "contexts": ["team leadership", "public speaking"]
}
```

**HardSkillDB** - Technical skills
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

**NativeSkillDB** - Innate abilities/languages
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

---

## Field Reference

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

---

## Usage Examples

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

---

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

## Related Documentation

- [User Model](user.md)
- [NAICS Model](naics.md)
- [Data Models Reference](/docs/backend/database/DATA_MODELS.md)
- [Schema Reference](/docs/backend/database/SCHEMA_REFERENCE.md)

---

**Last Updated:** November 20, 2025 | **Version:** 1.0
