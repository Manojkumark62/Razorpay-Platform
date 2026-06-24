from sqlalchemy import Column, Integer, String, Date
from core.base import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    description = Column(String(500))
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(String(50), default="PLANNED")