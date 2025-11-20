# NAICS Size Standards Extractor

Complete toolkit for extracting, querying, and analyzing NAICS (North American Industry Classification System) codes and SBA (Small Business Administration) size standards from PDF documents.

## 📋 Overview

This project provides Python scripts to:
- Extract all NAICS codes and size standards from the SBA PDF
- Query and search the extracted data
- Validate and clean the data
- Export data in various formats (JSON, CSV)
- Generate statistical analyses

## 🗂️ Files Generated

### Core Data Files
- **`naics_complete.json`** - Full extracted data (163KB, 1,037 industries)
- **`naics_cleaned.json`** - Cleaned and validated data
- **`naics_summary.json`** - Statistical summary
- **`validation_report.json`** - Data quality report

### Scripts
- **`naics_extractor.py`** - Main PDF extraction script
- **`naics_query.py`** - Query and search utilities
- **`naics_validator.py`** - Data validation and cleaning

## 🚀 Quick Start

### 1. Extract Data from PDF

```bash
python3 naics_extractor.py
```

**Output:**
- Processes all 49 pages of the PDF
- Extracts 1,037 industries from 18 sectors
- Creates `naics_complete.json`

### 2. Query the Data

```python
from naics_query import NAICSQuery

# Initialize query engine
query = NAICSQuery("/mnt/user-data/outputs/naics_complete.json")

# Search by code
result = query.search_by_code("111110")
print(f"{result['title']}: ${result['size_standard_millions']}M")

# Search by keyword
software_industries = query.search_by_keyword("software")

# Filter by size standard
large_businesses = query.filter_by_size_standard(min_millions=40.0)

# Get statistics
stats = query.get_statistics()
print(f"Total industries: {stats['total_industries']}")
```

### 3. Validate and Clean

```bash
python3 naics_validator.py
```

**Features:**
- Validates structure, codes, and size standards
- Checks for duplicates
- Cleans titles (removes newlines, extra spaces)
- Generates validation report

## 📊 Data Structure

### JSON Format

```json
{
  "document_info": {
    "title": "Table of Small Business Size Standards...",
    "source": "U.S. Small Business Administration",
    "effective_date": "May 2, 2022",
    "version": "NAICS 2017"
  },
  "sectors": [
    {
      "sector_code": "11",
      "sector_name": "Agriculture, Forestry, Fishing and Hunting",
      "industries": [
        {
          "code": "111110",
          "title": "Soybean Farming",
          "size_standard_millions": 2.0
        }
      ]
    }
  ],
  "metadata": {
    "total_sectors": 18,
    "total_industries": 1037,
    "extraction_date": "2025-01-19T..."
  }
}
```

### Industry Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `code` | string | 6-digit NAICS code (or with exception suffix) |
| `title` | string | Industry title/description |
| `size_standard_millions` | float | Revenue-based standard (millions USD) |
| `size_standard_employees` | int | Employee-based standard |
| `exception` | int | Exception number (if applicable) |
| `sector_code` | string | Parent sector code |
| `sector_name` | string | Parent sector name |

## 🔍 Query Examples

### Example 1: Find All Software Companies
```python
query = NAICSQuery("naics_complete.json")
software = query.search_by_keyword("software")

for industry in software:
    print(f"{industry['code']}: {industry['title']}")
```

### Example 2: Large Business Standards
```python
# Find industries with $40M+ revenue standards
large = query.filter_by_size_standard(min_millions=40.0)
print(f"Found {len(large)} industries with $40M+ standards")
```

### Example 3: Sector Analysis
```python
sector_54 = query.get_sector("54")
print(f"Sector 54: {sector_54['sector_name']}")
print(f"Total industries: {len(sector_54['industries'])}")

# Export to CSV
query.export_sector_csv("54", "professional_services.csv")
```

### Example 4: Compare Two Industries
```python
comparison = query.compare_codes("111110", "111120")
print(comparison)
```

## 📈 Statistics

### Overall Numbers
- **Total Sectors:** 18
- **Total Industries:** 1,037
- **Revenue-based standards:** 526
- **Employee-based standards:** 505
- **Average revenue standard:** $28.38M

### Size Standard Ranges

#### Revenue Standards
- **Minimum:** $2.0M (various farming industries)
- **Maximum:** $41.5M (multiple industries)
- **Most Common:** $8.0M - $16.5M

#### Employee Standards
- **Minimum:** 100 employees
- **Maximum:** 1,500 employees
- **Most Common:** 500 - 750 employees

## 🔧 Advanced Features

