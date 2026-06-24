from sqlalchemy import Column, Integer, String, Float, ForeignKey
from core.base import Base

class Opportunity(Base):
    __tablename__ = "opportunities"

    id = Column(Integer, primary_key=True)
    lead_id = Column(Integer, ForeignKey("leads.id"))
    title = Column(String(255))
    value = Column(Float)
    stage = Column(String(50), default="PROSPECTING")