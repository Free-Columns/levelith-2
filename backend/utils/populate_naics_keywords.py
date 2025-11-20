"""
NAICS Keywords and Aliases Generator

Utility script to help populate keywords and aliases fields for NAICS codes.

This script provides:
1. Automatic keyword extraction from titles and descriptions
2. Manual alias definitions for common industries
3. Batch update utilities
4. Validation tools

Usage:
    python -m backend.utils.populate_naics_keywords
"""

import re
from typing import List, Set, Dict
from sqlalchemy.orm import Session

from backend.database import SessionLocal, get_db_context
from backend.models.db_models import NAICSCodeDB


# ============================================================================
# KEYWORD EXTRACTION
# ============================================================================

# Common words to exclude from keyword extraction
STOPWORDS = {
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
    'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
    'to', 'was', 'will', 'with', 'not', 'all', 'other', 'nec',
    'services', 'activities', 'except', 'including', 'establishments',
    'primarily', 'engaged', 'such'
}

# Minimum word length for keywords
MIN_KEYWORD_LENGTH = 3


def extract_keywords_from_text(text: str, max_keywords: int = 10) -> List[str]:
    """
    Extract meaningful keywords from text.
    
    Args:
        text: Text to extract keywords from
        max_keywords: Maximum number of keywords to extract
        
    Returns:
        List of extracted keywords
    """
    if not text:
        return []
    
    # Lowercase and tokenize
    text = text.lower()
    
    # Remove special characters but keep hyphens in compound words
    text = re.sub(r'[^\w\s-]', ' ', text)
    
    # Split into words
    words = text.split()
    
    # Filter words
    keywords = []
    for word in words:
        word = word.strip('-')  # Remove leading/trailing hyphens
        
        if (len(word) >= MIN_KEYWORD_LENGTH and 
            word not in STOPWORDS and 
            not word.isdigit()):
            keywords.append(word)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_keywords = []
    for keyword in keywords:
        if keyword not in seen:
            seen.add(keyword)
            unique_keywords.append(keyword)
    
    return unique_keywords[:max_keywords]


def generate_keywords_for_code(code: NAICSCodeDB) -> List[str]:
    """
    Generate keywords for a NAICS code based on its title and description.
    
    Args:
        code: NAICSCodeDB instance
        
    Returns:
        List of generated keywords
    """
    all_text = code.title
    if code.description:
        all_text += " " + code.description
    
    return extract_keywords_from_text(all_text, max_keywords=15)


# ============================================================================
# COMMON ALIASES
# ============================================================================

# Predefined aliases for common NAICS codes
# Format: code -> list of aliases
PREDEFINED_ALIASES: Dict[str, List[str]] = {
    # Technology / Software
    "541511": [
        "Software Development",
        "Custom Software",
        "Application Development",
        "Software Engineering",
        "IT Development"
    ],
    "541512": [
        "Computer Systems Design",
        "IT Consulting",
        "Systems Integration",
        "IT Solutions"
    ],
    "541519": [
        "IT Services",
        "Computer Services",
        "Technology Services"
    ],
    "518210": [
        "Cloud Computing",
        "Data Processing",
        "Web Hosting",
        "SaaS"
    ],
    "519130": [
        "Internet Publishing",
        "Web Publishing",
        "Online Media"
    ],
    
    # Professional Services
    "541110": [
        "Law Firms",
        "Legal Services",
        "Attorneys"
    ],
    "541211": [
        "CPA",
        "Accounting Firms",
        "Tax Services",
        "Bookkeeping"
    ],
    "541330": [
        "Engineering Services",
        "Engineering Firms",
        "Consulting Engineers"
    ],
    "541611": [
        "Management Consulting",
        "Business Consulting",
        "Strategy Consulting"
    ],
    "541810": [
        "Advertising Agencies",
        "Ad Agencies",
        "Marketing Agencies"
    ],
    "541820": [
        "PR Firms",
        "Public Relations",
        "Communications Agencies"
    ],
    "541910": [
        "Market Research",
        "Marketing Research",
        "Consumer Research"
    ],
    
    # Healthcare
    "621111": [
        "Doctor's Offices",
        "Physician Offices",
        "Medical Practices"
    ],
    "621210": [
        "Dental Offices",
        "Dentists",
        "Dental Practices"
    ],
    "621511": [
        "Medical Labs",
        "Clinical Labs",
        "Diagnostic Labs"
    ],
    "622110": [
        "Hospitals",
        "General Hospitals",
        "Medical Centers"
    ],
    "623110": [
        "Nursing Homes",
        "Care Facilities",
        "Long-term Care"
    ],
    
    # Retail
    "445110": [
        "Supermarkets",
        "Grocery Stores",
        "Food Stores"
    ],
    "452311": [
        "Warehouse Clubs",
        "Wholesale Clubs",
        "Membership Stores"
    ],
    "454110": [
        "E-commerce",
        "Online Retail",
        "Internet Retail"
    ],
    
    # Food Service
    "722511": [
        "Full-Service Restaurants",
        "Sit-Down Restaurants",
        "Table Service"
    ],
    "722513": [
        "Fast Food",
        "Quick Service",
        "QSR"
    ],
    "722515": [
        "Food Trucks",
        "Mobile Food Services"
    ],
    
    # Real Estate
    "531210": [
        "Property Management",
        "Real Estate Management",
        "Building Management"
    ],
    "531390": [
        "Real Estate Agents",
        "Realtors",
        "Property Brokers"
    ],
    
    # Construction
    "236115": [
        "Homebuilders",
        "Home Construction",
        "Residential Construction"
    ],
    "236220": [
        "Commercial Construction",
        "Commercial Builders"
    ],
    "238210": [
        "Electrical Contractors",
        "Electricians"
    ],
    "238220": [
        "Plumbing",
        "Plumbers",
        "HVAC"
    ],
    
    # Manufacturing
    "334111": [
        "Computer Manufacturing",
        "PC Manufacturing"
    ],
    "335311": [
        "Power Generation Equipment"
    ],
    "336411": [
        "Aircraft Manufacturing",
        "Aerospace Manufacturing"
    ],
    
    # Finance
    "522110": [
        "Commercial Banks",
        "Banking",
        "Retail Banking"
    ],
    "523110": [
        "Investment Banking",
        "Securities Trading"
    ],
    "524113": [
        "Insurance Brokers",
        "Insurance Agents"
    ],
    
    # Education
    "611310": [
        "Colleges",
        "Universities",
        "Higher Education"
    ],
    "611430": [
        "Job Training",
        "Vocational Training",
        "Skills Training"
    ],
    "611699": [
        "Tutoring",
        "Test Prep",
        "Educational Services"
    ]
}


