from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from core.permission import require_roles
from core.response import success_response
from services.audit_log_service import get_audit_logs, user_audit_logs

router = APIRouter(prefix="/audit", tags=["Audit"], dependencies=[Depends(require_roles("ADMIN", "SUPER_ADMIN"))])

@router.get("/")
def get_logs(db: Session = Depends(get_db)):
    logs = get_audit_logs(db)
    return success_response("Audit logs fetched successfully", logs)

@router.get("/user/{user_id}")
def get_user_logs(user_id: int, db: Session = Depends(get_db)):
    logs = user_audit_logs(db, user_id)
    return success_response("User audit logs fetched successfully", logs)