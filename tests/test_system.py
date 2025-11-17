"""
Levelith-2 Internal Test System

This module provides a comprehensive testing framework for all code changes.
Every AI-assisted change MUST include corresponding tests.

Golden Rule: No code ships without tests.
"""

import pytest
import unittest
from typing import Any, Callable, Dict, List
from pathlib import Path
import json
import ast


class TestRequirement:
    """Enforces test coverage requirements for AI-assisted changes"""

    MINIMUM_COVERAGE = 80  # 80% minimum coverage
    REQUIRE_INTEGRATION_TESTS = True
    REQUIRE_UNIT_TESTS = True

    @staticmethod
    def validate_test_exists(module_path: str) -> bool:
        """
        Validate that tests exist for a given module.

        Args:
            module_path: Path to the module being tested

        Returns:
            bool: True if tests exist, False otherwise
        """
        path = Path(module_path)
        test_path = Path("tests") / f"test_{path.name}"

        return test_path.exists()

    @staticmethod
    def validate_coverage(module_path: str, coverage_data: Dict) -> bool:
        """
        Validate that module meets coverage requirements.

        Args:
            module_path: Path to the module
            coverage_data: Coverage report data

        Returns:
            bool: True if meets requirements, False otherwise
        """
        if module_path not in coverage_data:
            return False

        coverage_pct = coverage_data[module_path].get("coverage", 0)
        return coverage_pct >= TestRequirement.MINIMUM_COVERAGE


class TestGenerator:
    """
    Automatically generate test templates for new code.

    AI agents should use this to scaffold tests for new modules.
    """

    @staticmethod
    def generate_unit_test_template(module_path: str) -> str:
        """
        Generate a unit test template for a module.

        Args:
            module_path: Path to the module to test

        Returns:
            str: Test template code
        """
        path = Path(module_path)
        module_name = path.stem

        # Analyze the module
        with open(path) as f:
            tree = ast.parse(f.read())

        # Extract classes and functions
        classes = [
            node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)
        ]
        functions = [
            node.name
            for node in tree.body
            if isinstance(node, ast.FunctionDef) and not node.name.startswith("_")
        ]

        template = f'''"""
Unit tests for {module_name}.py

Auto-generated test template. AI agents should fill in test cases.
"""

import pytest
from {module_name} import {", ".join(classes + functions) if classes or functions else "*"}


class Test{module_name.title().replace("_", "")}:
    """Test suite for {module_name} module"""

    def setup_method(self):
        """Set up test fixtures"""
        pass

    def teardown_method(self):
        """Clean up after tests"""
        pass

'''

        # Generate test stubs for each class
        for cls in classes:
            template += f'''
    def test_{cls.lower()}_initialization(self):
        """Test {cls} initialization"""
        # TODO: Implement test
        pytest.skip("Test not implemented yet")

    def test_{cls.lower()}_methods(self):
        """Test {cls} methods"""
        # TODO: Implement test
        pytest.skip("Test not implemented yet")

'''

        # Generate test stubs for each function
        for func in functions:
            template += f'''
    def test_{func}(self):
        """Test {func} function"""
        # TODO: Implement test
        pytest.skip("Test not implemented yet")

'''

        template += '''
    def test_error_handling(self):
        """Test error handling"""
        # TODO: Implement error handling tests
        pytest.skip("Test not implemented yet")

    def test_edge_cases(self):
        """Test edge cases"""
        # TODO: Implement edge case tests
        pytest.skip("Test not implemented yet")
'''

        return template

    @staticmethod
    def generate_integration_test_template(feature_name: str) -> str:
        """
        Generate an integration test template.

        Args:
            feature_name: Name of the feature to test

        Returns:
            str: Integration test template
        """
        template = f'''"""
Integration tests for {feature_name}

Tests the complete workflow and interactions between components.
"""

import pytest
from pathlib import Path
import json


class Test{feature_name.title().replace("_", "")}Integration:
    """Integration test suite for {feature_name}"""

    @pytest.fixture
    def setup_environment(self):
        """Set up test environment"""
        # TODO: Set up test environment
        yield
        # TODO: Clean up

    def test_complete_workflow(self, setup_environment):
        """Test the complete {feature_name} workflow"""
        # TODO: Implement workflow test
        pytest.skip("Test not implemented yet")

    def test_component_integration(self, setup_environment):
        """Test integration between components"""
        # TODO: Implement integration test
        pytest.skip("Test not implemented yet")

    def test_data_flow(self, setup_environment):
        """Test data flow through the system"""
        # TODO: Implement data flow test
        pytest.skip("Test not implemented yet")

    def test_error_propagation(self, setup_environment):
        """Test error handling across components"""
        # TODO: Implement error propagation test
        pytest.skip("Test not implemented yet")
'''

        return template


