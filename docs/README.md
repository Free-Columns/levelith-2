# Levelith Documentation Index

**Last Updated:** 2025-11-20
**Project:** Levelith-2 - Social Resume Gamification Platform

---

## Quick Navigation

- **For AI Agents:** Start with [Agent Documentation](#agent-documentation)
- **For Developers:** See [Getting Started](#getting-started)
- **For Deployment:** See [Deployment Documentation](#deployment-documentation)
- **For API Reference:** See [API Documentation](#api-documentation)
- **For Executive Summary:** See [Reports](#reports)

---

## Documentation Structure

```
docs/
├── agent/               # AI agent guides and tooling
├── api/                 # API endpoint reference
├── architecture/        # Architecture analysis and comparisons
│   └── trees/
├── backend/            # Backend implementation docs
│   ├── database/       # Database architecture and models
│   │   ├── models/     # Individual model docs
│   │   ├── tools/      # Database tools
│   │   └── utils/      # Database utilities
│   ├── naics/          # NAICS classification system
│   │   └── data/       # NAICS TSV data files
│   └── core/           # Core backend documentation
├── deployment/         # Deployment guides
├── development/        # Development documentation
│   ├── admin/          # Admin dashboard
│   ├── ci-cd/          # CI/CD pipeline
│   └── testing/        # Testing guides
├── frontend/           # Frontend documentation
└── reports/            # Status reports and analysis
```

---

## Reports

Executive summaries and status reports for quick understanding of project health.

Location: `docs/reports/`

- **[CODEBASE_SUMMARY_REPORT.md](reports/CODEBASE_SUMMARY_REPORT.md)** - Executive summary of codebase analysis (12 min read)
  - Overall grade: B+ (85/100)
  - Current metrics and status
  - Critical issues summary
  - Path to production (60-100 hours)
  - Key recommendations

---

## Agent Documentation

Essential documentation for AI agent operation and navigation.

Location: `docs/agent/`

| Document | Purpose | Audience |
|----------|---------|----------|
| [MANIFEST.md](agent/MANIFEST.md) | ⚠️ Project vision, goals, architecture (START HERE) | AI Agents, All Developers |
| [AI_AGENT_GOLDEN_RULES.md](agent/AI_AGENT_GOLDEN_RULES.md) | ⚠️ MANDATORY 10 development rules | AI Agents |
| [AI_AGENT_GUIDE.md](agent/AI_AGENT_GUIDE.md) | Complete AI operating guide v2.0 | AI Agents |
| [AI_AGENT_TOOLING.md](agent/AI_AGENT_TOOLING.md) | Technical documentation for AI navigation system | AI Agents, Developers |
| [claude_navigation.md](agent/claude_navigation.md) | Navigation system overview | AI Agents, Developers |
| [KNOWN_ISSUES.md](agent/KNOWN_ISSUES.md) | Critical issues and gaps tracker | AI Agents, All Developers |

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

### Database

Complete database architecture, schema reference, and usage guides.

Location: `docs/backend/database/`

#### Overview & Architecture

- **[DATABASE_OVERVIEW.md](backend/database/DATABASE_OVERVIEW.md)** - Entry point for database documentation
  - PostgreSQL + SQLAlchemy ORM
  - Core tables (users, experiences, naics_codes)
  - Design philosophy and key features
  - Connection management and health checks

- **[DATABASE_ARCHITECTURE.md](backend/database/DATABASE_ARCHITECTURE.md)** - Design decisions and patterns
  - Layered architecture explanation
  - Single table inheritance rationale
  - Denormalized NAICS hierarchy
  - JSON fields strategy
  - Trade-offs and alternatives

- **[SCHEMA_REFERENCE.md](backend/database/SCHEMA_REFERENCE.md)** - Complete schema documentation
  - All 3 tables with column specifications
  - Constraints and indexes
  - Relationships and foreign keys
  - Example SQL queries

#### Usage & Testing

- **[USAGE_GUIDE.md](backend/database/USAGE_GUIDE.md)** - How to use the database
  - CRUD operations examples
  - Working with relationships
  - Common patterns (pagination, search, filtering)
  - Best practices and error handling

- **[TESTING_DATABASE.md](backend/database/TESTING_DATABASE.md)** - Testing strategies
  - Test fixtures and factories
  - Test patterns for CRUD, relationships, cascade deletes
  - Mocking strategies
  - 80% coverage requirements

- **[DATA_MODELS.md](backend/database/DATA_MODELS.md)** - ORM model reference
  - UserDB model complete specification
  - ExperienceDB model and 9 polymorphic subtypes
  - NAICSCodeDB model
  - Model relationships and enums

#### Model Documentation

Location: `docs/backend/database/models/`

- **[user.md](backend/database/models/user.md)** - Complete UserDB model reference
  - Field specifications and constraints
  - profile_data JSON schema
  - Relationships and cascade behavior
  - Usage examples and best practices

- **[experience.md](backend/database/models/experience.md)** - Complete ExperienceDB model reference
  - Base model definition
  - All 9 polymorphic subtypes (Certificate, Degree, Course, Gig, PartTime, FullTime, SoftSkill, HardSkill, NativeSkill)
  - type_specific_data schemas
  - Polymorphic query examples

- **[naics.md](backend/database/models/naics.md)** - Complete NAICSCodeDB model reference
  - NAICS 2022 hierarchy structure (2/3/4/6 digit levels)
  - Denormalized fields for performance
  - Search fields (keywords, aliases, examples)
  - SBA integration
  - Usage examples and optimization

### NAICS Classification

NAICS 2022 industry classification system implementation.

Location: `docs/backend/naics/`

- **[NAICS_EXPANSION_SUMMARY.md](backend/naics/NAICS_EXPANSION_SUMMARY.md)** - NAICS 2022 system implementation
  - 60+ official industry codes (expandable via TSV import)
  - 14 industry categories
  - Hierarchical support (2/3/4/6 digit levels)
  - Database persistence with PostgreSQL
  - TSV import/export functionality
  - Admin dashboard with visualizations
  - 197 comprehensive tests (98% coverage)

- **[NAICS_IMPORT_GUIDE.md](backend/naics/NAICS_IMPORT_GUIDE.md)** - Complete guide for importing NAICS codes from TSV files
  - TSV file format specification
  - Import command reference
  - Troubleshooting common issues

- **[NAICS_QUICK_REFERENCE.md](backend/naics/NAICS_QUICK_REFERENCE.md)** - Quick reference for NAICS database import commands
  - One-line import commands
  - Common usage patterns

#### NAICS Data Files

Location: `docs/backend/naics/data/`

- `naics_2022_all_10k_rows.tsv` - 10k NAICS codes dataset
- `naics_2022_sample_62_rows.tsv` - Sample 62 codes for testing

---

## Architecture Documentation

System architecture, design decisions, and comparisons.

Location: `docs/architecture/`

- **[COMPARISON.md](architecture/COMPARISON.md)** - Approach comparisons (Context Nodes vs AI Tooling)
  - Maintenance overhead comparison
  - Setup time analysis
  - Trade-off evaluation

---

## Development Documentation

Development tooling, testing, CI/CD, and admin dashboard.

Location: `docs/development/`

### Admin Dashboard

Location: `docs/development/admin/`

- **[ADMIN_PANEL_GUIDE.md](development/admin/ADMIN_PANEL_GUIDE.md)** - Complete admin dashboard integration and usage guide
  - User management interface
  - NAICS code management
  - Bulk import functionality
  - Visualization features

### Testing

Location: `docs/development/testing/`

- **[TEST_REPORT.md](development/testing/TEST_REPORT.md)** - Test system reports and coverage
  - Current test coverage metrics
  - Failed/passing tests summary
  - Coverage gaps analysis

- **[COMPREHENSIVE_TODO_REPORT.md](development/testing/COMPREHENSIVE_TODO_REPORT.md)** - Complete TODO analysis and action plan
  - All TODOs in codebase
  - Prioritized action items
  - Estimated completion times

### General Development

Location: `docs/development/`

- **[NAVIGATION.md](development/NAVIGATION.md)** - Auto-generated codebase navigation guide
- **[CODEBASE_ANALYSIS.md](development/CODEBASE_ANALYSIS.md)** - Comprehensive codebase analysis report
  - Architecture overview
  - Code quality metrics
  - Test coverage analysis
- **[DEVELOPMENT_PRIORITIES.md](development/DEVELOPMENT_PRIORITIES.md)** - Development roadmap and priorities
  - 60-100 hour plan to production
  - Prioritized tasks with time estimates
  - Critical path items

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

## Frontend Documentation

Frontend architecture, components, and user interface documentation.

Location: `docs/development/frontend/`

**Status:** Admin dashboard infrastructure complete (Phase 0 & Phase 1).

**Available Documentation:**

- **[INFRASTRUCTURE_OVERVIEW.md](development/frontend/INFRASTRUCTURE_OVERVIEW.md)** - Complete Phase 0 & 1 overview (15 min read)
  - Technology stack (React, TypeScript, Vite, Tailwind, React Query)
  - Folder structure and architecture principles
  - Type system and validation schemas
  - 35/165 tasks complete (21% progress)

- **[ADMIN_COMPONENTS_GUIDE.md](development/frontend/ADMIN_COMPONENTS_GUIDE.md)** - Reusable UI components (30 min read)
  - DataTable with sorting and selection
  - SearchBar with debouncing
  - FilterPanel, Pagination
  - Loading states (spinner, skeleton)
  - ErrorBoundary and ConfirmDialog
  - Complete usage examples and API reference

- **[ADMIN_HOOKS_GUIDE.md](development/frontend/ADMIN_HOOKS_GUIDE.md)** - Custom React hooks (20 min read)
  - useDebounce for search optimization
  - usePagination for state management
  - useLocalStorage with cross-tab sync
  - useDisclosure for modal state
  - Problem-solution explanations

- **[ADMIN_API_CLIENT_GUIDE.md](development/frontend/ADMIN_API_CLIENT_GUIDE.md)** - Type-safe API methods (25 min read)
  - Users API (7 methods)
  - Experiences API (9 methods, polymorphic)
  - NAICS API (9 methods, hierarchy support)
  - React Query integration patterns
  - Request/response examples

- **[ADMIN_DASHBOARD_REFACTOR_V2.md](development/admin/ADMIN_DASHBOARD_REFACTOR_V2.md)** - 8-phase implementation plan
  - Phase 0: Setup (✅ Complete)
  - Phase 1: Core Infrastructure (✅ Complete)
  - Phases 2-8: Features and production (Planned)

**Planned:**
- ONETRUTH theming guide
- User-facing frontend documentation
- State management patterns
- UI/UX guidelines

---

## Getting Started

### For AI Agents

**Read in this order:**

1. **[docs/agent/MANIFEST.md](agent/MANIFEST.md)** - Project vision and context
2. **[docs/agent/AI_AGENT_GOLDEN_RULES.md](agent/AI_AGENT_GOLDEN_RULES.md)** - Mandatory rules
3. **[docs/agent/AI_AGENT_GUIDE.md](agent/AI_AGENT_GUIDE.md)** - Complete operating guide
4. **[docs/development/NAVIGATION.md](development/NAVIGATION.md)** - Codebase navigation

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
2. **[docs/agent/MANIFEST.md](agent/MANIFEST.md)** - Project context and conventions
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
- [DATABASE_OVERVIEW.md](backend/database/DATABASE_OVERVIEW.md)
- [DATABASE_ARCHITECTURE.md](backend/database/DATABASE_ARCHITECTURE.md)
- [NAICS_EXPANSION_SUMMARY.md](backend/naics/NAICS_EXPANSION_SUMMARY.md)
- [MANIFEST.md](agent/MANIFEST.md) - Architecture section

### Frontend Developers
- [MANIFEST.md](agent/MANIFEST.md) - ONETRUTH branding section
- [INFRASTRUCTURE_OVERVIEW.md](development/frontend/INFRASTRUCTURE_OVERVIEW.md) - Phase 0 & 1 setup
- [ADMIN_COMPONENTS_GUIDE.md](development/frontend/ADMIN_COMPONENTS_GUIDE.md) - Reusable components
- [ADMIN_HOOKS_GUIDE.md](development/frontend/ADMIN_HOOKS_GUIDE.md) - Custom hooks
- [ADMIN_API_CLIENT_GUIDE.md](development/frontend/ADMIN_API_CLIENT_GUIDE.md) - API methods
- [ADMIN_DASHBOARD_REFACTOR_V2.md](development/admin/ADMIN_DASHBOARD_REFACTOR_V2.md) - Implementation plan

### DevOps Engineers
- [RENDER_DEPLOYMENT.md](deployment/RENDER_DEPLOYMENT.md)
- [DEPLOYMENT.md](deployment/DEPLOYMENT.md)
- [DATABASE_SETUP_NOTES.md](deployment/DATABASE_SETUP_NOTES.md)

### QA Engineers
- [TEST_REPORT.md](development/testing/TEST_REPORT.md)
- [TESTING_DATABASE.md](backend/database/TESTING_DATABASE.md)
- [AI_AGENT_GOLDEN_RULES.md](agent/AI_AGENT_GOLDEN_RULES.md) - Testing requirements

### AI Agents
- [MANIFEST.md](agent/MANIFEST.md) - START HERE
- [AI_AGENT_GOLDEN_RULES.md](agent/AI_AGENT_GOLDEN_RULES.md) - MANDATORY
- [AI_AGENT_GUIDE.md](agent/AI_AGENT_GUIDE.md)
- [KNOWN_ISSUES.md](agent/KNOWN_ISSUES.md) - Critical issues to be aware of
- [CODEBASE_ANALYSIS.md](development/CODEBASE_ANALYSIS.md) - Complete analysis report
- [DEVELOPMENT_PRIORITIES.md](development/DEVELOPMENT_PRIORITIES.md) - Development roadmap
- [AI_AGENT_TOOLING.md](agent/AI_AGENT_TOOLING.md)

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
   - `agent/` - AI agent guides and project fundamentals
   - `api/` - API endpoint documentation
   - `backend/database/` - Database architecture and models
   - `backend/naics/` - NAICS classification system
   - `backend/core/` - Core backend implementation
   - `frontend/` - Frontend implementation details
   - `development/` - Development tools and processes
   - `deployment/` - Deployment and infrastructure
   - `architecture/` - Design decisions and comparisons
   - `reports/` - Status reports and analysis

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

- **[development/NAVIGATION.md](development/NAVIGATION.md)** - Generated by `aiagent_navigator.py`
- **[development/testing/TEST_REPORT.md](development/testing/TEST_REPORT.md)** - Generated by test runs

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
| Reports | 1 | ✅ Complete | 100% |
| Agent | 6 | ✅ Complete | 100% |
| API | 1 | ✅ Complete | 100% |
| Backend - Database | 9 | ✅ Complete | 100% |
| Backend - NAICS | 4 | ✅ Complete | 100% |
| Architecture | 1 | ✅ Complete | 100% |
| Development - Admin | 2 | ✅ Complete | 100% |
| Development - Testing | 2 | ✅ Complete | 100% |
| Development - General | 3 | ✅ Complete | 100% |
| Development - Frontend | 4 | ✅ Complete | 100% |
| Deployment | 3 | ✅ Complete | 100% |

**Total:** 41 documentation files

---

## Quick Reference Links

### Most Important Documents
1. [CODEBASE_SUMMARY_REPORT.md](reports/CODEBASE_SUMMARY_REPORT.md) - Executive summary (START HERE)
2. [MANIFEST.md](agent/MANIFEST.md) - Project context
3. [AI_AGENT_GOLDEN_RULES.md](agent/AI_AGENT_GOLDEN_RULES.md) - Development rules
4. [KNOWN_ISSUES.md](agent/KNOWN_ISSUES.md) - Critical issues and gaps
5. [CODEBASE_ANALYSIS.md](development/CODEBASE_ANALYSIS.md) - Complete analysis report
6. [DEVELOPMENT_PRIORITIES.md](development/DEVELOPMENT_PRIORITIES.md) - Roadmap to production
7. [API_DOCUMENTATION.md](api/API_DOCUMENTATION.md) - API reference
8. [DATABASE_OVERVIEW.md](backend/database/DATABASE_OVERVIEW.md) - Database documentation
9. [RENDER_DEPLOYMENT.md](deployment/RENDER_DEPLOYMENT.md) - Deployment guide

### Frequently Accessed
- [AI Agent Guide](agent/AI_AGENT_GUIDE.md)
- [Database Architecture](backend/database/DATABASE_ARCHITECTURE.md)
- [NAICS Implementation](backend/naics/NAICS_EXPANSION_SUMMARY.md)
- [Navigation Guide](development/NAVIGATION.md)
- [Testing Documentation](development/testing/TEST_REPORT.md)

### Model Reference
- [User Model](backend/database/models/user.md)
- [Experience Model](backend/database/models/experience.md)
- [NAICS Model](backend/database/models/naics.md)

---

## Getting Help

- **For AI agents:** Read [AI_AGENT_GUIDE.md](agent/AI_AGENT_GUIDE.md)
- **For developers:** Check [MANIFEST.md](agent/MANIFEST.md) troubleshooting section
- **For deployment issues:** See [RENDER_DEPLOYMENT.md](deployment/RENDER_DEPLOYMENT.md)
- **For testing:** See [AI_AGENT_GOLDEN_RULES.md](agent/AI_AGENT_GOLDEN_RULES.md) Rule 1
- **For database:** See [DATABASE_OVERVIEW.md](backend/database/DATABASE_OVERVIEW.md)

---

**End of Documentation Index**
