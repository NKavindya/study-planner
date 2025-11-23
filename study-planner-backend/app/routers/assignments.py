from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.database import get_db
from app.models import assignment as assignment_model
from app.schemas import assignment_schema
from app.services.clash_detector import detect_all_clashes
from app.utils.date_utils import get_days_until_exam

router = APIRouter(prefix="/api/assignments", tags=["assignments"])

@router.post("/", response_model=assignment_schema.AssignmentResponse)
def create_assignment(assignment: assignment_schema.AssignmentCreate, db: Session = Depends(get_db)):
    """Create a new assignment"""
    # Set priority based on due date
    days_left = get_days_until_exam(assignment.due_date)
    if days_left <= 3:
        priority = "urgent"
    elif days_left <= 7:
        priority = "high"
    elif days_left > 30:
        priority = "low"
    else:
        priority = "medium"
    
    assignment_data = assignment.dict()
    assignment_data["priority"] = priority
    
    created_assignment = assignment_model.create_assignment(db, assignment_data)
    
    # Detect clashes after creating
    detect_all_clashes(db)
    
    return created_assignment

@router.get("/", response_model=List[assignment_schema.AssignmentResponse])
def get_assignments(db: Session = Depends(get_db)):
    """Get all assignments"""
    assignments = assignment_model.get_all_assignments(db)
    return assignments

@router.get("/{assignment_id}", response_model=assignment_schema.AssignmentResponse)
def get_assignment(assignment_id: int, db: Session = Depends(get_db)):
    """Get a specific assignment"""
    assignment = assignment_model.get_assignment(db, assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return assignment

@router.put("/{assignment_id}", response_model=assignment_schema.AssignmentResponse)
def update_assignment(assignment_id: int, assignment: assignment_schema.AssignmentCreate, db: Session = Depends(get_db)):
    """Update an assignment"""
    # Recalculate priority
    days_left = get_days_until_exam(assignment.due_date)
    if days_left <= 3:
        priority = "urgent"
    elif days_left <= 7:
        priority = "high"
    elif days_left > 30:
        priority = "low"
    else:
        priority = "medium"
    
    assignment_data = assignment.dict()
    assignment_data["priority"] = priority
    
    updated_assignment = assignment_model.update_assignment(db, assignment_id, assignment_data)
    if not updated_assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    # Detect clashes after updating
    detect_all_clashes(db)
    
    return updated_assignment

@router.delete("/{assignment_id}")
def delete_assignment(assignment_id: int, db: Session = Depends(get_db)):
    """Delete an assignment"""
    assignment = assignment_model.delete_assignment(db, assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    # Detect clashes after deleting
    detect_all_clashes(db)
    
    return {"message": "Assignment deleted successfully"}


