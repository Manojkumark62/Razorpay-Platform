from sqlalchemy import func
from models.employee_model import Employee
from models.attendance_model import Attendance
from models.leave_model import LeaveRequest
from models.inventory_model import Inventory

def employee_report(db):
    return {"total_employees":db.query(Employee).count()}

def attendance_report(db):
    return {"total_attendance":db.query(Attendance).count()}

def leave_report(db):
    approved = (db.query(LeaveRequest).filter(LeaveRequest.status == "APPROVED").count())
    rejected = (db.query(LeaveRequest).filter(LeaveRequest.status == "REJECTED").count())
    pending = (db.query(LeaveRequest).filter(LeaveRequest.status == "PENDING").count())
    return {"approved": approved, "rejected": rejected, "pending": pending}

def inventory_report(db):
    inventory = (db.query(Inventory).all())
    return {
        "total_products":
        len(inventory),

        "total_stock":
        sum(item.quantity
            for item in inventory)}