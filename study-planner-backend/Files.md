# Backend Files Documentation

This document provides a comprehensive explanation of all files in the study-planner-backend directory, including their purpose, functionality, and importance in the system architecture.

## Root Directory Files

### `requirements.txt`
**What it is:** Python dependency manifest file
**What it does:** Lists all Python packages and their versions required by the backend application
**Why we need it:** 
- Ensures consistent development environments across different machines
- Allows easy installation of all dependencies with `pip install -r requirements.txt`
- Documents the exact versions of libraries used (FastAPI, SQLAlchemy, scikit-learn, etc.)
- Essential for deployment and reproducibility

**Key Dependencies:**
- `fastapi==0.104.1` - Modern web framework for building APIs
- `uvicorn==0.24.0` - ASGI server to run FastAPI
- `sqlalchemy==2.0.23` - ORM for database operations
- `pydantic==2.5.0` - Data validation and settings management
- `pandas==2.1.3` - Data manipulation for ML training data
- `scikit-learn==1.3.2` - Machine learning library for predictions
- `python-dateutil==2.8.2` - Date parsing and manipulation utilities

### `migrate_db.py`
**What it is:** Database migration utility script
**What it does:** 
- Handles database schema migrations and updates
- Adds new columns to existing tables if needed
- Ensures database schema stays in sync with model definitions
**Why we need it:** 
- Allows adding new fields to existing database tables without losing data
- Maintains backward compatibility when schema changes occur
- Automatically migrates existing databases when new features are added

### `study_planner.db`
**What it is:** SQLite database file
**What it does:** 
- Stores all application data persistently
- Contains tables for subjects, assignments, exams, study plans, notifications, and reminders
**Why we need it:** 
- Provides persistent storage for all user data
- SQLite is lightweight and file-based, perfect for this application
- No separate database server required - simplifies deployment

### `Files.md` (this file)
**What it is:** Documentation file
**What it does:** Documents all backend files and their purposes
**Why we need it:** 
- Helps developers understand the codebase structure
- Serves as a reference guide for maintenance and onboarding
- Explains the purpose and relationships between files

## Application Structure (`app/`)

### `app/__init__.py`
**What it is:** Python package initialization file
**What it does:** 
- Marks the `app` directory as a Python package
- Can contain package-level initialization code
**Why we need it:** 
- Required for Python to recognize `app` as a package
- Allows importing modules using `from app import ...`
- Enables clean module organization

### `app/main.py`
**What it is:** FastAPI application entry point and main configuration file
**What it does:** 
- Creates and configures the FastAPI application instance
- Sets up CORS (Cross-Origin Resource Sharing) middleware for frontend communication
- Registers all API routers (subjects, assignments, exams, planner, etc.)
- Handles global exception handling
- Initializes the database on startup
- Defines the API documentation and metadata
**Why we need it:** 
- Central configuration point for the entire backend application
- CORS middleware is essential for frontend-backend communication
- Global exception handlers ensure consistent error responses
- Database initialization ensures tables exist before the app starts
- This is the file that gets run by uvicorn to start the server

### `app/study_model.pkl`
**What it is:** Serialized (pickled) machine learning model file
**What it does:** 
- Stores the trained Linear Regression model
- Contains the model's learned parameters and weights
**Why we need it:** 
- Persists the ML model so it doesn't need retraining on every server restart
- Allows quick loading of pre-trained model for predictions
- Enables model reuse across application instances

## Models (`app/models/`)

Models define the database structure and provide data access methods.

### `app/models/__init__.py`
**What it is:** Package initialization for models
**What it does:** Makes the models directory a Python package
**Why we need it:** Enables importing models using `from app.models import ...`

### `app/models/database.py`
**What it is:** Database configuration and base model definitions
**What it does:** 
- Defines SQLAlchemy database engine and session management
- Creates base class for all database models
- Defines all database tables as SQLAlchemy ORM models:
  - `Subject` - Stores subject information
  - `Assignment` - Stores assignment details and due dates
  - `Exam` - Stores exam information with ML predictions
  - `StudyPlan` - Stores generated study schedules
  - `Notification` - Stores clash notifications and alerts
  - `Reminder` - Stores reminder messages
