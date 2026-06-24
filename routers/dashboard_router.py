from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from core.permission import require_roles
from services.dashboard_service import dashboard_summary, hr_dashboard, inventory_dashboard, project_dashboard, ticket_dashboard
from middlewares.rate_limit import RateLimiter

router = APIRouter(prefix="/dashboard", tags=["Dashboard"], dependencies=[Depends(require_roles("ADMIN", "SUPER_ADMIN", "HR", "MANAGER"))])


@router.get("/summary", dependencies=[Depends(RateLimiter(requests=20, seconds=60))])
def get_dashboard_summary(db: Session = Depends(get_db)):
    return dashboard_summary(db)


@router.get("/hr")
def hr_dashboard_api(db: Session = Depends(get_db)):
    return hr_dashboard(db)


@router.get("/inventory")
def inventory_dashboard_api(db: Session = Depends(get_db)):
    return inventory_dashboard(db)


@router.get("/projects")
def project_dashboard_api(db: Session = Depends(get_db)):
    return project_dashboard(db)


@router.get("/tickets")
def ticket_dashboard_api(db: Session = Depends(get_db)):
    return ticket_dashboard(db)