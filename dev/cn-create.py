#!/usr/bin/env python3
"""
Context Node Generator
Creates context-node.md files for every file and directory in the repository
to provide structured documentation for AI agents.
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Set

class ContextNodeGenerator:
    def __init__(self, root_path: str):
        self.root = Path(root_path).resolve()
        self.dev_dir = self.root / "dev"
        self.context_node_name = "context-node.md"
        
        # Directories to skip
        self.skip_dirs = {
            '.git', '__pycache__', 'node_modules', '.venv', 'venv',
            'env', '.env', 'dist', 'build', '.pytest_cache', '.mypy_cache'
        }
        
        # File patterns to skip context nodes for
        self.skip_files = {
            '.DS_Store', 'Thumbs.db', '.gitignore', '.env',
            self.context_node_name
        }
        
    def should_process(self, path: Path) -> bool:
        """Check if path should have a context node."""
        # Skip hidden files/dirs (except .github)
        if path.name.startswith('.') and path.name != '.github':
            return False
            
        # Skip specified directories
        if path.is_dir() and path.name in self.skip_dirs:
            return False
            
        # Skip specified files
        if path.is_file() and path.name in self.skip_files:
            return False
            
        # Skip if it's the dev directory containing this script
        if path == self.dev_dir:
            return True  # Process dev dir but not this script
            
        return True
    
    def get_file_purpose(self, file_path: Path) -> str:
        """Infer file purpose from extension and name."""
        ext = file_path.suffix.lower()
        name = file_path.stem.lower()
        
        purpose_map = {
            '.py': 'Python module',
            '.js': 'JavaScript module',
            '.ts': 'TypeScript module',
            '.jsx': 'React component',
            '.tsx': 'React TypeScript component',
            '.md': 'Documentation',
            '.json': 'Configuration/Data',
            '.yaml': 'Configuration',
            '.yml': 'Configuration',
            '.css': 'Stylesheet',
            '.html': 'HTML template',
            '.sh': 'Shell script',
            '.sql': 'Database script',
            '.dockerfile': 'Container definition',
            '.gitignore': 'Git ignore rules',
        }
        
        if name == 'readme':
            return 'Project documentation'
        elif name == 'requirements':
            return 'Python dependencies'
        elif name == 'package':
            return 'Node.js package configuration'
        elif name == 'dockerfile' or name.startswith('docker'):
            return 'Container definition'
        elif name.startswith('test_') or name.endswith('_test'):
            return 'Test module'
            
        return purpose_map.get(ext, 'Project file')
    
    def create_file_context_node(self, file_path: Path) -> None:
        """Create context node for a file."""
        context_path = file_path.parent / f"{file_path.name}.{self.context_node_name}"
        
        # Skip if context node already exists
        if context_path.exists():
            print(f"  [EXISTS] {context_path.relative_to(self.root)}")
            return
            
        relative_path = file_path.relative_to(self.root)
        purpose = self.get_file_purpose(file_path)
        
        content = f"""# Context Node: {file_path.name}

## Overview
**Type**: File
**Purpose**: {purpose}
**Path**: `{relative_path}`
**Created**: {datetime.now().strftime('%Y-%m-%d')}

## Description
[Describe what this file does and its role in the project]

## Key Functions/Components
- [List main functions, classes, or components]

## Dependencies
- [List key dependencies or imports]

## Interfaces
**Inputs**: [What this file receives/processes]
**Outputs**: [What this file produces/returns]

## Usage Example
```
[Provide a brief usage example if applicable]
```

## Related Context Nodes
- [Link to related files or directories]