def get_predefined_aliases(code: str) -> List[str]:
    """Get predefined aliases for a NAICS code."""
    return PREDEFINED_ALIASES.get(code, [])


# ============================================================================
# BATCH UPDATE UTILITIES
# ============================================================================

def populate_keywords_for_all_codes(
    db: Session,
    overwrite: bool = False,
    dry_run: bool = True
) -> Dict[str, int]:
    """
    Populate keywords for all NAICS codes in the database.
    
    Args:
        db: Database session
        overwrite: If True, overwrite existing keywords. If False, only populate empty ones.
        dry_run: If True, don't commit changes
        
    Returns:
        Dictionary with statistics
    """
    stats = {
        "total_codes": 0,
        "updated": 0,
        "skipped": 0,
        "errors": 0
    }
    
    codes = db.query(NAICSCodeDB).all()
    stats["total_codes"] = len(codes)
    
    for code in codes:
        try:
            # Skip if keywords exist and we're not overwriting
            if code.keywords and len(code.keywords) > 0 and not overwrite:
                stats["skipped"] += 1
                continue
            
            # Generate keywords
            keywords = generate_keywords_for_code(code)
            
            if keywords:
                code.keywords = keywords
                stats["updated"] += 1
                
                if not dry_run:
                    db.add(code)
                    
                print(f"✓ {code.code}: {', '.join(keywords[:5])}")
            else:
                stats["skipped"] += 1
                
        except Exception as e:
            print(f"✗ Error processing {code.code}: {e}")
            stats["errors"] += 1
    
    if not dry_run:
        db.commit()
        print("\n✓ Changes committed to database")
    else:
        print("\n⚠ DRY RUN - No changes committed")
    
    return stats


def populate_aliases_for_all_codes(
    db: Session,
    overwrite: bool = False,
    dry_run: bool = True
) -> Dict[str, int]:
    """
    Populate predefined aliases for NAICS codes.
    
    Args:
        db: Database session
        overwrite: If True, overwrite existing aliases
        dry_run: If True, don't commit changes
        
    Returns:
        Dictionary with statistics
    """
    stats = {
        "total_codes": len(PREDEFINED_ALIASES),
        "updated": 0,
        "not_found": 0,
        "errors": 0
    }
    
    for code_str, aliases in PREDEFINED_ALIASES.items():
        try:
            code = db.query(NAICSCodeDB).filter_by(code=code_str).first()
            
            if not code:
                print(f"✗ Code {code_str} not found in database")
                stats["not_found"] += 1
                continue
            
            # Skip if aliases exist and we're not overwriting
            if code.aliases and len(code.aliases) > 0 and not overwrite:
                continue
            
            code.aliases = aliases
            stats["updated"] += 1
            
            if not dry_run:
                db.add(code)
            
            print(f"✓ {code_str}: {', '.join(aliases)}")
            
        except Exception as e:
            print(f"✗ Error processing {code_str}: {e}")
            stats["errors"] += 1
    
    if not dry_run:
        db.commit()
        print("\n✓ Changes committed to database")
    else:
        print("\n⚠ DRY RUN - No changes committed")
    
    return stats


