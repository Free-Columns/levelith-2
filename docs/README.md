# Levelith Documentation Index

**Last Updated:** 2025-11-20
**Project:** Levelith-2 - Social Resume Gamification Platform

---

## Quick Navigation

- **For AI Agents:** Start with [Core Documentation](#core-documentation)
- **For Developers:** See [Getting Started](#getting-started)
- **For Deployment:** See [Deployment Documentation](#deployment-documentation)
- **For API Reference:** See [API Documentation](#api-documentation)
- **For Executive Summary:** See [Codebase Summary Report](#executive-summary)

---

## Executive Summary

**New:** Comprehensive analysis report for quick understanding of the project status.

- **[CODEBASE_SUMMARY_REPORT.md](CODEBASE_SUMMARY_REPORT.md)** - Executive summary of codebase analysis, current state, and production roadmap (12 min read)
  - Overall grade: B+ (85/100)
  - Current metrics and status
  - Critical issues summary
  - Path to production (60-100 hours)
  - Key recommendations

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
  - 60+ official industry codes (expandable via TSV import)
  - 14 industry categories
  - Hierarchical support (2/3/4/6 digit levels)
  - Database persistence with PostgreSQL
  - TSV import/export functionality
  - Admin dashboard with visualizations
  - 197 comprehensive tests (98% coverage)

---

## Database Documentation

Complete database architecture, schema reference, and usage guides.

Location: `docs/database/`

- **[DATABASE_OVERVIEW.md](database/DATABASE_OVERVIEW.md)** - Entry point for database documentation
  - PostgreSQL + SQLAlchemy ORM
  - Core tables (users, experiences, naics_codes)
  - Design philosophy and key features
  - Connection management and health checks

- **[DATABASE_ARCHITECTURE.md](database/DATABASE_ARCHITECTURE.md)** - Design decisions and patterns
  - Layered architecture explanation
  - Single table inheritance rationale
  - Denormalized NAICS hierarchy
  - JSON fields strategy
  - Trade-offs and alternatives

- **[SCHEMA_REFERENCE.md](database/SCHEMA_REFERENCE.md)** - Complete schema documentation
  - All 3 tables with column specifications
  - Constraints and indexes
  - Relationships and foreign keys
  - Example SQL queries

- **[USAGE_GUIDE.md](database/USAGE_GUIDE.md)** - How to use the database
  - CRUD operations examples
  - Working with relationships
  - Common patterns (pagination, search, filtering)
  - Best practices and error handling

- **[TESTING_DATABASE.md](database/TESTING_DATABASE.md)** - Testing strategies
  - Test fixtures and factories
  - Test patterns for CRUD, relationships, cascade deletes
  - Mocking strategies
  - 80% coverage requirements

- **[DATA_MODELS.md](database/DATA_MODELS.md)** - ORM model reference
  - UserDB model complete specification
  - ExperienceDB model and 9 polymorphic subtypes
  - NAICSCodeDB model
  - Model relationships and enums

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
| [CODEBASE_ANALYSIS.md](dev/CODEBASE_ANALYSIS.md) | **NEW:** Comprehensive codebase analysis report (architecture, coverage, quality) |
| [DEVELOPMENT_PRIORITIES.md](dev/DEVELOPMENT_PRIORITIES.md) | **NEW:** Development roadmap and priorities (60-100 hour plan) |
| [TEST_REPORT.md](dev/TEST_REPORT.md) | Test system reports and coverage |
| [NAICS_IMPORT_GUIDE.md](dev/NAICS_IMPORT_GUIDE.md) | Complete guide for importing NAICS codes from TSV files |
| [NAICS_QUICK_REFERENCE.md](dev/NAICS_QUICK_REFERENCE.md) | Quick reference for NAICS database import commands |
| [ADMIN_PANEL_GUIDE.md](dev/ADMIN_PANEL_GUIDE.md) | Complete admin dashboard integration and usage guide |
| [COMPREHENSIVE_TODO_REPORT.md](dev/COMPREHENSIVE_TODO_REPORT.md) | Complete TODO analysis and action plan |

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

- **[DATABASE_SETUP_NOTES.md](deployment/DATABASE_SETUP_NOTES.md)** - Database initialization and configuration
  - PostgreSQL setup
  - Database initialization script
  - Connection troubleshooting
  - Environment configuration

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
- [KNOWN_ISSUES.md](core/KNOWN_ISSUES.md) - **NEW:** Critical issues to be aware of
- [CODEBASE_ANALYSIS.md](dev/CODEBASE_ANALYSIS.md) - **NEW:** Complete analysis report
- [DEVELOPMENT_PRIORITIES.md](dev/DEVELOPMENT_PRIORITIES.md) - **NEW:** Development roadmap
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
| Executive Summary | 1 | ✅ Complete | 100% |
| Core | 5 | ✅ Complete | 100% |
| API | 1 | ✅ Complete | 100% |
| Backend | 1 | ✅ Complete | 100% |
| Database | 6 | ✅ Complete | 100% |
| Frontend | 1 | ✅ Complete | 100% |
| Dev Tools | 11 | ✅ Complete | 100% |
| Deployment | 3 | ✅ Complete | 100% |
| Architecture | 1 | ✅ Complete | 100% |

**Total:** 31 documentation files

---

## Quick Reference Links

### Most Important Documents
1. [CODEBASE_SUMMARY_REPORT.md](CODEBASE_SUMMARY_REPORT.md) - **NEW:** Executive summary (START HERE)
2. [MANIFEST.md](core/MANIFEST.md) - Project context
3. [AI_AGENT_GOLDEN_RULES.md](core/AI_AGENT_GOLDEN_RULES.md) - Development rules
4. [KNOWN_ISSUES.md](core/KNOWN_ISSUES.md) - Critical issues and gaps
5. [CODEBASE_ANALYSIS.md](dev/CODEBASE_ANALYSIS.md) - Complete analysis report
6. [DEVELOPMENT_PRIORITIES.md](dev/DEVELOPMENT_PRIORITIES.md) - Roadmap to production
7. [API_DOCUMENTATION.md](api/API_DOCUMENTATION.md) - API reference
8. [RENDER_DEPLOYMENT.md](deployment/RENDER_DEPLOYMENT.md) - Deployment guide

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
