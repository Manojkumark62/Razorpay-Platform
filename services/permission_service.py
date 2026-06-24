from sqlalchemy.orm import Session
from models.permission_model import Permission
from models.role_permission_model import RolePermission

def create_permission(db: Session, name: str):
    permission = Permission(name=name)
    db.add(permission)
    db.commit()
    db.refresh(permission)
    return permission

def get_permissions(db: Session):
    return db.query(Permission).all()

def assign_permission(db: Session, role_id: int, permission_id: int):
    mapping = RolePermission(role_id=role_id, permission_id=permission_id)
    db.add(mapping)
    db.commit()
    db.refresh(mapping)
    return mapping

def get_role_permissions(db: Session, role_id: int):
    return (db.query(RolePermission).filter(RolePermission.role_id == role_id).all())