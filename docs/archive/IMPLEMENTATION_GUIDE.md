# Enhanced NAICS Search System - Implementation Guide

## Overview

This guide covers the complete implementation of an enhanced NAICS code search system that leverages keywords, aliases, and advanced search capabilities for the Levilith platform.

## What's New

Your database has **22 columns** in the `naics_codes` table, but your ORM models only defined 13. The missing 9 columns provide powerful search and categorization capabilities:

### Denormalized Hierarchy (4 columns)
- `sector` - 2-digit sector code
- `subsector` - 3-digit subsector code
- `industry_group` - 4-digit industry group code
- `industry_detail` - 6-digit national industry code

**Benefit**: Fast queries without string parsing

### SBA Integration (2 columns)
- `sba_size_standard` - Small Business Administration size classifications
- `sba_source` - Source reference for SBA data

**Benefit**: Business size/eligibility information

### Enhanced Search (3 columns)
- `keywords` - JSON array of searchable terms
- `aliases` - JSON array of alternative names/synonyms
- `examples` - Text examples of businesses in this category

**Benefit**: Much better search accuracy and user experience

---

## Implementation Steps

### Step 1: Update Your Models

#### Replace NAICSCodeDB in `backend/models/db_models.py`

```python
# Use the updated model from: db_models_naics_updated.py
```

**Key additions**:
- All 22 database columns defined
- Proper indexing on hierarchy fields
- Documentation for each field group

#### Update NAICSCode Domain Model in `backend/models/naics.py`

Add these fields to your dataclass:

```python
@dataclass
class NAICSCode:
    # ... existing fields ...
    
    # Add these:
    sector: Optional[str] = None
    subsector: Optional[str] = None
    industry_group: Optional[str] = None
    industry_detail: Optional[str] = None
    
    sba_size_standard: Optional[str] = None
    sba_source: Optional[str] = None
    
    keywords: List[str] = field(default_factory=list)
    aliases: List[str] = field(default_factory=list)
    examples: Optional[str] = None
    
    cross_references: List[str] = field(default_factory=list)
    notes: Optional[str] = None
    data_source: Optional[str] = None
```

**Helper methods to add**:
- `get_all_search_terms()` - Combines title, keywords, aliases
- `matches_search_term(term)` - Check if code matches a search term

### Step 2: Update Repository Layer

Update `backend/repositories/naics_db_repository.py` to handle new fields:

```python
def _db_to_domain(self, db_code: NAICSCodeDB) -> NAICSCode:
    """Convert database model to domain model."""
    naics_code = create_naics_code(...)
    
    # Add new fields
    naics_code.sector = db_code.sector
    naics_code.subsector = db_code.subsector
    naics_code.industry_group = db_code.industry_group
    naics_code.industry_detail = db_code.industry_detail
    
    naics_code.sba_size_standard = db_code.sba_size_standard
    naics_code.sba_source = db_code.sba_source
    
    naics_code.keywords = db_code.keywords or []
    naics_code.aliases = db_code.aliases or []
    naics_code.examples = db_code.examples
    
    naics_code.cross_references = db_code.cross_references or []
    naics_code.notes = db_code.notes
    naics_code.data_source = db_code.data_source
    
    return naics_code
```

### Step 3: Add Enhanced Search Service

Create new file: `backend/services/enhanced_naics_search.py`

```python
# Use the complete implementation from: enhanced_naics_search.py
```

**Key features**:
- **Multi-field search** with relevance scoring (0-100 scale)
- **Match type identification** (code, title, keyword, alias, description)
- **Autocomplete** with intelligent suggestions
- **Keyword-based search** (match ALL or ANY keywords)
- **Alias search** (exact or partial)
- **Related codes discovery** using cross-references and hierarchy

### Step 4: Create API Endpoints

Add to `backend/api/routes/` or update existing NAICS routes:

```python
# Use the complete implementation from: naics_search_api_routes.py
```

**New endpoints**:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/naics/search` | POST | Advanced search with relevance ranking |
| `/api/naics/autocomplete` | GET | Intelligent autocomplete suggestions |
| `/api/naics/keywords/{keywords}` | GET | Search by keywords |
| `/api/naics/alias/{alias}` | GET | Find codes by alias |
| `/api/naics/{code}/related` | GET | Get related NAICS codes |
| `/api/naics/categories` | GET | List all categories |
| `/api/naics/stats/keywords` | GET | Keyword statistics |

### Step 5: Populate Keywords & Aliases

Use the utility script to populate your data:

```bash
# Dry run - see what would change
python -m backend.utils.populate_naics_keywords keywords

# Actually populate keywords
python -m backend.utils.populate_naics_keywords keywords --commit

# Populate predefined aliases
python -m backend.utils.populate_naics_keywords aliases --commit

# Add custom alias
python -m backend.utils.populate_naics_keywords add-alias \
  --code 541511 \
  --alias "App Development" \
  --commit