### Custom Filters
```python
# Industries in manufacturing with 1000+ employees
manufacturing = query.get_sector("31")
large_mfg = [
    ind for ind in manufacturing['industries']
    if ind.get('size_standard_employees', 0) >= 1000
]
```

### Batch Export
```python
# Export all sectors to individual CSV files
for sector in query.data['sectors']:
    code = sector['sector_code']
    query.export_sector_csv(code, f"sector_{code}.csv")
```

### Statistical Analysis
```python
stats = query.get_statistics()

# Sector with most industries
largest_sector = max(stats['by_sector'], key=lambda x: x['industries'])
print(f"Largest sector: {largest_sector['name']}")

# Distribution analysis
print(f"Revenue-based: {stats['size_standards']['revenue_based']}")
print(f"Employee-based: {stats['size_standards']['employee_based']}")
```

## 🛠️ Validation Results

### Data Quality Checks
- ✓ **Structure Validation:** All sectors have required fields
- ✓ **Code Format:** All codes follow 6-digit format
- ✓ **Size Standards:** All industries have at least one standard
- ✗ **Duplicates:** 6 duplicate codes found (across exceptions)
- ✓ **Data Quality:** 257 issues fixed (newlines, whitespace)

### Common Issues Fixed
1. Removed newlines from titles (257 instances)
2. Trimmed leading/trailing whitespace
3. Consolidated multiple spaces
4. Standardized format consistency

## 📝 Sector List

| Code | Sector Name | Industries |
|------|-------------|-----------|
| 11 | Agriculture, Forestry, Fishing and Hunting | 65 |
| 21 | Mining, Quarrying, and Oil and Gas | 25 |
| 22 | Utilities | 14 |
| 23 | Construction | 41 |
| 31-33 | Manufacturing | 339 |
| 42 | Wholesale Trade | 91 |
| 44-45 | Retail Trade | 85 |
| 48-49 | Transportation and Warehousing | 39 |
| 51 | Information | 30 |
| 52 | Finance and Insurance | 33 |
| 53 | Real Estate and Rental and Leasing | 23 |
| 54 | Professional, Scientific and Technical Services | 75 |
| 55 | Management of Companies and Enterprises | 2 |
| 56 | Administrative and Support Services | 68 |
| 61 | Educational Services | 18 |
| 62 | Health Care and Social Assistance | 42 |
| 71 | Arts, Entertainment and Recreation | 26 |
| 72 | Accommodation and Food Services | 16 |

## 💡 Use Cases

### 1. Small Business Qualification
Check if your business qualifies as "small" for government contracts:
```python
my_industry = query.search_by_code("541511")  # Custom Computer Programming
print(f"Size standard: ${my_industry['size_standard_millions']}M")
```

### 2. Market Research
Find all industries in a specific sector:
```python
tech_sector = query.get_sector("54")  # Professional Services
for industry in tech_sector['industries']:
    if 'software' in industry['title'].lower():
        print(industry)
```

### 3. Competitive Analysis
Compare size standards across similar industries:
```python
comparison = query.compare_codes("541511", "541512")
# Custom Programming vs. Systems Design
```

### 4. Grant Applications
Export relevant sector data for grant documentation:
```python
query.export_sector_csv("62", "healthcare_standards.csv")
```

## 📦 Dependencies

```bash
pip install --break-system-packages pdfplumber
```

## 🐛 Known Issues

1. **Duplicate Codes:** 6 industries appear with exception variants (e.g., 115310, 115310-E1, 115310-E2)
2. **Special Characters:** Some titles contain superscript numbers from footnote references
3. **Sector 92:** Public Administration has no size standards (by design)

## 🔄 Updates

The SBA updates size standards periodically. To refresh your data:
1. Download latest PDF from [SBA Website](https://www.sba.gov/federal-contracting/contracting-guide/size-standards)
2. Run `naics_extractor.py` with new PDF
3. Run `naics_validator.py` to clean
4. Compare changes using query utilities

## 📄 License & Attribution

Data source: U.S. Small Business Administration  
Effective Date: May 2, 2022  
NAICS Version: 2017

## 🤝 Contributing

To improve the extractor:
1. Test with different PDF versions
2. Add new query methods
3. Enhance validation rules
4. Optimize performance

## 📧 Support

For issues with:
- **Extraction:** Check PDF format matches expected structure
- **Queries:** Review validation_report.json for data issues
- **Validation:** Run with cleaned JSON file

---

**Generated:** 2025-01-19  
**Version:** 1.0  
**Total Records:** 1,037 industries across 18 sectors
