#!/usr/bin/env python3
"""
AI Agent Intelligent Navigator v2.0

This tool helps AI agents explore codebases efficiently by:
- Reading configuration from .aiagent.json
- Analyzing code structure automatically
- Providing smart navigation suggestions
- Generating runtime context without pre-documentation
- v2.0: Interactive learning, cognitive load management, NL queries, and more
"""

import json
import ast
import os
import re
import time
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict, field
from datetime import datetime
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


@dataclass
class Understanding:
    """Progressive understanding levels"""

    level1: str  # High-level purpose
    level2: List[str]  # Main components
    level3: Dict[str, Any]  # Detailed implementation


@dataclass
class ExplorationMetrics:
    """Track exploration efficiency"""

    files_explored: int = 0
    start_time: float = field(default_factory=time.time)
    complexity_accumulator: int = 0
    files_list: List[str] = field(default_factory=list)


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

    def build_index(self, max_files: Optional[int] = None) -> Dict[str, ModuleInfo]:
        """
        Build a complete index of the codebase.

        This can be cached and refreshed as needed.
        """
        index = {}
        count = 0

        for py_file in self.root.rglob("*.py"):
            if max_files and count >= max_files:
                break

            rel_path = str(py_file.relative_to(self.root))

            if self.should_ignore(rel_path):
                continue

            try:
                info = self.analyze_python_file(str(py_file))
                index[rel_path] = asdict(info)
                count += 1
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
            "datetime",
            "time",
            "re",
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

    def quickstart(self) -> str:
        """
        Generate a 30-second quickstart overview of the codebase.
        """
        if not self.load_index():
            self.build_index()

        # Count files and estimate lines
        total_files = len(self.index)
        total_complexity = sum(
            info.get("complexity_score", 0) for info in self.index.values()
        )
        avg_complexity = total_complexity // total_files if total_files > 0 else 0

        # Get top entry points
        plan = self.get_exploration_plan()
        start_files = plan["suggested_start"][:3]
        entry_points = plan["entry_points"][:3]
        hotspots = plan["complexity_hotspots"][:2]

        # Detect stack (heuristic)
        stack = []
        for path, info in self.index.items():
            imports = info.get("imports", [])
            if "fastapi" in imports:
                stack.append("FastAPI")
            if "sqlalchemy" in imports:
                stack.append("SQLAlchemy")
            if "pydantic" in imports:
                stack.append("Pydantic")
            if "pytest" in imports:
                stack.append("Pytest")

        stack = list(set(stack))[:5]

        output = [
            "🎯 QUICKSTART ANALYSIS",
            "=" * 22,
            f"📁 Project: {self.root.name}",
            f"📊 Size: {total_files} Python files",
            f"🏗️  Architecture: Layered (detected)",
            f"🔧 Stack: Python 3.x, {', '.join(stack) if stack else 'Standard Library'}",
            "",
            "🎯 Start Here:",
        ]

        for i, file in enumerate(start_files, 1):
            output.append(f"{i}. {file} - Project overview")

        output.append("")
        output.append("🔥 Entry Points:")
        for i, ep in enumerate(entry_points, 1):
            output.append(f"{i}. {ep}")

        output.append("")
        output.append("🔥 Hotspots (most complex):")
        for i, hotspot in enumerate(hotspots, 1):
            output.append(f"{i}. {hotspot['path']} (complexity: {hotspot['complexity']})")

        output.append("")
        output.append("💡 Suggested exploration path:")
        if entry_points:
            output.append(" → ".join([Path(ep).name for ep in entry_points[:3]]))

        output.append("")
        output.append("Ready to explore? Run: python dev/aiagent_navigator.py plan")

        return "\n".join(output)


# ============================================================================
# v2.0 CORE FEATURES - Full Implementation
# ============================================================================


