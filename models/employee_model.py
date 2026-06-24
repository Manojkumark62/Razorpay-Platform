from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from core.base_model import BaseModel

class Employee(BaseModel):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    employee_code = Column(String(50), unique=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(255), unique=True)
    phone = Column(String(20))
    gender = Column(String(20))
    joining_date = Column(Date)
    department_id = Column(Integer, ForeignKey("departments.id"))
    designation_id = Column(Integer, ForeignKey("designations.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    department = relationship("Department")
    designation = relationship("Designation")