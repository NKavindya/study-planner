# Intelligent Study Planner - Project Report

## Problem Addressed

Students often struggle with managing their study schedules effectively, especially when dealing with multiple subjects, varying difficulty levels, and tight deadlines. The challenge lies in:

1. **Time Management**: Allocating appropriate study time for each subject based on difficulty, past performance, and exam proximity
2. **Clash Detection**: Identifying and resolving scheduling conflicts (e.g., overlapping exams, insufficient time allocation)
3. **Priority Management**: Determining which subjects need immediate attention based on deadlines and performance history
4. **Adaptive Scheduling**: Creating flexible study plans that can be adjusted based on changing circumstances

Traditional study planners lack the intelligence to automatically optimize schedules based on multiple factors, requiring manual intervention and often resulting in suboptimal time allocation.

## Approach

This project implements an **Intelligent Study Planner** that combines:

1. **Rule-Based Logic Engine**: A comprehensive set of 15+ rules that automatically adjust study recommendations based on:
   - Subject difficulty (easy, medium, hard)
   - Exam proximity (days until exam)
   - Past performance scores
   - Assignment and exam conflicts
   - Study history (hours studied last week)
   - Number of chapters

2. **Machine Learning Model**: A Linear Regression model that predicts recommended study hours based on:
   - Past score (0-100)
   - Difficulty level (easy=0, medium=1, hard=2)
   - Number of chapters
   - Days left until exam

3. **Intelligent Scheduler**: An algorithm that:
   - Detects clashes (overlapping exams)
   - Prioritizes subjects based on urgency
   - Allocates time slots efficiently
   - Compresses schedules when needed
   - Distributes study load evenly

4. **Interactive Interface**: A modern web application that allows users to:
   - Add and manage subjects
   - Generate optimized study plans
   - View weekly schedules
   - Receive reminders
   - Interact via command interface

## Implementation Details

### Architecture

The application follows a **MERN-style architecture** with:

- **Frontend**: React (with Vite) for modern, responsive UI
- **Backend**: FastAPI (Python) for RESTful API
- **Database**: SQLite for lightweight, file-based storage

### Backend Implementation

#### 1. Database Models (`app/models/database.py`)

Three main models:
- **Subject**: Stores subject information (name, difficulty, exam date, past scores, etc.)
- **StudyPlan**: Stores generated study schedules (day, time slot, subject, hours)
- **Reminder**: Stores reminders for upcoming exams and deadlines

#### 2. Rules Engine (`app/services/rules_engine.py`)

Implements 15 intelligent rules:

1. **Hard difficulty → +2 hours**: Hard subjects require more study time
2. **Medium difficulty → +1 hour**: Medium subjects get moderate boost
3. **Exam within 3 days → urgent priority**: Immediate attention needed
4. **Exam within 7 days → high priority**: High priority scheduling
5. **Past score < 40 → +2 hours**: Low performers need extra time
6. **Past score > 75 → -1 hour**: High performers need less time
7. **Assignment + exam → +1 hour**: Combined workload increases time
8. **Not studied last week → +1 hour**: Catch-up time needed
9. **Minimum 1 hour rule**: Ensure at least 1 hour per subject
10. **Many chapters (>10) → +1 hour**: More content requires more time
11. **Easy + good score → -0.5 hour**: Reduce time for easy subjects with good scores
12. **Hard + low score → +3 hours**: Significant boost for struggling students
13. **Exam > 30 days away → low priority**: Distant exams get lower priority
14. **Auto-set priority**: Automatically assign priority if missing
15. **Cap at 8 hours max**: Prevent unrealistic daily allocations

**Clash Detection**:
- Detects overlapping exam dates
- Identifies subjects with exams on the same day
- Provides warnings for scheduling conflicts

#### 3. ML Model (`app/services/ml_model.py`)

**Model Type**: Linear Regression

**Features**:
- `past_score`: Previous performance (0-100)
- `difficulty_level`: Numeric encoding (easy=0, medium=1, hard=2)
- `chapters`: Number of chapters to cover
- `days_left`: Days until exam

**Training Data**: 
- Sample dataset with 15 examples
- Can be extended with real user data
- Automatically creates training data if file doesn't exist

**Prediction**:
- Returns recommended study hours (minimum 1 hour)
- Used when creating/updating subjects
- Continuously improves with more training data

#### 4. Scheduler (`app/services/scheduler.py`)

**Algorithm**:
1. Apply rules engine to all subjects
2. Detect clashes
3. Calculate total hours needed vs. available
4. Compress schedule if needed (proportional reduction)
5. Sort subjects by priority (urgent > high > medium > low)
6. Allocate time slots (1-hour blocks starting at 9 AM)
7. Distribute subjects across available days
8. Generate weekly plan with day-by-day breakdown

**Features**:
- Handles insufficient time by compressing schedules
- Prioritizes urgent subjects
- Distributes study load evenly
- Creates time slots based on user availability

