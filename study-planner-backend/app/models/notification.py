from sqlalchemy.orm import Session
from app.models.database import Notification

def create_notification(db: Session, notification_data: dict):
    notification = Notification(**notification_data)
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification

def get_notification(db: Session, notification_id: int):
    return db.query(Notification).filter(Notification.id == notification_id).first()

def get_all_notifications(db: Session, unread_only: bool = False):
    query = db.query(Notification)
    if unread_only:
        query = query.filter(Notification.is_read == False)
    return query.order_by(Notification.created_at.desc()).all()

def mark_notification_read(db: Session, notification_id: int):
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if notification:
        notification.is_read = True
        db.commit()
        db.refresh(notification)
    return notification

def mark_all_notifications_read(db: Session):
    db.query(Notification).update({"is_read": True})
    db.commit()
    return {"message": "All notifications marked as read"}

def delete_notification(db: Session, notification_id: int):
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if notification:
        db.delete(notification)
        db.commit()
    return notification


