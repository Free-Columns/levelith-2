#!/usr/bin/env python3
"""
NAICS Database Seeding Script

Seeds the NAICS database table from the existing JSON file.
This provides a quick way to populate the database with the reference NAICS codes.

Usage:
    python backend/seed_naics.py
    python backend/seed_naics.py --clear
    python backend/seed_naics.py --verbose
"""

import sys
import argparse
import logging
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.config import settings
from backend.database import get_db_context, init_db, DatabaseHealthCheck
from backend.models.db_models import NAICSCodeDB
from backend.repositories.naics_repository import NAICSRepository
from backend.models.naics import get_naics_level

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def seed_naics_from_json(clear_first: bool = False, verbose: bool = False) -> bool:
    """
    Seed NAICS codes from JSON file into database.

    Args:
        clear_first: If True, clear existing NAICS codes first
        verbose: Enable verbose logging

    Returns:
        True if seeding succeeded, False otherwise
    """
    if verbose:
        logger.setLevel(logging.DEBUG)

    logger.info("=" * 70)
    logger.info("NAICS DATABASE SEEDING")
    logger.info("=" * 70)

    # Check database connection
    logger.info("Checking database connection...")
    if not DatabaseHealthCheck.check():
        logger.error("❌ Database connection failed!")
        logger.error("Please check your DATABASE_URL and ensure database is running.")
        return False

    logger.info("✅ Database connection successful")

    # Initialize database (create tables if needed)
    logger.info("Initializing database tables...")
    init_db()
    logger.info("✅ Database tables ready")

    # Load NAICS codes from JSON using the existing repository
    logger.info("Loading NAICS codes from JSON file...")
    json_repo = NAICSRepository()
    naics_codes = json_repo.get_all_codes(active_only=False)
    logger.info(f"✅ Loaded {len(naics_codes)} NAICS codes from JSON")

    if not naics_codes:
        logger.error("No NAICS codes found in JSON file")
        return False

    # Seed to database
    stats = {
        'inserted': 0,
        'updated': 0,
        'skipped': 0,
        'errors': 0
    }

    with get_db_context() as db:
        try:
            # Clear existing data if requested
            if clear_first:
                logger.warning("⚠️  Clearing existing NAICS codes...")
                deleted_count = db.query(NAICSCodeDB).delete()
                db.commit()
                logger.info(f"✅ Deleted {deleted_count} existing codes")

            # Insert NAICS codes
            for naics_code in naics_codes:
                try:
                    # Check if code already exists
                    existing = db.query(NAICSCodeDB).filter_by(code=naics_code.code).first()

                    # Determine level value
                    level_enum = get_naics_level(naics_code.code)
                    level_value = level_enum.value if level_enum else 6

                    if existing:
                        # Update existing
                        existing.title = naics_code.title
                        existing.description = naics_code.description
                        existing.category = naics_code.category
                        existing.level = level_value
                        existing.parent_code = naics_code.parent_code
                        existing.is_active = naics_code.is_active
                        existing.year = naics_code.year

                        stats['updated'] += 1

                        if verbose:
                            logger.debug(f"Updated: {naics_code.code} - {naics_code.title}")
                    else:
                        # Insert new
                        db_code = NAICSCodeDB(
                            code=naics_code.code,
                            title=naics_code.title,
                            description=naics_code.description,
                            category=naics_code.category,
                            level=level_value,
                            parent_code=naics_code.parent_code,
                            is_active=naics_code.is_active,
                            year=naics_code.year,
                        )
                        db.add(db_code)
                        stats['inserted'] += 1

                        if verbose:
                            logger.debug(f"Inserted: {naics_code.code} - {naics_code.title}")

                except Exception as e:
                    logger.error(f"Failed to process code {naics_code.code}: {e}")
                    stats['errors'] += 1
                    continue

            # Commit all changes
            db.commit()

            logger.info("=" * 70)
            logger.info("✅ SEEDING COMPLETE!")
            logger.info("=" * 70)
            logger.info(f"📊 Statistics:")
            logger.info(f"   Inserted (new): {stats['inserted']}")
            logger.info(f"   Updated (existing): {stats['updated']}")
            logger.info(f"   Errors: {stats['errors']}")
            logger.info(f"   Total codes in database: {stats['inserted'] + stats['updated']}")
            logger.info("=" * 70)

            return True

        except Exception as e:
            logger.error(f"❌ Seeding failed: {e}")
            db.rollback()
            return False


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Seed NAICS codes from JSON file into database",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                 # Seed from JSON file
  %(prog)s --clear         # Clear database and seed
  %(prog)s --verbose       # Show detailed logging
        """
    )

    parser.add_argument(
        '--clear', '-c',
        action='store_true',
        help='Clear existing NAICS codes before seeding'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )

    args = parser.parse_args()

    # Confirm if clearing data
    if args.clear:
        logger.warning("⚠️  WARNING: This will DELETE ALL existing NAICS codes!")
        response = input("Are you sure you want to continue? (yes/no): ")
        if response.lower() != 'yes':
            logger.info("Seeding cancelled")
            return

    # Run seeding
    success = seed_naics_from_json(
        clear_first=args.clear,
        verbose=args.verbose
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
