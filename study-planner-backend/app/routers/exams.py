from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.database import get_db
from app.models import exam as exam_model
from app.schemas import exam_schema
from app.services.ml_model import predict_hours
from app.services.clash_detector import detect_all_clashes
from app.utils.date_utils import get_days_until_exam

router = APIRouter(prefix="/api/exams", tags=["exams"])

@router.post("/", response_model=exam_schema.ExamResponse)
def create_exam(exam: exam_schema.ExamCreate, db: Session = Depends(get_db)):
    """Create a new exam"""
    # Calculate recommended hours using ML model
    days_left = get_days_until_exam(exam.exam_date)
    recommended_hours = predict_hours(
        exam.past_score,
        exam.difficulty,
        exam.chapters,
        days_left
    )
    
    # Set priority
    if days_left <= 3:
        priority = "urgent"
    elif days_left <= 7:
        priority = "high"
    elif days_left > 30:
        priority = "low"
    else:
        priority = "medium"
    
    exam_data = exam.dict()
    exam_data["recommended_hours"] = recommended_hours
    exam_data["priority"] = priority
    
    created_exam = exam_model.create_exam(db, exam_data)
    
    # Detect clashes after creating
    detect_all_clashes(db)
    
    return created_exam

@router.get("/", response_model=List[exam_schema.ExamResponse])
def get_exams(db: Session = Depends(get_db)):
    """Get all exams"""
    exams = exam_model.get_all_exams(db)
    return exams

@router.get("/{exam_id}", response_model=exam_schema.ExamResponse)
def get_exam(exam_id: int, db: Session = Depends(get_db)):
    """Get a specific exam"""
    exam = exam_model.get_exam(db, exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    return exam

@router.put("/{exam_id}", response_model=exam_schema.ExamResponse)
def update_exam(exam_id: int, exam: exam_schema.ExamCreate, db: Session = Depends(get_db)):
    """Update an exam"""
    # Recalculate recommended hours
    days_left = get_days_until_exam(exam.exam_date)
    recommended_hours = predict_hours(
        exam.past_score,
        exam.difficulty,
        exam.chapters,
        days_left
    )
    
    # Recalculate priority
    if days_left <= 3:
        priority = "urgent"
    elif days_left <= 7:
        priority = "high"
    elif days_left > 30:
        priority = "low"
    else:
        priority = "medium"
    
    exam_data = exam.dict()
    exam_data["recommended_hours"] = recommended_hours
    exam_data["priority"] = priority
    
    updated_exam = exam_model.update_exam(db, exam_id, exam_data)
    if not updated_exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    
    # Detect clashes after updating
    detect_all_clashes(db)
    
    return updated_exam

@router.delete("/{exam_id}")
def delete_exam(exam_id: int, db: Session = Depends(get_db)):
    """Delete an exam"""
    exam = exam_model.delete_exam(db, exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    
    # Detect clashes after deleting
    detect_all_clashes(db)
    
    return {"message": "Exam deleted successfully"}


