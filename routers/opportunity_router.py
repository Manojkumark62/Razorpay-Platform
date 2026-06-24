from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from core.permission import require_roles
from models.opportunity_model import Opportunity
from schemas.opportunity_schema import OpportunityCreate

router = APIRouter(prefix="/opportunities", tags=["Opportunities"], dependencies=[Depends(require_roles("ADMIN", "SUPER_ADMIN", "HR", "MANAGER"))])

@router.post("/")
def create_opportunity(payload: OpportunityCreate, db: Session = Depends(get_db)):
    opportunity = Opportunity(**payload.model_dump())
    db.add(opportunity)
    db.commit()
    return {"Info": "Opportunity Created"}

@router.get("/")
def get_opportunities(db: Session = Depends(get_db)):
    return db.query(Opportunity).all()

@router.put("/{opportunity_id}/stage")
def update_stage(opportunity_id: int, stage: str, db: Session = Depends(get_db)):
    opportunity = db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
    opportunity.stage = stage
    db.commit()
    return {"Info": "Stage Updated"}