## Notes for AI Agents
- [Special considerations for understanding this file]
- [Common patterns or conventions used]
"""
        
        try:
            context_path.write_text(content)
            print(f"  [CREATE] {context_path.relative_to(self.root)}")
        except Exception as e:
            print(f"  [ERROR] Failed to create {context_path}: {e}")
    
    def create_dir_context_node(self, dir_path: Path) -> None:
        """Create context node for a directory."""
        context_path = dir_path / self.context_node_name
        
        # Skip if context node already exists
        if context_path.exists():
            print(f"  [EXISTS] {context_path.relative_to(self.root)}")
            return
            
        relative_path = dir_path.relative_to(self.root)
        
        # List immediate children
        children = []
        for child in sorted(dir_path.iterdir()):
            if self.should_process(child) and child.name != self.context_node_name:
                child_type = "dir" if child.is_dir() else "file"
                children.append(f"- `{child.name}` ({child_type})")
        
        children_list = '\n'.join(children) if children else "- [Empty directory]"
        
        content = f"""# Context Node: {dir_path.name}/

## Overview
**Type**: Directory
**Purpose**: [Define directory purpose]
**Path**: `{relative_path}`
**Created**: {datetime.now().strftime('%Y-%m-%d')}

## Description
[Describe the purpose and contents of this directory]

## Directory Structure
{children_list}

## Architectural Role
- **Responsibility**: [What this directory is responsible for]
- **Interactions**: [How it interacts with other parts]
- **Patterns**: [Design patterns or conventions used]

## Key Files
- [Highlight important files and their roles]

## Dependencies
- **Internal**: [Dependencies within the project]
- **External**: [External dependencies]

## Development Guidelines
- [Conventions for adding new files]
- [Naming patterns]
- [Organization principles]

## Related Context Nodes
- [Link to parent or sibling directories]
- [Link to related functional areas]

## Notes for AI Agents
- [How to navigate this directory]
- [Key concepts to understand]
- [Common tasks performed here]
"""
        
        try:
            context_path.write_text(content)
            print(f"  [CREATE] {context_path.relative_to(self.root)}")
        except Exception as e:
            print(f"  [ERROR] Failed to create {context_path}: {e}")
    
    def generate_context_nodes(self) -> None:
        """Walk the repository and generate context nodes."""
        print(f"\n🚀 Generating context nodes for: {self.root}")
        print("=" * 60)
        
        # Track statistics
        dirs_processed = 0
        files_processed = 0
        
        for root, dirs, files in os.walk(self.root):
            current_path = Path(root)
            
            # Filter directories to process
            dirs[:] = [d for d in dirs if self.should_process(current_path / d)]
            
            # Process current directory
            if self.should_process(current_path):
                print(f"\n📁 Processing: {current_path.relative_to(self.root)}")
                self.create_dir_context_node(current_path)
                dirs_processed += 1
                
                # Process files in current directory
                for file_name in files:
                    file_path = current_path / file_name
                    
                    # Skip the script itself and context nodes
                    if file_name == 'cn-create.py' and current_path == self.dev_dir:
                        continue
                    if file_name.endswith(self.context_node_name):
                        continue
                        
                    if self.should_process(file_path):
                        self.create_file_context_node(file_path)
                        files_processed += 1
        
        print("\n" + "=" * 60)
        print(f"✅ Context node generation complete!")
        print(f"   Directories processed: {dirs_processed}")
        print(f"   Files processed: {files_processed}")
        print(f"   Total context nodes: {dirs_processed + files_processed}")

def main():
    # Determine repository root (parent of dev directory)
    script_path = Path(__file__).resolve()
    
    # Handle both execution from dev/ and from root
    if script_path.parent.name == 'dev':
        repo_root = script_path.parent.parent
    else:
        repo_root = script_path.parent
        
    # Confirm with user
    print(f"📍 Repository root: {repo_root}")
    response = input("Generate context nodes? (y/n): ").strip().lower()
    
    if response == 'y':
        generator = ContextNodeGenerator(str(repo_root))
        generator.generate_context_nodes()
    else:
        print("❌ Operation cancelled")
        sys.exit(0)

if __name__ == "__main__":
    main()
