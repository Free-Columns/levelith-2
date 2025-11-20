# Database Architecture

---
title: "Database Architecture"
description: "Detailed explanation of database design decisions, architectural patterns, and rationale behind the Levelith database implementation."
category: "architecture"
tags: ["database", "architecture", "design-decisions", "patterns", "sqlalchemy"]
author: "Semour Media Group"
date: "2025-11-20"
lastUpdated: "2025-11-20"
difficulty: "advanced"
readingTime: 15
relatedPages:
  - "/docs/database/DATABASE_OVERVIEW.md"
  - "/docs/database/SCHEMA_REFERENCE.md"
  - "/docs/architecture/COMPARISON.md"
nextPage: "/docs/database/SCHEMA_REFERENCE.md"
prevPage: "/docs/database/DATABASE_OVERVIEW.md"
searchKeywords:
  - "database architecture"
  - "design decisions"
  - "orm patterns"
  - "database design"
  - "sqlalchemy patterns"
showTOC: true
showBreadcrumbs: true
showLastUpdated: true
version: "1.0"
---

# Database Architecture

> **TL;DR:** Levelith's database uses layered clean architecture with SQLAlchemy ORM, single-table inheritance for experience polymorphism, denormalized NAICS hierarchy for performance, JSON fields for flexibility, and connection pooling for scalability. Trade-offs favor simplicity and performance over strict domain separation.

**Difficulty:** 🔴 Advanced | **Time:** ⏱️ 15 minutes | **Last Updated:** November 20, 2025

---

## Table of Contents

