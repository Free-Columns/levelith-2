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


def _scan_docs_recursive(base_path: Path, relative_path: str = "", max_depth: int = 4, current_depth: int = 0):
    """
    Recursively scan documentation directory up to max_depth levels.

    Args:
        base_path: Absolute path to scan
        relative_path: Relative path from docs root (for building doc paths)
        max_depth: Maximum depth to scan (default 4)
        current_depth: Current recursion depth

    Returns:
        List of dicts or nested structure with files and subdirectories
    """
    if current_depth >= max_depth or not base_path.exists():
        return []

    structure = []

    # Get all items in this directory
    items = sorted(base_path.iterdir(), key=lambda x: (not x.is_dir(), x.name))

    for item in items:
        if item.name.startswith('.'):
            continue

        item_relative_path = f"{relative_path}/{item.name}" if relative_path else item.name

        if item.is_dir():
            # Recursively scan subdirectory
            children = _scan_docs_recursive(item, item_relative_path, max_depth, current_depth + 1)
            if children:  # Only add if there are children
                structure.append({
                    "type": "folder",
                    "name": item.name,
                    "path": item_relative_path,
                    "children": children,
                })
        elif item.suffix == ".md":
            # Extract title from first line of markdown file
            try:
                with open(item, 'r', encoding='utf-8') as f:
                    first_line = f.readline().strip()
                    title = first_line.lstrip('#').strip() if first_line.startswith('#') else item.stem.replace("_", " ").replace("-", " ").title()
            except:
                title = item.stem.replace("_", " ").replace("-", " ").title()

            doc_path = f"{relative_path}/{item.stem}" if relative_path else item.stem

            structure.append({
                "type": "file",
                "name": item.stem,
                "title": title,
                "path": doc_path,
                "filename": item.name,
            })

    return structure


@router.get("/docs/list")
async def list_docs() -> Dict:
    """
    List all available documentation files in a hierarchical structure up to 4 levels deep.

    Returns:
        Dictionary with hierarchical documentation structure:
        {
            "structure": [
                {
                    "type": "folder",
                    "name": "agent",
                    "path": "agent",
                    "children": [
                        {
                            "type": "file",
                            "name": "MANIFEST",
                            "title": "Levelith Project Manifest",
                            "path": "agent/MANIFEST",
                            "filename": "MANIFEST.md"
                        },
                        ...
                    ]
                },
                ...
            ]
        }
    """
    if not DOCS_DIR.exists():
        raise HTTPException(status_code=404, detail="Documentation directory not found")

    structure = _scan_docs_recursive(DOCS_DIR, "", max_depth=4, current_depth=0)

    return {"structure": structure}


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
