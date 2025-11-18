# Levelith

**A social-resume gamification platform built with AI-first development methodology**

Levelith transforms professional experience tracking into an engaging, interactive platform. Track education, workplace experiences, and skills with NAICS-based industry classification, all backed by comprehensive testing and AI-powered development tools.

---

## 🚀 Quick Start

### For AI Agents

**⚠️ MANDATORY: Read these first before making ANY changes!**

1. **[docs/core/MANIFEST.md](docs/core/MANIFEST.md)** - Project vision, goals, and architecture
2. **[docs/core/AI_AGENT_GOLDEN_RULES.md](docs/core/AI_AGENT_GOLDEN_RULES.md)** - 10 mandatory development rules
3. **[docs/core/AI_AGENT_GUIDE.md](docs/core/AI_AGENT_GUIDE.md)** - Complete AI operating guide

```bash
# Build codebase index
python dev/aiagent_navigator.py index

# Get exploration plan
python dev/aiagent_navigator.py plan

# Before changes: generate test template
python tests/test_system.py generate <module_path>

# After changes: update AI index
python dev/aiagent_navigator.py index
```

**Essential Documentation:** [docs/README.md](docs/README.md) - Complete documentation index

### For Developers

```bash
# Install dependencies
pip install -r backend/requirements.txt
pip install -r backend/requirements-dev.txt

# Run tests
pytest

# Start backend
cd backend && uvicorn main:app --reload

# API Documentation
open http://localhost:8000/docs
```

---

## 🎯 Features

### Backend (FastAPI + PostgreSQL)
- ✅ **User Management** - Full CRUD with authentication
- ✅ **Experience Tracking** - 9 experience types (Education, Workplace, Skills)
- ✅ **NAICS 2022** - Complete industry classification system (60+ codes, 12 endpoints)
- ✅ **Health Checks** - Render-ready monitoring endpoints
- ✅ **Comprehensive Tests** - 80%+ coverage enforced

### Development Tools
- ✅ **AI Agent Navigation** - Dynamic codebase analysis and exploration
- ✅ **Test System** - Auto-generation and 80% minimum coverage enforcement
- ✅ **Golden Rules Framework** - Automated quality, security, and scalability checks
- ✅ **Color Visualizer** - Interactive ONETRUTH branding editor (`tools/color-visualizer.html`)
- ✅ **Admin Dashboard** - Full-featured UI for managing users and experiences

---

## 📚 Documentation

### Core Documentation (`docs/core/`)
- **[MANIFEST.md](docs/core/MANIFEST.md)** - **START HERE** - Project context and goals
- **[AI_AGENT_GOLDEN_RULES.md](docs/core/AI_AGENT_GOLDEN_RULES.md)** - **MANDATORY** development rules
- **[AI_AGENT_GUIDE.md](docs/core/AI_AGENT_GUIDE.md)** - Complete AI agent operating guide

### API & Backend (`docs/api/`, `docs/backend/`)
- **[API_DOCUMENTATION.md](docs/api/API_DOCUMENTATION.md)** - Complete API reference
- **[NAICS_EXPANSION_SUMMARY.md](docs/backend/NAICS_EXPANSION_SUMMARY.md)** - NAICS implementation details

### Development (`docs/dev/`)
- **[AI_AGENT_TOOLING.md](docs/dev/AI_AGENT_TOOLING.md)** - AI navigation technical docs
- **[NAVIGATION.md](docs/dev/NAVIGATION.md)** - Auto-generated codebase map
- **[ADMIN_PANEL_GUIDE.md](docs/dev/ADMIN_PANEL_GUIDE.md)** - Admin dashboard guide

### Deployment (`docs/deployment/`)
- **[RENDER_DEPLOYMENT.md](docs/deployment/RENDER_DEPLOYMENT.md)** - Step-by-step Render deployment
- **[DATABASE_SETUP_NOTES.md](docs/deployment/DATABASE_SETUP_NOTES.md)** - Database initialization

**Full Index:** [docs/README.md](docs/README.md)

---

## 🏗️ Architecture

```
levelith-2/
├── backend/           # FastAPI application
│   ├── models/        # Domain models (User, Experience + 9 subtypes)
│   ├── repositories/  # Data access layer
│   ├── services/      # Business logic layer
│   └── api/routes/    # API endpoints
├── tests/             # Comprehensive test suite (80%+ coverage)
├── dev/               # AI agent tools and admin dashboard
│   ├── aiagent_navigator.py  # Intelligent navigation system
│   └── dev-frontend/levelith_admin_dashboard/  # Admin UI
├── tools/             # Standalone development tools
│   └── color-visualizer.html  # ONETRUTH color editor
└── docs/              # Complete documentation
    ├── core/          # Project fundamentals
    ├── api/           # API reference
    ├── backend/       # Implementation details
    ├── dev/           # Development tools
    └── deployment/    # Deployment guides
```

