from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

SQLALCHEMY_DATABASE_URL = "sqlite:///./study_planner.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Subject(Base):
    __tablename__ = "subjects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    difficulty = Column(String)  # easy, medium, hard
    exam_date = Column(String)
    past_score = Column(Float, default=0.0)
    chapters = Column(Integer, default=0)
    has_assignment = Column(Boolean, default=False)
    has_exam = Column(Boolean, default=True)
    last_week_hours = Column(Float, default=0.0)
    recommended_hours = Column(Float, default=0.0)
    priority = Column(String, default="medium")  # low, medium, high, urgent
    created_at = Column(DateTime, default=datetime.utcnow)

class StudyPlan(Base):
    __tablename__ = "study_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer)
    day = Column(String)
    time_slot = Column(String)
    hours = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

class Reminder(Base):
    __tablename__ = "reminders"
    
    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer)
    message = Column(Text)
    reminder_date = Column(String)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

