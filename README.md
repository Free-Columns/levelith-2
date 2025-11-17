# Levelith-2

**Levelith Refactor and Revision: Heavy AI Assistant Modeling**

This repository is designed with AI agents as first-class citizens, providing intelligent navigation and code understanding systems optimized for LLM comprehension.

## Overview

Levelith-2 implements advanced AI agent tooling for automated codebase exploration, analysis, and documentation. The project offers two complementary approaches for AI navigation:

1. **Intelligent AI Agent Tooling** (Recommended) - Dynamic, automated code analysis
2. **Context Node System** (Legacy) - Static documentation files

## Quick Start

### For AI Agents

**Recommended: Use Intelligent Tooling**

```bash
# Build codebase index
python dev/aiagent_navigator.py index

# Get exploration plan
python dev/aiagent_navigator.py plan

# Generate navigation guide
python dev/aiagent_navigator.py guide

# Analyze specific file
python dev/aiagent_navigator.py analyze dev/cn-create.py
```

**See**: [AI_AGENT_GUIDE.md](AI_AGENT_GUIDE.md) for complete operating instructions.

### For Developers

```bash
# Clone repository
git clone <repository-url>
cd levelith-2

# Install dependencies (if any)
# pip install -r requirements.txt

# Explore the codebase
python dev/aiagent_navigator.py index
python dev/aiagent_navigator.py guide
cat NAVIGATION.md
```

## Architecture

### Intelligent AI Agent Tooling

The primary navigation system uses **dynamic code analysis** rather than static documentation:

- **`.aiagent.json`** - Configuration and navigation hints
- **`dev/aiagent_navigator.py`** - Intelligence engine with automated analysis
- **`.aiagent-index.json`** - Auto-generated codebase index (cached)
- **`NAVIGATION.md`** - Auto-generated navigation guide

**Benefits:**
- Always in sync with actual code
- Automated maintenance (single command)
- Minimal storage overhead
- Query interface for on-demand analysis
- CI/CD ready

**Documentation:**
- [dev/AI_AGENT_TOOLING.md](dev/AI_AGENT_TOOLING.md) - Complete technical documentation
- [AI_AGENT_GUIDE.md](AI_AGENT_GUIDE.md) - Learning and operating guide for AI agents
- [COMPARISON.md](COMPARISON.md) - Comparison with context nodes

### Context Node System (Legacy)

An alternative static documentation approach:

- **`dev/cn-create.py`** - Generates context node files
- **`dev/cn-validate.py`** - Validates context node completeness

Each file/directory gets a corresponding `.context-node.md` file with metadata.

**See**: [claude.md](claude.md) for context node documentation.

## Key Features

### For AI Agents

1. **Dynamic Code Analysis** - Extract structure on-demand from actual code
2. **Exploration Planning** - Smart suggestions for where to start
3. **Dependency Mapping** - Automatic relationship detection
4. **Complexity Analysis** - Identify hotspots and key modules
5. **Query Interface** - Ask specific questions about the codebase
6. **Related File Detection** - Find connected modules automatically

### For Developers

1. **Automated Documentation** - No manual maintenance required
2. **CI/CD Integration** - Auto-update in pipelines
3. **Codebase Insights** - Complexity metrics and patterns
4. **Navigation Guides** - Human-readable overviews
5. **Extensible** - Add support for other languages

## Project Structure

```
levelith-2/
├── README.md                       # This file
├── claude.md                       # AI agent navigation guide
├── AI_AGENT_GUIDE.md              # Learning resource for AI agents
├── COMPARISON.md                   # Context nodes vs AI tooling
├── NAVIGATION.md                   # Auto-generated navigation guide
│
├── .aiagent.json                   # AI agent configuration
├── .aiagent-index.json             # Auto-generated codebase index
│
├── dev/                            # Development tools
│   ├── aiagent_navigator.py        # Intelligent navigation system
│   ├── example_ai_agent_usage.py   # Demo and examples
│   ├── AI_AGENT_TOOLING.md        # Technical documentation
│   ├── cn-create.py                # Context node generator (legacy)
│   └── cn-validate.py              # Context node validator (legacy)
│
└── docs/                           # Additional documentation
```

## Usage Examples

### Automated Navigation

