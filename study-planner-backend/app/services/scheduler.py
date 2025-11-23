from datetime import datetime, timedelta
from app.utils.date_utils import get_days_until_exam, get_date_range, is_weekend, get_day_name

def generate_study_plan(assignments, exams, available_hours_per_day: float, start_date: str, end_date: str):
    """
    Generate a study plan based on assignments and exams, availability, and date range
    """
    # Convert to list format
    assignments_list = []
    for assgn in assignments:
        if hasattr(assgn, '__dict__'):
            assgn_dict = {k: v for k, v in assgn.__dict__.items() if not k.startswith('_')}
        else:
            assgn_dict = assgn
        assignments_list.append(assgn_dict)
    
    exams_list = []
    for exam in exams:
        if hasattr(exam, '__dict__'):
            exam_dict = {k: v for k, v in exam.__dict__.items() if not k.startswith('_')}
        else:
            exam_dict = exam
        exams_list.append(exam_dict)
    
    # Combine all items with category
    all_items = []
    
    # Add assignments
    for assgn in assignments_list:
        item = {
            "id": assgn.get("id"),
            "name": assgn.get("name", ""),
            "category": "assignment",
            "hours": assgn.get("estimated_hours", 0),
            "priority": assgn.get("priority", "medium"),
            "due_date": assgn.get("due_date", ""),
            "subject_name": assgn.get("subject_name", "")
        }
        all_items.append(item)
    
    # Add exams
    for exam in exams_list:
        item = {
            "id": exam.get("id"),
            "name": exam.get("name", ""),
            "category": "exam",
            "hours": exam.get("recommended_hours", 0),
            "priority": exam.get("priority", "medium"),
            "due_date": exam.get("exam_date", ""),
            "subject_name": exam.get("subject_name", "")
        }
        all_items.append(item)
    
    # Apply rules for assignments
    rules_triggered = []
    for item in all_items:
        if item["category"] == "assignment":
            # Rule: Assignment due within 3 days → urgent
            days_left = get_days_until_exam(item["due_date"])
            if days_left <= 3:
                item["priority"] = "urgent"
                rules_triggered.append(f"Rule: {item['name']} - Assignment due soon → urgent priority")
            # Rule: Large assignment (>10 hours) → high priority
            if item["hours"] > 10:
                item["priority"] = "high"
                rules_triggered.append(f"Rule: {item['name']} - Large assignment → high priority")
            # Rule: Small assignment (<2 hours) → can be scheduled flexibly
            if item["hours"] < 2:
                item["priority"] = min(item["priority"], "medium")
        
        elif item["category"] == "exam":
            # Rule: Exam within 3 days → urgent
            days_left = get_days_until_exam(item["due_date"])
            if days_left <= 3:
                item["priority"] = "urgent"
                rules_triggered.append(f"Rule: {item['name']} - Exam soon → urgent priority")
            # Rule: Exam within 7 days → high priority
            if 3 < days_left <= 7:
                item["priority"] = "high"
                rules_triggered.append(f"Rule: {item['name']} - Exam in 7 days → high priority")
    
    # Calculate total hours needed
    total_hours_needed = sum(item.get("hours", 0) for item in all_items)
    
    # Get date range
    dates = get_date_range(start_date, end_date)
    total_days = len(dates)
    total_available_hours = total_days * available_hours_per_day
    
    # Adjust if needed
    if total_hours_needed > total_available_hours:
        # Compress schedule - reduce hours proportionally
        compression_factor = total_available_hours / total_hours_needed
        for item in all_items:
            item["hours"] = item.get("hours", 0) * compression_factor
        rules_triggered.append(f"Schedule compressed by {compression_factor:.2%} due to insufficient time")
    
    # Sort items by priority and due date
    priority_order = {"urgent": 0, "high": 1, "medium": 2, "low": 3}
    all_items.sort(key=lambda x: (
        priority_order.get(x.get("priority", "medium"), 2),
        get_days_until_exam(x.get("due_date", ""))
    ))
    
    # Generate time slots (assuming 1-hour slots)
    time_slots = []
    for i in range(int(available_hours_per_day)):
        hour = 9 + i  # Start at 9 AM
        time_slots.append(f"{hour:02d}:00-{hour+1:02d}:00")
    
    # Allocate items to days
    study_plan = []
    item_index = 0
    hours_allocated_per_item = {item.get("id", i): 0.0 for i, item in enumerate(all_items)}
    
    for date in dates:
        day_name = get_day_name(date)
        day_plan = {
            "date": date,
            "day": day_name,
            "time_slots": []
        }
        
        hours_used_today = 0.0
        slot_index = 0
        
        # Allocate items for this day
        while hours_used_today < available_hours_per_day and item_index < len(all_items):
            item = all_items[item_index]
            item_id = item.get("id", item_index)
            remaining_hours = item.get("hours", 0) - hours_allocated_per_item.get(item_id, 0)
            
            if remaining_hours > 0 and slot_index < len(time_slots):
                hours_to_allocate = min(1.0, remaining_hours, available_hours_per_day - hours_used_today)
                
                day_plan["time_slots"].append({
                    "time": time_slots[slot_index],
                    "item_id": item_id,
                    "item_name": item.get("name", ""),
                    "category": item.get("category", ""),
                    "subject_name": item.get("subject_name", ""),
                    "hours": hours_to_allocate
                })
                
                hours_allocated_per_item[item_id] = hours_allocated_per_item.get(item_id, 0) + hours_to_allocate
                hours_used_today += hours_to_allocate
                slot_index += 1
                
                # Move to next item if this one is fully allocated
                if hours_allocated_per_item.get(item_id, 0) >= item.get("hours", 0):
                    item_index += 1
            else:
                item_index += 1
            
            # Reset if we've gone through all items
            if item_index >= len(all_items):
                item_index = 0
                # Check if all items are fully allocated
                if all(hours_allocated_per_item.get(item.get("id", i), 0) >= item.get("hours", 0) 
                       for i, item in enumerate(all_items)):
                    break
        
        study_plan.append(day_plan)
    
    return {
        "plan": study_plan,
        "rules_triggered": rules_triggered,
        "total_hours_needed": total_hours_needed,
        "total_available_hours": total_available_hours
    }
