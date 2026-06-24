from sqlalchemy.orm import Session
from models.notification_model import Notification

def create_notification(db: Session, user_id: int, title: str, message: str):
    notification = Notification(user_id=user_id, title=title, message=message)
    db.add(notification)
    db.commit()