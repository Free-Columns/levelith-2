"""
Tests for NAICS Database Models

Tests the NAICSCodeDB ORM model and database interactions.
"""

import pytest
from datetime import datetime
from sqlalchemy.exc import IntegrityError

from backend.models.db_models import NAICSCodeDB
from backend.models.naics import NAICSCategory
from backend.database import Base, engine, get_db_context


class TestNAICSCodeDB:
    """Test suite for NAICSCodeDB database model."""

    @pytest.fixture(autouse=True)
    def setup_database(self):
        """
        Create test database tables before each test.
        Drop tables after each test.
        """
        Base.metadata.create_all(bind=engine)
        yield
        Base.metadata.drop_all(bind=engine)

    def test_create_naics_code(self):
        """Test creating a NAICS code in database."""
        with get_db_context() as db:
            naics = NAICSCodeDB(
                code="541511",
                title="Custom Computer Programming Services",
                description="Software development services",
                level=6,
                category=NAICSCategory.TECHNOLOGY,
                parent_code="5415",
                is_active=True,
                year=2022
            )

            db.add(naics)
            db.commit()

            # Verify it was created
            retrieved = db.query(NAICSCodeDB).filter_by(code="541511").first()
            assert retrieved is not None
            assert retrieved.title == "Custom Computer Programming Services"
            assert retrieved.category == NAICSCategory.TECHNOLOGY
            assert retrieved.level == 6
            assert retrieved.is_active is True

    def test_code_is_primary_key(self):
        """Test that code is the primary key."""
        with get_db_context() as db:
            naics1 = NAICSCodeDB(
                code="54",
                title="Professional Services",
                level=2,
                category=NAICSCategory.PROFESSIONAL_SERVICES
            )
            db.add(naics1)
            db.commit()

            # Try to insert duplicate code (should fail)
            naics2 = NAICSCodeDB(
                code="54",
                title="Different Title",
                level=2,
                category=NAICSCategory.GENERAL
            )
            db.add(naics2)

            with pytest.raises(IntegrityError):
                db.commit()

    def test_required_fields(self):
        """Test that required fields are enforced."""
        with get_db_context() as db:
            # Missing title (required)
            naics = NAICSCodeDB(
                code="541",
                level=3,
                category=NAICSCategory.TECHNOLOGY
            )
            db.add(naics)

            with pytest.raises(IntegrityError):
                db.commit()

    def test_nullable_fields(self):
        """Test that nullable fields work correctly."""
        with get_db_context() as db:
            naics = NAICSCodeDB(
                code="54",
                title="Professional Services",
                level=2,
                category=NAICSCategory.PROFESSIONAL_SERVICES,
                # description is NULL
                # parent_code is NULL
            )
            db.add(naics)
            db.commit()

            retrieved = db.query(NAICSCodeDB).filter_by(code="54").first()
            assert retrieved.description is None
            assert retrieved.parent_code is None

    def test_timestamps(self):
        """Test that timestamps are automatically set."""
        with get_db_context() as db:
            naics = NAICSCodeDB(
                code="541511",
                title="Custom Computer Programming",
                level=6,
                category=NAICSCategory.TECHNOLOGY
            )
            db.add(naics)
            db.commit()

            retrieved = db.query(NAICSCodeDB).filter_by(code="541511").first()
            assert isinstance(retrieved.created_at, datetime)
            assert isinstance(retrieved.updated_at, datetime)

    def test_update_naics_code(self):
        """Test updating a NAICS code."""
        with get_db_context() as db:
            # Create
            naics = NAICSCodeDB(
                code="541511",
                title="Original Title",
                level=6,
                category=NAICSCategory.TECHNOLOGY
            )
            db.add(naics)
            db.commit()

            # Update
            naics.title = "Updated Title"
            naics.description = "New description"
            db.commit()

            # Verify update
            retrieved = db.query(NAICSCodeDB).filter_by(code="541511").first()
            assert retrieved.title == "Updated Title"
            assert retrieved.description == "New description"

    def test_delete_naics_code(self):
        """Test deleting a NAICS code."""
        with get_db_context() as db:
            naics = NAICSCodeDB(
                code="541511",
                title="Custom Computer Programming",
                level=6,
                category=NAICSCategory.TECHNOLOGY
            )
            db.add(naics)
            db.commit()

            # Delete
            db.delete(naics)
            db.commit()

            # Verify deletion
            retrieved = db.query(NAICSCodeDB).filter_by(code="541511").first()
            assert retrieved is None

    def test_query_by_category(self):
        """Test querying NAICS codes by category."""
        with get_db_context() as db:
            # Create multiple codes
            codes = [
                NAICSCodeDB(code="54", title="Professional Services", level=2, category=NAICSCategory.PROFESSIONAL_SERVICES),
                NAICSCodeDB(code="541", title="Professional Services", level=3, category=NAICSCategory.PROFESSIONAL_SERVICES),
                NAICSCodeDB(code="11", title="Agriculture", level=2, category=NAICSCategory.AGRICULTURE),
            ]
            db.add_all(codes)
            db.commit()

            # Query by category
            prof_services = db.query(NAICSCodeDB).filter_by(category=NAICSCategory.PROFESSIONAL_SERVICES).all()
            assert len(prof_services) == 2

            agriculture = db.query(NAICSCodeDB).filter_by(category=NAICSCategory.AGRICULTURE).all()
            assert len(agriculture) == 1

    def test_query_by_level(self):
        """Test querying NAICS codes by hierarchical level."""
        with get_db_context() as db:
            # Create codes at different levels
            codes = [
                NAICSCodeDB(code="54", title="Professional Services", level=2, category=NAICSCategory.PROFESSIONAL_SERVICES),
                NAICSCodeDB(code="541", title="Professional Services", level=3, category=NAICSCategory.PROFESSIONAL_SERVICES),
                NAICSCodeDB(code="5415", title="Computer Systems Design", level=4, category=NAICSCategory.TECHNOLOGY),
                NAICSCodeDB(code="541511", title="Custom Programming", level=6, category=NAICSCategory.TECHNOLOGY),
            ]
            db.add_all(codes)
            db.commit()

            # Query sectors (level 2)
            sectors = db.query(NAICSCodeDB).filter_by(level=2).all()
            assert len(sectors) == 1
            assert sectors[0].code == "54"

            # Query national industries (level 6)
            industries = db.query(NAICSCodeDB).filter_by(level=6).all()
            assert len(industries) == 1
            assert industries[0].code == "541511"

    def test_hierarchical_query(self):
        """Test querying hierarchical relationships."""
        with get_db_context() as db:
            # Create hierarchy
            codes = [
                NAICSCodeDB(code="54", title="Professional Services", level=2, category=NAICSCategory.PROFESSIONAL_SERVICES, parent_code=None),
                NAICSCodeDB(code="541", title="Professional Services", level=3, category=NAICSCategory.PROFESSIONAL_SERVICES, parent_code="54"),
                NAICSCodeDB(code="5415", title="Computer Systems Design", level=4, category=NAICSCategory.TECHNOLOGY, parent_code="541"),
            ]
            db.add_all(codes)
            db.commit()

            # Find children of "54"
            children = db.query(NAICSCodeDB).filter_by(parent_code="54").all()
            assert len(children) == 1
            assert children[0].code == "541"

            # Find children of "541"
            children = db.query(NAICSCodeDB).filter_by(parent_code="541").all()
            assert len(children) == 1
            assert children[0].code == "5415"

    def test_repr(self):
        """Test __repr__ method."""
        naics = NAICSCodeDB(
            code="541511",
            title="Custom Computer Programming",
            level=6,
            category=NAICSCategory.TECHNOLOGY
        )

        repr_str = repr(naics)
        assert "NAICSCode" in repr_str
        assert "541511" in repr_str
        assert "Custom Computer Programming" in repr_str

    def test_default_values(self):
        """Test default values for optional fields."""
        with get_db_context() as db:
            naics = NAICSCodeDB(
                code="541511",
                title="Custom Programming",
                level=6,
                category=NAICSCategory.TECHNOLOGY
            )
            db.add(naics)
            db.commit()

            retrieved = db.query(NAICSCodeDB).filter_by(code="541511").first()
            assert retrieved.is_active is True  # Default
            assert retrieved.year == 2022  # Default

    def test_bulk_insert(self):
        """Test bulk inserting multiple NAICS codes."""
        with get_db_context() as db:
            codes = [
                NAICSCodeDB(code=f"{i:02d}", title=f"Industry {i}", level=2, category=NAICSCategory.GENERAL)
                for i in range(1, 11)
            ]

            db.add_all(codes)
            db.commit()

            # Verify all were inserted
            count = db.query(NAICSCodeDB).count()
            assert count == 10

    def test_search_by_title(self):
        """Test searching NAICS codes by title."""
        with get_db_context() as db:
            codes = [
                NAICSCodeDB(code="541511", title="Custom Computer Programming", level=6, category=NAICSCategory.TECHNOLOGY),
                NAICSCodeDB(code="541512", title="Computer Systems Design", level=6, category=NAICSCategory.TECHNOLOGY),
                NAICSCodeDB(code="611420", title="Computer Training", level=6, category=NAICSCategory.EDUCATION),
            ]
            db.add_all(codes)
            db.commit()

            # Search for "computer" (case-insensitive)
            results = db.query(NAICSCodeDB).filter(NAICSCodeDB.title.ilike("%computer%")).all()
            assert len(results) == 3

            # Search for "programming"
            results = db.query(NAICSCodeDB).filter(NAICSCodeDB.title.ilike("%programming%")).all()
            assert len(results) == 1
            assert results[0].code == "541511"
