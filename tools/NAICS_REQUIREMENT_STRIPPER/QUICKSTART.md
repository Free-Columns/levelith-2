# NAICS Tools - Quickstart Guide

## 🚀 5-Minute Setup

### Prerequisites
```bash
pip install --break-system-packages pdfplumber
```

### Files You Have

#### Data Files
- **naics_complete.json** - Full extracted data (1,037 industries)
- **naics_cleaned.json** - Validated and cleaned version
- **naics_summary.json** - Statistical summary
- **validation_report.json** - Data quality report
- **sector_54_professional_services.csv** - Sample CSV export

#### Scripts
- **naics_extractor.py** - Extract from PDF
- **naics_query.py** - Search and filter data
- **naics_validator.py** - Validate and clean
- **naics_cli.py** - Command-line interface

## 📖 Common Tasks

### 1. Search for Your Industry

```bash
# By NAICS code
python3 naics_cli.py query naics_complete.json code 541511

# By keyword
python3 naics_cli.py query naics_complete.json keyword "software"

# Get all stats
python3 naics_cli.py query naics_complete.json stats
```

### 2. Export Sector Data

```bash
# Export a specific sector to CSV
python3 naics_cli.py export naics_complete.json csv my_sector.csv 54

# List all sectors first
python3 naics_cli.py list naics_complete.json
```

### 3. Python API Usage

```python
from naics_query import NAICSQuery

# Load data
query = NAICSQuery("naics_complete.json")

# Find your industry
my_biz = query.search_by_code("541511")
print(f"Small business limit: ${my_biz['size_standard_millions']}M")

# Search by keyword
results = query.search_by_keyword("consulting")
for r in results:
    print(f"{r['code']}: {r['title']}")

# Filter by size
large = query.filter_by_size_standard(min_millions=30.0)
print(f"Found {len(large)} industries with $30M+ standards")
```

### 4. Re-extract from Updated PDF

```bash
# When SBA releases new standards
python3 naics_cli.py extract new_sba_standards.pdf updated_data.json

# Validate the new data
python3 naics_cli.py validate updated_data.json --clean
```

## 💡 Quick Examples

### Example 1: Am I a Small Business?

```python
from naics_query import NAICSQuery

query = NAICSQuery("naics_complete.json")

# Your business details
my_code = "541511"  # Custom Computer Programming
my_revenue = 25.0   # $25M annual revenue

# Check size standard
industry = query.search_by_code(my_code)
standard = industry['size_standard_millions']

if my_revenue <= standard:
    print(f"✓ You qualify as small business (limit: ${standard}M)")
else:
    print(f"✗ Exceeds small business standard (limit: ${standard}M)")
```

### Example 2: Find Similar Industries

```python
# Find all software-related industries
query = NAICSQuery("naics_complete.json")
software = query.search_by_keyword("software")

print(f"Found {len(software)} software industries:")
for s in software:
    std = s.get('size_standard_millions', s.get('size_standard_employees'))
    print(f"  {s['code']}: {s['title']} - ${std}")
```

### Example 3: Sector Analysis

```python
# Analyze a specific sector
query = NAICSQuery("naics_complete.json")
sector = query.get_sector("54")  # Professional Services

print(f"Sector: {sector['sector_name']}")
print(f"Total industries: {len(sector['industries'])}")

# Export to CSV for detailed analysis
query.export_sector_csv("54", "professional_services_analysis.csv")
```

## 🎯 Common Use Cases

### For Small Business Owners
1. **Check eligibility:** Search your NAICS code
2. **Compare standards:** Look at similar industries
3. **Track changes:** Re-extract when standards update

### For Researchers
1. **Statistical analysis:** Use `naics_summary.json`
2. **Sector comparison:** Export multiple sectors to CSV
3. **Trend analysis:** Compare different PDF versions

### For Developers
1. **Integration:** Load JSON into your app
2. **API:** Use NAICSQuery class
3. **Custom filters:** Extend query methods

## 📊 Data Structure Reference

### Industry Object
```python
{
    "code": "541511",
    "title": "Custom Computer Programming Services",
    "size_standard_millions": 30.0,
    "size_standard_employees": None,  # or integer
    "sector_code": "54",
    "sector_name": "Professional, Scientific and Technical Services"
}
```

### Query Results
```python
# Search returns list of industries
results = query.search_by_keyword("consulting")
# Each result has: code, title, size standards, sector info

# Statistics return structured summary
stats = query.get_statistics()
# Includes: totals, ranges, sector breakdown
```

## ⚡ Performance Tips

1. **Large queries:** Use filters to narrow results
2. **Repeated searches:** Keep NAICSQuery instance in memory
3. **CSV exports:** Export once, query locally
4. **Batch operations:** Process multiple sectors at once

## 🔧 Troubleshooting

### "File not found"
```bash
# Make sure you're in the right directory
cd /mnt/user-data/outputs
python3 naics_cli.py list naics_complete.json
```

### "Module not found"
```bash
# Install dependencies
pip install --break-system-packages pdfplumber

# Make sure scripts are in same directory
ls -l naics_*.py
```

### "Invalid JSON"
```bash
# Validate and clean the data
python3 naics_cli.py validate naics_complete.json --clean
```

## 📚 Next Steps

1. **Read README.md** for full documentation
2. **Check validation_report.json** for data quality details
3. **Review naics_summary.json** for statistics
4. **Customize queries** for your specific needs

## 🆘 Getting Help

### Command Line Help
```bash
python3 naics_cli.py help
```

### Python Help
```python
from naics_query import NAICSQuery
help(NAICSQuery)
```

### Check Examples
```bash
# Run built-in demo
python3 naics_query.py
```

---

**Last Updated:** 2025-01-19  
**Data Version:** SBA Size Standards (Effective May 2, 2022)  
**Total Records:** 1,037 industries, 18 sectors
