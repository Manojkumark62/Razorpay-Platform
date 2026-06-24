from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import Base, engine
from core.exceptions import ERPException, erp_exception_handler

# Routers
from routers.auth_router import router as auth_router
from routers.department_router import router as department_router
from routers.designation_router import router as designation_router
from routers.employee_router import router as employee_router
from routers.attendance_router import router as attendance_router
from routers.leave_router import router as leave_router
from routers.salary_router import router as salary_router
from routers.category_router import router as category_router
from routers.product_router import router as product_router
from routers.supplier_router import router as supplier_router
from routers.inventory_router import router as inventory_router
from routers.project_router import router as project_router
from routers.task_router import router as task_router
from routers.timesheet_router import router as timesheet_router
from routers.client_router import router as client_router
from routers.lead_router import router as lead_router
from routers.opportunity_router import router as opportunity_router
from routers.ticket_router import router as ticket_router
from routers.notification_router import router as notification_router
from routers.audit_log_router import router as audit_router
from routers.report_router import router as report_router
from routers.dashboard_router import router as dashboard_router
from middlewares.audit_middleware import AuditMiddleware
from core.permission import attach_role_access_docs

# Create all tables
Base.metadata.create_all(bind=engine)

tags_metadata = [
    {"name": "Authentication", "description": "Authentication & Authorization APIs"},
    {"name": "Departments", "description": "Department Management"},
    {"name": "Designations", "description": "Designation Management"},
    {"name": "Employees", "description": "Employee Management"},
    {"name": "Attendance", "description": "Attendance Management"},
    {"name": "Leaves", "description": "Leave Management"},
    {"name": "Payroll", "description": "Payroll & Salary Management"},
    {"name": "Categories", "description": "Product Category Management"},
    {"name": "Products", "description": "Product Management"},
    {"name": "Suppliers", "description": "Supplier Management"},
    {"name": "Inventory", "description": "Inventory Management"},
    {"name": "Projects", "description": "Project Management"},
    {"name": "Tasks", "description": "Task Management"},
    {"name": "Timesheets", "description": "Timesheet Management"},
    {"name": "Clients", "description": "Client Management"},
    {"name": "Leads", "description": "Lead Management"},
    {"name": "Opportunities", "description": "Opportunity Management"},
    {"name": "Support Tickets", "description": "Support Ticket System"},
    {"name": "Notifications", "description": "Notification System"},
    {"name": "Audit", "description": "Audit Logs"},
    {"name": "Reports", "description": "Reporting APIs"},
    {"name": "Dashboard", "description": "Dashboard Summary APIs"},
]

app = FastAPI(
    title="Employee Platform ERP",
    version="1.0.0",
    description="""
    Enterprise Resource Planning System""",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=tags_metadata,
)

# Register custom exception handler
app.add_exception_handler(ERPException, erp_exception_handler)

# Audit middleware (must come before CORS)
app.add_middleware(AuditMiddleware)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(auth_router)
app.include_router(department_router)
app.include_router(designation_router)
app.include_router(employee_router)
app.include_router(attendance_router)
app.include_router(leave_router)
app.include_router(salary_router)
app.include_router(category_router)
app.include_router(product_router)
app.include_router(supplier_router)
app.include_router(inventory_router)
app.include_router(project_router)
app.include_router(task_router)
app.include_router(timesheet_router)
app.include_router(client_router)
app.include_router(lead_router)
app.include_router(opportunity_router)
app.include_router(ticket_router)
app.include_router(notification_router)
app.include_router(audit_router)
app.include_router(report_router)
app.include_router(dashboard_router)
attach_role_access_docs(app)


@app.get("/", tags=["Health"])
def health_check():
    return {"message": "ERP API Running Successfully", "version": "1.0.0"}


@app.get("/ping", tags=["Health"])
def ping():
    return {"status": "success", "message": "pong"}