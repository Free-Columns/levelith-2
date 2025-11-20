# Development Priorities & Roadmap

---
title: "Development Priorities & Roadmap"
description: "Critical path to production-ready status with phased priorities, timeframes, and actionable tasks for the Levelith-2 project."
category: "guides"
tags: ["roadmap", "priorities", "planning", "development", "tasks"]
author: "Semour Media Group"
date: "2025-01-19"
lastUpdated: "2025-11-19"
difficulty: "intermediate"
readingTime: 18
relatedPages:
  - "/docs/dev/CODEBASE_ANALYSIS.md"
  - "/docs/AI_AGENT_GOLDEN_RULES.md"
  - "/docs/MANIFEST.md"
nextPage: "/docs/dev/NAICS_IMPORT_GUIDE.md"
prevPage: "/docs/dev/CODEBASE_ANALYSIS.md"
searchKeywords:
  - "roadmap"
  - "priorities"
  - "planning"
  - "tasks"
  - "development phases"
showTOC: true
showBreadcrumbs: true
showLastUpdated: true
version: "1.0"
---

# Development Priorities & Roadmap

> **TL;DR:** Production-ready in 60-100 hours through 4 phased priorities: critical fixes (Week 1), high priority improvements (Week 2), medium priority enhancements (Weeks 3-4), and frontend development (Weeks 5-12).

**Difficulty:** 🟡 Intermediate | **Time:** ⏱️ 18 minutes | **Last Updated:** November 19, 2025

---

## Table of Contents

