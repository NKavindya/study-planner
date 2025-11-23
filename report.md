# Intelligent Study Planner - Project Report

## Problem Addressed

Students often struggle with managing their study schedules effectively, especially when dealing with multiple subjects, varying difficulty levels, and tight deadlines. The challenge lies in:

1. **Time Management**: Allocating appropriate study time for each subject based on difficulty, past performance, and exam proximity
2. **Clash Detection**: Identifying and resolving scheduling conflicts (e.g., overlapping exams, overlapping assignments, assignment-exam conflicts, insufficient time allocation)
3. **Priority Management**: Determining which subjects need immediate attention based on deadlines and performance history
4. **Adaptive Scheduling**: Creating flexible study plans that can be adjusted based on changing circumstances
5. **Assignment Management**: Tracking assignments separately from exams with estimated completion times
6. **Real-time Notifications**: Being informed immediately about scheduling conflicts and important deadlines

Traditional study planners lack the intelligence to automatically optimize schedules based on multiple factors, requiring manual intervention and often resulting in suboptimal time allocation. Additionally, they fail to distinguish between assignments and exams, which have different time allocation requirements.

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
   - Detects clashes (overlapping exams, assignments, and assignment-exam conflicts)
   - Prioritizes items based on urgency and category
   - Allocates time slots efficiently for both assignments and exams
   - Uses estimated hours for assignments and ML-predicted hours for exams
   - Compresses schedules when needed
   - Distributes study load evenly
   - Categorizes study plan items (assignment vs exam)

4. **Comprehensive Clash Detection System**: Automatically detects and notifies users about:
   - Assignment-Assignment overlaps (same due date or within 1 day)
   - Exam-Exam overlaps (same exam date)
   - Assignment-Exam conflicts (same date or within 1 day)

5. **Real-time Notification System**: 
   - Notification icon with unread count badge
   - Automatic clash detection on create/update/delete
   - Dropdown notification panel
   - Mark as read functionality

6. **Interactive Interface**: A modern web application that allows users to:
   - Add and manage subjects, assignments, and exams separately
   - Specify estimated hours for assignments
   - Generate optimized study plans with category distinction
   - View weekly schedules with assignment/exam categories
   - Receive real-time notifications about conflicts
   - Interact via command interface

## Implementation Details

### Architecture

The application follows a **MERN-style architecture** with:

- **Frontend**: React (with Vite) for modern, responsive UI
- **Backend**: FastAPI (Python) for RESTful API
- **Database**: SQLite for lightweight, file-based storage

### Backend Implementation

#### 1. Database Models (`app/models/database.py`)

Six main models:
- **Subject**: Stores simplified subject information (name, difficulty, recommended hours, past assignments, questionnaire results)
- **Assignment**: Stores assignment information (name, subject_name from dropdown, due date, estimated hours, difficulty, status)
- **Exam**: Stores exam information (name, subject_name from dropdown, exam date, difficulty, past score, chapters, recommended hours)
- **StudyPlan**: Stores generated study schedules (day, time slot, item_id, item_type, category, hours, subject_name)
- **Notification**: Stores clash notifications and reminders (type, title, message, item_type, item_ids, is_read)
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

**Clash Detection** (Enhanced in `app/services/clash_detector.py`):
- Detects Assignment-Assignment overlaps (same due date or within 1 day)
- Detects Exam-Exam overlaps (same exam date)
- Detects Assignment-Exam conflicts (same date or within 1 day)
- Automatically creates notifications for all detected clashes
- Prevents duplicate notifications
- Provides detailed clash summaries

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

#### 4. Enhanced Scheduler (`app/services/scheduler.py`)

**Algorithm**:
1. Combine assignments and exams into unified item list
2. Apply rules for assignments (due date proximity, estimated hours)
3. Apply rules for exams (exam date proximity, ML-predicted hours)
4. Calculate total hours needed (assignments use estimated_hours, exams use recommended_hours)
5. Compress schedule if needed (proportional reduction)
6. Sort items by priority (urgent > high > medium > low) and due date
7. Allocate time slots (1-hour blocks starting at 9 AM)
8. Distribute items across available days with category tracking
9. Generate weekly plan with day-by-day breakdown including category

