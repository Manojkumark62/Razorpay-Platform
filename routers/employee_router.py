from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from core.permission import require_roles
from core.response import success_response
from models.employee_model import Employee
from schemas.employee_schema import EmployeeCreate

router = APIRouter(prefix="/employees", tags=["Employees"], dependencies=[Depends(require_roles("ADMIN", "SUPER_ADMIN", "HR", "MANAGER"))])


@router.post("/")
def create_employee(payload: EmployeeCreate, db: Session = Depends(get_db)):
    employee = Employee(**payload.model_dump())
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return success_response(
        "Employee created successfully",
        {
            "id": employee.id,
            "first_name": employee.first_name,
            "last_name": employee.last_name,
            "email": employee.email,
            "department_id": employee.department_id,
            "designation_id": employee.designation_id,
        },
    )


@router.get("/")
def get_employees(db: Session = Depends(get_db)):
    employees = db.query(Employee).filter(Employee.is_deleted == False).all()
    return success_response(
        "Employees retrieved successfully",
        [
            {
                "id": employee.id,
                "first_name": employee.first_name,
                "last_name": employee.last_name,
                "email": employee.email,
                "department_id": employee.department_id,
                "designation_id": employee.designation_id,
            }
            for employee in employees
        ],
    )


@router.get("/search/")
def search_employee(keyword: str, db: Session = Depends(get_db)):
    from sqlalchemy import or_
    employees = db.query(Employee).filter(
        Employee.is_deleted == False,
        or_(
            Employee.first_name.ilike(f"%{keyword}%"),
            Employee.last_name.ilike(f"%{keyword}%"),
            Employee.email.ilike(f"%{keyword}%"),
        )
    ).all()
    return success_response(
        "Employees found successfully",
        [
            {
                "id": employee.id,
                "first_name": employee.first_name,
                "last_name": employee.last_name,
                "email": employee.email,
                "department_id": employee.department_id,
                "designation_id": employee.designation_id,
            }
            for employee in employees
        ],
    )


@router.get("/paginated/")
def get_paginated_employees(page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    skip = (page - 1) * limit
    total = db.query(Employee).filter(Employee.is_deleted == False).count()
    employees = db.query(Employee).filter(Employee.is_deleted == False).offset(skip).limit(limit).all()
    return success_response(
        "Employees retrieved successfully",
        {
            "total": total,
            "page": page,
            "limit": limit,
            "items": [
                {
                    "id": employee.id,
                    "first_name": employee.first_name,
                    "last_name": employee.last_name,
                    "email": employee.email,
                    "department_id": employee.department_id,
                    "designation_id": employee.designation_id,
                }
                for employee in employees
            ],
        },
    )


@router.get("/filter/")
def filter_employee(department_id: int, db: Session = Depends(get_db)):
    employees = db.query(Employee).filter(
        Employee.department_id == department_id,
        Employee.is_deleted == False
    ).all()
    return success_response(
        "Employees filtered successfully",
        [
            {
                "id": employee.id,
                "first_name": employee.first_name,
                "last_name": employee.last_name,
                "email": employee.email,
                "department_id": employee.department_id,
                "designation_id": employee.designation_id,
            }
            for employee in employees
        ],
    )


@router.get("/{employee_id}")
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(
        Employee.id == employee_id, Employee.is_deleted == False
    ).first()
    if not employee:
        return success_response("Employee not found", None)
    return success_response(
        "Employee retrieved successfully",
        {
            "id": employee.id,
            "first_name": employee.first_name,
            "last_name": employee.last_name,
            "email": employee.email,
            "department_id": employee.department_id,
            "designation_id": employee.designation_id,
        },
    )


@router.put("/{employee_id}")
def update_employee(employee_id: int, payload: EmployeeCreate, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(
        Employee.id == employee_id, Employee.is_deleted == False
    ).first()
    if not employee:
        return success_response("Employee not found", None)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(employee, key, value)
    db.commit()
    db.refresh(employee)
    return success_response(
        "Employee updated successfully",
        {
            "id": employee.id,
            "first_name": employee.first_name,
            "last_name": employee.last_name,
            "email": employee.email,
            "department_id": employee.department_id,
            "designation_id": employee.designation_id,
        },
    )


@router.delete("/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    from datetime import datetime, timezone
    employee = db.query(Employee).filter(
        Employee.id == employee_id, Employee.is_deleted == False
    ).first()
    if not employee:
        return success_response("Employee not found", None)
    # Soft delete
    employee.is_deleted = True
    employee.deleted_at = datetime.now(timezone.utc).replace(tzinfo=None)
    db.commit()
    return success_response("Employee deleted successfully", {"id": employee_id})