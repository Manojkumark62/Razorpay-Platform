from pydantic import BaseModel
from datetime import date

class EmployeeCreate(BaseModel):
    employee_code: str
    first_name: str
    last_name: str
    email: str
    phone: str
    gender: str
    joining_date: date
    department_id: int
    designation_id: int
    user_id: int