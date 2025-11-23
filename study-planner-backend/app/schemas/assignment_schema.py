from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AssignmentBase(BaseModel):
    name: str
    subject_name: str
    due_date: str
    estimated_hours: float
    difficulty: str = "medium"
    priority: str = "medium"
    status: str = "pending"

class AssignmentCreate(AssignmentBase):
    pass

class AssignmentResponse(AssignmentBase):
    id: int
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


