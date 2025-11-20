# Database Testing Guide

---
title: "Database Testing Guide"
description: "Comprehensive guide to testing database operations including fixtures, mocking strategies, test patterns, and best practices for the Levelith database."
category: "guides"
tags: ["testing", "database", "pytest", "fixtures", "test-patterns"]
author: "Semour Media Group"
date: "2025-11-20"
lastUpdated: "2025-11-20"
difficulty: "intermediate"
readingTime: 12
relatedPages:
  - "/docs/database/USAGE_GUIDE.md"
  - "/docs/core/AI_AGENT_GOLDEN_RULES.md"
  - "/docs/database/DATA_MODELS.md"
nextPage: "/docs/database/DATA_MODELS.md"
prevPage: "/docs/database/USAGE_GUIDE.md"
searchKeywords:
  - "database testing"
  - "test fixtures"
  - "pytest"
  - "test database"
showTOC: true
showBreadcrumbs: true
showLastUpdated: true
version: "1.0"
---

# Database Testing Guide

> **TL;DR:** Use pytest fixtures for test database, SQLite in-memory for speed, factory functions for test data, rollback after each test, mock external dependencies, maintain 80% minimum coverage per Golden Rules.

**Difficulty:** 🟡 Intermediate | **Time:** ⏱️ 12 minutes | **Last Updated:** November 20, 2025

---

## Quick Start

### Test Database Setup

```python
# conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database import Base
from backend.models.db_models import UserDB, ExperienceDB

@pytest.fixture(scope="function")
def test_db():
    """Create test database for each test."""
    # Use in-memory SQLite for speed
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    yield db
    
    db.close()
    Base.metadata.drop_all(engine)
```

### Test Example

```python
def test_create_user(test_db):
    """Test user creation."""
    user = UserDB(
        username="testuser",
        email="test@example.com",
        password_hash="hashed_password"
    )
    test_db.add(user)
    test_db.commit()
    
    # Verify
    saved_user = test_db.query(UserDB).filter(
        UserDB.username == "testuser"
    ).first()
    
    assert saved_user is not None
    assert saved_user.email == "test@example.com"
```

---

## Test Fixtures

### Database Fixtures

```python
@pytest.fixture(scope="session")
def test_engine():
    """Create test engine (session scope)."""
    engine = create_engine("sqlite:///:memory:")
    yield engine
    engine.dispose()

@pytest.fixture(scope="function")
def test_db(test_engine):
    """Create test database session (function scope)."""
    Base.metadata.create_all(test_engine)
    SessionLocal = sessionmaker(bind=test_engine)
    db = SessionLocal()
    
    yield db
    
    db.rollback()  # Rollback any uncommitted changes
    db.close()
    Base.metadata.drop_all(test_engine)
```

### Factory Fixtures

```python
@pytest.fixture
def create_user(test_db):
    """Factory for creating test users."""
    def _create_user(**kwargs):
        defaults = {
            "username": f"testuser_{secrets.token_hex(4)}",
            "email": f"test_{secrets.token_hex(4)}@example.com",
            "password_hash": "hashed_password",
            "is_active": True,
            "is_verified": False
        }
        defaults.update(kwargs)
        
        user = UserDB(**defaults)
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)
        return user
    
    return _create_user

# Usage
def test_user_creation(create_user):
    user = create_user(username="john_doe")
    assert user.username == "john_doe"
```

---

## Test Patterns

### Testing CRUD Operations

```python
class TestUserCRUD:
    def test_create(self, test_db):
        user = UserDB(username="test", email="test@example.com", 
                     password_hash="hash")
        test_db.add(user)
        test_db.commit()
        assert user.id is not None
    
    def test_read(self, test_db, create_user):
        user = create_user()
        found = test_db.query(UserDB).filter(UserDB.id == user.id).first()
        assert found.username == user.username
    
    def test_update(self, test_db, create_user):
        user = create_user()
        user.username = "updated"
        test_db.commit()
        
        updated = test_db.query(UserDB).filter(UserDB.id == user.id).first()
        assert updated.username == "updated"
    
    def test_delete(self, test_db, create_user):
        user = create_user()
        user_id = user.id
        
        test_db.delete(user)
        test_db.commit()
        
        deleted = test_db.query(UserDB).filter(UserDB.id == user_id).first()
        assert deleted is None
```

### Testing Relationships

```python
def test_user_experiences_relationship(test_db, create_user):
    user = create_user()
    
    # Create experiences
    exp1 = ExperienceDB(user_id=user.id, title="Experience 1", 
                       category="education", experience_type="degree")
    exp2 = ExperienceDB(user_id=user.id, title="Experience 2",
                       category="workplace", experience_type="full_time")
    
    test_db.add_all([exp1, exp2])
    test_db.commit()
    
    # Test relationship
    test_db.refresh(user)
    assert len(user.experiences) == 2
    assert user.experiences[0].title in ["Experience 1", "Experience 2"]
```