```python
from dev.aiagent_navigator import AIAgentNavigator

# Initialize navigator
nav = AIAgentNavigator()

# Get exploration plan
plan = nav.get_exploration_plan()
print(f"Start here: {plan['suggested_start']}")
print(f"Entry points: {plan['entry_points']}")
print(f"Key modules: {plan['key_modules']}")

# Analyze specific module
context = nav.get_module_context("dev/cn-create.py")
print(f"Classes: {context['classes']}")
print(f"Functions: {context['functions']}")
print(f"Imports: {context['imports']}")

# Find related files
related = nav.suggest_related_files("dev/cn-create.py")
for item in related:
    print(f"Related: {item['path']} - {item['reason']}")
```

### CLI Commands

```bash
# Build index and generate guide
python dev/aiagent_navigator.py index
python dev/aiagent_navigator.py guide

# View exploration plan (JSON)
python dev/aiagent_navigator.py plan

# Analyze specific file
python dev/aiagent_navigator.py analyze dev/aiagent_navigator.py

# Find related files
python dev/aiagent_navigator.py related dev/aiagent_navigator.py

# Run demo
python dev/example_ai_agent_usage.py
```

## Documentation

### For AI Agents

- **[AI_AGENT_GUIDE.md](AI_AGENT_GUIDE.md)** - Start here! Complete learning and operating guide
- **[claude.md](claude.md)** - Navigation system overview
- **[NAVIGATION.md](NAVIGATION.md)** - Auto-generated codebase map

### For Developers

- **[dev/AI_AGENT_TOOLING.md](dev/AI_AGENT_TOOLING.md)** - Technical documentation
- **[COMPARISON.md](COMPARISON.md)** - Approach comparison and migration guide
- **[dev/example_ai_agent_usage.py](dev/example_ai_agent_usage.py)** - Working code examples

## CI/CD Integration

Add to your workflow to keep AI navigation always up-to-date:

```yaml
name: Update AI Agent Index

on: [push]

jobs:
  update-index:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Build AI Index
        run: python dev/aiagent_navigator.py index

      - name: Generate Navigation Guide
        run: python dev/aiagent_navigator.py guide

      - name: Commit if changed
        run: |
          git config user.name "AI Agent Bot"
          git add .aiagent-index.json NAVIGATION.md
          git diff --quiet || git commit -m "Update AI agent index"
          git push
```

## Comparison: Context Nodes vs AI Tooling

| Aspect | Context Nodes | AI Tooling |
|--------|--------------|------------|
| **Maintenance** | Manual | Automated |
| **Sync Issues** | High risk | Always in sync |
| **Setup Time** | 4-8 hours | 5 minutes |
| **Storage** | 2x files | Minimal |
| **CI/CD** | Requires discipline | Auto-generate |
| **Accuracy** | Depends on humans | Extracted from code |

**See [COMPARISON.md](COMPARISON.md) for detailed analysis.**

## Extending to Other Languages

The navigator can be extended for JavaScript, TypeScript, Java, etc:

```python
class JSNavigator(AIAgentNavigator):
    def analyze_js_file(self, filepath):
        # Parse with esprima, babel, or similar
        # Extract exports, imports, functions, classes
        pass
```

## Philosophy

**AI Agents as First-Class Citizens**

This repository treats AI agents not as afterthoughts, but as primary users:

1. **Self-Documenting** - Code structure is discoverable
2. **Query-Driven** - Ask questions, get answers
3. **Always Current** - Generated from actual code, not stale docs
4. **Low Overhead** - Minimal burden on human developers
5. **Intelligent** - Smart suggestions and relationship detection

## Contributing

When adding code to this repository:

1. **Write good docstrings** - These are extracted automatically
2. **Run the index** - `python dev/aiagent_navigator.py index`
3. **Check the guide** - Review generated `NAVIGATION.md`
4. **Add insights to config** - Update `.aiagent.json` with special notes

## License

[Specify your license]

## Credits

Created as part of the Levelith project, reimagining software development with AI agents as collaborative partners.

---

**For AI Agents**: Start with [AI_AGENT_GUIDE.md](AI_AGENT_GUIDE.md) for complete operating instructions.

**For Developers**: Run `python dev/aiagent_navigator.py guide` to generate a fresh navigation guide.
