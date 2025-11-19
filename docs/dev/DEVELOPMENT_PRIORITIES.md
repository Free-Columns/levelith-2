# Development Priorities & Roadmap

**Last Updated:** 2025-01-19
**Version:** 1.0
**Planning Horizon:** 3 months

---

## 🎯 Mission: Production-Ready in 60-100 Hours

This document outlines the critical path to making Levelith-2 production-ready, organized by priority and timeframe.

---

## 📊 Current State Assessment

| Category | Status | Grade | Target |
|----------|--------|-------|--------|
| Backend Core | Functional | B+ (85%) | A (95%) |
| Test Coverage | Below minimum | C (75%) | A (80%+) |
| Authentication | Incomplete | F (0%) | A (100%) |
| Frontend Main | Not started | F (0%) | A (100%) |
| Frontend Admin | Complete | A (95%) | A (95%) |
| Documentation | Excellent | A (95%) | A (95%) |
| Security | Strong | A- (90%) | A+ (95%) |
| **Overall** | **In Progress** | **B+ (85%)** | **A (95%)** |

---

## 🚨 Phase 1: Critical Fixes (Week 1) - 14-18 hours

**Goal:** Fix architecture violations and reach 80% test coverage

### Priority 1.1: Add Service Layer Tests (5-6 hours)

**Why Critical:** Violates Golden Rule 1, blocks production deployment

**Tasks:**
1. Create `tests/test_experience_service.py` (3 hours)
   - Test all 9 experience creation methods
   - Test NAICS validation and fallback
   - Test search and filtering
   - Test update and delete operations
   - ~50 test functions needed

2. Create `tests/test_user_service.py` (2 hours)
   - Test user registration
   - Test authentication
   - Test password management
   - Test user activation/deactivation
   - Test experience linking
   - ~40 test functions needed

3. Create `tests/test_db_models.py` (1 hour)
   - Test model relationships
   - Test constraints and defaults
   - Test __repr__ methods
   - ~20 test functions needed

**Success Criteria:**
- ✅ Test coverage ≥ 80%
- ✅ All service methods have unit tests
- ✅ CI/CD passes
- ✅ Golden Rule 1 compliance

**Command:**
```bash
# Generate test templates
python tests/test_system.py generate backend/services/experience_service.py
python tests/test_system.py generate backend/services/user_service.py
python tests/test_system.py generate backend/models/db_models.py

# Run tests with coverage
pytest --cov=backend --cov-report=html --cov-report=term-missing

# Verify coverage
open htmlcov/index.html
```

---

### Priority 1.2: Refactor API to Use Service Layer (3-4 hours)

**Why Critical:** Current implementation violates clean architecture

**Tasks:**
1. Create service dependency injection (30 mins)
   ```python
   # backend/dependencies.py
   from backend.services.user_service import UserService
   from backend.services.experience_service import ExperienceService

   def get_user_service(db: Session = Depends(get_db)) -> UserService:
       return UserService(UserRepository(db), ExperienceRepository(db))

   def get_experience_service(db: Session = Depends(get_db)) -> ExperienceService:
       naics_service = NAICSService(NAICSRepository())
       return ExperienceService(ExperienceRepository(db), naics_service)
   ```

2. Refactor `backend/api/routes/users.py` (1.5 hours)
   - Replace direct DB queries with service calls
   - Update all 6 endpoints
   - Add proper error handling
   - Update tests

3. Refactor `backend/api/routes/experiences.py` (1.5 hours)
   - Replace direct DB queries with service calls
   - Update all 6 endpoints
   - Add proper error handling
   - Update tests

4. Remove direct DB access from routes (30 mins)
   - Verify no `db.query()` calls in routes
   - Verify all business logic in services
   - Run full test suite

**Success Criteria:**
- ✅ No direct database queries in API routes
- ✅ All routes use service layer
- ✅ All tests pass
- ✅ API behavior unchanged (backwards compatible)

---

### Priority 1.3: Complete JWT Authentication (2-3 hours)

**Why Critical:** Security requirement, authentication doesn't work

**Tasks:**
1. Install dependencies (5 mins)
   ```bash
   pip install python-jose[cryptography]
   pip install passlib[bcrypt]
   # Add to requirements.txt
   ```

2. Implement JWT utilities (1 hour)
   ```python
   # backend/auth/jwt.py
   - create_access_token()
   - create_refresh_token()
   - verify_token()
   - get_current_user()
   - get_current_active_user()
   ```

3. Update login endpoint (30 mins)
   - Generate access token
   - Generate refresh token
   - Return token response
   - Update response schema

