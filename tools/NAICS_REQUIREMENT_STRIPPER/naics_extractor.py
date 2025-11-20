#!/usr/bin/env python3
"""
NAICS Size Standards Extractor
Extracts NAICS codes and SBA size standards from PDF and converts to JSON
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

try:
    import pdfplumber
except ImportError:
    print("Installing pdfplumber...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--break-system-packages", "pdfplumber"])
    import pdfplumber


class NAICSExtractor:
    """Extract NAICS codes and size standards from SBA PDF"""
    
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.data = {
            "document_info": {},
            "sectors": [],
            "footnotes": [],
            "metadata": {}
        }
        
    def extract_document_info(self, first_page_text: str) -> Dict[str, str]:
        """Extract document metadata from first page"""
        info = {
            "title": "Table of Small Business Size Standards Matched to North American Industry Classification System Codes",
            "source": "U.S. Small Business Administration",
            "effective_date": None,
            "version": None
        }
        
        # Extract effective date
        date_match = re.search(r'effective\s+(\w+\s+\d+,\s+\d{4})', first_page_text, re.IGNORECASE)
        if date_match:
            info["effective_date"] = date_match.group(1)
            
        # Extract NAICS version
        naics_match = re.search(r'NAICS\s+(\d{4})', first_page_text)
        if naics_match:
            info["version"] = f"NAICS {naics_match.group(1)}"
            
        return info
    
    def parse_sector_header(self, text: str) -> Optional[Tuple[str, str]]:
        """Parse sector code and name from header"""
        # Pattern: Sector 11 – Agriculture, Forestry, Fishing and Hunting
        pattern = r'Sector\s+(\d+)\s*[–-]\s*(.+?)(?:\n|$)'
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1), match.group(2).strip()
        return None
    
    def parse_naics_row(self, row: List[str]) -> Optional[Dict[str, Any]]:
        """Parse a single NAICS code row from table"""
        if not row or len(row) < 2:
            return None
            
        # Clean up the data
        code = str(row[0]).strip() if row[0] else ""
        title = str(row[1]).strip() if len(row) > 1 and row[1] else ""
        size_millions = str(row[2]).strip() if len(row) > 2 and row[2] else ""
        size_employees = str(row[3]).strip() if len(row) > 3 and row[3] else ""
        
        # Skip header rows and empty rows
        if not code or code.upper() == "NAICS CODES" or "NAICS" in code.upper():
            return None
            
        # Skip rows that don't have valid NAICS codes
        if not re.match(r'^\d{6}', code):
            return None
        
        # Parse the code (handle exceptions like "541330 (Exception 1)")
        code_match = re.match(r'(\d{6})(?:\s*\(Exception\s*(\d+)\))?', code)
        if not code_match:
            return None
            
        naics_code = code_match.group(1)
        exception = code_match.group(2)
        
        # Build the result
        result = {
            "code": naics_code,
            "title": title
        }
        
        if exception:
            result["exception"] = int(exception)
            result["code"] = f"{naics_code}-E{exception}"
        
        # Parse size standards
        if size_millions and size_millions not in ['', '-', 'N/A']:
            # Remove $ and convert to float
            clean_millions = size_millions.replace('$', '').replace(',', '').strip()
            try:
                result["size_standard_millions"] = float(clean_millions)
            except ValueError:
                pass
        
        if size_employees and size_employees not in ['', '-', 'N/A']:
            # Remove commas and convert to int
            clean_employees = size_employees.replace(',', '').strip()
            try:
                result["size_standard_employees"] = int(clean_employees)
            except ValueError:
                pass
        
        # Handle special asset-based standards (for financial institutions)
        if "in assets" in size_millions.lower():
            result["size_standard_type"] = "assets"
            asset_match = re.search(r'\$(\d+(?:,\d+)?)\s*million', size_millions)
            if asset_match:
                result["size_standard_millions"] = float(asset_match.group(1).replace(',', ''))
        
        return result if result.get("title") else None
    
    def extract_table_data(self, page) -> List[Dict[str, Any]]:
        """Extract table data from a PDF page"""
        results = []
        
        try:
            tables = page.extract_tables()
            
            for table in tables:
                if not table:
                    continue
                    
                # Skip header rows
                for row in table[1:]:  # Skip first row (headers)
                    if not row:
                        continue
                        
                    parsed = self.parse_naics_row(row)
                    if parsed:
                        results.append(parsed)
                        
        except Exception as e:
            print(f"Warning: Error extracting table from page: {e}")
            
        return results
    
    def process_pdf(self) -> Dict[str, Any]:
        """Main processing function"""
        print(f"Opening PDF: {self.pdf_path}")
        
        with pdfplumber.open(self.pdf_path) as pdf:
            total_pages = len(pdf.pages)
            print(f"Total pages: {total_pages}")
            
            current_sector = None
            
            for page_num, page in enumerate(pdf.pages, 1):
                print(f"Processing page {page_num}/{total_pages}...", end='\r')
                
                text = page.extract_text()
                
                # Extract document info from first page
                if page_num == 1:
                    self.data["document_info"] = self.extract_document_info(text)
                
                # Check for sector header
                sector_info = self.parse_sector_header(text)
                if sector_info:
                    sector_code, sector_name = sector_info
                    current_sector = {
                        "sector_code": sector_code,
                        "sector_name": sector_name,
                        "industries": []
                    }
                    self.data["sectors"].append(current_sector)
                    print(f"\nFound Sector {sector_code}: {sector_name}")
                
                # Extract table data
                industries = self.extract_table_data(page)
                if industries and current_sector:
                    current_sector["industries"].extend(industries)
                    
                # Look for footnotes
                if "Footnote" in text or re.search(r'^\d+\.', text, re.MULTILINE):
                    footnote_section = self.extract_footnotes(text)
                    if footnote_section:
                        self.data["footnotes"].extend(footnote_section)
            
            print(f"\n✓ Processed {total_pages} pages")
            
        # Add metadata
        self.data["metadata"] = {
            "total_sectors": len(self.data["sectors"]),
            "total_industries": sum(len(s["industries"]) for s in self.data["sectors"]),
            "extraction_date": self.get_timestamp(),
            "size_standard_types": [
                {
                    "type": "size_standard_millions",
                    "description": "Annual receipts in millions of dollars",
                    "unit": "USD (millions)"
                },
                {
                    "type": "size_standard_employees",
                    "description": "Number of employees",
                    "unit": "employees"
                },
                {
                    "type": "size_standard_assets",
                    "description": "Total assets in millions of dollars (financial institutions)",
                    "unit": "USD (millions)"
                }
            ],
            "notes": [
                "Sector 42 and 44-45 codes should not be used for Government supply acquisitions",
                "Manufacturing NAICS codes should be used for supply acquisitions instead",
                "Some industries have exceptions with different size standards"
            ]
        }
        
        return self.data
    
    def extract_footnotes(self, text: str) -> List[Dict[str, str]]:
        """Extract footnotes from text"""
        footnotes = []
        
        # Pattern for footnote: "1. NAICS code..."
        pattern = r'(\d+)\.\s+(NAICS[^\.]+\.)'
        matches = re.finditer(pattern, text)
        
        for match in matches:
            footnotes.append({
                "number": match.group(1),
                "text": match.group(2).strip()
            })
        
        return footnotes
    
    def get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def save_json(self, output_path: str, indent: int = 2):
        """Save extracted data to JSON file"""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=indent, ensure_ascii=False)
        
        print(f"\n✓ Data saved to: {output_file}")
        print(f"  - Total sectors: {self.data['metadata']['total_sectors']}")
        print(f"  - Total industries: {self.data['metadata']['total_industries']}")
        print(f"  - File size: {output_file.stat().st_size:,} bytes")
        
        return str(output_file)
    
    def generate_summary(self) -> Dict[str, Any]:
        """Generate summary statistics"""
        summary = {
            "sectors": [],
            "size_standard_distribution": {
                "by_millions": 0,
                "by_employees": 0,
                "by_assets": 0
            }
        }
        
        for sector in self.data["sectors"]:
            sector_summary = {
                "code": sector["sector_code"],
                "name": sector["sector_name"],
                "total_industries": len(sector["industries"]),
                "size_standards": {
                    "millions": 0,
                    "employees": 0
                }
            }
            
            for industry in sector["industries"]:
                if "size_standard_millions" in industry:
                    sector_summary["size_standards"]["millions"] += 1
                    summary["size_standard_distribution"]["by_millions"] += 1
                if "size_standard_employees" in industry:
                    sector_summary["size_standards"]["employees"] += 1
                    summary["size_standard_distribution"]["by_employees"] += 1
            
            summary["sectors"].append(sector_summary)
        
        return summary


def main():
    """Main execution function"""
    # File paths
    pdf_path = "/mnt/user-data/uploads/naics-codes-with-sba-size-standards.pdf"
    output_path = "/mnt/user-data/outputs/naics_complete.json"
    summary_path = "/mnt/user-data/outputs/naics_summary.json"
    
    # Check if PDF exists
    if not Path(pdf_path).exists():
        print(f"Error: PDF file not found at {pdf_path}")
        return 1
    
    print("="*60)
    print("NAICS Size Standards Extractor")
    print("="*60)
    
    # Create extractor and process PDF
    extractor = NAICSExtractor(pdf_path)
    
    try:
        data = extractor.process_pdf()
        
        # Save full JSON
        extractor.save_json(output_path)
        
        # Generate and save summary
        summary = extractor.generate_summary()
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
        print(f"✓ Summary saved to: {summary_path}")
        
        print("\n" + "="*60)
        print("EXTRACTION COMPLETE")
        print("="*60)
        
        return 0
        
    except Exception as e:
        print(f"\n✗ Error during extraction: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
