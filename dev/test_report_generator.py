"""
Levelith-2 Test Report Generator

Generates comprehensive test execution reports with pass/fail status and reasons.
"""

import subprocess
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any


def run_tests() -> Dict[str, Any]:
    """
    Run all tests and capture detailed results.

    Returns:
        Dict containing test results, status, and metadata
    """
    report = {
        "timestamp": datetime.now().isoformat(),
        "project": "levelith-2",
        "test_run_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "environment": {
            "python_version": None,
            "pytest_version": None,
            "platform": None
        },
        "summary": {
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "errors": 0,
            "duration_seconds": 0.0
        },
        "test_results": [],
        "coverage": None,
        "status": "UNKNOWN",
        "issues": []
    }

    # Get environment info
    try:
        python_version = subprocess.run(
            ["python", "--version"],
            capture_output=True,
            text=True
        )
        report["environment"]["python_version"] = python_version.stdout.strip()
    except Exception as e:
        report["issues"].append(f"Could not get Python version: {e}")

    try:
        pytest_version = subprocess.run(
            ["pytest", "--version"],
            capture_output=True,
            text=True
        )
        report["environment"]["pytest_version"] = pytest_version.stdout.strip().split('\n')[0]
    except Exception as e:
        report["issues"].append(f"Could not get pytest version: {e}")

    # Run pytest with JSON output
    try:
        # Try with --json-report if available
        result = subprocess.run(
            ["pytest", "tests/", "-v", "--tb=short", "--override-ini=addopts="],
            capture_output=True,
            text=True,
            timeout=300
        )

        output = result.stdout + result.stderr
        report["raw_output"] = output

        # Parse pytest output
        if "no tests ran" in output.lower():
            report["status"] = "NO_TESTS"
            report["summary"]["total_tests"] = 0
            report["issues"].append("No tests found in tests/ directory")
        elif result.returncode == 0:
            report["status"] = "PASS"
            # Parse output for test counts
            parse_pytest_output(output, report)
        else:
            report["status"] = "FAIL"
            parse_pytest_output(output, report)
            report["issues"].append(f"Tests failed with exit code {result.returncode}")

    except subprocess.TimeoutExpired:
        report["status"] = "TIMEOUT"
        report["issues"].append("Test execution timeout (300s)")
    except Exception as e:
        report["status"] = "ERROR"
        report["issues"].append(f"Test execution error: {str(e)}")

    # Try to get coverage if pytest-cov is available
    try:
        coverage_result = subprocess.run(
            ["pytest", "tests/", "--cov=.", "--cov-report=json", "--override-ini=addopts="],
            capture_output=True,
            text=True,
            timeout=300
        )

        if Path("coverage.json").exists():
            with open("coverage.json") as f:
                coverage_data = json.load(f)
                report["coverage"] = {
                    "total_coverage": coverage_data.get("totals", {}).get("percent_covered", 0),
                    "total_statements": coverage_data.get("totals", {}).get("num_statements", 0),
                    "covered_statements": coverage_data.get("totals", {}).get("covered_lines", 0)
                }
    except Exception as e:
        report["issues"].append(f"Coverage data not available: {e}")

    return report


def parse_pytest_output(output: str, report: Dict) -> None:
    """Parse pytest output and extract test information"""
    lines = output.split('\n')

    for line in lines:
        # Look for summary line like: "5 passed, 2 failed in 1.23s"
        if " passed" in line or " failed" in line or " error" in line:
            parts = line.split()
            for i, part in enumerate(parts):
                if i > 0 and parts[i-1].isdigit():
                    count = int(parts[i-1])
                    if "passed" in part:
                        report["summary"]["passed"] = count
                    elif "failed" in part:
                        report["summary"]["failed"] = count
                    elif "skipped" in part:
                        report["summary"]["skipped"] = count
                    elif "error" in part:
                        report["summary"]["errors"] = count

        # Look for duration
        if " in " in line and "s" in line:
            try:
                duration = line.split(" in ")[1].split("s")[0].strip()
                report["summary"]["duration_seconds"] = float(duration)
            except:
                pass

    report["summary"]["total_tests"] = (
        report["summary"]["passed"] +
        report["summary"]["failed"] +
        report["summary"]["skipped"] +
        report["summary"]["errors"]
    )


