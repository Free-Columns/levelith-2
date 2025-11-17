#!/usr/bin/env python3
"""
Example: How an AI Agent Would Use the Intelligent Navigator

This demonstrates a simulated AI agent exploring a codebase using
the intelligent tooling instead of pre-generated context nodes.
"""

from aiagent_navigator import AIAgentNavigator
import json


class SimulatedAIAgent:
    """
    Simulates an AI agent exploring a codebase intelligently.

    This shows how an AI would use the navigator to understand
    a project without pre-existing documentation.
    """

    def __init__(self):
        self.navigator = AIAgentNavigator()
        self.knowledge = {}
        self.exploration_log = []

    def log(self, message: str):
        """Log exploration steps"""
        print(f"[AI Agent] {message}")
        self.exploration_log.append(message)

    def explore_codebase(self):
        """Main exploration workflow"""
        self.log("Starting codebase exploration...")

        # Step 1: Load exploration plan
        self.log("\n=== Step 1: Loading Exploration Plan ===")
        plan = self.navigator.get_exploration_plan()

        self.log(f"Suggested starting points: {plan['suggested_start']}")
        self.log(f"Entry points found: {plan['entry_points']}")
        self.log(f"Key modules: {len(plan['key_modules'])} identified")

        # Step 2: Examine key modules
        self.log("\n=== Step 2: Analyzing Key Modules ===")
        for module in plan['key_modules'][:3]:  # Top 3
            self._examine_module(module['path'])

        # Step 3: Follow dependencies
        self.log("\n=== Step 3: Following Dependencies ===")
        if plan['entry_points']:
            entry = plan['entry_points'][0]
            self._explore_dependencies(entry)

        # Step 4: Identify patterns
        self.log("\n=== Step 4: Identifying Patterns ===")
        self._identify_patterns(plan)

        # Step 5: Generate summary
        self.log("\n=== Step 5: Generating Summary ===")
        return self._generate_summary()

    def _examine_module(self, filepath: str):
        """Examine a specific module in detail"""
        self.log(f"\nExamining: {filepath}")

        context = self.navigator.get_module_context(filepath)

        # Store in knowledge base
        self.knowledge[filepath] = context

        # Log what we learned
        if context.get('docstring'):
            self.log(f"  Purpose: {context['docstring'][:100]}...")

        if context.get('classes'):
            self.log(f"  Classes: {', '.join(context['classes'])}")

        if context.get('functions'):
            self.log(f"  Functions: {', '.join(context['functions'][:5])}")
            if len(context['functions']) > 5:
                self.log(f"    ... and {len(context['functions']) - 5} more")

        if context.get('imports'):
            self.log(f"  Dependencies: {len(context['imports'])} imports")

        self.log(f"  Complexity: {context.get('complexity_score', 0)}")

    def _explore_dependencies(self, filepath: str):
        """Explore files related to a given file"""
        self.log(f"\nExploring dependencies of: {filepath}")

        related = self.navigator.suggest_related_files(filepath)

        if not related:
            self.log("  No related internal files found (standalone module)")
            return

        for item in related:
            self.log(f"  Related: {item['path']}")
            self.log(f"    Reason: {item['reason']}")
            self.log(f"    Strength: {item['score']}")

    def _identify_patterns(self, plan):
        """Identify architectural patterns"""
        self.log("\nIdentifying patterns...")

        # Check for common patterns
        dependency_graph = plan.get('dependency_graph', {})

        # Count files with many dependencies
        high_dependency_files = [
            (path, len(deps))
            for path, deps in dependency_graph.items()
            if len(deps) > 3
        ]

        if high_dependency_files:
            self.log("  Found files with many dependencies:")
            for path, count in sorted(high_dependency_files, key=lambda x: x[1], reverse=True)[:3]:
                self.log(f"    {path}: {count} dependencies")

        # Check for complexity hotspots
        hotspots = plan.get('complexity_hotspots', [])
        if hotspots:
            self.log("  Complexity hotspots identified:")
            for hs in hotspots[:3]:
                self.log(f"    {hs['path']}: complexity {hs['complexity']}")

    def _generate_summary(self) -> dict:
        """Generate summary of understanding"""
        summary = {
            "files_examined": len(self.knowledge),
            "total_classes": sum(
                len(info.get('classes', []))
                for info in self.knowledge.values()
            ),
            "total_functions": sum(
                len(info.get('functions', []))
                for info in self.knowledge.values()
            ),
            "average_complexity": sum(
                info.get('complexity_score', 0)
                for info in self.knowledge.values()
            ) / max(len(self.knowledge), 1),
            "exploration_steps": len(self.exploration_log)
        }

        self.log(f"\nSummary:")
        self.log(f"  Files examined: {summary['files_examined']}")
        self.log(f"  Total classes found: {summary['total_classes']}")
        self.log(f"  Total functions found: {summary['total_functions']}")
        self.log(f"  Average complexity: {summary['average_complexity']:.1f}")
        self.log(f"  Exploration steps: {summary['exploration_steps']}")

        return summary


