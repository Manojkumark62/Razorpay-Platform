from sqlalchemy import Column, Integer, String
from core.base import Base

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True)
    client_name = Column(String(255))
    email = Column(String(255))
    phone = Column(String(20))
    source = Column(String(100))
    status = Column(String(50), default="NEW")