from pydantic import BaseModel
from datetime import date

class TimesheetCreate(BaseModel):
    employee_id: int
    project_id: int
    work_date: date
    hours_worked: float
    remarks: str