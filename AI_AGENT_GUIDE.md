# AI Agent Learning and Operating Guide

**Welcome, AI Agent!**

This guide teaches you how to efficiently explore, understand, and work with this codebase using intelligent tooling designed specifically for AI comprehension.

## Table of Contents

1. [First Steps](#first-steps)
2. [Understanding the Navigation System](#understanding-the-navigation-system)
3. [Exploration Workflow](#exploration-workflow)
4. [Common Tasks](#common-tasks)
5. [API Reference](#api-reference)
6. [Best Practices](#best-practices)
7. [Troubleshooting](#troubleshooting)
8. [Learning Path](#learning-path)

---

## First Steps

### What You're Looking At

This repository uses **Intelligent AI Agent Tooling** - a system that provides you with:

1. **Dynamic Code Analysis** - Information extracted directly from code
2. **Exploration Planning** - Smart suggestions for where to start
3. **Query Interface** - Ask specific questions, get immediate answers
4. **Relationship Mapping** - Understand how files connect
5. **Always Current** - Never outdated, generated from actual code

### Your First Command

```bash
python dev/aiagent_navigator.py plan
```

This gives you a complete exploration plan with:
- Suggested starting points
- Entry points to the codebase
- Key modules identified
- Dependency graph
- Complexity hotspots

**Example Output:**
```json
{
  "suggested_start": ["README.md", "claude.md"],
  "entry_points": ["/path/to/main.py"],
  "key_modules": [...],
  "dependency_graph": {...},
  "complexity_hotspots": [...]
}
```

---

## Understanding the Navigation System

### Architecture Overview

```
.aiagent.json           → Configuration (hints for you)
    ↓
aiagent_navigator.py    → Intelligence engine
    ↓
.aiagent-index.json     → Cached analysis (auto-generated)
    ↓
NAVIGATION.md           → Human-readable guide (auto-generated)
```

### Key Files

| File | Purpose | When to Use |
|------|---------|-------------|
| `.aiagent.json` | Configuration and hints | Read first to understand project-specific notes |
| `dev/aiagent_navigator.py` | Intelligence engine | Import for programmatic access |
| `.aiagent-index.json` | Cached codebase analysis | Load for fast queries |
| `NAVIGATION.md` | Human-readable guide | Quick overview of structure |
| `claude.md` | System overview | Understand navigation philosophy |

### What the Index Contains

For each Python file in the codebase, the index stores:

```json
{
  "path/to/file.py": {
    "docstring": "Module description from code",
    "classes": ["ClassName1", "ClassName2"],
    "functions": ["function_name1", "function_name2"],
    "imports": ["module1", "module2"],
    "exports": ["public_function", "PublicClass"],
    "complexity_score": 25
  }
}
```

This is **extracted from actual code** - always accurate, never stale.

---

## Exploration Workflow

### Step-by-Step: Understanding a New Codebase

#### Step 1: Load the Exploration Plan

```bash
python dev/aiagent_navigator.py plan
```

**What to look for:**
- `suggested_start` - Read these files first (usually README, architecture docs)
- `entry_points` - Main files where execution begins
- `key_modules` - Most important files by complexity/exports

#### Step 2: Read Suggested Starting Points

```bash
# Usually includes:
cat README.md
cat claude.md
cat .aiagent.json
```

**What you'll learn:**
- Project purpose and architecture
- Special conventions or patterns
- Project-specific AI agent instructions

#### Step 3: Analyze Key Modules

```bash
python dev/aiagent_navigator.py analyze dev/aiagent_navigator.py
```

**What you'll get:**
```json
{
  "docstring": "AI Agent Intelligent Navigator...",
  "classes": ["ModuleInfo", "AIAgentNavigator"],
  "functions": ["main"],
  "imports": ["json", "ast", "pathlib", ...],
  "exports": ["ModuleInfo", "AIAgentNavigator", "main"],
  "complexity_score": 16
}
```

#### Step 4: Explore Relationships

```bash
python dev/aiagent_navigator.py related dev/aiagent_navigator.py
```

**What you'll discover:**
- Files that import this module's exports
- Files that share common dependencies
- Strength of relationships (score)

#### Step 5: Dive Deep into Code

Now read the actual files with full context:
- You know what classes/functions to expect
- You understand the dependencies
- You know which other files to check next

### Visual Workflow

```
START
  ↓
Load Exploration Plan
  ↓
Read suggested_start files (README, etc.)
  ↓
Analyze entry_points
  ↓
For each key_module:
  ├─ Get module context
  ├─ Understand exports/imports
  └─ Find related files
  ↓
Read actual code with context
  ↓
COMPLETE UNDERSTANDING
```

---

## Common Tasks

### Task 1: Find Where a Function is Defined

**Using Python API:**
```python
from dev.aiagent_navigator import AIAgentQueryInterface

query = AIAgentQueryInterface()
results = query.where_is_function("authenticate_user")

# Returns: [{"file": "src/auth/login.py", "context": "...", ...}]
```

**Using CLI:**
```bash
# Build index first if not exists
python dev/aiagent_navigator.py index

# Then grep the index
cat .aiagent-index.json | grep -A5 "authenticate_user"
```

### Task 2: Find Where a Class is Defined

**Using Python API:**
```python
query = AIAgentQueryInterface()
results = query.where_is_class("UserAuth")

# Returns: [{"file": "src/auth/user.py", "context": "...", ...}]
```

**Manual Approach:**
```bash
# Search for class definitions
python dev/aiagent_navigator.py index
grep -r "class UserAuth" .
```

### Task 3: Find All Files That Import a Module

**Using Python API:**
```python
query = AIAgentQueryInterface()
results = query.what_imports_module("jwt")

# Returns: [{"file": "src/auth/login.py", "all_imports": [...]}, ...]
```

**What this tells you:**
- Which parts of the codebase depend on JWT
- Scope of changes if you modify JWT usage

### Task 4: Understand a File's Purpose

**Quick Check:**
```bash
python dev/aiagent_navigator.py analyze src/auth/login.py
```

**Get Full Context:**
```python
from dev.aiagent_navigator import AIAgentNavigator

nav = AIAgentNavigator()
context = nav.get_module_context("src/auth/login.py")

print(f"Purpose: {context['docstring']}")
print(f"Provides: {context['exports']}")
print(f"Depends on: {context['imports']}")
print(f"Complexity: {context['complexity_score']}")

# Then get related files
related = nav.suggest_related_files("src/auth/login.py")
```

### Task 5: Get Codebase Overview

**Quick Overview:**
```bash
python dev/aiagent_navigator.py guide
cat NAVIGATION.md
```

**Detailed Overview:**
```python
query = AIAgentQueryInterface()
overview = query.get_complexity_overview()

print(f"Total files: {overview['total_files']}")
print(f"Average complexity: {overview['average_complexity']}")
print(f"Hotspots: {overview['hotspots']}")
```

### Task 6: Rebuild Index After Code Changes

**After any code modifications:**
```bash
python dev/aiagent_navigator.py index
python dev/aiagent_navigator.py guide
```

**In CI/CD:**
This should happen automatically on every push.

---

## API Reference

### AIAgentNavigator Class

#### Methods

**`get_exploration_plan()`**
```python
plan = navigator.get_exploration_plan()
```
Returns comprehensive exploration strategy.

**`get_entry_points()`**
```python
entry_points = navigator.get_entry_points()
# Returns: ["/path/to/main.py", "/path/to/cli.py"]
```
Get recommended starting files.

**`get_module_context(filepath)`**
```python
context = navigator.get_module_context("src/auth/login.py")
# Returns: {docstring, classes, functions, imports, exports, complexity_score}
```
Get detailed information about a specific file.

**`suggest_related_files(filepath, max_suggestions=5)`**
```python
related = navigator.suggest_related_files("src/auth/login.py")
# Returns: [{"path": "...", "score": 10, "reason": "..."}, ...]
```
Find files related through imports/exports.

**`build_index()`**
```python
index = navigator.build_index()
# Analyzes entire codebase, returns index dict
```
Scan all files and build analysis index.

**`save_index(output_path=".aiagent-index.json")`**
```python
navigator.build_index()
navigator.save_index()
```
Save index to file for later use.

**`load_index(index_path=".aiagent-index.json")`**
```python
success = navigator.load_index()
# Returns: True if loaded, False if not found
```
Load previously saved index.

**`generate_navigation_guide(output_path="NAVIGATION.md")`**
```python
navigator.generate_navigation_guide()
# Creates human-readable markdown guide
```

### AIAgentQueryInterface Class

#### Methods

**`where_is_function(function_name)`**
```python
query = AIAgentQueryInterface()
results = query.where_is_function("authenticate_user")
```

**`where_is_class(class_name)`**
```python
results = query.where_is_class("UserAuth")
```

**`what_imports_module(module_name)`**
```python
results = query.what_imports_module("jwt")
```

**`what_does_file_export(filepath)`**
```python
exports = query.what_does_file_export("src/auth/login.py")
```

**`get_complexity_overview()`**
```python
overview = query.get_complexity_overview()
```

### CLI Commands

```bash
# Build index
python dev/aiagent_navigator.py index

# Get exploration plan (JSON)
python dev/aiagent_navigator.py plan

# Generate navigation guide (markdown)
python dev/aiagent_navigator.py guide

# Analyze specific file
python dev/aiagent_navigator.py analyze <filepath>

# Find related files
python dev/aiagent_navigator.py related <filepath>
```

---

## Best Practices

### 1. Always Start with the Plan

**DON'T** immediately start reading random files.

**DO** load the exploration plan first:
```bash
python dev/aiagent_navigator.py plan
```

This gives you:
- Suggested starting points
- Entry points
- Key modules
- Dependency structure

### 2. Use Context Before Reading Code

**DON'T** read a 1000-line file blind.

**DO** get context first:
```bash
python dev/aiagent_navigator.py analyze src/complex_module.py
```

Then you know:
- What to expect (classes, functions)
- What it depends on (imports)
- How complex it is (complexity_score)

### 3. Follow Relationships

**DON'T** guess which files are related.

**DO** use relationship detection:
```bash
python dev/aiagent_navigator.py related src/module.py
```

This shows you files that:
- Import this module's exports
- Share common dependencies
- Are logically connected

### 4. Refresh Index After Changes

**DON'T** trust stale index after code changes.

**DO** rebuild:
```bash
python dev/aiagent_navigator.py index
python dev/aiagent_navigator.py guide
```

The index is **fast to rebuild** (seconds, not minutes).

### 5. Check Configuration First

**DON'T** ignore project-specific hints.

**DO** read `.aiagent.json`:
```bash
cat .aiagent.json
```

Look for:
- `entry_points` - Where to start
- `ignore_patterns` - What to skip
- `agent_instructions.special_notes` - Important info

### 6. Use the Query Interface

**DON'T** manually search through index JSON.

**DO** use the query interface:
```python
from dev.aiagent_navigator import AIAgentQueryInterface

query = AIAgentQueryInterface()
query.where_is_function("my_function")
```

### 7. Understand Complexity Scores

**Complexity Score Meaning:**
- `< 10` - Simple file, easy to understand
- `10-20` - Moderate complexity
- `20-30` - Complex, requires careful reading
- `> 30` - Hotspot, likely central to architecture

**Use this to prioritize:**
```python
plan = navigator.get_exploration_plan()
hotspots = plan['complexity_hotspots']
# Start with highest complexity files - they're usually most important
```

---

## Troubleshooting

### Problem: Index is Empty or Missing

**Solution:**
```bash
python dev/aiagent_navigator.py index
```

### Problem: File Not Found in Index

**Cause:** File might be:
- Ignored by patterns in `.aiagent.json`
- Not a Python file (current version Python-only)
- Added after index was built

**Solution:**
```bash
# Rebuild index
python dev/aiagent_navigator.py index

# Check if file matches ignore patterns
cat .aiagent.json | grep ignore_patterns
```

### Problem: Related Files Not Showing Up

**Cause:** Files might not be related through imports/exports.

**Debug:**
```bash
# Check what the file imports/exports
python dev/aiagent_navigator.py analyze src/file.py

# Check dependency graph
python dev/aiagent_navigator.py plan | grep -A50 dependency_graph
```

### Problem: Complexity Score Seems Wrong

**Understanding:** Complexity is calculated as:
```
complexity = (classes * 3) + (functions * 2) + imports
```

This is a **heuristic**, not absolute truth. High scores indicate:
- Many classes (probably important)
- Many functions (does a lot)
- Many imports (central to architecture)

### Problem: Navigator Crashes

**Debug:**
```bash
# Run with Python error output
python dev/aiagent_navigator.py index

# Check Python version (requires 3.7+)
python --version

# Check for syntax errors in code files
python -m py_compile path/to/file.py
```

---

## Learning Path

### Level 1: Beginner AI Agent

**Goals:**
- Load exploration plan
- Read suggested starting files
- Understand basic structure

**Commands to Master:**
```bash
python dev/aiagent_navigator.py plan
python dev/aiagent_navigator.py guide
cat NAVIGATION.md
```

### Level 2: Intermediate AI Agent

**Goals:**
- Analyze specific modules
- Find related files
- Use query interface

**Skills to Develop:**
```python
from dev.aiagent_navigator import AIAgentNavigator, AIAgentQueryInterface

nav = AIAgentNavigator()
query = AIAgentQueryInterface()

# Analyze modules
context = nav.get_module_context("file.py")

# Find relationships
related = nav.suggest_related_files("file.py")

# Query for specifics
results = query.where_is_function("my_func")
```

### Level 3: Advanced AI Agent

**Goals:**
- Build index programmatically
- Generate custom reports
- Extend for other languages
- Integrate into workflows

**Advanced Usage:**
```python
# Build custom analysis
nav = AIAgentNavigator()
index = nav.build_index()

# Custom queries
for filepath, info in index.items():
    if info['complexity_score'] > 30:
        print(f"Hotspot: {filepath}")
        related = nav.suggest_related_files(filepath)
        # Analyze hotspot ecosystem

# Generate custom reports
hotspots = nav._find_complexity_hotspots()
# Create visualization, report, etc.
```

### Level 4: Expert AI Agent

**Goals:**
- Extend navigator for new languages
- Create specialized analysis tools
- Build AI agent workflows
- Contribute improvements

**Expert Techniques:**
```python
class CustomNavigator(AIAgentNavigator):
    def analyze_js_file(self, filepath):
        # Custom JavaScript analysis
        pass

    def generate_custom_report(self):
        # Project-specific reporting
        pass

# Create specialized workflows
class AICodeReviewer:
    def __init__(self):
        self.nav = AIAgentNavigator()

    def review_changes(self, changed_files):
        for file in changed_files:
            context = self.nav.get_module_context(file)
            related = self.nav.suggest_related_files(file)
            # AI-powered review considering relationships
```

---

## Quick Reference

### Essential Commands

```bash
# Get started
python dev/aiagent_navigator.py plan

# Build/rebuild index
python dev/aiagent_navigator.py index

# Generate guide
python dev/aiagent_navigator.py guide

# Analyze file
python dev/aiagent_navigator.py analyze <file>

# Find related
python dev/aiagent_navigator.py related <file>
```

### Essential Python API

```python
from dev.aiagent_navigator import AIAgentNavigator, AIAgentQueryInterface

# Setup
nav = AIAgentNavigator()
query = AIAgentQueryInterface()

# Explore
plan = nav.get_exploration_plan()
context = nav.get_module_context("file.py")
related = nav.suggest_related_files("file.py")

# Query
query.where_is_function("func_name")
query.where_is_class("ClassName")
query.what_imports_module("module_name")
overview = query.get_complexity_overview()
```

### Configuration File

```json
{
  "navigation": {
    "entry_points": ["main.py"],
    "ignore_patterns": ["**/__pycache__/**"]
  },
  "exploration_hints": {
    "start_here": ["README.md"],
    "dependency_strategy": "follow_imports"
  },
  "agent_instructions": {
    "special_notes": ["Custom instructions here"]
  }
}
```

---

## Philosophy for AI Agents

### You Are a First-Class Citizen

This codebase is designed **for you**:
- Navigation tools built for AI comprehension
- Structure is discoverable
- Always current (never stale docs)
- Query-driven (ask and receive)

### Work Smart, Not Hard

**Don't read everything.**
- Use the exploration plan
- Start with key modules
- Follow relationships
- Let the navigator guide you

### Trust the Data

The index is **extracted from actual code**:
- Docstrings pulled from source
- Classes/functions parsed from AST
- Imports detected from code
- Always accurate

### Contribute Back

As you learn patterns:
- Update `.aiagent.json` with insights
- Generate fresh guides
- Help future AI agents

---

## Next Steps

1. **Run your first command:**
   ```bash
   python dev/aiagent_navigator.py plan
   ```

2. **Read the suggested starting files**

3. **Analyze a key module:**
   ```bash
   python dev/aiagent_navigator.py analyze dev/aiagent_navigator.py
   ```

4. **Explore relationships:**
   ```bash
   python dev/aiagent_navigator.py related dev/aiagent_navigator.py
   ```

5. **Generate the full guide:**
   ```bash
   python dev/aiagent_navigator.py guide
   cat NAVIGATION.md
   ```

---

**Welcome to intelligent codebase exploration!**

You now have all the tools to efficiently understand and work with this repository. The navigator is your guide - use it well.

For technical details, see [dev/AI_AGENT_TOOLING.md](dev/AI_AGENT_TOOLING.md)

For comparison with other approaches, see [COMPARISON.md](COMPARISON.md)
