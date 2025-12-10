# Levelith

**AI-first social-resume gamification platform**

[![CI Pipeline](https://github.com/Free-Columns/levelith-2/workflows/CI%20Pipeline/badge.svg)](https://github.com/Free-Columns/levelith-2/actions/workflows/ci.yml)
[![Golden Rules](https://github.com/Free-Columns/levelith-2/workflows/🏆%20Golden%20Rules%20Enforcement/badge.svg)](https://github.com/Free-Columns/levelith-2/actions/workflows/golden-rules.yml)
[![Test Coverage](https://img.shields.io/badge/coverage-75%25-yellow)](https://github.com/Free-Columns/levelith-2)

Transform professional experience tracking into an engaging platform with NAICS-based industry classification, comprehensive testing, and AI-powered development.

---

## 🚀 Quick Start

### AI Agents — Read This First

**⚠️ MANDATORY before making ANY changes:**

1. [**MANIFEST.md**](docs/agent/MANIFEST.md) — Project vision and architecture
2. [**AI_AGENT_GOLDEN_RULES.md**](docs/agent/AI_AGENT_GOLDEN_RULES.md) — 10 mandatory rules
3. [**AI_AGENT_GUIDE.md**](docs/agent/AI_AGENT_GUIDE.md) — Complete operating guide

```bash
# Build index and explore codebase
python dev/aiagent_navigator.py index
python dev/aiagent_navigator.py plan

# Before coding: generate test template
python tests/test_system.py generate <module_path>

# After changes: update AI index
python dev/aiagent_navigator.py index
```

📚 **Full Docs:** [docs/README.md](docs/README.md)

### Developers — Setup

```bash
# Install dependencies
pip install -r backend/requirements.txt
pip install -r backend/requirements-dev.txt

# Run tests (80% min coverage)
pytest

# Start backend
cd backend && uvicorn main:app --reload

# API docs at http://localhost:8000/docs
```

---

## ✨ Features

- ✅ **User & Experience Management** — 37 REST API endpoints
- ✅ **NAICS 2022 Integration** — 60+ industry codes, hierarchical navigation
- ✅ **9 Experience Types** — Education, Workplace, Skills (98% test coverage)
- ✅ **AI Agent Tooling** — Dynamic navigation, auto-generated docs
- ✅ **Admin Dashboard** — Full-featured React UI for management
- ✅ **Golden Rules Enforcement** — Automated quality, security, coverage checks

---

## 📊 Project Status

**Overall Grade: B+ (85/100)**

| Component | Status | Coverage/Completion |
|-----------|--------|---------------------|
| Backend Core | ✅ Functional | 85% |
| Test Coverage | ⚠️ Below target | 75% (need 80%) |
| Authentication | ⚠️ Incomplete | JWT partially done |
| Admin Dashboard | ✅ Complete | 95% |
| Main Frontend | ❌ Not started | 0% |
| Documentation | ✅ Excellent | 95% |

**Path to Production:** 60-100 hours — See [Development Priorities](docs/reports/DEVELOPMENT_PRIORITIES.md)

---

## 📚 Documentation

**Essential Reading:**

| Document | Purpose |
|----------|---------|
| [**MANIFEST.md**](docs/agent/MANIFEST.md) | 🎯 Project vision (START HERE) |
| [**Golden Rules**](docs/agent/AI_AGENT_GOLDEN_RULES.md) | ⚠️ MANDATORY development rules |
| [**Codebase Summary**](docs/CODEBASE_SUMMARY_REPORT.md) | 📊 Executive analysis report |
| [**API Docs**](docs/api/API_DOCUMENTATION.md) | 🔌 Complete API reference |
| [**Known Issues**](docs/reports/KNOWN_ISSUES.md) | 🐛 Critical issues tracker |
| [**Priorities**](docs/reports/DEVELOPMENT_PRIORITIES.md) | 🗺️ Development roadmap |

**Feature Documentation:**

| Document | Purpose |
|----------|---------|
| [**Admin Dashboard**](docs/features/admin-dashboard.md) | 🎛️ Complete admin dashboard guide (setup, features, API) |
| [**NAICS System**](docs/features/naics-system.md) | 🏭 Industry classification system (2222+ codes, import, API) |
| [**Database Guide**](docs/backend/database/README.md) | 🗄️ Schema, models, and database operations |
| [**API Documentation**](docs/api/API_DOCUMENTATION.md) | 🔌 Complete API reference (37 endpoints) |

**All Documentation:** [docs/README.md](docs/README.md)

---

## 🏗️ Architecture

```
levelith-2/
├── backend/          # FastAPI + PostgreSQL (11,168 lines)
│   ├── models/       # User, Experience, NAICS
│   ├── services/     # Business logic (needs tests!)
│   ├── repositories/ # Data access layer
│   └── api/routes/   # 37 REST endpoints
├── tests/            # 491 test functions (6,924 lines)
├── dev/              # AI tools + admin dashboard
├── docs/             # 28 documentation files
└── tools/            # Standalone dev tools
```

**Key Principles:**
- Test-first development (80% min coverage)
- Clean architecture (4 layers)
- Security first (OWASP compliant)
- AI-first methodology

---

## 🔧 API Endpoints

```
Health & Monitoring
GET  /health              # Basic health check
GET  /health/ready        # Database readiness

User Management
POST /api/v1/users/       # Create user
GET  /api/v1/users/{id}   # Get user with experiences

Experience Management
POST /api/v1/experiences/ # Create experience (9 types)
GET  /api/v1/experiences/ # List with filters

NAICS Classification (12 endpoints)
GET  /api/v1/naics/search # Search industry codes
GET  /api/v1/naics/suggest # Smart suggestions
```

**Full API:** http://localhost:8000/docs (when running)

---

## 🚧 Critical Issues

Before production deployment:

1. **Add service tests** (5-6 hrs) — 1,550 lines untested
2. **Refactor API routes** (3-4 hrs) — Use service layer properly
3. **Complete JWT auth** (2-3 hrs) — Token generation missing
4. **Build main frontend** (40-80 hrs) — User-facing app

**Details:** [Known Issues](docs/reports/KNOWN_ISSUES.md)

---

## 🔄 Development Workflow

### AI Agents

```bash
# 1. Read MANIFEST and Golden Rules (first time)
# 2. Build index
python dev/aiagent_navigator.py index

# 3. Generate test template BEFORE coding
python tests/test_system.py generate <module_path>

# 4. Write tests FIRST, then implement
# 5. Run tests (must pass at 80%+)
pytest

# 6. Update AI index after changes
python dev/aiagent_navigator.py index

# 7. Enforce golden rules before commit
python tests/test_system.py enforce
```

### Human Developers

```bash
# Setup
pip install -r backend/requirements-dev.txt
pip install pre-commit && pre-commit install

# Develop
pytest                              # Run tests
black . && flake8 .                 # Format & lint
python dev/aiagent_navigator.py index  # Update AI index

# Commit
git add . && git commit -m "feat: description"
```

---

## 🚀 Deployment

**Production:** https://levelith-backend.onrender.com

### Quick Deploy (Render.com)

1. Create PostgreSQL database
2. Create web service:
   - Build: `pip install -r backend/requirements.txt`
   - Start: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
   - Health: `/health`
3. Set environment variables

**Full Guide:** [RENDER_DEPLOYMENT.md](docs/deployment/RENDER_DEPLOYMENT.md)

---

## 🤝 Contributing

1. **Read the Golden Rules** — [AI_AGENT_GOLDEN_RULES.md](docs/agent/AI_AGENT_GOLDEN_RULES.md)
2. **Write tests first** — `python tests/test_system.py generate <module>`
3. **Update AI index** — `python dev/aiagent_navigator.py index`
4. **Follow conventions** — See [MANIFEST.md](docs/agent/MANIFEST.md)

---

## 📄 License

[Specify your license]

---

## 🔗 Key Resources

- 🎯 [MANIFEST](docs/agent/MANIFEST.md) — Project context (start here!)
- ⚠️ [Golden Rules](docs/agent/AI_AGENT_GOLDEN_RULES.md) — Development standards
- 📊 [Codebase Summary](docs/CODEBASE_SUMMARY_REPORT.md) — Executive analysis
- 🔌 [API Docs](docs/api/API_DOCUMENTATION.md) — Endpoint reference
- 🗺️ [Roadmap](docs/reports/DEVELOPMENT_PRIORITIES.md) — Path to production
- 📚 [Full Docs](docs/README.md) — Complete documentation index

---

**Built with AI-first methodology** • **Test coverage: 75%** • **Production-ready in 60-100 hours**
