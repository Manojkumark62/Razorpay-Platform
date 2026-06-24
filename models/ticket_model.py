from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from datetime import datetime

from core.base import Base

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    created_by = Column(Integer, ForeignKey("users.id"))
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)
    priority = Column(String(50), default="MEDIUM")
    status = Column(String(50), default="OPEN")
    created_at = Column(DateTime, default=datetime.utcnow)