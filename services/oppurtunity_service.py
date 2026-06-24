from sqlalchemy.orm import Session
from models.opportunity_model import Opportunity

def create_opportunity(db: Session, payload):
    opportunity = Opportunity(**payload.model_dump())
    db.add(opportunity)
    db.commit()
    db.refresh(opportunity)
    return opportunity

def get_opportunities(db: Session):
    return db.query(Opportunity).all()

def get_opportunity(db: Session, opportunity_id: int):
    return (db.query(Opportunity).filter(Opportunity.id == opportunity_id).first())

def update_opportunity_stage(db: Session, opportunity_id: int, stage: str):
    opportunity = get_opportunity(db, opportunity_id)
    if not opportunity:
        return None
    opportunity.stage = stage
    db.commit()
    db.refresh(opportunity)
    return opportunity

def pipeline_value(db: Session):
    opportunities = (db.query(Opportunity).all())
    return sum(
        item.value
        for item in opportunities)