# Validate data
python -m backend.utils.populate_naics_keywords validate
```

---

## Search Examples

### Example 1: Advanced Search

**Request**:
```bash
POST /api/naics/search
{
  "query": "software development",
  "category": "technology",
  "limit": 10,
  "min_score": 50.0
}
```

**Response**:
```json
{
  "query": "software development",
  "total_results": 8,
  "took_ms": 45.2,
  "results": [
    {
      "code": "541511",
      "title": "Custom Computer Programming Services",
      "category": "technology",
      "level": 6,
      "score": 85.0,
      "match_type": "title_contains",
      "matched_terms": ["Custom Computer Programming Services"],
      "keywords": ["software", "programming", "development", "custom", "applications"],
      "aliases": ["Software Development", "App Development", "Custom Software"]
    },
    ...
  ]
}
```

### Example 2: Autocomplete

**Request**:
```bash
GET /api/naics/autocomplete?q=soft&limit=5
```

**Response**:
```json
[
  {
    "code": "541511",
    "title": "Custom Computer Programming Services",
    "category": "technology",
    "level": 6,
    "match_type": "title_prefix",
    "score": 80.0,
    "aliases": ["Software Development", "Custom Software"],
    "keywords": ["software", "programming", "development"]
  },
  {
    "code": "518210",
    "title": "Data Processing, Hosting, and Related Services",
    "category": "technology",
    "level": 6,
    "match_type": "alias_contains",
    "score": 55.0,
    "aliases": ["Cloud Computing", "SaaS"],
    "keywords": ["data", "processing", "hosting", "cloud"]
  }
]
```

### Example 3: Keyword Search

**Request**:
```bash
GET /api/naics/keywords/software,programming,development?match_all=false&limit=15
```

Finds all codes that match ANY of the keywords: software OR programming OR development

### Example 4: Related Codes

**Request**:
```bash
GET /api/naics/541511/related?max_results=8
```

**Response**:
```json
{
  "source_code": "541511",
  "source_title": "Custom Computer Programming Services",
  "related": [
    {
      "code": "541512",
      "title": "Computer Systems Design Services",
      "reason": "same_subsector"
    },
    {
      "code": "518210",
      "title": "Data Processing, Hosting, and Related Services",
      "reason": "cross_reference"
    },
    ...
  ]
}
```

---

## Relevance Scoring

The search system uses a prioritized scoring algorithm:

| Match Type | Score | Description |
|------------|-------|-------------|
| exact_code | 100 | Code exactly matches query |
| code_prefix | 90 | Code starts with query |
| exact_title | 85 | Title exactly matches query |
| title_prefix | 80 | Title starts with query |
| exact_alias | 75 | Alias exactly matches query |
| exact_keyword | 70 | Keyword exactly matches query |
| title_contains | 60 | Title contains query |
| alias_contains | 55 | Alias contains query |
| keyword_contains | 50 | Keyword contains query |
| description_contains | 40 | Description contains query |

This ensures the most relevant results appear first.

---

## Performance Optimization

### Database Indexes

Your current indexes:
```sql
-- Already indexed:
CREATE INDEX ix_naics_codes_category ON naics_codes(category);
CREATE INDEX ix_naics_codes_level ON naics_codes(level);
CREATE INDEX ix_naics_codes_parent_code ON naics_codes(parent_code);

-- Add these for better performance:
CREATE INDEX ix_naics_codes_sector ON naics_codes(sector);
CREATE INDEX ix_naics_codes_subsector ON naics_codes(subsector);
CREATE INDEX ix_naics_codes_industry_group ON naics_codes(industry_group);

-- For JSON keyword/alias search (PostgreSQL only):
CREATE INDEX ix_naics_codes_keywords_gin ON naics_codes USING GIN (keywords);
CREATE INDEX ix_naics_codes_aliases_gin ON naics_codes USING GIN (aliases);
```

### Query Optimization Tips

1. **Use denormalized hierarchy fields** instead of string parsing:
   ```python
   # Good
   codes = db.query(NAICSCodeDB).filter_by(sector="54").all()
   
   # Slower
   codes = db.query(NAICSCodeDB).filter(NAICSCodeDB.code.like("54%")).all()
   ```

2. **Leverage GIN indexes** for JSON array searches:
   ```python
   # Efficient with GIN index
   codes = db.query(NAICSCodeDB).filter(
       NAICSCodeDB.keywords.op('@>')('"software"')
   ).all()
   ```

3. **Cache frequently accessed codes** (sector level, popular industries)

---

## Data Population Strategy

### Automatic Keywords

The utility script extracts keywords from titles and descriptions:

```
"Custom Computer Programming Services"
→ ["custom", "computer", "programming", "services"]
```

### Predefined Aliases

100+ common industries have predefined aliases:

```python
"541511": [
    "Software Development",
    "Custom Software", 
    "Application Development",
    "Software Engineering",
    "IT Development"
]
```

### Manual Curation

Add domain-specific aliases:

```bash
python -m backend.utils.populate_naics_keywords add-alias \
  --code 541511 \
  --alias "SaaS Development" \
  --commit
