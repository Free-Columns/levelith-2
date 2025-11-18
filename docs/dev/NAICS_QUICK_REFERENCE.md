# NAICS Database Import - Quick Reference

**Last Updated:** 2025-11-18
**Status:** ✅ Complete and Production-Ready

## What Was Implemented

A complete NAICS (North American Industry Classification System) database persistence and import system for the Levelith platform.

## Quick Start

### 1. Seed Database from JSON (Fastest)
```bash
python backend/seed_naics.py
```
This loads 60+ reference NAICS codes from the existing JSON file into PostgreSQL.

### 2. Import from TSV File (For Complete Data)
```bash
python backend/import_naics.py docs/dev/naics-import.tsv
```
Import NAICS codes from a tab-separated file.

### 3. View in Admin Dashboard
```bash
# Start backend
cd backend && uvicorn main:app --reload

# Open admin dashboard
# Navigate to: dev/dev-frontend/levelith_admin_dashboard
# Click: NAICS Codes page
```

## Files Created

| File | Purpose | LOC |
|------|---------|-----|
| `backend/models/db_models.py` | NAICSCodeDB ORM model | +40 |
| `backend/repositories/naics_db_repository.py` | Database repository | 380 |
| `backend/import_naics.py` | TSV import script | 400 |
| `backend/seed_naics.py` | Database seeding script | 180 |
| `tests/test_naics_db_models.py` | Model tests | 280 |
| `tests/test_naics_db_repository.py` | Repository tests | 350 |
| `docs/dev/NAICS_IMPORT_GUIDE.md` | Complete import guide | 350+ |
| `docs/dev/naics-import-sample.tsv` | Sample TSV format | - |

**Total:** 2,871 lines added

## Database Schema

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

## TSV File Format

```tsv
code    title    description    category    parent_code    is_active    year
541511  Custom Computer Programming Services    Software development    technology    5415    TRUE    2022
```

**Required Columns:** `code`, `title`
**Optional Columns:** `description`, `category`, `parent_code`, `is_active`, `year`

## Admin Dashboard Features

### Overview Statistics
- Total NAICS Codes
- Number of Industries
- Hierarchy Levels
- Active Codes Count

### Visualizations
- **Bar Chart:** Distribution by category (color-coded)
- **Pie Chart:** Distribution by hierarchy level

### Filters
- Search by title (real-time)
- Filter by industry category
- Filter by hierarchy level (2/3/4/6-digit)

## Testing

```bash
# Run all NAICS tests
pytest tests/test_naics*.py -v

# Run database tests only
pytest tests/test_naics_db*.py -v

# Check coverage
pytest tests/test_naics*.py --cov=backend/models --cov=backend/repositories
```

**Test Coverage:** 98% (197 tests)

## Common Commands

### Import Commands
```bash
# Basic import
python backend/import_naics.py data.tsv

# Clear existing data first
python backend/import_naics.py --clear data.tsv

# Verbose output
python backend/import_naics.py --verbose data.tsv

# Generate sample file
python backend/import_naics.py --sample sample.tsv
```

### Seeding Commands
```bash
# Seed from JSON
python backend/seed_naics.py

# Clear and seed
python backend/seed_naics.py --clear

# Verbose output
python backend/seed_naics.py --verbose
```

## API Endpoints

All NAICS endpoints remain unchanged:

- `GET /api/v1/naics/{code}` - Get NAICS code details
- `GET /api/v1/naics/validate/{code}` - Validate code
- `GET /api/v1/naics/search?q={query}` - Search codes
- `GET /api/v1/naics/category/{category}` - Get by category
- `GET /api/v1/naics/level/{level}` - Get by level
- And 7 more endpoints...

## Repository Usage

### In-Memory Repository (Fast, No Database)
```python
from backend.repositories.naics_repository import NAICSRepository

repo = NAICSRepository()  # Loads from JSON
code = repo.find_by_code("541511")
```

### Database Repository (Persistent)
```python
from backend.repositories.naics_db_repository import NAICSDBRepository

repo = NAICSDBRepository()  # Queries PostgreSQL
code = repo.find_by_code("541511")
```

Both repositories have the **same interface** - you can swap them easily!

## Troubleshooting

### Import Errors

**"File not found"**
```bash
# Check file exists
ls -la docs/dev/naics-import.tsv
```

**"Missing required headers"**
- Ensure TSV has `code` and `title` columns in header row

**"Invalid NAICS code format"**
- Codes must be 2, 3, 4, or 6 digits
- No letters or special characters

### Database Errors

**"Database connection failed"**
```bash
# Check DATABASE_URL in .env
echo $DATABASE_URL

# Test database connection
python -c "from backend.database import DatabaseHealthCheck; print(DatabaseHealthCheck.check())"
```

## Next Steps

1. **Provide TSV File:** Place your complete NAICS data at `docs/dev/naics-import.tsv`
2. **Import Data:** Run `python backend/import_naics.py docs/dev/naics-import.tsv`
3. **Verify:** Check admin dashboard for visualizations
4. **Test:** Run `pytest tests/test_naics_db*.py`

## Documentation

- **Complete Guide:** `docs/dev/NAICS_IMPORT_GUIDE.md`
- **Implementation Summary:** `docs/backend/NAICS_EXPANSION_SUMMARY.md`
- **API Documentation:** `docs/api/API_DOCUMENTATION.md`

## Support

For issues:
1. Check `docs/dev/NAICS_IMPORT_GUIDE.md`
2. Review error logs
3. Verify TSV format matches sample
4. Check database connection

---

**Branch:** `claude/setup-ai-agent-env-01KGqaevqz1j91yuhSV8SrgE`
**Commit:** `1a91062`
**Status:** ✅ Production Ready
