from fastapi import APIRouter, HTTPException
from app.models.schemas import ValidateRequest, FeedbackResponse
from app.services.ai_service import AIService

router = APIRouter()

@router.post("/validate-sentence", response_model=FeedbackResponse)
async def validate_sentence(request: ValidateRequest):
    """ตรวจสอบประโยคและให้ feedback จาก AI"""
    try:
        if not request.sentence.strip():
            raise HTTPException(status_code=400, detail="Sentence cannot be empty")
        
        feedback = await AIService.validate_sentence(
            request.word,
            request.sentence
        )
        
        return FeedbackResponse(**feedback)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))