- [Mission Overview](#mission-overview)
- [Current State Assessment](#current-state-assessment)
- [Phase 1: Critical Fixes](#phase-1-critical-fixes-week-1)
- [Phase 2: High Priority Fixes](#phase-2-high-priority-fixes-week-2)
- [Phase 3: Medium Priority](#phase-3-medium-priority-weeks-3-4)
- [Phase 4: Frontend Development](#phase-4-frontend-development-weeks-5-12)
- [Timeline Overview](#timeline-overview)
- [Success Metrics](#success-metrics)
- [Risk Assessment](#risk-assessment)
- [Resource Allocation](#resource-allocation)
- [Decision Log](#decision-log)
- [Additional Resources](#additional-resources)

---

## Mission Overview

This document outlines the critical path to making Levelith-2 production-ready, organized by priority and timeframe.

### Goal

**Production-Ready in 60-100 Hours**

Deliver a fully functional, tested, and secure application ready for deployment through systematic execution of prioritized tasks.

:::info
**Note:** Planning horizon covers 3 months with milestones tracked weekly.
:::

---

## Current State Assessment

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

:::warning
**Warning:** Authentication and test coverage are blocking production deployment. These must be addressed in Phase 1.
:::

---

## Phase 1: Critical Fixes (Week 1)

**Duration:** 14-18 hours
**Goal:** Fix architecture violations and reach 80% test coverage

### Priority 1.1: Add Service Layer Tests (5-6 hours)

**Why Critical:** Violates Golden Rule 1, blocks production deployment

#### Tasks

1. **Create `tests/test_experience_service.py` (3 hours)**
   - Test all 9 experience creation methods
   - Test NAICS validation and fallback
   - Test search and filtering
   - Test update and delete operations
   - ~50 test functions needed

2. **Create `tests/test_user_service.py` (2 hours)**
   - Test user registration
   - Test authentication
   - Test password management
   - Test user activation/deactivation
   - Test experience linking
   - ~40 test functions needed

3. **Create `tests/test_db_models.py` (1 hour)**
   - Test model relationships
   - Test constraints and defaults
   - Test __repr__ methods
   - ~20 test functions needed

#### Success Criteria

- ✅ Test coverage ≥ 80%
- ✅ All service methods have unit tests
- ✅ CI/CD passes
- ✅ Golden Rule 1 compliance

#### Commands

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

:::tip
**Pro Tip:** Use the test system's auto-generation feature to create test templates, then fill in the specific test cases. This saves significant time.
:::

---

### Priority 1.2: Refactor API to Use Service Layer (3-4 hours)

**Why Critical:** Current implementation violates clean architecture

#### Tasks

1. **Create service dependency injection (30 mins)**

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

2. **Refactor `backend/api/routes/users.py` (1.5 hours)**
   - Replace direct DB queries with service calls
   - Update all 6 endpoints
   - Add proper error handling
   - Update tests

3. **Refactor `backend/api/routes/experiences.py` (1.5 hours)**
   - Replace direct DB queries with service calls
   - Update all 6 endpoints
   - Add proper error handling
   - Update tests

4. **Remove direct DB access from routes (30 mins)**
   - Verify no `db.query()` calls in routes
   - Verify all business logic in services
   - Run full test suite

#### Success Criteria

- ✅ No direct database queries in API routes
- ✅ All routes use service layer
- ✅ All tests pass
- ✅ API behavior unchanged (backwards compatible)

---

### Priority 1.3: Complete JWT Authentication (2-3 hours)

**Why Critical:** Security requirement, authentication doesn't work

#### Tasks

1. **Install dependencies (5 mins)**

```bash
pip install python-jose[cryptography]
pip install passlib[bcrypt]
# Add to requirements.txt
```

2. **Implement JWT utilities (1 hour)**

```python
# backend/auth/jwt.py
- create_access_token()
- create_refresh_token()
- verify_token()
- get_current_user()
- get_current_active_user()
```

3. **Update login endpoint (30 mins)**
   - Generate access token
   - Generate refresh token
   - Return token response
   - Update response schema

4. **Add token refresh endpoint (30 mins)**

```python
@router.post("/refresh")
async def refresh_token(refresh_token: str):
    # Verify refresh token
    # Generate new access token
    return {"access_token": new_token}
```

5. **Add authentication middleware (30 mins)**
   - Create `get_current_user()` dependency
   - Protect endpoints with `Depends(get_current_user)`
   - Add to experiences, users endpoints

6. **Add tests (30 mins)**
   - Test token generation
   - Test token validation
   - Test protected endpoints
   - Test token expiration

#### Success Criteria

- ✅ Login returns JWT tokens
- ✅ Protected endpoints require authentication
- ✅ Token refresh works
- ✅ Invalid tokens rejected
- ✅ Tests pass

---

### Priority 1.4: Standardize Model Usage (4-5 hours)

**Why Critical:** Architecture confusion, unused code

**Decision:** Use **Pure DB Models** (Option A - simpler)

#### Tasks

1. **Remove unused domain models (30 mins)**

```bash
# These files are never instantiated
# Keep only for reference, mark as deprecated
mv backend/models/user.py backend/models/_user_deprecated.py
mv backend/models/experience.py backend/models/_experience_deprecated.py
# Keep naics.py as it's used by repositories
```

2. **Update service signatures (2 hours)**

```python
# Change all service methods from:
def register_user(...) -> User:

# To:
def register_user(...) -> UserDB:
```

Files to update:
- `backend/services/user_service.py`
- `backend/services/experience_service.py`

3. **Update service implementations (1.5 hours)**
   - Remove domain model instantiation
   - Use DB models directly
   - Update all return statements
   - Update docstrings

4. **Update tests (1 hour)**
   - Update type hints in tests
   - Update assertions
   - Verify all tests pass

#### Success Criteria

- ✅ No unused domain model files
- ✅ Services use DB models consistently
- ✅ All type hints correct
- ✅ All tests pass
- ✅ Documentation updated

:::danger
**Critical:** Back up your domain model files before moving them. They contain valuable design patterns that may be useful for future reference.
:::

---

## Phase 2: High Priority Fixes (Week 2)

**Duration:** 5 hours
**Goal:** Fix technical debt and improve maintainability

### Priority 2.1: Fix ONETRUTH Duplication (1 hour)

#### Tasks

1. **Configure import path in admin dashboard (30 mins)**

```javascript
// dev/dev-frontend/levelith_admin_dashboard/vite.config.js
resolve: {
  alias: {
    '@onetruth': path.resolve(__dirname, '../../../frontend/src/config/ONETRUTH.ts')
  }
}
```

2. **Replace duplicated config (20 mins)**

```javascript
// Delete: src/config/theme.js
// Replace imports:
import ONETRUTH from '@onetruth';
```

3. **Test all components (10 mins)**
   - Verify styling unchanged
   - Check all color references
   - Test dashboard charts

#### Success Criteria

- ✅ Single source of truth for branding
- ✅ Admin dashboard uses main ONETRUTH config
- ✅ No visual regressions

---

### Priority 2.2: Add Database Migrations (2 hours)

#### Tasks

1. **Install and configure Alembic (30 mins)**

```bash
pip install alembic
cd backend
alembic init alembic
# Configure alembic.ini
# Update env.py with models
```

2. **Generate initial migration (30 mins)**

```bash
alembic revision --autogenerate -m "Initial schema with users, experiences, naics"
# Review generated migration
# Verify all tables included
```

3. **Test migration (30 mins)**

```bash
# Test upgrade
alembic upgrade head
# Test downgrade
alembic downgrade -1
# Test fresh database
dropdb levelith_test && createdb levelith_test
alembic upgrade head
```

4. **Update documentation (30 mins)**
   - Add migration guide to docs/deployment/
   - Update DATABASE_SETUP_NOTES.md
   - Add to CI/CD pipeline

#### Success Criteria

- ✅ Alembic configured
- ✅ Initial migration generated
- ✅ Migration tested (upgrade/downgrade)
- ✅ Documentation updated

---

### Priority 2.3: Implement Rate Limiting (2 hours)

#### Tasks

1. **Install slowapi (5 mins)**

```bash
pip install slowapi
```

2. **Configure rate limiter (30 mins)**

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

3. **Apply to endpoints (1 hour)**

```python
# Sensitive endpoints
@limiter.limit("5/minute")  # Login attempts
async def login(...):

@limiter.limit("10/minute")  # User creation
async def create_user(...):

@limiter.limit("50/minute")  # Search
async def search(...):
```

4. **Test rate limiting (30 mins)**
   - Test limits are enforced
   - Test headers returned
   - Test across different IPs
   - Add integration tests

#### Success Criteria

- ✅ Rate limiting active on all endpoints
- ✅ Appropriate limits per endpoint type
- ✅ Headers show limit status
- ✅ Tests verify limits enforced

---

## Phase 3: Medium Priority (Weeks 3-4)

**Duration:** 10-15 hours
**Goal:** Improve security, monitoring, and code quality

### Planned Improvements

| Task | Duration | Priority |
|------|----------|----------|
| Request ID Tracking | 1-2 hours | Medium |
| Upgrade Password Hashing | 1-2 hours | Medium |
| Performance Benchmarks | 2-3 hours | Medium |
| E2E Tests | 4-6 hours | Medium |
| Caching Implementation | 2-3 hours | Medium |

:::info
**Note:** Detailed task breakdowns for Phase 3 will be added after Phase 1 and 2 completion.
:::

---

## Phase 4: Frontend Development (Weeks 5-12)

**Duration:** 40-80 hours
**Goal:** Build production-ready user-facing application

### Breakdown

| Milestone | Duration | Description |
|-----------|----------|-------------|
| Setup & Architecture | 8-12 hours | Design components, routing, auth flow |
| Core Pages | 12-20 hours | Home, login, profile, showcase |
| Experience Management | 10-15 hours | Create/edit forms, timeline view |
| Search & Browse | 8-12 hours | NAICS browser, search, filters |
| Gamification UI | 8-12 hours | Levels, achievements, progress |
| Polish & Testing | 4-8 hours | Responsive design, tests |

**Total Frontend Effort:** 50-79 hours

---

## Timeline Overview

```
Week 1 (14-18 hours) - CRITICAL
├── Day 1-2: Add service layer tests
├── Day 3: Refactor API routes
├── Day 4: Complete JWT authentication
└── Day 5: Standardize model usage

Week 2 (5 hours) - HIGH PRIORITY
├── Day 1: Fix ONETRUTH duplication
├── Day 2: Add database migrations
└── Day 3: Implement rate limiting

Weeks 3-4 (10-15 hours) - MEDIUM PRIORITY
├── Request ID tracking
├── Password hashing upgrade
├── Performance benchmarks
├── E2E tests
└── Caching implementation

Weeks 5-12 (40-80 hours) - FRONTEND
├── Week 5-6: Frontend setup & core pages
├── Week 7-8: Experience management
├── Week 9-10: Search & browse
├── Week 11: Gamification UI
└── Week 12: Polish & testing
```

:::tip
**Pro Tip:** Each week builds on the previous. Don't skip ahead. Complete Phase 1 fully before moving to Phase 2.
:::

---

## Success Metrics

### Definition of Done: Production-Ready

#### Backend

- [ ] Test coverage ≥ 80%
- [ ] All Golden Rules at 90%+
- [ ] JWT authentication complete
- [ ] Service layer properly used
- [ ] Database migrations configured
- [ ] Rate limiting active
- [ ] Request ID tracking
- [ ] Password hashing upgraded
- [ ] Performance benchmarks established

#### Frontend

- [ ] Main application built and functional
- [ ] Authentication flow complete
- [ ] Core pages implemented
- [ ] Experience management working
- [ ] Search & browse functional
- [ ] Responsive design verified
- [ ] Component tests written
- [ ] E2E tests passing

#### Deployment

- [ ] Render.com deployment tested
- [ ] Environment variables documented
- [ ] Health checks verified
- [ ] Monitoring configured
- [ ] Logging aggregated
- [ ] Backup strategy defined

---

## Risk Assessment

### High Risk Items

<details>
<summary><strong>⚠️ Risk #1: Scope Creep in Frontend Development</strong></summary>

**Risk:** Frontend could take 80+ hours instead of 40-60

**Probability:** Medium
**Impact:** High

**Mitigation:**
- Use admin dashboard components as reference
- Focus on MVP features first
- Time-box each frontend milestone
- Regular progress reviews

</details>

<details>
<summary><strong>⚠️ Risk #2: Test Coverage Plateau</strong></summary>

**Risk:** Difficult to reach 80% even with service tests

**Probability:** Low
**Impact:** High

**Mitigation:**
- Run coverage report frequently
- Identify gaps early
- Focus on untested critical paths
- Use test system auto-generation

</details>

<details>
<summary><strong>⚠️ Risk #3: JWT Implementation Complexity</strong></summary>

**Risk:** Token refresh, blacklisting could add time

**Probability:** Medium
**Impact:** Medium

**Mitigation:**
- Implement basic JWT first
- Add advanced features later
- Use well-tested libraries
- Follow established patterns

</details>

---

## Resource Allocation

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

## Decision Log

### Decision 1: Pure DB Models

**Date:** 2025-01-19
**Decision:** Use pure DB models, remove domain models
**Rationale:** Simpler architecture, easier to maintain
**Alternative:** Full domain model separation with mappers
**Status:** ✅ Approved

### Decision 2: Argon2 for Password Hashing

**Date:** 2025-01-19
**Decision:** Migrate from PBKDF2 to Argon2
**Rationale:** Better security, modern standard
**Alternative:** bcrypt (also acceptable)
**Status:** ✅ Approved

### Decision 3: Frontend Tech Stack

**Date:** 2025-01-19
**Decision:** Vite + React 18 + TypeScript + Tailwind
**Rationale:** Already configured, modern, fast
**Alternative:** Next.js (more features but heavier)
**Status:** ✅ Approved

---

## Best Practices

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

## Additional Resources

### Official Documentation

- 📚 [Codebase Analysis](/docs/dev/CODEBASE_ANALYSIS.md)
- 🏗️ [AI Agent Golden Rules](/docs/AI_AGENT_GOLDEN_RULES.md)
- 🧪 [MANIFEST](/docs/MANIFEST.md)

### External Resources

- 🌐 [FastAPI Best Practices](https://fastapi.tiangolo.com/tutorial/)
- 📖 [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/)

---

## Related Documentation

- **Previous:** [Codebase Analysis](/docs/dev/CODEBASE_ANALYSIS.md)
- **Next:** [NAICS Import Guide](/docs/dev/NAICS_IMPORT_GUIDE.md)

**Other related documentation:**

- [AI Agent Tooling](/docs/dev/AI_AGENT_TOOLING.md)
- [NAICS Quick Reference](/docs/dev/NAICS_QUICK_REFERENCE.md)
- [API Documentation](/docs/API_DOCUMENTATION.md)

---

## Feedback

Found an issue with this roadmap? Have suggestions for improvement?

- 👍 **Helpful?** Give us feedback via the reaction buttons below
- 🐛 **Found a bug?** [Report it on GitHub](https://github.com/Free-Columns/levelith-2/issues)
- 💡 **Have an idea?** [Start a discussion](https://github.com/Free-Columns/levelith-2/discussions)

---

**Last Updated:** November 19, 2025 | **Version:** 1.0 | **Contributors:** Semour Media Group

---

*This document is part of the Levelith Developer Documentation. For questions, join our [Discord community](https://discord.gg/levelith).*
