# User Database Model

---
title: "User Database Model"
description: "Complete reference for the UserDB SQLAlchemy model including fields, relationships, constraints, and usage examples."
category: "reference"
tags: ["database", "user-model", "sqlalchemy", "orm"]
author: "Semour Media Group"
date: "2025-11-20"
lastUpdated: "2025-11-20"
difficulty: "beginner"
readingTime: 8
relatedPages:
  - "/docs/backend/database/models/experience.md"
  - "/docs/backend/database/DATA_MODELS.md"
  - "/docs/backend/database/SCHEMA_REFERENCE.md"
nextPage: "/docs/backend/database/models/experience.md"
prevPage: "/docs/backend/database/DATA_MODELS.md"
searchKeywords:
  - "user model"
  - "userdb"
  - "user schema"
  - "authentication"
showTOC: true
showBreadcrumbs: true
showLastUpdated: true
version: "1.0"
---

# User Database Model

> **TL;DR:** UserDB model stores user accounts with authentication, profile data (JSON), and one-to-many relationship to experiences. Supports active/verified status, automatic timestamps, and cascade delete.

**Difficulty:** 🟢 Beginner | **Time:** ⏱️ 8 minutes | **Last Updated:** November 20, 2025

---

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

---

## Fields Reference

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

---

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

---

## Relationships

### One-to-Many: User → Experiences

```python
# Access user's experiences
user = db.query(UserDB).first()
experiences = user.experiences  # List[ExperienceDB]

# Count experiences
experience_count = len(user.experiences)

# Filter experiences
education = [e for e in user.experiences if e.category == "education"]
```

**Cascade Behavior:**
- Deleting a user automatically deletes all their experiences
- `cascade="all, delete-orphan"` ensures cleanup

---

## Usage Examples

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

---

## Validation Rules

- `username`: 3-50 characters, alphanumeric + underscore
- `email`: Valid email format
- `password_hash`: Must be hashed (PBKDF2/bcrypt/argon2)
- `profile_data`: Valid JSON object

---

## Indexes

| Index | Columns | Type | Purpose |
|-------|---------|------|---------|
| PRIMARY | id | BTREE | Fast lookups by ID |
| idx_users_username | username | BTREE UNIQUE | Fast username lookups, enforce uniqueness |
| idx_users_email | email | BTREE UNIQUE | Fast email lookups, enforce uniqueness |

---

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

## Related Documentation

- [Experience Model](experience.md)
- [NAICS Model](naics.md)
- [Data Models Reference](/docs/backend/database/DATA_MODELS.md)
- [Schema Reference](/docs/backend/database/SCHEMA_REFERENCE.md)

---

**Last Updated:** November 20, 2025 | **Version:** 1.0
