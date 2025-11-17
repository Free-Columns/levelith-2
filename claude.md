# Claude.md - AI Agent Navigation Guide

## Repository Architecture

This repository uses a **Context Node** system to provide AI agents with structured navigation and understanding of the codebase.

## Context Node System

### Core Concept
- Every file has a corresponding `[filename].context-node.md` file
- Every directory contains a `context-node.md` file
- These nodes provide structured metadata for AI comprehension

### File Structure
```
project/
├── context-node.md                 # Directory context
├── main.py
├── main.py.context-node.md        # File context
├── module/
│   ├── context-node.md            # Subdirectory context
│   ├── helper.py
│   └── helper.py.context-node.md  # File context
└── dev/
    └── cn-create.py                # Context node generator
```

### Context Node Format

Each context node contains:

1. **Overview** - Type, purpose, path, creation date
2. **Description** - Human-readable explanation
3. **Key Components** - Main elements (functions/files)
4. **Dependencies** - Internal and external requirements
5. **Interfaces** - Input/output specifications
6. **Related Nodes** - Navigation links
7. **AI Agent Notes** - Special instructions for AI processing

### Usage for AI Agents

When navigating this repository:

1. **Start** with root `context-node.md` for project overview
2. **Drill down** into directories via their context nodes
3. **Understand files** through their individual context nodes
4. **Follow relationships** using "Related Context Nodes" sections
5. **Check dependencies** to understand interconnections

### Generating Context Nodes

Run from project root:
```bash
python dev/cn-create.py
```

This creates skeleton context nodes for all files/directories. Human review and enhancement recommended.

### Best Practices for AI Navigation

- Read directory context nodes before exploring contents
- Use file context nodes to understand purpose before reading code
- Follow the "Related Context Nodes" for connected functionality
- Pay attention to "AI Agent Notes" for special handling instructions

## Benefits

- **Consistent Structure**: Predictable documentation pattern
- **Hierarchical Understanding**: Natural tree traversal
- **Relationship Mapping**: Clear dependency graphs
- **AI-Optimized**: Designed for LLM comprehension
- **Self-Documenting**: The structure itself conveys organization