**Features**:
- Handles assignments separately from exams
- Uses estimated hours for assignments (user-provided)
- Uses ML-predicted hours for exams
- Includes category column (assignment/exam) in study plans
- Handles insufficient time by compressing schedules
- Prioritizes urgent items based on due dates
- Distributes study load evenly
- Creates time slots based on user availability
- Tracks subject names for both assignments and exams

**New Rules for Assignments**:
- Assignment due within 3 days → urgent priority
- Large assignment (>10 hours) → high priority
- Small assignment (<2 hours) → flexible scheduling

**New Rules for Exams**:
- Exam within 3 days → urgent priority
- Exam within 7 days → high priority

#### 5. API Endpoints

**Subjects API** (`/api/subjects`):
- `POST /`: Create new subject (simplified: name, difficulty, past_assignments, questionnaire_results)
- `GET /`: Get all subjects
- `GET /{id}`: Get specific subject
- `PUT /{id}`: Update subject
- `DELETE /{id}`: Delete subject
- `GET /reminders/active`: Get active reminders

**Note**: Subjects are now simplified to store only essential information. Recommended hours are calculated based on difficulty (easy: 2h, medium: 4h, hard: 6h). Assignments and exams are linked to subjects via subject_name dropdown selection.

**Assignments API** (`/api/assignments`):
- `POST /`: Create new assignment (triggers clash detection)
- `GET /`: Get all assignments
- `GET /{id}`: Get specific assignment
- `PUT /{id}`: Update assignment (triggers clash detection)
- `DELETE /{id}`: Delete assignment (triggers clash detection)

**Exams API** (`/api/exams`):
- `POST /`: Create new exam (with ML prediction, triggers clash detection)
- `GET /`: Get all exams
- `GET /{id}`: Get specific exam
- `PUT /{id}`: Update exam (triggers clash detection)
- `DELETE /{id}`: Delete exam (triggers clash detection)

**Notifications API** (`/api/notifications`):
- `GET /`: Get all notifications (optional: unread_only parameter)
- `GET /unread/count`: Get count of unread notifications
- `POST /{id}/read`: Mark notification as read
- `POST /read-all`: Mark all notifications as read
- `DELETE /{id}`: Delete notification
- `POST /detect-clashes`: Manually trigger clash detection

**Planner API** (`/api/planner`):
- `POST /generate`: Generate study plan (uses assignments and exams)
- `GET /weekly`: Get weekly study plan (includes category column)
- `DELETE /clear`: Clear all plans

**ML API** (`/api/ml`):
- `POST /train`: Train the ML model
- `POST /predict`: Predict study hours for given inputs

### Frontend Implementation

#### 1. Components

- **Navbar**: Navigation between pages with notification icon
- **NotificationIcon**: Notification bell icon with unread count badge and dropdown panel
- **SubjectForm**: Simplified form for adding/editing subjects (name, difficulty, past assignments, questionnaire results)
- **AssignmentForm**: Form for adding/editing assignments (includes subject dropdown, estimated hours field, and relevant assignment questions)
- **ExamForm**: Form for adding/editing exams (includes subject dropdown and relevant exam questions)
- **StudyPlanTable**: Displays weekly study schedule with category column
- **ReminderBanner**: Shows active reminders
- **Loader**: Loading indicator

#### 2. Pages

- **Dashboard**: Overview with statistics and recent subjects
- **AddSubjects**: Simplified subject management (shows: name, difficulty, recommended hours, past assignments, questionnaire results)
- **AddAssignments**: Manage assignments (add, view, delete) with subject dropdown and estimated hours
- **AddExams**: Manage exams (add, view, delete) with subject dropdown
- **GeneratePlan**: Generate new study plans (includes assignments and exams)
- **ViewPlan**: View current study schedule with category distinction
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
- Centralized API modules (`subjects.js`, `assignments.js`, `exams.js`, `notifications.js`, `plan.js`, `ml.js`)
- Error handling and loading states
- Automatic data refresh
- Real-time notification polling (every 30 seconds)

