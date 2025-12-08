from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List

from backend.services.neural_hive_service import NeuralHiveService
from backend.schemas.experience import ExperienceCreate

router = APIRouter()

class JournalRequest(BaseModel):
    user_id: str
    text: str

class JournalResponse(BaseModel):
    message: str
    generated_experiences: List[dict] # Returning dicts for frontend review

@router.post("/process", response_model=JournalResponse)
async def process_journal(
    request: JournalRequest,
    service: NeuralHiveService = Depends(lambda: NeuralHiveService())
):
    """
    Process a raw journal entry through the Neural Hive.
    Returns proposed Experience Objects for the user to review/confirm.
    """
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Journal text cannot be empty")

    try:
        results = service.process_journal_entry(request.user_id, request.text)
        return {
            "message": f"Successfully processed. Generated {len(results)} objects.",
            "generated_experiences": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))