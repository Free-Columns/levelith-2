"""
NAICS Code API Endpoints

Provides endpoints for NAICS code lookups, search, validation, and suggestions.
Supports the experience tracking system with industry classification.
"""

from typing import Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query, Path, status
from pydantic import BaseModel, Field

from backend.services.naics_service import NAICSService
from backend.repositories.naics_repository import NAICSRepository
from backend.models.naics import NAICSCode


# Initialize service (in production, this would use dependency injection)
naics_repo = NAICSRepository()
naics_service = NAICSService(naics_repo=naics_repo)

router = APIRouter(prefix="/naics", tags=["naics"])


# Pydantic schemas for API responses
class NAICSCodeResponse(BaseModel):
    """Response schema for NAICS code data."""
    code: str = Field(..., description="NAICS code (2, 3, 4, or 6 digits)")
    title: str = Field(..., description="Official NAICS title")
    description: str = Field("", description="Detailed description")
    level: str = Field(..., description="Hierarchical level (SECTOR, SUBSECTOR, etc.)")
    level_value: int = Field(..., description="Level as integer (2, 3, 4, or 6)")
    category: str = Field(..., description="Industry category")
    parent_code: Optional[str] = Field(None, description="Parent NAICS code")
    is_active: bool = Field(..., description="Whether code is active in NAICS 2022")
    year: int = Field(2022, description="NAICS version year")
    hierarchy: List[str] = Field(..., description="Full hierarchical path")

    class Config:
        json_schema_extra = {
            "example": {
                "code": "541511",
                "title": "Custom Computer Programming Services",
                "description": "Establishments primarily engaged in writing, modifying, testing, and supporting software to meet the needs of a particular customer.",
                "level": "NATIONAL_INDUSTRY",
                "level_value": 6,
                "category": "technology",
                "parent_code": "5415",
                "is_active": True,
                "year": 2022,
                "hierarchy": ["54", "541", "5415", "541511"]
            }
        }


class NAICSValidationResponse(BaseModel):
    """Response schema for NAICS code validation."""
    is_valid: bool = Field(..., description="Whether the code is valid")
    code: str = Field(..., description="Normalized code or fallback")
    message: str = Field(..., description="Validation message")
    naics: Optional[NAICSCodeResponse] = Field(None, description="NAICS metadata if valid")

    class Config:
        json_schema_extra = {
            "example": {
                "is_valid": True,
                "code": "541511",
                "message": "Valid NAICS code",
                "naics": {
                    "code": "541511",
                    "title": "Custom Computer Programming Services",
                    "description": "Establishments primarily engaged in writing, modifying, testing, and supporting software to meet the needs of a particular customer.",
                    "level": "NATIONAL_INDUSTRY",
                    "level_value": 6,
                    "category": "technology",
                    "parent_code": "5415",
                    "is_active": True,
                    "year": 2022,
                    "hierarchy": ["54", "541", "5415", "541511"]
                }
            }
        }


class NAICSSearchResponse(BaseModel):
    """Response schema for NAICS code search results."""
    query: str = Field(..., description="Search query")
    results: List[NAICSCodeResponse] = Field(..., description="Search results")
    count: int = Field(..., description="Number of results returned")


class NAICSSuggestionResponse(BaseModel):
    """Response schema for NAICS code autocomplete suggestions."""
    code: str
    title: str
    description: str
    category: str


class NAICSCategorySummary(BaseModel):
    """Response schema for category summary."""
    category: str
    count: int


def _naics_to_response(naics: NAICSCode) -> NAICSCodeResponse:
    """Convert NAICSCode domain model to API response schema."""
    naics_dict = naics.to_dict()
    return NAICSCodeResponse(**naics_dict)


@router.get(
    "/{code}",
    response_model=NAICSCodeResponse,
    status_code=status.HTTP_200_OK,
    summary="Get NAICS code details",
    description="Look up a NAICS code and return its complete metadata including title, description, hierarchy, and category."
)
async def get_naics_code(
    code: str = Path(..., description="NAICS code (2, 3, 4, or 6 digits)", example="541511")
) -> NAICSCodeResponse:
    """
    Get detailed information about a NAICS code.

    Args:
        code: NAICS code to look up

    Returns:
        NAICSCodeResponse with complete metadata

    Raises:
        HTTPException: 404 if code not found
    """
    naics = naics_service.lookup_code(code)

    if not naics:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"NAICS code '{code}' not found"
        )

    return _naics_to_response(naics)


