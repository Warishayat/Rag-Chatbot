from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from Services.rag import get_answer

router = APIRouter(prefix="/api", tags=["Chat"])

class ChatRequest(BaseModel):
    query: str
    filename: str
    session_id: Optional[str] = "default"

@router.post("/chat")
def chat_with_document(request: ChatRequest):
    try:
        response_data = get_answer(request.query, request.filename, request.session_id)
        return response_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
