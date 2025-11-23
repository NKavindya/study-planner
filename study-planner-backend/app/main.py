from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models.database import init_db
from app.routers import subjects, planner, ml, assignments, exams, notifications

app = FastAPI(title="Study Planner API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
@app.on_event("startup")
def startup_event():
    init_db()

# Include routers
app.include_router(subjects.router)
app.include_router(planner.router)
app.include_router(ml.router)
app.include_router(assignments.router)
app.include_router(exams.router)
app.include_router(notifications.router)

@app.get("/")
def root():
    return {
        "message": "Study Planner API",
        "version": "1.0.0",
        "endpoints": {
            "subjects": "/api/subjects",
            "planner": "/api/planner",
            "ml": "/api/ml"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

