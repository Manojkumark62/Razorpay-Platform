from core.permission import require_roles
from fastapi import Depends, APIRouter

router = APIRouter(prefix="/auth", tags=["Admin"])

@router.get("/admin")
def admin_only(current_user=Depends(require_roles("SUPER_ADMIN"))):
    return {"Info": "Welcome Admin"}