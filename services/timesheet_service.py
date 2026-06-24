from sqlalchemy.orm import Session
from models.timesheet_model import Timesheet

def create_timesheet(db: Session, payload):
    timesheet = Timesheet(**payload.model_dump())
    db.add(timesheet)
    db.commit()
    db.refresh(timesheet)
    return timesheet

def get_timesheet(db: Session, timesheet_id: int):
    return (db.query(Timesheet).filter(Timesheet.id == timesheet_id).first())

def employee_timesheets(db: Session, employee_id: int):
    return (db.query(Timesheet).filter(Timesheet.employee_id == employee_id).all())

def project_timesheets(db: Session, project_id: int):
    return (db.query(Timesheet).filter(Timesheet.project_id == project_id).all())

def total_hours(db: Session, employee_id: int):
    sheets = employee_timesheets(db, employee_id)
    return sum(item.hours_worked for item in sheets)