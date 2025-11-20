# Claude.md - AI Agent Navigation Guide

---
title: "Claude.md - AI Agent Navigation Guide"
description: "Comprehensive navigation guide for AI agents featuring intelligent tooling, context node system, backend deployment instructions, and development tools for the Levelith platform."
category: "guides"
tags: ["navigation", "ai-agent", "intelligent-tooling", "context-nodes", "backend", "deployment", "render", "fastapi"]
author: "Semour Media Group"
date: "2025-11-15"
lastUpdated: "2025-11-19"
difficulty: "intermediate"
readingTime: 35
relatedPages:
  - "/docs/core/AI_AGENT_GUIDE.md"
  - "/docs/dev/AI_AGENT_TOOLING.md"
  - "/docs/COMPARISON.md"
  - "/docs/RENDER_DEPLOYMENT.md"
nextPage: "/docs/dev/AI_AGENT_TOOLING.md"
prevPage: "/docs/core/AI_AGENT_GUIDE.md"
searchKeywords:
  - "navigation"
  - "claude"
  - "ai agent"
  - "intelligent tooling"
  - "backend deployment"
  - "render"
  - "fastapi"
showTOC: true
showBreadcrumbs: true
showLastUpdated: true
version: "2.0"
---

# Claude.md - AI Agent Navigation Guide

> **TL;DR:** AI-first navigation system with intelligent tooling for dynamic code analysis, context nodes for human insights, production-ready FastAPI backend deployment to Render, and comprehensive development tools including a color visualizer.

**Difficulty:** 🟡 Intermediate | **Time:** ⏱️ 35 minutes | **Last Updated:** November 19, 2025

---

## Welcome, AI Agent!

This repository is designed with **you** as a first-class citizen. We provide two complementary navigation systems to help you efficiently explore and understand the codebase.