#### 5. API Endpoints

**Subjects API** (`/api/subjects`):
- `POST /`: Create new subject (with ML prediction)
- `GET /`: Get all subjects
- `GET /{id}`: Get specific subject
- `PUT /{id}`: Update subject
- `DELETE /{id}`: Delete subject
- `GET /reminders/active`: Get active reminders

**Planner API** (`/api/planner`):
- `POST /generate`: Generate study plan
- `GET /weekly`: Get weekly study plan
- `DELETE /clear`: Clear all plans

**ML API** (`/api/ml`):
- `POST /train`: Train the ML model
- `POST /predict`: Predict study hours for given inputs

### Frontend Implementation

#### 1. Components

- **Navbar**: Navigation between pages
- **SubjectForm**: Form for adding/editing subjects
- **StudyPlanTable**: Displays weekly study schedule
- **ReminderBanner**: Shows active reminders
- **Loader**: Loading indicator

#### 2. Pages

- **Dashboard**: Overview with statistics and recent subjects
- **AddSubjects**: Manage subjects (add, view, delete)
- **GeneratePlan**: Generate new study plans
- **ViewPlan**: View current study schedule
- **Settings**: ML model training and command interface info

#### 3. Interactive Command Interface

The Settings page provides a command interface where users can:
- `add subject`: Navigate to add subjects page
- `generate plan`: Generate a new study schedule
- `view plan`: View current schedule
- `clear plan`: Clear existing plan

Commands are implemented as navigation actions and button clicks in the UI.

#### 4. API Integration

- Custom hooks (`useFetch`, `usePost`, `useDelete`) for API calls
- Centralized API modules (`subjects.js`, `plan.js`, `ml.js`)
- Error handling and loading states
- Automatic data refresh

### Key Features

1. **AI-Powered Recommendations**: ML model predicts optimal study hours
2. **Rule-Based Optimization**: 15+ rules automatically adjust schedules
3. **Clash Detection**: Identifies and warns about conflicts
4. **Priority Management**: Automatically prioritizes based on deadlines
5. **Flexible Rescheduling**: Easy to regenerate plans with new parameters
6. **Reminders**: Active reminders for upcoming exams
7. **Responsive UI**: Modern, mobile-friendly interface
8. **Real-time Updates**: Automatic refresh of data

## Technical Stack

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: ORM for database operations
- **SQLite**: Lightweight database
- **scikit-learn**: Machine learning library
- **pandas**: Data manipulation
- **Pydantic**: Data validation

### Frontend
- **React 18**: UI library
- **React Router**: Navigation
- **Vite**: Build tool and dev server
- **Axios**: HTTP client
- **CSS3**: Styling with modern gradients and animations

## Database Schema

### Subjects Table
- `id`: Primary key
- `name`: Subject name
- `difficulty`: easy/medium/hard
- `exam_date`: Exam date (YYYY-MM-DD)
- `past_score`: Previous score (0-100)
- `chapters`: Number of chapters
- `has_assignment`: Boolean
- `has_exam`: Boolean
- `last_week_hours`: Hours studied last week
- `recommended_hours`: ML-predicted hours
- `priority`: urgent/high/medium/low
- `created_at`: Timestamp

### StudyPlans Table
- `id`: Primary key
- `subject_id`: Foreign key to subjects
- `day`: Day of week
- `time_slot`: Time range (e.g., "09:00-10:00")
- `hours`: Hours allocated
- `created_at`: Timestamp

### Reminders Table
- `id`: Primary key
- `subject_id`: Foreign key to subjects
- `message`: Reminder message
- `reminder_date`: Date for reminder
- `is_read`: Boolean flag
- `created_at`: Timestamp

## Future Enhancements

1. **Advanced ML Models**: Implement more sophisticated models (Random Forest, Neural Networks)
2. **User Feedback Loop**: Allow users to rate predictions and retrain model
3. **Calendar Integration**: Sync with Google Calendar, Outlook
4. **Mobile App**: Native mobile applications
5. **Collaborative Planning**: Share plans with study groups
6. **Analytics Dashboard**: Track study patterns and performance
7. **Adaptive Learning**: Learn from user behavior over time
8. **Notification System**: Push notifications for reminders
9. **Export Features**: Export plans to PDF, CSV
10. **Multi-language Support**: Internationalization

## Conclusion

The Intelligent Study Planner successfully addresses the problem of inefficient study scheduling by combining rule-based logic, machine learning, and intelligent algorithms. The system automatically optimizes study schedules based on multiple factors, detects conflicts, and provides a user-friendly interface for managing academic workload.

The implementation demonstrates:
- Effective use of AI/ML for prediction
- Comprehensive rule-based optimization
- Modern web development practices
- Scalable architecture
- User-centric design

The project provides a solid foundation for further enhancements and can be extended to support more advanced features and larger user bases.

