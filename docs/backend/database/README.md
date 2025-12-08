# Database Overview

---
title: "Database Overview"
description: "Complete overview of the Levelith database architecture, design philosophy, and core concepts. Entry point for understanding the database layer."
category: "reference"
tags: ["database", "postgresql", "sqlalchemy", "architecture", "overview"]
author: "Semour Media Group"
date: "2025-11-20"
lastUpdated: "2025-11-20"
difficulty: "intermediate"
readingTime: 10
relatedPages:
  - "/docs/database/DATABASE_ARCHITECTURE.md"
  - "/docs/database/SCHEMA_REFERENCE.md"
  - "/docs/database/USAGE_GUIDE.md"
nextPage: "/docs/database/DATABASE_ARCHITECTURE.md"
prevPage: "/docs/README.md"
searchKeywords:
  - "database overview"
  - "postgresql"
  - "sqlalchemy"
  - "orm"
  - "data persistence"
showTOC: true
showBreadcrumbs: true
showLastUpdated: true
version: "1.0"
---

# Database Overview

> **TL;DR:** Levelith uses PostgreSQL with SQLAlchemy ORM for data persistence. Three core tables (users, experiences, naics_codes) support user management, professional experience tracking, and NAICS industry classification. Clean architecture with layered design, connection pooling, and comprehensive health checks.

**Difficulty:** 🟡 Intermediate | **Time:** ⏱️ 10 minutes | **Last Updated:** November 20, 2025

---

## Table of Contents

