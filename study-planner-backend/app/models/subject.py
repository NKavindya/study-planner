from sqlalchemy.orm import Session
from app.models.database import Subject, Reminder
from datetime import datetime

def create_subject(db: Session, subject_data: dict):
    subject = Subject(**subject_data)
    db.add(subject)
    db.commit()
    db.refresh(subject)
    return subject

def get_subject(db: Session, subject_id: int):
    return db.query(Subject).filter(Subject.id == subject_id).first()

def get_all_subjects(db: Session):
    return db.query(Subject).all()

def update_subject(db: Session, subject_id: int, subject_data: dict):
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if subject:
        for key, value in subject_data.items():
            setattr(subject, key, value)
        db.commit()
        db.refresh(subject)
    return subject

def delete_subject(db: Session, subject_id: int):
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if subject:
        db.delete(subject)
        db.commit()
    return subject

def create_reminder(db: Session, reminder_data: dict):
    reminder = Reminder(**reminder_data)
    db.add(reminder)
    db.commit()
    db.refresh(reminder)
    return reminder

def get_active_reminders(db: Session):
    return db.query(Reminder).filter(Reminder.is_read == False).all()

def mark_reminder_read(db: Session, reminder_id: int):
    reminder = db.query(Reminder).filter(Reminder.id == reminder_id).first()
    if reminder:
        reminder.is_read = True
        db.commit()
        db.refresh(reminder)
    return reminder

