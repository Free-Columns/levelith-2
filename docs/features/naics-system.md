# NAICS Industry Classification System

> **Complete technical documentation for the NAICS (North American Industry Classification System) implementation in Levelith, covering domain models, database persistence, import tools, and API integration.**

**Status:** ✅ Production Ready | **Test Coverage:** 98% (197 tests) | **Last Updated:** December 8, 2025

---

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [NAICS Hierarchy](#naics-hierarchy)
- [Database Schema](#database-schema)
- [Importing NAICS Data](#importing-naics-data)
  - [TSV File Format](#tsv-file-format)
  - [Import Commands](#import-commands)
  - [Seeding from JSON](#seeding-from-json)
- [API Endpoints](#api-endpoints)
- [Domain Models](#domain-models)
- [Repository Layer](#repository-layer)
- [Service Layer](#service-layer)
- [Admin Dashboard](#admin-dashboard)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)

---

## Overview

The NAICS implementation provides a comprehensive industry classification system for the Levelith platform. It enables users to tag experiences with standardized industry codes, supports intelligent suggestions, and provides analytics across industries.

### Key Features

- ✅ **2222+ Industry Codes** - Complete NAICS 2022 database
- ✅ **Hierarchical Structure** - 4-level taxonomy (Sector → Subsector → Industry Group → National Industry)
- ✅ **Database Persistence** - PostgreSQL storage with indexes
- ✅ **TSV Import System** - Bulk data import with validation
- ✅ **12 REST API Endpoints** - Full CRUD and search capabilities
- ✅ **Smart Suggestions** - Experience-based code recommendations
- ✅ **Admin Dashboard** - Visual analytics and management
- ✅ **98% Test Coverage** - Production-ready reliability

### Tech Stack

- Python 3.11+ (Domain models, validation)
- PostgreSQL (Persistent storage)
- SQLAlchemy (ORM)
- FastAPI (REST API)
- React (Admin dashboard)

---

## Quick Start

### 1. Seed Database with Reference Data

```bash
# Load 60+ reference codes from JSON (fastest)
cd backend
python seed_naics.py
```

**Expected Output:**
```
Loading NAICS codes from JSON...
Found 62 codes
Inserting into database...
✅ Successfully seeded 62 NAICS codes
⏱️  Completed in 0.8 seconds
```

### 2. Import Complete Dataset (Optional)

```bash
# Import comprehensive NAICS data from TSV
python import_naics.py docs/dev/naics-import.tsv
```

### 3. Verify Installation

```bash
# Start backend
uvicorn main:app --reload

# Test API
curl http://localhost:8000/api/v1/naics/541511
```

### 4. View in Admin Dashboard

Navigate to the admin dashboard at `/admin/naics` to browse codes, view analytics, and manage data.

---

## NAICS Hierarchy

NAICS codes follow a 4-level hierarchical structure with increasing specificity:

```
┌──────────────────────────────────────────────┐
│  2-digit (Sector) - Broadest Level           │
│  Example: "54" = Professional Services       │
└──────────────┬───────────────────────────────┘
               ↓
┌──────────────────────────────────────────────┐
│  3-digit (Subsector) - More Specific         │
│  Example: "541" = Professional, Scientific   │
└──────────────┬───────────────────────────────┘
               ↓
┌──────────────────────────────────────────────┐
│  4-digit (Industry Group) - Even More        │
│  Example: "5415" = Computer Systems Design   │
└──────────────┬───────────────────────────────┘
               ↓
┌──────────────────────────────────────────────┐
│  6-digit (National Industry) - Most Specific │
│  Example: "541511" = Custom Programming      │
└──────────────────────────────────────────────┘
```

### Hierarchy Levels

| Digits | Level | Description | Example |
|--------|-------|-------------|---------|
| 2 | Sector | Broadest industry category | 54 - Professional Services |
| 3 | Subsector | Subdivision of sector | 541 - Professional, Scientific, Technical |
| 4 | Industry Group | Specific industry group | 5415 - Computer Systems Design |
| 6 | National Industry | Most specific classification | 541511 - Custom Programming |

### Valid Categories

NAICS codes are organized into 14 industry categories:

- `technology` - Software, IT, computer services
- `education` - Schools, training, certifications
- `healthcare` - Medical, hospitals, diagnostics
- `finance` - Banking, insurance, securities
- `manufacturing` - Production, assembly
- `retail` - Stores, e-commerce
- `hospitality` - Hotels, restaurants, tourism
- `construction` - Building, infrastructure
- `agriculture` - Farming, forestry, fishing
- `transportation` - Logistics, shipping
- `professional_services` - Consulting, legal, accounting
- `arts_entertainment` - Media, arts, sports
- `public_administration` - Government services
- `general` - Fallback for uncategorized

---

## Database Schema

### Table: `naics_codes`

```sql
CREATE TABLE naics_codes (
    code VARCHAR(6) PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    level INTEGER NOT NULL,
    category VARCHAR(50) NOT NULL,
    parent_code VARCHAR(6),
    is_active BOOLEAN DEFAULT TRUE,
    year INTEGER DEFAULT 2022,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_naics_category ON naics_codes(category);
CREATE INDEX idx_naics_level ON naics_codes(level);
CREATE INDEX idx_naics_parent ON naics_codes(parent_code);
```

### Schema Fields

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `code` | VARCHAR(6) | PRIMARY KEY | NAICS code (2-6 digits) |
| `title` | VARCHAR(500) | NOT NULL | Official industry title |
| `description` | TEXT | - | Detailed description |
| `level` | INTEGER | NOT NULL | Hierarchy level (2, 3, 4, or 6) |
| `category` | VARCHAR(50) | NOT NULL | Industry category |
| `parent_code` | VARCHAR(6) | - | Parent code in hierarchy |
| `is_active` | BOOLEAN | DEFAULT TRUE | Active status |
| `year` | INTEGER | DEFAULT 2022 | NAICS version year |
| `created_at` | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| `updated_at` | TIMESTAMP | DEFAULT NOW() | Last update timestamp |

### Database Indexes

Three indexes are automatically created for performance:

1. **Category Index** (`idx_naics_category`) - Fast filtering by industry category
2. **Level Index** (`idx_naics_level`) - Fast queries by hierarchy level
3. **Parent Index** (`idx_naics_parent`) - Fast parent-child relationship queries

---

## Importing NAICS Data

### TSV File Format

The import system accepts tab-separated values (TSV) files with the following structure:

#### Required Columns

| Column | Type | Description |
|--------|------|-------------|
| `code` | string | NAICS code (2, 3, 4, or 6 digits) |
| `title` | string | Official industry title |

#### Optional Columns

| Column | Type | Default | Description |
|--------|------|---------|-------------|
| `description` | text | - | Detailed description |
| `category` | string | `general` | Industry category |
| `parent_code` | string | - | Parent NAICS code |
| `is_active` | boolean | `TRUE` | Active status |
| `year` | integer | `2022` | NAICS version year |

#### Sample TSV File

```tsv
code	title	description	category	parent_code	is_active	year
11	Agriculture, Forestry, Fishing and Hunting	Establishments primarily engaged in growing crops...	agriculture		TRUE	2022
111	Crop Production	Establishments engaged in growing crops	agriculture	11	TRUE	2022
541511	Custom Computer Programming Services	Establishments primarily engaged in writing software	technology	5415	TRUE	2022
```

### Import Commands

#### Basic Import

```bash
python backend/import_naics.py data.tsv
```

Imports NAICS codes from the specified TSV file with automatic validation and batch processing.

#### Clear Existing Data and Import

```bash
python backend/import_naics.py --clear data.tsv
```

⚠️ **Warning:** This will delete ALL existing NAICS codes before importing. Always backup first!

#### Verbose Output

```bash
python backend/import_naics.py --verbose data.tsv
```

Shows detailed progress for each row being processed.

#### Generate Sample File

```bash
python backend/import_naics.py --sample sample.tsv
```

Creates a new sample TSV file with example data and proper formatting.

### Seeding from JSON

For quick development setup, seed from the included JSON reference data:

```bash
# Basic seed
python backend/seed_naics.py

# Clear and seed
python backend/seed_naics.py --clear

# Verbose output
python backend/seed_naics.py --verbose
```

This loads 60+ reference codes from `backend/data/naics_codes_2022.json`.

### Import Process

The import system follows these steps:

1. **Validate Database Connection** - Checks PostgreSQL connectivity
2. **Create Tables if Needed** - Ensures schema exists
3. **Validate TSV Format** - Checks headers and data types
4. **Normalize NAICS Codes** - Removes whitespace, validates format
5. **Determine Hierarchy Levels** - Auto-detects level from code length
6. **Handle Duplicates** - Skips or updates as configured
7. **Batch Insert** - Processes 100 rows per batch for performance
8. **Provide Statistics** - Reports success/error counts and timing

### Validation Rules

#### Code Format

- ✅ Must be 2, 3, 4, or 6 digits
- ❌ Cannot be 1, 5, or 7+ digits
- ❌ No letters or special characters

#### Required Fields

- ✅ `code` must be present and valid
- ✅ `title` must be present and non-empty

#### Category Values

Must be one of the 14 valid categories listed above. Invalid categories will be rejected.

---

## API Endpoints

### Core Endpoints

**Get NAICS Code Details**
```
GET /api/v1/naics/{code}
```

Returns complete metadata for a specific NAICS code.

**Example:**
```bash
curl http://localhost:8000/api/v1/naics/541511
```

**Response:**
```json
{
  "code": "541511",
  "title": "Custom Computer Programming Services",
  "description": "Software development services",
  "level": 6,
  "category": "technology",
  "parent_code": "5415",
  "is_active": true,
  "year": 2022,
  "hierarchy": ["54", "541", "5415", "541511"]
}
```

---

**Validate NAICS Code**
```
GET /api/v1/naics/validate/{code}
```

Checks if a code is valid and returns metadata if it exists.

**Example:**
```bash
curl http://localhost:8000/api/v1/naics/validate/541511
```

**Response:**
```json
{
  "is_valid": true,
  "code": "541511",
  "message": "Valid NAICS code",
  "naics": { /* full metadata */ }
}
```

---

### Search Endpoints

**Search by Keywords**
```
GET /api/v1/naics/search?q={query}&limit={limit}
```

Searches NAICS codes by title and description.

**Example:**
```bash
curl "http://localhost:8000/api/v1/naics/search?q=computer%20programming&limit=10"
```

---

**Autocomplete**
```
GET /api/v1/naics/autocomplete?q={partial}&limit={limit}
```

Provides autocomplete suggestions for partial code or title matches.

---

**Suggest for Experience**
```
GET /api/v1/naics/suggest/experience/{type}?title={title}&limit={limit}
```

Suggests NAICS codes based on experience type and title.

**Experience Types:**
- `certificate`, `degree`, `course` (Education)
- `full_time`, `part_time`, `gig` (Workplace)
- `soft_skill`, `hard_skill`, `native_skill` (Skills)

**Example:**
```bash
curl "http://localhost:8000/api/v1/naics/suggest/experience/full_time?title=Software%20Engineer"
```

---

### Hierarchy Endpoints

**Get Hierarchy Path**
```
GET /api/v1/naics/{code}/hierarchy
```

Returns the full hierarchy from sector to the specified code.

**Example:**
```bash
curl http://localhost:8000/api/v1/naics/541511/hierarchy
```

**Response:**
```json
{
  "hierarchy": [
    { "code": "54", "title": "Professional Services", "level": 2 },
    { "code": "541", "title": "Professional, Scientific", "level": 3 },
    { "code": "5415", "title": "Computer Systems Design", "level": 4 },
    { "code": "541511", "title": "Custom Programming", "level": 6 }
  ]
}
```

---

**Get Child Codes**
```
GET /api/v1/naics/{code}/children
```

Returns all direct child codes of the specified parent.

---

**Get Parent Code**
```
GET /api/v1/naics/{code}/parent
```

Returns the immediate parent code.

---

### Filtering Endpoints

**Get by Category**
```
GET /api/v1/naics/category/{category}?limit={limit}
```

Returns all codes in a specific industry category.

---

**Get by Level**
```
GET /api/v1/naics/level/{level}?limit={limit}
```

Returns all codes at a specific hierarchy level (2, 3, 4, or 6).

---

**Category Summary Statistics**
```
GET /api/v1/naics/categories/summary
```

Returns statistics about code distribution across categories.

---

**List All Categories**
```
GET /api/v1/naics/categories/list
```

Returns a list of all valid NAICS categories.

---

## Domain Models

### NAICSCode Dataclass

**File:** `backend/models/naics.py`

Core domain model representing a NAICS industry code.

```python
from dataclasses import dataclass
from enum import Enum

@dataclass
class NAICSCode:
    code: str
    title: str
    description: str = ""
    level: NAICSLevel = NAICSLevel.NATIONAL_INDUSTRY
    category: NAICSCategory = NAICSCategory.GENERAL
    parent_code: Optional[str] = None
    is_active: bool = True
    year: int = 2022

    def get_hierarchy(self) -> List[str]:
        """Returns full hierarchy path"""

    def is_parent_of(self, child_code: str) -> bool:
        """Check if this code is parent of another"""

    def is_child_of(self, parent_code: str) -> bool:
        """Check if this code is child of another"""
```

### Enums

**NAICSLevel Enum**
```python
class NAICSLevel(IntEnum):
    SECTOR = 2              # 2-digit codes
    SUBSECTOR = 3           # 3-digit codes
    INDUSTRY_GROUP = 4      # 4-digit codes
    NATIONAL_INDUSTRY = 6   # 6-digit codes
```

**NAICSCategory Enum**
```python
class NAICSCategory(str, Enum):
    TECHNOLOGY = "technology"
    EDUCATION = "education"
    HEALTHCARE = "healthcare"
    FINANCE = "finance"
    MANUFACTURING = "manufacturing"
    RETAIL = "retail"
    HOSPITALITY = "hospitality"
    CONSTRUCTION = "construction"
    AGRICULTURE = "agriculture"
    TRANSPORTATION = "transportation"
    PROFESSIONAL_SERVICES = "professional_services"
    ARTS_ENTERTAINMENT = "arts_entertainment"
    PUBLIC_ADMINISTRATION = "public_administration"
    GENERAL = "general"
```

### Validation Functions

**Normalize Code**
```python
def normalize_naics_code(code: str) -> str:
    """Removes whitespace and validates format"""
```

**Get Level**
```python
def get_naics_level(code: str) -> NAICSLevel:
    """Determines hierarchy level from code length"""
```

**Extract Parent**
```python
def extract_parent_codes(code: str) -> List[str]:
    """Returns all parent codes in hierarchy"""
```

---

## Repository Layer

Two repository implementations provide the same interface:

### In-Memory Repository

**File:** `backend/repositories/naics_repository.py`

Fast, JSON-based repository for development and testing.

```python
from backend.repositories.naics_repository import NAICSRepository

repo = NAICSRepository()

# Find by code (O(1))
code = repo.find_by_code("541511")

# Find by category (O(k))
tech_codes = repo.find_by_category(NAICSCategory.TECHNOLOGY)

# Search by title (O(n+m))
results = repo.search_by_title("computer", limit=10)

# Get children (O(n))
children = repo.get_children("5415")

# Get hierarchy (O(d))
hierarchy = repo.get_hierarchy("541511")
```

### Database Repository

**File:** `backend/repositories/naics_db_repository.py`

PostgreSQL-backed repository for production use.

```python
from backend.repositories.naics_db_repository import NAICSDBRepository

repo = NAICSDBRepository()

# Same interface as in-memory repository
code = repo.find_by_code("541511")
tech_codes = repo.find_by_category(NAICSCategory.TECHNOLOGY)

# Additional database-specific methods
summary = repo.get_summary_by_level()
bulk_insert = repo.bulk_insert(codes)
```

Both repositories provide:
- `find_by_code(code)` - Direct lookup
- `find_by_category(category)` - Category filtering
- `find_by_level(level)` - Level filtering
- `search_by_title(query, limit)` - Keyword search
- `get_children(parent_code)` - Child codes
- `get_parent(code)` - Parent code
- `get_hierarchy(code)` - Full hierarchy path
- `is_valid_code(code)` - Validation

---

## Service Layer

**File:** `backend/services/naics_service.py`

Business logic and intelligent suggestions.

```python
from backend.services.naics_service import NAICSService

service = NAICSService(naics_repo=repo)

# Lookup and validation
naics = service.lookup_code("541511")
is_valid, code = service.validate_code("541511")
validation = service.validate_with_metadata("541511")

# Search and autocomplete
results = service.search("computer programming", limit=10)
suggestions = service.autocomplete("5415", limit=5)

# Experience-based suggestions
codes = service.suggest_for_experience(
    experience_type="full_time",
    title="Software Engineer",
    limit=5
)

# Filtering
tech_codes = service.get_by_category("technology")
sector_codes = service.get_by_level(2)

# Hierarchy
hierarchy = service.get_hierarchy("541511")
summary = service.get_categories_summary()
```

### Experience Type Mapping

The service intelligently maps experience types to relevant NAICS categories:

| Experience Type | Suggested Categories |
|----------------|---------------------|
| certificate, degree, course | education, professional_services |
| full_time, part_time, gig | technology, finance, healthcare, manufacturing |
| soft_skill, hard_skill, native_skill | general (fallback) |

---

## Admin Dashboard

The admin dashboard provides a visual interface for browsing and managing NAICS codes.

### Features

**Overview Statistics:**
- 📊 Total NAICS Codes
- 🏭 Number of Industries (categories)
- 📏 Hierarchy Levels
- ✅ Active Codes Count

**Visualizations:**
- **Bar Chart** - Distribution by category (color-coded)
- **Pie Chart** - Distribution by hierarchy level

**Filters:**
- 🔍 Search by title (real-time)
- 📂 Filter by category
- 📏 Filter by level (2/3/4/6-digit)

**Table View:**
- Sortable columns
- Pagination (50 per page)
- Code, title, category, level display

### Accessing the Dashboard

1. Start the admin dashboard frontend
2. Navigate to `/admin/naics`
3. Browse codes, view analytics, apply filters

---

## Testing

### Test Coverage

**Overall: 98% (197 tests)**

| Component | File | Tests | Coverage |
|-----------|------|-------|----------|
| Domain Model | `test_naics.py` | 47 | 100% |
| In-Memory Repository | `test_naics_repository.py` | 40 | 100% |
| Database Model | `test_naics_db_models.py` | 20 | 100% |
| Database Repository | `test_naics_db_repository.py` | 25 | 95% |
| Service Layer | `test_naics_service.py` | 30 | 95% |
| API Endpoints | `test_api_naics.py` | 35 | 100% |

### Running Tests

```bash
# Run all NAICS tests
pytest tests/test_naics*.py -v

# Run with coverage
pytest tests/test_naics*.py --cov=backend --cov-report=html

# Run specific test file
pytest tests/test_naics_repository.py -v

# Run database tests only
pytest tests/test_naics_db*.py -v
```

### Test Categories

- ✅ Unit tests for domain models
- ✅ Integration tests for repository
- ✅ Service layer business logic tests
- ✅ API endpoint tests
- ✅ Error handling tests
- ✅ Validation tests
- ✅ Hierarchical operation tests
- ✅ Search functionality tests

---

## Troubleshooting

### Import Issues

**Error: "File not found"**

Check the file path and use absolute paths if needed:
```bash
ls -la docs/dev/naics-import.tsv
python backend/import_naics.py /full/path/to/file.tsv
```

---

**Error: "Missing required headers"**

Ensure the TSV file has `code` and `title` columns in the first row, separated by tabs (not spaces).

---

**Error: "Invalid NAICS code format"**

Valid formats: 2, 3, 4, or 6 digits only. No letters, special characters, or invalid lengths (1, 5, 7+ digits).

---

### Database Issues

**Error: "Database connection failed"**

Check your DATABASE_URL:
```bash
echo $DATABASE_URL
pg_isready
psql $DATABASE_URL -c "SELECT 1;"
```

---

**Error: "Table does not exist"**

Run database migrations:
```bash
cd backend
python -m alembic upgrade head
```

---

### API Issues

**404 on NAICS endpoints**

Verify the API is running and the NAICS router is registered:
```bash
curl http://localhost:8000/health
curl http://localhost:8000/docs  # Check Swagger UI
```

---

## Best Practices

### Import Best Practices

✅ **DO:**
- Backup database before using `--clear`
- Validate TSV format before importing
- Test on development database first
- Keep TSV files in version control
- Review import statistics after completion

❌ **DON'T:**
- Use spaces instead of tabs in TSV files
- Forget to include headers in TSV files
- Run `--clear` without backups
- Ignore error messages during import

### Code Usage Best Practices

✅ **DO:**
- Use the service layer for business logic
- Validate codes before storing in experiences
- Cache frequently accessed codes
- Use appropriate hierarchy level for your use case
- Leverage experience-based suggestions

❌ **DON'T:**
- Access repository directly from controllers
- Hard-code NAICS codes in application logic
- Skip validation when accepting user input
- Forget to handle parent-child relationships

---

## Additional Resources

### Official NAICS Resources

- [U.S. Census Bureau NAICS](https://www.census.gov/naics/)
- [NAICS 2022 Manual](https://www.census.gov/naics/?58967?yearbck=2022)
- [Bureau of Labor Statistics NAICS](https://www.bls.gov/bls/naics.htm)

### Related Documentation

- [API Documentation](/docs/api/API_DOCUMENTATION.md)
- [Database Guide](/docs/backend/database/DATABASE_OVERVIEW.md)
- [Admin Dashboard](/docs/features/admin-dashboard.md)
- [MVP Guide](/MVP_GUIDE.md)

---

**Last Updated:** December 8, 2025 | **Version:** 3.0 | **NAICS Version:** 2022 | **Maintained By:** Semour Media Group