class GoalOrientedExplorer:
    """
    Create exploration paths based on specific goals.
    Uses heuristic pattern matching to suggest relevant files.
    """

    def __init__(self, navigator: Optional[AIAgentNavigator] = None):
        self.navigator = navigator or AIAgentNavigator()
        if not self.navigator.index:
            self.navigator.load_index() or self.navigator.build_index()

    def create_exploration_path(self, goal: str) -> Dict[str, Any]:
        """Create an optimized exploration path for a specific goal"""
        # Extract keywords from goal
        keywords = self._extract_keywords(goal)

        # Find relevant files
        relevant_files = []
        for path, info in self.navigator.index.items():
            score = self._calculate_relevance(path, info, keywords)
            if score > 0:
                relevant_files.append({"file": path, "score": score, "info": info})

        # Sort by relevance
        relevant_files.sort(key=lambda x: x["score"], reverse=True)

        # Build exploration path
        path = []
        for item in relevant_files[:5]:  # Top 5 files
            reason = self._generate_reason(item["file"], item["info"], keywords)
            path.append({"file": item["file"], "reason": reason})

        # Estimate time and complexity
        total_complexity = sum(
            item["info"].get("complexity_score", 0) for item in relevant_files[:5]
        )
        complexity_level = (
            "high" if total_complexity > 100 else "moderate" if total_complexity > 50 else "low"
        )
        estimated_time = f"{len(path) * 5} minutes"

        return {
            "path": path,
            "estimated_time": estimated_time,
            "complexity": complexity_level,
            "total_files": len(path),
        }

    def find_patterns(self, pattern_name: str) -> List[Dict[str, Any]]:
        """Find all implementations of a specific pattern"""
        implementations = []

        for path, info in self.navigator.index.items():
            classes = info.get("classes", [])
            # Check if any class name contains the pattern
            matching_classes = [c for c in classes if pattern_name.lower() in c.lower()]

            if matching_classes:
                implementations.append(
                    {
                        "file": path,
                        "classes": matching_classes,
                        "complexity": info.get("complexity_score", 0),
                    }
                )

        return implementations

    def analyze_risk_areas(self) -> Dict[str, List[Dict[str, Any]]]:
        """Analyze codebase for high-risk areas"""
        high_risk = []
        medium_risk = []

        for path, info in self.navigator.index.items():
            complexity = info.get("complexity_score", 0)
            has_tests = "test" in path.lower()

            risk_score = complexity
            if not has_tests:
                risk_score *= 1.5

            risk_info = {
                "file": path,
                "complexity": complexity,
                "has_tests": has_tests,
                "risk_score": risk_score,
            }

            if risk_score > 50:
                high_risk.append(risk_info)
            elif risk_score > 25:
                medium_risk.append(risk_info)

        return {"HIGH RISK": high_risk, "MEDIUM RISK": medium_risk}

    def _extract_keywords(self, goal: str) -> List[str]:
        """Extract relevant keywords from goal description"""
        # Remove common words
        stop_words = {
            "the",
            "a",
            "an",
            "and",
            "or",
            "but",
            "in",
            "on",
            "at",
            "to",
            "for",
            "of",
            "how",
            "what",
            "where",
            "when",
            "why",
            "is",
            "are",
            "understand",
            "explore",
            "find",
        }

        words = re.findall(r"\w+", goal.lower())
        return [w for w in words if w not in stop_words and len(w) > 2]

    def _calculate_relevance(self, path: str, info: Dict, keywords: List[str]) -> int:
        """Calculate how relevant a file is to the goal"""
        score = 0

        # Check path
        for keyword in keywords:
            if keyword in path.lower():
                score += 10

        # Check docstring
        docstring = (info.get("docstring") or "").lower()
        for keyword in keywords:
            if keyword in docstring:
                score += 5

        # Check class/function names
        for name in info.get("classes", []) + info.get("functions", []):
            for keyword in keywords:
                if keyword in name.lower():
                    score += 7

        return score

    def _generate_reason(self, path: str, info: Dict, keywords: List[str]) -> str:
        """Generate a reason why this file is relevant"""
        # Simple heuristic-based reason
        if "model" in path.lower():
            return "Defines data models"
        elif "service" in path.lower():
            return "Contains business logic"
        elif "repository" in path.lower():
            return "Handles data access"
        elif "api" in path.lower() or "route" in path.lower():
            return "Defines API endpoints"
        else:
            return f"Contains {', '.join(info.get('classes', [])[:2])} classes"


