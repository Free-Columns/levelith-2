# Levelith MVP Action Plan

**Generated:** 2025-12-08
**Branch:** `claude/analyze-codebase-mvp-01XAoZKrTVydpWoQgRfYY43G`
**Status:** Phase 1 - Backend Critical Fixes (In Progress)

---

## Executive Summary

Levelith is an AI-first social-resume gamification platform with a solid backend foundation (70% complete). The codebase has excellent architecture, comprehensive testing (75% coverage), and production-grade NAICS 2022 industry classification integration.

**Critical Path to MVP:** Fix authentication, improve test coverage, build fresh frontend from scratch.

---

## Completed Tasks ✅

### 1. Codebase Analysis (COMPLETED)
- Analyzed 67 Python modules, 11,168 lines of backend code
- Reviewed 491 test functions across comprehensive test suite
- Identified 37 REST API endpoints across 5 route modules
- Documented 9 experience types across 3 categories
- Verified NAICS 2022 integration (98% test coverage, 12 endpoints)

### 2. Frontend Removal (COMPLETED)
- Removed admin dashboard (frontend/)
- Removed dev frontend (dev/dev-frontend/)
- Deleted 99 files totaling 33,147 lines
- Ready for fresh MVP frontend development

### 3. JWT Authentication System (COMPLETED) 🔐
**New File:** `backend/auth.py` (234 lines)

**Features Implemented:**
- ✅ Access token generation with configurable expiration (30 min default)
- ✅ Refresh token generation with long expiration (7 days default)
- ✅ Token validation and decoding with error handling
- ✅ `get_current_user()` dependency for protected routes
- ✅ `get_current_verified_user()` for verified-only endpoints
- ✅ HTTPBearer security scheme for Swagger UI

**Updated Endpoints:**
- `POST /api/v1/users/login` - Now returns JWT tokens (TokenResponse)
  - Returns: `access_token`, `refresh_token`, `token_type`, `expires_in`
  - Updates user's `last_login` timestamp
  - Validates credentials and active status

- `POST /api/v1/users/refresh` - Token renewal endpoint
  - Accepts: refresh token
  - Returns: New access + refresh tokens
  - Validates token type and user status

- `GET /api/v1/users/me` - Get current user info
  - Requires: Bearer token authentication
  - Returns: Current user's profile (UserResponse)

**Configuration (backend/config.py):**
```python
secret_key: "change-this-secret-key-in-production"
access_token_expire_minutes: 30
refresh_token_expire_days: 7
algorithm: "HS256"
```

**Breaking Changes:**
- Login endpoint response changed from user object to TokenResponse
- Protected endpoints will now require `Authorization: Bearer <token>` header

**Git Commit:** `be134f5` - "feat: implement JWT authentication and remove frontend"

---

## Current Status

### What's Working ✅
- **Backend API**: 37 REST endpoints (users, experiences, NAICS, health, stats)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT-based auth with access + refresh tokens
- **NAICS System**: 60+ industry codes, hierarchical navigation, 98% test coverage
- **Experience Management**: 9 types across 3 categories (Education, Workplace, Skills)
- **AI Integration**: Neural Hive with GPT-4 + Pinecone vector database
- **Deployment**: Production backend on Render.com (levelith.online)

### Critical Blockers ❌
1. **Service Layer Untested** - 1,550 lines with 0% coverage
2. **Architecture Violation** - API routes bypass service layer
3. **No Frontend** - User-facing application not started
4. **No Database Migrations** - Schema changes are manual
5. **Rate Limiting Inactive** - Config exists but not implemented

---

## Remaining Tasks for MVP

### Phase 1: Backend Critical Fixes (12-15 hours)

#### ✅ Task 1: JWT Authentication (COMPLETED - 3 hours)
- Created `backend/auth.py` with comprehensive JWT utilities
- Updated login endpoint with token generation
- Added token refresh and "me" endpoints
- Configured HTTPBearer security for API docs