- Provides database session dependency injection for FastAPI
- Includes database initialization function
**Why we need it:** 
- Central database configuration file
- All database tables are defined here using ORM approach
- Session management ensures proper database connection handling
- ORM models provide type safety and database abstraction
- Essential for all database operations throughout the application

### `app/models/subject.py`
**What it is:** Subject model with CRUD operations
**What it does:** 
- Provides functions to create, read, update, and delete subjects
- Handles reminder creation and retrieval
- Manages subject data in the database
**Why we need it:** 
- Encapsulates all subject-related database operations
- Separates data access logic from business logic
- Provides reusable functions for subject management
- Makes code more maintainable and testable

### `app/models/assignment.py`
**What it is:** Assignment model with CRUD operations
**What it does:** 
- Provides functions to create, read, update, and delete assignments
- Manages assignment data including due dates, estimated hours, and priorities
**Why we need it:** 
- Encapsulates assignment database operations
- Handles assignment-specific business logic
- Used by assignments router to interact with database
- Maintains separation of concerns

### `app/models/exam.py`
**What it is:** Exam model with CRUD operations
**What it does:** 
- Provides functions to create, read, update, and delete exams
- Manages exam data including exam dates, past scores, chapters, and ML-predicted hours
**Why we need it:** 
- Encapsulates exam database operations
- Handles exam-specific data management
- Used by exams router to interact with database
- Stores ML prediction results for study time recommendations

### `app/models/plan.py`
**What it is:** Study plan model with CRUD operations
**What it does:** 
- Provides functions to create, read, and delete study plans
- Manages generated study schedules with time slots
- Handles clearing all plans when regenerating
**Why we need it:** 
- Manages the generated study schedules
- Stores the output of the scheduling algorithm
- Allows users to view their study plans
- Essential for persisting scheduling results

### `app/models/notification.py`
**What it is:** Notification model with CRUD operations
**What it does:** 
- Provides functions to create, read, update, and delete notifications
- Manages clash detection notifications and alerts
- Handles marking notifications as read
**Why we need it:** 
- Stores and manages all system notifications
- Tracks clash detection alerts
- Provides notification status management
- Used by notification system to alert users about conflicts

## Routers (`app/routers/`)

Routers define the API endpoints that the frontend can call.

### `app/routers/__init__.py`
**What it is:** Package initialization for routers
**What it does:** Makes the routers directory a Python package
**Why we need it:** Enables importing routers in main.py

### `app/routers/subjects.py`
**What it is:** API router for subject-related endpoints
**What it does:** 
- Defines REST API endpoints for subject management:
  - `POST /api/subjects` - Create new subject
  - `GET /api/subjects` - Get all subjects
  - `GET /api/subjects/{id}` - Get specific subject
  - `PUT /api/subjects/{id}` - Update subject
  - `DELETE /api/subjects/{id}` - Delete subject
  - `GET /api/subjects/reminders/active` - Get active reminders
- Handles HTTP requests and responses for subjects
- Converts between database models and API schemas
**Why we need it:** 
- Provides HTTP API interface for frontend to manage subjects
- Validates incoming request data using Pydantic schemas
- Handles errors and returns appropriate HTTP status codes
- RESTful design makes API intuitive to use

### `app/routers/assignments.py`
**What it is:** API router for assignment-related endpoints
**What it does:** 
- Defines REST API endpoints for assignment management:
  - `POST /api/assignments` - Create assignment (triggers clash detection)
  - `GET /api/assignments` - Get all assignments
  - `GET /api/assignments/{id}` - Get specific assignment
  - `PUT /api/assignments/{id}` - Update assignment (triggers clash detection)
  - `DELETE /api/assignments/{id}` - Delete assignment (triggers clash detection)
