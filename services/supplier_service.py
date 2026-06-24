from sqlalchemy.orm import Session
from models.supplier_model import Supplier

def create_supplier(db: Session, payload):
    supplier = Supplier(**payload.model_dump())
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    return supplier

def get_supplier(db: Session, supplier_id: int):
    return (db.query(Supplier).filter(Supplier.id == supplier_id).first())

def get_suppliers(db: Session):
    return (db.query(Supplier).all())

def update_supplier(db: Session, supplier_id: int, payload):
    supplier = get_supplier(db, supplier_id)
    if not supplier:
        return None
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(supplier, key, value)
    db.commit()
    db.refresh(supplier)
    return supplier

def delete_supplier(db: Session, supplier_id: int):
    supplier = get_supplier(db, supplier_id)
    if not supplier:
        return False
    db.delete(supplier)
    db.commit()
    return True