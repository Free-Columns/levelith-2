# Levelith Documentation Index

**Last Updated:** 2025-12-08
**Status:** Consolidated for MVP

---

## 🎯 Start Here

### For Users
- **[MVP_GUIDE.md](./MVP_GUIDE.md)** - Complete MVP guide with all features, setup, and usage

### For Deployment
- **[RENDER_XP_DEPLOYMENT.md](./RENDER_XP_DEPLOYMENT.md)** - Step-by-step Render deployment for XP system

### For Developers
- **[README.md](./README.md)** - Project overview and quick start
- **API Documentation:** http://localhost:8000/docs (when running)

---

## 📚 Essential Documentation

### Project Overview
| Document | Purpose | Audience |
|----------|---------|----------|
| [README.md](./README.md) | Project overview, quick start | Everyone |
| [MVP_GUIDE.md](./MVP_GUIDE.md) | Complete MVP features & setup | Users, Developers |
| [MVP_ACTION_PLAN.md](./MVP_ACTION_PLAN.md) | Development roadmap | Developers |

### Deployment
| Document | Purpose | Audience |
|----------|---------|----------|
| [RENDER_XP_DEPLOYMENT.md](./RENDER_XP_DEPLOYMENT.md) | XP system deployment | DevOps |
| [docs/deployment/RENDER_DEPLOYMENT.md](./docs/deployment/RENDER_DEPLOYMENT.md) | General Render setup | DevOps |

### Development
| Document | Purpose | Audience |
|----------|---------|----------|
| [PROGRESS_REPORT.md](./PROGRESS_REPORT.md) | Latest changes summary | Developers |
| [SESSION_SUMMARY.md](./SESSION_SUMMARY.md) | Recent session notes | Developers |
| [docs/agent/MANIFEST.md](./docs/agent/MANIFEST.md) | Project vision | AI Agents, Developers |
| [docs/agent/AI_AGENT_GOLDEN_RULES.md](./docs/agent/AI_AGENT_GOLDEN_RULES.md) | Development standards | AI Agents |

---

## 🗂️ Documentation Structure

### `/docs` Directory

The `docs/` directory contains detailed technical documentation:

```
docs/
├── agent/                  # AI agent guides
│   ├── MANIFEST.md        # Project vision (must-read)
│   └── AI_AGENT_GOLDEN_RULES.md
├── api/                   # API documentation
│   └── API_DOCUMENTATION.md
├── features/              # Feature documentation
│   ├── admin-dashboard.md # Complete admin dashboard guide
│   └── naics-system.md    # NAICS industry classification
├── backend/               # Backend technical docs
│   └── database/          # Database schemas & models
│       └── README.md      # Database overview
├── deployment/            # Deployment guides
│   └── RENDER_DEPLOYMENT.md
└── archive/               # Historical docs (outdated)
```

**Note:** Legacy documentation has been archived. Use MVP_GUIDE.md and the consolidated feature docs.

---

## 🎓 Learning Path

### New to Levelith?

1. **Read** [README.md](./README.md) (5 min)
2. **Review** [MVP_GUIDE.md](./MVP_GUIDE.md) (15 min)
3. **Follow** Quick Start in MVP_GUIDE.md
4. **Explore** API docs at http://localhost:8000/docs

### Setting Up for Development?

1. **Read** [README.md](./README.md) - Quick start
2. **Read** [docs/agent/MANIFEST.md](./docs/agent/MANIFEST.md) - Project vision
3. **Read** [docs/agent/AI_AGENT_GOLDEN_RULES.md](./docs/agent/AI_AGENT_GOLDEN_RULES.md) - Dev standards
4. **Follow** Setup instructions in MVP_GUIDE.md

### Deploying to Production?

1. **Read** [MVP_GUIDE.md](./MVP_GUIDE.md) - Features overview
2. **Follow** [RENDER_XP_DEPLOYMENT.md](./RENDER_XP_DEPLOYMENT.md) - Deployment steps
3. **Reference** [docs/deployment/RENDER_DEPLOYMENT.md](./docs/deployment/RENDER_DEPLOYMENT.md) - General guide

---

## 📋 Documentation Cleanup Plan

### Files to Keep (Essential)

