from fastapi import APIRouter
from app.services.ml_model import train_model, predict_hours

router = APIRouter(prefix="/api/ml", tags=["ml"])

@router.post("/train")
def train_ml_model():
    """Train the ML model"""
    result = train_model()
    return {"message": result}

@router.post("/predict")
def predict_study_hours(past_score: float, difficulty: str, chapters: int, days_left: int):
    """Predict recommended study hours"""
    hours = predict_hours(past_score, difficulty, chapters, days_left)
    return {
        "predicted_hours": hours,
        "inputs": {
            "past_score": past_score,
            "difficulty": difficulty,
            "chapters": chapters,
            "days_left": days_left
        }
    }

