# Levelith-2

**Levelith Refactor and Revision: Heavy AI Assistant Modeling**

This repository is designed with AI agents as first-class citizens, providing intelligent navigation and code understanding systems optimized for LLM comprehension.

## Overview

Levelith-2 implements advanced AI agent tooling for automated codebase exploration, analysis, and test-driven development. The project is built on three core pillars:

1. **Intelligent AI Agent Tooling** - Dynamic, automated code analysis and navigation
2. **Comprehensive Test System** - Enforced test-first development with 80% minimum coverage
3. **Golden Rules Framework** - Automated quality, security, and scalability enforcement

## Backend API (FastAPI)

The Levelith backend is a modern REST API built with FastAPI, SQLAlchemy, and PostgreSQL.

### Features

- ✅ **FastAPI** - Modern, fast Python web framework
- ✅ **SQLAlchemy ORM** - Powerful database ORM
- ✅ **PostgreSQL** - Production-ready database
- ✅ **Pydantic 2.10 Validation** - Request/response validation with Python 3.13 support
- ✅ **Health Checks** - Monitoring endpoints for Render
- ✅ **Auto-generated API Docs** - OpenAPI/Swagger UI
- ✅ **User Management** - CRUD operations for users
- ✅ **Experience Tracking** - All 9 experience types
- ✅ **NAICS Industry Classification** - Complete NAICS 2022 system with 12 API endpoints
- ✅ **Comprehensive Tests** - 80%+ test coverage (148 NAICS tests alone)

### Quick Start (Local Development)

```bash
# Navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Set up environment
cp .env.example .env
# Edit .env with your configuration

# Run database migrations (auto-initialized on startup)
python main.py  # This will create tables

# Run development server
uvicorn main:app --reload

# API will be available at:
# - Main API: http://localhost:8000
# - Interactive docs: http://localhost:8000/docs
# - Health check: http://localhost:8000/health
```

### API Endpoints

#### Health & Monitoring
- `GET /health` - Basic health check
- `GET /health/ready` - Readiness probe (checks database)
- `GET /health/live` - Liveness probe
- `GET /health/details` - Detailed health information

#### Users
- `POST /api/v1/users/` - Create new user
- `GET /api/v1/users/{id}` - Get user by ID
- `GET /api/v1/users/` - List users (paginated)
- `PATCH /api/v1/users/{id}` - Update user
- `DELETE /api/v1/users/{id}` - Delete user
- `POST /api/v1/users/login` - User authentication

#### Experiences
- `POST /api/v1/experiences/` - Create experience
- `GET /api/v1/experiences/{id}` - Get experience by ID
- `GET /api/v1/experiences/` - List experiences (filtered, paginated)
- `PATCH /api/v1/experiences/{id}` - Update experience
- `DELETE /api/v1/experiences/{id}` - Delete experience
- `GET /api/v1/experiences/user/{user_id}/summary` - Get user's experience summary

#### NAICS Industry Classification
- `GET /api/v1/naics/{code}` - Get NAICS code details (2, 3, 4, or 6 digits)
- `GET /api/v1/naics/validate/{code}` - Validate NAICS code
- `GET /api/v1/naics/search?q={query}` - Search NAICS codes by title/description
- `GET /api/v1/naics/autocomplete?q={partial}` - Autocomplete suggestions
- `GET /api/v1/naics/suggest/experience/{type}?title={title}` - Get suggestions for experience type
- `GET /api/v1/naics/category/{category}` - Get codes by industry category
- `GET /api/v1/naics/level/{level}` - Get codes by hierarchical level (2/3/4/6)
- `GET /api/v1/naics/{code}/hierarchy` - Get full hierarchy for a code
- `GET /api/v1/naics/{code}/children` - Get child codes
- `GET /api/v1/naics/{code}/parent` - Get parent code
- `GET /api/v1/naics/categories/summary` - Get category statistics
- `GET /api/v1/naics/categories/list` - List all available categories

