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

### `backend/models/db_models.py`
- **Reason**: 11 exports, complexity: 40
- **Exports**: UserDB, ExperienceDB, CertificateDB, DegreeDB, CourseDB, GigDB, PartTimeDB, FullTimeDB, SoftSkillDB, HardSkillDB, NativeSkillDB
- **Description**: SQLAlchemy ORM Models

Database models for User and Experience using SQLAlchemy ORM.
These models ma

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

### `backend/database.py`
- **Reason**: 7 exports, complexity: 23
- **Exports**: DatabaseHealthCheck, set_sqlite_pragma, get_db, get_db_context, init_db, drop_db, reset_db
- **Description**: Database Configuration and Session Management

Provides SQLAlchemy engine, session management, and b

### `backend/schemas/experience.py`
- **Reason**: 6 exports, complexity: 22
- **Exports**: ExperienceBase, ExperienceCreate, ExperienceUpdate, ExperienceResponse, ExperienceList, Config
- **Description**: Experience API Schemas

Pydantic models for experience-related API requests and responses.

### `tests/test_system.py`
- **Reason**: 5 exports, complexity: 21
- **Exports**: TestRequirement, TestGenerator, TestValidator, enforce_test_requirements, main
- **Description**: Levelith-2 Internal Test System

This module provides a comprehensive testing framework for all code

### `tests/test_test_system.py`
- **Reason**: 4 exports, complexity: 19
- **Exports**: TestTestRequirement, TestTestGenerator, TestTestValidator, TestTestSystemIntegration
- **Description**: Unit tests for the test system itself.

This demonstrates the test framework in action and validates

## Complexity Hotspots

- `backend/models/experience.py` (complexity: 42)
- `backend/models/db_models.py` (complexity: 40)
- `tests/test_experience.py` (complexity: 39)
- `tests/test_api_experiences.py` (complexity: 32)
- `tests/test_api_users.py` (complexity: 29)
- `backend/schemas/user.py` (complexity: 27)
- `backend/database.py` (complexity: 23)
- `backend/schemas/experience.py` (complexity: 22)
- `tests/test_system.py` (complexity: 21)