- Automatically triggers clash detection when assignments are created/updated/deleted
- Generates automatic reminders for upcoming assignments
**Why we need it:** 
- Provides HTTP API interface for assignment management
- Integrates clash detection automatically
- Triggers reminder generation for urgent assignments
- Essential for frontend to manage assignments

### `app/routers/exams.py`
**What it is:** API router for exam-related endpoints
**What it does:** 
- Defines REST API endpoints for exam management:
  - `POST /api/exams` - Create exam (uses ML prediction)
  - `GET /api/exams` - Get all exams
  - `GET /api/exams/{id}` - Get specific exam
  - `PUT /api/exams/{id}` - Update exam (triggers clash detection)
  - `DELETE /api/exams/{id}` - Delete exam (triggers clash detection)
- Automatically calls ML model to predict recommended study hours
- Sets priority based on exam date proximity
- Triggers clash detection and reminder generation
**Why we need it:** 
- Provides HTTP API interface for exam management
- Integrates ML model predictions automatically
- Essential for scenario requirement of ML-based study time prediction
- Handles exam-specific logic (past scores, chapters, etc.)

### `app/routers/planner.py`
**What it is:** API router for study plan generation endpoints
**What it does:** 
- Defines REST API endpoints for study planning:
  - `POST /api/planner/generate` - Generate new study plan
  - `GET /api/planner/weekly` - Get weekly study plan
  - `DELETE /api/planner/clear` - Clear all plans
- Orchestrates the entire study plan generation process:
  - Fetches assignments and exams
  - Calls scheduler service
  - Handles automatic clash detection and rearrangement
  - Generates automatic reminders
  - Saves plans to database
**Why we need it:** 
- Provides HTTP API interface for study plan generation
- Core functionality for the intelligent scheduling feature
- Integrates multiple services (scheduler, clash detector, reminder service)
- Essential for scenario requirement of rule-based scheduling

### `app/routers/notifications.py`
**What it is:** API router for notification endpoints
**What it does:** 
- Defines REST API endpoints for notifications:
  - `GET /api/notifications` - Get all notifications
  - `GET /api/notifications/unread/count` - Get unread count
  - `POST /api/notifications/{id}/read` - Mark as read
  - `POST /api/notifications/read-all` - Mark all as read
  - `DELETE /api/notifications/{id}` - Delete notification
  - `POST /api/notifications/detect-clashes` - Manually trigger clash detection
**Why we need it:** 
- Provides HTTP API interface for notification management
- Allows frontend to display notifications to users
- Tracks read/unread status for notifications
- Essential for clash detection alerts

### `app/routers/ml.py`
**What it is:** API router for machine learning endpoints
**What it does:** 
- Defines REST API endpoints for ML operations:
  - `POST /api/ml/train` - Train the ML model
  - `POST /api/ml/predict` - Predict study hours for given inputs
- Allows manual model training and prediction testing
**Why we need it:** 
- Provides HTTP API interface for ML model operations
- Allows administrators to retrain the model
- Useful for testing predictions
- Supports scenario requirement of ML-based predictions

### `app/routers/admin.py`
**What it is:** API router for administrative operations
**What it does:** 
- Defines admin endpoints for system management:
  - `DELETE /api/admin/clear-all` - Clear all data (testing/debugging)
- Provides utility functions for system administration
**Why we need it:** 
- Useful for testing and development
- Allows resetting the entire database
- Can be extended for future admin features

## Schemas (`app/schemas/`)

Schemas define the data structures for API requests and responses using Pydantic.

### `app/schemas/__init__.py`
**What it is:** Package initialization for schemas
**What it does:** Makes the schemas directory a Python package
**Why we need it:** Enables importing schemas in routers

