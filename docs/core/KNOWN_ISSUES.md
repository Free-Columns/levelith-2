# Known Issues & Critical Gaps

**Last Updated:** 2025-01-19
**Version:** 1.0
**Status:** Active Development

---

## ⚠️ Critical Issues (Must Fix Before Production)

These issues must be resolved before the application can be deployed to production.

---

### 1. Service Layer Bypassed ❌

**Severity:** CRITICAL
**Impact:** Architecture violation, code duplication, maintainability
**Estimated Fix Time:** 3-4 hours

**Issue:**
API routes query the database directly instead of using the service layer, violating the clean architecture pattern.

**Affected Files:**
- `/home/user/levelith-2/backend/api/routes/users.py` (lines 30-100)
- `/home/user/levelith-2/backend/api/routes/experiences.py` (lines 25-80)

**Current Implementation (Wrong):**
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

**Should Be (Correct):**
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

**Why This Matters:**
- Business logic is duplicated in routes and services
- Services are written but never used
- Makes testing difficult (can't mock service layer)
- Violates Single Responsibility Principle
- Hard to maintain and extend

**Required Changes:**
1. Create dependency injection functions for services
2. Update all user endpoints to use `UserService`
3. Update all experience endpoints to use `ExperienceService`
4. Remove direct database queries from routes
5. Update tests to verify service usage

**Related Issue:** #4 (Mixed Domain/DB Models)

---

### 2. Missing Service Layer Tests ❌

**Severity:** CRITICAL
**Impact:** Test coverage below 80%, violates Golden Rule 1
**Estimated Fix Time:** 5-6 hours

**Issue:**
Two critical service files (1,550 lines of business logic) have zero tests, causing overall test coverage to fall below the 80% minimum requirement.

**Affected Files:**
- `/home/user/levelith-2/backend/services/experience_service.py` (968 lines, 0 tests)
- `/home/user/levelith-2/backend/services/user_service.py` (582 lines, 0 tests)
- `/home/user/levelith-2/backend/models/db_models.py` (100 lines, 0 tests)

**Current Coverage:**
- Overall: ~75% (need 80%)
- Experience Service: 0%
- User Service: 0%
- DB Models: 0%

**Untested Methods in experience_service.py:**
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

**Untested Methods in user_service.py:**
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

**Required Test Files:**
```bash
tests/test_experience_service.py  # ~50 test functions needed
tests/test_user_service.py        # ~40 test functions needed
tests/test_db_models.py           # ~20 test functions needed
```

**Test Template Generation:**
```bash
# Use test system to generate templates
python tests/test_system.py generate backend/services/experience_service.py
python tests/test_system.py generate backend/services/user_service.py
python tests/test_system.py generate backend/models/db_models.py
```

**Impact:**
- Violates Golden Rule 1: "Every code change MUST include tests"
- CI/CD fails due to coverage < 80%
- High risk of regressions when modifying services
- Business logic not validated

---

### 3. JWT Authentication Incomplete ⚠️

**Severity:** CRITICAL
**Impact:** Authentication doesn't work, security vulnerability
**Estimated Fix Time:** 2-3 hours

**Issue:**
The login endpoint returns user data but doesn't generate JWT tokens. Authentication is non-functional.

**Affected File:**
- `/home/user/levelith-2/backend/api/routes/users.py:234-270`

**Current Implementation:**
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

**What's Missing:**
1. JWT token generation (access + refresh)
2. Password verification
3. Token validation middleware
4. Protected endpoint decorator
5. Token refresh endpoint
6. Token blacklisting (optional)

**Required Implementation:**
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

**Dependencies to Add:**
```bash
pip install python-jose[cryptography]
pip install passlib[bcrypt]
```

**Configuration Already Present:**
```python
# backend/config.py (already configured)
secret_key: str = "your-secret-key-here"
algorithm: str = "HS256"
access_token_expire_minutes: int = 30
refresh_token_expire_days: int = 7
```

---

### 4. Mixed Domain/DB Models ⚠️

**Severity:** HIGH
**Impact:** Architecture confusion, unused code
**Estimated Fix Time:** 4-5 hours

**Issue:**
The codebase has both domain models and database models, but they're used inconsistently. Services are designed for domain models, but API routes use database models directly.

**Current State:**
```
Domain Models (unused):
├── backend/models/user.py       → User class (320 lines)
├── backend/models/experience.py → Experience + 9 subtypes (412 lines)
└── backend/models/naics.py      → NAICSCode class (372 lines)

Database Models (used):
├── backend/models/db_models.py  → UserDB, ExperienceDB, NAICSCodeDB
```

**Services Designed For Domain Models:**
```python
# backend/services/user_service.py
class UserService:
    def register_user(...) -> User:  # Returns domain model
        # But domain model is never actually created!
        pass
```

**API Routes Use DB Models:**
```python
# backend/api/routes/users.py
@router.post("/users")
async def create_user(...) -> UserDB:  # Returns DB model
    db_user = UserDB(...)  # Uses DB model directly
    return db_user
```

**The Problem:**
- Domain models exist but are never instantiated
- Services return type hints for domain models but can't actually return them
- API uses DB models, bypassing services
- No mapping layer between DB and domain models
- Architectural intent unclear

**Decision Required:**

**Option A: Pure DB Models (Recommended - Simpler)**
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
- Simpler architecture
- Less code to maintain
- No mapping overhead
- Easier to understand

**Cons:**
- Couples business logic to database
- ORM objects in service layer

**Option B: Full Domain Model Separation (Complex)**
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

class UserService:
    def register_user(...) -> User:  # Domain model
        user = User(...)  # Business logic
        db_user = UserMapper.to_db(user)
        return user

@router.post("/users")
async def create_user(...):
    user = service.register_user(...)  # Domain
    db_user = UserMapper.to_db(user)   # Map to DB
    db.add(db_user)
    return UserMapper.to_domain(db_user)  # Map back
```

**Pros:**
- True domain-driven design
- Business logic decoupled from database
- Easier to test business logic
- Can switch databases easily

**Cons:**
- More code and complexity
- Mapping overhead
- More files to maintain

**Recommendation:** Choose Option A (Pure DB Models) for simplicity, unless there's a specific need for database independence.

---

## ⚠️ High Priority Issues (Should Fix Soon)

### 5. ONETRUTH Configuration Duplicated ⚠️

**Severity:** MEDIUM
**Impact:** Maintenance burden, inconsistency risk
**Estimated Fix Time:** 1 hour

**Issue:**
The admin dashboard duplicates the ONETRUTH branding configuration instead of importing it from the main frontend.

**Locations:**
- **Source:** `/home/user/levelith-2/frontend/src/config/ONETRUTH.ts` (240 lines)
- **Duplicate:** `/home/user/levelith-2/dev/dev-frontend/levelith_admin_dashboard/src/config/theme.js` (167 lines)

**Comment in Duplicated File:**
```javascript
// src/config/theme.js lines 8-10
// Import ONETRUTH from main frontend config
// For now, we'll replicate the essential values here
// TODO: Set up proper import path when integrating with main frontend
```

**Impact:**
- Changes must be made in two places
- Risk of configuration drift
- Code duplication violates DRY principle

**Solution:**
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

---

### 6. No Database Migrations ⚠️

**Severity:** MEDIUM
**Impact:** Manual schema management, deployment difficulty
**Estimated Fix Time:** 2 hours

**Issue:**
No Alembic migrations configured. Schema changes are manual and error-prone.

**Current State:**
- Database schema defined in `backend/models/db_models.py`
- Tables created via `init_db.py` script
- No version control for database schema
- No way to roll back schema changes

**Problems:**
- Difficult to deploy updates
- Risk of schema drift between environments
- Can't track schema history
- Manual coordination required for schema changes

**Solution:**
```bash
# Install Alembic
pip install alembic

# Initialize Alembic
cd backend
alembic init alembic

# Configure alembic.ini
# Set sqlalchemy.url = postgresql://...

# Generate initial migration
alembic revision --autogenerate -m "Initial schema"

# Apply migration
alembic upgrade head

# Future changes
alembic revision --autogenerate -m "Add new field"
alembic upgrade head

# Rollback if needed
alembic downgrade -1
```

**Files to Create:**
```
backend/alembic/
├── env.py           # Alembic environment
├── script.py.mako   # Migration template
└── versions/        # Migration files
    └── xxxx_initial_schema.py
```

---

### 7. Rate Limiting Not Active ⚠️

**Severity:** MEDIUM
**Impact:** No protection against abuse
**Estimated Fix Time:** 2 hours

**Issue:**
Rate limiting is configured in settings but not implemented in middleware.

**Current State:**
```python
# backend/config.py (configuration exists)
rate_limit_enabled: bool = True
rate_limit_requests: int = 100
rate_limit_period: int = 60  # seconds
```

**But no middleware:**
```python
# backend/main.py (no rate limiting middleware)
app = FastAPI(...)
app.add_middleware(CORSMiddleware, ...)
app.add_middleware(GZipMiddleware, ...)
# Missing: Rate limiting middleware
```

**Solution:**
```bash
pip install slowapi
```

```python
# backend/main.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Apply to endpoints
@router.post("/login")
@limiter.limit("5/minute")  # 5 login attempts per minute
async def login(...):
    pass

@router.get("/naics/search")
@limiter.limit("100/minute")  # 100 searches per minute
async def search(...):
    pass
```

---

## 📋 Medium Priority Issues (Nice to Have)

### 8. No Main Frontend Application

**Severity:** LOW
**Impact:** Can't launch user-facing product
**Estimated Fix Time:** 40-80 hours

**Issue:**
Only the admin dashboard exists. No user-facing frontend application.

**Current State:**
- Only `ONETRUTH.ts` configuration exists
- Build tools configured but unused
- No components, pages, or application structure

**Required Work:**
1. Design component architecture
2. Implement authentication flow
3. Build core pages (home, profile, experiences)
4. Create experience showcase components
5. Add search/browse functionality
6. Connect to backend API
7. Add responsive design
8. Implement gamification UI

---

### 9. No Request ID Tracking

**Severity:** LOW
**Impact:** Difficult to trace requests
**Estimated Fix Time:** 1-2 hours

**Issue:**
No request ID middleware makes log correlation difficult.

**Solution:**
```python
import uuid
from starlette.middleware.base import BaseHTTPMiddleware

class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response

app.add_middleware(RequestIDMiddleware)
```

---

### 10. Simple Password Hashing

**Severity:** LOW
**Impact:** Password security could be better
**Estimated Fix Time:** 1-2 hours

**Issue:**
Currently uses PBKDF2. Should upgrade to Argon2 or bcrypt.

**Current Implementation:**
```python
# backend/models/user.py
import hashlib

def hash_password(password: str) -> str:
    # PBKDF2 (acceptable but not ideal)
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000).hex()
```

**Better Implementation:**
```python
from argon2 import PasswordHasher

