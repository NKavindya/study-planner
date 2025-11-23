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
    try:
        # Validate input
        if request.available_hours_per_day <= 0:
            raise HTTPException(status_code=400, detail="Available hours per day must be greater than 0")
        
        # Get all assignments and exams
        assignments = assignment_model.get_all_assignments(db)
        exams = exam_model.get_all_exams(db)
        
        if not assignments and not exams:
            raise HTTPException(status_code=400, detail="No assignments or exams found. Please add assignments or exams first.")
        
        # Auto-calculate start_date if not provided
        from datetime import datetime, timedelta
        start_date = request.start_date
        if not start_date:
            start_date = datetime.now().strftime("%Y-%m-%d")
        
        # Auto-calculate end_date from latest assignment due_date or exam exam_date
        end_date = request.end_date
        if not end_date:
            latest_date = None
            for assignment in assignments:
                if assignment.due_date:
                    try:
                        due_date = datetime.strptime(assignment.due_date, "%Y-%m-%d")
                        if latest_date is None or due_date > latest_date:
                            latest_date = due_date
                    except:
                        pass
            
            for exam in exams:
                if exam.exam_date:
                    try:
                        exam_date = datetime.strptime(exam.exam_date, "%Y-%m-%d")
                        if latest_date is None or exam_date > latest_date:
                            latest_date = exam_date
                    except:
                        pass
            
            if latest_date:
                # Add 1 day buffer after the latest deadline
                end_date = (latest_date + timedelta(days=1)).strftime("%Y-%m-%d")
            else:
                # Default to 7 days from start if no deadlines found
                start_obj = datetime.strptime(start_date, "%Y-%m-%d")
                end_date = (start_obj + timedelta(days=7)).strftime("%Y-%m-%d")
        
        if start_date >= end_date:
            raise HTTPException(status_code=400, detail="End date must be after start date")
        
        # Generate plan
        plan_result = generate_study_plan(
            assignments,
            exams,
            request.available_hours_per_day,
            start_date,
            end_date
        )
        
        # Clear existing plans
        plan_model.clear_all_plans(db)
        
        # Save new plans to database
        plans_saved = 0
        print(f"DEBUG: Generated plan has {len(plan_result['plan'])} days")
        
        # Use a transaction to ensure all plans are saved
        try:
            for day_idx, day_plan in enumerate(plan_result["plan"]):
                day_name = day_plan.get("day")
                date_str = day_plan.get("date", "")
                time_slots = day_plan.get("time_slots", [])
                
                # If day_name is missing, try to get it from date
                if not day_name or day_name == "Unknown":
                    if date_str:
                        from app.utils.date_utils import get_day_name
                        day_name = get_day_name(date_str)
                        if day_name == "Unknown":
                            # Fallback: calculate from date
                            try:
                                from datetime import datetime
                                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                                day_name = date_obj.strftime("%A")
                            except:
                                print(f"ERROR: Cannot determine day for date {date_str}")
                                continue
                    else:
                        print(f"ERROR: No day or date for day_plan {day_idx}")
                        continue
                
                print(f"DEBUG: Day {day_idx} ({day_name}) has {len(time_slots)} time slots")
                
                if not time_slots:
                    print(f"DEBUG: Skipping day {day_name} - no time slots")
                    continue  # Skip days with no time slots
                
                for slot_idx, slot in enumerate(time_slots):
                    try:
                        if not slot.get("item_id"):
                            print(f"DEBUG: Skipping slot {slot_idx} - no item_id: {slot}")
                            continue  # Skip invalid slots
                        
                        plan_data = {
                            "item_id": slot["item_id"],
                            "item_type": slot["category"],
                            "item_name": slot.get("item_name", ""),
                            "day": day_name,  # Ensure day is set
                            "date": date_str,  # Store date for calendar views
                            "time_slot": slot.get("time", ""),
                            "hours": slot.get("hours", 0),
                            "category": slot["category"]
                        }
                        print(f"DEBUG: Saving plan slot: day={day_name}, item={plan_data['item_name']}, time={plan_data['time_slot']}")
                        created_plan = plan_model.create_study_plan(db, plan_data)
                        if created_plan:
                            print(f"DEBUG: Plan saved with id={created_plan.id}, day={created_plan.day}")
                            plans_saved += 1
                        else:
                            print(f"ERROR: Plan creation returned None")
                    except Exception as e:
                        print(f"Error saving plan slot: {e}")
                        import traceback
                        traceback.print_exc()
                        continue
            
            # Verify plans were saved
            saved_plans = plan_model.get_study_plans(db)
            print(f"DEBUG: Verification - {len(saved_plans)} plans now in database")
            
        except Exception as e:
            db.rollback()
            print(f"Error saving plans: {e}")
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"Error saving study plan: {str(e)}")
        
        print(f"DEBUG: Saved {plans_saved} plan slots to database")
        
        return {
            "plan": plan_result["plan"],
            "rules_triggered": plan_result["rules_triggered"],
            "total_hours_needed": plan_result["total_hours_needed"],
            "total_available_hours": plan_result["total_available_hours"],
            "message": "Study plan generated successfully"
        }
    except HTTPException:
        # Re-raise HTTP exceptions (they already have proper status codes)
        raise
    except Exception as e:
        # Log the error for debugging
        print(f"Error generating study plan: {e}")
        import traceback
        traceback.print_exc()
        # Return a proper HTTP exception with CORS headers
        raise HTTPException(
            status_code=500,
            detail=f"Error generating study plan: {str(e)}"
        )