#### 5. Notification System

- **Notification Icon**: Bell icon in navbar with unread count badge
- **Dropdown Panel**: Shows all unread notifications with:
  - Notification type icons (clash, reminder, warning)
  - Title and message for each notification
  - Click to mark as read
  - "Mark all read" functionality
- **Auto-refresh**: Checks for new notifications every 30 seconds
- **Visual Indicators**: Color-coded notifications by type

### Key Features

1. **AI-Powered Recommendations**: ML model predicts optimal study hours for exams
2. **Rule-Based Optimization**: 15+ rules automatically adjust schedules
3. **Comprehensive Clash Detection**: 
   - Detects Assignment-Assignment overlaps
   - Detects Exam-Exam overlaps
   - Detects Assignment-Exam conflicts
   - Automatic notification generation
4. **Real-time Notification System**: 
   - Notification icon with unread count
   - Dropdown panel with all notifications
   - Auto-refresh every 30 seconds
   - Mark as read functionality
5. **Separate Assignment and Exam Management**: 
   - Dedicated pages for assignments and exams
   - Estimated hours for assignments (user-provided)
   - ML-predicted hours for exams
6. **Category-based Study Plans**: 
   - Study plans show category (assignment/exam)
   - Different time allocation strategies
   - Clear distinction in weekly view
7. **Priority Management**: Automatically prioritizes based on deadlines and urgency
8. **Flexible Rescheduling**: Easy to regenerate plans with new parameters
9. **Reminders**: Active reminders for upcoming exams and assignments
10. **Responsive UI**: Modern, mobile-friendly interface
11. **Real-time Updates**: Automatic refresh of data and notifications

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
- `recommended_hours`: Calculated based on difficulty (easy: 2h, medium: 4h, hard: 6h)
- `past_assignments`: Text field for past assignment information
- `questionnaire_results`: Text field for questionnaire/assessment results
- `created_at`: Timestamp

**Note**: Subjects are simplified to focus on core information. Assignments and exams are managed separately and linked via subject_name.

### Assignments Table
- `id`: Primary key
- `name`: Assignment name
- `subject_name`: Subject name
- `due_date`: Due date (YYYY-MM-DD)
- `estimated_hours`: User-estimated hours needed
- `difficulty`: easy/medium/hard
- `priority`: urgent/high/medium/low (auto-calculated)
- `status`: pending/in_progress/completed
- `created_at`: Timestamp

### Exams Table
- `id`: Primary key
- `name`: Exam name
- `subject_name`: Subject name
- `exam_date`: Exam date (YYYY-MM-DD)
- `difficulty`: easy/medium/hard
- `past_score`: Previous score (0-100)
- `chapters`: Number of chapters
- `recommended_hours`: ML-predicted hours
- `priority`: urgent/high/medium/low (auto-calculated)
- `created_at`: Timestamp

### StudyPlans Table
- `id`: Primary key
- `item_id`: ID of assignment or exam
- `item_type`: "assignment" or "exam"
- `item_name`: Name of the assignment or exam
- `day`: Day of week
- `time_slot`: Time range (e.g., "09:00-10:00")
- `hours`: Hours allocated
- `category`: "assignment" or "exam"
- `subject_name`: Subject name (retrieved from assignment/exam)
- `created_at`: Timestamp

### Notifications Table
- `id`: Primary key
- `type`: Notification type (clash/reminder/warning)
- `title`: Notification title
- `message`: Notification message
- `item_type`: "assignment", "exam", or "both"
- `item_ids`: Comma-separated IDs of related items
- `is_read`: Boolean flag
- `created_at`: Timestamp

