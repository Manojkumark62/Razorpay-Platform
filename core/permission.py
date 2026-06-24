from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from dependencies.dependency import get_current_user
from models.role_permission_model import RolePermission
from models.permission_model import Permission


ROLE_ACCESS_MAP = {
    "/auth": ("EMPLOYEE", "ADMIN", "SUPER_ADMIN"),
    "/admin": ("SUPER_ADMIN",),
    "/department": ("ADMIN", "SUPER_ADMIN", "HR", "MANAGER"),
    "/designation": ("ADMIN", "SUPER_ADMIN", "HR", "MANAGER"),
    "/employee": ("ADMIN", "SUPER_ADMIN", "HR", "MANAGER"),
    "/attendance": ("EMPLOYEE", "ADMIN", "SUPER_ADMIN", "HR", "MANAGER"),
    "/leave": ("EMPLOYEE", "ADMIN", "SUPER_ADMIN", "HR", "MANAGER"),
    "/salary": ("ADMIN", "SUPER_ADMIN", "HR", "MANAGER"),
    "/category": ("ADMIN", "SUPER_ADMIN", "HR", "MANAGER"),
    "/product": ("ADMIN", "SUPER_ADMIN", "HR", "MANAGER"),
    "/supplier": ("ADMIN", "SUPER_ADMIN", "HR", "MANAGER"),
    "/inventory": ("ADMIN", "SUPER_ADMIN", "HR", "MANAGER"),
    "/project": ("ADMIN", "SUPER_ADMIN", "HR", "MANAGER"),
    "/task": ("ADMIN", "SUPER_ADMIN", "HR", "MANAGER"),
    "/timesheet": ("EMPLOYEE", "ADMIN", "SUPER_ADMIN", "HR", "MANAGER"),
    "/client": ("ADMIN", "SUPER_ADMIN", "HR", "MANAGER"),
    "/lead": ("ADMIN", "SUPER_ADMIN", "HR", "MANAGER"),
    "/opportunity": ("ADMIN", "SUPER_ADMIN", "HR", "MANAGER"),
    "/ticket": ("EMPLOYEE", "ADMIN", "SUPER_ADMIN", "HR", "MANAGER"),
    "/notifications": ("EMPLOYEE", "ADMIN", "SUPER_ADMIN", "HR", "MANAGER"),
    "/audit": ("SUPER_ADMIN", "ADMIN"),
    "/report": ("SUPER_ADMIN", "ADMIN", "HR", "MANAGER"),
    "/dashboard": ("SUPER_ADMIN", "ADMIN", "HR", "MANAGER"),
}


def require_roles(*roles):
    def role_checker(current_user=Depends(get_current_user)):
        if current_user.role is None or current_user.role.name not in roles:
            raise HTTPException(status_code=403, detail="Permission denied")
        return current_user
    return role_checker


def require_permission(permission_name: str):
    def checker(
        current_user=Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        permissions = (
            db.query(Permission.name)
            .join(RolePermission, Permission.id == RolePermission.permission_id)
            .filter(RolePermission.role_id == current_user.role_id)
            .all()
        )
        permission_list = [p[0] for p in permissions]
        if permission_name not in permission_list:
            raise HTTPException(status_code=403, detail="Permission denied")
        return current_user
    return checker


def get_access_roles_for_path(path: str):
    normalized_path = path.lower()
    for prefix, roles in sorted(ROLE_ACCESS_MAP.items(), key=lambda item: len(item[0]), reverse=True):
        if normalized_path == prefix or normalized_path.startswith(prefix + "/"):
            return roles
    return None


def attach_role_access_docs(app):
    for route in app.routes:
        path = getattr(route, "path", None)
        if not path:
            continue
        roles = get_access_roles_for_path(path)
        if not roles:
            continue
        existing_description = getattr(route, "description", "") or ""
        marker = "Accessible by:"
        if marker not in existing_description:
            route.description = (
                f"{existing_description}\n\n{marker} {', '.join(roles)}".strip()
            )