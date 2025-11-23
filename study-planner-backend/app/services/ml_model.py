import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import pickle
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "study_model.pkl")

def create_training_data():
    """Create sample training data if it doesn't exist"""
    data = {
        "past_score": [45, 65, 80, 55, 70, 40, 85, 60, 75, 50, 90, 35, 68, 72, 58],
        "difficulty_level": [2, 1, 0, 2, 1, 2, 0, 1, 0, 2, 0, 2, 1, 1, 2],  # 0=easy, 1=medium, 2=hard
        "chapters": [10, 8, 5, 15, 7, 12, 4, 9, 6, 14, 3, 16, 8, 7, 11],
        "days_left": [5, 10, 20, 3, 15, 7, 25, 12, 18, 4, 30, 2, 14, 16, 8],
        "recommended_hours": [4, 3, 2, 5, 2.5, 5, 1.5, 3.5, 2, 5.5, 1, 6, 3, 2.5, 4.5]
    }
    df = pd.DataFrame(data)
    return df

def train_model():
    """Train the ML model"""
    # Check if training data file exists
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    training_file = os.path.join(base_dir, "app", "data", "ml_training_data.csv")
    
    if os.path.exists(training_file):
        data = pd.read_csv(training_file)
    else:
        # Create sample data
        data = create_training_data()
        os.makedirs(os.path.dirname(training_file), exist_ok=True)
        data.to_csv(training_file, index=False)
    
    # Prepare features
    X = data[["past_score", "difficulty_level", "chapters", "days_left"]]
    y = data["recommended_hours"]
    
    # Train model
    model = LinearRegression()
    model.fit(X, y)
    
    # Save model
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    
    return "Model trained successfully!"

def load_model():
    """Load the trained model"""
    if not os.path.exists(MODEL_PATH):
        train_model()
    
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    return model

def predict_hours(past_score: float, difficulty: str, chapters: int, days_left: int) -> float:
    """
    Predict recommended study hours based on features
    """
    # Convert difficulty to numeric
    difficulty_map = {"easy": 0, "medium": 1, "hard": 2}
    difficulty_level = difficulty_map.get(difficulty.lower(), 1)
    
    # Load model
    model = load_model()
    
    # Make prediction
    features = np.array([[past_score, difficulty_level, chapters, days_left]])
    prediction = model.predict(features)
    
    # Ensure minimum 1 hour
    return max(1.0, round(float(prediction[0]), 2))

def update_model_with_feedback(past_score: float, difficulty: str, chapters: int, 
                               days_left: int, actual_hours: float):
    """Update model with user feedback (optional enhancement)"""
    # This would append to training data and retrain
    # For now, just a placeholder
    pass

