from pydantic import BaseModel
from typing import Optional

# ส่ง word ไปหน้าเว็บ
class WordOut(BaseModel):
    id: int
    word: str
    pos: Optional[str]
    meaning: Optional[str]

# รับข้อมูลจาก frontend
class ValidateIn(BaseModel):
    word_id: int
    sentence: str

# ส่ง feedback กลับไป frontend
class ValidateOut(BaseModel):
    score: float
    percent: float
    level: str
    suggestion: str
    corrected_sentence: str
