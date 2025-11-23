# Intelligent Study Planner

An AI-powered study planner that uses machine learning and rule-based logic to suggest optimal study schedules based on deadlines, subject difficulty, and available time.

## Features

- 🤖 **AI-Powered Predictions**: ML model predicts optimal study hours
- 📋 **Rule-Based Optimization**: 15+ intelligent rules for scheduling
- ⚠️ **Clash Detection**: Automatically detects and warns about conflicts
- 🎯 **Priority Management**: Smart prioritization based on deadlines
- 🔄 **Flexible Rescheduling**: Easy plan regeneration
- 📱 **Modern UI**: Beautiful, responsive interface
- 🔔 **Reminders**: Active reminders for upcoming exams

## Tech Stack

- **Frontend**: React + Vite
- **Backend**: FastAPI (Python)
- **Database**: SQLite
- **ML**: scikit-learn (Linear Regression)

## Project Structure

```
study-planner/
├── study-planner-backend/     # FastAPI backend
│   ├── app/
│   │   ├── main.py           # FastAPI app entry point
│   │   ├── models/           # Database models
│   │   ├── routers/          # API routes
│   │   ├── services/         # Business logic (rules, ML, scheduler)
│   │   ├── schemas/          # Pydantic schemas
│   │   └── utils/            # Utility functions
│   └── requirements.txt
│
└── study-planner-frontend/    # React frontend
    ├── src/
    │   ├── components/        # React components
    │   ├── pages/            # Page components
    │   ├── api/              # API client functions
    │   ├── hooks/            # Custom React hooks
    │   └── utils/            # Helper functions
    └── package.json
```

## Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

## Installation & Setup

### Backend Setup

1. Navigate to the backend directory:
```bash
cd study-planner-backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Train the ML model (optional, will auto-train on first use):
```bash
python -c "from app.services.ml_model import train_model; train_model()"
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd study-planner-frontend
```

2. Install dependencies:
```bash
npm install
```

## Running the Application

### Step 1: Start the Backend

From the `study-planner-backend` directory:

```bash
# Activate virtual environment (if not already activated)
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run the FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at `http://localhost:8000`

API documentation (Swagger UI) will be available at `http://localhost:8000/docs`

### Step 2: Start the Frontend

From the `study-planner-frontend` directory (in a new terminal):

```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Usage Guide

### 1. Add Subjects

1. Navigate to "Add Subjects" page
2. Fill in the form:
   - Subject Name
   - Difficulty (Easy/Medium/Hard)
   - Exam Date
   - Past Score (0-100)
   - Number of Chapters
   - Other optional fields
3. Click "Save Subject"

The ML model will automatically predict recommended study hours based on your inputs.

### 2. Generate Study Plan

1. Navigate to "Generate Plan" page
2. Enter your availability:
   - Available hours per day
   - Start date
   - End date
3. Click "Generate Study Plan"

The system will:
- Apply 15+ rules to optimize the schedule
- Detect any clashes
- Allocate time slots efficiently
- Prioritize urgent subjects

### 3. View Study Plan

1. Navigate to "View Plan" page
2. See your weekly schedule with:
   - Day-by-day breakdown
   - Time slots
   - Subject assignments
   - Hours allocated

### 4. Dashboard

The dashboard provides:
- Overview statistics
- Recent subjects
- Active reminders
- Quick access to all features

### 5. Settings

- Train/retrain the ML model
- View command interface documentation
- Learn about the system

## Command Interface

You can interact with the planner using these commands (via UI buttons):

- **Add Subject**: Navigate to add subjects page
- **Generate Plan**: Create a new study schedule
- **View Plan**: View current schedule
- **Clear Plan**: Remove existing plan

## API Endpoints

### Subjects
- `GET /api/subjects` - Get all subjects
- `POST /api/subjects` - Create subject
- `GET /api/subjects/{id}` - Get subject by ID
- `PUT /api/subjects/{id}` - Update subject
- `DELETE /api/subjects/{id}` - Delete subject
- `GET /api/subjects/reminders/active` - Get active reminders

### Planner
- `POST /api/planner/generate` - Generate study plan
- `GET /api/planner/weekly` - Get weekly plan
- `DELETE /api/planner/clear` - Clear all plans

### ML
- `POST /api/ml/train` - Train ML model
- `POST /api/ml/predict` - Predict study hours

## Database

The application uses SQLite database (`study_planner.db`) which is automatically created in the backend directory on first run.

## Troubleshooting

### Backend Issues

1. **Port 8000 already in use**:
   ```bash
   # Change port in app/main.py or use:
   uvicorn app.main:app --reload --port 8001
   ```

2. **Module not found errors**:
   - Ensure you're in the `study-planner-backend` directory
   - Activate virtual environment
   - Reinstall requirements: `pip install -r requirements.txt`

3. **Database errors**:
   - Delete `study_planner.db` to reset database
   - The database will be recreated on next run

### Frontend Issues

1. **Port 3000 already in use**:
   - Vite will automatically use the next available port
   - Or change port in `vite.config.js`

2. **API connection errors**:
   - Ensure backend is running on port 8000
   - Check CORS settings in `app/main.py`
   - Verify API_BASE_URL in frontend API files

3. **Module not found**:
   ```bash
   # Reinstall dependencies
   rm -rf node_modules package-lock.json
   npm install
   ```

## Development

### Backend Development

- The backend uses FastAPI with auto-reload enabled
- Changes to Python files will automatically restart the server
- Check `http://localhost:8000/docs` for API documentation

### Frontend Development

- Frontend uses Vite with hot module replacement
- Changes to React files will automatically update in browser
- Check browser console for errors

## Testing

### Test Backend API

Visit `http://localhost:8000/docs` for interactive API documentation where you can test all endpoints.

### Test ML Model

```bash
# In Python shell
from app.services.ml_model import predict_hours
hours = predict_hours(past_score=65, difficulty="medium", chapters=8, days_left=10)
print(f"Predicted hours: {hours}")
```

## License

This project is open source and available for educational purposes.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Support

For issues or questions, please check the troubleshooting section or create an issue in the repository.

