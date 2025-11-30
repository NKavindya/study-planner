from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.database import get_db
from app.models import notification as notification_model
from app.schemas import notification_schema
from app.services.clash_detector import detect_all_clashes

router = APIRouter(prefix="/api/notifications", tags=["notifications"])

@router.get("/", response_model=List[notification_schema.NotificationResponse])
def get_notifications(unread_only: bool = False, db: Session = Depends(get_db)):
    """Get all notifications"""
    notifications = notification_model.get_all_notifications(db, unread_only=unread_only)
    return notifications

@router.get("/unread/count")
def get_unread_count(db: Session = Depends(get_db)):
    """Get count of unread notifications"""
    notifications = notification_model.get_all_notifications(db, unread_only=True)
    return {"count": len(notifications)}

@router.post("/{notification_id}/read")
def mark_notification_read(notification_id: int, db: Session = Depends(get_db)):
    """Mark a notification as read"""
    notification = notification_model.mark_notification_read(db, notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return {"message": "Notification marked as read"}

@router.post("/read-all")
def mark_all_notifications_read(db: Session = Depends(get_db)):
    """Mark all notifications as read"""
    result = notification_model.mark_all_notifications_read(db)
    return result

@router.delete("/{notification_id}")
def delete_notification(notification_id: int, db: Session = Depends(get_db)):
    """Delete a notification"""
    notification = notification_model.delete_notification(db, notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return {"message": "Notification deleted successfully"}

@router.post("/detect-clashes")
def detect_clashes_endpoint(db: Session = Depends(get_db)):
    """Manually trigger clash detection"""
    clashes = detect_all_clashes(db)
    return {
        "message": "Clash detection completed",
        "clashes_found": len(clashes)
    }

