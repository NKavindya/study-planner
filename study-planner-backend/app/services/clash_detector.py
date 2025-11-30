from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.database import Assignment, Exam, Notification
from app.models import notification as notification_model

def detect_all_clashes(db: Session):
    """
    Detect all types of clashes:
    - Assignment-Assignment overlaps
    - Assignment-Exam overlaps
    - Exam-Exam overlaps
    """
    notifications = []
    
    # Get all assignments and exams
    assignments = db.query(Assignment).all()
    exams = db.query(Exam).all()
    
    # Detect Assignment-Assignment clashes
    for i, assgn1 in enumerate(assignments):
        for assgn2 in assignments[i+1:]:
            if assgn1.due_date == assgn2.due_date:
                # Same due date
                notification = {
                    "type": "clash",
                    "title": "Assignment Clash Detected",
                    "message": f"'{assgn1.name}' and '{assgn2.name}' are due on the same date ({assgn1.due_date})",
                    "item_type": "assignment",
                    "item_ids": f"{assgn1.id},{assgn2.id}"
                }
                notifications.append(notification)
            else:
                # Check if within 1 day of each other
                try:
                    date1 = datetime.strptime(assgn1.due_date, "%Y-%m-%d")
                    date2 = datetime.strptime(assgn2.due_date, "%Y-%m-%d")
                    if abs((date1 - date2).days) <= 1:
                        notification = {
                            "type": "clash",
                            "title": "Assignment Clash Warning",
                            "message": f"'{assgn1.name}' (due {assgn1.due_date}) and '{assgn2.name}' (due {assgn2.due_date}) are due within 1 day of each other",
                            "item_type": "assignment",
                            "item_ids": f"{assgn1.id},{assgn2.id}"
                        }
                        notifications.append(notification)
                except:
                    pass
    
    # Detect Exam-Exam clashes
    for i, exam1 in enumerate(exams):
        for exam2 in exams[i+1:]:
            if exam1.exam_date == exam2.exam_date:
                notification = {
                    "type": "clash",
                    "title": "Exam Clash Detected",
                    "message": f"'{exam1.name}' and '{exam2.name}' are scheduled on the same date ({exam1.exam_date})",
                    "item_type": "exam",
                    "item_ids": f"{exam1.id},{exam2.id}"
                }
                notifications.append(notification)
    
    # Detect Assignment-Exam clashes
    for assignment in assignments:
        for exam in exams:
            if assignment.due_date == exam.exam_date:
                notification = {
                    "type": "clash",
                    "title": "Assignment-Exam Clash",
                    "message": f"Assignment '{assignment.name}' is due on the same date as exam '{exam.name}' ({assignment.due_date})",
                    "item_type": "both",
                    "item_ids": f"assignment:{assignment.id},exam:{exam.id}"
                }
                notifications.append(notification)
            else:
                # Check if within 1 day
                try:
                    assgn_date = datetime.strptime(assignment.due_date, "%Y-%m-%d")
                    exam_date = datetime.strptime(exam.exam_date, "%Y-%m-%d")
                    if abs((assgn_date - exam_date).days) <= 1:
                        notification = {
                            "type": "clash",
                            "title": "Assignment-Exam Conflict",
                            "message": f"Assignment '{assignment.name}' (due {assignment.due_date}) and exam '{exam.name}' (on {exam.exam_date}) are within 1 day of each other",
                            "item_type": "both",
                            "item_ids": f"assignment:{assignment.id},exam:{exam.id}"
                        }
                        notifications.append(notification)
                except:
                    pass
    
    # Create notifications in database
    for notif_data in notifications:
        # Check if notification already exists
        existing = db.query(Notification).filter(
            Notification.message == notif_data["message"],
            Notification.is_read == False
        ).first()
        
        if not existing:
            notification_model.create_notification(db, notif_data)
    
    return notifications

def get_clash_summary(db: Session):
    """Get summary of all clashes"""
    assignments = db.query(Assignment).all()
    exams = db.query(Exam).all()
    
    summary = {
        "assignment_assignment_clashes": 0,
        "exam_exam_clashes": 0,
        "assignment_exam_clashes": 0,
        "total_clashes": 0
    }
    
    # Count assignment-assignment
    for i, assgn1 in enumerate(assignments):
        for assgn2 in assignments[i+1:]:
            if assgn1.due_date == assgn2.due_date:
                summary["assignment_assignment_clashes"] += 1
    
    # Count exam-exam
    for i, exam1 in enumerate(exams):
        for exam2 in exams[i+1:]:
            if exam1.exam_date == exam2.exam_date:
                summary["exam_exam_clashes"] += 1
    
    # Count assignment-exam
    for assignment in assignments:
        for exam in exams:
            if assignment.due_date == exam.exam_date:
                summary["assignment_exam_clashes"] += 1
    
    summary["total_clashes"] = (
        summary["assignment_assignment_clashes"] +
        summary["exam_exam_clashes"] +
        summary["assignment_exam_clashes"]
    )
    
    return summary