```

### Validation

```bash
python -m backend.utils.populate_naics_keywords validate
```

Checks:
- Coverage percentages
- Invalid keywords/aliases
- Data quality issues

---

## Frontend Integration

### Autocomplete Component

```javascript
// React example
const NAICSAutocomplete = () => {
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState([]);

  const handleSearch = async (value) => {
    if (value.length < 2) return;
    
    const response = await fetch(
      `/api/naics/autocomplete?q=${encodeURIComponent(value)}&limit=10`
    );
    const data = await response.json();
    setSuggestions(data);
  };

  return (
    <Autocomplete
      options={suggestions}
      getOptionLabel={(option) => `${option.code}: ${option.title}`}
      renderOption={(props, option) => (
        <li {...props}>
          <div>
            <strong>{option.code}</strong>: {option.title}
            {option.aliases.length > 0 && (
              <div className="text-sm text-gray-600">
                Also: {option.aliases.join(', ')}
              </div>
            )}
          </div>
        </li>
      )}
      onInputChange={(_, value) => {
        setQuery(value);
        handleSearch(value);
      }}
    />
  );
};
```

### Search Results Display

```javascript
const NAICSSearchResults = ({ results }) => {
  return (
    <div>
      {results.map((result) => (
        <div key={result.code} className="result-card">
          <div className="flex justify-between">
            <h3>{result.code}: {result.title}</h3>
            <span className="badge">Score: {result.score}</span>
          </div>
          
          <p>{result.description}</p>
          
          {result.aliases.length > 0 && (
            <div>
              <strong>Also known as:</strong> {result.aliases.join(', ')}
            </div>
          )}
          
          {result.keywords.length > 0 && (
            <div className="tags">
              {result.keywords.map((keyword) => (
                <span key={keyword} className="tag">{keyword}</span>
              ))}
            </div>
          )}
          
          <div className="match-info text-sm">
            Matched: {result.match_type} ({result.matched_terms.join(', ')})
          </div>
        </div>
      ))}
    </div>
  );
};
```

---

## Testing

### Unit Tests

```python
def test_keyword_extraction():
    text = "Custom Computer Programming Services and Software Development"
    keywords = extract_keywords_from_text(text, max_keywords=5)
    
    assert "custom" in keywords
    assert "computer" in keywords
    assert "programming" in keywords
    assert "and" not in keywords  # Stopword removed

def test_search_relevance():
    search = EnhancedNAICSSearch()
    
    results = search.search("software", limit=10)
    
    # Higher scored results come first
    assert results[0].score >= results[1].score
    
    # Software-related codes should appear
    codes = [r.naics_code.code for r in results]
    assert "541511" in codes

def test_autocomplete():
    search = EnhancedNAICSSearch()
    
    suggestions = search.autocomplete("soft", limit=5)
    
    assert len(suggestions) <= 5
    assert all("soft" in s["title"].lower() for s in suggestions)
```

### Integration Tests

```python
def test_api_search(client):
    response = client.post("/api/naics/search", json={
        "query": "software",
        "limit": 10
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["total_results"] > 0
    assert len(data["results"]) <= 10

def test_api_autocomplete(client):
    response = client.get("/api/naics/autocomplete?q=comp&limit=5")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) <= 5
```

---

## Migration from Old System

If you need to create a migration to sync the model with the database:

```bash
# Generate migration detecting differences
alembic revision --autogenerate -m "add_missing_naics_fields"

# Review the generated migration
# Edit if needed to ensure it only adds columns, doesn't drop data

# Apply migration
alembic upgrade head
```

---

## Monitoring & Analytics

Track search performance:

```python
# Add to your logging
logger.info(f"Search: query='{query}' results={len(results)} took={elapsed_ms}ms")

# Analytics queries
most_searched_terms = db.query(
    SearchLog.query,
    func.count(SearchLog.id)
).group_by(SearchLog.query).order_by(desc(func.count(SearchLog.id))).limit(20)

# Popular codes
popular_codes = db.query(
    SearchResult.code,
    func.count(SearchResult.id)
).group_by(SearchResult.code).order_by(desc(func.count(SearchResult.id))).limit(20)
```

---

## Summary

You now have:

1. ✅ **Updated ORM models** matching all 22 database columns
2. ✅ **Enhanced domain models** with search helper methods
3. ✅ **Advanced search service** with relevance scoring
4. ✅ **Complete API endpoints** for all search functionality
5. ✅ **Data population utilities** for keywords and aliases
6. ✅ **Testing examples** and integration patterns

**Next Steps**:
1. Update your models with the provided code
2. Run the population utility to add keywords/aliases
3. Test the new search endpoints
4. Integrate autocomplete in your frontend
5. Monitor search quality and iterate

The enhanced search system will dramatically improve NAICS code discovery for your users, making it easier to find the right industry classification with natural language queries, alternative names, and intelligent suggestions.
