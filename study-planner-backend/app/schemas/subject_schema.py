from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SubjectBase(BaseModel):
    name: str
    difficulty: str
    exam_date: str
    past_score: float = 0.0
    chapters: int = 0
    has_assignment: bool = False
    has_exam: bool = True
    last_week_hours: float = 0.0

class SubjectCreate(SubjectBase):
    pass

class SubjectResponse(SubjectBase):
    id: int
    recommended_hours: float
    priority: str
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class ReminderResponse(BaseModel):
    id: int
    subject_id: int
    message: str
    reminder_date: str
    is_read: bool
    
    class Config:
        from_attributes = True

