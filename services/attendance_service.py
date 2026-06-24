from datetime import datetime, date
from sqlalchemy.orm import Session
from models.attendance_model import Attendance

def check_in(db: Session, employee_id: int):
    existing = (db.query(Attendance).filter(Attendance.employee_id == employee_id, Attendance.attendance_date == date.today()).first())
    if existing:
        raise Exception("Already checked in today")
    attendance = Attendance( employee_id=employee_id, attendance_date=date.today(), check_in=datetime.now(), status="PRESENT")
    db.add(attendance)
    db.commit()
    db.refresh(attendance)
    return attendance

def check_out(db: Session, employee_id: int):
    attendance = (db.query(Attendance).filter(Attendance.employee_id == employee_id, Attendance.attendance_date == date.today()).first())
    if not attendance:
        return None
    attendance.check_out = datetime.now()
    db.commit()
    db.refresh(attendance)
    return attendance

def attendance_report(db: Session, employee_id: int):
    return (db.query(Attendance).filter(Attendance.employee_id == employee_id).all())

def monthly_attendance(db: Session, employee_id: int, month: int, year: int):
    return (db.query(Attendance).filter(Attendance.employee_id == employee_id).all())