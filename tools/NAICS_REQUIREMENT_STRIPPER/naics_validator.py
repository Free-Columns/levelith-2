#!/usr/bin/env python3
"""
NAICS Data Validator and Cleaner
Validates extracted data and provides cleaning/fixing utilities
"""

import json
import re
from typing import Dict, List, Tuple, Any
from pathlib import Path


class NAICSValidator:
    """Validate and clean NAICS data"""
    
    def __init__(self, json_path: str):
        self.json_path = json_path
        with open(json_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        self.issues = []
        self.fixes_applied = []
    
    def validate_all(self) -> Dict[str, Any]:
        """Run all validation checks"""
        print("Running validation checks...")
        
        results = {
            "valid": True,
            "checks": {
                "structure": self.validate_structure(),
                "codes": self.validate_codes(),
                "size_standards": self.validate_size_standards(),
                "duplicates": self.check_duplicates(),
                "data_quality": self.check_data_quality()
            },
            "total_issues": len(self.issues),
            "issues": self.issues
        }
        
        results["valid"] = all(check["passed"] for check in results["checks"].values())
        
        return results
    
    def validate_structure(self) -> Dict[str, Any]:
        """Validate JSON structure"""
        required_keys = ["document_info", "sectors", "metadata"]
        issues = []
        
        for key in required_keys:
            if key not in self.data:
                issues.append(f"Missing required key: {key}")
        
        if "sectors" in self.data:
            for i, sector in enumerate(self.data["sectors"]):
                if "sector_code" not in sector:
                    issues.append(f"Sector {i} missing sector_code")
                if "industries" not in sector:
                    issues.append(f"Sector {i} missing industries")
        
        self.issues.extend(issues)
        return {
            "passed": len(issues) == 0,
            "issues_found": len(issues),
            "details": issues
        }
    
    def validate_codes(self) -> Dict[str, Any]:
        """Validate NAICS code format"""
        issues = []
        valid_pattern = re.compile(r'^\d{6}(-E\d+)?$')
        
        for sector in self.data.get("sectors", []):
            for industry in sector.get("industries", []):
                code = industry.get("code", "")
                
                # Check format
                if not valid_pattern.match(code):
                    issues.append({
                        "code": code,
                        "sector": sector.get("sector_code"),
                        "issue": "Invalid code format",
                        "expected": "6 digits or 6 digits-E# for exceptions"
                    })
                
                # Check title exists
                if not industry.get("title"):
                    issues.append({
                        "code": code,
                        "issue": "Missing title"
                    })
        
        self.issues.extend(issues)
        return {
            "passed": len(issues) == 0,
            "issues_found": len(issues),
            "details": issues[:10]  # Show first 10
        }
    
    def validate_size_standards(self) -> Dict[str, Any]:
        """Validate size standards"""
        issues = []
        
        for sector in self.data.get("sectors", []):
            for industry in sector.get("industries", []):
                code = industry.get("code")
                has_millions = "size_standard_millions" in industry
                has_employees = "size_standard_employees" in industry
                
                # Each industry should have at least one size standard
                if not has_millions and not has_employees:
                    issues.append({
                        "code": code,
                        "issue": "No size standard defined"
                    })
                
                # Validate ranges
                if has_millions:
                    value = industry["size_standard_millions"]
                    if not isinstance(value, (int, float)) or value <= 0:
                        issues.append({
                            "code": code,
                            "issue": f"Invalid revenue standard: {value}"
                        })
                
                if has_employees:
                    value = industry["size_standard_employees"]
                    if not isinstance(value, int) or value <= 0:
                        issues.append({
                            "code": code,
                            "issue": f"Invalid employee standard: {value}"
                        })
        
        self.issues.extend(issues)
        return {
            "passed": len(issues) == 0,
            "issues_found": len(issues),
            "details": issues[:10]
        }
    
    def check_duplicates(self) -> Dict[str, Any]:
        """Check for duplicate NAICS codes"""
        seen_codes = {}
        duplicates = []
        
        for sector in self.data.get("sectors", []):
            for industry in sector.get("industries", []):
                code = industry.get("code")
                
                if code in seen_codes:
                    duplicates.append({
                        "code": code,
                        "first_occurrence": seen_codes[code],
                        "duplicate_in": sector.get("sector_code")
                    })
                else:
                    seen_codes[code] = sector.get("sector_code")
        
        self.issues.extend(duplicates)
        return {
            "passed": len(duplicates) == 0,
            "issues_found": len(duplicates),
            "details": duplicates
        }
    
    def check_data_quality(self) -> Dict[str, Any]:
        """Check data quality issues"""
        issues = []
        
        for sector in self.data.get("sectors", []):
            for industry in sector.get("industries", []):
                code = industry.get("code")
                title = industry.get("title", "")
                
                # Check for newlines in titles
                if '\n' in title:
                    issues.append({
                        "code": code,
                        "issue": "Title contains newline character",
                        "can_fix": True
                    })
                
                # Check for excessive whitespace
                if title != title.strip():
                    issues.append({
                        "code": code,
                        "issue": "Title has leading/trailing whitespace",
                        "can_fix": True
                    })
                
                # Check for missing data
                if not title:
                    issues.append({
                        "code": code,
                        "issue": "Empty title",
                        "can_fix": False
                    })
        
        self.issues.extend(issues)
        return {
            "passed": len(issues) == 0,
            "issues_found": len(issues),
            "fixable": sum(1 for i in issues if i.get("can_fix")),
            "details": issues[:10]
        }
    
    def clean_data(self) -> int:
        """Clean and fix common data issues"""
        fixes = 0
        
        for sector in self.data.get("sectors", []):
            for industry in sector.get("industries", []):
                title = industry.get("title", "")
                
                # Remove newlines
                if '\n' in title:
                    industry["title"] = title.replace('\n', ' ')
                    fixes += 1
                    self.fixes_applied.append({
                        "code": industry.get("code"),
                        "fix": "Removed newline from title"
                    })
                
                # Trim whitespace
                cleaned = title.strip()
                if cleaned != title:
                    industry["title"] = cleaned
                    fixes += 1
                    self.fixes_applied.append({
                        "code": industry.get("code"),
                        "fix": "Trimmed whitespace from title"
                    })
                
                # Clean up multiple spaces
                cleaned = re.sub(r'\s+', ' ', industry["title"])
                if cleaned != industry["title"]:
                    industry["title"] = cleaned
                    fixes += 1
        
        return fixes
    
    def save_cleaned_data(self, output_path: str):
        """Save cleaned data to file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
        print(f"✓ Cleaned data saved to: {output_path}")
    
    def generate_report(self, output_path: str):
        """Generate validation report"""
        validation_results = self.validate_all()
        
        report = {
            "validation_summary": {
                "overall_valid": validation_results["valid"],
                "total_issues": validation_results["total_issues"],
                "total_fixes_applied": len(self.fixes_applied)
            },
            "check_results": validation_results["checks"],
            "issues": self.issues,
            "fixes_applied": self.fixes_applied,
            "statistics": {
                "total_sectors": len(self.data.get("sectors", [])),
                "total_industries": sum(
                    len(s.get("industries", [])) 
                    for s in self.data.get("sectors", [])
                )
            }
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return report


def main():
    """Main execution"""
    input_file = "/mnt/user-data/outputs/naics_complete.json"
    cleaned_file = "/mnt/user-data/outputs/naics_cleaned.json"
    report_file = "/mnt/user-data/outputs/validation_report.json"
    
    print("="*60)
    print("NAICS Data Validator")
    print("="*60)
    
    validator = NAICSValidator(input_file)
    
    # Run validation
    print("\n1. Running validation checks...")
    results = validator.validate_all()
    
    print(f"\n   Overall Valid: {results['valid']}")
    print(f"   Total Issues Found: {results['total_issues']}")
    
    for check_name, check_result in results['checks'].items():
        status = "✓ PASS" if check_result['passed'] else "✗ FAIL"
        print(f"   {status} - {check_name}: {check_result['issues_found']} issues")
    
    # Clean data
    print("\n2. Cleaning data...")
    fixes = validator.clean_data()
    print(f"   Applied {fixes} fixes")
    
    # Save cleaned data
    if fixes > 0:
        print("\n3. Saving cleaned data...")
        validator.save_cleaned_data(cleaned_file)
    
    # Generate report
    print("\n4. Generating validation report...")
    report = validator.generate_report(report_file)
    print(f"   ✓ Report saved to: {report_file}")
    
    print("\n" + "="*60)
    print("Validation Complete")
    print("="*60)
    
    # Summary
    print(f"\nSummary:")
    print(f"  Total Sectors: {report['statistics']['total_sectors']}")
    print(f"  Total Industries: {report['statistics']['total_industries']}")
    print(f"  Issues Found: {report['validation_summary']['total_issues']}")
    print(f"  Fixes Applied: {report['validation_summary']['total_fixes_applied']}")
    
    if report['validation_summary']['overall_valid']:
        print(f"\n✓ Data is valid and ready to use!")
    else:
        print(f"\n⚠ Some issues remain - review validation_report.json")


if __name__ == "__main__":
    main()
