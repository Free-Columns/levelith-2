#!/usr/bin/env python3
"""
AI Agent Intelligent Navigator

This tool helps AI agents explore codebases efficiently by:
- Reading configuration from .aiagent.json
- Analyzing code structure automatically
- Providing smart navigation suggestions
- Generating runtime context without pre-documentation
"""

import json
import ast
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import fnmatch


@dataclass
class ModuleInfo:
    """Information extracted from a Python module"""

    path: str
    docstring: Optional[str]
    classes: List[str]
    functions: List[str]
    imports: List[str]
    exports: List[str]
    complexity_score: int


class AIAgentNavigator:
    """
    Intelligent navigation system for AI agents.

    Provides dynamic codebase understanding without pre-generated documentation.
    """

    def __init__(self, config_path: str = ".aiagent.json"):
        self.root = Path.cwd()
        self.config = self._load_config(config_path)
        self.index = {}

    def _load_config(self, config_path: str) -> Dict:
        """Load AI agent configuration"""
        path = self.root / config_path
        if path.exists():
            with open(path) as f:
                return json.load(f)
        return self._default_config()

    def _default_config(self) -> Dict:
        """Default configuration if none exists"""
        return {
            "navigation": {
                "entry_points": ["main.py", "app.py", "cli.py"],
                "ignore_patterns": ["**/__pycache__/**", "**/*.pyc"],
            },
            "exploration_hints": {
                "start_here": ["README.md"],
                "dependency_strategy": "follow_imports",
            },
        }

    def get_entry_points(self) -> List[str]:
        """Get recommended starting points for exploration"""
        entry_points = self.config.get("navigation", {}).get("entry_points", [])
        existing = []

        for ep in entry_points:
            path = self.root / ep
            if path.exists():
                existing.append(str(path))

        return existing

    def should_ignore(self, path: str) -> bool:
        """Check if path should be ignored based on patterns"""
        ignore_patterns = self.config.get("navigation", {}).get("ignore_patterns", [])

        for pattern in ignore_patterns:
            if fnmatch.fnmatch(path, pattern):
                return True

        return False

    def analyze_python_file(self, filepath: str) -> ModuleInfo:
        """
        Extract comprehensive information from a Python file.

        This is the core intelligence - extracting structure on-demand
        rather than maintaining pre-generated documentation.
        """
        with open(filepath) as f:
            try:
                tree = ast.parse(f.read(), filename=filepath)
            except SyntaxError:
                return ModuleInfo(
                    path=filepath,
                    docstring=None,
                    classes=[],
                    functions=[],
                    imports=[],
                    exports=[],
                    complexity_score=0,
                )

        # Extract module docstring
        docstring = ast.get_docstring(tree)

        # Extract classes
        classes = [
            node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)
        ]

        # Extract functions (excluding methods)
        functions = [
            node.name for node in tree.body if isinstance(node, ast.FunctionDef)
        ]

        # Extract imports
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend([alias.name for alias in node.names])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)

        # Extract exports (functions/classes defined at module level)
        exports = classes + functions

        # Calculate complexity (simple metric)
        complexity = len(classes) * 3 + len(functions) * 2 + len(imports)

        return ModuleInfo(
            path=filepath,
            docstring=docstring,
            classes=classes,
            functions=functions,
            imports=imports,
            exports=exports,
            complexity_score=complexity,
        )

    def build_index(self) -> Dict[str, ModuleInfo]:
        """
        Build a complete index of the codebase.

        This can be cached and refreshed as needed.
        """
        index = {}

        for py_file in self.root.rglob("*.py"):
            rel_path = str(py_file.relative_to(self.root))

            if self.should_ignore(rel_path):
                continue

            try:
                info = self.analyze_python_file(str(py_file))
                index[rel_path] = asdict(info)
            except Exception as e:
                print(f"Warning: Could not analyze {rel_path}: {e}")

        self.index = index
        return index

    def save_index(self, output_path: str = ".aiagent-index.json"):
        """Save index for quick loading"""
        with open(self.root / output_path, "w") as f:
            json.dump(self.index, f, indent=2)

    def load_index(self, index_path: str = ".aiagent-index.json"):
        """Load pre-built index"""
        path = self.root / index_path
        if path.exists():
            with open(path) as f:
                self.index = json.load(f)
                return True
        return False

    def get_exploration_plan(self) -> Dict[str, Any]:
        """
        Generate a smart exploration plan for AI agents.

        Returns suggested reading order and key insights.
        """
        # Try to load existing index, otherwise build it
        if not self.load_index():
            self.build_index()

        plan = {
            "suggested_start": self.config.get("exploration_hints", {}).get(
                "start_here", []
            ),
            "entry_points": self.get_entry_points(),
            "key_modules": self._identify_key_modules(),
            "dependency_graph": self._build_dependency_graph(),
            "complexity_hotspots": self._find_complexity_hotspots(),
            "exploration_strategy": self.config.get("exploration_hints", {}).get(
                "preferred_approach", "breadth_first"
            ),
        }

        return plan

    def _identify_key_modules(self) -> List[Dict[str, Any]]:
        """Identify the most important modules based on connections and exports"""
        key_modules = []

        for path, info in self.index.items():
            # Modules with high export count are likely important
            export_count = len(info.get("exports", []))

            if export_count > 3 or info.get("complexity_score", 0) > 15:
                key_modules.append(
                    {
                        "path": path,
                        "reason": f"{export_count} exports, complexity: {info.get('complexity_score')}",
                        "exports": info.get("exports", []),
                        "docstring": info.get("docstring", "No documentation")[:100],
                    }
                )

        # Sort by complexity score
        key_modules.sort(
            key=lambda x: self.index[x["path"]].get("complexity_score", 0), reverse=True
        )

        return key_modules[:10]  # Top 10

    def _build_dependency_graph(self) -> Dict[str, List[str]]:
        """Build import dependency graph"""
        graph = {}

        for path, info in self.index.items():
            imports = info.get("imports", [])
            # Only track internal imports (not external packages)
            internal_imports = [
                imp for imp in imports if not self._is_external_package(imp)
            ]
            graph[path] = internal_imports

        return graph

    def _is_external_package(self, module_name: str) -> bool:
        """Check if import is external package"""
        # Simple heuristic: if it's not in our codebase, it's external
        common_external = [
            "os",
            "sys",
            "json",
            "ast",
            "pathlib",
            "typing",
            "dataclasses",
        ]
        return module_name.split(".")[0] in common_external

    def _find_complexity_hotspots(self) -> List[Dict[str, Any]]:
        """Find files with high complexity that might need attention"""
        hotspots = []

        for path, info in self.index.items():
            score = info.get("complexity_score", 0)
            if score > 20:
                hotspots.append(
                    {
                        "path": path,
                        "complexity": score,
                        "classes": len(info.get("classes", [])),
                        "functions": len(info.get("functions", [])),
                        "imports": len(info.get("imports", [])),
                    }
                )

        hotspots.sort(key=lambda x: x["complexity"], reverse=True)
        return hotspots

    def get_module_context(self, filepath: str) -> Dict[str, Any]:
        """
        Get rich context for a specific module.

        AI agents can call this on-demand for any file they're examining.
        """
        if filepath not in self.index:
            # Analyze on the fly
            info = self.analyze_python_file(str(self.root / filepath))
            return asdict(info)

        return self.index[filepath]

    def suggest_related_files(
        self, filepath: str, max_suggestions: int = 5
    ) -> List[str]:
        """
        Suggest related files based on imports and exports.

        Helps AI agents navigate relationships without pre-documentation.
        """
        if filepath not in self.index:
            return []

        current_info = self.index[filepath]
        current_imports = set(current_info.get("imports", []))
        current_exports = set(current_info.get("exports", []))

        related = []

        for path, info in self.index.items():
            if path == filepath:
                continue

            # Check if this file imports what current file exports
            other_imports = set(info.get("imports", []))
            other_exports = set(info.get("exports", []))

            # Calculate relatedness score
            import_overlap = len(current_imports & other_imports)
            export_usage = len(current_exports & other_imports)
            import_usage = len(other_exports & current_imports)

            score = import_overlap + (export_usage * 2) + (import_usage * 2)

            if score > 0:
                related.append(
                    {
                        "path": path,
                        "score": score,
                        "reason": self._explain_relation(
                            export_usage, import_usage, import_overlap
                        ),
                    }
                )

        # Sort by score and return top suggestions
        related.sort(key=lambda x: x["score"], reverse=True)
        return related[:max_suggestions]

    def _explain_relation(
        self, export_usage: int, import_usage: int, import_overlap: int
    ) -> str:
        """Explain why files are related"""
        reasons = []
        if export_usage > 0:
            reasons.append(f"imports {export_usage} of this file's exports")
        if import_usage > 0:
            reasons.append(f"exports {import_usage} items this file imports")
        if import_overlap > 0:
            reasons.append(f"shares {import_overlap} common imports")
        return ", ".join(reasons)

    def generate_navigation_guide(self, output_path: str = "NAVIGATION.md"):
        """Generate a markdown navigation guide from the index"""
        plan = self.get_exploration_plan()

        guide = ["# AI Agent Navigation Guide", ""]
        guide.append("*Auto-generated from codebase analysis*")
        guide.append("")

        # Entry points
        guide.append("## Entry Points")
        guide.append("")
        for ep in plan["entry_points"]:
            guide.append(f"- `{ep}`")
        guide.append("")

        # Key modules
        guide.append("## Key Modules")
        guide.append("")
        for module in plan["key_modules"]:
            guide.append(f"### `{module['path']}`")
            guide.append(f"- **Reason**: {module['reason']}")
            if module["exports"]:
                guide.append(f"- **Exports**: {', '.join(module['exports'])}")
            if module["docstring"]:
                guide.append(f"- **Description**: {module['docstring']}")
            guide.append("")

        # Complexity hotspots
        guide.append("## Complexity Hotspots")
        guide.append("")
        for hotspot in plan["complexity_hotspots"]:
            guide.append(f"- `{hotspot['path']}` (complexity: {hotspot['complexity']})")
        guide.append("")

        # Write to file
        with open(self.root / output_path, "w") as f:
            f.write("\n".join(guide))

        return output_path


