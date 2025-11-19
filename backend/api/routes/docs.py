"""
Documentation API Routes

Provides endpoints for serving documentation files.
"""

import os
from pathlib import Path
from typing import Dict

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

router = APIRouter()

# Get the project root directory (2 levels up from this file)
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"


@router.get("/docs/list")
async def list_docs() -> Dict:
    """
    List all available documentation files.

    Returns:
        Dictionary with documentation structure
    """
    if not DOCS_DIR.exists():
        raise HTTPException(status_code=404, detail="Documentation directory not found")

    docs_structure = {
        "core": [],
        "dev": [],
        "api": [],
        "backend": [],
        "frontend": [],
        "deployment": [],
        "architecture": [],
    }

    for category in docs_structure.keys():
        category_path = DOCS_DIR / category
        if category_path.exists():
            for file_path in category_path.glob("*.md"):
                docs_structure[category].append({
                    "path": f"{category}/{file_path.stem}",
                    "title": file_path.stem.replace("_", " ").title(),
                    "filename": file_path.name,
                })

    # Add root README
    readme_path = DOCS_DIR / "README.md"
    if readme_path.exists():
        docs_structure["core"].insert(0, {
            "path": "README",
            "title": "Documentation Index",
            "filename": "README.md",
        })

    return docs_structure


@router.get("/docs/{doc_path:path}")
async def get_doc(doc_path: str) -> Response:
    """
    Get documentation file content.

    Args:
        doc_path: Path to the documentation file (without .md extension)
                 Examples: "README", "core/MANIFEST", "dev/CODEBASE_ANALYSIS"

    Returns:
        Markdown content as plain text

    Raises:
        HTTPException: If file not found or invalid path
    """
    # Security: prevent directory traversal attacks
    if ".." in doc_path or doc_path.startswith("/"):
        raise HTTPException(status_code=400, detail="Invalid documentation path")

    # Handle root README case
    if doc_path == "README":
        file_path = DOCS_DIR / "README.md"
    else:
        # Add .md extension and construct full path
        file_path = DOCS_DIR / f"{doc_path}.md"

    # Verify the file exists and is within docs directory
    try:
        file_path = file_path.resolve()
        if not file_path.is_relative_to(DOCS_DIR):
            raise HTTPException(status_code=400, detail="Invalid documentation path")

        if not file_path.exists():
            raise HTTPException(status_code=404, detail=f"Documentation not found: {doc_path}")

        # Read and return the markdown content
        content = file_path.read_text(encoding="utf-8")

        return Response(
            content=content,
            media_type="text/markdown; charset=utf-8",
            headers={
                "Cache-Control": "public, max-age=300",  # Cache for 5 minutes
            },
        )

    except ValueError:
        # is_relative_to can raise ValueError in some cases
        raise HTTPException(status_code=400, detail="Invalid documentation path")
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error reading documentation: {str(e)}",
        )
