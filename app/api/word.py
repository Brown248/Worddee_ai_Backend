from fastapi import APIRouter, HTTPException
from app.models.schemas import WordResponse
from app.services.word_service import WordService

router = APIRouter()

@router.get("/word", response_model=WordResponse)
async def get_word_of_the_day():
    """ดึงคำศัพท์แบบสุ่มสำหรับวันนี้"""
    try:
        word = WordService.get_random_word()
        return WordResponse(**word)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))