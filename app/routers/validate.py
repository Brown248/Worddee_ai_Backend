# backend/app/routers/validate.py
from fastapi import APIRouter
from app.schemas import ValidateIn, ValidateOut
from app.database import database
from app.models import attempts
from datetime import datetime

router = APIRouter(prefix="/api", tags=["Validate Sentence"])

@router.post("/validate-sentence", response_model=ValidateOut)
async def validate_sentence(payload: ValidateIn):
    create_attempt_query = attempts.insert().values(
        word_id=payload.word_id,
        original_sentence=payload.sentence,
        corrected_sentence=None,
        score=None,
        level=None,
        suggestion=None,
        created_at=datetime.utcnow())
    
    attempt_id = await database.execute(create_attempt_query)
    mock_score = 7.5
    mock_percent = mock_score * 10
    mock_level = "Intermediate"
    mock_suggestion = "Try improving the sentence structure."
    mock_corrected_sentence = "This is a corrected mock sentence."

    update_query = attempts.update().where(
        attempts.c.id == attempt_id).values(
        corrected_sentence=mock_corrected_sentence,
        score=mock_score,
        level=mock_level,
        suggestion=mock_suggestion)
    
    await database.execute(update_query)

    return {"score": mock_score,
            "percent": mock_percent,
            "level": mock_level,
            "suggestion": mock_suggestion,
            "corrected_sentence": mock_corrected_sentence}