def main():
    """CLI interface for AI agent navigation"""
    import sys

    nav = AIAgentNavigator()

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python aiagent_navigator.py index          # Build codebase index")
        print(
            "  python aiagent_navigator.py plan           # Generate exploration plan"
        )
        print(
            "  python aiagent_navigator.py guide          # Generate navigation guide"
        )
        print("  python aiagent_navigator.py analyze <file> # Analyze specific file")
        print("  python aiagent_navigator.py related <file> # Find related files")
        return

    command = sys.argv[1]

    if command == "index":
        print("Building codebase index...")
        index = nav.build_index()
        nav.save_index()
        print(f"Indexed {len(index)} Python files")
        print(f"Saved to .aiagent-index.json")

    elif command == "plan":
        print("Generating exploration plan...")
        plan = nav.get_exploration_plan()
        print(json.dumps(plan, indent=2))

    elif command == "guide":
        print("Generating navigation guide...")
        output = nav.generate_navigation_guide()
        print(f"Generated {output}")

    elif command == "analyze" and len(sys.argv) > 2:
        filepath = sys.argv[2]
        print(f"Analyzing {filepath}...")
        context = nav.get_module_context(filepath)
        print(json.dumps(context, indent=2))

    elif command == "related" and len(sys.argv) > 2:
        filepath = sys.argv[2]
        print(f"Finding files related to {filepath}...")
        nav.build_index()  # Ensure index exists
        related = nav.suggest_related_files(filepath)
        for item in related:
            print(f"\n{item['path']} (score: {item['score']})")
            print(f"  Reason: {item['reason']}")

    else:
        print("Unknown command or missing arguments")


if __name__ == "__main__":
    main()
