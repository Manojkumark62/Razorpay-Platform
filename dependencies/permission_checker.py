from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from dependencies.dependency import get_current_user
from models.role_permission_model import RolePermission
from models.user_model import User


def permission_required(permission_id: int):
    def checker(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        permission = (
            db.query(RolePermission)
            .filter(
                RolePermission.role_id == current_user.role_id,
                RolePermission.permission_id == permission_id,
            )
            .first()
        )
        if not permission:
            raise HTTPException(status_code=403, detail="Permission Denied")
        return current_user
    return checker