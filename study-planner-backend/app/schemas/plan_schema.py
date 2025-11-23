from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class StudyPlanBase(BaseModel):
    subject_id: int
    day: str
    time_slot: str
    hours: float

class StudyPlanCreate(StudyPlanBase):
    pass

class StudyPlanResponse(StudyPlanBase):
    id: int
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class GeneratePlanRequest(BaseModel):
    available_hours_per_day: float
    start_date: str
    end_date: str

class WeeklyPlanResponse(BaseModel):
    day: str
    time_slots: List[dict]

