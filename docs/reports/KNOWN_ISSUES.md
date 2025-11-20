# Known Issues & Critical Gaps

---
title: "Known Issues & Critical Gaps"
description: "Comprehensive list of critical issues, high-priority bugs, and technical debt that must be addressed before production deployment of the Levelith platform."
category: "reference"
tags: ["known-issues", "bugs", "technical-debt", "critical-issues", "roadmap"]
author: "Semour Media Group"
date: "2025-01-19"
lastUpdated: "2025-11-19"
difficulty: "intermediate"
readingTime: 20
relatedPages:
  - "/docs/dev/DEVELOPMENT_PRIORITIES.md"
  - "/docs/dev/CODEBASE_ANALYSIS.md"
  - "/docs/core/AI_AGENT_GOLDEN_RULES.md"
nextPage: "/docs/dev/DEVELOPMENT_PRIORITIES.md"
prevPage: "/docs/core/MANIFEST.md"
searchKeywords:
  - "known issues"
  - "critical bugs"
  - "technical debt"
  - "production blockers"
  - "service layer"
  - "jwt authentication"
showTOC: true
showBreadcrumbs: true
showLastUpdated: true
version: "1.0"
---

# Known Issues & Critical Gaps

> **TL;DR:** This document tracks 10 critical issues blocking production deployment: service layer bypassed in API routes (3-4 hrs), missing service tests violating 80% coverage (5-6 hrs), incomplete JWT authentication (2-3 hrs), mixed domain/DB models (4-5 hrs), plus 6 additional high/medium priority items. Total estimated fix time: 62-106 hours.

**Difficulty:** 🟡 Intermediate | **Time:** ⏱️ 20 minutes | **Last Updated:** November 19, 2025

---

## Table of Contents

