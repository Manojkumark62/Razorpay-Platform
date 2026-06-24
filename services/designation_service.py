from sqlalchemy.orm import Session
from models.designation_model import Designation

def create_designation(db: Session, name: str, description: str = None):
    designation = Designation(title=name, description=description)
    db.add(designation)
    db.commit()
    db.refresh(designation)
    return designation

def get_designations(db: Session):
    return db.query(Designation).all()

def get_designation(db: Session, designation_id: int):
    return (db.query(Designation).filter(Designation.id == designation_id).first())

def update_designation(db: Session, designation_id: int, data):
    designation = get_designation(db, designation_id)
    if not designation:
        return None
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(designation, key, value)
    db.commit()
    db.refresh(designation)
    return designation

def delete_designation(db: Session, designation_id: int):
    designation = get_designation(db, designation_id)
    if not designation:
        return False
    db.delete(designation)
    db.commit()
    return True