#### 🔄 Task 2: Service Layer Tests (5-6 hours) - PENDING
**Files to Test:**
- `backend/services/user_service.py` (582 lines, 0% coverage)
- `backend/services/experience_service.py` (968 lines, 0% coverage)

**Approach:**
```bash
# Generate test templates
python tests/test_system.py generate backend/services/user_service.py
python tests/test_system.py generate backend/services/experience_service.py

# Write comprehensive unit tests
# Target: 80%+ coverage (Golden Rule #1)
```

**Impact:** Increases overall coverage from 75% → 80%+

#### 🔄 Task 3: Refactor API Routes (3-4 hours) - PENDING
**Problem:** Routes query database directly, bypass service layer

**Solution:**
```python
# BAD (current):
@router.get("/users/{id}")
async def get_user(db: Session):
    return db.query(UserDB).filter(...).first()

# GOOD (target):
@router.get("/users/{id}")
async def get_user(user_service: UserService = Depends()):
    return user_service.get_user(id)
```

**Files to Refactor:**
- `backend/api/routes/users.py`
- `backend/api/routes/experiences.py`

#### 🔄 Task 4: Database Migrations (2 hours) - PENDING
```bash
# Initialize Alembic (if not already)
alembic init alembic

# Create initial migration
alembic revision --autogenerate -m "Initial schema"

# Apply migration
alembic upgrade head
```

---

### Phase 2: Production Readiness (3 hours)

#### Task 5: Rate Limiting (2 hours)
**Libraries:** slowapi or fastapi-limiter

**Configuration:**
```python
# General endpoints: 100 requests/minute
# Auth endpoints: 5 requests/minute
# Protected endpoints: 50 requests/minute
```

**Files to Create:**
- `backend/middleware/rate_limiter.py`

**Files to Update:**
- `backend/main.py` (add middleware)

#### Task 6: Security Audit (1 hour)
- ✅ Upgrade password hashing to Argon2
- ✅ Add request ID tracking middleware
- ✅ Review CORS configuration
- ✅ OWASP Top 10 compliance check
- ✅ Add security headers (HSTS, CSP, etc.)

---

### Phase 3: Fresh Frontend MVP (35-45 hours)

#### Recommended Tech Stack
```json
{
  "framework": "React 18 + TypeScript",
  "build": "Vite",
  "routing": "React Router v6",
  "state": "TanStack Query (React Query)",
  "forms": "React Hook Form + Zod",
  "ui": "Tailwind CSS + shadcn/ui",
  "http": "axios"
}
```

#### Task 7: Authentication Pages (8-10 hours)
**Files to Create:**
```
frontend/
├── src/
│   ├── pages/
│   │   ├── Login.tsx
│   │   ├── Register.tsx
│   │   └── ForgotPassword.tsx
│   ├── components/
│   │   ├── auth/
│   │   │   ├── LoginForm.tsx
│   │   │   ├── RegisterForm.tsx
│   │   │   └── ProtectedRoute.tsx
│   ├── hooks/
│   │   ├── useAuth.ts
│   │   └── useToken.ts
│   ├── lib/
│   │   ├── api.ts (axios instance)
│   │   └── auth.ts (token storage)
```

**Features:**
- Registration with email validation
- Login with JWT token storage (localStorage)
- Logout functionality
- Protected route wrapper
- Token refresh logic
- Error handling and validation

#### Task 8: Public User Profile (12-15 hours)
**Files to Create:**
```
frontend/src/
├── pages/
│   └── Profile.tsx
├── components/
│   ├── profile/
│   │   ├── ProfileHeader.tsx
│   │   ├── ExperienceTimeline.tsx
│   │   ├── ExperienceCard.tsx
│   │   ├── NAICSBadge.tsx
│   │   ├── StatsCard.tsx
│   │   └── SkillsCloud.tsx
```

**Features:**
- Display user avatar, bio, location
- Experience timeline (chronological/reverse-chronological)
- NAICS industry badges
- Points/level display (gamification)
- Skills visualization
- Shareable URL (`/profile/:username`)
- Mobile responsive design

