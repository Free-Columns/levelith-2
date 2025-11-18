# AI Agent Navigation Guide

*Auto-generated from codebase analysis*

## Entry Points

- `/home/user/levelith-2/dev/aiagent_navigator.py`
- `/home/user/levelith-2/tests/test_system.py`

## Key Modules

### `dev/aiagent_navigator.py`
- **Reason**: 20 exports, complexity: 70
- **Exports**: ModuleInfo, Understanding, ExplorationMetrics, AIAgentNavigator, GoalOrientedExplorer, NaturalLanguageQuery, PerformanceNavigator, CognitiveLoadManager, MetricsCollector, InteractiveLearning, CollaborativeSession, KnowledgeExporter, KnowledgeImporter, BugInvestigator, FeaturePlanner, ReviewAssistant, UnderstandingValidator, AnalyticsDashboard, ContextOptimizer, main
- **Description**: AI Agent Intelligent Navigator v2.0

This tool helps AI agents explore codebases efficiently by:
- R

### `tests/test_aiagent_navigator_v2.py`
- **Reason**: 14 exports, complexity: 49
- **Exports**: TestAIAgentNavigatorQuickstart, TestGoalOrientedExplorer, TestNaturalLanguageQuery, TestPerformanceNavigator, TestCognitiveLoadManager, TestMetricsCollector, TestInteractiveLearning, TestStubClasses, TestV2Integration, TestV2ErrorHandling, TestV2CLICommands, TestV2Performance, temp_codebase, navigator
- **Description**: Test suite for AI Agent Navigator v2.0 features.

Tests cover:
- QuickStart functionality
- GoalOrie

### `backend/models/experience.py`
- **Reason**: 13 exports, complexity: 42
- **Exports**: ExperienceCategory, ExperienceType, Experience, Certificate, Degree, Course, Gig, PartTime, FullTime, SoftSkill, HardSkill, NativeSkill, validate_naics_code
- **Description**: Experience Domain Models

This module defines the core Experience model and all its subtypes.
Accord

### `tests/test_api_naics.py`
- **Reason**: 13 exports, complexity: 42
- **Exports**: TestGetNAICSCode, TestValidateNAICSCode, TestSearchNAICSCodes, TestAutocompleteNAICS, TestSuggestForExperience, TestGetByCategory, TestGetByLevel, TestGetHierarchy, TestGetChildren, TestGetParent, TestCategoriesSummary, TestListCategories, TestAPIResponseFormat
- **Description**: Tests for NAICS API Endpoints

This module tests the NAICS REST API endpoints.

Test coverage includ

### `tests/test_naics_service.py`
- **Reason**: 13 exports, complexity: 41
- **Exports**: TestNAICSServiceInitialization, TestCodeLookup, TestCodeValidation, TestSearch, TestAutocomplete, TestExperienceSuggestions, TestCategoryOperations, TestLevelOperations, TestHierarchicalOperations, TestExperienceCategoryMapping, mock_repo, naics_service, sample_naics_code
- **Description**: Tests for NAICS Service

This module tests the NAICS service business logic layer.

Test coverage in

### `backend/models/db_models.py`
- **Reason**: 11 exports, complexity: 40
- **Exports**: UserDB, ExperienceDB, CertificateDB, DegreeDB, CourseDB, GigDB, PartTimeDB, FullTimeDB, SoftSkillDB, HardSkillDB, NativeSkillDB
- **Description**: SQLAlchemy ORM Models

Database models for User and Experience using SQLAlchemy ORM.
These models ma

### `tests/test_naics_repository.py`
- **Reason**: 12 exports, complexity: 39
- **Exports**: TestNAICSRepositoryInitialization, TestNAICSCodeLookup, TestCategoryFiltering, TestLevelFiltering, TestNAICSSearch, TestHierarchicalOperations, TestCodeValidation, TestRepositoryQueries, TestIndexConsistency, sample_naics_data, temp_naics_file, naics_repo
- **Description**: Tests for NAICS Repository

This module tests the NAICS repository data access layer.

Test coverage

### `tests/test_experience.py`
- **Reason**: 12 exports, complexity: 39
- **Exports**: TestNAICSValidation, TestExperience, TestCertificate, TestDegree, TestCourse, TestGig, TestPartTime, TestFullTime, TestSoftSkill, TestHardSkill, TestNativeSkill, TestExperienceIntegration
- **Description**: Unit tests for experience.py

Comprehensive tests for Experience model, all 9 experience subtypes, a

### `tests/test_api_experiences.py`
- **Reason**: 10 exports, complexity: 32
- **Exports**: TestExperienceCreation, TestExperienceRetrieval, TestExperienceUpdate, TestExperienceDeletion, TestExperienceSummary, override_get_db, setup_database, client, test_user, sample_experience_data
- **Description**: Unit tests for experience API endpoints

Comprehensive tests for experience CRUD operations via REST

### `backend/api/routes/naics.py`
- **Reason**: 8 exports, complexity: 29
- **Exports**: NAICSCodeResponse, NAICSValidationResponse, NAICSSearchResponse, NAICSSuggestionResponse, NAICSCategorySummary, Config, Config, _naics_to_response
- **Description**: NAICS Code API Endpoints

Provides endpoints for NAICS code lookups, search, validation, and suggest

## Complexity Hotspots

- `dev/aiagent_navigator.py` (complexity: 70)
- `tests/test_aiagent_navigator_v2.py` (complexity: 49)
- `backend/models/experience.py` (complexity: 42)
- `tests/test_api_naics.py` (complexity: 42)
- `tests/test_naics_service.py` (complexity: 41)
- `backend/models/db_models.py` (complexity: 40)
- `tests/test_naics_repository.py` (complexity: 39)
- `tests/test_experience.py` (complexity: 39)
- `tests/test_api_experiences.py` (complexity: 32)
- `backend/api/routes/naics.py` (complexity: 29)
- `tests/test_api_users.py` (complexity: 29)
- `backend/schemas/user.py` (complexity: 27)
- `tests/test_naics.py` (complexity: 27)
- `backend/database.py` (complexity: 23)
- `backend/schemas/experience.py` (complexity: 22)
- `backend/models/naics.py` (complexity: 21)
- `tests/test_system.py` (complexity: 21)
