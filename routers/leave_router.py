from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from core.database import get_db
from core.permission import require_roles
from models.leave_model import LeaveRequest
from schemas.leave_schema import LeaveCreate
from services.notification_service import create_notification

router = APIRouter(prefix="/leaves", tags=["Leaves"], dependencies=[Depends(require_roles("EMPLOYEE", "ADMIN", "SUPER_ADMIN", "HR", "MANAGER"))])


@router.post("/")
def apply_leave(payload: LeaveCreate, db: Session = Depends(get_db)):
    leave = LeaveRequest(**payload.model_dump())
    db.add(leave)
    db.commit()
    return {"message": "Leave Applied", "id": leave.id}


@router.get("/")
def get_all_leaves(db: Session = Depends(get_db)):
    return db.query(LeaveRequest).all()


@router.get("/employee/{employee_id}")
def get_employee_leaves(employee_id: int, db: Session = Depends(get_db)):
    return db.query(LeaveRequest).filter(LeaveRequest.employee_id == employee_id).all()


@router.put("/approve/{leave_id}")
def approve_leave(leave_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    leave = db.query(LeaveRequest).filter(LeaveRequest.id == leave_id).first()
    if not leave:
        raise HTTPException(status_code=404, detail="Leave request not found")
    leave.status = "APPROVED"
    db.commit()
    background_tasks.add_task(
        create_notification, db, leave.employee_id,
        "Leave Approved", "Your leave request was approved"
    )
    return {"message": "Leave Approved"}


@router.put("/reject/{leave_id}")
def reject_leave(leave_id: int, db: Session = Depends(get_db)):
    leave = db.query(LeaveRequest).filter(LeaveRequest.id == leave_id).first()
    if not leave:
        raise HTTPException(status_code=404, detail="Leave request not found")
    if leave.status == "APPROVED":
        return {"message": "This leave is already approved and cannot be rejected"}
    leave.status = "REJECTED"
    db.commit()
    return {"message": "Leave Rejected"}