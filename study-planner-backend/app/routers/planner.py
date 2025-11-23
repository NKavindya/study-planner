from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models import subject as subject_model, plan as plan_model
from app.schemas import plan_schema
from app.services.scheduler import generate_study_plan
from app.utils.db_utils import subject_to_dict
from typing import List

router = APIRouter(prefix="/api/planner", tags=["planner"])

@router.post("/generate", response_model=dict)
def generate_plan(request: plan_schema.GeneratePlanRequest, db: Session = Depends(get_db)):
    """Generate a study plan"""
    # Get all subjects
    subjects = subject_model.get_all_subjects(db)
    if not subjects:
        raise HTTPException(status_code=400, detail="No subjects found. Please add subjects first.")
    
    # Convert to dict format
    subjects_list = [subject_to_dict(subj) for subj in subjects]
    
    # Generate plan
    plan_result = generate_study_plan(
        subjects_list,
        request.available_hours_per_day,
        request.start_date,
        request.end_date
    )
    
    # Clear existing plans
    plan_model.clear_all_plans(db)
    
    # Save new plans to database
    for day_plan in plan_result["plan"]:
        for slot in day_plan["time_slots"]:
            plan_data = {
                "subject_id": slot["subject_id"],
                "day": day_plan["day"],
                "time_slot": slot["time"],
                "hours": slot["hours"]
            }
            plan_model.create_study_plan(db, plan_data)
    
    return {
        "plan": plan_result["plan"],
        "rules_triggered": plan_result["rules_triggered"],
        "clashes": plan_result["clashes"],
        "total_hours_needed": plan_result["total_hours_needed"],
        "total_available_hours": plan_result["total_available_hours"],
        "message": "Study plan generated successfully"
    }

@router.get("/weekly", response_model=List[dict])
def get_weekly_plan(db: Session = Depends(get_db)):
    """Get weekly study plan"""
    plans = plan_model.get_study_plans(db)
    
    # Group by day
    weekly_plan = {}
    for plan in plans:
        day = plan.day
        if day not in weekly_plan:
            weekly_plan[day] = []
        
        # Get subject name
        subject = subject_model.get_subject(db, plan.subject_id)
        subject_name = subject.name if subject else f"Subject {plan.subject_id}"
        
        weekly_plan[day].append({
            "time": plan.time_slot,
            "subject": subject_name,
            "hours": plan.hours
        })
    
    # Convert to list format
    result = []
    days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    for day in days_order:
        if day in weekly_plan:
            result.append({
                "day": day,
                "time_slots": weekly_plan[day]
            })
    
    return result

@router.delete("/clear")
def clear_plan(db: Session = Depends(get_db)):
    """Clear all study plans"""
    plan_model.clear_all_plans(db)
    return {"message": "All plans cleared"}

