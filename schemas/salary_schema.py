from pydantic import BaseModel

class SalaryStructureCreate(BaseModel):

    employee_id: int
    basic_salary: float
    hra: float
    allowances: float
    deductions: float