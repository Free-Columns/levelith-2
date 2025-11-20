# Levelith-2 – Unified Navigation & Updates Guide ✅

**Date:** November 19–20, 2025  
**Version:** 2.1  
**Maintained By:** Semour Media Group  

---

## 📌 Table of Contents

1. [Executive Summary](#executive-summary)  
2. [Entry Points](#entry-points)  
3. [Key Modules](#key-modules)  
4. [Complexity Hotspots](#complexity-hotspots)  
5. [Backend Status](#backend-status)  
6. [Development Tools](#development-tools)  
7. [Navigation Systems](#navigation-systems)  
8. [Intelligent AI Agent Tooling](#intelligent-ai-agent-tooling)  
9. [Context Node System](#context-node-system)  
10. [Configuration](#configuration)  
11. [Backend Navigation Guide](#backend-navigation-guide)  
12. [Learning Path for AI Agents](#learning-path-for-ai-agents)  
13. [Quick Reference](#quick-reference)  
14. [Benefits](#benefits)  
15. [Recent Updates](#recent-updates)  
16. [Additional Resources](#additional-resources)  

---

## 1. Executive Summary

Levelith-2 is designed with **AI agents as first-class citizens**. Navigation is supported by two systems:

- **Intelligent AI Agent Tooling v2.0** – automated, always current, query-driven.  
- **Context Node System (legacy)** – manual, human commentary, higher maintenance.  

Recent updates include completion of the **Users feature**, a **global API transformation layer**, NAICS CRUD operations, admin dashboard fixes, and styling enforcement.

---

## 2. Entry Points

- `/home/user/levelith-2/dev/aiagent_navigator.py`  
- `/home/user/levelith-2/tests/test_system.py`  

---

## 3. Key Modules

### `dev/aiagent_navigator.py`
- **Exports:** ModuleInfo, Understanding, ExplorationMetrics, AIAgentNavigator, GoalOrientedExplorer, NaturalLanguageQuery, PerformanceNavigator, CognitiveLoadManager, MetricsCollector, InteractiveLearning, CollaborativeSession, KnowledgeExporter, KnowledgeImporter, BugInvestigator, FeaturePlanner, ReviewAssistant, UnderstandingValidator, AnalyticsDashboard, ContextOptimizer, main  
- **Complexity:** 70  
- **Description:** AI Agent Intelligent Navigator v2.0  

### `tests/test_aiagent_navigator_v2.py`
- **Exports:** Test suites for Navigator v2.0 features (Quickstart, Goal-Oriented, Natural Language, Performance, Error Handling, CLI).  
- **Complexity:** 49  

### `backend/models/experience.py`
- **Exports:** ExperienceCategory, ExperienceType, Experience, Certificate, Degree, Course, Gig, PartTime, FullTime, SoftSkill, HardSkill, NativeSkill, validate_naics_code  
- **Complexity:** 42  

### `backend/models/db_models.py`
- **Exports:** UserDB, ExperienceDB, CertificateDB, DegreeDB, CourseDB, GigDB, PartTimeDB, FullTimeDB, SoftSkillDB, HardSkillDB, NativeSkillDB  
- **Complexity:** 40  

### `backend/api/routes/naics.py`
- **Exports:** NAICSCodeResponse, NAICSValidationResponse, NAICSSearchResponse, NAICSSuggestionResponse, NAICSCategorySummary, Config, _naics_to_response  
- **Complexity:** 29  

### Test Suites
- `tests/test_api_naics.py` – NAICS API endpoints (complexity 42).  
- `tests/test_naics_service.py` – NAICS service logic (complexity 41).  
- `tests/test_naics_repository.py` – Repository layer (complexity 39).  
- `tests/test_experience.py` – Experience model/unit tests (complexity 39).  
- `tests/test_api_experiences.py` – Experience CRUD endpoints (complexity 32).  

---

## 4. Complexity Hotspots

Files requiring careful attention:

- `dev/aiagent_navigator.py` (70)  
- `tests/test_aiagent_navigator_v2.py` (49)  
- `backend/models/experience.py` (42)  
- `tests/test_api_naics.py` (42)  
- `tests/test_naics_service.py` (41)  
- `backend/models/db_models.py` (40)  
- `tests/test_naics_repository.py` (39)  
- `tests/test_experience.py` (39)  
- `tests/test_api_experiences.py` (32)  
- `backend/api/routes/naics.py` (29)  

---

## 5. Backend Status

- **Framework:** FastAPI 0.109.0  
- **Database:** PostgreSQL (Render Managed)  
- **ORM:** SQLAlchemy 2.0.25  
- **Validation:** Pydantic 2.10.4  
- **Deployment:** Render Web Service via `render.yaml`  
- **Production Ready:** ✅  

---

## 6. Development Tools

- **Color Visualizer:** `tools/color-visualizer.html` – interactive ONETRUTH theme editor.  
- **Features:** RGB/HSL/Hex controls, export options, gamification colors, NAICS industry palettes.  

---

## 7. Navigation Systems

| System | Type | Best For | Maintenance |
|--------|------|----------|-------------|
| Intelligent Tooling | Dynamic | Active development | Automated |
| Context Nodes | Static | Human commentary | Manual |

---

## 8. Intelligent AI Agent Tooling

- **Features:** Quickstart, exploration plan, natural language queries, relationship detection, performance navigator.  
- **Commands:**  
  - `python dev/aiagent_navigator.py quickstart`  
  - `python dev/aiagent_navigator.py plan`  
  - `python dev/aiagent_navigator.py index`  
  - `python dev/aiagent_navigator.py ask "question"`  
  - `python dev/aiagent_navigator.py guide`  

---

## 9. Context Node System

- **Static documentation system** with `.context-node.md` files.  
- **Limitations:** Manual maintenance, sync risk, storage overhead.  
- **Best Use:** Human commentary for stable codebases.  

---

## 10. Configuration

`.aiagent.json` defines entry points, exploration hints, and agent instructions.  

---

## 11. Backend Navigation Guide

Architecture pattern:  
```
API Endpoints → Services → Repositories → Data Store
```  

Key files:  
- `backend/models/user.py`  
- `backend/models/experience.py`  
- `backend/repositories/user_repository.py`  
- `backend/services/user_service.py`  
- `backend/services/experience_service.py`  

---

## 12. Learning Path for AI Agents

- **Level 1:** Quickstart (5 min) – run `plan`, read README, `.aiagent.json`.  
- **Level 2:** Deep Dive (15 min) – build index, analyze modules.  
- **Level 3:** Expert (30+ min) – programmatic queries, complexity analysis.  

---

## 13. Quick Reference

Essential commands:  
- `python dev/aiagent_navigator.py plan`  
- `python dev/aiagent_navigator.py index`  
- `python dev/aiagent_navigator.py guide`  
- `python dev/aiagent_navigator.py analyze <file>`  
- `python dev/aiagent_navigator.py related <file>`  

---

## 14. Benefits

- **Tooling:** Always current, automated, query-driven.  
- **Context Nodes:** Human commentary, explicit structure.  
- **Hybrid Approach:** Combine automation with human insights.  

---

## 15. Recent Updates

### Users Feature Complete
- **Global API Transformation Layer:** `frontend/src/lib/transformers.ts` (188 lines), 31 test cases.  
- **Admin Pages:** `UsersPage.tsx`, `UserDetailPage.tsx`.  
- **Routes:** `/admin/users`, `/admin/users/:id`.  
- **Docs:** `USERS_INTEGRATION_COMPLETE.md`, `BACKEND_CONNECTIVITY_TEST.md`.  

### Component Fixes
- **FormButton.jsx:** Created to resolve deployment failure. Variants: primary, secondary, danger.  

### NAICS CRUD
- **Backend:** Added admin fields (tags, custom_category, admin_notes).  
- **Frontend:** Complete CRUD UI with server-side pagination.  

### Admin Dashboard Fixes
- Removed hardcoded Tailwind classes, replaced with ONETRUTH dynamic styling.  
- Fixed filters in Experiences page.  

### API Endpoints Added
- `GET /api/v1/naics/paginated`  
- `PATCH /api/v1/naics/{code}`  
- `DELETE /api/v1/naics/{code}`  

### ONETRUTH Styling Enforcement
- All components now use ONETRUTH dynamic styling (no hardcoded CSS).  

### Previous Updates
- Fixed oversized icons, API/MOCK switch, added stats endpoint.  

---

## 16. Additional Resources

- 📚 [AI Agent Guide](/docs/core/AI_AGENT_GUIDE.md)  
- 🏗️ [AI Agent Tooling Docs](/docs/dev/AI_AGENT_TOOLING.md)  
-