**Key Principles:**
- **AI-First Development** - AI agents as first-class citizens
- **Test-Driven** - 80% minimum coverage, tests before code
- **Security First** - No hardcoded secrets, input validation, OWASP compliance
- **Self-Documenting** - Code structure is discoverable via AI tooling

---

## 🔧 API Endpoints

### Core Endpoints
```
GET  /health                        # Health check
GET  /health/ready                  # Readiness probe (checks database)
POST /api/v1/users/                 # Create user
GET  /api/v1/users/{id}             # Get user
POST /api/v1/experiences/           # Create experience
GET  /api/v1/experiences/{id}       # Get experience
```

### NAICS Industry Classification (12 Endpoints)
```
GET  /api/v1/naics/{code}                      # Get NAICS code details
GET  /api/v1/naics/search?q={query}            # Search codes
GET  /api/v1/naics/autocomplete?q={partial}    # Autocomplete
GET  /api/v1/naics/suggest/experience/{type}   # Get suggestions
```

**Full API Reference:** http://localhost:8000/docs (when backend running)

---

## 🚀 Deployment

### Quick Deploy to Render

1. **Create PostgreSQL Database** in Render Dashboard
2. **Create Web Service**
   - Build: `pip install -r backend/requirements.txt`
   - Start: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
   - Health: `/health`
3. **Set Environment Variables** (DATABASE_URL, SECRET_KEY, etc.)

**Complete Guide:** [docs/deployment/RENDER_DEPLOYMENT.md](docs/deployment/RENDER_DEPLOYMENT.md)

**Production:** https://levelith-backend.onrender.com

---

## 🛠️ Development Workflow

### AI Agent Workflow
```bash
# 1. Read MANIFEST and Golden Rules (FIRST TIME)
cat docs/core/MANIFEST.md
cat docs/core/AI_AGENT_GOLDEN_RULES.md

# 2. Build index and explore
python dev/aiagent_navigator.py index
python dev/aiagent_navigator.py plan

# 3. Generate test template BEFORE coding
python tests/test_system.py generate <module_path>

# 4. Write tests FIRST, then implement

# 5. Run tests (must pass with 80%+)
pytest

# 6. Update AI index after changes
python dev/aiagent_navigator.py index

# 7. Enforce golden rules before commit
python tests/test_system.py enforce
```

### Human Developer Workflow
```bash
# Install and setup
pip install -r backend/requirements.txt
pip install -r backend/requirements-dev.txt
pip install pre-commit && pre-commit install

# Develop
pytest                              # Run tests
black .                             # Format code
flake8 .                            # Lint code
python dev/aiagent_navigator.py index  # Update AI index

# Deploy
git add . && git commit -m "feat: description"
git push
```

---

## 📊 Project Status

### ✅ Completed
- AI agent navigation system
- Golden rules framework with enforcement
- Test system with 80% minimum coverage
- FastAPI backend with PostgreSQL
- NAICS 2022 industry classification (60+ codes, 197 tests, 98% coverage)
- Health checks and monitoring
- Admin dashboard (React + TypeScript)
- Render deployment configuration

### 🚧 In Progress
- Frontend application (React + TypeScript)
- JWT authentication
- Production deployment optimization

### 📋 Planned
- Mobile app (React Native)
- Advanced analytics dashboard
- Real-time social features
- Multi-language support

---

## 🤝 Contributing

When adding code:
1. **Read the Golden Rules** - [docs/core/AI_AGENT_GOLDEN_RULES.md](docs/core/AI_AGENT_GOLDEN_RULES.md)
2. **Write tests first** - Generate template: `python tests/test_system.py generate <module>`
3. **Update AI index** - `python dev/aiagent_navigator.py index`
4. **Follow conventions** - See [docs/core/MANIFEST.md](docs/core/MANIFEST.md)

---

## 📄 License

[Specify your license]

---

## 🎯 Key Resources

| Resource | Purpose |
|----------|---------|
| [MANIFEST.md](docs/core/MANIFEST.md) | **Project context** - Read first! |
| [AI_AGENT_GOLDEN_RULES.md](docs/core/AI_AGENT_GOLDEN_RULES.md) | **Development rules** - MANDATORY |
| [API_DOCUMENTATION.md](docs/api/API_DOCUMENTATION.md) | **API reference** - All endpoints |
| [RENDER_DEPLOYMENT.md](docs/deployment/RENDER_DEPLOYMENT.md) | **Deployment guide** - Production setup |
| [docs/README.md](docs/README.md) | **Documentation index** - All docs |

---

**For AI Agents:** Start with [docs/core/AI_AGENT_GUIDE.md](docs/core/AI_AGENT_GUIDE.md) for complete operating instructions.

**For Developers:** Run `python dev/aiagent_navigator.py guide` to generate a fresh navigation guide.

**For Support:** See [docs/core/MANIFEST.md](docs/core/MANIFEST.md) troubleshooting section.
