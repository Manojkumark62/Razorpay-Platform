from sqlalchemy import Column, Integer, String
from core.base import Base

class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(255))
    phone = Column(String(20))
    address = Column(String(500))