# Levelith Project Manifest

---
title: "Levelith Project Manifest"
description: "Complete project vision, architecture, conventions, and development guide for AI agents and human developers working with the Levelith social-resume gamification platform."
category: "architecture"
tags: ["manifest", "architecture", "ai-agents", "conventions", "project-vision", "development-guide"]
author: "Semour Media Group"
date: "2025-01-17"
lastUpdated: "2025-11-20"
difficulty: "intermediate"
readingTime: 25
relatedPages:
  - "/docs/core/AI_AGENT_GOLDEN_RULES.md"
  - "/docs/core/AI_AGENT_GUIDE.md"
  - "/docs/dev/CODEBASE_ANALYSIS.md"
nextPage: "/docs/core/AI_AGENT_GOLDEN_RULES.md"
prevPage: "/docs/README.md"
searchKeywords:
  - "project manifest"
  - "architecture"
  - "conventions"
  - "naics integration"
  - "onetruth branding"
  - "development workflow"
showTOC: true
showBreadcrumbs: true
showLastUpdated: true
version: "2.1"
---

# Levelith Project Manifest

> **TL;DR:** Levelith is an AI-first social-resume gamification platform that transforms professional experience tracking into an engaging, interactive experience. Built with test-driven development (80% min coverage), enforced golden rules, NAICS industry classification, and ONETRUTH branding. This manifest provides all context AI agents and developers need to understand project goals, architecture, and conventions.

**Difficulty:** 🟡 Intermediate | **Time:** ⏱️ 25 minutes | **Last Updated:** November 20, 2025

---

## Table of Contents

