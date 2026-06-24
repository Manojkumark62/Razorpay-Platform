from sqlalchemy import Column, Integer, Float, ForeignKey, Date
from core.base import Base

class Payroll(Base):
    __tablename__ = "payrolls"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    payroll_month = Column(Date)
    gross_salary = Column(Float)
    total_deductions = Column(Float)
    net_salary = Column(Float)