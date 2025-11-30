from datetime import datetime, timedelta
from app.utils.date_utils import get_days_until_exam, get_date_range, is_weekend, get_day_name

def detect_and_handle_clashes(assignments_list, exams_list):
    """
    Detect clashes and automatically adjust priorities/rearrange items.
    Rule-based logic: When overlapping exams are detected, rearrange study slots
    by adjusting priorities and spreading items across available dates.
    Returns: (adjusted_items, clash_rearrangements)
    """
    all_items = []
    clash_rearrangements = []
    
    # Add assignments
    for assgn in assignments_list:
        item = {
            "id": assgn.get("id"),
            "name": assgn.get("name", ""),
            "category": "assignment",
            "hours": assgn.get("estimated_hours", 0),
            "priority": assgn.get("priority", "medium"),
            "due_date": assgn.get("due_date", ""),
            "subject_name": assgn.get("subject_name", ""),
            "deadline": assgn.get("due_date", "")
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
            "subject_name": exam.get("subject_name", ""),
            "deadline": exam.get("exam_date", "")
        }
        all_items.append(item)
    
    # Detect clashes and rearrange
    # Check for overlapping exams (same exam date)
    exam_dates = {}
    for item in all_items:
        if item["category"] == "exam" and item.get("due_date"):
            exam_date = item["due_date"]
            if exam_date not in exam_dates:
                exam_dates[exam_date] = []
            exam_dates[exam_date].append(item)
    
    # Check for overlapping assignments (same due date or within 1 day)
    assignment_dates = {}
    for item in all_items:
        if item["category"] == "assignment" and item.get("due_date"):
            due_date = item["due_date"]
            if due_date not in assignment_dates:
                assignment_dates[due_date] = []
            assignment_dates[due_date].append(item)
    
    # Handle exam-exam clashes: rearrange by adjusting priorities and spreading study time
    for exam_date, conflicting_exams in exam_dates.items():
        if len(conflicting_exams) > 1:
            clash_rearrangements.append(
                f"Clash detected: {len(conflicting_exams)} exams on {exam_date}. "
                f"Rearranging study slots to spread preparation across available dates."
            )
            # Increase priority for all conflicting exams
            # And distribute hours more evenly by starting earlier
            for exam in conflicting_exams:
                if exam["priority"] != "urgent":
                    exam["priority"] = "high"
                    # Increase recommended hours to allow for earlier start
                    exam["hours"] = exam.get("hours", 0) * 1.2  # Add 20% buffer
    
    # Handle assignment-assignment clashes
    for due_date, conflicting_assignments in assignment_dates.items():
        if len(conflicting_assignments) > 1:
            clash_rearrangements.append(
                f"Clash detected: {len(conflicting_assignments)} assignments due on {due_date}. "
                f"Rearranging study slots to ensure all assignments are completed on time."
            )
            # Prioritize larger assignments and spread workload
            conflicting_assignments.sort(key=lambda x: x.get("hours", 0), reverse=True)
            for idx, assignment in enumerate(conflicting_assignments):
                # Give highest priority to the largest assignment
                if idx == 0 and assignment["hours"] > 5:
                    assignment["priority"] = "urgent"
                elif assignment["priority"] != "urgent":
                    assignment["priority"] = "high"
    
    # Handle assignment-exam conflicts (same date or within 1 day)
    for assignment in all_items:
        if assignment["category"] == "assignment" and assignment.get("due_date"):
            assgn_date = datetime.strptime(assignment["due_date"], "%Y-%m-%d")
            for exam in all_items:
                if exam["category"] == "exam" and exam.get("due_date"):
                    try:
                        exam_date = datetime.strptime(exam["due_date"], "%Y-%m-%d")
                        days_diff = abs((assgn_date - exam_date).days)
                        if days_diff <= 1:
                            clash_rearrangements.append(
                                f"Conflict: Assignment '{assignment['name']}' and exam '{exam['name']}' "
                                f"within {days_diff} day(s). Rearranging to prioritize assignment completion."
                            )
                            # Prioritize assignment (must be done first)
                            assignment["priority"] = "urgent"
                            # Start exam preparation earlier
                            if exam["priority"] != "urgent":
                                exam["priority"] = "high"
                    except:
                        pass
    
    return all_items, clash_rearrangements

