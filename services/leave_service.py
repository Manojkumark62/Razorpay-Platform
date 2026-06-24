from sqlalchemy.orm import Session
from models.leave_model import LeaveRequest

def apply_leave(db: Session, payload):
    leave = LeaveRequest(**payload.model_dump())
    db.add(leave)
    db.commit()
    db.refresh(leave)
    return leave

def get_leave(db: Session, leave_id: int):
    return (db.query(LeaveRequest).filter(LeaveRequest.id == leave_id).first())

def approve_leave(db: Session, leave_id: int):
    leave = get_leave(db, leave_id)
    if not leave:
        return None
    leave.status = "APPROVED"
    db.commit()
    return leave

def reject_leave(db: Session, leave_id: int):
    leave = get_leave(db, leave_id)
    if not leave:
        return None
    leave.status = "REJECTED"
    db.commit()
    return leave

def employee_leave_history(db: Session, employee_id: int):
    return (db.query(LeaveRequest).filter(LeaveRequest.employee_id == employee_id).all())