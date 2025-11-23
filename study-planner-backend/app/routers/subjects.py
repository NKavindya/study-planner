from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.database import get_db
from app.models import subject as subject_model
from app.schemas import subject_schema
from app.services.ml_model import predict_hours
from app.utils.date_utils import get_days_until_exam
from app.utils.db_utils import subject_to_dict

router = APIRouter(prefix="/api/subjects", tags=["subjects"])

@router.post("/", response_model=subject_schema.SubjectResponse)
def create_subject(subject: subject_schema.SubjectCreate, db: Session = Depends(get_db)):
    """Create a new subject"""
    # Calculate recommended hours using ML model
    days_left = get_days_until_exam(subject.exam_date)
    difficulty_map = {"easy": 0, "medium": 1, "hard": 2}
    difficulty_level = difficulty_map.get(subject.difficulty.lower(), 1)
    
    recommended_hours = predict_hours(
        subject.past_score,
        subject.difficulty,
        subject.chapters,
        days_left
    )
    
    # Create subject with ML prediction
    subject_data = subject.dict()
    subject_data["recommended_hours"] = recommended_hours
    
    # Set initial priority
    if days_left <= 3:
        subject_data["priority"] = "urgent"
    elif days_left <= 7:
        subject_data["priority"] = "high"
    elif days_left > 30:
        subject_data["priority"] = "low"
    else:
        subject_data["priority"] = "medium"
    
    created_subject = subject_model.create_subject(db, subject_data)
    return created_subject

@router.get("/", response_model=List[subject_schema.SubjectResponse])
def get_subjects(db: Session = Depends(get_db)):
    """Get all subjects"""
    subjects = subject_model.get_all_subjects(db)
    return subjects

@router.get("/{subject_id}", response_model=subject_schema.SubjectResponse)
def get_subject(subject_id: int, db: Session = Depends(get_db)):
    """Get a specific subject"""
    subject = subject_model.get_subject(db, subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return subject

@router.put("/{subject_id}", response_model=subject_schema.SubjectResponse)
def update_subject(subject_id: int, subject: subject_schema.SubjectCreate, db: Session = Depends(get_db)):
    """Update a subject"""
    # Recalculate recommended hours
    days_left = get_days_until_exam(subject.exam_date)
    recommended_hours = predict_hours(
        subject.past_score,
        subject.difficulty,
        subject.chapters,
        days_left
    )
    
    subject_data = subject.dict()
    subject_data["recommended_hours"] = recommended_hours
    
    updated_subject = subject_model.update_subject(db, subject_id, subject_data)
    if not updated_subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return updated_subject

@router.delete("/{subject_id}")
def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    """Delete a subject"""
    subject = subject_model.delete_subject(db, subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return {"message": "Subject deleted successfully"}

@router.get("/reminders/active", response_model=List[subject_schema.ReminderResponse])
def get_active_reminders(db: Session = Depends(get_db)):
    """Get active reminders"""
    reminders = subject_model.get_active_reminders(db)
    return reminders

@router.post("/reminders/{reminder_id}/read")
def mark_reminder_read(reminder_id: int, db: Session = Depends(get_db)):
    """Mark a reminder as read"""
    reminder = subject_model.mark_reminder_read(db, reminder_id)
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    return {"message": "Reminder marked as read"}

