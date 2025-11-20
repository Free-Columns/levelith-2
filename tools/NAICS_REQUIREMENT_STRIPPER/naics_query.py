#!/usr/bin/env python3
"""
NAICS Data Query Utilities
Helper functions to search, filter, and analyze extracted NAICS data
"""

import json
from typing import List, Dict, Optional, Any
from pathlib import Path


class NAICSQuery:
    """Query and analyze NAICS data"""
    
    def __init__(self, json_path: str):
        """Initialize with JSON data file"""
        self.json_path = json_path
        with open(json_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
        # Create lookup index for faster searches
        self.code_index = self._build_code_index()
        
    def _build_code_index(self) -> Dict[str, Dict]:
        """Build index of all NAICS codes for quick lookup"""
        index = {}
        for sector in self.data["sectors"]:
            for industry in sector["industries"]:
                code = industry["code"]
                index[code] = {
                    **industry,
                    "sector_code": sector["sector_code"],
                    "sector_name": sector["sector_name"]
                }
        return index
    
    def search_by_code(self, code: str) -> Optional[Dict]:
        """Search for industry by exact NAICS code"""
        return self.code_index.get(code)
    
    def search_by_keyword(self, keyword: str, case_sensitive: bool = False) -> List[Dict]:
        """Search for industries by keyword in title"""
        results = []
        search_term = keyword if case_sensitive else keyword.lower()
        
        for code, industry in self.code_index.items():
            title = industry["title"] if case_sensitive else industry["title"].lower()
            if search_term in title:
                results.append(industry)
        
        return results
    
    def get_sector(self, sector_code: str) -> Optional[Dict]:
        """Get all industries in a sector"""
        for sector in self.data["sectors"]:
            if sector["sector_code"] == sector_code:
                return sector
        return None
    
    def filter_by_size_standard(
        self, 
        min_millions: Optional[float] = None,
        max_millions: Optional[float] = None,
        min_employees: Optional[int] = None,
        max_employees: Optional[int] = None
    ) -> List[Dict]:
        """Filter industries by size standard ranges"""
        results = []
        
        for code, industry in self.code_index.items():
            # Check revenue standards
            if min_millions is not None or max_millions is not None:
                millions = industry.get("size_standard_millions")
                if millions:
                    if min_millions and millions < min_millions:
                        continue
                    if max_millions and millions > max_millions:
                        continue
                else:
                    continue
            
            # Check employee standards
            if min_employees is not None or max_employees is not None:
                employees = industry.get("size_standard_employees")
                if employees:
                    if min_employees and employees < min_employees:
                        continue
                    if max_employees and employees > max_employees:
                        continue
                else:
                    continue
            
            results.append(industry)
        
        return results
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistical summary of the data"""
        stats = {
            "total_sectors": len(self.data["sectors"]),
            "total_industries": len(self.code_index),
            "by_sector": [],
            "size_standards": {
                "revenue_based": 0,
                "employee_based": 0,
                "both": 0
            },
            "revenue_range": {
                "min": None,
                "max": None,
                "average": None
            },
            "employee_range": {
                "min": None,
                "max": None,
                "average": None
            }
        }
        
        revenue_values = []
        employee_values = []
        
        for code, industry in self.code_index.items():
            has_revenue = "size_standard_millions" in industry
            has_employees = "size_standard_employees" in industry
            
            if has_revenue:
                stats["size_standards"]["revenue_based"] += 1
                revenue_values.append(industry["size_standard_millions"])
            if has_employees:
                stats["size_standards"]["employee_based"] += 1
                employee_values.append(industry["size_standard_employees"])
            if has_revenue and has_employees:
                stats["size_standards"]["both"] += 1
        
        # Calculate ranges
        if revenue_values:
            stats["revenue_range"] = {
                "min": min(revenue_values),
                "max": max(revenue_values),
                "average": sum(revenue_values) / len(revenue_values)
            }
        
        if employee_values:
            stats["employee_range"] = {
                "min": min(employee_values),
                "max": max(employee_values),
                "average": sum(employee_values) / len(employee_values)
            }
        
        # Sector breakdown
        for sector in self.data["sectors"]:
            stats["by_sector"].append({
                "code": sector["sector_code"],
                "name": sector["sector_name"],
                "industries": len(sector["industries"])
            })
        
        return stats
    
    def export_sector_csv(self, sector_code: str, output_path: str):
        """Export a sector's industries to CSV"""
        import csv
        
        sector = self.get_sector(sector_code)
        if not sector:
            print(f"Sector {sector_code} not found")
            return False
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'code', 'title', 'size_standard_millions', 'size_standard_employees'
            ])
            writer.writeheader()
            
            for industry in sector["industries"]:
                row = {
                    'code': industry['code'],
                    'title': industry['title'],
                    'size_standard_millions': industry.get('size_standard_millions', ''),
                    'size_standard_employees': industry.get('size_standard_employees', '')
                }
                writer.writerow(row)
        
        print(f"✓ Exported {len(sector['industries'])} industries to {output_path}")
        return True
    
    def compare_codes(self, code1: str, code2: str) -> Dict:
        """Compare two NAICS codes"""
        industry1 = self.search_by_code(code1)
        industry2 = self.search_by_code(code2)
        
        if not industry1:
            return {"error": f"Code {code1} not found"}
        if not industry2:
            return {"error": f"Code {code2} not found"}
        
        comparison = {
            "code1": {
                "code": code1,
                "title": industry1["title"],
                "sector": industry1["sector_name"],
                "size_standard_millions": industry1.get("size_standard_millions"),
                "size_standard_employees": industry1.get("size_standard_employees")
            },
            "code2": {
                "code": code2,
                "title": industry2["title"],
                "sector": industry2["sector_name"],
                "size_standard_millions": industry2.get("size_standard_millions"),
                "size_standard_employees": industry2.get("size_standard_employees")
            },
            "same_sector": industry1["sector_code"] == industry2["sector_code"],
            "differences": []
        }
        
        # Compare size standards
        m1 = industry1.get("size_standard_millions")
        m2 = industry2.get("size_standard_millions")
        if m1 and m2:
            comparison["differences"].append({
                "metric": "Revenue Standard",
                "difference": m2 - m1,
                "percentage": ((m2 - m1) / m1) * 100 if m1 else 0
            })
        
        return comparison