:::info
**Quick Start:** Jump to [Intelligent AI Agent Tooling](#intelligent-ai-agent-tooling-v20-recommended) for the recommended approach to navigate this codebase.
:::

---

## Table of Contents

- [Backend Status](#backend-status-ready-for-render-deployment)
- [Development Tools](#development-tools)
- [Navigation Systems Overview](#navigation-systems-overview)
- [Intelligent AI Agent Tooling v2.0](#intelligent-ai-agent-tooling-v20-recommended)
- [Context Node System](#context-node-system-legacy)
- [Recommended Approach](#recommended-approach)
- [Configuration](#configuration-aiagentjson)
- [Backend Navigation Guide](#backend-navigation-guide)
- [Learning Path for AI Agents](#learning-path-for-ai-agents)
- [Quick Reference](#quick-reference)
- [Benefits](#benefits)
- [Next Steps](#next-steps)

---

## 🚀 Backend Status: READY FOR RENDER DEPLOYMENT

The Levelith backend is a **production-ready FastAPI application** configured for Render Web Service deployment.

### Backend Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Framework** | FastAPI | 0.109.0 |
| **Database** | PostgreSQL | Render Managed |
| **ORM** | SQLAlchemy | 2.0.25 |
| **Validation** | Pydantic | 2.10.4 |
| **Python** | Python | 3.11.0 |
| **Server** | Uvicorn + Gunicorn | - |
| **Deployment** | Render Web Service | IaC via render.yaml |

:::success
**Production Ready:** The backend is fully configured for Render deployment with Infrastructure as Code via `render.yaml`.
:::

### Key Backend Files to Understand

<details>
<summary><strong>📋 Essential Backend Files</strong></summary>

**Core Application:**
- `backend/main.py` - FastAPI application entry point
- `backend/config.py` - Environment configuration with Pydantic Settings
- `backend/database.py` - SQLAlchemy database session management

**Models & Data:**
- `backend/models/db_models.py` - SQLAlchemy ORM models for User and Experience
- `backend/models/naics.py` - NAICS code domain model with validation and hierarchy
- `backend/data/naics_codes_2022.json` - Official NAICS 2022 codes dataset (60+ codes)

**Repository Layer:**
- `backend/repositories/naics_repository.py` - In-memory NAICS data repository with indexing

**Service Layer:**
- `backend/services/naics_service.py` - NAICS business logic and experience suggestions

**API Layer:**
- `backend/api/routes/naics.py` - 12 NAICS REST API endpoints
- `backend/schemas/` - Pydantic request/response validation schemas
- `backend/api/routes/` - API endpoint handlers (health, users, experiences, naics)

**Deployment:**
- `render.yaml` - Render deployment configuration (Infrastructure as Code)
- `runtime.txt` - Python version specification (3.11.0, at repository root)
- `.env.render.example` - Environment variables reference

**Documentation:**
- `DEPLOYMENT.md` - Complete deployment guide with step-by-step instructions
- `NAICS_EXPANSION_SUMMARY.md` - Complete NAICS implementation documentation
- `RENDER_DEPLOYMENT.md` - Render-specific deployment guide with troubleshooting

</details>

### API Documentation (Local Development)

When running locally, access:

| Endpoint | URL | Description |
|----------|-----|-------------|
| **Swagger UI** | http://localhost:8000/docs | Interactive API documentation |
| **ReDoc** | http://localhost:8000/redoc | Alternative API documentation |
| **Health Check** | http://localhost:8000/health | Service health status |

### Deployment to Render

✅ **Production-ready for Render Web Service deployment (no blueprints required)**

<details>
<summary><strong>🚀 Quick Deploy Steps</strong></summary>

1. **Create PostgreSQL database** in Render Dashboard
2. **Create Web Service** (build: `pip install -r backend/requirements.txt`)
3. **Configure environment variables** (DATABASE_URL, SECRET_KEY, etc.)
4. **Deploy and test** health endpoint

See `RENDER_DEPLOYMENT.md` for complete step-by-step guide.

</details>

:::tip
**Pro Tip:** The `render.yaml` file provides Infrastructure as Code configuration, making deployment repeatable and version-controlled.
:::

---

## 🎨 Development Tools

### Color Visualizer

**Location:** `tools/color-visualizer.html`

An interactive standalone HTML tool for visualizing and editing the ONETRUTH color configuration (`frontend/src/config/ONETRUTH.ts`).

**Features:**
- ✅ **48 Color Swatches** - All ONETRUTH colors organized by category
- ✅ **Triple Control System** - RGB sliders, HSL sliders, and Hex input (all synchronized)
- ✅ **Real-time Updates** - See changes instantly
- ✅ **Export Options** - Download .ts file or copy to clipboard
- ✅ **Zero Dependencies** - Standalone HTML file

**Quick Start:**
```bash
# Open the tool
open tools/color-visualizer.html

# Or double-click in file browser
```

**Color Categories:**
- Main Colors (26): Primary, secondary, accent, backgrounds, text, status, borders
- Gamification Levels (6): Beginner through legend
- Gamification Achievements (5): Bronze through diamond
- Gamification Progress (3): Low, medium, high
- NAICS Industries (8): Industry-specific colors

:::info
**Documentation:** See `tools/README.md` for complete usage guide.
:::

---

## Navigation Systems Overview

We provide two complementary navigation systems, each with distinct strengths:

| System | Type | Best For | Maintenance |
|--------|------|----------|-------------|
| **Intelligent AI Agent Tooling** | Dynamic | Active development, automated workflows | ✅ Automated |
| **Context Node System** | Static | Adding human commentary, stable codebases | ⚠️ Manual |

:::tip
**Recommended:** Use **Intelligent AI Agent Tooling** for most tasks. It's automated, always current, and optimized for AI comprehension.
:::

---

## Intelligent AI Agent Tooling v2.0 (Recommended)

### What It Is

A **next-generation dynamic code analysis system** that extracts structure and relationships directly from code.

#### v2.0 New Features

- 🚀 **30-Second Quickstart** - Instant codebase overview
- 🎯 **Goal-Oriented Exploration** - AI-powered exploration paths
- 💬 **Natural Language Queries** - Ask questions in plain English
- 🧠 **Cognitive Load Management** - Context window optimization
- 🎓 **Interactive Learning** - Guided tutorials for AI agents
- ⚡ **Performance Navigator** - Progressive loading for large codebases
- 📊 **Exploration Metrics** - Track efficiency and improve

#### v1.0 Core Features

- ✅ **Always Current Information** - Generated from actual code, never stale
- ✅ **On-Demand Analysis** - Query what you need, when you need it
- ✅ **Relationship Mapping** - Automatic dependency detection
- ✅ **Smart Exploration** - Guided navigation through complex codebases

### Quick Start

```bash
# NEW v2.0: Get 30-second overview
python dev/aiagent_navigator.py quickstart

# Get exploration plan
python dev/aiagent_navigator.py plan

# Build codebase index
python dev/aiagent_navigator.py index

# NEW v2.0: Ask questions in natural language
python dev/aiagent_navigator.py ask "How does NAICS classification work?"

# Generate navigation guide
python dev/aiagent_navigator.py guide

# Analyze specific file
python dev/aiagent_navigator.py analyze dev/aiagent_navigator.py

# NEW v2.0: Interactive tutorial
python dev/aiagent_navigator.py tutorial
```

### How It Works

```
1. Configuration (.aiagent.json)
   ↓
2. Navigator scans code → Builds index
   ↓
3. You query for information
   ↓
4. Get real-time analysis from actual code
```

### Key Features

#### 1. Exploration Planning

Get a smart exploration strategy:

```bash
python dev/aiagent_navigator.py plan
```

**Returns:**
- ✅ **Suggested starting points** - Where to begin reading
- ✅ **Entry points** - Main executable files
- ✅ **Key modules** - Most important files by complexity/exports
- ✅ **Dependency graph** - How files connect
- ✅ **Complexity hotspots** - Files that need attention

#### 2. Module Analysis

Get detailed information about any file:

```bash
python dev/aiagent_navigator.py analyze src/auth/login.py
```

**Returns:**
```json
{
  "docstring": "Module description from code",
  "classes": ["UserAuth", "LoginHandler"],
  "functions": ["authenticate", "validate"],
  "imports": ["bcrypt", "jwt", "database"],
  "exports": ["UserAuth", "authenticate"],
  "complexity_score": 18
}
```

#### 3. Relationship Detection

Find related files automatically:

```bash
python dev/aiagent_navigator.py related src/auth/login.py
```

Shows files that:
- Import this module's exports
- Export things this module imports
- Share common dependencies

#### 4. Query Interface

Ask specific questions:

```python
from dev.aiagent_navigator import AIAgentQueryInterface

query = AIAgentQueryInterface()

# Where is this function defined?
query.where_is_function("authenticate_user")

# Where is this class?
query.where_is_class("UserAuth")

# What imports this module?
query.what_imports_module("jwt")

# What does this file export?
query.what_does_file_export("src/auth/login.py")

# Get codebase overview
query.get_complexity_overview()
```

### Files and Their Purposes

| File | Purpose | When to Use |
|------|---------|-------------|
| `.aiagent.json` | Configuration and hints | Read first for project-specific instructions |
| `dev/aiagent_navigator.py` | Intelligence engine | Import for programmatic access |
| `.aiagent-index.json` | Cached analysis | Auto-generated, speeds up queries |
| `NAVIGATION.md` | Navigation guide | Auto-generated, human-readable overview |
| `AI_AGENT_GUIDE.md` | Learning resource | Complete tutorial and reference |

### Typical Workflow

```
1. Read .aiagent.json for project-specific hints
   ↓
2. Run: python dev/aiagent_navigator.py plan
   ↓
3. Read suggested starting files (README, etc.)
   ↓
4. Analyze key modules one by one
   ↓
5. Follow relationships to understand connections
   ↓
6. Read actual code with full context
   ↓
COMPLETE UNDERSTANDING
```

:::tip
**Pro Tip:** Always start with `quickstart` for a 30-second overview, then use `plan` for a detailed exploration strategy.
:::

### When to Use

- ✅ **Starting fresh** - New to the codebase
- ✅ **After code changes** - Rebuild index to stay current
- ✅ **Finding specific code** - Query for functions/classes
- ✅ **Understanding structure** - Dependency analysis
- ✅ **Active development** - Always in sync

### Complete Documentation

- 📚 **[AI_AGENT_GUIDE.md](/docs/core/AI_AGENT_GUIDE.md)** - Complete learning and operating guide
- 🏗️ **[dev/AI_AGENT_TOOLING.md](/docs/dev/AI_AGENT_TOOLING.md)** - Technical documentation
- 🧪 **[COMPARISON.md](/docs/COMPARISON.md)** - Detailed comparison with Context Nodes

---

## Context Node System (Legacy)

### What It Is

A **static documentation system** where every file and directory has a corresponding `.context-node.md` file containing structured metadata.

:::warning
**Legacy System:** Context nodes require manual maintenance and can become outdated. Use intelligent tooling for automated, always-current analysis.
:::

### Core Concept

- Every file has a corresponding `[filename].context-node.md` file
- Every directory contains a `context-node.md` file
- These nodes provide structured metadata for AI comprehension

### File Structure

```
project/
├── context-node.md                 # Directory context
├── main.py
├── main.py.context-node.md        # File context
├── module/
│   ├── context-node.md            # Subdirectory context
│   ├── helper.py
│   └── helper.py.context-node.md  # File context
└── dev/
    └── cn-create.py                # Context node generator
```

### Context Node Format

Each context node contains:

1. **Overview** - Type, purpose, path, creation date
2. **Description** - Human-readable explanation
3. **Key Components** - Main elements (functions/files)
4. **Dependencies** - Internal and external requirements
5. **Interfaces** - Input/output specifications
6. **Related Nodes** - Navigation links
7. **AI Agent Notes** - Special instructions for AI processing

### Usage for AI Agents

<details>
<summary><strong>📖 How to Navigate with Context Nodes</strong></summary>

When navigating with context nodes:

1. **Start** with root `context-node.md` for project overview
2. **Drill down** into directories via their context nodes
3. **Understand files** through their individual context nodes
4. **Follow relationships** using "Related Context Nodes" sections
5. **Check dependencies** to understand interconnections

</details>

### Generating Context Nodes

Run from project root:

```bash
python dev/cn-create.py
```

This creates skeleton context nodes for all files/directories. Human review and enhancement recommended.

### Validating Context Nodes

Ensure context nodes are complete:

```bash
python dev/cn-validate.py
```

### Best Practices for Context Node Navigation

- ✅ Read directory context nodes before exploring contents
- ✅ Use file context nodes to understand purpose before reading code
- ✅ Follow the "Related Context Nodes" for connected functionality
- ✅ Pay attention to "AI Agent Notes" for special handling instructions

### When to Use

- **Human commentary needed** - Adding insights beyond code
- **Stable codebase** - Code doesn't change frequently
- **Documentation culture** - Team maintains docs actively
- **Complementary to tooling** - Add human insights to automated analysis

### Limitations

- ⚠️ **Manual maintenance required** - Update after every code change
- ⚠️ **Sync risk** - Docs can drift from code
- ⚠️ **Storage overhead** - Doubles number of files
- ⚠️ **Setup time** - Hours for initial creation

---

## Recommended Approach

### For AI Agents: Use Intelligent Tooling

**Start here:**
1. Run `python dev/aiagent_navigator.py plan`
2. Read [AI_AGENT_GUIDE.md](/docs/core/AI_AGENT_GUIDE.md)
3. Follow the exploration plan

**Why:**
- ✅ Always accurate (extracted from code)
- ✅ Fast (seconds to rebuild)
- ✅ Comprehensive (automatic analysis)
- ✅ Query-driven (ask questions)

### Hybrid Approach: Best of Both

You can use **both systems together**:

1. **Intelligent tooling** for structure and relationships
2. **Context nodes** for human insights and commentary
3. **Good docstrings** as single source of truth

**Example workflow:**
```bash
# Get automated structure
python dev/aiagent_navigator.py plan

# Read human insights (if they exist)
cat context-node.md  # Project-level commentary

# Analyze code
python dev/aiagent_navigator.py analyze src/module.py

# Read actual code with full context
cat src/module.py
```

:::tip
**Pro Tip:** The hybrid approach combines automation with human insight, giving you the best of both worlds.
:::

---

## Configuration: .aiagent.json

The intelligent tooling uses `.aiagent.json` for project-specific configuration:

```json
{
  "version": "1.0",

  "navigation": {
    "entry_points": ["dev/cn-create.py"],
    "key_directories": {
      "dev/": "Development tools and utilities"
    },
    "ignore_patterns": [
      "**/__pycache__/**",
      "**/*.pyc"
    ]
  },

  "exploration_hints": {
    "start_here": ["README.md", "claude.md"],
    "dependency_strategy": "follow_imports",
    "max_depth": 3
  },

  "agent_instructions": {
    "preferred_approach": "Start with entry_points, follow imports",
    "special_notes": [
      "This project uses context-node.md files for navigation",
      "Run 'python dev/cn-create.py' to generate context nodes"
    ]
  }
}
```

**Key Sections:**

- **navigation** - Entry points, directories, ignore patterns
- **exploration_hints** - Where to start, how to traverse
- **agent_instructions** - Project-specific AI instructions

:::info
**Note:** The `.aiagent.json` file is the first place to look for project-specific guidance and configuration.
:::

---

## Backend Navigation Guide

### Backend Architecture Overview

The Levelith backend follows a **layered architecture** pattern with comprehensive documentation at all levels:

```
backend/
├── API_DOCUMENTATION.md        # Complete API design specification
├── models/                     # Domain Layer
│   ├── user.py                 # User model with authentication
│   └── experience.py           # Experience + 9 subtypes
├── repositories/               # Data Access Layer
│   ├── user_repository.py      # User CRUD operations
│   └── experience_repository.py # Experience CRUD operations
├── services/                   # Business Logic Layer
│   ├── user_service.py         # User business logic
│   └── experience_service.py   # Experience business logic
└── api/                        # API Layer (to be implemented)
```

### Exploring the Backend

<details>
<summary><strong>Step 1: Understand the Domain Models</strong></summary>

```bash
# Analyze User model
python dev/aiagent_navigator.py analyze backend/models/user.py

# Analyze Experience model (includes 9 subtypes)
python dev/aiagent_navigator.py analyze backend/models/experience.py
```

**Key concepts:**
- **User**: Authentication, profile management, experience array
- **Experience**: 9 subtypes across 3 categories (Education, Workplace, Skills)
- **NAICS codes**: Every experience has a NAICS code (fallback: 123456)

</details>

<details>
<summary><strong>Step 2: Review Repository Layer</strong></summary>

```bash
# UserRepository - data access for users
python dev/aiagent_navigator.py analyze backend/repositories/user_repository.py

# ExperienceRepository - data access with NAICS indexing
python dev/aiagent_navigator.py analyze backend/repositories/experience_repository.py
```

**Repository pattern provides:**
- Data persistence abstraction
- Indexing for fast queries
- Search and filtering capabilities
- Clean separation from business logic

</details>

<details>
<summary><strong>Step 3: Understand Service Layer</strong></summary>

```bash
# UserService - registration, authentication, profiles
python dev/aiagent_navigator.py analyze backend/services/user_service.py

# ExperienceService - all 9 experience types
python dev/aiagent_navigator.py analyze backend/services/experience_service.py
```

**Services handle:**
- Business logic and validation
- NAICS code validation and fallback
- User-experience relationship management
- Orchestration across repositories

</details>

<details>
<summary><strong>Step 4: Read API Documentation</strong></summary>

```bash
# Complete API design (endpoints, auth, errors, etc.)
cat backend/API_DOCUMENTATION.md
```

**API documentation includes:**
- All REST endpoints (design phase)
- JWT authentication flow
- Request/response schemas
- Error handling patterns
- NAICS code reference
- Pagination and filtering
- Rate limiting rules

</details>

### Backend Quick Reference

**Key Files:**
- `backend/API_DOCUMENTATION.md` - Complete API design
- `backend/models/user.py` - User domain model
- `backend/models/experience.py` - Experience models
- `backend/repositories/user_repository.py` - User data access
- `backend/repositories/experience_repository.py` - Experience data access
- `backend/services/user_service.py` - User business logic
- `backend/services/experience_service.py` - Experience business logic

**Experience Types (9 total):**
- **Education**: Certificate, Degree, Course
- **Workplace**: Gig, PartTime, FullTime
- **Skills**: SoftSkill, HardSkill, NativeSkill

**Architecture Pattern:**
```
API Endpoints → Services → Repositories → Data Store
```

### Backend Development Workflow

When working on backend code:

1. **Read the domain models** to understand data structures
2. **Check repositories** for available data operations
3. **Review services** for business logic patterns
4. **Consult API docs** for endpoint design
5. **Run tests** to verify functionality:
   ```bash
   pytest tests/test_user*.py tests/test_experience*.py -v
   ```

---

## Learning Path for AI Agents

### Level 1: Quick Start (5 minutes)

```bash
# Get exploration plan
python dev/aiagent_navigator.py plan

# Read suggested files
cat README.md
cat .aiagent.json

# Generate guide
python dev/aiagent_navigator.py guide
cat NAVIGATION.md
```

### Level 2: Deep Dive (15 minutes)

```bash
# Build full index
python dev/aiagent_navigator.py index

# Analyze key modules
python dev/aiagent_navigator.py analyze dev/aiagent_navigator.py

# Explore relationships
python dev/aiagent_navigator.py related dev/aiagent_navigator.py

# Read actual code
cat dev/aiagent_navigator.py
```

### Level 3: Expert Usage (30+ minutes)

```python
# Programmatic access
from dev.aiagent_navigator import AIAgentNavigator, AIAgentQueryInterface

# Custom analysis
nav = AIAgentNavigator()
plan = nav.get_exploration_plan()

for module in plan['key_modules']:
    context = nav.get_module_context(module['path'])
    related = nav.suggest_related_files(module['path'])
    # Deep analysis...

# Query interface
query = AIAgentQueryInterface()
overview = query.get_complexity_overview()

# Custom queries
for filepath, info in nav.index.items():
    if info['complexity_score'] > 20:
        # Analyze complex files
        pass
```

---

## Quick Reference

### Essential Commands

```bash
# Intelligent Tooling (Recommended)
python dev/aiagent_navigator.py plan      # Get exploration plan
python dev/aiagent_navigator.py index     # Build codebase index
python dev/aiagent_navigator.py guide     # Generate navigation guide
python dev/aiagent_navigator.py analyze <file>  # Analyze specific file
python dev/aiagent_navigator.py related <file>  # Find related files

# Context Nodes (Legacy)
python dev/cn-create.py                   # Generate context nodes
python dev/cn-validate.py                 # Validate context nodes
```

### Essential Files to Read

1. **[AI_AGENT_GUIDE.md](/docs/core/AI_AGENT_GUIDE.md)** - Complete learning guide
2. **README.md** - Project overview
3. **.aiagent.json** - Configuration and hints
4. **NAVIGATION.md** - Auto-generated navigation guide
5. **[COMPARISON.md](/docs/COMPARISON.md)** - System comparison

---

## Benefits

### Intelligent AI Agent Tooling

- ✅ **Consistent Structure**: Predictable API and output
- ✅ **Always Current**: Generated from actual code
- ✅ **Zero Maintenance**: Automated regeneration
- ✅ **Query Interface**: Ask specific questions
- ✅ **Fast**: Rebuild in seconds
- ✅ **AI-Optimized**: Designed for LLM comprehension

### Context Node System

- ✅ **Human Commentary**: Add insights beyond code
- ✅ **Explicit Structure**: Documented relationships
- ✅ **Hierarchical Understanding**: Natural tree traversal
- ✅ **AI Agent Notes**: Special handling instructions
- ✅ **Self-Documenting**: Structure conveys organization

### Combined Approach

- ✅ **Automated + Human**: Best of both worlds
- ✅ **Fast + Insightful**: Speed with depth
- ✅ **Current + Contextual**: Accurate with commentary

---

## Next Steps

### For AI Agents New to This Codebase

1. **Read this file** (you're doing it!)
2. **Run**: `python dev/aiagent_navigator.py plan`
3. **Read**: [AI_AGENT_GUIDE.md](/docs/core/AI_AGENT_GUIDE.md)
4. **Follow**: The exploration plan
5. **Query**: Use the navigator as needed

### For AI Agents Already Familiar

- **Rebuild index** after code changes: `python dev/aiagent_navigator.py index`
- **Check updates**: `cat NAVIGATION.md`
- **Query as needed**: Use `AIAgentQueryInterface` for specific questions

---

## Philosophy

**AI Agents as First-Class Citizens**

This repository treats you not as an afterthought, but as a primary user:

1. ✅ **Self-Documenting** - Code structure is discoverable
2. ✅ **Query-Driven** - Ask questions, get answers
3. ✅ **Always Current** - Generated from actual code, not stale docs
4. ✅ **Low Overhead** - Minimal burden on developers
5. ✅ **Intelligent** - Smart suggestions and relationship detection

**Two Paths to Understanding**

- **Fast Path**: Use intelligent tooling for immediate, accurate analysis
- **Deep Path**: Combine tooling with context nodes for human insights

**Choose Your Approach**

- **New codebase?** Start with intelligent tooling
- **Need human context?** Check for context nodes
- **Want both?** Use hybrid approach

:::success
**Success Tip:** The intelligent tooling approach will get you productive fastest while maintaining accuracy.
:::

---

## Additional Resources

### Official Documentation

- 📚 [AI Agent Learning Guide](/docs/core/AI_AGENT_GUIDE.md)
- 🏗️ [AI Agent Tooling Technical Docs](/docs/dev/AI_AGENT_TOOLING.md)
- 🧪 [System Comparison](/docs/COMPARISON.md)
- 🚀 [Render Deployment Guide](/docs/RENDER_DEPLOYMENT.md)

### Code Examples

- 💻 [Example AI Agent Usage](https://github.com/Free-Columns/levelith-2/blob/main/dev/example_ai_agent_usage.py)
- 🎯 [Backend Examples](https://github.com/Free-Columns/levelith-2/tree/main/backend)

### External Resources

- 🌐 [FastAPI Documentation](https://fastapi.tiangolo.com/)
- 📖 [Render Documentation](https://render.com/docs)
- 🐘 [PostgreSQL Documentation](https://www.postgresql.org/docs/)

### Community

- 💬 [Discord: #ai-agents](https://discord.gg/levelith)
- 🐛 [Report Issues](https://github.com/Free-Columns/levelith-2/issues)
- ❓ [GitHub Discussions](https://github.com/Free-Columns/levelith-2/discussions)

---

## Related Documentation

- **Previous:** [AI Agent Learning and Operating Guide](/docs/core/AI_AGENT_GUIDE.md)
- **Next:** [AI Agent Tooling Technical Documentation](/docs/dev/AI_AGENT_TOOLING.md)

**Other related documentation:**

- [System Comparison: Intelligent Tooling vs Context Nodes](/docs/COMPARISON.md)
- [Backend API Documentation](/docs/backend/API_DOCUMENTATION.md)
- [Render Deployment Guide](/docs/RENDER_DEPLOYMENT.md)
- [NAICS Implementation Summary](/docs/NAICS_EXPANSION_SUMMARY.md)

---

## Feedback

Found an issue with this guide? Have suggestions for improvement?

- 👍 **Helpful?** Give us feedback via GitHub reactions
- 🐛 **Found a bug?** [Report it on GitHub](https://github.com/Free-Columns/levelith-2/issues)
- 💡 **Have an idea?** [Start a discussion](https://github.com/Free-Columns/levelith-2/discussions)

---

**Last Updated:** November 19, 2025 | **Version:** 2.0 | **Contributors:** Semour Media Group

---

*This document is part of the Levelith Developer Documentation. For questions, join our [Discord community](https://discord.gg/levelith).*
