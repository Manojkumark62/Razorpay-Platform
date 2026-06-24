from sqlalchemy import Column, Integer, String, Date, ForeignKey
from core.base import Base

class LeaveRequest(Base):
    __tablename__ = "leave_requests"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    leave_type = Column(String(100))
    start_date = Column(Date)
    end_date = Column(Date)
    reason = Column(String(500))
    status = Column(String(50), default="PENDING")