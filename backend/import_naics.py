#!/usr/bin/env python3
"""
NAICS Code Import Script

Imports NAICS codes from TSV file into PostgreSQL database.
Supports bulk import with validation and error reporting.

Usage:
    python backend/import_naics.py docs/dev/naics-import.tsv
    python backend/import_naics.py --file docs/dev/naics-import.tsv --clear
    python backend/import_naics.py --help

TSV Format:
    code    title    description    category    level    parent_code    is_active    year
    11      Agriculture...    Farming and...    agriculture    2        TRUE    2022
    111     Crop Production...    Growing crops...    agriculture    3    11    TRUE    2022
"""

import sys
import csv
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.config import settings
from backend.database import get_db_context, init_db, DatabaseHealthCheck
from backend.models.db_models import NAICSCodeDB
from backend.models.naics import NAICSCategory, get_naics_level, normalize_naics_code

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class NAICSImporter:
    """Import NAICS codes from TSV file into database."""

    def __init__(self, file_path: Path, clear_existing: bool = False, verbose: bool = False):
        """
        Initialize NAICS importer.

        Args:
            file_path: Path to TSV file
            clear_existing: If True, clear existing NAICS codes before import
            verbose: Enable verbose logging
        """
        self.file_path = file_path
        self.clear_existing = clear_existing
        self.verbose = verbose

        if verbose:
            logger.setLevel(logging.DEBUG)

        self.stats = {
            'total_rows': 0,
            'imported': 0,
            'updated': 0,
            'skipped': 0,
            'errors': 0
        }

    def validate_tsv_format(self, row: Dict[str, str], line_num: int) -> Optional[Dict[str, Any]]:
        """
        Validate and transform a TSV row.

        Args:
            row: Dictionary from CSV DictReader
            line_num: Line number for error reporting

        Returns:
            Validated and transformed data, or None if invalid
        """
        try:
            # Required fields
            code = row.get('code', '').strip()
            title = row.get('title', '').strip()

            if not code or not title:
                logger.error(f"Line {line_num}: Missing required field (code or title)")
                return None

            # Normalize code
            code = normalize_naics_code(code)
            if not code:
                logger.error(f"Line {line_num}: Invalid NAICS code format: {row.get('code')}")
                return None

            # Determine level from code length
            naics_level = get_naics_level(code)
            if not naics_level:
                logger.error(f"Line {line_num}: Invalid NAICS code length: {code}")
                return None

            level_value = naics_level.value

            # Category - default to GENERAL if not specified or invalid
            category_str = row.get('category', 'general').strip().lower()
            try:
                category = NAICSCategory(category_str)
            except ValueError:
                logger.warning(f"Line {line_num}: Invalid category '{category_str}', using GENERAL")
                category = NAICSCategory.GENERAL

            # Optional fields
            description = row.get('description', '').strip() or None
            parent_code = row.get('parent_code', '').strip() or None

            if parent_code:
                parent_code = normalize_naics_code(parent_code)

            # Boolean fields
            is_active_str = row.get('is_active', 'TRUE').strip().upper()
            is_active = is_active_str in ('TRUE', 'T', '1', 'YES', 'Y')

            # Year field
            year_str = row.get('year', '2022').strip()
            try:
                year = int(year_str)
            except ValueError:
                logger.warning(f"Line {line_num}: Invalid year '{year_str}', using 2022")
                year = 2022

            return {
                'code': code,
                'title': title,
                'description': description,
                'level': level_value,
                'category': category,
                'parent_code': parent_code,
                'is_active': is_active,
                'year': year
            }

        except Exception as e:
            logger.error(f"Line {line_num}: Validation error: {e}")
            return None

    def import_from_tsv(self) -> bool:
        """
        Import NAICS codes from TSV file.

        Returns:
            True if import succeeded, False otherwise
        """
        logger.info("=" * 70)
        logger.info("NAICS CODE IMPORT")
        logger.info("=" * 70)
        logger.info(f"File: {self.file_path}")

        # Check file exists
        if not self.file_path.exists():
            logger.error(f"File not found: {self.file_path}")
            return False

        # Check database connection
        logger.info("Checking database connection...")
        if not DatabaseHealthCheck.check():
            logger.error("❌ Database connection failed!")
            return False

        logger.info("✅ Database connection successful")

        # Initialize database (create tables if needed)
        logger.info("Initializing database tables...")
        init_db()
        logger.info("✅ Database tables ready")

        # Read and validate TSV
        logger.info(f"Reading TSV file: {self.file_path}")
        validated_rows: List[Dict[str, Any]] = []

        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter='\t')

                # Validate header
                expected_headers = ['code', 'title']
                if not all(h in reader.fieldnames for h in expected_headers):
                    logger.error(f"Missing required headers. Expected at least: {expected_headers}")
                    logger.error(f"Found headers: {reader.fieldnames}")
                    return False

                for line_num, row in enumerate(reader, start=2):  # Start at 2 (header is line 1)
                    self.stats['total_rows'] += 1

                    validated = self.validate_tsv_format(row, line_num)
                    if validated:
                        validated_rows.append(validated)
                    else:
                        self.stats['skipped'] += 1

        except Exception as e:
            logger.error(f"Failed to read TSV file: {e}")
            return False

        logger.info(f"Validated {len(validated_rows)} rows from {self.stats['total_rows']} total rows")

        if not validated_rows:
            logger.error("No valid rows to import")
            return False

        # Import to database
        logger.info("Importing to database...")

        with get_db_context() as db:
            try:
                # Clear existing data if requested
                if self.clear_existing:
                    logger.warning("⚠️  Clearing existing NAICS codes...")
                    deleted_count = db.query(NAICSCodeDB).delete()
                    db.commit()
                    logger.info(f"✅ Deleted {deleted_count} existing codes")

                # Import rows
                for row_data in validated_rows:
                    try:
                        # Check if code already exists
                        existing = db.query(NAICSCodeDB).filter_by(code=row_data['code']).first()

                        if existing:
                            # Update existing
                            for key, value in row_data.items():
                                setattr(existing, key, value)
                            existing.updated_at = datetime.utcnow()
                            self.stats['updated'] += 1

                            if self.verbose:
                                logger.debug(f"Updated: {row_data['code']} - {row_data['title']}")
                        else:
                            # Insert new
                            naics_code = NAICSCodeDB(**row_data)
                            db.add(naics_code)
                            self.stats['imported'] += 1

                            if self.verbose:
                                logger.debug(f"Imported: {row_data['code']} - {row_data['title']}")

                    except Exception as e:
                        logger.error(f"Failed to import code {row_data['code']}: {e}")
                        self.stats['errors'] += 1
                        continue

                # Commit all changes
                db.commit()

                logger.info("=" * 70)
                logger.info("✅ IMPORT COMPLETE!")
                logger.info("=" * 70)
                logger.info(f"📊 Statistics:")
                logger.info(f"   Total rows read: {self.stats['total_rows']}")
                logger.info(f"   Imported (new): {self.stats['imported']}")
                logger.info(f"   Updated (existing): {self.stats['updated']}")
                logger.info(f"   Skipped (invalid): {self.stats['skipped']}")
                logger.info(f"   Errors: {self.stats['errors']}")
                logger.info("=" * 70)

                return True

            except Exception as e:
                logger.error(f"❌ Import failed: {e}")
                db.rollback()
                return False


