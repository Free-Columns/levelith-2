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

### `tests/test_experience.py`
- **Reason**: 12 exports, complexity: 39
- **Exports**: TestNAICSValidation, TestExperience, TestCertificate, TestDegree, TestCourse, TestGig, TestPartTime, TestFullTime, TestSoftSkill, TestHardSkill, TestNativeSkill, TestExperienceIntegration
- **Description**: Unit tests for experience.py

Comprehensive tests for Experience model, all 9 experience subtypes, a

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

### `dev/aiagent_navigator.py`
- **Reason**: 3 exports, complexity: 16
- **Exports**: ModuleInfo, AIAgentNavigator, main
- **Description**: AI Agent Intelligent Navigator

This tool helps AI agents explore codebases efficiently by:
- Readin

### `tests/test_user.py`
- **Reason**: 4 exports, complexity: 15
- **Exports**: TestUser, TestPasswordFunctions, TestCreateUser, TestUserEdgeCases
- **Description**: Unit tests for user.py

Comprehensive tests for User model and authentication functions.
Tests follo

### `backend/models/user.py`
- **Reason**: 4 exports, complexity: 14
- **Exports**: User, hash_password, verify_password, create_user
- **Description**: User Domain Model

This module defines the User model for the Levelith application.
Users have usern

### `dev/test_report_generator.py`
- **Reason**: 4 exports, complexity: 13
- **Exports**: run_tests, parse_pytest_output, generate_markdown_report, main
- **Description**: Levelith-2 Test Report Generator

Generates comprehensive test execution reports with pass/fail stat

## Complexity Hotspots

- `backend/models/experience.py` (complexity: 42)
- `tests/test_experience.py` (complexity: 39)
- `tests/test_system.py` (complexity: 21)
