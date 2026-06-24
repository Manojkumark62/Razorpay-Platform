from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from core.permission import require_roles
from models.supplier_model import Supplier
from schemas.supplier_schema import SupplierCreate

router = APIRouter(prefix="/suppliers", tags=["Suppliers"], dependencies=[Depends(require_roles("ADMIN", "SUPER_ADMIN", "HR", "MANAGER"))])

@router.post("/")
def create_supplier(payload: SupplierCreate, db: Session = Depends(get_db)):
    supplier = Supplier(**payload.model_dump())
    db.add(supplier)
    db.commit()
    return {"Info": "Supplier Created"}

@router.get("/")
def get_suppliers(db: Session = Depends(get_db)):
    return db.query(Supplier).all()