@router.get(
    "/validate/{code}",
    response_model=NAICSValidationResponse,
    status_code=status.HTTP_200_OK,
    summary="Validate NAICS code",
    description="Validate a NAICS code against the official database and return validation result with metadata."
)
async def validate_naics_code(
    code: str = Path(..., description="NAICS code to validate", example="541511")
) -> NAICSValidationResponse:
    """
    Validate a NAICS code and return validation result.

    Args:
        code: NAICS code to validate

    Returns:
        NAICSValidationResponse with validation status and metadata
    """
    is_valid, naics = naics_service.validate_with_metadata(code)

    return NAICSValidationResponse(
        is_valid=is_valid,
        code=naics.code,
        message="Valid NAICS code" if is_valid else f"Invalid NAICS code. Using fallback: {naics.code}",
        naics=_naics_to_response(naics) if is_valid else None
    )


@router.get(
    "/search",
    response_model=NAICSSearchResponse,
    status_code=status.HTTP_200_OK,
    summary="Search NAICS codes",
    description="Search for NAICS codes by title or description keywords."
)
async def search_naics_codes(
    q: str = Query(..., description="Search query", example="computer programming"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of results")
) -> NAICSSearchResponse:
    """
    Search for NAICS codes by title or description.

    Args:
        q: Search query string
        limit: Maximum number of results (1-100)

    Returns:
        NAICSSearchResponse with matching codes
    """
    results = naics_service.search(q, limit=limit)

    return NAICSSearchResponse(
        query=q,
        results=[_naics_to_response(naics) for naics in results],
        count=len(results)
    )


@router.get(
    "/autocomplete",
    response_model=List[NAICSSuggestionResponse],
    status_code=status.HTTP_200_OK,
    summary="Autocomplete NAICS codes",
    description="Get autocomplete suggestions for NAICS codes based on partial input."
)
async def autocomplete_naics(
    q: str = Query(..., description="Partial search query", example="comp"),
    limit: int = Query(10, ge=1, le=50, description="Maximum number of suggestions")
) -> List[NAICSSuggestionResponse]:
    """
    Get autocomplete suggestions for NAICS codes.

    Args:
        q: Partial search query
        limit: Maximum number of suggestions (1-50)

    Returns:
        List of NAICS code suggestions
    """
    suggestions = naics_service.autocomplete(q, limit=limit)
    return [NAICSSuggestionResponse(**suggestion) for suggestion in suggestions]


@router.get(
    "/suggest/experience/{experience_type}",
    response_model=List[NAICSCodeResponse],
    status_code=status.HTTP_200_OK,
    summary="Suggest NAICS codes for experience type",
    description="Get relevant NAICS code suggestions based on experience type and optional title."
)
async def suggest_naics_for_experience(
    experience_type: str = Path(..., description="Experience type", example="full_time"),
    title: Optional[str] = Query(None, description="Experience title for better suggestions", example="Software Engineer"),
    limit: int = Query(10, ge=1, le=50, description="Maximum number of suggestions")
) -> List[NAICSCodeResponse]:
    """
    Suggest relevant NAICS codes for an experience.

    Args:
        experience_type: Type of experience
        title: Optional experience title for intelligent matching
        limit: Maximum number of suggestions

    Returns:
        List of suggested NAICS codes
    """
    suggestions = naics_service.suggest_for_experience(
        experience_type=experience_type,
        title=title,
        limit=limit
    )

    return [_naics_to_response(naics) for naics in suggestions]


@router.get(
    "/category/{category}",
    response_model=List[NAICSCodeResponse],
    status_code=status.HTTP_200_OK,
    summary="Get NAICS codes by category",
    description="Get all NAICS codes in a specific industry category."
)
async def get_naics_by_category(
    category: str = Path(..., description="Industry category", example="technology")
) -> List[NAICSCodeResponse]:
    """
    Get all NAICS codes in a specific category.

    Args:
        category: Industry category name

    Returns:
        List of NAICS codes in the category

    Raises:
        HTTPException: 404 if category not found
    """
    codes = naics_service.get_by_category(category)

    if not codes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category '{category}' not found or has no codes"
        )

    return [_naics_to_response(naics) for naics in codes]


