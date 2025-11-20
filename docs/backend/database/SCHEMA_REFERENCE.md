# Database Schema Reference

---
title: "Database Schema Reference"
description: "Complete reference documentation for all database schemas including tables, columns, constraints, indexes, and relationships in the Levelith database."
category: "reference"
tags: ["schema", "database", "tables", "reference", "sql"]
author: "Semour Media Group"
date: "2025-11-20"
lastUpdated: "2025-11-20"
difficulty: "intermediate"
readingTime: 20
relatedPages:
  - "/docs/database/DATABASE_OVERVIEW.md"
  - "/docs/database/DATABASE_ARCHITECTURE.md"
  - "/docs/database/DATA_MODELS.md"
nextPage: "/docs/database/USAGE_GUIDE.md"
prevPage: "/docs/database/DATABASE_ARCHITECTURE.md"
searchKeywords:
  - "database schema"
  - "table reference"
  - "column reference"
  - "database structure"
showTOC: true
showBreadcrumbs: true
showLastUpdated: true
version: "1.0"
---

# Database Schema Reference

> **TL;DR:** Complete reference for all 3 database tables (users, experiences, naics_codes) including column specifications, data types, constraints, indexes, relationships, and example SQL queries.

**Difficulty:** 🟡 Intermediate | **Time:** ⏱️ 20 minutes | **Last Updated:** November 20, 2025

---

## Table of Contents