@router.get("/weekly", response_model=List[dict])
def get_weekly_plan(db: Session = Depends(get_db)):
    """Get weekly study plan"""
    try:
        plans = plan_model.get_study_plans(db)
        print(f"DEBUG: Found {len(plans)} plans in database")
        
        if not plans:
            print("DEBUG: No plans found in database")
            return []
        
        # Debug: Print first few plans
        for i, p in enumerate(plans[:3]):
            print(f"DEBUG: Plan {i}: day={p.day}, item_id={p.item_id}, item_type={p.item_type}, item_name={p.item_name}, time_slot={p.time_slot}")
        
        # Group by date (preferred) or day (fallback)
        date_groups = {}  # Key: date string (YYYY-MM-DD) or day name
        plans_with_day = 0
        plans_without_day = 0
        
        for plan in plans:
            day = plan.day
            date = getattr(plan, 'date', None) if hasattr(plan, 'date') else None
            
            if not day or day.strip() == "":
                plans_without_day += 1
                print(f"DEBUG: Skipping plan with no day: id={plan.id}, item_id={plan.item_id}, item_type={plan.item_type}")
                continue
            plans_with_day += 1
            
            # Use date as key if available, otherwise use day
            key = date if date else day
            if key not in date_groups:
                date_groups[key] = {
                    "day": day,
                    "date": date,
                    "time_slots": []
                }
            
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
            
            slot_data = {
                "time": plan.time_slot,
                "item_name": item_name,
                "category": plan.category if plan.category else plan.item_type,
                "subject_name": subject_name,
                "hours": plan.hours,
                "date": date  # Include date for calendar
            }
            date_groups[key]["time_slots"].append(slot_data)
            print(f"DEBUG: Added slot to {key}: {slot_data}")
        
        # Convert to list format, sorted by date if available
        result = []
        if any(dg.get("date") for dg in date_groups.values()):
            # Sort by date
            sorted_items = sorted(
                date_groups.items(),
                key=lambda x: x[1]["date"] if x[1]["date"] else "9999-99-99"
            )
            for key, group in sorted_items:
                result.append({
                    "day": group["day"],
                    "date": group["date"],
                    "time_slots": group["time_slots"]
                })
        else:
            # Fallback to day-based ordering
            days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            for day in days_order:
                if day in date_groups:
                    result.append({
                        "day": day,
                        "date": date_groups[day]["date"],
                        "time_slots": date_groups[day]["time_slots"]
                    })
        
        print(f"DEBUG: Plans with day: {plans_with_day}, Plans without day: {plans_without_day}")
        print(f"DEBUG: Returning {len(result)} days with plans, total slots: {sum(len(r['time_slots']) for r in result)}")
        
        if plans_with_day == 0 and plans_without_day > 0:
            print(f"WARNING: All {plans_without_day} plans have no day field!")
        
        return result
    except Exception as e:
        print(f"Error in get_weekly_plan: {e}")
        import traceback
        traceback.print_exc()
        return []

@router.get("/debug")
def debug_plans(db: Session = Depends(get_db)):
    """Debug endpoint to see what's in the database"""
    plans = plan_model.get_study_plans(db)
    plans_data = []
    for p in plans[:20]:  # First 20 plans
        plans_data.append({
            "id": p.id,
            "day": p.day if p.day else "NULL",
            "item_id": p.item_id,
            "item_type": p.item_type if p.item_type else "NULL",
            "item_name": p.item_name if p.item_name else "NULL",
            "time_slot": p.time_slot if p.time_slot else "NULL",
            "hours": p.hours,
            "category": p.category if p.category else "NULL"
        })
    return {
        "total_plans": len(plans),
        "plans_with_day": len([p for p in plans if p.day]),
        "plans_without_day": len([p for p in plans if not p.day]),
        "plans": plans_data
    }

@router.delete("/clear")
def clear_plan(db: Session = Depends(get_db)):
    """Clear all study plans"""
    plan_model.clear_all_plans(db)
    return {"message": "All plans cleared"}

