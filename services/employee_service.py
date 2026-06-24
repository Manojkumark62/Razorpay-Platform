from sqlalchemy.orm import Session
from sqlalchemy import or_
from models.employee_model import Employee


def create_employee(db: Session, payload):
    employee = Employee(**payload.model_dump())
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


def get_employee(db: Session, employee_id: int):
    return db.query(Employee).filter(
        Employee.id == employee_id, Employee.is_deleted == False
    ).first()


def get_employees(db: Session):
    return db.query(Employee).filter(Employee.is_deleted == False).all()


def update_employee(db: Session, employee_id: int, payload):
    employee = get_employee(db, employee_id)
    if not employee:
        return None
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(employee, key, value)
    db.commit()
    db.refresh(employee)
    return employee


def delete_employee(db: Session, employee_id: int):
    from datetime import datetime, timezone
    employee = get_employee(db, employee_id)
    if not employee:
        return False
    employee.is_deleted = True
    employee.deleted_at = datetime.now(timezone.utc).replace(tzinfo=None)
    db.commit()
    return True


def search_employees(db: Session, keyword: str):
    return db.query(Employee).filter(
        Employee.is_deleted == False,
        or_(
            Employee.first_name.ilike(f"%{keyword}%"),
            Employee.last_name.ilike(f"%{keyword}%"),
            Employee.email.ilike(f"%{keyword}%"),
        )
    ).all()


def get_employees_paginated(db: Session, page: int, size: int):
    offset = (page - 1) * size
    return db.query(Employee).filter(Employee.is_deleted == False).offset(offset).limit(size).all()


def filter_by_department(db: Session, department_id: int):
    return db.query(Employee).filter(
        Employee.department_id == department_id,
        Employee.is_deleted == False
    ).all()


def filter_by_designation(db: Session, designation_id: int):
    return db.query(Employee).filter(
        Employee.designation_id == designation_id,
        Employee.is_deleted == False
    ).all()


def employee_statistics(db: Session):
    # FIX: Employee model has no is_active column - use is_deleted
    total = db.query(Employee).count()
    active = db.query(Employee).filter(Employee.is_deleted == False).count()
    deleted = db.query(Employee).filter(Employee.is_deleted == True).count()
    return {"total_employees": total, "active_employees": active, "deleted_employees": deleted}