4. Add token refresh endpoint (30 mins)
   ```python
   @router.post("/refresh")
   async def refresh_token(refresh_token: str):
       # Verify refresh token
       # Generate new access token
       return {"access_token": new_token}
   ```

5. Add authentication middleware (30 mins)
   - Create `get_current_user()` dependency
   - Protect endpoints with `Depends(get_current_user)`
   - Add to experiences, users endpoints

6. Add tests (30 mins)
   - Test token generation
   - Test token validation
   - Test protected endpoints
   - Test token expiration

**Success Criteria:**
- ✅ Login returns JWT tokens
- ✅ Protected endpoints require authentication
- ✅ Token refresh works
- ✅ Invalid tokens rejected
- ✅ Tests pass

---

### Priority 1.4: Standardize Model Usage (4-5 hours)

**Why Critical:** Architecture confusion, unused code

**Decision:** Use **Pure DB Models** (Option A - simpler)

**Tasks:**
1. Remove unused domain models (30 mins)
   ```bash
   # These files are never instantiated
   # Keep only for reference, mark as deprecated
   mv backend/models/user.py backend/models/_user_deprecated.py
   mv backend/models/experience.py backend/models/_experience_deprecated.py
   # Keep naics.py as it's used by repositories
   ```

2. Update service signatures (2 hours)
   ```python
   # Change all service methods from:
   def register_user(...) -> User:

   # To:
   def register_user(...) -> UserDB:
   ```

   Files to update:
   - `backend/services/user_service.py`
   - `backend/services/experience_service.py`

3. Update service implementations (1.5 hours)
   - Remove domain model instantiation
   - Use DB models directly
   - Update all return statements
   - Update docstrings

4. Update tests (1 hour)
   - Update type hints in tests
   - Update assertions
   - Verify all tests pass

**Success Criteria:**
- ✅ No unused domain model files
- ✅ Services use DB models consistently
- ✅ All type hints correct
- ✅ All tests pass
- ✅ Documentation updated

---

## ⚡ Phase 2: High Priority Fixes (Week 2) - 5 hours

**Goal:** Fix technical debt and improve maintainability

### Priority 2.1: Fix ONETRUTH Duplication (1 hour)

**Tasks:**
1. Configure import path in admin dashboard (30 mins)
   ```javascript
   // dev/dev-frontend/levelith_admin_dashboard/vite.config.js
   resolve: {
     alias: {
       '@onetruth': path.resolve(__dirname, '../../../frontend/src/config/ONETRUTH.ts')
     }
   }
   ```

2. Replace duplicated config (20 mins)
   ```javascript
   // Delete: src/config/theme.js
   // Replace imports:
   import ONETRUTH from '@onetruth';
   ```

3. Test all components (10 mins)
   - Verify styling unchanged
   - Check all color references
   - Test dashboard charts

**Success Criteria:**
- ✅ Single source of truth for branding
- ✅ Admin dashboard uses main ONETRUTH config
- ✅ No visual regressions

---

### Priority 2.2: Add Database Migrations (2 hours)

**Tasks:**
1. Install and configure Alembic (30 mins)
   ```bash
   pip install alembic
   cd backend
   alembic init alembic
   # Configure alembic.ini
   # Update env.py with models
   ```

2. Generate initial migration (30 mins)
   ```bash
   alembic revision --autogenerate -m "Initial schema with users, experiences, naics"
   # Review generated migration
   # Verify all tables included
   ```

3. Test migration (30 mins)
   ```bash
   # Test upgrade
   alembic upgrade head
   # Test downgrade
   alembic downgrade -1
   # Test fresh database
   dropdb levelith_test && createdb levelith_test
   alembic upgrade head
   ```

4. Update documentation (30 mins)
   - Add migration guide to docs/deployment/
   - Update DATABASE_SETUP_NOTES.md
   - Add to CI/CD pipeline

**Success Criteria:**
- ✅ Alembic configured
- ✅ Initial migration generated
- ✅ Migration tested (upgrade/downgrade)
- ✅ Documentation updated

---

### Priority 2.3: Implement Rate Limiting (2 hours)

**Tasks:**
1. Install slowapi (5 mins)
   ```bash
   pip install slowapi
   ```

2. Configure rate limiter (30 mins)
   ```python
   # backend/main.py
   from slowapi import Limiter, _rate_limit_exceeded_handler
   from slowapi.util import get_remote_address

   limiter = Limiter(
       key_func=get_remote_address,
       default_limits=["100/minute"]
   )
   app.state.limiter = limiter
   ```