### `app/schemas/subject_schema.py`
**What it is:** Pydantic schemas for subject API data validation
**What it does:** 
- Defines `SubjectCreate` - Schema for creating subjects
- Defines `SubjectResponse` - Schema for subject API responses
- Defines `ReminderResponse` - Schema for reminder responses
- Validates data types and required fields
**Why we need it:** 
- Ensures data integrity at API boundaries
- Automatically validates request data before processing
- Provides clear error messages for invalid data
- Type safety for API requests/responses

### `app/schemas/assignment_schema.py`
**What it is:** Pydantic schemas for assignment API data validation
**What it does:** 
- Defines `AssignmentCreate` - Schema for creating assignments
- Defines `AssignmentResponse` - Schema for assignment API responses
- Validates assignment data (name, due date, hours, etc.)
**Why we need it:** 
- Validates assignment data before database operations
- Ensures required fields are present
- Type safety and data validation

### `app/schemas/exam_schema.py`
**What it is:** Pydantic schemas for exam API data validation
**What it does:** 
- Defines `ExamCreate` - Schema for creating exams
- Defines `ExamResponse` - Schema for exam API responses
- Validates exam data (name, exam date, past score, chapters, etc.)
**Why we need it:** 
- Validates exam data before ML prediction
- Ensures required fields for ML features are present
- Type safety for exam-related API calls

### `app/schemas/plan_schema.py`
**What it is:** Pydantic schemas for study plan API data validation
**What it does:** 
- Defines `GeneratePlanRequest` - Schema for plan generation requests
- Defines plan response schemas
- Validates plan generation parameters (hours per day, start date, etc.)
**Why we need it:** 
- Validates plan generation parameters
- Ensures required scheduling inputs are provided
- Type safety for planning operations

### `app/schemas/notification_schema.py`
**What it is:** Pydantic schemas for notification API data validation
**What it does:** 
- Defines notification request and response schemas
- Validates notification data structures
**Why we need it:** 
- Validates notification data
- Ensures proper notification structure
- Type safety for notification operations

## Services (`app/services/`)

Services contain the core business logic and algorithms.

### `app/services/__init__.py`
**What it is:** Package initialization for services
**What it does:** Makes the services directory a Python package
**Why we need it:** Enables importing services in routers

### `app/services/rules_engine.py`
**What it is:** Rule-based logic engine for intelligent scheduling
**What it does:** 
- Implements 15+ intelligent rules that adjust study recommendations:
  - Difficulty-based adjustments (hard +2h, medium +1h)
  - Deadline-based priorities (urgent within 3 days, high within 7 days)
  - Performance-based adjustments (low score +2h, high score -1h)
  - Chapter-based adjustments (many chapters +1h)
- Applies rules to subjects/exams/assignments to optimize scheduling
- Detects basic clashes between subjects
**Why we need it:** 
- Core logic for intelligent scheduling
- Implements rule-based AI as required by the scenario
- Automatically adjusts study time based on multiple factors
- Provides adaptive scheduling recommendations

### `app/services/clash_detector.py`
**What it is:** Comprehensive clash detection system
**What it does:** 
- Detects all types of scheduling conflicts:
  - Assignment-Assignment overlaps (same due date or within 1 day)
  - Exam-Exam overlaps (same exam date)
  - Assignment-Exam conflicts (same date or within 1 day)
- Creates automatic notifications for detected clashes
- Provides clash summaries
- Prevents duplicate notifications
**Why we need it:** 
- Essential for scenario requirement of clash detection
- Proactively identifies scheduling problems
- Notifies users about conflicts automatically
- Prevents duplicate notification spam

### `app/services/scheduler.py`
**What it is:** Intelligent study plan generation engine
**What it does:** 
- **Core Function**: `generate_study_plan()` - Generates optimized study schedules
- **Clash Handling**: `detect_and_handle_clashes()` - Automatically rearranges when clashes detected
- Implements deadline-aware scheduling:
  - Assignments must be scheduled before due dates
  - Exams should be scheduled before exam dates
