from sqlalchemy.orm import Session
from models.lead_model import Lead

def create_lead(db: Session, payload):
    lead = Lead(**payload.model_dump())
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead

def get_leads(db: Session):
    return db.query(Lead).all()

def get_lead(db: Session, lead_id: int):
    return (db.query(Lead).filter(Lead.id == lead_id).first())

def update_lead_status(db: Session, lead_id: int, status: str):
    lead = get_lead(db, lead_id)
    if not lead:
        return None
    lead.status = status
    db.commit()
    db.refresh(lead)
    return lead