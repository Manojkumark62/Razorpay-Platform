from pydantic import BaseModel

class EmployeeReportResponse(BaseModel):
    total_employees: int

class AttendanceReportResponse(BaseModel):
    total_attendance: int

class LeaveReportResponse(BaseModel):
    approved: int
    rejected: int
    pending: int

class InventoryReportResponse(BaseModel):
    total_products: int
    total_stock: int