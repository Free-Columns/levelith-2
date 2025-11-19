# AI Agent Tooling & Navigation System

---
title: "AI Agent Tooling & Navigation System"
description: "Runtime code intelligence system for AI agents with dynamic analysis, cached indexing, and automated navigation guides."
category: "guides"
tags: ["ai-agents", "tooling", "navigation", "code-intelligence", "automation"]
author: "Semour Media Group"
date: "2025-01-19"
lastUpdated: "2025-11-19"
difficulty: "intermediate"
readingTime: 12
relatedPages:
  - "/docs/AI_AGENT_GOLDEN_RULES.md"
  - "/docs/AI_AGENT_GUIDE.md"
  - "/docs/dev/CODEBASE_ANALYSIS.md"
nextPage: "/docs/AI_AGENT_GUIDE.md"
prevPage: "/docs/AI_AGENT_GOLDEN_RULES.md"
searchKeywords:
  - "ai agent"
  - "navigation"
  - "code intelligence"
  - "dynamic analysis"
  - "aiagent navigator"
showTOC: true
showBreadcrumbs: true
showLastUpdated: true
version: "2.0"
---

# AI Agent Tooling & Navigation System

> **TL;DR:** Runtime code intelligence system that eliminates manual context node maintenance by providing AI agents with dynamic analysis, cached indexing, and auto-generated navigation guides.

**Difficulty:** 🟡 Intermediate | **Time:** ⏱️ 12 minutes | **Last Updated:** November 19, 2025

---

## Table of Contents