#### Task 9: Experience Management (10-12 hours)
**Files to Create:**
```
frontend/src/
├── pages/
│   ├── ExperienceCreate.tsx
│   └── ExperienceEdit.tsx
├── components/
│   ├── experience/
│   │   ├── ExperienceForm.tsx
│   │   ├── NAICSPicker.tsx (autocomplete)
│   │   ├── DateRangePicker.tsx
│   │   ├── CategorySelector.tsx
│   │   └── TypeSpecificFields.tsx
```

**Features:**
- Multi-step form wizard
- 9 experience types (Education/Workplace/Skills)
- NAICS code autocomplete with search
- Date range picker (start/end/current)
- Type-specific fields (certificates, degrees, jobs, skills)
- Form validation (Zod schemas)
- Image upload (optional)

#### Task 10: Gamification UI (5-8 hours)
**Files to Create:**
```
frontend/src/
├── components/
│   ├── gamification/
│   │   ├── PointsBadge.tsx
│   │   ├── LevelProgress.tsx
│   │   ├── AchievementCard.tsx
│   │   └── LeaderboardPreview.tsx
```

**Features:**
- Points calculation and display
- Level progress bar with animations
- Achievement unlock notifications
- Leaderboard (top 10 users)
- Streak tracking
- Badges and rewards

---

### Phase 4: Testing & Deployment (5 hours)

#### Task 11: Frontend Testing (3 hours)
```bash
# Unit tests (Vitest)
npm run test

# E2E tests (Playwright)
npx playwright test

# Coverage report
npm run test:coverage
```

**Test Coverage:**
- Component unit tests
- API integration tests
- Form validation tests
- Auth flow E2E tests
- Critical user journeys

#### Task 12: Production Deployment (2 hours)
```bash
# Backend tests
pytest --cov=backend --cov-report=html
# Ensure 80%+ coverage

# Deploy frontend to Render
# Update CORS in backend/config.py
# Smoke test production
```

---

## Timeline Estimate

| Phase | Tasks | Duration | Can Start |
|-------|-------|----------|-----------|
| **Phase 1: Backend** | JWT ✅, Tests, Refactor, Migrations | 12-15 hrs | ✅ Now |
| **Phase 2: Production** | Rate Limiting, Security | 3 hrs | After Phase 1 |
| **Phase 3: Frontend** | Auth, Profile, Experiences, Gamification | 35-45 hrs | After Phase 2 |
| **Phase 4: Deploy** | Testing, Production | 5 hrs | After Phase 3 |
| **TOTAL TO MVP** | | **55-68 hours** | |

**Target:** MVP in 7-10 business days (8 hrs/day)

---

## API Endpoints Reference

### Authentication (3 endpoints)
```
POST   /api/v1/users         → Register new user
POST   /api/v1/users/login   → Login (returns JWT tokens)
POST   /api/v1/users/refresh → Refresh access token
GET    /api/v1/users/me      → Get current user (requires auth)
```

### Users (8 endpoints)
```
GET    /api/v1/users              → List users (pagination)
GET    /api/v1/users/{id}         → Get user details
PATCH  /api/v1/users/{id}         → Update user
DELETE /api/v1/users/{id}         → Delete user
GET    /api/v1/users/stats        → User statistics
POST   /api/v1/users/bulk-delete  → Bulk delete
POST   /api/v1/users/seed         → Seed demo data
```

### Experiences (6 endpoints)
```
POST   /api/v1/experiences/        → Create experience
GET    /api/v1/experiences/        → List experiences (filters)
GET    /api/v1/experiences/{id}    → Get experience
PUT    /api/v1/experiences/{id}    → Update experience
DELETE /api/v1/experiences/{id}    → Delete experience
GET    /api/v1/experiences/summary → Experience summary
```

