# AI Agent Golden Rules

---
title: "AI Agent Golden Rules"
description: "Mandatory development rules that all AI agents must follow when working with the Levelith codebase. Defines 10 core principles for code quality, maintainability, and scalability."
category: "reference"
tags: ["ai-agents", "development-rules", "code-quality", "testing", "security"]
author: "Semour Media Group"
date: "2025-01-17"
lastUpdated: "2025-11-19"
difficulty: "advanced"
readingTime: 15
relatedPages:
  - "/docs/core/AI_AGENT_GUIDE.md"
  - "/docs/core/MANIFEST.md"
  - "/docs/dev/AI_AGENT_TOOLING.md"
nextPage: "/docs/core/AI_AGENT_GUIDE.md"
prevPage: "/docs/core/MANIFEST.md"
searchKeywords:
  - "golden rules"
  - "ai agent development"
  - "code standards"
  - "testing requirements"
  - "security guidelines"
showTOC: true
showBreadcrumbs: true
showLastUpdated: true
version: "1.0"
---

# AI Agent Golden Rules

> **TL;DR:** These 10 mandatory rules define code quality standards for AI agents: test-first development (≥80% coverage), comprehensive documentation, security-first design, AI index maintenance, quality standards, dependency management, performance awareness, scalability by design, error handling, and version control hygiene. No exceptions permitted.

**Difficulty:** 🔴 Advanced | **Time:** ⏱️ 15 minutes | **Last Updated:** November 19, 2025

---

## Table of Contents

