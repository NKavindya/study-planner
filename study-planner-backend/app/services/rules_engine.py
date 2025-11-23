from datetime import datetime
from app.utils.date_utils import get_days_until_exam

def apply_rules(subjects):
    """
    Apply 15+ rules to subjects for intelligent scheduling
    Returns: (updated_subjects, rules_triggered)
    """
    rules_triggered = []
    
    for subject in subjects:
        # Rule 1: Hard difficulty → increase recommended hours
        if subject.get("difficulty") == "hard":
            subject["recommended_hours"] = subject.get("recommended_hours", 0) + 2
            rules_triggered.append(f"Rule 1: {subject.get('name')} - Hard subject: +2 hours")
        
        # Rule 2: Medium difficulty → small extra
        if subject.get("difficulty") == "medium":
            subject["recommended_hours"] = subject.get("recommended_hours", 0) + 1
            rules_triggered.append(f"Rule 2: {subject.get('name')} - Medium subject: +1 hour")
        
        # Rule 3: Exam within 3 days → high priority
        exam_date = subject.get("exam_date")
        if exam_date:
            days_left = get_days_until_exam(exam_date)
            if days_left <= 3:
                subject["priority"] = "urgent"
                rules_triggered.append(f"Rule 3: {subject.get('name')} - Exam soon → urgent priority")
            
            # Rule 4: Exam within 7 days → medium priority
            if 3 < days_left <= 7:
                subject["priority"] = "high"
                rules_triggered.append(f"Rule 4: {subject.get('name')} - Exam in 7 days → high priority")
            
            # Rule 13: Big gap between today and exam (>30 days) → low priority
            if days_left > 30:
                subject["priority"] = "low"
                rules_triggered.append(f"Rule 13: {subject.get('name')} - Exam far → low priority")
        
        # Rule 5: Past score < 40 → more hours recommended
        past_score = subject.get("past_score", 0)
        if past_score < 40:
            subject["recommended_hours"] = subject.get("recommended_hours", 0) + 2
            rules_triggered.append(f"Rule 5: {subject.get('name')} - Low score <40 → +2 hours")
        
        # Rule 6: Past score > 75 → fewer hours
        if past_score > 75:
            subject["recommended_hours"] = max(1, subject.get("recommended_hours", 0) - 1)
            rules_triggered.append(f"Rule 6: {subject.get('name')} - High score >75 → -1 hour")
        
        # Rule 7: Assignment and exam in same week → increase study load
        if subject.get("has_assignment") and subject.get("has_exam"):
            subject["recommended_hours"] = subject.get("recommended_hours", 0) + 1
            rules_triggered.append(f"Rule 7: {subject.get('name')} - Assignment + exam → +1 hour")
        
        # Rule 8: Subject studied less than 2h last week → boost
        if subject.get("last_week_hours", 0) < 2:
            subject["recommended_hours"] = subject.get("recommended_hours", 0) + 1
            rules_triggered.append(f"Rule 8: {subject.get('name')} - Not studied last week → +1 hour")
        
        # Rule 9: If recommended hours <1 → fix to minimum
        if subject.get("recommended_hours", 0) < 1:
            subject["recommended_hours"] = 1
            rules_triggered.append(f"Rule 9: {subject.get('name')} - Minimum 1 hour rule")
        
        # Rule 10: More chapters → more hours needed
        chapters = subject.get("chapters", 0)
        if chapters > 10:
            subject["recommended_hours"] = subject.get("recommended_hours", 0) + 1
            rules_triggered.append(f"Rule 10: {subject.get('name')} - Many chapters → +1 hour")
        
        # Rule 11: Easy difficulty with good past score → reduce hours
        if subject.get("difficulty") == "easy" and past_score > 70:
            subject["recommended_hours"] = max(1, subject.get("recommended_hours", 0) - 0.5)
            rules_triggered.append(f"Rule 11: {subject.get('name')} - Easy + good score → -0.5 hour")
        
        # Rule 12: Hard difficulty with low past score → significant boost
        if subject.get("difficulty") == "hard" and past_score < 50:
            subject["recommended_hours"] = subject.get("recommended_hours", 0) + 3
            rules_triggered.append(f"Rule 12: {subject.get('name')} - Hard + low score → +3 hours")
        
        # Rule 14: Ensure priority is set
        if "priority" not in subject or not subject.get("priority"):
            days_left = get_days_until_exam(exam_date) if exam_date else 999
            if days_left <= 3:
                subject["priority"] = "urgent"
            elif days_left <= 7:
                subject["priority"] = "high"
            elif days_left > 30:
                subject["priority"] = "low"
            else:
                subject["priority"] = "medium"
            rules_triggered.append(f"Rule 14: {subject.get('name')} - Priority auto-set")
        
        # Rule 15: Cap maximum recommended hours at 8 per day
        if subject.get("recommended_hours", 0) > 8:
            subject["recommended_hours"] = 8
            rules_triggered.append(f"Rule 15: {subject.get('name')} - Capped at 8 hours max")
    
    return subjects, rules_triggered

def detect_clashes(subjects):
    """
    Detect overlapping exams and scheduling conflicts
    Returns: list of clash descriptions
    """
    clashes = []
    exam_dates = {}
    
    for subject in subjects:
        exam_date = subject.get("exam_date")
        if exam_date:
            if exam_date in exam_dates:
                clashes.append(f"Clash detected: {exam_dates[exam_date]} and {subject.get('name')} have exams on {exam_date}")
                exam_dates[exam_date].append(subject.get("name"))
            else:
                exam_dates[exam_date] = [subject.get("name")]
    
    return clashes