### Reminders Table
- `id`: Primary key
- `subject_id`: Foreign key to subjects
- `message`: Reminder message
- `reminder_date`: Date for reminder
- `is_read`: Boolean flag
- `created_at`: Timestamp

## Recent Enhancements (Latest Update)

1. **Simplified Subject Management**: 
   - Subjects now store only essential information: name, difficulty, recommended hours, past assignments, and questionnaire results
   - Removed exam_date, past_score, chapters, has_assignment, has_exam, and last_week_hours from subjects
   - Recommended hours calculated based on difficulty (easy: 2h, medium: 4h, hard: 6h)
   - Subjects serve as reference entities for assignments and exams

2. **Subject Dropdown in Assignments and Exams**:
   - Assignment and Exam forms now include subject dropdown selection
   - Users select from registered subjects when creating assignments/exams
   - Ensures consistency and proper linking between subjects and their assignments/exams

3. **Enhanced View Plan Functionality**:
   - Fixed study plan loading issue
   - Study plans now correctly display subject names from linked assignments/exams
   - Improved data retrieval and display

4. **Separate Assignment and Exam Management**: 
   - Dedicated database models and API endpoints
   - Separate UI pages for managing assignments and exams
   - Different time allocation strategies for each type

5. **Enhanced Clash Detection**:
   - Comprehensive detection of all overlap scenarios
   - Assignment-Assignment, Exam-Exam, and Assignment-Exam conflicts
   - Automatic notification generation

6. **Real-time Notification System**:
   - Notification icon with unread count badge
   - Dropdown panel with all notifications
   - Auto-refresh and mark-as-read functionality

7. **Estimated Hours for Assignments**:
   - User-provided estimated hours field
   - Better time allocation for assignment-based work

8. **Category-based Study Plans**:
   - Study plans now include category column
   - Clear distinction between assignments and exams in schedule

## Future Enhancements

1. **Advanced ML Models**: Implement more sophisticated models (Random Forest, Neural Networks)
2. **User Feedback Loop**: Allow users to rate predictions and retrain model
3. **Calendar Integration**: Sync with Google Calendar, Outlook
4. **Mobile App**: Native mobile applications
5. **Collaborative Planning**: Share plans with study groups
6. **Analytics Dashboard**: Track study patterns and performance
7. **Adaptive Learning**: Learn from user behavior over time
8. **Push Notifications**: Browser push notifications for important alerts
9. **Export Features**: Export plans to PDF, CSV
10. **Multi-language Support**: Internationalization
11. **Assignment Templates**: Pre-defined assignment types with default estimated hours
12. **Study Session Tracking**: Track actual time spent vs. estimated time

## Conclusion

The Intelligent Study Planner successfully addresses the problem of inefficient study scheduling by combining rule-based logic, machine learning, and intelligent algorithms. The system automatically optimizes study schedules based on multiple factors, detects conflicts comprehensively, and provides a user-friendly interface for managing academic workload.

### Key Achievements

1. **Comprehensive Conflict Management**: The system now detects and notifies users about all types of scheduling conflicts (assignment-assignment, exam-exam, assignment-exam), providing proactive conflict resolution.

2. **Separate Management of Assignments and Exams**: By distinguishing between assignments and exams, the system can apply different time allocation strategies - user-estimated hours for assignments and ML-predicted hours for exams.

3. **Real-time Notification System**: Users are immediately informed about conflicts and important deadlines through an intuitive notification system with visual indicators.

4. **Enhanced User Experience**: Separate pages for assignments and exams, along with category-based study plans, provide clear organization and better visibility into the study schedule.

The implementation demonstrates:
- Effective use of AI/ML for prediction
- Comprehensive rule-based optimization
- Proactive conflict detection and notification
- Modern web development practices
- Scalable architecture with separate models for different entity types
- User-centric design with real-time feedback

The project provides a solid foundation for further enhancements and can be extended to support more advanced features and larger user bases. The recent updates significantly improve the system's ability to handle complex academic scheduling scenarios with multiple types of deadlines and commitments.

