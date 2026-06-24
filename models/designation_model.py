from sqlalchemy import Column, Integer, String
from core.base import Base

class Designation(Base):
    __tablename__ = "designations"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), unique=True, nullable=False)
    description = Column(String(255))