def demo_queries():
    """Demonstrate query capabilities"""
    json_path = "/mnt/user-data/outputs/naics_complete.json"
    
    if not Path(json_path).exists():
        print(f"Error: {json_path} not found. Run naics_extractor.py first.")
        return
    
    print("="*60)
    print("NAICS Query Utilities Demo")
    print("="*60)
    
    query = NAICSQuery(json_path)
    
    # Example 1: Search by code
    print("\n1. Search by code (111110):")
    result = query.search_by_code("111110")
    if result:
        print(f"   {result['code']}: {result['title']}")
        print(f"   Sector: {result['sector_name']}")
        print(f"   Size Standard: ${result.get('size_standard_millions', 'N/A')}M")
    
    # Example 2: Keyword search
    print("\n2. Search for 'Software' industries:")
    results = query.search_by_keyword("software")
    for r in results[:5]:  # Show first 5
        print(f"   {r['code']}: {r['title']}")
    print(f"   ... found {len(results)} total")
    
    # Example 3: Filter by size
    print("\n3. Industries with $40M+ revenue standard:")
    results = query.filter_by_size_standard(min_millions=40.0)
    print(f"   Found {len(results)} industries")
    for r in results[:3]:
        print(f"   {r['code']}: {r['title']} (${r['size_standard_millions']}M)")
    
    # Example 4: Get statistics
    print("\n4. Overall Statistics:")
    stats = query.get_statistics()
    print(f"   Total Sectors: {stats['total_sectors']}")
    print(f"   Total Industries: {stats['total_industries']}")
    print(f"   Revenue-based standards: {stats['size_standards']['revenue_based']}")
    print(f"   Employee-based standards: {stats['size_standards']['employee_based']}")
    if stats['revenue_range']['average']:
        print(f"   Average revenue standard: ${stats['revenue_range']['average']:.2f}M")
    
    # Example 5: Export sector to CSV
    print("\n5. Exporting Sector 54 to CSV:")
    query.export_sector_csv("54", "/mnt/user-data/outputs/sector_54_professional_services.csv")
    
    print("\n" + "="*60)
    print("Query utilities ready for use!")
    print("="*60)


if __name__ == "__main__":
    demo_queries()