- [Architectural Principles](#architectural-principles)
- [Layered Architecture](#layered-architecture)
- [Design Decisions](#design-decisions)
- [Table Design](#table-design)
- [Polymorphic Experience Model](#polymorphic-experience-model)
- [NAICS Hierarchy Design](#naics-hierarchy-design)
- [JSON Fields Strategy](#json-fields-strategy)
- [Indexing Strategy](#indexing-strategy)
- [Connection Pooling](#connection-pooling)
- [Trade-Offs and Alternatives](#trade-offs-and-alternatives)
- [Future Considerations](#future-considerations)
- [Additional Resources](#additional-resources)

---

## Architectural Principles

The database architecture follows these core principles:

### 1. Simplicity Over Purity

**Decision:** Use SQLAlchemy ORM models directly instead of separate domain models

**Rationale:**
- ✅ Reduces code duplication
- ✅ Easier to maintain
- ✅ Less mapping overhead
- ❌ Couples business logic to database

:::info
**Design Choice:** We chose pragmatism over strict domain-driven design. For a project of this size, the benefits of simplicity outweigh theoretical purity.
:::

### 2. Performance Through Denormalization

**Decision:** Denormalize NAICS hierarchy fields

**Rationale:**
- ✅ Fast queries without string parsing
- ✅ Simple filtering by hierarchy level
- ✅ Indexed lookups
- ❌ Data duplication (acceptable trade-off)

### 3. Flexibility Through JSON

**Decision:** Use JSON columns for variable/extensible data

**Rationale:**
- ✅ Schema evolution without migrations
- ✅ Type-specific data storage
- ✅ Flexible metadata
- ❌ Slower queries on JSON fields

### 4. Type Safety First

**Decision:** Use SQLAlchemy 2.0 with Python type hints

**Rationale:**
- ✅ Compile-time type checking
- ✅ Better IDE support
- ✅ Self-documenting code
- ✅ Reduced runtime errors

---

## Layered Architecture

### Architecture Layers

```
┌───────────────────────────────────────────────┐
│  API Layer (FastAPI Routes)                   │
│  - HTTP request/response                      │
│  - Input validation (Pydantic)                │
│  - Depends(get_db) for session injection      │
└────────────────┬──────────────────────────────┘
                 ↓
┌───────────────────────────────────────────────┐
│  Service Layer (Business Logic)               │
│  - User registration, authentication          │
│  - Experience creation and validation         │
│  - NAICS code lookups and suggestions         │
└────────────────┬──────────────────────────────┘
                 ↓
┌───────────────────────────────────────────────┐
│  Repository Layer (Data Access)               │
│  - CRUD operations                            │
│  - Query building                             │
│  - Database abstraction                       │
└────────────────┬──────────────────────────────┘
                 ↓
┌───────────────────────────────────────────────┐
│  ORM Layer (SQLAlchemy Models)                │
│  - UserDB, ExperienceDB, NAICSCodeDB          │
│  - Relationships and constraints              │
│  - Type definitions                           │
└────────────────┬──────────────────────────────┘
                 ↓
┌───────────────────────────────────────────────┐
│  Database Layer (PostgreSQL)                  │
│  - Physical storage                           │
│  - Transactions and ACID guarantees           │
│  - Indexes and constraints                    │
└───────────────────────────────────────────────┘
```

### Separation of Concerns

| Layer | Responsibility | Examples |
|-------|----------------|----------|
| **API** | HTTP handling | Route definitions, request validation |
| **Service** | Business logic | Password hashing, NAICS validation |
| **Repository** | Data access | `find_by_email()`, `create_user()` |
| **ORM** | Object mapping | Model definitions, relationships |
| **Database** | Persistence | Tables, indexes, constraints |

---

## Design Decisions

### Decision 1: Single Table Inheritance for Experiences

**Problem:** Need to store 9 different experience types with shared and unique fields

<details>
<summary><strong>Option A: Single Table Inheritance (CHOSEN)</strong></summary>

```python
class ExperienceDB(Base):
    __tablename__ = "experiences"
    experience_type = Column(SQLEnum(ExperienceType))
    type_specific_data = Column(JSON)  # Type-specific fields

class CertificateDB(ExperienceDB):
    __mapper_args__ = {'polymorphic_identity': ExperienceType.CERTIFICATE}
```

**Pros:**
- ✅ Simple queries (single table)
- ✅ Easy to add new types
- ✅ Referential integrity
- ✅ Good performance

**Cons:**
- ❌ Sparse columns (many NULLs)
- ❌ All types share same table
</details>

<details>
<summary><strong>Option B: Joined Table Inheritance (NOT CHOSEN)</strong></summary>

```python
# experiences table (base)
# certificates table (inherits)
# degrees table (inherits)
# etc.
```

**Pros:**
- ✅ No sparse columns
- ✅ Clear type separation

**Cons:**
- ❌ JOINs required for queries
- ❌ Slower performance
- ❌ More complex migrations
</details>

**Decision:** Single Table Inheritance with JSON for type-specific data

---

### Decision 2: Denormalized NAICS Hierarchy

**Problem:** Need fast queries across NAICS hierarchy levels

<details>
<summary><strong>Normalized vs Denormalized Design</strong></summary>

**Normalized (NOT CHOSEN):**
```python
# Parse code string to determine hierarchy
level = len(code)  # 2, 3, 4, or 6
sector = code[:2]  # Parse on every query
```

**Denormalized (CHOSEN):**
```python
level = Column(Integer, index=True)
sector = Column(String(2), index=True)
subsector = Column(String(3), index=True)
industry_group = Column(String(4), index=True)
```
</details>

**Rationale:**
- ✅ Faster queries (indexed integers vs string parsing)
- ✅ Simple filtering (`WHERE level = 2`)
- ✅ Better query planner optimization
- ❌ Data duplication (minimal, worth it)

---

### Decision 3: JSON Fields for Flexibility

**Problem:** Need flexible storage for:
- User profile data (variable fields)
- Experience type-specific data
- NAICS keywords and aliases

<details>
<summary><strong>Column vs JSON Storage</strong></summary>

**Individual Columns (NOT CHOSEN):**
```python
# For Certificate
certification_number = Column(String)
certification_body = Column(String)
expiration_date = Column(DateTime)
# For Degree
degree_level = Column(String)
major = Column(String)
gpa = Column(Float)
# etc. - leads to sparse table
```

**JSON Storage (CHOSEN):**
```python
type_specific_data = Column(JSON, default=dict)
# Certificate: {"certification_number": "...", "body": "..."}
# Degree: {"degree_level": "...", "major": "...", "gpa": 3.8}
```
</details>

**Rationale:**
- ✅ Schema flexibility
- ✅ No migrations for new fields
- ✅ Clean table design
- ❌ Can't index JSON fields (acceptable)

---

### Decision 4: Direct ORM Models (No Domain Layer)

**Problem:** Should we separate domain models from database models?

<details>
<summary><strong>Design Options</strong></summary>

**Option A: Pure ORM Models (CHOSEN):**
```python
# Use UserDB, ExperienceDB directly
def register_user(...) -> UserDB:
    user = UserDB(username=username, ...)
    return user
```

**Option B: Domain + Database Models (NOT CHOSEN):**
```python
# Separate User (domain) and UserDB (database)
def register_user(...) -> User:
    user = User(username=username, ...)
    user_db = UserMapper.to_db(user)
    return user

class UserMapper:
    @staticmethod
    def to_domain(user_db: UserDB) -> User: ...
    @staticmethod
    def to_db(user: User) -> UserDB: ...
```
</details>

**Decision:** Use ORM models directly

**Rationale:**
- ✅ Simpler codebase (less code)
- ✅ No mapping overhead
- ✅ Easier to maintain
- ❌ Couples business logic to database (acceptable for this project size)

---

## Table Design

### Users Table Design

```sql
CREATE TABLE users (
    -- Identity
    id VARCHAR(32) PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,

    -- Profile
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    is_verified BOOLEAN DEFAULT FALSE NOT NULL,
    profile_data JSONB DEFAULT '{}' NOT NULL,

    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP DEFAULT NOW() NOT NULL,
    last_login TIMESTAMP
);

CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
```

**Design Rationale:**

| Field | Type | Rationale |
|-------|------|-----------|
| `id` | VARCHAR(32) | Hex token (16 bytes = 32 hex chars), random |
| `username` | VARCHAR(50) | Unique, indexed for fast lookups |
| `email` | VARCHAR(255) | Standard max email length, indexed |
| `password_hash` | VARCHAR(255) | Stores bcrypt/PBKDF2 hash |
| `profile_data` | JSONB | Flexible user metadata |

---

### Experiences Table Design

```sql
CREATE TABLE experiences (
    -- Identity
    id VARCHAR(32) PRIMARY KEY,
    user_id VARCHAR(32) REFERENCES users(id) ON DELETE CASCADE NOT NULL,

    -- Core fields
    title VARCHAR(255) NOT NULL,
    description TEXT,
    naics_code VARCHAR(6) DEFAULT '123456' NOT NULL,

    -- Classification
    category VARCHAR(20) NOT NULL,  -- education, workplace, skills
    experience_type VARCHAR(20) NOT NULL,  -- certificate, degree, etc.

    -- Dates
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    is_current BOOLEAN DEFAULT FALSE,

    -- Organization
    organization VARCHAR(255),
    location VARCHAR(255),

    -- Flexible data
    type_specific_data JSONB DEFAULT '{}' NOT NULL,
    tags JSONB DEFAULT '[]' NOT NULL,
    experience_metadata JSONB DEFAULT '{}' NOT NULL,

    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_experiences_user_id ON experiences(user_id);
CREATE INDEX idx_experiences_category ON experiences(category);
CREATE INDEX idx_experiences_type ON experiences(experience_type);
```

**Design Rationale:**

| Feature | Implementation | Rationale |
|---------|----------------|-----------|
| **Polymorphism** | Single table + JSON | Simplicity, performance |
| **Cascade Delete** | `ON DELETE CASCADE` | Auto-cleanup user experiences |
| **NAICS Default** | `DEFAULT '123456'` | Ensure valid NAICS always |
| **JSON Fields** | `type_specific_data` | Flexible type-specific storage |

---

### NAICS Codes Table Design

```sql
CREATE TABLE naics_codes (
    -- Primary key
    code VARCHAR(6) PRIMARY KEY,

    -- Core
    title VARCHAR(500) NOT NULL,
    description TEXT,

    -- Hierarchy
    level INTEGER NOT NULL,
    parent_code VARCHAR(6),
    sector VARCHAR(2),
    subsector VARCHAR(3),
    industry_group VARCHAR(4),
    industry_detail VARCHAR(6),

    -- Categorization
    category VARCHAR(50) NOT NULL,

    -- SBA
    sba_size_standard VARCHAR(255),
    sba_source VARCHAR(255),

    -- Search
    keywords JSONB DEFAULT '[]' NOT NULL,
    aliases JSONB DEFAULT '[]' NOT NULL,
    examples TEXT,

    -- Metadata
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    year INTEGER DEFAULT 2022 NOT NULL,

    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_naics_level ON naics_codes(level);
CREATE INDEX idx_naics_sector ON naics_codes(sector);
CREATE INDEX idx_naics_category ON naics_codes(category);
CREATE INDEX idx_naics_parent ON naics_codes(parent_code);
```

**Denormalization Strategy:**

```
code: "541511" (6 digits)
├── level: 6 (national industry)
├── sector: "54" (Professional Services)
├── subsector: "541" (Professional, Scientific, Technical)
├── industry_group: "5415" (Computer Systems Design)
└── industry_detail: "541511" (Custom Computer Programming)
```

**Benefits:**
- Fast queries: `WHERE level = 2` (sectors only)
- Fast filtering: `WHERE sector = '54'` (all professional services)
- No string parsing needed

---

## Polymorphic Experience Model

### Implementation

```python
# Base model
class ExperienceDB(Base):
    __tablename__ = "experiences"
    experience_type = Column(SQLEnum(ExperienceType))
    # ... other fields

# Subtype models
class CertificateDB(ExperienceDB):
    __mapper_args__ = {'polymorphic_identity': ExperienceType.CERTIFICATE}

class DegreeDB(ExperienceDB):
    __mapper_args__ = {'polymorphic_identity': ExperienceType.DEGREE}

# ... 7 more subtypes
```

### Querying

```python
# Query all experiences (polymorphic)
experiences = db.query(ExperienceDB).all()
# Returns: [CertificateDB, DegreeDB, CourseDB, ...]

# Query specific type
certificates = db.query(CertificateDB).all()
# Returns: [CertificateDB, CertificateDB, ...]

# Filter by type
certs = db.query(ExperienceDB).filter(
    ExperienceDB.experience_type == ExperienceType.CERTIFICATE
).all()
```

---

## NAICS Hierarchy Design

### Hierarchical Structure

```
Level 2 (Sector): "54"
└── Level 3 (Subsector): "541"
    └── Level 4 (Industry Group): "5415"
        └── Level 6 (National Industry): "541511"
```

### Self-Referential Relationship

```python
parent_code = Column(String(6), nullable=True, index=True)

# Query hierarchy
def get_children(code: str):
    return db.query(NAICSCodeDB).filter(
        NAICSCodeDB.parent_code == code
    ).all()

# Example
sector_54 = get_naics("54")
subsectors = get_children("54")  # ["541", "542", "543", ...]
```

### Fast Hierarchy Queries

```python
# Get all sectors (2-digit)
sectors = db.query(NAICSCodeDB).filter(NAICSCodeDB.level == 2).all()

# Get all codes in Professional Services sector
codes = db.query(NAICSCodeDB).filter(NAICSCodeDB.sector == "54").all()

# Get specific subsector
codes = db.query(NAICSCodeDB).filter(NAICSCodeDB.subsector == "541").all()
```

---

## JSON Fields Strategy

### When to Use JSON

✅ **Use JSON for:**
- Variable fields per type
- User-defined metadata
- Lists/arrays (keywords, tags)
- Schema-flexible data

❌ **Don't use JSON for:**
- Frequently queried fields
- Sortable fields
- Fields needing indexes
- Critical business fields

### JSON Field Examples

```python
# Experience type-specific data
Certificate:
  type_specific_data = {
    "certification_number": "ABC123",
    "certifying_body": "AWS",
    "expiration_date": "2025-12-31"
  }

Degree:
  type_specific_data = {
    "degree_level": "Bachelor",
    "major": "Computer Science",
    "gpa": 3.8,
    "honors": ["Dean's List", "Cum Laude"]
  }

# User profile
profile_data = {
  "bio": "Software engineer...",
  "location": "San Francisco",
  "avatar_url": "https://...",
  "social": {
    "github": "username",
    "linkedin": "profile"
  }
}
```

---

## Indexing Strategy

### Primary Indexes

| Table | Field | Type | Rationale |
|-------|-------|------|-----------|
| users | username | UNIQUE | Fast lookups, unique constraint |
| users | email | UNIQUE | Fast lookups, unique constraint |
| experiences | user_id | FOREIGN KEY | Fast user experience queries |
| naics_codes | level | INDEX | Fast hierarchy filtering |
| naics_codes | sector | INDEX | Fast sector queries |
| naics_codes | category | INDEX | Fast category filtering |

### Index Usage

```python
# Indexed query (FAST)
user = db.query(UserDB).filter(UserDB.email == email).first()
# Uses: idx_users_email

# Indexed query (FAST)
experiences = db.query(ExperienceDB).filter(
    ExperienceDB.user_id == user_id
).all()
# Uses: idx_experiences_user_id

# Indexed query (FAST)
sectors = db.query(NAICSCodeDB).filter(NAICSCodeDB.level == 2).all()
# Uses: idx_naics_level
```

---

## Connection Pooling

### Configuration

```python
engine = create_engine(
    database_url,
    poolclass=QueuePool,
    pool_size=5,              # Base pool size
    max_overflow=10,          # Additional connections
    pool_pre_ping=True,       # Verify connections
    echo=settings.debug       # Log SQL in debug
)
```

### Pool Behavior

```
┌──────────────────────────────────────┐
│ Connection Pool (size=5)             │
│ [conn1] [conn2] [conn3] [conn4] [...] │
└──────────────────────────────────────┘
         ↓
┌──────────────────────────────────────┐
│ Overflow Pool (max=10)               │
│ [conn6] [conn7] ... [conn15]         │
└──────────────────────────────────────┘
```

**Behavior:**
1. Request arrives → Pool provides connection
2. Pool empty → Create overflow connection (up to 10)
3. Request completes → Return connection to pool
4. Idle connections → Maintained for reuse

---

## Trade-Offs and Alternatives

### Trade-Off 1: Single Table vs Joined Table Inheritance

**Current: Single Table**
- ✅ Simpler queries
- ✅ Better performance
- ❌ Sparse columns

**Alternative: Joined Tables**
- ✅ No sparse columns
- ❌ Complex JOINs
- ❌ Slower queries

**Decision:** Performance and simplicity win

---

### Trade-Off 2: Denormalized vs Normalized NAICS

**Current: Denormalized**
- ✅ Fast queries
- ✅ Simple filtering
- ❌ Data duplication

**Alternative: Normalized**
- ✅ No duplication
- ❌ String parsing needed
- ❌ Slower queries

**Decision:** Query performance wins

---

### Trade-Off 3: JSON vs Columns

**Current: JSON for variable data**
- ✅ Flexibility
- ✅ No migrations needed
- ❌ Can't index JSON

**Alternative: Many columns**
- ✅ Indexable
- ❌ Sparse table
- ❌ Migration hell

**Decision:** Flexibility wins for variable data

---

## Future Considerations

### Potential Improvements

1. **Database Migrations**
   - Add Alembic for schema versioning
   - Automated migration generation
   - Rollback capability

2. **Read Replicas**
   - Separate read/write connections
   - Scale read operations
   - Reduce primary load

3. **Caching Layer**
   - Redis for frequent queries
   - Cache NAICS lookups
   - Session storage

4. **Full-Text Search**
   - PostgreSQL text search
   - Elasticsearch integration
   - Better experience search

5. **Time-Series Data**
   - User activity tracking
   - Analytics events
   - Separate time-series table

---

## Additional Resources

### Official Documentation

- 📚 [Database Overview](/docs/database/DATABASE_OVERVIEW.md)
- 🏗️ [Schema Reference](/docs/database/SCHEMA_REFERENCE.md)
- 🧪 [Usage Guide](/docs/database/USAGE_GUIDE.md)
- 📖 [Testing Guide](/docs/database/TESTING_DATABASE.md)
- 💻 [Data Models](/docs/database/DATA_MODELS.md)

### External Resources

- 🌐 [SQLAlchemy ORM Tutorial](https://docs.sqlalchemy.org/en/14/orm/tutorial.html)
- 📖 [PostgreSQL Performance](https://www.postgresql.org/docs/current/performance-tips.html)
- 📊 [Database Design Patterns](https://www.postgresql.org/docs/current/ddl.html)

---

## Related Documentation

- **Next:** [Schema Reference](/docs/database/SCHEMA_REFERENCE.md)
- **Previous:** [Database Overview](/docs/database/DATABASE_OVERVIEW.md)

**Other related documentation:**

- [Architecture Comparison](/docs/architecture/COMPARISON.md)
- [MANIFEST](/docs/core/MANIFEST.md)
- [API Documentation](/docs/api/API_DOCUMENTATION.md)

---

## Feedback

Found an issue with this guide? Have suggestions for improvement?

- 👍 **Helpful?** This explains database design decisions
- 🐛 **Found a bug?** [Report it on GitHub](https://github.com/Free-Columns/levelith-2/issues)
- 💡 **Have an idea?** [Start a discussion](https://github.com/Free-Columns/levelith-2/discussions)

---

**Last Updated:** November 20, 2025 | **Version:** 1.0 | **Contributors:** Semour Media Group

---

*This document is part of the Levelith Developer Documentation. For questions, join our [Discord community](https://discord.gg/levelith).*
