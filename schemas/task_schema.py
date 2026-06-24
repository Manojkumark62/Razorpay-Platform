from pydantic import BaseModel
from datetime import date

class TaskCreate(BaseModel):
    project_id: int
    employee_id: int
    title: str
    description: str
    due_date: date