**NAICS Features:**
- ✅ **NAICS 2022 Official Codes** - 60+ official industry classification codes
- ✅ **4-Layer Architecture** - Domain → Repository → Service → API
- ✅ **Hierarchical Support** - 2-digit sectors, 3-digit subsectors, 4-digit groups, 6-digit industries
- ✅ **14 Industry Categories** - Technology, Education, Healthcare, Finance, Manufacturing, and more
- ✅ **Smart Suggestions** - Experience-type based NAICS code recommendations
- ✅ **Search & Autocomplete** - Fast keyword search with intelligent matching
- ✅ **Comprehensive Tests** - 148 tests with 98% coverage
- ✅ **Complete Documentation** - See `NAICS_EXPANSION_SUMMARY.md` for full details

### Deployment to Render

✅ **Production-Ready for Render Web Service Deployment**

The backend is fully configured for deployment to Render as a Web Service (no blueprints required).

**Quick Deploy:**

1. **Create PostgreSQL Database** in Render Dashboard
   - Database name: `levelith`
   - Region: Oregon (US West)
   - Copy Internal Database URL

2. **Create Web Service** in Render Dashboard
   - Connect GitHub repository: `Free-Columns/levelith-2`
   - Build Command: `pip install -r backend/requirements.txt`
   - Start Command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
   - Health Check Path: `/health`

