# Database Usage Guide

---
title: "Database Usage Guide"
description: "Practical guide to using the Levelith database including common operations, best practices, connection management, and code examples."
category: "guides"
tags: ["database", "usage", "howto", "sqlalchemy", "examples"]
author: "Semour Media Group"
date: "2025-11-20"
lastUpdated: "2025-11-20"
difficulty: "beginner"
readingTime: 15
relatedPages:
  - "/docs/database/DATABASE_OVERVIEW.md"
  - "/docs/database/SCHEMA_REFERENCE.md"
  - "/docs/database/TESTING_DATABASE.md"
nextPage: "/docs/database/TESTING_DATABASE.md"
prevPage: "/docs/database/SCHEMA_REFERENCE.md"
searchKeywords:
  - "database usage"
  - "how to use database"
  - "database operations"
  - "crud operations"
showTOC: true
showBreadcrumbs: true
showLastUpdated: true
version: "1.0"
---

# Database Usage Guide

> **TL;DR:** Use `Depends(get_db)` in FastAPI routes for automatic session management. Repository pattern for data access. Always use parameterized queries. Leverage SQLAlchemy relationships. Close sessions automatically. Follow examples for CRUD operations.

**Difficulty:** 🟢 Beginner | **Time:** ⏱️ 15 minutes | **Last Updated:** November 20, 2025

---

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

## Additional Resources

- 📚 [Database Overview](/docs/database/DATABASE_OVERVIEW.md)
- 🏗️ [Schema Reference](/docs/database/SCHEMA_REFERENCE.md)
- 🧪 [Testing Guide](/docs/database/TESTING_DATABASE.md)
- 📖 [Data Models](/docs/database/DATA_MODELS.md)

---

**Last Updated:** November 20, 2025 | **Version:** 1.0