def add_custom_alias(
    db: Session,
    code: str,
    alias: str,
    dry_run: bool = False
) -> bool:
    """
    Add a custom alias to a NAICS code.
    
    Args:
        db: Database session
        code: NAICS code
        alias: Alias to add
        dry_run: If True, don't commit changes
        
    Returns:
        True if successful, False otherwise
    """
    try:
        naics = db.query(NAICSCodeDB).filter_by(code=code).first()
        
        if not naics:
            print(f"✗ Code {code} not found")
            return False
        
        # Initialize aliases if empty
        if not naics.aliases:
            naics.aliases = []
        
        # Check if alias already exists
        if alias in naics.aliases:
            print(f"⚠ Alias '{alias}' already exists for code {code}")
            return False
        
        # Add alias
        naics.aliases.append(alias)
        
        if not dry_run:
            db.add(naics)
            db.commit()
            print(f"✓ Added alias '{alias}' to code {code}")
        else:
            print(f"⚠ DRY RUN - Would add alias '{alias}' to code {code}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


# ============================================================================
# VALIDATION
# ============================================================================

def validate_keywords_and_aliases(db: Session) -> Dict[str, any]:
    """
    Validate keywords and aliases in the database.
    
    Returns:
        Dictionary with validation results
    """
    codes = db.query(NAICSCodeDB).all()
    
    stats = {
        "total_codes": len(codes),
        "codes_with_keywords": 0,
        "codes_with_aliases": 0,
        "empty_keywords": 0,
        "empty_aliases": 0,
        "invalid_keywords": [],
        "invalid_aliases": []
    }
    
    for code in codes:
        # Check keywords
        if code.keywords and len(code.keywords) > 0:
            stats["codes_with_keywords"] += 1
            
            # Validate keyword format
            for keyword in code.keywords:
                if not isinstance(keyword, str) or len(keyword) < MIN_KEYWORD_LENGTH:
                    stats["invalid_keywords"].append({
                        "code": code.code,
                        "keyword": keyword
                    })
        else:
            stats["empty_keywords"] += 1
        
        # Check aliases
        if code.aliases and len(code.aliases) > 0:
            stats["codes_with_aliases"] += 1
            
            # Validate alias format
            for alias in code.aliases:
                if not isinstance(alias, str) or len(alias) < 2:
                    stats["invalid_aliases"].append({
                        "code": code.code,
                        "alias": alias
                    })
        else:
            stats["empty_aliases"] += 1
    
    # Calculate percentages
    stats["keywords_coverage"] = round(
        (stats["codes_with_keywords"] / stats["total_codes"]) * 100, 1
    )
    stats["aliases_coverage"] = round(
        (stats["codes_with_aliases"] / stats["total_codes"]) * 100, 1
    )
    
    return stats


# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    """Main CLI interface."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Populate keywords and aliases for NAICS codes"
    )
    
    parser.add_argument(
        "command",
        choices=["keywords", "aliases", "validate", "add-alias"],
        help="Command to execute"
    )
    
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing keywords/aliases"
    )
    
    parser.add_argument(
        "--commit",
        action="store_true",
        help="Commit changes (default is dry run)"
    )
    
    parser.add_argument(
        "--code",
        type=str,
        help="NAICS code (for add-alias command)"
    )
    
    parser.add_argument(
        "--alias",
        type=str,
        help="Alias to add (for add-alias command)"
    )
    
    args = parser.parse_args()
    
    with get_db_context() as db:
        if args.command == "keywords":
            print("Populating keywords...")
            stats = populate_keywords_for_all_codes(
                db,
                overwrite=args.overwrite,
                dry_run=not args.commit
            )
            print(f"\nStats: {stats}")
            
        elif args.command == "aliases":
            print("Populating aliases...")
            stats = populate_aliases_for_all_codes(
                db,
                overwrite=args.overwrite,
                dry_run=not args.commit
            )
            print(f"\nStats: {stats}")
            
        elif args.command == "validate":
            print("Validating keywords and aliases...")
            stats = validate_keywords_and_aliases(db)
            print(f"\nValidation Results:")
            print(f"  Total codes: {stats['total_codes']}")
            print(f"  Keywords coverage: {stats['keywords_coverage']}%")
            print(f"  Aliases coverage: {stats['aliases_coverage']}%")
            print(f"  Invalid keywords: {len(stats['invalid_keywords'])}")
            print(f"  Invalid aliases: {len(stats['invalid_aliases'])}")
            
        elif args.command == "add-alias":
            if not args.code or not args.alias:
                print("✗ Error: --code and --alias are required for add-alias command")
                return
            
            add_custom_alias(
                db,
                code=args.code,
                alias=args.alias,
                dry_run=not args.commit
            )


if __name__ == "__main__":
    main()