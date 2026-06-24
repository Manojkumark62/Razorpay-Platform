from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from core.permission import require_roles
from models.department_model import Department
from schemas.department_schema import DepartmentCreate

router = APIRouter(prefix="/departments", tags=["Departments"], dependencies=[Depends(require_roles("ADMIN", "SUPER_ADMIN", "HR", "MANAGER"))])


@router.post("/")
def create_department(payload: DepartmentCreate, db: Session = Depends(get_db)):
    existing = db.query(Department).filter(Department.name == payload.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Department already exists")
    department = Department(name=payload.name, description=payload.description)
    db.add(department)
    db.commit()
    return {"message": "Department Created", "id": department.id}


@router.get("/")
def get_departments(db: Session = Depends(get_db)):
    return db.query(Department).all()


@router.get("/{department_id}")
def get_department(department_id: int, db: Session = Depends(get_db)):
    department = db.query(Department).filter(Department.id == department_id).first()
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return department


@router.put("/{department_id}")
def update_department(department_id: int, payload: DepartmentCreate, db: Session = Depends(get_db)):
    department = db.query(Department).filter(Department.id == department_id).first()
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    department.name = payload.name
    department.description = payload.description
    db.commit()
    return {"message": "Department Updated"}


@router.delete("/{department_id}")
def delete_department(department_id: int, db: Session = Depends(get_db)):
    department = db.query(Department).filter(Department.id == department_id).first()
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    db.delete(department)
    db.commit()
    return {"message": "Department Deleted"}