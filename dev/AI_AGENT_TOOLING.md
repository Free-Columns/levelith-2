# Intelligent AI Agent Tooling

This system provides **runtime code intelligence** for AI agents without requiring pre-generated documentation files.

## How It Works

Instead of maintaining duplicate `.context-node.md` files, AI agents use:

1. **Configuration** (`.aiagent.json`) - Hints and preferences
2. **Dynamic Analysis** (`aiagent_navigator.py`) - On-demand code analysis
3. **Cached Index** (`.aiagent-index.json`) - Fast lookups

## Quick Start

### 1. Build the Index

```bash
python dev/aiagent_navigator.py index
```

This analyzes your entire codebase and creates `.aiagent-index.json`.

### 2. Generate Navigation Guide

```bash
python dev/aiagent_navigator.py guide
```

Creates `NAVIGATION.md` with:
- Entry points
- Key modules
- Complexity hotspots
- Auto-generated from actual code

### 3. Get Exploration Plan

```bash
python dev/aiagent_navigator.py plan
```

Returns JSON with suggested exploration strategy:
```json
{
  "suggested_start": ["README.md", "claude.md"],
  "entry_points": ["dev/cn-create.py"],
  "key_modules": [...],
  "dependency_graph": {...},
  "complexity_hotspots": [...]
}
```

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
# Read these files first: ['dev/cn-create.py']
```

**Step 3: Analyze Files On-Demand**
```python
context = nav.get_module_context("dev/cn-create.py")
print(context["docstring"])
print(context["classes"])
print(context["functions"])
print(context["imports"])
```

**Step 4: Find Related Files**
```python
related = nav.suggest_related_files("dev/cn-create.py")
# Returns files that import/export from this module
```

### CLI Commands

```bash
# Analyze a specific file
python dev/aiagent_navigator.py analyze dev/cn-create.py

# Find related files
python dev/aiagent_navigator.py related dev/cn-create.py
```

## Configuration: `.aiagent.json`

```json
{
  "navigation": {
    "entry_points": ["main.py", "app.py"],
    "key_directories": {
      "src/": "Source code",
      "tests/": "Test files"
    },
    "ignore_patterns": ["**/__pycache__/**"]
  },

  "exploration_hints": {
    "start_here": ["README.md"],
    "dependency_strategy": "follow_imports",
    "max_depth": 3
  },

  "agent_instructions": {
    "preferred_approach": "Start with entry_points, follow imports",
    "special_notes": ["Custom notes for this codebase"]
  }
}
```

## Advantages Over Static Context Nodes

| Aspect | Context Nodes | AI Agent Tooling |
|--------|---------------|------------------|
| **Maintenance** | Manual, per-file | Automated |
| **Sync Issues** | High risk | Always in sync |
| **Storage** | 2x files | Minimal |
| **Setup Time** | Hours | Minutes |
| **Accuracy** | Depends on humans | Extracted from code |
| **Updates** | Manual editing | Re-run index |
| **CI/CD** | Requires discipline | Can auto-generate |

## Integration with CI/CD

Add to your workflow:

```yaml
# .github/workflows/update-index.yml
name: Update AI Agent Index

on: [push]

jobs:
  update-index:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build AI Index
        run: python dev/aiagent_navigator.py index
      - name: Generate Guide
        run: python dev/aiagent_navigator.py guide
      - name: Commit if changed
        run: |
          git config user.name "AI Agent Bot"
          git add .aiagent-index.json NAVIGATION.md
          git diff --quiet || git commit -m "Update AI agent index"
          git push
```

## Example AI Agent Session

```
AI Agent: I need to understand this codebase.

Step 1: Load exploration plan
$ python dev/aiagent_navigator.py plan

Step 2: Start with suggested entry point
Reading: dev/cn-create.py

Step 3: Get context
$ python dev/aiagent_navigator.py analyze dev/cn-create.py
{
  "docstring": "Context node generator...",
  "functions": ["create_node", "scan_directory"],
  "imports": ["os", "pathlib", "json"]
}

Step 4: Find related files
$ python dev/aiagent_navigator.py related dev/cn-create.py
[No related internal files found]

Conclusion: This is a standalone utility script.
```

## API Reference

### `AIAgentNavigator` Class

#### Methods

- `get_entry_points()` - Returns list of recommended starting files
- `build_index()` - Analyzes entire codebase
- `get_exploration_plan()` - Returns comprehensive exploration strategy
- `get_module_context(filepath)` - Get info about specific module
- `suggest_related_files(filepath)` - Find related modules
- `generate_navigation_guide()` - Create markdown guide

#### Data Structures

**ModuleInfo:**
```python
{
  "path": "dev/cn-create.py",
  "docstring": "Module description",
  "classes": ["ClassName"],
  "functions": ["func_name"],
  "imports": ["os", "sys"],
  "exports": ["public_func"],
  "complexity_score": 25
}
```

**Exploration Plan:**
```python
{
  "suggested_start": ["README.md"],
  "entry_points": ["main.py"],
  "key_modules": [...],
  "dependency_graph": {...},
  "complexity_hotspots": [...]
}
```

## Extending for Other Languages

The navigator can be extended for JavaScript, Java, etc:

```python
class JSNavigator(AIAgentNavigator):
    def analyze_js_file(self, filepath):
        # Parse with esprima or similar
        # Extract exports, imports, functions
        pass
```

## Migration from Context Nodes

If you have existing `.context-node.md` files:

1. Run: `python dev/aiagent_navigator.py index`
2. Compare generated `NAVIGATION.md` with context nodes
3. Add any human insights to `.aiagent.json` config
4. Gradually remove context node files

## Best Practices

1. **Run index after major changes** - Keeps navigation fresh
2. **Add human insights to config** - Complement automated analysis
3. **Use in CI/CD** - Automated documentation generation
4. **Cache the index** - Fast lookups for AI agents
5. **Customize per project** - Adjust config for your architecture

## Comparison

**Before (Context Nodes):**
```
project/
├── main.py
├── main.py.context-node.md
├── utils.py
├── utils.py.context-node.md
└── ...
```
= 2x files, manual maintenance

**After (AI Agent Tooling):**
```
project/
├── .aiagent.json              # Configuration
├── .aiagent-index.json        # Auto-generated
├── NAVIGATION.md              # Auto-generated
├── main.py
└── utils.py
```
= Minimal overhead, automated
