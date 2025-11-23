from sqlalchemy.orm import Session
from app.models.database import Assignment

def create_assignment(db: Session, assignment_data: dict):
    assignment = Assignment(**assignment_data)
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment

def get_assignment(db: Session, assignment_id: int):
    return db.query(Assignment).filter(Assignment.id == assignment_id).first()

def get_all_assignments(db: Session):
    return db.query(Assignment).all()

def update_assignment(db: Session, assignment_id: int, assignment_data: dict):
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if assignment:
        for key, value in assignment_data.items():
            setattr(assignment, key, value)
        db.commit()
        db.refresh(assignment)
    return assignment

def delete_assignment(db: Session, assignment_id: int):
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if assignment:
        db.delete(assignment)
        db.commit()
    return assignment


