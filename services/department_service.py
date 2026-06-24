from sqlalchemy.orm import Session
from models.department_model import Department

def create_department(db: Session, name: str, description: str = None):
    department = Department(name=name, description=description)
    db.add(department)
    db.commit()
    db.refresh(department)
    return department

def get_departments(db: Session):
    return db.query(Department).all()

def get_department(db: Session, department_id: int):
    return (db.query(Department).filter(Department.id == department_id).first())

def update_department(db: Session, department_id: int, data):
    department = get_department(db, department_id)
    if not department:
        return None
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(department, key, value)
    db.commit()
    db.refresh(department)
    return department

def delete_department(db: Session, department_id: int):
    department = get_department(db, department_id)
    if not department:
        return False
    db.delete(department)
    db.commit()
    return True