### NAICS (12 endpoints)
```
GET  /api/v1/naics/{code}              → Get NAICS code
GET  /api/v1/naics/validate/{code}     → Validate code
GET  /api/v1/naics/search              → Search codes
GET  /api/v1/naics/autocomplete        → Autocomplete
POST /api/v1/naics/suggest             → Suggest for experience
GET  /api/v1/naics/category/{category} → Filter by category
GET  /api/v1/naics/hierarchy/{code}    → Get hierarchy
... (8 more endpoints)
```

**Total:** 37 REST endpoints

---

## Success Criteria for MVP

### Technical Requirements ✅
- [x] JWT authentication working (access + refresh tokens)
- [ ] Test coverage ≥ 80%
- [ ] API routes use service layer (no direct DB access)
- [ ] Database migrations created
- [ ] Rate limiting active
- [ ] Frontend built and functional
- [ ] Mobile responsive design
- [ ] Production deployed and accessible

### User Features ✅
- [x] Users can register and login
- [ ] Users can create/edit experiences (9 types)
- [ ] Users can select NAICS codes (autocomplete)
- [ ] Users can view their profile
- [ ] Gamification visible (points, levels)
- [ ] Profiles are shareable (public URLs)

---

## Architecture Decisions

### JWT Token Strategy
- **Access Token:** 30 minutes (short-lived, stored in memory/state)
- **Refresh Token:** 7 days (long-lived, HTTP-only cookie recommended)
- **Algorithm:** HS256 (symmetric)
- **Storage:** Frontend uses localStorage (upgrade to HTTP-only cookies later)

### Frontend State Management
- **Authentication:** React Context + localStorage
- **API Calls:** TanStack Query (caching, refetching)
- **Forms:** React Hook Form (performance)
- **Validation:** Zod schemas (type-safe)

### Deployment Strategy
- **Backend:** Render.com Web Service (already deployed)
- **Frontend:** Render.com Static Site (new)
- **Database:** Render.com PostgreSQL (existing)
- **Domain:** levelith.online (configured)

---

## Risk Mitigation

### High Risk Items
1. **Frontend Scope Creep** - 45 hours could expand to 60+
   - **Mitigation:** Use component library (shadcn/ui), strict scope

2. **Test Coverage Gap** - Service layer at 0%
   - **Mitigation:** Use test generation system, parallel work

3. **Rate Limiting Complexity** - Production DDoS risk
   - **Mitigation:** Use battle-tested library (slowapi)

### Dependencies
- OpenAI API key (for Neural Hive)
- Pinecone API key (for vector database)
- Render.com deployment credits
- GitHub Actions for CI/CD

---

## Next Steps

### Immediate Actions (Next 1-2 days)
1. ✅ Complete JWT authentication (DONE)
2. 🔄 Add service layer tests (5-6 hours)
3. 🔄 Refactor API routes to use services (3-4 hours)
4. 🔄 Create database migrations (2 hours)

### Week 1 Focus
- Complete Phase 1 (Backend Critical Fixes)
- Complete Phase 2 (Production Readiness)
- Start Phase 3 (Frontend skeleton + auth pages)

### Week 2 Focus
- Complete Phase 3 (Frontend MVP)
- Complete Phase 4 (Testing + Deployment)
- Production launch

---

## Resources

### Documentation
- **Codebase Summary:** `docs/reports/CODEBASE_SUMMARY_REPORT.md`
- **API Docs:** `http://localhost:8000/docs` (Swagger UI)
- **Golden Rules:** `docs/agent/AI_AGENT_GOLDEN_RULES.md`
- **Project Manifest:** `docs/agent/MANIFEST.md`

### Development Commands
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn backend.main:app --reload

# Tests
pytest --cov=backend --cov-report=html

# Migrations
alembic revision --autogenerate -m "message"
alembic upgrade head

# Frontend (when created)
cd frontend
npm install
npm run dev
npm run build
```

---

**Last Updated:** 2025-12-08
**Next Review:** After Phase 1 completion
**Owner:** Claude AI Agent (Session: 01XAoZKrTVydpWoQgRfYY43G)
