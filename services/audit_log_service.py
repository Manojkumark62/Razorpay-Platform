from models.audit_log_model import AuditLog


def _serialize_audit_log(log):
    return {
        "id": log.id,
        "user_id": log.user_id,
        "action": log.action,
        "entity": log.entity,
        "entity_id": log.entity_id,
        "ip_address": log.ip_address,
        "created_at": log.created_at.isoformat() if log.created_at else None,
    }


def create_audit_log(db, user_id, action, entity, entity_id):
    audit = AuditLog(user_id=user_id, action=action, entity=entity, entity_id=entity_id)
    db.add(audit)
    db.commit()
    return _serialize_audit_log(audit)


def get_audit_logs(db):
    logs = db.query(AuditLog).all()
    return [_serialize_audit_log(log) for log in logs]


def user_audit_logs(db, user_id):
    logs = db.query(AuditLog).filter(AuditLog.user_id == user_id).all()
    return [_serialize_audit_log(log) for log in logs]