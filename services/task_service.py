from sqlalchemy.orm import Session
from models.task_model import Task

def create_task(db: Session, payload):
    task = Task(**payload.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_task(db: Session, task_id: int):
    return (db.query(Task).filter(Task.id == task_id).first())

def get_tasks(db: Session):
    return db.query(Task).all()

def update_task_status(db: Session, task_id: int, status: str):
    task = get_task(db, task_id)
    if not task:
        return None
    task.status = status
    db.commit()
    db.refresh(task)
    return task

def employee_tasks(db: Session, employee_id: int):
    return (db.query(Task).filter(Task.employee_id == employee_id).all())

def project_tasks(db: Session, project_id: int):
    return (db.query(Task).filter(Task.project_id == project_id).all())