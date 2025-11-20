"""
Enhanced NAICS Search Service

Leverages keywords, aliases, and advanced search capabilities for better
NAICS code discovery and matching.

This should be added to backend/services/naics_service.py or created as
a separate search utility.
"""

from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from sqlalchemy import or_, and_, func
from sqlalchemy.orm import Session

from backend.models.db_models import NAICSCodeDB
from backend.models.naics import NAICSCode, NAICSCategory, NAICSLevel
from backend.database import get_db_context


@dataclass
class SearchResult:
    """
    Enhanced search result with relevance scoring.
    
    Attributes:
        naics_code: The matched NAICS code object
        score: Relevance score (0-100)
        match_type: Where the match was found (code, title, keyword, alias, etc.)
        matched_terms: List of terms that matched
    """
    naics_code: NAICSCode
    score: float
    match_type: str
    matched_terms: List[str]


class EnhancedNAICSSearch:
    """
    Advanced NAICS code search with keyword/alias support and relevance ranking.
    
    Features:
    - Multi-field search (code, title, keywords, aliases, description)
    - Relevance scoring and ranking
    - Fuzzy matching support
    - Category and level filtering
    - Autocomplete suggestions
    - Related code discovery
    """
    
    def __init__(self, db: Optional[Session] = None):
        """Initialize search service."""
        self._db = db
    
    def search(
        self,
        query: str,
        category: Optional[NAICSCategory] = None,
        level: Optional[NAICSLevel] = None,
        limit: int = 20,
        min_score: float = 0.0
    ) -> List[SearchResult]:
        """
        Perform comprehensive search across all NAICS fields.
        
        Searches in priority order:
        1. Exact code match (score: 100)
        2. Code starts with query (score: 90)
        3. Exact title match (score: 85)
        4. Title starts with query (score: 80)
        5. Alias exact match (score: 75)
        6. Keyword exact match (score: 70)
        7. Title contains query (score: 60)
        8. Alias contains query (score: 55)
        9. Keyword contains query (score: 50)
        10. Description contains query (score: 40)
        
        Args:
            query: Search term
            category: Optional category filter
            level: Optional level filter
            limit: Maximum results to return
            min_score: Minimum relevance score (0-100)
            
        Returns:
            List of SearchResult objects sorted by relevance
        """
        if not query or not query.strip():
            return []
        
        query_lower = query.lower().strip()
        results = []
        
        with get_db_context() as db:
            # Build base query
            base_query = db.query(NAICSCodeDB).filter(NAICSCodeDB.is_active == True)
            
            # Apply filters
            if category:
                base_query = base_query.filter(NAICSCodeDB.category == category)
            if level:
                base_query = base_query.filter(NAICSCodeDB.level == level.value)
            
            # Get all matching codes
            codes = base_query.all()
            
            for code_db in codes:
                score, match_type, matched = self._calculate_relevance(code_db, query_lower)
                
                if score >= min_score:
                    # Convert to domain model
                    naics = self._db_to_domain(code_db)
                    
                    results.append(SearchResult(
                        naics_code=naics,
                        score=score,
                        match_type=match_type,
                        matched_terms=matched
                    ))
            
            # Sort by relevance score (highest first)
            results.sort(key=lambda r: r.score, reverse=True)
            
            return results[:limit]
    
    def _calculate_relevance(
        self,
        code_db: NAICSCodeDB,
        query: str
    ) -> Tuple[float, str, List[str]]:
        """
        Calculate relevance score for a NAICS code against a query.
        
        Returns:
            Tuple of (score, match_type, matched_terms)
        """
        matched_terms = []
        
        # 1. Exact code match (100 points)
        if code_db.code.lower() == query:
            return (100.0, "exact_code", [code_db.code])
        
        # 2. Code starts with query (90 points)
        if code_db.code.lower().startswith(query):
            return (90.0, "code_prefix", [code_db.code])
        
        # 3. Exact title match (85 points)
        if code_db.title.lower() == query:
            return (85.0, "exact_title", [code_db.title])
        
        # 4. Title starts with query (80 points)
        if code_db.title.lower().startswith(query):
            return (80.0, "title_prefix", [code_db.title])
        
        # 5. Alias exact match (75 points)
        if code_db.aliases:
            for alias in code_db.aliases:
                if alias.lower() == query:
                    return (75.0, "exact_alias", [alias])
        
        # 6. Keyword exact match (70 points)
        if code_db.keywords:
            for keyword in code_db.keywords:
                if keyword.lower() == query:
                    return (70.0, "exact_keyword", [keyword])
        
        # 7. Title contains query (60 points)
        if query in code_db.title.lower():
            matched_terms.append(code_db.title)
            return (60.0, "title_contains", matched_terms)
        
        # 8. Alias contains query (55 points)
        if code_db.aliases:
            for alias in code_db.aliases:
                if query in alias.lower():
                    matched_terms.append(alias)
            if matched_terms:
                return (55.0, "alias_contains", matched_terms)
        
        # 9. Keyword contains query (50 points)
        if code_db.keywords:
            for keyword in code_db.keywords:
                if query in keyword.lower():
                    matched_terms.append(keyword)
            if matched_terms:
                return (50.0, "keyword_contains", matched_terms)
        
        # 10. Description contains query (40 points)
        if code_db.description and query in code_db.description.lower():
            return (40.0, "description_contains", [query])
        
        return (0.0, "no_match", [])
    
    def autocomplete(
        self,
        partial: str,
        limit: int = 10,
        category: Optional[NAICSCategory] = None
    ) -> List[Dict[str, any]]:
        """
        Provide intelligent autocomplete suggestions.
        
        Prioritizes:
        1. Code matches
        2. Title matches
        3. Alias matches
        4. Keyword matches
        
        Args:
            partial: Partial search string
            limit: Maximum suggestions
            category: Optional category filter
            
        Returns:
            List of suggestion dictionaries with code, title, match_type
        """
        results = self.search(
            query=partial,
            category=category,
            limit=limit,
            min_score=40.0  # Only show reasonably relevant matches
        )
        
        suggestions = []
        for result in results:
            suggestions.append({
                "code": result.naics_code.code,
                "title": result.naics_code.title,
                "category": result.naics_code.category.value,
                "level": result.naics_code.level.value,
                "match_type": result.match_type,
                "score": result.score,
                "aliases": result.naics_code.aliases[:3],  # First 3 aliases
                "keywords": result.naics_code.keywords[:5],  # First 5 keywords
            })
        
        return suggestions
    
    def find_by_keywords(
        self,
        keywords: List[str],
        match_all: bool = False,
        limit: int = 20
    ) -> List[NAICSCode]:
        """
        Find NAICS codes by multiple keywords.
        
        Args:
            keywords: List of keywords to search for
            match_all: If True, code must match ALL keywords. If False, ANY keyword.
            limit: Maximum results
            
        Returns:
            List of matching NAICSCode objects
        """
        if not keywords:
            return []
        
        results = []
        
        with get_db_context() as db:
            base_query = db.query(NAICSCodeDB).filter(NAICSCodeDB.is_active == True)
            
            if match_all:
                # Must match ALL keywords
                for keyword in keywords:
                    keyword_lower = keyword.lower()
                    base_query = base_query.filter(
                        or_(
                            func.lower(NAICSCodeDB.title).contains(keyword_lower),
                            NAICSCodeDB.keywords.op('@>')(f'["{keyword}"]'),  # JSON contains
                        )
                    )
            else:
                # Match ANY keyword
                conditions = []
                for keyword in keywords:
                    keyword_lower = keyword.lower()
                    conditions.extend([
                        func.lower(NAICSCodeDB.title).contains(keyword_lower),
                        NAICSCodeDB.keywords.op('@>')(f'["{keyword}"]'),
                    ])
                
                base_query = base_query.filter(or_(*conditions))
            
            codes = base_query.limit(limit).all()
            results = [self._db_to_domain(code) for code in codes]
        
        return results
    
    def find_by_alias(self, alias: str, exact: bool = False) -> List[NAICSCode]:
        """
        Find NAICS codes by alias.
        
        Args:
            alias: Alias to search for
            exact: If True, exact match. If False, partial match.
            
        Returns:
            List of matching NAICSCode objects
        """
        results = []
        
        with get_db_context() as db:
            base_query = db.query(NAICSCodeDB).filter(NAICSCodeDB.is_active == True)
            
            if exact:
                # Exact match in JSON array
                base_query = base_query.filter(
                    NAICSCodeDB.aliases.op('@>')(f'["{alias}"]')
                )
            else:
                # This is trickier with JSON - we'll fetch all and filter in Python
                all_codes = base_query.all()
                alias_lower = alias.lower()
                
                for code in all_codes:
                    if code.aliases and any(alias_lower in a.lower() for a in code.aliases):
                        results.append(self._db_to_domain(code))
                
                return results
            
            codes = base_query.all()
            results = [self._db_to_domain(code) for code in codes]
        
        return results
    
    def get_related_codes(self, code: str, max_results: int = 10) -> List[NAICSCode]:
        """
        Find codes related to a given code.
        
        Uses:
        1. Cross-references field
        2. Same sector/subsector
        3. Similar keywords
        
        Args:
            code: NAICS code to find related codes for
            max_results: Maximum number of related codes
            
        Returns:
            List of related NAICSCode objects
        """
        related = []
        
        with get_db_context() as db:
            # Get the source code
            source = db.query(NAICSCodeDB).filter_by(code=code).first()
            if not source:
                return []
            
            # 1. Get explicitly cross-referenced codes
            if source.cross_references:
                cross_refs = db.query(NAICSCodeDB).filter(
                    NAICSCodeDB.code.in_(source.cross_references),
                    NAICSCodeDB.is_active == True
                ).all()
                related.extend([self._db_to_domain(c) for c in cross_refs])
            
            # 2. Get codes in same subsector (if we don't have enough)
            if len(related) < max_results and source.subsector:
                same_subsector = db.query(NAICSCodeDB).filter(
                    NAICSCodeDB.subsector == source.subsector,
                    NAICSCodeDB.code != code,
                    NAICSCodeDB.is_active == True
                ).limit(max_results - len(related)).all()
                
                related.extend([self._db_to_domain(c) for c in same_subsector])
            
            # 3. Get codes with similar keywords (if we still need more)
            if len(related) < max_results and source.keywords:
                # Find codes that share keywords
                similar = db.query(NAICSCodeDB).filter(
                    NAICSCodeDB.code != code,
                    NAICSCodeDB.is_active == True
                ).all()
                
                # Score by keyword overlap
                scored = []
                for candidate in similar:
                    if candidate.keywords:
                        overlap = len(set(source.keywords) & set(candidate.keywords))
                        if overlap > 0:
                            scored.append((overlap, candidate))
                
                # Sort by overlap and take top results
                scored.sort(key=lambda x: x[0], reverse=True)
                for _, candidate in scored[:max_results - len(related)]:
                    related.append(self._db_to_domain(candidate))
        
        # Remove duplicates (by code) and limit
        seen = set()
        unique_related = []
        for naics in related:
            if naics.code not in seen:
                seen.add(naics.code)
                unique_related.append(naics)
        
        return unique_related[:max_results]
    
    def _db_to_domain(self, db_code: NAICSCodeDB) -> NAICSCode:
        """Convert database model to domain model."""
        from backend.models.naics import create_naics_code
        
        naics_code = create_naics_code(
            code=db_code.code,
            title=db_code.title,
            description=db_code.description or "",
            category=db_code.category,
            is_active=db_code.is_active,
        )
        
        # Add all additional fields
        naics_code.sector = db_code.sector
        naics_code.subsector = db_code.subsector
        naics_code.industry_group = db_code.industry_group
        naics_code.industry_detail = db_code.industry_detail
        
        naics_code.sba_size_standard = db_code.sba_size_standard
        naics_code.sba_source = db_code.sba_source
        
        naics_code.keywords = db_code.keywords if db_code.keywords else []
        naics_code.aliases = db_code.aliases if db_code.aliases else []
        naics_code.examples = db_code.examples
        
        naics_code.cross_references = db_code.cross_references if db_code.cross_references else []
        naics_code.notes = db_code.notes
        naics_code.data_source = db_code.data_source
        
        naics_code.tags = db_code.tags if db_code.tags else []
        naics_code.custom_category = db_code.custom_category
        naics_code.admin_notes = db_code.admin_notes
        
        naics_code.year = db_code.year
        naics_code.created_at = db_code.created_at
        naics_code.updated_at = db_code.updated_at
        
        return naics_code


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

def example_usage():
    """Example usage of the enhanced search service."""
    
    search = EnhancedNAICSSearch()
    
    # 1. Comprehensive search with relevance ranking
    results = search.search("software development", limit=10)
    for result in results:
        print(f"[{result.score:.1f}] {result.naics_code.code}: {result.naics_code.title}")
        print(f"  Match type: {result.match_type}")
        print(f"  Matched: {', '.join(result.matched_terms)}")
        print()
    
    # 2. Autocomplete
    suggestions = search.autocomplete("comp", limit=5)
    for suggestion in suggestions:
        print(f"{suggestion['code']}: {suggestion['title']}")
        if suggestion['aliases']:
            print(f"  Also known as: {', '.join(suggestion['aliases'])}")
    
    # 3. Keyword-based search
    tech_codes = search.find_by_keywords(
        keywords=["software", "programming", "development"],
        match_all=False,  # Match ANY keyword
        limit=15
    )
    
    # 4. Find by alias
    codes = search.find_by_alias("IT services", exact=False)
    
    # 5. Get related codes
    related = search.get_related_codes("541511", max_results=8)
    print(f"\nCodes related to 541511:")
    for naics in related:
        print(f"  {naics.code}: {naics.title}")


if __name__ == "__main__":
    example_usage()


