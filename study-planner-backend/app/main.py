from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.models.database import init_db
from app.routers import subjects, planner, ml, assignments, exams, notifications, admin
import traceback

app = FastAPI(title="Study Planner API", version="1.0.0")

# CORS middleware - must be added before exception handlers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Global exception handler to ensure CORS headers on errors
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"Global exception handler: {exc}")
    traceback.print_exc()
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": f"Internal server error: {str(exc)}"},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
        }
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
app.include_router(admin.router)

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

