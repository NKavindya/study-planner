"""
Automatic Reminder Generation Service
Generates reminders for upcoming exams and deadlines based on dates and priorities.
"""
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.database import Assignment, Exam, Reminder
from app.models import subject as subject_model


def generate_automatic_reminders(db: Session):
    """
    Automatically generate reminders for:
    - Exams within 7 days
    - Assignments due within 3 days
    - Exams within 3 days (urgent)
    """
    reminders_created = []
    today = datetime.now().date()
    
    # Get all assignments
    assignments = db.query(Assignment).all()
    for assignment in assignments:
        if assignment.due_date:
            try:
                due_date = datetime.strptime(assignment.due_date, "%Y-%m-%d").date()
                days_until = (due_date - today).days
                
                # Create reminder if due within 3 days
                if 0 <= days_until <= 3:
                    message = f"Assignment '{assignment.name}' is due in {days_until} day(s) ({assignment.due_date})"
                    reminder_data = {
                        "subject_id": None,  # Assignments don't have subject_id directly
                        "message": message,
                        "reminder_date": assignment.due_date,
                        "is_read": False
                    }
                    
                    # Check if reminder already exists
                    existing = db.query(Reminder).filter(
                        Reminder.message == message,
                        Reminder.is_read == False
                    ).first()
                    
                    if not existing:
                        reminder = subject_model.create_reminder(db, reminder_data)
                        reminders_created.append(message)
            except Exception as e:
                print(f"Error processing assignment reminder: {e}")
    
    # Get all exams
    exams = db.query(Exam).all()
    for exam in exams:
        if exam.exam_date:
            try:
                exam_date = datetime.strptime(exam.exam_date, "%Y-%m-%d").date()
                days_until = (exam_date - today).days
                
                # Create reminders for exams
                if 0 <= days_until <= 7:
                    if days_until <= 3:
                        message = f"⚠️ URGENT: Exam '{exam.name}' is in {days_until} day(s) ({exam.exam_date})"
                    else:
                        message = f"Exam '{exam.name}' is in {days_until} day(s) ({exam.exam_date})"
                    
                    reminder_data = {
                        "subject_id": None,
                        "message": message,
                        "reminder_date": exam.exam_date,
                        "is_read": False
                    }
                    
                    # Check if reminder already exists
                    existing = db.query(Reminder).filter(
                        Reminder.message == message,
                        Reminder.is_read == False
                    ).first()
                    
                    if not existing:
                        reminder = subject_model.create_reminder(db, reminder_data)
                        reminders_created.append(message)
            except Exception as e:
                print(f"Error processing exam reminder: {e}")
    
    return reminders_created