- [Introduction](#introduction)
- [Database Technology Stack](#database-technology-stack)
- [Core Tables](#core-tables)
- [Design Philosophy](#design-philosophy)
- [Key Features](#key-features)
- [Quick Start](#quick-start)
- [Architecture Overview](#architecture-overview)
- [Connection Management](#connection-management)
- [Security Features](#security-features)
- [Performance Considerations](#performance-considerations)
- [Additional Resources](#additional-resources)

---

## Introduction

The Levelith database layer provides persistent storage for user accounts, professional experiences, and NAICS industry classification data. Built on PostgreSQL with SQLAlchemy ORM, it offers a robust, scalable, and type-safe foundation for the application.

### What This Documentation Covers

- **Database Overview** (this document) - High-level architecture and concepts
- **[Database Architecture](DATABASE_ARCHITECTURE.md)** - Detailed design decisions and patterns
- **[Schema Reference](SCHEMA_REFERENCE.md)** - Complete schema documentation
- **[Usage Guide](USAGE_GUIDE.md)** - How to interact with the database
- **[Testing Guide](TESTING_DATABASE.md)** - Testing strategies and patterns
- **[Data Models](DATA_MODELS.md)** - ORM model reference

:::info
**Note:** This documentation assumes familiarity with SQL and basic ORM concepts. For PostgreSQL basics, see [PostgreSQL Documentation](https://www.postgresql.org/docs/).
:::

---

## Database Technology Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Database** | PostgreSQL | 13+ | Primary data store |
| **ORM** | SQLAlchemy | 2.0+ | Object-relational mapping |
| **Driver** | psycopg2 | Latest | PostgreSQL adapter |
| **Connection Pool** | QueuePool | Built-in | Connection management |
| **Migrations** | Alembic | Latest | Schema versioning (planned) |

### Why PostgreSQL?

✅ **ACID Compliance** - Ensures data integrity and consistency
✅ **JSON Support** - Native JSON columns for flexible data
✅ **Performance** - Excellent query optimization and indexing
✅ **Scalability** - Handles millions of records efficiently
✅ **Open Source** - No licensing costs, community-driven

### Why SQLAlchemy?

✅ **Type Safety** - Python type hints with ORM models
✅ **Flexibility** - Both ORM and raw SQL support
✅ **Abstraction** - Database-agnostic queries
✅ **Relationships** - Automatic JOIN handling
✅ **Testing** - Easy to mock and test

---

## Core Tables

The database consists of three primary tables:

### 1. Users Table

**Purpose:** Store user accounts and profile information

```
users
├── id (primary key)
├── username (unique, indexed)
├── email (unique, indexed)
├── password_hash
├── profile_data (JSON)
├── is_active, is_verified
└── timestamps (created_at, updated_at, last_login)
```

**Features:**
- Unique username and email constraints
- JSON profile data for flexibility
- Account status flags
- Automatic timestamp tracking

### 2. Experiences Table

**Purpose:** Store professional experiences (education, workplace, skills)

```
experiences
├── id (primary key)
├── user_id (foreign key → users.id)
├── title, description
├── category (enum: education, workplace, skills)
├── experience_type (enum: 9 types)
├── naics_code (default: "123456")
├── organization, location
├── start_date, end_date, is_current
├── type_specific_data (JSON)
├── tags (JSON array)
└── timestamps
```

**Features:**
- 9 experience subtypes (polymorphic)
- NAICS code integration
- Flexible JSON fields for type-specific data
- Cascade delete with user

### 3. NAICS Codes Table

**Purpose:** Store NAICS 2022 industry classification system

```
naics_codes
├── code (primary key, 6 digits)
├── title, description
├── level (2/3/4/6 digit hierarchy)
├── parent_code (self-referential)
├── sector, subsector, industry_group (denormalized)
├── category (enum)
├── keywords, aliases (JSON arrays)
├── sba_size_standard
└── admin fields (tags, notes)
```

**Features:**
- Hierarchical industry classification
- Denormalized fields for fast queries
- Enhanced search with keywords/aliases
- SBA integration support

---

## Design Philosophy

### 1. Clean Architecture

The database layer follows clean architecture principles:

```
┌─────────────────────────────────────┐
│   API Layer                          │
└─────────────┬───────────────────────┘
              ↓
┌─────────────────────────────────────┐
│   Service Layer                      │  ← Business logic
└─────────────┬───────────────────────┘
              ↓
┌─────────────────────────────────────┐
│   Repository Layer                   │  ← Data access abstraction
└─────────────┬───────────────────────┘
              ↓
┌─────────────────────────────────────┐
│   Database Layer (SQLAlchemy)        │  ← ORM models
└─────────────┬───────────────────────┘
              ↓
┌─────────────────────────────────────┐
│   PostgreSQL                         │  ← Physical storage
└─────────────────────────────────────┘
```

### 2. Database-Agnostic Design

While optimized for PostgreSQL, the codebase supports:
- **PostgreSQL** - Production (recommended)
- **SQLite** - Local development and testing

### 3. Type Safety First

All models use Python type hints and SQLAlchemy types:

```python
class UserDB(Base):
    id: str = Column(String(32), primary_key=True)
    username: str = Column(String(50), unique=True, nullable=False)
    email: str = Column(String(255), unique=True, nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
```

---

## Key Features

### ✅ Connection Pooling

- **QueuePool** manages database connections
- **pool_size**: 5 connections (configurable)
- **max_overflow**: 10 additional connections
- **pool_pre_ping**: Verifies connections before use

### ✅ Automatic Timestamps

All models track creation and update times:

```python
created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

### ✅ Relationship Management

SQLAlchemy handles relationships automatically:

```python
# User has many experiences
user.experiences  # Returns list of ExperienceDB objects

# Experience belongs to user
experience.user  # Returns UserDB object
```

### ✅ Cascade Deletes

Deleting a user automatically deletes all their experiences:

```python
experiences = relationship("ExperienceDB", cascade="all, delete-orphan")
```

### ✅ JSON Fields

Flexible data storage with PostgreSQL JSON:

```python
profile_data = Column(JSON, default=dict, nullable=False)
type_specific_data = Column(JSON, default=dict, nullable=False)
tags = Column(JSON, default=list, nullable=False)
```

### ✅ Health Checks

Built-in database health monitoring:

```python
from backend.database import DatabaseHealthCheck

is_healthy = DatabaseHealthCheck.check()  # Returns bool
info = DatabaseHealthCheck.get_info()     # Returns detailed info
```

---

## Quick Start

### Initialize Database

```python
from backend.database import init_db

# Create all tables
init_db()
```

### Get Database Session

```python
from backend.database import get_db
from fastapi import Depends

@app.get("/users")
def list_users(db: Session = Depends(get_db)):
    users = db.query(UserDB).all()
    return users
```

### Context Manager Usage

```python
from backend.database import get_db_context

with get_db_context() as db:
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    print(user.username)
```

### Check Database Health

```python
from backend.database import DatabaseHealthCheck

# Simple health check
if DatabaseHealthCheck.check():
    print("Database is healthy")

# Detailed information
info = DatabaseHealthCheck.get_info()
print(f"Database: {info['database']}")
print(f"Version: {info['version']}")
```

---

## Architecture Overview

### File Structure

```
backend/
├── database.py           # Database configuration and session management
├── models/
│   ├── db_models.py      # SQLAlchemy ORM models
│   ├── user.py           # Domain model (deprecated)
│   ├── experience.py     # Domain model (deprecated)
│   └── naics.py          # NAICS domain model
├── repositories/         # Data access layer
│   ├── user_repository.py
│   ├── experience_repository.py
│   └── naics_repository.py
└── services/             # Business logic layer
    ├── user_service.py
    ├── experience_service.py
    └── naics_service.py
```

### Configuration

Database settings are managed via environment variables:

```python
# backend/config.py
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost/dbname")
DATABASE_POOL_SIZE = int(os.getenv("DATABASE_POOL_SIZE", "5"))
DATABASE_MAX_OVERFLOW = int(os.getenv("DATABASE_MAX_OVERFLOW", "10"))
```

---

## Connection Management

### Session Lifecycle

1. **Request arrives** → FastAPI creates session via `get_db()`
2. **Query execution** → SQLAlchemy uses session for queries
3. **Request completes** → Session automatically closed (cleanup)

### Connection Pool Behavior

```python
# Pool maintains 5 active connections
pool_size = 5

# Can create up to 10 additional connections during peak load
max_overflow = 10

# Total max connections = 15
```

### Best Practices

✅ **DO:**
- Use `Depends(get_db)` for FastAPI endpoints
- Use `get_db_context()` for scripts/utilities
- Let SQLAlchemy manage transactions
- Use connection pooling (already configured)

❌ **DON'T:**
- Create engine/session manually
- Keep sessions open longer than needed
- Disable connection pooling
- Use raw SQL without parameterization

---

## Security Features

### 1. SQL Injection Protection

SQLAlchemy automatically parameterizes queries:

```python
# ✅ SAFE - Parameterized query
user = db.query(UserDB).filter(UserDB.email == user_email).first()

# ❌ DANGEROUS - String interpolation (never do this)
user = db.execute(f"SELECT * FROM users WHERE email = '{user_email}'")
```

### 2. Password Hashing

Passwords are never stored in plain text:

```python
password_hash = Column(String(255), nullable=False)  # Stores hashed password
# Plain password never touches database
```

### 3. Production Safeguards

```python
def drop_db():
    if settings.is_production:
        raise RuntimeError("Cannot drop database in production!")
    Base.metadata.drop_all(bind=engine)
```

### 4. Foreign Key Constraints

Referential integrity enforced at database level:

```python
user_id = Column(String(32), ForeignKey("users.id"), nullable=False)
```

---

## Performance Considerations

### Indexing Strategy

**Indexed Fields:**
- `users.username` - Fast username lookups
- `users.email` - Fast email lookups
- `experiences.user_id` - Fast user experience queries
- `naics_codes.level` - Fast hierarchy queries
- `naics_codes.category` - Fast category filtering

### Query Optimization

**Eager Loading:**
```python
# Load user with experiences in single query
user = db.query(UserDB).options(joinedload(UserDB.experiences)).first()
```

**Filtering:**
```python
# Use indexed fields for filtering
users = db.query(UserDB).filter(UserDB.is_active == True).all()
```

### JSON Field Performance

- Fast for writes and small reads
- Slower for complex queries/filtering
- Consider extracting frequently-queried JSON fields to columns

---

## Additional Resources

### Official Documentation

- 📚 [Database Architecture](/docs/database/DATABASE_ARCHITECTURE.md) - Design decisions
- 🏗️ [Schema Reference](/docs/database/SCHEMA_REFERENCE.md) - Complete schemas
- 🧪 [Usage Guide](/docs/database/USAGE_GUIDE.md) - How to use the database
- 📖 [Testing Guide](/docs/database/TESTING_DATABASE.md) - Testing strategies
- 💻 [Data Models](/docs/database/DATA_MODELS.md) - ORM model reference

### External Resources

- 🌐 [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- 📖 [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- 📊 [Database Design Best Practices](https://www.postgresql.org/docs/current/tutorial.html)

### Code Examples

- 💻 [Database Module](https://github.com/Free-Columns/levelith-2/blob/main/backend/database.py)
- 🎯 [ORM Models](https://github.com/Free-Columns/levelith-2/blob/main/backend/models/db_models.py)
- 📊 [Repositories](https://github.com/Free-Columns/levelith-2/tree/main/backend/repositories)

---

## Related Documentation

- **Next:** [Database Architecture](/docs/database/DATABASE_ARCHITECTURE.md)
- **Previous:** [Documentation Index](/docs/README.md)

**Other related documentation:**

- [API Documentation](/docs/api/API_DOCUMENTATION.md)
- [Backend NAICS Summary](/docs/backend/NAICS_EXPANSION_SUMMARY.md)
- [Deployment Guide](/docs/deployment/RENDER_DEPLOYMENT.md)

---

## Feedback

Found an issue with this guide? Have suggestions for improvement?

- 👍 **Helpful?** This provides database overview
- 🐛 **Found a bug?** [Report it on GitHub](https://github.com/Free-Columns/levelith-2/issues)
- 💡 **Have an idea?** [Start a discussion](https://github.com/Free-Columns/levelith-2/discussions)

---

**Last Updated:** November 20, 2025 | **Version:** 1.0 | **Contributors:** Semour Media Group

---

*This document is part of the Levelith Developer Documentation. For questions, join our [Discord community](https://discord.gg/levelith).*
