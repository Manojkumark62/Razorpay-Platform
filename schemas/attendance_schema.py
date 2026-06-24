from pydantic import BaseModel

class AttendanceCheckIn(BaseModel):
    employee_id: int

class AttendanceCheckOut(BaseModel):
    employee_id: int