- Automatically rearranges study slots when overlaps are detected
- Distributes study load evenly across available days
- Allocates time slots based on user availability
- Compresses schedules if insufficient time available
- Applies priority-based sorting
**Why we need it:** 
- Core functionality for study plan generation
- Implements automatic clash rearrangement as required by scenario
- Uses ML predictions for exam study time
- Distributes workload intelligently
- Essential for the entire scheduling feature

### `app/services/ml_model.py`
**What it is:** Machine learning model service for study time prediction
**What it does:** 
- Trains a Linear Regression model on historical data
- Predicts recommended study hours based on:
  - Past score (0-100)
  - Difficulty level (easy/medium/hard)
  - Number of chapters
  - Days left until exam
- Saves and loads the trained model
- Creates training data if it doesn't exist
- Returns predictions with minimum 1 hour guarantee
**Why we need it:** 
- Implements ML-based prediction as required by scenario
- Predicts which subjects need more study time based on past performance
- Provides data-driven study time recommendations
- Can be improved with more training data over time

### `app/services/reminder_service.py`
**What it is:** Automatic reminder generation service
**What it does:** 
- Automatically generates reminders for:
  - Assignments due within 3 days
  - Exams within 7 days (urgent for exams within 3 days)
- Creates reminder messages with appropriate urgency indicators
- Prevents duplicate reminders
- Stores reminders in database
**Why we need it:** 
- Implements automatic reminder generation as required by scenario
- Proactively alerts users about upcoming deadlines
- Essential for the reminder and notification system
- Helps students stay on top of their schedules

## Utils (`app/utils/`)

Utility functions for common operations.

### `app/utils/__init__.py`
**What it is:** Package initialization for utils
**What it does:** Makes the utils directory a Python package
**Why we need it:** Enables importing utility functions

### `app/utils/date_utils.py`
**What it is:** Date manipulation and calculation utilities
**What it does:** 
- Calculates days until exam/deadline
- Generates date ranges for scheduling
- Determines day names from dates
- Handles date parsing and formatting
- Checks if dates are weekends
**Why we need it:** 
- Centralizes all date-related operations
- Ensures consistent date handling throughout the application
- Reduces code duplication
- Handles timezone and date calculations reliably

### `app/utils/db_utils.py`
**What it is:** Database utility functions
**What it does:** 
- Provides helper functions for database operations
- May include migration utilities
- Database connection helpers
**Why we need it:** 
- Common database operations in one place
- Reduces code duplication
- Provides reusable database utilities

### `app/utils/priority_utils.py`
**What it is:** Priority calculation utilities
**What it does:** 
- Calculates priority levels based on deadlines
- Determines urgency based on days until deadline
- Provides priority mapping functions
**Why we need it:** 
- Centralizes priority calculation logic
- Ensures consistent priority assignment
- Reusable priority determination functions

## Data Directory (`app/data/`)

### `app/data/ml_training_data.csv`
**What it is:** CSV file containing training data for the ML model
**What it does:** 
- Stores historical examples used to train the Linear Regression model
- Contains features (past_score, difficulty_level, chapters, days_left) and labels (recommended_hours)
**Why we need it:** 
- Provides training data for the ML model
- Can be expanded with real user data to improve predictions
- Allows the model to learn from examples
- Essential for ML functionality

## Virtual Environment (`venv/`)

### `venv/`
**What it is:** Python virtual environment directory
**What it does:** 
- Contains isolated Python interpreter and installed packages
- Separates project dependencies from system Python
**Why we need it:** 
- Prevents dependency conflicts between projects
- Ensures consistent environment across development and deployment
- Contains all installed packages listed in requirements.txt
- Should NOT be committed to version control (typically in .gitignore)

## Summary

The backend is organized following a clean architecture pattern:
- **Models**: Database structure and data access
- **Routers**: HTTP API endpoints
- **Schemas**: Data validation
- **Services**: Core business logic (scheduling, ML, clash detection)
- **Utils**: Reusable helper functions

This separation of concerns makes the codebase maintainable, testable, and scalable.

