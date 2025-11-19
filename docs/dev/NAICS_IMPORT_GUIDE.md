# NAICS Import Guide

---
title: "NAICS Import Guide"
description: "Complete guide for importing NAICS (North American Industry Classification System) codes from TSV files into the Levelith PostgreSQL database."
category: "guides"
tags: ["naics", "import", "database", "tsv", "data-loading"]
author: "Semour Media Group"
date: "2025-01-19"
lastUpdated: "2025-11-19"
difficulty: "beginner"
readingTime: 10
relatedPages:
  - "/docs/dev/NAICS_QUICK_REFERENCE.md"
  - "/docs/backend/NAICS_EXPANSION_SUMMARY.md"
  - "/docs/API_DOCUMENTATION.md"
nextPage: "/docs/dev/NAICS_QUICK_REFERENCE.md"
prevPage: "/docs/dev/DEVELOPMENT_PRIORITIES.md"
searchKeywords:
  - "naics"
  - "import"
  - "tsv"
  - "data loading"
  - "industry codes"
showTOC: true
showBreadcrumbs: true
showLastUpdated: true
version: "1.0"
---

# NAICS Import Guide

> **TL;DR:** Import NAICS industry codes from TSV files into PostgreSQL with automatic validation, hierarchy detection, and batch processing using the `import_naics.py` script.

**Difficulty:** 🟢 Beginner | **Time:** ⏱️ 10 minutes | **Last Updated:** November 19, 2025

---

## Table of Contents

