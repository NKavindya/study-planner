from datetime import datetime, timedelta

def get_days_until_exam(exam_date_str: str) -> int:
    """Calculate days until exam date"""
    try:
        exam_date = datetime.strptime(exam_date_str, "%Y-%m-%d")
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        days = (exam_date - today).days
        return max(0, days)
    except:
        return 999

def is_weekend(date_str: str) -> bool:
    """Check if a date is weekend"""
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        return date.weekday() >= 5  # Saturday = 5, Sunday = 6
    except:
        return False

def get_date_range(start_date: str, end_date: str) -> list:
    """Get list of dates between start and end"""
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        
        if start > end:
            raise ValueError("Start date must be before or equal to end date")
        
        dates = []
        current = start
        while current <= end:
            dates.append(current.strftime("%Y-%m-%d"))
            current += timedelta(days=1)
        
        if not dates:
            raise ValueError("Date range is invalid")
        
        return dates
    except ValueError as e:
        raise e
    except Exception as e:
        raise ValueError(f"Invalid date format: {str(e)}")

def get_day_name(date_str: str) -> str:
    """Get day name from date string"""
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        return date.strftime("%A")
    except:
        return "Unknown"

