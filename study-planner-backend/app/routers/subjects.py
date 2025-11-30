from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.database import get_db
from app.models import subject as subject_model
from app.schemas import subject_schema
import json

router = APIRouter(prefix="/api/subjects", tags=["subjects"])

@router.post("/", response_model=subject_schema.SubjectResponse)
def create_subject(subject: subject_schema.SubjectCreate, db: Session = Depends(get_db)):
    """Create a new subject"""
    try:
        # Calculate recommended hours based on difficulty
        difficulty_map = {"easy": 2.0, "medium": 4.0, "hard": 6.0}
        recommended_hours = difficulty_map.get(subject.difficulty.lower(), 4.0)
        
        # Convert lists to JSON strings for storage
        past_assignments_json = json.dumps([item.dict() for item in subject.past_assignments]) if subject.past_assignments else "[]"
        questionnaire_results_json = json.dumps([item.dict() for item in subject.questionnaire_results]) if subject.questionnaire_results else "[]"
        
        # Create subject
        subject_data = {
            "name": subject.name,
            "difficulty": subject.difficulty,
            "recommended_hours": recommended_hours,
            "past_assignments": past_assignments_json,
            "questionnaire_results": questionnaire_results_json
        }
        
        created_subject = subject_model.create_subject(db, subject_data)
        
        # Convert back to list format for response
        created_subject.past_assignments = json.loads(created_subject.past_assignments) if created_subject.past_assignments else []
        created_subject.questionnaire_results = json.loads(created_subject.questionnaire_results) if created_subject.questionnaire_results else []
        
        return created_subject
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating subject: {str(e)}")

@router.get("/", response_model=List[subject_schema.SubjectResponse])
def get_subjects(db: Session = Depends(get_db)):
    """Get all subjects"""
    import json
    subjects = subject_model.get_all_subjects(db)
    # Convert JSON strings back to lists
    for subject in subjects:
        try:
            subject.past_assignments = json.loads(subject.past_assignments) if subject.past_assignments else []
        except:
            subject.past_assignments = []
        try:
            subject.questionnaire_results = json.loads(subject.questionnaire_results) if subject.questionnaire_results else []
        except:
            subject.questionnaire_results = []
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
    try:
        # Recalculate recommended hours based on difficulty
        difficulty_map = {"easy": 2.0, "medium": 4.0, "hard": 6.0}
        recommended_hours = difficulty_map.get(subject.difficulty.lower(), 4.0)
        
        # Convert lists to JSON strings for storage
        past_assignments_json = json.dumps([item.dict() for item in subject.past_assignments]) if subject.past_assignments else "[]"
        questionnaire_results_json = json.dumps([item.dict() for item in subject.questionnaire_results]) if subject.questionnaire_results else "[]"
        
        subject_data = {
            "name": subject.name,
            "difficulty": subject.difficulty,
            "recommended_hours": recommended_hours,
            "past_assignments": past_assignments_json,
            "questionnaire_results": questionnaire_results_json
        }
        
        updated_subject = subject_model.update_subject(db, subject_id, subject_data)
        if not updated_subject:
            raise HTTPException(status_code=404, detail="Subject not found")
        
        # Convert back to list format for response
        updated_subject.past_assignments = json.loads(updated_subject.past_assignments) if updated_subject.past_assignments else []
        updated_subject.questionnaire_results = json.loads(updated_subject.questionnaire_results) if updated_subject.questionnaire_results else []
        
        return updated_subject
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating subject: {str(e)}")

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

