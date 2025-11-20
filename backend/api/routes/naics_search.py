"""
Enhanced NAICS Search API Endpoints

FastAPI routes for advanced NAICS code search, autocomplete, and discovery.

Add these to your backend/api/routes/naics.py or create a new routes file.
"""

from typing import List, Optional
from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel, Field

from backend.services.enhanced_naics_search import EnhancedNAICSSearch, SearchResult
from backend.models.naics import NAICSCategory, NAICSLevel


# ============================================================================
# PYDANTIC SCHEMAS
# ============================================================================

class NAICSSearchRequest(BaseModel):
    """Request schema for NAICS search."""
    query: str = Field(..., min_length=1, max_length=200, description="Search query")
    category: Optional[str] = Field(None, description="Filter by category")
    level: Optional[int] = Field(None, description="Filter by level (2, 3, 4, or 6)")
    limit: int = Field(20, ge=1, le=100, description="Maximum results to return")
    min_score: float = Field(0.0, ge=0.0, le=100.0, description="Minimum relevance score")


class NAICSSearchResultResponse(BaseModel):
    """Response schema for a single search result."""
    code: str
    title: str
    description: str
    category: str
    level: int
    sector: Optional[str]
    subsector: Optional[str]
    industry_group: Optional[str]
    keywords: List[str]
    aliases: List[str]
    examples: Optional[str]
    score: float = Field(..., description="Relevance score (0-100)")
    match_type: str = Field(..., description="Type of match (code, title, keyword, etc.)")
    matched_terms: List[str] = Field(..., description="Terms that matched the query")


class NAICSSearchResponse(BaseModel):
    """Response schema for search results."""
    query: str
    total_results: int
    results: List[NAICSSearchResultResponse]
    took_ms: Optional[float] = Field(None, description="Query execution time in milliseconds")


class AutocompleteResponse(BaseModel):
    """Response schema for autocomplete suggestions."""
    code: str
    title: str
    category: str
    level: int
    match_type: str
    score: float
    aliases: List[str] = Field(default_factory=list)
    keywords: List[str] = Field(default_factory=list)


class RelatedCodesResponse(BaseModel):
    """Response schema for related codes."""
    source_code: str
    source_title: str
    related: List[dict]


# ============================================================================
# API ROUTER
# ============================================================================

router = APIRouter(prefix="/api/naics", tags=["NAICS Advanced Search"])


@router.post("/search", response_model=NAICSSearchResponse)
async def search_naics(request: NAICSSearchRequest):
    """
    Advanced NAICS code search with relevance ranking.
    
    Searches across:
    - NAICS codes
    - Titles
    - Keywords
    - Aliases
    - Descriptions
    
    Results are ranked by relevance with scores from 0-100.
    
    Example:
        POST /api/naics/search
        {
            "query": "software development",
            "category": "technology",
            "limit": 10,
            "min_score": 40.0
        }
    """
    import time
    start_time = time.time()
    
    try:
        search = EnhancedNAICSSearch()
        
        # Parse category
        category = None
        if request.category:
            try:
                category = NAICSCategory(request.category.lower())
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid category: {request.category}"
                )
        
        # Parse level
        level = None
        if request.level:
            try:
                if request.level == 2:
                    level = NAICSLevel.SECTOR
                elif request.level == 3:
                    level = NAICSLevel.SUBSECTOR
                elif request.level == 4:
                    level = NAICSLevel.INDUSTRY_GROUP
                elif request.level == 6:
                    level = NAICSLevel.NATIONAL_INDUSTRY
                else:
                    raise ValueError("Invalid level")
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid level: {request.level}. Must be 2, 3, 4, or 6"
                )
        
        # Perform search
        results = search.search(
            query=request.query,
            category=category,
            level=level,
            limit=request.limit,
            min_score=request.min_score
        )
        
        # Convert to response format
        response_results = []
        for result in results:
            response_results.append(NAICSSearchResultResponse(
                code=result.naics_code.code,
                title=result.naics_code.title,
                description=result.naics_code.description,
                category=result.naics_code.category.value,
                level=result.naics_code.level.value,
                sector=result.naics_code.sector,
                subsector=result.naics_code.subsector,
                industry_group=result.naics_code.industry_group,
                keywords=result.naics_code.keywords,
                aliases=result.naics_code.aliases,
                examples=result.naics_code.examples,
                score=result.score,
                match_type=result.match_type,
                matched_terms=result.matched_terms
            ))
        
        elapsed_ms = (time.time() - start_time) * 1000
        
        return NAICSSearchResponse(
            query=request.query,
            total_results=len(response_results),
            results=response_results,
            took_ms=round(elapsed_ms, 2)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/autocomplete", response_model=List[AutocompleteResponse])
async def autocomplete_naics(
    q: str = Query(..., min_length=1, max_length=100, description="Partial search query"),
    category: Optional[str] = Query(None, description="Filter by category"),
    limit: int = Query(10, ge=1, le=50, description="Maximum suggestions")
):
    """
    Get autocomplete suggestions for NAICS codes.
    
    Provides intelligent suggestions based on partial input, prioritizing
    exact matches in codes and titles, then keywords and aliases.
    
    Example:
        GET /api/naics/autocomplete?q=soft&limit=5
    """
    try:
        search = EnhancedNAICSSearch()
        
        # Parse category
        category_enum = None
        if category:
            try:
                category_enum = NAICSCategory(category.lower())
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid category: {category}"
                )
        
        # Get suggestions
        suggestions = search.autocomplete(
            partial=q,
            limit=limit,
            category=category_enum
        )
        
        # Convert to response format
        response = [
            AutocompleteResponse(**suggestion)
            for suggestion in suggestions
        ]
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/keywords/{keywords}", response_model=List[dict])
async def search_by_keywords(
    keywords: str = Query(..., description="Comma-separated keywords"),
    match_all: bool = Query(False, description="If true, match ALL keywords. If false, match ANY."),
    limit: int = Query(20, ge=1, le=100)
):
    """
    Search NAICS codes by keywords.
    
    Example:
        GET /api/naics/keywords/software,programming,development?match_all=false&limit=15
    """
    try:
        search = EnhancedNAICSSearch()
        
        # Parse keywords
        keyword_list = [k.strip() for k in keywords.split(",") if k.strip()]
        
        if not keyword_list:
            raise HTTPException(status_code=400, detail="No valid keywords provided")
        
        # Search
        results = search.find_by_keywords(
            keywords=keyword_list,
            match_all=match_all,
            limit=limit
        )
        
        # Convert to dict
        return [naics.to_dict() for naics in results]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/alias/{alias}", response_model=List[dict])