- [Overview](#overview)
- [Critical Issues (Must Fix Before Production)](#critical-issues-must-fix-before-production)
  - [1. Service Layer Bypassed](#1-service-layer-bypassed-)
  - [2. Missing Service Layer Tests](#2-missing-service-layer-tests-)
  - [3. JWT Authentication Incomplete](#3-jwt-authentication-incomplete-)
  - [4. Mixed Domain/DB Models](#4-mixed-domaindb-models-)
- [High Priority Issues (Should Fix Soon)](#high-priority-issues-should-fix-soon)
- [Medium Priority Issues (Nice to Have)](#medium-priority-issues-nice-to-have)
- [Issue Summary & Recommended Fix Order](#issue-summary--recommended-fix-order)
- [Additional Resources](#additional-resources)

---

## Overview

This document maintains a comprehensive list of known issues, bugs, and technical debt that must be addressed before the Levelith platform can be deployed to production. Issues are categorized by severity and include estimated fix times, affected files, and detailed solutions.

:::danger
**Status:** Active Development - Several critical issues must be resolved before production deployment
:::

### Issue Categories

| Priority | Description | Count | Total Time |
|----------|-------------|-------|------------|
| **Critical** | Must fix before production | 4 | 14-17 hours |
| **High** | Should fix soon | 3 | 5 hours |
| **Medium** | Nice to have | 3 | 43-84 hours |
| **Total** | All issues | 10 | 62-106 hours |

---

## Critical Issues (Must Fix Before Production)

These issues must be resolved before the application can be deployed to production.

### 1. Service Layer Bypassed ❌

**Severity:** 🔴 CRITICAL
**Impact:** Architecture violation, code duplication, maintainability
**Estimated Fix Time:** 3-4 hours
**Affected Files:** `backend/api/routes/users.py:30-100`, `backend/api/routes/experiences.py:25-80`

#### Issue

API routes query the database directly instead of using the service layer, violating the clean architecture pattern.

#### Current Implementation (Wrong)

```python
@router.post("/api/v1/users")
async def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # Direct database access
    existing_user = db.query(UserDB).filter(
        UserDB.email == user_data.email
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = UserDB(**user_data.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
```

#### Should Be (Correct)

```python
@router.post("/api/v1/users")
async def create_user(
    user_data: UserCreate,
    service: UserService = Depends(get_user_service)
):
    # Use service layer
    try:
        user = service.register_user(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password
        )
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
```

#### Why This Matters

- Business logic is duplicated in routes and services
- Services are written but never used
- Makes testing difficult (can't mock service layer)
- Violates Single Responsibility Principle
- Hard to maintain and extend

#### Required Changes

1. Create dependency injection functions for services
2. Update all user endpoints to use `UserService`
3. Update all experience endpoints to use `ExperienceService`
4. Remove direct database queries from routes
5. Update tests to verify service usage

:::warning
**Related Issue:** #4 (Mixed Domain/DB Models)
:::

---

### 2. Missing Service Layer Tests ❌

**Severity:** 🔴 CRITICAL
**Impact:** Test coverage below 80%, violates Golden Rule 1
**Estimated Fix Time:** 5-6 hours
**Affected Files:**
- `backend/services/experience_service.py` (968 lines, 0 tests)
- `backend/services/user_service.py` (582 lines, 0 tests)
- `backend/models/db_models.py` (100 lines, 0 tests)

#### Issue

Two critical service files (1,550 lines of business logic) have zero tests, causing overall test coverage to fall below the 80% minimum requirement.

#### Current Coverage

| Component | Coverage | Target |
|-----------|----------|--------|
| Overall | ~75% | 80% |
| Experience Service | 0% | 80% |
| User Service | 0% | 80% |
| DB Models | 0% | 80% |

<details>
<summary><strong>📋 Untested Methods in experience_service.py</strong></summary>

```python
create_certificate()    # Certificate experience creation
create_degree()         # Degree experience creation
create_course()         # Course experience creation
create_gig()           # Gig experience creation
create_part_time()     # Part-time experience creation
create_full_time()     # Full-time experience creation
create_soft_skill()    # Soft skill creation
create_hard_skill()    # Hard skill creation
create_native_skill()  # Native skill creation
get_user_experiences() # Get experiences with filtering
search_experiences()   # Search by title/skills
update_experience()    # Update existing experience
delete_experience()    # Delete experience
get_experience_count() # Count experiences
_validate_dates()      # Date validation
```
</details>

<details>
<summary><strong>📋 Untested Methods in user_service.py</strong></summary>

```python
register_user()              # User registration
authenticate_user()          # Login/authentication
change_password()            # Password changes
activate_user()              # Activate account
deactivate_user()            # Deactivate account
verify_user_email()          # Email verification
update_profile()             # Profile updates
delete_user()                # User deletion
list_users()                 # User listing
get_user_by_id()            # User retrieval
get_user_by_email()         # Email lookup
get_user_by_username()      # Username lookup
add_experience_to_user()    # Link experience
remove_experience_from_user() # Unlink experience
```
</details>

#### Required Test Files

```bash
tests/test_experience_service.py  # ~50 test functions needed
tests/test_user_service.py        # ~40 test functions needed
tests/test_db_models.py           # ~20 test functions needed
```

#### Test Template Generation

```bash
# Use test system to generate templates
python tests/test_system.py generate backend/services/experience_service.py
python tests/test_system.py generate backend/services/user_service.py
python tests/test_system.py generate backend/models/db_models.py
```

:::danger
**Impact:**
- Violates Golden Rule 1: "Every code change MUST include tests"
- CI/CD fails due to coverage < 80%
- High risk of regressions when modifying services
- Business logic not validated
:::

---

### 3. JWT Authentication Incomplete ⚠️

**Severity:** 🔴 CRITICAL
**Impact:** Authentication doesn't work, security vulnerability
**Estimated Fix Time:** 2-3 hours
**Affected File:** `backend/api/routes/users.py:234-270`

#### Issue

The login endpoint returns user data but doesn't generate JWT tokens. Authentication is non-functional.

#### Current Implementation

```python
@router.post("/login", response_model=UserResponse)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate user and return user information.

    TODO: Implement JWT token generation and return access/refresh tokens
    """
    user = db.query(UserDB).filter(UserDB.username == credentials.username).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # TODO: Verify password hash
    # TODO: Generate JWT tokens

    return user  # Should return tokens!
```

#### What's Missing

1. JWT token generation (access + refresh)
2. Password verification
3. Token validation middleware
4. Protected endpoint decorator
5. Token refresh endpoint
6. Token blacklisting (optional)

<details>
<summary><strong>📋 Show Required Implementation</strong></summary>

```python
from jose import JWTError, jwt
from datetime import datetime, timedelta
from backend.config import settings

def create_access_token(data: dict, expires_delta: timedelta = None):
    """Create JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

def create_refresh_token(data: dict):
    """Create JWT refresh token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> UserDB:
    """Validate token and return current user."""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user

# Update login endpoint
@router.post("/login")
async def login(credentials: UserLogin, service: UserService = Depends(get_user_service)):
    user = service.authenticate_user(credentials.username, credentials.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.id})
    refresh_token = create_refresh_token(data={"sub": user.id})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

# Protected endpoint example
@router.get("/me")
async def get_current_user_info(current_user: UserDB = Depends(get_current_user)):
    return current_user
```
</details>

#### Dependencies to Add

```bash
pip install python-jose[cryptography]
pip install passlib[bcrypt]
```

:::info
**Note:** Configuration is already present in `backend/config.py`:
- secret_key: "your-secret-key-here"
- algorithm: "HS256"
- access_token_expire_minutes: 30
- refresh_token_expire_days: 7
:::

---

### 4. Mixed Domain/DB Models ⚠️

**Severity:** 🔴 HIGH
**Impact:** Architecture confusion, unused code
**Estimated Fix Time:** 4-5 hours

#### Issue

The codebase has both domain models and database models, but they're used inconsistently. Services are designed for domain models, but API routes use database models directly.

#### Current State

```
Domain Models (unused):
├── backend/models/user.py       → User class (320 lines)
├── backend/models/experience.py → Experience + 9 subtypes (412 lines)
└── backend/models/naics.py      → NAICSCode class (372 lines)

Database Models (used):
├── backend/models/db_models.py  → UserDB, ExperienceDB, NAICSCodeDB
```

#### The Problem

- Domain models exist but are never instantiated
- Services return type hints for domain models but can't actually return them
- API uses DB models, bypassing services
- No mapping layer between DB and domain models
- Architectural intent unclear

<details>
<summary><strong>Option A: Pure DB Models (Recommended - Simpler)</strong></summary>

```python
# Remove domain models entirely
# Use DB models throughout
# Update service signatures

class UserService:
    def register_user(...) -> UserDB:  # Use DB model
        user = UserDB(...)
        return user
```

**Pros:**
- ✅ Simpler architecture
- ✅ Less code to maintain
- ✅ No mapping overhead
- ✅ Easier to understand

**Cons:**
- ❌ Couples business logic to database
- ❌ ORM objects in service layer
</details>

<details>
<summary><strong>Option B: Full Domain Model Separation (Complex)</strong></summary>

```python
# Keep domain models
# Implement mapper layer
# Services use domain models
# API maps DB <-> domain

class UserMapper:
    @staticmethod
    def to_domain(db_user: UserDB) -> User:
        return User(...)

    @staticmethod
    def to_db(user: User) -> UserDB:
        return UserDB(...)
```

**Pros:**
- ✅ True domain-driven design
- ✅ Business logic decoupled from database
- ✅ Easier to test business logic
- ✅ Can switch databases easily

**Cons:**
- ❌ More code and complexity
- ❌ Mapping overhead
- ❌ More files to maintain
</details>

**Recommendation:** Choose Option A (Pure DB Models) for simplicity, unless there's a specific need for database independence.

---

## High Priority Issues (Should Fix Soon)

### 5. ONETRUTH Configuration Duplicated ⚠️

**Severity:** 🟡 MEDIUM | **Fix Time:** 1 hour

**Issue:** Admin dashboard duplicates ONETRUTH branding instead of importing it.

**Locations:**
- Source: `frontend/src/config/ONETRUTH.ts` (240 lines)
- Duplicate: `dev/dev-frontend/levelith_admin_dashboard/src/config/theme.js` (167 lines)

<details>
<summary><strong>Show Solution</strong></summary>

```javascript
// Option 1: Symlink (simple)
cd dev/dev-frontend/levelith_admin_dashboard/src/config/
ln -s ../../../../../../frontend/src/config/ONETRUTH.ts theme.ts

// Option 2: Vite alias (better)
// vite.config.js
export default {
  resolve: {
    alias: {
      '@onetruth': path.resolve(__dirname, '../../../../frontend/src/config/ONETRUTH.ts')
    }
  }
}

// Then import:
import ONETRUTH from '@onetruth';
```
</details>

---

### 6. No Database Migrations ⚠️

**Severity:** 🟡 MEDIUM | **Fix Time:** 2 hours

**Issue:** No Alembic migrations configured. Schema changes are manual and error-prone.

<details>
<summary><strong>Show Solution</strong></summary>

```bash
# Install Alembic
pip install alembic

# Initialize Alembic
cd backend
alembic init alembic

# Generate initial migration
alembic revision --autogenerate -m "Initial schema"

# Apply migration
alembic upgrade head
```
</details>

---

### 7. Rate Limiting Not Active ⚠️

**Severity:** 🟡 MEDIUM | **Fix Time:** 2 hours

**Issue:** Rate limiting is configured but not implemented in middleware.

<details>
<summary><strong>Show Solution</strong></summary>

```bash
pip install slowapi
```

```python
# backend/main.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# Apply to endpoints
@router.post("/login")
@limiter.limit("5/minute")
async def login(...):
    pass
```
</details>

---

## Medium Priority Issues (Nice to Have)

### 8. No Main Frontend Application

**Severity:** 🟢 LOW | **Fix Time:** 40-80 hours

Only the admin dashboard exists. No user-facing frontend application. This represents the bulk of remaining frontend development work.

---

### 9. No Request ID Tracking

**Severity:** 🟢 LOW | **Fix Time:** 1-2 hours

No request ID middleware makes log correlation difficult.

---

### 10. Simple Password Hashing

**Severity:** 🟢 LOW | **Fix Time:** 1-2 hours

Currently uses PBKDF2. Should upgrade to Argon2 or bcrypt for better security.

---

## Issue Summary & Recommended Fix Order

### Week 1: Critical Issues (14-18 hours)

1. ✅ Add service layer tests (5-6 hours)
2. ✅ Refactor API to use services (3-4 hours)
3. ✅ Complete JWT authentication (2-3 hours)
4. ✅ Standardize model usage (4-5 hours)

### Week 2: High Priority (5 hours)

5. ✅ Fix ONETRUTH duplication (1 hour)
6. ✅ Add database migrations (2 hours)
7. ✅ Implement rate limiting (2 hours)

### Month 1: Medium Priority (42-84 hours)

8. ✅ Add request ID tracking (1-2 hours)
9. ✅ Upgrade password hashing (1-2 hours)
10. ✅ Begin main frontend (40-80 hours)

---

## Issue Tracking

For each issue, create a GitHub issue with:
- Title from this document
- Description and impact
- Code examples
- Estimated fix time
- Priority label
- Link to this document

**GitHub Labels to Use:**
- `priority: critical` - Must fix before production
- `priority: high` - Should fix soon
- `priority: medium` - Nice to have
- `type: bug` - Something is broken
- `type: architecture` - Architecture violation
- `type: security` - Security concern
- `type: technical-debt` - Code quality issue

---

## Additional Resources

### Official Documentation

- 📚 [Development Priorities](/docs/dev/DEVELOPMENT_PRIORITIES.md) - Prioritized roadmap
- 🏗️ [Codebase Analysis](/docs/dev/CODEBASE_ANALYSIS.md) - Architecture assessment
- 🧪 [AI Agent Golden Rules](/docs/core/AI_AGENT_GOLDEN_RULES.md) - Development standards

### Code References

- 💻 [Service Layer](https://github.com/Free-Columns/levelith-2/tree/main/backend/services)
- 🎯 [API Routes](https://github.com/Free-Columns/levelith-2/tree/main/backend/api/routes)
- 📊 [Models](https://github.com/Free-Columns/levelith-2/tree/main/backend/models)

---

## Related Documentation

- **Previous:** [MANIFEST](/docs/core/MANIFEST.md)
- **Next:** [Development Priorities](/docs/dev/DEVELOPMENT_PRIORITIES.md)

**Other related documentation:**

- [Codebase Analysis](/docs/dev/CODEBASE_ANALYSIS.md)
- [API Documentation](/docs/api/API_DOCUMENTATION.md)
- [Testing Guide](/docs/core/AI_AGENT_GOLDEN_RULES.md#rule-1-test-first-development-mandatory)

---

## Feedback

Found an issue with this guide? Have suggestions for improvement?

- 👍 **Helpful?** This document tracks all known issues
- 🐛 **Found a bug?** [Report it on GitHub](https://github.com/Free-Columns/levelith-2/issues)
- 💡 **Have an idea?** [Start a discussion](https://github.com/Free-Columns/levelith-2/discussions)

---

**Last Updated:** November 19, 2025 | **Version:** 1.0 | **Next Review:** After critical issues are resolved

---

*This document is part of the Levelith Developer Documentation. For questions, join our [Discord community](https://discord.gg/levelith).*
