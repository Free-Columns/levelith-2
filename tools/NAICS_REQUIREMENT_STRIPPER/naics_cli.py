#!/usr/bin/env python3
"""
NAICS Tools - Command Line Interface
Unified interface for all NAICS extraction and analysis tools
"""

import sys
import json
from pathlib import Path
from naics_extractor import NAICSExtractor
from naics_query import NAICSQuery
from naics_validator import NAICSValidator


def print_header(title):
    """Print formatted header"""
    print("\n" + "="*60)
    print(title.center(60))
    print("="*60 + "\n")


def extract_command(pdf_path, output_path):
    """Extract data from PDF"""
    print_header("EXTRACT NAICS DATA")
    
    if not Path(pdf_path).exists():
        print(f"❌ Error: PDF file not found: {pdf_path}")
        return 1
    
    extractor = NAICSExtractor(pdf_path)
    data = extractor.process_pdf()
    extractor.save_json(output_path)
    
    print(f"\n✓ Extraction complete!")
    print(f"  Output: {output_path}")
    return 0


def query_command(json_path, query_type, query_value):
    """Query the data"""
    print_header("QUERY NAICS DATA")
    
    if not Path(json_path).exists():
        print(f"❌ Error: JSON file not found: {json_path}")
        return 1
    
    query = NAICSQuery(json_path)
    
    if query_type == "code":
        result = query.search_by_code(query_value)
        if result:
            print(f"Code: {result['code']}")
            print(f"Title: {result['title']}")
            print(f"Sector: {result['sector_name']}")
            if 'size_standard_millions' in result:
                print(f"Size Standard (Revenue): ${result['size_standard_millions']}M")
            if 'size_standard_employees' in result:
                print(f"Size Standard (Employees): {result['size_standard_employees']}")
        else:
            print(f"❌ Code '{query_value}' not found")
            return 1
    
    elif query_type == "keyword":
        results = query.search_by_keyword(query_value)
        print(f"Found {len(results)} industries matching '{query_value}':\n")
        for i, result in enumerate(results[:10], 1):
            print(f"{i}. {result['code']}: {result['title']}")
            if len(result['title']) > 60:
                print(f"   {result['title'][:60]}...")
            else:
                print(f"   {result['title']}")
        if len(results) > 10:
            print(f"\n... and {len(results) - 10} more")
    
    elif query_type == "sector":
        sector = query.get_sector(query_value)
        if sector:
            print(f"Sector {sector['sector_code']}: {sector['sector_name']}")
            print(f"Total industries: {len(sector['industries'])}\n")
            for i, ind in enumerate(sector['industries'][:5], 1):
                print(f"{i}. {ind['code']}: {ind['title']}")
            if len(sector['industries']) > 5:
                print(f"\n... and {len(sector['industries']) - 5} more")
        else:
            print(f"❌ Sector '{query_value}' not found")
            return 1
    
    elif query_type == "stats":
        stats = query.get_statistics()
        print(f"Total Sectors: {stats['total_sectors']}")
        print(f"Total Industries: {stats['total_industries']}")
        print(f"\nSize Standards:")
        print(f"  Revenue-based: {stats['size_standards']['revenue_based']}")
        print(f"  Employee-based: {stats['size_standards']['employee_based']}")
        if stats['revenue_range']['average']:
            print(f"\nRevenue Standards:")
            print(f"  Min: ${stats['revenue_range']['min']}M")
            print(f"  Max: ${stats['revenue_range']['max']}M")
            print(f"  Average: ${stats['revenue_range']['average']:.2f}M")
        if stats['employee_range']['average']:
            print(f"\nEmployee Standards:")
            print(f"  Min: {stats['employee_range']['min']}")
            print(f"  Max: {stats['employee_range']['max']}")
            print(f"  Average: {int(stats['employee_range']['average'])}")
    
    return 0


def validate_command(json_path, clean=False):
    """Validate and optionally clean data"""
    print_header("VALIDATE NAICS DATA")
    
    if not Path(json_path).exists():
        print(f"❌ Error: JSON file not found: {json_path}")
        return 1
    
    validator = NAICSValidator(json_path)
    results = validator.validate_all()
    
    print(f"Overall Status: {'✓ VALID' if results['valid'] else '✗ INVALID'}")
    print(f"Total Issues: {results['total_issues']}\n")
    
    print("Check Results:")
    for check_name, check_result in results['checks'].items():
        status = "✓" if check_result['passed'] else "✗"
        print(f"  {status} {check_name}: {check_result['issues_found']} issues")
    
    if clean:
        print("\nCleaning data...")
        fixes = validator.clean_data()
        print(f"✓ Applied {fixes} fixes")
        
        cleaned_path = json_path.replace('.json', '_cleaned.json')
        validator.save_cleaned_data(cleaned_path)
        
        report_path = json_path.replace('.json', '_validation_report.json')
        validator.generate_report(report_path)
        print(f"✓ Validation report: {report_path}")
    
    return 0 if results['valid'] else 1