3. **Set Environment Variables** (Required)
   - `DATABASE_URL` - Your PostgreSQL Internal URL
   - `SECRET_KEY` - Generate strong key (use Render's "Generate Value")
   - `ENVIRONMENT=production`
   - `DEBUG=false`
   - `CORS_ORIGINS` - Your frontend URL

4. **Deploy!**
   - Click "Create Web Service"
   - Wait ~3-5 minutes for deployment
   - Test: `https://your-service.onrender.com/health`

**Complete Guide:** See **[RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)** for detailed step-by-step instructions.

**Service URL:** `https://levelith-backend.onrender.com`

**Deployment Files:**
- `runtime.txt` - Python version specification (3.11.0, located in root)
- `render.yaml` - Render infrastructure configuration
- `.env.render.example` - Environment variables template
- `RENDER_DEPLOYMENT.md` - Complete deployment guide

**Python & Dependencies:**
- Python 3.11.0 (specified in `runtime.txt` at repository root)
- Pydantic 2.10.4 (upgraded for Python 3.13 compatibility with pre-built wheels)
- All dependencies have pre-built wheels for fast deployment

## Development Tools

### 🎨 Color Visualizer

An interactive standalone HTML tool for visualizing and editing the ONETRUTH color configuration.

**Location:** `tools/color-visualizer.html`

**Features:**
- ✅ **48 Color Swatches** - View all ONETRUTH colors organized by category
- ✅ **Triple Control System** - RGB sliders, HSL sliders, and Hex input (all synchronized)
- ✅ **Real-time Updates** - See color changes instantly as you adjust values
- ✅ **Export Options** - Download .ts file or copy to clipboard
- ✅ **Zero Dependencies** - Standalone HTML file, no installation required

**Quick Start:**
```bash
# Open the tool (from project root)
open tools/color-visualizer.html

# Or double-click the file in your file browser
```

**Color Categories:**
- Main Colors (26): Primary, secondary, accent, backgrounds, text, status, borders
- Gamification Levels (6): Beginner through legend progression
- Gamification Achievements (5): Bronze, silver, gold, platinum, diamond
- Gamification Progress (3): Low, medium, high progress states
- NAICS Industries (8): Industry-specific color coding

**Documentation:** See `tools/README.md` for complete usage guide and testing checklist.

## Quick Start

### For AI Agents

**⚠️  CRITICAL: Read these files FIRST before making ANY changes!**

1. **[MANIFEST.md](MANIFEST.md)** - Project vision, goals, architecture, conventions (Human-curated context)
2. **[AI_AGENT_GOLDEN_RULES.md](AI_AGENT_GOLDEN_RULES.md)** - 10 mandatory rules for all AI agents

```bash
# 1. Read project manifest for broad context (FIRST TIME)
cat MANIFEST.md

# 2. Read the golden rules (MANDATORY)
cat AI_AGENT_GOLDEN_RULES.md

# 3. Get 30-second quickstart overview (NEW v2.0!)
python dev/aiagent_navigator.py quickstart

# 4. Build codebase index
python dev/aiagent_navigator.py index

# 5. Get exploration plan
python dev/aiagent_navigator.py plan

# 6. Ask natural language questions (NEW v2.0!)
python dev/aiagent_navigator.py ask "How does authentication work?"

# 7. Before making changes - generate test template
python tests/test_system.py generate <module_path>

# 8. Write tests FIRST, then implement

# 9. Run tests (must pass with 80%+ coverage)
pytest

# 10. Update AI index after changes
python dev/aiagent_navigator.py index

# 11. Enforce golden rules before commit
python tests/test_system.py enforce
```

**Essential Reading (in order):**
1. [MANIFEST.md](MANIFEST.md) - **START HERE** - Project context and goals
2. [AI_AGENT_GOLDEN_RULES.md](AI_AGENT_GOLDEN_RULES.md) - **MANDATORY** rules
3. [AI_AGENT_GUIDE.md](AI_AGENT_GUIDE.md) - **v2.0** Complete operating guide with interactive learning
4. [claude.md](claude.md) - Navigation system overview

### For Developers

```bash
# Clone repository
git clone <repository-url>
cd levelith-2

# Install dependencies
pip install -r requirements.txt  # Production dependencies
pip install -r requirements-dev.txt  # Dev and test dependencies

# Set up pre-commit hooks (enforces golden rules)
pip install pre-commit
pre-commit install

# Explore the codebase
python dev/aiagent_navigator.py index
python dev/aiagent_navigator.py guide
cat NAVIGATION.md

# Run tests
pytest

# Check code quality
black .
flake8 .
mypy .
```

## Architecture

### Intelligent AI Agent Tooling

The primary navigation system uses **dynamic code analysis** rather than static documentation:

- **`.aiagent.json`** - Configuration and navigation hints
- **`dev/aiagent_navigator.py`** - Intelligence engine with automated analysis
- **`.aiagent-index.json`** - Auto-generated codebase index (cached)
- **`NAVIGATION.md`** - Auto-generated navigation guide

**Benefits:**
- Always in sync with actual code
- Automated maintenance (single command)
- Minimal storage overhead
- Query interface for on-demand analysis
- CI/CD ready

**Documentation:**
- [dev/AI_AGENT_TOOLING.md](dev/AI_AGENT_TOOLING.md) - Complete technical documentation
- [AI_AGENT_GUIDE.md](AI_AGENT_GUIDE.md) - Learning and operating guide for AI agents
- [COMPARISON.md](COMPARISON.md) - Comparison with alternative approaches

### Comprehensive Test System

**Test-First Development is MANDATORY** - Every code change must include tests.

- **`tests/test_system.py`** - Test requirement enforcement and template generation
- **`pytest.ini`** - Test configuration with 80% minimum coverage
- **`.github/workflows/enforce-golden-rules.yml`** - Automated test enforcement

**Key Features:**
- Auto-generate test templates for new modules
- Validate test quality and coverage
- Pre-commit hooks enforce test requirements
- CI/CD blocks merges without tests

```bash
# Generate test template
python tests/test_system.py generate <module_path>

# Validate test file
python tests/test_system.py validate <test_path>

# Enforce requirements before commit
python tests/test_system.py enforce
```

### Golden Rules Framework

**AI agents MUST follow these rules for every action.**

- **`AI_AGENT_GOLDEN_RULES.md`** - Complete golden rules documentation
- **`.github/workflows/enforce-golden-rules.yml`** - Automated enforcement

**The 10 Golden Rules:**
1. Test-First Development (MANDATORY)
2. Documentation is Non-Negotiable
3. Security First
4. Maintain the AI Agent Index
5. Code Quality Standards
6. Dependency Management
7. Performance Awareness
8. Scalability by Design
9. Error Handling and Logging
10. Version Control Hygiene

**See**: [AI_AGENT_GOLDEN_RULES.md](AI_AGENT_GOLDEN_RULES.md) for complete details.

## Key Features

### For AI Agents

**v2.0 Features:**
1. **QuickStart Analysis** - Get 30-second overview of entire codebase
2. **Goal-Oriented Exploration** - Create optimized exploration paths for specific goals
3. **Natural Language Queries** - Ask questions in plain English with AI/heuristic hybrid
4. **Cognitive Load Management** - Optimize context window usage automatically
5. **Interactive Learning** - Guided tutorials and exercises for AI agents
6. **Performance Navigator** - Progressive loading and incremental indexing for large codebases
7. **Exploration Metrics** - Track efficiency and get improvement suggestions

**v1.0 Core Features:**
1. **Dynamic Code Analysis** - Extract structure on-demand from actual code
2. **Golden Rules Enforcement** - Automated quality, security, and scalability checks
3. **Test-First Development** - Auto-generate test templates, enforce coverage
4. **Exploration Planning** - Smart suggestions for where to start
5. **Dependency Mapping** - Automatic relationship detection
6. **Complexity Analysis** - Identify hotspots and key modules
7. **Query Interface** - Ask specific questions about the codebase
8. **Related File Detection** - Find connected modules automatically

### For Developers

1. **Automated Testing** - Test templates, coverage enforcement, CI/CD integration
2. **Code Quality Automation** - Black, Flake8, MyPy, Pylint in CI/CD
3. **Security Scanning** - Bandit, Safety, Pip-audit, secret detection
4. **Automated Documentation** - No manual maintenance required
5. **CI/CD Integration** - Golden rules enforced in every pipeline
6. **Codebase Insights** - Complexity metrics and patterns
7. **Navigation Guides** - Human-readable overviews
8. **Extensible** - Add support for other languages

## Project Structure

```
levelith-2/
├── README.md                       # This file - Entry point for humans
├── MANIFEST.md                     # ⚠️  Project manifest - Entry point for AI agents
├── AI_AGENT_GOLDEN_RULES.md       # ⚠️  MANDATORY rules for AI agents
├── AI_AGENT_GUIDE.md              # Complete AI agent operating guide
├── claude.md                       # AI agent navigation guide
├── COMPARISON.md                   # Approach comparisons
├── NAVIGATION.md                   # Auto-generated navigation guide
├── DEPLOYMENT.md                   # 📦 Render deployment guide
│
├── .aiagent.json                   # AI agent configuration
├── .aiagent-index.json             # Auto-generated codebase index
├── pytest.ini                      # Test configuration
├── .commitlintrc.json              # Commit message standards
├── render.yaml                     # 🚀 Render deployment configuration
│
├── backend/                        # 🔧 FastAPI Backend
│   ├── main.py                     # FastAPI application entry point
│   ├── config.py                   # Environment configuration
│   ├── database.py                 # Database setup and session management
│   ├── requirements.txt            # Production dependencies
│   ├── requirements-dev.txt        # Development dependencies
│   ├── Procfile                    # Render start command
│   ├── .env.example                # Environment variables template
│   ├── models/                     # Domain and ORM models
│   │   ├── user.py                 # User domain model
│   │   ├── experience.py           # Experience domain models
│   │   └── db_models.py            # SQLAlchemy ORM models
│   ├── schemas/                    # Pydantic API schemas
│   │   ├── user.py                 # User request/response schemas
│   │   └── experience.py           # Experience request/response schemas
│   ├── api/                        # API routes
│   │   └── routes/                 # Route handlers
│   │       ├── health.py           # Health check endpoints
│   │       ├── users.py            # User management API
│   │       └── experiences.py      # Experience management API
│   ├── services/                   # Business logic layer
│   └── repositories/               # Data access layer
│
├── backend/                        # ✅ Backend application (Python)
│   ├── API_DOCUMENTATION.md        # ✅ Comprehensive API design document
│   ├── models/                     # ✅ Domain models (User, Experience + 9 subtypes)
│   │   ├── __init__.py             # Model exports
│   │   ├── user.py                 # User model with authentication
│   │   └── experience.py           # Experience base + 9 subtypes
│   ├── repositories/               # ✅ Data access layer (Repository pattern)
│   │   ├── __init__.py             # Repository exports
│   │   ├── user_repository.py      # User data access operations
│   │   └── experience_repository.py # Experience data access operations
│   ├── services/                   # ✅ Business logic layer (Service pattern)
│   │   ├── __init__.py             # Service exports
│   │   ├── user_service.py         # User business logic
│   │   └── experience_service.py   # Experience business logic
│   ├── api/                        # 🚧 API endpoints (to be implemented)
│   ├── Dockerfile                  # Docker configuration
│   └── Makefile                    # Build and development commands
│
├── tests/                          # Comprehensive test suite
│   ├── __init__.py                 # Test package initialization
│   ├── test_system.py              # Test enforcement and generation
│   ├── test_api_health.py          # Health endpoint tests
│   ├── test_api_users.py           # User API tests
│   ├── test_api_experiences.py     # Experience API tests
│   ├── test_user.py                # User domain model tests
│   ├── test_experience.py          # Experience domain model tests
│   └── test_test_system.py         # Test system tests
│   ├── test_user.py                # ✅ User model tests
│   ├── test_experience.py          # ✅ Experience model tests
│   ├── test_user_repository.py     # ✅ UserRepository tests
│   ├── test_experience_repository.py # ✅ ExperienceRepository tests
│   ├── unit/                       # Unit tests
│   ├── integration/                # Integration tests
│   └── e2e/                        # End-to-end tests
│
├── dev/                            # Development tools
│   ├── aiagent_navigator.py        # Intelligent navigation system
│   ├── example_ai_agent_usage.py   # Demo and examples
│   └── AI_AGENT_TOOLING.md        # Technical documentation
│
├── tools/                          # 🎨 Standalone development tools
│   ├── color-visualizer.html       # Interactive ONETRUTH color editor
│   └── README.md                   # Tools documentation and usage
│
├── .github/workflows/              # CI/CD pipelines
│   ├── enforce-golden-rules.yml    # Golden rules enforcement
│   ├── main-ci.yml                 # Main CI/CD pipeline
│   ├── frontend-ci.yml             # Frontend tests and builds
│   └── backend-ci.yml              # Backend tests and builds
│
└── docs/                           # Additional documentation
```

### Backend Architecture

The backend follows a layered architecture pattern:

**Domain Layer** (`backend/models/`)
- `User`: User authentication and profile management
- `Experience`: Base class for all experience types
- 9 Experience subtypes: Certificate, Degree, Course, Gig, PartTime, FullTime, SoftSkill, HardSkill, NativeSkill

**Repository Layer** (`backend/repositories/`)
- `UserRepository`: User data access (CRUD, search, filtering)
- `ExperienceRepository`: Experience data access with NAICS indexing

**Service Layer** (`backend/services/`)
- `UserService`: User registration, authentication, profile management
- `ExperienceService`: Experience creation/management for all 9 types

**API Layer** (`backend/api/`) - *To be implemented*
- RESTful endpoints for all operations
- JWT authentication
- Request/response schemas
- See `backend/API_DOCUMENTATION.md` for complete API design

**Key Features:**
- ✅ Complete domain models with comprehensive docstrings
- ✅ Repository pattern for data access abstraction
- ✅ Service layer for business logic encapsulation
- ✅ NAICS code validation and fallback (123456 for GENERAL)
- ✅ Comprehensive test coverage for all layers
- 🚧 API endpoints (FastAPI) - to be implemented
- 🚧 Database integration (PostgreSQL) - to be implemented

## Usage Examples

### Automated Navigation

```python
from dev.aiagent_navigator import AIAgentNavigator

# Initialize navigator
nav = AIAgentNavigator()

# Get exploration plan
plan = nav.get_exploration_plan()
print(f"Start here: {plan['suggested_start']}")
print(f"Entry points: {plan['entry_points']}")
print(f"Key modules: {plan['key_modules']}")

# Analyze specific module
context = nav.get_module_context("dev/cn-create.py")
print(f"Classes: {context['classes']}")
print(f"Functions: {context['functions']}")
print(f"Imports: {context['imports']}")

# Find related files
related = nav.suggest_related_files("dev/cn-create.py")
for item in related:
    print(f"Related: {item['path']} - {item['reason']}")
```

### CLI Commands

```bash
# Build index and generate guide
python dev/aiagent_navigator.py index
python dev/aiagent_navigator.py guide

# View exploration plan (JSON)
python dev/aiagent_navigator.py plan

# Analyze specific file
python dev/aiagent_navigator.py analyze dev/aiagent_navigator.py

# Find related files
python dev/aiagent_navigator.py related dev/aiagent_navigator.py

# Run demo
python dev/example_ai_agent_usage.py
```

## Documentation

### For AI Agents

- **[AI_AGENT_GUIDE.md](AI_AGENT_GUIDE.md)** - Start here! Complete learning and operating guide
- **[claude.md](claude.md)** - Navigation system overview
- **[NAVIGATION.md](NAVIGATION.md)** - Auto-generated codebase map

### For Developers

- **[dev/AI_AGENT_TOOLING.md](dev/AI_AGENT_TOOLING.md)** - Technical documentation
- **[COMPARISON.md](COMPARISON.md)** - Approach comparison and migration guide
- **[dev/example_ai_agent_usage.py](dev/example_ai_agent_usage.py)** - Working code examples

## CI/CD Integration

Add to your workflow to keep AI navigation always up-to-date:

```yaml
name: Update AI Agent Index

on: [push]

jobs:
  update-index:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Build AI Index
        run: python dev/aiagent_navigator.py index

      - name: Generate Navigation Guide
        run: python dev/aiagent_navigator.py guide

      - name: Commit if changed
        run: |
          git config user.name "AI Agent Bot"
          git add .aiagent-index.json NAVIGATION.md
          git diff --quiet || git commit -m "Update AI agent index"
          git push
```

## Comparison: Context Nodes vs AI Tooling

| Aspect | Context Nodes | AI Tooling |
|--------|--------------|------------|
| **Maintenance** | Manual | Automated |
| **Sync Issues** | High risk | Always in sync |
| **Setup Time** | 4-8 hours | 5 minutes |
| **Storage** | 2x files | Minimal |
| **CI/CD** | Requires discipline | Auto-generate |
| **Accuracy** | Depends on humans | Extracted from code |

**See [COMPARISON.md](COMPARISON.md) for detailed analysis.**

## Extending to Other Languages

The navigator can be extended for JavaScript, TypeScript, Java, etc:

```python
class JSNavigator(AIAgentNavigator):
    def analyze_js_file(self, filepath):
        # Parse with esprima, babel, or similar
        # Extract exports, imports, functions, classes
        pass
```

## Philosophy

**AI Agents as First-Class Citizens**

This repository treats AI agents not as afterthoughts, but as primary users:

1. **Self-Documenting** - Code structure is discoverable
2. **Query-Driven** - Ask questions, get answers
3. **Always Current** - Generated from actual code, not stale docs
4. **Low Overhead** - Minimal burden on human developers
5. **Intelligent** - Smart suggestions and relationship detection

## Contributing

When adding code to this repository:

1. **Write good docstrings** - These are extracted automatically
2. **Run the index** - `python dev/aiagent_navigator.py index`
3. **Check the guide** - Review generated `NAVIGATION.md`
4. **Add insights to config** - Update `.aiagent.json` with special notes

## License

[Specify your license]

## Credits

Created as part of the Levelith project, reimagining software development with AI agents as collaborative partners.

---

**For AI Agents**: Start with [AI_AGENT_GUIDE.md](AI_AGENT_GUIDE.md) for complete operating instructions.

**For Developers**: Run `python dev/aiagent_navigator.py guide` to generate a fresh navigation guide.