@router.get(
    "/level/{level}",
    response_model=List[NAICSCodeResponse],
    status_code=status.HTTP_200_OK,
    summary="Get NAICS codes by level",
    description="Get all NAICS codes at a specific hierarchical level (2, 3, 4, or 6 digits)."
)
async def get_naics_by_level(
    level: int = Path(..., description="Hierarchical level (2, 3, 4, or 6)", example=6)
) -> List[NAICSCodeResponse]:
    """
    Get all NAICS codes at a specific hierarchical level.

    Args:
        level: Level value (2, 3, 4, or 6)

    Returns:
        List of NAICS codes at the level

    Raises:
        HTTPException: 400 if invalid level
    """
    if level not in [2, 3, 4, 6]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Level must be 2, 3, 4, or 6"
        )

    codes = naics_service.get_by_level(level)
    return [_naics_to_response(naics) for naics in codes]


@router.get(
    "/{code}/hierarchy",
    response_model=List[NAICSCodeResponse],
    status_code=status.HTTP_200_OK,
    summary="Get NAICS code hierarchy",
    description="Get the full hierarchical path for a NAICS code from sector to the specific code."
)
async def get_naics_hierarchy(
    code: str = Path(..., description="NAICS code", example="541511")
) -> List[NAICSCodeResponse]:
    """
    Get the full hierarchical path for a NAICS code.

    Args:
        code: NAICS code

    Returns:
        List of NAICS codes from sector to the specified code

    Raises:
        HTTPException: 404 if code not found
    """
    hierarchy = naics_service.get_hierarchy(code)

    if not hierarchy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"NAICS code '{code}' not found"
        )

    return [_naics_to_response(naics) for naics in hierarchy]


@router.get(
    "/{code}/children",
    response_model=List[NAICSCodeResponse],
    status_code=status.HTTP_200_OK,
    summary="Get child NAICS codes",
    description="Get all child codes of a parent NAICS code in the hierarchy."
)
async def get_naics_children(
    code: str = Path(..., description="Parent NAICS code", example="54")
) -> List[NAICSCodeResponse]:
    """
    Get all child codes of a parent NAICS code.

    Args:
        code: Parent NAICS code

    Returns:
        List of child NAICS codes
    """
    children = naics_service.get_children(code)
    return [_naics_to_response(naics) for naics in children]


@router.get(
    "/{code}/parent",
    response_model=NAICSCodeResponse,
    status_code=status.HTTP_200_OK,
    summary="Get parent NAICS code",
    description="Get the parent code of a NAICS code in the hierarchy."
)
async def get_naics_parent(
    code: str = Path(..., description="NAICS code", example="541511")
) -> NAICSCodeResponse:
    """
    Get the parent NAICS code.

    Args:
        code: NAICS code

    Returns:
        Parent NAICS code

    Raises:
        HTTPException: 404 if code or parent not found
    """
    parent = naics_service.get_parent(code)

    if not parent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Parent code not found for '{code}'"
        )

    return _naics_to_response(parent)


@router.get(
    "/categories/summary",
    response_model=List[NAICSCategorySummary],
    status_code=status.HTTP_200_OK,
    summary="Get category summary",
    description="Get a summary of NAICS code counts by category."
)
async def get_categories_summary() -> List[NAICSCategorySummary]:
    """
    Get a summary of NAICS codes by category.

    Returns:
        List of categories with code counts
    """
    summary = naics_service.get_categories_summary()
    return [
        NAICSCategorySummary(category=category, count=count)
        for category, count in summary.items()
    ]


@router.get(
    "/categories/list",
    response_model=List[str],
    status_code=status.HTTP_200_OK,
    summary="List all categories",
    description="Get a list of all available NAICS categories."
)
async def list_categories() -> List[str]:
    """
    Get all available NAICS categories.

    Returns:
        List of category names
    """
    return naics_service.get_all_categories()
