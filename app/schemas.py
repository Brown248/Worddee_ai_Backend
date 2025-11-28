# backend/app/schemas.py
from pydantic import BaseModel
from typing import Optional

class WordOut(BaseModel):
    id: int
    word: str
    pos: Optional[str]
    meaning: Optional[str]

class ValidateIn(BaseModel):
    word_id: int
    sentence: str

class ValidateOut(BaseModel):
    score: float
    percent: float
    level: str
    suggestion: str
    corrected_sentence: str
