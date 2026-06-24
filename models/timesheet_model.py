from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from core.base import Base

class Timesheet(Base):
    __tablename__ = "timesheets"

    id = Column(Integer, primary_key=True)
    employee_id = Column( Integer, ForeignKey("employees.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    work_date = Column(Date)
    hours_worked = Column(Float)
    remarks = Column(String(500))