from sqlalchemy import Column, Integer, Float, ForeignKey
from core.base import Base

class SalaryStructure(Base):
    __tablename__ = "salary_structures"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), unique=True)
    basic_salary = Column(Float)
    hra = Column(Float)
    allowances = Column(Float)
    deductions = Column(Float)