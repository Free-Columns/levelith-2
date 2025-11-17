#!/usr/bin/env python3
"""
Context Node Validator
Validates that context nodes are complete and properly formatted.
Used in CI/CD pipeline to ensure documentation quality.
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple
import argparse

class ContextNodeValidator:
    def __init__(self, root_path: str):
        self.root = Path(root_path).resolve()
        self.context_node_name = "context-node.md"
        self.errors = []
        self.warnings = []
        
        # Required sections for validation
        self.required_sections = {
            'file': [
                '## Overview',
                '## Description',
                '## Key Functions/Components',
                '## Dependencies',
                '## Interfaces',
                '## Related Context Nodes',
                '## Notes for AI Agents'
            ],
            'directory': [
                '## Overview',
                '## Description',
                '## Directory Structure',
                '## Architectural Role',
                '## Key Files',
                '## Dependencies',
                '## Development Guidelines',
                '## Related Context Nodes',
                '## Notes for AI Agents'
            ]
        }
        
        # Patterns to check for incomplete content
        self.incomplete_patterns = [
            r'\[.*?\]',  # Unfilled placeholders
            r'\[Describe.*?\]',
            r'\[List.*?\]',
            r'\[Define.*?\]',
            r'\[What.*?\]',
            r'\[How.*?\]'
        ]
    
    def validate_node(self, node_path: Path) -> Tuple[List[str], List[str]]:
        """Validate a single context node."""
        errors = []
        warnings = []
        
        if not node_path.exists():
            errors.append(f"Missing context node: {node_path}")
            return errors, warnings
        
        content = node_path.read_text()
        
        # Determine if it's a file or directory node
        is_directory = node_path.name == self.context_node_name
        node_type = 'directory' if is_directory else 'file'
        
        # Check for required sections
        required = self.required_sections[node_type]
        for section in required:
            if section not in content:
                errors.append(f"{node_path}: Missing section '{section}'")
        
        # Check for incomplete placeholders
        for pattern in self.incomplete_patterns:
            matches = re.findall(pattern, content)
            if matches:
                warnings.append(f"{node_path}: Incomplete content found: {matches[0]}")
        
        # Check for proper metadata
        if '**Type**:' not in content:
            errors.append(f"{node_path}: Missing Type metadata")
        if '**Purpose**:' not in content:
            errors.append(f"{node_path}: Missing Purpose metadata")
        if '**Path**:' not in content:
            errors.append(f"{node_path}: Missing Path metadata")
        
        # Check for empty sections
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('##'):
                # Check if next non-empty line is another section header
                j = i + 1
                while j < len(lines) and not lines[j].strip():
                    j += 1
                if j < len(lines) and lines[j].startswith('##'):
                    warnings.append(f"{node_path}: Empty section '{line}'")
        
        return errors, warnings
    
    def check_file_coverage(self) -> Tuple[List[str], List[str]]:
        """Check if all files have corresponding context nodes."""
        errors = []
        warnings = []
        
        for root, dirs, files in os.walk(self.root):
            current_path = Path(root)
            
            # Skip hidden and build directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in 
                      {'node_modules', '__pycache__', 'dist', 'build', 'venv'}]
            
            # Check directory context node
            dir_context = current_path / self.context_node_name
            if not dir_context.exists():
                errors.append(f"Missing directory context node: {dir_context}")
            
            # Check file context nodes
            for file_name in files:
                if file_name.endswith(self.context_node_name):
                    continue
                if file_name.startswith('.'):
                    continue
                
                file_path = current_path / file_name
                expected_context = current_path / f"{file_name}.{self.context_node_name}"
                
                if not expected_context.exists():
                    warnings.append(f"Missing file context node: {expected_context}")
        
        return errors, warnings
    
    def validate_all(self) -> bool:
        """Validate all context nodes in the repository."""
        print(f"\n🔍 Validating context nodes in: {self.root}")
        print("=" * 60)
        
        all_errors = []
        all_warnings = []
        
        # Check coverage
        coverage_errors, coverage_warnings = self.check_file_coverage()
        all_errors.extend(coverage_errors)
        all_warnings.extend(coverage_warnings)
        
        # Validate existing nodes
        for node_path in self.root.rglob(f"*{self.context_node_name}"):
            errors, warnings = self.validate_node(node_path)
            all_errors.extend(errors)
            all_warnings.extend(warnings)
        
        # Print results
        if all_errors:
            print("\n❌ ERRORS:")
            for error in all_errors:
                print(f"  - {error}")
        
        if all_warnings:
            print("\n⚠️  WARNINGS:")
            for warning in all_warnings:
                print(f"  - {warning}")
        
        if not all_errors and not all_warnings:
            print("\n✅ All context nodes are valid and complete!")
        
        print("\n" + "=" * 60)
        print(f"Summary: {len(all_errors)} errors, {len(all_warnings)} warnings")
        
        return len(all_errors) == 0
    
    def check_completeness(self) -> Dict[str, float]:
        """Calculate completeness percentage of context nodes."""
        total_files = 0
        complete_files = 0
        partial_files = 0
        
        for root, dirs, files in os.walk(self.root):
            current_path = Path(root)
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in 
                      {'node_modules', '__pycache__', 'dist', 'build', 'venv'}]
            
            for file_name in files:
                if file_name.endswith(self.context_node_name):
                    continue
                total_files += 1
                
                expected_context = current_path / f"{file_name}.{self.context_node_name}"
                if expected_context.exists():
                    content = expected_context.read_text()
                    if not any(re.search(p, content) for p in self.incomplete_patterns):
                        complete_files += 1
                    else:
                        partial_files += 1
        
        completeness = (complete_files / total_files * 100) if total_files > 0 else 0
        
        return {
            'total': total_files,
            'complete': complete_files,
            'partial': partial_files,
            'missing': total_files - complete_files - partial_files,
            'completeness': completeness
        }

def main():
    parser = argparse.ArgumentParser(description='Validate context nodes')
    parser.add_argument('--root', default='.', help='Repository root path')
    parser.add_argument('--quick', action='store_true', help='Quick check only')
    parser.add_argument('--check-completeness', action='store_true', 
                       help='Check completeness percentage')
    parser.add_argument('--fail-on-warnings', action='store_true',
                       help='Fail if warnings are found')
    
    args = parser.parse_args()
    
    # Determine repository root
    root_path = Path(args.root).resolve()
    if not root_path.exists():
        print(f"Error: Path {root_path} does not exist")
        sys.exit(1)
    
    validator = ContextNodeValidator(str(root_path))
    
    if args.check_completeness:
        stats = validator.check_completeness()
        print(f"\n📊 Context Node Completeness Report:")
        print(f"  Total files: {stats['total']}")
        print(f"  Complete: {stats['complete']} ✅")
        print(f"  Partial: {stats['partial']} ⚠️")
        print(f"  Missing: {stats['missing']} ❌")
        print(f"  Completeness: {stats['completeness']:.1f}%")
        
        if stats['completeness'] < 80:
            print("\n⚠️  Warning: Less than 80% complete!")
            sys.exit(1 if args.fail_on_warnings else 0)
    else:
        is_valid = validator.validate_all()
        if not is_valid:
            sys.exit(1)

if __name__ == "__main__":
    import os
    main()