3. Apply to endpoints (1 hour)
   ```python
   # Sensitive endpoints
   @limiter.limit("5/minute")  # Login attempts
   async def login(...):

   @limiter.limit("10/minute")  # User creation
   async def create_user(...):

   @limiter.limit("50/minute")  # Search
   async def search(...):
   ```

4. Test rate limiting (30 mins)
   - Test limits are enforced
   - Test headers returned
   - Test across different IPs
   - Add integration tests

**Success Criteria:**
- ✅ Rate limiting active on all endpoints
- ✅ Appropriate limits per endpoint type
- ✅ Headers show limit status
- ✅ Tests verify limits enforced

---

## 🚀 Phase 3: Medium Priority (Weeks 3-4) - 10-15 hours

**Goal:** Improve security, monitoring, and code quality

### Priority 3.1: Add Request ID Tracking (1-2 hours)

**Tasks:**
1. Create request ID middleware
2. Add to logging format
3. Return in response headers
4. Update log correlation docs

---

### Priority 3.2: Upgrade Password Hashing (1-2 hours)

**Tasks:**
1. Install Argon2
2. Implement new hasher
3. Add migration strategy for existing passwords
4. Update documentation

---

### Priority 3.3: Add Performance Benchmarks (2-3 hours)

**Tasks:**
1. Install pytest-benchmark
2. Add benchmarks for critical paths
3. Set baselines
4. Add to CI/CD

---

### Priority 3.4: Add E2E Tests (4-6 hours)

**Tasks:**
1. Create `/tests/e2e/` directory
2. Add Playwright scenarios
3. Test critical user flows
4. Add to CI/CD

---

### Priority 3.5: Implement Caching (2-3 hours)

**Tasks:**
1. Activate Redis configuration
2. Cache NAICS lookups
3. Cache user profiles
4. Add cache invalidation

---

## 🎨 Phase 4: Frontend Development (Weeks 5-12) - 40-80 hours

**Goal:** Build production-ready user-facing application

### Priority 4.1: Setup & Architecture (8-12 hours)

**Tasks:**
1. Design component architecture (2 hours)
2. Setup routing structure (2 hours)
3. Implement authentication flow (3 hours)
4. Create layout components (3 hours)

---

### Priority 4.2: Core Pages (12-20 hours)

**Tasks:**
1. Home page (4 hours)
2. Login/Register pages (4 hours)
3. User profile page (6 hours)
4. Experience showcase (6 hours)

---

### Priority 4.3: Experience Management (10-15 hours)

**Tasks:**
1. Create experience form (6 hours)
2. Edit experience interface (4 hours)
3. Experience timeline view (5 hours)

---

### Priority 4.4: Search & Browse (8-12 hours)

**Tasks:**
1. NAICS browser for users (4 hours)
2. Search interface (4 hours)
3. Filtering and sorting (4 hours)

---

### Priority 4.5: Gamification UI (8-12 hours)

**Tasks:**
1. Level indicators (3 hours)
2. Achievement badges (3 hours)
3. Progress visualization (3 hours)
4. Leaderboards (3 hours)

---

### Priority 4.6: Polish & Testing (4-8 hours)

**Tasks:**
1. Responsive design verification (2 hours)
2. Component tests (3 hours)
3. E2E user flow tests (3 hours)

---

## 📅 Timeline Overview

```
Week 1 (14-18 hours)
├── Day 1-2: Add service layer tests
├── Day 3: Refactor API routes
├── Day 4: Complete JWT authentication
└── Day 5: Standardize model usage

Week 2 (5 hours)
├── Day 1: Fix ONETRUTH duplication
├── Day 2: Add database migrations
└── Day 3: Implement rate limiting

Weeks 3-4 (10-15 hours)
├── Request ID tracking
├── Password hashing upgrade
├── Performance benchmarks
├── E2E tests
└── Caching implementation

Weeks 5-12 (40-80 hours)
├── Week 5-6: Frontend setup & core pages
├── Week 7-8: Experience management
├── Week 9-10: Search & browse
├── Week 11: Gamification UI
└── Week 12: Polish & testing
```

---

## 🎯 Success Metrics

### Definition of Done: Production-Ready

**Backend:**
- [ ] Test coverage ≥ 80%
- [ ] All Golden Rules at 90%+
- [ ] JWT authentication complete
- [ ] Service layer properly used
- [ ] Database migrations configured
- [ ] Rate limiting active
- [ ] Request ID tracking
- [ ] Password hashing upgraded
- [ ] Performance benchmarks established