- [Overview](#overview)
- [Core Golden Rules](#core-golden-rules)
  - [Rule 1: Test-First Development](#rule-1-test-first-development-mandatory)
  - [Rule 2: Documentation is Non-Negotiable](#rule-2-documentation-is-non-negotiable)
  - [Rule 3: Security First](#rule-3-security-first)
  - [Rule 4: Maintain the AI Agent Index](#rule-4-maintain-the-ai-agent-index)
  - [Rule 5: Code Quality Standards](#rule-5-code-quality-standards)
  - [Rule 6: Dependency Management](#rule-6-dependency-management)
  - [Rule 7: Performance Awareness](#rule-7-performance-awareness)
  - [Rule 8: Scalability by Design](#rule-8-scalability-by-design)
  - [Rule 9: Error Handling and Logging](#rule-9-error-handling-and-logging)
  - [Rule 10: Version Control Hygiene](#rule-10-version-control-hygiene)
- [Enforcement Mechanisms](#enforcement-mechanisms)
- [Quick Reference for AI Agents](#quick-reference-for-ai-agents)
- [Additional Resources](#additional-resources)

---

## Overview

**CRITICAL: These rules MUST be followed for every action. No exceptions.**

This document defines the core principles that AI agents must follow when working with this codebase. These rules ensure code quality, maintainability, and scalability.

:::danger
**Critical:** All AI agents must read and follow these golden rules before making ANY code changes. Violations will result in commit rejection, CI/CD failures, and code review rejections.
:::

### Why These Rules Exist

1. **Quality**: High standards produce reliable software
2. **Maintainability**: Future developers (AI and human) understand the code
3. **Scalability**: Code grows without technical debt
4. **Security**: Vulnerabilities are prevented, not patched
5. **Collaboration**: AI agents work effectively with humans
6. **Sustainability**: Codebase remains healthy long-term

---

## Core Golden Rules

### Rule 1: Test-First Development (MANDATORY)

**Every code change MUST include tests.**

```python
# ❌ WRONG - Code without tests
def new_feature():
    return "implementation"

# ✅ CORRECT - Code with tests
def new_feature():
    return "implementation"

# tests/test_new_feature.py
def test_new_feature():
    assert new_feature() == "implementation"
```

#### Requirements

- ✅ **Unit tests** for all functions and classes
- ✅ **Integration tests** for cross-component features
- ✅ **Minimum 80% code coverage** (non-negotiable)
- ✅ **Tests must pass** before committing

#### Enforcement

```bash
# Generate test template
python tests/test_system.py generate <module_path>

# Validate before commit
python tests/test_system.py enforce
```

:::warning
**Consequences of violation:**
- Commit will be rejected
- CI/CD pipeline will fail
- Code review will request changes
:::

---

### Rule 2: Documentation is Non-Negotiable

**Every module, class, and function MUST have docstrings.**

```python
# ❌ WRONG - No documentation
def process_data(data):
    return data.transform()

# ✅ CORRECT - Complete documentation
def process_data(data: dict) -> dict:
    """
    Process raw data and transform it for storage.

    Args:
        data: Raw data dictionary with 'values' key

    Returns:
        Transformed data ready for storage

    Raises:
        ValueError: If data is missing required keys

    Example:
        >>> process_data({'values': [1, 2, 3]})
        {'processed': [1, 2, 3], 'timestamp': ...}
    """
    return data.transform()
```

#### Requirements

- ✅ **Module-level docstring** explaining purpose
- ✅ **Class docstrings** with attributes and usage
- ✅ **Function docstrings** with Args/Returns/Raises
- ✅ **Type hints** for all parameters and returns
- ✅ **Examples** for complex functions

:::info
**Note:** AI agents automatically extract docstrings for navigation.
:::

---

### Rule 3: Security First

**Never introduce security vulnerabilities.**

#### Common Vulnerabilities to Avoid

```python
# ❌ WRONG - SQL Injection
query = f"SELECT * FROM users WHERE id = {user_id}"

# ✅ CORRECT - Parameterized query
query = "SELECT * FROM users WHERE id = ?"
cursor.execute(query, (user_id,))

# ❌ WRONG - Command injection
os.system(f"process {user_input}")

# ✅ CORRECT - Safe execution
subprocess.run(["process", user_input], check=True)

# ❌ WRONG - Hardcoded secrets
API_KEY = "sk-1234567890abcdef"

# ✅ CORRECT - Environment variables
API_KEY = os.getenv("API_KEY")
```

#### Security Checklist

- ✅ No hardcoded secrets or credentials
- ✅ Validate and sanitize all inputs
- ✅ Use parameterized queries for databases
- ✅ Avoid dangerous functions (eval, exec, os.system)
- ✅ Implement proper authentication/authorization
- ✅ Use secure random for cryptography
- ✅ Keep dependencies updated
- ✅ Follow OWASP Top 10 guidelines

#### Security Scanning Tools

```bash
# Run security scan
bandit -r . -f json
safety check
```

---

### Rule 4: Maintain the AI Agent Index

**Always update the AI agent index after code changes.**

```bash
# After any code modification
python dev/aiagent_navigator.py index
python dev/aiagent_navigator.py guide
```

#### Why This Matters

- AI agents rely on the index for navigation
- Stale index = incorrect understanding
- Fresh index = accurate code comprehension

#### Quick Workflow

```bash
# Recommended workflow
git add <files>
python dev/aiagent_navigator.py index  # Update index
git commit -m "message"
```

:::tip
**Pro Tip:** The index is automatically updated in CI/CD, but keeping it fresh during local development helps catch issues earlier.
:::

---

### Rule 5: Code Quality Standards

**Write clean, maintainable, production-ready code.**

#### Code Examples

```python
# ✅ Meaningful names
def calculate_total_revenue(transactions: List[Transaction]) -> Decimal:
    """Calculate total revenue from transactions"""
    pass

# ❌ Unclear names
def calc(t):
    pass

# ✅ Small, focused functions
def validate_email(email: str) -> bool:
    """Validate email format"""
    return EMAIL_REGEX.match(email) is not None

def validate_age(age: int) -> bool:
    """Validate age is within valid range"""
    return 0 <= age <= 150

# ❌ God function
def validate(data):
    # 500 lines of validation logic
    pass

# ✅ Clear error handling
try:
    result = risky_operation()
except ValueError as e:
    logger.error(f"Invalid value: {e}")
    raise
except Exception as e:
    logger.exception("Unexpected error")
    raise

# ❌ Silent failures
try:
    risky_operation()
except:
    pass
```

#### Quality Checklist

- ✅ Functions < 50 lines
- ✅ Classes < 300 lines
- ✅ Cyclomatic complexity < 10
- ✅ No duplicated code
- ✅ Clear variable names
- ✅ Consistent formatting (use black/prettier)
- ✅ No commented-out code
- ✅ Proper error handling

#### Quality Tools

```bash
# Python
black .
flake8 .
mypy .
pylint .

# JavaScript
prettier --write .
eslint --fix .
```

---

### Rule 6: Dependency Management

**Keep dependencies minimal, updated, and documented.**

```toml
# pyproject.toml or requirements.txt
# ✅ CORRECT - Pinned versions with comments
requests==2.31.0  # HTTP library for API calls
pydantic==2.5.0   # Data validation

# ❌ WRONG - Unpinned versions
requests
pydantic
```

#### Dependency Rules

- ✅ Pin exact versions
- ✅ Document why each dependency is needed
- ✅ Regular security updates
- ✅ Remove unused dependencies
- ✅ Use virtual environments
- ✅ Check for vulnerabilities

#### Dependency Workflow

```bash
# Check for updates
pip list --outdated

# Security audit
safety check
npm audit

# Update safely
pip install --upgrade <package>
```

---

### Rule 7: Performance Awareness

**Write efficient code. Optimize when necessary.**

```python
# ❌ WRONG - N+1 query problem
for user in users:
    user.orders = db.query(Order).filter_by(user_id=user.id).all()

# ✅ CORRECT - Single query
users_with_orders = db.query(User).options(joinedload(User.orders)).all()

# ❌ WRONG - Inefficient algorithm
def find_duplicates(items):
    duplicates = []
    for i, item in enumerate(items):
        for j in range(i + 1, len(items)):  # O(n²)
            if items[i] == items[j]:
                duplicates.append(item)
    return duplicates

# ✅ CORRECT - Efficient algorithm
def find_duplicates(items):
    seen = set()
    duplicates = set()
    for item in items:  # O(n)
        if item in seen:
            duplicates.add(item)
        seen.add(item)
    return list(duplicates)
```

#### Performance Checklist

- ✅ Use appropriate data structures
- ✅ Avoid N+1 queries
- ✅ Cache expensive operations
- ✅ Use lazy loading when appropriate
- ✅ Profile before optimizing
- ✅ Set timeouts for external calls
- ✅ Use async for I/O-bound operations

---

### Rule 8: Scalability by Design

**Design for growth from day one.**

```python
# ✅ Configurable limits
MAX_BATCH_SIZE = int(os.getenv("MAX_BATCH_SIZE", "1000"))

# ✅ Pagination
def get_items(page: int = 1, page_size: int = 50):
    offset = (page - 1) * page_size
    return db.query(Item).offset(offset).limit(page_size).all()

# ✅ Rate limiting
@rate_limit(requests=100, period=60)
def api_endpoint():
    pass

# ✅ Resource cleanup
with open("file.txt") as f:
    process(f)  # File automatically closed

# ✅ Horizontal scaling considerations
# Use stateless design
# Externalize session storage
# Design for multiple instances
```

#### Scalability Checklist

- ✅ Stateless architecture
- ✅ Pagination for large datasets
- ✅ Rate limiting on APIs
- ✅ Configurable resource limits
- ✅ Database connection pooling
- ✅ Caching strategy
- ✅ Async/queue for long tasks

---

### Rule 9: Error Handling and Logging

**Fail gracefully. Log comprehensively.**

```python
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# ✅ CORRECT - Comprehensive error handling
def process_user_data(user_id: str) -> Optional[dict]:
    """
    Process user data with proper error handling.

    Args:
        user_id: User identifier

    Returns:
        Processed data or None if error
    """
    try:
        logger.info(f"Processing user {user_id}")
        user = fetch_user(user_id)

        if not user:
            logger.warning(f"User {user_id} not found")
            return None

        result = transform_data(user)
        logger.info(f"Successfully processed user {user_id}")
        return result

    except ValidationError as e:
        logger.error(f"Validation failed for user {user_id}: {e}")
        raise

    except DatabaseError as e:
        logger.exception(f"Database error processing user {user_id}")
        # Maybe retry logic here
        raise

    except Exception as e:
        logger.exception(f"Unexpected error processing user {user_id}")
        raise

# ❌ WRONG - Silent failures and poor logging
def process_user_data(user_id):
    try:
        user = fetch_user(user_id)
        return transform_data(user)
    except:
        return None
```

#### Logging Levels

| Level | Use Case |
|-------|----------|
| **DEBUG** | Detailed diagnostic information |
| **INFO** | General informational messages |
| **WARNING** | Warning messages for recoverable issues |
| **ERROR** | Error messages for failures |
| **CRITICAL** | Critical issues requiring immediate attention |

#### What to Log

- ✅ Application startup/shutdown
- ✅ Configuration loaded
- ✅ User actions (with privacy consideration)
- ✅ External API calls
- ✅ Database queries (in debug mode)
- ✅ Errors with context
- ✅ Performance metrics
- ❌ Sensitive data (passwords, tokens, PII)

---

### Rule 10: Version Control Hygiene

**Make meaningful commits with clear messages.**

```bash
# ✅ CORRECT - Clear, descriptive commits
git commit -m "Add user authentication with JWT

Implemented:
- JWT token generation and validation
- Login/logout endpoints
- Password hashing with bcrypt
- Token refresh mechanism

Tests: tests/test_auth.py
Coverage: 95%
Closes: #123"

# ❌ WRONG - Vague commits
git commit -m "fix stuff"
git commit -m "wip"
git commit -m "updates"
```

#### Commit Message Format

```
<type>: <subject>

<body>

<footer>
```

#### Commit Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **test**: Adding/updating tests
- **refactor**: Code refactoring
- **perf**: Performance improvements
- **chore**: Maintenance tasks

#### Commit Checklist

- ✅ One logical change per commit
- ✅ Tests pass
- ✅ Code formatted
- ✅ No debugging code
- ✅ No sensitive data
- ✅ AI agent index updated

---

## Enforcement Mechanisms

### Pre-Commit Hooks

```bash
# Install pre-commit hooks
pip install pre-commit
pre-commit install

# .pre-commit-config.yaml includes:
# - Test enforcement
# - Code formatting
# - Security scanning
# - AI agent index update
```

### CI/CD Pipeline

All golden rules are enforced in CI/CD:

```yaml
# .github/workflows/enforce-golden-rules.yml
- name: Enforce test coverage
  run: pytest --cov-fail-under=80

- name: Security scan
  run: bandit -r . && safety check

- name: Code quality
  run: flake8 . && mypy .

- name: Update AI index
  run: python dev/aiagent_navigator.py index
```

### Code Review Checklist

Reviewers must verify:
- ✅ Tests included and passing
- ✅ Documentation complete
- ✅ No security vulnerabilities
- ✅ AI agent index updated
- ✅ Code quality standards met
- ✅ Performance considerations addressed

---

## Quick Reference for AI Agents

**Before making ANY code change:**

1. ✅ Generate test template: `python tests/test_system.py generate <file>`
2. ✅ Write tests FIRST
3. ✅ Implement feature
4. ✅ Run tests: `pytest`
5. ✅ Update AI index: `python dev/aiagent_navigator.py index`
6. ✅ Format code: `black .` or `prettier --write .`
7. ✅ Security scan: `bandit -r .`
8. ✅ Commit with clear message

### Command Sequence

```bash
# 1. Generate test
python tests/test_system.py generate dev/new_module.py

# 2. Implement & test
pytest tests/test_new_module.py -v

# 3. Update index
python dev/aiagent_navigator.py index

# 4. Format
black .

# 5. Final check
pytest
python tests/test_system.py enforce

# 6. Commit
git add .
git commit -m "feat: Add new module with tests"
```

---

## Consequences of Rule Violations

| Violation | Consequence |
|-----------|-------------|
| No tests | Commit rejected, CI fails |
| No documentation | Code review rejection |
| Security issue | Immediate fix required, deployment blocked |
| Outdated AI index | Navigation confusion, review rejection |
| Poor code quality | Refactoring required |
| Bad dependencies | Security vulnerability, update required |
| Performance issues | Optimization required before merge |
| No error handling | Code review rejection |
| Bad commits | Rewrite commit history |

---

## Best Practices

### ✅ DO

1. **Read these rules before every task** - Keep them fresh in memory
2. **Run tests frequently** - Catch issues early
3. **Update documentation as you code** - Don't leave it for later
4. **Ask questions when uncertain** - Better to clarify than assume

### ❌ DON'T

1. **Skip tests to save time** - Technical debt compounds quickly
2. **Copy-paste code without understanding** - Leads to bugs and security issues
3. **Ignore security warnings** - They exist for a reason
4. **Commit broken code** - Breaks CI/CD and team workflow

---

## Additional Resources

### Official Documentation

- 📚 [AI Agent Guide](/docs/core/AI_AGENT_GUIDE.md) - Complete operating guide
- 🏗️ [MANIFEST](/docs/core/MANIFEST.md) - Project vision and architecture
- 🧪 [AI Agent Tooling](/docs/dev/AI_AGENT_TOOLING.md) - Technical navigation system

### External Resources

- 🌐 [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- 📖 [Python Type Hints](https://docs.python.org/3/library/typing.html)
- 📊 [Conventional Commits](https://www.conventionalcommits.org/)

### Code Examples

- 💻 [Test Examples](https://github.com/Free-Columns/levelith-2/tree/main/tests)
- 🎯 [Service Layer Examples](https://github.com/Free-Columns/levelith-2/tree/main/backend/services)

---

## Related Documentation

- **Previous:** [MANIFEST - Project Vision](/docs/core/MANIFEST.md)
- **Next:** [AI Agent Guide](/docs/core/AI_AGENT_GUIDE.md)

**Other related documentation:**

- [Codebase Analysis](/docs/dev/CODEBASE_ANALYSIS.md)
- [Development Priorities](/docs/dev/DEVELOPMENT_PRIORITIES.md)
- [Known Issues](/docs/core/KNOWN_ISSUES.md)

---

## Feedback

Found an issue with this guide? Have suggestions for improvement?

- 👍 **Helpful?** These rules help maintain code quality
- 🐛 **Found a bug?** [Report it on GitHub](https://github.com/Free-Columns/levelith-2/issues)
- 💡 **Have an idea?** [Start a discussion](https://github.com/Free-Columns/levelith-2/discussions)

---

**Last Updated:** November 19, 2025 | **Version:** 1.0 | **Contributors:** Semour Media Group

---

> "Every AI agent is responsible for maintaining code quality. No exceptions. No shortcuts. No technical debt."

*This document is part of the Levelith Developer Documentation. For questions, join our [Discord community](https://discord.gg/levelith).*