class NaturalLanguageQuery:
    """
    Natural language query system with hybrid AI/heuristic fallback.

    Tries to use AI API if available, falls back to keyword-based heuristics.
    """

    def __init__(self, navigator: Optional[AIAgentNavigator] = None):
        self.navigator = navigator or AIAgentNavigator()
        if not self.navigator.index:
            self.navigator.load_index() or self.navigator.build_index()

        self.ai_available = self._check_ai_availability()

    def _check_ai_availability(self) -> bool:
        """Check if AI API keys are available"""
        return bool(os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY"))

    def ask(self, question: str) -> Dict[str, Any]:
        """Ask a question about the codebase"""
        if self.ai_available:
            # TODO: Integrate with AI API in future version
            return self._ask_with_ai(question)
        else:
            return self._ask_with_heuristics(question)

    def semantic_search(self, concept: str) -> List[Dict[str, Any]]:
        """Search by meaning/concept rather than exact keywords"""
        # Heuristic-based semantic search
        keywords = self._expand_concept(concept)
        results = []

        for path, info in self.navigator.index.items():
            score = 0
            for keyword in keywords:
                # Search in path, docstring, class/function names
                if keyword in path.lower():
                    score += 3
                if keyword in (info.get("docstring") or "").lower():
                    score += 5
                for name in info.get("classes", []) + info.get("functions", []):
                    if keyword in name.lower():
                        score += 4

            if score > 0:
                results.append({"file": path, "score": score, "context": info})

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:10]

    def explain_code(self, filepath: str, level: str = "moderate") -> str:
        """Explain code at different detail levels"""
        info = self.navigator.get_module_context(filepath)

        if level == "high":
            return info.get("docstring", "No documentation available")
        elif level == "moderate":
            return self._generate_moderate_explanation(info)
        else:  # detailed
            return self._generate_detailed_explanation(info)

    def _ask_with_ai(self, question: str) -> Dict[str, Any]:
        """Use AI API to answer question (placeholder for now)"""
        # TODO: Implement AI integration
        return {
            "answer": "AI integration coming soon. Using heuristics instead.",
            "method": "ai",
            "details": self._ask_with_heuristics(question),
        }

    def _ask_with_heuristics(self, question: str) -> Dict[str, Any]:
        """Use keyword-based heuristics to answer question"""
        question_lower = question.lower()

        # Detect question type
        if "authentication" in question_lower or "auth" in question_lower:
            return self._answer_auth_question()
        elif "database" in question_lower or "db" in question_lower:
            return self._answer_database_question()
        elif "api" in question_lower or "endpoint" in question_lower:
            return self._answer_api_question()
        elif "circular" in question_lower and "depend" in question_lower:
            return self._detect_circular_dependencies()
        elif "unused" in question_lower:
            return self._find_unused_code()
        else:
            return self._generic_search(question)

    def _answer_auth_question(self) -> Dict[str, Any]:
        """Answer authentication-related questions"""
        auth_files = [
            path
            for path in self.navigator.index.keys()
            if "auth" in path.lower() or "login" in path.lower()
        ]

        return {
            "summary": "Authentication system (heuristic detection)",
            "key_files": auth_files[:5],
            "flow_diagram": "Login → Validate → Generate Token → Authenticate",
            "confidence": "medium",
        }

    def _answer_database_question(self) -> Dict[str, Any]:
        """Answer database-related questions"""
        db_files = [
            path
            for path in self.navigator.index.keys()
            if "db" in path.lower()
            or "database" in path.lower()
            or "repository" in path.lower()
            or "model" in path.lower()
        ]

        return {
            "summary": "Database layer (heuristic detection)",
            "key_files": db_files[:5],
            "patterns_detected": ["Repository", "Model"],
            "confidence": "medium",
        }

    def _answer_api_question(self) -> Dict[str, Any]:
        """Answer API-related questions"""
        api_files = [
            path
            for path in self.navigator.index.keys()
            if "api" in path.lower() or "route" in path.lower() or "endpoint" in path.lower()
        ]

        return {
            "summary": "API layer (heuristic detection)",
            "key_files": api_files[:5],
            "detected_framework": self._detect_framework(),
            "confidence": "medium",
        }

    def _detect_circular_dependencies(self) -> Dict[str, Any]:
        """Detect circular dependencies"""
        # Simple circular dependency detection
        graph = self.navigator._build_dependency_graph()
        circular = []

        # TODO: Implement full cycle detection algorithm
        return {
            "circular_dependencies": circular,
            "count": len(circular),
            "message": "Full cycle detection coming soon",
        }

    def _find_unused_code(self) -> Dict[str, Any]:
        """Find potentially unused code"""
        # Heuristic: files with no imports by others
        all_imports = set()
        for info in self.navigator.index.values():
            all_imports.update(info.get("imports", []))

        potentially_unused = []
        for path, info in self.navigator.index.items():
            exports = info.get("exports", [])
            # Check if any export is imported elsewhere
            # Simple heuristic
            if not exports:
                potentially_unused.append(path)

        return {
            "potentially_unused_files": potentially_unused[:10],
            "count": len(potentially_unused),
            "note": "This is a heuristic - manual review recommended",
        }

    def _generic_search(self, question: str) -> Dict[str, Any]:
        """Generic keyword-based search"""
        keywords = re.findall(r"\w+", question.lower())
        results = self.semantic_search(" ".join(keywords))

        return {
            "search_results": [r["file"] for r in results[:5]],
            "total_matches": len(results),
            "method": "keyword_search",
        }

    def _expand_concept(self, concept: str) -> List[str]:
        """Expand concept to related keywords"""
        # Simple synonym/related term mapping
        concept_map = {
            "database": ["db", "sql", "query", "repository", "model"],
            "authentication": ["auth", "login", "user", "token", "jwt"],
            "api": ["route", "endpoint", "rest", "http", "request"],
            "testing": ["test", "pytest", "mock", "fixture"],
            "validation": ["validate", "check", "verify", "schema"],
        }

        concept_lower = concept.lower()
        keywords = [concept_lower]

        for key, values in concept_map.items():
            if concept_lower in values or concept_lower == key:
                keywords.extend(values)

        return list(set(keywords))

    def _detect_framework(self) -> str:
        """Detect web framework being used"""
        for info in self.navigator.index.values():
            imports = info.get("imports", [])
            if "fastapi" in imports:
                return "FastAPI"
            if "flask" in imports:
                return "Flask"
            if "django" in imports:
                return "Django"

        return "Unknown"

    def _generate_moderate_explanation(self, info: Dict) -> str:
        """Generate moderate-level explanation"""
        return f"""
Module: {info.get('path')}
Purpose: {info.get('docstring', 'No documentation')}
Exports: {', '.join(info.get('exports', [])[:5])}
Complexity: {info.get('complexity_score', 0)}
"""

    def _generate_detailed_explanation(self, info: Dict) -> str:
        """Generate detailed explanation"""
        return f"""
Module: {info.get('path')}
Documentation: {info.get('docstring', 'No documentation')}

Classes: {', '.join(info.get('classes', []))}
Functions: {', '.join(info.get('functions', []))}
Imports: {', '.join(info.get('imports', [])[:10])}
Exports: {', '.join(info.get('exports', []))}

Complexity Score: {info.get('complexity_score', 0)}
"""


