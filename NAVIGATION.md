# AI Agent Navigation Guide

*Auto-generated from codebase analysis*

## Entry Points

- `/home/user/levelith-2/dev/aiagent_navigator.py`
- `/home/user/levelith-2/tests/test_system.py`

## Key Modules

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

### `tests/test_api_users.py`
- **Reason**: 9 exports, complexity: 29
- **Exports**: TestUserCreation, TestUserRetrieval, TestUserUpdate, TestUserDeletion, TestUserLogin, override_get_db, setup_database, client, sample_user_data
- **Description**: Unit tests for user API endpoints

Comprehensive tests for user CRUD operations via REST API.

### `backend/schemas/user.py`
- **Reason**: 8 exports, complexity: 27
- **Exports**: UserBase, UserCreate, UserUpdate, UserLogin, UserResponse, TokenResponse, UserWithExperiences, Config
- **Description**: User API Schemas

Pydantic models for user-related API requests and responses.

## Complexity Hotspots

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
