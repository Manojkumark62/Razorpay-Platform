from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from core.permission import require_roles
from models.lead_model import Lead
from models.client_model import Client
from schemas.lead_schema import LeadCreate

router = APIRouter(prefix="/leads", tags=["Leads"], dependencies=[Depends(require_roles("ADMIN", "SUPER_ADMIN", "HR", "MANAGER"))])


@router.post("/")
def create_lead(payload: LeadCreate, db: Session = Depends(get_db)):
    lead = Lead(**payload.model_dump())
    db.add(lead)
    db.commit()
    return {"message": "Lead Created", "id": lead.id}


@router.get("/")
def get_leads(db: Session = Depends(get_db)):
    return db.query(Lead).filter(Lead.status != "CONVERTED", Lead.status != "WON").all()


@router.get("/{lead_id}")
def get_lead(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead


@router.put("/{lead_id}/status")
def update_lead_status(lead_id: int, status: str, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    lead.status = status
    db.commit()
    return {"message": "Lead Updated"}


@router.post("/{lead_id}/convert")
def convert_lead(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    client = Client(
        company_name=lead.client_name,
        contact_person=lead.client_name,
        email=lead.email,
        phone=lead.phone,
    )
    db.add(client)
    lead.status = "CONVERTED"
    db.commit()
    return {"message": "Lead Converted to Client", "client_id": client.id}