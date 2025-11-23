from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db, Subject, Assignment, Exam, StudyPlan, Notification, Reminder

router = APIRouter(prefix="/api/admin", tags=["admin"])

@router.delete("/clear-all")
def clear_all_data(db: Session = Depends(get_db)):
    """Clear all data from the database"""
    try:
        # Clear all tables
        db.query(StudyPlan).delete()
        db.query(Notification).delete()
        db.query(Reminder).delete()
        db.query(Assignment).delete()
        db.query(Exam).delete()
        db.query(Subject).delete()
        db.commit()
        return {
            "message": "All data cleared successfully",
            "cleared": {
                "subjects": True,
                "assignments": True,
                "exams": True,
                "study_plans": True,
                "notifications": True,
                "reminders": True
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error clearing data: {str(e)}")

