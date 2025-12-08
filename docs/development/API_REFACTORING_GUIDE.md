# API Routes Refactoring Guide

**Status:** Phase 1 - In Progress
**Goal:** Refactor API routes to use service layer instead of direct database access
**Estimated Time:** 3-4 hours

---

## Overview

This guide outlines the systematic refactoring of API routes to use the service layer, following clean architecture principles.

### Current State
- ✅ Service layer implemented and tested (80%+ coverage)
- ✅ Dependency injection framework created (`backend/dependencies.py`)
- ❌ API routes still query database directly (architecture violation)

### Target State
- API routes use service layer via dependency injection
- No direct database queries in route handlers
- Clean separation between API layer and business logic
- Easier to test and maintain

---

## Dependency Injection Setup

**File:** `backend/dependencies.py` (created)

### Available Dependencies

```python
from backend.dependencies import (
    get_db,                    # Database session
    get_user_service,          # UserService instance
    get_experience_service,    # ExperienceService instance
    get_naics_service,         # NAICSService instance
    get_user_repository,       # UserRepository instance
    get_experience_repository, # ExperienceRepository instance
    get_naics_repository,      # NAICSRepository instance
)
```

---

## Refactoring Pattern

### Before (Direct DB Access - BAD ❌)
```python
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.db_models import UserDB

@router.get("/{user_id}")
async def get_user(user_id: str, db: Session = Depends(get_db)):
    """Get user by ID."""
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        ...
    )
```

### After (Service Layer - GOOD ✅)
```python
from backend.dependencies import get_user_service
from backend.services.user_service import UserService

@router.get("/{user_id}")
async def get_user(
    user_id: str,
    user_service: UserService = Depends(get_user_service)
):
    """Get user by ID."""
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Convert domain model to response schema
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        is_active=user.is_active,
        is_verified=user.is_verified,
        profile_data=user.profile_data,
        created_at=user.created_at,
        updated_at=user.updated_at,
        last_login=user.last_login,
        experience_count=len(user.experiences)
    )
```

---

## Files to Refactor

### Priority 1: User Routes (High Impact)
**File:** `backend/api/routes/users.py` (613 lines)

**Endpoints to Refactor:**
1. `POST /` - Create user
2. `GET /{user_id}` - Get user by ID
3. `GET /` - List users with pagination
4. `PATCH /{user_id}` - Update user
5. `DELETE /{user_id}` - Delete user
6. `GET /stats` - User statistics
7. `POST /bulk-delete` - Bulk delete users
8. `POST /seed` - Seed database (keep DB access - acceptable)

**Auth Endpoints (Keep as-is for now):**
- `POST /login` - ✅ Already uses auth.py utilities
- `POST /refresh` - ✅ Already uses auth.py utilities
- `GET /me` - ✅ Already uses get_current_user dependency

**Estimated Time:** 2-3 hours

### Priority 2: Experience Routes (High Impact)
**File:** `backend/api/routes/experiences.py` (~500 lines)

**Endpoints to Refactor:**
1. `POST /` - Create experience
2. `GET /` - List experiences
3. `GET /{experience_id}` - Get experience
4. `PUT /{experience_id}` - Update experience
5. `DELETE /{experience_id}` - Delete experience
6. `GET /summary` - Experience summary

**Estimated Time:** 1-2 hours

### Priority 3: NAICS Routes (Already Good)
**File:** `backend/api/routes/naics.py`

**Status:** ✅ Already uses NAICSService
**Action:** Review and verify, but likely no changes needed

---

## Step-by-Step Refactoring Process

### Step 1: Update Imports
```python
# Remove or reduce these:
from backend.database import get_db
from backend.models.db_models import UserDB
from sqlalchemy.orm import Session

# Add these:
from backend.dependencies import get_user_service
from backend.services.user_service import UserService
```

### Step 2: Change Route Signature
```python
# BEFORE
async def create_user(user_data: UserCreate, db: Session = Depends(get_db)):

# AFTER
async def create_user(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
```

### Step 3: Replace DB Queries with Service Calls
```python
# BEFORE
user = db.query(UserDB).filter(UserDB.id == user_id).first()

# AFTER
user = user_service.get_user_by_id(user_id)
```

