from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from core.permission import require_roles
from core.response import success_response
from models.designation_model import Designation
from schemas.designation_schema import DesignationCreate

router = APIRouter(prefix="/designations", tags=["Designations"], dependencies=[Depends(require_roles("ADMIN", "SUPER_ADMIN", "HR", "MANAGER"))])

@router.post("/")
def create_designation(payload: DesignationCreate, db: Session = Depends(get_db)):
    designation = Designation(title=payload.title, description=payload.description)
    db.add(designation)
    db.commit()
    db.refresh(designation)
    return success_response(
        "Designation created successfully",
        {
            "id": designation.id,
            "title": designation.title,
            "description": designation.description,
        },
    )

@router.get("/")
def get_dsignations(db: Session = Depends(get_db)):
    designations = db.query(Designation).all()
    return success_response(
        "Designations retrieved successfully",
        [
            {
                "id": item.id,
                "title": item.title,
                "description": item.description,
            }
            for item in designations
        ],
    )

@router.get("/{designation_id}")
def get_designation(designation_id: int, db: Session = Depends(get_db)):
    designation = db.query(Designation).filter(Designation.id == designation_id).first()
    if not designation:
        return success_response("Designation not found", None)
    return success_response(
        "Designation retrieved successfully",
        {
            "id": designation.id,
            "title": designation.title,
            "description": designation.description,
        },
    )

@router.delete("/{designation_id}")
def delete_designation(designation_id: int, db: Session = Depends(get_db)):
    designation = db.query(Designation).filter(Designation.id == designation_id).first()
    if not designation:
        return success_response("Designation not found", None)
    db.delete(designation)
    db.commit()
    return success_response("Designation deleted successfully", {"id": designation_id})