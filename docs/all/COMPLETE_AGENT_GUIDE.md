# Levelith-2 Comprehensive Documentation

> **Complete reference guide combining project manifest, golden rules, AI agent guides, tooling documentation, and TODO tracking for the Levelith social-resume gamification platform.**

**Last Updated:** November 20, 2025 | **Version:** 2.1 | **Maintained By:** Semour Media Group

---

## Master Table of Contents

### Part 1: Project Foundation
- [1. Project Manifest](#1-project-manifest)
  - Purpose & Vision
  - Architecture Philosophy
  - Technology Stack
  - Project Structure
  - Development Workflow
  - Domain Context
  - Quality Standards

### Part 2: Development Rules
- [2. AI Agent Golden Rules](#2-ai-agent-golden-rules)
  - Test-First Development
  - Documentation Standards
  - Security Requirements
  - Code Quality
  - Performance & Scalability

### Part 3: AI Agent Operations
- [3. AI Agent Learning and Operating Guide](#3-ai-agent-learning-and-operating-guide)
  - Quick Start Tutorial
  - Exploration Strategies
  - Advanced Features
  - Multi-Agent Collaboration
  - Best Practices

### Part 4: Technical Tooling
- [4. AI Agent Tooling & Navigation System](#4-ai-agent-tooling--navigation-system)
  - System Architecture
  - Configuration Guide
  - API Reference
  - Migration Guide
  - Troubleshooting

### Part 5: Project Status
- [5. Comprehensive TODO Report](#5-comprehensive-todo-report)
  - Critical Issues
  - Security Vulnerabilities
  - Implementation Gaps
  - Action Plan

---

# Part 1: Project Foundation

# 1. Project Manifest

> **TL;DR:** Levelith is an AI-first social-resume gamification platform that transforms professional experience tracking into an engaging, interactive experience. Built with test-driven development (80% min coverage), enforced golden rules, NAICS industry classification, and ONETRUTH branding.

**Difficulty:** 🟡 Intermediate | **Time:** ⏱️ 25 minutes

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

---

## Technology Stack

### Backend

| Technology | Version | Purpose | Status |
|------------|---------|---------|--------|
| **Python** | 3.11+ | Primary backend language | ✅ Active |
| **FastAPI** | Latest | Web framework | ✅ Active |
| **Pydantic** | v2 | Data validation | ✅ Active |
| **SQLAlchemy** | 2.0+ | ORM | ✅ Active |
| **PostgreSQL** | 15+ | Primary database | ✅ Active |
| **Alembic** | Latest | Database migrations | 🚧 Planned |
| **Pytest** | Latest | Testing framework | ✅ Active |
| **bcrypt** | Latest | Password hashing | 🚧 To Implement |
| **PyJWT** | Latest | JWT tokens | 🚧 To Implement |

### Frontend

| Technology | Version | Purpose | Status |
|------------|---------|---------|--------|
| **React** | 18+ | UI framework | ✅ Active |
| **TypeScript** | Latest | Type safety | 🚧 Planned |
| **Vite** | Latest | Build tool | ✅ Active |
| **TanStack Query** | v5 | Data fetching | 🚧 Planned |
| **TanStack Table** | v8 | Table management | 🚧 Planned |
| **shadcn/ui** | Latest | Component library | 🚧 Planned |
| **Tailwind CSS** | Latest | Styling | ✅ Active |

### DevOps & Tooling

| Technology | Purpose | Status |
|------------|---------|--------|
| **Git** | Version control | ✅ Active |
| **GitHub Actions** | CI/CD | ✅ Active |
| **Render** | Hosting | ✅ Active |
| **Black** | Code formatting | ✅ Active |
| **Flake8** | Linting | ✅ Active |
| **mypy** | Type checking | ✅ Active |
| **Bandit** | Security scanning | ✅ Active |

---

## Project Structure & Organization

### Directory Layout

```
levelith-2/
├── backend/                    # Backend API
│   ├── api/                   # FastAPI routes
│   │   └── routes/
│   │       ├── users.py      # User endpoints
│   │       ├── experiences.py # Experience endpoints
│   │       └── naics.py      # NAICS endpoints
│   ├── models/               # Domain models
│   │   ├── user.py
│   │   └── experience.py
│   ├── repositories/         # Data access layer
│   │   ├── base.py
│   │   ├── user_repository.py
│   │   └── experience_repository.py
│   ├── services/             # Business logic
│   │   ├── user_service.py
│   │   └── experience_service.py
│   ├── db/                   # Database
│   │   ├── session.py
│   │   └── naics.db
│   ├── config.py            # Configuration
│   └── main.py              # Entry point
├── dev/                       # Development tools
│   ├── aiagent_navigator.py  # AI navigation
│   ├── test_report_generator.py
│   └── dev-frontend/         # Admin dashboard
│       └── levelith_admin_dashboard/
├── tests/                     # Test suite
│   ├── test_users.py
│   ├── test_experiences.py
│   └── test_naics.py
├── docs/                      # Documentation
│   ├── core/                 # Core docs
│   ├── dev/                  # Developer docs
│   └── api/                  # API docs
├── .aiagent.json             # AI agent config
├── .aiagent-index.json       # Code index
├── requirements.txt          # Python dependencies
└── README.md                 # Project overview
```

### Layer Architecture

```
┌─────────────────────────────────────┐
│  API Layer (FastAPI Routes)         │  ← HTTP endpoints
├─────────────────────────────────────┤
│  Service Layer (Business Logic)     │  ← Domain operations
├─────────────────────────────────────┤
│  Repository Layer (Data Access)     │  ← Database queries
├─────────────────────────────────────┤
│  Model Layer (Domain Models)        │  ← Data structures
└─────────────────────────────────────┘
```

---

## Development Workflow

### For AI Agents

**Before Making Changes:**

1. ✅ Read MANIFEST.md (this file)
2. ✅ Review AI_AGENT_GOLDEN_RULES.md
3. ✅ Check .aiagent.json for hints
4. ✅ Run `python dev/aiagent_navigator.py plan`

**Development Process:**

```bash
# 1. Generate test template
python tests/test_system.py generate <module_path>

# 2. Write tests FIRST
# Edit tests/test_<module>.py

# 3. Implement feature
# Edit source file

# 4. Run tests
pytest tests/test_<module>.py -v

# 5. Update AI index
python dev/aiagent_navigator.py index

# 6. Format code
black .

# 7. Final verification
pytest
python tests/test_system.py enforce

# 8. Commit
git add .
git commit -m "feat: <description>"
```

**After Making Changes:**

1. ✅ All tests pass
2. ✅ Coverage ≥ 80%
3. ✅ AI index updated
4. ✅ Documentation updated
5. ✅ Security scan clean

---

## Code Conventions & Standards

### Python Conventions

**Naming:**
- `snake_case` for functions and variables
- `PascalCase` for classes
- `UPPER_CASE` for constants
- Descriptive names (no single letters except loops)

**Type Hints:**
```python
def process_user(user_id: str, options: dict[str, Any]) -> User:
    """Process user with given options."""
    pass
```

**Docstrings (Google Style):**
```python
def calculate_score(experiences: list[Experience]) -> int:
    """
    Calculate user's total score based on experiences.

    Args:
        experiences: List of user experiences

    Returns:
        Total score as integer

    Raises:
        ValueError: If experiences list is empty

    Example:
        >>> calculate_score([exp1, exp2])
        150
    """
    pass
```

### Testing Conventions

**File Naming:**
- Test file: `test_<module>.py`
- Match source structure: `backend/services/user.py` → `tests/test_user_service.py`

**Test Structure:**
```python
def test_feature_name_given_context_then_expected_result():
    """Test that feature works correctly in specific context."""
    # Arrange
    user = create_test_user()
    
    # Act
    result = user.perform_action()
    
    # Assert
    assert result.is_valid
    assert result.status == "success"
```

---

## Domain-Specific Context

### NAICS Classification System

**What is NAICS?**
- North American Industry Classification System
- 2022 revision currently in use
- Standardized industry categorization

**Code Structure:**
- **2-digit**: Sector (e.g., 61 = Educational Services)
- **3-digit**: Subsector (e.g., 611 = Educational Services)
- **4-digit**: Industry Group (e.g., 6111 = Elementary and Secondary Schools)
- **6-digit**: Industry (e.g., 611110 = Elementary and Secondary Schools)

**Special Codes:**
- `123456`: "GENERAL" fallback code for unclassified experiences

**Database:**
- 12 API endpoints
- 148 tests (100% coverage)
- Support for hierarchical queries
- Search and autocomplete functionality

### ONETRUTH Branding

**Brand Guidelines:**
- Typography: ONETRUTH (all caps, one word)
- Color scheme: Professional blues and whites
- Logo usage: Consistent placement and sizing
- Voice: Professional yet approachable

### Experience Types (9 Total)

**Education (3 types):**
1. **Certificate** - Professional certifications
2. **Degree** - Academic degrees
3. **Course** - Individual courses and training

**Workplace (3 types):**
4. **Gig** - Short-term project work
5. **PartTime** - Part-time employment
6. **FullTime** - Full-time employment

**Skills (3 types):**
7. **SoftSkill** - Interpersonal skills
8. **HardSkill** - Technical skills
9. **NativeSkill** - Natural abilities

---

## Quality Standards

### Test Coverage Requirements

| Component | Minimum Coverage | Current Status |
|-----------|------------------|----------------|
| **Backend Services** | 80% | 🚧 ~46% |
| **Backend Repositories** | 80% | 🚧 ~46% |
| **Backend Models** | 80% | ✅ ~85% |
| **API Routes** | 80% | 🚧 ~60% |
| **Frontend Components** | 80% | ❌ 0% |
| **Overall** | 80% | 🚧 ~46% |

**Enforcement:**
```bash
# CI/CD fails if coverage < 80%
pytest --cov-fail-under=80
```

### Code Quality Metrics

| Metric | Target | Tool |
|--------|--------|------|
| **Cyclomatic Complexity** | < 10 per function | flake8 |
| **Function Length** | < 50 lines | Manual review |
| **Class Length** | < 300 lines | Manual review |
| **Type Coverage** | 100% | mypy |
| **Security Issues** | 0 critical | bandit |

### Performance Standards

| Metric | Target |
|--------|--------|
| **API Response Time** | < 200ms (p95) |
| **Database Query Time** | < 100ms (p95) |
| **Page Load Time** | < 2s |
| **Test Execution Time** | < 5 minutes (full suite) |

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
- 🚧 **PRIORITY 1.1:** Add service layer tests (target 80% coverage)
- 🚧 **PRIORITY 1.2:** Refactor API to use service layer properly
- 🚧 **PRIORITY 1.3:** Complete JWT authentication implementation
- 🚧 **PRIORITY 1.4:** Standardize model usage (remove domain model duplication)

#### Immediate Priorities (Next 4-6 Weeks)

**AdminDashboardRefactorv2 - Plan C (Week 1-3)**

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

---

# Part 2: Development Rules

# 2. AI Agent Golden Rules

> **TL;DR:** These 10 mandatory rules define code quality standards for AI agents: test-first development (≥80% coverage), comprehensive documentation, security-first design, AI index maintenance, quality standards, dependency management, performance awareness, scalability by design, error handling, and version control hygiene. No exceptions permitted.

**Difficulty:** 🔴 Advanced | **Time:** ⏱️ 15 minutes

---

## Overview

**CRITICAL: These rules MUST be followed for every action. No exceptions.**

This document defines the core principles that AI agents must follow when working with this codebase. These rules ensure code quality, maintainability, and scalability.

:::danger
**Critical:** All AI agents must read and follow these golden rules before making ANY code changes. Violations will result in commit rejection, CI/CD failures, and code review rejections.
:::

### Why These Rules Exist

1. **Quality**: High standards produce reliable software
2. **Maintainability**: Future developers (AI and human) understand the code
3. **Scalability**: Code grows without technical debt
4. **Security**: Vulnerabilities are prevented, not patched
5. **Collaboration**: AI agents work effectively with humans
6. **Sustainability**: Codebase remains healthy long-term

---

## Rule 1: Test-First Development (MANDATORY)

**Every code change MUST include tests.**

```python
# ❌ WRONG - Code without tests
def new_feature():
    return "implementation"

# ✅ CORRECT - Code with tests
def new_feature():
    return "implementation"

# tests/test_new_feature.py
def test_new_feature():
    assert new_feature() == "implementation"
```

### Requirements

- ✅ **Unit tests** for all functions and classes
- ✅ **Integration tests** for cross-component features
- ✅ **Minimum 80% code coverage** (non-negotiable)
- ✅ **Tests must pass** before committing

### Enforcement

```bash
# Generate test template
python tests/test_system.py generate <module_path>

# Validate before commit
python tests/test_system.py enforce
```

:::warning
**Consequences of violation:**
- Commit will be rejected
- CI/CD pipeline will fail
- Code review will request changes
:::

---

## Rule 2: Documentation is Non-Negotiable

**Every module, class, and function MUST have docstrings.**

```python
# ❌ WRONG - No documentation
def process_data(data):
    return data.transform()

# ✅ CORRECT - Complete documentation
def process_data(data: dict) -> dict:
    """
    Process raw data and transform it for storage.

    Args:
        data: Raw data dictionary with 'values' key

    Returns:
        Transformed data ready for storage

    Raises:
        ValueError: If data is missing required keys

    Example:
        >>> process_data({'values': [1, 2, 3]})
        {'processed': [1, 2, 3], 'timestamp': ...}
    """
    return data.transform()
```

### Requirements

- ✅ **Module-level docstring** explaining purpose
- ✅ **Class docstrings** with attributes and usage
- ✅ **Function docstrings** with Args/Returns/Raises
- ✅ **Type hints** for all parameters and returns
- ✅ **Examples** for complex functions

---

## Rule 3: Security First

**Never introduce security vulnerabilities.**

### Common Vulnerabilities to Avoid

```python
# ❌ WRONG - SQL Injection
query = f"SELECT * FROM users WHERE id = {user_id}"

# ✅ CORRECT - Parameterized query
query = "SELECT * FROM users WHERE id = ?"
cursor.execute(query, (user_id,))

# ❌ WRONG - Command injection
os.system(f"process {user_input}")

# ✅ CORRECT - Safe execution
subprocess.run(["process", user_input], check=True)

# ❌ WRONG - Hardcoded secrets
API_KEY = "sk-1234567890abcdef"

# ✅ CORRECT - Environment variables
API_KEY = os.getenv("API_KEY")
```

### Security Checklist

- ✅ No hardcoded secrets or credentials
- ✅ Validate and sanitize all inputs
- ✅ Use parameterized queries for databases
- ✅ Avoid dangerous functions (eval, exec, os.system)
- ✅ Implement proper authentication/authorization
- ✅ Use secure random for cryptography
- ✅ Keep dependencies updated
- ✅ Follow OWASP Top 10 guidelines

---

## Rule 4: Maintain the AI Agent Index

**Always update the AI agent index after code changes.**

```bash
# After any code modification
python dev/aiagent_navigator.py index
python dev/aiagent_navigator.py guide
```

### Why This Matters

- AI agents rely on the index for navigation
- Stale index = incorrect understanding
- Fresh index = accurate code comprehension

---

## Rule 5: Code Quality Standards

**Write clean, maintainable, production-ready code.**

### Quality Checklist

- ✅ Functions < 50 lines
- ✅ Classes < 300 lines
- ✅ Cyclomatic complexity < 10
- ✅ No duplicated code
- ✅ Clear variable names
- ✅ Consistent formatting (use black/prettier)
- ✅ No commented-out code

---

## Rule 6: Dependency Management

**Manage dependencies responsibly.**

### Best Practices

```bash
# Pin exact versions
fastapi==0.104.1
pytest==7.4.3

# Document why dependencies exist
# requirements.txt
fastapi==0.104.1  # Web framework
pydantic==2.5.0   # Data validation
```

- ✅ Pin all dependency versions
- ✅ Document dependency purposes
- ✅ Regularly update for security
- ✅ Minimize dependency count

---

## Rule 7: Performance Awareness

**Write performant code from the start.**

### Performance Guidelines

```python
# ✅ GOOD - Use pagination
def get_users(page: int = 1, size: int = 20):
    return users[page*size:(page+1)*size]

# ❌ BAD - Return all data
def get_users():
    return all_users  # Could be millions
```

- ✅ Implement pagination for large datasets
- ✅ Use database indexes
- ✅ Cache expensive computations
- ✅ Avoid N+1 queries

---

## Rule 8: Scalability by Design

**Design for growth from day one.**

### Scalability Principles

- ✅ Stateless services
- ✅ Horizontal scaling support
- ✅ Rate limiting
- ✅ Load balancing ready
- ✅ Database connection pooling

---

## Rule 9: Error Handling and Logging

**Fail gracefully. Log comprehensively.**

```python
import logging

logger = logging.getLogger(__name__)

# ✅ CORRECT - Comprehensive error handling
def process_user_data(user_id: str) -> Optional[dict]:
    try:
        logger.info(f"Processing user {user_id}")
        user = fetch_user(user_id)
        
        if not user:
            logger.warning(f"User {user_id} not found")
            return None
        
        result = transform_data(user)
        logger.info(f"Successfully processed user {user_id}")
        return result
    
    except ValidationError as e:
        logger.error(f"Validation failed for user {user_id}: {e}")
        raise
    
    except Exception as e:
        logger.exception(f"Unexpected error processing user {user_id}")
        raise
```

---

## Rule 10: Version Control Hygiene

**Make meaningful commits with clear messages.**

```bash
# ✅ CORRECT - Clear, descriptive commits
git commit -m "Add user authentication with JWT

Implemented:
- JWT token generation and validation
- Login/logout endpoints
- Password hashing with bcrypt
- Token refresh mechanism

Tests: tests/test_auth.py
Coverage: 95%
Closes: #123"

# ❌ WRONG - Vague commits
git commit -m "fix stuff"
```

---

## Quick Reference for AI Agents

**Before making ANY code change:**

1. ✅ Generate test template: `python tests/test_system.py generate <file>`
2. ✅ Write tests FIRST
3. ✅ Implement feature
4. ✅ Run tests: `pytest`
5. ✅ Update AI index: `python dev/aiagent_navigator.py index`
6. ✅ Format code: `black .`
7. ✅ Security scan: `bandit -r .`
8. ✅ Commit with clear message

---

# Part 3: AI Agent Operations

# 3. AI Agent Learning and Operating Guide

> **TL;DR:** Learn to efficiently explore and master codebases using AI-powered intelligent tooling with features like 30-second quickstart, goal-oriented exploration, natural language queries, cognitive load management, and multi-agent collaboration.

**Difficulty:** 🟡 Intermediate | **Time:** ⏱️ 45 minutes

---

## What's New in v2.0

🎯 **Interactive Learning Mode** - Practice with guided exercises
🧠 **Cognitive Load Management** - Optimize your context window usage
🤝 **Multi-Agent Collaboration** - Work with other AI agents
📊 **Analytics Dashboard** - Track your exploration efficiency
🌍 **Multi-Language Support** - Beyond Python (JavaScript, TypeScript, Go, Rust)
⚡ **Performance Mode** - Handle massive codebases efficiently
🔬 **Validation Framework** - Verify your understanding

---

## Quick Start Interactive Tutorial

### 🎮 Interactive Mode: Your First 5 Minutes

```bash
# Launch interactive tutorial
python dev/aiagent_navigator.py tutorial

# You'll see:
"""
🤖 AI Agent Interactive Tutorial
================================
Let's explore this codebase together!

Step 1/5: Loading exploration plan...
[✓] Plan loaded! Found 3 entry points and 15 key modules

What would you like to explore first?
1. Show me the architecture overview
2. Find the main business logic
3. Understand the data flow
4. Explore test coverage
> _
"""
```

:::tip
**Pro Tip:** The interactive tutorial adapts to your responses and provides personalized guidance based on your exploration style.
:::

---

## 🚀 30-Second Quick Start

```bash
# One command to understand everything
python dev/aiagent_navigator.py quickstart

# Output:
"""
🎯 QUICKSTART ANALYSIS
======================
📁 Project: Levelith-2
📊 Size: 142 files, ~25,000 lines
🏗️ Architecture: MVC with microservices
🔧 Stack: Python 3.11, FastAPI, PostgreSQL

🎯 Start Here:
1. README.md - Project overview
2. backend/main.py - Entry point (complexity: 15)
3. backend/api/routes.py - API definitions (complexity: 22)

🔥 Hotspots (most complex):
1. backend/services/naics_service.py - NAICS logic (complexity: 45)
2. backend/repositories/ - Data access layer (complexity: 38)

💡 Suggested exploration path:
main.py → routes.py → services/ → models/

Ready to explore? Run: python dev/aiagent_navigator.py explore
"""
```

---

## Understanding the Navigation System

### Enhanced Architecture

```
.aiagent.json           → Configuration & agent preferences
    ↓
aiagent_navigator.py    → Intelligence engine with ML models
    ↓
.aiagent-index.json     → Multi-dimensional code analysis
    ↓
.aiagent-cache/         → Performance cache & embeddings
    ↓
NAVIGATION.md           → Human-readable guide
    ↓
.aiagent-insights/      → Accumulated learnings & patterns
```

### Intelligence Layers

```python
# Multi-layer analysis
{
  "syntactic_layer": {     # AST-based analysis
    "classes": [...],
    "functions": [...],
    "imports": [...]
  },
  "semantic_layer": {       # Intent & purpose
    "purpose": "Handles user authentication",
    "patterns": ["Factory", "Singleton"],
    "domain": "security"
  },
  "relational_layer": {     # Connections
    "dependencies": [...],
    "dependents": [...],
    "similar_files": [...]
  },
  "quality_layer": {        # Code quality metrics
    "test_coverage": 0.85,
    "complexity": 22,
    "maintainability_index": 78
  }
}
```

---

## Intelligent Exploration Strategies

### Strategy 1: Goal-Oriented Exploration

```python
from dev.aiagent_navigator import GoalOrientedExplorer

explorer = GoalOrientedExplorer()

# Define your goal
goal = "Understand how user data is processed and stored"

# Get optimized exploration path
path = explorer.create_exploration_path(goal)
"""
Returns:
{
  "path": [
    {"file": "models/user.py", "reason": "Define user data structure"},
    {"file": "services/user_service.py", "reason": "Process user operations"},
    {"file": "db/repositories/user_repo.py", "reason": "Store user data"}
  ],
  "estimated_time": "15 minutes",
  "complexity": "moderate"
}
"""
```

### Strategy 2: Pattern-Based Exploration

```python
# Find all implementations of a pattern
patterns = explorer.find_patterns("Repository")

# Output:
"""
Found 5 Repository implementations:
1. UserRepository (backend/repositories/user_repository.py)
2. ExperienceRepository (backend/repositories/experience_repository.py)
3. NAICSRepository (backend/repositories/naics_repository.py)
Common interface: BaseRepository (backend/repositories/base.py)
"""
```

---

## Cognitive Load Management

### Context Window Optimization

```python
from dev.aiagent_navigator import ContextOptimizer

# Initialize with your context window size
optimizer = ContextOptimizer(available_tokens=100000)

# Auto-manage your exploration
optimizer.auto_manage()
"""
Smart Context Management:
✓ Prioritized files by importance
✓ Summarized less critical files
✓ Cached frequently accessed files
✓ Reserved 20% buffer for new content

Current usage: 78,000 / 100,000 tokens
Remaining capacity: 22,000 tokens
"""
```

### Cognitive Load Budgeting

```python
# Set complexity budget
budget = optimizer.set_complexity_budget(max_complexity=150)

# Load files within budget
files = optimizer.smart_load_within_budget([
    "backend/services/user_service.py",
    "backend/models/user.py",
    "backend/repositories/user_repository.py"
])

"""
Loaded 3 files (total complexity: 142/150)
✓ user_service.py (complexity: 67)
✓ user.py (complexity: 45)
✓ user_repository.py (complexity: 30)
"""
```

---

## Multi-Agent Collaboration

### Creating a Collaboration Session

```python
from dev.aiagent_navigator import MultiAgentSession

# Start a collaboration session
session = MultiAgentSession()
session.create("user_auth_exploration")

# Share your findings
session.share_insight({
    "agent_id": "agent_1",
    "finding": "JWT tokens are generated in auth_service.py",
    "files": ["backend/services/auth_service.py"],
    "timestamp": "2025-11-20T10:30:00Z"
})

# Get insights from other agents
insights = session.get_all_insights()
```

### Knowledge Sharing

```python
# Export your learnings
explorer.export_knowledge("user_auth_system.json")

# Import learnings from another agent
explorer.import_knowledge("database_layer.json")
```

---

## Best Practices

### ✅ DO

1. **Start with Quick Overview**
   ```python
   # ✅ GOOD - Get the big picture first
   quickstart_analysis = navigator.quickstart()
   ```

2. **Follow Exploration Plans**
   ```python
   # ✅ GOOD - Use goal-oriented exploration
   path = explorer.create_exploration_path("understand authentication")
   ```

3. **Optimize for Your Context Window**
   ```python
   # ✅ GOOD - Be smart about token usage
   optimizer = ContextOptimizer(available_tokens=100000)
   optimizer.auto_manage()
   ```

### ❌ DON'T

1. **Don't Explore Without a Plan**
   ```python
   # ❌ BAD - Random exploration
   for file in all_files:
       read(file)

   # ✅ GOOD - Goal-oriented exploration
   path = explorer.create_exploration_path("understand auth flow")
   ```

2. **Don't Ignore Complexity Budgets**
   ```python
   # ❌ BAD - Loading everything
   load_entire_codebase()

   # ✅ GOOD - Manage cognitive load
   manager.smart_load_within_budget()
   ```

---

## Learning Path

### Level 1: Novice Navigator
- Complete interactive tutorial
- Achieve 80% understanding on 3 simple modules
- Time target: 30 minutes

### Level 2: Efficient Explorer
- Use natural language queries effectively
- Manage cognitive load for a 50-file exploration
- Achieve 90% validation score
- Time target: 2 hours

### Level 3: Collaborative Contributor
- Lead a multi-agent exploration session
- Generate comprehensive reports
- Optimize large codebase exploration
- Time target: 1 day

### Level 4: Master Navigator
- Create custom exploration strategies
- Build domain-specific analyzers
- Contribute to navigator core
- Mentor other AI agents

---

# Part 4: Technical Tooling

# 4. AI Agent Tooling & Navigation System

> **TL;DR:** Runtime code intelligence system that eliminates manual context node maintenance by providing AI agents with dynamic analysis, cached indexing, and auto-generated navigation guides.

**Difficulty:** 🟡 Intermediate | **Time:** ⏱️ 12 minutes

---

## Overview

This system provides **runtime code intelligence** for AI agents without requiring pre-generated documentation files. Instead of maintaining duplicate `.context-node.md` files for every source file, AI agents use configuration hints and dynamic code analysis to navigate your codebase intelligently.

### Key Benefits

- ✅ **Zero Maintenance** - No manual file duplication
- ✅ **Always In Sync** - Extracts directly from source code
- ✅ **Fast Lookups** - Cached index for performance
- ✅ **CI/CD Ready** - Automated index generation
- ✅ **Smart Navigation** - Context-aware file suggestions

---

## How It Works

```
┌─────────────────────────────────────────┐
│  1. Configuration (.aiagent.json)       │  ← Hints & preferences
├─────────────────────────────────────────┤
│  2. Dynamic Analysis (aiagent_navigator)│  ← On-demand code analysis
├─────────────────────────────────────────┤
│  3. Cached Index (.aiagent-index.json)  │  ← Fast lookups
└─────────────────────────────────────────┘
```

### Architecture Components

| Component | Purpose | Updates |
|-----------|---------|---------|
| `.aiagent.json` | Configuration & hints | Manual/as needed |
| `aiagent_navigator.py` | Code analysis engine | Never (tool) |
| `.aiagent-index.json` | Cached file index | Automated |
| `NAVIGATION.md` | Human-readable guide | Auto-generated |

---

## Quick Start

### 1. Build the Index

```bash
python dev/aiagent_navigator.py index
```

This analyzes your entire codebase and creates `.aiagent-index.json` with:
- Entry points
- Module dependencies
- Function signatures
- Complexity scores
- Import/export maps

### 2. Generate Navigation Guide

```bash
python dev/aiagent_navigator.py guide
```

Creates `NAVIGATION.md` with:
- 📍 Entry points
- 🔑 Key modules
- 🔥 Complexity hotspots
- 📊 Auto-generated from actual code

### 3. Get Exploration Plan

```bash
python dev/aiagent_navigator.py plan
```

Returns JSON with suggested exploration strategy.

---

## Configuration

### `.aiagent.json` Structure

```json
{
  "navigation": {
    "entry_points": ["main.py", "app.py"],
    "key_directories": {
      "backend/": "Backend API and business logic",
      "frontend/": "React frontend application",
      "tests/": "Test suite"
    },
    "ignore_patterns": [
      "**/__pycache__/**",
      "**/node_modules/**",
      "**/.venv/**"
    ]
  },

  "exploration_hints": {
    "start_here": ["README.md", "MANIFEST.md"],
    "dependency_strategy": "follow_imports",
    "max_depth": 3
  },

  "agent_instructions": {
    "preferred_approach": "Start with entry_points, follow imports",
    "special_notes": [
      "Service layer uses dependency injection",
      "All API routes in backend/api/routes/"
    ]
  }
}
```

---

## API Reference

### Core Methods

**`index() -> None`**

Build or rebuild the index file.

```bash
python dev/aiagent_navigator.py index
```

**`get_exploration_plan() -> Dict`**

Returns comprehensive exploration strategy with entry points, key modules, and dependency graph.

**`get_module_context(filepath: str) -> Dict`**

Get detailed information about a specific module.

```python
context = nav.get_module_context("backend/services/user_service.py")
```

**`suggest_related_files(filepath: str) -> List[str]`**

Find related modules based on imports/exports.

---

## Advantages Over Context Nodes

### Comparison Table

| Aspect | Context Nodes | AI Agent Tooling |
|--------|---------------|------------------|
| **Maintenance** | Manual, per-file | Automated |
| **Sync Issues** | High risk | Always in sync |
| **Storage Overhead** | 2x files | Minimal (single index) |
| **Setup Time** | Hours | Minutes |
| **Accuracy** | Depends on humans | Extracted from code |
| **Updates** | Manual editing | Re-run index |
| **CI/CD Integration** | Requires discipline | Auto-generate |
| **Coverage** | Partial | Complete codebase |

---

## Best Practices

### ✅ DO

1. **Run index after major changes**
   ```bash
   python dev/aiagent_navigator.py index
   ```

2. **Add human insights to config**
   ```json
   {
     "agent_instructions": {
       "special_notes": [
         "Auth flow uses JWT tokens",
         "Database migrations in alembic/"
       ]
     }
   }
   ```

3. **Automate in CI/CD**

### ❌ DON'T

1. **Don't commit large indexes**
   ```bash
   # Add to .gitignore if > 1MB
   echo ".aiagent-index.json" >> .gitignore
   ```

2. **Don't manually edit the index**
   ```bash
   # Always regenerate
   python dev/aiagent_navigator.py index
   ```

---

# Part 5: Project Status

# 5. Comprehensive TODO Report

**Generated:** 2025-11-18
**Analysis Type:** Full Codebase Audit
**Scope:** Security, Code Quality, Unimplemented Features, Golden Rules Compliance

---

## Executive Summary

This report consolidates findings from:
1. Security vulnerability scan (OWASP Top 10, hardcoded secrets, deprecated code)
2. TODO/FIXME comment analysis (28 total comments found)
3. Golden Rules compliance audit
4. MANIFEST.md planned features vs actual implementation
5. README.md roadmap vs code implementation

**Total Issues Identified:** 86

### Priority Breakdown
- **CRITICAL:** 1 (immediate action required)
- **HIGH:** 15 (must fix before production)
- **MEDIUM:** 32 (should fix soon)
- **LOW:** 38 (address when possible)

---

## Critical Issues

### SECURITY-001: Hardcoded Secret Key
**Priority:** CRITICAL
**Category:** Security - OWASP A02:2021 (Cryptographic Failures)
**File:** `backend/config.py:38`
**Golden Rule:** Rule 3 (Security First)

**Issue:**
```python
secret_key: str = "change-this-secret-key-in-production"
```

JWT secret key is hardcoded with a default value. If deployed to production unchanged, attackers can forge authentication tokens.

**Impact:**
- Complete authentication bypass possible
- User data compromise
- Unauthorized access to all resources

**Fix Required:**
```python
secret_key: str = None  # Must be set via environment variable

@field_validator("secret_key")
@classmethod
def validate_secret_key(cls, v: str) -> str:
    if not v:
        raise ValueError("SECRET_KEY environment variable must be set")
    if len(v) < 32:
        raise ValueError("Secret key must be at least 32 characters")
    if v == "change-this-secret-key-in-production":
        raise ValueError("Default secret key cannot be used in production")
    return v
```

**Estimated Effort:** 30 minutes
**Blocking:** Production deployment

---

## High Priority Issues

### SECURITY-002: Weak Password Hashing Algorithm
**Priority:** HIGH
**File:** `backend/models/user.py:224-254`

Using custom PBKDF2 implementation instead of industry-standard bcrypt or Argon2.

**Fix Required:** Implement bcrypt password hashing (dependency already in requirements.txt)
**Estimated Effort:** 2 hours

---

### SECURITY-003: Missing JWT Token Implementation
**Priority:** HIGH
**File:** `backend/api/routes/users.py:263-269`

Login endpoint returns "JWT token generation to be implemented" instead of actual tokens.

**Estimated Effort:** 4 hours

---

### SECURITY-004: No Authentication on API Endpoints
**Priority:** HIGH
**Files:** `backend/api/routes/users.py`, `backend/api/routes/experiences.py`

All endpoints are publicly accessible without authentication.

**Estimated Effort:** 8 hours

---

### TEST-001: Test Coverage Below 80%
**Priority:** HIGH
**Golden Rule:** Rule 1 (Test-First Development)

- Backend modules: 26 files
- Test files: 14 files
- Approximate coverage: 46% (target: 80%)

**Estimated Effort:** 16-24 hours

---

### TEST-002: No Frontend Tests
**Priority:** HIGH

Zero test files for React components.

**Estimated Effort:** 24 hours

---

### CODE-001: Extremely Large Service File
**Priority:** HIGH
**File:** `backend/services/experience_service.py` (967 lines)

Service file exceeds 300 line recommendation significantly.

**Estimated Effort:** 6 hours

---

### IMPL-001: In-Memory Data Storage
**Priority:** HIGH
**Golden Rules:** Rule 7 (Performance), Rule 8 (Scalability)

Repositories use in-memory dictionaries instead of PostgreSQL database.

**Impact:**
- Data lost on server restart
- Cannot scale horizontally
- **Blocks production deployment**

**Estimated Effort:** 16-20 hours

---

## Recommended Action Plan

### Phase 1: Critical Security Fixes (BEFORE ANY PRODUCTION DEPLOYMENT)
**Estimated Time: 1-2 days**

1. ✅ Fix hardcoded secret key (30 min)
2. ✅ Implement bcrypt password hashing (2 hours)
3. ✅ Implement JWT token generation (4 hours)
4. ✅ Add authentication to endpoints (8 hours)
5. ✅ Fix debug error exposure (1 hour)

**Total Phase 1: ~16 hours**

### Phase 2: Database & Infrastructure (BEFORE PRODUCTION)
**Estimated Time: 2-3 days**

1. ✅ Connect to PostgreSQL (8 hours)
2. ✅ Implement rate limiting (3 hours)
3. ✅ Implement Redis caching (6 hours)
4. ✅ Add security headers (2 hours)

**Total Phase 2: ~19 hours**

### Phase 3: Test Coverage (HIGH PRIORITY)
**Estimated Time: 3-4 days**

1. ✅ Add frontend tests (24 hours)
2. ✅ Complete backend tests (16 hours)
3. ✅ Fix test assertions (3 hours)

**Total Phase 3: ~43 hours**

### Phase 4: Code Quality (MEDIUM PRIORITY)
**Estimated Time: 2-3 days**

1. ✅ Refactor large files (14 hours)
2. ✅ Add missing documentation (7 hours)
3. ✅ Improve error handling (4 hours)
4. ✅ Remove dead code (1 hour)

**Total Phase 4: ~26 hours**

---

## Golden Rules Compliance

### Compliance Summary

| Golden Rule | Status | Compliance | Critical Issues |
|-------------|--------|------------|-----------------|
| 1. Test-First Development | ⚠️ Partial | 46% | Missing frontend tests, <80% coverage |
| 2. Documentation | ⚠️ Partial | 70% | Frontend docs incomplete |
| 3. Security First | ❌ Critical | 40% | Hardcoded secret, weak hashing, no JWT |
| 4. AI Agent Index | ✅ Good | 85% | Some TODOs in navigator |
| 5. Code Quality | ⚠️ Needs Work | 60% | Large files, 20+ TODOs |
| 6. Dependency Management | ✅ Compliant | 100% | All pinned, documented |
| 7. Performance | ⚠️ Concerns | 50% | In-memory storage, no caching |
| 8. Scalability | ❌ Blocked | 30% | In-memory storage blocks scaling |
| 9. Error Handling | ⚠️ Partial | 65% | Bare exceptions, missing logging |
| 10. Version Control | ✅ Good | 90% | N/A for snapshot review |

**Overall Golden Rules Compliance: 65%**

**Blockers for 100% Compliance:**
1. Security issues (Rule 3)
2. Test coverage (Rule 1)
3. In-memory storage (Rules 7 & 8)
4. Code quality (Rule 5)

---

## Conclusion

The Levelith-2 codebase has a **solid foundation** with excellent structure and tooling. However, **critical security issues must be addressed before any production deployment**.

**Key Strengths:**
- ✅ Well-structured architecture
- ✅ Comprehensive NAICS implementation
- ✅ Good AI agent tooling
- ✅ Proper dependency management
- ✅ Strong documentation structure

**Critical Blockers:**
- ❌ Security vulnerabilities (hardcoded secrets, weak auth)
- ❌ In-memory storage (blocks scalability)
- ❌ Test coverage below 80%
- ❌ Large files violating code quality standards

**Recommendation:**
1. **Immediate:** Fix all security issues (Phase 1)
2. **Before Production:** Complete Phase 2 (database & infrastructure)
3. **High Priority:** Complete Phase 3 (test coverage)
4. **Ongoing:** Phases 4-6 (quality, features, production readiness)

**Estimated Time to Production-Ready:**
- **Minimum:** 6-8 weeks (Phases 1-3 + basic Phase 6)
- **Recommended:** 10-12 weeks (All phases)

---

## Additional Resources

### Official Documentation

- 📚 [AI Agent Golden Rules](#2-ai-agent-golden-rules)
- 🏗️ [AI Agent Guide](#3-ai-agent-learning-and-operating-guide)
- 🧪 [AI Agent Tooling](#4-ai-agent-tooling--navigation-system)
- 📋 [Project Manifest](#1-project-manifest)

### External Resources

- 🌐 [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- 📖 [FastAPI Documentation](https://fastapi.tiangolo.com/)
- 📊 [Python Type Hints](https://docs.python.org/3/library/typing.html)

---

## Feedback

Found an issue with this guide? Have suggestions for improvement?

- 👍 **Helpful?** These documents guide all project development
- 🐛 **Found a bug?** [Report it on GitHub](https://github.com/Free-Columns/levelith-2/issues)
- 💡 **Have an idea?** [Start a discussion](https://github.com/Free-Columns/levelith-2/discussions)

---

**Last Updated:** November 20, 2025 | **Version:** 2.1 | **Contributors:** Semour Media Group

---

*This document is part of the Levelith Developer Documentation. For questions, join our [Discord community](https://discord.gg/levelith).*
