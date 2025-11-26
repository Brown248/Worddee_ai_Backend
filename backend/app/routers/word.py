from fastapi import APIRouter, HTTPException
from app.database import database
from app.schemas import WordOut

router = APIRouter(prefix="/api", tags=["Word"])

@router.get("/word", response_model=WordOut)
async def get_random_word():
    query = """
    SELECT id, word, pos, meaning
    FROM words
    ORDER BY RANDOM()
    LIMIT 1;
    """
    row = await database.fetch_one(query)

    if not row:
        raise HTTPException(status_code=404, detail="No words found")

    return row