def generate_study_plan(assignments, exams, available_hours_per_day: float, start_date: str, end_date: str):
    """
    Generate a deadline-aware study plan with automatic clash resolution:
    - Detects overlapping exams and automatically rearranges study slots
    - Assignments must be scheduled BEFORE their due dates
    - After assignment due dates, time can be allocated to exams
    - Exams should be scheduled before their exam dates
    - Rule-based logic rearranges items when clashes are detected
    """
    # Validate inputs
    if available_hours_per_day <= 0:
        raise ValueError("Available hours per day must be greater than 0")
    
    if not start_date or not end_date:
        raise ValueError("Start date and end date are required")
    
    # Convert to list format
    assignments_list = []
    if assignments:
        for assgn in assignments:
            try:
                if hasattr(assgn, '__dict__'):
                    assgn_dict = {k: v for k, v in assgn.__dict__.items() if not k.startswith('_')}
                else:
                    assgn_dict = assgn
                assignments_list.append(assgn_dict)
            except Exception as e:
                print(f"Error processing assignment: {e}")
                continue
    
    exams_list = []
    if exams:
        for exam in exams:
            try:
                if hasattr(exam, '__dict__'):
                    exam_dict = {k: v for k, v in exam.__dict__.items() if not k.startswith('_')}
                else:
                    exam_dict = exam
                exams_list.append(exam_dict)
            except Exception as e:
                print(f"Error processing exam: {e}")
                continue
    
    # Detect clashes and automatically rearrange (rule-based logic)
    all_items, clash_rearrangements = detect_and_handle_clashes(assignments_list, exams_list)
    
    # Apply additional rules
    rules_triggered = []
    # Add clash rearrangements to rules_triggered
    rules_triggered.extend(clash_rearrangements)
    for item in all_items:
        if item["category"] == "assignment":
            days_left = get_days_until_exam(item["due_date"])
            if days_left <= 3:
                item["priority"] = "urgent"
                rules_triggered.append(f"Rule: {item['name']} - Assignment due soon → urgent priority")
            elif days_left <= 7:
                item["priority"] = "high"
            if item["hours"] > 10:
                item["priority"] = "high"
                rules_triggered.append(f"Rule: {item['name']} - Large assignment → high priority")
        
        elif item["category"] == "exam":
            days_left = get_days_until_exam(item["due_date"])
            if days_left <= 3:
                item["priority"] = "urgent"
                rules_triggered.append(f"Rule: {item['name']} - Exam soon → urgent priority")
            elif days_left <= 7:
                item["priority"] = "high"
                rules_triggered.append(f"Rule: {item['name']} - Exam in 7 days → high priority")
    
    # Get date range
    dates = get_date_range(start_date, end_date)
    total_days = len(dates)
    total_available_hours = total_days * available_hours_per_day
    
    # Calculate total hours needed
    total_hours_needed = sum(item.get("hours", 0) for item in all_items)
    
    # Adjust if needed
    if total_hours_needed > total_available_hours:
        compression_factor = total_available_hours / total_hours_needed
        for item in all_items:
            item["hours"] = item.get("hours", 0) * compression_factor
        rules_triggered.append(f"Schedule compressed by {compression_factor:.2%} due to insufficient time")
    
    # Sort items by priority and deadline
    priority_order = {"urgent": 0, "high": 1, "medium": 2, "low": 3}
    all_items.sort(key=lambda x: (
        priority_order.get(x.get("priority", "medium"), 2),
        get_days_until_exam(x.get("due_date", ""))
    ))
    
    # Generate time slots
    time_slots = []
    for i in range(int(available_hours_per_day)):
        hour = 9 + i
        time_slots.append(f"{hour:02d}:00-{hour+1:02d}:00")
    
    # Deadline-aware allocation
    study_plan = []
    hours_allocated_per_item = {item.get("id", i): 0.0 for i, item in enumerate(all_items)}
    
    print(f"DEBUG: Starting allocation for {len(dates)} dates with {len(all_items)} items")
    
    for date in dates:
        day_name = get_day_name(date)
        # Fallback if day_name is invalid
        if not day_name or day_name == "Unknown":
            try:
                date_obj = datetime.strptime(date, "%Y-%m-%d")
                day_name = date_obj.strftime("%A")
            except:
                day_name = "Unknown"
        
        day_plan = {
            "date": date,
            "day": day_name,
            "time_slots": []
        }
        print(f"DEBUG: Created day_plan for {date} ({day_name})")
        
        # Get items that can be scheduled on this date
        # Assignments: only if due_date is after this date (or same day)
        # Exams: only if exam_date is after this date (or same day)
        available_items = []
        current_date_obj = datetime.strptime(date, "%Y-%m-%d")
        
        for item in all_items:
            item_id = item.get("id")
            remaining_hours = item.get("hours", 0) - hours_allocated_per_item.get(item_id, 0)
            
            if remaining_hours > 0:
                deadline = item.get("deadline", "")
                if deadline:
                    try:
                        deadline_date = datetime.strptime(deadline, "%Y-%m-%d")
                        # Can schedule if deadline is on or after current date
                        if deadline_date >= current_date_obj:
                            available_items.append(item)
                        else:
                            print(f"DEBUG: Item {item.get('name')} deadline {deadline} is before {date}, skipping")
                    except Exception as e:
                        print(f"DEBUG: Error parsing deadline {deadline}: {e}, including item anyway")
                        available_items.append(item)
                else:
                    # No deadline, include it
                    available_items.append(item)
        
        print(f"DEBUG: Date {date} ({day_name}) has {len(available_items)} available items")
        
        # Sort available items by priority
        available_items.sort(key=lambda x: (
            priority_order.get(x.get("priority", "medium"), 2),
            get_days_until_exam(x.get("due_date", ""))
        ))
        
        hours_used_today = 0.0
        slot_index = 0
        
        # Allocate items for this day
        for item in available_items:
            if hours_used_today >= available_hours_per_day or slot_index >= len(time_slots):
                break
            
            item_id = item.get("id")
            remaining_hours = item.get("hours", 0) - hours_allocated_per_item.get(item_id, 0)
            
            if remaining_hours > 0:
                hours_to_allocate = min(1.0, remaining_hours, available_hours_per_day - hours_used_today)
                
                slot_data = {
                    "time": time_slots[slot_index],
                    "item_id": item_id,
                    "item_name": item.get("name", ""),
                    "category": item.get("category", ""),
                    "subject_name": item.get("subject_name", ""),
                    "hours": hours_to_allocate
                }
                day_plan["time_slots"].append(slot_data)
                
                hours_allocated_per_item[item_id] = hours_allocated_per_item.get(item_id, 0) + hours_to_allocate
                hours_used_today += hours_to_allocate
                slot_index += 1
        
        print(f"DEBUG: Day {day_name} allocated {len(day_plan['time_slots'])} slots")
        if len(day_plan['time_slots']) > 0:
            print(f"DEBUG: First slot for {day_name}: {day_plan['time_slots'][0]}")
        study_plan.append(day_plan)
    
    print(f"DEBUG: Generated plan with {len(study_plan)} days, total slots: {sum(len(d['time_slots']) for d in study_plan)}")
    
    return {
        "plan": study_plan,
        "rules_triggered": rules_triggered,
        "total_hours_needed": total_hours_needed,
        "total_available_hours": total_available_hours
    }