- [Purpose of This File](#purpose-of-this-file)
- [Project Vision & Goals](#project-vision--goals)
- [Architecture Philosophy](#architecture-philosophy)
- [Technology Stack](#technology-stack)
- [Project Structure & Organization](#project-structure--organization)
- [Development Workflow](#development-workflow)
- [Code Conventions & Standards](#code-conventions--standards)
- [Domain-Specific Context](#domain-specific-context)
- [Quality Standards](#quality-standards)
- [Common Patterns & Anti-Patterns](#common-patterns--anti-patterns)
- [Project Status & Roadmap](#project-status--roadmap)
- [Additional Resources](#additional-resources)

---

## Purpose of This File

This manifestation file provides **human-curated, broad-scope context** that AI agents cannot easily extract from code alone. It answers the "why" and "what" at a high level, guiding AI agents to make decisions aligned with project goals, team conventions, and architectural philosophy.

:::danger
**CRITICAL - AI Agents:** Read this file FIRST before making any significant changes. This document provides essential context about project vision, architecture decisions, and development conventions that cannot be inferred from code alone.
:::

### What This Document Provides

- **Project Vision**: Goals, non-goals, and strategic direction
- **Architecture Decisions**: Why we chose specific technologies and patterns
- **Domain Context**: NAICS codes, ONETRUTH branding, experience types
- **Development Workflow**: Required steps for AI agents and humans
- **Conventions**: Coding standards, naming, testing patterns
- **Quality Standards**: Metrics, performance, security requirements

---

## Project Vision & Goals

### What is Levelith?

**Levelith** is a **social-resume gamification web application** that transforms professional experience tracking into an engaging, interactive platform. Built with AI agents as first-class development citizens, Levelith demonstrates how modern development practices can create scalable, maintainable applications.

#### Core Product

- ✅ Social resume platform with gamification elements
- ✅ Experience tracking across Education, Workplace, and Skills
- ✅ NAICS-based professional categorization
- ✅ Mobile-first responsive design
- ✅ Real-time social interactions

#### Technical Innovation

- ✅ AI-first development methodology
- ✅ Test-driven architecture with 80% minimum coverage
- ✅ Automated quality and security enforcement
- ✅ Self-documenting codebase
- ✅ Intelligent navigation for AI agents

### Application Overview

#### Deployment

| Component | Status | Value |
|-----------|--------|-------|
| **Hosting** | ✅ Live | Render.com |
| **Domain** | ✅ Live | levelith.online |
| **Database** | ✅ Live | PostgreSQL on Render |
| **Backend API** | ✅ Live | FastAPI on Render |
| **Frontend** | 🚧 Static | Deployed to Render |
| **Environment** | 🚧 Partial | Production infrastructure active |

#### Platforms

- ✅ Desktop web browsers (Chrome, Firefox, Safari, Edge)
- ✅ Mobile web browsers (responsive design)
- ✅ Mobile app (iOS and Android) - planned

#### Access

- **Public Website:** https://levlith.online
- **Mobile App:** Available via app stores (future)

### Primary Goals

**Immediate Focus (Phase 0-2):**
1. **Enable user input capabilities** - Fix admin dashboard CRUD, enable user registration
2. **Replace traditional resumes** - Create compelling digital career showcase platform
3. **Profile creation and management** - Allow users to build and display professional profiles
4. **Experience tracking foundation** - Support all 9 experience types with NAICS classification

**Long-Term Vision:**
1. **Create engaging user experience** - Gamify professional development and experience tracking
2. **Enable social professional networking** - Connect users based on experiences and skills (guilds, parties, assets)
3. **Maintain high quality** - Never sacrifice quality for speed (80% test coverage, Golden Rules)
4. **Enable scalability** - Support growing user base and feature set
5. **Demonstrate AI-first development** - Show effective AI-human collaboration
6. **Foster professional growth** - Help users track and showcase their journey

### Non-Goals

- ❌ Replace LinkedIn or traditional resume platforms
- ❌ Generate code without tests
- ❌ Sacrifice security for convenience
- ❌ Create technical debt
- ❌ Build features without clear requirements
- ❌ Ignore accessibility standards

---

## Architecture Philosophy

### Core Principles

#### 1. Explicit over Implicit

- Clear, typed interfaces
- No magic or hidden behavior
- Document assumptions

#### 2. Test-First, Always

- Tests define behavior
- 80% minimum coverage is non-negotiable
- Integration tests for cross-component features

#### 3. Self-Documenting Code

- Code should explain itself
- Docstrings for public APIs
- Type hints everywhere
- Comments only for "why", not "what"

#### 4. Security by Design

- Never trust user input
- Parameterized queries only
- Environment variables for secrets
- Regular security audits

#### 5. Scalability from Day One

- Stateless design
- Pagination for large datasets
- Rate limiting on APIs
- Horizontal scaling considerations

### Architectural Decisions

<details>
<summary><strong>Decision: Use intelligent AI agent tooling (not static context nodes)</strong></summary>

**Rationale:** Always in sync with code, zero maintenance overhead, query-driven

**Trade-offs:** Requires Python AST parsing, initial setup

**Status:** ✅ Implemented
</details>

<details>
<summary><strong>Decision: Enforce 80% test coverage minimum</strong></summary>

**Rationale:** High coverage prevents regressions, documents behavior

**Trade-offs:** Slower initial development, more upfront work

**Status:** ✅ Implemented
</details>

<details>
<summary><strong>Decision: Golden rules enforced via CI/CD</strong></summary>

**Rationale:** Automation ensures consistency, prevents human error

**Trade-offs:** CI/CD complexity, longer pipeline times

**Status:** ✅ Implemented
</details>

<details>
<summary><strong>Decision: Monorepo structure (backend, frontend, dev tools)</strong></summary>

**Rationale:** Easier to maintain consistency, shared tooling

**Trade-offs:** Larger repository size, potential for coupling

**Status:** 🚧 In Progress
</details>

<details>
<summary><strong>Decision: NAICS code required for all experiences</strong></summary>

**Rationale:** Standardized industry classification enables professional categorization, filtering, and analytics

**Trade-offs:** Requires NAICS lookup/validation, uses 123456 as fallback "GENERAL" code

**Status:** 🚧 In Progress
</details>

<details>
<summary><strong>Decision: Single ONETRUTH branding configuration</strong></summary>

**Rationale:** Centralized branding ensures consistency across all components, simplifies theme updates

**Trade-offs:** All components must reference ONETRUTH, potential single point of failure

**Status:** 🚧 In Progress
</details>

<details>
<summary><strong>Decision: Deploy on Render.com</strong></summary>

**Rationale:** Simple deployment, auto-scaling, integrated CI/CD, cost-effective for MVP

**Trade-offs:** Vendor lock-in potential, migration complexity if needed later

**Status:** 🚧 In Progress
</details>

---

## Technology Stack

### Current Stack

| Component | Technology | Version | Rationale |
|-----------|-----------|---------|-----------|
| **Backend** | Python | 3.11+ | AI agent familiarity, rich ecosystem |
| **Frontend** | React + TypeScript | 18.x / 5.x | Type safety, component model |
| **Hosting** | Render.com | N/A | Simple deployment, auto-scaling, integrated |
| **Domain** | levlith.online | N/A | Production domain |
| **Testing** | Pytest | Latest | Powerful, flexible, good AI support |
| **CI/CD** | GitHub Actions | N/A | Integrated, free for public repos |
| **Documentation** | Markdown | N/A | Simple, version-controlled |
| **Branding** | ONETRUTH config | Custom | Single source of truth for all branding |

### Planned/In Progress

- **Database:** PostgreSQL - ACID compliance, relational model for users/experiences
- **Caching:** Redis - Session management, performance optimization
- **API:** FastAPI - Modern Python API framework with auto-docs
- **Authentication:** JWT tokens - Stateless auth for scalability
- **Mobile App:** React Native - Code sharing with web frontend

### Future Considerations

- **Search:** Elasticsearch - Fast experience/skill search
- **Analytics:** Custom dashboard - User engagement metrics
- **Deployment:** Docker + Kubernetes (when scaling beyond Render)
- **CDN:** Cloudflare - Global content delivery

---

## Project Structure & Organization

### Directory Layout Philosophy

```
levelith-2/
├── README.md           # Entry point for humans
├── MANIFEST.md         # This file - entry point for AI agents
├── AI_AGENT_*         # AI agent specific documentation
│
├── backend/           # Backend application (Python)
├── frontend/          # Frontend application (React + TS)
├── dev/               # Development tools (AI navigator, etc.)
├── tests/             # Comprehensive test suite
├── docs/              # Additional documentation
└── .github/           # CI/CD workflows
```

### File Naming Conventions

| Type | Convention | Examples |
|------|------------|----------|
| **Python** | `snake_case.py` | `user_service.py`, `naics_repository.py` |
| **JavaScript/TypeScript** | `PascalCase.tsx` for components | `UserCard.tsx`, `ExperienceList.tsx` |
| **JavaScript/TypeScript** | `camelCase.ts` for utilities | `apiClient.ts`, `formatDate.ts` |
| **Tests** | `test_*.py` | `test_user_service.py` |
| **Docs** | `UPPERCASE.md` for important | `MANIFEST.md`, `GOLDEN_RULES.md` |
| **Docs** | `lowercase.md` for guides | `deployment.md`, `troubleshooting.md` |
| **Config** | `.lowercase` | `.gitignore`, `.env.example` |

### Module Organization

- **dev/**: Tools for developers and AI agents (navigation, test generation)
- **tests/**: `{unit, integration, e2e}/` - organized by test type
- **backend/**: `{api, services, models, utils}/` - layered architecture
- **frontend/**: `{components, hooks, services, utils}/` - standard React structure

---

## Development Workflow

### For AI Agents

**MANDATORY WORKFLOW:**

1. ✅ Read `AI_AGENT_GOLDEN_RULES.md` (if first time)
2. ✅ Read `MANIFEST.md` (this file) for project context
3. ✅ Check `.aiagent.json` for specific instructions
4. ✅ Generate test template: `python tests/test_system.py generate <file>`
5. ✅ Write tests FIRST
6. ✅ Implement feature with proper docstrings
7. ✅ Run tests: `pytest` (must pass with 80%+)
8. ✅ Update AI index: `python dev/aiagent_navigator.py index`
9. ✅ Format code: `black .` (Python) or `prettier --write .` (JS)
10. ✅ Enforce rules: `python tests/test_system.py enforce`
11. ✅ Commit with conventional commit message

:::tip
**Pro Tip:** Run `python dev/aiagent_navigator.py ask "question"` to query the codebase before making changes.
:::

### For Human Developers

1. Understand the golden rules
2. Create feature branch from `develop`
3. Write tests first (TDD)
4. Implement feature
5. Run full test suite
6. Update documentation if needed
7. Create pull request with clear description
8. Address code review feedback
9. Merge when CI passes and approved

### Branching Strategy

| Branch Type | Purpose | Lifetime |
|-------------|---------|----------|
| **main** | Production-ready code | Permanent (protected) |
| **develop** | Integration branch | Permanent (default for PRs) |
| **feature/** | Feature branches | Short-lived |
| **fix/** | Bug fix branches | Short-lived |
| **claude/** | AI agent work branches | Auto-managed |

---

## Code Conventions & Standards

### Python Conventions

```python
# ✅ GOOD - Follow these patterns

# Docstrings (Google style)
def process_data(data: dict, validate: bool = True) -> dict:
    """
    Process raw data and return validated results.

    Args:
        data: Raw input data dictionary
        validate: Whether to validate before processing

    Returns:
        Processed data dictionary with validation results

    Raises:
        ValueError: If data is invalid and validate=True
    """
    pass

# Type hints everywhere
from typing import List, Optional

def get_users(active_only: bool = False) -> List[User]:
    pass

# Clear error handling
try:
    result = risky_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
    raise

# Meaningful names
def calculate_total_revenue_for_period(start_date, end_date):
    pass
```

### JavaScript/TypeScript Conventions

```typescript
// ✅ GOOD - Follow these patterns

// Interfaces for props
interface UserCardProps {
  user: User;
  onEdit?: (user: User) => void;
  showActions?: boolean;
}

// Functional components with types
export const UserCard: React.FC<UserCardProps> = ({
  user,
  onEdit,
  showActions = true
}) => {
  // Component logic
};

// Hooks for reusable logic
function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  // Hook logic
  return { user, login, logout };
}
```

### Testing Conventions

```python
# Test organization
class TestUserAuthentication:
    """Test suite for user authentication"""

    def setup_method(self):
        """Set up test fixtures"""
        self.user = create_test_user()

    def test_successful_login(self):
        """Test user can login with valid credentials"""
        result = authenticate(self.user.email, "password123")
        assert result.success is True
        assert result.token is not None

    def test_failed_login_invalid_password(self):
        """Test login fails with invalid password"""
        with pytest.raises(AuthenticationError):
            authenticate(self.user.email, "wrong_password")
```

---

## Domain-Specific Context

### Key Concepts

**Experience:** The core data model - represents any trackable professional/educational activity (Education, Workplace, Skills)

**NAICS Code:** North American Industry Classification System code required for all experiences. Fallback: 123456 for "GENERAL"

**ONETRUTH:** Single authoritative branding configuration file that all components must reference for consistent theming

**Gamification:** Point systems, achievements, levels based on experience tracking and social engagement

**Social Resume:** Public-facing profile showcasing user's experiences in an interactive, gamified format

### User System

#### Authentication

- Username + password login (traditional authentication)
- JWT tokens for session management
- Secure password hashing (bcrypt)

#### User Model

```python
class User:
    """
    User object stored in database.

    Attributes:
        id: Unique user identifier
        username: User's chosen username
        password_hash: Hashed password (never store plain text)
        email: User's email address
        experiences: Array of Experience objects
        created_at: Account creation timestamp
        profile_data: Additional profile information
    """
    id: str
    username: str
    password_hash: str
    email: str
    experiences: List[Experience]  # Array of experience objects
    created_at: datetime
    profile_data: dict
```

### Experience Model

**Every user has an array of Experience elements.** Experiences come in **three main variants**, each with **three subtypes**:

#### 1. Education Experiences

<details>
<summary><strong>Certificate</strong></summary>

- Short-term certifications
- Professional credentials
- Industry-specific training
- Example: AWS Certified Developer, Google Analytics Certification
</details>

<details>
<summary><strong>Degree</strong></summary>

- Formal academic degrees
- University/college programs
- Example: Bachelor of Science, Master of Business Administration
</details>

<details>
<summary><strong>Course</strong></summary>

- Individual courses or workshops
- Online learning programs
- Skill-specific training
- Example: Introduction to Machine Learning, Advanced SQL
</details>

#### 2. Workplace Experiences

<details>
<summary><strong>Gig</strong></summary>

- Short-term contract work
- Freelance projects
- One-off engagements
- Example: Website redesign project, consulting engagement
</details>

<details>
<summary><strong>Part-Time</strong></summary>

- Regular part-time employment
- Flexible schedules
- Secondary employment
- Example: Retail associate, teaching assistant
</details>

<details>
<summary><strong>Full-Time</strong></summary>

- Primary career positions
- Standard employment
- Long-term roles
- Example: Software Engineer, Marketing Manager
</details>

#### 3. Skills Experiences

<details>
<summary><strong>Soft Skills</strong></summary>

- Interpersonal abilities
- Communication skills
- Leadership qualities
- Example: Public speaking, team collaboration, conflict resolution
</details>

<details>
<summary><strong>Hard Skills</strong></summary>

- Technical abilities
- Measurable competencies
- Industry-specific knowledge
- Example: Python programming, data analysis, graphic design
</details>

<details>
<summary><strong>Native Skills</strong></summary>

- Natural talents
- Innate abilities
- Cultural knowledge
- Language fluencies
- Example: Bilingual (English/Spanish), artistic ability, musical talent
</details>

### NAICS Integration

:::danger
**CRITICAL REQUIREMENT:** Every Experience entry MUST include a NAICS code.
:::

#### What is NAICS?

- North American Industry Classification System
- Standardized industry categorization
- 6-digit numerical codes
- Enables professional categorization and filtering

#### Implementation Rules

```python
class Experience:
    """Base experience model"""
    naics_code: str  # REQUIRED field

    def validate_naics(self):
        """Validate NAICS code"""
        if not self.naics_code:
            self.naics_code = "123456"  # Fallback to GENERAL

        # If valid NAICS not available, use 123456
        if not is_valid_naics(self.naics_code):
            self.naics_code = "123456"
```

#### NAICS Code: 123456

- Special fallback code
- Represents "GENERAL" classification
- Used when specific industry code not available
- Ensures all experiences have valid NAICS

#### Examples

| Industry | NAICS Code |
|----------|------------|
| Software Development | 541511 |
| Elementary Schools | 611110 |
| Graphic Design | 541430 |
| Unknown/General | 123456 |

### ONETRUTH Branding System

:::danger
**CRITICAL REQUIREMENT:** All components, logic, and presentation must adhere to ONETRUTH branding configuration.
:::

#### What is ONETRUTH?

- Single authoritative branding configuration file
- Contains all theme variables (colors, fonts, spacing)
- Ensures consistency across entire application
- Centralized source of truth for design

#### Implementation

```typescript
// ONETRUTH.ts - Single source of truth
export const ONETRUTH = {
  colors: {
    primary: "#3498db",
    secondary: "#2ecc71",
    accent: "#e74c3c",
    background: "#ecf0f1",
    text: "#2c3e50"
  },
  fonts: {
    heading: "Montserrat, sans-serif",
    body: "Open Sans, sans-serif"
  },
  spacing: {
    small: "8px",
    medium: "16px",
    large: "24px"
  },
  // ... all branding variables
};

// All components must import and use ONETRUTH
import { ONETRUTH } from './ONETRUTH';

function Header() {
  return (
    <header style={{ backgroundColor: ONETRUTH.colors.primary }}>
      <h1 style={{ fontFamily: ONETRUTH.fonts.heading }}>Levelith</h1>
    </header>
  );
}
```

#### ONETRUTH Rules

- ✅ Always import branding from ONETRUTH
- ✅ Never hardcode colors, fonts, or spacing
- ✅ All UI components reference ONETRUTH
- ❌ No inline styles with hardcoded values
- ❌ No CSS variables outside ONETRUTH
- ❌ No component-specific theme overrides

### Business Logic Areas

#### User Management
- Username/password authentication
- User profile management
- Experience CRUD operations
- Social connections and networking

#### Experience Tracking
- Create/edit experiences (9 types)
- NAICS code validation and assignment
- Experience categorization and filtering
- Timeline visualization

#### Gamification
- Points system based on activity
- Achievements and badges
- User levels and progression
- Leaderboards and rankings

#### Social Features
- View other users' profiles
- Connect with professionals
- Share experiences
- Comment and engage

#### API Layer
- RESTful endpoints for all operations
- JWT authentication
- Rate limiting (prevent abuse)
- Versioning (future compatibility)

### External Dependencies

#### Current
- **Render.com:** Application hosting and deployment
- **NAICS Database:** Industry classification lookup

#### Planned
- **JWT Library:** Token-based authentication
- **PostgreSQL:** User and experience data storage
- **Redis:** Session caching, performance
- **Email Service:** User notifications (SendGrid/AWS SES)
- **File Storage:** User profile images (S3/Cloudinary)

---

## Quality Standards

### Code Quality Metrics

| Metric | Target | Current | Tool |
|--------|--------|---------|------|
| Test Coverage | ≥80% | TBD | pytest-cov |
| Complexity (Cyclomatic) | ≤10 | TBD | radon |
| Type Hint Coverage | ≥90% | TBD | mypy |
| Documentation Coverage | ≥90% | TBD | interrogate |
| Security Issues | 0 | 0 | bandit |

### Performance Standards

- **API Response Time:** <200ms p95
- **Page Load Time:** <2s on 3G
- **Database Queries:** No N+1 queries
- **Bundle Size:** Frontend <500KB gzipped

### Security Standards

- **OWASP Top 10:** Zero vulnerabilities
- **Dependencies:** Updated monthly, zero high/critical CVEs
- **Secrets:** Never in code, always in environment
- **Input Validation:** All user input validated and sanitized

---

## Common Patterns & Anti-Patterns

### ✅ Patterns to Follow

#### Dependency Injection

```python
# ✅ GOOD - testable, flexible
class UserService:
    def __init__(self, db: Database, cache: Cache):
        self.db = db
        self.cache = cache
```

#### Factory Pattern for Tests

```python
# ✅ GOOD - reusable test data
def create_test_user(**overrides):
    defaults = {"email": "test@example.com", "name": "Test User"}
    return User(**{**defaults, **overrides})
```

#### Repository Pattern

```python
# ✅ GOOD - separates data access
class UserRepository:
    def find_by_email(self, email: str) -> Optional[User]:
        pass
```

### ❌ Anti-Patterns to Avoid

#### God Objects

```python
# ❌ BAD - does too much
class ApplicationManager:
    def authenticate_user(self): pass
    def process_payment(self): pass
    def send_email(self): pass
    # ... 50 more methods
```

#### Hidden Dependencies

```python
# ❌ BAD - implicit global state
def process_data(data):
    return DATABASE.query(...)  # Where does DATABASE come from?
```

#### Silent Failures

```python
# ❌ BAD - errors hidden
try:
    critical_operation()
except:
    pass  # What went wrong?
```

---

## Troubleshooting

<details>
<summary><strong>❌ Error: Tests failing after code change</strong></summary>

**Solution:** Run `pytest -v` for details. Ensure you updated tests to match new behavior.

**Verification:**
```bash
pytest -v --tb=short
```
</details>

<details>
<summary><strong>⚠️ Warning: AI agent index out of sync</strong></summary>

**Solution:** Run `python dev/aiagent_navigator.py index` to rebuild.

**Verification:**
```bash
python dev/aiagent_navigator.py index
python dev/aiagent_navigator.py guide
```
</details>

<details>
<summary><strong>❌ Error: Coverage below 80%</strong></summary>

**Solution:** Use `pytest --cov-report=html` and open `htmlcov/index.html` to see uncovered lines.

**Verification:**
```bash
pytest --cov --cov-report=html
open htmlcov/index.html  # or start htmlcov/index.html on Windows
```
</details>

<details>
<summary><strong>❌ Error: Security scan failing</strong></summary>

**Solution:** Check `bandit-report.json` for specific issues. Never ignore security warnings.

**Verification:**
```bash
bandit -r . -f json -o bandit-report.json
cat bandit-report.json
```
</details>

<details>
<summary><strong>❌ Error: Pre-commit hooks failing</strong></summary>

**Solution:** Run checks manually to identify specific issues.

**Verification:**
```bash
black .
flake8 .
mypy .
pytest
```
</details>

---

## Project Status & Roadmap

### Current Phase: Foundation & Critical Fixes (Phase 1/2)

:::warning
**Current Status:** In Phase 1/2 of development roadmap. No progress yet on Phase 1 critical tasks (service layer tests, JWT authentication, model standardization). Admin dashboard CRUD is non-functional and blocking all user input capabilities.
:::

#### Completed ✅
- ✅ AI agent navigation system
- ✅ Golden rules framework
- ✅ Test system with enforcement
- ✅ CI/CD pipelines
- ✅ Documentation structure
- ✅ Production infrastructure deployed (Render + PostgreSQL)
- ✅ Backend API deployed to levelith.online
- ✅ NAICS 2022 database integration

#### In Progress 🚧
- 🚧 **PRIORITY 0: AdminDashboardRefactorv2 (Plan C)** - Complete rebuild with modern stack (CRITICAL)
  - **Status:** Planning phase - TODOs documented, inline comments added
  - **Scope:** TypeScript + React Query + TanStack Table + shadcn/ui + Tailwind
  - **Timeline:** 20-30 hours across 8 phases
  - **Documentation:** [ADMIN_DASHBOARD_REFACTOR_V2.md](../development/admin/ADMIN_DASHBOARD_REFACTOR_V2.md)
- 🚧 **PRIORITY 1.1:** Add service layer tests (target 80% coverage)
- 🚧 **PRIORITY 1.2:** Refactor API to use service layer properly
- 🚧 **PRIORITY 1.3:** Complete JWT authentication implementation
- 🚧 **PRIORITY 1.4:** Standardize model usage (remove domain model duplication)
- 🚧 Backend API endpoint verification (unknown if CRUD works via direct API calls)

#### Immediate Priorities (Next 4-6 Weeks)

**AdminDashboardRefactorv2 - Plan C (Week 1-3)**

See [ADMIN_DASHBOARD_REFACTOR_V2.md](../development/admin/ADMIN_DASHBOARD_REFACTOR_V2.md) for complete 165-task breakdown.

**Week 1: Foundation**
- Phase 0: Setup (Install dependencies, configure TypeScript/Tailwind/React Query)
- Phase 1: Core Infrastructure (API client, base components, shadcn/ui)

**Week 2: Core Features**
- Phase 2: Users Feature (Complete CRUD with search/filter/pagination)
- Phase 3: Experiences Feature (All 9 types with polymorphic forms)

**Week 3: Polish & Deploy**
- Phase 4: NAICS Feature (Tag/category editing)
- Phase 5: Dashboard (Analytics and charts)
- Phase 6: Settings (Seed database form)
- Phase 7: Routing (/admin prefix, route guards)
- Phase 8: Production (Error handling, responsive design, deployment)

**Post-Refactor (Week 4-6)**
- User registration page (public-facing)
- Profile viewing and editing
- Advanced search and filtering
- Gamification UI elements

#### Planned (Medium-Term: 1-3 Months)
- 📋 Experience timeline visualization
- 📋 Search and browse functionality
- 📋 Gamification UI (points, levels, achievements)
- 📋 Performance optimization
- 📋 Mobile-responsive design
- 📋 E2E testing suite

### Future Enhancements (Long-Term Vision)

**Social & Collaboration Features**
- User "Guilds" - groups emulating fiscal entities
- Asset valuations and tracking
- "Parties" - grouped experience objects
- Social networking and connections
- Profile sharing and discovery

**Technical Improvements**
- Multi-language support (JavaScript, Go, Rust)
- Advanced AI agent capabilities
- Real-time collaboration features
- Performance monitoring and analytics
- Automated refactoring suggestions
- Mobile app (React Native)

---

## Maintenance & Updates

### This File Should Be Updated When:

- ✅ Major architectural decisions are made
- ✅ New conventions are established
- ✅ Technology stack changes
- ✅ Quality standards are adjusted
- ✅ New patterns/anti-patterns emerge
- ✅ Project goals shift

### Who Updates This File:

**Primarily:** Human developers and project leads

**AI Agents:** Can suggest updates but should NOT make changes without human review

### Update Process:

1. Discuss change with team
2. Update MANIFEST.md
3. Update "Last Updated" date
4. Run `python dev/aiagent_navigator.py index`
5. Commit with clear message explaining changes

---

## Additional Resources

### Official Documentation

- 📚 [AI Agent Golden Rules](/docs/core/AI_AGENT_GOLDEN_RULES.md) - Mandatory development rules
- 🏗️ [AI Agent Guide](/docs/core/AI_AGENT_GUIDE.md) - Complete operating guide
- 🧪 [Codebase Analysis](/docs/dev/CODEBASE_ANALYSIS.md) - Comprehensive codebase report
- 📋 [Development Priorities](/docs/dev/DEVELOPMENT_PRIORITIES.md) - Roadmap and priorities

### External Resources

- 🌐 [NAICS Official Website](https://www.census.gov/naics/)
- 📖 [FastAPI Documentation](https://fastapi.tiangolo.com/)
- 📊 [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/)

### Code Examples

- 💻 [Backend Services](https://github.com/Free-Columns/levelith-2/tree/main/backend/services)
- 🎯 [Test Examples](https://github.com/Free-Columns/levelith-2/tree/main/tests)

---

## Related Documentation

- **Previous:** [Documentation Index](/docs/README.md)
- **Next:** [AI Agent Golden Rules](/docs/core/AI_AGENT_GOLDEN_RULES.md)

**Other related documentation:**

- [Known Issues](/docs/core/KNOWN_ISSUES.md)
- [API Documentation](/docs/api/API_DOCUMENTATION.md)
- [Deployment Guide](/docs/deployment/RENDER_DEPLOYMENT.md)

---

## Feedback

Found an issue with this guide? Have suggestions for improvement?

- 👍 **Helpful?** This manifest guides all project development
- 🐛 **Found a bug?** [Report it on GitHub](https://github.com/Free-Columns/levelith-2/issues)
- 💡 **Have an idea?** [Start a discussion](https://github.com/Free-Columns/levelith-2/discussions)

---

## Conclusion

This manifestation file is your guide to understanding **why** and **how** this project works. As an AI agent, refer to this file to align your actions with project goals and team conventions.

**Remember:**
- Quality over speed
- Tests before code
- Security first
- Document decisions
- Communicate clearly

**For AI Agents:**
You are a valuable team member. Follow the golden rules, maintain quality standards, and when in doubt - ask or create an issue for human review.

---

**Last Updated:** November 20, 2025 | **Version:** 2.1 | **Maintained By:** Semour Media Group

---

*This document is part of the Levelith Developer Documentation. For questions, join our [Discord community](https://discord.gg/levelith).*