async def search_by_alias(
    alias: str,
    exact: bool = Query(False, description="If true, exact match. If false, partial match.")
):
    """
    Find NAICS codes by alias (alternative name).
    
    Example:
        GET /api/naics/alias/IT%20services?exact=false
    """
    try:
        search = EnhancedNAICSSearch()
        
        results = search.find_by_alias(alias=alias, exact=exact)
        
        return [naics.to_dict() for naics in results]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{code}/related", response_model=RelatedCodesResponse)
async def get_related_codes(
    code: str,
    max_results: int = Query(10, ge=1, le=50, description="Maximum related codes to return")
):
    """
    Get codes related to a given NAICS code.
    
    Uses:
    - Explicit cross-references
    - Same sector/subsector
    - Similar keywords
    
    Example:
        GET /api/naics/541511/related?max_results=8
    """
    try:
        search = EnhancedNAICSSearch()
        
        # Get the source code first
        with get_db_context() as db:
            from backend.models.db_models import NAICSCodeDB
            source = db.query(NAICSCodeDB).filter_by(code=code).first()
            
            if not source:
                raise HTTPException(status_code=404, detail=f"NAICS code '{code}' not found")
        
        # Get related codes
        related = search.get_related_codes(code=code, max_results=max_results)
        
        return RelatedCodesResponse(
            source_code=code,
            source_title=source.title,
            related=[naics.to_dict() for naics in related]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/categories", response_model=List[str])
async def get_categories():
    """
    Get all available NAICS categories.
    
    Example:
        GET /api/naics/categories
    """
    return [category.value for category in NAICSCategory]


@router.get("/stats/keywords", response_model=dict)
async def get_keyword_stats():
    """
    Get statistics about keywords in the NAICS database.
    
    Returns:
    - Total codes with keywords
    - Most common keywords
    - Average keywords per code
    """
    try:
        from backend.database import get_db_context
        from backend.models.db_models import NAICSCodeDB
        from collections import Counter
        
        with get_db_context() as db:
            codes = db.query(NAICSCodeDB).filter(NAICSCodeDB.is_active == True).all()
            
            total_codes = len(codes)
            codes_with_keywords = sum(1 for c in codes if c.keywords)
            
            # Count all keywords
            all_keywords = []
            for code in codes:
                if code.keywords:
                    all_keywords.extend(code.keywords)
            
            keyword_counts = Counter(all_keywords)
            
            return {
                "total_codes": total_codes,
                "codes_with_keywords": codes_with_keywords,
                "total_keywords": len(all_keywords),
                "unique_keywords": len(keyword_counts),
                "average_keywords_per_code": round(len(all_keywords) / codes_with_keywords, 2) if codes_with_keywords > 0 else 0,
                "top_keywords": [
                    {"keyword": k, "count": v}
                    for k, v in keyword_counts.most_common(20)
                ]
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# INTEGRATION HELPER
# ============================================================================

def include_naics_search_routes(app):
    """
    Include NAICS search routes in your FastAPI app.
    
    Usage:
        from backend.api.routes.naics_search import include_naics_search_routes
        
        app = FastAPI()
        include_naics_search_routes(app)
    """
    app.include_router(router)