- [Overview](#overview)
- [How It Works](#how-it-works)
- [Quick Start](#quick-start)
- [For AI Agents](#for-ai-agents)
- [Configuration](#configuration)
- [Advantages Over Context Nodes](#advantages-over-context-nodes)
- [CI/CD Integration](#cicd-integration)
- [API Reference](#api-reference)
- [Best Practices](#best-practices)
- [Migration Guide](#migration-guide)
- [Additional Resources](#additional-resources)

---

## Overview

This system provides **runtime code intelligence** for AI agents without requiring pre-generated documentation files. Instead of maintaining duplicate `.context-node.md` files for every source file, AI agents use configuration hints and dynamic code analysis to navigate your codebase intelligently.

### Key Benefits

- ✅ **Zero Maintenance** - No manual file duplication
- ✅ **Always In Sync** - Extracts directly from source code
- ✅ **Fast Lookups** - Cached index for performance
- ✅ **CI/CD Ready** - Automated index generation
- ✅ **Smart Navigation** - Context-aware file suggestions

:::info
**Note:** This system is designed specifically for AI-assisted development workflows where AI agents need to understand and navigate large codebases efficiently.
:::

---

## How It Works

The AI agent tooling system uses a three-layer approach:

```
┌─────────────────────────────────────────┐
│  1. Configuration (.aiagent.json)       │  ← Hints & preferences
├─────────────────────────────────────────┤
│  2. Dynamic Analysis (aiagent_navigator)│  ← On-demand code analysis
├─────────────────────────────────────────┤
│  3. Cached Index (.aiagent-index.json)  │  ← Fast lookups
└─────────────────────────────────────────┘
```

### Architecture Components

| Component | Purpose | Updates |
|-----------|---------|---------|
| `.aiagent.json` | Configuration & hints | Manual/as needed |
| `aiagent_navigator.py` | Code analysis engine | Never (tool) |
| `.aiagent-index.json` | Cached file index | Automated |
| `NAVIGATION.md` | Human-readable guide | Auto-generated |

---

## Quick Start

### 1. Build the Index

```bash
python dev/aiagent_navigator.py index
```

This analyzes your entire codebase and creates `.aiagent-index.json` with:
- Entry points
- Module dependencies
- Function signatures
- Complexity scores
- Import/export maps

**Expected output:**
```
Analyzing codebase...
Found 87 Python files
Analyzed 1,234 functions
Generated index: .aiagent-index.json (49KB)
```

### 2. Generate Navigation Guide

```bash
python dev/aiagent_navigator.py guide
```

Creates `NAVIGATION.md` with:
- 📍 Entry points
- 🔑 Key modules
- 🔥 Complexity hotspots
- 📊 Auto-generated from actual code

### 3. Get Exploration Plan

```bash
python dev/aiagent_navigator.py plan
```

Returns JSON with suggested exploration strategy:

```json
{
  "suggested_start": ["README.md", "claude.md"],
  "entry_points": ["dev/cn-create.py"],
  "key_modules": ["backend/services/", "backend/models/"],
  "dependency_graph": {...},
  "complexity_hotspots": [
    {"file": "backend/services/experience_service.py", "score": 45}
  ]
}
```

:::tip
**Pro Tip:** Run `index` after major code changes to keep navigation fresh. Add it to your pre-commit hooks or CI/CD pipeline for automation.
:::

---

## For AI Agents

### Usage in AI Agent Workflows

**Step 1: Load Configuration**

```python
from dev.aiagent_navigator import AIAgentNavigator

nav = AIAgentNavigator()
plan = nav.get_exploration_plan()
```

**Step 2: Start with Entry Points**

```python
entry_points = nav.get_entry_points()
# Returns: ['dev/cn-create.py', 'backend/main.py']
```

**Step 3: Analyze Files On-Demand**

```python
context = nav.get_module_context("backend/services/user_service.py")

print(context["docstring"])   # Module description
print(context["classes"])      # ['UserService']
print(context["functions"])    # ['register_user', 'authenticate', ...]
print(context["imports"])      # ['bcrypt', 'jwt', ...]
```

**Step 4: Find Related Files**

```python
related = nav.suggest_related_files("backend/services/user_service.py")
# Returns files that import/export from this module
```

### CLI Commands

```bash
# Analyze a specific file
python dev/aiagent_navigator.py analyze backend/services/user_service.py

# Find related files
python dev/aiagent_navigator.py related backend/services/user_service.py

# Get complexity report
python dev/aiagent_navigator.py complexity --threshold 30
```

---

## Configuration

### `.aiagent.json` Structure

```json
{
  "navigation": {
    "entry_points": ["main.py", "app.py"],
    "key_directories": {
      "backend/": "Backend API and business logic",
      "frontend/": "React frontend application",
      "tests/": "Test suite"
    },
    "ignore_patterns": [
      "**/__pycache__/**",
      "**/node_modules/**",
      "**/.venv/**"
    ]
  },

  "exploration_hints": {
    "start_here": ["README.md", "MANIFEST.md"],
    "dependency_strategy": "follow_imports",
    "max_depth": 3
  },

  "agent_instructions": {
    "preferred_approach": "Start with entry_points, follow imports",
    "special_notes": [
      "Service layer uses dependency injection",
      "All API routes in backend/api/routes/"
    ]
  }
}
```

### Configuration Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `entry_points` | `array` | ✅ Yes | Main application entry files |
| `key_directories` | `object` | ❌ No | Important directories with descriptions |
| `ignore_patterns` | `array` | ❌ No | Glob patterns to exclude |
| `dependency_strategy` | `string` | ❌ No | `follow_imports` or `breadth_first` |
| `max_depth` | `integer` | ❌ No | Maximum traversal depth (default: 3) |

:::warning
**Warning:** Large `max_depth` values (>5) can significantly increase index generation time for large codebases.
:::

---

## Advantages Over Context Nodes

### Comparison Table

| Aspect | Context Nodes | AI Agent Tooling |
|--------|---------------|------------------|
| **Maintenance** | Manual, per-file | Automated |
| **Sync Issues** | High risk | Always in sync |
| **Storage Overhead** | 2x files | Minimal (single index) |
| **Setup Time** | Hours | Minutes |
| **Accuracy** | Depends on humans | Extracted from code |
| **Updates** | Manual editing | Re-run index |
| **CI/CD Integration** | Requires discipline | Auto-generate |
| **Coverage** | Partial | Complete codebase |

### Before (Context Nodes)

```
project/
├── main.py
├── main.py.context-node.md        ← Manual maintenance
├── utils.py
├── utils.py.context-node.md       ← Can get out of sync
├── services/
│   ├── user.py
│   ├── user.py.context-node.md    ← 2x files for everything
│   ├── auth.py
│   └── auth.py.context-node.md
└── ...
```

= 2x files, high maintenance burden

### After (AI Agent Tooling)

```
project/
├── .aiagent.json              # Configuration (one-time)
├── .aiagent-index.json        # Auto-generated
├── NAVIGATION.md              # Auto-generated
├── main.py
├── utils.py
├── services/
│   ├── user.py
│   └── auth.py
└── ...
```

= Minimal overhead, automated

---

## CI/CD Integration

### GitHub Actions Example

Add to your workflow:

```yaml
# .github/workflows/update-index.yml
name: Update AI Agent Index

on:
  push:
    branches: [main, develop]
  pull_request:

jobs:
  update-index:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Build AI Index
        run: python dev/aiagent_navigator.py index

      - name: Generate Guide
        run: python dev/aiagent_navigator.py guide

      - name: Commit if changed
        run: |
          git config user.name "AI Agent Bot"
          git config user.email "bot@example.com"
          git add .aiagent-index.json NAVIGATION.md
          git diff --quiet || git commit -m "chore: Update AI agent index [skip ci]"
          git push
```

### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: update-ai-index
        name: Update AI Agent Index
        entry: python dev/aiagent_navigator.py index
        language: system
        pass_filenames: false
```

---

## API Reference

### `AIAgentNavigator` Class

#### Methods

**`get_entry_points() -> List[str]`**

Returns list of recommended starting files based on configuration.

```python
nav = AIAgentNavigator()
entry_points = nav.get_entry_points()
# ['backend/main.py', 'frontend/src/App.tsx']
```

**`build_index() -> Dict`**

Analyzes entire codebase and builds comprehensive index.

```python
index = nav.build_index()
# Creates .aiagent-index.json
```

**`get_exploration_plan() -> Dict`**

Returns comprehensive exploration strategy with entry points, key modules, and dependency graph.

**`get_module_context(filepath: str) -> Dict`**

Get detailed information about a specific module.

```python
context = nav.get_module_context("backend/services/user_service.py")
```

**`suggest_related_files(filepath: str) -> List[str]`**

Find related modules based on imports/exports.

**`generate_navigation_guide() -> str`**

Create markdown navigation guide.

#### Data Structures

**ModuleInfo:**

```python
{
  "path": "backend/services/user_service.py",
  "docstring": "User management service with authentication",
  "classes": ["UserService"],
  "functions": ["register_user", "authenticate", "update_profile"],
  "imports": ["bcrypt", "jwt", "sqlalchemy"],
  "exports": ["UserService"],
  "complexity_score": 25,
  "dependencies": ["backend/repositories/user_repository.py"]
}
```

**Exploration Plan:**

```python
{
  "suggested_start": ["README.md", "MANIFEST.md"],
  "entry_points": ["backend/main.py"],
  "key_modules": [
    "backend/services/",
    "backend/api/routes/"
  ],
  "dependency_graph": {
    "backend/main.py": ["backend/api/routes/users.py", ...]
  },
  "complexity_hotspots": [
    {"file": "backend/services/experience_service.py", "score": 45}
  ]
}
```

---

## Best Practices

### ✅ DO

1. **Run index after major changes**
   ```bash
   # After refactoring or adding new modules
   python dev/aiagent_navigator.py index
   ```

2. **Add human insights to config**
   ```json
   {
     "agent_instructions": {
       "special_notes": [
         "Auth flow uses JWT tokens",
         "Database migrations in alembic/"
       ]
     }
   }
   ```

3. **Automate in CI/CD**
   - Keep index up-to-date automatically
   - Reduce manual maintenance

4. **Cache the index for speed**
   - Use `.aiagent-index.json` for fast lookups
   - Rebuild only when code changes

5. **Customize per project**
   - Adjust config for your architecture
   - Define clear entry points

### ❌ DON'T

1. **Don't commit large indexes**
   ```bash
   # ❌ BAD - Huge index in git
   git add .aiagent-index.json  # If > 1MB

   # ✅ GOOD - Add to .gitignore or use compression
   echo ".aiagent-index.json" >> .gitignore
   ```

2. **Don't manually edit the index**
   ```python
   # ❌ BAD - Manual editing
   # Manually editing .aiagent-index.json

   # ✅ GOOD - Always regenerate
   python dev/aiagent_navigator.py index
   ```

---

## Migration Guide

### Migrating from Context Nodes

If you have existing `.context-node.md` files:

**Step 1: Run Initial Index**

```bash
python dev/aiagent_navigator.py index
```

**Step 2: Compare Generated Guide**

```bash
python dev/aiagent_navigator.py guide
# Review NAVIGATION.md vs existing context nodes
```

**Step 3: Extract Human Insights**

Add unique insights from context nodes to `.aiagent.json`:

```json
{
  "agent_instructions": {
    "special_notes": [
      "Legacy auth system in deprecated/",
      "New features must follow Golden Rules"
    ]
  }
}
```

**Step 4: Gradually Remove Context Nodes**

```bash
# After verification, remove old context nodes
find . -name "*.context-node.md" -delete
```

:::danger
**Critical:** Back up your context node files before deletion. Some may contain valuable human insights that should be migrated to `.aiagent.json`.
:::

---

## Extending for Other Languages

The navigator can be extended for JavaScript, TypeScript, Java, etc:

### JavaScript/TypeScript Extension

```python
class JSNavigator(AIAgentNavigator):
    """Extended navigator for JavaScript/TypeScript projects."""

    def analyze_js_file(self, filepath: str) -> Dict:
        """
        Parse JavaScript/TypeScript files.

        Uses esprima or @babel/parser for AST analysis.
        """
        # Parse with esprima or similar
        # Extract exports, imports, functions, classes
        pass

    def get_package_dependencies(self) -> Dict:
        """Extract dependencies from package.json."""
        pass
```

### Java Extension

```python
class JavaNavigator(AIAgentNavigator):
    """Extended navigator for Java projects."""

    def analyze_java_file(self, filepath: str) -> Dict:
        """Parse Java files using javalang or similar."""
        pass
```

---

## Troubleshooting

<details>
<summary><strong>❌ Error: "No Python files found"</strong></summary>

**Symptoms:** Index generation finds 0 files

**Causes:**
1. Running from wrong directory
2. All files excluded by ignore patterns
3. No Python files in project

**Solutions:**
```bash
# Check current directory
pwd

# Verify Python files exist
find . -name "*.py" -type f | head -10

# Review ignore patterns
cat .aiagent.json | grep -A5 "ignore_patterns"
```

**Explanation:** The navigator starts from the current working directory. Ensure you're in the project root.
</details>

<details>
<summary><strong>⚠️ Warning: "Index file is stale"</strong></summary>

**Symptoms:** Navigator warns that index is outdated

**Solutions:**
1. Regenerate the index
   ```bash
   python dev/aiagent_navigator.py index
   ```

2. Set up automatic regeneration in CI/CD

**Additional context:** Index becomes stale when source files are modified after index generation. This is normal during active development.
</details>

<details>
<summary><strong>ℹ️ Question: How often should I regenerate the index?</strong></summary>

**Answer:** Regenerate after significant code changes:
- Adding new modules
- Major refactoring
- Changing project structure
- Before important AI agent sessions

**Example automation:**
```bash
# Add to pre-commit hook
python dev/aiagent_navigator.py index
```
</details>

---

## Additional Resources

### Official Documentation

- 📚 [AI Agent Golden Rules](/docs/AI_AGENT_GOLDEN_RULES.md)
- 🏗️ [AI Agent Guide](/docs/AI_AGENT_GUIDE.md)
- 🧪 [Codebase Analysis](/docs/dev/CODEBASE_ANALYSIS.md)

### External Resources

- 🌐 [AST Module Documentation](https://docs.python.org/3/library/ast.html)
- 📖 [Static Analysis Best Practices](https://en.wikipedia.org/wiki/Static_program_analysis)

### Code Examples

- 💻 [AIAgentNavigator Source](/dev/aiagent_navigator.py)
- 🎯 [Example Configuration](/.aiagent.json)

---

## Related Documentation

- **Previous:** [AI Agent Golden Rules](/docs/AI_AGENT_GOLDEN_RULES.md)
- **Next:** [AI Agent Guide](/docs/AI_AGENT_GUIDE.md)

**Other related documentation:**

- [Codebase Analysis Report](/docs/dev/CODEBASE_ANALYSIS.md)
- [Development Priorities](/docs/dev/DEVELOPMENT_PRIORITIES.md)
- [MANIFEST](/docs/MANIFEST.md)

---

## Feedback

Found an issue with this guide? Have suggestions for improvement?

- 👍 **Helpful?** Give us feedback via the reaction buttons below
- 🐛 **Found a bug?** [Report it on GitHub](https://github.com/Free-Columns/levelith-2/issues)
- 💡 **Have an idea?** [Start a discussion](https://github.com/Free-Columns/levelith-2/discussions)

---

**Last Updated:** November 19, 2025 | **Version:** 2.0 | **Contributors:** Semour Media Group

---

*This document is part of the Levelith Developer Documentation. For questions, join our [Discord community](https://discord.gg/levelith).*