**Root Level:**
- ✅ README.md
- ✅ MVP_GUIDE.md (NEW)
- ✅ RENDER_XP_DEPLOYMENT.md (NEW)
- ✅ DOCUMENTATION_INDEX.md (NEW)
- ✅ MVP_ACTION_PLAN.md
- ✅ PROGRESS_REPORT.md
- ✅ SESSION_SUMMARY.md

**docs/ Directory:**
- ✅ docs/agent/MANIFEST.md
- ✅ docs/agent/AI_AGENT_GOLDEN_RULES.md
- ✅ docs/agent/AI_AGENT_GUIDE.md
- ✅ docs/api/API_DOCUMENTATION.md
- ✅ docs/deployment/RENDER_DEPLOYMENT.md
- ✅ docs/backend/database/* (technical references)
- ✅ docs/features/admin-dashboard.md (admin dashboard guide)
- ✅ docs/features/naics-system.md (NAICS documentation)

### Files Archived (Completed)

**Successfully archived:**
- ✅ _deprecated/* (deleted)
- ✅ docs/all/* (moved to docs/archive/)
- ✅ docs/development/admin/* (merged into docs/features/admin-dashboard.md)
- ✅ docs/development/frontend/* (merged into docs/features/admin-dashboard.md)
- ✅ docs/backend/naics/* (merged into docs/features/naics-system.md)
- ✅ Root clutter files (NAVIGATION.md, PHASE_2_*.md, etc.)

**Result:** ~50% reduction in markdown files (~80 → ~40 files)

---

## 🔍 Quick Reference

### Common Tasks

| Task | Documentation |
|------|---------------|
| Start development | [MVP_GUIDE.md](./MVP_GUIDE.md) → Quick Start |
| Deploy to Render | [RENDER_XP_DEPLOYMENT.md](./RENDER_XP_DEPLOYMENT.md) |
| Understand XP system | [MVP_GUIDE.md](./MVP_GUIDE.md) → XP System Details |
| Use dev interface | [MVP_GUIDE.md](./MVP_GUIDE.md) → Dev Interface Setup |
| API reference | http://localhost:8000/docs (Swagger UI) |
| Database schema | [docs/backend/database/README.md](./docs/backend/database/README.md) |
| NAICS codes | [docs/features/naics-system.md](./docs/features/naics-system.md) |
| Admin dashboard | [docs/features/admin-dashboard.md](./docs/features/admin-dashboard.md) |
| Project vision | [docs/agent/MANIFEST.md](./docs/agent/MANIFEST.md) |

### Quick Links

- **Swagger API Docs:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health
- **Dev Interface:** `dev_interface.html`

---

## 🆘 Getting Help

### Documentation Issues?

1. Check this index for the right document
2. Most info is in [MVP_GUIDE.md](./MVP_GUIDE.md)
3. For deployment, see [RENDER_XP_DEPLOYMENT.md](./RENDER_XP_DEPLOYMENT.md)
4. For API details, check Swagger UI

### Code Issues?

1. Check API docs at `/docs`
2. Review code comments (well-documented)
3. Check test files for usage examples
4. See PROGRESS_REPORT.md for recent changes

---

## 📝 Documentation Standards

### When to Create New Docs

**DO create new docs for:**
- Major new features
- Deployment procedures
- Integration guides
- Architecture decisions

**DON'T create new docs for:**
- Minor bug fixes (use commit messages)
- Code explanations (use code comments)
- Temporary notes (use session summaries)

### Where to Put Documentation

| Type | Location | Example |
|------|----------|---------|
| User guides | Root `.md` files | MVP_GUIDE.md |
| Deployment | Root or docs/deployment/ | RENDER_XP_DEPLOYMENT.md |
| API reference | Swagger UI | /docs endpoint |
| Technical specs | docs/backend/ | Database schemas |
| Project vision | docs/agent/ | MANIFEST.md |

---

## 🎯 Summary

**All you need:**
1. [MVP_GUIDE.md](./MVP_GUIDE.md) - Complete feature and setup guide
2. [RENDER_XP_DEPLOYMENT.md](./RENDER_XP_DEPLOYMENT.md) - Deployment instructions
3. [README.md](./README.md) - Project overview
4. Swagger UI - API documentation (when backend running)

**Everything else is supplementary.**

---

**Last Updated:** 2025-12-08
**Maintainer:** Claude AI Agent
