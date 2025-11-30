from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ExamBase(BaseModel):
    name: str
    subject_name: str
    exam_date: str
    difficulty: str = "medium"
    past_score: float = 0.0
    chapters: int = 0
    recommended_hours: float = 0.0
    priority: str = "medium"

class ExamCreate(ExamBase):
    pass

class ExamResponse(ExamBase):
    id: int
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


