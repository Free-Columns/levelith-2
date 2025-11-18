# NAICS Import Guide

## Overview

This guide explains how to import NAICS (North American Industry Classification System) codes from TSV files into the Levelith database.

## TSV File Format

The import script expects a tab-separated values (TSV) file with the following columns:

### Required Columns

- **code** (required): The NAICS code (2, 3, 4, or 6 digits)
- **title** (required): The official title/name of the industry classification

### Optional Columns

- **description**: Detailed description of the industry classification
- **category**: Industry category (technology, education, healthcare, finance, manufacturing, retail, hospitality, construction, agriculture, transportation, professional_services, arts_entertainment, public_administration, general)
- **parent_code**: The parent NAICS code in the hierarchy (for 3+ digit codes)
- **is_active**: Whether the code is currently active (TRUE/FALSE, default: TRUE)
- **year**: The NAICS version year (default: 2022)

## Sample TSV File

A sample TSV file is located at: `docs/dev/naics-import-sample.tsv`

```tsv
code    title    description    category    parent_code    is_active    year
11      Agriculture, Forestry, Fishing and Hunting    Establishments primarily engaged in growing crops...    agriculture        TRUE    2022
111     Crop Production    Establishments engaged in growing crops    agriculture    11    TRUE    2022
541511  Custom Computer Programming Services    Establishments primarily engaged in writing software    technology    5415    TRUE    2022
```

## NAICS Code Hierarchy

NAICS codes follow a hierarchical structure:

- **2-digit** (Sector): Broadest level (e.g., "54" = Professional Services)
- **3-digit** (Subsector): More specific (e.g., "541" = Professional, Scientific, and Technical Services)
- **4-digit** (Industry Group): Even more specific (e.g., "5415" = Computer Systems Design)
- **6-digit** (National Industry): Most specific (e.g., "541511" = Custom Computer Programming)

Each child code should reference its parent via the `parent_code` column.

## Importing Data

### Basic Import

```bash
python backend/import_naics.py docs/dev/naics-import.tsv
```

### Clear Existing Data and Import

**WARNING**: This will delete all existing NAICS codes!

```bash
python backend/import_naics.py --clear docs/dev/naics-import.tsv
```

### Verbose Output

```bash
python backend/import_naics.py --verbose docs/dev/naics-import.tsv
```

### Generate Sample File

```bash
python backend/import_naics.py --sample docs/dev/my-sample.tsv
```

## Import Process

The import script:

1. ✅ Validates database connection
2. ✅ Creates tables if needed
3. ✅ Validates TSV format and data
4. ✅ Normalizes NAICS codes
5. ✅ Determines hierarchy levels automatically
6. ✅ Inserts new codes or updates existing ones
7. ✅ Provides detailed statistics

## Validation Rules

The import script validates:

- **Code format**: Must be 2, 3, 4, or 6 digits
- **Required fields**: Code and title must be present
- **Category**: Must be a valid category enum value
- **Parent codes**: Automatically normalized
- **Hierarchy**: Level determined by code length

## Error Handling

- Invalid rows are skipped with error logging
- Line numbers are reported for debugging
- Import continues even if some rows fail
- Final statistics show success/error counts

## Data Sources

### Official NAICS Data

Download the official 2022 NAICS codes from the U.S. Census Bureau:
- Website: https://www.census.gov/naics/
- 2022 NAICS: https://www.census.gov/naics/?58967?yearbck=2022

### Converting Excel to TSV

If you have NAICS data in Excel format:

1. Open the file in Excel or LibreOffice Calc
2. Save As → Tab delimited (*.txt) or Tab Separated Values (*.tsv)
3. Ensure the first row contains the column headers
4. Verify tabs separate columns (not spaces or commas)

## Troubleshooting

### "File not found" Error

Make sure the file path is correct and the file exists:

```bash
ls -la docs/dev/naics-import.tsv
```

### "Missing required headers" Error

Check that your TSV file has at least `code` and `title` columns in the header row.

### "Invalid NAICS code format" Error

NAICS codes must be:
- Numeric only (no letters or special characters)
- 2, 3, 4, or 6 digits long (5-digit codes are not valid in NAICS)

### Database Connection Error

Ensure your database is running and `DATABASE_URL` is correctly set in `.env`:

```bash
# Check database health
python -c "from backend.database import DatabaseHealthCheck; print(DatabaseHealthCheck.check())"
```

## Post-Import Verification

After importing, verify the data:

```bash
# Start the backend
cd backend && uvicorn main:app --reload

# Visit the API docs
# http://localhost:8000/docs

# Test the NAICS endpoints
curl http://localhost:8000/api/v1/naics/541511
```

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

## Admin Dashboard Integration

Once imported, NAICS codes will be visible in the admin dashboard at:

```
dev/dev-frontend/levelith_admin_dashboard
```

The dashboard provides:
- 📊 Total NAICS codes count
- 📈 Distribution by category
- 📉 Distribution by hierarchy level
- 🔍 Search and filter capabilities

## Examples

### Import from Census Bureau Data

1. Download the 2022 NAICS Excel file from Census Bureau
2. Open in spreadsheet software
3. Select columns: Code, Title, Description
4. Save as TSV: `naics-2022-complete.tsv`
5. Add headers and map to our column names
6. Import:

```bash
python backend/import_naics.py --clear naics-2022-complete.tsv
```

### Update Specific Codes

To update just a few codes without clearing all data:

1. Create a TSV with only the codes to update
2. Run import without `--clear` flag:

```bash
python backend/import_naics.py naics-updates.tsv
```

Existing codes will be updated, new codes will be added.

## Best Practices

1. **Backup First**: Always backup your database before using `--clear`
2. **Validate Data**: Review your TSV file before importing
3. **Test Import**: Try importing to a development database first
4. **Check Results**: Verify the statistics after import
5. **Use Version Control**: Keep your TSV files in git for tracking changes

## Support

For issues or questions:
1. Check this guide
2. Review the import script: `backend/import_naics.py`
3. Check logs for detailed error messages
4. Verify TSV format matches the sample file

---

**Last Updated**: 2025-11-18
**NAICS Version**: 2022
**Database**: PostgreSQL
