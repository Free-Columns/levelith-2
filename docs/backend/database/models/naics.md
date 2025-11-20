# NAICS Database Model

---
title: "NAICS Database Model"
description: "Complete reference for the NAICSCodeDB model storing NAICS 2022 industry classification with hierarchical structure and enhanced search capabilities."
category: "reference"
tags: ["database", "naics-model", "industry-classification", "hierarchy"]
author: "Semour Media Group"
date: "2025-11-20"
lastUpdated: "2025-11-20"
difficulty: "intermediate"
readingTime: 10
relatedPages:
  - "/docs/backend/database/models/user.md"
  - "/docs/backend/database/models/experience.md"
  - "/docs/backend/naics/NAICS_EXPANSION_SUMMARY.md"
nextPage: "/docs/backend/database/DATA_MODELS.md"
prevPage: "/docs/backend/database/models/experience.md"
searchKeywords:
  - "naics model"
  - "industry classification"
  - "naics codes"
  - "hierarchy"
showTOC: true
showBreadcrumbs: true
showLastUpdated: true
version: "1.0"
---

# NAICS Database Model

> **TL;DR:** NAICSCodeDB stores NAICS 2022 industry classification with 4-level hierarchy (2/3/4/6 digits), denormalized fields for performance, JSON keywords/aliases for search, SBA integration, and self-referential parent relationship.

**Difficulty:** 🟡 Intermediate | **Time:** ⏱️ 10 minutes | **Last Updated:** November 20, 2025

---

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

---

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

---

## Field Reference

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

---

## Categories

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

## Usage Examples

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

---

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

---

## Indexes

| Index | Purpose |
|-------|---------|
| PRIMARY (code) | Fast code lookups |
| idx_naics_level | Fast level filtering (get all sectors) |
| idx_naics_sector | Fast sector queries |
| idx_naics_subsector | Fast subsector queries |
| idx_naics_category | Fast category filtering |
| idx_naics_parent | Fast parent lookups |

---

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

## Related Documentation

- [User Model](user.md)
- [Experience Model](experience.md)
- [NAICS Expansion Summary](/docs/backend/naics/NAICS_EXPANSION_SUMMARY.md)
- [NAICS Import Guide](/docs/backend/naics/NAICS_IMPORT_GUIDE.md)

---

**Last Updated:** November 20, 2025 | **Version:** 1.0
