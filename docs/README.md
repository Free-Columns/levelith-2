# Levelith Documentation Index

**Last Updated:** 2025-11-18
**Project:** Levelith-2 - Social Resume Gamification Platform

---

## Quick Navigation

- **For AI Agents:** Start with [Core Documentation](#core-documentation)
- **For Developers:** See [Getting Started](#getting-started)
- **For Deployment:** See [Deployment Documentation](#deployment-documentation)
- **For API Reference:** See [API Documentation](#api-documentation)

---

## Core Documentation

Essential documentation for understanding the project and AI agent operation.

### AI Agent Operation
- **[AI_AGENT_GUIDE.md](core/AI_AGENT_GUIDE.md)** - Complete AI agent learning and operating guide v2.0
- **[AI_AGENT_GOLDEN_RULES.md](core/AI_AGENT_GOLDEN_RULES.md)** - ⚠️ MANDATORY rules for all AI agents
- **[MANIFEST.md](core/MANIFEST.md)** - ⚠️ Project vision, goals, architecture (START HERE for AI agents)
- **[claude_navigation.md](core/claude_navigation.md)** - Navigation system overview

### Project Foundation
Location: `docs/core/`

| Document | Purpose | Audience |
|----------|---------|----------|
| MANIFEST.md | Project vision, goals, conventions | AI Agents, All Developers |
| AI_AGENT_GOLDEN_RULES.md | 10 mandatory development rules | AI Agents |
| AI_AGENT_GUIDE.md | Complete AI operating guide v2.0 | AI Agents |
| claude_navigation.md | Navigation system explained | AI Agents, Developers |

---

## API Documentation

Complete API endpoint reference and design documentation.

Location: `docs/api/`

- **[API_DOCUMENTATION.md](api/API_DOCUMENTATION.md)** - Comprehensive API design and endpoint reference
  - User Management API
  - Experience Management API (9 types)
  - NAICS Industry Classification API (12 endpoints)
  - Authentication & Authorization
  - Request/Response Schemas

---

## Backend Documentation

Backend architecture, features, and implementation details.

Location: `docs/backend/`

- **[NAICS_EXPANSION_SUMMARY.md](backend/NAICS_EXPANSION_SUMMARY.md)** - NAICS 2022 system implementation
  - 60+ official industry codes
  - 14 industry categories
  - Hierarchical support (2/3/4/6 digit levels)
  - 148 comprehensive tests

---

## Frontend Documentation

Frontend architecture, components, and user interface documentation.

Location: `docs/frontend/`

**Status:** No frontend-specific documentation yet.

**Planned:**
- Component library documentation
- ONETRUTH theming guide
- State management documentation
- UI/UX guidelines

---

## Development Tools Documentation

Development tooling, testing, and AI agent navigation.

Location: `docs/dev/`

| Document | Purpose |
|----------|---------|
| [AI_AGENT_TOOLING.md](dev/AI_AGENT_TOOLING.md) | Technical documentation for AI navigation system |
| [NAVIGATION.md](dev/NAVIGATION.md) | Auto-generated codebase navigation guide |
| [TEST_REPORT.md](dev/TEST_REPORT.md) | Test system reports and coverage |
| [AI Agent Learning and Operating Guide v2.0.md](dev/AI%20Agent%20Learning%20and%20Operating%20Guide%20v2.0.md) | Extended AI agent operating guide |

---

## Deployment Documentation

Production deployment guides and configuration.

Location: `docs/deployment/`

- **[RENDER_DEPLOYMENT.md](deployment/RENDER_DEPLOYMENT.md)** - Step-by-step Render.com deployment guide
  - PostgreSQL database setup
  - Web service configuration
  - Environment variables
  - Health checks
  - Troubleshooting

- **[DEPLOYMENT.md](deployment/DEPLOYMENT.md)** - General deployment documentation
  - Docker configuration
  - CI/CD pipelines
  - Production checklist

---

## Architecture Documentation

System architecture, design decisions, and comparisons.

Location: `docs/architecture/`

- **[COMPARISON.md](architecture/COMPARISON.md)** - Approach comparisons (Context Nodes vs AI Tooling)
  - Maintenance overhead comparison
  - Setup time analysis
  - Trade-off evaluation

---

## Getting Started

### For AI Agents

**Read in this order:**

1. **[docs/core/MANIFEST.md](core/MANIFEST.md)** - Project vision and context
2. **[docs/core/AI_AGENT_GOLDEN_RULES.md](core/AI_AGENT_GOLDEN_RULES.md)** - Mandatory rules
3. **[docs/core/AI_AGENT_GUIDE.md](core/AI_AGENT_GUIDE.md)** - Complete operating guide
4. **[docs/dev/NAVIGATION.md](dev/NAVIGATION.md)** - Codebase navigation

**Then run:**
```bash
# Build AI navigation index
python dev/aiagent_navigator.py index

# Get exploration plan
python dev/aiagent_navigator.py plan

# Ask questions
python dev/aiagent_navigator.py ask "How does authentication work?"
```

### For Human Developers

**Read in this order:**

1. **[../README.md](../README.md)** - Project overview and quick start
2. **[docs/core/MANIFEST.md](core/MANIFEST.md)** - Project context and conventions
3. **[docs/api/API_DOCUMENTATION.md](api/API_DOCUMENTATION.md)** - API reference
4. **[docs/deployment/RENDER_DEPLOYMENT.md](deployment/RENDER_DEPLOYMENT.md)** - Deployment guide

**Then run:**
```bash
# Install dependencies
pip install -r backend/requirements.txt
pip install -r backend/requirements-dev.txt

# Run tests
pytest

# Start development server
cd backend && uvicorn main:app --reload
```

---

## Documentation by Role

### Backend Developers
- [API_DOCUMENTATION.md](api/API_DOCUMENTATION.md)
- [NAICS_EXPANSION_SUMMARY.md](backend/NAICS_EXPANSION_SUMMARY.md)
- [MANIFEST.md](core/MANIFEST.md) - Architecture section

### Frontend Developers
- [MANIFEST.md](core/MANIFEST.md) - ONETRUTH branding section
- Frontend docs (planned)

### DevOps Engineers
- [RENDER_DEPLOYMENT.md](deployment/RENDER_DEPLOYMENT.md)
- [DEPLOYMENT.md](deployment/DEPLOYMENT.md)

### QA Engineers
- [TEST_REPORT.md](dev/TEST_REPORT.md)
- [AI_AGENT_GOLDEN_RULES.md](core/AI_AGENT_GOLDEN_RULES.md) - Testing requirements

### AI Agents
- [MANIFEST.md](core/MANIFEST.md) - START HERE
- [AI_AGENT_GOLDEN_RULES.md](core/AI_AGENT_GOLDEN_RULES.md) - MANDATORY
- [AI_AGENT_GUIDE.md](core/AI_AGENT_GUIDE.md)
- [AI_AGENT_TOOLING.md](dev/AI_AGENT_TOOLING.md)

---

## Documentation Standards

All documentation in this repository follows these standards:

### Format
- **Markdown (.md)** for all documentation
- **UPPERCASE.md** for important core documents
- **lowercase.md** for guides and references

### Structure
- Clear table of contents for documents > 200 lines
- Code examples with syntax highlighting
- Cross-references using relative links
- Last Updated date at top of document

### Maintenance
- Update docs in same PR as code changes
- Run `python dev/aiagent_navigator.py index` after doc updates
- Review auto-generated NAVIGATION.md for accuracy

---

## Contributing to Documentation

### Adding New Documentation

1. **Choose the correct directory:**
   - `core/` - Project fundamentals and AI agent guides
   - `api/` - API endpoint documentation
   - `backend/` - Backend implementation details
   - `frontend/` - Frontend implementation details
   - `dev/` - Development tools and processes
   - `deployment/` - Deployment and infrastructure
   - `architecture/` - Design decisions and comparisons

2. **Follow naming conventions:**
   - Use UPPERCASE.md for critical documents
   - Use descriptive lowercase names for guides
   - Include version numbers if versioned

3. **Update this index:**
   - Add entry to appropriate section
   - Include brief description
   - Add to role-based navigation if applicable

4. **Commit with clear message:**
   ```bash
   git add docs/
   git commit -m "docs: Add [document name] for [purpose]"
   ```

### Updating Existing Documentation

1. Update the "Last Updated" date
2. Add changelog entry if significant changes
3. Update AI navigation index: `python dev/aiagent_navigator.py index`
4. Verify all links still work

---

## Auto-Generated Documentation

Some documentation is automatically generated and should NOT be manually edited:

- **[dev/NAVIGATION.md](dev/NAVIGATION.md)** - Generated by `aiagent_navigator.py`
- **[dev/TEST_REPORT.md](dev/TEST_REPORT.md)** - Generated by test runs

To regenerate:
```bash
# Navigation guide
python dev/aiagent_navigator.py guide

# Test reports
python dev/test_report_generator.py
```

---

## Documentation Health

| Category | Files | Status | Coverage |
|----------|-------|--------|----------|
| Core | 4 | ✅ Complete | 100% |
| API | 1 | ✅ Complete | 100% |
| Backend | 1 | ✅ Complete | 100% |
| Frontend | 0 | ⚠️ Needs docs | 0% |
| Dev Tools | 4 | ✅ Complete | 100% |
| Deployment | 2 | ✅ Complete | 100% |
| Architecture | 1 | ✅ Complete | 100% |

**Total:** 13 documentation files

---

## Quick Reference Links

### Most Important Documents
1. [MANIFEST.md](core/MANIFEST.md) - Project context
2. [AI_AGENT_GOLDEN_RULES.md](core/AI_AGENT_GOLDEN_RULES.md) - Development rules
3. [API_DOCUMENTATION.md](api/API_DOCUMENTATION.md) - API reference
4. [RENDER_DEPLOYMENT.md](deployment/RENDER_DEPLOYMENT.md) - Deployment guide

### Frequently Accessed
- [AI Agent Guide](core/AI_AGENT_GUIDE.md)
- [NAICS Implementation](backend/NAICS_EXPANSION_SUMMARY.md)
- [Navigation Guide](dev/NAVIGATION.md)
- [Testing Documentation](dev/TEST_REPORT.md)

---

## Getting Help

- **For AI agents:** Read [AI_AGENT_GUIDE.md](core/AI_AGENT_GUIDE.md)
- **For developers:** Check [MANIFEST.md](core/MANIFEST.md) troubleshooting section
- **For deployment issues:** See [RENDER_DEPLOYMENT.md](deployment/RENDER_DEPLOYMENT.md)
- **For testing:** See [AI_AGENT_GOLDEN_RULES.md](core/AI_AGENT_GOLDEN_RULES.md) Rule 1

---

**End of Documentation Index**