def create_sample_tsv(output_path: Path) -> None:
    """
    Create a sample TSV file showing expected format.

    Args:
        output_path: Path where sample TSV will be created
    """
    sample_data = [
        ['code', 'title', 'description', 'category', 'parent_code', 'is_active', 'year'],
        ['11', 'Agriculture, Forestry, Fishing and Hunting',
         'Establishments primarily engaged in growing crops, raising animals, harvesting timber',
         'agriculture', '', 'TRUE', '2022'],
        ['111', 'Crop Production',
         'Establishments engaged in growing crops',
         'agriculture', '11', 'TRUE', '2022'],
        ['1111', 'Oilseed and Grain Farming',
         'Establishments engaged in growing oilseed and grain crops',
         'agriculture', '111', 'TRUE', '2022'],
        ['111110', 'Soybean Farming',
         'Establishments primarily engaged in growing soybeans',
         'agriculture', '1111', 'TRUE', '2022'],
        ['54', 'Professional, Scientific, and Technical Services',
         'Establishments that specialize in performing professional, scientific, and technical activities',
         'professional_services', '', 'TRUE', '2022'],
        ['541', 'Professional, Scientific, and Technical Services',
         'Establishments that specialize in performing professional, scientific, and technical activities',
         'professional_services', '54', 'TRUE', '2022'],
        ['5415', 'Computer Systems Design and Related Services',
         'Establishments providing expertise in the field of information technologies',
         'technology', '541', 'TRUE', '2022'],
        ['541511', 'Custom Computer Programming Services',
         'Establishments primarily engaged in writing, modifying, testing software',
         'technology', '5415', 'TRUE', '2022'],
    ]

    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerows(sample_data)

    logger.info(f"✅ Created sample TSV file: {output_path}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Import NAICS codes from TSV file",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s docs/dev/naics-import.tsv
  %(prog)s --file docs/dev/naics-import.tsv --clear
  %(prog)s --sample docs/dev/naics-sample.tsv
        """
    )

    parser.add_argument(
        'file',
        nargs='?',
        type=Path,
        help='Path to TSV file to import'
    )

    parser.add_argument(
        '--file', '-f',
        dest='file_path',
        type=Path,
        help='Path to TSV file (alternative to positional arg)'
    )

    parser.add_argument(
        '--clear', '-c',
        action='store_true',
        help='Clear existing NAICS codes before importing'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )

    parser.add_argument(
        '--sample', '-s',
        type=Path,
        help='Create a sample TSV file at specified path'
    )

    args = parser.parse_args()

    # Create sample if requested
    if args.sample:
        create_sample_tsv(args.sample)
        return

    # Determine file path
    file_path = args.file or args.file_path

    if not file_path:
        parser.print_help()
        sys.exit(1)

    # Confirm if clearing data
    if args.clear:
        logger.warning("⚠️  WARNING: This will DELETE ALL existing NAICS codes!")
        response = input("Are you sure you want to continue? (yes/no): ")
        if response.lower() != 'yes':
            logger.info("Import cancelled")
            return

    # Run import
    importer = NAICSImporter(
        file_path=file_path,
        clear_existing=args.clear,
        verbose=args.verbose
    )

    success = importer.import_from_tsv()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