### Step 4: Handle Service Exceptions
```python
# BEFORE
if not user:
    raise HTTPException(status_code=404, detail="User not found")

# AFTER (same, but service may raise ValueError)
try:
    user = user_service.update_profile(user_id, profile_data)
except ValueError as e:
    raise HTTPException(status_code=404, detail=str(e))
```

### Step 5: Convert Models if Needed
```python
# Service returns domain model (User), API returns schema (UserResponse)
# Most schemas already have from_attributes = True, so this works:

return UserResponse(
    id=user.id,
    username=user.username,
    # ... all fields
)

# Or if schema supports it:
return UserResponse.model_validate(user)
```

---

## Detailed Endpoint Refactoring Examples

### Example 1: Create User

#### Before
```python
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if username already exists
    existing_user = db.query(UserDB).filter(UserDB.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Username already exists")

    # Check if email already exists
    existing_email = db.query(UserDB).filter(UserDB.email == user_data.email).first()
    if existing_email:
        raise HTTPException(status_code=409, detail="Email already exists")

    # Hash password
    password_hash = hash_password(user_data.password)

    # Create user
    db_user = UserDB(
        username=user_data.username,
        email=user_data.email,
        password_hash=password_hash,
        profile_data=user_data.profile_data or {}
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return UserResponse(...)
```

#### After
```python
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    """Create a new user."""
    try:
        user = user_service.register_user(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password,
            **user_data.profile_data or {}
        )

        return UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            is_verified=user.is_verified,
            profile_data=user.profile_data,
            created_at=user.created_at,
            updated_at=user.updated_at,
            last_login=user.last_login,
            experience_count=len(user.experiences)
        )
    except ValueError as e:
        # Service raises ValueError for business rule violations
        error_msg = str(e)
        if "already taken" in error_msg or "already registered" in error_msg:
            raise HTTPException(status_code=409, detail=error_msg)
        raise HTTPException(status_code=400, detail=error_msg)
```

**Benefits:**
- ✅ Business logic in service layer
- ✅ Easier to test (mock service instead of DB)
- ✅ Consistent error handling
- ✅ Less code duplication

---

### Example 2: List Users with Pagination

#### Before
```python
@router.get("/")
async def list_users(
    page: int = 1,
    page_size: int = 50,
    search: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    page_size = min(page_size, 200)
    skip = (page - 1) * page_size

    query = db.query(UserDB)

    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            (UserDB.username.ilike(search_filter)) |
            (UserDB.email.ilike(search_filter))
        )

    if is_active is not None:
        query = query.filter(UserDB.is_active == is_active)

    total = query.count()
    users = query.order_by(UserDB.created_at.desc()).offset(skip).limit(page_size).all()

    return {
        "data": [UserResponse(...) for user in users],
        "total": total,
        ...
    }
```

#### After
```python
@router.get("/")
async def list_users(
    page: int = 1,
    page_size: int = 50,
    search: Optional[str] = None,
    is_active: Optional[bool] = None,
    user_service: UserService = Depends(get_user_service)
):
    """List users with pagination and filtering."""
    page_size = min(page_size, 200)
    offset = (page - 1) * page_size

    # Get users from service
    if search:
        users = user_service.search_users(search)
        # Apply additional filters if needed
        if is_active is not None:
            users = [u for u in users if u.is_active == is_active]
        total = len(users)
        users = users[offset:offset + page_size]
    else:
        users = user_service.list_users(
            active_only=is_active if is_active else False,
            limit=page_size,
            offset=offset
        )
        total = user_service.get_user_count()

    total_pages = (total + page_size - 1) // page_size if total > 0 else 1

    return {
        "data": [
            UserResponse(
                id=user.id,
                username=user.username,
                email=user.email,
                is_active=user.is_active,
                is_verified=user.is_verified,
                profile_data=user.profile_data,
                created_at=user.created_at,
                updated_at=user.updated_at,
                last_login=user.last_login,
                experience_count=len(user.experiences)
            )
            for user in users
        ],
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }
```

**Note:** This example shows that some complex queries may need service layer enhancements. Consider adding:
- `user_service.search_users_paginated(query, is_active, limit, offset)`
- This keeps pagination logic in service layer

---

## Common Pitfalls & Solutions

### Pitfall 1: Complex Queries
**Problem:** Service doesn't support complex filtering
```python
# Complex query not in service
query = db.query(UserDB).filter(...).join(...).group_by(...)
```