class AIAgentQueryInterface:
    """
    Interface for AI agents to ask questions about the codebase.

    Instead of reading pre-generated docs, AI can query on-demand.
    """

    def __init__(self):
        self.navigator = AIAgentNavigator()
        self.navigator.load_index()  # Load cached index if available

    def where_is_function(self, function_name: str) -> list:
        """Find where a function is defined"""
        results = []

        for filepath, info in self.navigator.index.items():
            if function_name in info.get('functions', []):
                results.append({
                    'file': filepath,
                    'context': info.get('docstring', 'No documentation'),
                    'complexity': info.get('complexity_score', 0)
                })

        return results

    def where_is_class(self, class_name: str) -> list:
        """Find where a class is defined"""
        results = []

        for filepath, info in self.navigator.index.items():
            if class_name in info.get('classes', []):
                results.append({
                    'file': filepath,
                    'context': info.get('docstring', 'No documentation'),
                    'other_classes': info.get('classes', [])
                })

        return results

    def what_imports_module(self, module_name: str) -> list:
        """Find what files import a given module"""
        results = []

        for filepath, info in self.navigator.index.items():
            imports = info.get('imports', [])
            if module_name in imports or any(module_name in imp for imp in imports):
                results.append({
                    'file': filepath,
                    'all_imports': imports
                })

        return results

    def what_does_file_export(self, filepath: str) -> dict:
        """Get all exports from a file"""
        context = self.navigator.get_module_context(filepath)
        return {
            'exports': context.get('exports', []),
            'classes': context.get('classes', []),
            'functions': context.get('functions', []),
            'description': context.get('docstring', 'No documentation')
        }

    def get_complexity_overview(self) -> dict:
        """Get overview of codebase complexity"""
        if not self.navigator.index:
            self.navigator.build_index()

        total_files = len(self.navigator.index)
        total_complexity = sum(
            info.get('complexity_score', 0)
            for info in self.navigator.index.values()
        )

        return {
            'total_files': total_files,
            'total_complexity': total_complexity,
            'average_complexity': total_complexity / max(total_files, 1),
            'hotspots': self.navigator._find_complexity_hotspots()[:5]
        }


def demo_ai_exploration():
    """Demonstrate AI agent using the intelligent navigator"""
    print("=" * 60)
    print("AI AGENT INTELLIGENT CODEBASE EXPLORATION DEMO")
    print("=" * 60)

    agent = SimulatedAIAgent()
    summary = agent.explore_codebase()

    print("\n" + "=" * 60)
    print("AI AGENT QUERY INTERFACE DEMO")
    print("=" * 60)

    query = AIAgentQueryInterface()

    # Example queries
    print("\n[Query 1] What does 'dev/cn-create.py' export?")
    try:
        exports = query.what_does_file_export('dev/cn-create.py')
        print(json.dumps(exports, indent=2))
    except Exception as e:
        print(f"  File not in index yet: {e}")

    print("\n[Query 2] Get complexity overview")
    try:
        overview = query.get_complexity_overview()
        print(f"  Total files: {overview['total_files']}")
        print(f"  Average complexity: {overview['average_complexity']:.1f}")
        if overview['hotspots']:
            print(f"  Top hotspot: {overview['hotspots'][0]['path']}")
    except Exception as e:
        print(f"  Error: {e}")

    print("\n" + "=" * 60)
    print("BENEFITS OVER STATIC CONTEXT NODES")
    print("=" * 60)
    print("""
1. ✓ No duplicate files to maintain
2. ✓ Always in sync with actual code
3. ✓ On-demand analysis (only analyze what's needed)
4. ✓ Query interface for specific questions
5. ✓ Automatic complexity analysis
6. ✓ Dependency graph generation
7. ✓ Can be cached and refreshed easily
8. ✓ Works with any codebase without setup
    """)


if __name__ == "__main__":
    demo_ai_exploration()