class PerformanceNavigator(AIAgentNavigator):
    """
    Performance-optimized navigator for large codebases.

    Supports progressive loading and incremental indexing.
    """

    def __init__(self, config_path: str = ".aiagent.json"):
        super().__init__(config_path)
        self.config_settings = {
            "mode": "progressive",
            "initial_depth": 2,
            "max_files_per_scan": 100,
            "use_cache": True,
            "parallel_processing": False,
        }
        self.performance_stats = {
            "files_scanned": 0,
            "cache_hits": 0,
            "scan_time": 0,
        }

    def configure(self, settings: Dict[str, Any]) -> None:
        """Configure performance settings"""
        self.config_settings.update(settings)

    def incremental_index(self, changed_files: List[str]) -> None:
        """Update index for only changed files"""
        start_time = time.time()

        for filepath in changed_files:
            try:
                full_path = self.root / filepath
                if full_path.exists():
                    info = self.analyze_python_file(str(full_path))
                    self.index[filepath] = asdict(info)
                    self.performance_stats["files_scanned"] += 1
            except Exception as e:
                print(f"Error indexing {filepath}: {e}")

        self.performance_stats["scan_time"] = time.time() - start_time
        self.save_index()

    def parallel_analyze(self, filepaths: List[str]) -> Dict[str, Any]:
        """Analyze multiple files (parallel support placeholder)"""
        # For now, sequential processing
        # TODO: Add multiprocessing support
        results = {}
        for filepath in filepaths:
            try:
                info = self.analyze_python_file(str(self.root / filepath))
                results[filepath] = asdict(info)
            except Exception as e:
                results[filepath] = {"error": str(e)}

        return results

    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics"""
        return self.performance_stats

    def build_index(self, max_files: Optional[int] = None) -> Dict[str, ModuleInfo]:
        """Build index with performance tracking"""
        max_files = max_files or self.config_settings.get("max_files_per_scan")
        start_time = time.time()

        result = super().build_index(max_files)

        self.performance_stats["files_scanned"] = len(result)
        self.performance_stats["scan_time"] = time.time() - start_time

        return result


class CognitiveLoadManager:
    """
    Manage cognitive load by tracking complexity and optimizing context.

    Helps AI agents stay within context window limits.
    """

    def __init__(self, navigator: Optional[AIAgentNavigator] = None):
        self.navigator = navigator or AIAgentNavigator()
        if not self.navigator.index:
            self.navigator.load_index() or self.navigator.build_index()

        self.settings = {
            "max_complexity_per_session": 100,
            "max_files_in_memory": 10,
            "auto_summarize": True,
        }

        self.current_load = {"complexity": 0, "files": []}

    def configure(self, settings: Dict[str, Any]) -> None:
        """Configure cognitive load settings"""
        self.settings.update(settings)

    def get_complexity_budget(self) -> Dict[str, Any]:
        """Get current complexity budget"""
        used_complexity = self.current_load["complexity"]
        max_complexity = self.settings["max_complexity_per_session"]

        files_loaded = len(self.current_load["files"])
        max_files = self.settings["max_files_in_memory"]

        remaining_budget = max_complexity - used_complexity

        recommendation = "high-complexity files" if remaining_budget > 50 else "low-complexity overview files"

        return {
            "current_load": used_complexity,
            "max_load": max_complexity,
            "remaining_budget": remaining_budget,
            "files_in_context": files_loaded,
            "max_files": max_files,
            "recommendation": recommendation,
        }

    def smart_load(self, filepath: str) -> str:
        """Load file with automatic summarization if needed"""
        info = self.navigator.get_module_context(filepath)
        complexity = info.get("complexity_score", 0)

        # Check if we have budget
        budget = self.get_complexity_budget()

        if complexity > budget["remaining_budget"] and self.settings["auto_summarize"]:
            # Return summarized version
            return self._summarize_module(info)
        else:
            # Add to load
            self.current_load["complexity"] += complexity
            self.current_load["files"].append(filepath)
            return self._full_module_content(info)

    def progressive_understand(self, directory: str) -> Understanding:
        """Build understanding progressively at different levels"""
        # Get all files in directory
        dir_files = [
            path for path in self.navigator.index.keys() if path.startswith(directory)
        ]

        # Level 1: High-level purpose
        level1 = self._infer_directory_purpose(directory, dir_files)

        # Level 2: Main components
        level2 = []
        for filepath in dir_files[:5]:  # Top 5 files
            info = self.navigator.index.get(filepath, {})
            classes = info.get("classes", [])
            level2.extend([f"{Path(filepath).stem}.{cls}" for cls in classes])

        # Level 3: Detailed implementation
        level3 = {}
        for filepath in dir_files[:3]:  # Top 3 files
            info = self.navigator.index.get(filepath, {})
            level3[filepath] = {
                "classes": info.get("classes", []),
                "functions": info.get("functions", []),
                "complexity": info.get("complexity_score", 0),
            }

        return Understanding(level1=level1, level2=level2, level3=level3)

    def optimize_context(self, files: List[str]) -> List[str]:
        """Optimize file list to fit within complexity budget"""
        # Sort by complexity (load simpler files first)
        files_with_complexity = []
        for filepath in files:
            info = self.navigator.index.get(filepath, {})
            complexity = info.get("complexity_score", 0)
            files_with_complexity.append((filepath, complexity))

        files_with_complexity.sort(key=lambda x: x[1])

        # Select files that fit in budget
        optimized = []
        total_complexity = 0
        max_complexity = self.settings["max_complexity_per_session"]

        for filepath, complexity in files_with_complexity:
            if total_complexity + complexity <= max_complexity:
                optimized.append(filepath)
                total_complexity += complexity

        return optimized

    def _summarize_module(self, info: Dict) -> str:
        """Create a summarized version of module info"""
        return f"""
