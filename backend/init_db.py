#!/usr/bin/env python3
"""
Database Initialization Script

Initializes the PostgreSQL database with all required tables.
Safe to run multiple times - creates tables only if they don't exist.

Usage:
    python backend/init_db.py              # Initialize database
    python backend/init_db.py --reset      # Drop and recreate all tables (WARNING: destroys data!)
    python backend/init_db.py --check      # Check database connection
"""

import sys
import argparse
import logging
from pathlib import Path

# Add backend directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.config import settings
from backend.database import engine, init_db, drop_db, reset_db, DatabaseHealthCheck
from backend.models.db_models import Base, UserDB, ExperienceDB

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def check_database_connection() -> bool:
    """
    Check if database connection is healthy.

    Returns:
        True if connection successful, False otherwise.
    """
    logger.info("Checking database connection...")

    if DatabaseHealthCheck.check():
        logger.info("✅ Database connection successful!")

        # Get database info
        info = DatabaseHealthCheck.get_info()
        logger.info(f"Database: {info.get('database', 'unknown')}")
        logger.info(f"Version: {info.get('version', 'unknown')}")
        logger.info(f"Status: {info.get('status', 'unknown')}")
        return True
    else:
        logger.error("❌ Database connection failed!")
        logger.error(f"Database URL: {settings.database_url}")
        logger.error("Please check:")
        logger.error("  1. Database is running and accessible")
        logger.error("  2. DATABASE_URL environment variable is correct")
        logger.error("  3. Network connectivity to database host")
        return False


def initialize_database() -> None:
    """
    Initialize database by creating all tables.

    Safe to run multiple times - only creates tables if they don't exist.
    """
    logger.info("Initializing database...")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Database URL: {settings.database_url.split('@')[-1]}")  # Hide credentials

    try:
        # Check connection first
        if not check_database_connection():
            logger.error("Cannot initialize database - connection check failed")
            sys.exit(1)

        # Create all tables
        logger.info("Creating database tables...")
        init_db()

        # Verify tables were created
        inspector = engine.dialect.inspector(engine)
        tables = inspector.get_table_names()

        logger.info(f"✅ Database initialized successfully!")
        logger.info(f"Created/verified {len(tables)} tables:")
        for table in sorted(tables):
            logger.info(f"  - {table}")

    except Exception as e:
        logger.error(f"❌ Failed to initialize database: {e}")
        logger.exception("Full error:")
        sys.exit(1)


def reset_database() -> None:
    """
    Reset database by dropping and recreating all tables.

    WARNING: This will destroy all data!
    Only allowed in development/test environments.
    """
    if settings.is_production:
        logger.error("❌ Cannot reset database in production environment!")
        logger.error("This operation would destroy all production data.")
        sys.exit(1)

    logger.warning("⚠️  WARNING: This will DELETE ALL DATA in the database!")
    logger.warning(f"Environment: {settings.environment}")
    logger.warning(f"Database: {settings.database_url.split('@')[-1]}")

    # Require explicit confirmation
    response = input("\nType 'DELETE ALL DATA' to confirm: ")
    if response != "DELETE ALL DATA":
        logger.info("Reset cancelled.")
        return

    try:
        logger.info("Dropping all tables...")
        drop_db()
        logger.info("✅ All tables dropped")

        logger.info("Creating fresh tables...")
        init_db()
        logger.info("✅ Database reset complete")

    except Exception as e:
        logger.error(f"❌ Failed to reset database: {e}")
        logger.exception("Full error:")
        sys.exit(1)


def main():
    """Main entry point for database initialization."""
    parser = argparse.ArgumentParser(
        description="Initialize Levelith PostgreSQL database",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Initialize database (create tables)
  %(prog)s --check            # Check database connection only
  %(prog)s --reset            # Reset database (WARNING: destroys data!)
        """
    )

    parser.add_argument(
        '--check',
        action='store_true',
        help='Check database connection and exit'
    )

    parser.add_argument(
        '--reset',
        action='store_true',
        help='Reset database (drop and recreate all tables - DESTROYS DATA!)'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )

    args = parser.parse_args()

    # Set verbose logging
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Print header
    logger.info("=" * 60)
    logger.info("Levelith Database Initialization")
    logger.info("=" * 60)
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Debug Mode: {settings.debug}")
    logger.info("=" * 60)

    # Execute requested action
    if args.check:
        # Just check connection
        if check_database_connection():
            logger.info("✅ Database check passed")
            sys.exit(0)
        else:
            logger.error("❌ Database check failed")
            sys.exit(1)

    elif args.reset:
        # Reset database (dangerous!)
        reset_database()

    else:
        # Normal initialization
        initialize_database()

    logger.info("=" * 60)
    logger.info("Done!")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
