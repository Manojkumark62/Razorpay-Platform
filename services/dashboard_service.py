from models.employee_model import Employee
from models.attendance_model import Attendance
from models.leave_model import LeaveRequest
from models.inventory_model import Inventory
from models.project_model import Project
from models.task_model import Task
from models.ticket_model import Ticket


def dashboard_summary(db):
    # FIX: function was missing from original, dashboard_router imported it
    return {
        "employees": db.query(Employee).count(),
        "projects": db.query(Project).count(),
        "tasks": db.query(Task).count(),
        "tickets": db.query(Ticket).count(),
        "leave_requests": db.query(LeaveRequest).count(),
    }


def hr_dashboard(db):
    return {
        "employees": db.query(Employee).count(),
        "attendance": db.query(Attendance).count(),
        "leave_requests": db.query(LeaveRequest).count(),
    }


def inventory_dashboard(db):
    inventory = db.query(Inventory).all()
    return {
        "products": len(inventory),
        "stock": sum(item.quantity for item in inventory),
    }


def project_dashboard(db):
    return {
        "projects": db.query(Project).count(),
        "tasks": db.query(Task).count(),
    }


def ticket_dashboard(db):
    return {
        "tickets": db.query(Ticket).count(),
        "open": db.query(Ticket).filter(Ticket.status == "OPEN").count(),
        "closed": db.query(Ticket).filter(Ticket.status == "CLOSED").count(),
    }