- [Overview](#overview)
- [TSV File Format](#tsv-file-format)
- [NAICS Code Hierarchy](#naics-code-hierarchy)
- [Importing Data](#importing-data)
- [Import Process](#import-process)
- [Validation Rules](#validation-rules)
- [Data Sources](#data-sources)
- [Troubleshooting](#troubleshooting)
- [Post-Import Verification](#post-import-verification)
- [Best Practices](#best-practices)
- [Additional Resources](#additional-resources)

---

## Overview

This guide explains how to import NAICS (North American Industry Classification System) codes from TSV files into the Levelith database. The import system provides automatic validation, hierarchy detection, and error handling for reliable data loading.

### Key Features

- ✅ **Automatic validation** of code format and structure
- ✅ **Hierarchy detection** based on code length
- ✅ **Batch processing** for large datasets (100 rows per batch)
- ✅ **Duplicate handling** with smart skip logic
- ✅ **Error recovery** continues on invalid rows
- ✅ **Detailed statistics** on import success/failure

:::info
**Note:** NAICS 2022 is the current standard. The system defaults to 2022 codes.
:::

---

## TSV File Format

The import script expects a tab-separated values (TSV) file with specific column structure.

### Required Columns

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| `code` | `string` | ✅ Yes | NAICS code (2, 3, 4, or 6 digits) |
| `title` | `string` | ✅ Yes | Official title/name of classification |

### Optional Columns

| Column | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `description` | `text` | ❌ No | - | Detailed description |
| `category` | `string` | ❌ No | `general` | Industry category |
| `parent_code` | `string` | ❌ No | - | Parent NAICS code |
| `is_active` | `boolean` | ❌ No | `TRUE` | Whether code is active |
| `year` | `integer` | ❌ No | `2022` | NAICS version year |

### Valid Categories

```
technology, education, healthcare, finance, manufacturing,
retail, hospitality, construction, agriculture, transportation,
professional_services, arts_entertainment, public_administration, general
```

### Sample TSV File

A sample TSV file is located at: `docs/dev/naics-import-sample.tsv`

```tsv
code	title	description	category	parent_code	is_active	year
11	Agriculture, Forestry, Fishing and Hunting	Establishments primarily engaged in growing crops...	agriculture		TRUE	2022
111	Crop Production	Establishments engaged in growing crops	agriculture	11	TRUE	2022
541511	Custom Computer Programming Services	Establishments primarily engaged in writing software	technology	5415	TRUE	2022
```

:::tip
**Pro Tip:** Use tabs (not spaces) to separate columns. Most spreadsheet applications can export TSV format directly.
:::

---

## NAICS Code Hierarchy

NAICS codes follow a hierarchical structure with increasing specificity:

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

**Important:** Each child code should reference its parent via the `parent_code` column.

---

## Importing Data

### Basic Import

```bash
python backend/import_naics.py docs/dev/naics-import.tsv
```

**Expected output:**
```
Reading NAICS codes from: docs/dev/naics-import.tsv
Processing 150 rows...
✅ Successfully imported 148 codes
⚠️  Skipped 2 duplicate codes
⏱️  Completed in 2.3 seconds
```

### Clear Existing Data and Import

```bash
python backend/import_naics.py --clear docs/dev/naics-import.tsv
```

:::danger
**Warning:** The `--clear` flag will delete ALL existing NAICS codes from the database before importing. Always backup your database first!
:::

### Verbose Output

```bash
python backend/import_naics.py --verbose docs/dev/naics-import.tsv
```

Shows detailed progress for each row:
```
Row 1: Importing code 11 - Agriculture, Forestry...
Row 2: Importing code 111 - Crop Production...
Row 3: Skipping duplicate code 541511
```

### Generate Sample File

```bash
python backend/import_naics.py --sample docs/dev/my-sample.tsv
```

Creates a new sample TSV file with example data.

---

## Import Process

The import script follows these steps:

1. **Validate Database Connection**
   - Checks PostgreSQL connection
   - Verifies database schema

2. **Create Tables if Needed**
   - Creates `naics_codes` table if missing
   - Adds indexes automatically

3. **Validate TSV Format and Data**
   - Checks required headers
   - Validates data types
   - Reports line-specific errors

4. **Normalize NAICS Codes**
   - Removes whitespace
   - Validates digit length
   - Checks format

5. **Determine Hierarchy Levels**
   - 2 digits → level 2
   - 3 digits → level 3
   - 4 digits → level 4
   - 6 digits → level 6

6. **Handle Duplicate Codes**
   - Skips duplicates within TSV file
   - Updates existing database codes

7. **Insert or Update Codes**
   - Uses upsert (insert or update)
   - Maintains referential integrity

8. **Commit in Batches**
   - Processes 100 rows per batch
   - Faster for large imports

9. **Provide Statistics**
   - Success/error counts
   - Processing time
   - Detailed error messages

---

## Validation Rules

The import script validates:

### Code Format

- ✅ Must be 2, 3, 4, or 6 digits
- ❌ Cannot be 1, 5, or 7+ digits
- ❌ No letters or special characters

### Required Fields

- ✅ `code` must be present
- ✅ `title` must be present
- ❌ Empty values rejected

### Category Values

Must be one of the valid categories:

```python
Valid: technology, education, healthcare, finance, manufacturing,
       retail, hospitality, construction, agriculture, transportation,
       professional_services, arts_entertainment, public_administration, general

Invalid: tech, ed, health  # Use full names
```

### Parent Codes

- Parent codes automatically normalized
- Parent validation optional
- Hierarchy calculated from code length

### Duplicate Handling

- Same code multiple times in TSV → only first occurrence imported
- Code exists in database → updated with new data
- Normal behavior for placeholder codes (like "123456")

:::warning
**Warning:** 5-digit codes are not valid in the NAICS system. Use 4-digit or 6-digit codes instead.
:::

---

## Data Sources

### Official NAICS Data

Download the official 2022 NAICS codes from the U.S. Census Bureau:

- 🌐 **Website:** [https://www.census.gov/naics/](https://www.census.gov/naics/)
- 📊 **2022 NAICS:** [https://www.census.gov/naics/?58967?yearbck=2022](https://www.census.gov/naics/?58967?yearbck=2022)

### Converting Excel to TSV

If you have NAICS data in Excel format:

1. **Open the file** in Excel or LibreOffice Calc

2. **Save As** → Tab delimited (*.txt) or Tab Separated Values (*.tsv)

3. **Ensure proper format:**
   - First row contains column headers
   - Tabs separate columns (not spaces or commas)
   - No extra formatting or formulas

4. **Verify export:**
   ```bash
   head -5 naics-export.tsv
   # Should show tab-separated values
   ```

---

## Troubleshooting

<details>
<summary><strong>❌ Error: "File not found"</strong></summary>

**Symptoms:** Script cannot find the TSV file

**Solutions:**

```bash
# Check file exists
ls -la docs/dev/naics-import.tsv

# Use absolute path
python backend/import_naics.py /full/path/to/naics-import.tsv

# Check current directory
pwd
```

**Explanation:** Relative paths are resolved from the current working directory.
</details>

<details>
<summary><strong>❌ Error: "Missing required headers"</strong></summary>

**Symptoms:** TSV file missing `code` or `title` columns

**Solutions:**
1. Open TSV file in text editor
2. Verify first line has headers: `code	title	...`
3. Ensure tabs separate headers (not spaces)
4. Column names are case-sensitive

**Example:**
```tsv
code	title	description
11	Agriculture	...
```
</details>

<details>
<summary><strong>❌ Error: "Invalid NAICS code format"</strong></summary>

**Symptoms:** Code validation fails

**Causes:**
- Letters in code (e.g., "54A")
- Wrong length (e.g., "12345" - 5 digits)
- Special characters (e.g., "54-15")

**Solutions:**
```python
# ❌ INVALID
"54A"      # Letters not allowed
"12345"    # 5 digits not valid
"54-15"    # Special characters not allowed

# ✅ VALID
"54"       # 2 digits
"541"      # 3 digits
"5415"     # 4 digits
"541511"   # 6 digits
```
</details>

<details>
<summary><strong>⚠️ Warning: "Skipping duplicate code in TSV"</strong></summary>

**Symptoms:** Multiple rows with same NAICS code

**Explanation:**
- Same code appears multiple times in TSV file
- Only first occurrence will be imported
- Normal for placeholder codes (like "123456")

**Solutions:**
1. Clean TSV file to have unique codes only
2. Or accept warning (first occurrence wins)

**Example:**
```tsv
code	title
541511	Custom Programming  ← Imported
541511	Software Development  ← Skipped (duplicate)
```
</details>

<details>
<summary><strong>❌ Error: "Database connection failed"</strong></summary>

**Symptoms:** Cannot connect to PostgreSQL

**Solutions:**

```bash
# Check DATABASE_URL in .env
echo $DATABASE_URL

# Test database connection
python -c "from backend.database import DatabaseHealthCheck; print(DatabaseHealthCheck.check())"

# Verify PostgreSQL is running
pg_isready

# Check credentials
psql $DATABASE_URL -c "SELECT 1;"
```
</details>

---

## Post-Import Verification

After importing, verify the data:

### 1. Check Import Statistics

```
✅ Successfully imported 148 codes
⚠️  Skipped 2 duplicate codes
❌ Failed to import 0 codes
⏱️  Completed in 2.3 seconds
```

### 2. Start the Backend

```bash
cd backend && uvicorn main:app --reload
```

### 3. Visit API Docs

Navigate to: [http://localhost:8000/docs](http://localhost:8000/docs)

### 4. Test NAICS Endpoints

```bash
# Get specific code
curl http://localhost:8000/api/v1/naics/541511

# Search codes
curl http://localhost:8000/api/v1/naics/search?q=software

# Get category summary
curl http://localhost:8000/api/v1/naics/categories/summary
```

### 5. View in Admin Dashboard

Open: `dev/dev-frontend/levelith_admin_dashboard`

The dashboard provides:
- 📊 Total NAICS codes count
- 📈 Distribution by category
- 📉 Distribution by hierarchy level
- 🔍 Search and filter capabilities

:::tip
**Pro Tip:** The admin dashboard is the easiest way to visualize your imported NAICS data with charts and filters.
:::

---

## Best Practices

### ✅ DO

1. **Backup First**
   ```bash
   # Always backup before using --clear
   pg_dump levelith > backup_$(date +%Y%m%d).sql
   ```

2. **Validate Data**
   ```bash
   # Review TSV file first
   head -20 naics-import.tsv
   # Check for tabs, not spaces
   cat -A naics-import.tsv | head -5
   ```

3. **Test Import**
   ```bash
   # Try on development database first
   DATABASE_URL=postgresql://localhost/levelith_dev python backend/import_naics.py naics.tsv
   ```

4. **Check Results**
   ```bash
   # Verify statistics after import
   # Use API or admin dashboard to spot-check data
   ```

5. **Version Control**
   ```bash
   # Keep TSV files in git
   git add docs/dev/naics-import.tsv
   git commit -m "Add NAICS import data v2022"
   ```

### ❌ DON'T

1. **Don't use spaces instead of tabs**
   ```tsv
   # ❌ WRONG - Spaces
   code  title  description

   # ✅ CORRECT - Tabs
   code	title	description
   ```

2. **Don't forget headers**
   ```tsv
   # ❌ WRONG - No headers
   11	Agriculture
   111	Crop Production

   # ✅ CORRECT - With headers
   code	title
   11	Agriculture
   111	Crop Production
   ```

3. **Don't use --clear without backup**
   ```bash
   # ❌ DANGEROUS
   python backend/import_naics.py --clear data.tsv

   # ✅ SAFE
   pg_dump levelith > backup.sql
   python backend/import_naics.py --clear data.tsv
   ```

---

## Database Schema

The NAICS codes are stored in the `naics_codes` table:

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

CREATE INDEX idx_naics_level ON naics_codes(level);
CREATE INDEX idx_naics_category ON naics_codes(category);
CREATE INDEX idx_naics_parent ON naics_codes(parent_code);
```

### Key Fields

- **code:** Primary key, 2-6 digits
- **level:** Hierarchical level (2, 3, 4, or 6)
- **category:** Industry category for filtering
- **parent_code:** Reference to parent in hierarchy
- **is_active:** Whether code is currently active

---

## Common Use Cases

### Use Case 1: Import Complete NAICS Dataset

```bash
# 1. Download from Census Bureau
# 2. Convert to TSV format
# 3. Add category mappings
# 4. Import with clear flag

pg_dump levelith > backup_$(date +%Y%m%d).sql
python backend/import_naics.py --clear naics-2022-complete.tsv --verbose
```

### Use Case 2: Update Specific Codes

```bash
# Create TSV with only codes to update
# Run import without --clear flag

python backend/import_naics.py naics-updates.tsv
```

Existing codes will be updated, new codes will be added.

### Use Case 3: Add Custom Industry Categories

```tsv
code	title	description	category
541511	Custom Programming	Software dev services	technology
541519	Other Programming	Programming services	technology
```

---

## Additional Resources

### Official Documentation

- 📚 [NAICS Quick Reference](/docs/dev/NAICS_QUICK_REFERENCE.md)
- 🏗️ [NAICS Expansion Summary](/docs/backend/NAICS_EXPANSION_SUMMARY.md)
- 🧪 [API Documentation](/docs/API_DOCUMENTATION.md)

### External Resources

- 🌐 [U.S. Census Bureau NAICS](https://www.census.gov/naics/)
- 📖 [NAICS 2022 Manual](https://www.census.gov/naics/?58967?yearbck=2022)

### Code Examples

- 💻 [Import Script](/backend/import_naics.py)
- 🎯 [Sample TSV File](/docs/dev/naics-import-sample.tsv)

---

## Related Documentation

- **Previous:** [Development Priorities](/docs/dev/DEVELOPMENT_PRIORITIES.md)
- **Next:** [NAICS Quick Reference](/docs/dev/NAICS_QUICK_REFERENCE.md)

**Other related documentation:**

- [Codebase Analysis](/docs/dev/CODEBASE_ANALYSIS.md)
- [AI Agent Tooling](/docs/dev/AI_AGENT_TOOLING.md)

---

## Feedback

Found an issue with this guide? Have suggestions for improvement?

- 👍 **Helpful?** Give us feedback via the reaction buttons below
- 🐛 **Found a bug?** [Report it on GitHub](https://github.com/Free-Columns/levelith-2/issues)
- 💡 **Have an idea?** [Start a discussion](https://github.com/Free-Columns/levelith-2/discussions)

---

**Last Updated:** November 19, 2025 | **Version:** 1.0 | **Contributors:** Semour Media Group | **NAICS Version:** 2022 | **Database:** PostgreSQL

---

*This document is part of the Levelith Developer Documentation. For questions, join our [Discord community](https://discord.gg/levelith).*