### Testing Cascade Delete

```python
def test_cascade_delete(test_db, create_user):
    user = create_user()
    
    # Create experience
    exp = ExperienceDB(user_id=user.id, title="Test", 
                      category="education", experience_type="degree")
    test_db.add(exp)
    test_db.commit()
    
    exp_id = exp.id
    
    # Delete user (should cascade to experiences)
    test_db.delete(user)
    test_db.commit()
    
    # Verify experience deleted
    deleted_exp = test_db.query(ExperienceDB).filter(
        ExperienceDB.id == exp_id
    ).first()
    assert deleted_exp is None
```

---

## Test Data Factories

```python
import secrets
from datetime import datetime, timedelta

class UserFactory:
    @staticmethod
    def create(db, **kwargs):
        defaults = {
            "username": f"user_{secrets.token_hex(4)}",
            "email": f"{secrets.token_hex(4)}@example.com",
            "password_hash": "hashed_password",
            "is_active": True,
            "is_verified": False,
            "profile_data": {}
        }
        defaults.update(kwargs)
        
        user = UserDB(**defaults)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

class ExperienceFactory:
    @staticmethod
    def create_degree(db, user_id, **kwargs):
        defaults = {
            "user_id": user_id,
            "title": "Bachelor of Science",
            "category": "education",
            "experience_type": "degree",
            "naics_code": "611310",
            "organization": "University",
            "start_date": datetime(2020, 1, 1),
            "end_date": datetime(2024, 5, 1),
            "type_specific_data": {
                "degree_level": "Bachelor",
                "major": "Computer Science",
                "gpa": 3.8
            }
        }
        defaults.update(kwargs)
        
        exp = ExperienceDB(**defaults)
        db.add(exp)
        db.commit()
        db.refresh(exp)
        return exp
```

---

## Mocking Strategies

### Mock Database Session

```python
from unittest.mock import Mock

def test_with_mock_db():
    mock_db = Mock()
    mock_user = UserDB(username="test", email="test@example.com")
    mock_db.query().filter().first.return_value = mock_user
    
    # Use mock_db in test
    result = mock_db.query(UserDB).filter(UserDB.id == "123").first()
    assert result.username == "test"
```

### Mock External Dependencies

```python
from unittest.mock import patch

@patch('backend.services.user_service.hash_password')
def test_user_registration(mock_hash, test_db):
    mock_hash.return_value = "mocked_hash"
    
    # Test registration logic
    user = UserDB(username="test", email="test@example.com",
                 password_hash=mock_hash("password"))
    test_db.add(user)
    test_db.commit()
    
    assert user.password_hash == "mocked_hash"
    mock_hash.assert_called_once_with("password")
```

---

## Best Practices

### ✅ DO

1. **Use In-Memory SQLite for Speed**
```python
engine = create_engine("sqlite:///:memory:")
```

2. **Isolate Tests**
```python
@pytest.fixture(scope="function")  # New DB per test
def test_db(test_engine):
    # ... creates fresh DB for each test
```

3. **Use Factories for Test Data**
```python
user = UserFactory.create(test_db, username="specific_user")
```

4. **Test Edge Cases**
```python
def test_unique_constraint_violation(test_db, create_user):
    create_user(username="duplicate")
    
    with pytest.raises(IntegrityError):
        create_user(username="duplicate")
```

5. **Maintain 80% Coverage**
```bash
pytest --cov=backend --cov-report=html
```

### ❌ DON'T

1. **Don't Use Production Database**
```python
# ❌ WRONG
engine = create_engine(settings.database_url)

# ✅ CORRECT  
engine = create_engine("sqlite:///:memory:")
```

2. **Don't Share State Between Tests**
```python
# ❌ WRONG - Session scope causes shared state
@pytest.fixture(scope="session")
def test_db():
    # Tests can interfere with each other

# ✅ CORRECT - Function scope isolates tests
@pytest.fixture(scope="function")
def test_db():
    # Each test gets fresh database
```

3. **Don't Skip Cleanup**
```python
# ✅ ALWAYS cleanup after tests
@pytest.fixture
def test_db():
    db = setup_db()
    yield db
    db.close()  # Cleanup
```

---

## Coverage Requirements

Per [Golden Rules](/docs/core/AI_AGENT_GOLDEN_RULES.md), maintain ≥80% test coverage:

```bash
# Run with coverage
pytest --cov=backend --cov-report=term-missing

# Generate HTML report
pytest --cov=backend --cov-report=html
open htmlcov/index.html
```

---

## Additional Resources

- 📚 [AI Agent Golden Rules](/docs/core/AI_AGENT_GOLDEN_RULES.md)
- 🏗️ [Usage Guide](/docs/database/USAGE_GUIDE.md)
- 🧪 [Data Models](/docs/database/DATA_MODELS.md)

---

**Last Updated:** November 20, 2025 | **Version:** 1.0
