from datetime import datetime, timedelta
from app.utils.date_utils import get_days_until_exam, get_date_range, is_weekend, get_day_name
from app.services.rules_engine import apply_rules, detect_clashes

def generate_study_plan(subjects, available_hours_per_day: float, start_date: str, end_date: str):
    """
    Generate a study plan based on subjects, availability, and date range
    """
    # Convert subjects to dict format if needed
    subjects_list = []
    for subj in subjects:
        if hasattr(subj, '__dict__'):
            subj_dict = {k: v for k, v in subj.__dict__.items() if not k.startswith('_')}
        else:
            subj_dict = subj
        subjects_list.append(subj_dict)
    
    # Apply rules engine
    subjects_list, rules_triggered = apply_rules(subjects_list)
    
    # Detect clashes
    clashes = detect_clashes(subjects_list)
    
    # Calculate total hours needed
    total_hours_needed = sum(subj.get("recommended_hours", 0) for subj in subjects_list)
    
    # Get date range
    dates = get_date_range(start_date, end_date)
    total_days = len(dates)
    total_available_hours = total_days * available_hours_per_day
    
    # Adjust if needed
    if total_hours_needed > total_available_hours:
        # Compress schedule - reduce hours proportionally
        compression_factor = total_available_hours / total_hours_needed
        for subj in subjects_list:
            subj["recommended_hours"] = subj.get("recommended_hours", 0) * compression_factor
    
    # Sort subjects by priority
    priority_order = {"urgent": 0, "high": 1, "medium": 2, "low": 3}
    subjects_list.sort(key=lambda x: (
        priority_order.get(x.get("priority", "medium"), 2),
        get_days_until_exam(x.get("exam_date", ""))
    ))
    
    # Generate time slots (assuming 1-hour slots)
    time_slots = []
    for i in range(int(available_hours_per_day)):
        hour = 9 + i  # Start at 9 AM
        time_slots.append(f"{hour:02d}:00-{hour+1:02d}:00")
    
    # Allocate subjects to days
    study_plan = []
    subject_index = 0
    hours_allocated_per_subject = {subj.get("id", i): 0.0 for i, subj in enumerate(subjects_list)}
    
    for date in dates:
        day_name = get_day_name(date)
        day_plan = {
            "date": date,
            "day": day_name,
            "time_slots": []
        }
        
        hours_used_today = 0.0
        slot_index = 0
        
        # Allocate subjects for this day
        while hours_used_today < available_hours_per_day and subject_index < len(subjects_list):
            subj = subjects_list[subject_index]
            subj_id = subj.get("id", subject_index)
            remaining_hours = subj.get("recommended_hours", 0) - hours_allocated_per_subject.get(subj_id, 0)
            
            if remaining_hours > 0 and slot_index < len(time_slots):
                hours_to_allocate = min(1.0, remaining_hours, available_hours_per_day - hours_used_today)
                
                day_plan["time_slots"].append({
                    "time": time_slots[slot_index],
                    "subject_id": subj_id,
                    "subject_name": subj.get("name", ""),
                    "hours": hours_to_allocate
                })
                
                hours_allocated_per_subject[subj_id] = hours_allocated_per_subject.get(subj_id, 0) + hours_to_allocate
                hours_used_today += hours_to_allocate
                slot_index += 1
                
                # Move to next subject if this one is fully allocated
                if hours_allocated_per_subject.get(subj_id, 0) >= subj.get("recommended_hours", 0):
                    subject_index += 1
            else:
                subject_index += 1
            
            # Reset if we've gone through all subjects
            if subject_index >= len(subjects_list):
                subject_index = 0
                # Check if all subjects are fully allocated
                if all(hours_allocated_per_subject.get(subj.get("id", i), 0) >= subj.get("recommended_hours", 0) 
                       for i, subj in enumerate(subjects_list)):
                    break
        
        study_plan.append(day_plan)
    
    return {
        "plan": study_plan,
        "rules_triggered": rules_triggered,
        "clashes": clashes,
        "total_hours_needed": total_hours_needed,
        "total_available_hours": total_available_hours
    }

