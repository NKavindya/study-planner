from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models import assignment as assignment_model, exam as exam_model, plan as plan_model
from app.schemas import plan_schema
from app.services.scheduler import generate_study_plan
from typing import List

router = APIRouter(prefix="/api/planner", tags=["planner"])

@router.post("/generate", response_model=dict)
def generate_plan(request: plan_schema.GeneratePlanRequest, db: Session = Depends(get_db)):
    """Generate a study plan"""
    # Get all assignments and exams
    assignments = assignment_model.get_all_assignments(db)
    exams = exam_model.get_all_exams(db)
    
    if not assignments and not exams:
        raise HTTPException(status_code=400, detail="No assignments or exams found. Please add assignments or exams first.")
    
    # Generate plan
    plan_result = generate_study_plan(
        assignments,
        exams,
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
                "item_id": slot["item_id"],
                "item_type": slot["category"],
                "item_name": slot["item_name"],
                "day": day_plan["day"],
                "time_slot": slot["time"],
                "hours": slot["hours"],
                "category": slot["category"]
            }
            plan_model.create_study_plan(db, plan_data)
    
    return {
        "plan": plan_result["plan"],
        "rules_triggered": plan_result["rules_triggered"],
        "total_hours_needed": plan_result["total_hours_needed"],
        "total_available_hours": plan_result["total_available_hours"],
        "message": "Study plan generated successfully"
    }

@router.get("/weekly", response_model=List[dict])
def get_weekly_plan(db: Session = Depends(get_db)):
    """Get weekly study plan"""
    try:
        plans = plan_model.get_study_plans(db)
        
        if not plans:
            return []
        
        # Group by day
        weekly_plan = {}
        for plan in plans:
            day = plan.day
            if day not in weekly_plan:
                weekly_plan[day] = []
            
            # Get item name (use stored name or fetch from database)
            item_name = plan.item_name if plan.item_name else f"Item {plan.item_id}"
            
            # Get subject name from assignment or exam
            subject_name = "N/A"
            try:
                if plan.item_type == "assignment":
                    assignment = assignment_model.get_assignment(db, plan.item_id)
                    if assignment:
                        subject_name = assignment.subject_name
                elif plan.item_type == "exam":
                    exam = exam_model.get_exam(db, plan.item_id)
                    if exam:
                        subject_name = exam.subject_name
            except Exception as e:
                print(f"Error fetching subject name: {e}")
            
            weekly_plan[day].append({
                "time": plan.time_slot,
                "item_name": item_name,
                "category": plan.category if plan.category else plan.item_type,
                "subject_name": subject_name,
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
    except Exception as e:
        print(f"Error in get_weekly_plan: {e}")
        return []

@router.delete("/clear")
def clear_plan(db: Session = Depends(get_db)):
    """Clear all study plans"""
    plan_model.clear_all_plans(db)
    return {"message": "All plans cleared"}

