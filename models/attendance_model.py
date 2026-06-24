from sqlalchemy import Column, Integer, ForeignKey, Date, DateTime, String
from core.base import Base

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    attendance_date = Column(Date)
    check_in = Column(DateTime)
    check_out = Column(DateTime)
    status = Column(String(50), default="PRESENT")