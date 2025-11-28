from pydantic import BaseModel
from typing import Optional

class WordResponse(BaseModel):
    word: str
    part_of_speech: str
    meaning: str
    example: str

class ValidateRequest(BaseModel):
    word: str
    sentence: str

class FeedbackResponse(BaseModel):
    score: float
    level: str
    suggestion: str
    corrected_sentence: str

class AttemptData(BaseModel):
    date: str
    score: float

class SummaryResponse(BaseModel):
    attempts: list[AttemptData]
    totalAttempts: int
    averageScore: float
    currentLevel: str