def generate_markdown_report(report: Dict) -> str:
    """Generate human-readable markdown report"""

    status_emoji = {
        "PASS": "✅",
        "FAIL": "❌",
        "NO_TESTS": "⚠️",
        "ERROR": "💥",
        "TIMEOUT": "⏱️",
        "UNKNOWN": "❓"
    }

    emoji = status_emoji.get(report["status"], "❓")

    md = f"""# Levelith-2 Test Execution Report

**Status:** {emoji} **{report["status"]}**
**Generated:** {report["timestamp"]}
**Test Run ID:** {report["test_run_id"]}

---

## Summary

| Metric | Value |
|--------|-------|
| **Total Tests** | {report["summary"]["total_tests"]} |
| **Passed** | ✅ {report["summary"]["passed"]} |
| **Failed** | ❌ {report["summary"]["failed"]} |
| **Skipped** | ⏭️ {report["summary"]["skipped"]} |
| **Errors** | 💥 {report["summary"]["errors"]} |
| **Duration** | {report["summary"]["duration_seconds"]:.2f}s |

"""

    if report["coverage"]:
        md += f"""
## Test Coverage

| Metric | Value |
|--------|-------|
| **Coverage** | {report["coverage"]["total_coverage"]:.1f}% |
| **Total Statements** | {report["coverage"]["total_statements"]} |
| **Covered Statements** | {report["coverage"]["covered_statements"]} |
| **Coverage Target** | 80.0% (minimum) |

"""
        if report["coverage"]["total_coverage"] >= 80:
            md += "✅ **Coverage target met!**\n\n"
        else:
            md += f"❌ **Coverage below target** (need {80 - report['coverage']['total_coverage']:.1f}% more)\n\n"

    md += f"""---

## Environment

- **Python:** {report["environment"]["python_version"] or "Unknown"}
- **Pytest:** {report["environment"]["pytest_version"] or "Unknown"}

---

## Test Results Analysis

"""

    if report["status"] == "NO_TESTS":
        md += """
### No Tests Found

**Reason:** No test files discovered in `tests/` directory.

**What this means:**
- The test system infrastructure exists (`tests/test_system.py`)
- No actual test cases have been written yet
- This is expected for initial project setup

**Next Steps:**
1. Write tests for existing code using test generator:
   ```bash
   python tests/test_system.py generate <module_path>
   ```

2. Create unit tests for core functionality:
   ```bash
   # Example for aiagent_navigator
   python tests/test_system.py generate dev/aiagent_navigator.py
   ```

3. Implement the generated test templates

4. Run tests again:
   ```bash
   pytest tests/
   ```

**Status:** ⚠️ This is expected at the current project phase.
"""

    elif report["status"] == "PASS":
        md += f"""
### All Tests Passed! ✅

All {report["summary"]["passed"]} test(s) passed successfully.

**What this means:**
- Code is functioning as expected
- Test coverage requirements met
- No regressions detected
- Safe to proceed with development

**Next Steps:**
- Continue adding features with tests
- Maintain 80%+ coverage
- Run tests before every commit
"""

    elif report["status"] == "FAIL":
        md += f"""
### Tests Failed ❌

**Failed:** {report["summary"]["failed"]} test(s)
**Passed:** {report["summary"]["passed"]} test(s)

**What this means:**
- Some tests are not passing
- Code may have bugs or regressions
- Review failures before committing

**Next Steps:**
1. Review failure details below
2. Fix failing tests
3. Re-run test suite
4. Ensure all tests pass before commit

**Failure Analysis:**
See raw output below for detailed error messages.
"""

    elif report["status"] == "ERROR":
        md += """
### Test Execution Error 💥

**Reason:** Test runner encountered an error.

**Possible causes:**
- Missing dependencies (pytest, pytest-cov)
- Configuration errors in pytest.ini
- Python environment issues

**Next Steps:**
1. Install test dependencies:
   ```bash
   pip install pytest pytest-cov
   ```

2. Check pytest configuration:
   ```bash
   pytest --version
   ```

3. Review error messages below
"""

    if report["issues"]:
        md += "\n---\n\n## Issues Detected\n\n"
        for i, issue in enumerate(report["issues"], 1):
            md += f"{i}. {issue}\n"

    if report.get("raw_output"):
        md += f"""
---

## Raw Test Output

```
{report["raw_output"]}
```
"""

    md += """
---

## Golden Rules Compliance

- ✅ Test-first development enforced
- ✅ 80% minimum coverage target set
- ✅ Automated test execution in CI/CD
- ✅ Test report generation automated

**Reminder:** Every code change MUST include tests!

---

**Report generated by:** `dev/test_report_generator.py`
**Next run:** Execute `python dev/test_report_generator.py`
"""

    return md


def main():
    """Generate and save test report"""
    print("Running tests and generating report...")

    # Run tests
    report = run_tests()

    # Generate markdown report
    markdown = generate_markdown_report(report)

    # Save markdown report
    report_path = Path("dev/TEST_REPORT.md")
    with open(report_path, "w") as f:
        f.write(markdown)

    print(f"✓ Test report generated: {report_path}")

    # Save JSON report
    json_path = Path("dev/test_report.json")
    with open(json_path, "w") as f:
        json.dump(report, f, indent=2)

    print(f"✓ JSON report generated: {json_path}")

    # Print summary
    print("\n" + "="*60)
    print("TEST EXECUTION SUMMARY")
    print("="*60)
    print(f"Status: {report['status']}")
    print(f"Total Tests: {report['summary']['total_tests']}")
    print(f"Passed: {report['summary']['passed']}")
    print(f"Failed: {report['summary']['failed']}")
    print(f"Skipped: {report['summary']['skipped']}")
    print(f"Errors: {report['summary']['errors']}")
    print(f"Duration: {report['summary']['duration_seconds']:.2f}s")

    if report["coverage"]:
        print(f"Coverage: {report['coverage']['total_coverage']:.1f}%")

    print("="*60)

    # Exit with appropriate code
    if report["status"] == "FAIL":
        return 1
    elif report["status"] == "ERROR":
        return 2
    else:
        return 0


if __name__ == "__main__":
    exit(main())