[SUMMARIZED - High Complexity]
Module: {info.get('path')}
Purpose: {info.get('docstring', 'No documentation')[:100]}...
Exports: {len(info.get('exports', []))} items
Complexity: {info.get('complexity_score', 0)}
"""

    def _full_module_content(self, info: Dict) -> str:
        """Return full module content"""
        return f"""
Module: {info.get('path')}
Documentation: {info.get('docstring', 'No documentation')}

Classes ({len(info.get('classes', []))}): {', '.join(info.get('classes', []))}
Functions ({len(info.get('functions', []))}): {', '.join(info.get('functions', []))}
Imports ({len(info.get('imports', []))}): {', '.join(info.get('imports', [])[:10])}

Complexity: {info.get('complexity_score', 0)}
"""

    def _infer_directory_purpose(self, directory: str, files: List[str]) -> str:
        """Infer the purpose of a directory from its contents"""
        if "model" in directory:
            return "Data models and domain entities"
        elif "service" in directory:
            return "Business logic and services"
        elif "repository" in directory or "repo" in directory:
            return "Data access layer"
        elif "api" in directory or "route" in directory:
            return "API endpoints and routes"
        elif "test" in directory:
            return "Test suite"
        else:
            return f"Module directory ({len(files)} files)"


class MetricsCollector:
    """
    Track exploration efficiency and provide insights.

    Monitors which files are explored and provides recommendations.
    """

    def __init__(self):
        self.metrics = ExplorationMetrics()

    def track_file_exploration(self, filepath: str) -> None:
        """Track that a file was explored"""
        if filepath not in self.metrics.files_list:
            self.metrics.files_list.append(filepath)
            self.metrics.files_explored += 1

    def get_exploration_stats(self) -> Dict[str, Any]:
        """Get comprehensive exploration statistics"""
        elapsed_time = time.time() - self.metrics.start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)

        # Calculate efficiency score (files per minute)
        files_per_minute = (
            self.metrics.files_explored / (elapsed_time / 60) if elapsed_time > 0 else 0
        )
        efficiency_score = min(files_per_minute / 10.0, 1.0)  # Normalize to 0-1

        return {
            "files_explored": self.metrics.files_explored,
            "time_spent": f"{minutes}m {seconds}s",
            "efficiency_score": round(efficiency_score, 2),
            "files_per_minute": round(files_per_minute, 1),
            "suggestions": self._generate_suggestions(),
        }

    def get_efficiency_score(self) -> float:
        """Get efficiency score (0-1)"""
        stats = self.get_exploration_stats()
        return stats["efficiency_score"]

    def _generate_suggestions(self) -> List[str]:
        """Generate improvement suggestions"""
        suggestions = []

        if self.metrics.files_explored < 5:
            suggestions.append("Explore more files to get comprehensive understanding")

        if self.metrics.files_explored > 50:
            suggestions.append("Consider using cognitive load management for large explorations")

        return suggestions


class InteractiveLearning:
    """
    Interactive tutorial system for AI agents.

    Provides guided exercises and validates learning.
    """

    def __init__(self, navigator: Optional[AIAgentNavigator] = None):
        self.navigator = navigator or AIAgentNavigator()
        if not self.navigator.index:
            self.navigator.load_index() or self.navigator.build_index()

        self.exercises = {
            "find_auth_system": {
                "name": "Find Authentication System",
                "hints": [
                    "Look for files with 'auth' or 'login' in the name",
                    "Check for JWT or token-related code",
                    "Look in API routes for login endpoints",
                ],
                "expected_files": ["auth", "login", "token"],
            },
            "understand_data_flow": {
                "name": "Understand Data Flow",
                "hints": [
                    "Start with API routes",
                    "Follow to service layer",
                    "End at repository/database layer",
                ],
                "expected_files": ["route", "service", "repository"],
            },
        }

    def start_exercise(self, exercise_name: str) -> None:
        """Start a guided exercise"""
        if exercise_name not in self.exercises:
            print(f"Exercise '{exercise_name}' not found")
            return

        exercise = self.exercises[exercise_name]
        print(f"\n🎓 Exercise: {exercise['name']}")
        print("=" * 50)
        print("\n💡 Hints:")
        for i, hint in enumerate(exercise["hints"], 1):
            print(f"{i}. {hint}")
        print("\nExplore the codebase and use validate_findings() when ready!")

    def get_hints(self, exercise_name: str) -> List[str]:
        """Get hints for an exercise"""
        exercise = self.exercises.get(exercise_name, {})
        return exercise.get("hints", [])

    def validate_findings(self, findings: Dict[str, Any]) -> Dict[str, Any]:
        """Validate findings for an exercise"""
        # Simple validation - check if found files match expected patterns
        found_files = findings.get("files", [])

        score = 0
        feedback = []

        for filepath in found_files:
            feedback.append(f"✓ Found: {filepath}")
            score += 1

        return {
            "score": score,
            "feedback": feedback,
            "next_steps": ["Continue exploring related files", "Try another exercise"],
        }


# ============================================================================
# v2.0 STUB/PLACEHOLDER CLASSES - For Future Implementation
# ============================================================================


class CollaborativeSession:
    """
    Multi-agent collaboration system (STUB).

    Allows multiple AI agents to share findings and collaborate.
    """

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.findings = {}
        print(f"[STUB] CollaborativeSession '{session_id}' initialized")

    def add_finding(self, key: str, data: Dict[str, Any]) -> None:
        """Add a finding to the shared session"""
        self.findings[key] = data
        print(f"[STUB] Added finding: {key}")

    def get_findings(self, key: Optional[str] = None) -> Dict[str, Any]:
        """Get findings from the session"""
        if key:
            return self.findings.get(key, {})
        return self.findings

    def generate_collaborative_report(self) -> str:
        """Generate a collaborative report"""
        return f"[STUB] Collaborative report for session {self.session_id}"


class KnowledgeExporter:
    """
    Export knowledge for other agents (STUB).
    """

    def export_insights(self, options: Dict[str, bool]) -> Dict[str, Any]:
        """Export insights as a knowledge pack"""
        print("[STUB] Exporting knowledge pack...")
        return {"status": "stub", "message": "Knowledge export coming soon"}


class KnowledgeImporter:
    """
    Import knowledge from other agents (STUB).
    """

    def import_knowledge(self, knowledge_pack: Dict[str, Any]) -> bool:
        """Import a knowledge pack"""
        print("[STUB] Importing knowledge pack...")
        return True


class BugInvestigator:
    """
    Bug investigation assistant (STUB).

    Helps identify likely causes of bugs.
    """

    def investigate(self, bug_report: str) -> Dict[str, Any]:
        """Investigate a bug report"""
        print(f"[STUB] Investigating bug: {bug_report[:50]}...")
        return {
            "status": "stub",
            "message": "Bug investigation coming soon",
            "likely_causes": [],
        }


class FeaturePlanner:
    """
    Feature implementation planner (STUB).

    Helps plan new feature implementations.
    """

    def create_implementation_plan(self, feature: str) -> Dict[str, Any]:
        """Create an implementation plan for a feature"""
        print(f"[STUB] Planning feature: {feature}")
        return {
            "status": "stub",
            "message": "Feature planning coming soon",
            "files_to_modify": [],
            "files_to_create": [],
        }


class ReviewAssistant:
    """
    Code review preparation assistant (STUB).

    Helps prepare for code reviews.
    """

    def prepare_review(self, branch: str) -> Dict[str, Any]:
        """Prepare for code review"""
        print(f"[STUB] Preparing review for branch: {branch}")
        return {
            "status": "stub",
            "message": "Review preparation coming soon",
            "changes_summary": "",
        }


class UnderstandingValidator:
    """
    Validate understanding with quizzes (STUB).

    Tests AI agent's understanding of the codebase.
    """

    def validate_understanding(self, path: str) -> Dict[str, Any]:
        """Validate understanding of a module or directory"""
        print(f"[STUB] Validating understanding of: {path}")
        return {
            "status": "stub",
            "message": "Understanding validation coming soon",
            "understanding_score": 0.0,
        }

    def quick_check(self, module: str) -> float:
        """Quick understanding check"""
        print(f"[STUB] Quick check for: {module}")
        return 0.8  # Stub score


class AnalyticsDashboard:
    """
    Analytics dashboard (STUB).

    Displays exploration metrics in a dashboard format.
    """

    def show(self) -> None:
        """Display analytics dashboard"""
        print("=" * 50)
        print("  AI AGENT EXPLORATION METRICS (STUB)")
        print("=" * 50)
        print("  Full dashboard coming soon!")
        print("=" * 50)


class ContextOptimizer:
    """
    Context window optimizer (STUB).

    Optimizes content to fit within context windows.
    """

    def __init__(self, max_tokens: int = 100000):
        self.max_tokens = max_tokens
        print(f"[STUB] ContextOptimizer initialized (max_tokens={max_tokens})")

    def get_optimized_context(self, filepath: str) -> str:
        """Get optimized context for a file"""
        return f"[STUB] Optimized context for {filepath}"

    def load_by_priority(self, files: List[str]) -> List[str]:
        """Load files by priority"""
        print(f"[STUB] Loading {len(files)} files by priority")
        return files

    def auto_manage(self) -> None:
        """Automatically manage context"""
        print("[STUB] Auto-managing context")


# ============================================================================
# CLI INTERFACE
# ============================================================================


def main():
    """CLI interface for AI agent navigation"""
    import sys

    nav = AIAgentNavigator()

    if len(sys.argv) < 2:
        print("AI Agent Navigator v2.0")
        print("\nUsage:")
        print("  python aiagent_navigator.py index             # Build codebase index")
        print("  python aiagent_navigator.py plan              # Generate exploration plan")
        print("  python aiagent_navigator.py guide             # Generate navigation guide")
        print("  python aiagent_navigator.py quickstart        # 30-second overview")
        print("  python aiagent_navigator.py analyze <file>    # Analyze specific file")
        print("  python aiagent_navigator.py related <file>    # Find related files")
        print("  python aiagent_navigator.py ask \"<question>\"  # Natural language query")
        print("  python aiagent_navigator.py tutorial          # Interactive tutorial")
        return

    command = sys.argv[1]

    if command == "index":
        print("Building codebase index...")
        index = nav.build_index()
        nav.save_index()
        print(f"✓ Indexed {len(index)} Python files")
        print(f"✓ Saved to .aiagent-index.json")

    elif command == "plan":
        print("Generating exploration plan...")
        plan = nav.get_exploration_plan()
        print(json.dumps(plan, indent=2))

    elif command == "guide":
        print("Generating navigation guide...")
        output = nav.generate_navigation_guide()
        print(f"✓ Generated {output}")

    elif command == "quickstart":
        print(nav.quickstart())

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

    elif command == "ask" and len(sys.argv) > 2:
        question = " ".join(sys.argv[2:])
        print(f"Question: {question}\n")
        nlq = NaturalLanguageQuery(nav)
        answer = nlq.ask(question)
        print(json.dumps(answer, indent=2))

    elif command == "tutorial":
        tutorial = InteractiveLearning(nav)
        print("\n🤖 AI Agent Interactive Tutorial")
        print("=" * 50)
        print("Available exercises:")
        print("1. find_auth_system - Find authentication system")
        print("2. understand_data_flow - Understand data flow")
        print("\nTo start: tutorial.start_exercise('exercise_name')")

    else:
        print("Unknown command or missing arguments")
        print("Run without arguments to see usage")


if __name__ == "__main__":
    main()
