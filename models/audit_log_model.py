from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from core.base import Base

class AuditLog(Base):

    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String(255), nullable=False)
    entity = Column(String(255), nullable=False)
    entity_id = Column(Integer, nullable=True)
    ip_address = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)