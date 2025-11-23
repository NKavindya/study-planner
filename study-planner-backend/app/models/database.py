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
    recommended_hours = Column(Float, default=0.0)
    past_assignments = Column(Text, default="")  # JSON string or comma-separated
    questionnaire_results = Column(Text, default="")  # JSON string or text
    created_at = Column(DateTime, default=datetime.utcnow)

class Assignment(Base):
    __tablename__ = "assignments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    subject_name = Column(String)
    due_date = Column(String)  # YYYY-MM-DD
    estimated_hours = Column(Float, default=0.0)
    difficulty = Column(String, default="medium")  # easy, medium, hard
    priority = Column(String, default="medium")  # low, medium, high, urgent
    status = Column(String, default="pending")  # pending, in_progress, completed
    created_at = Column(DateTime, default=datetime.utcnow)

class Exam(Base):
    __tablename__ = "exams"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    subject_name = Column(String)
    exam_date = Column(String)  # YYYY-MM-DD
    difficulty = Column(String, default="medium")  # easy, medium, hard
    past_score = Column(Float, default=0.0)
    chapters = Column(Integer, default=0)
    recommended_hours = Column(Float, default=0.0)
    priority = Column(String, default="medium")  # low, medium, high, urgent
    created_at = Column(DateTime, default=datetime.utcnow)

class StudyPlan(Base):
    __tablename__ = "study_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer)  # Can be assignment_id or exam_id
    item_type = Column(String)  # "assignment" or "exam"
    item_name = Column(String)
    day = Column(String)
    time_slot = Column(String)
    hours = Column(Float)
    category = Column(String)  # "assignment" or "exam"
    created_at = Column(DateTime, default=datetime.utcnow)

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)  # "clash", "reminder", "warning"
    title = Column(String)
    message = Column(Text)
    item_type = Column(String)  # "assignment", "exam", or "both"
    item_ids = Column(String)  # Comma-separated IDs
    is_read = Column(Boolean, default=False)
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
    # Migrate existing tables if needed
    migrate_subjects_table()

def migrate_subjects_table():
    """Add new columns to subjects table if they don't exist"""
    from sqlalchemy import inspect, text
    
    try:
        inspector = inspect(engine)
        
        # Check if subjects table exists
        if 'subjects' not in inspector.get_table_names():
            return
        
        columns = [col['name'] for col in inspector.get_columns('subjects')]
        
        with engine.begin() as conn:
            # Add past_assignments column if it doesn't exist
            if 'past_assignments' not in columns:
                try:
                    conn.execute(text("ALTER TABLE subjects ADD COLUMN past_assignments TEXT DEFAULT ''"))
                    print("Added past_assignments column to subjects table")
                except Exception as e:
                    print(f"Error adding past_assignments column: {e}")
            
            # Add questionnaire_results column if it doesn't exist
            if 'questionnaire_results' not in columns:
                try:
                    conn.execute(text("ALTER TABLE subjects ADD COLUMN questionnaire_results TEXT DEFAULT ''"))
                    print("Added questionnaire_results column to subjects table")
                except Exception as e:
                    print(f"Error adding questionnaire_results column: {e}")
    except Exception as e:
        print(f"Error during migration: {e}")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

