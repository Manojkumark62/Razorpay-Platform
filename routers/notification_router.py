from fastapi import APIRouter, Depends, HTTPException
from services.email_service import send_email
from sqlalchemy.orm import Session
from core.database import get_db
from core.permission import require_roles
from core.response import success_response
from models.notification_model import Notification

router = APIRouter(prefix="/notifications", tags=["Notifications"], dependencies=[Depends(require_roles("EMPLOYEE", "ADMIN", "SUPER_ADMIN", "HR", "MANAGER"))])


@router.post("/send-email")
async def test_email(email: str):
    try:
        await send_email(email, "Test Mail", "<h1>Email Working</h1>")
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return success_response("Email sent successfully", {"email": email})


@router.get("/{user_id}")
def get_notifications(user_id: int, db: Session = Depends(get_db)):
    return db.query(Notification).filter(Notification.user_id == user_id).all()


@router.put("/{notification_id}/read")
def mark_read(notification_id: int, db: Session = Depends(get_db)):
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    notification.is_read = True
    db.commit()
    return {"message": "Marked as Read"}


@router.put("/mark-all-read/{user_id}")
def mark_all_read(user_id: int, db: Session = Depends(get_db)):
    db.query(Notification).filter(
        Notification.user_id == user_id,
        Notification.is_read == False
    ).update({"is_read": True})
    db.commit()
    return {"message": "All notifications marked as read"}