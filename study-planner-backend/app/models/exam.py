from sqlalchemy.orm import Session
from app.models.database import Exam

def create_exam(db: Session, exam_data: dict):
    exam = Exam(**exam_data)
    db.add(exam)
    db.commit()
    db.refresh(exam)
    return exam

def get_exam(db: Session, exam_id: int):
    return db.query(Exam).filter(Exam.id == exam_id).first()

def get_all_exams(db: Session):
    return db.query(Exam).all()

def update_exam(db: Session, exam_id: int, exam_data: dict):
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if exam:
        for key, value in exam_data.items():
            setattr(exam, key, value)
        db.commit()
        db.refresh(exam)
    return exam

def delete_exam(db: Session, exam_id: int):
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if exam:
        db.delete(exam)
        db.commit()
    return exam


