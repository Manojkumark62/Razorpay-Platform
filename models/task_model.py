from sqlalchemy import Column, Integer, String, ForeignKey, Date
from core.base import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    employee_id = Column(Integer, ForeignKey("employees.id"))
    title = Column(String(255))
    description = Column(String(500))
    due_date = Column(Date)
    status = Column(String(50), default="PENDING")