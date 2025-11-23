from sqlalchemy.orm import Session
from app.models.database import StudyPlan, Subject

def create_study_plan(db: Session, plan_data: dict):
    plan = StudyPlan(**plan_data)
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan

def get_study_plans(db: Session):
    return db.query(StudyPlan).all()

def get_study_plans_by_day(db: Session, day: str):
    return db.query(StudyPlan).filter(StudyPlan.day == day).all()

def delete_study_plan(db: Session, plan_id: int):
    plan = db.query(StudyPlan).filter(StudyPlan.id == plan_id).first()
    if plan:
        db.delete(plan)
        db.commit()
    return plan

def clear_all_plans(db: Session):
    db.query(StudyPlan).delete()
    db.commit()
    return {"message": "All plans cleared"}