def export_command(json_path, format_type, output_path, sector_code=None):
    """Export data in different formats"""
    print_header("EXPORT NAICS DATA")
    
    if not Path(json_path).exists():
        print(f"❌ Error: JSON file not found: {json_path}")
        return 1
    
    query = NAICSQuery(json_path)
    
    if format_type == "csv":
        if sector_code:
            success = query.export_sector_csv(sector_code, output_path)
            if success:
                print(f"✓ Exported sector {sector_code} to CSV")
                return 0
            return 1
        else:
            print("❌ Sector code required for CSV export")
            print("   Usage: export csv <sector_code> <output_path>")
            return 1
    
    elif format_type == "summary":
        stats = query.get_statistics()
        with open(output_path, 'w') as f:
            json.dump(stats, f, indent=2)
        print(f"✓ Exported summary to: {output_path}")
        return 0
    
    return 0


def list_sectors(json_path):
    """List all sectors"""
    print_header("NAICS SECTORS")
    
    if not Path(json_path).exists():
        print(f"❌ Error: JSON file not found: {json_path}")
        return 1
    
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    print(f"{'Code':<8} {'Name':<50} {'Industries':<12}")
    print("-" * 70)
    
    for sector in data['sectors']:
        code = sector['sector_code']
        name = sector['sector_name'][:48]
        count = len(sector['industries'])
        print(f"{code:<8} {name:<50} {count:<12}")
    
    return 0


def print_usage():
    """Print usage information"""
    print("""
NAICS Tools - Command Line Interface

Usage: python3 naics_cli.py <command> [options]

Commands:

  extract <pdf_path> <output_path>
      Extract NAICS data from PDF
      Example: extract input.pdf output.json

  query <json_path> <type> <value>
      Query the extracted data
      Types: code, keyword, sector, stats
      Examples:
        query data.json code 111110
        query data.json keyword "software"
        query data.json sector 54
        query data.json stats

  validate <json_path> [--clean]
      Validate data quality
      Use --clean to fix issues
      Example: validate data.json --clean

  export <json_path> <format> <output> [sector]
      Export data in different formats
      Formats: csv, summary
      Example: export data.json csv sector_54.csv 54

  list <json_path>
      List all sectors
      Example: list data.json

  help
      Show this help message

Default Paths:
  PDF: /mnt/user-data/uploads/naics-codes-with-sba-size-standards.pdf
  JSON: /mnt/user-data/outputs/naics_complete.json
    """)


def main():
    """Main CLI entry point"""
    if len(sys.argv) < 2:
        print_usage()
        return 1
    
    command = sys.argv[1].lower()
    
    # Default paths
    default_pdf = "naics-codes-with-sba-size-standards.pdf"
    default_json = "naics_complete.json"
    
    if command == "help":
        print_usage()
        return 0
    
    elif command == "extract":
        pdf_path = sys.argv[2] if len(sys.argv) > 2 else default_pdf
        output_path = sys.argv[3] if len(sys.argv) > 3 else default_json
        return extract_command(pdf_path, output_path)
    
    elif command == "query":
        if len(sys.argv) < 4:
            print("❌ Usage: query <json_path> <type> <value>")
            return 1
        json_path = sys.argv[2]
        query_type = sys.argv[3]
        query_value = sys.argv[4] if len(sys.argv) > 4 else ""
        return query_command(json_path, query_type, query_value)
    
    elif command == "validate":
        json_path = sys.argv[2] if len(sys.argv) > 2 else default_json
        clean = "--clean" in sys.argv
        return validate_command(json_path, clean)
    
    elif command == "export":
        if len(sys.argv) < 5:
            print("❌ Usage: export <json_path> <format> <output> [sector]")
            return 1
        json_path = sys.argv[2]
        format_type = sys.argv[3]
        output_path = sys.argv[4]
        sector_code = sys.argv[5] if len(sys.argv) > 5 else None
        return export_command(json_path, format_type, output_path, sector_code)
    
    elif command == "list":
        json_path = sys.argv[2] if len(sys.argv) > 2 else default_json
        return list_sectors(json_path)
    
    else:
        print(f"❌ Unknown command: {command}")
        print("   Use 'help' to see available commands")
        return 1


if __name__ == "__main__":
    sys.exit(main())