**Solution:** Add method to service layer
```python
# In user_service.py
def get_users_with_experience_count(self, min_count: int) -> List[User]:
    return self.user_repo.find_users_with_min_experiences(min_count)
```

### Pitfall 2: Model Conversion
**Problem:** Service returns domain model, API needs DB model
```python
# Domain model doesn't match DB schema exactly
```

**Solution:** Use Pydantic's model_validate or explicit mapping
```python
return UserResponse.model_validate(user)
# OR
return UserResponse(id=user.id, username=user.username, ...)
```

### Pitfall 3: Transaction Management
**Problem:** Need to commit multiple operations in one transaction
```python
# Multiple service calls need to be atomic
```

**Solution:** Create new service method that handles the transaction
```python
# In user_service.py
def create_user_with_initial_experience(self, user_data, exp_data):
    user = self.register_user(...)
    # Add experience
    # Both saved in same transaction
    return user
```

### Pitfall 4: Seed Endpoint
**Problem:** Seed endpoint creates hundreds of records with complex logic
```python
# Seed needs bulk insert for performance
```

**Solution:** Keep seed endpoint as-is (direct DB access acceptable for admin endpoints)
```python
@router.post("/seed")  # Keep this one with DB access
async def seed_users(user_count: int = 50, db: Session = Depends(get_db)):
    # Bulk operations are OK here
    ...
```

---

## Testing Strategy

### 1. Keep Existing Tests
Don't delete API tests - they should still pass after refactoring

### 2. Mock Service Layer in Route Tests
```python
# tests/test_api_users.py
from unittest.mock import Mock, patch

def test_create_user_endpoint():
    mock_service = Mock()
    mock_service.register_user.return_value = sample_user

    with patch('backend.dependencies.get_user_service', return_value=mock_service):
        response = client.post("/api/v1/users", json=user_data)
        assert response.status_code == 201
```

### 3. Integration Tests Still Use Real DB
Keep integration tests that use real database to ensure end-to-end functionality

---

## Validation Checklist

Before marking refactoring complete:

### Code Quality
- [ ] All API routes use service layer (except seed endpoints)
- [ ] No direct `db.query()` calls in route handlers
- [ ] Proper error handling (try/except for service errors)
- [ ] Consistent response schemas

### Testing
- [ ] All existing tests still pass
- [ ] Service layer tests cover business logic (already done ✅)
- [ ] Route tests mock service layer
- [ ] Integration tests verify end-to-end

### Documentation
- [ ] Docstrings updated for refactored endpoints
- [ ] API docs (Swagger) still accurate
- [ ] README updated if needed

### Performance
- [ ] No N+1 query problems introduced
- [ ] Pagination still works correctly
- [ ] Response times similar or better

---

## Rollout Strategy

### Option A: Incremental (Recommended ✅)
1. Refactor one route at a time
2. Test after each change
3. Commit working changes frequently
4. Low risk, easy to debug

### Option B: All at Once
1. Refactor all routes in one session
2. Test everything together
3. One big commit
4. Higher risk, harder to debug

**Recommendation:** Use Option A (incremental) to minimize risk

---

## Example Commit Message

```
refactor: migrate user routes to use service layer

- Update create_user endpoint to use UserService.register_user()
- Update get_user endpoint to use UserService.get_user_by_id()
- Update list_users endpoint with service layer integration
- Add proper error handling for service exceptions
- Remove direct database queries from route handlers

Part of Phase 1: API refactoring to follow clean architecture
```

---

## Next Steps After Refactoring

1. ✅ User routes refactored
2. ✅ Experience routes refactored
3. ✅ All tests passing
4. → Create database migrations (Phase 1 final task)
5. → Move to Phase 2 (Production readiness)

---

## Resources

- **Service Layer Code:** `backend/services/user_service.py`, `backend/services/experience_service.py`
- **Service Tests:** `tests/test_user_service.py`, `tests/test_experience_service.py`
- **Dependencies:** `backend/dependencies.py`
- **Clean Architecture:** `docs/agent/MANIFEST.md`

---

**Last Updated:** 2025-12-08
**Status:** Ready to begin refactoring
**Next Action:** Start with `create_user` endpoint in `backend/api/routes/users.py`