- [Overview](#overview)
- [Users Table](#users-table)
- [Experiences Table](#experiences-table)
- [NAICS Codes Table](#naics-codes-table)
- [Relationships](#relationships)
- [Constraints](#constraints)
- [Indexes](#indexes)
- [Data Types Reference](#data-types-reference)
- [Additional Resources](#additional-resources)

---

## Overview

The Levelith database consists of **3 primary tables**:

| Table | Rows (est.) | Purpose |
|-------|-------------|---------|
| `users` | Variable | User accounts and profiles |
| `experiences` | Variable | Professional experiences (9 types) |
| `naics_codes` | 60+ (expandable) | NAICS 2022 industry classification |

---

## Users Table

### Table Structure

```sql
CREATE TABLE users (
    -- Identity
    id                 VARCHAR(32)  PRIMARY KEY,
    username           VARCHAR(50)  UNIQUE NOT NULL,
    email              VARCHAR(255) UNIQUE NOT NULL,
    password_hash      VARCHAR(255) NOT NULL,
    
    -- Profile
    is_active          BOOLEAN      DEFAULT TRUE NOT NULL,
    is_verified        BOOLEAN      DEFAULT FALSE NOT NULL,
    profile_data       JSONB        DEFAULT '{}' NOT NULL,
    
    -- Timestamps
    created_at         TIMESTAMP    DEFAULT NOW() NOT NULL,
    updated_at         TIMESTAMP    DEFAULT NOW() NOT NULL,
    last_login         TIMESTAMP
);

CREATE UNIQUE INDEX idx_users_username ON users(username);
CREATE UNIQUE INDEX idx_users_email ON users(email);
```

### Column Reference

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| `id` | VARCHAR(32) | NO | `secrets.token_hex(16)` | Unique user identifier (hex) |
| `username` | VARCHAR(50) | NO | - | Unique username (3-50 chars) |
| `email` | VARCHAR(255) | NO | - | Unique email address |
| `password_hash` | VARCHAR(255) | NO | - | Hashed password (PBKDF2/bcrypt) |
| `is_active` | BOOLEAN | NO | TRUE | Account active status |
| `is_verified` | BOOLEAN | NO | FALSE | Email verification status |
| `profile_data` | JSONB | NO | `{}` | Flexible profile metadata |
| `created_at` | TIMESTAMP | NO | NOW() | Account creation timestamp |
| `updated_at` | TIMESTAMP | NO | NOW() | Last update timestamp |
| `last_login` | TIMESTAMP | YES | NULL | Last login timestamp |

### Constraints

- **Primary Key:** `id`
- **Unique:** `username`, `email`
- **Not Null:** `id`, `username`, `email`, `password_hash`, `is_active`, `is_verified`, `profile_data`, `created_at`, `updated_at`

### Profile Data Schema

```json
{
  "bio": "Software engineer passionate about...",
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
    "notifications": true
  }
}
```

### Example Queries

```sql
-- Find user by email
SELECT * FROM users WHERE email = 'user@example.com';

-- Find active users
SELECT * FROM users WHERE is_active = TRUE;

-- Count verified users
SELECT COUNT(*) FROM users WHERE is_verified = TRUE;

-- Recent signups
SELECT * FROM users 
ORDER BY created_at DESC 
LIMIT 10;
```

---

## Experiences Table

### Table Structure

```sql
CREATE TABLE experiences (
    -- Identity
    id                    VARCHAR(32)  PRIMARY KEY,
    user_id               VARCHAR(32)  REFERENCES users(id) ON DELETE CASCADE NOT NULL,
    
    -- Core
    title                 VARCHAR(255) NOT NULL,
    description           TEXT,
    naics_code            VARCHAR(6)   DEFAULT '123456' NOT NULL,
    
    -- Classification
    category              VARCHAR(20)  NOT NULL,
    experience_type       VARCHAR(20)  NOT NULL,
    
    -- Dates
    start_date            TIMESTAMP,
    end_date              TIMESTAMP,
    is_current            BOOLEAN      DEFAULT FALSE,
    
    -- Organization
    organization          VARCHAR(255),
    location              VARCHAR(255),
    
    -- Flexible Data
    type_specific_data    JSONB        DEFAULT '{}' NOT NULL,
    tags                  JSONB        DEFAULT '[]' NOT NULL,
    experience_metadata   JSONB        DEFAULT '{}' NOT NULL,
    
    -- Timestamps
    created_at            TIMESTAMP    DEFAULT NOW() NOT NULL,
    updated_at            TIMESTAMP    DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_experiences_user_id ON experiences(user_id);
CREATE INDEX idx_experiences_category ON experiences(category);
CREATE INDEX idx_experiences_type ON experiences(experience_type);
CREATE INDEX idx_experiences_naics ON experiences(naics_code);
```

### Column Reference

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| `id` | VARCHAR(32) | NO | `token_hex(16)` | Unique experience ID |
| `user_id` | VARCHAR(32) | NO | - | Foreign key to users.id |
| `title` | VARCHAR(255) | NO | - | Experience title |
| `description` | TEXT | YES | NULL | Detailed description |
| `naics_code` | VARCHAR(6) | NO | '123456' | NAICS industry code |
| `category` | VARCHAR(20) | NO | - | education, workplace, skills |
| `experience_type` | VARCHAR(20) | NO | - | 9 specific types |
| `start_date` | TIMESTAMP | YES | NULL | Start date |
| `end_date` | TIMESTAMP | YES | NULL | End date |
| `is_current` | BOOLEAN | NO | FALSE | Currently active |
| `organization` | VARCHAR(255) | YES | NULL | Organization/institution |
| `location` | VARCHAR(255) | YES | NULL | Location |
| `type_specific_data` | JSONB | NO | `{}` | Type-specific fields |
| `tags` | JSONB | NO | `[]` | Searchable tags |
| `experience_metadata` | JSONB | NO | `{}` | Additional metadata |
| `created_at` | TIMESTAMP | NO | NOW() | Creation timestamp |
| `updated_at` | TIMESTAMP | NO | NOW() | Last update |

### Category and Type Enums

**Categories:**
- `education` - Educational experiences
- `workplace` - Work experiences
- `skills` - Skill-based experiences

**Experience Types:**

Education:
- `certificate` - Professional certifications
- `degree` - Academic degrees
- `course` - Individual courses

Workplace:
- `gig` - Short-term contracts
- `part_time` - Part-time employment
- `full_time` - Full-time employment

Skills:
- `soft_skill` - Interpersonal skills
- `hard_skill` - Technical skills
- `native_skill` - Innate abilities/languages

### Type-Specific Data Schemas

**Certificate:**
```json
{
  "certification_number": "ABC123",
  "certifying_body": "AWS",
  "expiration_date": "2025-12-31",
  "is_renewable": true
}
```

**Degree:**
```json
{
  "degree_level": "Bachelor",
  "major": "Computer Science",
  "minor": "Mathematics",
  "gpa": 3.8,
  "honors": ["Dean's List", "Cum Laude"]
}
```

**Full-Time:**
```json
{
  "job_title": "Senior Software Engineer",
  "department": "Engineering",
  "employment_type": "permanent",
  "responsibilities": ["Led team of 5", "Architected system"]
}
```

### Example Queries

```sql
-- Get user's experiences
SELECT * FROM experiences 
WHERE user_id = 'abc123'
ORDER BY start_date DESC;

-- Find all certificates
SELECT * FROM experiences 
WHERE experience_type = 'certificate';

-- Current experiences
SELECT * FROM experiences 
WHERE is_current = TRUE;

-- Experiences in specific industry
SELECT e.*, n.title as industry
FROM experiences e
JOIN naics_codes n ON e.naics_code = n.code
WHERE n.sector = '54';
```

---

## NAICS Codes Table

### Table Structure

```sql
CREATE TABLE naics_codes (
    -- Primary Key
    code                  VARCHAR(6)   PRIMARY KEY,
    
    -- Core
    title                 VARCHAR(500) NOT NULL,
    description           TEXT,
    
    -- Hierarchy
    level                 INTEGER      NOT NULL,
    parent_code           VARCHAR(6),
    sector                VARCHAR(2),
    subsector             VARCHAR(3),
    industry_group        VARCHAR(4),
    industry_detail       VARCHAR(6),
    
    -- Classification
    category              VARCHAR(50)  NOT NULL,
    
    -- SBA
    sba_size_standard     VARCHAR(255),
    sba_source            VARCHAR(255),
    
    -- Search
    keywords              JSONB        DEFAULT '[]' NOT NULL,
    aliases               JSONB        DEFAULT '[]' NOT NULL,
    examples              TEXT,
    cross_references      JSONB        DEFAULT '[]' NOT NULL,
    notes                 TEXT,
    
    -- Admin
    tags                  JSONB        DEFAULT '[]' NOT NULL,
    custom_category       VARCHAR(100),
    admin_notes           TEXT,
    
    -- Metadata
    is_active             BOOLEAN      DEFAULT TRUE NOT NULL,
    year                  INTEGER      DEFAULT 2022 NOT NULL,
    data_source           VARCHAR(255),
    
    -- Timestamps
    created_at            TIMESTAMP    DEFAULT NOW() NOT NULL,
    updated_at            TIMESTAMP    DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_naics_level ON naics_codes(level);
CREATE INDEX idx_naics_sector ON naics_codes(sector);
CREATE INDEX idx_naics_subsector ON naics_codes(subsector);
CREATE INDEX idx_naics_category ON naics_codes(category);
CREATE INDEX idx_naics_parent ON naics_codes(parent_code);
```

### Hierarchy Levels

| Level | Digits | Example | Description |
|-------|--------|---------|-------------|
| 2 | XX | 54 | Sector |
| 3 | XXX | 541 | Subsector |
| 4 | XXXX | 5415 | Industry Group |
| 6 | XXXXXX | 541511 | National Industry |

### NAICS Categories

- AGRICULTURE_FORESTRY_FISHING
- MINING_QUARRYING
- UTILITIES
- CONSTRUCTION
- MANUFACTURING
- WHOLESALE_TRADE
- RETAIL_TRADE
- TRANSPORTATION_WAREHOUSING
- INFORMATION
- FINANCE_INSURANCE
- REAL_ESTATE
- PROFESSIONAL_TECHNICAL_SERVICES
- EDUCATIONAL_SERVICES
- HEALTHCARE

### Example Queries

```sql
-- Get all sectors (2-digit)
SELECT * FROM naics_codes WHERE level = 2 ORDER BY code;

-- Get subsectors of a sector
SELECT * FROM naics_codes 
WHERE parent_code = '54'
ORDER BY code;

-- Search by keyword
SELECT * FROM naics_codes 
WHERE title ILIKE '%software%' 
   OR description ILIKE '%software%';

-- Get hierarchy for a code
WITH RECURSIVE hierarchy AS (
  SELECT * FROM naics_codes WHERE code = '541511'
  UNION ALL
  SELECT n.* FROM naics_codes n
  INNER JOIN hierarchy h ON n.code = h.parent_code
)
SELECT * FROM hierarchy;
```

---

## Relationships

### ER Diagram

```
┌──────────────────┐
│      users       │
│  id (PK)         │
│  username        │
│  email           │
└────────┬─────────┘
         │ 1
         │
         │ has many
         │
         │ N
┌────────┴─────────┐
│   experiences    │
│  id (PK)         │
│  user_id (FK)    │──┐
│  naics_code (FK) │  │
└──────────────────┘  │
         │            │
         │ references │
         │            │
┌────────┴────────────┴─┐
│    naics_codes        │
│  code (PK)            │
│  parent_code (FK,self)│
└───────────────────────┘
```

### Foreign Keys

| Table | Column | References | On Delete |
|-------|--------|------------|-----------|
| experiences | user_id | users(id) | CASCADE |
| experiences | naics_code | naics_codes(code) | (no action) |
| naics_codes | parent_code | naics_codes(code) | (no action) |

---

## Constraints

### Primary Keys

- `users.id` - Unique user identifier
- `experiences.id` - Unique experience identifier
- `naics_codes.code` - NAICS code (6 digits)

### Unique Constraints

- `users.username` - Unique username
- `users.email` - Unique email

### Check Constraints (Future)

```sql
-- Example check constraints (to be added)
ALTER TABLE users ADD CONSTRAINT chk_username_length 
  CHECK (LENGTH(username) >= 3);

ALTER TABLE experiences ADD CONSTRAINT chk_dates 
  CHECK (end_date IS NULL OR end_date >= start_date);

ALTER TABLE naics_codes ADD CONSTRAINT chk_code_length 
  CHECK (LENGTH(code) IN (2, 3, 4, 6));
```

---

## Indexes

### Users Indexes

| Index | Column(s) | Type | Purpose |
|-------|-----------|------|---------|
| PRIMARY | id | BTREE | Primary key lookup |
| idx_users_username | username | BTREE UNIQUE | Username lookups, constraint |
| idx_users_email | email | BTREE UNIQUE | Email lookups, constraint |

### Experiences Indexes

| Index | Column(s) | Type | Purpose |
|-------|-----------|------|---------|
| PRIMARY | id | BTREE | Primary key lookup |
| idx_experiences_user_id | user_id | BTREE | User experience queries |
| idx_experiences_category | category | BTREE | Category filtering |
| idx_experiences_type | experience_type | BTREE | Type filtering |
| idx_experiences_naics | naics_code | BTREE | Industry filtering |

### NAICS Indexes

| Index | Column(s) | Type | Purpose |
|-------|-----------|------|---------|
| PRIMARY | code | BTREE | Primary key lookup |
| idx_naics_level | level | BTREE | Hierarchy level filtering |
| idx_naics_sector | sector | BTREE | Sector filtering |
| idx_naics_subsector | subsector | BTREE | Subsector filtering |
| idx_naics_category | category | BTREE | Category filtering |
| idx_naics_parent | parent_code | BTREE | Parent lookup |

---

## Data Types Reference

### PostgreSQL Types Used

| Type | Usage | Example Values |
|------|-------|----------------|
| VARCHAR(n) | Text with max length | 'username', 'email@example.com' |
| TEXT | Unlimited text | Long descriptions |
| BOOLEAN | True/false | TRUE, FALSE |
| INTEGER | Whole numbers | 2, 3, 4, 6 |
| TIMESTAMP | Date and time | '2025-11-20 10:30:00' |
| JSONB | JSON data (binary) | {"key": "value"} |

### JSONB Performance

**Benefits:**
- Native PostgreSQL type
- Binary storage (faster than JSON)
- Indexable (GIN indexes)
- Query support

**Limitations:**
- Slower than regular columns
- No enforcement of schema
- Harder to optimize

---

## Additional Resources

### Official Documentation

- 📚 [Database Overview](/docs/database/DATABASE_OVERVIEW.md)
- 🏗️ [Database Architecture](/docs/database/DATABASE_ARCHITECTURE.md)
- 🧪 [Usage Guide](/docs/database/USAGE_GUIDE.md)
- 📖 [Data Models](/docs/database/DATA_MODELS.md)

### External Resources

- 🌐 [PostgreSQL Data Types](https://www.postgresql.org/docs/current/datatype.html)
- 📖 [PostgreSQL Indexes](https://www.postgresql.org/docs/current/indexes.html)
- 📊 [JSONB Type](https://www.postgresql.org/docs/current/datatype-json.html)

---

## Feedback

- 👍 **Helpful?** This provides complete schema reference
- 🐛 **Found a bug?** [Report it](https://github.com/Free-Columns/levelith-2/issues)
- 💡 **Have an idea?** [Start a discussion](https://github.com/Free-Columns/levelith-2/discussions)

---

**Last Updated:** November 20, 2025 | **Version:** 1.0 | **Contributors:** Semour Media Group
