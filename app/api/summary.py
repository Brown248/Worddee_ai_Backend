from fastapi import APIRouter
from app.models.schemas import SummaryResponse, AttemptData

router = APIRouter()

# Mock data storage (ในการใช้งานจริงควรใช้ database)
MOCK_SUMMARY = {
    "attempts": [
        {"date": "Mon", "score": 7.5},
        {"date": "Tue", "score": 8.0},
        {"date": "Wed", "score": 8.5},
        {"date": "Thu", "score": 9.0},
        {"date": "Fri", "score": 8.8},
        {"date": "Sat", "score": 8.2},
        {"date": "Sun", "score": 9.2}
    ],
    "totalAttempts": 25,
    "averageScore": 8.46,
    "currentLevel": "Intermediate"
}

@router.get("/summary", response_model=SummaryResponse)
async def get_summary():
    """ดึงข้อมูลสรุปการทำแบบฝึกหัด"""
    return SummaryResponse(**MOCK_SUMMARY)