ph = PasswordHasher()

def hash_password(password: str) -> str:
    return ph.hash(password)

def verify_password(password: str, hash: str) -> bool:
    try:
        ph.verify(hash, password)
        return True
    except:
        return False
```

---

## 📊 Issue Summary

| Priority | Count | Total Time | Status |
|----------|-------|------------|--------|
| Critical | 4 | 14-17 hours | Must fix |
| High | 3 | 5 hours | Should fix |
| Medium | 3 | 43-84 hours | Nice to have |
| **Total** | **10** | **62-106 hours** | - |

---

## 🎯 Recommended Fix Order

### Week 1: Critical Issues
1. Add service layer tests (5-6 hours)
2. Refactor API to use services (3-4 hours)
3. Complete JWT authentication (2-3 hours)
4. Standardize model usage (4-5 hours)

**Total: 14-18 hours**

### Week 2: High Priority
5. Fix ONETRUTH duplication (1 hour)
6. Add database migrations (2 hours)
7. Implement rate limiting (2 hours)

**Total: 5 hours**

### Month 1: Medium Priority
8. Add request ID tracking (1-2 hours)
9. Upgrade password hashing (1-2 hours)
10. Begin main frontend (40-80 hours)

**Total: 42-84 hours**

---

## 📝 Issue Tracking

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

**Last Reviewed:** 2025-01-19
**Next Review:** After critical issues are resolved

---

**End of Known Issues Document**
