from sqlalchemy.orm import Session
from app.models.database import Subject

def subject_to_dict(subject: Subject) -> dict:
    """Convert SQLAlchemy subject to dictionary"""
    return {
        "id": subject.id,
        "name": subject.name,
        "difficulty": subject.difficulty,
        "exam_date": subject.exam_date,
        "past_score": subject.past_score,
        "chapters": subject.chapters,
        "has_assignment": subject.has_assignment,
        "has_exam": subject.has_exam,
        "last_week_hours": subject.last_week_hours,
        "recommended_hours": subject.recommended_hours,
        "priority": subject.priority
    }

