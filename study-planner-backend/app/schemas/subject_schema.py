from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class PastAssignmentItem(BaseModel):
    name: str
    result: str

class QuestionnaireItem(BaseModel):
    name: str
    result: str

class SubjectBase(BaseModel):
    name: str
    difficulty: str
    past_assignments: List[PastAssignmentItem] = []
    questionnaire_results: List[QuestionnaireItem] = []

class SubjectCreate(SubjectBase):
    pass

class SubjectResponse(SubjectBase):
    id: int
    recommended_hours: float
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