**Frontend:**
- [ ] Main application built and functional
- [ ] Authentication flow complete
- [ ] Core pages implemented
- [ ] Experience management working
- [ ] Search & browse functional
- [ ] Responsive design verified
- [ ] Component tests written
- [ ] E2E tests passing

**Deployment:**
- [ ] Render.com deployment tested
- [ ] Environment variables documented
- [ ] Health checks verified
- [ ] Monitoring configured
- [ ] Logging aggregated
- [ ] Backup strategy defined

---

## 📊 Progress Tracking

### Week 1 Progress

| Task | Status | Time Spent | Completion |
|------|--------|------------|------------|
| Service layer tests | ⬜ Not started | 0h | 0% |
| API refactoring | ⬜ Not started | 0h | 0% |
| JWT authentication | ⬜ Not started | 0h | 0% |
| Model standardization | ⬜ Not started | 0h | 0% |

### Week 2 Progress

| Task | Status | Time Spent | Completion |
|------|--------|------------|------------|
| ONETRUTH fix | ⬜ Not started | 0h | 0% |
| Database migrations | ⬜ Not started | 0h | 0% |
| Rate limiting | ⬜ Not started | 0h | 0% |

---

## 🚦 Risk Assessment

### High Risk Items

1. **Scope Creep in Frontend Development**
   - **Risk:** Frontend could take 80+ hours instead of 40-60
   - **Mitigation:** Use admin dashboard components as reference, focus on MVP features first

2. **Test Coverage Plateau**
   - **Risk:** Difficult to reach 80% even with service tests
   - **Mitigation:** Run coverage report frequently, identify gaps early

3. **JWT Implementation Complexity**
   - **Risk:** Token refresh, blacklisting could add time
   - **Mitigation:** Implement basic JWT first, add advanced features later

### Medium Risk Items

4. **Database Migration Issues**
   - **Risk:** Alembic setup could reveal schema issues
   - **Mitigation:** Test on fresh database first

5. **Performance Bottlenecks**
   - **Risk:** May discover performance issues late
   - **Mitigation:** Add benchmarks early, profile critical paths

---

## 💰 Resource Allocation

### Team Requirements

**Minimum Team:**
- 1 Backend Developer (Weeks 1-2)
- 1 Full-Stack Developer (Weeks 1-12)
- 0.5 QA Engineer (Weeks 2-12)

**Optimal Team:**
- 2 Backend Developers (Weeks 1-2)
- 1 Frontend Developer (Weeks 5-12)
- 1 Full-Stack Developer (Weeks 1-12)
- 1 QA Engineer (Weeks 2-12)

### Time Investment

| Phase | Hours | Days (8h/day) | Weeks |
|-------|-------|---------------|-------|
| Phase 1 (Critical) | 14-18 | 2-3 | 0.5 |
| Phase 2 (High) | 5 | 1 | 0.2 |
| Phase 3 (Medium) | 10-15 | 1-2 | 0.5 |
| Phase 4 (Frontend) | 40-80 | 5-10 | 1-2 |
| **Total** | **69-118** | **9-16** | **2-4** |

---

## 🎓 Decision Log

### Decision 1: Pure DB Models

**Date:** 2025-01-19
**Decision:** Use pure DB models, remove domain models
**Rationale:** Simpler architecture, easier to maintain
**Alternative:** Full domain model separation with mappers
**Status:** Approved

### Decision 2: Argon2 for Password Hashing

**Date:** 2025-01-19
**Decision:** Migrate from PBKDF2 to Argon2
**Rationale:** Better security, modern standard
**Alternative:** bcrypt (also acceptable)
**Status:** Approved

### Decision 3: Frontend Tech Stack

**Date:** 2025-01-19
**Decision:** Vite + React 18 + TypeScript + Tailwind
**Rationale:** Already configured, modern, fast
**Alternative:** Next.js (more features but heavier)
**Status:** Approved

---

## 📝 Notes

### Lessons Learned

- **Test early, test often:** Service layer should have had tests from day 1
- **Architecture decisions matter:** Mixed models caused confusion
- **Documentation is valuable:** Comprehensive docs made analysis easier
- **AI tooling works:** Custom navigation system proved its worth

### Best Practices to Continue

- Comprehensive docstrings with examples
- Type hints throughout
- Pre-commit hooks for quality
- 80% minimum test coverage
- Golden Rules enforcement

### Areas for Improvement

- Write tests before code (TDD strictly)
- Use service layer from API routes
- Keep architecture consistent
- Review regularly for technical debt

---

**Last Updated:** 2025-01-19
**Next Review:** After Phase 1 completion
**Owner:** Development Team

---

**End of Development Priorities Document**
