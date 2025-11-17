"""
Test System Debugger

Debugging utilities for the Levelith test system.
Provides detailed diagnostics, failure analysis, and troubleshooting tools.

Usage:
    python dev/test_debugger.py diagnose               # Full system diagnostic
    python dev/test_debugger.py analyze-failure <test> # Analyze specific test failure
    python dev/test_debugger.py coverage-gaps          # Find coverage gaps
    python dev/test_debugger.py validate-all           # Validate all test files
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Any
import ast
import re


class TestDebugger:
    """Debugging utilities for test system"""

    def __init__(self, root_path: str = "."):
        self.root = Path(root_path)
        self.test_dir = self.root / "tests"
        self.diagnostics = {}

    def run_full_diagnostic(self) -> Dict[str, Any]:
        """
        Run comprehensive diagnostic of test system.

        Returns detailed report of test system health.
        """
        print("=" * 70)
        print("LEVELITH TEST SYSTEM DIAGNOSTIC")
        print("=" * 70)
        print()

        diagnostics = {
            "timestamp": subprocess.run(
                ["date", "+%Y-%m-%d %H:%M:%S"], capture_output=True, text=True
            ).stdout.strip(),
            "environment": self._check_environment(),
            "test_files": self._analyze_test_files(),
            "coverage": self._analyze_coverage_status(),
            "test_execution": self._run_test_diagnostic(),
            "validation": self._validate_all_tests(),
            "recommendations": [],
        }

        # Generate recommendations
        diagnostics["recommendations"] = self._generate_recommendations(diagnostics)

        # Print summary
        self._print_diagnostic_summary(diagnostics)

        return diagnostics

    def _check_environment(self) -> Dict[str, Any]:
        """Check test environment setup"""
        print("📋 Checking Environment...")

        env = {
            "python_version": None,
            "pytest_installed": False,
            "pytest_cov_installed": False,
            "black_installed": False,
            "test_dir_exists": self.test_dir.exists(),
            "issues": [],
        }

        # Check Python version
        try:
            result = subprocess.run(
                ["python", "--version"], capture_output=True, text=True
            )
            env["python_version"] = result.stdout.strip()
            print(f"  ✓ Python: {env['python_version']}")
        except Exception as e:
            env["issues"].append(f"Python check failed: {e}")
            print(f"  ✗ Python: FAILED")

        # Check pytest
        try:
            result = subprocess.run(
                ["pytest", "--version"], capture_output=True, text=True
            )
            env["pytest_installed"] = True
            print(f"  ✓ Pytest: {result.stdout.strip().split()[1]}")
        except Exception as e:
            env["issues"].append("pytest not installed")
            print(f"  ✗ Pytest: NOT FOUND")

        # Check pytest-cov
        try:
            result = subprocess.run(
                ["pytest", "--co", "--cov=.", "-q"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if "unrecognized arguments" not in result.stderr:
                env["pytest_cov_installed"] = True
                print(f"  ✓ Pytest-cov: INSTALLED")
            else:
                print(f"  ⚠ Pytest-cov: NOT INSTALLED (optional)")
        except Exception:
            print(f"  ⚠ Pytest-cov: NOT INSTALLED (optional)")

        # Check Black
        try:
            result = subprocess.run(
                ["black", "--version"], capture_output=True, text=True
            )
            env["black_installed"] = True
            print(f"  ✓ Black: {result.stdout.strip()}")
        except Exception:
            env["issues"].append("black not installed")
            print(f"  ✗ Black: NOT FOUND")

        # Check test directory
        if env["test_dir_exists"]:
            print(f"  ✓ Test directory: {self.test_dir}")
        else:
            env["issues"].append("Test directory does not exist")
            print(f"  ✗ Test directory: NOT FOUND")

        print()
        return env

    def _analyze_test_files(self) -> Dict[str, Any]:
        """Analyze all test files"""
        print("📁 Analyzing Test Files...")

        if not self.test_dir.exists():
            print("  ✗ No test directory found")
            return {"count": 0, "files": [], "issues": ["Test directory missing"]}

        test_files = list(self.test_dir.glob("test_*.py"))
        analysis = {"count": len(test_files), "files": [], "total_tests": 0}

        for test_file in test_files:
            file_info = self._analyze_single_test_file(test_file)
            analysis["files"].append(file_info)
            analysis["total_tests"] += file_info["test_count"]

        print(f"  ✓ Found {analysis['count']} test files")
        print(f"  ✓ Total test functions: {analysis['total_tests']}")
        print()

        return analysis

    def _analyze_single_test_file(self, test_path: Path) -> Dict[str, Any]:
        """Analyze a single test file"""
        try:
            with open(test_path) as f:
                content = f.read()
                tree = ast.parse(content)

            test_functions = [
                node.name
                for node in ast.walk(tree)
                if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")
            ]

            test_classes = [
                node.name
                for node in ast.walk(tree)
                if isinstance(node, ast.ClassDef) and node.name.startswith("Test")
            ]

            # Check for common issues
            issues = []
            if not test_functions:
                issues.append("No test functions found")

            # Check for pytest import
            has_pytest = "import pytest" in content or "from pytest" in content
            if not has_pytest:
                issues.append("No pytest import found")

            return {
                "path": str(test_path.relative_to(self.root)),
                "test_count": len(test_functions),
                "test_classes": len(test_classes),
                "has_pytest_import": has_pytest,
                "test_functions": test_functions,
                "issues": issues,
            }
        except Exception as e:
            return {
                "path": str(test_path.relative_to(self.root)),
                "test_count": 0,
                "error": str(e),
                "issues": [f"Parse error: {e}"],
            }

    def _analyze_coverage_status(self) -> Dict[str, Any]:
        """Analyze test coverage status"""
        print("📊 Analyzing Coverage Status...")

        coverage_info = {
            "available": False,
            "total_coverage": 0,
            "by_file": {},
            "gaps": [],
        }

        try:
            # Try to run coverage
            result = subprocess.run(
                [
                    "pytest",
                    "tests/",
                    "--cov=.",
                    "--cov-report=json",
                    "--override-ini=addopts=",
                    "-q",
                ],
                capture_output=True,
                text=True,
                timeout=60,
            )

            coverage_file = self.root / "coverage.json"
            if coverage_file.exists():
                with open(coverage_file) as f:
                    cov_data = json.load(f)
                    coverage_info["available"] = True
                    coverage_info["total_coverage"] = cov_data.get("totals", {}).get(
                        "percent_covered", 0
                    )

                    # Analyze per-file coverage
                    files = cov_data.get("files", {})
                    for filepath, file_cov in files.items():
                        pct = file_cov.get("summary", {}).get("percent_covered", 0)
                        coverage_info["by_file"][filepath] = pct

                        # Flag gaps (< 80%)
                        if pct < 80 and not filepath.startswith("test"):
                            coverage_info["gaps"].append(
                                {"file": filepath, "coverage": pct}
                            )

                print(f"  ✓ Total coverage: {coverage_info['total_coverage']:.1f}%")
                if coverage_info["gaps"]:
                    print(f"  ⚠ Found {len(coverage_info['gaps'])} files below 80%")
            else:
                print("  ⚠ Coverage data not available (run with pytest-cov)")
        except Exception as e:
            print(f"  ⚠ Coverage analysis failed: {e}")
            coverage_info["error"] = str(e)

        print()
        return coverage_info

    def _run_test_diagnostic(self) -> Dict[str, Any]:
        """Run tests and capture diagnostic info"""
        print("🧪 Running Test Diagnostic...")

        diagnostic = {
            "ran": False,
            "passed": 0,
            "failed": 0,
            "errors": 0,
            "skipped": 0,
            "duration": 0,
            "failures": [],
        }

        try:
            result = subprocess.run(
                ["pytest", "tests/", "-v", "--tb=short", "--override-ini=addopts="],
                capture_output=True,
                text=True,
                timeout=120,
            )

            diagnostic["ran"] = True
            output = result.stdout + result.stderr

            # Parse output
            lines = output.split("\n")
            for line in lines:
                if " passed" in line:
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if "passed" in part and i > 0 and parts[i - 1].isdigit():
                            diagnostic["passed"] = int(parts[i - 1])
                        elif "failed" in part and i > 0 and parts[i - 1].isdigit():
                            diagnostic["failed"] = int(parts[i - 1])
                        elif "error" in part and i > 0 and parts[i - 1].isdigit():
                            diagnostic["errors"] = int(parts[i - 1])
                        elif "skipped" in part and i > 0 and parts[i - 1].isdigit():
                            diagnostic["skipped"] = int(parts[i - 1])

                # Capture failures
                if "FAILED" in line:
                    diagnostic["failures"].append(line.strip())

            total = (
                diagnostic["passed"]
                + diagnostic["failed"]
                + diagnostic["errors"]
                + diagnostic["skipped"]
            )

            print(f"  ✓ Tests executed: {total}")
            print(f"    Passed: {diagnostic['passed']}")
            if diagnostic["failed"] > 0:
                print(f"    Failed: {diagnostic['failed']} ❌")
            if diagnostic["errors"] > 0:
                print(f"    Errors: {diagnostic['errors']} 💥")
            if diagnostic["skipped"] > 0:
                print(f"    Skipped: {diagnostic['skipped']} ⏭")

        except subprocess.TimeoutExpired:
            diagnostic["error"] = "Test execution timed out"
            print("  ✗ Test execution timed out")
        except Exception as e:
            diagnostic["error"] = str(e)
            print(f"  ✗ Test execution failed: {e}")

        print()
        return diagnostic

    def _validate_all_tests(self) -> Dict[str, Any]:
        """Validate all test files"""
        print("✅ Validating Test Files...")

        if not self.test_dir.exists():
            print("  ✗ No test directory")
            return {"valid": False, "files": []}

        # Import test_system for validation
        sys.path.insert(0, str(self.test_dir))
        try:
            from test_system import TestValidator

            test_files = list(self.test_dir.glob("test_*.py"))
            validation = {"valid": True, "files": [], "issues": []}

            for test_file in test_files:
                result = TestValidator.validate_test_file(str(test_file))
                validation["files"].append(result)

                if not result["valid"]:
                    validation["valid"] = False
                    validation["issues"].extend(result["errors"])

            valid_count = sum(1 for f in validation["files"] if f["valid"])
            print(f"  ✓ Valid test files: {valid_count}/{len(test_files)}")

            if validation["issues"]:
                print(f"  ⚠ Found {len(validation['issues'])} validation issues")

        except ImportError:
            validation = {
                "valid": False,
                "error": "test_system module not found",
                "files": [],
            }
            print("  ✗ test_system module not available")
        except Exception as e:
            validation = {"valid": False, "error": str(e), "files": []}
            print(f"  ✗ Validation failed: {e}")

        print()
        return validation

    def _generate_recommendations(self, diagnostics: Dict) -> List[str]:
        """Generate recommendations based on diagnostics"""
        recommendations = []

        # Environment issues
        if not diagnostics["environment"]["pytest_installed"]:
            recommendations.append("❗ Install pytest: pip install pytest")

        if not diagnostics["environment"]["black_installed"]:
            recommendations.append("❗ Install black: pip install black")

        # Coverage issues
        if diagnostics["coverage"]["available"]:
            if diagnostics["coverage"]["total_coverage"] < 80:
                recommendations.append(
                    f"⚠️  Coverage is {diagnostics['coverage']['total_coverage']:.1f}% (target: 80%)"
                )

            for gap in diagnostics["coverage"]["gaps"]:
                recommendations.append(
                    f"📝 Add tests for {gap['file']} ({gap['coverage']:.1f}% coverage)"
                )

        # Test execution issues
        if diagnostics["test_execution"]["failed"] > 0:
            recommendations.append(
                f"❌ Fix {diagnostics['test_execution']['failed']} failing tests"
            )

        if diagnostics["test_execution"]["errors"] > 0:
            recommendations.append(
                f"💥 Fix {diagnostics['test_execution']['errors']} test errors"
            )

        # Validation issues
        if not diagnostics["validation"]["valid"]:
            recommendations.append("🔍 Review test validation issues")

        if not recommendations:
            recommendations.append("✅ All systems operational!")

        return recommendations

    def _print_diagnostic_summary(self, diagnostics: Dict):
        """Print summary of diagnostics"""
        print()
        print("=" * 70)
        print("RECOMMENDATIONS")
        print("=" * 70)
        for rec in diagnostics["recommendations"]:
            print(f"  {rec}")
        print()

        # Overall health score
        health_score = 100
        if not diagnostics["environment"]["pytest_installed"]:
            health_score -= 30
        if diagnostics["test_execution"]["failed"] > 0:
            health_score -= 20
        if diagnostics["coverage"]["available"]:
            if diagnostics["coverage"]["total_coverage"] < 80:
                health_score -= 15
        if not diagnostics["validation"]["valid"]:
            health_score -= 10

        health_emoji = (
            "🟢" if health_score >= 80 else "🟡" if health_score >= 60 else "🔴"
        )
        print(f"Overall Health Score: {health_emoji} {health_score}/100")
        print("=" * 70)

    def analyze_test_failure(self, test_name: str) -> Dict[str, Any]:
        """Analyze a specific test failure in detail"""
        print(f"🔍 Analyzing test failure: {test_name}")
        print("=" * 70)

        analysis = {"test_name": test_name, "found": False, "details": {}}

        # Run the specific test with verbose output
        try:
            result = subprocess.run(
                ["pytest", f"tests/{test_name}", "-vv", "--tb=long"],
                capture_output=True,
                text=True,
                timeout=30,
            )

            output = result.stdout + result.stderr
            analysis["found"] = "PASSED" in output or "FAILED" in output
            analysis["output"] = output

            # Extract failure details
            if "FAILED" in output:
                analysis["status"] = "FAILED"
                # Extract assertion error
                assertion_match = re.search(r"AssertionError: (.+)", output)
                if assertion_match:
                    analysis["assertion_error"] = assertion_match.group(1)

                # Extract traceback
                if "Traceback" in output:
                    tb_start = output.find("Traceback")
                    tb_end = output.find("\n\n", tb_start)
                    analysis["traceback"] = output[tb_start:tb_end]

            elif "PASSED" in output:
                analysis["status"] = "PASSED"

            print(output)

        except Exception as e:
            analysis["error"] = str(e)
            print(f"Error analyzing test: {e}")

        return analysis

    def find_coverage_gaps(self) -> List[Dict[str, Any]]:
        """Find files with insufficient test coverage"""
        print("🔎 Finding Coverage Gaps...")
        print("=" * 70)

        gaps = []

        try:
            # Run coverage
            subprocess.run(
                [
                    "pytest",
                    "tests/",
                    "--cov=.",
                    "--cov-report=json",
                    "--override-ini=addopts=",
                    "-q",
                ],
                capture_output=True,
                text=True,
                timeout=60,
            )

            coverage_file = Path("coverage.json")
            if coverage_file.exists():
                with open(coverage_file) as f:
                    cov_data = json.load(f)

                files = cov_data.get("files", {})
                for filepath, file_cov in files.items():
                    # Skip test files and __pycache__
                    if "test_" in filepath or "__pycache__" in filepath:
                        continue

                    summary = file_cov.get("summary", {})
                    pct = summary.get("percent_covered", 0)
                    missing_lines = file_cov.get("missing_lines", [])

                    if pct < 80:
                        gap = {
                            "file": filepath,
                            "coverage": pct,
                            "missing_lines": missing_lines,
                            "num_missing": summary.get("num_statements", 0)
                            - summary.get("covered_lines", 0),
                        }
                        gaps.append(gap)

                # Sort by coverage (worst first)
                gaps.sort(key=lambda x: x["coverage"])

                print(f"Found {len(gaps)} files below 80% coverage:\n")
                for gap in gaps:
                    print(f"  {gap['file']}: {gap['coverage']:.1f}%")
                    print(f"    Missing {gap['num_missing']} lines")
                    if gap["missing_lines"][:5]:
                        print(f"    Lines: {gap['missing_lines'][:5]}...")
                    print()
            else:
                print("No coverage data available. Install pytest-cov.")

        except Exception as e:
            print(f"Error finding coverage gaps: {e}")

        return gaps


def main():
    """CLI entry point"""
    debugger = TestDebugger()

    if len(sys.argv) < 2:
        print("Levelith Test System Debugger\n")
        print("Usage:")
        print("  python dev/test_debugger.py diagnose               # Full diagnostic")
        print(
            "  python dev/test_debugger.py analyze-failure <test> # Analyze specific failure"
        )
        print(
            "  python dev/test_debugger.py coverage-gaps          # Find coverage gaps"
        )
        print(
            "  python dev/test_debugger.py validate-all           # Validate all tests"
        )
        return

    command = sys.argv[1]

    if command == "diagnose":
        report = debugger.run_full_diagnostic()
        # Save to file
        with open("dev/diagnostic_report.json", "w") as f:
            json.dump(report, f, indent=2)
        print("\n✓ Full report saved to: dev/diagnostic_report.json")

    elif command == "analyze-failure" and len(sys.argv) > 2:
        test_name = sys.argv[2]
        debugger.analyze_test_failure(test_name)

    elif command == "coverage-gaps":
        gaps = debugger.find_coverage_gaps()

    elif command == "validate-all":
        validation = debugger._validate_all_tests()
        print(json.dumps(validation, indent=2))

    else:
        print(f"Unknown command: {command}")
        print("Run without arguments to see usage.")


if __name__ == "__main__":
    main()
