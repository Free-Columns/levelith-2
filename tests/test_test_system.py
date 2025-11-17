"""
Unit tests for the test system itself.

This demonstrates the test framework in action and validates
the test enforcement and generation tools.
"""

import pytest
from pathlib import Path
import sys
import os

# Add parent directory to path to import test_system
sys.path.insert(0, str(Path(__file__).parent))

from test_system import (
    TestRequirement,
    TestGenerator,
    TestValidator
)


class TestTestRequirement:
    """Test suite for TestRequirement class"""

    def test_validate_test_exists_returns_true_when_test_file_exists(self, tmp_path):
        """Test that validate_test_exists returns True when test file exists"""
        # Create a test file
        test_file = tmp_path / "tests" / "test_example.py"
        test_file.parent.mkdir(parents=True)
        test_file.touch()

        # Create module file
        module_file = tmp_path / "example.py"
        module_file.touch()

        # Change to temp directory
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            result = TestRequirement.validate_test_exists("example.py")
            assert result is True
        finally:
            os.chdir(original_cwd)

    def test_validate_test_exists_returns_false_when_test_file_missing(self, tmp_path):
        """Test that validate_test_exists returns False when test file missing"""
        module_file = tmp_path / "example.py"
        module_file.touch()

        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            result = TestRequirement.validate_test_exists("example.py")
            assert result is False
        finally:
            os.chdir(original_cwd)

    def test_minimum_coverage_constant_is_80_percent(self):
        """Test that minimum coverage is set to 80%"""
        assert TestRequirement.MINIMUM_COVERAGE == 80

    def test_require_unit_tests_is_true(self):
        """Test that unit tests are required"""
        assert TestRequirement.REQUIRE_UNIT_TESTS is True

    def test_require_integration_tests_is_true(self):
        """Test that integration tests are required"""
        assert TestRequirement.REQUIRE_INTEGRATION_TESTS is True


class TestTestGenerator:
    """Test suite for TestGenerator class"""

    def test_generate_unit_test_template_creates_valid_python(self, tmp_path):
        """Test that generated unit test template is valid Python"""
        # Create a simple module
        module_file = tmp_path / "example.py"
        module_file.write_text("""
def add(a, b):
    return a + b

class Calculator:
    def multiply(self, a, b):
        return a * b
""")

        template = TestGenerator.generate_unit_test_template(str(module_file))

        # Check template contains expected elements
        assert "import pytest" in template
        assert "def test_" in template
        assert "class Test" in template

        # Verify it's valid Python syntax
        try:
            compile(template, "<string>", "exec")
            valid = True
        except SyntaxError:
            valid = False

        assert valid is True

    def test_generate_integration_test_template_creates_valid_python(self):
        """Test that generated integration test template is valid Python"""
        template = TestGenerator.generate_integration_test_template("user_auth")

        # Check template contains expected elements
        assert "import pytest" in template
        assert "Integration" in template
        assert "def test_" in template

        # Verify it's valid Python syntax
        try:
            compile(template, "<string>", "exec")
            valid = True
        except SyntaxError:
            valid = False

        assert valid is True

    def test_generated_template_includes_test_class(self, tmp_path):
        """Test that generated template includes a test class"""
        module_file = tmp_path / "example.py"
        module_file.write_text("def foo(): pass")

        template = TestGenerator.generate_unit_test_template(str(module_file))

        assert "class Test" in template

    def test_generated_template_includes_setup_method(self, tmp_path):
        """Test that generated template includes setup method"""
        module_file = tmp_path / "example.py"
        module_file.write_text("def foo(): pass")

        template = TestGenerator.generate_unit_test_template(str(module_file))

        assert "def setup_method" in template


class TestTestValidator:
    """Test suite for TestValidator class"""

    def test_validate_test_file_returns_valid_for_good_test(self, tmp_path):
        """Test that validator returns valid for properly structured test"""
        test_file = tmp_path / "test_example.py"
        test_file.write_text("""
import pytest

class TestExample:
    def setup_method(self):
        pass

    def test_something(self):
        assert True

    def test_another_thing(self):
        assert 1 + 1 == 2
""")

        results = TestValidator.validate_test_file(str(test_file))

        assert results["valid"] is True
        assert results["test_count"] == 2
        assert results["has_setup"] is True

    def test_validate_test_file_returns_invalid_for_no_tests(self, tmp_path):
        """Test that validator returns invalid for file with no tests"""
        test_file = tmp_path / "test_example.py"
        test_file.write_text("""
import pytest

def helper_function():
    pass
""")

        results = TestValidator.validate_test_file(str(test_file))

        assert results["valid"] is False
        assert results["test_count"] == 0
        assert "No test functions found" in results["errors"]

    def test_validate_test_file_warns_about_too_many_skips(self, tmp_path):
        """Test that validator warns when too many tests are skipped"""
        test_file = tmp_path / "test_example.py"
        test_file.write_text("""
import pytest

def test_one():
    pytest.skip("Not implemented")

def test_two():
    pytest.skip("Not implemented")

def test_three():
    assert True
""")

        results = TestValidator.validate_test_file(str(test_file))

        assert len(results["warnings"]) > 0
        assert any("skipped" in w.lower() for w in results["warnings"])


class TestTestSystemIntegration:
    """Integration tests for the test system"""

    def test_test_system_module_imports_successfully(self):
        """Test that test_system module can be imported"""
        import test_system
        assert test_system is not None

    def test_all_required_classes_exist(self):
        """Test that all required classes are defined"""
        import test_system

        assert hasattr(test_system, 'TestRequirement')
        assert hasattr(test_system, 'TestGenerator')
        assert hasattr(test_system, 'TestValidator')

    def test_test_requirement_class_has_required_methods(self):
        """Test that TestRequirement has required methods"""
        assert hasattr(TestRequirement, 'validate_test_exists')
        assert hasattr(TestRequirement, 'validate_coverage')

    def test_test_generator_class_has_required_methods(self):
        """Test that TestGenerator has required methods"""
        assert hasattr(TestGenerator, 'generate_unit_test_template')
        assert hasattr(TestGenerator, 'generate_integration_test_template')

    def test_test_validator_class_has_required_methods(self):
        """Test that TestValidator has required methods"""
        assert hasattr(TestValidator, 'validate_test_file')
        assert hasattr(TestValidator, 'validate_test_coverage')


# Mark all tests in this file as unit tests
pytestmark = pytest.mark.unit
