# Quick Start Guide

## Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

## Quick Setup (5 minutes)

### 1. Backend Setup
```bash
cd study-planner-backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Frontend Setup
```bash
cd ../study-planner-frontend
npm install
```

### 3. Run the Application

**Terminal 1 - Backend:**
```bash
cd study-planner-backend
source venv/bin/activate  # Windows: venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd study-planner-frontend
npm run dev
```

### 4. Access the Application
- Frontend: http://localhost:3000
- Backend API Docs: http://localhost:8000/docs

## First Steps

1. **Add Subjects**: Go to "Add Subjects" and add your courses
2. **Generate Plan**: Go to "Generate Plan" and create your schedule
3. **View Plan**: Check "View Plan" to see your weekly schedule

That's it! You're ready to use the Intelligent Study Planner.