class TestValidator:
    """
    Validates that tests meet quality requirements.

    Used in CI/CD to ensure test quality.
    """

    @staticmethod
    def validate_test_file(test_path: str) -> Dict[str, Any]:
        """
        Validate a test file meets quality standards.

        Args:
            test_path: Path to test file

        Returns:
            Dict with validation results
        """
        results = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "test_count": 0,
            "has_setup": False,
            "has_teardown": False,
            "has_fixtures": False,
        }

        try:
            with open(test_path) as f:
                tree = ast.parse(f.read())

            # Count test functions
            test_functions = [
                node.name
                for node in ast.walk(tree)
                if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")
            ]
            results["test_count"] = len(test_functions)

            if results["test_count"] == 0:
                results["valid"] = False
                results["errors"].append("No test functions found")

            # Check for setup/teardown
            all_functions = [
                node.name
                for node in ast.walk(tree)
                if isinstance(node, ast.FunctionDef)
            ]
            results["has_setup"] = any("setup" in f.lower() for f in all_functions)
            results["has_teardown"] = any(
                "teardown" in f.lower() for f in all_functions
            )

            # Check for pytest.skip usage (should be minimal)
            skip_count = sum(
                1
                for node in ast.walk(tree)
                if isinstance(node, ast.Call)
                and hasattr(node.func, "attr")
                and node.func.attr == "skip"
            )

            if skip_count > results["test_count"] * 0.5:
                results["warnings"].append(
                    f"More than 50% of tests are skipped ({skip_count}/{results['test_count']})"
                )

        except Exception as e:
            results["valid"] = False
            results["errors"].append(f"Failed to parse test file: {str(e)}")

        return results

    @staticmethod
    def validate_test_coverage(coverage_file: str, threshold: float = 80.0) -> bool:
        """
        Validate test coverage meets threshold.

        Args:
            coverage_file: Path to coverage report
            threshold: Minimum coverage percentage

        Returns:
            bool: True if coverage meets threshold
        """
        try:
            with open(coverage_file) as f:
                coverage_data = json.load(f)

            total_coverage = coverage_data.get("totals", {}).get("percent_covered", 0)
            return total_coverage >= threshold

        except Exception:
            return False


def enforce_test_requirements():
    """
    Enforce test requirements before allowing commits.

    This should be called in pre-commit hooks.
    """
    print("Enforcing test requirements...")

    # Check for new/modified Python files
    import subprocess

    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=AM"],
        capture_output=True,
        text=True,
    )

    modified_files = [f for f in result.stdout.split("\n") if f.endswith(".py")]
    modified_files = [
        f for f in modified_files if not f.startswith("tests/") and "test_" not in f
    ]

    if not modified_files:
        print("✓ No Python files modified")
        return True

    print(f"Found {len(modified_files)} modified Python files")

    all_tests_exist = True
    for file in modified_files:
        if TestRequirement.validate_test_exists(file):
            print(f"✓ Tests exist for {file}")
        else:
            print(f"✗ No tests found for {file}")
            print(f"  Create tests/test_{Path(file).name}")
            all_tests_exist = False

    if not all_tests_exist:
        print("\n❌ Test requirement not met!")
        print("Golden Rule: Every code change MUST have tests.")
        print("\nGenerate test templates:")
        for file in modified_files:
            if not TestRequirement.validate_test_exists(file):
                print(f"  python tests/test_system.py generate {file}")
        return False

    print("\n✓ All test requirements met")
    return True


def main():
    """CLI interface for test system"""
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print(
            "  python tests/test_system.py generate <module_path>  # Generate test template"
        )
        print(
            "  python tests/test_system.py validate <test_path>     # Validate test file"
        )
        print(
            "  python tests/test_system.py enforce                  # Enforce test requirements"
        )
        return

    command = sys.argv[1]

    if command == "generate" and len(sys.argv) > 2:
        module_path = sys.argv[2]
        test_type = sys.argv[3] if len(sys.argv) > 3 else "unit"

        if test_type == "unit":
            template = TestGenerator.generate_unit_test_template(module_path)
            output_path = Path("tests") / f"test_{Path(module_path).name}"
        else:
            feature_name = Path(module_path).stem
            template = TestGenerator.generate_integration_test_template(feature_name)
            output_path = (
                Path("tests/integration") / f"test_{feature_name}_integration.py"
            )

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            f.write(template)

        print(f"Generated test template: {output_path}")

    elif command == "validate" and len(sys.argv) > 2:
        test_path = sys.argv[2]
        results = TestValidator.validate_test_file(test_path)

        print(f"\nValidation results for {test_path}:")
        print(f"  Valid: {results['valid']}")
        print(f"  Test count: {results['test_count']}")
        print(f"  Has setup: {results['has_setup']}")
        print(f"  Has teardown: {results['has_teardown']}")

        if results["errors"]:
            print("\nErrors:")
            for error in results["errors"]:
                print(f"  ✗ {error}")

        if results["warnings"]:
            print("\nWarnings:")
            for warning in results["warnings"]:
                print(f"  ⚠ {warning}")

    elif command == "enforce":
        success = enforce_test_requirements()
        sys.exit(0 if success else 1)

    else:
        print("Unknown command")


if __name__ == "__main__":
    main()
