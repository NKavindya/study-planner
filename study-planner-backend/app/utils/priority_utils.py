def calculate_priority(difficulty: str, days_until_exam: int, past_score: float) -> str:
    """Calculate priority based on multiple factors"""
    if days_until_exam <= 3:
        return "urgent"
    elif days_until_exam <= 7:
        return "high"
    elif days_until_exam > 30:
        return "low"
    elif difficulty == "hard" and past_score < 50:
        return "high"
    else:
        return "medium"

