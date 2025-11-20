# Database Data Models Reference

---
title: "Database Data Models Reference"
description: "Complete reference for SQLAlchemy ORM models including UserDB, ExperienceDB, NAICSCodeDB and their relationships, methods, and usage patterns."
category: "reference"
tags: ["orm", "models", "sqlalchemy", "data-models", "reference"]
author: "Semour Media Group"
date: "2025-11-20"
lastUpdated: "2025-11-20"
difficulty: "intermediate"
readingTime: 15
relatedPages:
  - "/docs/database/SCHEMA_REFERENCE.md"
  - "/docs/database/USAGE_GUIDE.md"
  - "/docs/database/DATABASE_ARCHITECTURE.md"
nextPage: "/docs/database/DATABASE_OVERVIEW.md"
prevPage: "/docs/database/TESTING_DATABASE.md"
searchKeywords:
  - "data models"
  - "orm models"
  - "model reference"
  - "sqlalchemy models"
showTOC: true
showBreadcrumbs: true
showLastUpdated: true
version: "1.0"
---

# Database Data Models Reference

> **TL;DR:** Complete ORM model reference for UserDB, ExperienceDB (with 9 polymorphic subtypes), and NAICSCodeDB. Includes field definitions, relationships, methods, and usage examples.

**Difficulty:** 🟡 Intermediate | **Time:** ⏱️ 15 minutes | **Last Updated:** November 20, 2025

---

## Table of Contents

- [UserDB Model](#userdb-model)
- [ExperienceDB Model](#experiencedb-model)
- [Experience Subtypes](#experience-subtypes)
- [NAICSCodeDB Model](#naicscodedb-model)
- [Model Relationships](#model-relationships)
- [Enums Reference](#enums-reference)
- [Additional Resources](#additional-resources)

---

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

**CertificateDB:**
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

**DegreeDB:**
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

**CourseDB:**
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

**GigDB:**
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

**PartTimeDB:**
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

**FullTimeDB:**
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

**SoftSkillDB:**
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

**HardSkillDB:**
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

**NativeSkillDB:**
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

## Additional Resources

- 📚 [Schema Reference](/docs/database/SCHEMA_REFERENCE.md)
- 🏗️ [Usage Guide](/docs/database/USAGE_GUIDE.md)
- 🧪 [Testing Guide](/docs/database/TESTING_DATABASE.md)
- 📖 [Database Architecture](/docs/database/DATABASE_ARCHITECTURE.md)

---

**Last Updated:** November 20, 2025 | **Version:** 1.0
