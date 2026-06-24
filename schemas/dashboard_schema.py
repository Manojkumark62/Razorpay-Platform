from pydantic import BaseModel

class DashboardSummary(BaseModel):
    employees: int
    projects: int
    tasks: int
    tickets: int
    leave_requests: int